"""
Covers the Arabic-first terminology layer:

  * the dictionary itself, and that the backend's generated copy has not
    drifted from the frontend source it is generated from;
  * query normalization — the thing that makes an Arabic search and an
    English search reach the same course instead of two duplicate ones;
  * the content lint that warns an author who translated a term away;
  * the vocabulary-progress API;
  * bilingual search;
  * that the Arabic quiz blob is stripped of its answer key exactly like the
    English one.
"""
import re
import uuid
from pathlib import Path

import pytest

from app.content import terminology as T
from app.db.session import SessionLocal
from app.models.learning import DifficultyLevel
from app.models.tool_course import ToolCourse
from app.services.content.terminology_lint import lint_content
from app.services.language.language_policy import build_policy


def _register(client) -> str:
    email = f"term-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Term Test", "password": "correcthorsebatterystaple",
    })
    assert resp.status_code == 201
    return resp.json()["access_token"]


# ─── The dictionary ──────────────────────────────────────────────────────


def test_dictionary_entries_are_well_formed():
    assert len(T.TERMS) > 20
    for term_id, term in T.TERMS.items():
        assert term["id"] == term_id, "a term's id must match its key"
        for field in ("en", "ar", "preferred", "category", "level", "definitionAr", "definitionEn"):
            assert term.get(field), f"{term_id} is missing {field}"
        # The whole policy rests on `preferred` being the English industry
        # form. An Arabic `preferred` would mean the platform teaches the
        # term in a way no job description uses.
        assert not any("؀" <= ch <= "ۿ" for ch in term["preferred"]), (
            f"{term_id}: preferred must be the English industry term"
        )


_FRONTEND_SOURCE = (
    Path(__file__).resolve().parents[2] / "frontend" / "src" / "content" / "terminology" / "ai-terms.ts"
)


@pytest.mark.skipif(
    not _FRONTEND_SOURCE.exists(),
    reason="frontend source not present (running inside the api container)",
)
def test_generated_dictionary_matches_frontend_source():
    """`npm run terminology:export` was run after the dictionary changed.

    Without this, adding a term in the frontend silently leaves search, the
    tutor's prompt and the linter working from a stale copy.
    """
    source = _FRONTEND_SOURCE.read_text(encoding="utf-8")
    body = source.split("export const AI_TERMS", 1)[1]
    authored = set(re.findall(r"^  ([a-z][a-z0-9_]*): \{$", body, re.MULTILINE))

    assert authored, "could not parse term ids out of ai-terms.ts"
    assert authored == set(T.TERMS), (
        "backend/app/content/ai_terms.json is out of date — "
        "run `npm run terminology:export` in frontend/ and commit the result"
    )


# ─── Normalization and lookup ────────────────────────────────────────────


@pytest.mark.parametrize(
    "query,expected_preferred",
    [
        ("Embeddings", "Embeddings"),
        ("embedding", "Embeddings"),
        ("التضمينات", "Embeddings"),
        ("تمثيل النصوص", "Embeddings"),
        ("RAG", "RAG"),
        ("الـ RAG", "RAG"),  # Arabic article glued onto an English term
        ("Retrieval Augmented Generation", "RAG"),
        ("التوليد المعزز بالاسترجاع", "RAG"),
        ("قاعدة بيانات المتجهات", "Vector Database"),
        ("vector db", "Vector Database"),
        ("إعادة الترتيب", "Reranking"),
    ],
)
def test_find_term_resolves_either_language(query, expected_preferred):
    term = T.find_term(query)
    assert term is not None, f"{query!r} did not resolve"
    assert term["preferred"] == expected_preferred


def test_expand_query_bridges_the_two_languages():
    """The property the whole search design rests on: an Arabic query and its
    English equivalent expand to the same set, so one course serves both."""
    assert T.expand_query("التضمينات") == T.expand_query("Embeddings")
    assert T.normalize_term("embeddings") in T.expand_query("التضمينات")


