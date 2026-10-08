"""
app/services/curriculum/validate.py

Structural validation of the loaded course folders. Every rule here is one the
importer must not paper over: it raises `CurriculumError` with *all* the
problems found (not just the first), so one seed run tells the author
everything that is wrong.

  course ids and slugs unique             lesson ids unique within a course
  every lesson names a real module        module ids unique within a course
  no lesson file the manifest lists is missing, none on disk is unlisted
  declared module / lesson counts match what was loaded
  no lesson without a title or (where bodies exist) a body
  every image a lesson places exists       the asset manifest is sound
  no empty `<a id="...">` extraction anchor left in a lesson body
  every track mapping refers to a real career goal and a real course

`warnings()` lists what is worth knowing but is not wrong (a course that states
no lesson durations, an image no lesson places, an `[[IMAGE_NEEDED]]` still waiting for its file).
"""
from __future__ import annotations

from typing import Iterable, List, Mapping, Sequence

from app.services.content.lesson_blocks import empty_anchors, exercise_ids, malformed_exercise_markers
from app.services.curriculum import images
from app.services.curriculum.spec import CourseSpec, CurriculumError
from app.services.code_grading import SUPPORTED_TEST_TYPES
from app.services.code_grading.authoring import count_python_blanks
from app.services.code_grading.custom import CUSTOM_TESTS


_TEST_REQUIRED_FIELDS = {
    "variable_exists": ("variable",), "variable_not_exists": ("variable",),
    "value_equals": ("variable", "expected"), "value_approx": ("variable", "expected"),
    "type_equals": ("variable", "expected"), "function_called": ("function",),
    "function_not_called": ("function",), "function_argument": ("function", "argument_index", "expected"),
    "function_call_count": ("function",), "expression_uses": ("expression",),
    "operator_used": ("operator",), "stdout_equals": ("expected",), "stdout_contains": ("expected",),
    "list_length": ("variable", "expected"), "dict_contains_key": ("variable", "key"),
    "dataframe_exists": ("variable",), "dataframe_columns": ("variable", "expected"),
    "dataframe_shape": ("variable", "expected"),
    "dataframe_column_values": ("variable", "column", "expected"),
    "return_value_equals": ("function", "expected"), "function_exists": ("function",),
    "custom": ("checker",),
    "code_changed": ("starter_fingerprint",),
    "placeholders_removed": ("max_pass",),
    "ast_requirements": ("requirements",),
    "ast_contains": ("expected_ast", "path"),
    "text_changed": ("starter_fingerprint",),
    "regex_all": ("patterns",),
    "regex_none": ("patterns",),
    "regex_ordered": ("patterns",),
    "sql_blank": ("blank", "accepted"),
    "sql_result": ("setup_sql", "expected_rows"),
}


def _test_definition_problems(where: str, test: Mapping[str, object]) -> List[str]:
    test_id = str(test.get("id") or "<missing>")
    kind = str(test.get("type") or "")
    out: List[str] = []
    if kind not in SUPPORTED_TEST_TYPES:
        return [f"{where} {test_id}: unknown test type {kind!r}"]
    missing = [field for field in _TEST_REQUIRED_FIELDS[kind] if field not in test]
    if missing:
        out.append(f"{where} {test_id}: missing required fields: {', '.join(missing)}")
    if not test.get("feedback"):
        out.append(f"{where} {test_id}: missing feedback")
    if kind == "custom" and str(test.get("checker") or "") not in CUSTOM_TESTS:
        out.append(f"{where} {test_id}: unknown custom checker {test.get('checker')!r}")
    return out


def _dupes(values: Iterable[str]) -> List[str]:
    seen, dupes = set(), []
    for v in values:
        if v in seen and v not in dupes:
            dupes.append(v)
        seen.add(v)
    return dupes


def exercise_marker_problems(course: CourseSpec) -> List[str]:
    """`{{exercise:ID}}` in a lesson body must name one of that lesson's own exercises (by the id the
    author wrote, or the same id with the course prefix the loader adds), on a line of its own. A marker
    that points nowhere would otherwise be silently cut out of the lesson."""
    out: List[str] = []
    cid = course.course_id
    for lesson in course.lessons:
        known = {e.exercise_id for e in lesson.exercises if e.exercise_id}
        for lang, text in ((("en", lesson.content or ""),) + ((("ar", lesson.content_ar),) if lesson.content_ar else ())):
            where = f"{cid} {lesson.lesson_id}" + (" (ar)" if lang == "ar" else "")
            out += [f"{where}: exercise marker is not on a line of its own or is malformed: {m}"
                    for m in malformed_exercise_markers(text)]
            for ref in dict.fromkeys(exercise_ids(text)):
                if ref not in known and f"{cid}.{ref}" not in known:
                    shown = ", ".join(sorted(e.rsplit(".", 1)[-1] for e in known)) or "none"
                    out.append(f"{where}: references exercise '{ref}' but the lesson has no such exercise "
                               f"(it has: {shown})")
    return out


