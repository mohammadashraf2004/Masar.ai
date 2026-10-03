"""Mentor v2 replies: prompt → model → validate → retry once → fallback.

The model is asked for structured `blocks`, each labelled with where its
content came from (`grounding`). Every reply goes through
mentor_validator before the learner sees it. A reply that fails is retried
once with the violations quoted back; one that fails again is replaced by
a rule-based fallback, which the controller refunds.
"""
import logging
from typing import List, Optional, Tuple

from app.services.language.language_policy import build_policy
from app.services.mentor import mentor_validator
from app.services.mentor.mentor_context import MentorContext
from app.services.mentor.mentor_quiz import L
from app.services.mentor.mentor_text import overlap, token_set, tokens
from app.services.utils import parse_json_response

logger = logging.getLogger(__name__)

MAX_REPLY_TOKENS = 900
MAX_HINT_LEVEL = 3

INTENT_GUIDE = {
    "explain": "Explain the concept clearly, tied to the current lesson. One short analogy is fine.",
    "simplify": "Re-explain in the simplest possible terms, shorter than the lesson does. No new jargon.",
    "example": "Give one small, concrete example (a short code block is fine), then explain what it shows.",
    "why": "Explain why this matters: what breaks without it, and where it is used later.",
    "hint": (
        "Give ONE hint at the requested level. Level 1: a conceptual nudge, as a question. "
        "Level 2: point to the specific place or argument to look at. Level 3: detailed guidance "
        "in words. Never write the solution; at most 3 lines of illustrative code."
    ),
    "socratic": "Do not answer directly. Ask one or two guiding questions that lead the learner to the answer.",
    "quiz": "Ask one short question that checks understanding of the current lesson. Do not give the answer.",
    "practice": "Propose one short practice task that applies the current lesson. Describe it; do not solve it.",
    "review": "Summarise the current lesson in 3-4 points, then ask one check question.",
}

SYSTEM_V2 = """You are Masar's AI tutor. You know which course, lesson and exercise the learner
is on, and where they have been struggling. You choose the teaching move that fits the intent.

Intent: {intent}. {guide}

Return ONLY a JSON object, no prose around it:
{{"blocks": [{{"kind": "text|code|flow|check|hint", "grounding": "{groundings}",
  "text": "...", "code": "...", "language": "python", "steps": ["A", "B"], "level": 1}}]}}

Block kinds: "text" prose; "code" a short code sample (put it in "code"); "flow" a short chain of
concepts in "steps"; "hint" a hint (set "level"); "check" one short question that checks understanding.

Grounding says where a block's content comes from, and must be one of: {groundings}.
  "lesson" = the CURRENT LESSON excerpts; "module" = OTHER LESSONS IN THIS MODULE;
  "prerequisite" = PREREQUISITE LESSONS; "mistakes" = the learner's RECENT MISTAKES;
  "general" = your own general knowledge, not taken from the course.
Never label a block as course content unless it is in the excerpts below. If it is not, use "general".

Rules:
- Refer to a lesson by number only if it is listed under MODULE LESSONS.
- Never reveal the answer to a quiz question, and never write an exercise's full solution.
- At most 4 blocks and about {limit} characters in total. Short sentences.
- Unless the intent is "hint", end with one "check" block.
"""


def _section(title: str, lines: List[str]) -> str:
    return f"## {title}\n" + "\n".join(lines) if lines else ""


def build_context_message(ctx: MentorContext, selection: Optional[str], hint_level: Optional[int]) -> str:
    if not ctx.has_course_context:
        return (
            "No course context is attached: the learner detached it. Answer from general knowledge "
            'only, and set every block\'s grounding to "general".'
        )
    parts = []
    if ctx.lesson is not None:
        parts.append(_section(f"CURRENT LESSON: {ctx.lesson_title}",
                              [c.text for c in ctx.chunks_for("lesson")]))
    if ctx.exercise is not None:
        parts.append(_section(f"CURRENT EXERCISE: {ctx.exercise_title}",
                              ["(The learner is working on this. Its solution is not shown to you; do not write one.)"]))
    if ctx.module_lessons:
        parts.append(_section(f"MODULE: {ctx.module_title} — MODULE LESSONS",
                              [f"{o}. {t}" for o, t in sorted(ctx.module_lessons.items())]))
    parts.append(_section("OTHER LESSONS IN THIS MODULE (excerpts)",
                          [f"[{c.lesson_title}] {c.text}" for c in ctx.chunks_for("module")]))
    parts.append(_section("PREREQUISITE LESSONS (excerpts)",
                          [f"[{c.lesson_title}] {c.text}" for c in ctx.chunks_for("prerequisite")]))
    parts.append(_section("RECENT MISTAKES (wrong quiz answers, newest first)", [f"- {m}" for m in ctx.mistakes]))
    learner = [f"Lessons completed in this module: {ctx.lessons_completed}"]
    if ctx.skills:
        learner.append("Skill confidence: " + ", ".join(f"{n} {v:.2f}" for n, v in ctx.skills))
    parts.append(_section("LEARNER", learner))
    if selection:
        parts.append(_section("TEXT THE LEARNER SELECTED IN THE LESSON", [f"«{selection.strip()}»"]))
    if hint_level:
        parts.append(f"Hint level requested: {hint_level} of {MAX_HINT_LEVEL}.")
    return "\n\n".join(p for p in parts if p)


