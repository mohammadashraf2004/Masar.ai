"""
app/services/curriculum/spec.py

The one shape every course folder is normalised into before anything touches
the database.

The course folders under `backend/courses/` were authored in several layouts
(one Python module per lesson, a manifest per course, per-module manifests, ...).
Each layout has a loader in `loaders.py` that produces a `CourseSpec`; the
importer only ever reads this shape. That keeps "how a folder is laid out" and
"how the catalogue stores it" independent of each other, and it is what makes
the validation rules below possible to state once for every course.

Nothing here knows about SQLAlchemy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

# Kept as strings, not the ORM enum, so this module has no database dependency.
DIFFICULTIES = ("beginner", "intermediate", "advanced")


class CurriculumError(Exception):
    """A course folder is structurally invalid. Raised - never swallowed - so a
    seed run stops instead of importing a partial course."""

    def __init__(self, problems: List[str]):
        self.problems = list(problems)
        super().__init__("\n".join(f"  - {p}" for p in self.problems))


@dataclass
class AssetSpec:
    """One image a course's lessons can place with `{{image:<key>}}` (or `{{figure:<key>}}`).

    `file` is relative to the course folder; `storage_key` is relative to the
    courses root (what the asset store resolves). Type, size, hash and dimensions
    are read from the file itself when the manifest is loaded, never trusted from
    the manifest."""
    key: str
    file: str
    alt: str
    caption: Optional[str] = None
    # Shown to learners only when the manifest sets it.
    figure_number: Optional[str] = None
    # Where the figure came from in the source material; for authors only.
    source_reference: Optional[str] = None
    storage_key: str = ""
    mime_type: str = ""
    byte_size: int = 0
    sha256: str = ""
    width: Optional[int] = None
    height: Optional[int] = None
    # Arabic description and caption; `alt` / `caption` are the English ones. A missing Arabic
    # value falls back to the English at read time. The picture itself is shared.
    alt_ar: Optional[str] = None
    caption_ar: Optional[str] = None
    # The lesson the image was made for (informational; any lesson may place it).
    lesson: Optional[str] = None


@dataclass
class QuestionSpec:
    question: str
    # None for an open-ended question (graded through the AI answer chat).
    options: Optional[List[str]] = None
    correct: Optional[int] = None
    explanation: str = ""
    question_id: str = ""
    lesson_id: str = ""
    # Reserved for the uncommon assessment that genuinely spans lessons.
    lesson_ids: List[str] = field(default_factory=list)
    metadata: Dict[str, object] = field(default_factory=dict)
    # The Arabic twin from the course's `ar/` folder: {question, options, explanation}, with the
    # options in the order the English was *authored* in (the importer reorders them to follow
    # the English if it rebalances the key). None when the question has no Arabic yet.
    ar: Optional[Dict[str, Any]] = None

    @property
    def is_open(self) -> bool:
        return self.options is None

    def as_json(self) -> Dict[str, object]:
        """The shape `quizzes.questions` already uses."""
        trace = dict(self.metadata)
        if self.question_id:
            trace["id"] = self.question_id
        if self.lesson_id:
            trace["lesson_id"] = self.lesson_id
        if self.lesson_ids:
            trace.pop("lesson_id", None)
            trace["lesson_ids"] = list(self.lesson_ids)
        if self.is_open:
            return {**trace, "question": self.question, "type": "open", "explanation": self.explanation}
        return {
            **trace, "question": self.question, "options": list(self.options or []),
            "correct": self.correct, "explanation": self.explanation,
        }


@dataclass
class ExerciseSpec:
    title: str
    description: str
    difficulty: str
    skill_tested: List[str] = field(default_factory=list)
    starter_code: Optional[str] = None
    solution_code: Optional[str] = None
    exercise_type: str = "legacy"
    language: Optional[str] = None
    pre_exercise_code: Optional[str] = None
    tests: List[Dict[str, Any]] = field(default_factory=list)
    hint: Optional[str] = None
    success_message: Optional[str] = None
    exercise_id: str = ""
    course_id: str = ""
    module_id: str = ""
    lesson_id: str = ""
    title_ar: Optional[str] = None
    description_ar: Optional[str] = None
    hint_ar: Optional[str] = None
    success_message_ar: Optional[str] = None


@dataclass
class ProjectSpec:
    title: str
    description: str
    difficulty: str
    tech_stack: List[str] = field(default_factory=list)
    objectives: List[str] = field(default_factory=list)
    rubric: Dict[str, float] = field(default_factory=dict)
    starter_repo_url: Optional[str] = None
    estimated_hours: Optional[float] = None


@dataclass
class LessonSpec:
    lesson_id: str
    module_id: str
    order: int
    title: str
    content: str
    # None when the course does not say (COURSE-011): never guessed.
    estimated_minutes: Optional[int]
    difficulty: str
    skill_tags: List[str] = field(default_factory=list)
    description: Optional[str] = None
    exercises: List[ExerciseSpec] = field(default_factory=list)
    # Loader staging only. Legacy source files keep their question banks beside
    # the lesson for compatibility; load_course_dir moves them into ModuleSpec.quiz.
    questions: List[QuestionSpec] = field(default_factory=list)
    project: Optional[ProjectSpec] = None
    source_file: str = ""
    # Arabic from the course's `ar/` folder, whole (code already put back). English stays in
    # `title`/`content`; these only ever fill the `*_ar` columns.
    title_ar: Optional[str] = None
    content_ar: Optional[str] = None

    @property
    def has_code_examples(self) -> bool:
        return "```" in self.content


@dataclass
class ModuleSpec:
    module_id: str
    order: int
    title: str
    title_ar: Optional[str] = None
    description: Optional[str] = None
    description_ar: Optional[str] = None
    lessons: List[LessonSpec] = field(default_factory=list)
    quiz: Optional["ModuleQuizSpec"] = None
    project: Optional[ProjectSpec] = None
    # Modules the source marks optional (e.g. the elective chapters of COURSE-003).
    optional: bool = False
    # None follows `not optional`; an explicit source value can distinguish a
    # project-only/capstone module from an optional specialization.
    completion_required: Optional[bool] = None
    # A hands-on lab that accompanies the module (COURSE-013's `guided_lab.py`).
    lab: Optional[ProjectSpec] = None
    # Minutes the source declares for a module whose lessons are not imported.
    declared_minutes: Optional[int] = None
    # Outline-only courses can still validate assessment traceability without
    # pretending that an outline is a complete, renderable lesson body.
    declared_lesson_ids: List[str] = field(default_factory=list)
    # Temporary loader bridge for outline-only sources that still author real
    # assessment questions. Cleared after module-quiz consolidation.
    legacy_question_sources: Dict[str, List[QuestionSpec]] = field(default_factory=dict, repr=False)
    # A project-only terminal module may intentionally have no lesson bodies.
    is_capstone: bool = False

    @property
    def estimated_minutes(self) -> Optional[int]:
        """Sum of the lessons' own estimates; None when no lesson states one."""
        stated = [l.estimated_minutes for l in self.lessons if l.estimated_minutes is not None]
        if stated:
            return sum(stated)
        return self.declared_minutes

    @property
    def counts_toward_completion(self) -> bool:
        return not self.optional if self.completion_required is None else self.completion_required


