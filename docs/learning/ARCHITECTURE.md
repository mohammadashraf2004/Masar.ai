# Learning paths — architecture

Masar builds a learner's roadmap from four answers, not from a fixed role track:

```
User
 |-- Level               where am I?
 |-- Fields / Interests  what interests me?
 |-- Career Goal         where do I want to go?
 `-- Declared Skills     what do I already know?  (a claim, never evidence)
          |
          v
   Roadmap Generator     deterministic and pure: path_generator.generate_plan
          |
          v
 Personalized Roadmap    stages -> courses, each required / completed / waived / optional
          |
          v
 Courses / Projects / Progress   derived from lessons the learner actually finished
```

Any combination is valid: *Intermediate + NLP + AI Engineer*, *Beginner + Computer Vision + ML Engineer*,
*Advanced + Speech + NLP + AI Engineer*. **AI Engineer is a career goal with several routes** (NLP, Vision,
Speech, Multimodal) — it is not the result of finishing other roles.

## Concepts that must not be confused

| Not the same as | Why it matters |
|---|---|
| **Skill != Tool** | `skills.kind` is `skill` (a capability: RAG, Embeddings) or `tool` (a named product: LangChain, Qdrant, FastAPI). Knowing LangChain is not knowing RAG, and knowing RAG is not knowing LangChain; no rule treats one as the other. Tools are still catalogue skills, so a course that *teaches* a tool needs that tool declared to be waived (see the rule below). The five tools are tagged by slug in migration `013` and in the seed. |
| **Skill != Course** | A skill is something a learner can know; a course is a catalogue facade over lessons. `course_skills` (teaches / assumes) is the only link, and a course usually teaches 3-9 skills. |
| **Declared skill != Completed course** | Declaring is a self-report stored in `learner_skills` (`known` + `self_declared`). It can make a course *Already know* (`waived`); it never marks anything `completed`, never counts as progress and never creates a completion record. Only finished lessons complete a course. |
| **Declared skill != claimed prerequisites** | Declaring RAG does not declare Embeddings, and it does not satisfy a course's prerequisites. Each prerequisite of a waived course is judged on its own: pulled in as required unless the learner declared it too. |
| **Career goal != a sum of old roles** | **AI Engineer** is a career goal in its own right, with several specialisation routes (NLP, Vision, Speech, Multimodal). It is not "the result of completing two or three of the other roles"; its template and required skills (evaluation, production deployment) are the ones every route shares. |
| **Multimodal != a required stage** | Multimodal is an *advanced specialisation* that builds on modality knowledge: at least one of NLP / Vision / Speech (two recommended), whether earned by finishing courses or declared. Below advanced it is advised against and the missing modality is added to the route - it is never blocked. |

### The "Already know" rule

A course is `waived` and shown as **Already know** **only when the learner declared every skill it teaches**
(all-of; a course that teaches no catalogued skill can never be waived by a declaration). Not a percentage, not any-of.

| Course teaches | Learner declares | Result |
|---|---|---|
| RAG, Embeddings, Vector Databases, Evaluation | RAG | **Not** known; the roadmap says "You already know 1 of 4 skills here" |
| RAG, Embeddings, Vector Databases, Evaluation | all four | Already know (still listed, in no denominator) |
| LangChain (tool) + LLMs + RAG + ... | every capability but not `langchain` | **Not** known - the tool is one of the skills it teaches |

Skills a learner gained by *finishing* courses never waive a third course; only a declaration does.

## Where things live

| Concern | Location |
|---|---|
| Schema | `backend/app/models/learning_path.py`, migrations `011`, `012`, `013` (learner skills, `skills.kind`), `014` (legal acceptance) |
| Path rules (pure, no DB) | `backend/app/services/learning/path_generator.py`, `prerequisites.py` |
| Reading the catalogue | `services/learning/catalog_service.py` (ORM → immutable `Catalog`) |
| Progress (derived, never stored) | `services/learning/progress_service.py` |
| Skill gaps and "Why this course?" (pure) | `services/learning/skill_gaps.py`; shaped for the API in `presenters.py` (`skill_gaps_out`, `_why_out`) |
| Profile / path persistence, logging, metrics | `services/learning/learning_service.py` |
| Admin writes (shared with the seed) | `services/learning/catalog_admin.py` |
| API | `controllers/learning_controller.py`, `controllers/admin_learning_controller.py` |
| Configuration data | `backend/seeds/seed_learning_paths.py` |
| Frontend | `frontend/src/components/learning/`, pages `learn/ explore/ paths/ courses/ onboarding/` |

**The backend owns the rules; the frontend only displays them.** Nothing in `frontend/` decides what a path
contains, which stage is current, or what a percentage is. Field names, career goals and every list come from the API.

## Data model

- `learning_levels`, `learning_fields`, `career_roles`, `skills` — vocabularies as rows, keyed by stable **slugs**,
  each with an English name and an optional `_ar` twin (the same Arabic-first convention as every content table).
- `courses` — a catalogue **facade** over exactly one existing content source (a `tool_courses` row or a
  `track_levels` row; a CHECK enforces it). Lessons are never copied, and a course is never duplicated per language,
  field or goal: `course_fields`, `course_roles`, `course_skills` (teaches / assumes) and `course_prerequisites` carry the
  many-to-many relationships.
- `path_stages` + `path_stage_courses` — reusable chapters (Foundations, RAG Engineering…) and what is in them.
- `path_templates` + `path_template_stages` — a career goal's ordered stage list; a stage tied to a field appears
  only when that field is in the learner's route. *"AI Engineer — Computer Vision"* is the AI Engineer template
  filtered to `computer-vision`; there is no separate list for it.
- `learning_profiles` — what a learner said (level, fields, goal). Every column is nullable; nothing is guessed.
- `learning_paths` — a saved path: a snapshot of stage/course **membership and order only**. Titles, translations and
  progress are resolved live. One `active` path per learner (partial unique index); rebuilding archives the old one.

## How a path is generated

`generate_plan(catalog, level, career_goal, fields, user_state)` — deterministic, no I/O:

1. **Fields.** A field below its `min_level` draws an advisory; a field short of its prerequisite *threshold*
   ("at least `k` of these fields") gets the missing prerequisite fields **added to the route** — never refused.
   Multimodal = `min_level advanced`, prerequisites NLP/Vision/Speech, min 1, recommended 2. It is data.
2. **Stages** come from the goal's template, filtered by the fields in the route.
3. **Courses** offered are *available* ones (active and with published lessons); the rest count as "upcoming".
4. **States.** `completed` / `waived`; a course *below* the learner's level is `optional` unless it teaches a skill the
   goal requires and the learner lacks; everything else `required`. Advanced learners are not forced through basics.
5. **Prerequisites** a required course needs are pulled in before it; a cycle never fails a generation — it is reported.

## Known skills: how a roadmap becomes personal

After the goal and field, onboarding asks **"Skills & Technologies I Know"**. The list comes from the backend
(`GET /learning/skills?career_goal=&level=&field=`): it is *derived* — generate the route for an empty learner, take what
its courses teach plus what the goal requires — so a new course or field shows its skills with no release. Each option
carries a `kind` (`skill` = a capability such as RAG, `tool` = a product such as LangChain), the field most of its
courses belong to (its section), and whether the goal requires it. Knowing a tool is **not** knowing the skill it is
used for; the picker says so, and no rule ever treats one as the other.

**Storage.** `learner_skills` (migration `013`): one row per learner and skill with a `status`
(`known | learning | mastered`) and a `source` (`self_declared | assessment | course_completion`). Onboarding writes
`known` + `self_declared`. That is a claim, not evidence, and is never presented as a qualification. Better evidence later
(practice, AI grading, an assessment) upgrades the *same row's* source and status without a schema change; editing the
self-declared list never removes or downgrades a row that came from better evidence. `learning_profiles.known_skill_slugs`
is deprecated: copied by 013, never read by application code (the roadmap and every response read `learner_skills`), and
only ever written as an empty list when a profile row is created (the column is NOT NULL). Kept so nothing is destroyed; a
later release can drop it once 013 has been applied everywhere.

**Rule (in `path_generator.py`).** A course is `waived` — shown to the learner as **"Already know"** — when they declared
*every skill it teaches* (all-of, never any-of; a course teaching nothing catalogued is never waived by a declaration).
Real courses teach 3-9 skills each (the union of their topic tags), so this is deliberately conservative: a partly-known
course stays on the roadmap and says what is already known ("You already know 2 of 6 skills here: ..."). Skills a learner
gained by *finishing* courses never waive a third course; only a declaration does.

**Prerequisites are never claimed on the learner's behalf.** Declaring RAG does not declare Embeddings. The prerequisites
of a course waived by declaration are judged on their own: pulled in as required unless the learner declared them too
(then they are not added). Waived courses stay in the path, visible, in no denominator, never counted twice.

**Fields.** A learner's declared skills also count when deciding which fields they have covered, so a Multimodal route does
not send someone back through NLP they told us they know. Multimodal itself is unchanged: advanced, never blocked, "at
least one modality required, two recommended" is data.

**Regeneration.** `PUT /learning/my-skills` saves the list and rebuilds the roadmap (`rebuild_path`): the old path is
archived (one active path - a partial unique index - history kept). Completion is derived from lessons, not stored on a
path, so completed courses stay completed and keep their progress wherever they now sit; only the future of the path
changes. The current/next course and the progress counts are recomputed by the server from the new roadmap, the field
route and its advisories (Multimodal's prerequisite information) are regenerated from the saved profile, and a reload
(`GET /learning/my-path`) reproduces the same roadmap. `skills` is a required key on that request: an empty list clears
the declaration, but a body that forgot the key is a 422, not "the learner knows nothing". Saving an unchanged list
still rebuilds (and archives): the result is identical, the only cost is one more history row.

**Roadmap payload.** `PathOut` adds `current_course` (a course already under way, else the first still to do),
`next_course`, `is_complete`, and `progress.path_completed / path_total / path_known`; each course carries
`known_skills`. All decided on the server; the frontend renders states and never derives them - in particular it never
infers "finished" from a missing current course: it reads `is_complete`.

## Skill gap analysis and "Why this course?"

A layer on top of the roadmap, not a second generator. The roadmap answers *what to learn, in what order*; this answers
*what am I missing?* and *why is this course here?* from the same data, so the two can never disagree.

```
Declared skills ┐
Level           │
Fields          ├──> Roadmap Generator ──> Personalized Roadmap ──┐
Career goal     ┘        (unchanged)                              │
                                                                  ├──> Skill Gap Analysis ──> gaps, per course "why"
