"""
Public browsing, authenticated learning.

Anyone may explore Masar - the course, track, challenge and Project Lab
catalogues, course outlines, tools, vocabulary, plans and prices - but every
endpoint that serves learning content, takes an action, or reads an account
requires a signed-in user. These tests pin that boundary at the API, where it
actually holds, rather than trusting the frontend's route guards:

  * every route is either authenticated or on an explicit public allowlist, so
    a new route can never become public by accident;
  * every authenticated route answers an anonymous caller with 401;
  * the public catalogue responses carry no lesson body, exercise, answer,
    dataset, hint, rubric or attempt.
"""
import json
import re
import uuid

import pytest
from fastapi.routing import APIRoute

from app.core import security
from app.models.challenge import ChallengeAttempt, ChallengeDifficulty, ChallengeProject
from tests.conftest import verify_registered
from tests.learning_fixtures import learn_catalog, learn_client, learn_db, legacy_catalog, logs_enabled  # noqa: F401

API = "/api/v1"
PASSWORD = "correct-horse-battery-staple-7"

# Every route an anonymous caller may reach. Adding to this list is a product
# decision: it must be catalogue/metadata only, or a webhook/auth flow.
PUBLIC_ROUTES = {
    ("GET", "/"), ("GET", "/health"), ("GET", "/metrics"),
    # Signing in, signing up, recovering an account.
    ("POST", f"{API}/auth/login"), ("POST", f"{API}/auth/register"),
    ("POST", f"{API}/auth/forgot-password"), ("POST", f"{API}/auth/reset-password"),
    ("POST", f"{API}/auth/verify-email"),
    # Plans and prices.
    ("GET", f"{API}/billing/catalog"), ("GET", f"{API}/billing/courses/{{course_id}}/offer"),
    ("GET", f"{API}/exam-payments/price"), ("GET", f"{API}/wallet/costs"), ("GET", f"{API}/wallet/packages"),
    # Public certificate verification (by its id, nothing else).
    ("GET", f"{API}/exams/certificates/{{certificate_id}}"),
    # The learning catalogue: courses, outlines, tracks, paths, taxonomy.
    ("GET", f"{API}/learning/career-goals"), ("GET", f"{API}/learning/courses"),
    ("GET", f"{API}/learning/courses/{{slug}}"), ("GET", f"{API}/learning/courses/{{slug}}/assets/{{key}}"),
    ("GET", f"{API}/learning/fields"), ("GET", f"{API}/learning/levels"), ("GET", f"{API}/learning/paths"),
    ("GET", f"{API}/learning/paths/{{slug}}"), ("GET", f"{API}/learning/skills"),
    ("GET", f"{API}/learning/tracks"), ("GET", f"{API}/learning/tracks/{{goal}}/workflow"),
    ("GET", f"{API}/learning/tracks/{{slug}}"), ("GET", f"{API}/learning/tracks/{{slug}}/courses"),
    ("GET", f"{API}/tracks/"), ("GET", f"{API}/tracks/{{slug}}"), ("GET", f"{API}/tool-courses/"),
    # Challenge and Project Lab catalogues (cards and overviews only).
    ("GET", f"{API}/challenges/catalog"),
    ("GET", f"{API}/project-lab/projects"), ("GET", f"{API}/project-lab/projects/{{slug}}"),
    # Vocabulary, terminology and search.
    ("GET", f"{API}/terminology/"), ("GET", f"{API}/vocabulary/"), ("GET", f"{API}/vocabulary/categories"),
    ("GET", f"{API}/vocabulary/courses"), ("GET", f"{API}/vocabulary/{{slug}}"), ("GET", f"{API}/search/"),
    # Legal documents.
    ("GET", f"{API}/legal/versions"), ("GET", f"{API}/legal/{{kind}}"),
    # Payment provider callbacks: authenticated by signature, not by a user.
    ("GET", f"{API}/payments/kashier/return"), ("POST", f"{API}/payments/kashier/webhook"),
    ("GET", f"{API}/payments/paymob/callback"), ("POST", f"{API}/payments/paymob/webhook"),
}


