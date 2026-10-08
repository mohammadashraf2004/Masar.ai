"""A mentor quiz question and its feedback follow the UI language, even though the authored
course quizzes are English-only (no Arabic twin)."""
import json

from app.models.mentor_translation import MentorQuizTranslation
from app.services.mentor.v2 import message as message_service
from app.services.mentor.v2 import translate
from tests.mentor_fixtures import FakeLLM, _auth, _register
from tests.test_mentor_v2 import ANSWER, MESSAGE, _curriculum

QUESTION = "Which `thread_id` value resumes the same conversation?"
OPTIONS = ["A stable thread_id", "A new graph each call", "A higher temperature"]
EXPLANATION = "The checkpointer keys state by thread_id."

AR = {
    "question": "أي قيمة `thread_id` تستأنف المحادثة نفسها؟",
    "options": ["thread_id ثابت", "graph جديد في كل استدعاء", "رفع قيمة temperature"],
    "explanation": "يربط الـ checkpointer الحالة بقيمة thread_id.",
}


def _english_only(db):
    """The curriculum fixture, with the quiz the way the real catalogue has it: English, no twin."""
    lesson, exercise, quiz, topic = _curriculum(db)
    quiz.questions = [{
        "lesson_id": quiz.questions[0]["lesson_id"], "question": QUESTION,
        "options": OPTIONS, "correct": 0, "explanation": EXPLANATION,
    }]
    quiz.questions_ar = None
    db.commit()
    return lesson, quiz


def _llm(monkeypatch, *replies):
    llm = FakeLLM(*[r if isinstance(r, (str, BaseException)) else json.dumps(r, ensure_ascii=False) for r in replies])
    monkeypatch.setattr(translate, "get_llm", lambda: llm)
    return llm


def _ask_quiz(api, token, lesson, language):
    return api.post(MESSAGE, headers=_auth(token), json={
        "text": "quiz me", "intent": "QUIZ", "context": {"lessonId": str(lesson.id)}, "language": language,
    })


def _quiz_block(response):
    assert response.status_code == 200, response.text
    return response.json()["blocks"][0]


def test_arabic_ui_gets_an_arabic_question_with_the_same_options_and_no_key(api, db, monkeypatch):
    lesson, quiz = _english_only(db)
    token, _ = _register(api)
    _llm(monkeypatch, AR)

    block = _quiz_block(_ask_quiz(api, token, lesson, "ar"))

    assert block["kind"] == "quiz" and block["lang"] == "ar"
    assert block["question"] == AR["question"]
    assert [o["text"] for o in block["options"]] == AR["options"]
    assert [o["id"] for o in block["options"]] == ["a", "b", "c"]
    assert block["quizId"] == f"{quiz.id}:0"
    assert "correct" not in block and "explanation" not in block


def test_english_ui_keeps_the_authored_question_and_calls_no_model(api, db, monkeypatch):
    lesson, _ = _english_only(db)
    token, _ = _register(api)
    llm = _llm(monkeypatch, RuntimeError("must not be called"))

    block = _quiz_block(_ask_quiz(api, token, lesson, "en"))

    assert block["lang"] == "en" and block["question"] == QUESTION
    assert llm.calls == []


def test_a_translation_is_made_once_and_reused(api, db, monkeypatch):
    lesson, quiz = _english_only(db)
    token, _ = _register(api)
    llm = _llm(monkeypatch, AR)

    first = _quiz_block(_ask_quiz(api, token, lesson, "ar"))
    second = _quiz_block(_ask_quiz(api, token, lesson, "ar"))

    assert first["question"] == second["question"] == AR["question"]
    assert len(llm.calls) == 1
    rows = db.query(MentorQuizTranslation).filter(MentorQuizTranslation.quiz_id == quiz.id).all()
    assert [(r.question_index, r.language) for r in rows] == [(0, "ar")]
    assert "correct" not in json.dumps(rows[0].payload)


def test_an_edited_question_is_translated_again(api, db, monkeypatch):
    lesson, quiz = _english_only(db)
    token, _ = _register(api)
    llm = _llm(monkeypatch, AR)
    _ask_quiz(api, token, lesson, "ar")

    quiz.questions = [{**quiz.questions[0], "question": QUESTION + " Why?"}]
    db.commit()
    _ask_quiz(api, token, lesson, "ar")

    assert len(llm.calls) == 2
    assert db.query(MentorQuizTranslation).filter(MentorQuizTranslation.quiz_id == quiz.id).count() == 1