Declared skills + progress on the roadmap's courses ──────────────┘    (services/learning/skill_gaps.py, pure)
```

`calculate_skill_gaps(catalog, plan, declared, completion)` and `explain_courses(...)` take the `Catalog` snapshot and the
`PathPlan` the generator produced. No database, no clock, no LLM, no second skill catalogue, no hard-coded skill lists.

**Which skills are relevant.** A skill taught by a roadmap course that is `required`, `completed` or `waived`, plus the skills the
career goal requires (`career_role_skills.is_required`) even when no published course teaches them yet - those are reported
with `course_count: 0`, never hidden and never invented (SQL, Statistics and Machine Learning are catalogue skills the
goal names but no published course teaches today). Courses that are `optional` (below the learner's level) contribute nothing:
that is all of the level-awareness, so a beginner and an advanced learner get different gaps from the roadmap stages
alone, with no second progression system. One exception: a field the generator *added as a prerequisite route*
(Multimodal's modality route) counts even when its courses are below the level, because that is exactly what is missing to
reach what the learner asked for. Nothing hard-codes "two modalities": the route is whatever the field's prerequisite
configuration produced.

**Status of a skill**

| Status | Meaning |
|---|---|
| `known` | The learner **declared** it. Nothing else makes a skill known: not finishing a course, not knowing a related skill, not knowing a prerequisite. |
| `partially_covered` | Not declared, but a roadmap course that teaches it is under way and unfinished. Skills are atomic in the catalogue, so this is the honest meaning of "partly": started, not known. |
| `missing` | Everything else. A skill taught only by a course the learner *finished* is still `missing` (`covered_by_completed: true` says so). |

**The skill-gap system does not infer undeclared skills from unrelated knowledge.** Declaring RAG does not make Embeddings known;
knowing a tool does not make the capability known (or the reverse); a prerequisite is never claimed.
**Completed courses and declared skills remain separate concepts**: completion is derived from lessons and only ever changes a
course's state; a declaration is a self-report and only ever changes a skill's status. Neither writes the other.

**Tools follow the existing semantics, unchanged.** A `tool`-kind skill is an ordinary skill: a course that teaches LangChain counts
LangChain among the skills it teaches, so it is one of the relevant skills, and (exactly as for "Already know") it must be
declared like any other. Tools are grouped apart and flagged `kind: tool`. *Follow-up proposal, not done here:* if tools
should later stop being required for "Already know" and for coverage, that is a single decision in
`skill_waived_course_ids` and in the relevance rule of `skill_gaps.py`, and it needs its own migration of expectations and tests.

**Immediate vs later.** `is_immediate` means a required course in the roadmap's *current stage* teaches the skill and the learner
lacks it. Every other gap sits later on the same roadmap and carries the earliest stage that teaches it (`stage`).

**Grouping.** By the field most of the roadmap courses teaching the skill belong to (ties broken by the field's configured
position), then "general" (no field-specific course), then tools last. The grouping the picker already uses; no new taxonomy.

**API.** `GET /learning/my-skill-gaps` (signed in; `my-*` like the rest of the learner's resources). `available: false` - not an
error - when there is no roadmap yet. Otherwise: `level`, `career_goal`, `fields` (the route), `current_stage`,
`summary {required, known, partial, missing, immediate, coverage_pct}`, flat `known` / `partial` / `missing` lists, and `groups`
(`key`, `kind` = field|general|tools, `field`, `total`, `known_count`, and the `skills` still to do). Each skill carries `status`,
`group`, `stage`, `is_goal_required`, `is_immediate`, `course_count`, `covered_by_completed`. `coverage_pct` is the declared share of
the relevant skills (null when nothing is relevant - not 0%).

**Why this course?** Every roadmap course carries `why`, structured facts and never sentences: `career_goal`, `fields` (the fields on
the route it belongs to), `stage`, `reasons`, `skills_taught`, `known_skills`, `skills_to_gain` (`known_skills` and `skills_to_gain`
partition `skills_taught`), `goal_skills`, `prerequisite_for`, and the counts. `current_course` and `next_course` carry the same block.
Reasons are codes, and a course can have several:

| Code | When |
|---|---|
| `career_requirement` | it teaches a skill the career goal requires |
| `field_requirement` | it belongs to a field on the learner's route |
| `stage_requirement` | it is a step of a stage of the goal's path (not for a course the generator pulled in as a prerequisite) |
| `skill_gap` | it is still to do and teaches a skill the learner has not declared |
| `prerequisite` | it was pulled in as one, or another course still to do needs it first |

The per-course coverage ("You already know 1 of 4 skills here") is `known_count` of `taught_count`, the same strict semantics as
"Already know": a course is waived only when `to_gain_count` would be 0.

**Frontend.** `SkillGapSummary` (counts and coverage), `SkillGapsPanel` (fetch + grouped list; `roadmap` and compact `profile`
variants), `WhyThisCourse` (collapsed by default), `SkillChips` (the one way a list of skills is drawn: course cards and the why
panel share it) and the `useSkillGaps` hook. They fetch and draw: relevance, status, grouping, coverage, reasons and counts are all
the backend's, and only the sentences around them are interface copy (`gap.*`, `why.*` in `lib/i18n.ts`, both languages; technical
terms stay English through the terminology dictionary). A fact the backend did not send is not drawn, and nothing is inferred in the
browser.

What "Why this course?" opens to, all from `why`: the career goal and the field(s) as a two-row fact list; one sentence per reason
code (the sentences live in `why.reason.*`); the coverage line built from `known_count` / `taught_count` / `to_gain_count`;
`known_skills` and `skills_to_gain` as chips; and `prerequisite_for` as links to the later courses that need this one first.

Where each surface puts it - the roadmap is the subject, everything else supports it:

| Surface | What it shows |
|---|---|
| Roadmap (`/learn`) | the summary card, then a compact coverage card (summary always visible; the per-field list of skills to gain is closed until asked for, so it never pushes the stages out of view), then the stages. A "Why this course?" toggle on each course still to do (required or optional; never on a finished or already-known one) |
| Dashboard card | goal, route, progress, current and next course, "N skills to gain" for the current course, and the next action. No explanation: that belongs to the roadmap |
| Home card | the same, one button |
| Profile -> My Skills | the declared list, what is being learned, and the coverage plus the first few skills still to gain - read-only; the declared list stays the only thing edited there |

Presentation rules the components share: eyebrow labels use `tracking-widest`, which `globals.css` cancels in Arabic (letter-spacing
pulls joined letters apart); a navigation is a `<Link className={buttonStyles(...)}>` and never a `<button>` inside an `<a>`; badges
mark status ("In progress", "Now") and everything else is plain secondary text; on a phone the status badge drops under the course
title and the why panel spans the row, so a long Arabic title keeps its width.

**Tools and skills, today.** A tool (LangChain, FastAPI, Qdrant...) is a `Skill` with `kind = tool`, taught by its tool course and
counted in coverage like any other skill; the analysis groups them under "Tools & frameworks". Whether tools should become a
separate concept is deliberately left open - nothing here changes the current behaviour. Declared skill != completed course still
holds: finishing a course never adds a skill (a gap can carry `covered_by_completed` as a hint, and stays a gap).

**Multimodal.** The analysis does not touch the route. Multimodal stays advanced-only and never blocked; when its modality
prerequisites are missing the route gains them (the advisories say so), and the skills of those prerequisite fields count as gaps
even when their courses are below the learner's level, because that is exactly what is missing.

**Regeneration is unchanged.** Editing skills still archives the roadmap and builds a new one; the analysis reads whatever roadmap is
saved, so it follows it. **Performance:** one catalogue snapshot per request (the same one the roadmap uses); the gap report is a few
passes over that snapshot with no per-course queries (a test asserts the query count does not grow with the roadmap and never exceeds
`GET /my-path`'s). No caching was added.

## Progress

Completion belongs to the learner and the course, not to a path. A course is done when every lesson and exercise
in it is marked complete (derived from `user_progress`, so it also works for track topics, whose `status` is never set).
A course finished once counts everywhere it belongs and never twice within one number. Optional and waived courses
are never in a denominator.

## API (existing conventions: `/api/v1`, `my-*` for the signed-in learner)

Public catalogue: `GET /learning/levels · fields · career-goals · courses[/{slug}] · paths[/{slug}]`.
Also public: `GET /learning/skills` (what to ask "do you know it?" about).
Signed in: `POST /learning/paths/generate` (preview), `GET|PUT /learning/my-profile`, `GET|PUT /learning/my-path`,
`GET|PUT /learning/my-skills`, `GET /learning/my-skill-gaps`, `GET /learning/my-progress`. Public legal endpoints: `GET /legal/versions`,
`GET /legal/{terms|privacy}?lang=en|ar`; `POST /auth/accept-legal` and `POST /auth/updates/{release_id}/acknowledge` (signed in). Admin (`require_admin`): `PUT /admin/learning/{levels|fields|career-goals|skills|courses|stages|templates}/{slug}`,
`GET /admin/learning/catalog`, `GET /admin/learning/health`. There is no DELETE — retire with `is_active: false`.

## Adding a specialisation (no code)

1. `PUT /admin/learning/fields/robotics` — name, `name_ar`, icon key, `min_level`, prerequisites.
2. `PUT /admin/learning/courses/<slug>` — point at existing content; tag `fields`, `roles`, `teaches`.
3. `PUT /admin/learning/stages/robotics-core` — the courses in it.
4. `PUT /admin/learning/templates/ai-engineer-path` — add `{stage: "robotics-core", field: "robotics"}` where it belongs.

Onboarding, Explore, the filters and the path pages pick it up with no release. (`tests/test_learning_admin.py::test_a_new_field_needs_no_code_change` does exactly this.)

## Existing learners

Migration `012` maps a learner with **exactly one** distinct active track enrolment to that career goal (by slug,
never by row id — `tool_courses.related_track_ids` holds raw ids and is not trusted). Level is left `NULL` (the legacy
`users.experience_level` defaults to *beginner* and the sign-up form pre-selects it, so it cannot be told from a choice),
fields are left empty, and `onboarding_completed_at` stays `NULL`, so the app asks them to finish onboarding. Old
enrolments, exams and certificates are untouched. `users.experience_level` is kept in step when the learner saves a level.

## Observability

Structured `learning event` log lines (and a `learning_events_total{event}` counter) for `learning_onboarding_started`
(first time a learner's answers are saved), `career_goal_selected`, `field_selected`, `known_skills_selected`,
`roadmap_generated`, `roadmap_updated`, and, for legal acceptance, `legal_terms_accepted` / `privacy_policy_accepted`.
They carry counts only, never the answers or the list of skills ticked. Generation also logs `known_skill_count`,
`required_course_count`, `waived_course_count`, `roadmap_generation_success` and feeds two histograms.
**Intentional follow-up, not emitted today:** `roadmap_course_started` and `roadmap_course_completed`. Both need a hook
in the lesson-progress endpoints (to notice the first lesson of, or the last lesson completing, a course that is on the
learner's roadmap), and lesson-progress behaviour was deliberately left untouched. Completion is still fully visible
through the derived progress counts; only the *event* is missing.

## Introducing a release: "What's New" and the first-roadmap introduction

An announcement is a **stable identifier** the server knows (`app/core/releases.py`), never a date or a counter, so it is shown
once, acknowledged, and a later release simply adds its own. The skill-gap release has two, one per audience:

| Identifier | Shown to | Where |
|---|---|---|
| `2026-09-skill-gap` ("What's New") | an account that **existed before** the release | the next time it reaches Home, the dashboard or the roadmap |
| `2026-09-skill-gap-intro` | an account **created after** it | once its roadmap exists ("Your skill gap is ready", with the real number) |

Who is "existing" is decided by data, not by comparing dates: registration writes the What's New row for a new account in the
same transaction as the account, and nothing was backfilled by the migration - so *no row* means "existed before". An account is
only ever asked about one at a time: the introduction is due once What's New is out of the way, and acknowledging What's New
also covers the introduction (`COVERS`), so an existing account is never introduced to the feature twice.

**Storage.** `user_update_acknowledgements (user_id, release_id, acknowledged_at)` with a unique `(user_id, release_id)`
(migration `015`). There was no existing per-account preferences mechanism (legal acceptance is a fixed pair of columns for two
documents), and a column per feature would need a migration per announcement; a row per acknowledgement needs none, and the
constraint is what makes acknowledging idempotent. The server, not the browser, holds it, so it survives another device,
cleared storage and signing out. `POST /auth/updates/{release_id}/acknowledge` needs authentication, accepts only identifiers in
`KNOWN_RELEASES` (unknown -> 404, so nothing can be pre-dismissed), is safe to repeat (a race resolves to one row), always acts
on the caller, and touches neither the roadmap nor the skills. It returns the account. `UserResponse.pending_updates` lists what
is still due (at most one); the client shows the first entry and never decides who is new.

**Frontend.** `UpdateGate` (mounted in `AppShell` beside `LegalGate`) renders `WhatsNewDialog` or `SkillGapIntroDialog` for the
first pending id, on Home, the dashboard and the roadmap only - never a lesson, an exam, sign-in or onboarding - and not while
the Terms are waiting to be accepted. Both are built on one `Modal` primitive (`role="dialog"`, accessible name and description,
focus in / trapped / restored, Escape, content that scrolls inside the panel). They are introductions only: no skill list, course
card or progress of their own - the button leads to the existing roadmap, and the number in the new-user dialog is the backend's
`GET /learning/my-skill-gaps` (partial + missing; a learner with nothing left is told so instead of "0 skills to gain"; the dialog
is skipped while there is no roadmap or nothing measured). An existing account without a roadmap is offered "Build My Roadmap"
instead of a skill-gap tour that could not exist.

**Acknowledging.** Every way out - the button, "Maybe later", the close button, Escape - acknowledges it. The id leaves the stored
account at once (the dialog closes and cannot reopen while the request is out; a second click does nothing) and the server's
answer then replaces the list. If the request fails nothing breaks and navigation still works; the server never heard, so it is
offered again at the next sign-in - not forever, and not in this session. A session that predates the field is refreshed once by
`LegalGate` (whose `/auth/me` answer carries it). No analytics events were added.

To announce something new: add an identifier (and, if it supersedes another, a `COVERS` entry) to `app/core/releases.py`,
teach `pending_updates` its order, and draw it in `UpdateGate`.

## Terms and Privacy

`app/core/legal.py` holds `TERMS_VERSION` and `PRIVACY_VERSION`; `app/content/legal_documents.py` holds the text (English
and Arabic) beside them, and `GET /legal/{terms|privacy}?lang=` serves both, so the site never carries a copy of the
wording or the version. Registration requires `accept_terms` and `accept_privacy` (strict booleans) and writes
`terms_version / terms_accepted_at / privacy_version / privacy_accepted_at` in the same INSERT as the account; the
versions are the server's, a client-sent version or timestamp is ignored, and the acceptance is written in that same
transaction as the account (nothing is created when either box is missing). `POST /auth/accept-legal` is idempotent: an
account already on the current versions keeps its original acceptance time. `users.requires_legal_acceptance` is true until an account
has accepted the versions in force; existing accounts are *not* backfilled (they never saw the documents) and are asked at
next use through `POST /auth/accept-legal`. To change a document: edit the text and bump the version.
**The wording is a working draft and has not been reviewed by a lawyer.**

## Running the tests

Backend needs a disposable Postgres whose name contains `test` (see `backend/tests/conftest.py`):
`DATABASE_URL=postgresql://…/ai_career_platform_test pytest tests/test_learning_*.py`.
Frontend: `cd frontend && npm test` (Vitest + Testing Library). jsdom has no layout engine, so real RTL and responsive
rendering are checked in a browser against the running app.
