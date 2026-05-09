from typing import List

from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider
from app.services.utils import parse_json_response

SYSTEM_PROMPT = """You are an experienced technical interviewer at a top tech company.
Conduct mock interviews for software and AI engineering roles.

Return ONLY a valid JSON object:
{
  "question": "the interview question",
  "question_type": "theoretical|coding|system_design|behavioral",
  "hints": ["hint 1 if stuck", "hint 2"],
  "follow_up": "a follow-up question or null"
}"""

_FALLBACK = {
    "question": "",
    "question_type": "theoretical",
    "hints": [],
    "follow_up": None,
}


def generate_question(
    llm: BaseLLMProvider,
    topic: str,
    difficulty: str = "intermediate",
    previous_qa: List[dict] = None,
) -> dict:
    previous_qa = previous_qa or []
    context = f"Topic: {topic}\nDifficulty: {difficulty}"

    if previous_qa:
        prev_str = "\n".join(
            f"Q: {qa.get('question', '')}\nA: {qa.get('answer', '')}"
            for qa in previous_qa[-3:]
        )
        context += f"\n\nPrevious Q&A:\n{prev_str}\n\nAsk a different, progressively harder question."

    raw = llm.chat(system=SYSTEM_PROMPT, messages=[{"role": "user", "content": context}], max_tokens=500)
    result = parse_json_response(raw, {**_FALLBACK, "question": raw[:300]})
    return result if isinstance(result, dict) else {**_FALLBACK, "question": raw[:300]}
