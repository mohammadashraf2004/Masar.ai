# COURSE-015 — Voice AI Engineering: Real-Time Voice Agents

Finalized Masar curriculum export from **BOOK-015 — Building Live Voice Agents** plus current-doc modernization boundaries captured during curriculum design.

- **Course ID:** COURSE-015
- **Modules:** 8
- **Lessons:** 64
- **Guided time:** 67h 30m (provisional until lesson-authoring re-audit)
- **Module projects:** 7
- **Final capstone:** Production-Ready Multilingual Voice AI Agent
- **Source review:** Chapters 1–20 complete
- **Manual source figures:** 2 required / 6 optional
- **Frozen IDs:** M015-01..M015-08 / L015-001..L015-064

## Windows-safe filenames

This archive intentionally uses short filesystem paths (`M015-01/L015-001.py`) while preserving full lesson titles/slugs inside metadata. Compiled Python cache files (`__pycache__`, `.pyc`) are excluded. See `WINDOWS_README.md`.

## Folder contract

Each module folder contains one Python file per lesson. Every lesson file includes:

- `LESSON_ID` / `MODULE_ID` / `LESSON_META`
- chapter-level BOOK-015 source mapping
- duration / slug / prerequisite metadata
- Arabic-first Masar instructional Markdown framing
- two exercises
- a three-question quiz with explanations
- module project metadata on the module-final lesson

The package also includes course/module/lesson manifests, manual-figure references, Masar-original diagram specs, setup notes, loader, repository-neutral seed adapter, validation, tree, finalization audit, and capstone metadata.

## Module inventory

| Module | Title | Lessons | Guided time |
|---|---|---:|---:|
| M015-01 | Voice AI Fundamentals & Real-Time Audio | 8 | 6h 45m |
| M015-02 | Streaming STT & TTS Engineering | 8 | 8h 15m |
| M015-03 | Real-Time Voice with Gemini Live | 8 | 8h 15m |
| M015-04 | Real-Time Voice with OpenAI Realtime | 8 | 8h 15m |
| M015-05 | Provider-Neutral Voice Agent Architecture | 8 | 8h 20m |
| M015-06 | External Speech Services & Multi-Channel Voice | 8 | 8h 50m |
| M015-07 | Advanced Voice Agents & Telephony | 8 | 8h 30m |
| M015-08 | Production Voice AI Engineering | 8 | 10h 20m |

## Important boundaries

- This is a **repository-neutral curriculum/course-folder seed export**, not proof of production Masar database integration.
- Provider model IDs, pricing, limits, language support, exact SDK APIs, and beta features are dynamic and must be verified against current official documentation when a lesson/lab is authored or run.
- Generic LLM, RAG, agent, multi-agent, Docker/CI/CD, and multimodal foundations remain owned by prerequisite Masar courses; COURSE-015 teaches their Voice-specific integration.
- Source-book figures are manual references only. Never ask the user to upload them to ChatGPT. Prefer Masar-original redraws.

## Validation

```bash
python validate_course.py
```

The validator checks Python syntax/import, module/lesson counts, contiguous IDs, unique slugs, guided minutes, exercises/quizzes, module projects, capstone, manual-figure counts, and core manifest consistency.
