# Masar مسار

An Arabic-first AI career platform — *masar* (مسار) is Arabic for “track”.
Structured career tracks, standalone tool/framework courses (LangChain, LangGraph, Qdrant, ...), an AI mentor, conversational AI grading for exercises and quizzes, and progress tracking.

---

## Quick Start (Docker — recommended)

This is the only setup path you need. No local Python/Node/Postgres install required — just Docker Desktop.

```bash
git clone <repo-url>
cd 2helny

# 1. Environment files
cp backend/.env.example backend/.env
cp frontend/.env.local.example frontend/.env.local
```

Open `backend/.env` and set at least one AI API key — `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` — matching `GENERATION_BACKEND` (`openai` or `anthropic`). Everything else in `.env.example` has a working default for local dev.

```bash
# 2. Build and start the whole stack (Postgres + FastAPI + Next.js)
docker compose up -d --build

# 3. Apply database migrations
docker compose exec api alembic upgrade head

# 4. Seed content (run in this order — later scripts depend on earlier ones)
docker compose exec api python seed.py                         # 5 career tracks (shells)
docker compose exec api python seeds/seed_track_ai_developer.py # AI Developer track content
docker compose exec api python seeds/seed_tool_courses.py       # 16 tool/framework course shells
docker compose exec api python seeds/seed_tool_langchain.py
docker compose exec api python seeds/seed_tool_langgraph.py
docker compose exec api python seeds/seed_tool_llamaindex.py
docker compose exec api python seeds/seed_tool_qdrant.py
docker compose exec api python seeds/seed_tool_fastapi.py
docker compose exec api python seeds/seed_arabic_first_demo.py   # Arabic-first reference lesson
```

All seed scripts are idempotent — safe to re-run any time (e.g. after adding more content to a seed file).

**You're up:**

| | URL |
|---|---|
| App | http://localhost:3000 |
| API | http://localhost:8000 |
| Swagger docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

Register a new account in the app to get started — new accounts receive starter credits automatically (used for AI mentor chat and AI-graded exercises/quizzes).

### Everyday use

```bash
docker compose up -d          # start (no rebuild)
docker compose logs -f api    # tail backend logs
docker compose logs -f frontend
docker compose down           # stop (keeps the postgres_data volume)
```

The backend runs with `--reload` in local dev (auto-loaded via `docker-compose.override.yml`), and `backend/` is volume-mounted — edit backend code and it picks it up live, no rebuild needed. The frontend does **not** hot-reload (it always runs the production standalone build) — after a frontend change, run `docker compose up -d --build frontend`.

---

## Running the Backend Without Docker

Useful if Docker itself won't build on your machine (e.g. a broken WSL2/Docker Desktop integration), or you just prefer a native workflow. The frontend still expects the API at `http://localhost:8000`, so this can run standalone or alongside a Dockerized frontend.

**Prerequisites:** Python 3.11+, and a reachable Postgres. Easiest way to get the latter without installing Postgres yourself — start only the `db` service from Docker:

```bash
docker compose up -d db
```

(This pulls one small, unrelated image — `pgvector/pgvector:pg16` — so it works independently of whatever is breaking the `api`/`frontend` builds.) Alternatively, point `DATABASE_URL` in `backend/.env` at any Postgres 15+ instance you already have.

```bash
cd backend
python -m venv venv

# Linux / Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env   # set your AI API key, same as the Docker path
```

`alembic.ini`'s default `DATABASE_URL` (`localhost:5432`) already matches the `docker compose up -d db` setup above, so no edits needed there.

```bash
alembic upgrade head

# Seed content — same scripts and order as the Docker path, just without
# `docker compose exec api` in front:
python seed.py
python seeds/seed_track_ai_developer.py
python seeds/seed_tool_courses.py
python seeds/seed_tool_langchain.py
python seeds/seed_tool_langgraph.py
python seeds/seed_tool_llamaindex.py
python seeds/seed_tool_qdrant.py
python seeds/seed_tool_fastapi.py
python seeds/seed_arabic_first_demo.py

uvicorn app.main:app --reload --port 8000
```

Running tests natively is the same idea — `pip install -r requirements-dev.txt && python -m pytest -q`, no `docker compose exec` needed since you're already in the venv.

---

## Environment Variables

Full reference lives in `backend/.env.example` and `frontend/.env.local.example`. The ones that actually matter to get running:

| Variable | Required? | Notes |
|---|---|---|
| `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` | Yes (at least one) | Powers the AI mentor, exercise/quiz grading, and content generation. |
| `GENERATION_BACKEND` | Yes | `"openai"` or `"anthropic"` — picks which key above is used. |
| `GENERATION_MODEL_ID` | Yes | e.g. `gpt-4o-mini` (cheap, default) or `claude-sonnet-4-20250514`. |
| `SECRET_KEY` | Prod only | JWT signing key. The app refuses to boot with `APP_ENV=production` and a weak/default key — fine to leave as-is for local dev. |
| `DATABASE_URL` | No | Ignored under Docker (`docker-compose.yml` always points it at the `db` service). Only matters running natively. |
| `RESEND_API_KEY` | No | Email sending is best-effort — silently skipped if unset. |
| `REDIS_URL` | **Prod only** | Shared rate-limit/lockout storage. Without it, each of Gunicorn's 4 workers keeps its own counters and every limit is ~4x looser than documented. |
| `PAYMOB_*` | No | Only needed to test real payment flows. |

