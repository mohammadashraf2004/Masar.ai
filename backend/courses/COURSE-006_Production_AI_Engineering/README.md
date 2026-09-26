# COURSE-006 — Production AI Engineering

Implementation-ready **Masar curriculum seed package** generated from the completed BOOK-006 curriculum design.

## Frozen curriculum

- Course ID: `COURSE-006`
- Source: `BOOK-006 — AI Engineering`
- Modules: **10**
- Lessons: **67**
- Guided time: **53h 50m**
- Module IDs: `M006-01..M006-10`
- Lesson IDs: `L006-001..L006-067`
- Status: curriculum design finished; seed package generated

> Final validation corrected an earlier arithmetic summary: M006-08 contains eight designed lessons (`L006-049..L006-056`), so the consistent frozen total is 67 lessons / 53h50m.

## Package structure

```text
COURSE-006_Production_AI_Engineering/
├── course_manifest.py
├── course_data_loader.py
├── seed_course.py
├── validate_course.py
├── README.md
├── EXPORT_REPORT.md
└── m006_XX_.../
    ├── module_manifest.py
    └── l006_XXX_....py
```

Every lesson file exports a `LESSON` dictionary containing:

- stable course/module/lesson IDs
- title and slug
- guided minutes
- CORE / REVISION / production-extension classification
- BOOK-006 source mapping
- production focus
- learning objectives
- content outline
- practice task and acceptance criteria
- short quiz with explanations

## Masar integration

Masar's application hierarchy is expected to map curriculum into:

`CareerTrack → TrackLevel → Topic → {Lesson, Exercise, Quiz, Project}`

This package intentionally does **not** invent repository-specific SQLAlchemy/Pydantic field names. `seed_course.py` defines a small adapter protocol. Implement its three `ensure_*` methods against the actual Masar repository models and use the stable IDs for idempotency.

The adapter should never overwrite learner progress or unrelated records.

## Validate

```bash
python validate_course.py
```

Expected:

```text
VALIDATION: PASS
modules=10 lessons=67 guided_minutes=3230 guided_time=53h50m
```

## Load curriculum data

```bash
python course_data_loader.py
```

## Dry-run seed count

```bash
python seed_course.py
```

## Important boundary

This ZIP is a structured curriculum/database-seed package. Syntax and package validation do not prove that repository-specific database insertion, provider APIs, external checkpoints, frontend rendering, or production deployment have been tested end-to-end.
