# AI Career Acceleration Platform

An AI-powered career acceleration platform that turns students into job-ready tech professionals through adaptive theoretical + practical learning.

## Architecture

```
ai-career-platform/
├── backend/
│   └── app/
│       ├── core/           # Config, security, dependencies
│       ├── db/             # Database connection & migrations
│       ├── models/         # SQLAlchemy ORM models
│       ├── controllers/    # Route handlers (FastAPI routers)
│       ├── services/       # Business logic layer
│       └── views/          # Pydantic schemas (request/response)
├── frontend/               # Next.js app (see frontend/README.md)
└── docker-compose.yml
```

## Tech Stack

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **AI**: OpenAI / Claude APIs
- **Vector DB**: pgvector (PostgreSQL extension)
- **Auth**: JWT (python-jose)
- **Frontend**: Next.js + Tailwind

## Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 15+ with pgvector extension
- Node.js 18+

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and edit environment variables
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Core Features (MVP)

1. **User Auth** — Register, login, JWT tokens
2. **Career Tracks** — AI Engineer path with structured skill tree
3. **AI Mentor** — Contextual chat mentor powered by Claude/OpenAI
4. **Roadmap Generator** — Personalized learning roadmap
5. **Progress Tracking** — Lessons, quizzes, skill scores
6. **Project Recommendations** — Level-appropriate projects
7. **AI Code Reviewer** — Submit code, get AI feedback
8. **Skill Gap Analyzer** — Upload CV/GitHub → get gap analysis

## Environment Variables

See `.env.example` for all required variables.
