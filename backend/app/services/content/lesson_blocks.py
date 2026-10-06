"""
app/services/content/lesson_blocks.py

A lesson body is Markdown with one extra construct: a *figure marker* on a line
of its own,

    {{image:lora-low-rank-adaptation}}
    {{image:lora-low-rank-adaptation|Only the small matrices are trained.}}

which says "render this image HERE" (the optional text after `|` is a caption for
this occurrence, overriding the manifest's). `{{figure:key}}` is the same marker under
its first name and is still accepted. The marker names a stable asset key (see
`course_assets`), never a file path or a URL, so a lesson does not change when
the files move from the course folder to object storage.

Two more constructs are authoring syntax, never learner content:

    {{exercise:M01.L02.EX04}}        where the author wants that lesson exercise to come up
    [[IMAGE_NEEDED: title | what the figure shows | what to notice]]
                                      the image does NOT exist yet

An exercise marker names one of the lesson's own exercises by its authored id. The exercises themselves are
rendered by the lesson page in its exercise section (paired to the lesson by `lesson_id`), so the marker is
source/import metadata: it is parsed into an `ExerciseBlock` here, validated against the lesson's exercises
by the curriculum validator, and left out of what a learner reads. An `IMAGE_NEEDED` marker is parsed into an
`AuthorMarkerBlock`; whether anyone sees it is the caller's decision (an author in development may, a learner
never). Neither marker is removed from the stored Markdown: validators, `seeds/link_images.py` and the status
tools still read them there.

This module is the only place that knows the syntax. It splits a body into the
ordered blocks a client renders one after the other:

    [TextBlock("LoRA decomposes ..."), FigureBlock("lora-low-rank-adaptation"), TextBlock("The original ...")]

Rules, all of them about not surprising an author:

  * a marker is recognised only on a line by itself (indentation and trailing
    spaces are ignored) - a marker in the middle of a sentence is reported by
    `malformed_markers`, not silently kept as text;
  * a marker inside a fenced code block is code, not a figure - a lesson may
    legitimately *show* the syntax;
  * the surrounding Markdown is preserved byte for byte, apart from the blank
    lines that separated it from the marker;
  * a body with no marker yields exactly one `TextBlock` holding it unchanged,
    which is what makes lessons without figures render as they always did;
  * authoring syntax that is NOT on a line of its own (an inline `{{exercise:..}}`, a request with prose
    after it, a misspelt image marker) is cut out of the text blocks, so a typo cannot reach a learner;
    the same syntax inside a fenced block or an inline code span is a lesson *showing* it and is kept.

Pure functions, no database and no I/O.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

# Keys are lowercase words joined by hyphens: URL-safe, unambiguous, and easy to
# validate without a lookup.
KEY_PATTERN = r"[a-z0-9]+(?:-[a-z0-9]+)*"
_KEY = re.compile(rf"^{KEY_PATTERN}$")
# `{{image:key}}` / `{{image:key|caption}}` (and the older `{{figure:...}}`). A caption is any
# text without braces or line breaks; an empty one (`{{image:key|}}`) is a typo, not a caption.
_MARKER_LINE = re.compile(
    rf"^[ \t]*\{{\{{(?:image|figure):({KEY_PATTERN})(?:\|([^{{}}\n]*[^{{}}\s][^{{}}\n]*))?\}}\}}[ \t]*$")
# Anything that looks like an attempt at a marker, valid or not. `image` must be followed by
# `:`, `|` or `}` (after optional spaces) so prose like `{{ image_url }}` is not taken for one.
_ANY_MARKER = re.compile(r"\{\{\s*(?:figure\b|image\s*[:|}])[^}\n]*\}?\}?", re.IGNORECASE)
_FENCE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")

# `{{exercise:M01.L02.EX04}}` on a line of its own. Ids are what the course author wrote: letters, digits,
# dots, hyphens and underscores.
EXERCISE_ID_PATTERN = r"[A-Za-z0-9][A-Za-z0-9._-]*"
_EXERCISE_LINE = re.compile(rf"^[ \t]*\{{\{{exercise:({EXERCISE_ID_PATTERN})\}}\}}[ \t]*$")
_ANY_EXERCISE = re.compile(r"\{\{\s*exercise\b[^}\n]*\}?\}?", re.IGNORECASE)
# `[[IMAGE_NEEDED: ...]]`; a request may hold bracketed text (`[CLS]`, `[1, 4, 384]`) and may wrap over lines.
IMAGE_REQUEST_PATTERN = r"\[\[IMAGE_NEEDED(?:[^\[\]]|\[[^\[\]\n]*\])*\]\]"
_IMAGE_REQUEST = re.compile(IMAGE_REQUEST_PATTERN)
_UNCLOSED_REQUEST = re.compile(r"\[\[IMAGE_NEEDED[^\n]*")
_REQUEST_START = "[[IMAGE_NEEDED"
_MAX_REQUEST_LINES = 12
# Source/course bookkeeping is useful in authored files and validation, but is
# not lesson prose.  Match only a complete metadata-labelled line, in either
# authored language; ordinary blockquotes and uses of these words are kept.
_AUTHORING_METADATA_LINE = re.compile(
    r"^[ \t]*(?:>\s*)?(?:\*\*)?"
    r"(?:Course|Lesson|Module|Source alignment|المقرر|الدرس|الوحدة|مواءمة المصدر)"
    r":(?:\*\*)?[^\r\n]*$",
    re.IGNORECASE | re.MULTILINE,
)
# Quick test: is there anything here the stripping below could touch?
_AUTHORING_HINT = re.compile(
    r"\{\{\s*(?:image|figure|exercise)\b|\[\[IMAGE_NEEDED|"
    r"^[ \t]*(?:>\s*)?(?:\*\*)?(?:Course|Lesson|Module|Source alignment|المقرر|الدرس|الوحدة|مواءمة المصدر):",
    re.IGNORECASE | re.MULTILINE,
)
_CODE_SPAN = re.compile(r"(?<!`)(`+)(?!`)(.+?)(?<!`)\1(?!`)", re.DOTALL)


@dataclass(frozen=True)
class TextBlock:
    content: str


@dataclass(frozen=True)
class FigureBlock:
    key: str
    # Caption written at this spot in the lesson; overrides the manifest's for this occurrence.
    caption: Optional[str] = None


@dataclass(frozen=True)
class ExerciseBlock:
    """`{{exercise:ID}}` - where the author wants the lesson's exercise ID to come up."""
    exercise_id: str


