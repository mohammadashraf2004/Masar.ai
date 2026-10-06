"""
Regression coverage for the curriculum loader (`app/services/curriculum/loaders.py`).

COURSE-015 ships its real content one directory deeper than every other
course - inside a redundant `COURSE-015/` folder nested under the outer
`COURSE-015_Voice_AI_Engineering_Real_Time_Voice_Agents/` folder (an
extraction artifact) - and uses its own file convention (bare `M0XX-NN/`
module directories with `module_manifest.json`, and bare `L0XX-NNN.py`
lesson files instead of the descriptive-slug names other courses use).
`load_course_dir` detects and unwraps that nesting generically (by name, not by
course id), and a layout function reads the bare-numbered convention. These
tests pin that behaviour down so a future change cannot silently break
COURSE-015, and exercise all sixteen course folders.
"""
import base64
import json

import pytest

from app.services.curriculum import validate
from app.services.curriculum.loaders import (
    course_dirs, course_id_of, load_all_courses, load_course_dir,
)
from app.services.curriculum.spec import CurriculumError


@pytest.fixture(scope="module")
def courses():
    return load_all_courses(only=[f"COURSE-{n:03d}" for n in range(1, 17)])


def test_all_sixteen_courses_load_with_no_errors(courses):
    assert [c.course_id for c in courses] == [f"COURSE-{n:03d}" for n in range(1, 17)]


def test_course_015_loads_through_the_nested_nested_wrapper_folder(courses):
    c15 = next(c for c in courses if c.course_id == "COURSE-015")
    assert len(c15.modules) == 1
    assert sum(len(m.lessons) for m in c15.modules) == 13
    # The outer folder's name is what the rest of the system displays/keys
    # off (source_dir), even though its content was read from the nested one.
    assert c15.source_dir == "COURSE-015_Voice_AI_Engineering_Real_Time_Voice_Agents"


def test_course_015_lessons_have_real_content_and_stable_source_keys(courses):
    c15 = next(c for c in courses if c.course_id == "COURSE-015")
    first_module = c15.modules[0]
    first_lesson = first_module.lessons[0]
    assert first_lesson.lesson_id == "M01.L01"
    assert first_module.module_id == "M015-01"
    assert len(first_lesson.content) > 500
    assert first_lesson.title

    # Stable across repeated loads (the importer relies on this for re-imports).
    reloaded = next(c for c in load_all_courses() if c.course_id == "COURSE-015")
    reloaded_lesson = reloaded.modules[0].lessons[0]
    assert reloaded_lesson.lesson_id == first_lesson.lesson_id
    assert reloaded_lesson.content == first_lesson.content


def test_course_015_manifest_prerequisites_are_read_from_the_nested_folder():
    from app.services.curriculum.loaders import read_manifest_prerequisites

    named = dict(read_manifest_prerequisites("COURSE-015"))
    assert named["COURSE-005"] == "required"
    assert {"COURSE-010", "COURSE-007", "COURSE-012"} <= set(named)


def test_other_courses_are_unaffected_by_the_wrapper_unwrap_logic(courses):
    """None of them have a nested same-name subfolder, so `load_course_dir`
    must take its normal, direct-layout-detection path for all of them. (The
    module counts are what the folders hold today; update them with the content.)"""
    expected_module_counts = {
        "COURSE-001": 7, "COURSE-002": 15, "COURSE-003": 14, "COURSE-004": 2,
        "COURSE-005": 12, "COURSE-006": 9, "COURSE-007": 5, "COURSE-008": 1,
        "COURSE-009": 1, "COURSE-010": 1, "COURSE-011": 8, "COURSE-012": 1,
        "COURSE-013": 15, "COURSE-014": 13, "COURSE-016": 16,
    }
    by_id = {c.course_id: c for c in courses}
    for course_id, expected in expected_module_counts.items():
        assert len(by_id[course_id].modules) == expected, course_id


def test_assessments_are_one_module_quiz_with_stable_lesson_traceability(courses):
    question_ids = []
    exercise_ids = []
    for course in courses:
        for module in course.modules:
            assert all(not lesson.questions for lesson in module.lessons)
            assert all(not lesson.project for lesson in module.lessons)
            valid_lessons = {lesson.lesson_id for lesson in module.lessons} | set(module.declared_lesson_ids)
            if module.quiz:
                assert module.quiz.quiz_id.startswith("QUIZ-")
                assert module.quiz.module_id == module.module_id
                assert module.quiz.questions
                for question in module.quiz.questions:
                    assert question.question_id
                    refs = question.lesson_ids or [question.lesson_id]
                    assert refs and set(refs) <= valid_lessons
                    question_ids.append(question.question_id)
            for lesson in module.lessons:
                for exercise in lesson.exercises:
                    assert (exercise.course_id, exercise.module_id, exercise.lesson_id) == (
                        course.course_id, module.module_id, lesson.lesson_id,
                    )
                    assert exercise.exercise_id
                    exercise_ids.append(exercise.exercise_id)
    assert len(question_ids) == len(set(question_ids))
    assert len(exercise_ids) == len(set(exercise_ids))


