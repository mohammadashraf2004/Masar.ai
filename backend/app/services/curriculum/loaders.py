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
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple

from app.services.curriculum import normalize as N
from app.services.curriculum.assets import load_assets
from app.services.curriculum.spec import (
    CourseSpec, CurriculumError, LessonSpec, ModuleSpec, ProjectSpec,
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
    return LessonSpec(
        lesson_id=lesson_id, module_id=module_id, order=order,
        title=N.as_text(title), content=N.as_text(content),
        estimated_minutes=int(minutes) if isinstance(minutes, (int, float)) and not isinstance(minutes, bool) else None,
        difficulty=diff, skill_tags=N.norm_tags(tags), description=N.as_text(description) or None,
        exercises=N.norm_exercises(exercises, where, diff),
        questions=N.norm_questions(quiz, where),
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
        module = ModuleSpec(module_id=module_id, order=order, title=N.as_text(meta["title"]))
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
        modules.append(ModuleSpec(
            module_id=str(meta["module_id"]), order=order, title=N.as_text(meta["title"]),
            description=None,
            declared_minutes=sum(int(l.get("guided_minutes") or 0) for l in lessons) or None,
        ))
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
        module = ModuleSpec(module_id=module_id, order=order, title=N.as_text(meta["title"]))
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
    raise CurriculumError([f"{root.name}: folder layout not recognised - add a loader for it"])


def load_course_dir(root: Path) -> CourseSpec:
    spec = _layout(root)(root, course_id_of(root))
    # Figures are course-level, whatever the lesson layout: one manifest per folder.
    spec.assets, spec.asset_problems = load_assets(root)
    return spec


def load_all_courses(root: Path = COURSES_ROOT) -> List[CourseSpec]:
    return [load_course_dir(d) for d in course_dirs(root)]
