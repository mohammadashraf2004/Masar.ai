# Exercise grading audit — 2026-10-10

Branch `exercise/grading-audit-2026-10-10`, built on `origin/release/2026-10-10` (bd66d41).
Not pushed, not deployed. Learner execution in production stays disabled until the
production-host gVisor checks in `deploy/exercise-release-checklist.md` pass.

## 1. What was audited

The full path: course definitions (`backend/courses`, `curriculum/guided`) → loader and
importer → `exercises` rows → `/practice/exercises/*` API → graders (Python, SQL, text)
→ execution (driver + project runner) → results → `CodeCell` / `AnswerChat` → progress.

Catalogue at the time of the audit: 886 exercises — 205 Python, 10 SQL, 24 text/config
(all fill-in-the-blank), and 647 written exercises graded by the AI evaluator.

Every defect below was reproduced against the real runner harness before it was fixed.

## 2. Confirmed defects and root causes

| # | Defect | Root cause |
|---|--------|-----------|
| 1 | Typing a blank's computed result passes: **183 blanks in 98 exercises** (e.g. `0.1349` instead of `round(partial / full, 4)`) | Behavioural checks only observed a value that is computed once from fixed data |
| 2 | Divide exercise: a wrong zero check gave only "runtime error", not "does not handle a zero divisor" | Hidden checks were appended to the learner's file, so a crash in the demo line stopped them |
| 3 | Divide exercise: a hardcoded `{"result": 2.5}` was blamed on blank 2 | One check mixed blank 2 and blank 3 behaviour |
| 4 | Hidden test inputs leaked into the learner's console (`print` inside a function) | Check-phase output went to the same stdout |
| 5 | A correct answer failed when the learner named a variable `sorted`, `sum`, `max`, `list`… | Checks resolved builtins in the learner's namespace |
| 6 | 425 check messages in 168 exercises quote the exact answer, shown on the first wrong attempt | Content style, no disclosure policy |
| 7 | Source-policy bypasses: `__builtins__.open(...)`, `__loader__`, `g = getattr`, generator frames | AST rules checked only direct calls and private attributes |
| 8 | Memory exhaustion reported as "runtime error"; SQL typo `SELEC` as "not allowed"; SQL "no such column" as syntax error | Status mapping by message, not by kind |
| 9 | A malformed test (unknown type, missing field) failed every learner as "incorrect" | No configuration validation at grade time |
| 10 | `grading_error` (broken exercise) counted toward unlocking the solution and showed as a wrong answer | Only `execution_error` was treated as ungraded |
| 11 | Written exercises could be marked complete with a direct POST, without a passing answer (feeds the course-completion credential) | Progress routes trusted the client |
| 12 | Concurrent completions in one topic could lose an id or create a duplicate progress row | Read-modify-write of a JSON list, no lock, no unique key |
| 13 | A code-exercise pass did not refresh `ToolEnrollment.progress_pct` / completion record | Only the generic progress route recomputed it |
| 14 | Python 3.11 (production) turns a 5,000-term expression into a parser `RecursionError` → HTTP 500 | Learner code parsed without a depth guard |
| 15 | SQL feedback and resource messages were English in Arabic mode; three runner outage messages had no Arabic | Raw messages passed through |
| 16 | Equivalent float answers could fail (exact `==`); SQL unordered comparison sorted rows by `repr` | No tolerance |
| 17 | No way to require an expected exception; the two runners reported raised calls differently | Missing feature, diverging local harness |
| 18 | Frontend: "Correct" stayed after editing the code; reset kept old results; outages looked like wrong answers; HTTP errors shown as "Request failed with status code 429" | Result not tied to the code; error mapping missing |
| 19 | `PythonGrader()` defaulted to a host-subprocess runner with no production guard | Unsafe default |
| 20 | Written exercises had no reference/example answer (0 of 647) | Content gap |

## 3. What changed

**Execution (the main design change).** `isolated_python_runner.py` now sends two files to
the project runner: the learner's code unchanged (`exercise.py`, so tracebacks keep the
learner's own line numbers) and a trusted driver (`masar_check.py`). The driver runs the
setup and the learner's file in their own namespace, then evaluates the hidden checks:
after a crash too, with all output discarded, with real builtins, and with results the
learner's code cannot name. `LocalPythonRunner` (dev/tests) now uses the same driver and
harness and refuses to run in production. Fixes 2, 4, 5, 17, 19 and part of 8.

**Grading** (`code_grading/grader.py`, `blanks.py`, `sql_grader.py`):
- every required check is evaluated; new `partial` status; first failing check is reported;
- a crash still reports the check that explains it, plus "your program also stopped with X on line N";
- float tolerance (rel 1e-9, abs 1e-12) in value, expression, return and SQL row comparisons;
- `raises` on a check expects an exception type;
- configuration validation up front → `grading_error` ("not counted"), never "incorrect";
- `blank_computed` guard, generated at import for blanks whose answer is a computation:
  fails only when the confirmed slot holds a constant; it gates a pass but is not counted
  as a check;
- static blanks accept keyword arguments in any order;
- SQL: write vs typo vs query error vs timeout classified; localized feedback.

