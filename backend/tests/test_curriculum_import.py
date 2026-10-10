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
    return load_and_validate(only=[f"COURSE-{n:03d}" for n in range(1, 19)])


def test_all_eighteen_course_folders_load_and_validate(specs):
    assert [s.course_id for s in specs] == [f"COURSE-{n:03d}" for n in range(1, 19)]
    # 194 for COURSE-001..016 (converted chapter courses show each file as a
    # module) + 8 each for COURSE-017 and COURSE-018.
    assert sum(len(s.modules) for s in specs) == 210
    # Every course whose folder holds lesson text imports every lesson it declares.
    for spec in specs:
        if spec.has_lesson_bodies:
            assert spec.declared_lessons in (None, len(spec.lessons)), spec.course_id
            assert spec.declared_modules in (None, len(spec.modules)), spec.course_id


def test_courses_17_and_18_keep_arabic_course_and_module_descriptions(specs):
    selected = {
        course.course_id: course
        for course in specs
        if course.course_id in {"COURSE-017", "COURSE-018"}
    }
    assert set(selected) == {"COURSE-017", "COURSE-018"}
    for course in selected.values():
        assert course.title_ar
        assert course.description_ar
        assert all(module.title_ar and module.description_ar for module in course.modules)


def test_ids_are_unique_and_every_lesson_belongs_to_the_module_it_sits_in(specs):
    assert len({s.course_id for s in specs}) == len(specs)
    for spec in specs:
        assert len({m.module_id for m in spec.modules}) == len(spec.modules)
        lesson_ids = [l.lesson_id for l in spec.lessons]
        assert len(lesson_ids) == len(set(lesson_ids)), spec.course_id
        for module in spec.modules:
            assert {l.module_id for l in module.lessons} <= {module.module_id}
            assert [l.order for l in module.lessons] == list(range(1, len(module.lessons) + 1))


def test_every_imported_lesson_has_a_title_and_body_and_module_questions_are_gradable(specs):
    for spec in specs:
        if not spec.has_lesson_bodies:
            continue
        for lesson in spec.lessons:
            assert lesson.title and lesson.content, (spec.course_id, lesson.lesson_id)
            assert lesson.questions == []
        for module in spec.modules:
            for q in module.quiz.questions if module.quiz else []:
                assert q.is_open or (0 <= q.correct < len(q.options))
                assert q.lesson_id in {lesson.lesson_id for lesson in module.lessons}


def test_every_course_folder_holds_lesson_text(specs):
    # COURSE-006 used to be an outline only; no folder is now.
    assert all(spec.has_lesson_bodies for spec in specs)
    assert len(next(s for s in specs if s.course_id == "COURSE-006").lessons) == 9


def test_the_registry_agrees_with_the_folders_and_stages_point_at_real_courses(specs):
    known = {c.course_id for c in specs}
    registry = [d for d in cfg.COURSE_DIRECTORY_COURSES if d["course_id"] in known]
    slugs = {d["slug"] for d in registry}
    validate.validate_registry(
        specs, registry, goals=cfg.GOALS,
        stage_courses={
            slug: [m for m in members if not m.startswith("course-") or m in slugs]
            for slug, _t, _a, _p, _k, members in cfg.STAGES
        },
    )


def test_manifest_prerequisites_are_read_as_recommended_unless_the_manifest_says_required():
    assert ("COURSE-001", "required") in read_manifest_prerequisites("COURSE-014")
    assert ("COURSE-002", "required") in read_manifest_prerequisites("COURSE-014")
    assert ("COURSE-003", "recommended") in read_manifest_prerequisites("COURSE-014")
    assert ("COURSE-005", "required") in read_manifest_prerequisites("COURSE-012")
    assert read_manifest_prerequisites("COURSE-001") == []          # the entry course: nothing is required first
    assert read_manifest_prerequisites("COURSE-013") == []          # a manifest that names none
    # COURSE-011's manifest names the LLM/RAG/MCP courses as recommended, not required.
    named = dict(read_manifest_prerequisites("COURSE-011"))
    assert named["COURSE-010"] == "required" and named["COURSE-005"] == named["COURSE-009"] == "recommended"


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
    assert N.norm_tags([
        "Machine_Learning", "module-01", "machine learning", "Module 18", "machine-learning", "ML",
    ]) == ["machine-learning", "ml"]


