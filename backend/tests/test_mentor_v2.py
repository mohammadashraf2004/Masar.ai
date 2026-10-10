"""Contracts for POST /mentor/message and POST /mentor/quiz/answer."""
import json
import uuid

from app.models.learning import CareerTrack, Exercise, Lesson, Quiz, Topic, TrackLevel
from app.models.mentor_evidence import MentorEvidence
from app.models.progress import ProgressStatus, UserProgress
from app.models.wallet import TransactionType, UserWallet
from app.services.mentor.v2 import message as message_service
from app.services.wallet.wallet_service import CREDIT_COSTS
from tests.mentor_fixtures import FakeLLM, _auth, _balance, _register, _txs

MESSAGE = "/api/v1/mentor/message"
ANSWER = "/api/v1/mentor/quiz/answer"


def _curriculum(db):
    suffix = uuid.uuid4().hex[:8]
    track = CareerTrack(slug=f"mentor-v2-{suffix}", title="AI Engineer")
    db.add(track)
    db.flush()
    level = TrackLevel(track_id=track.id, title="Foundations", order=1)
    db.add(level)
    db.flush()
    topic = Topic(
        level_id=level.id, title="Checkpointers", slug=f"checkpointers-{suffix}", order=1,
        prerequisite_ids=[], skill_tags=["Checkpointers"],
    )
    db.add(topic)
    db.flush()
    lesson = Lesson(
        topic_id=topic.id, source_key=f"COURSE-X/L-{suffix}", title="Graph memory",
        content="A Checkpointer stores graph state after every node and resumes a thread.",
        content_ar="يحفظ Checkpointer حالة graph بعد كل node ويستأنف thread.", order=1,
    )
    db.add(lesson)
    db.flush()
    exercise = Exercise(
        topic_id=topic.id, lesson_id=lesson.id, source_key=f"COURSE-X/L-{suffix}/x1",
        title="Persist memory", description="Complete the graph memory function.",
        starter_code="def persist_graph_state():\n    pass",
        solution_code="def persist_graph_state_for_every_node():\n    return checkpoint_repository.save_complete_graph_state()",
        skill_tested=["Checkpointers"],
    )
    quiz = Quiz(
        topic_id=topic.id, source_key=f"COURSE-X/L-{suffix}/quiz", title="Memory check",
        questions=[{
            "lesson_id": f"L-{suffix}",
            "question": "When is graph state stored?",
            "options": ["After every node using the private-correct-token", "Only after shutdown", "Never"],
            "correct": 0,
            "explanation": "State is checkpointed after a node.",
        }],
        questions_ar=[{
            "lesson_id": f"L-{suffix}",
            "question": "متى تُحفظ حالة graph؟",
            "options": ["بعد كل node باستخدام private-correct-token", "بعد الإغلاق فقط", "أبداً"],
            "correct": 0,
            "explanation": "تُحفظ الحالة بعد node.",
        }],
    )
    db.add_all([exercise, quiz])
    db.commit()
    return lesson, exercise, quiz, topic


def _valid(lesson_id: int, text: str = "الـ Checkpointer يحفظ graph state بعد كل node.") -> str:
    return json.dumps({"blocks": [{
        "kind": "text", "text": text, "grounding": "lesson", "sourceLessonId": str(lesson_id),
    }]}, ensure_ascii=False)


def _post_message(api, token, *, text="اشرح Checkpointer", intent="EXPLAIN", context=None, **extra):
    return api.post(MESSAGE, headers=_auth(token), json={
        "text": text, "intent": intent, "context": context or {}, "language": "ar", **extra,
    })