@dataclass(frozen=True)
class AuthorMarkerBlock:
    """An authoring placeholder that is not learner content. `text` is what follows `IMAGE_NEEDED:`, the
    fields separated by `|` (title, what the figure shows, what to notice)."""
    kind: str
    text: str

    @property
    def title(self) -> str:
        return self.text.split("|", 1)[0].strip()


Block = Union[TextBlock, FigureBlock, ExerciseBlock, AuthorMarkerBlock]


def is_valid_key(key: str) -> bool:
    return bool(_KEY.match(key)) and len(key) <= 120


def _lines_outside_code(text: str):
    """(line, in_code) for every line of `text`, keeping line endings."""
    fence = None  # the opening fence: (character, length)
    for line in text.splitlines(keepends=True):
        opener = _FENCE.match(line)
        if fence is None:
            in_code = False
            if opener:
                fence = (opener.group(1)[0], len(opener.group(1)))
                in_code = True
        else:
            in_code = True
            if opener and opener.group(1)[0] == fence[0] and len(opener.group(1)) >= fence[1] \
                    and not line.strip().strip(fence[0]):
                fence = None
        yield line, in_code


def _request_text(marker: str) -> str:
    return marker[len(_REQUEST_START):-2].lstrip(":").strip()


def _own_line_request(lines: List[Tuple[str, bool]], i: int) -> Optional[Tuple[str, int]]:
    """(the marker, index of its last line) when the lines from `i` hold an `[[IMAGE_NEEDED ...]]` that fills
    whole lines, else None (not a request at all, or one with prose around it)."""
    chunk = lines[i][0].lstrip()
    if not chunk.startswith(_REQUEST_START):
        return None
    j = i
    while True:
        found = _IMAGE_REQUEST.match(chunk)
        if found:
            return (found.group(0), j) if not chunk[found.end():].strip() else None
        j += 1
        if j >= len(lines) or lines[j][1] or j - i >= _MAX_REQUEST_LINES:
            return None
        chunk += lines[j][0]