def problems_in_course(course: CourseSpec) -> List[str]:
    cid = course.course_id
    out: List[str] = []
    if not course.title:
        out.append(f"{cid}: course has no title")
    if not course.modules:
        out.append(f"{cid}: course has no modules")

    if dupes := _dupes(m.module_id for m in course.modules):
        out.append(f"{cid}: duplicate module ids: {', '.join(dupes)}")
    if dupes := _dupes(l.lesson_id for l in course.lessons):
        out.append(f"{cid}: duplicate lesson ids: {', '.join(dupes)}")
    if dupes := _dupes(e.exercise_id for l in course.lessons for e in l.exercises):
        out.append(f"{cid}: duplicate exercise ids: {', '.join(dupes)}")
    quizzes = [m.quiz for m in course.modules if m.quiz is not None]
    if dupes := _dupes(q.quiz_id for q in quizzes):
        out.append(f"{cid}: duplicate module quiz ids: {', '.join(dupes)}")
    if dupes := _dupes(q.question_id for quiz in quizzes for q in quiz.questions):
        out.append(f"{cid}: duplicate quiz question ids: {', '.join(dupes)}")

    module_ids = {m.module_id for m in course.modules}
    for module in course.modules:
        if not module.title:
            out.append(f"{cid} {module.module_id}: module has no title")
        if course.has_lesson_bodies and not module.lessons and not module.is_capstone:
            out.append(f"{cid} {module.module_id}: module has no lessons")
        valid_lesson_ids = {lesson.lesson_id for lesson in module.lessons} | set(module.declared_lesson_ids)
        for lesson in module.lessons:
            where = f"{cid} {lesson.lesson_id}"
            if lesson.module_id not in module_ids or lesson.module_id != module.module_id:
                out.append(f"{where}: refers to module '{lesson.module_id}' but sits in '{module.module_id}'")
            if not lesson.title:
                out.append(f"{where}: lesson has no title ({lesson.source_file})")
            if course.has_lesson_bodies and not lesson.content:
                out.append(f"{where}: lesson has no body ({lesson.source_file})")
            if lesson.questions:
                out.append(f"{where}: retains a lesson-local quiz instead of the module quiz")
            if lesson.project:
                out.append(f"{where}: retains a lesson-local project instead of the module project")
            for exercise in lesson.exercises:
                if not exercise.exercise_id:
                    out.append(f"{where}: exercise has no stable id")
                if (exercise.course_id, exercise.module_id, exercise.lesson_id) != (cid, module.module_id, lesson.lesson_id):
                    out.append(f"{where}: exercise {exercise.exercise_id or exercise.title!r} has invalid ownership")
                if exercise.exercise_type == "code":
                    exercise_where = f"{where} {exercise.exercise_id or exercise.title!r}"
                    if not exercise.starter_code:
                        out.append(f"{exercise_where}: code exercise has no starter_code")
                    if not exercise.language:
                        out.append(f"{exercise_where}: code exercise has no language")
                    if exercise.language and exercise.language not in {"python", "sql", "bash", "dockerfile", "hcl", "ini", "sparql", "yaml"}:
                        out.append(f"{exercise_where}: unsupported code language {exercise.language!r}")
                    if exercise.language == "python" and exercise.starter_code:
                        blank_count = count_python_blanks(exercise.starter_code)
                        if not 1 <= blank_count <= 5:
                            out.append(
                                f"{exercise_where}: starter_code must contain 1-5 editable ___ blanks "
                                f"(found {blank_count})"
                            )
                    if exercise.language == "sql" and exercise.starter_code:
                        blank_count = exercise.starter_code.count("___")
                        if not 1 <= blank_count <= 5:
                            out.append(
                                f"{exercise_where}: starter_code must contain 1-5 editable ___ blanks "
                                f"(found {blank_count})"
                            )
                    if not exercise.tests:
                        out.append(f"{exercise_where}: code exercise has no deterministic tests")
                    elif not any(test.get("required", True) for test in exercise.tests):
                        out.append(f"{exercise_where}: code exercise has no required deterministic tests")
                    test_ids = [str(test.get("id") or "") for test in exercise.tests]
                    if any(not test_id for test_id in test_ids):
                        out.append(f"{exercise_where}: every test needs an id")
                    if dupes := _dupes(test_ids):
                        out.append(f"{exercise_where}: duplicate test ids: {', '.join(dupes)}")
                    for test in exercise.tests:
                        out += _test_definition_problems(exercise_where, test)
                    if exercise.tests and not exercise.solution_code:
                        out.append(f"{exercise_where}: tested code exercise has no solution_code")
                elif exercise.exercise_type == "code_pending":
                    exercise_where = f"{where} {exercise.exercise_id or exercise.title!r}"
                    if not exercise.starter_code:
                        out.append(f"{exercise_where}: pending code exercise has no starter_code")
                    if not exercise.language:
                        out.append(f"{exercise_where}: pending code exercise has no language")
                    if exercise.tests or exercise.solution_code:
                        out.append(f"{exercise_where}: partially migrated code must be completed as type 'code'")
                elif exercise.exercise_type != "legacy":
                    out.append(f"{where}: exercise has unknown type {exercise.exercise_type!r}")
        if module.quiz:
            if module.quiz.module_id != module.module_id:
                out.append(f"{cid} {module.quiz.quiz_id}: quiz belongs to {module.quiz.module_id}, not {module.module_id}")
            if not module.quiz.quiz_id:
                out.append(f"{cid} {module.module_id}: module quiz has no id")
            if not module.quiz.questions:
                out.append(f"{cid} {module.quiz.quiz_id}: module quiz has no questions")
            for question in module.quiz.questions:
                where = f"{cid} {module.quiz.quiz_id} {question.question_id or '<missing question id>'}"
                if not question.question_id:
                    out.append(f"{where}: quiz question has no stable id")
                refs = question.lesson_ids or ([question.lesson_id] if question.lesson_id else [])
                if not refs:
                    out.append(f"{where}: quiz question has no lesson reference")
                invalid = sorted(set(refs) - valid_lesson_ids)
                if invalid:
                    out.append(f"{where}: references lessons outside the module: {', '.join(invalid)}")
                if not question.is_open and (question.correct is None or not 0 <= question.correct < len(question.options)):
                    out.append(f"{where}: quiz answer index is outside the options")

    loaded_modules = len(course.modules)
    loaded_lessons = len(course.lessons) if course.has_lesson_bodies else course.outline_lesson_count
    if course.declared_modules is not None and course.declared_modules != loaded_modules:
        out.append(f"{cid}: manifest declares {course.declared_modules} modules, {loaded_modules} loaded")
    if course.declared_lessons is not None and course.declared_lessons != loaded_lessons:
        out.append(f"{cid}: manifest declares {course.declared_lessons} lessons, {loaded_lessons} loaded")
    out += course.asset_problems
    out += course.structure_problems
    out += course.arabic_problems
    out += images.problems(course)
    out += exercise_marker_problems(course)
    for lesson in course.lessons:
        where = f"{cid} {lesson.lesson_id}"
        out += [f"{where}: line {n}: empty extraction anchor {tag} - delete it, it is not learner-facing text "
                f"({lesson.source_file})" for n, tag in empty_anchors(lesson.content)]
    out += [f"{cid}: manifest lists a file that does not exist: {f}" for f in course.missing_files]
    out += [f"{cid}: file is not listed by the course and was not imported: {f}" for f in course.unloaded_files]
    return out


