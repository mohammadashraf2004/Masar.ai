# COURSE-007 — Advanced LLM Systems & Application Architecture

Finalized Masar curriculum export from BOOK-007.

- **Course ID:** COURSE-007
- **Source:** BOOK-007
- **Book title / edition:** SOURCE INFORMATION MISSING
- **Source structure:** 3 parts / 13 chapters
- **Modules:** 10
- **Lessons:** 60
- **Guided lesson time:** 40h30m
- **Source review:** 13/13 chapters complete
- **Approval:** Not explicitly approved
- **Frozen IDs:** M007-01..M007-10 / L007-001..L007-060

## Corrected source identity

The initial VLM framing was discarded after the corrected book front matter was provided. The supplied source explicitly focuses on LLMs and LLM application systems and states that multimodal models are out of scope. COURSE-007 is therefore an advanced LLM systems course, not a VLM course.

## Folder contract

Each module folder contains one Python file per lesson. Every lesson file contains:

- `LESSON_ID` / `MODULE_ID` / `LESSON_META`
- chapter-level source mapping
- explicit curriculum role (`REVISION`, `EXTENSION`, or `MASAR SYNTHESIS`)
- original Masar Markdown instructional framing
- two exercises
- a three-question quiz with explanations
- a module project on the final lesson

Repeated material from COURSE-001 through COURSE-006 remains explicitly labeled **REVISION**, following the user's final duplication rule.

`prerequisite_ids` inside `TOPIC` is intentionally empty because the supplied application schema expects runtime database IDs rather than stable curriculum IDs. Stable curriculum prerequisites remain in `LESSON_META`.

## Module inventory

| Module | Title | Lessons | Guided time |
|---|---|---:|---:|
| M007-01 | LLM Foundations & Pre-Training Revision | 4 | 1h55m |
| M007-02 | Pretrained Model Selection, Evaluation & Execution | 5 | 2h50m |
| M007-03 | Fine-Tuning & Dataset Engineering | 6 | 4h05m |
| M007-04 | Advanced Model Adaptation & Model Fusion | 5 | 3h50m |
| M007-05 | Alignment, Reliability & Reasoning | 6 | 4h05m |
| M007-06 | Inference Performance Engineering | 6 | 4h00m |
| M007-07 | LLM Application Paradigms, Tools & Agents | 8 | 5h20m |
| M007-08 | Embeddings, Retrieval & Document Representation | 7 | 5h05m |
| M007-09 | Advanced RAG Systems Engineering | 8 | 5h55m |
| M007-10 | LLM System Architecture & Programming Patterns | 5 | 3h25m |

## Integration

The supplied application model is `CareerTrack -> TrackLevel -> Topic -> Lesson / Exercise / Quiz / Project`; it does not expose a reusable Course entity. Because COURSE-007 belongs to several tracks, `seed_course_007.py` requires an explicit `MASAR_COURSE007_TRACK_SLUG` and does **not** silently duplicate the course across tracks.

## Validation

Run:

```bash
python validate_course.py
```

The export validates lesson count, module count, Python syntax, unique lesson IDs, unique slugs, frozen ID range, module-project count, and total guided minutes.

## Duration audit

The final package normalizes M007-07 to **5h20m**, preserving the latest cumulative COURSE-007 total of **40h30m**. Four short revision/application lessons in that module are set to 30 minutes so lesson-level totals match the module and course totals exactly.

## Status boundary

This package is a **course-folder / database-seed draft export** from the finalized curriculum design. It does not prove that:

- every code exercise or training job has run end-to-end,
- all external checkpoints/APIs/packages still expose source-era interfaces,
- the seed adapter matches later repository changes,
- database insertion has been tested against production data,
- frontend rendering has been tested, or
- the course has been deployed.

## Source boundaries

The supplied book front matter states that:

- multimodal models are out of scope,
- multilingual LLMs are mostly out of scope,
- deep theory/math is not the focus,
- reasoning-model coverage is rudimentary.

The isolated source-supported topics on screenshot-based computer use and visual/layout-aware document retrieval are therefore kept as narrow application extensions, not evidence that the course is multimodal.
