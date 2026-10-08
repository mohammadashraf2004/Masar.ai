"""Opt-in end-to-end Mentor v2 check against the configured provider.

Run with ``RUN_LIVE_MENTOR_TESTS=1``. It creates an isolated test learner,
uses the normal authenticated endpoint and wallet, and costs one small provider
request. It is skipped during deterministic test runs.
"""
import os

import pytest

from app.models.wallet import TransactionType
from app.services.wallet.wallet_service import CREDIT_COSTS
from tests.mentor_fixtures import _balance, _register, _txs
from tests.test_mentor_v2 import _curriculum, _post_message


pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_LIVE_MENTOR_TESTS") != "1",
    reason="opt-in: set RUN_LIVE_MENTOR_TESTS=1 (calls a real provider, costs tokens)",
)


def test_live_mentor_reply_is_returned_and_charged_once(api, db):
    lesson, _, _, _ = _curriculum(db)
    token, user_id = _register(api)
    before = _balance(db, user_id)

    response = _post_message(
        api, token, text="Explain the lesson's main idea in one sentence.",
        intent="EXPLAIN", context={"lessonId": str(lesson.id)},
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["blocks"]
    assert body["creditCost"] == CREDIT_COSTS["mentor_message"]
    assert _balance(db, user_id) == before - CREDIT_COSTS["mentor_message"]
    assert len(_txs(db, user_id, TransactionType.deduction)) == 1
    assert _txs(db, user_id, TransactionType.refund) == []
