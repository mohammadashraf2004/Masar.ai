"""Intent for a Mentor v2 message.

Order of authority:
    1. an explicit `intent` from the client (a chip, a toolbar button)
    2. keyword rules, Arabic and English
    3. the model, only when the rules cannot decide (no match, or a tie)
    4. "explain" if the model is unavailable or answers off-list
"""
import logging
import re
from typing import Optional, Tuple

from app.services.mentor.mentor_text import normalize
from app.views.mentor_v2 import INTENTS

logger = logging.getLogger(__name__)

# Patterns run against normalize()d text (no diacritics, hamza folded,
# ة→ه, ى→ي), so they are written in that form.
_RULES = {
    "hint": [r"تلميح", r"\bhint", r"عالق", r"\bstuck\b", r"(?:الاختبار|test)\S*\s+\S*\s*(?:يفشل|فاشل|fail)",
             r"مش شغال", r"لا يعمل"],
    "quiz": [r"اختبرني", r"\bquiz\b", r"test me", r"اسالني"],
    "simplify": [r"بس[ّ]?ط", r"ابسط", r"ببساطه", r"\bsimplif", r"\bsimpler\b", r"\beli5\b",
                 r"مش فاهم", r"ما فهمت", r"لم افهم", r"مو فاهم"],
    "example": [r"مثال", r"\bexample", r"\be\.g\b"],
    "why": [r"لماذا مهم", r"ليش مهم", r"ليه مهم", r"why (?:does it|is (?:this|it)) (?:matter|important)",
            r"\bwhy\b", r"^(?:ليش|ليه|لماذا)\b"],
    "practice": [r"تمرين", r"\bpractice\b", r"\bexercise\b"],
    "review": [r"راجع", r"ملخص", r"لخص", r"\bsummar", r"\brecap\b", r"\breview\b"],
    "socratic": [r"سقراط", r"\bsocratic\b", r"ساعدني افكر", r"خليني افكر"],
    "explain": [r"اشرح", r"\bexplain", r"ما هو", r"ما هي", r"what is", r"what are", r"شو يعني",
                r"يعني ايه", r"وضح"],
}
_COMPILED = {k: [re.compile(p) for p in v] for k, v in _RULES.items()}

CLASSIFY_PROMPT = (
    "Classify the student's message to an AI tutor into exactly one intent.\n"
    "Intents: " + ", ".join(INTENTS) + ".\n"
    "Reply with the single intent word only, nothing else."
)


def classify_by_rules(text: str) -> Optional[str]:
    t = normalize(text)
    scores = {k: sum(1 for p in pats if p.search(t)) for k, pats in _COMPILED.items()}
    best = max(scores.values())
    if best == 0:
        return None
    winners = [k for k, v in scores.items() if v == best]
    return winners[0] if len(winners) == 1 else None


def classify_by_model(llm, text: str) -> Optional[str]:
    try:
        raw = llm.chat(system=CLASSIFY_PROMPT, messages=[{"role": "user", "content": text[:1000]}], max_tokens=5)
    except Exception:
        logger.warning("mentor intent classification failed; defaulting", exc_info=True)
        return None
    word = re.sub(r"[^a-z]", "", str(raw or "").strip().lower().split()[0] if str(raw or "").strip() else "")
    return word if word in INTENTS else None


def needs_model(explicit: Optional[str], text: str) -> bool:
    return explicit is None and classify_by_rules(text) is None


def resolve_intent(explicit: Optional[str], text: str, llm_factory=None) -> Tuple[str, str]:
    """Returns (intent, source). `llm_factory` is only called when the rules
    could not decide, so a decidable message never touches the provider."""
    if explicit:
        return explicit, "explicit"
    by_rules = classify_by_rules(text)
    if by_rules:
        return by_rules, "rules"
    if llm_factory is not None:
        by_model = classify_by_model(llm_factory(), text)
        if by_model:
            return by_model, "model"
    return "explain", "default"