def test_exercise_extras_are_folded_into_the_description_not_dropped():
    exercise = N.norm_exercise({
        "title": "T", "description": "Task summary.",
        "instructions": "Answer all four numbered requirements.",
        "prompt": "Use the supplied scenario.",
        "acceptance_criteria": ["works"], "hints": ["think"],
        "validation_code": "assert True", "starter_code": "x = 1"}, "t", "beginner")
    for expected in (
        "Task summary.", "Instructions", "Answer all four numbered requirements.",
        "Prompt", "Use the supplied scenario.", "Acceptance criteria", "- works",
        "Hints", "- think", "assert True",
    ):
        assert expected in exercise.description
    assert exercise.starter_code == "x = 1"


def test_duplicate_exercise_instruction_text_is_not_repeated():
    exercise = N.norm_exercise({
        "title": "T", "description": "Do the task.", "instructions": "Do the task.",
    }, "t", "beginner")
    assert exercise.description == "Do the task."


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


def test_imported_exercises_keep_their_authored_lesson_relationship(learn_db, learn_catalog):
    spec = make_spec("COURSE-001", modules=1, lessons=2)
    importer.import_course(learn_db, spec, DEFINITIONS["COURSE-001"])
    learn_db.commit()

    first = learn_db.query(Lesson).filter(
        Lesson.source_key == "COURSE-001/L001-0101",
    ).one()
    second = learn_db.query(Lesson).filter(
        Lesson.source_key == "COURSE-001/L001-0102",
    ).one()
    first_exercises = learn_db.query(Exercise).filter(
        Exercise.source_key.like("COURSE-001/L001-0101/x%"),
    ).all()
    second_exercises = learn_db.query(Exercise).filter(
        Exercise.source_key.like("COURSE-001/L001-0102/x%"),
    ).all()

    assert len(first_exercises) == 2
    assert len(second_exercises) == 2
    assert {exercise.lesson_id for exercise in first_exercises} == {first.id}
    assert {exercise.lesson_id for exercise in second_exercises} == {second.id}


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


def test_a_lesson_dropped_from_the_folder_is_retired(learn_db, learn_catalog):
    """The importer used to keep a dropped lesson forever ("stale"), so a course that was
    ever replaced served its old and new content together. It now retires it."""
    import_small_courses(learn_db, ["COURSE-001"])
    smaller = make_spec("COURSE-001", lessons=1)
    report = importer.import_course(learn_db, smaller, DEFINITIONS["COURSE-001"])
    learn_db.commit()
    assert report.stale == []
    assert report.retired["lessons"] == 2 and report.retired["exercises"] == 4
    assert learn_db.query(Lesson).filter(Lesson.source_key == "COURSE-001/L001-0102").count() == 0
    assert learn_db.query(Lesson).filter(Lesson.source_key == "COURSE-001/L001-0101").count() == 1


def _course_rows(db, course_id):
    """Every keyed row an import of `course_id` owns, as {kind: set(source_key)}."""
    prefix = f"{course_id}/%"
    topics = db.query(ToolTopic).filter(ToolTopic.source_key.like(prefix)).all()
    ids = [t.id for t in topics]
    rows = {"topics": {t.source_key for t in topics}}
    for kind, model in (("lessons", Lesson), ("exercises", Exercise), ("quizzes", Quiz), ("projects", Project)):
        rows[kind] = {r.source_key for r in db.query(model).filter(model.tool_topic_id.in_(ids)).all()}
    return rows