def test_a_hand_written_arabic_twin_is_used_without_a_model(api, db, monkeypatch):
    lesson, _, quiz, _ = _curriculum(db)  # the fixture's quiz has an Arabic twin
    token, _ = _register(api)
    llm = _llm(monkeypatch, RuntimeError("must not be called"))

    block = _quiz_block(_ask_quiz(api, token, lesson, "ar"))

    assert block["lang"] == "ar" and block["question"] == quiz.questions_ar[0]["question"]
    assert llm.calls == []


def test_a_translation_that_does_not_line_up_is_rejected_and_the_authored_text_shown(api, db, monkeypatch):
    lesson, _ = _english_only(db)
    token, _ = _register(api)
    llm = _llm(monkeypatch, {**AR, "options": AR["options"][:2]})  # an option went missing, twice

    block = _quiz_block(_ask_quiz(api, token, lesson, "ar"))

    assert block["lang"] == "en" and block["question"] == QUESTION
    assert len(llm.calls) == 2


def test_a_translation_that_changes_code_is_rejected():
    source = translate._source({"question": QUESTION, "options": OPTIONS, "explanation": EXPLANATION})
    assert translate.accept(source, AR) is not None
    renamed = {**AR, "options": ["معرّف_خيط ثابت", *AR["options"][1:]]}  # thread_id was translated away
    assert translate.accept(source, renamed) is None
    merged = {**AR, "options": [AR["options"][0], AR["options"][0], AR["options"][2]]}
    assert translate.accept(source, merged) is None


def test_a_provider_failure_still_serves_the_quiz(api, db, monkeypatch):
    lesson, _ = _english_only(db)
    token, _ = _register(api)
    _llm(monkeypatch, RuntimeError("provider down"))

    block = _quiz_block(_ask_quiz(api, token, lesson, "ar"))

    assert block["lang"] == "en" and block["question"] == QUESTION


def test_quiz_feedback_follows_the_ui_language_and_never_gives_the_key(api, db, monkeypatch):
    _, quiz = _english_only(db)
    token, _ = _register(api)
    _llm(monkeypatch, AR)

    right = api.post(ANSWER, headers=_auth(token), json={"quizId": f"{quiz.id}:0", "optionId": "a", "language": "ar"})
    assert right.status_code == 200, right.text
    assert AR["explanation"] in right.json()["feedback"][0]["text"]
    assert EXPLANATION not in right.text

    wrong = api.post(ANSWER, headers=_auth(token), json={"quizId": f"{quiz.id}:0", "optionId": "b", "language": "ar"})
    assert wrong.status_code == 200, wrong.text
    text = wrong.json()["feedback"][0]["text"]
    assert AR["question"] in text and QUESTION not in text
    assert AR["options"][0] not in wrong.text  # the right option is never named


def test_the_same_question_can_be_fetched_in_the_other_language(api, db, monkeypatch):
    _, quiz = _english_only(db)
    token, user_id = _register(api)
    _llm(monkeypatch, AR)

    arabic = api.get(f"/api/v1/mentor/quiz/{quiz.id}:0?language=ar", headers=_auth(token))
    english = api.get(f"/api/v1/mentor/quiz/{quiz.id}:0?language=en", headers=_auth(token))

    assert arabic.status_code == english.status_code == 200
    assert (arabic.json()["lang"], arabic.json()["question"]) == ("ar", AR["question"])
    assert (english.json()["lang"], english.json()["question"]) == ("en", QUESTION)
    assert arabic.json()["quizId"] == english.json()["quizId"] == f"{quiz.id}:0"
    assert [o["id"] for o in arabic.json()["options"]] == [o["id"] for o in english.json()["options"]]
    assert "correct" not in arabic.text and "explanation" not in arabic.text


def test_fetching_a_question_needs_a_valid_reference_and_a_login(api, db):
    _, quiz = _english_only(db)
    token, _ = _register(api)
    assert api.get(f"/api/v1/mentor/quiz/{quiz.id}:0?language=ar").status_code in (401, 403)
    assert api.get("/api/v1/mentor/quiz/nope?language=ar", headers=_auth(token)).status_code == 422
    assert api.get(f"/api/v1/mentor/quiz/{quiz.id}:9?language=ar", headers=_auth(token)).status_code == 404
    assert api.get(f"/api/v1/mentor/quiz/{quiz.id}:0?language=fr", headers=_auth(token)).status_code == 422


def test_the_reply_language_policy_overrides_the_language_of_earlier_turns():
    english = message_service._language_policy("en")
    arabic = message_service._language_policy("ar")
    assert "Reply in English" in english and "another language" in english
    assert "Arabic-first" in arabic and "English" in arabic and "Reply in English" not in arabic
