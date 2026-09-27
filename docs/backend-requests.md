# Backend requests from the frontend

What the frontend has built, or stubbed, that needs something behind it from the backend.
Each item says what exists today, what is asked for, and what the frontend already does with it.

## 1. Course certificates

**Today:** only exam certificates exist (`GET /exams/my-certificates`, and the public
`GET /exams/certificates/{certificate_id}`). Each has `certificate_id`, `track_title`,
`user_name`, `score`, `issued_at`, `is_valid`; the holder's own list also has `exam_id`.

**Asked for:** a certificate issued on finishing a *course*, and an endpoint that lists a
learner's and looks one up publicly (same shape, no internal ids):

| field | notes |
| --- | --- |
| `certificate_id` | UUID, the public identifier the QR code carries |
| `course_title` | English (the certificate is English only) |
| `parent_track_title` | the career track the course belongs to, or `null` |
| `duration_hours` | how long the course is |
| `issued_at` | ISO time |
| `holder_name_en` | see item 2; the certificate prints this, not the account name |
| `is_valid` | false once revoked |

Either extend the existing routes with a `kind: "exam" | "course"` field, or add
`/certificates/...`; the frontend does not mind which.

**Frontend:** `<CourseCertificate variant="course">` (CERTIFICATE OF COMPLETION, Date issued +
Course duration) is built and tested but nothing renders it yet. Exam certificates use
`variant="exam"` (PROFESSIONAL CERTIFICATION, Date issued + Exam score).

## 2. `holder_name_en` on the profile

The certificate is English only. Account names are often Arabic (`full_name`), and the Syne
face used on the certificate has no Arabic glyphs, so an Arabic name falls back to another font
and reads badly next to English text.

**Asked for:** an optional `holder_name_en` on the user profile (read and update), and a rule for
which name a certificate prints: `holder_name_en` when set, otherwise `full_name`. Ask for it at
registration or when a first certificate is issued.

**Frontend:** prints `user_name` as given today. Once the field exists, the certificate pages
should show a prompt to fill it in when the name has no Latin letters.

## 3. The deferred Home items

The design's Home screen has three blocks the frontend has deliberately **not** built yet, because
there is nothing to show in them:

- **Readiness score:** a 0-100 score, its change over the week, and four skill bars.
  Today: `overall_readiness_score` on the user, `GET /mentor/skill-scores`, and
  `GET /profile/scorecard` (certificates, pass rate, project scores; no weekly delta and no
  per-skill 0-100 list in the shape the design draws).
  *Asked for:* `GET /learning/readiness` returning `{ score, delta_7d, skills: [{ skill, score }] }`.
- **Milestones:** the learner's path as an ordered list, each with a status.
  *Asked for:* `GET /learning/my-path/milestones` returning
  `[{ id, title, meta, status: "done" | "current" | "locked", progress_pct }]`, derived from the
  personalised path (`/learning/my-path`), so the screen and the path never disagree.
