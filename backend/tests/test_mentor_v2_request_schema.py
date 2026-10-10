"""Focused request-contract checks for the Mentor v2 composer."""

import pytest
from pydantic import ValidationError

from app.views.mentor_v2 import MentorMessageIn


@pytest.mark.parametrize("intent", ["HINT", "QUIZ", "REVIEW"])
def test_context_actions_do_not_require_redundant_typed_text(intent):
    payload = MentorMessageIn(intent=intent, context={"lessonId": "123"})

    assert payload.text is None
    assert payload.intent == intent


@pytest.mark.parametrize("intent", [None, "EXPLAIN", "SIMPLIFY", "PRACTICE"])
def test_other_messages_still_require_typed_text(intent):
    body = {"context": {"lessonId": "123"}}
    if intent is not None:
        body["intent"] = intent

    with pytest.raises(ValidationError, match="message needs text"):
        MentorMessageIn(**body)
