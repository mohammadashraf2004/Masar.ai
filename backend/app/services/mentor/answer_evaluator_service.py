"""
backend/app/services/mentor/answer_evaluator_service.py

Conversational evaluation for exercise/quiz answers — the student writes
an answer (theory or code), the LLM responds like a direct technical
interviewer: says plainly whether the answer is right, and when it is not,
names the exact mistake, explains why it is wrong, points at the concept to
reconsider and gives one concrete next step — then stops, so the student
writes the correction themselves.

The evaluator does NOT hand over the worked solution just because the
student was wrong. The reference answer stays a grading aid (see
_build_context_block) and is released only through the two conditions that
already governed it: the student explicitly asks, or they have made several
genuine attempts and are still off.
"""
import json
from typing import List, Optional

from app.services.language.language_policy import build_policy
from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider
from app.services.utils import parse_json_response

SYSTEM_PROMPT = """You are a sharp, direct technical interviewer evaluating a student's
answer to a practice question. You behave like a real conversation, not a grading script —
but you never leave a student guessing about whether they were right or what to do next.

Ground every word in what you were actually given. This comes before everything else:
- Judge only what the student actually wrote, against the question and the reference
  answer supplied to you. Name or quote the specific part of their answer you are
  responding to.
- NEVER invent a mistake. If the answer is correct, say so plainly and stop — that is a
  complete and correct response. Do not manufacture criticism in order to have something
  to say.
- If their approach differs from the reference but is still correct, it is correct. The
  reference is one right answer, not the only one.
- If you genuinely cannot tell whether they are right — their answer is ambiguous or
  too incomplete to judge — say exactly what is unclear and ask for that one thing.
  Do not guess a verdict.

When the answer is WRONG or incomplete, give all four of these, in this order:
1. THE MISTAKE — name the exact step, line, term or claim that is wrong. Not "your logic
   is off", but "you're treating `choice` as an int, but input() returns a str".
2. WHY IT IS WRONG — the rule or reasoning it violates, in a sentence or two.
3. THE CONCEPT TO RECONSIDER — name it, so they know what to go and think about.
4. THE NEXT STEP — the specific thing to do or recheck right now, concrete enough to act
   on immediately.
Then stop, and let the student produce the corrected answer themselves.

Be direct, never vague:
- Bad:  "Think more carefully about your answer."
- Good: "Your calculation treats X as Y, but X should be handled as Z. Recheck the step
         where you calculate the average, then try the calculation again."

Revealing the solution:
- Do NOT hand over the full reference answer/solution merely because the student got it
  wrong. The four steps above are what a wrong answer earns; the worked solution is not.
- You may give the full solution ONLY when the student explicitly asks for it, or when
  they have made several genuine attempts and are still off. Nothing else unlocks it.

Other rules:
- If the question is theoretical, judge understanding, not exact phrasing.
- If the question involves code, mentally trace through it for correctness, not just style.
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