def _replacement_spec(course_id):
    """The COURSE-012 swap in miniature: a smaller course that reuses the first module id
    (so the same module row is rewritten in place) but whose lessons have new ids."""
    spec = make_spec(course_id, modules=1, lessons=2)
    module = spec.modules[0]
    for index, lesson in enumerate(module.lessons, start=1):
        old_id = lesson.lesson_id
        lesson.lesson_id = f"M01.L{index:02d}"
        for exercise in lesson.exercises:
            exercise.lesson_id = lesson.lesson_id
            exercise.exercise_id = exercise.exercise_id.replace(old_id, lesson.lesson_id)
        for question in module.quiz.questions:
            if question.lesson_id == old_id:
                question.lesson_id = lesson.lesson_id
    return spec


def test_replacing_a_course_with_a_smaller_one_retires_only_its_obsolete_rows(learn_db, learn_catalog):
    """An EXISTING database, not a fresh one: the old layout is in the catalogue (with a
    learner on it), the new smaller folder is imported over it, and the catalogue ends up
    as exactly the new folder - with nothing of any other course or any learner touched."""
    from app.models.tool_course import ToolCourse
    from app.models.user import User

    import_small_courses(learn_db, ["COURSE-001", "COURSE-002"])
    other_before = _course_rows(learn_db, "COURSE-002")

    legacy = ToolCourse(slug="legacy-tool-x", title="Legacy tool")
    learn_db.add(legacy)
    learn_db.flush()
    legacy_topic = ToolTopic(tool_course_id=legacy.id, title="Legacy topic", slug="legacy-topic-x", order=1)
    learn_db.add(legacy_topic)
    learn_db.flush()
    legacy_lesson = Lesson(tool_topic_id=legacy_topic.id, title="Legacy lesson", content="x", order=1)
    learn_db.add(legacy_lesson)

    user = User(email="stale-retire@example.com", hashed_password="x", full_name="S")
    learn_db.add(user)
    learn_db.flush()
    first_topic = learn_db.query(ToolTopic).filter(ToolTopic.source_key == "COURSE-001/M001-01").one()
    progress = UserProgress(user_id=user.id, tool_topic_id=first_topic.id, lessons_completed=[], exercises_completed=[])
    learn_db.add(progress)
    learn_db.commit()
    progress_id, topic_id, legacy_ids = progress.id, first_topic.id, (legacy_topic.id, legacy_lesson.id)

    before = _course_rows(learn_db, "COURSE-001")
    assert len(before["topics"]) == 2 and len(before["lessons"]) == 4

    report = importer.import_course(learn_db, _replacement_spec("COURSE-001"), DEFINITIONS["COURSE-001"])
    learn_db.commit()

    after = _course_rows(learn_db, "COURSE-001")
    assert after["topics"] == {"COURSE-001/M001-01"}
    assert after["lessons"] == {"COURSE-001/M01.L01", "COURSE-001/M01.L02"}
    assert not any(k.startswith("COURSE-001/L001-") for rows in after.values() for k in rows)
    assert after["quizzes"] == {"COURSE-001/M001-01/quiz"}
    assert report.stale == []
    assert report.retired["topics"] == 1 and report.retired["lessons"] == 4

    # The reused module is the same row (ids never change for what survives) ...
    assert learn_db.query(ToolTopic).filter(ToolTopic.source_key == "COURSE-001/M001-01").one().id == topic_id
    # ... the learner on it is untouched ...
    kept = learn_db.query(UserProgress).filter(UserProgress.id == progress_id).one()
    assert (kept.user_id, kept.tool_topic_id) == (user.id, topic_id)
    # ... and neither another course nor a legacy tool course was looked at.
    assert _course_rows(learn_db, "COURSE-002") == other_before
    assert learn_db.query(ToolTopic).filter(ToolTopic.id == legacy_ids[0]).count() == 1
    assert learn_db.query(Lesson).filter(Lesson.id == legacy_ids[1]).count() == 1

    # Idempotent: a second import changes nothing and finds nothing left to retire.
    again = importer.import_course(learn_db, _replacement_spec("COURSE-001"), DEFINITIONS["COURSE-001"])
    learn_db.commit()
    assert again.retired == {} and again.stale == [] and not again.changed
    assert _course_rows(learn_db, "COURSE-001") == after


