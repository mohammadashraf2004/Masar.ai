"""Arabic for the messages Masar itself writes in place of output when it cannot run learner
code: execution switched off, the runner unavailable, busy or broken, an invalid exercise
setup. They are never the learner's own output, so they follow the interface language like
every other message. Anything not listed here (the learner's program output) passes through
unchanged, and English is always the text as written.

tests/test_platform_messages.py fails when one of these messages is added or reworded in the
code without an Arabic entry here.
"""
from __future__ import annotations

PLATFORM_MESSAGES_AR: dict[str, str] = {
    "Project execution is not available right now.": "تشغيل الكود غير متاح الآن.",
    "The project runner is unavailable. Try again shortly.": "بيئة التشغيل غير متاحة الآن. حاول مرة أخرى بعد قليل.",
    "The project runner is busy. Try again in a moment.": "بيئة التشغيل مشغولة الآن. حاول مرة أخرى بعد لحظات.",
    "The project runner failed.": "تعطّلت بيئة التشغيل.",
    "The project runner returned an invalid result.": "أعادت بيئة التشغيل نتيجة غير صالحة.",
    "The execution environment failed.": "تعطّلت بيئة التشغيل.",
    "The execution service failed.": "تعطّلت خدمة التشغيل.",
    "The execution service returned an invalid result.": "أعادت خدمة التشغيل نتيجة غير صالحة.",
    "Exercise setup is invalid.": "إعداد هذا التمرين غير صالح.",
}


def platform_message(text: str | None, language: str) -> str:
    """``text`` in the interface ``language`` when Masar wrote it; otherwise unchanged."""
    if not text:
        return text or ""
    if language != "ar":
        return text
    return PLATFORM_MESSAGES_AR.get(text.strip(), text)
