"""
app/services/content/lesson_blocks.py

A lesson body is Markdown with one extra construct: a *figure marker* on a line
of its own,

    {{figure:lora-low-rank-adaptation}}

which says "render this image HERE". The marker names a stable asset key (see
`course_assets`), never a file path or a URL, so a lesson does not change when
the files move from the course folder to object storage.

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
    which is what makes lessons without figures render as they always did.

Pure functions, no database and no I/O.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Union

# Keys are lowercase words joined by hyphens: URL-safe, unambiguous, and easy to
# validate without a lookup.
KEY_PATTERN = r"[a-z0-9]+(?:-[a-z0-9]+)*"
_KEY = re.compile(rf"^{KEY_PATTERN}$")
_MARKER_LINE = re.compile(rf"^[ \t]*\{{\{{figure:({KEY_PATTERN})\}}\}}[ \t]*$")
# Anything that looks like an attempt at a marker, valid or not.
_ANY_MARKER = re.compile(r"\{\{\s*figure\b[^}\n]*\}\}?", re.IGNORECASE)
_FENCE = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")


@dataclass(frozen=True)
class TextBlock:
    content: str


@dataclass(frozen=True)
class FigureBlock:
    key: str


Block = Union[TextBlock, FigureBlock]


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


def split_lesson(text: str) -> List[Block]:
    """The lesson as ordered blocks. Never returns an empty list for a non-empty
    body; a body that is empty or only blank yields `[]`."""
    blocks: List[Block] = []
    pending: List[str] = []

    def flush() -> None:
        chunk = "".join(pending).strip("\n")
        if chunk.strip():
            blocks.append(TextBlock(chunk))
        pending.clear()

    for line, in_code in _lines_outside_code(text or ""):
        marker = None if in_code else _MARKER_LINE.match(line.rstrip("\r\n"))
        if marker:
            flush()
            blocks.append(FigureBlock(marker.group(1)))
        else:
            pending.append(line)
    flush()
    return blocks


def has_figures(text: str) -> bool:
    return any(isinstance(b, FigureBlock) for b in split_lesson(text))


def figure_keys(text: str) -> List[str]:
    """Every figure key the body places, in order (repeats kept)."""
    return [b.key for b in split_lesson(text) if isinstance(b, FigureBlock)]


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
