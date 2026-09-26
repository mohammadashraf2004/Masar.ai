# COURSE-012 — Agentic AI Systems Engineering

Finalized Masar curriculum export from **BOOK-012 — AI Agents in Action**.

- **Course ID:** COURSE-012
- **Modules:** 11
- **Lessons:** 91
- **Declared guided time:** 94h 40m
- **Source review:** 11/11 chapters + Appendix A + Appendix B
- **Approval:** Not explicitly approved
- **Frozen IDs:** M012-01..M012-11 / L012-001..L012-091
- **Manual source figures:** 39 required + 13 optional

## Folder contract

Each module folder contains:

- `module_manifest.json`
- `module_project.py`
- one Python seed file per lesson

Every lesson seed contains:

- `COURSE_ID` / `MODULE_ID` / `LESSON_ID`
- `LESSON_META`
- source mapping
- original Masar Markdown instructional content
- two exercises
- a three-question quiz with explanations
- manual figure placeholders where relevant
- the module project on the final lesson

Additional files include:

- `course_manifest.json`
- `assets_manifest.json`
- `course_data.py`
- `seed_course_012.py`
- `validate_course.py`
- setup/reference docs from Appendices A/B
- `capstone/`
- `FINALIZATION_AUDIT.md`
- `FOLDER_TREE.txt`

## Important curriculum boundaries

- Generic RAG engineering remains owned by COURSE-009.
- Generic FastAPI/service engineering remains owned by COURSE-010.
- Generic cloud/CI/CD remains owned by COURSE-011.
- Deeper multi-agent systems are resolved by M012-04 + M012-08.
- Deep reasoning-model **training/engineering** remains an open future gap.
- Private chain-of-thought is not required or stored. Use observable plans, selected actions, tool traces, evaluator outputs, and state transitions.

## MCP modernization

The source contains legacy SSE-era remote MCP examples. COURSE-012 uses:

- **STDIO** for local subprocess MCP
- **Streamable HTTP** as the primary remote transport
- legacy HTTP+SSE only as compatibility awareness

## Source figures

Source-book images are intentionally **not bundled**. Add only the figures listed in `assets_manifest.json` using the exact destination paths.

## Integration

The demonstrated Masar data hierarchy is:

`CareerTrack → TrackLevel → Topic → Lesson / Exercise / Quiz / Project`

This export is repository-neutral. `seed_course_012.py` performs a dry run only until you map it to the real Masar ORM/repository contract. It requires an explicit `MASAR_COURSE012_TRACK_SLUG` because COURSE-012 is reusable across multiple tracks and must not be silently duplicated.

## Validation

Run:

```bash
python validate_course.py
```

The validator checks:

- module count
- lesson count
- Python syntax
- contiguous frozen lesson IDs
- unique lesson IDs/slugs
- two exercises per lesson
- three quiz questions per lesson
- module-project count
- required/optional figure counts
- setup/capstone files
- loader importability

### Duration note

The previously established curriculum notes contained arithmetic inconsistencies between some individual lesson/project estimates and module/course totals. This export preserves both the frozen course-level **94h40m** estimate and the authored per-lesson estimates, and reports the discrepancy instead of silently rewriting the curriculum.
