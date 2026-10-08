"""
backend/seeds/seed_vocabulary.py

Seeds the AI Vocabulary dictionary (migration 022):

1. Migrates the 65 legacy terms from `app/content/ai_terms.json` into
   `vocabulary_terms` (one canonical row per term — that file already has no
   duplicates, per the terminology audit).
2. Adds the curated terms in `app/content/vocabulary_seed_terms.py` and
   `vocabulary_seed_terms_expansion.py` — concepts the legacy dictionary never
   covered, hand-selected from the real curriculum (lesson `concepts` fields
   and, for the six courses without one, real lesson titles/bodies) rather
   than a bulk dump of every extracted candidate string.
3. Creates `related` edges (`VocabularyTermRelation`) between curated terms.
4. Derives course/module/lesson associations by loading the real curriculum
   (the same per-course loader the importer and validator use) and
   word-boundary text-matching each term's surface forms (English/acronym
   forms require a word boundary; surfaces under 3 characters are never
   matched, so short ambiguous tokens like "AI"/"CI" cannot fire) against
   each lesson's actual title, description and content. A term is only ever
   associated with a lesson it is genuinely mentioned in. A course that ships
   as an outline only (no lesson bodies) would get course+module-level
   associations with `lesson_key=None`, never a fabricated lesson id; no
   current course does (COURSE-006 now has lesson bodies).
5. Sets each term's `first_course_key`/`first_lesson_key` to the mention with
   the strongest evidence tier (named in the lesson's title > in its
   objective/description > repeated in the body > a single incidental
   mention), tie-broken by earliest course/module/lesson order. Module-level
   (outline-only) mentions are never chosen here, since there is no real
   lesson to link to.
6. Backfills `UserTermProgress.vocabulary_term_id` for any existing progress
   row whose `term_id` matches a seeded slug.

Idempotent: every step is an upsert (query by unique key, update if found,
insert if not) or an existence check before insert. Run it twice and every
table's row count is unchanged the second time.

    python seed.py                      (base schema/content, if not already done)
    python seeds/seed_vocabulary.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from typing import Dict, List, Tuple

import app.main  # noqa: F401  (imports every router/model module, resolving all relationship() string refs)

from app.db.schema_guard import require_migrated_schema
from app.db.session import SessionLocal

from app.content.terminology import TERMS as LEGACY_TERMS
from app.content.vocabulary_seed_terms import TERMS as CURATED_TERMS
from app.content.vocabulary_seed_terms_expansion import TERMS as EXPANSION_TERMS
from app.content.vocabulary_legacy_enrichment import ENRICHMENT as LEGACY_ENRICHMENT
from app.models.vocabulary import UserTermProgress
from app.models.vocabulary_term import (
    VocabularyTerm,
    VocabularyTermAssociation,
    VocabularyTermRelation,
)
from app.services.curriculum.loaders import course_dirs, load_course_dir, load_py, course_id_of
from app.services.curriculum.spec import CurriculumError

# Vocabulary is seeded only against courses that have actually shipped to
# learners. `course_dirs()` scans the filesystem generically, so a course
# folder that another in-progress process drops under backend/courses/ ahead
# of its own launch would otherwise get real term associations before the
# course itself is live ("used in COURSE-0xx" copy for a course nobody can
# open yet). Keep this in lockstep with the curriculum's actual launched set
# (COURSE-001..018, the 18 canonical courses in seeds/curriculum.py) rather
# than "whatever is on disk right now". COURSE-016 was added once it became a
# canonical production course (2026-10-03); COURSE-017 and 018 on 2026-10-07.
_LAUNCHED_COURSES = {f"COURSE-{i:03d}" for i in range(1, 19)}


def _launched_course_dirs():
    return [d for d in course_dirs() if course_id_of(d) in _LAUNCHED_COURSES]

# Evidence tiers for "which mention is most instructionally prominent" (used
# only to pick a term's `first_introduced` lesson, never to decide whether an
# association exists at all — every real match still gets an association row).
_TIER_TITLE = 3       # the term is named in the lesson's own title
_TIER_DESCRIPTION = 2  # the term appears in the lesson's stated objective/description
_TIER_REPEATED_BODY = 1  # the term is mentioned more than once in the lesson body
_TIER_INCIDENTAL = 0   # a single, unremarkable body mention


def _word_pattern(surface: str) -> "re.Pattern":
    # Case-insensitive whole-phrase match; \b fails on some Arabic joins, so
    # English/acronym surfaces use \b and Arabic surfaces just check containment.
    #
    # A trailing optional "s" is allowed on Latin surfaces so a plain-English
    # plural ("Vision Transformers", "Random Forests") still counts as a real
    # title/body match for the singular canonical surface ("Vision
    # Transformer") — found via the first-introduced audit: COURSE-008's own
    # lesson titled "From Language Transformers to Vision Transformers" was
    # being *missed* by its own dedicated title (the bare \b boundary sits
    # inside "Transformers", right before the trailing "s", so it never
    # matched), which let an incidental concept-list mention in an unrelated
    # earlier course win first_introduced by a tie-break instead. `\b` still
    # anchors both ends, so this does not loosen the match into the middle of
    # an unrelated word — only a genuine plural of the exact surface.
    escaped = re.escape(surface.strip())
    if re.search(r"[A-Za-z0-9]", surface):
        return re.compile(rf"\b{escaped}s?\b", re.IGNORECASE)
    return re.compile(escaped)


# Surfaces under 3 characters are dropped as too noisy to text-match — except
# these, individually reviewed and safe in an AI/ML curriculum corpus ("F1"
# collides with nothing here; "F1 Score"/"f-measure" alone never appear
# verbatim in the real lessons, only bare "F1" does).
_SHORT_SURFACE_ALLOWLIST = {"f1", "r²"}


def _surfaces(term_en: str, acronym: str | None, aliases: List[str], *, slug: str = "") -> List[str]:
    bare_ok = slug not in _AMBIGUOUS_BARE_TERMS
    forms = ([term_en] if bare_ok else []) + ([acronym] if acronym else []) + list(aliases or [])
    return [
        f for f in {s.strip() for s in forms if s}
        if len(f) >= 3 or f.lower() in _SHORT_SURFACE_ALLOWLIST
    ]


# Aliases from the legacy dictionary (authored for display, not for text
# matching) that turned out too broad or ambiguous once used to scan real
# lesson text — found by auditing the highest-association-count terms.
# Removed here, at seed time, rather than editing the frontend-authored
# ai_terms.json source: "workflow" false-matches any ML/data pipeline
# ("...scikit-learn estimators for distinct parts of a workflow" - nothing to
# do with agent orchestration); "eval" collides with PyTorch's train/eval
# mode; "ci/cd" duplicates the dedicated CI/CD term instead of being a true
# alias of Deployment. "splitter" (bare) collides with cross-validation
# splitters (KFold/StratifiedKFold/"choose a splitter for an imbalanced
# dataset") in COURSE-001 — found by the first-introduced audit: with the
# plural-tolerant word pattern below, "Splitters" in that unrelated lesson's
# own title outranked chunking's real, dedicated COURSE-005 lesson and won
# first_introduced. "text splitting" (the two-word alias) stays; it is not
# ambiguous the same way.
_NOISY_LEGACY_ALIASES: Dict[str, set] = {
    "orchestration": {"workflow"},
    "evaluation": {"eval"},
    "deployment": {"ci/cd"},
    "chunking": {"splitter"},
}

# Terms whose bare English name collides with an unrelated, very common
# technical sense elsewhere in the curriculum (e.g. "Memory" the agent/chat
# concept vs. "GPU memory" / "memory budget" everywhere in systems content —
# audited by sampling real lesson matches, see the association-quality
# report). For these, only the term's more specific aliases are used as
# match surfaces; the bare name is still shown to users everywhere, just
# never scanned for on its own in lesson titles/bodies.
_AMBIGUOUS_BARE_TERMS = {"memory"}

# Difficulty/category corrections to the legacy dictionary, found in the
# quality audit: the frontend-authored `level` field tracked how advanced the
# *feature* using the concept was, not how hard the concept itself is to
# grasp. These six are conceptually intermediate ("combine two things",
# "wait for human approval") even though the legacy content marked them
# "advanced". `term_en`/`term_ar`/definitions are untouched.
_LEGACY_DIFFICULTY_OVERRIDES: Dict[str, str] = {
    "guardrails": "intermediate",
    "human_in_the_loop": "beginner",
    "orchestration": "intermediate",
    "knowledge_graph": "intermediate",
    "query_expansion": "intermediate",
    "hybrid_search": "intermediate",
    "model_serving": "intermediate",
}

# "Engineering" was ambiguous next to "Systems"/"MLOps"/"Serving" (all also
# engineering-flavored) — renamed to say what actually distinguishes it:
# general software-engineering concepts, not AI-specific ones.
_LEGACY_CATEGORY_RENAMES: Dict[str, str] = {"Engineering": "Software Engineering"}


def upsert_legacy_terms(db) -> Dict[str, VocabularyTerm]:
    by_slug: Dict[str, VocabularyTerm] = {}
    for term_id, entry in LEGACY_TERMS.items():
        row = db.query(VocabularyTerm).filter(VocabularyTerm.slug == term_id).first()
        if row is None:
            row = VocabularyTerm(slug=term_id)
            db.add(row)
        row.term_en = entry["en"]
        row.term_ar = entry["ar"]
        row.acronym = entry.get("abbreviation") or None
        noisy = _NOISY_LEGACY_ALIASES.get(term_id, set())
        row.aliases = [a for a in (entry.get("aliases") or []) if a.lower() not in noisy]
        category = entry.get("category")
        row.category = _LEGACY_CATEGORY_RENAMES.get(category, category)
        row.difficulty = _LEGACY_DIFFICULTY_OVERRIDES.get(term_id, entry.get("level") or "intermediate")
        row.tags = row.tags or []
        row.definition_en = entry.get("definitionEn") or ""
        row.definition_ar = entry.get("definitionAr") or ""
        row.example_ar = entry.get("exampleAr")
        row.source_references = ["app/content/ai_terms.json"]
        # Enrichment only ever fills a field the legacy dictionary left empty
        # — term_en/term_ar/definition_ar/aliases above are untouched, they
        # were already good.
        enrichment = LEGACY_ENRICHMENT.get(term_id)
        if enrichment:
            row.explanation_simple_ar = row.explanation_simple_ar or enrichment.get("explanation_simple_ar")
            row.why_it_matters_ar = row.why_it_matters_ar or enrichment.get("why_it_matters_ar")
            row.example_ar = row.example_ar or enrichment.get("example_ar")
        by_slug[term_id] = row
    db.flush()
    return by_slug


def upsert_authored_terms(db, terms: List[dict], source_file: str) -> Dict[str, VocabularyTerm]:
    """Upsert a list of hand-authored term dicts (the shape used by both
    `vocabulary_seed_terms.py` and `vocabulary_seed_terms_expansion.py`)."""
    by_slug: Dict[str, VocabularyTerm] = {}
    for entry in terms:
        slug = entry["slug"]
        row = db.query(VocabularyTerm).filter(VocabularyTerm.slug == slug).first()
        if row is None:
            row = VocabularyTerm(slug=slug)
            db.add(row)
        row.term_en = entry["term_en"]
        row.term_ar = entry["term_ar"]
        row.acronym = entry.get("acronym")
        row.aliases = entry.get("aliases") or []
        row.category = entry.get("category")
        row.difficulty = entry.get("difficulty") or "intermediate"
        row.tags = entry.get("tags") or []
        row.definition_en = entry["definition_en"]
        row.definition_ar = entry["definition_ar"]
        row.explanation_simple_ar = entry.get("explanation_simple_ar")
        row.why_it_matters_ar = entry.get("why_it_matters_ar")
        row.example_ar = entry.get("example_ar")
        row.source_references = [source_file]
        by_slug[slug] = row
    db.flush()
    return by_slug


# The legacy dictionary has no `related` field of its own; these fill the
# gap for the legacy terms that anchor an otherwise one-directional cluster
# (e.g. Reranking/RAG already point at Chunking — this makes viewing Chunking
# itself show the same cluster back).
_LEGACY_RELATIONS: Dict[str, List[str]] = {
    "chunking": ["retrieval", "reranking"],
}


def upsert_relations(db, all_by_slug: Dict[str, VocabularyTerm], *term_lists: List[dict]) -> int:
    created = 0
    entries = [e for lst in term_lists for e in lst]
    entries += [{"slug": slug, "related": related} for slug, related in _LEGACY_RELATIONS.items()]
    for entry in entries:
        term = all_by_slug.get(entry["slug"])
        if term is None:
            continue
        for related_slug in entry.get("related", []):
            related = all_by_slug.get(related_slug)
            if related is None or related.id == term.id:
                continue
            exists = (
                db.query(VocabularyTermRelation)
                .filter(
                    VocabularyTermRelation.term_id == term.id,
                    VocabularyTermRelation.related_term_id == related.id,
                )
                .first()
            )
            if exists is None:
                db.add(VocabularyTermRelation(term_id=term.id, related_term_id=related.id))
                created += 1
    db.flush()
    return created


def _lesson_tier(pattern: "re.Pattern", lesson) -> int:
    """How prominently a term's surface form appears in one lesson. Title beats
    the lesson's own stated objective/description, which beats being mentioned
    more than once in the body, which beats a single incidental mention —
    real signals only (no fabricated 'concepts' field)."""
    if pattern.search(lesson.title or ""):
        return _TIER_TITLE
    if pattern.search(lesson.description or ""):
        return _TIER_DESCRIPTION
    count = len(pattern.findall(lesson.content or ""))
    if count >= 2:
        return _TIER_REPEATED_BODY
    return _TIER_INCIDENTAL


def _ensure_association(db, term_id: int, course_key: str, module_key, lesson_key, created_counter: List[int]) -> None:
    exists = (
        db.query(VocabularyTermAssociation)
        .filter(
            VocabularyTermAssociation.term_id == term_id,
            VocabularyTermAssociation.course_key == course_key,
            VocabularyTermAssociation.module_key == module_key,
            VocabularyTermAssociation.lesson_key == lesson_key,
        )
        .first()
    )
    if exists is None:
        db.add(VocabularyTermAssociation(term_id=term_id, course_key=course_key, module_key=module_key, lesson_key=lesson_key))
        created_counter[0] += 1


def _course_006_module_texts(root) -> Dict[str, Tuple[str, str]]:
    """Module-level text for an outline-only course layout (`m006_*` module
    directories). COURSE-006 used to ship that way; it now has full lesson bodies,
    is handled by the ordinary lesson-level pass above, and has no `m006_*`
    directories, so this returns nothing for it. Kept for a course that again
    ships as an outline: only a title, learning objectives, an
    outline of bullet points, a practice prompt and a quiz per lesson. That is
    real, genuine text; it is scanned here (module id -> (module title,
    combined outline text)) so COURSE-006 can still get honest COURSE/MODULE
    level associations without ever inventing a lesson body or a lesson id."""
    result: Dict[str, Tuple[str, str]] = {}
    for module_dir in sorted(p for p in root.iterdir() if p.is_dir() and p.name.startswith("m006_")):
        manifest_file = module_dir / "module_manifest.py"
        if not manifest_file.is_file():
            continue
        module_meta = getattr(load_py(manifest_file), "MODULE", {})
        module_id = str(module_meta.get("module_id") or "")
        module_title = str(module_meta.get("title") or "")
        if not module_id:
            continue
        chunks = [module_title]
        for lesson_file in sorted(module_dir.glob("l006_*.py")):
            lesson = getattr(load_py(lesson_file), "LESSON", {})
            chunks.append(str(lesson.get("title") or ""))
            chunks.append(" ".join(str(o) for o in (lesson.get("learning_objectives") or [])))
            chunks.append(" ".join(str(b.get("text", "")) for b in (lesson.get("content_outline") or [])))
            practice = lesson.get("practice") or {}
            chunks.append(str(practice.get("instructions") or ""))
            chunks.append(" ".join(str(a) for a in (practice.get("acceptance_criteria") or [])))
            for q in lesson.get("quiz") or []:
                chunks.append(str(q.get("question", "")) + " " + str(q.get("explanation", "")))
        result[module_id] = (module_title, "\n".join(chunks))
    return result


def derive_associations(db, all_by_slug: Dict[str, VocabularyTerm]) -> Tuple[int, Dict[str, set]]:
    """Text-match every term's surface forms against every real lesson (and,
    for the one outline-only course, against its real outline text at module
    granularity). Returns (associations created, {course_id: set(lesson_ids
    or 'module:<id>' touched)})."""
    patterns_by_term: Dict[int, List["re.Pattern"]] = {}
    for term in all_by_slug.values():
        patterns_by_term[term.id] = [_word_pattern(s) for s in _surfaces(term.term_en, term.acronym, term.aliases, slug=term.slug)]

    created = [0]
    coverage: Dict[str, set] = {}
    # term_id -> (best_tier, course_id, module_id, lesson_id) seen so far
    best: Dict[int, Tuple[int, str, str, str]] = {}

    courses = []
    load_errors: List[str] = []
    for course_dir in _launched_course_dirs():
        try:
            courses.append(load_course_dir(course_dir))
        except CurriculumError as exc:
            # A folder-layout gap in the curriculum loader itself (pre-existing,
            # not something this seed can fix) — skip that course rather than
            # aborting every course's association derivation.
            load_errors.append(f"{course_dir.name}: {exc}")
    if load_errors:
        print("Courses skipped (loader could not parse them):")
        for line in load_errors:
            print(f"  {line}")

    for course in sorted(courses, key=lambda c: c.course_id):
        for module in course.modules:
            for lesson in module.lessons:
                for term_id, patterns in patterns_by_term.items():
                    tier = max((_lesson_tier(p, lesson) for p in patterns if p.search(f"{lesson.title}\n{lesson.content}")), default=None)
                    if tier is None:
                        continue
                    coverage.setdefault(course.course_id, set()).add(lesson.lesson_id)
                    current = best.get(term_id)
                    candidate = (tier, course.course_id, module.module_id, lesson.lesson_id)
                    if current is None or tier > current[0]:
                        best[term_id] = candidate
                    _ensure_association(db, term_id, course.course_id, module.module_id, lesson.lesson_id, created)

    # COURSE-006: outline-only, real text at module granularity, never a
    # fabricated lesson id (see `_course_006_module_texts`).
    course_006_dir = next((d for d in _launched_course_dirs() if course_id_of(d) == "COURSE-006"), None)
    if course_006_dir is not None:
        for module_id, (_title, text) in _course_006_module_texts(course_006_dir).items():
            for term_id, patterns in patterns_by_term.items():
                if not any(p.search(text) for p in patterns):
                    continue
                coverage.setdefault("COURSE-006", set()).add(f"module:{module_id}")
                _ensure_association(db, term_id, "COURSE-006", module_id, None, created)
                # Module-level (no lesson body exists to point to) is never
                # promoted to `first_introduced` — that field only ever names
                # a real, openable lesson.
    db.flush()

    for term in all_by_slug.values():
        seen = best.get(term.id)
        if seen and not term.first_course_key:
            _tier, term.first_course_key, _module_id, term.first_lesson_key = seen
    db.flush()
    return created[0], coverage


def backfill_progress(db, all_by_slug: Dict[str, VocabularyTerm]) -> int:
    updated = 0
    rows = (
        db.query(UserTermProgress)
        .filter(UserTermProgress.vocabulary_term_id.is_(None))
        .all()
    )
    for row in rows:
        term = all_by_slug.get(row.term_id)
        if term is not None:
            row.vocabulary_term_id = term.id
            updated += 1
    db.flush()
    return updated


def run(db) -> None:
    legacy = upsert_legacy_terms(db)
    curated = upsert_authored_terms(db, CURATED_TERMS, "app/content/vocabulary_seed_terms.py")
    expansion = upsert_authored_terms(db, EXPANSION_TERMS, "app/content/vocabulary_seed_terms_expansion.py")
    all_by_slug = {**legacy, **curated, **expansion}
    print(
        f"Terms: {len(legacy)} legacy + {len(curated)} curated + {len(expansion)} expansion "
        f"= {len(all_by_slug)} total canonical rows"
    )

    relations_created = upsert_relations(db, all_by_slug, CURATED_TERMS, EXPANSION_TERMS)
    print(f"Relations created: {relations_created}")

    associations_created, coverage = derive_associations(db, all_by_slug)
    print(f"Associations created: {associations_created}")
    for course_id in sorted(coverage):
        print(f"  {course_id}: {len(coverage[course_id])} lessons with >=1 term match")

    progress_backfilled = backfill_progress(db, all_by_slug)
    print(f"UserTermProgress rows backfilled: {progress_backfilled}")

    db.commit()
    print("Done.")


if __name__ == "__main__":
    require_migrated_schema()
    db = SessionLocal()
    try:
        run(db)
    except Exception as exc:
        db.rollback()
        print(f"\nFailed: {exc}")
        raise
    finally:
        db.close()
