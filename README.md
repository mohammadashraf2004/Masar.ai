# AI Career Acceleration Platform

An AI-powered career acceleration platform that helps students become job-ready tech professionals through structured learning, AI mentorship, project-based practice, and personalized roadmaps.

---

# Project Structure

```text id="h4v2kr"
ai-career-platform/
│
├── backend/
│   ├── app/
│   │   ├── core/              # Config & security
│   │   ├── db/                # Database connection
│   │   ├── models/            # SQLAlchemy models
│   │   ├── views/             # Pydantic schemas
│   │   ├── controllers/       # FastAPI routers
│   │   └── services/          # Business logic & AI services
│   │
│   ├── seeds/                 # Learning tracks seed files
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/               # Next.js pages
│   │   ├── components/        # Shared UI components
│   │   ├── hooks/             # Custom hooks
│   │   ├── lib/               # API client & utilities
│   │   └── types/             # TypeScript types
│   │
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.ts
│   ├── Dockerfile
│   └── .env.local.example
│
├── docker-compose.yml
└── README.md
```

---

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* Alembic
* JWT Authentication

## Frontend

* Next.js 14
* TypeScript
* Tailwind CSS
* Zustand

## AI Integration

* OpenAI API
* Anthropic Claude API

---

# Core Features

* User Authentication
* AI Career Tracks
* AI Mentor
* Personalized Learning Roadmaps
* Progress Tracking
* AI Code Review
* Skill Gap Analysis

---

# Quick Start

## Prerequisites

* Python 3.11+
* Node.js 18+
* PostgreSQL 15+

---

# Backend Setup

```bash id="z2t7xn"
cd backend

python -m venv venv

# Linux / Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

Copy environment variables:

```bash id="u5m9rk"
cp .env.example .env
```

Run migrations:

```bash id="c1f6ye"
alembic upgrade head
```

Start backend server:

```bash id="p3x8jl"
uvicorn app.main:app --reload --port 8000
```

---

# Frontend Setup

```bash id="b6k2wp"
cd frontend

npm install
```

Copy environment variables:

```bash id="r8n4tv"
cp .env.local.example .env.local
```

Start frontend:

```bash id="f5q1mc"
npm run dev
```

---

# API Documentation

After running the backend:

* Swagger UI
  `http://localhost:8000/docs`

* ReDoc
  `http://localhost:8000/redoc`

---

# Docker Setup

```bash id="j7v3pd"
docker-compose up --build
```

---

# Environment Variables

See:

```text id="q9l4yx"
backend/.env.example
frontend/.env.local.example
```

for all required environment variables.