def test_normalization_folds_arabic_orthography():
    # ة/ه and ى/ي and the definite article are all reader-typed variation,
    # not different words.
    assert T.normalize_term("قاعدة") == T.normalize_term("قاعده")
    assert T.normalize_term("الاسترجاع") == T.normalize_term("استرجاع")


def test_unknown_query_still_normalizes():
    assert T.find_term("qwertyuiop") is None
    assert T.expand_query("qwertyuiop") == {"qwertyuiop"}


# ─── Content lint ────────────────────────────────────────────────────────


def test_lint_warns_when_the_english_term_is_translated_away():
    text = "التضمينات هي طريقة لتحويل النصوص، ثم نستخدم إعادة الترتيب لتحسين النتائج."
    result = lint_content(text)
    flagged = {w["term_id"] for w in result["warnings"]}
    assert {"embeddings", "reranking"} <= flagged
    suggestions = {w["suggestion"] for w in result["warnings"]}
    assert "Reranking (إعادة الترتيب)" in suggestions


def test_lint_accepts_the_first_mention_form():
    text = (
        "Embeddings (التضمينات) هي تمثيلات رقمية للنصوص في صورة vectors، "
        "ثم نستخدم Reranking (إعادة الترتيب) لتحسين ترتيب النتائج."
    )
    result = lint_content(text)
    assert result["warnings"] == []
    assert "embeddings" in result["terms_used"]
    assert "reranking" in result["terms_used"]


# ─── AI language policy ──────────────────────────────────────────────────


def test_language_policy_forbids_translating_code_in_every_mode():
    for mode in ("arabic_first", "industry", "english_technical"):
        policy = build_policy("ar", mode)
        assert "NEVER translate code" in policy
        assert "LangChain" in policy  # technology names listed verbatim


def test_language_policy_falls_back_instead_of_raising():
    """A bad client value must not fail a request the student paid for."""
    assert build_policy("klingon", "nonsense") == build_policy("ar", "arabic_first")


# ─── Vocabulary progress API ─────────────────────────────────────────────


def test_dictionary_endpoint_is_public(client):
    resp = client.get("/api/v1/terminology/")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["terms"]) == len(T.TERMS)
    assert "LangChain" in body["tech_names"]


def test_vocabulary_progress_requires_auth(client):
    assert client.get("/api/v1/terminology/progress").status_code in (401, 403)


def test_vocabulary_progress_records_and_upgrades(client):
    headers = {"Authorization": f"Bearer {_register(client)}"}

    empty = client.get("/api/v1/terminology/progress", headers=headers).json()
    assert empty["encountered"] == [] and empty["learned"] == []
    assert empty["total_terms"] == len(T.TERMS)

    seen = client.post(
        "/api/v1/terminology/progress",
        json={"term_ids": ["embeddings", "reranking"], "status": "encountered"},
        headers=headers,
    )
    assert seen.status_code == 200
    assert set(seen.json()["encountered"]) == {"embeddings", "reranking"}
    assert seen.json()["learned"] == []

    learned = client.post(
        "/api/v1/terminology/progress",
        json={"term_ids": ["embeddings"], "status": "learned"},
        headers=headers,
    )
    assert learned.json()["learned"] == ["embeddings"]
    # Still one row per term, not a second one.
    assert sorted(learned.json()["encountered"]) == ["embeddings", "reranking"]

    # Re-reading the lesson must not demote a term already proven.
    again = client.post(
        "/api/v1/terminology/progress",
        json={"term_ids": ["embeddings"], "status": "encountered"},
        headers=headers,
    )
    assert again.json()["learned"] == ["embeddings"]


def test_vocabulary_rejects_ids_outside_the_dictionary(client):
    """term_id is not a foreign key, so this validation is the only thing
    between the table and arbitrary client strings."""
    headers = {"Authorization": f"Bearer {_register(client)}"}
    resp = client.post(
        "/api/v1/terminology/progress",
        json={"term_ids": ["definitely-not-a-term"], "status": "encountered"},
        headers=headers,
    )
    assert resp.status_code == 400


