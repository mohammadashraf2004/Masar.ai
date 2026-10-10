# Writing example answers for written exercises

Written exercises (graded by the AI evaluator) can carry one good answer in English and
Arabic. Learners see it after their first evaluated answer, and the evaluator receives it as
its reference. The evaluator's prompt already treats a reference as "one acceptable answer,
not a specification", so an example never forces learners into one wording.

## Status (2026-10-10)

| Course | Written exercises | Done |
|--------|------------------:|-----:|
| COURSE-001 … COURSE-007 | 134 | all |
| COURSE-008 | 59 | 0 |
| COURSE-009 | 169 | 0 |
| COURSE-010 | 49 | 0 |
| COURSE-011 | 44 | 0 |
| COURSE-012 | 8 | 0 |
| COURSE-013 | 12 | 0 |
| COURSE-014 | 3 | 0 |
| COURSE-015 | 71 | 0 |
| COURSE-016 | 70 | 0 |
| COURSE-017 | 16 | 0 |
| COURSE-018 | 12 | 0 |
| **Total** | **647** | **134** |

Exercises without an example keep working exactly as before; the "Show an example answer"
button simply does not appear for them.

## Where things live

- `backend/app/services/curriculum/examples/cNNN.py` — one module per course, or parts
  `cNNN_a.py`, `cNNN_b.py` … for large courses. Each defines
  `EXAMPLES = {"COURSE-008.M01.L01.EX01": ("English…", "Arabic…"), ...}`.
- `examples/__init__.py` — validation rules and `COMPLETE_COURSES`.
- `examples/catalog.py` — merges every module whose name matches `c\d{3}(_[a-z])?`.
- Loader: `apply_example_answers` runs after the guided exercises; the importer writes
  `exercises.example_answer` / `example_answer_ar` (migration 040).

## Step by step for one course

1. List what is missing (inside the backend test image, from `backend/`):

   ```
   python scripts/example_answers_status.py                 # coverage per course
   python scripts/example_answers_status.py COURSE-008 0 12 # first 12 briefs to write
   ```

2. Read each brief and write the answer into `examples/c008.py` (or `c008_a.py`,
   `c008_b.py` for 40+ exercises). Work in batches of about 10–12.

3. Run the checks:

   ```
   python -m pytest tests/test_written_example_answers.py -q
   ```

4. When every written exercise of the course has an example, add the course id to
   `COMPLETE_COURSES` in `examples/__init__.py`. From then on the test suite fails if an
   exercise of that course loses its example or a new written exercise is added without one.

5. Update the status table above.

## Rules for a good example answer

- Answer every numbered instruction of the brief, in order, using the same numbering.
  Keep each point short; tables are fine for comparisons.
- Ground every fact in the lesson the exercise belongs to. Use the lesson's numbers and
  terms (for example the reported accuracy in a chapter). Do not invent figures or claims;
  when the brief asks for a design, give one sound design and say what remains a choice.
- Stay specific and correct rather than long: one good answer, not every possible answer.
  The limit is 40–4,000 characters per language (enforced).
- Arabic: write the explanation in Arabic and keep technical terms, code, API names and
  numbers in English, as the platform's terminology policy does (for example
  "يقلل الـ dropout الـ overfitting"). The Arabic must say the same thing as the English, not
  a summary of it.
- Plain text. Lines and simple Markdown-like tables render with line breaks preserved.
  Do not put triple double quotes inside an answer (the files use `"""` strings).
- Never include personal data, secrets or links that are not in the lesson.

## Checklist before committing

- `python -m pytest tests/test_written_example_answers.py tests/test_guided_exercises.py -q`
- Spot-read a few answers in the app (Arabic and English) after re-importing locally.
- Commit the new `examples/cNNN*.py` files and the `COMPLETE_COURSES` change together.

## Deploying new answers

Answers reach learners through the curriculum import: deploy the code (migration 040 must
already be applied), then re-import the courses. No other migration is needed.
