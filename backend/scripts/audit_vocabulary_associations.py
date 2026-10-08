"""
backend/scripts/audit_vocabulary_associations.py

Association-quality audit for the AI Vocabulary dictionary. Re-derives, for
every (term, lesson) match the seed would create, which evidence tier
produced it — without storing anything in the database. The seed's matching
is deterministic from the curriculum source, so this is recomputed on demand
rather than persisted as a column (the smallest maintainable option: no
migration, and the audit stays exactly in sync with whatever the seed
actually does, because it calls the *same* functions).

Usage:  python scripts/audit_vocabulary_associations.py [--top N]

Prints, per term (sorted by total association count, descending):
  association_count, courses touched, high/medium/low confidence split.

Confidence buckets (mirrors seeds/seed_vocabulary.py's evidence tiers):
  high   = title or objective/description exact match
  medium = the surface form repeated more than once in the lesson body
  low    = a single, incidental body mention
"""
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.main  # noqa: F401
from app.content.terminology import TERMS as LEGACY_TERMS
from app.content.vocabulary_seed_terms import TERMS as CURATED_TERMS
from app.content.vocabulary_seed_terms_expansion import TERMS as EXPANSION_TERMS
from app.services.curriculum.loaders import course_dirs, load_course_dir, course_id_of
from app.services.curriculum.spec import CurriculumError
from seeds.seed_vocabulary import (
    _NOISY_LEGACY_ALIASES, _TIER_DESCRIPTION, _TIER_INCIDENTAL,
    _TIER_REPEATED_BODY, _TIER_TITLE, _course_006_module_texts, _lesson_tier,
    _surfaces, _word_pattern,
)


def _all_term_specs():
    # Mirrors seeds/seed_vocabulary.py's upsert_legacy_terms exactly: aliases
    # that were found, by auditing the highest-association-count terms, to be
    # too broad once used to scan real lesson text ("workflow" for
    # orchestration, "eval" for evaluation, "ci/cd" for deployment) are
    # stripped from the DB row at seed time. Using the raw, unstripped
    # LEGACY_TERMS aliases here (as an earlier version of this script did)
    # silently re-introduces exactly that noise into the audit report without
    # it ever reaching the database — under-reporting the seed's real
    # precision instead of measuring it.
    for slug, entry in LEGACY_TERMS.items():
        noisy = _NOISY_LEGACY_ALIASES.get(slug, set())
        aliases = [a for a in (entry.get("aliases") or []) if a.lower() not in noisy]
        yield slug, entry["en"], entry.get("abbreviation"), aliases
    for entry in CURATED_TERMS + EXPANSION_TERMS:
        yield entry["slug"], entry["term_en"], entry.get("acronym"), entry.get("aliases") or []


def main(top: int) -> None:
    patterns_by_slug = {
        slug: [_word_pattern(s) for s in _surfaces(term_en, acronym, aliases, slug=slug)]
        for slug, term_en, acronym, aliases in _all_term_specs()
    }

    courses = []
    for d in course_dirs():
        try:
            courses.append(load_course_dir(d))
        except CurriculumError:
            continue

    tier_counts: dict = {slug: Counter() for slug in patterns_by_slug}
    courses_touched: dict = {slug: set() for slug in patterns_by_slug}

    for course in courses:
        for module in course.modules:
            for lesson in module.lessons:
                haystack = f"{lesson.title}\n{lesson.content}"
                for slug, patterns in patterns_by_slug.items():
                    matched = [p for p in patterns if p.search(haystack)]
                    if not matched:
                        continue
                    tier = max(_lesson_tier(p, lesson) for p in matched)
                    tier_counts[slug][tier] += 1
                    courses_touched[slug].add(course.course_id)

    # COURSE-006 (outline-only, no lesson bodies) additionally gets
    # course/module-level associations in the real seed, on top of whatever
    # the generic per-lesson loop above already found in its real
    # title/objective text — see derive_associations() and
    # _course_006_module_texts() in seeds/seed_vocabulary.py. Skipping this
    # pass (as an earlier version of this script did) under-counts the real
    # seed's association total for every term mentioned only in COURSE-006's
    # outline/practice/quiz text.
    course_006_dir = next((d for d in course_dirs() if course_id_of(d) == "COURSE-006"), None)
    if course_006_dir is not None:
        from types import SimpleNamespace
        for module_id, (module_title, text) in _course_006_module_texts(course_006_dir).items():
            body = text[len(module_title):] if text.startswith(module_title) else text
            pseudo_lesson = SimpleNamespace(title=module_title, description="", content=body)
            for slug, patterns in patterns_by_slug.items():
                matched = [p for p in patterns if p.search(text)]
                if not matched:
                    continue
                tier = max(_lesson_tier(p, pseudo_lesson) for p in matched)
                tier_counts[slug][tier] += 1
                courses_touched[slug].add("COURSE-006")

    totals = {slug: sum(c.values()) for slug, c in tier_counts.items()}
    ranked = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)

    label = {_TIER_TITLE: "high (title)", _TIER_DESCRIPTION: "high (objective)",
              _TIER_REPEATED_BODY: "medium (repeated body)", _TIER_INCIDENTAL: "low (incidental)"}

    grand_high = grand_medium = grand_low = 0
    print(f"{'term':40s} {'count':>6s}  {'courses':>7s}  high  medium  low")
    for slug, total in ranked[:top]:
        c = tier_counts[slug]
        high = c[_TIER_TITLE] + c[_TIER_DESCRIPTION]
        medium = c[_TIER_REPEATED_BODY]
        low = c[_TIER_INCIDENTAL]
        grand_high += high
        grand_medium += medium
        grand_low += low
        print(f"{slug:40s} {total:6d}  {len(courses_touched[slug]):7d}  {high:4d}  {medium:6d}  {low:4d}")

    # Totals across ALL terms (not just the printed top N).
    for slug, total in ranked[top:]:
        c = tier_counts[slug]
        grand_high += c[_TIER_TITLE] + c[_TIER_DESCRIPTION]
        grand_medium += c[_TIER_REPEATED_BODY]
        grand_low += c[_TIER_INCIDENTAL]

    print(f"\nTotals across all {len(ranked)} terms with >=1 association:")
    print(f"  high_confidence:   {grand_high}")
    print(f"  medium_confidence: {grand_medium}")
    print(f"  low_confidence:    {grand_low}")
    print(f"  total:             {grand_high + grand_medium + grand_low}")


if __name__ == "__main__":
    top_n = 30
    if "--top" in sys.argv:
        top_n = int(sys.argv[sys.argv.index("--top") + 1])
    main(top_n)
