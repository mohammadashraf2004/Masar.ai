# COURSE-005 — Applied LLM Engineering

Finalized Masar curriculum export.

- **Course ID:** COURSE-005
- **Source:** BOOK-005
- **Book title / edition:** SOURCE INFORMATION MISSING
- **Modules:** 10
- **Lessons:** 70
- **Guided lesson time:** 50h55m
- **Source review:** 12/12 chapters complete
- **Approval:** Not explicitly approved
- **Frozen IDs:** M005-01..M005-10 / L005-001..L005-070

## Folder contract

Each module folder contains one Python file per lesson. Every lesson file contains:

- `LESSON_ID` / `MODULE_ID` / `LESSON_META` with source mapping, curriculum role, concepts, prerequisites, and modernization notes
- `TOPIC` using only fields present in the supplied Masar seed template
- lesson Markdown content
- two exercises
- a quiz with explanations
- a module project on the final lesson

Repeated material from COURSE-001 through COURSE-004 is explicitly labeled **REVISION** rather than silently duplicated as new knowledge.

`prerequisite_ids` inside `TOPIC` is intentionally empty because the supplied application schema expects runtime database IDs, not curriculum IDs. Stable curriculum prerequisites remain in `LESSON_META`.

## Integration

The supplied application model is `CareerTrack -> TrackLevel -> Topic -> Lesson / Exercise / Quiz / Project`; it does not expose a reusable Course entity. Because COURSE-005 belongs to several tracks, `seed_course_005.py` requires an explicit `MASAR_COURSE005_TRACK_SLUG` and does **not** silently duplicate the course across tracks. Review that mapping in the actual repository before production seeding.

## Validation

Run:

```bash
python validate_course.py
```

The export validates file count, module count, Python syntax, unique lesson IDs, unique slugs, frozen ID range, and total guided minutes.

## Status boundary

This package is a **course-folder / database-seed draft export** from the completed curriculum design. It does not prove:

- every code exercise or training job has executed end-to-end,
- all external checkpoints/APIs/packages still expose the source-era interfaces,
- the seed adapter matches later repository changes,
- database insertion has been tested against production data,
- frontend rendering has been tested, or
- the course has been deployed.

## Protected future-course boundaries

- Full RAG Systems Engineering remains a dedicated future course.
- Deep multimodal / vision-language implementation remains a future specialized course.
- Production serving, Kubernetes, observability, rollout, and model operations remain future MLOps / Production ML material.
- Advanced production agent engineering remains deeper future material beyond the COURSE-005 foundations.
