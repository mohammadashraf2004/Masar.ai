# Masar — Frontend

Next.js 14 frontend with App Router, TypeScript, Tailwind CSS, and Zustand.

## Setup

```bash
npm install
cp .env.local.example .env.local
# Edit NEXT_PUBLIC_API_URL if your backend is not on localhost:8000
npm run dev
```

Open http://localhost:3000

## Pages

| Route | Description |
|---|---|
| `/auth/login` | Sign in |
| `/auth/register` | Create account + pick experience level |
| `/dashboard` | Overview: enrollments, skill scores, weekly plan |
| `/tracks` | Browse career tracks |
| `/tracks/[slug]` | Track detail: skill tree, lessons, exercises, projects |
| `/mentor` | AI mentor: chat, code review, skill gap, mock interview |
| `/profile` | Edit profile, update experience level |

## Design system

- **Font**: DM Sans (body) · Syne (headings) · JetBrains Mono (code)
- **Palette**: Near-black base (#080A0E) · Amber accent (#F59E0B) · Emerald/Rose/Sky status
- **Dark-only** — designed for developers, no light mode

## State management

- `src/lib/store.ts` — Zustand auth store (persisted to localStorage)
- `src/lib/api.ts` — Axios API client (auto-attaches JWT, auto-redirects on 401)
- `src/hooks/useAuth.ts` — auth guard hook used on every protected page
