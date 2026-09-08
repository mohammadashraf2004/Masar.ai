import json
from typing import Any, Iterator, List

from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider

SYSTEM_PROMPT = """You are an expert curriculum designer for tech careers.
Generate a personalized weekly learning roadmap.

Return ONLY a valid JSON array of weeks:
[
  {
    "week": 1,
    "theme": "...",
    "topics": ["topic1", "topic2"],
    "project": "mini project description",
    "goal": "what the student will be able to do by end of week"
  }
]
Generate exactly 4 weeks."""


# ─── Parsing ──────────────────────────────────────────────────────────────────
# This roadmap is the one LLM response in the app whose top level is a JSON
# ARRAY. app.services.utils.parse_json_response only ever returns a dict —
# an array falls through its isinstance check, and its brace scanner then
# happily returns the FIRST WEEK OBJECT found inside the array. That dict
# then failed the `isinstance(result, list)` guard here, so a perfectly good
# four-week roadmap became `[]` — every single time, for every model. The
# endpoint charged 5 credits and returned an empty plan.
#
# The parsing therefore lives here rather than in the shared helper: every
# other consumer (mentor reply, code review, hints, skill gap) legitimately
# expects an object, and widening the shared parser to return lists would
# change what all of them receive.


def _iter_balanced_arrays(text: str) -> Iterator[str]:
    """Yield each balanced top-level [...] block, in order of appearance.

    Same brace-matching idea as utils._iter_balanced_objects, for brackets.
    Nested arrays (a week's "topics") only close the outer block when depth
    returns to zero, and prose before/after the array is skipped.
    """
    depth = 0
    start = None
    for i, ch in enumerate(text):
        if ch == "[":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "]":
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    yield text[start:i + 1]
                    start = None


def _is_usable_week(item: Any) -> bool:
    """Minimum a week must have to be worth showing.

    Taken from what the prompt above asks for and what the reader actually
    renders (week / theme / topics.length / goal) — not a new schema. The
    `topics` list check matters most: the dashboard calls `.length` on it,
    so a week without it would render as a crash rather than a plan.
    """
    return (
        isinstance(item, dict)
        and isinstance(item.get("theme"), str)
        and bool(item["theme"].strip())
        and isinstance(item.get("topics"), list)
    )


def _extract_weeks(raw: str) -> List[dict]:
    """Pull the week array out of a model response. Returns [] when the
    response contains nothing usable — the caller treats that as a failed
    generation rather than as an empty-but-successful roadmap."""
    text = raw.strip()
    if text.startswith("```"):
        text = text.lstrip("`")
        if text.lower().startswith("json"):
            text = text[4:]
        text = text.rstrip("`").strip()

    candidates: List[Any] = []
    try:
        candidates.append(json.loads(text))
    except json.JSONDecodeError:
        pass
    # Prose around the array is common even when the prompt forbids it.
    for block in _iter_balanced_arrays(raw):
        try:
            candidates.append(json.loads(block))
        except json.JSONDecodeError:
            continue

    for candidate in candidates:
        if isinstance(candidate, list):
            weeks = [w for w in candidate if _is_usable_week(w)]
            if weeks:
                return weeks
        # Tolerated deviation: some models wrap the array in an object
        # despite the instruction. Cheap to accept, and the alternative is
        # charging the student for a formatting preference.
        if isinstance(candidate, dict):
            for key in ("weeks", "roadmap", "plan"):
                value = candidate.get(key)
                if isinstance(value, list):
                    weeks = [w for w in value if _is_usable_week(w)]
                    if weeks:
                        return weeks

    return []


def generate_roadmap(
    llm: BaseLLMProvider,
    track: str,
    experience_level: str,
    weak_skills: List[str] = None,
    completed_topics: List[str] = None,
) -> List[dict]:
    weak_skills = weak_skills or []
    completed_topics = completed_topics or []

    message = (
        f"Track: {track}\n"
        f"Experience level: {experience_level}\n"
        f"Weak areas: {', '.join(weak_skills) if weak_skills else 'none identified yet'}\n"
        f"Already covered: {', '.join(completed_topics) if completed_topics else 'just starting'}"
    )

    raw = llm.chat(system=SYSTEM_PROMPT, messages=[{"role": "user", "content": message}], max_tokens=1000)
    # An empty list here means "the model produced nothing usable", which the
    # caller must treat as a failure — never as a successful empty roadmap.
    return _extract_weeks(raw)
