import json
from typing import List, Optional, Tuple

from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider
from app.services.utils import parse_json_response

SYSTEM_PROMPT = """You are an expert AI career mentor helping students in Egypt and the MENA region
become job-ready software and AI engineers. You are encouraging, precise, and practical.

Your role:
- Explain technical concepts clearly with examples
- Quiz students to check understanding
- Recommend what to practice next based on their level
- Review code they share
- Keep students accountable and motivated
- Adapt your explanations to beginner, intermediate, or advanced levels
- When relevant, mention real-world applications

Keep responses concise but thorough. Use code examples when helpful.
Always end with a clear next action for the student.

Return a JSON object with keys:
  "reply"             — your full response as a string
  "suggested_actions" — list of 2-3 short follow-up strings (e.g. "Try the exercise", "Ask me to quiz you")
"""


def get_mentor_reply(
    llm: BaseLLMProvider,
    conversation_history: List[dict],
    user_message: str,
    user_context: Optional[dict] = None,
) -> Tuple[str, List[str]]:
    context_note = f"\n\nStudent context: {json.dumps(user_context)}" if user_context else ""
    messages = conversation_history + [
        {"role": "user", "content": user_message + context_note}
    ]

    raw = llm.chat(system=SYSTEM_PROMPT, messages=messages, max_tokens=800)

    fallback = (raw, ["Continue learning", "Ask me a question", "Request a quiz"])
    data = parse_json_response(raw, None)

    if isinstance(data, dict):
        return data.get("reply", raw), data.get("suggested_actions", [])
    return fallback
# ── Add this to the END of backend/app/services/mentor/mentor_service.py ─────

HINT_SYSTEM_PROMPT = """You are an expert AI mentor helping a student work through a real-world
data engineering challenge. Your job is to give a targeted, Socratic hint — guide them toward
the solution without giving it away directly.

Rules:
- NEVER write the complete solution code
- DO point to the right tool, concept, or approach
- DO ask a guiding question that helps them think through the problem
- Keep it short: 3-5 sentences max
- If they mention a specific error or stuck point, address that directly
- Use concrete examples from the Egyptian/MENA tech context when relevant

Return a JSON object with keys:
  "hint"        — the hint text (string)
  "concept"     — the key concept or tool they should look up (e.g. "pandas.drop_duplicates")
  "next_step"   — one concrete action they can take right now (string)
"""


def get_challenge_hint(
    llm,
    challenge_title: str,
    challenge_difficulty: str,
    rubric: list,
    dirty_dataset_sample: list,
    stuck_on: str,
    hints_already_given: list = None,
) -> dict:
    rubric_text = "\n".join([
        f"- {r['criterion']} ({r['weight']}%): {r['description']}"
        for r in rubric
    ])

    prev_hints = ""
    if hints_already_given:
        prev_hints = "\n\nPrevious hints already given (don't repeat):\n" + "\n".join(
            f"- {h}" for h in hints_already_given
        )

    message = f"""Challenge: {challenge_title} ({challenge_difficulty})

Grading rubric:
{rubric_text}

Sample of the dirty dataset (first 3 records):
{json.dumps(dirty_dataset_sample[:3], ensure_ascii=False, indent=2)}

The student says they are stuck on:
"{stuck_on}"
{prev_hints}

Give a targeted hint that guides them without solving it for them."""

    raw = llm.chat(
        system=HINT_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": message}],
        max_tokens=300,
    )

    data = parse_json_response(raw, None)
    if isinstance(data, dict):
        return {
            "hint":      data.get("hint", raw),
            "concept":   data.get("concept", ""),
            "next_step": data.get("next_step", ""),
        }
    return {"hint": raw, "concept": "", "next_step": ""}