def _clean_blocks(data) -> Optional[list]:
    if not isinstance(data, dict) or not isinstance(data.get("blocks"), list):
        return None
    out = []
    for b in data["blocks"]:
        if not isinstance(b, dict):
            return None
        clean = {"kind": b.get("kind"), "grounding": b.get("grounding")}
        for key in ("text", "code", "language"):
            if isinstance(b.get(key), str) and b[key].strip():
                clean[key] = b[key].strip()
        if isinstance(b.get("steps"), list):
            clean["steps"] = [str(s)[:80] for s in b["steps"][:8]]
        if isinstance(b.get("level"), int):
            clean["level"] = max(1, min(MAX_HINT_LEVEL, b["level"]))
        out.append(clean)
    return out


def attach_sources(blocks: List[dict], ctx: MentorContext) -> None:
    """Name the lesson a course-grounded block came from (the UI shows
    "extra concept · lesson 8")."""
    for b in blocks:
        g = b.get("grounding")
        if g == "lesson" and ctx.lesson is not None:
            b["source"] = {"lessonId": ctx.lesson.id, "title": ctx.lesson_title}
        elif g in ("module", "prerequisite"):
            bt = token_set(mentor_validator._block_text(b))
            best = max(ctx.chunks_for(g), key=lambda c: overlap(tokens(c.text), bt), default=None)
            if best is not None:
                b["source"] = {"lessonId": best.lesson_id, "title": best.lesson_title}


def fallback_blocks(ctx: MentorContext, intent: str) -> List[dict]:
    lang = ctx.language
    if intent == "hint" and ctx.exercise is not None:
        return [{
            "kind": "hint", "grounding": "lesson", "level": 1,
            "text": L(lang,
                      f"لنبدأ من الاختبار نفسه: ماذا يتوقّع أن يُرجع «{ctx.exercise_title}»؟ قارن ذلك بما يُرجعه كودك الآن، وحدّد أول سطر يختلف فيه الناتج.",
                      f"Start from the test itself: what does it expect \"{ctx.exercise_title}\" to return? Compare that with what your code returns now, and find the first line where they differ."),
        }]
    lesson_chunks = ctx.chunks_for("lesson")
    if lesson_chunks:
        return [
            {"kind": "text", "grounding": "general",
             "text": L(lang, "لم أتمكّن من صياغة إجابة موثوقة الآن. هذا أقرب ما في الدرس لسؤالك:",
                       "I couldn't put together a reliable answer just now. This is the closest part of the lesson:")},
            {"kind": "text", "grounding": "lesson", "text": lesson_chunks[0].text[:500]},
        ]
    return [{
        "kind": "text", "grounding": "general",
        "text": L(lang, "لم أتمكّن من صياغة إجابة موثوقة الآن. جرّب إعادة صياغة سؤالك، أو أرفق الدرس الذي تعمل عليه.",
                  "I couldn't put together a reliable answer just now. Try rephrasing, or attach the lesson you're working on."),
    }]


def generate_reply(
    llm,
    ctx: MentorContext,
    *,
    intent: str,
    text: str,
    selection: Optional[str],
    history: List[dict],
    hint_level: Optional[int],
    language: Optional[str],
    terminology_mode: Optional[str],
) -> Tuple[List[dict], bool, List[str]]:
    """Returns (blocks, used_fallback, last_violations). Provider errors
    propagate: the controller refunds and reports them."""
    allowed = ctx.tiers() + ["general"] if ctx.has_course_context else ["general"]
    limit = mentor_validator.MAX_CHARS.get(intent, mentor_validator.DEFAULT_MAX_CHARS)
    system = SYSTEM_V2.format(
        intent=intent, guide=INTENT_GUIDE[intent], groundings="|".join(allowed), limit=int(limit * 0.8),
    ) + build_policy(language, terminology_mode)

    question = (text or "").strip() or L(ctx.language, "اشرح هذا.", "Explain this.")
    messages = list(history) + [{
        "role": "user",
        "content": build_context_message(ctx, selection, hint_level) + "\n\n## LEARNER MESSAGE\n" + question,
    }]

    violations: List[str] = []
    for attempt in range(2):
        raw = llm.chat(system=system, messages=messages, max_tokens=MAX_REPLY_TOKENS)
        blocks = _clean_blocks(parse_json_response(raw, None))
        if blocks is not None and not ctx.has_course_context:
            # Context was detached: whatever the model says, nothing in this
            # reply can be backed by the course.
            for b in blocks:
                b["grounding"] = "general"
        ok, violations = mentor_validator.validate(blocks, ctx, intent, allowed)
        if ok:
            if intent == "hint":
                for b in blocks:
                    if b["kind"] == "hint":
                        b["level"] = hint_level or 1
            attach_sources(blocks, ctx)
            return blocks, False, []
        logger.info("mentor v2 reply failed validation (attempt %d): %s", attempt + 1, violations)
        messages = messages + [
            {"role": "assistant", "content": str(raw)[:4000]},
            {"role": "user", "content": "Your reply failed validation:\n- " + "\n- ".join(violations)
             + "\nReturn a corrected JSON object only."},
        ]
    return fallback_blocks(ctx, intent), True, violations


def blocks_as_text(blocks: List[dict]) -> str:
    """Plain-text rendering stored as the message `content`, so v1 readers
    of mentor_sessions.messages (and the model's history) still work."""
    out = []
    for b in blocks:
        if b.get("kind") == "quiz" and b.get("quiz"):
            q = b["quiz"]
            out.append(q["question"] + "\n" + "\n".join(f"- {o}" for o in q["options"]))
        else:
            out.append(mentor_validator._block_text(b))
    return "\n\n".join(o for o in out if o)


def history_for_model(messages: list, limit: int = 6) -> List[dict]:
    return [
        {"role": m["role"], "content": str(m.get("content", ""))[:2000]}
        for m in (messages or [])[-limit:]
        if m.get("role") in ("user", "assistant") and m.get("content")
    ]

