"""
The course folders under backend/courses/ -> the catalogue.

Two layers: the real folders are loaded and validated as they are (no database - it
is the same check `seeds/import_courses.py --validate-only` runs), and the importer is
exercised against the seeded catalogue, including the properties a re-run must keep:
nothing duplicated, nothing deleted, ids and learner progress untouched.
"""
import json
import textwrap

import pytest

from app.models.learning import Exercise, Lesson, Project, Quiz
from app.models.learning_path import Course
from app.models.progress import UserProgress
from app.models.tool_course import ToolTopic
from app.services.content.quiz_lint import lint_quiz
from app.services.curriculum import importer, normalize as N, validate
from app.services.curriculum.loaders import load_course_dir, read_manifest_prerequisites
from app.services.curriculum.spec import CourseSpec, CurriculumError
from seeds import curriculum as cfg
from seeds.import_courses import import_courses, load_and_validate
from tests.curriculum_fixtures import import_small_courses, make_spec
from tests.learning_fixtures import *  # noqa: F401,F403

DEFINITIONS = {d["course_id"]: d for d in cfg.COURSE_DIRECTORY_COURSES}


# ─── The real folders (no database) ─────────────────────────────────────────

@pytest.fixture(scope="module")
def specs():
    return load_and_validate()


def test_all_fourteen_course_folders_load_and_validate(specs):
    assert [s.course_id for s in specs] == [f"COURSE-{n:03d}" for n in range(1, 15)]
    assert sum(len(s.modules) for s in specs) == 163
    # Every course whose folder holds lesson text imports every lesson it declares.
    for spec in specs:
        if spec.has_lesson_bodies:
            assert spec.declared_lessons in (None, len(spec.lessons)), spec.course_id
            assert spec.declared_modules in (None, len(spec.modules)), spec.course_id


def test_ids_are_unique_and_every_lesson_belongs_to_the_module_it_sits_in(specs):
    assert len({s.course_id for s in specs}) == len(specs)
    for spec in specs:
        assert len({m.module_id for m in spec.modules}) == len(spec.modules)
        lesson_ids = [l.lesson_id for l in spec.lessons]
        assert len(lesson_ids) == len(set(lesson_ids)), spec.course_id
        for module in spec.modules:
            assert {l.module_id for l in module.lessons} <= {module.module_id}
            assert [l.order for l in module.lessons] == list(range(1, len(module.lessons) + 1))


def test_every_imported_lesson_has_a_title_a_body_and_gradable_or_open_questions(specs):
    for spec in specs:
        if not spec.has_lesson_bodies:
            continue
        for lesson in spec.lessons:
            assert lesson.title and lesson.content, (spec.course_id, lesson.lesson_id)
            for q in lesson.questions:
                assert q.is_open or (0 <= q.correct < len(q.options))


def test_course_006_is_an_outline_and_is_never_given_invented_lessons(specs):
    outline = next(s for s in specs if s.course_id == "COURSE-006")
    assert not outline.has_lesson_bodies
    assert outline.lessons == [] and outline.outline_lesson_count == 67
    assert len(outline.modules) == 10 and outline.estimated_minutes == 3230


def test_the_registry_agrees_with_the_folders_and_stages_point_at_real_courses(specs):
    validate.validate_registry(
        specs, cfg.COURSE_DIRECTORY_COURSES, goals=cfg.GOALS,
        stage_courses={slug: members for slug, _t, _a, _p, _k, members in cfg.STAGES},
    )


def test_manifest_prerequisites_are_read_as_recommended_unless_the_manifest_says_required():
    assert ("COURSE-001", "required") in read_manifest_prerequisites("COURSE-014")
    assert ("COURSE-002", "recommended") in read_manifest_prerequisites("COURSE-014")
    assert ("COURSE-005", "required") in read_manifest_prerequisites("COURSE-012")
    assert read_manifest_prerequisites("COURSE-001") == []          # no manifest: none invented
    assert read_manifest_prerequisites("COURSE-013") == []          # a manifest that names none
    # 'COURSE-005/007/009 as relevant' names three courses.
    assert {c for c, _ in read_manifest_prerequisites("COURSE-011")} >= {"COURSE-005", "COURSE-007", "COURSE-009"}


# ─── Validation fails loudly ────────────────────────────────────────────────

def _spec_with(**changes) -> CourseSpec:
    spec = make_spec("COURSE-004")
    for key, value in changes.items():
        setattr(spec, key, value)
    return spec


