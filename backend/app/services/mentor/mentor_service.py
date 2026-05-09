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
