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
from typing import Dict, List, Optional, Tuple

# Kept as strings, not the ORM enum, so this module has no database dependency.
DIFFICULTIES = ("beginner", "intermediate", "advanced")


class CurriculumError(Exception):
    """A course folder is structurally invalid. Raised - never swallowed - so a
    seed run stops instead of importing a partial course."""

    def __init__(self, problems: List[str]):
        self.problems = list(problems)
        super().__init__("\n".join(f"  - {p}" for p in self.problems))


@dataclass
class QuestionSpec:
    question: str
    # None for an open-ended question (graded through the AI answer chat).
    options: Optional[List[str]] = None
    correct: Optional[int] = None
    explanation: str = ""

    @property
    def is_open(self) -> bool:
        return self.options is None

    def as_json(self) -> Dict[str, object]:
        """The shape `quizzes.questions` already uses."""
        if self.is_open:
            return {"question": self.question, "type": "open", "explanation": self.explanation}
        return {
            "question": self.question, "options": list(self.options or []),
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
    questions: List[QuestionSpec] = field(default_factory=list)
    project: Optional[ProjectSpec] = None
    source_file: str = ""

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
    lessons: List[LessonSpec] = field(default_factory=list)
    project: Optional[ProjectSpec] = None
    # Modules the source marks optional (e.g. the elective chapters of COURSE-003).
    optional: bool = False
    # A hands-on lab that accompanies the module (COURSE-013's `guided_lab.py`).
    lab: Optional[ProjectSpec] = None
    # Minutes the source declares for a module whose lessons are not imported.
    declared_minutes: Optional[int] = None

    @property
    def estimated_minutes(self) -> Optional[int]:
        """Sum of the lessons' own estimates; None when no lesson states one."""
        stated = [l.estimated_minutes for l in self.lessons if l.estimated_minutes is not None]
        if stated:
            return sum(stated)
        return self.declared_minutes


@dataclass
class CourseSpec:
    course_id: str                      # 'COURSE-004' - the frozen id in the export
    source_dir: str
    title: str
    modules: List[ModuleSpec] = field(default_factory=list)
    # A bilingual manifest title ('English | العربية') is split into both halves.
    title_ar: Optional[str] = None
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