def test_duplicate_lesson_ids_missing_files_and_wrong_counts_are_all_reported_together():
    spec = make_spec("COURSE-004")
    spec.modules[1].lessons[0].lesson_id = spec.modules[0].lessons[0].lesson_id          # duplicate id
    spec.modules[1].lessons[1].module_id = "M004-99"                                       # invalid module reference
    spec.modules[0].lessons[0].content = ""                                                # no body
    spec.declared_lessons, spec.declared_modules = 9, 3
    spec.missing_files = ["modules/M004_01/L004_099.py"]
    spec.unloaded_files = ["modules/M004_01/L004_050.py"]
    with pytest.raises(CurriculumError) as error:
        validate.validate_courses([spec])
    text = str(error.value)
    for expected in ("duplicate lesson ids", "refers to module 'M004-99'", "has no body",
                     "manifest declares 9 lessons", "manifest declares 3 modules",
                     "does not exist: modules/M004_01/L004_099.py", "was not imported: modules/M004_01/L004_050.py"):
        assert expected in text, expected


def test_duplicate_course_ids_and_slugs_are_rejected():
    with pytest.raises(CurriculumError) as error:
        validate.validate_courses([make_spec("COURSE-004"), make_spec("COURSE-004")])
    assert "duplicate course ids" in str(error.value) and "duplicate course slugs" in str(error.value)


def test_a_broken_prerequisite_and_an_orphan_stage_mapping_are_rejected(specs):
    registry = [dict(d) for d in cfg.COURSE_DIRECTORY_COURSES]
    registry[3] = {**registry[3], "prerequisites": ["course-999"]}
    stages = {slug: list(members) for slug, _t, _a, _p, _k, members in cfg.STAGES}
    stages["deep-learning"] = [*stages["deep-learning"], "course-998"]
    with pytest.raises(CurriculumError) as error:
        validate.validate_registry(specs, registry, goals=cfg.GOALS, stage_courses=stages)
    assert "prerequisite 'course-999' is not a known course" in str(error.value)
    assert "orphan track mapping" in str(error.value)


def test_a_folder_that_lists_a_lesson_file_that_is_not_there_fails_the_load_check(tmp_path):
    folder = tmp_path / "COURSE-777_Broken"
    module = folder / "modules" / "M777_01_intro"
    module.mkdir(parents=True)
    (folder / "course_manifest.json").write_text(json.dumps(
        {"course_id": "COURSE-777", "course_title": "Broken", "modules": 1, "lessons": 2, "prerequisites": []}))
    (module / "module.py").write_text('MODULE = {"id": "M777-01", "title": "Intro"}\n'
                                      'LESSON_FILES = ["L777_001_a", "L777_002_missing"]\n')
    (module / "L777_001_a.py").write_text(textwrap.dedent('''
        LESSON_ID = "L777-001"
        TOPIC = {"title": "A", "difficulty": "beginner",
                 "lesson": {"title": "A", "content": "# A\\n\\nbody", "estimated_minutes": 10},
                 "exercises": [], "quiz": {"questions": []}}
    '''))
    (module / "L777_003_unlisted.py").write_text("LESSON_ID = 'L777-003'\nTOPIC = {}\n")
    spec = load_course_dir(folder)
    with pytest.raises(CurriculumError) as error:
        validate.validate_courses([spec])
    assert "L777_002_missing" in str(error.value) and "L777_003_unlisted" in str(error.value)
    assert "manifest declares 2 lessons, 1 loaded" in str(error.value)


def test_an_unrecognised_layout_is_an_error_not_a_silent_skip(tmp_path):
    folder = tmp_path / "COURSE-778_Odd"
    folder.mkdir()
    (folder / "README.md").write_text("nothing here")
    with pytest.raises(CurriculumError):
        load_course_dir(folder)


# ─── Normalisation ──────────────────────────────────────────────────────────

def test_every_quiz_shape_becomes_a_gradable_or_an_open_question():
    mcq = N.norm_question({"question": "Q", "options": ["a", "b", "c"], "correct": 2}, "t")
    by_index = N.norm_question({"question": "Q", "choices": ["a", "b"], "answer_index": 1}, "t")
    by_text = N.norm_question({"question": "Q", "options": ["x", "y"], "answer": "y", "explanation": "e"}, "t")
    true_false = N.norm_question({"question": "Q", "type": "true_false", "answer": False}, "t")
    short = N.norm_question({"question": "Q", "type": "short_answer", "answer": "Because.", "explanation": "e"}, "t")
    assert (mcq.correct, by_index.correct, by_text.correct) == (2, 1, 1)
    assert true_false.options == ["True", "False"] and true_false.correct == 1
    assert short.is_open and short.explanation == "Because.\n\ne"           # the reference answer survives
    assert short.as_json() == {"question": "Q", "type": "open", "explanation": "Because.\n\ne"}
    for bad in ({"question": "Q", "options": ["a", "b"], "correct": 5},
                {"question": "Q", "options": ["a", "b"]},
                {"question": "Q", "options": ["a", "a"], "correct": 0}, {"question": ""}):
        with pytest.raises(CurriculumError):
            N.norm_question(bad, "t")


