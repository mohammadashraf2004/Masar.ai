# COURSE-010 — AI Service Engineering with FastAPI

Finalized Masar curriculum/course-folder seed export from BOOK-010.

- **Course ID:** COURSE-010
- **Source:** BOOK-010 — *Building Generative AI Services with FastAPI* by Alireza Parandeh
- **Edition / page ranges:** SOURCE INFORMATION MISSING where not supplied
- **Source review:** Chapters 1–12 complete
- **Modules:** 9
- **Lessons:** 84
- **Guided lesson time:** 71h00m
- **Approval:** Not explicitly approved
- **Frozen IDs:** M010-01..M010-09 / L010-001..L010-084
- **Manual visual references:** 29

## Professional capability

Design, implement, secure, test, optimize, and deploy production-oriented backend services for AI applications using FastAPI, typed contracts, model lifecycle management, asynchronous workloads, streaming, databases, identity/access controls, runtime security, testing, and containerization.

## Folder contract

Each module folder contains one Python file per lesson and a `module_project.py`. Every lesson file contains:

- `LESSON_ID` / `MODULE_ID` / `LESSON_META`
- chapter/section-level source mapping where available
- curriculum role
- learner-facing Markdown instructional content
- two practical exercises
- a three-question quiz with explanations
- the module project on the final lesson

## Module inventory

| Module | Title | Lessons | Guided time |
|---|---|---:|---:|
| M010-01 | AI Service Architecture & FastAPI Foundations | 10 | 7h 15m |
| M010-02 | Model Integration, Lifecycle & Type-Safe API Contracts | 14 | 10h 30m |
| M010-03 | Async AI Workloads, Concurrency & Background Processing | 8 | 7h 15m |
| M010-04 | Streaming & Real-Time AI Communication | 7 | 6h 10m |
| M010-05 | Persistence & Database Engineering for AI Services | 8 | 6h 50m |
| M010-06 | Authentication, Authorization & Secure Service Boundaries | 14 | 12h 20m |
| M010-07 | AI Service Performance & Optimization | 7 | 5h 50m |
| M010-08 | Testing & Reliability Engineering for AI APIs | 8 | 7h 05m |
| M010-09 | Containerized AI Service Deployment & Capstone | 8 | 7h 45m |

## Capstone

**Production-Ready AI Service with FastAPI** — progressively build a service architecture, typed provider gateway, concurrent/streaming runtime, persistence, identity/security controls, optimization, release test suite, and containerized production candidate.

## Integration

The supplied Masar hierarchy from the prior seed exports is:

```text
CareerTrack
    ↓
TrackLevel
    ↓
Topic
    ├── Lesson
    ├── Exercise
    ├── Quiz
    └── Project
```

`seed_course_010.py` requires an explicit `MASAR_COURSE010_TRACK_SLUG` and does not overwrite existing lesson/exercise/quiz/project rows. Review the target track mapping inside the real backend before running it.

## Validation

```bash
python validate_course.py
```

The package validates 9 module folders, 84 lesson files, Python syntax, embedded Python snippets, frozen IDs, unique slugs, 2 exercises and 3 quiz questions per lesson, 9 module projects, 4,260 guided minutes, and 29 manual visual references.

## Status boundary

This ZIP is a **course-folder/database-seed export from the finalized curriculum design**. Syntax/structure validation does not prove that every external provider API, database import, deployment platform, exercise, frontend renderer, or production integration has been executed against the current Masar repository.
