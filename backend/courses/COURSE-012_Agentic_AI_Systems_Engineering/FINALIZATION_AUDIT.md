# COURSE-012 Finalization Audit

## Package checks

- Module folders: **11 — PASS**
- Lesson seed files: **91 — PASS**
- Frozen IDs: **L012-001..L012-091 — PASS**
- Unique slugs: **PASS**
- Python lesson syntax: **PASS**
- Exercises: **2 per lesson — PASS**
- Quiz: **3 questions with explanations per lesson — PASS**
- Module projects: **11 — PASS**
- Required manual figure references: **39 — PASS**
- Optional manual figure references: **13 — PASS**
- Setup/reference layer: **Appendix A + Appendix B incorporated — PASS**
- Course capstone: **present — PASS**
- Course loader smoke test: **PASS**
- Repository-specific DB insertion: **NOT VERIFIED / intentionally not attempted**
- Frontend rendering: **NOT VERIFIED**
- External provider/tool execution: **NOT VERIFIED**
- Production deployment: **NOT VERIFIED**

## Duration audit

- Frozen course-level guided estimate: **94h 40m / 5680 min**
- Sum of authored individual lesson estimates: **5280 min**
- Status: **WARN — historical curriculum arithmetic is inconsistent.**

The export preserves the frozen course-level duration and the authored per-lesson estimates rather than silently rewriting either.

## Validator output

```text
COURSE-012 validation
modules=11
lessons=91
module_projects=11
required_figures=39
optional_figures=13
lesson_minutes=5280
WARN: Duration warning: individual lesson estimates total 5280 min, while the frozen course-level estimate is 5680 min. See course_manifest.json duration_audit.
PASS
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.L2TH2Y5coc/artifact_tool_v2-2.8.22/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.L2TH2Y5coc/artifact_tool_v2-2.8.22/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.L2TH2Y5coc/artifact_tool_v2-2.8.22/artifact_tool/spreadsheet_warmup.py", line 720, in _warm_feature_flows
  File "/tmp/tmp.L2TH2Y5coc/artifact_tool_v2-2.8.22/artifact_tool/spreadsheet_warmup.py", line 704, in _warm_collaboration_flows
  File "/tmp/tmp.L2TH2Y5coc/artifact_tool_v2-2.8.22/artifact_tool/generated/interface/models.py", line 32317, in hydrate_crdt_from_proto
  File "/tmp/tmp.L2TH2Y5coc/artifact_tool_v2-2.8.22/artifact_tool/rpc/remote.py", line 749, in __call__
  File "/tmp/tmp.L2TH2Y5coc/artifact_tool_v2-2.8.22/artifact_tool/rpc/client.py", line 150, in call
artifact_tool.rpc.client.RemoteError: hydrateCrdtFromProto requires an empty collaborative document.
```
