"""
What the learner is asking for.

Three steps, cheapest first:

1. an explicit intent the client sent (a chip the learner pressed) - it always wins;
2. keyword rules, Arabic and English, which decide most messages for free;
3. the model, only when the rules cannot decide - and even then a bad answer from it just
   means GENERAL_QUESTION.
"""
from __future__ import annotations

import re
from typing import Optional, Pattern, Tuple

from app.services.utils import parse_json_response
from app.views.mentor_v2 import INTENTS

DEFAULT_INTENT = "GENERAL_QUESTION"


def _rx(*words: str) -> Pattern[str]:
    return re.compile("|".join(words), re.IGNORECASE)


# Order matters: the first rule that matches decides. The specific asks (an error to debug,
# a hint, a quiz) come before the broad ones (explain), because "explain why this fails" is
# a debugging question first.
_RULES: Tuple[Tuple[str, Pattern[str]], ...] = (
    ("DEBUG", _rx(r"traceback", r"exception", r"\berror\b", r"\bbug\b", r"doesn'?t work", r"not working",
                  r"\bfails?\b", r"\bfailing\b", r"خطأ", r"الخطأ", r"يفشل", r"فشل", r"لا يعمل", r"ما يشتغل",
                  r"مش شغال", r"مشكلة في الكود", r"\bwrong\b", r"غلط", r"خاطئ", r"خاطئة")),
    ("HINT", _rx(r"\bhint\b", r"\bstuck\b", r"give me a clue", r"تلميح", r"عالق", r"تعبت", r"ساعدني بدون الحل",
                 r"بدون الحل")),
    ("QUIZ", _rx(r"\bquiz\b", r"test me", r"\bexam me\b", r"اختبرني", r"اختبار", r"سؤال لي", r"اسألني")),
    ("SIMPLIFY", _rx(r"simplif", r"\beli5\b", r"in simple terms", r"simpler", r"بسّط", r"بسط", r"أبسط", r"ابسط",
                     r"مش فاهم", r"ما فهمت", r"لم أفهم", r"بشكل مبسط")),
    ("PRACTICE", _rx(r"\bpractice\b", r"\bexercise me\b", r"give me an exercise", r"تمرين", r"تدرّب", r"تدرب",
                     r"تطبيق عملي")),
    ("REVIEW", _rx(r"\breview\b", r"\bsummar", r"recap", r"راجع", r"مراجعة", r"ملخص", r"لخّص", r"لخص")),
    ("SOCRATIC", _rx(r"socratic", r"guide me", r"ask me questions", r"سقراط", r"وجّهني", r"وجهني",
                     r"اسألني أسئلة")),
    ("CONNECT", _rx(r"how does this relate", r"connect(s|ed)? to", r"relationship between", r"علاقة", r"يرتبط",
                    r"كيف يرتبط", r"ربط")),
    ("WHY", _rx(r"\bwhy\b", r"لماذا", r"ليش", r"ليه", r"ما الفائدة", r"why does this matter", r"أهمية")),
    ("CAREER_CONTEXT", _rx(r"\bcareer\b", r"\bjob\b", r"interview", r"\bcv\b", r"resume", r"وظيفة", r"مقابلة",
                           r"سيرة ذاتية", r"سوق العمل")),
    ("PROJECT_COACH", _rx(r"\bproject\b", r"portfolio", r"capstone", r"مشروع", r"مشروعي")),
    ("EXPLAIN", _rx(r"\bexplain\b", r"what is\b", r"what are\b", r"\bmeaning\b", r"\bhow does\b", r"اشرح", r"شرح",
                    r"ما هو", r"ما هي", r"يعني ايه", r"يعني إيه", r"وضّح", r"وضح", r"كيف يعمل")),
)


def by_rules(text: Optional[str]) -> Optional[str]:
    """The intent the keywords decide, or None."""
    if not text:
        return None
    for intent, pattern in _RULES:
        if pattern.search(text):
            return intent
    return None


CLASSIFY_SYSTEM = (
    "Classify the learner's message into exactly one intent. Intents: "
    + ", ".join(INTENTS)
    + '. Reply with JSON only: {"intent": "<one of the intents>"}. '
    "Use GENERAL_QUESTION when nothing else clearly fits."
)


def by_model(llm, text: str) -> str:
    """Ask the model to choose among the known intents. Anything it returns that is not one of
    them - or an answer that is not JSON at all - is GENERAL_QUESTION. A provider failure is
    not caught here: it is the same failure as the reply's would be, and the caller refunds."""
    raw = llm.chat(system=CLASSIFY_SYSTEM, messages=[{"role": "user", "content": text[:1000]}], max_tokens=40)
    data = parse_json_response(raw, None) if isinstance(raw, str) else None
    value = data.get("intent") if isinstance(data, dict) else None
    return value if isinstance(value, str) and value in INTENTS else DEFAULT_INTENT


def explicit_or_rules(explicit: Optional[str], text: Optional[str]) -> Optional[str]:
    """An explicit intent wins over detection. Otherwise the rules; None means 'undecided'."""
    if explicit in INTENTS:
        return explicit
    return by_rules(text)
