# COURSE-009 — Enterprise RAG Engineering

Finalized Masar curriculum export from BOOK-009.

- **Course ID:** COURSE-009
- **Source:** BOOK-009
- **Book title / edition:** SOURCE INFORMATION MISSING
- **Source review:** Chapters 1–10 complete
- **Modules:** 10
- **Lessons:** 80
- **Guided lesson time:** 72h15m
- **Approval:** Not explicitly approved
- **Frozen IDs:** M009-01..M009-10 / L009-001..L009-080
- **Manual visual references:** 14

## Professional capability

Engineer production RAG systems that combine high-precision retrieval, enterprise data ingestion, grounding and hallucination control, rigorous evaluation, agentic and multimodal retrieval, knowledge-graph enhancement, latency/cost optimization, observability, governance, and production resiliency.

## Folder contract

Each module folder contains one Python file per lesson. Every lesson file contains:

- `LESSON_ID` / `MODULE_ID` / `LESSON_META`
- chapter/section-level source mapping where available
- curriculum role (`CORE`, `REVISION + EXTENSION`, `MASAR SYNTHESIS`, etc.)
- original Masar Markdown instructional content
- two practical exercises
- a three-question quiz with explanations
- the module project on the final lesson

The export intentionally treats prerequisite material from COURSE-005..008 as revision instead of rebuilding those courses.

## Module inventory

| Module | Title | Lessons | Guided time |
|---|---|---:|---:|
| M009-01 | Production RAG Architecture & Failure Analysis | 4 | 2h 50m |
| M009-02 | Enterprise Data Ingestion & Document Engineering | 8 | 7h 15m |
| M009-03 | High-Precision Retrieval: Hybrid Search & Reranking | 8 | 7h 15m |
| M009-04 | Agentic Retrieval & Agentic RAG | 8 | 7h 20m |
| M009-05 | Grounding, Hallucination Control & RAG Guardrails | 6 | 5h 30m |
| M009-06 | RAG Evaluation Engineering | 10 | 9h 05m |
| M009-07 | Multimodal Enterprise RAG | 9 | 8h 15m |
| M009-08 | Knowledge-Enhanced RAG | 9 | 8h 15m |
| M009-09 | Production Performance, Governance, Observability & Resiliency | 9 | 8h 10m |
| M009-10 | Enterprise RAG Evolution, System Integration & Capstone | 9 | 8h 20m |

## Capstone

**Production Enterprise Knowledge Assistant** — integrate heterogeneous ingestion, high-precision retrieval, grounding controls, evaluation, observability, federated access, and production decision records.

## Integration

The supplied application hierarchy is:

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

The application schema does not expose a reusable `Course` entity. `seed_course_009.py` therefore requires an explicit `MASAR_COURSE009_TRACK_SLUG`. It creates COURSE-009 module levels by title only when they do not already exist and does **not** overwrite existing lesson/exercise/quiz/project rows.

Run from the Masar backend only after reviewing the target track mapping:

```bash
export MASAR_COURSE009_TRACK_SLUG="ai-developer"
python path/to/COURSE-009-Enterprise-RAG-Engineering/seed_course_009.py
```

Use the correct target track slug for your repository; COURSE-009 is reusable across ML Engineer, AI Developer, MLOps Engineer, and AI Engineer tracks.

## Validation

```bash
python validate_course.py
```

The export validates:

- 10 module folders
- 80 lesson files
- Python syntax
- unique frozen lesson IDs
- unique topic slugs
- two exercises per lesson
- three quiz questions per lesson
- 10 module projects
- 4,335 guided minutes
- 14 manual visual references

## Visual assets

No book images are included. `assets/visual_assets_manifest.json` lists the 14 figures to add manually. Check reuse rights before publication; use original Masar redraws where rights are unclear.

## Status boundary

This package is a **course-folder/database-seed export from a finalized curriculum design**. It does not prove that:

- every exercise or lab has been executed end-to-end;
- every external model/API/framework still matches source-era interfaces;
- repository-specific imports match the current production repository;
- database insertion has been tested against production data;
- frontend rendering has been tested;
- visual assets have been populated;
- the course has been deployed.

`seed_course_009.py` is syntax-validated here, but its application imports can only be integration-tested inside the real Masar backend.
