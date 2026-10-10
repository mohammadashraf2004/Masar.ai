"""
Guided exercises (app/services/curriculum/guided): every coding task in the
catalogue is a short, bilingual fill-in-the-blank exercise with hidden,
deterministic checks.

These tests hold the registry to that promise against the real course
folders: each definition lands on an existing exercise, its official
solution passes, its untouched starter is reported as unfinished, a wrong
value in a blank is rejected, and both languages carry the full brief.
"""
import asyncio
import re
from collections import Counter

import pytest

from app.models.learning import Exercise
from app.models.progress import UserProgress
from app.services.code_execution.python_runner import LocalPythonRunner
from app.services.code_exercises import check_without_running, grader_for_language
from app.services.code_grading import PythonGrader, SQLGrader, TextGrader
from app.services.code_grading.authoring import count_python_blanks
from app.services.code_grading.grader import is_static_only
from app.services.curriculum import importer, validate
from app.services.curriculum.guided import BLANK, Guided, build, eq, fill, registry
from app.services.curriculum.loaders import load_all_courses
from seeds import curriculum as cfg
from tests.curriculum_fixtures import import_small_courses, make_spec
from tests.learning_fixtures import *  # noqa: F401,F403

DEFINITIONS = registry()
GUIDED_IDS = sorted(DEFINITIONS)
RUNNER = LocalPythonRunner(timeout_seconds=20)
PYTHON = PythonGrader(RUNNER)
TEXT = TextGrader()
SQL = SQLGrader()


@pytest.fixture(scope="module")
def courses():
    return load_all_courses()


@pytest.fixture(scope="module")
def by_id(courses):
    found = Counter(e.exercise_id for c in courses for lesson in c.lessons for e in lesson.exercises)
    assert not [eid for eid, count in found.items() if count > 1], "duplicate exercise ids"
    return {e.exercise_id: e for c in courses for lesson in c.lessons for e in lesson.exercises}


def _grade(fields, code):
    language = fields["language"]
    if language == "python":
        return asyncio.run(PYTHON.grade(code, fields["tests"], pre_exercise_code=fields["pre_exercise_code"] or ""))
    grader = SQL if language == "sql" else TEXT
    return asyncio.run(grader.grade(code, fields["tests"]))


def _with_blank(guided: Guided, fields, index: int, value: str) -> str:
    """The completed program with blank ``index`` (0-based) set to ``value``."""
    answers = list(guided.answers)
    answers[index] = value
    return fill(fields["starter_code"], tuple(answers))


def _numbered(text: str) -> int:
    return len(re.findall(r"(?m)^\d+\. ", text))


def _arabic(text: str) -> bool:
    return any("؀" <= ch <= "ۿ" for ch in text)


# ─── The catalogue ──────────────────────────────────────────────────────────

def test_every_guided_definition_lands_on_one_existing_exercise_unchanged(by_id):
    assert len(DEFINITIONS) >= 229
    missing = [eid for eid in GUIDED_IDS if eid not in by_id]
    assert not missing
    for exercise_id in GUIDED_IDS:
        exercise = by_id[exercise_id]
        fields = build(exercise_id, DEFINITIONS[exercise_id])
        # The loader applied this definition (same starter, checks and brief).
        for name, value in fields.items():
            assert getattr(exercise, name) == value, (exercise_id, name)


def test_every_code_exercise_has_a_complete_code_cell(courses, by_id):
    assert validate.code_exercise_problems(courses) == []
    code = {eid: e for eid, e in by_id.items() if e.exercise_type == "code"}
    assert len(code) >= len(DEFINITIONS)
    for exercise_id, exercise in code.items():
        assert grader_for_language(exercise.language) is not None, exercise_id
        assert exercise.starter_code and exercise.starter_code.strip(), exercise_id
        assert exercise.solution_code and exercise.tests, exercise_id
        assert exercise.starter_code != exercise.solution_code, exercise_id


