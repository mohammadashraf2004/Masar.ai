"""Masar's own "could not run" messages follow the interface language; learner output never changes.

The messages are written in English where they happen (the execution backends and runners) and
translated by app/services/code_execution/messages.py. The first test reads those sources so a new
or reworded message cannot ship without its Arabic.
"""
import re
from pathlib import Path

from app.services.code_execution.messages import PLATFORM_MESSAGES_AR, platform_message

APP = Path(__file__).resolve().parents[1] / "app"
SOURCES = (
    APP / "services" / "project_lab" / "execution.py",
    APP / "services" / "code_execution" / "python_runner.py",
    APP / "services" / "code_execution" / "isolated_python_runner.py",
    # The runner's own outage messages reach the learner through the adapter.
    APP.parent / "project_runner" / "executor.py",
)
WRITTEN = re.compile(
    r'(?:JobOutcome\("infrastructure_error"|ExecutionResult\("(?:execution_error|grading_error)"),\s*stderr="([^"]+)"'
)


def test_every_message_masar_writes_instead_of_output_has_arabic():
    found = {message for path in SOURCES for message in WRITTEN.findall(path.read_text(encoding="utf-8"))}
    assert len(found) >= 10, f"the pattern no longer finds the messages: {sorted(found)}"
    missing = sorted(found - set(PLATFORM_MESSAGES_AR))
    assert not missing, f"add Arabic for: {missing}"
    assert all(re.search(r"[؀-ۿ]", text) for text in PLATFORM_MESSAGES_AR.values())


def test_english_and_learner_output_pass_through_unchanged():
    message = "Project execution is not available right now."
    assert platform_message(message, "en") == message
    assert platform_message(message, "ar") == "تشغيل الكود غير متاح الآن."
    assert platform_message(f"{message}\n", "ar") == "تشغيل الكود غير متاح الآن."
    learner = "Traceback (most recent call last):\nValueError: bad value"
    assert platform_message(learner, "ar") == learner
    assert platform_message("", "ar") == "" and platform_message(None, "ar") == ""
