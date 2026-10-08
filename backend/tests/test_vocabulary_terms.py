"""
Covers the normalized AI Vocabulary dictionary (migration 022):

  * canonical uniqueness (slug is the identity, no duplicate concept rows)
  * aliases are searchable without creating a second row for the same concept
  * English / Arabic / category / difficulty / course filters, and pagination
  * detail lookup: related terms, course mappings, progress state
  * progress is upgrade-only, same rule as the legacy /terminology/progress
  * seed idempotency: running the upsert twice leaves row counts unchanged
"""
import uuid

import pytest

from app.models.vocabulary import TermStatus, UserTermProgress
from app.models.vocabulary_term import (
    VocabularyTerm,
    VocabularyTermAssociation,
    VocabularyTermRelation,
)


def _slug(name: str) -> str:
    return f"{name}_{uuid.uuid4().hex[:8]}"


def _register(client) -> tuple[str, int]:
    email = f"vocab-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post(
        "/api/v1/auth/register",
        json={
            "accept_terms": True, "accept_privacy": True,
            "email": email, "full_name": "Vocab Test", "password": "correcthorsebatterystaple",
        },
    )
    assert resp.status_code == 201
    body = resp.json()
    return body["access_token"], body["user"]["id"]


def make_term(db, *, slug=None, term_en="Embedding", term_ar="تمثيل", category="RAG",
              difficulty="intermediate", aliases=None, definition_en="def", definition_ar="تعريف"):
    term = VocabularyTerm(
        slug=slug or _slug("term"),
        term_en=term_en,
        term_ar=term_ar,
        aliases=aliases or [],
        category=category,
        difficulty=difficulty,
        tags=[],
        definition_en=definition_en,
        definition_ar=definition_ar,
        source_references=[],
    )
    db.add(term)
    db.flush()
    return term


@pytest.fixture(autouse=True)
def _cleanup(db):
    yield
    db.rollback()


# ─── Canonical uniqueness ────────────────────────────────────────────────


def test_slug_is_unique(db):
    slug = _slug("dup")
    make_term(db, slug=slug)
    db.commit()
    with pytest.raises(Exception):
        make_term(db, slug=slug)
        db.commit()
    db.rollback()


def test_aliases_do_not_create_a_second_row(db, client):
    slug = _slug("rag")
    make_term(
        db, slug=slug, term_en="Retrieval-Augmented Generation", term_ar="التوليد المعزز",
        aliases=["RAG", "retrieval augmented generation"],
    )
    db.commit()

    resp = client.get("/api/v1/vocabulary/", params={"search": "RAG"})
    assert resp.status_code == 200
    matches = [t for t in resp.json()["items"] if t["slug"] == slug]
    assert len(matches) == 1, "one alias hit must resolve to exactly one canonical term"


# ─── Search / filters ────────────────────────────────────────────────────


def test_english_search(db, client):
    slug = _slug("transformer")
    make_term(db, slug=slug, term_en="Transformer Architecture", term_ar="بنية المحول")
    db.commit()
    resp = client.get("/api/v1/vocabulary/", params={"search": "Transformer Architecture"})
    assert any(t["slug"] == slug for t in resp.json()["items"])


def test_arabic_search(db, client):
    slug = _slug("attn")
    make_term(db, slug=slug, term_en="Attention Mechanism", term_ar="آلية الانتباه الفريدة")
    db.commit()
    resp = client.get("/api/v1/vocabulary/", params={"search": "الانتباه الفريدة"})
    assert any(t["slug"] == slug for t in resp.json()["items"])


def test_category_filter(db, client):
    slug = _slug("catf")
    make_term(db, slug=slug, term_en="Unique Category Term", category="voice-ai-test")
    db.commit()
    resp = client.get("/api/v1/vocabulary/", params={"category": "voice-ai-test"})
    items = resp.json()["items"]
    assert all(t["category"] == "voice-ai-test" for t in items)
    assert any(t["slug"] == slug for t in items)


def test_difficulty_filter(db, client):
    slug = _slug("diff")
    make_term(db, slug=slug, term_en="Very Advanced Unique Term", difficulty="advanced")
    db.commit()
    resp = client.get("/api/v1/vocabulary/", params={"difficulty": "advanced", "search": "Very Advanced Unique"})
    items = resp.json()["items"]
    assert all(t["difficulty"] == "advanced" for t in items)
    assert any(t["slug"] == slug for t in items)


def test_course_filter(db, client):
    slug = _slug("courseterm")
    term = make_term(db, slug=slug, term_en="Course Filter Unique Term")
    course_key = f"COURSE-{uuid.uuid4().hex[:4]}"
    db.add(VocabularyTermAssociation(term_id=term.id, course_key=course_key, module_key=None, lesson_key=None))
    db.commit()

    resp = client.get("/api/v1/vocabulary/", params={"course_id": course_key})
    items = resp.json()["items"]
    assert len(items) == 1
    assert items[0]["slug"] == slug