def test_retirement_keeps_rows_that_a_learner_refers_to(learn_db, learn_catalog):
    """Learner state is never deleted and never orphaned: a stale lesson a learner marked
    done, a stale quiz someone attempted and a module with progress all stay, reported."""
    from app.models.progress import QuizAttempt
    from app.models.user import User

    import_small_courses(learn_db, ["COURSE-001"])
    user = User(email="stale-keep@example.com", hashed_password="x", full_name="K")
    learn_db.add(user)
    learn_db.flush()
    stale_topic = learn_db.query(ToolTopic).filter(ToolTopic.source_key == "COURSE-001/M001-02").one()
    stale_quiz = learn_db.query(Quiz).filter(Quiz.source_key == "COURSE-001/M001-02/quiz").one()
    done_lesson = learn_db.query(Lesson).filter(Lesson.source_key == "COURSE-001/L001-0101").one()
    learn_db.add(QuizAttempt(user_id=user.id, quiz_id=stale_quiz.id, answers={}, score=0.0, passed=False))
    learn_db.add(UserProgress(user_id=user.id, tool_topic_id=stale_topic.id, lessons_completed=[], exercises_completed=[]))
    learn_db.add(UserProgress(
        user_id=user.id, tool_topic_id=done_lesson.tool_topic_id, lessons_completed=[done_lesson.id], exercises_completed=[],
    ))
    learn_db.commit()

    report = importer.import_course(learn_db, _replacement_spec("COURSE-001"), DEFINITIONS["COURSE-001"])
    learn_db.commit()

    rows = _course_rows(learn_db, "COURSE-001")
    # The module the learner has progress on, and the quiz they attempted, survive.
    assert "COURSE-001/M001-02" in rows["topics"] and "COURSE-001/M001-02/quiz" in rows["quizzes"]
    # The lesson a learner marked done survives (it sits in a surviving module).
    assert "COURSE-001/L001-0101" in rows["lessons"]
    kept = " ".join(report.stale)
    assert "COURSE-001/M001-02 (kept: referenced by user_progress.tool_topic_id)" in report.stale
    assert "COURSE-001/M001-02/quiz (kept: referenced by quiz_attempts.quiz_id)" in report.stale
    assert "COURSE-001/L001-0101 (kept: referenced by user_progress.lessons_completed)" in report.stale
    # Everything unreferenced is still retired, and no learner row moved.
    assert "COURSE-001/L001-0102" not in rows["lessons"]
    assert learn_db.query(QuizAttempt).filter(QuizAttempt.user_id == user.id).count() == 1
    assert learn_db.query(UserProgress).filter(UserProgress.user_id == user.id).count() == 2
    assert kept
    # Re-running does not delete them later either.
    importer.import_course(learn_db, _replacement_spec("COURSE-001"), DEFINITIONS["COURSE-001"])
    learn_db.commit()
    assert _course_rows(learn_db, "COURSE-001") == rows


def test_an_empty_or_outline_only_folder_retires_nothing(learn_db, learn_catalog):
    import_small_courses(learn_db, ["COURSE-001"])
    before = _course_rows(learn_db, "COURSE-001")

    empty = make_spec("COURSE-001")
    empty.modules = []
    report = importer.import_course(learn_db, empty, DEFINITIONS["COURSE-001"])
    outline = make_spec("COURSE-001")
    outline.has_lesson_bodies = False
    outline_report = importer.import_course(learn_db, outline, DEFINITIONS["COURSE-001"])
    learn_db.commit()

    assert not report.retired and not outline_report.retired
    assert _course_rows(learn_db, "COURSE-001") == before


def test_retirement_can_be_switched_off_and_reports_what_it_would_have_kept(learn_db, learn_catalog):
    import_small_courses(learn_db, ["COURSE-001"])
    before = _course_rows(learn_db, "COURSE-001")
    report = importer.import_course(
        learn_db, _replacement_spec("COURSE-001"), DEFINITIONS["COURSE-001"], retire_stale=False,
    )
    learn_db.commit()
    assert not report.retired and "COURSE-001/L001-0102" in report.stale
    assert before["lessons"] <= _course_rows(learn_db, "COURSE-001")["lessons"]


