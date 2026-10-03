"""Validation layer for Mentor v2 replies.

Runs on every model reply before the learner sees it. The service calls it
once, retries the model once with the violations spelled out, and serves a
rule-based fallback if the retry fails too. Each check returns a short,
model-readable reason, which is what the retry prompt quotes back.

Checks:
  * structure    – blocks parse into the schema; grounding is one we offered
  * hint leak    – a hint does not hand over the exercise's solution
  * quiz leak    – no reply gives away a quiz answer for this module
  * invented     – "lesson N" exists; a course-grounded block overlaps the
                   course text it claims to come from
  * length       – the reply is not too long for its intent
"""
import difflib
import re
from typing import List, Tuple

from app.services.mentor.mentor_context import MentorContext
from app.services.mentor.mentor_text import normalize, squash, token_set, tokens

MAX_BLOCKS = 6
MAX_CHARS = {"hint": 700, "quiz": 900, "socratic": 900, "simplify": 1200}
DEFAULT_MAX_CHARS = 1800
MAX_HINT_CODE_LINES = 3
MIN_SOLUTION_LINE = 12
MIN_GROUNDING_OVERLAP = 2

_ANSWER_PHRASES = re.compile(
    r"(الاجابه الصحيحه|الجواب الصحيح|الخيار الصحيح|الاجابه هي|الجواب هو|correct answer|the answer is|right answer|correct option)"
)
_LESSON_REF = re.compile(r"(?:الدرس|lesson)\s*(?:رقم\s*)?(\d{1,3})")


def _block_text(b: dict) -> str:
    parts = [b.get("text") or "", b.get("code") or ""]
    parts += [str(s) for s in (b.get("steps") or [])]
    return "\n".join(p for p in parts if p)


def reply_text(blocks: List[dict]) -> str:
    return "\n".join(_block_text(b) for b in blocks)


def _solution_lines(solution: str) -> List[str]:
    out = []
    for line in (solution or "").splitlines():
        s = squash(line)
        if len(s) < MIN_SOLUTION_LINE or s.startswith(("#", "import ", "from ", "//")):
            continue
        out.append(s)
    return out


def check_hint_leak(blocks: List[dict], ctx: MentorContext, intent: str) -> List[str]:
    if intent not in ("hint", "socratic", "practice") and not any(b.get("kind") == "hint" for b in blocks):
        return []
    problems = []
    for b in blocks:
        code = b.get("code") or ""
        if code and len([l for l in code.splitlines() if l.strip()]) > MAX_HINT_CODE_LINES:
            problems.append(f"hint_leak: a hint may show at most {MAX_HINT_CODE_LINES} lines of code")
            break
    sol = ctx.solution_code or ""
    if sol.strip():
        text = squash(reply_text(blocks))
        if any(line in text for line in _solution_lines(sol)):
            problems.append("hint_leak: the reply contains a line of the exercise solution")
        else:
            code = "\n".join(b.get("code") or "" for b in blocks).strip()
            if code and difflib.SequenceMatcher(None, squash(code), squash(sol)).ratio() > 0.6:
                problems.append("hint_leak: the reply's code is close to the exercise solution")
    return problems


def check_quiz_leak(blocks: List[dict], ctx: MentorContext, intent: str) -> List[str]:
    if not ctx.quiz_keys:
        return []
    text = squash(reply_text(blocks))
    reply_tokens = token_set(text)
    names_answer = bool(_ANSWER_PHRASES.search(text))
    for key in ctx.quiz_keys:
        correct = squash(key.correct_text)
        if len(correct) < 4 or correct not in text:
            continue
        stem = token_set(key.question)
        stem_hit = bool(stem) and len(stem & reply_tokens) / len(stem) >= 0.5
        if names_answer or stem_hit or intent == "quiz":
            return ["quiz_leak: the reply gives away the answer to a quiz question in this module"]
    return []


def check_invented(blocks: List[dict], ctx: MentorContext) -> List[str]:
    problems = []
    if ctx.module_lessons:
        for m in _LESSON_REF.finditer(normalize(reply_text(blocks))):
            if int(m.group(1)) not in ctx.module_lessons:
                problems.append(f"invented: lesson {m.group(1)} does not exist in this module")
                break
    for b in blocks:
        g = b.get("grounding")
        if g in (None, "general"):
            continue
        if g == "mistakes":
            source = token_set("\n".join(ctx.mistakes))
        else:
            source = token_set("\n".join(c.text + " " + c.lesson_title for c in ctx.chunks_for(g)))
        if not source:
            problems.append(f"invented: a block claims grounding '{g}' but no such course content was provided")
            continue
        if b.get("kind") in ("check", "quiz"):
            continue  # a question about the lesson needn't quote it
        block_tokens = tokens(_block_text(b))
        need = min(MIN_GROUNDING_OVERLAP, len(set(block_tokens)))
        if need and len(set(block_tokens) & source) < need:
            problems.append(f"invented: a block labelled '{g}' does not match the {g} content")
    return problems


def check_length(blocks: List[dict], intent: str) -> List[str]:
    limit = MAX_CHARS.get(intent, DEFAULT_MAX_CHARS)
    total = sum(len(_block_text(b)) for b in blocks)
    problems = []
    if len(blocks) > MAX_BLOCKS:
        problems.append(f"too_long: at most {MAX_BLOCKS} blocks")
    if total > limit:
        problems.append(f"too_long: {total} characters, the limit for '{intent}' is {limit}")
    return problems


def check_structure(blocks, allowed_groundings: List[str]) -> List[str]:
    if not isinstance(blocks, list) or not blocks:
        return ["structure: reply must be a JSON object with a non-empty 'blocks' list"]
    for b in blocks:
        if not isinstance(b, dict):
            return ["structure: every block must be an object"]
        if b.get("kind") not in ("text", "code", "flow", "check", "hint"):
            return ["structure: block kind must be one of text, code, flow, check, hint"]
        if b.get("grounding") not in allowed_groundings:
            return [f"structure: grounding must be one of {', '.join(allowed_groundings)}"]
        if not _block_text(b).strip():
            return ["structure: empty block"]
    return []


def validate(blocks, ctx: MentorContext, intent: str, allowed_groundings: List[str]) -> Tuple[bool, List[str]]:
    problems = check_structure(blocks, allowed_groundings)
    if problems:
        return False, problems
    problems = (
        check_hint_leak(blocks, ctx, intent)
        + check_quiz_leak(blocks, ctx, intent)
        + check_invented(blocks, ctx)
        + check_length(blocks, intent)
    )
    return not problems, problems
