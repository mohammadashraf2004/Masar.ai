"""
Fixtures for the curriculum-import and independent-enrollment tests.

Small, generated course folders - two modules of two lessons, each lesson with
exercises and a three-question quiz - are imported through the real importer over
the real seeded catalogue. The catalogue's own relations (roles, prerequisites,
stages) come from `learn_catalog`, so a course such as `course-002` has exactly the
prerequisites and roadmap places it has in production; only its *lessons* are
test data. The real course folders are exercised separately, by
`test_curriculum_import.py`.
"""
from typing import Dict, Iterable, List

from sqlalchemy.orm import Session

from app.models.learning import Exercise, Lesson, Quiz
from app.models.learning_path import Course
from app.models.progress import UserProgress
from app.models.tool_course import ToolTopic
from app.services.curriculum import importer
from app.services.curriculum.spec import (
    CourseSpec, ExerciseSpec, LessonSpec, ModuleQuizSpec, ModuleSpec, ProjectSpec, QuestionSpec,
)
from seeds import curriculum as cfg

# A small chain with real registry prerequisites (001 -> 002 -> 003, 001/002/003 -> 004)
# plus two independent beginner courses.
SMALL_COURSES = ("COURSE-001", "COURSE-002", "COURSE-003", "COURSE-004", "COURSE-013", "COURSE-014")


def make_spec(course_id: str, *, modules: int = 2, lessons: int = 2, title: str = "") -> CourseSpec:
    number = course_id.split("-")[1]
    spec = CourseSpec(course_id=course_id, source_dir=f"test-{number}", title=title or f"Course {number}")
    for m in range(1, modules + 1):
        module = ModuleSpec(module_id=f"M{number}-{m:02d}", order=m, title=f"Module {m} of {number}")
        for l in range(1, lessons + 1):
            lesson_id = f"L{number}-{m:02d}{l:02d}"
            module.lessons.append(LessonSpec(
                lesson_id=lesson_id, module_id=module.module_id, order=l, title=f"Lesson {m}.{l} of {number}",
                content=f"# Lesson {m}.{l}\n\nBody of {lesson_id}.", estimated_minutes=30, difficulty="beginner",
                skill_tags=["testing"],
                exercises=[ExerciseSpec(
                    f"Exercise {lesson_id}-{x}", f"Do task {x} of {lesson_id}.", "beginner",
                    exercise_id=f"EX-{lesson_id}-{x:02d}", course_id=course_id,
                    module_id=module.module_id, lesson_id=lesson_id,
                )
                           for x in (1, 2)],
                questions=[
                    QuestionSpec(
                        f"{lesson_id} question {q}: which option is right?",
                        [f"option A of {lesson_id}-{q}", f"option B of {lesson_id}-{q}", f"option C of {lesson_id}-{q}",
                         f"option D of {lesson_id}-{q}"], 1, f"Explained for {lesson_id}-{q}.",
                        f"Q-{module.module_id}-{(l - 1) * 3 + q:03d}", lesson_id)
                    for q in (1, 2, 3)
                ],
            ))
        questions = [question for lesson in module.lessons for question in lesson.questions]
        for lesson in module.lessons:
            lesson.questions = []
        module.quiz = ModuleQuizSpec(
            quiz_id=f"QUIZ-{module.module_id}", module_id=module.module_id,
            title=f"Module quiz: {module.title}", questions=questions,
        )
        module.project = ProjectSpec(f"Project of {module.module_id}", "Build the thing.", "beginner",
                                     objectives=["one", "two"], estimated_hours=2.0)
        spec.modules.append(module)
    spec.capstone = ProjectSpec(f"Capstone {number}", "Put it all together.", "intermediate")
    return spec


def import_small_courses(db: Session, ids: Iterable[str] = SMALL_COURSES) -> List[Course]:
    """Give the catalogue's shell courses real (small) content."""
    definitions = {d["course_id"]: d for d in cfg.COURSE_DIRECTORY_COURSES}
    courses = []
    for course_id in ids:
        report = importer.import_course(db, make_spec(course_id), definitions[course_id])
        assert report.lessons.created > 0
        courses.append(db.query(Course).filter(Course.slug == course_id.lower()).one())
    db.commit()
    return courses


def topic_ids(db: Session, course: Course) -> List[int]:
    return [t.id for t in db.query(ToolTopic).filter(ToolTopic.tool_course_id == course.tool_course_id)
            .order_by(ToolTopic.order).all()]


def finish_topics(db: Session, user_id: int, course: Course, *, upto: int = None) -> None:
    """Mark every lesson and exercise of the course's first `upto` modules done
    (all of them by default) the way the progress endpoints record it."""
    for tid in topic_ids(db, course)[:upto]:
        lessons = [l.id for l in db.query(Lesson).filter(Lesson.tool_topic_id == tid).all()]
        exercises = [e.id for e in db.query(Exercise).filter(Exercise.tool_topic_id == tid).all()]
        row = db.query(UserProgress).filter(UserProgress.user_id == user_id, UserProgress.tool_topic_id == tid).first()
        if row is None:
            db.add(UserProgress(user_id=user_id, tool_topic_id=tid, lessons_completed=lessons,
                                exercises_completed=exercises))
        else:
            row.lessons_completed, row.exercises_completed = lessons, exercises
    db.commit()


def correct_answers(db: Session, question_ids: Iterable[str]) -> Dict[str, int]:
    """The answer key, read straight from the stored quizzes - for tests only."""
    answers = {}
    for qid in question_ids:
        quiz_id, index = (int(x) for x in qid.split(":"))
        answers[qid] = db.query(Quiz).filter(Quiz.id == quiz_id).one().questions[index]["correct"]
    return answers