def test_a_folder_with_no_recognisable_layout_and_no_nested_wrapper_still_raises(tmp_path):
    empty_course = tmp_path / "COURSE-999_Nothing_Here"
    empty_course.mkdir()
    with pytest.raises(CurriculumError):
        load_course_dir(empty_course)


def test_consolidated_files_are_discovered_grouped_and_link_figures(tmp_path):
    course_dir = tmp_path / "COURSE-777_Consolidated"
    modules_dir = course_dir / "modules"
    assets_dir = course_dir / "assets"
    modules_dir.mkdir(parents=True)
    assets_dir.mkdir()
    (course_dir / "course_manifest.json").write_text(json.dumps({
        "course_id": "COURSE-777", "course_title": "Consolidated", "prerequisites": [],
    }), encoding="utf-8")
    (course_dir / "module_quizzes.json").write_text(json.dumps({
        "schema_version": 1, "course_id": "COURSE-777", "modules": [
            {"module_id": "M777-01", "quiz_id": "QUIZ-M777-01", "question_sources": []},
        ],
    }), encoding="utf-8")
    # A valid one-pixel GIF is enough to exercise manifest -> marker linking.
    (assets_dir / "flow.gif").write_bytes(base64.b64decode("R0lGODlhAQABAIAAAAAAAP///ywAAAAAAQABAAACAUwAOw=="))
    (course_dir / "assets_manifest.json").write_text(json.dumps({
        "version": 1, "course_id": "COURSE-777", "assets": [{
            "key": "training-flow", "file": "assets/flow.gif", "alt": "Training flow",
        }],
    }), encoding="utf-8")

    def lesson(code, title, figure=False):
        body = f"# {title}\n\nBody."
        if figure:
            body += "\n\n{{figure:training-flow}}\n"
        return (
            f"LESSON_CODE = {code!r}\nMODULE_ORDER = 1\nMODULE_TITLE = 'Foundations'\n"
            "MODULE_DESCRIPTION = 'The foundation module.'\n"
            f"TOPIC = {{'title': {title!r}, 'order': 1, 'difficulty': 'beginner', "
            f"'lesson': {{'title': {title!r}, 'content': {body!r}, 'estimated_minutes': 10}}, "
            "'exercises': [{'id': 'EX01', 'title': 'Try', 'description': 'Do it'}], "
            "'quiz': {'questions': [{'id': 'Q01', 'question': 'Ready?', "
            "'options': ['Yes', 'No'], 'correct': 0}]}}\n"
        )

    # File names do not define ownership or order; authored metadata does.
    (modules_dir / "module_20.py").write_text(lesson("M01.L02", "Second"), encoding="utf-8")
    (modules_dir / "module_01.py").write_text(lesson("M01.L01", "First", figure=True), encoding="utf-8")
    (modules_dir / "module_99.py").write_text("", encoding="utf-8")  # unfinished files are not content

    course = load_course_dir(course_dir)
    validate.validate_courses([course])

    assert len(course.modules) == 1
    module = course.modules[0]
    assert module.module_id == "M777-01"
    assert [item.lesson_id for item in module.lessons] == ["M01.L01", "M01.L02"]
    assert module.quiz.quiz_id == "QUIZ-M777-01"
    assert all(not item.questions for item in module.lessons)
    assert course.assets[0].key == "training-flow"
    assert not validate.warnings([course])


def test_course_id_of_reads_the_outer_folder_name_not_the_nested_one():
    directory = next(d for d in course_dirs() if course_id_of(d) == "COURSE-015")
    assert directory.name == "COURSE-015_Voice_AI_Engineering_Real_Time_Voice_Agents"


# ─── COURSE-006 now ships lesson bodies ────────────────────────────────────


def test_course_006_has_lesson_bodies_like_every_other_course(courses):
    c6 = next(c for c in courses if c.course_id == "COURSE-006")
    assert c6.has_lesson_bodies is True
    assert sum(len(m.lessons) for m in c6.modules) == 9
    assert all(m.title for m in c6.modules)
    # The author's module ids follow the source chapters (M006-05 is not used);
    # the number a learner sees is the position, so it has no gap.
    assert [m.order for m in c6.modules] == list(range(1, 10))
    assert "M006-05" not in {m.module_id for m in c6.modules}
