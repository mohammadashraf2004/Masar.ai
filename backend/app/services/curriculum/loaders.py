"""
app/services/curriculum/loaders.py

Reads the course folders under `backend/courses/` into `CourseSpec`s.

The folders were authored in nine layouts. Each has one small loader below; the
`load_course_dir` dispatcher picks the loader from the folder's *structure*, not
its name, so a tenth course that reuses a layout needs no code. What every
loader shares:

  * lesson text stays in the files - this module reads it, nothing is copied
    into Python or TypeScript;
  * a file that cannot be imported, a file the manifest names that does not
    exist, and a lesson file no manifest names are all reported (never skipped),
    because a silently dropped lesson is a course with a hole in it;
  * nothing is generated. A field a course does not provide is left empty.

Lesson modules are executed with `importlib`. They are repository content that
is reviewed like code (several import `app.models`), which is why this runs at
seed time and never on a request.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Tuple

from app.services.curriculum import normalize as N
from app.services.curriculum.code_classification import apply_pending_code_classification
from app.services.curriculum.code_blanks import apply_fill_in_blank_format
from app.services.curriculum.arabic import attach_arabic
from app.services.curriculum.assets import load_asset_manifest
from app.services.curriculum.spec import (
    CourseSpec, CurriculumError, LessonSpec, ModuleQuizSpec, ModuleSpec, ProjectSpec,
)

COURSES_ROOT = Path(__file__).resolve().parents[3] / "courses"
_COURSE_DIR = re.compile(r"^COURSE-(\d{3})(?![\d])")


# ─── File access ────────────────────────────────────────────────────────────

def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CurriculumError([f"{path}: cannot read JSON ({exc})"])


_loaded = 0


def load_py(path: Path) -> Any:
    """Execute one content file and return its module. Each file gets its own
    module object so two `TOPIC`s never share state."""
    global _loaded
    _loaded += 1
    spec = importlib.util.spec_from_file_location(f"_curriculum_{_loaded}", path)
    if spec is None or spec.loader is None:
        raise CurriculumError([f"{path}: cannot be imported"])
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # content file raised: report which one, do not skip it
        raise CurriculumError([f"{path}: raised {type(exc).__name__} while loading ({exc})"])
    return module


def _sym(module: Any, name: str, path: Path) -> Any:
    if not hasattr(module, name):
        raise CurriculumError([f"{path}: missing required symbol {name}"])
    return getattr(module, name)


def _rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def course_dirs(root: Path = COURSES_ROOT) -> List[Path]:
    return sorted(p for p in root.iterdir() if p.is_dir() and _COURSE_DIR.match(p.name))


def course_id_of(directory: Path) -> str:
    return f"COURSE-{_COURSE_DIR.match(directory.name).group(1)}"


# ─── Manifest prerequisites ─────────────────────────────────────────────────

_MENTION = re.compile(r"COURSE-(\d{3})((?:/\d{3})*)")

# Manifest keys under which a prerequisite list may appear, and what each
# sub-list means. Only `required` is required; everything else is advice.
_REQUIRED_KEYS = {"required"}


def manifest_prerequisites(manifest: Dict[str, Any]) -> List[Tuple[str, str]]:
    """`[(course id, 'required' | 'recommended')]` in the order the manifest gives
    them. A bare list of `COURSE-00X — Title` lines names recommended courses;
    the dict form (`required` / `strongly_recommended` / `supporting` / ...)
    keeps its own distinction. 'COURSE-005/007/009 as relevant' names three."""
    raw = manifest.get("prerequisites", manifest.get("prerequisite_courses"))
    if raw is None:
        return []
    groups: List[Tuple[str, Iterable[Any]]]
    if isinstance(raw, dict):
        groups = [("required" if key in _REQUIRED_KEYS else "recommended", values) for key, values in raw.items()]
    else:
        groups = [("recommended", raw)]
    found: List[Tuple[str, str]] = []
    for kind, values in groups:
        for value in values if isinstance(values, list) else [values]:
            for match in _MENTION.finditer(str(value)):
                ids = [match.group(1)] + [p for p in match.group(2).split("/") if p]
                for number in ids:
                    entry = (f"COURSE-{number}", kind)
                    if entry[0] not in [c for c, _ in found]:
                        found.append(entry)
    return found


def read_manifest_prerequisites(course_id: str, root: Path = COURSES_ROOT) -> List[Tuple[str, str]]:
    """The prerequisites a course's manifest names, without loading its lessons.
    A folder with no manifest (COURSE-001) names none."""
    directory = next((d for d in course_dirs(root) if course_id_of(d) == course_id), None)
    manifest_file = directory / "course_manifest.json" if directory else None
    # A folder that wraps its content in one directory named after the course id
    # (COURSE-015) keeps its manifest there; `load_course_dir` descends the same way.
    if directory and not manifest_file.is_file() and (directory / course_id / "course_manifest.json").is_file():
        manifest_file = directory / course_id / "course_manifest.json"
    if manifest_file is None or not manifest_file.is_file():
        return []
    return manifest_prerequisites(read_json(manifest_file))


# ─── Shared lesson builder ──────────────────────────────────────────────────

def _lesson(
    course_id: str, module_id: str, order: int, *, lesson_id: str, title: str, content: Any,
    minutes: Any, difficulty: Any, tags: Iterable[Any] = (), description: Any = None,
    exercises: Any = None, quiz: Any = None, project: Any = None, file: str, course_difficulty: str,
) -> LessonSpec:
    where = f"{course_id} {lesson_id}"
    diff = N.norm_difficulty(difficulty, course_difficulty)
    normalized_exercises = N.norm_exercises(exercises, where, diff)
    for index, exercise in enumerate(normalized_exercises, start=1):
        exercise.exercise_id = exercise.exercise_id or f"EX-{course_id.split('-')[1]}-{lesson_id}-{index:02d}"
        exercise.course_id = exercise.course_id or course_id
        exercise.module_id = exercise.module_id or module_id
        exercise.lesson_id = exercise.lesson_id or lesson_id
    normalized_questions = N.norm_questions(quiz, where)
    for question in normalized_questions:
        question.lesson_id = question.lesson_id or lesson_id
    return LessonSpec(
        lesson_id=lesson_id, module_id=module_id, order=order,
        title=N.as_text(title), content=N.as_text(content),
        estimated_minutes=int(minutes) if isinstance(minutes, (int, float)) and not isinstance(minutes, bool) else None,
        difficulty=diff, skill_tags=N.norm_tags(tags), description=N.as_text(description) or None,
        exercises=normalized_exercises,
        questions=normalized_questions,
        project=N.norm_project(project, where, diff),
        source_file=file,
    )


def _topic_lesson(
    course_id: str, module_id: str, order: int, lesson_id: str, topic: Dict[str, Any], file: str,
    course_difficulty: str,
) -> LessonSpec:
    """A lesson whose file follows the Masar seed template: a `TOPIC` dict with
    a nested `lesson` (COURSES 001-005, 007-010)."""
    body = topic.get("lesson") or {}
    minutes = body.get("estimated_minutes")
    if minutes is None and isinstance(topic.get("estimated_hours"), (int, float)):
        minutes = round(topic["estimated_hours"] * 60)
    return _lesson(
        course_id, module_id, order, lesson_id=lesson_id, title=body.get("title") or topic.get("title"),
        content=body.get("content") or body.get("content_markdown"), minutes=minutes,
        difficulty=topic.get("difficulty"), tags=topic.get("skill_tags") or [], description=topic.get("description"),
        exercises=topic.get("exercises"), quiz=topic.get("quiz"), project=topic.get("project"),
        file=file, course_difficulty=course_difficulty,
    )


def _default_difficulty(course_id: str, manifest: Dict[str, Any]) -> str:
    return N.norm_difficulty(manifest.get("level") or manifest.get("difficulty"), "intermediate")


def _ordered(directory: Path, pattern: str) -> List[Path]:
    return sorted(directory.glob(pattern), key=lambda p: p.name.lower())


def _capstone(raw: Any, where: str, difficulty: str) -> Optional[ProjectSpec]:
    return N.norm_project(raw, where, difficulty)


def _consolidate_module_quizzes(course: CourseSpec, root: Path) -> None:
    """Turn legacy lesson-local question banks into one canonical quiz/module.

    `module_quizzes.json` is intentionally an index, not a second copy of the
    questions: source prose and answer metadata stay in their reviewed lesson
    files, while the manifest makes module ownership and lesson traceability
    explicit. This keeps every historical course layout loadable without
    duplicating or rewriting assessment content.
    """
    path = root / "module_quizzes.json"
    raw = read_json(path) if path.is_file() else {"modules": []}
    if path.is_file() and (not isinstance(raw, dict) or raw.get("schema_version") != 1):
        course.structure_problems.append(f"{path}: schema_version must be 1")
    if isinstance(raw, dict) and raw.get("course_id") not in (None, course.course_id):
        course.structure_problems.append(
            f"{path}: course_id {raw.get('course_id')!r} does not match {course.course_id}"
        )
    entries = raw.get("modules") if isinstance(raw, dict) else None
    if not isinstance(entries, list):
        course.structure_problems.append(f"{path}: 'modules' must be a list")
        entries = []

    known_modules = {module.module_id for module in course.modules}
    by_module: Dict[str, Dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not N.as_text(entry.get("module_id")):
            course.structure_problems.append(f"{path}: every module quiz entry needs module_id")
            continue
        raw_module_id = str(entry["module_id"])
        module_id = raw_module_id if raw_module_id in known_modules else N.module_id_for(course.course_id, raw_module_id)
        if module_id in by_module:
            course.structure_problems.append(f"{path}: duplicate module quiz entry for {module_id}")
        by_module[module_id] = entry

    for module_id in sorted(set(by_module) - known_modules):
        course.structure_problems.append(f"{path}: quiz references missing module {module_id}")

    for module in course.modules:
        sources = {lesson.lesson_id: list(lesson.questions) for lesson in module.lessons if lesson.questions}
        sources.update({lesson_id: list(questions) for lesson_id, questions in module.legacy_question_sources.items()
                        if questions})
        entry = by_module.get(module.module_id)
        if not sources:
            if entry is not None:
                course.structure_problems.append(
                    f"{path}: {module.module_id} declares a quiz but has no source questions"
                )
            continue
        default_quiz_id = (
            f"QUIZ-{module.module_id}" if course.course_id.split("-")[1] in module.module_id
            else f"QUIZ-C{course.course_id.split('-')[1]}-{module.module_id}"
        )
        if entry is None:
            course.structure_problems.append(
                f"{path}: {module.module_id} has lesson questions but no canonical module quiz entry"
            )
            declared_sources = list(sources)
            quiz_id = default_quiz_id
            title = f"Module quiz: {module.title}"
        else:
            quiz_id = N.as_text(entry.get("quiz_id")) or default_quiz_id
            title = N.as_text(entry.get("title")) or f"Module quiz: {module.title}"
            raw_sources = entry.get("question_sources")
            if not isinstance(raw_sources, list):
                course.structure_problems.append(f"{path}: {module.module_id} question_sources must be a list")
                raw_sources = []
            declared_sources = []
            for source in raw_sources:
                if not isinstance(source, dict) or not N.as_text(source.get("lesson_id")):
                    course.structure_problems.append(
                        f"{path}: {module.module_id} has a question source without lesson_id"
                    )
                    continue
                lesson_id = N.lesson_id_for(course.course_id, source["lesson_id"])
                declared_sources.append(lesson_id)
                actual = len(sources.get(lesson_id, []))
                if lesson_id not in sources:
                    course.structure_problems.append(
                        f"{path}: {module.module_id} references lesson {lesson_id} with no questions"
                    )
                if isinstance(source.get("question_count"), int) and source["question_count"] != actual:
                    course.structure_problems.append(
                        f"{path}: {module.module_id} {lesson_id} declares {source['question_count']} questions, "
                        f"but {actual} loaded"
                    )
            missing = sorted(set(sources) - set(declared_sources))
            extra = sorted(set(declared_sources) - set(sources))
            if missing:
                course.structure_problems.append(
                    f"{path}: {module.module_id} omits question sources: {', '.join(missing)}"
                )
            if extra:
                course.structure_problems.append(
                    f"{path}: {module.module_id} has invalid question sources: {', '.join(extra)}"
                )

        questions = []
        for lesson_id in declared_sources:
            for question in sources.get(lesson_id, []):
                if question.lesson_ids:
                    if lesson_id not in question.lesson_ids:
                        course.structure_problems.append(
                            f"{course.course_id} {question.question_id or question.question[:40]}: source lesson "
                            f"{lesson_id} is absent from lesson_ids"
                        )
                elif question.lesson_id != lesson_id:
                    course.structure_problems.append(
                        f"{course.course_id} {question.question_id or question.question[:40]}: lesson_id "
                        f"{question.lesson_id!r} disagrees with source lesson {lesson_id}"
                    )
                questions.append(question)
        for index, question in enumerate(questions, start=1):
            question.question_id = question.question_id or f"Q-{quiz_id.removeprefix('QUIZ-')}-{index:03d}"
        module.quiz = ModuleQuizSpec(quiz_id=quiz_id, module_id=module.module_id, title=title, questions=questions)
        for lesson in module.lessons:
            lesson.questions = []
        module.legacy_question_sources.clear()


def _consolidate_embedded_quizzes(course: CourseSpec, quiz_ids: Mapping[str, str]) -> None:
    """Promote questions from self-contained lesson files to module quizzes.

    The owning lesson is already known while loading this layout, so it does
    not need the legacy manifest to repeat every question source. Existing
    quiz ids are retained where possible so imports update rows in place.
    """
    for module in course.modules:
        questions = [question for lesson in module.lessons for question in lesson.questions]
        if not questions:
            continue
        quiz_id = quiz_ids.get(module.module_id) or f"QUIZ-{module.module_id}"
        for index, question in enumerate(questions, start=1):
            question.question_id = question.question_id or f"Q-{quiz_id.removeprefix('QUIZ-')}-{index:03d}"
        module.quiz = ModuleQuizSpec(
            quiz_id=quiz_id,
            module_id=module.module_id,
            title=f"Module quiz: {module.title}",
            questions=questions,
        )
        for lesson in module.lessons:
            lesson.questions = []


def _consolidate_module_projects(course: CourseSpec) -> None:
    """Promote legacy end-of-lesson project fields to their owning module.

    Several exports repeat the same project both in the final lesson and in a
    separate module-project file. The canonical model keeps one module project;
    identical-title copies are references to that same project, not two learner
    assignments.
    """
    for module in course.modules:
        authored = [(lesson, lesson.project) for lesson in module.lessons if lesson.project]
        if not authored:
            continue
        if module.project is None and len(authored) == 1:
            lesson, project = authored[0]
            module.project = project
            lesson.project = None
            continue
        if module.project is not None and all(project.title == module.project.title for _, project in authored):
            for lesson, _project in authored:
                lesson.project = None
            continue
        course.structure_problems.append(
            f"{course.course_id} {module.module_id}: multiple distinct module projects are authored in lesson files"
        )


# ─── Layout 1: COURSE-001 - lessons/module_NN/lesson_NN_*.py ────────────────

def _load_module_dirs_001(root: Path, course_id: str) -> CourseSpec:
    base = root / "lessons"
    modules: List[ModuleSpec] = []
    for module_dir in sorted(p for p in base.iterdir() if p.is_dir() and p.name.startswith("module_")):
        files = _ordered(module_dir, "lesson_*.py")
        loaded = [(f, load_py(f)) for f in files]
        if not loaded:
            raise CurriculumError([f"{module_dir}: module folder has no lesson files"])
        first = loaded[0][1]
        module_id = f"M{int(_sym(first, 'MODULE_ORDER', loaded[0][0])):02d}"
        module = ModuleSpec(
            module_id=module_id, order=int(first.MODULE_ORDER), title=N.as_text(first.MODULE_TITLE),
            description=N.as_text(first.MODULE_DESCRIPTION) or None,
        )
        for index, (file, mod) in enumerate(loaded, start=1):
            if mod.MODULE_ORDER != first.MODULE_ORDER:
                raise CurriculumError([f"{file}: MODULE_ORDER {mod.MODULE_ORDER} disagrees with its module {first.MODULE_ORDER}"])
            topic = _sym(mod, "TOPIC", file)
            module.lessons.append(_topic_lesson(
                course_id, module_id, index, N.as_text(_sym(mod, "LESSON_CODE", file)), topic,
                _rel(file, root), "beginner",
            ))
        modules.append(module)
    title = root.name.split("_", 1)[1].replace("_", " ")
    return CourseSpec(course_id=course_id, source_dir=root.name, title=title, modules=modules)


# ─── Consolidated layout: modules/module_NN.py or flat lessons/*.py ────────

_CONSOLIDATED_MODULE_FILE = re.compile(r"^(?:module_\d+|m\d+_l\d+.*)\.py$", re.IGNORECASE)
_CONSOLIDATED_LESSON_FILE = re.compile(r"^lesson_.*\.py$", re.IGNORECASE)
_LESSON_CODE_ORDER = re.compile(r"^M(\d+)\.L(\d+)$", re.IGNORECASE)


def _consolidated_files(root: Path) -> List[Path]:
    """Return only files belonging to the self-contained lesson layout."""
    modules_dir = root / "modules"
    if modules_dir.is_dir():
        found = sorted(
            p for p in modules_dir.iterdir()
            if p.is_file() and p.stat().st_size > 0 and _CONSOLIDATED_MODULE_FILE.match(p.name)
        )
        if found:
            return found
    lessons_dir = root / "lessons"
    if lessons_dir.is_dir():
        return sorted(
            p for p in lessons_dir.iterdir()
            if p.is_file() and p.stat().st_size > 0 and _CONSOLIDATED_LESSON_FILE.match(p.name)
        )
    return []


def _legacy_quiz_identity(root: Path) -> Tuple[Dict[int, str], Dict[str, str], str]:
    """Read stable ids without trusting the legacy lesson-source index."""
    path = root / "module_quizzes.json"
    raw = read_json(path) if path.is_file() else {}
    entries = raw.get("modules") if isinstance(raw, dict) else []
    module_ids: Dict[int, str] = {}
    quiz_ids: Dict[str, str] = {}
    style = "canonical"
    for entry in entries if isinstance(entries, list) else []:
        if not isinstance(entry, dict):
            continue
        module_id = N.as_text(entry.get("module_id"))
        match = re.search(r"(\d{2})$", module_id)
        if not match:
            continue
        module_ids[int(match.group(1))] = module_id
        quiz_id = N.as_text(entry.get("quiz_id"))
        if quiz_id:
            quiz_ids[module_id] = quiz_id
        if re.fullmatch(r"M\d{2}", module_id, re.IGNORECASE):
            style = "short"
    return module_ids, quiz_ids, style


def _module_id_for_order(course_id: str, order: int, known: Mapping[int, str], style: str) -> str:
    if order in known:
        return known[order]
    if style == "short":
        return f"M{order:02d}"
    return f"M{course_id.split('-')[1]}-{order:02d}"


def _load_consolidated_topics(root: Path, course_id: str) -> CourseSpec:
    """Load complete lesson files grouped by their authored module metadata.

    The directory is the inventory: adding or removing one lesson does not
    require repeating its path in a central Python registry or JSON manifest.
    Converted chapter courses can opt into ``consolidated_file_modules`` when
    each self-contained file is meant to remain a separate learner-visible
    module even though its preserved lesson id still belongs to an older
    module numbering scheme.
    """
    loaded = [(path, load_py(path)) for path in _consolidated_files(root)]
    required = ("LESSON_CODE", "MODULE_ORDER", "MODULE_TITLE", "MODULE_DESCRIPTION", "TOPIC")
    for path, authored in loaded:
        for symbol in required:
            _sym(authored, symbol, path)

    manifest_file = root / "course_manifest.json"
    manifest = read_json(manifest_file) if manifest_file.is_file() else {}
    difficulty = _default_difficulty(course_id, manifest)
    known_module_ids, known_quiz_ids, id_style = _legacy_quiz_identity(root)
    file_modules = manifest.get("consolidated_file_modules") is True

    def lesson_position(item: Tuple[Path, Any]) -> Tuple[int, int, str]:
        path, authored = item
        code = N.as_text(authored.LESSON_CODE)
        match = _LESSON_CODE_ORDER.match(code)
        lesson_order = int(match.group(2)) if match and int(match.group(1)) == int(authored.MODULE_ORDER) else 0
        return int(authored.MODULE_ORDER), lesson_order, path.name.lower()

    grouped: Dict[int, List[Tuple[Path, Any]]] = {}
    if file_modules:
        # Preserve authored module/lesson order while promoting each complete
        # file to its own learner-visible module. Keep lesson ids stable: they
        # key translations, imports, progress and assessment history.
        grouped = {order: [item] for order, item in enumerate(sorted(loaded, key=lesson_position), 1)}
    else:
        for item in sorted(loaded, key=lesson_position):
            grouped.setdefault(int(item[1].MODULE_ORDER), []).append(item)

    modules: List[ModuleSpec] = []
    # `MODULE_ORDER` is the author's identity for a module (it can follow the
    # source book's chapter numbers and skip some, as COURSE-002 and COURSE-006
    # do) and picks the stable module id. What a learner sees as "Module N" is
    # the module's position in the course, so it never has a gap.
    for position, (module_order, items) in enumerate(sorted(grouped.items()), start=1):
        _first_path, first = items[0]
        module_id = _module_id_for_order(course_id, module_order, known_module_ids, id_style)
        module = ModuleSpec(
            module_id=module_id,
            order=position,
            title=N.as_text(first.MODULE_TITLE),
            description=N.as_text(first.MODULE_DESCRIPTION) or None,
        )
        for index, (path, authored) in enumerate(items, start=1):
            lesson = _topic_lesson(
                course_id,
                module_id,
                index,
                N.as_text(authored.LESSON_CODE),
                _sym(authored, "TOPIC", path),
                _rel(path, root),
                difficulty,
            )
            # Consolidated authors use readable ids such as M01.L01.EX01 in
            # every course. Namespace assessment ids at the loader boundary so
            # independently authored courses can coexist in one catalogue.
            prefix = f"{course_id}."
            for exercise in lesson.exercises:
                if exercise.exercise_id and not exercise.exercise_id.startswith(prefix):
                    local_id = exercise.exercise_id
                    if not local_id.startswith(f"{lesson.lesson_id}."):
                        local_id = f"{lesson.lesson_id}.{local_id}"
                    exercise.exercise_id = prefix + local_id
            for question in lesson.questions:
                if question.question_id and not question.question_id.startswith(prefix):
                    local_id = question.question_id
                    if not local_id.startswith(f"{lesson.lesson_id}."):
                        local_id = f"{lesson.lesson_id}.{local_id}"
                    question.question_id = prefix + local_id
            module.lessons.append(lesson)
        if file_modules:
            # A chapter file is both the module and its sole lesson. The
            # learner-facing lesson title is more precise than the broad
            # legacy MODULE_TITLE copied into every converted file.
            module.title = module.lessons[0].title
        modules.append(module)

    raw_title = manifest.get("course_title") or manifest.get("title")
    if raw_title:
        english, _, arabic = N.as_text(raw_title).partition("|")
        title, title_ar = english.strip(), arabic.strip() or None
    else:
        title, title_ar = root.name.split("_", 1)[-1].replace("_", " "), None

    capstone = None
    project_file = root / "course_project.py"
    if project_file.is_file():
        project_module = load_py(project_file)
        capstone = _capstone(
            getattr(project_module, "CAPSTONE", None) or getattr(project_module, "COURSE_PROJECT", None),
            f"{course_id} capstone",
            difficulty,
        )

    course = CourseSpec(
        course_id=course_id,
        source_dir=root.name,
        title=title,
        title_ar=title_ar,
        modules=modules,
        capstone=capstone,
        manifest_prerequisites=manifest_prerequisites(manifest),
        embedded_quizzes_are_canonical=True,
    )
    _consolidate_embedded_quizzes(course, known_quiz_ids)
    return course


# ─── Layout 2: COURSE-002/003 - manifest lists lessons by file ──────────────

def _load_manifest_lessons(root: Path, course_id: str) -> CourseSpec:
    manifest = read_json(root / "course_manifest.json")
    difficulty = _default_difficulty(course_id, manifest)
    modules: List[ModuleSpec] = []
    listed: set = set()
    missing: List[str] = []
    for order, entry in enumerate(manifest["modules"], start=1):
        module = ModuleSpec(
            module_id=str(entry["module_id"]), order=order, title=N.as_text(entry["title"]),
            title_ar=N.as_text(entry.get("arabic_title")) or None,
            description=N.as_text(entry.get("learning_objective")) or None,
            optional=bool(entry.get("optional")),
        )
        for index, item in enumerate(entry["lessons"], start=1):
            path = root / item["file"]
            listed.add(path.resolve())
            if not path.is_file():
                missing.append(_rel(path, root))
                continue
            mod = load_py(path)
            topic = _sym(mod, "TOPIC", path)
            module.lessons.append(_topic_lesson(course_id, module.module_id, index, str(item["id"]), topic,
                                                _rel(path, root), difficulty))
        # A project lives on a lesson's TOPIC; the manifest's is used only when no
        # lesson in the module carries one, so a module never gets it twice.
        if not any(l.project for l in module.lessons):
            module.project = N.norm_project(entry.get("project"), f"{course_id} {module.module_id}", difficulty)
        modules.append(module)
    on_disk = {p.resolve() for p in (root / "modules").rglob("*.py") if p.name != "__init__.py"}
    english, _, arabic = N.as_text(manifest.get("title")).partition("|")
    spec = CourseSpec(
        course_id=course_id, source_dir=root.name, title=english.strip(), title_ar=arabic.strip() or None, modules=modules,
        declared_modules=manifest.get("module_count"), declared_lessons=manifest.get("lesson_count"),
        manifest_prerequisites=manifest_prerequisites(manifest), missing_files=missing,
        unloaded_files=sorted(_rel(p, root) for p in on_disk - listed),
    )
    return spec


# ─── Layout 3: COURSES 004/005/007/008 - modules/M00X_NN_*/module.py ─────────

def _load_module_py(root: Path, course_id: str) -> CourseSpec:
    manifest = read_json(root / "course_manifest.json")
    difficulty = _default_difficulty(course_id, manifest)
    modules: List[ModuleSpec] = []
    missing: List[str] = []
    unloaded: List[str] = []
    for order, module_dir in enumerate(sorted(p for p in (root / "modules").iterdir() if p.is_dir() and (p / "module.py").is_file()), start=1):
        header = load_py(module_dir / "module.py")
        meta = _sym(header, "MODULE", module_dir / "module.py")
        module_id = N.module_id_for(course_id, meta["id"])
        module = ModuleSpec(
            module_id=module_id,
            order=order,
            title=N.as_text(meta["title"]),
            description=N.as_text(meta.get("summary")) or None,
            optional=bool(meta.get("optional")),
            completion_required=meta.get("completion_required"),
            is_capstone=bool(meta.get("capstone")),
        )
        stems = list(_sym(header, "LESSON_FILES", module_dir / "module.py"))
        for index, stem in enumerate(stems, start=1):
            path = module_dir / f"{stem}.py"
            if not path.is_file():
                missing.append(_rel(path, root))
                continue
            mod = load_py(path)
            topic = _sym(mod, "TOPIC", path)
            module.lessons.append(_topic_lesson(
                course_id, module_id, index, N.lesson_id_for(course_id, _sym(mod, "LESSON_ID", path)), topic,
                _rel(path, root), difficulty,
            ))
        listed = {f"{s}.py" for s in stems}
        unloaded += [_rel(p, root) for p in module_dir.glob("L*.py") if p.name not in listed]
        modules.append(module)
    capstone = None
    project_file = root / "course_project.py"
    if project_file.is_file():
        project_module = load_py(project_file)
        capstone = _capstone(
            getattr(project_module, "CAPSTONE", None) or getattr(project_module, "COURSE_PROJECT", None),
            f"{course_id} capstone", difficulty,
        )
    return CourseSpec(
        course_id=course_id, source_dir=root.name, title=N.as_text(manifest["course_title"]), modules=modules,
        capstone=capstone, declared_modules=manifest.get("modules"), declared_lessons=manifest.get("lessons"),
        manifest_prerequisites=manifest_prerequisites(manifest), missing_files=missing, unloaded_files=unloaded,
    )


# ─── Layout 4: COURSE-006 - outline only (no lesson text) ───────────────────

def _load_outline(root: Path, course_id: str) -> CourseSpec:
    """COURSE-006 ships each lesson as a title, objectives and a generic
    outline - no lesson body. Nothing is written from an outline: the modules
    (real titles, real lesson counts and minutes) are imported so the course can
    be listed, and it stays non-startable until the lessons are written."""
    manifest = read_json(root / "course_manifest.json")
    modules: List[ModuleSpec] = []
    outline = 0
    for order, module_dir in enumerate(sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("m006_")), start=1):
        meta = _sym(load_py(module_dir / "module_manifest.py"), "MODULE", module_dir)
        lessons = [_sym(load_py(f), "LESSON", f) for f in _ordered(module_dir, "l006_*.py")]
        outline += len(lessons)
        module = ModuleSpec(
            module_id=str(meta["module_id"]), order=order, title=N.as_text(meta["title"]),
            description=None,
            declared_minutes=sum(int(l.get("guided_minutes") or 0) for l in lessons) or None,
            declared_lesson_ids=[N.lesson_id_for(course_id, lesson.get("lesson_id")) for lesson in lessons],
        )
        for lesson in lessons:
            lesson_id = N.lesson_id_for(course_id, lesson.get("lesson_id"))
            questions = N.norm_questions(lesson.get("quiz"), f"{course_id} {lesson_id}")
            for question in questions:
                question.lesson_id = question.lesson_id or lesson_id
            module.legacy_question_sources[lesson_id] = questions
        modules.append(module)
    return CourseSpec(
        course_id=course_id, source_dir=root.name, title=N.as_text(manifest["course_title"]), modules=modules,
        declared_modules=manifest.get("modules"), declared_lessons=manifest.get("lessons"),
        manifest_prerequisites=manifest_prerequisites(manifest), has_lesson_bodies=False, outline_lesson_count=outline,
    )


# ─── Layout 5: COURSES 009/010 - M00X-NN_*/l00X-NNN_*.py ────────────────────

def _load_lettered_modules(root: Path, course_id: str) -> CourseSpec:
    manifest = read_json(root / "course_manifest.json")
    difficulty = _default_difficulty(course_id, manifest)
    number = course_id.split("-")[1]
    modules: List[ModuleSpec] = []
    for order, module_dir in enumerate(sorted(p for p in root.iterdir() if p.is_dir() and re.match(rf"^M{number}-\d{{2}}", p.name)), start=1):
        module_id = N.module_id_for(course_id, module_dir.name.split("_")[0])
        lessons = _ordered(module_dir, f"l{number}-*.py")
        module = ModuleSpec(module_id=module_id, order=order, title="")
        for index, path in enumerate(lessons, start=1):
            mod = load_py(path)
            meta = _sym(mod, "LESSON_META", path)
            module.title = module.title or N.as_text(meta.get("module_title"))
            topic = _sym(mod, "TOPIC", path)
            module.lessons.append(_topic_lesson(
                course_id, module_id, index, N.lesson_id_for(course_id, _sym(mod, "LESSON_ID", path)), topic,
                _rel(path, root), difficulty,
            ))
        project_file = module_dir / "module_project.py"
        if project_file.is_file():
            module.project = N.norm_project(_sym(load_py(project_file), "MODULE_PROJECT", project_file),
                                            f"{course_id} {module_id}", difficulty)
        modules.append(module)
    return CourseSpec(
        course_id=course_id, source_dir=root.name, title=N.as_text(manifest["course_title"]), modules=modules,
        declared_modules=manifest.get("modules"), declared_lessons=manifest.get("lessons"),
        manifest_prerequisites=manifest_prerequisites(manifest),
    )


# ─── Layout 6: COURSE-011 - modules/M011-NN_*/lesson_order.json ─────────────

def _load_json_ordered(root: Path, course_id: str) -> CourseSpec:
    manifest = read_json(root / "course_manifest.json")
    difficulty = "intermediate"
    modules: List[ModuleSpec] = []
    missing: List[str] = []
    unloaded: List[str] = []
    for order, module_dir in enumerate(sorted(p for p in (root / "modules").iterdir() if p.is_dir()), start=1):
        meta = read_json(module_dir / "module_manifest.json")
        module_id = N.module_id_for(course_id, meta["module_id"])
        module = ModuleSpec(
            module_id=module_id,
            order=order,
            title=N.as_text(meta["title"]),
            description=N.as_text(meta.get("summary")) or None,
            optional=bool(meta.get("optional")),
            completion_required=meta.get("completion_required"),
            is_capstone=bool(meta.get("capstone")),
        )
        names = read_json(module_dir / "lesson_order.json")
        for index, name in enumerate(names, start=1):
            path = module_dir / name
            if not path.is_file():
                missing.append(_rel(path, root))
                continue
            mod = load_py(path)
            info = _sym(mod, "LESSON_META", path)
            module.lessons.append(_lesson(
                course_id, module_id, index, lesson_id=N.lesson_id_for(course_id, info["lesson_id"]),
                title=info["title"], content=_sym(mod, "LESSON_MARKDOWN", path), minutes=info.get("estimated_minutes"),
                difficulty=info.get("difficulty"), description=info.get("learning_objective"),
                exercises=getattr(mod, "EXERCISES", None), quiz=getattr(mod, "QUIZ", None),
                project=getattr(mod, "PROJECT", None), file=_rel(path, root), course_difficulty=difficulty,
            ))
        unloaded += [_rel(p, root) for p in module_dir.glob("L*.py") if p.name not in names]
        modules.append(module)
    totals = manifest.get("totals") or {}
    return CourseSpec(
        course_id=course_id, source_dir=root.name, title=N.as_text(manifest["course_title"]), modules=modules,
        declared_modules=totals.get("modules"), declared_lessons=totals.get("lessons"),
        manifest_prerequisites=manifest_prerequisites(manifest), missing_files=missing, unloaded_files=unloaded,
    )


# ─── Layout 7: COURSE-012 - module_NN_*/lesson_NNN.py ───────────────────────

def _load_lesson_numbered(root: Path, course_id: str) -> CourseSpec:
    manifest = read_json(root / "course_manifest.json")
    difficulty = _default_difficulty(course_id, manifest)
    inventory = {e["folder"]: e for e in manifest["module_inventory"]}
    modules: List[ModuleSpec] = []
    unlisted: List[str] = []
    for order, module_dir in enumerate(sorted(p for p in root.iterdir() if p.is_dir() and re.match(r"^module_\d{2}_", p.name)), start=1):
        entry = inventory.get(module_dir.name)
        if entry is None:
            unlisted.append(module_dir.name)
            continue
        module_id = N.module_id_for(course_id, entry["module_id"])
        module = ModuleSpec(module_id=module_id, order=order, title=N.as_text(entry["title"]))
        for index, path in enumerate(_ordered(module_dir, "lesson_*.py"), start=1):
            mod = load_py(path)
            meta = _sym(mod, "LESSON_META", path)
            topic = _sym(mod, "TOPIC", path)
            module.lessons.append(_lesson(
                course_id, module_id, index, lesson_id=N.lesson_id_for(course_id, meta["lesson_id"]),
                title=topic.get("title") or meta["title"], content=(topic.get("lesson") or {}).get("content_markdown"),
                minutes=topic.get("estimated_minutes") or meta.get("estimated_minutes"),
                difficulty=topic.get("difficulty") or meta.get("difficulty"), description=topic.get("description"),
                exercises=getattr(mod, "EXERCISES", None) or topic.get("exercises"),
                quiz=getattr(mod, "QUIZ", None) or topic.get("quiz"), project=getattr(mod, "PROJECT", None),
                file=_rel(path, root), course_difficulty=difficulty,
            ))
        project_file = module_dir / "module_project.py"
        if project_file.is_file():
            module.project = N.norm_project(_sym(load_py(project_file), "PROJECT", project_file),
                                            f"{course_id} {module_id}", difficulty)
        modules.append(module)
    capstone = None
    capstone_file = root / "capstone" / "capstone.py"
    if capstone_file.is_file():
        capstone = _capstone(_sym(load_py(capstone_file), "CAPSTONE", capstone_file), f"{course_id} capstone", difficulty)
    return CourseSpec(
        course_id=course_id, source_dir=root.name, title=N.as_text(manifest["course_title"]), modules=modules,
        capstone=capstone, declared_modules=manifest.get("modules"), declared_lessons=manifest.get("lessons"),
        manifest_prerequisites=manifest_prerequisites(manifest),
        unloaded_files=[f"{name} (module folder not in course_manifest module_inventory)" for name in unlisted],
    )


# ─── Layout 8: COURSE-013 - M013-NN_*/L013-NNN_*.py + modules_manifest.json ─

def _load_modules_manifest(root: Path, course_id: str) -> CourseSpec:
    manifest = read_json(root / "course_manifest.json")
    modules_manifest = read_json(root / "modules_manifest.json")
    difficulty = "beginner"
    number = course_id.split("-")[1]
    modules: List[ModuleSpec] = []
    missing: List[str] = []
    unloaded: List[str] = []
    on_disk = {p.name: p for p in root.glob(f"M{number}-*/L{number}-*.py")}
    for order, entry in enumerate(modules_manifest, start=1):
        module_id = N.module_id_for(course_id, entry["module_id"])
        module_dir = next((p for p in root.iterdir() if p.is_dir() and p.name.startswith(f"{entry['module_id']}_")), None)
        module = ModuleSpec(module_id=module_id, order=order, title=N.as_text(entry["title"]),
                            description=N.as_text(entry.get("description")) or None)
        if module_dir is None:
            missing.append(f"{entry['module_id']}_* (module folder)")
            modules.append(module)
            continue
        for index, lesson_id in enumerate(entry["lessons"], start=1):
            path = next(iter(sorted(module_dir.glob(f"{lesson_id}_*.py"))), None)
            if path is None:
                missing.append(f"{module_dir.name}/{lesson_id}_*.py")
                continue
            on_disk.pop(path.name, None)
            mod = load_py(path)
            info = _sym(mod, "LESSON_META", path)
            topic = _sym(mod, "TOPIC", path)
            module.lessons.append(_lesson(
                course_id, module_id, index, lesson_id=N.lesson_id_for(course_id, info["lesson_id"]),
                title=topic.get("title") or info["title"], content=topic.get("content_markdown"),
                minutes=info.get("estimated_minutes"), difficulty=info.get("difficulty"),
                description=info.get("learning_objective"), exercises=topic.get("exercises"),
                quiz=topic.get("quiz"), file=_rel(path, root), course_difficulty=difficulty,
            ))
        project_file = module_dir / "module_project.py"
        if project_file.is_file():
            module.project = N.norm_project(_sym(load_py(project_file), "PROJECT", project_file),
                                            f"{course_id} {module_id}", difficulty)
        lab_file = module_dir / "guided_lab.py"
        if lab_file.is_file():
            lab = _sym(load_py(lab_file), "LAB", lab_file)
            module.lab = N.norm_project({**lab, "title": f"Guided lab: {lab.get('title')}"}, f"{course_id} {module_id} lab", difficulty)
        modules.append(module)
    unloaded += [_rel(p, root) for p in on_disk.values()]
    capstone = None
    capstone_file = root / "final_capstone" / "capstone.py"
    if capstone_file.is_file():
        capstone = _capstone(_sym(load_py(capstone_file), "CAPSTONE", capstone_file), f"{course_id} capstone", difficulty)
    return CourseSpec(
        course_id=course_id, source_dir=root.name, title=N.as_text(manifest["course_title"]), modules=modules,
        capstone=capstone, declared_modules=manifest.get("modules"), declared_lessons=manifest.get("lessons"),
        manifest_prerequisites=manifest_prerequisites(manifest), missing_files=missing, unloaded_files=unloaded,
    )


# ─── Layout 10: COURSE-015 - bare M0XX-NN/ dirs, module_manifest.json + L0XX-NNN.py ──

def _load_bare_numbered_modules(root: Path, course_id: str) -> CourseSpec:
    """Each module is a bare `M0XX-NN` directory (no descriptive suffix)
    holding `module_manifest.json` (title + the ordered `lesson_ids` it
    owns) and one `L0XX-NNN.py` per lesson, each carrying its own
    `LESSON_META` + a flat `TOPIC` (content directly on the dict, not
    nested under a `lesson` key). Per-module and capstone projects are
    separate JSON files under `projects/`, not embedded in a lesson."""
    manifest = read_json(root / "course_manifest.json")
    difficulty = _default_difficulty(course_id, manifest)
    number = course_id.split("-")[1]
    modules: List[ModuleSpec] = []
    missing: List[str] = []
    for order, module_dir in enumerate(
        sorted(p for p in root.iterdir() if p.is_dir() and re.match(rf"^M{number}-\d{{2}}$", p.name)), start=1
    ):
        meta = read_json(module_dir / "module_manifest.json")
        module_id = N.module_id_for(course_id, meta["module_id"])
        module = ModuleSpec(
            module_id=module_id,
            order=order,
            title=N.as_text(meta["title"]),
            description=N.as_text(meta.get("summary")) or None,
            optional=bool(meta.get("optional")),
            completion_required=meta.get("completion_required"),
            is_capstone=bool(meta.get("capstone")),
        )
        for index, lesson_id in enumerate(meta.get("lesson_ids") or [], start=1):
            candidates = sorted(module_dir.glob(f"{lesson_id}*.py"))
            if not candidates:
                missing.append(f"{module_dir.name}/{lesson_id}*.py")
                continue
            path = candidates[0]
            mod = load_py(path)
            topic = _sym(mod, "TOPIC", path)
            lesson_meta = _sym(mod, "LESSON_META", path)
            module.lessons.append(_lesson(
                course_id, module_id, index, lesson_id=N.lesson_id_for(course_id, _sym(mod, "LESSON_ID", path)),
                title=topic.get("title") or lesson_meta.get("title"),
                content=topic.get("content"),
                minutes=topic.get("duration_minutes") or lesson_meta.get("duration_minutes"),
                difficulty=topic.get("difficulty"), description=topic.get("description"),
                exercises=getattr(mod, "EXERCISES", None) or topic.get("exercises"),
                quiz=getattr(mod, "QUIZ", None) or topic.get("quiz"),
                project=getattr(mod, "MODULE_PROJECT", None) or getattr(mod, "PROJECT", None),
                file=_rel(path, root), course_difficulty=difficulty,
            ))
        project_file = root / "projects" / f"{module_id}_project.json"
        if project_file.is_file():
            module.project = N.norm_project(read_json(project_file), f"{course_id} {module_id}", difficulty)
        modules.append(module)
    capstone = None
    capstone_file = root / "projects" / "final_capstone.json"
    if capstone_file.is_file():
        capstone = _capstone(read_json(capstone_file), f"{course_id} capstone", difficulty)
    return CourseSpec(
        course_id=course_id, source_dir=root.name, title=N.as_text(manifest["course_title"]), modules=modules,
        capstone=capstone, declared_modules=manifest.get("modules"), declared_lessons=manifest.get("lessons"),
        manifest_prerequisites=manifest_prerequisites(manifest), missing_files=missing,
    )


# ─── Layout 9: COURSE-014 - m014_NN_*/l014_NNN_*.py, titles in the README ───

_README_MODULE_ROW = re.compile(r"^\|\s*(M\d{3}-\d{2})\s*\|\s*(.+?)\s*\|\s*\d+\s*\|", re.MULTILINE)


def _load_flat_lessons(root: Path, course_id: str) -> CourseSpec:
    manifest = read_json(root / "course_manifest.json")
    difficulty = "intermediate"
    number = course_id.split("-")[1]
    titles = {m: t for m, t in _README_MODULE_ROW.findall((root / "README.md").read_text(encoding="utf-8"))}
    modules: List[ModuleSpec] = []
    for order, module_dir in enumerate(sorted(p for p in root.iterdir() if p.is_dir() and re.match(rf"^m{number}_\d{{2}}_", p.name)), start=1):
        module_id = f"M{number}-{module_dir.name.split('_')[1]}"
        title = titles.get(module_id) or module_dir.name.split("_", 2)[2].replace("-", " ").title()
        module = ModuleSpec(module_id=module_id, order=order, title=title)
        for index, path in enumerate(_ordered(module_dir, f"l{number}_*.py"), start=1):
            mod = load_py(path)
            info = _sym(mod, "LESSON_META", path)
            topic = _sym(mod, "TOPIC", path)
            module.lessons.append(_lesson(
                course_id, module_id, index, lesson_id=N.lesson_id_for(course_id, _sym(mod, "LESSON_ID", path)),
                title=topic.get("title") or info["title"], content=topic.get("content_markdown"),
                minutes=topic.get("estimated_minutes") or info.get("estimated_minutes"),
                difficulty=None, description=topic.get("description") or info.get("learning_objective"),
                exercises=getattr(mod, "EXERCISES", None), quiz=getattr(mod, "QUIZ", None),
                project=getattr(mod, "PROJECT", None), file=_rel(path, root), course_difficulty=difficulty,
            ))
        modules.append(module)
    capstone = None
    capstone_md = root / "CAPSTONE.md"
    if capstone_md.is_file() and manifest.get("course_capstone"):
        capstone = N.norm_project(
            {"title": manifest["course_capstone"], "description": capstone_md.read_text(encoding="utf-8")},
            f"{course_id} capstone", difficulty,
        )
    return CourseSpec(
        course_id=course_id, source_dir=root.name, title=N.as_text(manifest["course_title"]), modules=modules,
        capstone=capstone, declared_modules=manifest.get("modules"), declared_lessons=manifest.get("lessons"),
        manifest_prerequisites=manifest_prerequisites(manifest),
    )


# ─── Dispatcher ─────────────────────────────────────────────────────────────

def _layout(root: Path) -> Callable[[Path, str], CourseSpec]:
    """The loader for this folder, chosen from what is in it."""
    if _consolidated_files(root):
        return _load_consolidated_topics
    if (root / "lessons").is_dir() and any(p.name.startswith("module_") for p in (root / "lessons").iterdir()):
        return _load_module_dirs_001
    manifest_file = root / "course_manifest.json"
    manifest = read_json(manifest_file) if manifest_file.is_file() else {}
    modules = manifest.get("modules")
    if isinstance(modules, list) and modules and isinstance(modules[0], dict) and "lessons" in modules[0] \
            and isinstance(modules[0]["lessons"], list) and modules[0]["lessons"] and isinstance(modules[0]["lessons"][0], dict) \
            and "file" in modules[0]["lessons"][0]:
        return _load_manifest_lessons
    modules_dir = root / "modules"
    if modules_dir.is_dir() and any((p / "module.py").is_file() for p in modules_dir.iterdir() if p.is_dir()):
        return _load_module_py
    if any(p.is_dir() and p.name.startswith("m006_") for p in root.iterdir()):
        return _load_outline
    if any(p.is_dir() and re.match(r"^M\d{3}-\d{2}_", p.name) for p in root.iterdir()):
        return _load_modules_manifest if (root / "modules_manifest.json").is_file() else _load_lettered_modules
    if (root / "modules").is_dir() and any((p / "lesson_order.json").is_file() for p in (root / "modules").iterdir() if p.is_dir()):
        return _load_json_ordered
    if any(p.is_dir() and re.match(r"^module_\d{2}_", p.name) for p in root.iterdir()):
        return _load_lesson_numbered
    if any(p.is_dir() and re.match(r"^m\d{3}_\d{2}_", p.name) for p in root.iterdir()):
        return _load_flat_lessons
    if any(
        p.is_dir() and re.match(r"^M\d{3}-\d{2}$", p.name) and (p / "module_manifest.json").is_file()
        for p in root.iterdir()
    ):
        return _load_bare_numbered_modules
    raise CurriculumError([f"{root.name}: folder layout not recognised - add a loader for it"])


def load_course_dir(root: Path) -> CourseSpec:
    course_id = course_id_of(root)
    content_root = root
    # A course folder can wrap its real content in one redundant nested
    # directory literally named after the course id - an extraction
    # artifact (COURSE-015 ships this way). When the outer folder has no
    # layout of its own but that exact subdirectory does, descend into it;
    # everything else about the course (its id, its listing) still comes
    # from the outer folder's name.
    nested = root / course_id
    if nested.is_dir():
        try:
            _layout(root)
        except CurriculumError:
            content_root = nested
    spec = _layout(content_root)(content_root, course_id)
    spec.source_dir = root.name
    _consolidate_module_projects(spec)
    if not spec.embedded_quizzes_are_canonical:
        _consolidate_module_quizzes(spec, content_root)
    from app.services.curriculum.course_exercise_definitions import apply_deterministic_course_exercises
    apply_deterministic_course_exercises(spec)
    apply_fill_in_blank_format(spec)
    apply_pending_code_classification(spec)
    # Figures are course-level, whatever the lesson layout: one manifest per folder.
    images = load_asset_manifest(content_root, store_root=root.parent)
    spec.assets, spec.asset_problems = images.assets, images.problems
    spec.asset_warnings, spec.broken_asset_keys = images.warnings, images.broken_keys
    # Arabic from the folder's `ar/` (absent = none yet); after the quizzes are consolidated, because
    # an Arabic question attaches to the English question it is the twin of.
    attach_arabic(spec, content_root, root)
    # After the Arabic, whose source hash covers the authored English exercise text.
    from app.services.curriculum.guided import apply_guided_exercises
    apply_guided_exercises(spec)
    manifest_file = content_root / "course_manifest.json"
    manifest = read_json(manifest_file) if manifest_file.is_file() else {}
    file_modules = manifest.get("consolidated_file_modules") is True
    keep_module_ar_descriptions = manifest.get("consolidated_module_ar_descriptions") is True
    # When a one-lesson module intentionally shares the lesson's English
    # title, its translated lesson title is also the best module title. In a
    # promoted-file layout it must override ar/_course.json: those entries use
    # the old grouped module ids and can otherwise attach to the wrong chapter.
    for module in spec.modules:
        if len(module.lessons) == 1 and module.title == module.lessons[0].title:
            if file_modules:
                module.title_ar = module.lessons[0].title_ar or module.title_ar
                if not keep_module_ar_descriptions:
                    module.description_ar = None
            elif not module.title_ar:
                module.title_ar = module.lessons[0].title_ar
    return spec


def load_all_courses(root: Path = COURSES_ROOT, only: Optional[List[str]] = None) -> List[CourseSpec]:
    """Every course folder under `root`, loaded - or, with `only`, just the
    course ids named (in `root`'s own folder order). A folder whose id is not
    in `only` is never opened, so a course that cannot load at all (not just
    one that fails semantic validation) can still be excluded."""
    dirs = course_dirs(root)
    if only is not None:
        wanted = set(only)
        dirs = [d for d in dirs if course_id_of(d) in wanted]
    return [load_course_dir(d) for d in dirs]