def test_pagination(db, client):
    prefix = uuid.uuid4().hex[:6]
    for i in range(5):
        make_term(db, slug=_slug(f"page{prefix}{i}"), term_en=f"Pagination Term {prefix} {i}")
    db.commit()

    page1 = client.get("/api/v1/vocabulary/", params={"search": f"Pagination Term {prefix}", "page": 1, "page_size": 2}).json()
    page2 = client.get("/api/v1/vocabulary/", params={"search": f"Pagination Term {prefix}", "page": 2, "page_size": 2}).json()
    assert len(page1["items"]) == 2
    assert len(page2["items"]) == 2
    assert {t["slug"] for t in page1["items"]}.isdisjoint({t["slug"] for t in page2["items"]})


# ─── Detail lookup ───────────────────────────────────────────────────────


def test_detail_includes_related_terms_and_course_mappings(db, client):
    a = make_term(db, slug=_slug("a"), term_en="Term A")
    b = make_term(db, slug=_slug("b"), term_en="Term B")
    db.add(VocabularyTermRelation(term_id=a.id, related_term_id=b.id))
    course_key = f"COURSE-{uuid.uuid4().hex[:4]}"
    db.add(VocabularyTermAssociation(term_id=a.id, course_key=course_key, module_key=None, lesson_key=None))
    db.commit()

    resp = client.get(f"/api/v1/vocabulary/{a.slug}")
    assert resp.status_code == 200
    body = resp.json()
    assert body["related_terms"][0]["slug"] == b.slug
    assert body["courses"][0]["course_key"] == course_key


def test_detail_404_for_unknown_slug(client):
    resp = client.get("/api/v1/vocabulary/does-not-exist")
    assert resp.status_code == 404


# ─── Progress ────────────────────────────────────────────────────────────


def test_progress_defaults_to_new(db, client):
    term = make_term(db, slug=_slug("newstate"))
    db.commit()
    resp = client.get(f"/api/v1/vocabulary/{term.slug}")
    assert resp.json()["progress"]["status"] == "new"


def test_progress_is_upgrade_only(db, client):
    term = make_term(db, slug=_slug("upgrade"))
    db.commit()
    token, user_id = _register(client)
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.post(f"/api/v1/vocabulary/{term.slug}/progress", json={"status": "mastered"}, headers=headers)
    assert resp.status_code == 200
    assert resp.json()["progress"]["status"] == "mastered"

    # A later "learning" write must not demote an already-mastered term.
    resp = client.post(f"/api/v1/vocabulary/{term.slug}/progress", json={"status": "learning"}, headers=headers)
    assert resp.json()["progress"]["status"] == "mastered"

    row = (
        db.query(UserTermProgress)
        .filter(UserTermProgress.user_id == user_id, UserTermProgress.vocabulary_term_id == term.id)
        .first()
    )
    assert row is not None
    assert row.status == TermStatus.learned
    assert row.term_id == term.slug


def test_learning_status_filter(db, client):
    term = make_term(db, slug=_slug("statusfilter"), term_en="Status Filter Unique Term")
    db.commit()
    token, _user_id = _register(client)
    headers = {"Authorization": f"Bearer {token}"}
    client.post(f"/api/v1/vocabulary/{term.slug}/progress", json={"status": "mastered"}, headers=headers)

    mastered = client.get("/api/v1/vocabulary/", params={"status": "mastered", "search": "Status Filter Unique"}, headers=headers).json()
    assert any(t["slug"] == term.slug for t in mastered["items"])

    new_only = client.get("/api/v1/vocabulary/", params={"status": "new", "search": "Status Filter Unique"}, headers=headers).json()
    assert not any(t["slug"] == term.slug for t in new_only["items"])


def test_course_counts_endpoint(db, client):
    term = make_term(db, slug=_slug("countterm"))
    course_key = f"COURSE-{uuid.uuid4().hex[:4]}"
    db.add(VocabularyTermAssociation(term_id=term.id, course_key=course_key, module_key=None, lesson_key=None))
    db.commit()

    resp = client.get("/api/v1/vocabulary/courses")
    assert resp.status_code == 200
    counts = {c["course_key"]: c["term_count"] for c in resp.json()["courses"]}
    assert counts[course_key] == 1


def test_category_counts_are_included_in_the_categories_endpoint(db, client):
    """"Browse by Category" needs a real per-category count, not just the
    list of category names — one grouped query (list_category_counts), not a
    Python-side scan of every term."""
    category = f"Cat-{uuid.uuid4().hex[:8]}"
    make_term(db, slug=_slug("cat1"), category=category)
    make_term(db, slug=_slug("cat2"), category=category)
    db.commit()

    resp = client.get("/api/v1/vocabulary/categories")
    assert resp.status_code == 200
    body = resp.json()
    assert category in body["categories"]
    counts = {c["category"]: c["term_count"] for c in body["counts"]}
    assert counts[category] == 2


# ─── Seed idempotency ────────────────────────────────────────────────────


def test_seed_upsert_is_idempotent(db):
    from seeds.seed_vocabulary import upsert_authored_terms
    from app.content.vocabulary_seed_terms import TERMS as CURATED_TERMS

    before = db.query(VocabularyTerm).count()
    upsert_authored_terms(db, CURATED_TERMS, "app/content/vocabulary_seed_terms.py")
    db.commit()
    after_first = db.query(VocabularyTerm).count()
    upsert_authored_terms(db, CURATED_TERMS, "app/content/vocabulary_seed_terms.py")
    db.commit()
    after_second = db.query(VocabularyTerm).count()

    assert after_first == after_second
    assert after_first >= before
