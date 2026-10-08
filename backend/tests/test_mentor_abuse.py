"""
Provider spend a learner can trigger must stay bounded (audit findings #6 and #7).

#7: a learner who keeps asking for quiz answers gets every model reply rejected by validation.
Each such send costs up to three provider calls; refunding every one made model use unlimited
and unbilled. Refunds for rejected replies are now a small daily allowance per account.

#6: quiz translation is unmetered. It must not call the model for unverified accounts, and a
question that cannot be translated must not cost two provider calls on every reload.
"""
import json
import uuid
from datetime import timedelta

from app.core.config import settings
from app.models.mentor_translation import MentorQuizTranslation
from app.models.wallet import TransactionType
from app.services.mentor.v2 import message as message_service
from app.services.mentor.v2 import translate
from tests.mentor_fixtures import FakeLLM, _auth, _balance, _register, _txs
from tests.test_mentor_quiz_language import AR, QUESTION, _english_only, _llm
from tests.test_mentor_v2 import _curriculum, _post_message

COST = 2  # CREDIT_COSTS["mentor_message"]


def _always_leaks(lesson, quiz):
    return json.dumps({"blocks": [{
        "kind": "quiz", "quizId": f"{quiz.id}:0", "question": "Which one?",
        "options": [{"id": "a", "text": "private-correct-token"}, {"id": "b", "text": "other"}],
        "correct": "a", "grounding": "lesson", "sourceLessonId": str(lesson.id),
    }]})


def test_rejected_replies_are_refunded_only_a_few_times_a_day(api, db, monkeypatch):
    monkeypatch.setattr(settings, "MENTOR_VALIDATION_REFUNDS_PER_DAY", 2)
    lesson, exercise, quiz, _ = _curriculum(db)
    token, user_id = _register(api)
    llm = FakeLLM(_always_leaks(lesson, quiz))
    monkeypatch.setattr(message_service, "get_llm", lambda: llm)
    start = _balance(db, user_id)
    context = {"lessonId": str(lesson.id), "exerciseId": str(exercise.id)}

    costs = []
    for _ in range(4):
        response = _post_message(api, token, intent="HINT", context=context)
        assert response.status_code == 200, response.text
        assert "private-correct-token" not in response.text  # the fallback, never the leak
        costs.append(response.json()["creditCost"])

    assert costs == [0, 0, COST, COST]
    assert _balance(db, user_id) == start - 2 * COST
    assert len(llm.calls) == 8  # explicit intent: two reply attempts per send, no classification
    refunds = _txs(db, user_id, TransactionType.refund)
    assert len(refunds) == 2 and all(r.description == message_service.VALIDATION_REFUND for r in refunds)


def test_provider_failures_are_still_always_refunded(api, db, monkeypatch):
    monkeypatch.setattr(settings, "MENTOR_VALIDATION_REFUNDS_PER_DAY", 0)
    lesson, _, _, _ = _curriculum(db)
    token, user_id = _register(api)
    before = _balance(db, user_id)
    monkeypatch.setattr(message_service, "get_llm", lambda: FakeLLM(RuntimeError("provider down")))
    for _ in range(3):
        assert _post_message(api, token, context={"lessonId": str(lesson.id)}).status_code == 503
    assert _balance(db, user_id) == before


def _unverified(api):
    response = api.post("/api/v1/auth/register", json={
        "accept_terms": True, "accept_privacy": True, "email": f"unv-{uuid.uuid4().hex[:12]}@example.com",
        "full_name": "Unverified", "password": "correct-horse-battery-staple-7",
    })
    assert response.status_code == 201, response.text
    return response.json()["access_token"]


def test_an_unverified_account_never_causes_a_translation_call(api, db, monkeypatch):
    _, quiz = _english_only(db)
    token = _unverified(api)
    llm = _llm(monkeypatch, AR)
    for _ in range(5):
        response = api.get(f"/api/v1/mentor/quiz/{quiz.id}:0?language=ar", headers=_auth(token))
        assert response.status_code == 200, response.text
        assert response.json()["question"] == QUESTION and response.json()["lang"] == "en"
    assert llm.calls == []


def test_an_unverified_account_still_reads_an_existing_translation(api, db, monkeypatch):
    _, quiz = _english_only(db)
    verified, _ = _register(api)
    llm = _llm(monkeypatch, AR)
    assert api.get(f"/api/v1/mentor/quiz/{quiz.id}:0?language=ar", headers=_auth(verified)).json()["lang"] == "ar"
    calls = len(llm.calls)
    response = api.get(f"/api/v1/mentor/quiz/{quiz.id}:0?language=ar", headers=_auth(_unverified(api)))
    assert response.json()["question"] == AR["question"] and len(llm.calls) == calls


def test_a_question_that_cannot_be_translated_is_not_retried_on_every_reload(api, db, monkeypatch):
    _, quiz = _english_only(db)
    token, _ = _register(api)
    llm = _llm(monkeypatch, {**AR, "options": AR["options"][:2]})  # never lines up
    for _ in range(5):
        response = api.get(f"/api/v1/mentor/quiz/{quiz.id}:0?language=ar", headers=_auth(token))
        assert response.status_code == 200 and response.json()["question"] == QUESTION
    assert len(llm.calls) == 2  # one translation attempt (two tries), then remembered
    row = db.query(MentorQuizTranslation).filter_by(quiz_id=quiz.id, question_index=0, language="ar").one()
    assert translate.accept(translate._source(quiz.questions[0]), row.payload) is None

    # Once the retry window has passed it is attempted again (a provider may have recovered).
    monkeypatch.setattr(translate, "FAILURE_RETRY_AFTER", timedelta(0))
    api.get(f"/api/v1/mentor/quiz/{quiz.id}:0?language=ar", headers=_auth(token))
    assert len(llm.calls) == 4


def test_a_provider_error_is_remembered_too(api, db, monkeypatch):
    _, quiz = _english_only(db)
    token, _ = _register(api)
    llm = _llm(monkeypatch, RuntimeError("provider down"))
    for _ in range(4):
        api.get(f"/api/v1/mentor/quiz/{quiz.id}:0?language=ar", headers=_auth(token))
    assert len(llm.calls) == 1