def test_hint_and_quiz_answers_are_rejected_then_retried(api, db, monkeypatch):
    lesson, exercise, quiz, _ = _curriculum(db)
    token, _ = _register(api)
    leaked = json.dumps({"blocks": [{
        "kind": "hint", "label": "الحل", "text": exercise.solution_code,
        "grounding": "lesson", "sourceLessonId": str(lesson.id),
    }]})
    still_leaked = json.dumps({"blocks": [{
        "kind": "quiz", "quizId": f"{quiz.id}:0", "question": "When?",
        "options": [{"id": "a", "text": "private-correct-token"}, {"id": "b", "text": "later"}],
        "correct": "a", "grounding": "lesson", "sourceLessonId": str(lesson.id),
    }]})
    safe = json.dumps({"blocks": [{
        "kind": "hint", "label": "تلميح", "text": "راقب أين تُحفظ graph state بعد كل node.",
        "grounding": "lesson", "sourceLessonId": str(lesson.id),
    }]}, ensure_ascii=False)
    llm = FakeLLM(leaked, still_leaked, safe)
    monkeypatch.setattr(message_service, "get_llm", lambda: llm)

    # The first request exhausts its one retry and falls back; the unsafe text never leaves.
    first = _post_message(api, token, intent="HINT", context={"lessonId": str(lesson.id), "exerciseId": str(exercise.id)})
    assert first.status_code == 200, first.text
    assert exercise.solution_code not in first.text
    assert "private-correct-token" not in first.text
    assert first.json()["creditCost"] == 0

    # A later request uses the safe scripted reply.
    second = _post_message(api, token, intent="HINT", context={"lessonId": str(lesson.id), "exerciseId": str(exercise.id)})
    assert second.status_code == 200, second.text
    assert "private-correct-token" not in second.text


def test_explicit_intent_wins_without_model_classification(api, db, monkeypatch):
    lesson, _, _, _ = _curriculum(db)
    token, _ = _register(api)
    llm = FakeLLM(_valid(lesson.id))
    monkeypatch.setattr(message_service, "get_llm", lambda: llm)

    response = _post_message(
        api, token, text="quiz me now", intent="SIMPLIFY", context={"lessonId": str(lesson.id)},
    )
    assert response.status_code == 200, response.text
    assert response.json()["intent"] == "SIMPLIFY"
    assert len(llm.calls) == 1, "an explicit intent must skip the classifier call"


def test_message_prompt_follows_the_selected_language(api, db, monkeypatch):
    lesson, _, _, _ = _curriculum(db)
    token, _ = _register(api)
    llm = FakeLLM(_valid(lesson.id, "A Checkpointer stores graph state after every node."))
    monkeypatch.setattr(message_service, "get_llm", lambda: llm)

    response = api.post(MESSAGE, headers=_auth(token), json={
        "text": "Explain Checkpointers", "intent": "EXPLAIN",
        "context": {"lessonId": str(lesson.id)}, "language": "en",
    })

    assert response.status_code == 200, response.text
    assert "Reply in English" in llm.calls[-1]["system"]
    assert "Arabic-first" not in llm.calls[-1]["system"]


def test_common_provider_text_aliases_are_normalized_before_validation(api, db, monkeypatch):
    lesson, _, _, _ = _curriculum(db)
    token, user_id = _register(api)
    before = _balance(db, user_id)
    reply = json.dumps({"blocks": [{
        "type": "text", "content": "A Checkpointer stores graph state after every node.",
        "grounding": "lesson", "sourceLessonId": lesson.id,
    }]})
    llm = FakeLLM(reply)
    monkeypatch.setattr(message_service, "get_llm", lambda: llm)

    response = api.post(MESSAGE, headers=_auth(token), json={
        "text": "Explain Checkpointers", "intent": "EXPLAIN",
        "context": {"lessonId": str(lesson.id)}, "language": "en",
    })

    assert response.status_code == 200, response.text
    assert response.json()["blocks"][0]["kind"] == "text"
    assert response.json()["blocks"][0]["text"].startswith("A Checkpointer")
    assert response.json()["creditCost"] == CREDIT_COSTS["mentor_message"]
    assert _balance(db, user_id) == before - CREDIT_COSTS["mentor_message"]


def test_no_attached_context_forces_general_grounding(api, monkeypatch):
    token, _ = _register(api)
    reply = json.dumps({"blocks": [{"kind": "text", "text": "إجابة عامة عن Python.", "grounding": "general"}]})
    llm = FakeLLM(reply)
    monkeypatch.setattr(message_service, "get_llm", lambda: llm)

    response = _post_message(api, token, text="اشرح Python", context={})
    assert response.status_code == 200, response.text
    assert {block["grounding"] for block in response.json()["blocks"]} == {"general"}
    prompt = llm.calls[-1]["messages"][-1]["content"]
    assert "current_lesson" not in prompt and "recent_mistake" not in prompt


