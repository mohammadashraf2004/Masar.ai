"""Profile practice activity: per-day counts in the learner's timezone and the
current streak, from records that carry a time."""
from datetime import datetime, timezone

from app.services import learning_activity
from tests.test_code_exercise_api import _register, code_exercise  # noqa: F401  (fixture)

NOW = datetime(2026, 10, 9, 22, 30, tzinfo=timezone.utc)  # 01:30 on 10 Oct in Cairo (UTC+3)


def _with(monkeypatch, moments):
    monkeypatch.setattr(learning_activity, "_timestamps", lambda db, user_id, since: list(moments))


def test_days_are_counted_in_the_learners_timezone(monkeypatch):
    _with(monkeypatch, [datetime(2026, 10, 9, 21, 15, tzinfo=timezone.utc)])  # 00:15 on 10 Oct in Cairo
    utc = learning_activity.daily_activity(None, 1, days=3, now=NOW)
    cairo = learning_activity.daily_activity(None, 1, days=3, tz_offset_minutes=-180, now=NOW)
    assert [d["date"] for d in utc["days"]] == ["2026-10-07", "2026-10-08", "2026-10-09"]
    assert utc["days"][-1]["count"] == 1
    assert [d["date"] for d in cairo["days"]] == ["2026-10-08", "2026-10-09", "2026-10-10"]
    assert cairo["days"][-1]["count"] == 1 and cairo["days"][-2]["count"] == 0


def test_streak_counts_consecutive_days_and_survives_an_empty_today(monkeypatch):
    day = lambda d, h=12: datetime(2026, 10, d, h, tzinfo=timezone.utc)  # noqa: E731
    _with(monkeypatch, [day(8), day(8, 15), day(7), day(6), day(4)])
    result = learning_activity.daily_activity(None, 1, days=7, now=NOW)
    # 9 Oct (today) is empty, 8-7-6 are active, 5 is a gap.
    assert result["current_streak"] == 3
    assert result["active_days"] == 4
    assert {d["date"]: d["count"] for d in result["days"]}["2026-10-08"] == 2

    _with(monkeypatch, [day(9), day(7)])
    assert learning_activity.daily_activity(None, 1, days=7, now=NOW)["current_streak"] == 1
    _with(monkeypatch, [day(7)])
    assert learning_activity.daily_activity(None, 1, days=7, now=NOW)["current_streak"] == 0


def test_activity_outside_the_window_is_ignored(monkeypatch):
    _with(monkeypatch, [datetime(2026, 9, 1, tzinfo=timezone.utc)])
    result = learning_activity.daily_activity(None, 1, days=7, now=NOW)
    assert result["active_days"] == 0 and len(result["days"]) == 7


def test_a_checked_exercise_shows_up_as_activity_today(client, db, code_exercise):  # noqa: F811
    _, headers = _register(client)
    base = "/api/v1/profile/activity"
    assert client.get(base, headers=headers).json()["active_days"] == 0
    client.post(
        f"/api/v1/practice/exercises/{code_exercise.id}/submit",
        headers=headers, json={"code": "value = 3.14159\nresult = round(value, 2)"},
    )
    body = client.get(f"{base}?days=7", headers=headers).json()
    assert len(body["days"]) == 7
    assert body["days"][-1]["count"] >= 1
    assert (body["active_days"], body["current_streak"]) == (1, 1)
    assert client.get(base).status_code in (401, 403)
    assert client.get(f"{base}?days=0", headers=headers).status_code == 422
