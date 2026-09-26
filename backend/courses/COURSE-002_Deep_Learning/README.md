# Deep Learning Foundations | أساسيات التعلم العميق

**Only the course folder.** 19 modules, 147 individual Python topic/lesson files,
original theoretical exercises and knowledge checks, and one Masar design project
attached to the final lesson of each module. Total estimated guided time: 111h 20m.

## Structure

- `course_manifest.json`: chapter-to-module index and exact *source-file line* mappings.
- `modules/M##_*/T###_*.py`: **one lesson per file**, with `TOPIC` fields aligned with
  your uploaded seed example: `title`, `slug`, `description`, `order`, `difficulty`,
  `estimated_hours`, `skill_tags`, `prerequisite_ids`, `lesson`, `exercises`, `quiz`,
  and optional `project`. Each also exposes `SOURCE`.
- `course_data.py`: assembles the 19 modules into the same structural
  `LEVELS -> topics -> lesson/exercises/quiz/project` shape.

To inspect: `python course_data.py` from this folder. This command **does not**
write to a database. The uploaded example targets the `CareerTrack` SQLAlchemy
model, whereas this is a shared course usable by several tracks; your actual
course model and track associations need to be mapped before creating a DB seed.
Difficulty is stored as a portable string and should be mapped to
`DifficultyLevel` when integrating; `prerequisite_ids=[]` until actual database IDs
are known. The lesson files contain authored Arabic instructional seeds, not copies
of book chapters or tested implementation recipes.

## Source and scope

Chapters **1–6 and 8–20** are represented. **Chapter 7 (A Deep Dive on Keras)
is intentionally excluded**, with no lesson or project. Other chapters' Keras,
JAX and TensorFlow fragments are conceptual references, not implementation
requirements. A separate PyTorch-focused Applied Deep Learning course awaits
its own book. Printed page numbers and exact book edition remain
`SOURCE INFORMATION MISSING`; the included line spans refer to the supplied
Markdown excerpts. Projects, lesson explanations, practices, and quizzes are
Masar originals grounded in the chapter-mapped curriculum.

This is an export of instructional seed content, not a claim of a deployed or
published course. Before DB insertion, review compatibility with your actual
model schema, resolve persistent prerequisites, and validate any code intended
for execution.
