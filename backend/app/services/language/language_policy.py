"""
app/services/language/language_policy.py

The language contract every AI-generated response obeys.

The mentor is the part of the platform a student talks to most, so if it
answers in formal Arabic that translates "Reranking" as "إعادة الترتيب", it
undoes the whole policy the courses follow. It has to behave exactly like the
lessons: explain in Arabic, name things in English, never touch code.

`build_policy()` produces the block appended to a service's system prompt.
The terminology examples in it come from the same dictionary the lessons
render from, so adding a term teaches the tutor too — nobody has to remember
to update a prompt.
"""
from __future__ import annotations

from typing import List, Optional

from app.content import terminology as T

#: Response language.
LANGUAGES = ("ar", "en")

#: How much English terminology the explanation carries. Matches the client's
#: TerminologyMode ladder (frontend/src/lib/language.ts).
MODES = ("arabic_first", "industry", "english_technical")

DEFAULT_LANGUAGE = "ar"
DEFAULT_MODE = "arabic_first"

# How many dictionary terms to name explicitly in the prompt. The tutor does
# not need the whole dictionary to get the pattern — it needs enough examples
# to generalise, without spending a thousand tokens on every request.
_TERM_SAMPLE = 24

_MODE_GUIDANCE = {
    "arabic_first": (
        "Explain in clear, natural Modern Standard Arabic — the register a "
        "university student reads comfortably, not formal literary Arabic. "
        "Introduce each technical term as `English (العربية)` the first time "
        "it appears, then keep using the English term."
    ),
    "industry": (
        "Explain in Arabic, but lean harder on English terminology — the way "
        "engineers actually talk in an Arabic-speaking team. Mix English "
        "terms into Arabic sentences freely: "
        "\"نستخدم Embeddings لتحويل documents إلى vectors، ثم Vector Database "
        "لتنفيذ similarity search\"."
    ),
    "english_technical": (
        "Answer in professional English, the register of documentation and "
        "engineering discussion. Arabic is only for a short clarification if "
        "the student seems stuck on a concept."
    ),
}

_ENGLISH_GUIDANCE = (
    "Answer in English. Keep terminology exactly as the industry writes it."
)


def _terminology_examples(limit: int = _TERM_SAMPLE) -> str:
    """`Preferred (العربية)` lines for the most commonly taught terms."""
    # Beginner/intermediate terms first: those are the ones a student is most
    # likely to ask about, and the ones most often mistranslated.
    ordered = sorted(
        T.TERMS.values(),
        key=lambda term: (
            {"beginner": 0, "intermediate": 1, "advanced": 2}.get(term.get("level"), 3),
            term["preferred"],
        ),
    )
    return "\n".join(
        f'  {term["preferred"]} ({term["ar"]})' for term in ordered[:limit]
    )


def build_policy(
    language: Optional[str] = DEFAULT_LANGUAGE,
    mode: Optional[str] = DEFAULT_MODE,
    *,
    include_terms: bool = True,
) -> str:
    """The language block to append to a system prompt.

    Unknown values fall back to the Arabic-first default rather than raising:
    this is prompt text, and a bad client value should not fail a request the
    student paid credits for.
    """
    language = language if language in LANGUAGES else DEFAULT_LANGUAGE
    mode = mode if mode in MODES else DEFAULT_MODE

    if language == "en":
        register = _ENGLISH_GUIDANCE
    else:
        register = _MODE_GUIDANCE[mode]

    lines: List[str] = [
        "",
        "LANGUAGE POLICY (follow exactly):",
        register,
        "",
        "Terminology rules, in every language setting:",
        "- Keep AI/ML technical terms in English. Do not translate them into "
        "Arabic and do not transliterate them into Arabic letters.",
        "- Keep official technology names exactly as written: "
        f"{', '.join(T.TECH_NAMES[:18])}, and the like.",
        "- NEVER translate code. Keywords, library and package names, class, "
        "function and variable names, CLI and git commands, file paths, URLs "
        "and error messages stay exactly as they are. Only the prose around a "
        "code block is in Arabic.",
        "- Write code comments in English too — they are part of the code.",
    ]

    if include_terms and language == "ar":
        lines += [
            "",
            "Use these English terms (Arabic meaning in brackets is for "
            "explaining once, not for replacing the term):",
            _terminology_examples(),
        ]

    return "\n".join(lines)


def normalize_language(value: Optional[str]) -> str:
    return value if value in LANGUAGES else DEFAULT_LANGUAGE


def normalize_mode(value: Optional[str]) -> str:
    return value if value in MODES else DEFAULT_MODE
