"""
Logging and metrics around profile creation, path generation and catalogue
problems.

Two properties matter: the events an operator needs are actually emitted (a
failed generation, a prerequisite cycle, a rejected profile), and nothing
personal is in them — ids and catalogue slugs only.
"""
import logging

import pytest
from prometheus_client import REGISTRY

from app.models.learning_path import Course, CoursePrerequisite
from app.services.learning import learning_service as svc
from tests.learning_fixtures import *  # noqa: F401,F403
from tests.learning_fixtures import register

API = "/api/v1/learning"
SERVICE_LOGGER = "app.services.learning.learning_service"


def _count(name, **labels):
    return REGISTRY.get_sample_value(name, labels) or 0.0


@pytest.fixture()
def deltas():
    """Read a counter's change across a `with` block."""
    class _Delta:
        def __init__(self):
            self.before = {}

        def start(self, name, **labels):
            self.before[(name, tuple(sorted(labels.items())))] = _count(name, **labels)

        def change(self, name, **labels):
            return _count(name, **labels) - self.before[(name, tuple(sorted(labels.items())))]
    return _Delta()


def _generate(client, who, **body):
    body = {"level": "intermediate", "fields": ["nlp"], "career_goal": "ai-engineer", **body}
    return client.post(f"{API}/paths/generate", headers=who["headers"], json=body)


# ─── Metrics ────────────────────────────────────────────────────────────────

def test_a_generation_is_counted_and_timed(learn_client, legacy_catalog, deltas):
    who = register(learn_client)
    deltas.start("learning_path_generations_total", outcome="ok")
    deltas.start("learning_path_generation_seconds_count")
    assert _generate(learn_client, who).status_code == 200
    assert deltas.change("learning_path_generations_total", outcome="ok") == 1
    assert deltas.change("learning_path_generation_seconds_count") == 1


def test_a_rejected_generation_is_counted_separately(learn_client, legacy_catalog, deltas):
    who = register(learn_client)
    deltas.start("learning_path_generations_total", outcome="rejected")
    assert _generate(learn_client, who, career_goal="chef").status_code == 422
    assert deltas.change("learning_path_generations_total", outcome="rejected") == 1


def test_a_route_with_nothing_published_is_counted_as_empty_not_ok(learn_client, legacy_catalog, deltas):
    who = register(learn_client)
    deltas.start("learning_path_generations_total", outcome="empty")
    deltas.start("learning_path_generations_total", outcome="ok")
    resp = _generate(learn_client, who, level="beginner", fields=["data"], career_goal="data-analyst")
    assert resp.status_code == 200
    assert "no_available_courses" in [a["code"] for a in resp.json()["advisories"]]
    assert deltas.change("learning_path_generations_total", outcome="empty") == 1
    assert deltas.change("learning_path_generations_total", outcome="ok") == 0