**Feedback policy** (`code_exercises.withhold_answers`): a message that quotes code from the
solution (not in the starter) is replaced by "Blank N does not give the required result yet…"
until the learner's second *different* wrong answer; `feedback.withheld` tells the UI.

**Source policy** (`python_runner.py`): dunder names, frame attributes, `ctypeslib`, and any
reference to a dangerous builtin unless it is provably a local name; one safe parser with a
depth limit for all learner code.

**Completion** (`services/exercise_progress.py`): written exercises complete when the
evaluator accepts the answer (recorded server-side); the progress routes refuse an exercise
id without that verdict (`409 ANSWER_NOT_ACCEPTED_YET`, after the access check); completions
are serialized per learner and topic with a Postgres advisory lock; a code pass refreshes the
tool-course figures. Run never completes anything.

**Divide-tool exercise** (`guided/c015.py`): six checks, one blank each, covering 10/4,
negatives, fractions, zero dividend, zero divisor, unknown tool; non-revealing messages.

**Frontend** (`CodeCell`, `useExerciseRun`, `AnswerChat`, i18n): Partly correct, Not graded
(amber, "attempt not counted"), memory/output limits, stale-result note, reset clears results,
localized request errors, traceback under "Technical details", example-answer panel.

**Example answers** (user request): migration `040_exercise_example_answers` adds
`exercises.example_answer` / `example_answer_ar`; definitions in
`curriculum/examples/cNNN*.py`; shown after the learner's first evaluated answer
(`GET /practice/exercises/{id}/example`, 403 before); used as the evaluator's reference.
**Written for COURSE-001 to COURSE-007: 134 of 647.** Continue with
`docs/written-example-answers-guide.md`.

## 4. Tests

New: `test_grading_rules.py`, `test_divide_tool_exercise.py` (every case in the brief),
`test_runner_source_policy.py`, `test_exercise_grading_flow.py` (API flows, concurrency,
written completion), `test_written_example_answers.py`, `test_migration_040.py`,
`AnswerChat.example.test.tsx`, new cases in `CodeCellGuided.test.tsx`.
Updated for intended behaviour changes: SQL multiple statements is `forbidden_operation`;
outage feedback adds "not counted"; `3 + 4 + 5` for `sum(scores)` is now hardcoding;
tests that completed written exercises now record an accepted answer first; 038 tests
point at the new head.

Results on this branch (2026-10-10):

| Check | Result |
|-------|--------|
| Backend full suite (CI-equivalent image, Postgres 16) | 2,832 passed, 0 failed, 9 skipped (pre-existing), 1 xfailed |
| Frontend lint / typecheck | clean |
| Frontend vitest | 1,488 / 1,488 |
| Frontend production build | succeeded |
| Every guided solution through the new driver | passes (`test_guided_exercises.py`) |

Not done this session: a real-browser (Playwright) run of the new cell states, and real
written-answer grading against a live LLM provider (the only local key is revoked); the
written flow was tested with a stubbed evaluator.

Curriculum-wide probe (`blank` replaced by its computed constant): **183 → 5** exploitable
blanks; the remaining 5 (COURSE-003.M07.L01.EX04, COURSE-014.M13.L01.EX01) are arithmetic
answers by design (`3072 * 512 + 512`), where typing the number is legitimate.

## 5. Content issues left for separate correction

- 425 check messages in 168 exercises quote the answer. They are now withheld on the first
  wrong attempt, but rewriting them non-revealing (as done for the divide exercise) is better.
- The two arithmetic exercises above accept a typed number.
- 513 written exercises (COURSE-008 to COURSE-018) still have no example answer.
- The probe could not instrument blank 3 of COURSE-007.M03.L02.EX04 and COURSE-010.M01.L11.EX09.

## 6. Security status and production readiness

- The boundary for learner Python is the isolated project runner; production refuses the
  local backend, requires `runsc`, attests gVisor at startup and every 60 s, and defaults to
  execution disabled (unchanged, verified in code and tests).
- The new driver and source rules are defense in depth inside that boundary.
- SQL still runs in-process on SQLite (`:memory:`, query-only, authorizer, VM-step deadline,
  heap and length limits, 500-row cap). An isolated SQL runner exists uncommitted in
  `D:/2helny-launch`; it is not integrated here.
- **Not production ready.** The production host has never been inspected from this
  workstation (no SSH/SSM); the gVisor runbook has not been executed. Do not enable learner
  execution until it has.

## 7. Deployment notes

- New migration head is `040_exercise_example_answers` (revises 038). A concurrent,
  uncommitted `039_additional_credit_packs.py` exists in the main worktree: whichever lands
  second must re-point its `down_revision`.
- Re-import the curriculum after deploying: the guards, the new divide checks and the
  example answers live in the imported `grading_tests` / exercise rows.
- Merge overlap: the uncommitted phase-2 work in `D:/2helny-exercise-phase2` (SQL/text
  "blanks remaining", Arabic dual forms), the SQL runner in `D:/2helny-launch`, and the
  uncommitted bare-`___` SQL blank format in the main worktree all touch the same grader,
  controller and CodeCell files. This branch keeps the `/* blank:N */` SQL markers.