def _strip_segment(text: str) -> str:
    """Cut authoring syntax out of prose (no fenced code in it), keeping inline code spans as they are."""
    spans: List[str] = []

    def keep(match: "re.Match[str]") -> str:
        spans.append(match.group(0))
        return f"\x00{len(spans) - 1}\x00"

    text = _CODE_SPAN.sub(keep, text)
    for pattern in (_IMAGE_REQUEST, _UNCLOSED_REQUEST, _ANY_MARKER, _ANY_EXERCISE, _AUTHORING_METADATA_LINE):
        text = pattern.sub("", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: spans[int(m.group(1))], text)


def has_authoring_syntax(text: Optional[str]) -> bool:
    """True when the body contains anything this module treats as authoring syntax."""
    return bool(text) and bool(_AUTHORING_HINT.search(text))


def strip_authoring(text: str) -> str:
    """`text` with every piece of authoring syntax that is not inside code removed. Text without any is
    returned unchanged, character for character."""
    if not text or not _AUTHORING_HINT.search(text):
        return text
    out: List[str] = []
    run: List[str] = []

    def close() -> None:
        if run:
            out.append(_strip_segment("".join(run)))
            run.clear()

    for line, in_code in _lines_outside_code(text):
        if in_code:
            close()
            out.append(line)
        else:
            run.append(line)
    close()
    return "".join(out)


def learner_markdown(text: Optional[str]) -> Optional[str]:
    """`text` as learner-facing Markdown: every authoring line (`{{image:..}}`, `{{figure:..}}`, `{{exercise:..}}`,
    `[[IMAGE_NEEDED: ..]]`) is dropped, together with the one blank line that separated it from its neighbour, and any
    authoring syntax left inside prose is cut out (see `strip_authoring`). Fenced code and inline code are kept as
    written, and so is every other character: a body with no authoring syntax is returned unchanged.

    This is a serialization of the stored body for clients that read `content`; it is not what the lesson page renders
    (that is `split_lesson`'s blocks), and the stored Markdown is never modified."""
    if not has_authoring_syntax(text):
        return text
    lines = list(_lines_outside_code(text or ""))
    out: List[str] = []
    i = 0
    while i < len(lines):
        line, in_code = lines[i]
        dropped_to = None
        if not in_code:
            bare = line.rstrip("\r\n")
            if _MARKER_LINE.match(bare) or _EXERCISE_LINE.match(bare) or _AUTHORING_METADATA_LINE.match(bare):
                dropped_to = i
            else:
                request = _own_line_request(lines, i)
                if request:
                    dropped_to = request[1]
        if dropped_to is None:
            out.append(line)
            i += 1
            continue
        i = dropped_to + 1
        # `a`, blank, MARKER, blank, `b`  ->  `a`, blank, `b`   (and a marker at the very top leaves no leading blank)
        blank_before = not out or not out[-1].strip()
        if blank_before:
            while i < len(lines) and not lines[i][1] and not lines[i][0].strip():
                i += 1
                if out:
                    break
    return strip_authoring("".join(out))


def split_lesson(text: str) -> List[Block]:
    """The lesson as ordered blocks. Never returns an empty list for a non-empty
    body; a body that is empty or only blank yields `[]`."""
    blocks: List[Block] = []
    pending: List[str] = []

    def flush() -> None:
        chunk = strip_authoring("".join(pending).strip("\n"))
        if chunk.strip():
            blocks.append(TextBlock(chunk))
        pending.clear()

    lines = list(_lines_outside_code(text or ""))
    i = 0
    while i < len(lines):
        line, in_code = lines[i]
        if not in_code:
            bare = line.rstrip("\r\n")
            figure = _MARKER_LINE.match(bare)
            if figure:
                flush()
                blocks.append(FigureBlock(figure.group(1), (figure.group(2) or '').strip() or None))
                i += 1
                continue
            exercise = _EXERCISE_LINE.match(bare)
            if exercise:
                flush()
                blocks.append(ExerciseBlock(exercise.group(1)))
                i += 1
                continue
            request = _own_line_request(lines, i)
            if request:
                flush()
                blocks.append(AuthorMarkerBlock("image_needed", _request_text(request[0])))
                i = request[1] + 1
                continue
        pending.append(line)
        i += 1
    flush()
    return blocks


