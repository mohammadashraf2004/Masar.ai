# COURSE-013 — Applied Data Analysis with Python

**Status:** Finalized  
**Version:** 1.0  
**Primary track:** Data Analyst — Core  
**Lessons:** 88  
**Modules:** 10  
**Guided lesson time:** 70h 55m  
**Capstone:** End-to-End Real-World Data Analysis Capstone (8h suggested, not included in guided lesson time)  
**Source:** BOOK-013 — title/edition not supplied

## Export contract

This folder follows the Masar course-code export style:

- module folders;
- one plain-Python seed file per lesson;
- `LESSON_META` and `TOPIC` in every lesson file;
- 2 exercises and 3 quiz questions with answers/explanations per lesson;
- module projects where defined;
- course/module/assets manifests;
- framework-neutral seed adapter;
- loader;
- validation script;
- final capstone;
- manual figure manifest.

No concrete database/ORM fields are assumed. Map the returned dictionaries to the live Masar application schema in the application layer.

## Module map

- M013-01 — Data Analysis Workflow, Roles & Python Workspace (6 lessons)
- M013-02 — NumPy & pandas for Analytical Data Work (10 lessons)
- M013-03 — Practical Statistics & Experimentation for Data Analysts (11 lessons)
- M013-04 — Linear Algebra Essentials for Data Analysis (3 lessons)
- M013-05 — Visual Analysis & Interactive Dashboards (9 lessons)
- M013-06 — Data Retrieval, Storage & Ingestion (8 lessons)
- M013-07 — Data Cleaning, Quality & Feature Engineering (8 lessons)
- M013-08 — Time-Series Analysis & Forecasting (9 lessons)
- M013-09 — Applied Predictive Analytics (16 lessons)
- M013-10 — Segmentation, Dimensionality Reduction & Anomaly Detection (8 lessons)

## Frozen source scope

BOOK-013 Chapters 1–12 were used to construct COURSE-013. Chapters 13–17 are intentionally excluded from this course because their subject matter is already owned by dedicated NLP, vision/deep-learning, LLM, scaling, or big-data courses.

## Visual assets

Required manual source figures: **4**  
Optional source figures: **8**

See `assets_manifest.json`.

## Validation

Run:

```bash
python validate_course.py
```

Expected:

```text
COURSE-013 validation passed: 10 modules, 88 lessons, 4255 guided minutes.
```
