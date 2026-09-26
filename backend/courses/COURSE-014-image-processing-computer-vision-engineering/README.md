# COURSE-014 — Image Processing & Computer Vision Engineering

Finalized Masar curriculum seed export from BOOK-014.

- **Course ID:** COURSE-014
- **Source:** BOOK-014
- **Source review:** 13/13 chapters complete
- **Modules:** 10
- **Lessons:** 99
- **Guided lesson time:** 98h 40m
- **Frozen IDs:** M014-01..M014-10 / L014-001..L014-099
- **Finalization:** Finished by user
- **Approval:** Not explicitly approved
- **Manual visual references:** 11 required + 2 optional

## Track roles

- Data Analyst — Optional
- ML Engineer — Core
- AI Developer — Supporting
- MLOps Engineer — Supporting
- AI Engineer — Core

## Prerequisites

- Required: COURSE-001 — Machine Learning Foundations
- Strongly recommended: COURSE-002 — Deep Learning Foundations; COURSE-003 — Applied Deep Learning
- Supporting: COURSE-013 — Applied Data Analysis with Python

## Folder contract

Each module folder contains one Python seed file per lesson. Every lesson file contains:

- `LESSON_ID`
- `MODULE_ID`
- `LESSON_META`
- chapter-level source mapping
- explicit curriculum role
- original Masar Markdown instructional framing
- two exercises with acceptance criteria
- a three-question quiz with answer explanations
- a module project on the final lesson

This is a **repository-neutral curriculum/course-folder seed export**. It does not write to the Masar production database until `seed_course_014.py` is mapped to the current canonical registry / ORM / reconciliation contract.

## Module inventory

| Module | Title | Lessons | Guided time |
|---|---|---:|---:|
| M014-01 | Digital Images & Image Computing Foundations | 7 | 6h 00m |
| M014-02 | Image Manipulation, Geometry & Compositing | 10 | 8h 55m |
| M014-03 | Sampling, Quantization & Frequency-Domain Representation | 9 | 9h 40m |
| M014-04 | Convolution, Correlation & Spatial Filtering | 8 | 8h 05m |
| M014-05 | Frequency-Domain Filtering & Noise Analysis | 8 | 7h 45m |
| M014-06 | Image Enhancement & Computational Photography | 9 | 8h 50m |
| M014-07 | Gradients, Edges & Multiscale Image Analysis | 9 | 9h 05m |
| M014-08 | Image Restoration & Inverse Problems | 9 | 8h 55m |
| M014-09 | Image Segmentation Engineering | 13 | 13h 30m |
| M014-10 | Modern Computer Vision Integration & Capstone | 17 | 17h 55m |

## Manual figures

See `assets_manifest.json`.

The export intentionally does **not** contain copyrighted source-book images. Required source visuals are listed as manual references / redraw targets only.

## Validation

Run:

```bash
python validate_course.py
```

It validates:

- module count
- lesson file count
- Python syntax
- unique lesson IDs
- unique slugs
- frozen ID range
- total guided minutes
- two exercises per lesson
- three quiz questions per lesson
- module-project count
- required/optional figure counts

## Integration boundary

`seed_course_014.py` intentionally raises before database insertion. Connect `build_seed_payload()` to Masar's production curriculum registry and safe reconciliation layer before seeding. Repository-specific imports, database writes, frontend rendering, all optional model/API calls, and production deployment are **not** verified by this standalone package.
