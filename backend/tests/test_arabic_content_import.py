"""
Tests for the Arabic content workbook (seeds/arabic_content.py).

The import writes to production content tables, so the tests are weighted
towards what must NOT happen: English must never be modified, a bad workbook
must write nothing at all, and a quiz's answer key must survive translation
intact. The happy path is the smallest part of this file on purpose.
"""
import uuid

import pytest

from app.db.session import SessionLocal
from app.models.learning import (
    CareerTrack, DifficultyLevel, Lesson, Quiz, Topic, TrackLevel,
)
from seeds.arabic_content import (
    ImportError_, apply_workbook, coverage, export_workbook,
)

WORKBOOK_FORMAT = "masar-arabic-workbook/1"


# ─── fixtures ─────────────────────────────────────────────────────────────

@pytest.fixture()
def content(db):
    """A track → level → topic → lesson + quiz chain to translate."""
    suffix = uuid.uuid4().hex[:8]
    track = CareerTrack(
        slug=f"ar-test-{suffix}", title="Arabic Import Track",
        description="English description", is_active=True, estimated_weeks=4,
    )
    db.add(track)
    db.flush()

    level = TrackLevel(track_id=track.id, title="Foundations", order=1)
    db.add(level)
    db.flush()

    topic = Topic(
        level_id=level.id, title="Retrieval", slug=f"retrieval-{suffix}", order=1,
        difficulty=DifficultyLevel.beginner, estimated_hours=2,
        skill_tags=["rag"],
    )
    db.add(topic)
    db.flush()

    lesson = Lesson(
        topic_id=topic.id, title="What is RAG?", order=1,
        content="# English body\n\nSome text.",
    )
    quiz = Quiz(
        topic_id=topic.id, title="RAG quiz", passing_score=70,
        questions=[
            {
                "question": "What does RAG stand for?",
                "options": ["A", "B", "C"],
                "correct": 2,
                "explanation": "Because C.",
            },
            {
                "question": "Why chunk documents?",
                "options": ["X", "Y"],
                "correct": 0,
                "explanation": "Because X.",
            },
        ],
    )
    db.add_all([lesson, quiz])
    db.commit()

    return {"track": track, "level": level, "topic": topic, "lesson": lesson, "quiz": quiz}


def _record(table, row_id, path="test", en=None, ar=None):
    return {"table": table, "id": row_id, "path": path, "en": en or {}, "ar": ar or {}}


def _workbook(*records):
    return {"format": WORKBOOK_FORMAT, "records": list(records)}


def _reload(db, model, row_id):
    db.expire_all()
    return db.query(model).filter(model.id == row_id).first()


# ─── export ───────────────────────────────────────────────────────────────

def test_export_includes_english_and_a_blank_arabic_slot(db, content):
    book = export_workbook(db, only={"lessons"})
    entry = next(r for r in book["records"] if r["id"] == content["lesson"].id)

    assert book["format"] == WORKBOOK_FORMAT
    assert entry["en"]["content"] == "# English body\n\nSome text."
    assert entry["ar"]["content_ar"] == ""
    assert entry["ar"]["title_ar"] == ""


def test_export_quiz_skeleton_mirrors_option_counts_and_omits_the_answer_key(db, content):
    book = export_workbook(db, only={"quizzes"})
    entry = next(r for r in book["records"] if r["id"] == content["quiz"].id)

    skeleton = entry["ar"]["questions_ar"]
    assert [len(q["options"]) for q in skeleton] == [3, 2]
    # Nothing for a translator to get wrong: the answer key is not in the file.
    assert all("correct" not in q for q in skeleton)


# ─── dry run ──────────────────────────────────────────────────────────────

def test_dry_run_writes_nothing(db, content):
    lesson_id = content["lesson"].id
    book = _workbook(_record("lessons", lesson_id, ar={"title_ar": "ما هو RAG؟"}))

    outcome = apply_workbook(db, book, apply=False)
    assert outcome.updated == 1

    assert _reload(db, Lesson, lesson_id).title_ar is None


# ─── applying ─────────────────────────────────────────────────────────────

def test_apply_writes_arabic_and_leaves_english_untouched(db, content):
    lesson_id = content["lesson"].id
    book = _workbook(_record("lessons", lesson_id, ar={
        "title_ar": "ما هو RAG؟",
        "content_ar": "# شرح بالعربية\n\nنص.",
    }))

    outcome = apply_workbook(db, book, apply=True)
    assert outcome.updated == 1
    assert outcome.fields_written == 2

    lesson = _reload(db, Lesson, lesson_id)
    assert lesson.title_ar == "ما هو RAG؟"
    assert lesson.content_ar.startswith("# شرح بالعربية")
    assert lesson.title == "What is RAG?"
    assert lesson.content == "# English body\n\nSome text."


def test_rerunning_the_same_workbook_changes_nothing(db, content):
    lesson_id = content["lesson"].id
    book = _workbook(_record("lessons", lesson_id, ar={"title_ar": "ما هو RAG؟"}))

    first = apply_workbook(db, book, apply=True)
    second = apply_workbook(db, book, apply=True)

    assert first.updated == 1
    assert second.updated == 0
    assert second.unchanged == 1
    assert second.fields_written == 0


def test_blank_arabic_does_not_overwrite_existing_content(db, content):
    lesson_id = content["lesson"].id
    apply_workbook(db, _workbook(_record("lessons", lesson_id, ar={"title_ar": "عنوان"})), apply=True)

    # A workbook where the author left this one blank must not erase it.
    apply_workbook(db, _workbook(_record("lessons", lesson_id, ar={"title_ar": "   "})), apply=True)

    assert _reload(db, Lesson, lesson_id).title_ar == "عنوان"


