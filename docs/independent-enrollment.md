# Independent course enrollment, readiness and recommendations

A learner picks a **course**, not a track. Tracks are recommended roadmaps that
sit beside the catalogue; nothing here requires choosing one.

```
Course catalogue -> open any course -> readiness (advice) -> enroll -> learn
Career roadmap   -> an ordered list of the same canonical courses (guidance, never a gate)
```

## Model

| Concept | Where | Notes |
| --- | --- | --- |
| Course | `courses` | One canonical row per course. Its content (modules, lessons, exercises, quizzes, projects) is imported from `backend/courses/` by `seeds/import_courses.py`. |
| Track / roadmap | `career_roles` + `course_roles` | Many-to-many. `course_roles` carries the role of the course in that roadmap (`core`, `supporting`, `optional`); order lives in the path template. A course is never copied per track. |
| Prerequisites | `course_prerequisites` | Typed (`recommended` / `required`), read from each course manifest (its `required` list is `required`, the rest `recommended`). Nothing blocks enrollment: `required` only orders a roadmap and weighs most in the readiness advice. |
| Enrollment | `course_enrollments` | One row per learner and course; access (`status`, `source`) and lifecycle (`learning_status`: enrolled, in_progress, completed, paused). No track, goal or path column. Progress is derived from `user_progress`, never stored. |
| Learner skill levels | derived | Per skill: `not_assessed`, `beginner`, `intermediate`, `advanced`, computed from finished courses, quiz results, readiness checks and, weakest, the onboarding answers. Not one global level. |
| Readiness check | `readiness_assessments` | 5-10 real questions taken from a course's prerequisite courses. Graded on the server; the answer key never leaves it. |

Migration `018_independent_enrollment` adds all of this and backfills an
enrollment for every learner who was already working in a course. Nothing is
reset.

## API (all under `/api/v1/learning`)

```
GET   /courses                          the catalogue; every filter optional (level|difficulty, field|category, career_goal, skill, enrolled, q)
GET   /courses/{slug}                   one course: structure, prerequisites, roadmaps it appears in (no lesson text)
POST  /courses/{slug}/enroll            idempotent; refuses only an unpurchased paid course; returns enrollment + readiness + how to start
PATCH /courses/{slug}/enrollment        pause / resume
GET   /courses/{slug}/progress          per-module progress
GET   /courses/{slug}/readiness         strengths, gaps, what to review first
GET   /courses/{slug}/readiness-assessment    the questions
POST  /courses/{slug}/readiness-assessment    answers only -> graded on the server
GET   /my-courses                       the learner's enrollments
GET   /recommendations                  continue / recommended next / build foundations / completed, each with a reason
GET   /tracks, /tracks/{slug}, /tracks/{slug}/courses    roadmaps
GET   /my-skill-levels                  per-skill proficiency
```

Readiness states (`ready`, `mostly_ready`, `needs_foundation`, `not_assessed`)
are separate from a course's difficulty. They are advice: "Start anyway" is
always available, and the score is a summary the state does not rest on alone.

Payments are unchanged: a paid course still needs a purchase (or an admin
grant), decided by `access_service` on the server. A free enrollment never
opens a course that is later made paid.

## Recommendations

Deterministic and explainable (`services/learning/recommendations.py`). Each item
carries a `reason_code` plus the names needed to write the sentence; the client
localises it and falls back to the server's English `reason` for a code it does
not know. A completed course is never recommended as next. A career goal, if the
learner has one, sharpens the order; it never controls access.

## Frontend

| Route | What |
| --- | --- |
| `/learn` | Your learning, recommended for you, build your foundations, the whole catalogue (difficulty and category filters), career roadmaps |
| `/learn/masar` | The personalised path (the earlier "Your Masar" page) |
| `/learn/my-courses` | Enrolled courses |
| `/courses/{slug}` | A course on its own: outline, readiness, quick check, enroll |
| `/courses/{slug}/learn` | The lessons of a curriculum course |
| `/roadmaps/{slug}` | A career roadmap |
| `/onboarding/quick` | Three questions (programming, AI, interests); no career track |

## Not built yet

* Challenge-to-skip (test out of a module). The pieces it needs exist (server-side
  grading, per-module status) but no rule yet says what passing a module test means
  for completion or certification, and exams and payments must stay intact.
* No course is outline-only any more: all sixteen `COURSE-0xx` folders carry lesson
  text (COURSE-006 included). The importer still supports an outline-only layout and
  would import such a course as a non-startable shell.
* Nothing hard-blocks on a prerequisite. A manifest's `required` list makes a
  prerequisite `required` (it orders roadmaps and weighs most in readiness); everything
  else is `recommended`. If Masar ever wants a hard block it needs an explicit business rule.