@dataclass
class ModuleQuizSpec:
    quiz_id: str
    module_id: str
    title: str
    questions: List[QuestionSpec] = field(default_factory=list)


@dataclass
class CourseSpec:
    course_id: str                      # 'COURSE-004' - the frozen id in the export
    source_dir: str
    title: str
    modules: List[ModuleSpec] = field(default_factory=list)
    # A bilingual manifest title ('English | العربية') is split into both halves.
    title_ar: Optional[str] = None
    # Optional course-level Arabic summary from ar/_course.json. The registry's
    # English capability remains the canonical English description.
    description_ar: Optional[str] = None
    capstone: Optional[ProjectSpec] = None
    # Counts the course's own manifest declares. Checked against what was
    # actually loaded, so a folder with a missing lesson file cannot pass.
    declared_modules: Optional[int] = None
    declared_lessons: Optional[int] = None
    # Course ids named in the manifest's prerequisites (raw mentions, in order).
    # (course id, 'required' | 'recommended') pairs, in manifest order.
    manifest_prerequisites: List[Tuple[str, str]] = field(default_factory=list)
    # True when the folder carries lesson *text*. A folder with only an outline
    # (COURSE-006) imports its structure and stays a non-startable shell.
    has_lesson_bodies: bool = True
    # Lessons an outline-only folder lists (they are counted, not imported).
    outline_lesson_count: int = 0
    # Lesson ids present on disk but never loaded (or the reverse), reported by
    # the loader so validation can fail on them.
    unloaded_files: List[str] = field(default_factory=list)
    missing_files: List[str] = field(default_factory=list)
    # The figures the course ships (`assets_manifest.json`), and anything wrong
    # with that manifest, reported by validation like every other structural fault.
    assets: List[AssetSpec] = field(default_factory=list)
    asset_problems: List[str] = field(default_factory=list)
    # Things worth fixing in the manifest that do not stop an import.
    asset_warnings: List[str] = field(default_factory=list)
    # Keys the manifest declares whose file is missing or unusable; counted by the image report.
    broken_asset_keys: List[str] = field(default_factory=list)
    # Problems in the optional canonical module-quiz manifest.
    structure_problems: List[str] = field(default_factory=list)
    # Consolidated exports keep the complete lesson and its assessment in one
    # file. Their loader promotes those questions directly to a module quiz,
    # so the legacy module_quizzes.json index must not be applied again.
    embedded_quizzes_are_canonical: bool = False
    # Faults in the course's Arabic files (`ar/`) fail validation like any other structural fault;
    # a warning (an Arabic file made from an older English text) is reported and does not.
    arabic_problems: List[str] = field(default_factory=list)
    arabic_warnings: List[str] = field(default_factory=list)

    @property
    def slug(self) -> str:
        return self.course_id.lower()

    @property
    def lessons(self) -> List[LessonSpec]:
        return [lesson for module in self.modules for lesson in module.lessons]

    @property
    def estimated_minutes(self) -> Optional[int]:
        stated = [m.estimated_minutes for m in self.modules if m.estimated_minutes is not None]
        return sum(stated) if stated else None
