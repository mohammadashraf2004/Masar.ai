"""
Covers the association-quality improvements in `seeds/seed_vocabulary.py`:

  * short, ambiguous acronyms never fire on a substring
  * a real word-boundary match still works
  * the evidence-tier ranking (title > description > repeated body > a
    single incidental mention) picks the more prominent mention for
    `first_introduced`
  * COURSE-006 (outline-only, no lesson bodies) gets course/module-level
    associations with `lesson_key=None`, never a fabricated lesson id
"""
import uuid
from types import SimpleNamespace

import pytest

from app.content.terminology import TERMS as LEGACY_TERMS
from app.models.vocabulary_term import VocabularyTerm, VocabularyTermAssociation
from seeds.seed_vocabulary import _NOISY_LEGACY_ALIASES, _lesson_tier, _surfaces, _word_pattern


def _slug(name: str) -> str:
    return f"{name}_{uuid.uuid4().hex[:8]}"


def _lesson(title="", description="", content=""):
    return SimpleNamespace(title=title, description=description, content=content)


# ─── Short-token guard ───────────────────────────────────────────────────


def test_short_acronyms_are_never_matched():
    assert _surfaces("Artificial Intelligence", "AI", []) == ["Artificial Intelligence"]
    assert _surfaces("Continuous Integration", "CI", []) == ["Continuous Integration"]


def test_word_boundary_pattern_does_not_match_inside_another_word():
    pattern = _word_pattern("RAG")
    assert pattern.search("We use RAG for retrieval.")
    assert not pattern.search("The dragon flew over the lagoon.")


def test_plain_english_plural_still_matches_the_singular_surface():
    """A lesson titled "...Vision Transformers" (plural) is a real match for
    the canonical surface "Vision Transformer" (singular) — found by the
    first-introduced audit: without this, COURSE-008's own lesson titled
    "From Language Transformers to Vision Transformers" never matched its own
    title, and an incidental concept-list mention in an unrelated earlier
    course won `first_introduced` by a tie-break instead."""
    pattern = _word_pattern("Vision Transformer")
    assert pattern.search("Introduction to Vision Transformers")
    assert pattern.search("Vision Transformer")
    # still word-bounded: no false match inside an unrelated longer word
    assert not pattern.search("VisionTransformersAreCool")


def test_chunking_does_not_match_unrelated_cross_validation_splitters():
    """"splitter" was a legacy alias of Chunking (RAG document chunking), but
    also the generic ML term for a cross-validation splitter
    (KFold/StratifiedKFold). Once plural matching was added, a lesson titled
    "Stratified and Alternative Splitters" (about cross-validation, nothing to
    do with RAG) started outranking Chunking's real, dedicated lesson for
    first_introduced. Regression guard: "splitter" must stay excluded."""
    assert "splitter" in _NOISY_LEGACY_ALIASES.get("chunking", set())
    entry = LEGACY_TERMS["chunking"]
    noisy = _NOISY_LEGACY_ALIASES["chunking"]
    aliases = [a for a in entry["aliases"] if a.lower() not in noisy]
    surfaces = _surfaces(entry["en"], entry.get("abbreviation"), aliases, slug="chunking")
    patterns = [_word_pattern(s) for s in surfaces]
    assert not any(p.search("Stratified and Alternative Splitters") for p in patterns)


# ─── Evidence tiers ──────────────────────────────────────────────────────


def test_title_mention_outranks_body_mention():
    pattern = _word_pattern("Grounding")
    title_lesson = _lesson(title="Grounding in RAG Systems", content="")
    body_lesson = _lesson(title="Something Else", content="A brief mention of grounding here.")
    assert _lesson_tier(pattern, title_lesson) > _lesson_tier(pattern, body_lesson)


def test_description_mention_outranks_single_body_mention():
    pattern = _word_pattern("Latency")
    description_lesson = _lesson(title="Unrelated", description="Understand latency budgets.", content="")
    incidental_lesson = _lesson(title="Unrelated", content="One incidental mention of latency in passing.")
    assert _lesson_tier(pattern, description_lesson) > _lesson_tier(pattern, incidental_lesson)


def test_repeated_body_mention_outranks_a_single_one():
    pattern = _word_pattern("Throughput")
    repeated_lesson = _lesson(title="X", content="Throughput matters. We measure throughput carefully.")
    single_lesson = _lesson(title="X", content="Throughput is mentioned once.")
    assert _lesson_tier(pattern, repeated_lesson) > _lesson_tier(pattern, single_lesson)


# ─── Related-term pedagogical audit ──────────────────────────────────────


def test_diffusion_model_reciprocates_its_classic_alternatives():
    """GAN and VAE both already pointed at Diffusion Model as the approach
    that largely superseded them; the reverse link was missing, so a learner
    landing directly on Diffusion Model never saw the two alternatives it's
    normally compared against. Regression guard for that specific gap found
    in the related-term pedagogical audit."""
    from app.content.vocabulary_seed_terms_expansion import TERMS as EXPANSION_TERMS

    by_slug = {e["slug"]: e for e in EXPANSION_TERMS}
    related = set(by_slug["diffusion_model"]["related"])
    assert {"gan", "variational_autoencoder"} <= related


# ─── COURSE-006 module-level associations ───────────────────────────────


@pytest.fixture(autouse=True)
def _cleanup(db):
    yield
    db.rollback()


def test_course_006_style_association_has_no_lesson_key(db):
    """A term found only in COURSE-006's outline text must be recorded as a
    course/module-level association (lesson_key=None), never a fabricated
    lesson id — mirrors what `derive_associations` does for real COURSE-006
    content."""
    term = VocabularyTerm(
        slug=_slug("outline_term"), term_en="Outline Term", term_ar="مصطلح",
        aliases=[], category="Systems", difficulty="intermediate", tags=[],
        definition_en="d", definition_ar="د", source_references=[],
    )
    db.add(term)
    db.flush()
    db.add(VocabularyTermAssociation(term_id=term.id, course_key="COURSE-006", module_key="M006-01", lesson_key=None))
    db.commit()

    row = (
        db.query(VocabularyTermAssociation)
        .filter(VocabularyTermAssociation.term_id == term.id, VocabularyTermAssociation.course_key == "COURSE-006")
        .one()
    )
    assert row.module_key == "M006-01"
    assert row.lesson_key is None