- **Exam eligibility:** whether the next certification exam can be booked, and what is missing.
  Today the exam start endpoint checks eligibility itself but does not report it.
  *Asked for:* `GET /exams/eligibility` returning
  `{ exam_id, eligible, requirements: [{ label, met, current, needed }] }` (e.g. "readiness 75 or
  above: 72 / 75"), so the card can list what is left.

## 4. Billing (Plans & offers)

`/billing` and `/billing/success` are built against two stand-ins: a catalog
(`frontend/src/lib/billing/catalog.ts`) holding the handoff's *example* plans, packs and offer,
and a `PaymentProvider` (`payments.ts`) whose only implementation, `MockPaymentProvider`, moves no
money. In a production build with no provider the page says payments are not open and disables
Pay. **Nothing on the page is a price list.**

**Asked for:**

- **Catalog:** `GET /billing/catalog` -> `{ currency, current_plan, plans: [{ id, monthly, yearly,
  popular }], packs: [{ id, credits, bonus, price }], offer: { code, percent, ends_at } | null }`.
  Prices are **VAT-inclusive** and the frontend adds no tax; confirm that is the business's intent.
  The plan and feature wording is frontend copy keyed by plan id today, and lists feature claims
  (unlimited exercises, 300 credits a month, a quarterly proctored exam) that need the business to
  confirm or replace.
- **Promo codes:** `POST /billing/promo/validate { code }` -> `{ valid, percent }` or a reason
  (`invalid`, `expired`), checked on the server against the offer.
- **Checkout:** `POST /billing/checkout { item, cycle, method, promo_code }` -> an outcome or a
  redirect to the gateway; after a redirect or webhook the user lands on
  `/billing/success?invoice=...`, and `GET /billing/invoices/{id}` returns what the invoice was
  (item, cycle, amount, method, paid_at), plus a downloadable tax invoice (PDF).
- **Methods:** the design asks for mada, Apple Pay, STC Pay, a card and Tabby (installments).
  The gateway is not chosen. The frontend needs hosted card fields from it (card data never touches
  our inputs) and each brand's official logo assets for the method rows.

**An integration already exists and is not used by this page:** the backend has a Paymob checkout
(`/payments/wallet/topup/init`, `/payments/exam/init`, webhook confirmation, `credit_packages`
priced in **EGP**), and the dashboard's `PaymentResultBanner` reads its result. It supports cards and
mobile wallets, not mada, Apple Pay, STC Pay or Tabby, and it prices in EGP where the design shows
SAR. Whether billing wraps it, replaces it, or runs beside it is a decision for whoever chooses the
gateway. `frontend/src/lib/billing/paymobProvider.ts` is a stub that fits the interface (it lists cards
and mobile wallets and throws "not configured" for anything that would move money); nothing returns
it, and it is not wired.

**Dead code:** `frontend/src/components/ui/WalletWidget.tsx` is the only UI that used those
endpoints (`getWalletPackages`, `requestTopUp`, `initWalletTopUp`) and nothing imports it, so the
existing top-up flow has no entry point today. It is left alone on purpose; delete it, or reuse it,
when the gateway decision is made.

**The catalog owns the tax rule:** `currency`, `vatRate` and `pricesIncludeVat` come with the
catalog. With `pricesIncludeVat: true` (today's placeholder) the total is the sum of the prices and
the page says "VAT included" under it; with `false` it adds a VAT line at `vatRate`. The payment
methods come from the provider (`listMethods()`), not from the page.

## 5. AI mentor and mock interview

`/mentor` (chat + mock interview, handoff Task 12) is built on what the API does today, and where
it does not reach there is a stand-in with **Mock** in its name. What exists, checked against
`backend/app/controllers/mentor_controller.py`:

| | Today | What the frontend does |
| --- | --- | --- |
| Streaming | **None.** `POST /mentor/chat` returns the whole reply. | "The mentor is typing" covers the wait; replies appear whole. The composer is disabled while one is pending. |
| Threads | `GET /mentor/sessions` (latest 20), `GET /mentor/sessions/{id}`, `POST /mentor/new-session`. **But `chat` takes no session id: it always continues the most recently updated one.** | Lists threads and opens one to *read*. Sending from an earlier thread goes to the latest, and the page says so. |
| Thread titles | The first message, cut to 50 characters, **only for a session `chat` creates.** A "New session" keeps the title "New Session" forever. | Shows the first user message instead when the title is "New Session". |
| Context injected | Name, `experience_level`, `overall_readiness_score`, `language`, `terminology_mode`, optional `topic_id`, the last 10 messages. **Not** the current lesson, track, weakest skill or exercise code. | "What the mentor knows about you" lists exactly those, and says the lesson and exercise are not sent. "Attach code" pastes code into the message as a fenced block. |
| Quota | **No plan quota.** Each message costs 2 credits (`mentor_chat`) and a 402 comes back when they run out; there are no plans on the backend. | `MockMentorQuota` (browser storage, 20 a day) drives the counter and the Free-plan upsell, only in development or with `NEXT_PUBLIC_MENTOR_MOCKS=1`. A real 402 raises the credits upsell in any build. Both link to `/billing`. `?mockQuotaUsed=20` reaches the limit state. |
| Suggestions | `suggested_actions` in the chat reply. | Chips; tapping one sends it. |

**Mock interview.** `POST /mentor/mock-interview` generates *one question* (3 credits) from a
free-text topic, a difficulty and the earlier question/answer pairs. It never sees an answer, scores
nothing and stores nothing. It takes no language: questions come back in English.

**Asked for:**

- **Streaming chat:** an SSE or chunked variant of `/mentor/chat`.
- **`session_id` on `POST /mentor/chat`** so a thread can be continued, and a title taken from its
  first message for every session (or a rename).
- **Context:** the learner's current lesson/track and weakest skills (from the readiness work in
  item 3), and an optional `code` field for the current exercise, added to the model's context.
- **A plan quota:** `GET /mentor/quota -> { limit, used, resets_at } | { unlimited: true }`, and a
  429 or 402 with a machine-readable code when it is spent.
- **Interviews as a resource:** `POST /mentor/interviews` (role, type, language, duration) ->
  an id; `POST /mentor/interviews/{id}/answer { question_id, answer }` -> the score
  `{ accuracy, structure, clarity, note }` (each 1-10, so the report and side panel need nothing
  else) and the next question; `POST /mentor/interviews/{id}/end`; `GET /mentor/interviews` and
  `GET /mentor/interviews/{id}` for the report and the history. A `language` (`ar`|`en`) for the
  questions, and the cost (credits or plan allowance) reported before starting.

**Stand-ins in the frontend** (all in `frontend/src/lib/mentor/`):

- `MockAnswerScorer` (`scoring.ts`): scores an answer from its length, sentence count and whether it
  contains a number. **It is not an evaluation** and the panel says "sample scores". Off in a
  production build, where the panel says scoring is not available and the report lists questions
  and answers only.
- `MockInterviewStore` (`interviewStore.ts`): keeps interviews in this browser (last 20), for the
  report, the history and "retry weak questions". Not a claim, so it is on everywhere; a different
  browser or device sees none of them.
- `MockMentorQuota` (`quota.ts`), as above.
- All three are gated by `mentorMocksEnabled()` (`mocks.ts`) except the store.

**Also:** the interviewer's halo pulses while the next question is being fetched. There is no
synthetic voice; if the backend gets one, `InterviewerTile`'s `busy` prop is where "speaking" plugs
in. Dictation uses the browser's Web Speech API (Chrome and Safari send the audio to their vendor's
speech service); the microphone control is hidden where it does not exist (Firefox).

