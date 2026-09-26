# COURSE-011 — Cloud Deployment & CI/CD for AI Engineers

## Frozen current scope

This package exports the curriculum **exactly at the current approved scope**:

- Modules: 6
- Lessons: 85
- IDs: `L011-001` → `L011-085`
- Kubernetes: **not included**
- Monitoring / observability: **not included**
- Required manual figures: 14
- Optional manual figures: 7

## Masar export shape

```text
CareerTrack
└── TrackLevel
    └── Topic / Module
        ├── Lesson
        ├── Exercise
        ├── Quiz
        └── Project
```

This repository-neutral package does **not** assume your application/database field names.
`course_data.py` loads a generic payload that you can map to Masar's real models.

## Folder structure

- `course_manifest.json` — authoritative course metadata and counts
- `assets_manifest.json` — figures the learner/admin should add manually
- `course_data.py` — generic loader for all module and lesson seed files
- `seed_course.py` — repository-neutral seed adapter entry point
- `validate_course.py` — validates IDs, slugs, syntax, counts, projects, and figures
- `modules/` — one folder per module
- each lesson is one Python seed file containing:
  - `LESSON_META`
  - `TOPICS`
  - `SOURCE_REFERENCES`
  - `LESSON_MARKDOWN`
  - `EXERCISES`
  - `QUIZ`
  - optional `PROJECT` on the final lesson of each module

## Integration

1. Run validation:
   ```bash
   python validate_course.py
   ```
2. Inspect the generic payload:
   ```bash
   python seed_course.py
   ```
3. Map the generic structures in `course_data.py` to the real Masar repository/database models.
4. Keep seeding idempotent in the real application: upsert by stable `course_id`, `module_id`, `lesson_id`, and `slug`.
5. Do not overwrite learner progress or approved content without an explicit migration.

## Figures

No source-book image is bundled. `assets_manifest.json` lists exactly which figures should be added manually and where.