def test_a_failing_generation_is_counted_and_logged_with_a_traceback(learn_db, legacy_catalog, deltas, caplog, logs_enabled, monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("catalogue exploded")

    monkeypatch.setattr(svc, "generate_plan", boom)
    deltas.start("learning_path_generations_total", outcome="error")
    with caplog.at_level(logging.ERROR, logger=SERVICE_LOGGER):
        with pytest.raises(RuntimeError):
            svc.generate(learn_db, level="beginner", career_goal="ai-engineer", fields=["nlp"])
    assert deltas.change("learning_path_generations_total", outcome="error") == 1
    record = next(r for r in caplog.records if r.getMessage() == "learning path generation failed")
    assert record.exc_info is not None and record.career_goal == "ai-engineer"


def test_profile_saves_are_counted_by_outcome(learn_client, legacy_catalog, deltas):
    who = register(learn_client)
    for outcome in ("created", "updated", "rejected"):
        deltas.start("learning_profile_events_total", outcome=outcome)
    put = lambda body: learn_client.put(f"{API}/my-profile", headers=who["headers"], json=body)  # noqa: E731
    assert put({"level": "beginner"}).status_code == 200
    assert put({"fields": ["nlp"]}).status_code == 200
    assert put({"level": "expert"}).status_code == 422
    assert deltas.change("learning_profile_events_total", outcome="created") == 1
    assert deltas.change("learning_profile_events_total", outcome="updated") == 1
    assert deltas.change("learning_profile_events_total", outcome="rejected") == 1


def test_metric_labels_are_a_fixed_vocabulary_never_a_slug_or_an_id(learn_client, legacy_catalog):
    who = register(learn_client)
    _generate(learn_client, who, fields=["speech"], career_goal="ml-engineer")
    labels = {
        tuple(sorted(s.labels.items()))
        for family in REGISTRY.collect() if family.name.startswith("learning_")
        for s in family.samples
    }
    values = {v for label in labels for _, v in label}
    assert not values & {"speech", "ml-engineer", "nlp", "ai-engineer", str(who["id"])}


# ─── Invalid prerequisite graphs ────────────────────────────────────────────

def _make_cycle(db):
    a = db.query(Course).filter(Course.slug == "langchain").one()
    b = db.query(Course).filter(Course.slug == "llamaindex").one()
    db.add_all([CoursePrerequisite(course_id=a.id, prerequisite_course_id=b.id),
                CoursePrerequisite(course_id=b.id, prerequisite_course_id=a.id)])
    db.commit()


def test_a_prerequisite_cycle_is_reported_but_never_breaks_a_learner(learn_client, legacy_catalog, learn_db, deltas, caplog, logs_enabled):
    _make_cycle(learn_db)  # written around the API, which would have refused it
    who = register(learn_client)
    deltas.start("learning_catalog_issues_total", issue="prerequisite_cycle")
    with caplog.at_level(logging.WARNING, logger=SERVICE_LOGGER):
        resp = _generate(learn_client, who)
    assert resp.status_code == 200
    assert "prerequisite_cycle" in [a["code"] for a in resp.json()["advisories"]]
    assert deltas.change("learning_catalog_issues_total", issue="prerequisite_cycle") == 1
    warning = next(r for r in caplog.records if r.getMessage() == "learning catalogue issue: prerequisite_cycle")
    assert warning.levelno == logging.WARNING and warning.career_goal == "ai-engineer"


def test_a_career_goal_without_a_template_is_reported(learn_client, legacy_catalog, learn_db, deltas):
    from app.models.learning_path import PathTemplate

    learn_db.query(PathTemplate).filter(PathTemplate.slug == "mlops-engineer-path").delete()
    learn_db.commit()
    who = register(learn_client)
    deltas.start("learning_catalog_issues_total", issue="no_template")
    resp = _generate(learn_client, who, career_goal="mlops-engineer", fields=[])
    assert resp.status_code == 200 and resp.json()["template_slug"] is None
    assert deltas.change("learning_catalog_issues_total", issue="no_template") == 1


# ─── What is and is not logged ──────────────────────────────────────────────

def test_logs_carry_ids_and_slugs_never_personal_data(learn_client, legacy_catalog, caplog, logs_enabled):
    who = register(learn_client)
    with caplog.at_level(logging.DEBUG, logger=SERVICE_LOGGER):
        learn_client.put(f"{API}/my-profile", headers=who["headers"],
                         json={"level": "advanced", "fields": ["speech"], "career_goal": "ai-engineer"})
        learn_client.put(f"{API}/my-path", headers=who["headers"], json={})
    ours = [r for r in caplog.records if r.name == SERVICE_LOGGER]
    assert {r.getMessage() for r in ours} >= {"learning profile saved", "learning path generated"}
    generated = next(r for r in ours if r.getMessage() == "learning path generated")
    assert generated.user_id == who["id"] and generated.level == "advanced" and generated.fields == ["speech"]
    dump = " ".join(f"{r.getMessage()} {sorted(r.__dict__.items(), key=str)}" for r in ours)
    assert who["email"] not in dump and "Learner Test" not in dump and "Bearer" not in dump
