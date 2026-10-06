"""
app/services/language/arabic_review.py

The checks every Arabic draft of a lesson must pass, whoever or whatever wrote it.

They began life in seeds/generate_arabic_lessons.py (which still imports them from here, so its
callers are unchanged) and moved here so the course importer can hold Arabic text written by
hand, by a model or by a translator to the same bar:

  * executable code is never translated - it is swapped for a placeholder before drafting and put
    back afterwards, and a code block that is not byte-identical is a hard failure;
  * a fenced block is learner-facing TEXT (a ``text`` diagram, a formula, a worked example, a list of
    labels) or CODE, decided by its info string (`TEXT_INFO`). Text blocks are part of the
    explanation and ARE translated - keeping their layout, arrows and operators, numbers and
    identifiers - and a text block with English words that was left without any Arabic is a hard
    failure; so is a line of prose or a table cell left in English;
  * a term the lesson teaches must still be in Latin script (see `terminology_problems`);
  * a draft cut short, empty, or with no Arabic in it is rejected.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List

from app.content import terminology as T

FENCE = re.compile(r"```[\w+-]*\n.*?```", re.DOTALL)
FENCE_BODY = re.compile(r"```[\w+-]*\n(.*?)```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]+`")

# Code is removed from the text before it is sent and put back afterwards.
# Asking a model to "reproduce this exactly" is a request it will sometimes
# decline: gpt-4o-mini rewrote 7 of 17 blocks in the first real run — mostly
# translating comments, which is exactly the failure that silently teaches a
# student something wrong. A placeholder cannot be mistranslated.
PLACEHOLDER = "⟦CODE_{}⟧"
PLACEHOLDER_RE = re.compile(r"⟦CODE_(\d+)⟧")


# A fence's info string says what it is for. These are for READING - diagrams, formulas, worked
# examples, lists of labels, sample output - so they are translated with the prose around them.
# Every other info string (python, bash, yaml, json, javascript, sql, dockerfile ...) is code that
# runs, and stays byte-identical. Across the 16 courses 9,147 fences are `text` and 2,114 `python`.
TEXT_INFO = frozenset({"", "text", "txt", "plaintext", "plain", "ascii", "diagram"})

_FENCE_PARTS = re.compile(r"```([\w+-]*)\n(.*?)```", re.DOTALL)


def fence_info(block: str) -> str:
    match = _FENCE_PARTS.match(block)
    return match.group(1).lower() if match else ""


def is_text_fence(block: str) -> bool:
    """A learner-facing text block (translated), as opposed to executable code (never touched)."""
    return fence_info(block) in TEXT_INFO


def fences(markdown: str) -> List[str]:
    """Every fenced block, whole, in order."""
    return [m.group(0) for m in FENCE.finditer(markdown)]


def protect_code(markdown: str):
    """Swap every fenced block of executable CODE for a placeholder. Returns (masked, blocks).

    Learner-facing `text` blocks are left in the text on purpose: they are what a translator has to
    translate. The placeholders are numbered over the code blocks only."""
    blocks: List[str] = []

    def take(match):
        if is_text_fence(match.group(0)):
            return match.group(0)
        blocks.append(match.group(0))
        return PLACEHOLDER.format(len(blocks) - 1)

    return FENCE.sub(take, markdown), blocks


def restore_code(masked: str, blocks: List[str]) -> str:
    def put(match):
        index = int(match.group(1))
        return blocks[index] if 0 <= index < len(blocks) else match.group(0)

    return PLACEHOLDER_RE.sub(put, masked)


def placeholder_problems(masked_draft: str, blocks: List[str]) -> List[str]:
    """Every placeholder must come back exactly once, and none invented."""
    found = [int(n) for n in PLACEHOLDER_RE.findall(masked_draft)]
    problems = []
    missing = [i for i in range(len(blocks)) if i not in found]
    if missing:
        problems.append(
            f"the draft dropped {len(missing)} of {len(blocks)} code placeholders"
        )
    duplicated = {i for i in found if found.count(i) > 1}
    if duplicated:
        problems.append(f"code placeholder(s) {sorted(duplicated)} appear more than once")
    invented = {i for i in found if i >= len(blocks)}
    if invented:
        problems.append(f"the draft invented code placeholder(s) {sorted(invented)}")
    return problems


# ─── Learner-facing text ──────────────────────────────────────────────────

# What an author writes that must survive a translation untouched: `inline code`, snake_case,
# camelCase / PascalCase, ALL_CAPS, calls like fit(), dotted names such as X.shape or torch.nn.
TECHNICAL = re.compile(
    r"`[^`]+`"
    r"|\b[A-Za-z0-9]+(?:_[A-Za-z0-9]+)+\b"
    r"|\b[a-z]+(?:[A-Z][a-z0-9]*)+\b"
    r"|\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]*)+\b"
    r"|\b[A-Z]{2,}[A-Z0-9]*\b"
    r"|\b[A-Za-z_][\w]*\(\)"
    r"|\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+\b"
)
_NUMBER = re.compile(r"\d[\d,.]*\d|\d")
_VARIABLE = re.compile(r"^[ \t]*([A-Za-z])[ \t]*(?==)", re.MULTILINE)
_ENGLISH_WORD = re.compile(r"[A-Za-z]{3,}")
# Structure a text block carries in symbols: arrows, operators, separators. Arabic uses the same ones.
_STRUCTURE = "→←↑↓↔⇒⇐×÷=+<>/|≈≥≤"
_ARABIC = re.compile(r"[؀-ۿ]")
# An image request is a `[[IMAGE_NEEDED: ...]]` marker; it may be wrapped over several lines.
_IMAGE_REQUEST = re.compile(r"\[\[IMAGE_NEEDED(?:[^\[\]]|\[[^\[\]\n]*\])*\]\]")
_MARKER_OR_HTML = re.compile(r"\{\{[^{}\n]+\}\}|\[\[(?:[^\[\]\n]|\[[^\[\]\n]*\])*\]\]|<[^>\n]+>|https?://\S+|⟦CODE_\d+⟧")


def technical_tokens(text: str) -> List[str]:
    """The identifiers, variables and numbers a translation must not change."""
    return sorted(TECHNICAL.findall(text) + _VARIABLE.findall(text) + _NUMBER.findall(text))


def english_words(text: str) -> List[str]:
    """Words a translator is expected to translate: what is left once code-like tokens and numbers go."""
    stripped = _NUMBER.sub(" ", TECHNICAL.sub(" ", text))
    return _ENGLISH_WORD.findall(stripped)


def text_fence_problems(english_body: str, arabic_body: str) -> List[str]:
    """What is wrong with the translation of one learner-facing text block, if anything."""
    problems: List[str] = []
    if not english_words(english_body):
        # Only identifiers, numbers and symbols (`2 + 2 = 4`, `X.shape = (10000, 12)`, or code that
        # an author tagged `text`): there is nothing to translate, so nothing may change.
        if english_body.strip() != arabic_body.strip():
            problems.append("has no words to translate (only identifiers, numbers and symbols), so it must stay identical")
        return problems
    en_lines, ar_lines = english_body.strip("\n").split("\n"), arabic_body.strip("\n").split("\n")
    if len(en_lines) != len(ar_lines):
        # A diagram or a list keeps its shape: one translated line for each English line.
        problems.append(f"has {len(ar_lines)} lines against {len(en_lines)} in the English")
    for symbol in _STRUCTURE:
        if english_body.count(symbol) != arabic_body.count(symbol):
            problems.append(f"the symbol {symbol!r} appears {arabic_body.count(symbol)} times against {english_body.count(symbol)}")
    wanted, got = technical_tokens(english_body), technical_tokens(arabic_body)
    lost = [t for t in dict.fromkeys(wanted) if wanted.count(t) > got.count(t)]
    if lost:
        problems.append(f"identifiers or numbers changed or lost: {', '.join(lost)}")
    if english_words(english_body) and not _ARABIC.search(arabic_body):
        problems.append("is learner-facing text that was left in English")
    return problems


def left_in_english(text: str) -> bool:
    """Three or more English words and no Arabic letter at all: a sentence nobody translated.
    Inline code, markers, HTML and links do not count as words."""
    plain = _MARKER_OR_HTML.sub(" ", INLINE_CODE.sub(" ", text))
    return len(english_words(plain)) >= 3 and not _ARABIC.search(plain)


def untranslated_lines(markdown: str) -> List[str]:
    """Lines of prose, headings and table cells (outside every fence) that are `left_in_english`."""
    flagged: List[str] = []
    for raw in _IMAGE_REQUEST.sub("", FENCE.sub("", markdown)).splitlines():
        line = raw.strip()
        if not line or line == "---" or line.startswith("```"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")] if line.startswith("|") else [line]
        for cell in cells:
            if re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")):
                continue
            if left_in_english(cell):
                flagged.append(cell[:80])
    return flagged


# Characters nobody can see: zero-width joiners and spaces, bidi overrides and isolates, a BOM and a
# no-break space. They are never typed on purpose in lesson text, they break search, copy-paste and
# bidirectional layout, and an editor can insert one without any sign.
INVISIBLE = re.compile("[​‌‍‎‏‪-‮⁦-⁩﻿ ]")


def invisible_characters(text: str) -> List[str]:
    """The invisible characters in `text`, as U+XXXX with a little context."""
    return [f"U+{ord(m.group()):04X} near {text[max(0, m.start() - 12):m.start()]!r}" for m in INVISIBLE.finditer(text)]


# ─── The lesson page's glossary ───────────────────────────────────────────
#
# The page glosses glossary terms by itself (components/ui/TermAnnotator.tsx): the FIRST mention of a
# term in a lesson renders as `English (Arabic)`, later mentions as `English`, and it matches any of a
# term's surfaces - preferred, English, Arabic or abbreviation - longest first, on word boundaries.
# So an author's own parenthetical gloss next to a glossary term is glossed a second time:
#   `طول متجه (vector)`        ->  `Vector (Vector)`
#   `... (deployment)` first   ->  `(Deployment (النشر))`
# A term is written once, in English, and the page adds the Arabic.

_WORD_CHAR = re.compile(r"[0-9A-Za-z_؀-ۿ]")


def _glossary():
    entries = []
    for entry in T.TERMS.values():
        forms = {entry.get("preferred"), entry.get("en"), entry.get("ar"), entry.get("abbreviation")}
        entries += [(f, entry["id"]) for f in forms if f and len(f) >= 2]
    entries.sort(key=lambda e: -len(e[0]))
    pattern = re.compile("|".join(re.escape(f) for f, _ in entries), re.IGNORECASE)
    return pattern, {f.lower(): tid for f, tid in entries}


def glossary_matches(text: str) -> List[tuple]:
    """(start, end, surface, term id) for each glossary term the page would annotate in `text`."""
    pattern, by_surface = _glossary()
    found = []
    for m in pattern.finditer(text):
        s, e = m.start(), m.end()
        if (s > 0 and _WORD_CHAR.match(text[s - 1])) or (e < len(text) and _WORD_CHAR.match(text[e])):
            continue
        term = by_surface.get(m.group(0).lower())
        if term:
            found.append((s, e, m.group(0), term))
    return found


def _annotated_texts(markdown: str):
    """The strings the page annotates: prose, headings, list items, table cells - never code."""
    for raw in _IMAGE_REQUEST.sub("", FENCE.sub("", markdown)).splitlines():
        line = raw.strip()
        if not line or line == "---" or line.startswith("{{") or line.startswith("⟦"):
            continue
        line = re.sub(r"^#{1,6}\s+", "", line)
        line = re.sub(r"^>\s*", "", line)
        line = re.sub(r"^([-*]|\d+\.)\s+", "", line)
        cells = [c.strip() for c in line.strip("|").split("|")] if line.startswith("|") else [line]
        for cell in cells:
            if not re.fullmatch(r":?-{3,}:?", cell.replace(" ", "")):
                yield re.sub(r"`[^`]*`", " ", cell.replace("**", "").replace("*", ""))


def arabic_replacements(text: str) -> List[tuple]:
    """(Arabic phrase, the English term the page will show instead, the words around it) for every
    Arabic phrase of ours that is a glossary term's Arabic form. Usually right (`التقييم` -> Evaluation);
    a reviewer needs to see them because a phrase that merely CONTAINS a glossary form is cut in two:
    `مسار المعالجة المسبقة` becomes `Pipeline المسبقة`."""
    out = []
    for node in _annotated_texts(text):
        for (start, end, surface, term) in glossary_matches(node):
            if _ARABIC.search(surface):
                context = node[max(0, start - 28):start] + "[[" + surface + "]]" + node[end:end + 28]
                out.append((surface, T.TERMS[term]["preferred"], context))
    return out


def glossary_doubling(markdown: str) -> List[str]:
    """Places where the page's own glossary gloss would double the author's: a glossary term followed
    by its own parenthetical equivalent, or one that sits alone in parentheses at its first mention."""
    seen: set = set()
    out: List[str] = []
    for node in _annotated_texts(markdown):
        previous = None
        flagged = False
        for (start, end, surface, term) in glossary_matches(node):
            first = term not in seen
            seen.add(term)
            alone = start > 0 and node[start - 1] == "(" and end < len(node) and node[end] == ")"
            twice = bool(
                previous and previous[3] == term and re.fullmatch(r"\s*\(\s*", node[previous[1]:start])
                and re.match(r"\s*\)", node[end:])
            )
            if (twice or (alone and first)) and not flagged:
                flagged = True
                out.append(f"{surface!r} in {node.strip()[:90]!r}")
            previous = (start, end, surface, term)
    return out


_HEADING_LINE = re.compile(r"^#{1,6} ")


def heading_levels(markdown: str) -> List[int]:
    """Heading hierarchy in authored order, excluding fenced examples."""
    prose = FENCE.sub("", markdown)
    return [len(match.group(1)) for match in re.finditer(r"^(#{1,6})\s+", prose, re.MULTILINE)]


def table_shapes(markdown: str) -> List[tuple]:
    """Column count of every row in each pipe-table, in authored order.

    Cell text is deliberately ignored: Arabic tables are localized prose.  The
    shape is structural, and catches a dropped or merged cell that section-line
    parity alone cannot see.
    """
    prose = FENCE.sub("", markdown)
    tables: List[tuple] = []
    current: List[int] = []
    for raw in prose.splitlines():
        line = raw.strip()
        if line.startswith("|") and line.endswith("|") and line.count("|") >= 2:
            # Markdown permits escaped pipes inside a cell; they are content,
            # not separators.
            current.append(len(re.findall(r"(?<!\\)\|", line)) - 1)
        elif not line:
            # Some canonical source lessons retain extraction-time blank lines
            # between table rows.  Whitespace does not change the table's row
            # or column structure, and translated Markdown may normalize it.
            continue
        elif current:
            tables.append(tuple(current))
            current = []
    if current:
        tables.append(tuple(current))
    return tables


def sections(markdown: str) -> List[tuple]:
    """(heading, content lines) for each section, in order. A fenced block counts as ONE line here
    (its own lines are held to the English by `text_fence_problems`); blank lines and rules do not
    count. Text before the first heading is section 0."""
    collapsed = _IMAGE_REQUEST.sub("⟦IMAGE⟧", FENCE.sub("⟦FENCE⟧", markdown))
    out: List[tuple] = [("(start)", 0)]
    heading, count = "(start)", 0
    for raw in collapsed.splitlines():
        if _HEADING_LINE.match(raw):
            out[-1] = (heading, count)
            heading, count = raw.strip(), 1
            out.append((heading, count))
        elif raw.strip() and raw.strip() != "---":
            count += 1
    out[-1] = (heading, count)
    return out


def section_parity_problems(english: str, arabic: str) -> List[str]:
    """Nothing omitted, nothing summarised: every section of the Arabic has as many lines of prose,
    bullets, table rows and fenced blocks as the same section of the English. A translator who
    merges two sentences into one line, or skips a bullet, is caught at the section it happened in."""
    en, ar = sections(english), sections(arabic)
    if len(en) != len(ar):
        return []  # a different number of headings is reported on its own
    problems = []
    for index, ((en_heading, en_lines), (ar_heading, ar_lines)) in enumerate(zip(en, ar)):
        if en_lines != ar_lines:
            problems.append(
                f"section {index} ({ar_heading[:50]!r}, English {en_heading[:50]!r}): "
                f"{ar_lines} lines against {en_lines} in the English"
            )
    return problems


# ─── Review ───────────────────────────────────────────────────────────────

@dataclass
class Review:
    problems: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.problems


def protected_vocabulary() -> List[str]:
    """Technology names and AI terms that must survive in Latin script.

    Sourced from the same dictionary the lessons, the glossary and the mentor
    already use, so "which words stay English" has one answer across the
    product rather than one per tool.
    """
    vocabulary = set(T.TECH_NAMES)
    for entry in T.TERMS.values():
        for key in ("en", "preferred", "abbreviation"):
            value = (entry.get(key) or "").strip()
            # Single characters match far too much prose to be useful, but
            # two-letter acronyms are kept when they are all-caps — AI and ML
            # are among the most important tokens on the platform, and an
            # earlier length cut-off let "AI Models vs AI Applications" come
            # back as "نماذج الذكاء الاصطناعي" without tripping anything.
            if len(value) > 2 or (len(value) == 2 and value.isupper()):
                vocabulary.add(value)
    return sorted(vocabulary, key=len, reverse=True)


def terminology_problems(english_prose: str, arabic_prose: str):
    """Terms present in the source must still be present, in Latin script.

    This catches both failure modes at once without needing to enumerate
    transliterations: whether the model rendered Python as بايثون or
    translated API to واجهة برمجة التطبيقات, the English token simply stops
    appearing. Run against prose only — code blocks are full of these words
    and would hide the problem entirely.

    Returns (lost_taught, lost_mentioned). The split is what makes the check
    usable in bulk: a term the lesson uses repeatedly is a term the lesson
    *teaches*, and losing it is a failure. A single lowercase mention inside
    a list of things covered later is a deviation worth seeing but not worth
    discarding an otherwise sound 3,500-character draft over — which is
    exactly what an uncalibrated version of this check did to gpt-4o.
    """
    taught, mentioned = [], []
    for term in protected_vocabulary():
        # ``React`` is both a case-sensitive framework name and an ordinary
        # lowercase English verb.  Treating every technology name
        # case-insensitively made prose such as "must react instantly" look
        # like a missing framework reference in Arabic.  Keep this exception
        # deliberately narrow: an authored ``React`` still has to survive,
        # while lowercase ``react`` is normal translatable prose.
        flags = 0 if term == "React" else re.I
        pattern = re.compile(r"(?<![A-Za-z0-9])" + re.escape(term) + r"(?![A-Za-z0-9])", flags)
        occurrences = len(pattern.findall(english_prose))
        if occurrences and not pattern.search(arabic_prose):
            (taught if occurrences >= 2 else mentioned).append(term)
    return taught, mentioned


def review(english: str, arabic: str) -> Review:
    """Check a draft before it is allowed into the workbook."""
    r = Review()

    if not arabic or not arabic.strip():
        r.problems.append("empty draft")
        return r

    # Terminology is the product's whole premise, so a draft that translates
    # or transliterates away a term the lesson teaches is rejected outright.
    taught, mentioned = terminology_problems(
        protect_code(english)[0], protect_code(arabic)[0]
    )

    def listed(terms):
        return ", ".join(terms[:6]) + (f" and {len(terms) - 6} more" if len(terms) > 6 else "")

    if taught:
        r.problems.append(f"taught terms no longer in English: {listed(taught)}")
    if mentioned:
        r.warnings.append(f"terms mentioned once, now Arabic: {listed(mentioned)}")

    # Executable code is byte-identical by construction (placeholders), so a difference here means
    # the restore step itself is wrong. Learner-facing text blocks are translated, so they are held
    # to a different bar: same place, same kind, same shape and symbols, same identifiers and
    # numbers, and not left in English.
    en_fences, ar_fences = fences(english), fences(arabic)
    if [fence_info(b) for b in en_fences] != [fence_info(b) for b in ar_fences]:
        r.problems.append(
            f"{len(ar_fences)} fenced blocks ({', '.join(fence_info(b) or 'untagged' for b in ar_fences)}) against "
            f"{len(en_fences)} ({', '.join(fence_info(b) or 'untagged' for b in en_fences)}) in the source"
        )
    else:
        for i, (en_b, ar_b) in enumerate(zip(en_fences, ar_fences), start=1):
            if is_text_fence(en_b):
                for problem in text_fence_problems(_FENCE_PARTS.match(en_b).group(2), _FENCE_PARTS.match(ar_b).group(2)):
                    r.problems.append(f"fenced block {i} (text): {problem}")
            elif en_b.strip() != ar_b.strip():
                r.problems.append(f"fenced block {i} (code) was modified — it must be identical")

    r.problems += section_parity_problems(english, arabic)

    en_heading_levels, ar_heading_levels = heading_levels(english), heading_levels(arabic)
    if en_heading_levels != ar_heading_levels:
        r.problems.append(
            f"heading hierarchy/order {ar_heading_levels} against {en_heading_levels} in the source"
        )

    en_tables, ar_tables = table_shapes(english), table_shapes(arabic)
    if en_tables != ar_tables:
        r.problems.append(f"table shapes {ar_tables} against {en_tables} in the source")

    hidden = invisible_characters(arabic)
    if hidden:
        r.problems.append(f"{len(hidden)} invisible character(s) in the text, e.g. {hidden[0]}")

    doubled = glossary_doubling(arabic)
    if doubled:
        r.problems.append(
            f"{len(doubled)} place(s) the lesson page would gloss twice (it adds the Arabic to a glossary term "
            f"by itself; write the term once, in English, with no parenthetical of your own), e.g. {doubled[0]}"
        )

    left = untranslated_lines(arabic)
    if left:
        r.problems.append(
            f"{len(left)} line(s) of prose or table cells left in English, e.g. {left[0]!r}"
        )

    # Inline spans carry class and function names. A large drop means the
    # model unwrapped them into prose, where they can be translated.
    en_inline, ar_inline = len(INLINE_CODE.findall(english)), len(INLINE_CODE.findall(arabic))
    if en_inline and ar_inline < en_inline * 0.6:
        r.warnings.append(f"{ar_inline} inline code spans against {en_inline} in the source")

    # Arabic runs longer than English; far short of that means the model
    # stopped early, which is what a too-small max_tokens looks like.
    ratio = len(arabic) / max(len(english), 1)
    if ratio < 0.8:
        r.problems.append(f"draft is {ratio:.0%} of the source length — likely truncated")
    elif ratio > 2.5:
        r.warnings.append(f"draft is {ratio:.0%} of the source length — unusually long")

    en_headings = len(re.findall(r"^#{1,6} ", english, re.MULTILINE))
    ar_headings = len(re.findall(r"^#{1,6} ", arabic, re.MULTILINE))
    if en_headings and ar_headings != en_headings:
        r.warnings.append(f"{ar_headings} headings against {en_headings} in the source")

    if not re.search(r"[؀-ۿ]", arabic):
        r.problems.append("no Arabic script in the draft")

    return r
