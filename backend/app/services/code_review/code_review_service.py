from typing import Optional

from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider
from app.services.utils import parse_json_response

SYSTEM_PROMPT = """You are an expert software engineer and code reviewer specializing in Python,
AI/ML, and backend development. Review code critically but constructively.

Return ONLY a valid JSON object with this exact structure:
{
  "overall_quality": "poor|fair|good|excellent",
  "score": <integer 0-100>,
  "issues": [
    {
      "type": "bug|style|performance|security|architecture",
      "severity": "low|medium|high",
      "line": <int or null>,
      "message": "...",
      "suggestion": "..."
    }
  ],
  "strengths": ["...", "..."],
  "improvements": ["...", "..."],
  "summary": "2-3 sentence overall assessment"
}"""

_FALLBACK = {
    "overall_quality": "fair",
    "score": 50,
    "issues": [],
    "strengths": [],
    "improvements": ["Could not parse detailed review. Please try again."],
    "summary": "",
}


def review_code(
    llm: BaseLLMProvider,
    code: str,
    language: str = "python",
    context: Optional[str] = None,
) -> dict:
    context_str = f"\nContext: {context}" if context else ""
    message = f"Review this {language} code:{context_str}\n\n```{language}\n{code}\n```"

    raw = llm.chat(system=SYSTEM_PROMPT, messages=[{"role": "user", "content": message}], max_tokens=1200)
    result = parse_json_response(raw, {**_FALLBACK, "summary": raw[:500]})
    return result if isinstance(result, dict) else {**_FALLBACK, "summary": raw[:500]}