def _routes():
    """(method, path, dependency calls) for every API route, through included routers."""
    from app.main import app

    def walk(dep, seen):
        for sub in dep.dependencies:
            if sub.call is not None:
                seen.add(sub.call)
            walk(sub, seen)
        return seen

    out = []

    def visit(routes, prefix, inherited):
        for r in routes:
            if type(r).__name__ == "_IncludedRouter":
                ctx = r.include_context
                deps = [d.dependency for d in (ctx.dependencies or [])]
                deps += [d.dependency for d in (r.original_router.dependencies or [])]
                visit(r.original_router.routes, prefix + ctx.prefix, inherited + deps)
            elif hasattr(r, "include_router") is False and isinstance(r, APIRoute):
                calls = walk(r.dependant, set()) | set(inherited)
                for method in r.methods:
                    out.append((method, prefix + r.path, calls))

    visit(app.routes, "", [])
    assert len(out) > 150, "route discovery found too few routes - the walker is broken"
    return out


def _requires_user(calls) -> bool:
    return security.get_current_user in calls


def test_every_route_is_authenticated_or_explicitly_public():
    unexpected = sorted(
        f"{m} {p}" for m, p, calls in _routes()
        if not _requires_user(calls) and (m, p) not in PUBLIC_ROUTES
    )
    assert not unexpected, "routes reachable without signing in that are not on the allowlist:\n" + "\n".join(unexpected)


def test_the_allowlist_has_no_stale_entries():
    live = {(m, p) for m, p, calls in _routes() if not _requires_user(calls)}
    assert PUBLIC_ROUTES <= live, sorted(PUBLIC_ROUTES - live)


def _fill(path: str) -> str:
    return re.sub(r"\{[^}]+\}", "1", path)


def test_every_authenticated_route_rejects_an_anonymous_caller(api):
    """No token -> 401, before the endpoint body, a payment or a lookup runs."""
    failures = []
    for method, path, calls in _routes():
        if not _requires_user(calls):
            continue
        resp = api.request(method, _fill(path), json={} if method in ("POST", "PUT", "PATCH") else None)
        if resp.status_code != 401:
            failures.append(f"{method} {path} -> {resp.status_code}")
    assert not failures, "\n".join(failures)


# ─── Challenges ──────────────────────────────────────────────────────────────

SECRET_DATASET = "row-only-an-enrolled-learner-may-see"
SECRET_HINT = "hint-only-an-enrolled-learner-may-see"
SECRET_RUBRIC = "rubric-criterion-kept-private"


@pytest.fixture()
def challenge(db):
    ch = ChallengeProject(
        title="Public Catalogue Challenge", slug=f"pub-chal-{uuid.uuid4().hex[:8]}",
        description="Clean a dirty dataset.", difficulty=ChallengeDifficulty.beginner,
        credit_cost=25, passing_score=70.0, max_attempts=3, is_active=True,
        dirty_dataset=[{"value": SECRET_DATASET}], dataset_description="A dirty export.",
        dataset_filename="dirty.csv", grading_rubric=[{"criterion": SECRET_RUBRIC, "weight": 100}],
        hints=[SECRET_HINT], tags=["pandas"],
    )
    db.add(ch)
    db.commit()
    db.refresh(ch)
    yield ch
    db.query(ChallengeAttempt).filter(ChallengeAttempt.challenge_id == ch.id).delete()
    db.delete(ch)
    db.commit()


def test_the_challenge_catalogue_is_public_and_shows_only_the_card(client, challenge):
    resp = client.get(f"{API}/challenges/catalog")
    assert resp.status_code == 200
    card = next(c for c in resp.json() if c["slug"] == challenge.slug)
    assert set(card) == {"id", "title", "slug", "difficulty", "credit_cost", "passing_score",
                         "max_attempts", "description", "tags"}
    assert card["description"] == "Clean a dirty dataset." and card["tags"] == ["pandas"]
    for secret in (SECRET_DATASET, SECRET_HINT, SECRET_RUBRIC, "dirty.csv", "A dirty export."):
        assert secret not in resp.text


def test_a_challenge_inactive_in_the_catalogue_is_not_listed(client, db, challenge):
    challenge.is_active = False
    db.commit()
    assert challenge.slug not in {c["slug"] for c in client.get(f"{API}/challenges/catalog").json()}