def has_figures(text: str) -> bool:
    return any(isinstance(b, FigureBlock) for b in split_lesson(text))


def figure_keys(text: str) -> List[str]:
    """Every figure key the body places, in order (repeats kept)."""
    return [b.key for b in split_lesson(text) if isinstance(b, FigureBlock)]


def exercise_ids(text: str) -> List[str]:
    """Every exercise id the body points at with `{{exercise:ID}}`, in order (repeats kept)."""
    return [b.exercise_id for b in split_lesson(text) if isinstance(b, ExerciseBlock)]


def author_markers(text: str) -> List[AuthorMarkerBlock]:
    """The unresolved `[[IMAGE_NEEDED]]` requests that stand on lines of their own, in order."""
    return [b for b in split_lesson(text) if isinstance(b, AuthorMarkerBlock)]


def malformed_exercise_markers(text: str) -> List[str]:
    """Text outside code that looks like an exercise marker but is not a valid one on its own line
    (inline, a missing brace, an id with spaces). Reported so it is fixed, not left to be cut out silently."""
    found: List[str] = []
    for line, in_code in _lines_outside_code(text or ""):
        if in_code or _EXERCISE_LINE.match(line.rstrip("\r\n")):
            continue
        if _ANY_EXERCISE.search(_CODE_SPAN.sub("", line)):
            found.append(line.strip()[:120])
    return found


def malformed_markers(text: str) -> List[str]:
    """Text outside code that looks like a figure marker but is not a valid one on
    its own line: an inline marker, a misspelt key, a missing brace. Reported so a
    typo cannot leave `{{figure:...}}` showing in front of a learner."""
    found: List[str] = []
    for line, in_code in _lines_outside_code(text or ""):
        if in_code or not _ANY_MARKER.search(line):
            continue
        if _MARKER_LINE.match(line.rstrip("\r\n")):
            continue
        found.append(line.strip()[:120])
    return found


# An anchor with nothing inside it: `<a id="x"></a>`, `<a name='x' ></a>`, `<a id="x">\n</a>`, or the
# same written as HTML entities. It only defines an old fragment target, which the lesson renderer
# neither draws nor links to. Real links (`<a href=...>text</a>`) carry text and never match.
_EMPTY_ANCHOR = re.compile(
    r"<a\s[^<>]*?\b(?:id|name)\s*=[^<>]*>\s*</a\s*>"
    r"|&lt;a\s[^<>]*?\b(?:id|name)\s*=.*?&gt;\s*&lt;/a\s*&gt;",
    re.IGNORECASE,
)


def empty_anchors(text: str) -> List[Tuple[int, str]]:
    """(line number, tag) for every empty `<a id>` / `<a name>` anchor outside code. These come from
    book/Markdown extraction and are not learner-facing content. One inside a fenced block or an
    inline code span is a lesson *showing* the syntax, so it is left alone."""
    text = text or ""
    code_spans: List[Tuple[int, int]] = []
    pos = 0
    for line, in_code in _lines_outside_code(text):
        if in_code:
            code_spans.append((pos, pos + len(line)))
        pos += len(line)
    found: List[Tuple[int, str]] = []
    for m in _EMPTY_ANCHOR.finditer(text):
        if any(start <= m.start() < end for start, end in code_spans):
            continue
        if text.count("`", text.rfind("\n", 0, m.start()) + 1, m.start()) % 2:
            continue  # inside an inline code span
        found.append((text.count("\n", 0, m.start()) + 1, " ".join(m.group(0).split())[:120]))
    return found
