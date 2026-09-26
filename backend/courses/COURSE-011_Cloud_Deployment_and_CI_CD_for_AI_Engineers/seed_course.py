"""Generic seed entry point for COURSE-011.

Replace `persist_payload` with a repository-specific adapter after mapping the
generic curriculum payload to Masar's actual models. Do not invent database fields.
"""
from course_data import load_course_payload

def persist_payload(payload: dict) -> None:
    # Repository-neutral default: inspection only.
    # Real Masar integration should upsert by stable IDs/slugs and preserve learner progress.
    course = payload["course"]
    lesson_count = sum(len(m["lessons"]) for m in payload["modules"])
    print(f"Prepared {course['course_id']} — {course['course_title']}")
    print(f"Modules: {len(payload['modules'])}")
    print(f"Lessons: {lesson_count}")
    print("No database write performed: repository/schema adapter not provided.")

if __name__ == "__main__":
    persist_payload(load_course_payload())
