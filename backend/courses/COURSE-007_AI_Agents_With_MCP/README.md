# COURSE-007 — AI Agents with MCP

Build agentic applications with the Model Context Protocol (MCP): MCP clients and
servers, tools, prompts and resources, transports, security, and the MCP ecosystem.

- **Course ID:** COURSE-007 (slug `course-007`)
- **Layout:** `modules/module_NN.py` — one self-contained lesson per file; the lesson's
  module and position come from its own `LESSON_CODE` / `MODULE_ORDER`, not its file name.
- **Loaded structure:** 5 modules / 8 lessons (see `course_manifest.json`).
- **Hard prerequisite:** COURSE-005 — Applied LLM Engineering.

| Module | Title | Lessons |
|---|---|---:|
| M007-01 | Agentic AI & MCP Foundations | 1 |
| M007-02 | Building MCP Clients | 2 |
| M007-03 | Building MCP Servers | 3 |
| M007-04 | MCP Transport Layer | 1 |
| M007-05 | MCP Ecosystem and Extensions | 1 |

## Scope relative to COURSE-012

COURSE-012 (AI Agents Foundations) is the general agent course: what an agent is, tools,
a first MCP server, multi-agent patterns, planning, memory/RAG, evaluation and
deployment. COURSE-007 owns MCP in depth — clients, servers, transports, security and the
ecosystem. COURSE-007 introduces agents itself (M07-01), so it needs only COURSE-005;
taking COURSE-012 first is recommended, and its MCP lesson (M01.L03) is the gentler first
pass that this course deepens.

## Notes

- This course replaced the earlier "Advanced LLM Systems & Application Architecture"
  course; that curriculum is not part of COURSE-007.
- No course capstone is defined yet.
- The curriculum registry is `backend/seeds/curriculum.py`; the loader is
  `backend/app/services/curriculum/loaders.py`.
