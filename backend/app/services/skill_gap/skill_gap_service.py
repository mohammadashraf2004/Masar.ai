from typing import List, Optional

from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider
from app.services.utils import parse_json_response

SYSTEM_PROMPT = """You are a technical career advisor for software and AI engineering roles.
Analyze the candidate's background and identify skill gaps for their target role.

Return ONLY a valid JSON object:
{
  "target_role": "...",
  "current_skills": ["..."],
  "missing_skills": [
    {"skill": "...", "priority": "critical|high|medium", "reason": "..."}
  ],
  "recommended_roadmap": ["Step 1: ...", "Step 2: ...", "..."],
  "readiness_score": <integer 0-100>,
  "summary": "3-4 sentence assessment"
}"""


def analyze_skill_gap(
    llm: BaseLLMProvider,
    target_role: str,
    current_skills: List[str],
    cv_text: Optional[str] = None,
    github_url: Optional[str] = None,
) -> dict:
    parts = [f"Target role: {target_role}"]
    if current_skills:
        parts.append(f"Self-reported skills: {', '.join(current_skills)}")
    if cv_text:
        parts.append(f"CV/Resume:\n{cv_text[:3000]}")
    if github_url:
        parts.append(f"GitHub: {github_url}")

    message = "\n\n".join(parts)
    raw = llm.chat(system=SYSTEM_PROMPT, messages=[{"role": "user", "content": message}], max_tokens=1000)

    fallback = {
        "target_role": target_role,
        "current_skills": current_skills,
        "missing_skills": [],
        "recommended_roadmap": [],
        "readiness_score": 0,
        "summary": raw[:500],
    }
    result = parse_json_response(raw, fallback)
    return result if isinstance(result, dict) else fallback