def test_sql_starters_show_only_bare_blanks_and_are_still_graded_blank_by_blank(by_id):
    sql = {eid: e for eid, e in by_id.items() if e.exercise_type == "code" and e.language == "sql"}
    assert sql
    for exercise_id, exercise in sql.items():
        for code in (exercise.starter_code, exercise.solution_code):
            assert "blank:" not in code and "endblank" not in code, exercise_id
        untouched = asyncio.run(SQL.grade(exercise.starter_code, exercise.tests))
        assert (untouched.feedback_code, untouched.failed_test_id) == ("BLANK_INCORRECT", "blank_1"), exercise_id
        assert asyncio.run(SQL.grade(exercise.solution_code, exercise.tests)).passed, exercise_id


def test_every_exercise_uses_a_known_interaction_and_nothing_is_run_only(by_id):
    types = Counter(e.exercise_type for e in by_id.values())
    assert set(types) == {"code", "legacy"}, types
    for exercise_id, exercise in by_id.items():
        if exercise.exercise_type == "legacy":
            # A written answer: no editor, no hidden checks, no solution to leak.
            assert not exercise.tests and not exercise.solution_code, exercise_id


@pytest.mark.parametrize("exercise_id", [
    # Design write-ups and questionnaires that had been queued as code.
    "COURSE-004.M02.L01.EX02", "COURSE-006.M02.L01.EX02", "COURSE-006.M08.L01.EX02",
    "COURSE-006.M08.L01.EX03", "COURSE-012.M01.L08.EX01", "COURSE-012.M01.L08.EX02",
    "COURSE-014.M09.L01.EX02", "COURSE-014.M10.L01.EX02", "COURSE-015.M01.L05.EX03",
    "COURSE-015.M01.L07.EX04", "COURSE-016.M14.L01.EX04",
])
def test_conceptual_tasks_stay_written_answers(by_id, exercise_id):
    exercise = by_id[exercise_id]
    assert exercise.exercise_type == "legacy"
    assert exercise_id not in DEFINITIONS


def test_every_exercise_brief_has_numbered_steps_in_both_languages(courses, by_id):
    for exercise_id, exercise in by_id.items():
        assert "**Instructions**" in (exercise.description or ""), exercise_id
        assert "**التعليمات**" in (exercise.description_ar or ""), exercise_id
        assert _numbered(exercise.description) == _numbered(exercise.description_ar), exercise_id
        # Every brief is a numbered list of steps. The one exception lays out
        # two labelled flows under bold sub-headings instead.
        if exercise_id != "COURSE-010.M01.L05.EX05":
            assert _numbered(exercise.description) > 0, exercise_id
    # No Arabic file was translated from an older version of its English.
    stale = [w for c in courses for w in c.arabic_warnings if "source_hash differs" in w]
    assert stale == []


@pytest.mark.parametrize("exercise_id", GUIDED_IDS)
def test_guided_definition_is_complete_in_both_languages(exercise_id):
    guided = DEFINITIONS[exercise_id]
    fields = build(exercise_id, guided)
    assert 1 <= guided.starter.count(BLANK) <= 5
    for en, ar in (*guided.hints, *guided.blanks):
        assert en.strip() and ar.strip(), exercise_id
    # Feedback on a blank may be just the code it expects; the prose may not.
    for en, ar in (guided.goal, guided.success, *guided.steps):
        assert en.strip() and _arabic(ar), (exercise_id, ar)
    assert any(_arabic(ar) for _en, ar in guided.hints), exercise_id
    # Progressive hints and numbered steps: the same ladder in both languages.
    assert len(fields["hint"].split("\n\n")) == len(fields["hint_ar"].split("\n\n")) == len(guided.hints)
    assert _numbered(fields["description"]) == _numbered(fields["description_ar"]) >= len(guided.steps)
    for test in fields["tests"]:
        feedback = test.get("feedback")
        if isinstance(feedback, dict):
            assert feedback.get("en") and feedback.get("ar"), (exercise_id, test["id"])
    # The solution is the starter with its blanks filled, and nothing else.
    assert BLANK not in fields["solution_code"]
    if fields["language"] == "python":
        assert count_python_blanks(fields["solution_code"]) == 0