def test_one_learner_cannot_read_another_learners_mistake_context(api, db, monkeypatch):
    lesson, _, quiz, _ = _curriculum(db)
    token_a, user_a = _register(api)
    token_b, _ = _register(api)
    db.add(MentorEvidence(
        user_id=user_a, skill="PRIVATE-SKILL", correct=False, quiz_id=quiz.id,
        question_index=0, lesson_id=lesson.id, selected=1,
    ))
    db.commit()
    llm = FakeLLM(_valid(lesson.id))
    monkeypatch.setattr(message_service, "get_llm", lambda: llm)

    response = _post_message(
        api, token_b, context={"lessonId": str(lesson.id)},
        learnerId=user_a, mastery={"PRIVATE-SKILL": 0}, grades=[0], progress={"lesson": "failed"},
    )
    assert response.status_code == 200, response.text
    serialized_prompt = llm.calls[-1]["messages"][-1]["content"]
    assert "PRIVATE-SKILL" not in serialized_prompt
    assert "Learner selected" not in serialized_prompt


def test_failed_reply_is_refunded(api, db, monkeypatch):
    lesson, _, _, _ = _curriculum(db)
    token, user_id = _register(api)
    before = _balance(db, user_id)
    monkeypatch.setattr(message_service, "get_llm", lambda: FakeLLM(RuntimeError("provider down")))

    response = _post_message(api, token, context={"lessonId": str(lesson.id)})
    assert response.status_code == 503, response.text
    assert _balance(db, user_id) == before
    assert len(_txs(db, user_id, TransactionType.deduction)) == 1
    refunds = _txs(db, user_id, TransactionType.refund)
    assert len(refunds) == 1 and refunds[0].credits == CREDIT_COSTS["mentor_message"]


def test_selected_lesson_changes_context_without_reusing_previous_lesson(api, db, monkeypatch):
    first, _, _, _ = _curriculum(db)
    second, _, _, _ = _curriculum(db)
    second.content = "A second module discusses durable checkpoints."
    db.commit()
    token, _ = _register(api)
    llm = FakeLLM(_valid(first.id, "Graph memory stores graph state."), _valid(second.id, "Graph memory stores graph state."))
    monkeypatch.setattr(message_service, "get_llm", lambda: llm)

    one = _post_message(api, token, text="FIRST-COURSE-ONLY", context={"lessonId": str(first.id)})
    two = _post_message(api, token, text="SECOND-COURSE-ONLY", context={"lessonId": str(second.id)})

    assert one.status_code == 200, one.text
    assert two.status_code == 200, two.text
    first_prompt = llm.calls[0]["messages"][-1]["content"]
    second_prompt = llm.calls[1]["messages"][-1]["content"]
    assert f'"lessonId": {first.id}' in first_prompt
    assert f'"lessonId": {second.id}' in second_prompt
    assert first.content not in second_prompt
    assert "FIRST-COURSE-ONLY" not in second_prompt
    assert all("FIRST-COURSE-ONLY" not in item["content"] for item in llm.calls[1]["messages"])

    first_ref = api.get("/api/v1/mentor/context", headers=_auth(token), params={"lessonId": str(first.id)}).json()
    second_ref = api.get("/api/v1/mentor/context", headers=_auth(token), params={"lessonId": str(second.id)}).json()
    assert first_ref["courseId"] != second_ref["courseId"]
    assert first_ref["lessonId"] == str(first.id)
    assert second_ref["lessonId"] == str(second.id)


def test_context_endpoint_returns_the_verified_selected_lesson(api, db):
    lesson, exercise, _, _ = _curriculum(db)
    token, _ = _register(api)

    response = api.get(
        "/api/v1/mentor/context",
        headers=_auth(token),
        params={"lessonId": str(lesson.id), "exerciseId": str(exercise.id), "language": "en"},
    )

    assert response.status_code == 200, response.text
    assert response.json()["lessonId"] == str(lesson.id)
    assert response.json()["exerciseId"] == str(exercise.id)
    assert response.json()["lessonTitle"] == lesson.title


