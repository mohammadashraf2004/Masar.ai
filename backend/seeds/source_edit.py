"""
backend/seeds/source_edit.py

Replace one piece of text inside the string literals of a Python lesson module, changing nothing else.

Lesson modules wrap long lines as adjacent string literals (implicit concatenation):

    '[[IMAGE_NEEDED: The agentic stack | Three layers: reasoning LLM, '
    'orchestration, and tools/external systems. | The LLM requests actions.]]\\n'

so the text a learner sees (`[[IMAGE_NEEDED: ... ]]`) is not one contiguous run of the file. `replace_in_literals`
finds the run of literals that holds it, rewrites only the fragments it touches, and returns the exact old
and new source for that region. Every other character, quote and line break stays as written.

It refuses (raises `SourceEditError`) rather than guess: the text is in a triple-quoted, raw or prefixed
literal, is not found exactly once, or nothing would be left of the fragments.
"""
import ast
import io
import re
import tokenize
from typing import List, Optional, Tuple

_PLAIN_START = re.compile(r"""^(?:'(?!'')|"(?!""))""")


class SourceEditError(Exception):
    pass


def _offsets(text: str) -> List[int]:
    starts = [0]
    for line in text.split("\n"):
        starts.append(starts[-1] + len(line) + 1)
    return starts


def _runs_of_strings(text: str) -> List[List[Tuple[int, int, str]]]:
    """Runs of STRING tokens with only whitespace, comments and line breaks between them."""
    starts = _offsets(text)
    runs: List[List[Tuple[int, int, str]]] = [[]]
    for tok in tokenize.generate_tokens(io.StringIO(text).readline):
        if tok.type == tokenize.STRING:
            runs[-1].append((starts[tok.start[0] - 1] + tok.start[1], starts[tok.end[0] - 1] + tok.end[1], tok.string))
        elif tok.type not in (tokenize.NL, tokenize.COMMENT):
            runs.append([])
    return [r for r in runs if r]


def literal_kind_at(text: str, offset: int) -> Optional[str]:
    """How the string literal that contains `offset` is written: "triple" (a triple-quoted string, where a
    line break is a real line break), "single" (one-line quotes, where it is the escape \\n), "other"
    (raw, prefixed or bytes - not safe to edit) or None when `offset` is not inside a literal."""
    for run in _runs_of_strings(text):
        for start, end, literal in run:
            if start <= offset < end:
                prefix = literal[: len(literal) - len(literal.lstrip("rRuUbBfF"))]
                body = literal[len(prefix):]
                triple = body[:3] in ("'''", '"""')
                if prefix.lower() not in ("", "r") or body[:1] not in ("'", '"'):
                    return "other"
                if prefix and not triple:
                    return "other"       # a raw one-line string has no escape for a line break
                return "triple" if triple else "single"
    return None


def replace_in_literals(text: str, old: str, new: str) -> Tuple[str, str]:
    """`(old source region, new source region)` for turning `old` into `new`; apply it with
    `text.replace(old_region, new_region, 1)` (the region is unique because it contains `old`)."""
    hits = []
    for run in _runs_of_strings(text):
        if not all(_PLAIN_START.match(literal) for _s, _e, literal in run):
            if any(old[:30] in literal for _s, _e, literal in run):
                raise SourceEditError("the text sits in a triple-quoted, raw or prefixed string literal")
            continue
        try:
            values = [ast.literal_eval(literal) for _s, _e, literal in run]
        except (ValueError, SyntaxError):
            continue
        joined = "".join(values)
        if old in joined:
            hits.append((run, values, joined))
    if len(hits) != 1 or hits[0][2].count(old) != 1:
        raise SourceEditError(f"the text is not found exactly once in the string literals ({len(hits)} runs hold it)")
    run, values, joined = hits[0]
    begin = joined.index(old)
    end = begin + len(old)
    spans, cursor = [], 0
    for value in values:
        spans.append((cursor, cursor + len(value)))
        cursor += len(value)
    touched = [i for i, (a, b) in enumerate(spans) if a < end and b > begin]
    first, last = touched[0], touched[-1]

    rewritten: List[Tuple[int, str]] = []
    for i in touched:
        a, _b = spans[i]
        head = values[i][: max(begin - a, 0)] if i == first else ""
        tail = values[i][end - a:] if i == last else ""
        rewritten.append((i, head + (new if i == first else "") + tail))

    region_start, region_end = run[first][0], run[last][1]
    out: str = ""
    emitted = False
    previous_end: Optional[int] = run[first][0]
    for i, value in rewritten:
        start, stop, _literal = run[i]
        if value != "":
            out += (text[previous_end:start] if emitted else "") + repr(value)
            emitted = True
        previous_end = stop
    if not emitted:
        raise SourceEditError("nothing would be left of the string literals")
    return text[region_start:region_end], out