**Removed from the page:** the old `/mentor` also had a *Code review* and a *Skill gap* tool. The
design has only chat and interview, so neither is reachable from the UI now. `POST /mentor/code-review`
and `POST /mentor/skill-gap` and their `api.reviewCode` / `api.analyzeSkillGap` client methods are
untouched; the chat's "attach code" covers the first, and the learning-path
skill-gap panel covers the second.

## 6. Walkthrough (tour) records per account

**Today:** no endpoint. The frontend (`frontend/src/features/tours/`) remembers what each account
did with each tour in **this browser**: `localStorage["masar.tours"]`, keyed by account id then tour
id, each value `{ "status": "done" | "skipped", "version": <int>, "at": <ISO time> }`. So the same
account on another device, or after clearing site data, sees its tours again. "Never two tours in one
session" is per browser tab (`sessionStorage`) and stays client-side.

**Asked for:** the same record on the account, so it follows it.

Fields of a tour record:

| Field     | Type                    | Notes |
|-----------|-------------------------|-------|
| `tour_id` | string                  | `onboarding`, `mentor-interview` or `language` today. Free-form: the server does not need to know the list. |
| `status`  | `"done"` \| `"skipped"` | Skipping counts as seen. |
| `version` | integer                 | The tour's version when it was seen. A tour is due when there is no record for its **current** version, so the server stores the number it is given and never compares versions itself, except below. |
| `at`      | ISO 8601 timestamp      | Set by the server on write. |

Endpoints (for the signed-in account; no account id in the path):

- `GET /me/tours/:id` -> `{ "tour_id", "status", "version", "at" }`, or `404` when the account has
  never seen that tour. (The client asks once per tour on the page that runs it. A `GET /me/tours`
  returning all of them would save requests, but is not needed.)
- `PUT /me/tours/:id` with `{ "status": "done" | "skipped", "version": <int> }` upserts the record and
  returns it. Idempotent. A `version` lower than the stored one is ignored (the stored record is
  returned), so an out-of-date tab cannot make a newer tour show again.
- Nothing else is needed: which tour runs where, and the "New" tag (an account created before
  `TOURS_RELEASED_AT` in `registry.ts` is "existing"), are decided in the client from `created_at`.

**What the frontend does when it lands:** only `records.ts` changes (read and write through the
endpoints, keep localStorage as the offline fallback). The eligibility rules, the tests and the UI do
not.

**Set at release:** `TOURS_RELEASED_AT` (`registry.ts`) is a placeholder (2026-09-27, marked
`TODO(product)`). Accounts created before it get feature tours with the "New" tag and are not given the
first-run onboarding; accounts created after it get the opposite. Change it to the real release date.
