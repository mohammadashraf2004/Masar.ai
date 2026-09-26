"""
app/services/learning/readiness.py

What does this learner already know for this course, what are they missing, and
what should they study first? Deterministic and explainable - no model call, no
score the client can influence.

The three layers
----------------
1. **Evidence** (`gather_evidence`): everything the platform already knows about
   the learner - courses finished or under way, quiz results, readiness checks
   they took, the skills they declared, their onboarding answers. Read once, in a
   fixed number of queries.
2. **Skill strength** (`skill_strengths`): each skill gets a strength 0..1 from
   the *best* single piece of evidence, never a sum:

       finished a course teaching it   completion x cap(course level)
       quiz results in such a course   mean best score x coverage x cap
       a readiness check               fraction correct x 0.75
       "I know it" (declared)          0.5 - a claim, never proof
       stored assessment / completion  0.75, and mastered 0.9
       onboarding answers              a weak prior, at most 0.6

   `cap` is 0.7 / 0.8 / 0.9 for a beginner / intermediate / advanced course, so
   finishing a beginner course makes a learner *intermediate* at its skills, and
   reaching *advanced* takes intermediate coursework. That is the whole model of
   proficiency: `advanced >= 0.8 > intermediate >= 0.6 > beginner > 0`, and a
   skill with no evidence at all is `not_assessed`.
3. **Readiness** (`evaluate`): the skills a course needs are the skills taught by
   its prerequisite courses. Each is strong, partial, a gap or unknown, and the
   state of the course is one of `ready` / `mostly_ready` / `needs_foundation` /
   `not_assessed`. Where a skill is weak, the review list names the prerequisite
   course that teaches it.

Readiness is advice. Nothing in this module (or any caller) refuses an
enrollment because of it, and readiness is independent of the course's difficulty:
an advanced course can be `ready` for one learner and `needs_foundation` for another.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.learning import Quiz, Topic
from app.models.learning_path import (
    COURSE_KIND_TOOL, LEARNER_SKILL_MASTERED, LEARNER_SKILL_SELF_DECLARED,
    LearnerSkill, LearningProfile, ReadinessAssessment,
)
from app.models.progress import QuizAttempt
from app.models.tool_course import ToolTopic
from app.services.learning.catalog_service import CatalogBundle
from app.services.learning.domain import Catalog, CourseInfo
from app.services.learning.progress_service import course_completion

# ── Vocabulary ───────────────────────────────────────────────────────────────
READY = "ready"
MOSTLY_READY = "mostly_ready"
NEEDS_FOUNDATION = "needs_foundation"
NOT_ASSESSED = "not_assessed"
READINESS_STATES = (READY, MOSTLY_READY, NEEDS_FOUNDATION, NOT_ASSESSED)

LEVEL_NOT_ASSESSED = "not_assessed"
LEVEL_BEGINNER, LEVEL_INTERMEDIATE, LEVEL_ADVANCED = "beginner", "intermediate", "advanced"

# Per-skill standing for one course.
SKILL_STRONG, SKILL_PARTIAL, SKILL_GAP, SKILL_UNKNOWN = "strong", "partial", "gap", "unknown"

# ── Tunable constants (documented in the module docstring) ───────────────────
LEVEL_CAP = {1: 0.7, 2: 0.8, 3: 0.9}
ADVANCED_AT, INTERMEDIATE_AT, PARTIAL_AT = 0.8, 0.6, 0.3
ASSESSMENT_WEIGHT = 0.75
DECLARED_STRENGTH = 0.5
STORED_STRENGTH, MASTERED_STRENGTH = 0.75, 0.9
QUIZ_COVERAGE_NEEDED = 3            # quizzes attempted before quiz scores count in full
READY_SCORE, MOSTLY_READY_SCORE = 85.0, 55.0
REQUIRED_WEIGHT, RECOMMENDED_WEIGHT = 2, 1

_PROGRAMMING_PRIOR = {"none": 0.0, "basic": 0.3, "comfortable": 0.45, "professional": 0.6}
_AI_PRIOR = {"none": 0.0, "basics": 0.3, "projects": 0.45, "applications": 0.6}
# Which catalogue skill each onboarding answer is a prior for.
PROGRAMMING_SKILL, AI_SKILL = "python", "machine-learning"


def level_for(strength: Optional[float]) -> str:
    if strength is None:
        return LEVEL_NOT_ASSESSED
    if strength >= ADVANCED_AT:
        return LEVEL_ADVANCED
    if strength >= INTERMEDIATE_AT:
        return LEVEL_INTERMEDIATE
    return LEVEL_BEGINNER if strength > 0 else LEVEL_NOT_ASSESSED


def _standing(strength: Optional[float]) -> str:
    if strength is None:
        return SKILL_UNKNOWN
    if strength >= INTERMEDIATE_AT:
        return SKILL_STRONG
    return SKILL_PARTIAL if strength >= PARTIAL_AT else SKILL_GAP


# ─── Evidence ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class LearnerEvidence:
    completion: Mapping[int, float] = field(default_factory=dict)      # course id -> 0..1
    # course id -> (mean of the best score per attempted quiz, 0..1; how many quizzes attempted)
    quiz: Mapping[int, Tuple[float, int]] = field(default_factory=dict)
    assessed: Mapping[str, float] = field(default_factory=dict)        # skill -> latest fraction correct
    declared: Mapping[str, Tuple[str, str]] = field(default_factory=dict)  # skill -> (status, source)
    priors: Mapping[str, float] = field(default_factory=dict)          # skill -> weak prior

    @property
    def has_any(self) -> bool:
        return bool(
            any(v > 0 for v in self.completion.values()) or self.quiz or self.assessed or self.declared
            or any(v > 0 for v in self.priors.values())
        )


EMPTY_EVIDENCE = LearnerEvidence()


def _quiz_evidence(db: Session, user_id: int, bundle: CatalogBundle) -> Dict[int, Tuple[float, int]]:
    """Best score per attempted quiz, averaged per catalogue course."""
    by_tool = {c.tool_course_id: c.id for c in bundle.courses.values() if c.kind == COURSE_KIND_TOOL and c.tool_course_id}
    by_level = {c.track_level_id: c.id for c in bundle.courses.values() if c.kind != COURSE_KIND_TOOL and c.track_level_id}
    best: Dict[int, List[float]] = {}

    def collect(rows, owner_map) -> None:
        for owner, score in rows:
            course_id = owner_map.get(owner)
            if course_id is not None:
                best.setdefault(course_id, []).append(float(score) / 100.0)

    if by_tool:
        collect(
            db.query(ToolTopic.tool_course_id, func.max(QuizAttempt.score))
            .join(Quiz, Quiz.tool_topic_id == ToolTopic.id)
            .join(QuizAttempt, QuizAttempt.quiz_id == Quiz.id)
            .filter(QuizAttempt.user_id == user_id, ToolTopic.tool_course_id.in_(list(by_tool)))
            .group_by(Quiz.id, ToolTopic.tool_course_id).all(), by_tool)
    if by_level:
        collect(
            db.query(Topic.level_id, func.max(QuizAttempt.score))
            .join(Quiz, Quiz.topic_id == Topic.id)
            .join(QuizAttempt, QuizAttempt.quiz_id == Quiz.id)
            .filter(QuizAttempt.user_id == user_id, Topic.level_id.in_(list(by_level)))
            .group_by(Quiz.id, Topic.level_id).all(), by_level)
    return {cid: (sum(scores) / len(scores), len(scores)) for cid, scores in best.items()}


def gather_evidence(db: Session, user_id: int, bundle: CatalogBundle) -> LearnerEvidence:
    """Everything the platform already knows about this learner, in a fixed
    number of queries. Read-only."""
    available = [bundle.courses[cid] for cid, info in bundle.catalog.courses.items() if info.is_available]
    completion = course_completion(db, user_id, available)

    slug_of = {s.id: s.slug for s in bundle.skills.values()}
    declared: Dict[str, Tuple[str, str]] = {}
    for row in db.query(LearnerSkill).filter(LearnerSkill.user_id == user_id).all():
        slug = slug_of.get(row.skill_id)
        if slug and row.status in ("known", "mastered"):
            declared[slug] = (row.status, row.source)

    assessed: Dict[str, float] = {}
    for row in (db.query(ReadinessAssessment).filter(ReadinessAssessment.user_id == user_id)
                .order_by(ReadinessAssessment.created_at, ReadinessAssessment.id).all()):
        for slug, fraction in (row.skill_results or {}).items():
            if isinstance(fraction, (int, float)):
                assessed[slug] = float(fraction)   # a later check replaces an earlier one

    priors: Dict[str, float] = {}
    profile = db.query(LearningProfile).filter(LearningProfile.user_id == user_id).first()
    if profile is not None:
        if profile.programming_experience in _PROGRAMMING_PRIOR:
            priors[PROGRAMMING_SKILL] = _PROGRAMMING_PRIOR[profile.programming_experience]
        if profile.ai_experience in _AI_PRIOR:
            priors[AI_SKILL] = _AI_PRIOR[profile.ai_experience]

    return LearnerEvidence(
        completion=completion, quiz=_quiz_evidence(db, user_id, bundle),
        assessed=assessed, declared=declared, priors=priors,
    )


# ─── Skill strength ─────────────────────────────────────────────────────────

def _cap(info: CourseInfo) -> float:
    return LEVEL_CAP.get(info.level_rank, LEVEL_CAP[2])


def skill_strength(catalog: Catalog, evidence: LearnerEvidence, skill: str) -> Optional[float]:
    """The strength (0..1) of one skill from the best evidence, or None when
    there is no evidence at all."""
    candidates: List[float] = []
    for info in catalog.courses.values():
        if not info.is_available or skill not in info.teaches:
            continue
        fraction = evidence.completion.get(info.id, 0.0)
        if fraction > 0:
            candidates.append(fraction * _cap(info))
        mean_best, attempted = evidence.quiz.get(info.id, (0.0, 0))
        if attempted:
            candidates.append(mean_best * min(1.0, attempted / QUIZ_COVERAGE_NEEDED) * _cap(info))
    if skill in evidence.assessed:
        candidates.append(evidence.assessed[skill] * ASSESSMENT_WEIGHT)
    if skill in evidence.declared:
        status, source = evidence.declared[skill]
        if status == LEARNER_SKILL_MASTERED:
            candidates.append(MASTERED_STRENGTH)
        elif source == LEARNER_SKILL_SELF_DECLARED:
            candidates.append(DECLARED_STRENGTH)
        else:
            candidates.append(STORED_STRENGTH)
    if evidence.priors.get(skill, 0) > 0:
        candidates.append(evidence.priors[skill])
    return max(candidates) if candidates else None


def skill_strengths(catalog: Catalog, evidence: LearnerEvidence, skills: Iterable[str]) -> Dict[str, Optional[float]]:
    return {s: skill_strength(catalog, evidence, s) for s in skills}


def known_skill_names(catalog: Catalog) -> List[str]:
    """Every skill some available course teaches (the assessable vocabulary)."""
    seen: List[str] = []
    for info in catalog.courses.values():
        if info.is_available:
            seen += [s for s in sorted(info.teaches) if s not in seen]
    return seen


# ─── Readiness ──────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class Requirement:
    skill: str
    required: bool                                  # some *required* prerequisite teaches it
    courses: Tuple[int, ...]                        # the prerequisite courses that teach it


@dataclass(frozen=True)
class SkillStanding:
    skill: str
    standing: str                                   # strong | partial | gap | unknown
    level: str                                      # not_assessed | beginner | intermediate | advanced
    strength: Optional[float]
    required: bool


@dataclass(frozen=True)
class ReviewTarget:
    """A prerequisite course to study first, and the weak skills it would fix."""
    course_id: int
    skills: Tuple[str, ...]
    required: bool


@dataclass(frozen=True)
class ReadinessResult:
    course_id: int
    state: str
    score: int
    standings: Tuple[SkillStanding, ...]
    review: Tuple[ReviewTarget, ...]
    has_prerequisites: bool

    @property
    def strengths(self) -> List[SkillStanding]:
        return [s for s in self.standings if s.standing == SKILL_STRONG]

    @property
    def gaps(self) -> List[SkillStanding]:
        return [s for s in self.standings if s.standing != SKILL_STRONG]


def requirements_for(catalog: Catalog, course: CourseInfo) -> List[Requirement]:
    """The skills this course builds on: everything its prerequisite courses
    teach (required ones marked), plus any skill it explicitly `assumes`. Derived
    from the catalogue - nothing here is written by hand."""
    found: Dict[str, Dict[str, object]] = {}

    def add(skill: str, course_id: Optional[int], required: bool) -> None:
        entry = found.setdefault(skill, {"required": False, "courses": []})
        entry["required"] = entry["required"] or required
        if course_id is not None and course_id not in entry["courses"]:
            entry["courses"].append(course_id)

    # A prerequisite with no published lessons yet cannot be studied, so what it will teach is
    # not something to ask a learner to have: it joins the requirements when its content does.
    for pid in sorted(course.prerequisite_ids):
        prereq = catalog.courses.get(pid)
        for skill in sorted(prereq.teaches) if prereq and prereq.is_available else ():
            add(skill, pid, True)
    for pid in sorted(course.recommended_prerequisite_ids):
        prereq = catalog.courses.get(pid)
        for skill in sorted(prereq.teaches) if prereq and prereq.is_available else ():
            add(skill, pid, False)
    for skill in sorted(course.assumes):
        add(skill, None, True)
    return [Requirement(s, bool(e["required"]), tuple(e["courses"])) for s, e in found.items()]


def evaluate(catalog: Catalog, course: CourseInfo, evidence: LearnerEvidence) -> ReadinessResult:
    """Readiness of a learner (their `evidence`) for `course`. Pure: no I/O."""
    requirements = requirements_for(catalog, course)
    if not requirements:
        return ReadinessResult(course.id, READY, 100, (), (), False)

    standings: List[SkillStanding] = []
    earned = total = 0.0
    for req in requirements:
        strength = skill_strength(catalog, evidence, req.skill)
        standings.append(SkillStanding(req.skill, _standing(strength), level_for(strength), strength, req.required))
        weight = REQUIRED_WEIGHT if req.required else RECOMMENDED_WEIGHT
        total += weight
        earned += weight * min(1.0, (strength or 0.0) / INTERMEDIATE_AT)
    score = round(100.0 * earned / total)

    if all(s.standing == SKILL_UNKNOWN for s in standings):
        state = NOT_ASSESSED
    elif score >= READY_SCORE and all(s.standing == SKILL_STRONG for s in standings if s.required):
        state = READY
    elif score >= MOSTLY_READY_SCORE and all(s.standing in (SKILL_STRONG, SKILL_PARTIAL) for s in standings if s.required):
        state = MOSTLY_READY
    else:
        state = NEEDS_FOUNDATION

    return ReadinessResult(
        course.id, state, score, tuple(standings), tuple(_review_targets(catalog, course, requirements, standings)),
        True,
    )


def _review_targets(
    catalog: Catalog, course: CourseInfo, requirements: Sequence[Requirement], standings: Sequence[SkillStanding],
) -> List[ReviewTarget]:
    """One prerequisite course per weak skill, grouped by course, cheapest first.
    A course the learner has finished is never proposed."""
    by_course: Dict[int, List[str]] = {}
    required_in: Dict[int, bool] = {}
    for req, standing in zip(requirements, standings):
        if standing.standing == SKILL_STRONG:
            continue
        providers = [
            catalog.courses[c] for c in req.courses if c in catalog.courses
        ] or [
            c for c in catalog.courses.values() if c.id != course.id and req.skill in c.teaches
        ]
        providers = [p for p in providers if p.is_available]
        providers.sort(key=lambda p: (p.level_rank, p.id))
        pick = next((p for p in providers if p.id != course.id), None)
        if pick is None:
            continue
        by_course.setdefault(pick.id, []).append(req.skill)
        required_in[pick.id] = required_in.get(pick.id, False) or req.required
    order = sorted(by_course, key=lambda cid: (not required_in[cid], catalog.courses[cid].level_rank, cid))
    return [ReviewTarget(cid, tuple(by_course[cid]), required_in[cid]) for cid in order]


def readiness_for(bundle: CatalogBundle, course_id: int, evidence: LearnerEvidence) -> ReadinessResult:
    return evaluate(bundle.catalog, bundle.catalog.courses[course_id], evidence)


def evaluate_course_readiness(
    db: Session, user_id: int, course_id: int, *, bundle: CatalogBundle,
    evidence: Optional[LearnerEvidence] = None,
) -> ReadinessResult:
    """The entry point named in the design: readiness of one learner for one
    course. Pass `evidence` to reuse what a caller already gathered."""
    if evidence is None:
        evidence = gather_evidence(db, user_id, bundle)
    return readiness_for(bundle, course_id, evidence)


def skill_levels(bundle: CatalogBundle, evidence: LearnerEvidence) -> Dict[str, str]:
    """`{skill: 'not_assessed' | 'beginner' | 'intermediate' | 'advanced'}` for
    every skill some available course teaches. A learner can be advanced at
    Python and a beginner at machine learning - there is no single global level."""
    return {
        skill: level_for(skill_strength(bundle.catalog, evidence, skill))
        for skill in known_skill_names(bundle.catalog)
    }
