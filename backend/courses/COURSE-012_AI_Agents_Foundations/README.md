# COURSE-012 — AI Agents Foundations

Build AI agents from the ground up: what an agent is, how tools and the Model Context
Protocol (MCP) extend it, multi-agent patterns, reasoning and planning, memory and RAG,
evaluation, deployment, agentic loops and cognitive agents. Based on **AI Agents in
Action**; each lesson covers one book chapter.

- **Course ID:** COURSE-012 (slug `course-012`)
- **Layout:** `modules/module_NN.py` — one self-contained lesson per file; the lesson's
  module and position come from its own `LESSON_CODE` / `MODULE_ORDER`, not its file name.
- **Loaded structure:** 1 module / 11 lessons (see `course_manifest.json`).
- **Hard prerequisite:** COURSE-005 — Applied LLM Engineering.
- **Recommended first:** COURSE-006 (production AI) and COURSE-010 (FastAPI, Docker) for
  the deployment lesson; COURSE-009 (enterprise RAG) for the retrieval lesson. COURSE-011
  is deliberately not listed: it recommends COURSE-007, which follows this course.

| Module | Title | Lessons |
|---|---|---:|
| M012-01 | Foundations of AI Agents | 11 |

## Scope relative to COURSE-007

COURSE-012 is the general agent course: agent architecture, a first MCP server, and the
surrounding engineering (multi-agent, planning, memory, evaluation, deployment).
COURSE-007 (AI Agents with MCP) follows it and goes deep on MCP alone — clients, servers,
transports, security and the ecosystem. COURSE-007 does not require this course (it
introduces agents itself), but lesson M01.L03 here is the gentler first pass over MCP.

## Notes

- This course replaced the earlier 11-module / 91-lesson "Agentic AI Systems Engineering"
  design; those lesson files are gone from the working tree (history has them).
- `assets/` and `assets_manifest.json` hold the book figures; the new lessons carry
  `[[IMAGE_NEEDED]]` placeholders and do not place them yet (see the figure xfail in
  `tests/test_course_figures_real.py`).
- `capstone/` describes the old, much larger course and is not loaded by the new layout.
- `00-course-setup/` holds the setup guides (Python environment, MCP/Node, environment
  variables).
- The curriculum registry is `backend/seeds/curriculum.py`; the loader is
  `backend/app/services/curriculum/loaders.py`.