def validate_courses(courses: Sequence[CourseSpec]) -> None:
    """Course-level and cross-course rules. Raises `CurriculumError`."""
    problems: List[str] = []
    if dupes := _dupes(c.course_id for c in courses):
        problems.append(f"duplicate course ids: {', '.join(dupes)}")
    if dupes := _dupes(c.slug for c in courses):
        problems.append(f"duplicate course slugs: {', '.join(dupes)}")
    if dupes := _dupes(
        exercise.exercise_id for course in courses for lesson in course.lessons for exercise in lesson.exercises
    ):
        problems.append(f"duplicate exercise ids across courses: {', '.join(dupes)}")
    if dupes := _dupes(
        module.quiz.quiz_id for course in courses for module in course.modules if module.quiz
    ):
        problems.append(f"duplicate module quiz ids across courses: {', '.join(dupes)}")
    if dupes := _dupes(
        question.question_id for course in courses for module in course.modules if module.quiz
        for question in module.quiz.questions
    ):
        problems.append(f"duplicate quiz question ids across courses: {', '.join(dupes)}")
    for course in courses:
        problems += problems_in_course(course)
    if problems:
        raise CurriculumError(problems)


def code_exercise_problems(courses: Sequence[CourseSpec]) -> List[str]:
    """Focused report for deterministic exercise CI.

    Kept independent from prose/translation validation so an unrelated
    Arabic draft cannot hide whether official code solutions grade correctly.
    """
    problems: List[str] = []
    exercises = [
        exercise for course in courses for lesson in course.lessons for exercise in lesson.exercises
        if exercise.exercise_type == "code"
    ]
    if dupes := _dupes(exercise.exercise_id for exercise in exercises):
        problems.append(f"duplicate code exercise ids: {', '.join(dupes)}")
    for exercise in exercises:
        where = f"{exercise.course_id} {exercise.exercise_id or exercise.title!r}"
        if not exercise.exercise_id:
            problems.append(f"{where}: missing exercise id")
        if not exercise.starter_code:
            problems.append(f"{where}: missing starter_code")
        if not exercise.language:
            problems.append(f"{where}: missing language")
        elif exercise.language not in {"python", "sql", "bash", "dockerfile", "hcl", "ini", "sparql", "yaml"}:
            problems.append(f"{where}: unsupported language {exercise.language!r}")
        elif exercise.language == "python" and exercise.starter_code:
            blank_count = count_python_blanks(exercise.starter_code)
            if not 1 <= blank_count <= 5:
                problems.append(
                    f"{where}: starter_code must contain 1-5 editable ___ blanks "
                    f"(found {blank_count})"
                )
        if exercise.language == "sql" and exercise.starter_code:
            blank_count = exercise.starter_code.count("___")
            if not 1 <= blank_count <= 5:
                problems.append(
                    f"{where}: starter_code must contain 1-5 editable ___ blanks "
                    f"(found {blank_count})"
                )
        if not exercise.tests:
            problems.append(f"{where}: missing deterministic tests")
        elif not any(test.get("required", True) for test in exercise.tests):
            problems.append(f"{where}: no required deterministic tests")
        if not exercise.solution_code:
            problems.append(f"{where}: missing solution_code")
        ids = [str(test.get("id") or "") for test in exercise.tests]
        if any(not test_id for test_id in ids):
            problems.append(f"{where}: every test needs an id")
        if dupes := _dupes(ids):
            problems.append(f"{where}: duplicate test ids: {', '.join(dupes)}")
        for test in exercise.tests:
            problems += _test_definition_problems(where, test)
    return problems