# ─── Grading ────────────────────────────────────────────────────────────────

@pytest.mark.parametrize("exercise_id", GUIDED_IDS)
def test_guided_solution_passes_and_the_untouched_starter_does_not(exercise_id):
    fields = build(exercise_id, DEFINITIONS[exercise_id])
    solution = _grade(fields, fields["solution_code"])
    assert solution.passed, (solution.failed_test_id, solution.feedback, solution.execution.stderr[-400:])
    assert solution.tests_passed == solution.tests_total

    starter = _grade(fields, fields["starter_code"])
    assert not starter.passed
    if fields["language"] == "python":
        assert starter.feedback_code == "BLANKS_REMAINING"


def _mutation_sample():
    """Every exercise graded without execution, plus the first runnable
    Python exercise of each course (the full set runs in verify tooling)."""
    picked, seen = [], set()
    for exercise_id in GUIDED_IDS:
        fields = build(exercise_id, DEFINITIONS[exercise_id])
        runnable = fields["language"] == "python" and not is_static_only(fields["tests"])
        course = exercise_id.split(".", 1)[0]
        if not runnable:
            picked.append(exercise_id)
        elif course not in seen:
            seen.add(course)
            picked.append(exercise_id)
    return picked


@pytest.mark.parametrize("exercise_id", _mutation_sample())
def test_a_wrong_value_in_any_blank_is_rejected_and_alternatives_are_accepted(exercise_id):
    guided = DEFINITIONS[exercise_id]
    fields = build(exercise_id, guided)
    wrong_value = "None" if fields["language"] == "python" else "WRONG_VALUE"
    for index, answer in enumerate(guided.answers):
        wrong = "0" if answer.strip() == wrong_value else wrong_value
        result = _grade(fields, _with_blank(guided, fields, index, wrong))
        assert not result.passed, f"blank {index + 1} accepts a wrong value"
    for number, options in guided.alternatives.items():
        for option in options:
            if option.startswith("re:"):
                continue
            result = _grade(fields, _with_blank(guided, fields, number - 1, option))
            assert result.passed, (number, option, result.failed_test_id)


def test_a_static_exercise_accepts_an_equivalent_blank_and_names_the_wrong_one():
    exercise_id = next(
        eid for eid in GUIDED_IDS
        if DEFINITIONS[eid].language == "python" and not DEFINITIONS[eid].checks and DEFINITIONS[eid].alternatives
    )
    guided = DEFINITIONS[exercise_id]
    fields = build(exercise_id, guided)
    number, options = next(iter(guided.alternatives.items()))
    assert _grade(fields, _with_blank(guided, fields, number - 1, options[0])).passed
    rejected = _grade(fields, _with_blank(guided, fields, number - 1, "None"))
    assert rejected.failed_test_id == f"blank_{number}"
    assert rejected.feedback["en"].startswith(f"Blank {number}:")
    assert rejected.feedback["ar"].startswith(f"الفراغ {number}:")


