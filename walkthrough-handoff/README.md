# Walkthrough tours — handoff sync

Reconciles the design handoff (`Masar Walkthrough.dc.html` / `MasarTour.dc.html`) with what actually
shipped in `frontend/src/features/tours/` (see `docs/backend-requests.md` §6 for the backend ask, and
the `walkthrough-tours-2026-09-27` project note for the full list of spec-vs-app decisions). This file
covers only the points that changed or need an acceptance check; everything else in the original
design doc (card anatomy, placement order, transitions, memory model) still matches as designed.

## 1. Phone onboarding — 4 steps

Order: **path → learn → practice → mentor**, same as desktop. There is no dedicated Exercises nav
item or stat on a phone, so `practice` points at a phone-only **Challenges row** on the dashboard
(`<Card data-tour="practice" className="... lg:hidden">`, `frontend/src/app/dashboard/page.tsx`) —
hidden from `lg` up, where the sidebar's own Challenges item (`nav-practice`) is used instead.

Because `learn` sits further down the page than the Challenges row, moving from step 2 to step 3
causes a short scroll back up as the target comes into view (`reveal()` in
`frontend/src/features/tours/targets.ts` — generic "scroll the target into view" behavior, not a
special case for this transition). Expected, not a bug.

## 2. Phone language tour — 2 steps

The tour is defined with 3 steps (switch, lesson terms, mentor tone), but only 2 ever resolve on a
given page: `lesson-terms` only exists on a lesson, `mentor-lang` only on the mentor page, and a page
is never both. So the phone tour is always exactly 2 steps, in whichever of those two contexts it
starts.

Step 1 targets `{ desktop: 'lang-switch', mobile: 'menu-button' }` (`registry.ts`). On a phone the
language switch itself lives inside the closed mobile menu, which the tour never opens — it points at
the button that opens that menu instead, and **never opens `#mobile-menu` programmatically**. The
step carries phone-only wording via `mobile.bodyKey` to say "from the menu" instead of pointing at a
control that isn't visible yet:

- en: "Switch the interface language from the menu anytime; your progress stays the same."
- ar: "بدّل لغة الواجهة من القائمة في أي وقت، وسيبقى تقدّمك كما هو."

## 3. Mobile-only copy on a step

`TourStep.mobile?: { titleKey?: StringKey; bodyKey?: StringKey }` (`registry.ts`) overrides the
title and/or body key on a phone; whatever isn't named falls back to the step's desktop copy
(`copyFor()`). Used today only by the language tour's step 1 (mobile `bodyKey` only, same title).

## 4. Ring rule (acceptance check)

The spotlight ring is drawn in the tour's own portal layer (`createPortal(..., document.body)` in
`Tour.tsx`), not as an outline on the target element itself. It equals the target's bounding rect
expanded by 6px on every side (`PAD = 6` in `Tour.tsx`, applied to both x/y and w/h before it's passed
to `place()`).

**Check:** for any tour step, `ring rect == target.getBoundingClientRect() ± 6px` on all four sides,
within ±1px. Measured every frame (scroll, resize, DOM mutation), so this should hold whether the
target moves or the viewport does.

## 5. Mentor-lang ring — verified, no fix needed

The earlier report of the mentor page's language-tour step showing no ring did not reproduce: the ring
is portal-drawn (see §4), and the target+6px check above passes on `mentor-lang` in every viewport,
theme and language combination tested. No code change made.

## 6. Backend

No endpoint exists yet. See `docs/backend-requests.md` §6, "Walkthrough (tour) records per account":
record fields are `tour_id`, `status`, `version`, `at`; the ask is `GET /me/tours/:id` and
`PUT /me/tours/:id`. Until it ships, records live in this browser's `localStorage["masar.tours"]`.
