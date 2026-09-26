# Applied Deep Learning | التعلم العميق التطبيقي

Practical PyTorch course seed package for **COURSE-003**. Source review of BOOK-003 is complete (9/9 chapters).

## Practicality upgrade

This export intentionally makes the course more hands-on than the earlier foundations course:

- **47 lesson files** across **16 modules** (14 core + 2 optional specializations).
- **Every lesson contains runnable guided PyTorch code.**
- **At least 2 code exercises per lesson = 94 code exercises** with starter code and acceptance criteria.
- Debugging, shape/device/dtype assertions, benchmarking and experiments are used throughout instead of passive API memorization.
- **16 module projects/labs**, including **9 portfolio-scale projects**.
- Core guided time: **27h 25m**. Optional audio + advanced vision: **6h 10m**. Total including optional: **33h 35m**.

## Structure

- `course_manifest.json` — course/module/lesson index, source chapter/file line mappings, core/optional flags.
- `modules/M##_*/T###_*.py` — one lesson per Python file. Each exports `SOURCE`, `MODERNIZATION`, and `TOPIC`.
- `TOPIC['lesson']['guided_code']` — runnable example or core implementation pattern.
- `TOPIC['exercises']` — two practical exercises with `starter_code`, acceptance criteria, validation code when useful, and hints.
- `TOPIC['project']` — attached to the final lesson of each module.
- `course_data.py` — assembles the portable `LEVELS -> topics` structure; performs no DB writes.
- `validate_course.py` — validates counts, IDs/slugs, Python syntax and starter-code syntax.

Run:

```bash
python validate_course.py
python course_data.py
```

## Scope boundary

This course teaches applied PyTorch model building, training, fine-tuning, debugging, profiling, export, robustness, recurrent sequence implementation, plus optional audio/advanced vision. Docker/Kubernetes/cloud serving are reserved for MLOps. Modern Transformer fine-tuning belongs in a separate Applied NLP / AI Developer course. Distributed PyTorch and modern quantization remain source gaps rather than being invented from BOOK-003.

## Source policy

BOOK-003 remains the primary source. Exercises, projects, explanations and modernization code are **Masar additions**, clearly separated in each lesson file. Outdated source APIs (legacy torchtext, TorchScript-first export, old pretrained=True, old SoX effects, maskrcnn-benchmark) are not copied as current best practice.
