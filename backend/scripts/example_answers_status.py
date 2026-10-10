"""Coverage of example answers for written exercises, and the briefs still to write.

    python scripts/example_answers_status.py                    # coverage per course
    python scripts/example_answers_status.py COURSE-008         # briefs without an example
    python scripts/example_answers_status.py COURSE-008 0 12    # only items 0..11 of that list

Run it from backend/ with the application importable (the test image), as
the loader reads the real course folders. See docs/written-example-answers-guide.md.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.curriculum.examples import COMPLETE_COURSES  # noqa: E402
from app.services.curriculum.loaders import load_all_courses  # noqa: E402


def main(argv: list[str]) -> int:
    courses = load_all_courses()
    if not argv:
        total = done = 0
        for course in courses:
            written = [e for lesson in course.lessons for e in lesson.exercises if e.exercise_type != "code"]
            if not written:
                continue
            have = sum(bool(e.example_answer) for e in written)
            total, done = total + len(written), done + have
            mark = "complete" if course.course_id in COMPLETE_COURSES else ""
            print(f"{course.course_id}  {have:>4}/{len(written):<4} {mark}")
        print(f"TOTAL        {done:>4}/{total}")
        return 0
    course_id = argv[0]
    start = int(argv[1]) if len(argv) > 1 else 0
    end = start + int(argv[2]) if len(argv) > 2 else None
    course = next((c for c in courses if c.course_id == course_id), None)
    if course is None:
        print(f"unknown course {course_id}")
        return 1
    todo = [
        (lesson, e) for lesson in course.lessons for e in lesson.exercises
        if e.exercise_type != "code" and not e.example_answer
    ]
    print(f"{course.course_id} {course.title}: {len(todo)} written exercises without an example answer")
    for lesson, exercise in todo[start:end]:
        brief = re.sub(r"\n{2,}", "\n", exercise.description or "").strip()
        print(f"\n### {exercise.exercise_id} | {lesson.title} | {exercise.title}\n{brief}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