def test_invalid_explicit_lesson_never_falls_back_to_latest_progress(api, db):
    lesson, _, _, topic = _curriculum(db)
    token, user_id = _register(api)
    db.add(UserProgress(
        user_id=user_id, topic_id=topic.id, status=ProgressStatus.in_progress,
        lessons_completed=[], exercises_completed=[],
    ))
    db.commit()

    missing = lesson.id + 999_999
    response = api.get(
        "/api/v1/mentor/context", headers=_auth(token), params={"lessonId": str(missing)},
    )

    assert response.status_code == 404, response.text
    assert response.json()["detail"] == "Lesson not found"


def test_no_explicit_id_and_no_enrolment_attaches_nothing(api, db):
    # Progress in content the learner is not enrolled in is not the hub's default: the hub only
    # attaches courses the learner is taking (test_mentor_audit pins the enrolled default).
    first, _, _, topic = _curriculum(db)
    token, user_id = _register(api)
    db.add(UserProgress(
        user_id=user_id, topic_id=topic.id, status=ProgressStatus.in_progress,
        lessons_completed=[first.id], exercises_completed=[],
    ))
    db.commit()

    response = api.get("/api/v1/mentor/context", headers=_auth(token))

    assert response.status_code == 200, response.text
    assert response.json()["lessonId"] is None and response.json()["courseId"] is None


def test_successful_message_charges_once_and_insufficient_credit_is_distinct(api, db, monkeypatch):
    lesson, _, _, _ = _curriculum(db)
    token, user_id = _register(api)
    llm = FakeLLM(_valid(lesson.id))
    monkeypatch.setattr(message_service, "get_llm", lambda: llm)
    before = _balance(db, user_id)

    success = _post_message(api, token, context={"lessonId": str(lesson.id)})
    assert success.status_code == 200, success.text
    assert _balance(db, user_id) == before - CREDIT_COSTS["mentor_message"]
    assert len(_txs(db, user_id, TransactionType.deduction)) == 1

    wallet = db.query(UserWallet).filter(UserWallet.user_id == user_id).one()
    wallet.credit_balance = 0
    db.commit()
    denied = _post_message(api, token, context={"lessonId": str(lesson.id)})
    assert denied.status_code == 402, denied.text
    assert denied.json()["detail"]["error"] == "insufficient_credits"
    assert len(_txs(db, user_id, TransactionType.deduction)) == 1
    assert len(llm.calls) == 1, "insufficient credit must stop before another provider call"


def test_verified_proactive_reply_costs_zero(api, db, monkeypatch):
    lesson, _, _, topic = _curriculum(db)
    token, user_id = _register(api)
    db.add(UserProgress(
        user_id=user_id, topic_id=topic.id, status=ProgressStatus.in_progress,
        lessons_completed=[lesson.id], exercises_completed=[],
    ))
    db.commit()
    before = _balance(db, user_id)
    llm = FakeLLM(RuntimeError("must not be called"))
    monkeypatch.setattr(message_service, "get_llm", lambda: llm)

    response = api.post(MESSAGE, headers=_auth(token), json={
        "trigger": "lesson_completed", "context": {"lessonId": str(lesson.id)}, "language": "ar",
    })
    assert response.status_code == 200, response.text
    assert response.json()["creditCost"] == 0
    assert response.json()["proactive"]["trigger"] == "lesson_completed"
    assert _balance(db, user_id) == before
    assert llm.calls == []


def test_wrong_quiz_answer_guides_without_key_and_one_miss_keeps_learning(api, db):
    _, _, quiz, _ = _curriculum(db)
    token, user_id = _register(api)

    response = api.post(ANSWER, headers=_auth(token), json={
        "quizId": f"{quiz.id}:0", "optionId": "b", "language": "en",
    })
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["correct"] is False
    assert len(body["feedback"]) == 2
    assert body["feedback"][0]["kind"] == "text"
    assert body["feedback"][1]["kind"] == "check"
    assert "private-correct-token" not in response.text
    assert "correctOption" not in response.text and "correct_option" not in response.text
    assert body["skillDelta"]["status"] == "learning"
    assert db.query(MentorEvidence).filter(MentorEvidence.user_id == user_id).count() == 1