> **Before deploying, read [SECURITY.md](SECURITY.md)** — it lists the
> configuration that has to be set outside the application (`REDIS_URL`,
> `SECRET_KEY`, database credentials and TLS, ingress `X-Forwarded-For`
> handling, log shipping, backups) and what remains a known risk.

---

## Project Structure

```text
2helny/
│
├── backend/
│   ├── app/
│   │   ├── core/              # Config & security
│   │   ├── db/                # Database connection
│   │   ├── models/             # SQLAlchemy models
│   │   ├── views/              # Pydantic schemas
│   │   ├── controllers/        # FastAPI routers
│   │   └── services/           # Business logic & AI services (mentor, wallet, LLM providers)
│   │
│   ├── alembic/                # Migrations (source of truth for schema)
│   ├── seeds/                  # Content seed scripts (career tracks, tool courses)
│   │   └── track_ai_developer/ # AI Developer track content, one file per level
│   ├── tests/
│   ├── requirements.txt
│   ├── requirements-dev.txt    # pytest etc. -- not installed in the running container image
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js App Router pages
│   │   ├── components/          # Shared UI components
│   │   ├── hooks/
│   │   ├── lib/                 # API client & utilities
│   │   └── types/
│   ├── package.json
│   ├── Dockerfile
│   └── .env.local.example
│
├── docker-compose.yml           # Base stack (Postgres + API + frontend)
├── docker-compose.override.yml  # Auto-loaded for local dev (hot-reload backend)
└── README.md
```

---

## Tech Stack

**Backend:** FastAPI · SQLAlchemy 2.0 · Alembic · PostgreSQL (pgvector) · JWT auth · Gunicorn/Uvicorn

**Frontend:** Next.js 14 (App Router) · TypeScript · Tailwind CSS · Zustand · Prism.js (syntax highlighting) · react-simple-code-editor (in-browser code exercises)

**AI:** OpenAI (`gpt-4o-mini` by default) or Anthropic Claude — swappable via `GENERATION_BACKEND`

---

## Core Features

* Career tracks (multi-level, structured curriculum) and standalone tool/framework courses (LangChain, LangGraph, LlamaIndex, Qdrant, FastAPI, ...) — pick either or both
* **Arabic-first learning** — every course can be read in Arabic or English, with AI/ML terminology kept in English throughout, plus Industry Mode, clickable term definitions, bilingual search and English-vocabulary progress (see below)
* AI mentor chat
* Conversational AI grading for exercises and quizzes (theory questions graded by an LLM interviewer; coding exercises use a DataCamp-style in-browser editor)
* Wallet/credits system gating AI features, with starter credits on signup
* Progress tracking, quiz attempts, project submissions

---

## Arabic-First Learning

Courses are read in Arabic by default, but the AI/ML terminology stays in English — the words a student will meet on GitHub, in papers, and in job descriptions. The philosophy and the authoring rules are in
**[docs/content/ARABIC_FIRST_GUIDELINES.md](docs/content/ARABIC_FIRST_GUIDELINES.md)**; `seeds/seed_arabic_first_demo.py` publishes a worked reference lesson.

What ships with it:

| | |
|---|---|
| **Language control** (page header) | Explanations in العربية or English; Industry Mode ladder (Arabic First → Industry Mode → English Technical). Code never changes in any setting. |
| **Terminology dictionary** | `frontend/src/content/terminology/ai-terms.ts` — one file, one source of truth. Run `npm run terminology:export` after editing it to regenerate `backend/app/content/ai_terms.json`. |
| **First-mention rule** | Lesson prose renders a term's first appearance as `Embeddings (التضمينات)`, later ones as a clickable `Embeddings`. Code blocks are never annotated. |
| **Bilingual search** | `GET /api/v1/search/?q=` — "Embeddings", "embedding" and "التضمينات" all reach the same course. One course per subject, never one per language. |
| **Vocabulary progress** | `/glossary` and the dashboard widget. A term is *encountered* when read, *learned* when answered correctly. |
| **AI tutor** | Mentor chat, challenge hints and answer grading all apply the same policy, built from the same dictionary (`app/services/language/language_policy.py`). |
| **Quiz quality** | `seeds/fix_quiz_answer_bias.py` spreads MCQ answers across option positions (option text untouched, answer key remapped, idempotent) and reports questions where the correct option is conspicuously the longest. `app/services/content/quiz_lint.py` is the same check as a library. |
| **Content lint** | `POST /api/v1/terminology/lint` warns an author who wrote «إعادة الترتيب» where the lesson should teach `Reranking (إعادة الترتيب)`. Advisory — it never blocks publishing. |