def test_an_outline_only_course_imports_its_modules_and_stays_non_startable(learn_db, learn_catalog):
    # No real course is outline-only any more (COURSE-006 ships lessons), so the
    # outline layout is exercised with a generated spec.
    outline = make_spec("COURSE-006")
    for module in outline.modules:
        module.lessons = []
    outline.has_lesson_bodies, outline.outline_lesson_count = False, 4
    report = importer.import_course(learn_db, outline, DEFINITIONS["COURSE-006"])
    learn_db.commit()
    course = learn_db.query(Course).filter(Course.slug == "course-006").one()
    assert report.modules.created == 2 and report.lessons.created == 0
    assert learn_db.query(Lesson).join(ToolTopic, Lesson.tool_topic_id == ToolTopic.id).filter(
        ToolTopic.tool_course_id == course.tool_course_id).count() == 0
    assert report.notes and "non-startable" in report.notes[0]


def test_imported_quizzes_do_not_leak_the_correct_answer_by_position(learn_db, learn_catalog, specs):
    """Whatever positions a course authors, the import leaves no position over-represented and
    never touches option text: the answer key follows its text."""
    spec = next(s for s in specs if s.course_id == "COURSE-013")
    importer.import_course(learn_db, spec, DEFINITIONS["COURSE-013"])
    learn_db.commit()
    quizzes = learn_db.query(Quiz).filter(Quiz.source_key.like("COURSE-013/%")).all()
    positions = [q["correct"] for quiz in quizzes for q in quiz.questions if "options" in q]
    assert len(positions) > 100 and max(positions.count(i) for i in set(positions)) / len(positions) < 0.5
    assert sum(lint_quiz(q.questions)["position_bias"] is not None for q in quizzes) < len(quizzes) * 0.2
    authored = {q.question: q.options[q.correct] for m in spec.modules for q in m.quiz.questions if not q.is_open}
    for quiz in quizzes:
        for q in quiz.questions:
            if "options" in q:
                assert q["options"][q["correct"]] == authored[q["question"]]           # the answer key followed its text


def test_arabic_first_lessons_store_their_body_in_the_arabic_column(learn_db, learn_catalog, specs):
    # Today's COURSE-002 is authored in English; an Arabic-first body is exercised with a generated course.
    arabic = make_spec("COURSE-002")
    first = arabic.lessons[0]
    first.content = '# \u0645\u0642\u062f\u0645\u0629 \u0641\u064a \u0627\u0644\u062a\u0639\u0644\u0645 \u0627\u0644\u0639\u0645\u064a\u0642\n\n\u0647\u0630\u0627 \u062f\u0631\u0633 \u064a\u0634\u0631\u062d \u0643\u064a\u0641 \u062a\u062a\u0639\u0644\u0645 \u0627\u0644\u0634\u0628\u0643\u0627\u062a \u0627\u0644\u0639\u0635\u0628\u064a\u0629 \u0645\u0646 \u0627\u0644\u0628\u064a\u0627\u0646\u0627\u062a \u062e\u0637\u0648\u0629 \u0628\u062e\u0637\u0648\u0629.'
    importer.import_course(learn_db, arabic, DEFINITIONS["COURSE-002"])
    learn_db.commit()
    lesson = learn_db.query(Lesson).filter(Lesson.source_key == f"COURSE-002/{first.lesson_id}").one()
    assert lesson.content == "" and lesson.content_ar == first.content       # empty English twin: the reader falls back to Arabic
    english = next(s for s in specs if s.course_id == "COURSE-004")
    importer.import_course(learn_db, english, DEFINITIONS["COURSE-004"])
    en_lesson = learn_db.query(Lesson).filter(Lesson.source_key == f"COURSE-004/{english.lessons[0].lesson_id}").one()
    # COURSE-004 is English-authored and now ships its Arabic in `ar/`: the English stays in `content`
    # and the Arabic from the folder (whole, or none if the folder has none) lands in `content_ar`.
    assert english.lessons[0].content_ar, "COURSE-004's ar/ folder is expected to supply this lesson's Arabic"
    assert en_lesson.content == english.lessons[0].content
    assert en_lesson.content_ar == english.lessons[0].content_ar
    assert en_lesson.content_ar != en_lesson.content


