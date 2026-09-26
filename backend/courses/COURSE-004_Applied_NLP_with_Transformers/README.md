# COURSE-004 — Applied NLP with Transformers

Finalized Masar curriculum export.

- **Course ID:** COURSE-004
- **Source:** BOOK-004
- **Book title / edition:** SOURCE INFORMATION MISSING
- **Modules:** 11
- **Lessons:** 71
- **Guided lesson time:** 49h45m
- **Source review:** 11/11 chapters complete
- **Approval:** Not explicitly approved

## Folder contract

Each module folder contains one Python file per lesson. Every lesson file contains:

- `LESSON_ID` / `MODULE_ID` / `LESSON_META` (source mapping, concepts, prerequisites, modernization)
- `TOPIC` using only fields present in the supplied Masar seed template
- lesson Markdown content
- two exercises
- a quiz with explanations
- a module project on the final lesson where appropriate

`prerequisite_ids` inside `TOPIC` is intentionally left empty because the supplied application schema expects runtime database IDs, not curriculum IDs. Stable curriculum prerequisites are preserved in `LESSON_META`.

## Integration

The supplied application model is `CareerTrack -> TrackLevel -> Topic -> Lesson / Exercise / Quiz / Project`; it does not expose a reusable Course entity. Because COURSE-004 belongs to several tracks, `seed_course_004.py` requires an explicit `MASAR_COURSE004_TRACK_SLUG` and **does not silently duplicate the course across tracks**. Review that mapping in the actual repository before production seeding.

## Validation

Run:

```bash
python validate_course.py
```

The export validates file count, module count, Python syntax, unique lesson IDs, unique slugs, and total guided minutes.

## Status boundary

This package is a **course-folder / database-seed draft export** from the finalized curriculum design. It does not prove:

- every exercise has been executed end-to-end,
- all external model checkpoints remain available,
- the seed adapter matches later repository changes,
- database insertion has been tested against production data,
- frontend rendering has been tested, or
- the course has been deployed.
