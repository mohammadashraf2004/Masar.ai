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
  every figure a lesson places exists      the asset manifest is sound
  every track mapping refers to a real career goal and a real course

`warnings()` lists what is worth knowing but is not wrong (a course that states
no lesson durations, a figure no lesson places).
"""
from __future__ import annotations

from typing import Iterable, List, Mapping, Sequence

from app.services.content.lesson_blocks import figure_keys, malformed_markers
from app.services.curriculum.spec import CourseSpec, CurriculumError


def _dupes(values: Iterable[str]) -> List[str]:
    seen, dupes = set(), []
    for v in values:
        if v in seen and v not in dupes:
            dupes.append(v)
        seen.add(v)
    return dupes


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

    module_ids = {m.module_id for m in course.modules}
    for module in course.modules:
        if not module.title:
            out.append(f"{cid} {module.module_id}: module has no title")
        if course.has_lesson_bodies and not module.lessons:
            out.append(f"{cid} {module.module_id}: module has no lessons")
        for lesson in module.lessons:
            where = f"{cid} {lesson.lesson_id}"
            if lesson.module_id not in module_ids or lesson.module_id != module.module_id:
                out.append(f"{where}: refers to module '{lesson.module_id}' but sits in '{module.module_id}'")
            if not lesson.title:
                out.append(f"{where}: lesson has no title ({lesson.source_file})")
            if course.has_lesson_bodies and not lesson.content:
                out.append(f"{where}: lesson has no body ({lesson.source_file})")
            for question in lesson.questions:
                if not question.is_open and (question.correct is None or not 0 <= question.correct < len(question.options)):
                    out.append(f"{where}: quiz answer index is outside the options")

    loaded_modules = len(course.modules)
    loaded_lessons = len(course.lessons) if course.has_lesson_bodies else course.outline_lesson_count
    if course.declared_modules is not None and course.declared_modules != loaded_modules:
        out.append(f"{cid}: manifest declares {course.declared_modules} modules, {loaded_modules} loaded")
    if course.declared_lessons is not None and course.declared_lessons != loaded_lessons:
        out.append(f"{cid}: manifest declares {course.declared_lessons} lessons, {loaded_lessons} loaded")
    out += course.asset_problems
    asset_keys = {a.key for a in course.assets}
    for lesson in course.lessons:
        where = f"{cid} {lesson.lesson_id}"
        out += [f"{where}: figure marker is not on a line of its own or is malformed: {m}"
                for m in malformed_markers(lesson.content)]
        for key in dict.fromkeys(figure_keys(lesson.content)):
            if key not in asset_keys:
                out.append(f"{where}: references figure '{key}' but no corresponding asset exists in {cid}'s assets_manifest.json")
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
    for course in courses:
        problems += problems_in_course(course)
    if problems:
        raise CurriculumError(problems)


def validate_registry(
    courses: Sequence[CourseSpec],
    registry: Sequence[Mapping[str, object]],
    *,
    goals: Iterable[str],
    stage_courses: Mapping[str, Sequence[str]],
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

    slugs = {str(r["slug"]) for r in registry}
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
        placed = {k for l in course.lessons for k in figure_keys(l.content)}
        unused = sorted(a.key for a in course.assets if a.key not in placed)
        if unused:
            notes.append(f"{course.course_id}: unused asset{'s' if len(unused) != 1 else ''} (no lesson places "
                         f"{'them' if len(unused) != 1 else 'it'}): {', '.join(unused)}")
        no_quiz = [l.lesson_id for l in course.lessons if not l.questions]
        if no_quiz:
            notes.append(f"{course.course_id}: {len(no_quiz)} lessons have no quiz questions")
    return notes