def test_curriculum_courses_are_absent_from_the_tools_listing(learn_client, learn_db, learn_catalog):
    import_small_courses(learn_db, ["COURSE-001"])
    listing = learn_client.get("/api/v1/tool-courses/").json()
    assert "course-001" not in {c["slug"] for c in listing}
    assert "langchain" in {c["slug"] for c in listing}


def _regrouped(spec: CourseSpec) -> CourseSpec:
    """The same lessons, one module each - the shape of the `consolidated_file_modules`
    restructure. Lesson ids (and so database ids) are unchanged; only the grouping moves."""
    from app.services.curriculum.spec import ModuleSpec

    lessons = [lesson for module in spec.modules for lesson in module.lessons]
    first = spec.modules[0]
    spec.modules = []
    for index, lesson in enumerate(lessons, start=1):
        module = first if index == 1 else ModuleSpec(
            module_id=f"{first.module_id}-{index:02d}", order=index, title=lesson.title)
        module.lessons = [lesson]
        lesson.module_id, lesson.order = module.module_id, 1
        spec.modules.append(module)
    return spec


def test_regrouping_lessons_into_new_modules_carries_learner_progress(learn_db, learn_catalog):
    """Release decision 2026-10-07: the module restructure must not silently erase progress.
    Completion is counted against an item's CURRENT module, so a lesson that moves takes each
    learner's completion of it along to their progress row for the new module."""
    from app.models.user import User
    from app.services.learning.progress_service import course_completion
    from tests.curriculum_fixtures import finish_topics

    spec = make_spec("COURSE-001", modules=1, lessons=4)
    importer.import_course(learn_db, spec, DEFINITIONS["COURSE-001"])
    learn_db.commit()
    course = learn_db.query(Course).filter(Course.slug == "course-001").one()
    done_all = User(email="carry-all@example.com", hashed_password="x", full_name="All")
    done_one = User(email="carry-one@example.com", hashed_password="x", full_name="One")
    learn_db.add_all([done_all, done_one])
    learn_db.flush()
    finish_topics(learn_db, done_all.id, course)
    third = learn_db.query(Lesson).filter(Lesson.source_key == "COURSE-001/L001-0103").one()
    learn_db.add(UserProgress(user_id=done_one.id, tool_topic_id=third.tool_topic_id, lessons_completed=[third.id]))
    learn_db.commit()
    before = course_completion(learn_db, done_all.id, [course])[course.id]
    one_before = course_completion(learn_db, done_one.id, [course])[course.id]
    assert before == 1.0 and one_before > 0

    report = importer.import_course(learn_db, _regrouped(make_spec("COURSE-001", modules=1, lessons=4)),
                                    DEFINITIONS["COURSE-001"])
    learn_db.commit()

    assert report.modules.created == 3                     # three lessons moved to new modules
    # done_all: lessons 2-4 moved (3) with their 2 exercises each (6); done_one: lesson 3 (1).
    assert report.progress_carried == 3 + 6 + 1
    assert course_completion(learn_db, done_all.id, [course])[course.id] == before
    assert course_completion(learn_db, done_one.id, [course])[course.id] == one_before
    third = learn_db.query(Lesson).filter(Lesson.source_key == "COURSE-001/L001-0103").one()
    moved_row = learn_db.query(UserProgress).filter(UserProgress.user_id == done_one.id,
                                                    UserProgress.tool_topic_id == third.tool_topic_id).one()
    assert moved_row.lessons_completed == [third.id]

    again = importer.import_course(learn_db, _regrouped(make_spec("COURSE-001", modules=1, lessons=4)),
                                   DEFINITIONS["COURSE-001"])
    learn_db.commit()
    assert again.progress_carried == 0 and not again.changed
