# COURSE-008 — Vision-Language & Multimodal AI Engineering

Finalized Masar curriculum export from BOOK-008 (**Vision Language Models**).

- **Course ID:** COURSE-008
- **Source:** BOOK-008
- **Edition:** SOURCE INFORMATION MISSING
- **Source chapters:** 11/11 processed
- **Modules:** 11
- **Lessons:** 106
- **Guided lesson time:** 96h55m
- **Visual assets:** 76 user-provided reference images
- **Approval:** Not explicitly approved
- **Frozen IDs:** M008-01..M008-11 / L008-001..L008-106

## Professional capability

Build, train, adapt, evaluate, optimize, retrieve with, deploy, and extend modern vision-language and multimodal AI systems across image-text, documents, video, any-to-any generation, visual agents, and VLA architectures.

## Folder contract

Each module folder contains one Python file per lesson. Every lesson file contains:

- `LESSON_ID` / `MODULE_ID` / `LESSON_META`
- source mapping to BOOK-008 chapter
- curriculum role (`CORE`, `REVISION`, `PRACTICAL`, `SYNTHESIS`, etc.)
- original Masar Markdown instructional framing
- two exercises
- a three-question quiz with explanations
- a module project on the final lesson
- visual-asset metadata when a user-provided figure is mapped to the lesson

The package uses the demonstrated Masar schema: `CareerTrack -> TrackLevel -> Topic -> Lesson / Exercise / Quiz / Project`.
`prerequisite_ids` inside `TOPIC` remains empty because the application schema expects runtime database IDs; stable curriculum prerequisites are preserved in `LESSON_META`.

## Module inventory

| Module | Title | Lessons | Guided time |
|---|---|---:|---:|
| M008-01 | Foundations of Vision-Language Systems | 8 | 5h50m |
| M008-02 | Vision-Language Applications & Evaluation | 8 | 6h45m |
| M008-03 | Training Vision-Language Models from First Principles | 10 | 9h15m |
| M008-04 | Multimodal Data Engineering, Curation & Dataset Mixtures | 10 | 9h20m |
| M008-05 | Post-Training & Alignment for Vision-Language Models | 10 | 9h20m |
| M008-06 | Core Architectures of Vision-Language Models | 9 | 8h00m |
| M008-07 | Multimodal Inference & Deployment Engineering | 10 | 9h40m |
| M008-08 | Document AI & Multimodal RAG | 10 | 9h40m |
| M008-09 | Video-Language Models & Video-RAG | 10 | 9h30m |
| M008-10 | Any-to-Any Multimodal Systems | 11 | 10h20m |
| M008-11 | Agentic Vision & Vision-Language-Action Systems | 10 | 9h15m |

## Visual assets

`assets/` contains all 76 user-provided figures with descriptive filenames. `assets_manifest.json` maps each asset to its primary lesson and includes a publication/reuse note.

The lesson database schema shown in the prior Masar export does not include a first-class image/asset field. Therefore assets are stored in the package and referenced in `LESSON_META` rather than inventing unsupported database fields. Integrate these files with the frontend/static asset pipeline before expecting them to render from persisted lesson Markdown.

**Rights note:** several figures may originate from the supplied book or other external sources. Verify reuse/publication rights before public release; where permission is unclear, create an original Masar redraw while preserving the instructional concept.

## Integration

Because the supplied database schema has no reusable Course entity and COURSE-008 belongs to several tracks, `seed_course_008.py` requires an explicit `MASAR_COURSE008_TRACK_SLUG`. It does not silently duplicate the course across tracks.

Example:

```bash
MASAR_COURSE008_TRACK_SLUG=ai-developer python COURSE-008_Vision_Language_and_Multimodal_AI_Engineering/seed_course_008.py
```

## Validation

Run:

```bash
python validate_course.py
```

The validator checks lesson/module counts, Python syntax, unique lesson IDs/slugs, frozen ID range, module-project count, guided minutes, and image-asset count.

## Implementation boundary

This is a **curriculum/course-folder seed export**. It is not proof that every exercise, model checkpoint, training job, document/video pipeline, inference optimization, visual-agent workflow, or VLA experiment has been executed end-to-end in the current Masar repository. Repository imports, database insertion, frontend asset rendering, provider/model APIs, GPU-specific kernels, and production deployment must be validated in the actual application environment.