def test_grading_distinguishes_blanks_syntax_runtime_and_wrong_answers():
    guided = Guided(
        goal=("Add up the scores.", "اجمع الدرجات."),
        steps=(("Fill the blank with the total.", "املأ الفراغ بالمجموع."),),
        starter="scores = [3, 4, 5]\ntotal = ___\n",
        answers=("sum(scores)",),
        hints=(("Python has a built-in for this.", "في Python دالة جاهزة لذلك."),),
        success=("Correct.", "صحيح."),
        checks=(eq("total", 12, "The total should be 12.", "يجب أن يكون المجموع 12."),),
    )
    fields = build("TEST.EX01", guided)

    blanks = _grade(fields, fields["starter_code"])
    assert (blanks.feedback_code, blanks.status) == ("BLANKS_REMAINING", "incorrect")
    assert "line 2" in blanks.feedback["en"] and "السطر 2" in blanks.feedback["ar"]

    syntax = _grade(fields, "scores = [3, 4, 5]\ntotal = sum(scores\n")
    assert syntax.status == "syntax_error"
    assert "syntax error" in syntax.feedback["en"] and "خطأ في الصياغة" in syntax.feedback["ar"]

    runtime = _grade(fields, "scores = [3, 4, 5]\ntotal = sum(scores) / 0\n")
    assert runtime.status == "runtime_error"
    assert "ZeroDivisionError" in runtime.feedback["en"] and "توقف بسبب خطأ" in runtime.feedback["ar"]

    wrong = _grade(fields, "scores = [3, 4, 5]\ntotal = max(scores)\n")
    assert (wrong.status, wrong.passed) == ("incorrect", False)
    assert wrong.feedback == {"en": "The total should be 12.", "ar": "يجب أن يكون المجموع 12."}

    # Behaviour is graded, not text: any correct expression passes.
    for answer in ("sum(scores)", "3 + 4 + 5", "scores[0] + scores[1] + scores[2]"):
        assert _grade(fields, f"scores = [3, 4, 5]\ntotal = {answer}\n").passed, answer


def test_run_on_a_static_exercise_checks_syntax_and_explains_why_it_does_not_execute():
    ok = check_without_running("import torch\nmodel = torch.nn.Linear(2, 1)\n", "en")
    assert ok.status == "success" and "torch" in ok.stdout and "Check answer" in ok.stdout
    assert "بقراءة بنيته" in check_without_running("import torch\n", "ar").stdout
    assert check_without_running("def broken(:\n", "en").status == "syntax_error"


# ─── Import and learner progress ────────────────────────────────────────────

def test_converting_a_written_exercise_to_guided_code_keeps_its_id_and_progress(learn_db, learn_catalog):
    import_small_courses(learn_db, ["COURSE-001"])

    def lesson_rows():
        return {
            row.source_key: row
            for row in learn_db.query(Exercise).filter(Exercise.source_key.like("COURSE-001/L001-0101/x%"))
        }

    before = {key: (row.id, row.exercise_type) for key, row in lesson_rows().items()}
    assert before and all(kind != "code" for _id, kind in before.values())
    topic_id = next(iter(lesson_rows().values())).tool_topic_id
    completed = sorted(row_id for row_id, _kind in before.values())

    from app.models.user import User
    user = User(email="guided-progress@example.com", hashed_password="x", full_name="G")
    learn_db.add(user)
    learn_db.flush()
    learn_db.add(UserProgress(user_id=user.id, tool_topic_id=topic_id, exercises_completed=completed))
    learn_db.commit()

    spec = make_spec("COURSE-001")
    target = spec.modules[0].lessons[0].exercises[0]
    guided = next(DEFINITIONS[eid] for eid in GUIDED_IDS if DEFINITIONS[eid].language == "python")
    for name, value in build(target.exercise_id, guided).items():
        setattr(target, name, value)
    definition = {d["course_id"]: d for d in cfg.COURSE_DIRECTORY_COURSES}["COURSE-001"]
    importer.import_course(learn_db, spec, definition)
    learn_db.commit()

    learn_db.expire_all()
    after = lesson_rows()
    assert {key: row.id for key, row in after.items()} == {key: row_id for key, (row_id, _k) in before.items()}
    converted = [row for row in after.values() if row.exercise_type == "code"]
    assert len(converted) == 1
    assert converted[0].starter_code == target.starter_code and converted[0].hint_ar
    progress = learn_db.query(UserProgress).filter(UserProgress.user_id == user.id).one()
    assert progress.exercises_completed == completed