def test_missing_row_is_reported_not_fatal(db, content):
    lesson_id = content["lesson"].id
    book = _workbook(
        _record("lessons", 9_999_999, ar={"title_ar": "يتيم"}),
        _record("lessons", lesson_id, ar={"title_ar": "عنوان"}),
    )

    outcome = apply_workbook(db, book, apply=True)
    assert outcome.skipped == 1
    assert outcome.updated == 1
    assert any("no such row" in p for p in outcome.problems)
    assert _reload(db, Lesson, lesson_id).title_ar == "عنوان"


def test_changed_english_is_flagged_but_still_applied(db, content):
    lesson_id = content["lesson"].id
    book = _workbook(_record(
        "lessons", lesson_id,
        en={"title": "A DIFFERENT English title than the row has"},
        ar={"title_ar": "عنوان"},
    ))

    outcome = apply_workbook(db, book, apply=True)
    assert any("changed since export" in p for p in outcome.problems)
    assert _reload(db, Lesson, lesson_id).title_ar == "عنوان"


# ─── transactional behaviour ──────────────────────────────────────────────

def test_a_later_bad_record_rolls_back_the_earlier_good_one(db, content):
    """The whole point of one transaction: no half-imported catalogue."""
    lesson_id, quiz_id = content["lesson"].id, content["quiz"].id
    book = _workbook(
        _record("lessons", lesson_id, ar={"title_ar": "عنوان صحيح"}),
        # Two Arabic questions were expected; one is supplied.
        _record("quizzes", quiz_id, ar={"questions_ar": [
            {"question": "س؟", "options": ["أ", "ب", "ج"]},
        ]}),
    )

    with pytest.raises(ImportError_):
        apply_workbook(db, book, apply=True)

    assert _reload(db, Lesson, lesson_id).title_ar is None


def test_unknown_format_is_refused(db):
    with pytest.raises(ImportError_):
        apply_workbook(db, {"format": "something-else", "records": []}, apply=True)


def test_unknown_table_is_refused(db, content):
    with pytest.raises(ImportError_):
        apply_workbook(
            db, _workbook(_record("wallets", 1, ar={"title_ar": "x"})), apply=True
        )


# ─── quiz safety ──────────────────────────────────────────────────────────

def test_quiz_answer_key_is_copied_from_english_not_the_file(db, content):
    quiz_id = content["quiz"].id
    book = _workbook(_record("quizzes", quiz_id, ar={"questions_ar": [
        {"question": "ماذا يعني RAG؟", "options": ["أ", "ب", "ج"]},
        {"question": "لماذا نقسّم المستندات؟", "options": ["س", "ص"]},
    ]}))

    apply_workbook(db, book, apply=True)

    quiz = _reload(db, Quiz, quiz_id)
    assert [q["correct"] for q in quiz.questions_ar] == [2, 0]
    # English blob — the one grading actually reads — is untouched.
    assert [q["correct"] for q in quiz.questions] == [2, 0]
    assert quiz.questions[0]["question"] == "What does RAG stand for?"


def test_quiz_rejects_a_different_option_count(db, content):
    """Option order and count carry the answer key, because the client
    submits a positional index graded against the English list."""
    quiz_id = content["quiz"].id
    book = _workbook(_record("quizzes", quiz_id, ar={"questions_ar": [
        {"question": "ماذا يعني RAG؟", "options": ["أ", "ب"]},          # 2, needs 3
        {"question": "لماذا نقسّم المستندات؟", "options": ["س", "ص"]},
    ]}))

    with pytest.raises(ImportError_, match="options against"):
        apply_workbook(db, book, apply=True)
    assert _reload(db, Quiz, quiz_id).questions_ar is None


def test_quiz_rejects_an_answer_key_supplied_by_the_author(db, content):
    quiz_id = content["quiz"].id
    book = _workbook(_record("quizzes", quiz_id, ar={"questions_ar": [
        {"question": "ماذا يعني RAG؟", "options": ["أ", "ب", "ج"], "correct": 0},
        {"question": "لماذا نقسّم المستندات؟", "options": ["س", "ص"]},
    ]}))

    with pytest.raises(ImportError_, match="remove correct"):
        apply_workbook(db, book, apply=True)


def test_quiz_rejects_a_partially_translated_question_set(db, content):
    quiz_id = content["quiz"].id
    book = _workbook(_record("quizzes", quiz_id, ar={"questions_ar": [
        {"question": "ماذا يعني RAG؟", "options": ["أ", "ب", "ج"]},
        {"question": "", "options": ["", ""]},
    ]}))

    with pytest.raises(ImportError_, match="fully Arabic or fully English"):
        apply_workbook(db, book, apply=True)


def test_quiz_left_entirely_blank_is_simply_skipped(db, content):
    quiz_id = content["quiz"].id
    book = _workbook(_record("quizzes", quiz_id, ar={
        "title_ar": "اختبار RAG", "questions_ar": [],
    }))

    outcome = apply_workbook(db, book, apply=True)
    assert outcome.updated == 1  # the title was written

    quiz = _reload(db, Quiz, quiz_id)
    assert quiz.title_ar == "اختبار RAG"
    # Not an empty list: the reader treats null as "no Arabic version".
    assert quiz.questions_ar is None


# ─── coverage reporting ───────────────────────────────────────────────────

def test_coverage_counts_move_only_after_apply(db, content):
    def lessons_with_arabic():
        return dict(
            (name, counts) for name, _total, counts in coverage(db)
        )["lessons"]["title_ar"]

    before = lessons_with_arabic()
    book = _workbook(_record("lessons", content["lesson"].id, ar={"title_ar": "عنوان"}))

    apply_workbook(db, book, apply=False)
    assert lessons_with_arabic() == before

    apply_workbook(db, book, apply=True)
    assert lessons_with_arabic() == before + 1
