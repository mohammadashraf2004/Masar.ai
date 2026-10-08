"""A locked exercise in /tracks must be redacted exactly like /tool-courses:
no description, starter code, hints (en/ar) or grading flag."""
from types import SimpleNamespace

from app.controllers import tracks_controller


class _Query:
    def __init__(self, rows):
        self.rows = rows

    def filter(self, *args, **kwargs):
        return self

    def all(self):
        return self.rows


def test_locked_track_exercise_hides_its_hints(monkeypatch):
    course = SimpleNamespace(track_level_id=7, slug="paid-course")
    data = {"levels": [{"id": 7, "topics": [{
        "lessons": [], "projects": [], "quizzes": [],
        "exercises": [{
            "id": 1, "description": "d", "description_ar": "د", "starter_code": "x = 1",
            "hint": "use groupby", "hint_ar": "استخدم groupby", "grading_available": True,
        }],
    }]}]}
    monkeypatch.setattr(tracks_controller, "CareerTrackResponse",
                        SimpleNamespace(model_validate=lambda _t: SimpleNamespace(model_dump=lambda: data)))
    monkeypatch.setattr(tracks_controller, "course_access", lambda *_a: SimpleNamespace(has_access=False))
    monkeypatch.setattr(tracks_controller, "free_lesson_ids", lambda *_a: set())
    monkeypatch.setattr(tracks_controller, "free_preview_content_ids", lambda *_a: (set(), set()))
    track = SimpleNamespace(levels=[SimpleNamespace(id=7)])
    db = SimpleNamespace(query=lambda *_a: _Query([course]))

    out = tracks_controller._redact_locked_track(track, user_id=1, db=db)

    exercise = out["levels"][0]["topics"][0]["exercises"][0]
    assert exercise["is_locked"] is True
    assert exercise["hint"] is None and exercise["hint_ar"] is None
    assert exercise["grading_available"] is False
    assert exercise["starter_code"] is None and exercise["description"] == ""