def test_lint_endpoint_returns_warnings(client):
    headers = {"Authorization": f"Bearer {_register(client)}"}
    resp = client.post(
        "/api/v1/terminology/lint",
        json={"text": "نستخدم إعادة الترتيب لتحسين النتائج."},
        headers=headers,
    )
    assert resp.status_code == 200
    assert any(w["term_id"] == "reranking" for w in resp.json()["warnings"])


# ─── Bilingual search ────────────────────────────────────────────────────


def _make_arabic_course() -> str:
    slug = f"search-test-{uuid.uuid4().hex[:8]}"
    setup = SessionLocal()
    setup.add(
        ToolCourse(
            slug=slug,
            title="Vector Databases in Practice",
            title_ar="قواعد بيانات المتجهات عملياً",
            description="Store embeddings and run similarity search at scale.",
            description_ar=(
                "خزّن الـ Embeddings ونفّذ similarity search داخل Vector Database."
            ),
            category="Vector Databases",
            difficulty=DifficultyLevel.intermediate,
            estimated_hours=4.0,
            related_track_ids=[],
            technical_terms=["embeddings", "vector_database"],
            industry_skills=["Vector Search"],
            is_active=True,
        )
    )
    setup.commit()
    setup.close()
    return slug


def test_search_finds_the_same_course_in_either_language(client):
    slug = _make_arabic_course()

    def slugs(query):
        resp = client.get("/api/v1/search/", params={"q": query})
        assert resp.status_code == 200
        return {hit["href"] for hit in resp.json()["hits"]}

    # The point of the whole design: one course, reachable from either
    # language, rather than an Arabic duplicate of an English course.
    assert f"/tools/{slug}" in slugs("Embeddings")
    assert f"/tools/{slug}" in slugs("التضمينات")
    assert f"/tools/{slug}" in slugs("قاعدة بيانات المتجهات")


def test_search_reports_the_term_it_matched(client):
    _make_arabic_course()
    body = client.get("/api/v1/search/", params={"q": "التضمينات"}).json()
    assert [t["preferred"] for t in body["matched_terms"]] == ["Embeddings"]
    # The expansion is surfaced so the UI can show what else was searched.
    assert T.normalize_term("embeddings") in body["expanded"]


def test_search_rejects_a_one_character_query(client):
    assert client.get("/api/v1/search/", params={"q": "a"}).status_code == 422


# ─── Answer-key safety on the Arabic quiz blob ───────────────────────────


def test_arabic_questions_are_stripped_of_the_answer_key():
    """questions_ar carries the same answer key as questions, so adding it
    must not re-open the leak the English validator closed."""
    from app.views.learning import QuizResponse

    quiz = QuizResponse(
        id=1,
        title="Quiz",
        title_ar="اختبار",
        questions=[{"question": "Q?", "options": ["a", "b"], "correct": 1, "explanation": "because"}],
        questions_ar=[{"question": "س؟", "options": ["أ", "ب"], "correct": 1, "explanation": "لأن"}],
        passing_score=70,
    )
    assert "correct" not in quiz.questions[0]
    assert "explanation" not in quiz.questions[0]
    assert quiz.questions_ar is not None
    assert "correct" not in quiz.questions_ar[0]
    assert "explanation" not in quiz.questions_ar[0]
    assert quiz.questions_ar[0]["question"] == "س؟"


def test_quiz_without_arabic_version_reports_none():
    from app.views.learning import QuizResponse

    quiz = QuizResponse(
        id=1, title="Quiz",
        questions=[{"question": "Q?", "options": ["a"], "correct": 0}],
        passing_score=70,
    )
    assert quiz.questions_ar is None
    assert quiz.title_ar is None
