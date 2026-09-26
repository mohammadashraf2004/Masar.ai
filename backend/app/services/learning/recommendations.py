"""
app/services/learning/recommendations.py

"What should I do next?" - a transparent, deterministic recommender. No model
call and no learned weights: every suggestion is a score built from named,
documented parts, and every suggestion carries the *reason* it was made, as a
code plus parameters (the client turns those into a sentence in the reader's
language).

Four groups, in the order the dashboard shows them
    continue_learning   courses the learner is in the middle of
    recommended_next    what to start, best first
    build_foundations   prerequisites that would strengthen what they are doing
    completed           finished courses (to review) - never offered as "next"

What feeds the score (the learner's career goal is one input among several and
is *optional*; with none, the other inputs still produce a full list)
    next in the goal's roadmap    +50 for the first unfinished roadmap course, less for each later one
    weight in the goal            core +25, supporting +12, optional +4
    follows what they finished    +20 when a course's prerequisite is one they completed
    matches their interests       +15 when a field they picked is one of the course's
    readiness                     ready +30, mostly ready +20, not assessed +8
    fits their level              +6 at their level, -6 a level above, -20 two or more above
    a place to start              +10 for a beginner course that needs nothing first

A course whose *required* prerequisites are not finished is not offered as
"next"; it is a candidate for the foundations group instead. That is advice about
order, not a gate: any published course can still be opened and enrolled in.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence, Set, Tuple

from sqlalchemy.orm import Session

from app.models.billing import CourseEnrollment
from app.models.learning_path import LearningProfile
from app.services.learning.catalog_service import CatalogBundle
from app.services.learning.domain import CourseInfo
from app.services.learning.progress_service import _DONE
from app.services.learning import readiness as R

MAX_NEXT = 6
# A course that only scrapes by (ready, but a level above them and nothing else in its favour)
# is not worth a slot: an empty group is better than a poor suggestion.
MIN_SCORE = 25
MAX_FOUNDATIONS = 4

# ── Reason codes (wording lives with the client's interface strings) ─────────
IN_PROGRESS = "in_progress"
ENROLLED_NOT_STARTED = "enrolled_not_started"
NEXT_IN_ROADMAP = "next_in_roadmap"
FOLLOWS_COMPLETED = "follows_completed"
ROADMAP_COURSE = "roadmap_course"
MATCHES_INTEREST = "matches_interest"
READY_TO_START = "ready_to_start"
GOOD_PLACE_TO_START = "good_place_to_start"
STRENGTHENS_ENROLLED = "strengthens_enrolled"
PREPARES_FOR_NEXT = "prepares_for_next"
COMPLETED = "completed"

_ROLE_WEIGHT = {"core": 25, "supporting": 12, "optional": 4}
_READINESS_WEIGHT = {R.READY: 30, R.MOSTLY_READY: 20, R.NOT_ASSESSED: 8, R.NEEDS_FOUNDATION: 0}


@dataclass
class Recommendation:
    course_id: int
    reason_code: str
    params: Dict[str, object] = field(default_factory=dict)
    readiness: Optional[str] = None
    score: float = 0.0


@dataclass
class Recommendations:
    continue_learning: List[Recommendation] = field(default_factory=list)
    recommended_next: List[Recommendation] = field(default_factory=list)
    build_foundations: List[Recommendation] = field(default_factory=list)
    completed: List[Recommendation] = field(default_factory=list)


def goal_sequence(bundle: CatalogBundle, role_slug: Optional[str]) -> List[int]:
    """Course ids of a career goal's roadmap in the order its template lists them
    (stage by stage), each once. Empty when the goal has no template."""
    template = bundle.catalog.templates.get(role_slug) if role_slug else None
    ordered: List[int] = []
    for entry in (template.stages if template else ()):
        for cid in entry.stage.course_ids:
            if cid not in ordered:
                ordered.append(cid)
    return ordered


def _title(bundle: CatalogBundle, course_id: int) -> str:
    course = bundle.courses[course_id]
    return course.title or (course.tool_course.title if course.tool_course else course.slug)


def build(
    db: Session, user_id: int, bundle: CatalogBundle, evidence: R.LearnerEvidence,
    profile: Optional[LearningProfile], enrollments: Sequence[CourseEnrollment],
) -> Recommendations:
    catalog = bundle.catalog
    out = Recommendations()
    available: Dict[int, CourseInfo] = {cid: c for cid, c in catalog.courses.items() if c.is_available}
    done: Set[int] = {cid for cid, f in evidence.completion.items() if f >= _DONE and cid in available}

    # ── Where the learner is ────────────────────────────────────────────────
    live = [e for e in enrollments if e.status == "active" and e.course_id in available and e.course_id not in done]
    started = sorted(
        (e for e in live if evidence.completion.get(e.course_id, 0.0) > 0 and e.learning_status != "paused"),
        key=lambda e: e.updated_at or e.enrolled_at, reverse=True,
    )
    unstarted = sorted(
        (e for e in live if evidence.completion.get(e.course_id, 0.0) <= 0 and e.learning_status != "paused"),
        key=lambda e: e.enrolled_at, reverse=True,
    )
    for e in started:
        out.continue_learning.append(Recommendation(
            e.course_id, IN_PROGRESS, {"percent": round(100 * evidence.completion.get(e.course_id, 0.0))},
            R.readiness_for(bundle, e.course_id, evidence).state))
    for e in unstarted:
        out.continue_learning.append(Recommendation(
            e.course_id, ENROLLED_NOT_STARTED, {}, R.readiness_for(bundle, e.course_id, evidence).state))
    engaged: Set[int] = {r.course_id for r in out.continue_learning}

    for cid in sorted(done):
        out.completed.append(Recommendation(cid, COMPLETED))

    # ── What the learner asked for (all optional) ───────────────────────────
    goal = profile.career_role.slug if profile is not None and profile.career_role is not None else None
    interests = set(profile.field_slugs or []) if profile is not None else set()
    level_rank = profile.level.rank if profile is not None and profile.level is not None else None
    roadmap = [cid for cid in goal_sequence(bundle, goal) if cid in available]
    remaining = [cid for cid in roadmap if cid not in done]
    # Their level: what they said, else the highest they have finished, else the first.
    learner_rank = level_rank if level_rank is not None else max(
        (available[c].level_rank for c in done), default=1)

    # ── Candidates for "next" and their score ───────────────────────────────
    scored: List[Recommendation] = []
    blocked: List[Tuple[int, List[int]]] = []          # (candidate, its unmet required prerequisites)
    for cid, info in sorted(available.items()):
        if cid in done or cid in engaged:
            continue
        unmet = [p for p in sorted(info.prerequisite_ids) if p in available and p not in done]
        if unmet:
            blocked.append((cid, unmet))
            continue
        result = R.readiness_for(bundle, cid, evidence)
        score, reasons = 0.0, []
        if cid in remaining:
            position = remaining.index(cid)
            score += max(50 - 3 * min(position, 10), 20)
            if position == 0:
                reasons.append((NEXT_IN_ROADMAP, {"goal": goal}))
            else:
                reasons.append((ROADMAP_COURSE, {"goal": goal}))
        relation = info.relation_for(goal) if goal else None
        score += _ROLE_WEIGHT.get(relation or "", 0)
        followed = [p for p in sorted(info.prerequisite_ids | info.recommended_prerequisite_ids) if p in done]
        if followed:
            score += 20
            reasons.append((FOLLOWS_COMPLETED, {"course_ids": followed}))
        shared = sorted(info.field_slugs & interests)
        if shared:
            score += 15
            reasons.append((MATCHES_INTEREST, {"fields": shared}))
        score += _READINESS_WEIGHT.get(result.state, 0)
        gap = info.level_rank - learner_rank
        score += 6 if gap == 0 else 2 if gap < 0 else -6 if gap == 1 else -20
        if info.level_rank == 1 and not info.prerequisite_ids and not info.recommended_prerequisite_ids:
            score += 10
            reasons.append((GOOD_PLACE_TO_START, {}))
        if result.state in (R.READY, R.MOSTLY_READY) and not reasons:
            reasons.append((READY_TO_START, {}))
        if not reasons:
            reasons.append((READY_TO_START, {}))
        # The reason shown is the first of these that applies: it is ordered by how specific it is.
        rank = {NEXT_IN_ROADMAP: 0, FOLLOWS_COMPLETED: 1, ROADMAP_COURSE: 2, MATCHES_INTEREST: 3,
                GOOD_PLACE_TO_START: 4, READY_TO_START: 5}
        code, params = min(reasons, key=lambda r: rank[r[0]])
        scored.append(Recommendation(cid, code, params, result.state, score))
    scored.sort(key=lambda r: (-r.score, r.course_id))
    out.recommended_next = [r for r in scored if r.score >= MIN_SCORE][:MAX_NEXT]

    # ── Foundations: what would make current and next courses easier ────────
    targets = [r.course_id for r in out.continue_learning] + [r.course_id for r in out.recommended_next[:3]]
    # Where a learner has nothing to continue and nothing ready, the blocked courses are the targets.
    if not targets:
        targets = [cid for cid, _unmet in blocked[:3]]
    serves: Dict[int, List[int]] = {}
    for target in targets:
        for review in R.readiness_for(bundle, target, evidence).review:
            if review.course_id in done or review.course_id in engaged:
                continue
            serves.setdefault(review.course_id, [])
            if target not in serves[review.course_id]:
                serves[review.course_id].append(target)
    enrolled_targets = {r.course_id for r in out.continue_learning}
    ordered = sorted(serves, key=lambda cid: (-len(serves[cid]), catalog.courses[cid].level_rank, cid))
    for cid in ordered[:MAX_FOUNDATIONS]:
        for_enrolled = [t for t in serves[cid] if t in enrolled_targets]
        if for_enrolled:
            out.build_foundations.append(Recommendation(
                cid, STRENGTHENS_ENROLLED, {"course_ids": for_enrolled, "count": len(for_enrolled)}))
        else:
            out.build_foundations.append(Recommendation(cid, PREPARES_FOR_NEXT, {"course_ids": serves[cid][:2]}))
    return out


def english_reason(bundle: CatalogBundle, rec: Recommendation) -> str:
    """One readable sentence for API consumers that do not localise themselves.
    The client normally builds its own from `reason_code` and `params`."""
    def names(ids: object) -> str:
        return ", ".join(_title(bundle, int(i)) for i in ids if int(i) in bundle.courses)  # type: ignore[union-attr]

    goal = rec.params.get("goal")
    goal_title = bundle.roles[goal].title if isinstance(goal, str) and goal in bundle.roles else "your"
    code = rec.reason_code
    if code == IN_PROGRESS:
        return f"You are {rec.params.get('percent', 0)}% through this course."
    if code == ENROLLED_NOT_STARTED:
        return "You enrolled in this course but have not started it yet."
    if code == NEXT_IN_ROADMAP:
        return f"This is the next unfinished course in the {goal_title} roadmap."
    if code == ROADMAP_COURSE:
        return f"This course is part of the {goal_title} roadmap."
    if code == FOLLOWS_COMPLETED:
        return f"You completed {names(rec.params.get('course_ids', []))}, and this course builds on it."
    if code == MATCHES_INTEREST:
        return "This course matches the areas you said you are interested in."
    if code == GOOD_PLACE_TO_START:
        return "A good place to start: it assumes no earlier course."
    if code == STRENGTHENS_ENROLLED:
        return (f"This course will strengthen skills needed by {rec.params.get('count', 0)} of the courses "
                "you are taking.")
    if code == PREPARES_FOR_NEXT:
        return f"This course prepares you for {names(rec.params.get('course_ids', []))}."
    if code == COMPLETED:
        return "You finished this course."
    return "You are ready to start this course."
