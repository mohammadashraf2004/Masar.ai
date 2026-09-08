import json
from typing import List, Optional, Tuple

from app.services.language.language_policy import build_policy
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
    language: Optional[str] = None,
    terminology_mode: Optional[str] = None,
) -> Tuple[str, List[str]]:
    """`language` / `terminology_mode` come from the student's own language
    preferences, so the mentor answers the way their lessons are written:
    Arabic explanation, English terminology, untouched code. Omitted, they
    fall back to the Arabic-first default — see
    app/services/language/language_policy.py.
    """
    context_note = f"\n\nStudent context: {json.dumps(user_context)}" if user_context else ""
    messages = conversation_history + [
        {"role": "user", "content": user_message + context_note}
    ]

    system = SYSTEM_PROMPT + build_policy(language, terminology_mode)
    raw = llm.chat(system=system, messages=messages, max_tokens=800)

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
    language: Optional[str] = None,
    terminology_mode: Optional[str] = None,
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

    # A hint is the shortest thing the tutor ever says, which makes it the
    # easiest place to slip into pure Arabic and hide the term the student
    # actually needs to look up. The policy applies here too — the "concept"
    # field in particular has to come back as something searchable
    # ("pandas.drop_duplicates", "Reranking"), not an Arabic paraphrase.
    raw = llm.chat(
        system=HINT_SYSTEM_PROMPT + build_policy(language, terminology_mode),
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

PROJECT_HINT_SYSTEM_PROMPT = """You are an expert AI mentor helping a student build a portfolio
project. Your job is to give a targeted, Socratic hint — guide them toward the solution without
writing it for them.

Rules:
- NEVER write the complete solution
- A short illustrative snippet (a few lines showing an API or pattern) is fine; a working
  implementation of their project is not
- DO point to the right tool, concept, or approach
- DO ask a guiding question that helps them think it through
- If they pasted code, address what is actually in it — the specific bug, the missing piece,
  the thing they got right
- Keep it short: 3-5 sentences max

Return a JSON object with keys:
  "hint"        — the hint text (string)
  "concept"     — the key concept or tool they should look up (e.g. "pandas.merge", "FastAPI dependency")
  "next_step"   — one concrete action they can take right now (string)
"""


def get_project_hint(
    llm,
    project_title: str,
    project_description: str,
    objectives: list,
    tech_stack: list,
    stuck_on: str,
    code: Optional[str] = None,
    hints_already_given: list = None,
    language: Optional[str] = None,
    terminology_mode: Optional[str] = None,
) -> dict:
    """A hint for a portfolio project, as the challenge hint is for a
    challenge. Same contract, same return shape — the difference is the
    context the tutor gets: a project brief and the student's own code
    rather than a rubric and a dirty dataset.
    """
    objectives_text = "\n".join(f"- {o}" for o in (objectives or [])) or "- (none listed)"
    stack_text = ", ".join(tech_stack or []) or "(unspecified)"

    # Trimmed rather than sent whole: the request schema already caps the
    # code, but the hint is a short answer and does not need a 20k-token
    # prompt to give one.
    code_block = ""
    if code and code.strip():
        code_block = f"\n\nWhat the student has written so far:\n```\n{code[:4000]}\n```"

    prev_hints = ""
    if hints_already_given:
        prev_hints = "\n\nHints already given (don't repeat these):\n" + "\n".join(
            f"- {h}" for h in hints_already_given[:20]
        )

    message = f"""Project: {project_title}

Brief:
{project_description}

What it has to deliver:
{objectives_text}

Stack: {stack_text}{code_block}

The student says they are stuck on:
"{stuck_on}"
{prev_hints}

Give a targeted hint that guides them without building it for them."""

    raw = llm.chat(
        system=PROJECT_HINT_SYSTEM_PROMPT + build_policy(language, terminology_mode),
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
