"""
backend/app/services/mentor/answer_evaluator_service.py

Conversational evaluation for exercise/quiz answers — the student writes
an answer (theory or code), the LLM responds like a patient technical
interviewer: assesses it, explains what's right or missing, and keeps
the door open for a follow-up rather than issuing a single flat verdict.
"""
import json
from typing import List, Optional

from app.services.language.language_policy import build_policy
from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider
from app.services.utils import parse_json_response

SYSTEM_PROMPT = """You are a sharp, encouraging technical interviewer evaluating a student's
answer to a practice question. You behave like a real conversation, not a grading script:
acknowledge what they got right, point out what's missing or wrong, ask a clarifying or
follow-up question when it helps, and let the student respond again before you finalize
a verdict if their first answer is incomplete.

Rules:
- Be specific: reference their actual wording or code, don't give generic feedback.
- If the question is theoretical, judge understanding, not exact phrasing.
- If the question involves code, mentally trace through it for correctness, not just style.
- Don't reveal the full reference answer/solution outright if their answer is wrong or
  incomplete — nudge them toward it first, the way a good interviewer does. You may reveal
  it once they've made a genuine attempt and are still off, or if they explicitly ask.
- Keep replies conversational and concise (3-8 sentences), not a wall of text.
- Only set "is_correct" to true/false once you can make that call — use null while the
  conversation is still in progress (e.g. you just asked a clarifying question).

Return ONLY a valid JSON object with this exact structure:
{
  "reply": "your conversational response to the student",
  "is_correct": true | false | null,
  "score": <integer 0-100, or null if not yet resolved>,
  "suggested_actions": ["short follow-up prompt", "..."]
}"""

_FALLBACK_ACTIONS = ["Try explaining your reasoning further", "Ask for a hint"]


def _build_context_block(context: dict) -> str:
    kind = context.get("kind", "exercise")
    lines = [f"[{'Exercise' if kind == 'exercise' else 'Quiz question'}]"]
    lines.append(f"Title: {context.get('title', '')}")
    lines.append(f"Prompt: {context.get('prompt', '')}")
    if context.get("starter_code"):
        lines.append(f"Starter code given to student:\n{context['starter_code']}")
    if context.get("reference"):
        lines.append(f"Reference answer/solution (for YOUR grading only — do not paste this to the student unprompted):\n{context['reference']}")
    if context.get("skill_tags"):
        lines.append(f"Skills being tested: {', '.join(context['skill_tags'])}")
    return "\n".join(lines)


def evaluate_answer(
    llm: BaseLLMProvider,
    context: dict,
    conversation_history: List[dict],
    user_message: str,
    language: Optional[str] = None,
    terminology_mode: Optional[str] = None,
) -> dict:
    """
    context: {
        kind: "exercise" | "quiz_question",
        title: str,
        prompt: str,                  # exercise.description or quiz question text
        starter_code: Optional[str],
        reference: Optional[str],     # solution_code or the quiz question's explanation
        skill_tags: List[str],
    }
    """
    context_block = _build_context_block(context)

    # The context block is re-sent as a system-adjacent user turn only on the
    # first message, to avoid repeating a large block every turn — the model
    # already has it in its own context window from the conversation history.
    if not conversation_history:
        first_message = f"{context_block}\n\nStudent's answer:\n{user_message}"
        messages = [{"role": "user", "content": first_message}]
    else:
        messages = conversation_history + [{"role": "user", "content": user_message}]

    raw = llm.chat(
        system=SYSTEM_PROMPT + build_policy(language, terminology_mode),
        messages=messages,
        max_tokens=700,
    )

    fallback = {
        "reply": raw,
        "is_correct": None,
        "score": None,
        "suggested_actions": _FALLBACK_ACTIONS,
    }
    data = parse_json_response(raw, fallback)
    if not isinstance(data, dict):
        return fallback
    return {
        "reply": data.get("reply", raw),
        "is_correct": data.get("is_correct"),
        "score": data.get("score"),
        "suggested_actions": data.get("suggested_actions", _FALLBACK_ACTIONS),
    }