Existing English-only courses keep working untouched: every Arabic column is nullable, and a lesson with no Arabic version renders the English original with a note saying so.

---

## Monitoring (Prometheus + Grafana)

Both come up with the rest of the stack — `docker compose up -d` — and are
bound to **127.0.0.1 only**, because Grafana ships with default credentials
and Prometheus has no auth at all. On a server, reach them over an SSH
tunnel or put them behind your own authenticating proxy; do not publish
these ports.

| | URL | Login |
|---|---|---|
| Grafana | http://localhost:3001 | `GRAFANA_USER` / `GRAFANA_PASSWORD` (default `admin`/`admin`) |
| Prometheus | http://localhost:9090 | none — that is why it is localhost-only |

The **CareerTrack — Platform Overview** dashboard is provisioned on first
boot (folder *CareerTrack*), along with the Prometheus datasource. Rows:
health, traffic, latency, AI spend, users, infrastructure.

### What is measured

`/metrics` on the API is bearer-token gated (`METRICS_TOKEN`) — it is served
on the same published port as the app, and the payload maps every route, its
latency and error rate, plus credit burn and auth-failure counts. A wrong
token gets a 404. The app refuses to boot in production with
`METRICS_ENABLED=true` and no token set.

| Metric | Why it is there |
|---|---|
| `http_requests_total`, `http_request_duration_seconds` | RED metrics, labelled by route *template* — `/api/v1/tracks/{slug}`, never the raw path |
| `llm_requests_total`, `llm_request_duration_seconds`, `llm_tokens_total` | What the AI features cost and how long students wait. Token counts come from the provider's own usage field |
| `credits_spent_total`, `credit_denials_total` | Where the wallet goes, and who is hitting the paywall mid-task |
| `auth_events_total`, `payments_total`, `rate_limit_hits_total` | Signups, logins, confirmed payments, limiter activity |
| `pg_*`, `redis_*` | Connection saturation and Redis memory — the two infra failures that look like an application hang |

Nine alert rules ship in `monitoring/prometheus/alerts.yml` (service down,
5xx rate, latency, LLM error rate, credit denials, login-failure spikes,
Postgres connections, Redis memory). They fire in Prometheus' **Alerts**
page — there is no Alertmanager wired up, so nothing pages anyone yet. Point
them at Alertmanager or Grafana alerting before you rely on being told
rather than looking.

### A detail that matters

The API runs gunicorn with 4 workers, and each keeps its own counters in
memory. They are written to a shared directory instead
(`PROMETHEUS_MULTIPROC_DIR`) and summed at scrape time; `backend/gunicorn.conf.py`
empties it at boot and retires a dead worker's files. Without both, request
rates drift upward forever and no `rate()` over them means anything. Local
dev runs a single uvicorn, where the override sets the variable empty and the
ordinary in-process registry is used.

---

## Running Tests

`pytest` is a dev dependency, not part of the running container's image — install it into the container once per session:

```bash
docker compose exec api pip install -r requirements-dev.txt
docker compose exec api python -m pytest -q
```

The suite resets the schema it points at on every run, so `DATABASE_URL`
must reference a **disposable** database — never one holding data you
care about.

`tests/test_security.py` holds the security regression tests. They are
written from the attacker's side: each asserts that an attack *fails*, so
they go red when an authorization check or a validator is removed. See
[SECURITY.md](SECURITY.md) for what each group covers.

---

## Production-style Run

`docker-compose.override.yml` is auto-loaded by `docker compose up` and is dev-only (hot-reload, relaxed config checks). To run the base stack as it would run in production (Gunicorn, no reload):

```bash
docker compose -f docker-compose.yml up -d --build
```

This enforces the production safety checks — you'll need a real `SECRET_KEY` (32+ random chars, e.g. `openssl rand -hex 32`), a non-default `DATABASE_URL`, and an `https://` `FRONTEND_URL`, or the API refuses to boot. Note that "production" here means *any* `APP_ENV` that isn't `development`/`dev`/`local`/`test`/`testing` — a typo fails safe rather than silently disabling the checks.

The base file also does **not** publish Postgres on the host (only the dev override does), so the database is reachable on the Compose network and nowhere else.

---

## Troubleshooting

**Pages 404 that should exist / weird routing behavior that a rebuild doesn't fix.** This has happened from heavy Docker Desktop churn (many rebuilds in a session) rather than an actual code issue. Fully quit Docker Desktop (not just restart the containers) and relaunch it, then `docker compose up -d --build` again.

**A new API endpoint doesn't work locally but curl to `/health` is fine.** Check `docker compose logs api` — since the dev override runs `uvicorn --reload`, a Python syntax error in changed code shows up there rather than as a Docker build failure.

**`docker compose exec api alembic ...` fails to connect.** Should not happen — `alembic/env.py` reads `DATABASE_URL` from the container's environment when present. If you see a `localhost:5432 connection refused` error, something has overridden that env var; check `docker compose exec api env | grep DATABASE_URL`.

---

## License

MIT