def validate_registry(
    courses: Sequence[CourseSpec],
    registry: Sequence[Mapping[str, object]],
    *,
    goals: Iterable[str],
    stage_courses: Mapping[str, Sequence[str]],
    known_course_slugs: Iterable[str] | None = None,
) -> None:
    """The registry (`seeds/curriculum.py`) says where each course sits. Every
    course folder needs an entry, every entry needs a folder, and nothing the
    registry points at may be missing."""
    problems: List[str] = []
    goal_set = set(goals)
    folder_ids = {c.course_id for c in courses}
    registry_ids = {str(r["course_id"]) for r in registry}
    for cid in sorted(folder_ids - registry_ids):
        problems.append(f"{cid}: has a course folder but no entry in the curriculum registry")
    for cid in sorted(registry_ids - folder_ids):
        problems.append(f"{cid}: is in the curriculum registry but has no course folder")

    # A scoped ``--course`` import validates only the selected folder/registry
    # entry, but its prerequisites may legitimately live in the rest of the
    # catalogue. Keep coverage checks scoped while resolving relationships
    # against the complete registry supplied by the caller.
    slugs = set(known_course_slugs) if known_course_slugs is not None else {str(r["slug"]) for r in registry}
    for r in registry:
        cid = r["course_id"]
        for prerequisite in r["prerequisites"]:
            if prerequisite not in slugs:
                problems.append(f"{cid}: prerequisite '{prerequisite}' is not a known course")
            if prerequisite == r["slug"]:
                problems.append(f"{cid}: is its own prerequisite")
        for goal in r["roles"]:
            if goal not in goal_set:
                problems.append(f"{cid}: role for unknown career goal '{goal}'")
        if r["track"] not in r["roles"]:
            problems.append(f"{cid}: primary track '{r['track']}' has no role entry")

    for stage, members in stage_courses.items():
        for slug in members:
            if slug.startswith("course-") and slug not in slugs:
                problems.append(f"stage '{stage}': lists '{slug}', which is not a known course (orphan track mapping)")

    for course in courses:
        for prerequisite, _kind in course.manifest_prerequisites:
            if prerequisite.lower() not in slugs:
                problems.append(f"{course.course_id}: manifest names prerequisite {prerequisite}, which is not a known course")
            if prerequisite == course.course_id:
                problems.append(f"{course.course_id}: manifest lists itself as a prerequisite")
    if problems:
        raise CurriculumError(problems)


def warnings(courses: Sequence[CourseSpec]) -> List[str]:
    notes: List[str] = []
    for course in courses:
        if not course.has_lesson_bodies:
            notes.append(f"{course.course_id}: folder holds an outline only (no lesson text) - imported as a "
                         f"non-startable shell with {len(course.modules)} modules")
            continue
        unstated = [l.lesson_id for l in course.lessons if l.estimated_minutes is None]
        if unstated:
            notes.append(f"{course.course_id}: {len(unstated)} of {len(course.lessons)} lessons state no duration")
        notes += images.warnings(course)
        notes += course.arabic_warnings
        no_quiz = [m.module_id for m in course.modules if m.quiz is None]
        if no_quiz:
            notes.append(f"{course.course_id}: {len(no_quiz)} modules have no quiz")
    return notes
