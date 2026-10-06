# COURSE-016 — Machine Learning Systems & MLOps Engineering

Repository-neutral Masar curriculum seed export.

## Completion structure

- **Core:** M016-01..M016-10 — 94 lessons — **80h 15m**
- **Optional Kubernetes:** M016-11 — 31 lessons — **27h 45m**
- **Required capstone:** M016-12
- Total lesson time if optional Kubernetes is taken: **108h 00m**

The six Kubernetes source chapters (3, 5, 6, 8, 11, 15) are intentionally **optional**. They do not block core COURSE-016 completion.

## Loader behavior

`course_data.load_course()` loads core lessons only. Use `load_course(include_optional=True)` to include M016-11. The seed adapter uses `MASAR_COURSE016_INCLUDE_OPTIONAL_K8S=true` to opt in.

## Source boundaries

Primary source: BOOK-016 — *Designing Machine Learning Systems* (edition: SOURCE INFORMATION MISSING).

Supplemental Kubernetes source: formal book metadata/edition kept as `SOURCE INFORMATION MISSING`; selected chapters are 3, 5, 6, 8, 11, and 15. Kubernetes commands and API details are version-sensitive and should be verified when labs are authored or executed.

## Validation

Run:

```bash
python validate_course.py
```

This validates seed structure and Python syntax. It does **not** prove production Masar ORM integration or execute all ML/MLOps/Kubernetes labs end-to-end.