def test_difficulty_ranges_start_at_their_first_level_and_arabic_is_detected_by_letters():
    assert N.norm_difficulty("Intermediate → Advanced") == "intermediate"
    assert N.norm_difficulty("intermediate-to-advanced") == "intermediate"
    assert N.norm_difficulty(None, "advanced") == "advanced"
    assert N.is_arabic("# الشرح الأساسي\n\nيتعلم النموذج `model.fit(X)` مع numpy") is True
    assert N.is_arabic("# Title\n\nAn English body with one word: مرحبا") is False


def test_skill_tag_variants_collapse_to_one_tag():
    assert N.norm_tags(["Machine_Learning", "machine learning", "machine-learning", "ML"]) == ["machine-learning", "ml"]


def test_exercise_extras_are_folded_into_the_description_not_dropped():
    exercise = N.norm_exercise({
        "title": "T", "description": "Task.", "acceptance_criteria": ["works"], "hints": ["think"],
        "validation_code": "assert True", "starter_code": "x = 1"}, "t", "beginner")
    for expected in ("Task.", "Acceptance criteria", "- works", "Hints", "- think", "assert True"):
        assert expected in exercise.description
    assert exercise.starter_code == "x = 1"


# ─── Importing into the catalogue ───────────────────────────────────────────

def test_all_new_courses_import_and_a_second_run_creates_and_changes_nothing(learn_db, learn_catalog, specs):
    reports = import_courses(learn_db, specs)
    learn_db.commit()
    lessons = sum(len(s.lessons) for s in specs)
    assert sum(r.lessons.created for r in reports) == lessons
    assert learn_db.query(Lesson).filter(Lesson.source_key.like("COURSE-%")).count() == lessons
    assert learn_db.query(ToolTopic).filter(ToolTopic.source_key.like("COURSE-%")).count() == sum(
        len(s.modules) for s in specs)
    assert sum(r.exercises.created for r in reports) == learn_db.query(Exercise).filter(
        Exercise.source_key.like("COURSE-%")).count()

    # Every course is one canonical entity: exactly one catalogue row per course id, on its own tool course.
    assert learn_db.query(Course).filter(Course.slug.like("course-0%")).count() == len(specs)
    counts = {m.__tablename__: learn_db.query(m).count() for m in (ToolTopic, Lesson, Exercise, Quiz, Project, Course)}

    again = import_courses(learn_db, specs)
    learn_db.commit()
    for report in again:
        for tally in (report.modules, report.lessons, report.exercises, report.quizzes, report.projects):
            assert (tally.created, tally.updated) == (0, 0), report.course_id
        assert report.stale == []
    assert counts == {m.__tablename__: learn_db.query(m).count()
                      for m in (ToolTopic, Lesson, Exercise, Quiz, Project, Course)}


def test_imported_courses_are_available_except_the_outline_only_one(learn_db, learn_catalog, specs):
    import_courses(learn_db, specs)
    learn_db.commit()
    from app.services.learning.catalog_service import load_catalog_bundle

    catalog = load_catalog_bundle(learn_db).catalog
    by_slug = {c.slug: c for c in catalog.courses.values()}
    for spec in specs:
        info = by_slug[spec.slug]
        assert info.is_available is spec.has_lesson_bodies, spec.course_id
        assert info.module_count == len(spec.modules) and info.lesson_count == len(spec.lessons)


