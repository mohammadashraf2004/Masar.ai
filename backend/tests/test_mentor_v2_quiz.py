"""POST /mentor/quiz/answer — server-graded single questions.

Pins down: the correct option never reaches the client, a wrong answer
gets a guiding question and a smaller follow-up (never the answer), skill
state moves only on repeated evidence, and the mistake is stored for
later /mentor/message replies.
"""
import json

import pytest

from app.models.progress import MentorQuizAnswer, UserSkillScore
from tests.mentor_v2_fixtures import (
    CORRECT_OPTION, MESSAGE, QUIZ_ANSWER, blocks_json, install_llm, make_course, register,
)


@pytest.fixture()
def course():
    return make_course()


def _answer(client, headers, course, choice, **extra):
    resp = client.post(QUIZ_ANSWER, headers=headers, json={
        "quizId": course["quiz"], "questionIndex": 0, "choice": choice, **extra})
    assert resp.status_code == 200, resp.text
    return resp.json()


def test_wrong_answer_never_returns_the_correct_option(client, course):
    headers, _ = register(client)
    body = _answer(client, headers, course, 1, lessonId=course["lesson"])

    assert body["correct"] is False
    dumped = json.dumps(body, ensure_ascii=False).lower()
    assert CORRECT_OPTION.lower() not in dumped
    assert "snapshot per node" not in dumped  # nor the explanation, which gives it away
    assert not {"correctIndex", "correct_index", "answer", "explanation"} & set(body)


def test_wrong_answer_gets_a_guiding_question_and_a_smaller_follow_up(client, course):
    headers, _ = register(client)
    body = _answer(client, headers, course, 2, lessonId=course["lesson"])

    kinds = [b["kind"] for b in body["feedback"]]
    assert kinds == ["hint", "check"]
    guide, follow = (b["text"] for b in body["feedback"])
    assert guide.rstrip().endswith(("?", "؟", "»", '"'))
    assert follow.rstrip().endswith(("?", "؟"))
    assert all(b["grounding"] == "lesson" for b in body["feedback"])


def test_correct_answer_is_confirmed_with_the_explanation(client, course):
    headers, _ = register(client)
    body = _answer(client, headers, course, 0)
    assert body["correct"] is True
    assert "snapshot per node" in body["feedback"][0]["text"]
    assert body["skillDelta"]["skill"] == "Checkpointers"
    assert body["skillDelta"]["after"] > body["skillDelta"]["before"]


def test_one_wrong_answer_does_not_flip_a_skill_to_needs_review(client, db, course):
    headers, user_id = register(client)
    for _ in range(3):
        _answer(client, headers, course, 0)
    db.expire_all()
    row = db.query(UserSkillScore).filter_by(user_id=user_id, skill_name="Checkpointers").one()
    score_before = row.score

    first_wrong = _answer(client, headers, course, 1)
    assert first_wrong["skillDelta"] is None  # no confidence change, so no delta
    db.expire_all()
    assert db.query(UserSkillScore).filter_by(user_id=user_id, skill_name="Checkpointers").one().score == score_before

    # A second wrong answer is repeated evidence: now it moves.
    second_wrong = _answer(client, headers, course, 2)
    delta = second_wrong["skillDelta"]
    assert delta is not None
    assert delta["after"] < delta["before"]
    assert delta["status"] == "needs_review"
    assert delta["previousStatus"] != "needs_review"


def test_mistake_is_stored_and_used_by_later_replies(client, db, monkeypatch, course):
    headers, user_id = register(client)
    _answer(client, headers, course, 1, lessonId=course["lesson"])

    db.expire_all()
    row = db.query(MentorQuizAnswer).filter_by(user_id=user_id).one()
    assert row.is_correct is False and row.skill_name == "Checkpointers" and row.lesson_id == course["lesson"]

    fake = install_llm(monkeypatch, [blocks_json({"kind": "text", "grounding": "general", "text": "ok"})])
    client.post(MESSAGE, headers=headers, json={
        "content": "explain the checkpointer", "lessonId": course["lesson"], "intent": "explain"})
    prompt = fake.prompts()
    assert "## RECENT MISTAKES" in prompt
    assert "Checkpointers: When does LangGraph call the checkpointer?" in prompt


def test_out_of_range_choice_and_unknown_question(client, course):
    headers, _ = register(client)
    r = client.post(QUIZ_ANSWER, headers=headers, json={"quizId": course["quiz"], "questionIndex": 0, "choice": 9})
    assert r.status_code == 422
    r = client.post(QUIZ_ANSWER, headers=headers, json={"quizId": course["quiz"], "questionIndex": 5, "choice": 0})
    assert r.status_code == 404
    r = client.post(QUIZ_ANSWER, headers=headers, json={"quizId": 987654321, "questionIndex": 0, "choice": 0})
    assert r.status_code == 404