@pytest.mark.parametrize("method,suffix", [
    ("get", ""), ("get", "/attempts"), ("get", "/dataset/download"),
    ("post", "/enroll"), ("post", "/submit"), ("post", "/hint"),
])
def test_challenge_content_and_actions_need_an_account(client, challenge, method, suffix):
    resp = getattr(client, method)(f"{API}/challenges/{challenge.slug}{suffix}",
                                   **({"json": {}} if method == "post" else {}))
    assert resp.status_code == 401
    assert SECRET_DATASET not in resp.text and SECRET_HINT not in resp.text


def test_catalog_is_not_mistaken_for_a_challenge_slug_when_signed_in(client, challenge):
    resp = client.post(f"{API}/auth/register", json={
        "accept_terms": True, "accept_privacy": True, "email": f"pub-{uuid.uuid4().hex[:10]}@example.com",
        "full_name": "Public Browser", "password": PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    verify_registered(client, resp.json()["user"]["id"])
    headers = {"Authorization": f"Bearer {resp.json()['access_token']}"}
    # The signed-in list and detail keep their richer shape (enrolment state).
    listed = client.get(f"{API}/challenges/", headers=headers).json()
    assert any(c["slug"] == challenge.slug and c["is_enrolled"] is False for c in listed)
    assert client.get(f"{API}/challenges/catalog", headers=headers).status_code == 200


# ─── Course outlines ─────────────────────────────────────────────────────────

BODY_KEYS = {"content", "content_ar", "body", "blocks", "solution", "solution_code", "starter_code",
             "expected_output", "test_cases", "answer", "answers", "correct_answer", "correct_option",
             "explanation", "questions", "instructions", "hints", "rubric"}


def _keys(value, found=None):
    found = set() if found is None else found
    if isinstance(value, dict):
        for k, v in value.items():
            found.add(k)
            _keys(v, found)
    elif isinstance(value, list):
        for v in value:
            _keys(v, found)
    return found


def test_a_course_outline_is_public_with_lesson_titles_and_no_lesson_content(learn_client, learn_db, legacy_catalog):  # noqa: F811
    from app.models.learning import Lesson

    resp = learn_client.get(f"{API}/learning/courses/langchain")
    assert resp.status_code == 200
    course = resp.json()
    lessons = [lesson for m in course["modules"] for lesson in m["lessons"]]
    assert lessons, "the outline should name the lessons"
    for lesson in lessons:
        assert set(lesson) == {"id", "order", "title", "title_ar"}
    assert not (_keys(course) & BODY_KEYS), _keys(course) & BODY_KEYS
    assert course["enrollment"] is None
    assert all(m["completion_pct"] is None for m in course["modules"])

    # The outline's lesson count agrees with each module's own count.
    for module in course["modules"]:
        assert len(module["lessons"]) == module["lesson_count"]

    # And none of the real lesson bodies appear anywhere in the response.
    ids = [lesson["id"] for lesson in lessons]
    bodies = [b for (b,) in learn_db.query(Lesson.content).filter(Lesson.id.in_(ids)).all() if b and len(b) > 40]
    text = json.dumps(course)
    for body in bodies:
        assert body[:40] not in text


@pytest.mark.parametrize("path", [
    "tool-courses/langchain", "tool-courses/topics/1", "tool-courses/topics/1/progress",
    "learning/courses/langchain/progress", "learning/courses/langchain/access",
    "learning/courses/langchain/readiness", "tracks/topics/1",
])
def test_lesson_bodies_and_progress_need_an_account(learn_client, legacy_catalog, path):  # noqa: F811
    assert learn_client.get(f"{API}/{path}").status_code == 401


@pytest.mark.parametrize("method,path", [
    ("post", "learning/courses/langchain/enroll"),
    ("post", "tool-courses/enroll"),
    ("post", "tracks/enroll"),
    ("post", "challenges/anything/enroll"),
    ("post", "challenges/anything/submit"),
    ("post", "project-lab/projects/anything/start"),
    ("post", "practice/exercises/1/run"),
    ("post", "practice/exercises/1/submit"),
    ("post", "tracks/quizzes/1/submit"),
    ("post", "tracks/topics/1/progress"),
    ("post", "tool-courses/topics/1/progress"),
    ("post", "mentor/chat"),
])
def test_enrolling_starting_submitting_or_saving_progress_needs_an_account(client, method, path):
    assert getattr(client, method)(f"{API}/{path}", json={}).status_code == 401