def test_a_re_import_updates_in_place_keeping_ids_and_learner_progress(learn_db, learn_catalog):
    from tests.learning_fixtures import register  # noqa: F401  (a real user row is needed for progress)
    (course,) = import_small_courses(learn_db, ["COURSE-001"])
    lesson = learn_db.query(Lesson).filter(Lesson.source_key == "COURSE-001/L001-0101").one()
    lesson_id, topic_id = lesson.id, lesson.tool_topic_id

    from app.models.user import User
    user = User(email="import-progress@example.com", hashed_password="x", full_name="P")
    learn_db.add(user)
    learn_db.flush()
    learn_db.add(UserProgress(user_id=user.id, tool_topic_id=topic_id, lessons_completed=[lesson_id]))
    learn_db.commit()

    spec = make_spec("COURSE-001")
    spec.modules[0].lessons[0].title = "A better title"
    spec.modules[0].lessons[0].content = "# Reworded\n\nNew body."
    report = importer.import_course(learn_db, spec, DEFINITIONS["COURSE-001"])
    learn_db.commit()

    assert (report.lessons.updated, report.lessons.created) == (1, 0)
    lesson = learn_db.query(Lesson).filter(Lesson.source_key == "COURSE-001/L001-0101").one()
    assert lesson.id == lesson_id and lesson.title == "A better title" and lesson.content.startswith("# Reworded")
    assert learn_db.query(UserProgress).filter(UserProgress.user_id == user.id).one().lessons_completed == [lesson_id]


def test_a_lesson_dropped_from_the_folder_is_reported_stale_and_never_deleted(learn_db, learn_catalog):
    import_small_courses(learn_db, ["COURSE-001"])
    smaller = make_spec("COURSE-001", lessons=1)
    report = importer.import_course(learn_db, smaller, DEFINITIONS["COURSE-001"])
    learn_db.commit()
    assert "COURSE-001/L001-0102" in report.stale
    assert learn_db.query(Lesson).filter(Lesson.source_key == "COURSE-001/L001-0102").count() == 1


def test_an_outline_only_course_imports_its_modules_and_stays_non_startable(learn_db, learn_catalog, specs):
    outline = next(s for s in specs if s.course_id == "COURSE-006")
    report = importer.import_course(learn_db, outline, DEFINITIONS["COURSE-006"])
    learn_db.commit()
    course = learn_db.query(Course).filter(Course.slug == "course-006").one()
    assert report.modules.created == 10 and report.lessons.created == 0
    assert learn_db.query(Lesson).join(ToolTopic, Lesson.tool_topic_id == ToolTopic.id).filter(
        ToolTopic.tool_course_id == course.tool_course_id).count() == 0
    assert report.notes and "non-startable" in report.notes[0]


def test_imported_quizzes_do_not_leak_the_correct_answer_by_position(learn_db, learn_catalog, specs):
    """COURSE-013 authors the right option first in every question; the import spreads the
    positions the way the rest of the catalogue already is, without touching option text."""
    spec = next(s for s in specs if s.course_id == "COURSE-013")
    assert {q.correct for l in spec.lessons for q in l.questions if not q.is_open} == {0}    # as authored
    importer.import_course(learn_db, spec, DEFINITIONS["COURSE-013"])
    learn_db.commit()
    quizzes = learn_db.query(Quiz).filter(Quiz.source_key.like("COURSE-013/%")).all()
    positions = [q["correct"] for quiz in quizzes for q in quiz.questions if "options" in q]
    assert len(positions) > 200 and max(positions.count(i) for i in set(positions)) / len(positions) < 0.5
    assert sum(lint_quiz(q.questions)["position_bias"] is not None for q in quizzes) < len(quizzes) * 0.2
    authored = {q.question: q.options[q.correct] for l in spec.lessons for q in l.questions}
    for quiz in quizzes:
        for q in quiz.questions:
            assert q["options"][q["correct"]] == authored[q["question"]]           # the answer key followed its text


def test_arabic_first_lessons_store_their_body_in_the_arabic_column(learn_db, learn_catalog, specs):
    spec = next(s for s in specs if s.course_id == "COURSE-002")
    importer.import_course(learn_db, spec, DEFINITIONS["COURSE-002"])
    learn_db.commit()
    first = spec.lessons[0]
    lesson = learn_db.query(Lesson).filter(Lesson.source_key == f"COURSE-002/{first.lesson_id}").one()
    assert lesson.content == "" and lesson.content_ar == first.content       # empty English twin: the reader falls back to Arabic
    english = next(s for s in specs if s.course_id == "COURSE-004")
    importer.import_course(learn_db, english, DEFINITIONS["COURSE-004"])
    en_lesson = learn_db.query(Lesson).filter(Lesson.source_key == f"COURSE-004/{english.lessons[0].lesson_id}").one()
    assert en_lesson.content == english.lessons[0].content and en_lesson.content_ar is None


def test_curriculum_courses_are_absent_from_the_tools_listing(learn_client, learn_db, learn_catalog):
    import_small_courses(learn_db, ["COURSE-001"])
    listing = learn_client.get("/api/v1/tool-courses/").json()
    assert "course-001" not in {c["slug"] for c in listing}
    assert "langchain" in {c["slug"] for c in listing}
