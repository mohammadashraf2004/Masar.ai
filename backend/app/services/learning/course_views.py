"""
app/services/learning/course_views.py

Builds the API models for the course catalogue - cards, detail, readiness, start
plan, roadmaps, recommendations - from the services that decide things
(`readiness`, `enrollment`, `recommendations`, `course_content`).

It only assembles: no rule about readiness or recommendation lives here. Every
listing is built from one `LearnerContext` loaded once, so a page of forty course
cards costs the same handful of queries as a page of four.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.billing import CourseEnrollment
from app.models.learning_path import Course, LearningProfile, ReadinessAssessment
from app.models.user import User
from app.services.learning import course_content as content
from app.services.learning import presenters as P
from app.services.learning import readiness as R
from app.services.learning import readiness_assessment as RA
from app.services.learning import recommendations as REC
from app.services.learning.catalog_service import CatalogBundle
from app.services.learning.progress_service import pct
from app.views import learning_courses as V
from app.views.learning_path import (
    CourseCard, CourseRef, EnrollmentBrief, ModuleOut, ProjectOut, ReadinessBrief, RoadmapMembership,
)


# ─── The signed-in learner, loaded once ─────────────────────────────────────

@dataclass
class LearnerContext:
    user: Optional[User]
    enrollments: Dict[int, CourseEnrollment] = field(default_factory=dict)
    evidence: R.LearnerEvidence = R.EMPTY_EVIDENCE
    profile: Optional[LearningProfile] = None

    @property
    def signed_in(self) -> bool:
        return self.user is not None

    def fraction(self, course_id: int) -> float:
        return self.evidence.completion.get(course_id, 0.0)


def load_learner(db: Session, user: Optional[User], bundle: CatalogBundle) -> LearnerContext:
    if user is None:
        return LearnerContext(None)
    enrollments = {
        e.course_id: e for e in db.query(CourseEnrollment).filter(CourseEnrollment.user_id == user.id).all()
    }
    return LearnerContext(
        user, enrollments, R.gather_evidence(db, user.id, bundle),
        db.query(LearningProfile).filter(LearningProfile.user_id == user.id).first(),
    )


def enrollment_brief(learner: LearnerContext, course_id: int) -> Optional[EnrollmentBrief]:
    row = learner.enrollments.get(course_id)
    if row is None or row.status != "active":
        return None
    return EnrollmentBrief(
        status=row.learning_status, progress_percentage=pct(learner.fraction(course_id)),
        enrolled_at=row.enrolled_at, started_at=row.started_at, completed_at=row.completed_at,
    )


# ─── Cards ──────────────────────────────────────────────────────────────────

def _ref(bundle: CatalogBundle, course_id: int) -> CourseRef:
    c = bundle.courses[course_id]
    title, title_ar, _d, _da = P._source_text(c)
    return CourseRef(id=c.id, slug=c.slug, title=c.title or title or c.slug, title_ar=c.title_ar or title_ar)


def course_card(bundle: CatalogBundle, course: Course, learner: LearnerContext, *,
                role_slug: Optional[str] = None) -> CourseCard:
    info = bundle.catalog.courses[course.id]
    card = CourseCard(**P.course_summary(bundle, course, role_slug=role_slug).model_dump())
    card.recommended_before = [
        _ref(bundle, pid)
        for pid in sorted(info.prerequisite_ids | info.recommended_prerequisite_ids,
                          key=lambda p: (p not in info.prerequisite_ids, bundle.catalog.courses[p].level_rank, p))
        if pid in bundle.courses
    ][:3]
    if learner.signed_in:
        card.enrollment = enrollment_brief(learner, course.id)
        if info.is_available:
            result = R.readiness_for(bundle, course.id, learner.evidence)
            card.readiness = ReadinessBrief(state=result.state, score=result.score)
    return card


# ─── Readiness report ───────────────────────────────────────────────────────

def _skill_out(bundle: CatalogBundle, slug: str):
    return P.skill_out(bundle.skills[slug]) if slug in bundle.skills else None


def _standing_out(bundle: CatalogBundle, s: R.SkillStanding) -> Optional[V.SkillStandingOut]:
    skill = _skill_out(bundle, s.skill)
    if skill is None:
        return None
    return V.SkillStandingOut(skill=skill, standing=s.standing, level=s.level, required=s.required)


def review_out(db: Session, bundle: CatalogBundle, learner: LearnerContext, target: R.ReviewTarget) -> V.ReviewOut:
    """A prerequisite course to study first, with the modules to begin with: the
    ones the learner has not finished, in order."""
    course = bundle.courses[target.course_id]
    modules = content.course_modules(db, course, learner.user.id if learner.user else None)
    open_modules = [m for m in modules if m.status != content.MODULE_COMPLETED] or modules
    return V.ReviewOut(
        course=_ref(bundle, target.course_id),
        skills=[s for s in (_skill_out(bundle, k) for k in target.skills) if s is not None],
        required=target.required,
        modules=[V.ReviewModuleOut(id=m.id, order=m.order, title=m.title, title_ar=m.title_ar)
                 for m in open_modules[:3]],
    )


def last_assessment(db: Session, user_id: int, course_id: int) -> Optional[ReadinessAssessment]:
    return (db.query(ReadinessAssessment)
            .filter(ReadinessAssessment.user_id == user_id, ReadinessAssessment.course_id == course_id)
            .order_by(ReadinessAssessment.created_at.desc(), ReadinessAssessment.id.desc()).first())


def readiness_report(db: Session, bundle: CatalogBundle, learner: LearnerContext, course: Course) -> V.ReadinessOut:
    result = R.readiness_for(bundle, course.id, learner.evidence)
    last = last_assessment(db, learner.user.id, course.id) if learner.user else None
    return V.ReadinessOut(
        course_id=course.id, course_slug=course.slug, state=result.state, score=result.score,
        strengths=[o for o in (_standing_out(bundle, s) for s in result.strengths) if o],
        gaps=[o for o in (_standing_out(bundle, s) for s in result.gaps) if o],
        recommended_review=[review_out(db, bundle, learner, t) for t in result.review],
        has_prerequisites=result.has_prerequisites,
        assessment_available=bool(RA.select_questions(db, bundle, course)),
        last_assessed_at=last.created_at if last else None,
    )


def module_ref(m: content.ModuleInfo) -> V.ModuleRef:
    return V.ModuleRef(id=m.id, order=m.order, title=m.title, title_ar=m.title_ar)


def start_plan(db: Session, bundle: CatalogBundle, learner: LearnerContext, course: Course,
               readiness: V.ReadinessOut) -> V.StartPlanOut:
    """Where to begin. A learner with progress resumes at the first module they
    have not finished; anyone else starts at the first. The preparation list is
    the readiness review, advisory - the learner can start straight away."""
    modules = content.course_modules(db, course, learner.user.id if learner.user else None)
    target = content.first_incomplete(modules)
    resumed = any((m.completion or 0) > 0 for m in modules)
    if target is None and modules:
        target = modules[0]
    return V.StartPlanOut(
        mode="resume" if resumed else "start",
        recommended_module=module_ref(target) if target else None,
        preparation=[] if resumed else readiness.recommended_review,
    )


# ─── Detail, progress ───────────────────────────────────────────────────────

def module_out(m: content.ModuleInfo) -> ModuleOut:
    return ModuleOut(
        id=m.id, order=m.order, title=m.title, title_ar=m.title_ar, description=m.description,
        description_ar=m.description_ar, estimated_hours=m.estimated_hours, lesson_count=m.lesson_count,
        exercise_count=m.exercise_count, quiz_count=m.quiz_count, project_count=m.project_count,
        completion_required=m.completion_required, is_optional=m.is_optional,
        completion_pct=pct(m.completion) if m.completion is not None else None, status=m.status,
    )


def roadmap_order(bundle: CatalogBundle, role_slug: str) -> List[int]:
    """A roadmap's courses in its recommended order: the goal's own template,
    stage by stage, then any other course tagged for the goal (by weight, then id).
    One canonical course appears once, wherever it is listed."""
    sequence = [c for c in REC.goal_sequence(bundle, role_slug) if c in bundle.catalog.courses]
    weight = {"core": 0, "supporting": 1, "optional": 2}
    extras = sorted(
        (info for info in bundle.catalog.courses.values()
         if info.id not in sequence and role_slug in info.role_slugs),
        key=lambda i: (weight.get(i.relation_for(role_slug) or "core", 0), i.id),
    )
    return sequence + [i.id for i in extras]


def roadmap_memberships(bundle: CatalogBundle, course: Course) -> List[RoadmapMembership]:
    info = bundle.catalog.courses[course.id]
    result: List[RoadmapMembership] = []
    for role_slug, relation in info.role_relations:
        role = bundle.roles.get(role_slug)
        if role is None:
            continue
        sequence = roadmap_order(bundle, role_slug)
        result.append(RoadmapMembership(
            career_goal=P.role_ref(role), track_role=relation,
            position=sequence.index(course.id) + 1 if course.id in sequence else None, total=len(sequence),
        ))
    return sorted(result, key=lambda m: bundle.roles[m.career_goal.slug].position)


def course_detail(db: Session, bundle: CatalogBundle, course: Course, learner: LearnerContext):
    from app.views.learning_path import CourseDetail
    base = P.course_detail(bundle, course).model_dump()
    info = bundle.catalog.courses[course.id]
    base["recommended_prerequisites"] = [
        _ref(bundle, p).model_dump() for p in sorted(info.recommended_prerequisite_ids) if p in bundle.courses]
    uid = learner.user.id if learner.user else None
    base["modules"] = [module_out(m).model_dump() for m in content.course_modules(db, course, uid)]
    base["projects"] = [ProjectOut(
        id=p.id, title=p.title, title_ar=p.title_ar, estimated_hours=p.estimated_hours,
        module_order=p.module_order, kind=p.kind).model_dump() for p in content.course_projects(db, course)]
    base["roadmaps"] = [m.model_dump() for m in roadmap_memberships(bundle, course)]
    base["enrollment"] = enrollment_brief(learner, course.id)
    return CourseDetail(**base)


def course_progress(db: Session, bundle: CatalogBundle, learner: LearnerContext, course: Course) -> V.CourseProgressOut:
    modules = content.course_modules(db, course, learner.user.id if learner.user else None)
    required_modules = [module for module in modules if module.completion_required]
    row = learner.enrollments.get(course.id)
    enrolled = row is not None and row.status == "active"
    nxt = content.first_incomplete(modules)
    fraction = learner.fraction(course.id)
    status = row.learning_status if enrolled else "enrolled"
    return V.CourseProgressOut(
        course_id=course.id, course_slug=course.slug, enrolled=enrolled, status=status,
        progress_percentage=pct(fraction), modules_total=len(required_modules),
        modules_completed=sum(1 for m in required_modules if m.status == content.MODULE_COMPLETED),
        lessons_total=sum(m.lesson_count for m in required_modules),
        modules=[module_out(m) for m in modules],
        next_module=module_ref(nxt) if nxt else None,
    )


# ─── Recommendations ────────────────────────────────────────────────────────

def _reason_params(bundle: CatalogBundle, rec: REC.Recommendation) -> dict:
    """The reason's parameters plus the *names* a client needs to write the sentence
    in the reader's language: the ids in `params` mean nothing to a browser."""
    params = dict(rec.params)
    goal = params.get("goal")
    if isinstance(goal, str) and goal in bundle.roles:
        params["goal_title"], params["goal_title_ar"] = bundle.roles[goal].title, bundle.roles[goal].title_ar
    ids = params.get("course_ids")
    if isinstance(ids, (list, tuple)):
        params["courses"] = [
            {"slug": bundle.courses[i].slug, "title": REC._title(bundle, i), "title_ar": bundle.courses[i].title_ar}
            for i in ids if i in bundle.courses
        ]
    return params


def recommendation_out(bundle: CatalogBundle, learner: LearnerContext, rec: REC.Recommendation) -> V.RecommendationOut:
    return V.RecommendationOut(
        course=course_card(bundle, bundle.courses[rec.course_id], learner),
        reason_code=rec.reason_code, params=_reason_params(bundle, rec), reason=REC.english_reason(bundle, rec),
        readiness=rec.readiness,
    )


def recommendations_out(db: Session, bundle: CatalogBundle, learner: LearnerContext) -> V.RecommendationsOut:
    assert learner.user is not None
    recs = REC.build(db, learner.user.id, bundle, learner.evidence, learner.profile, list(learner.enrollments.values()))
    convert = lambda items: [recommendation_out(bundle, learner, r) for r in items]  # noqa: E731
    role = learner.profile.career_role if learner.profile is not None else None
    return V.RecommendationsOut(
        continue_learning=convert(recs.continue_learning), recommended_next=convert(recs.recommended_next),
        build_foundations=convert(recs.build_foundations), completed=convert(recs.completed),
        career_goal=P.role_ref(role) if role is not None and role.slug in bundle.roles else None,
    )


# ─── Roadmaps ───────────────────────────────────────────────────────────────

def track_courses(bundle: CatalogBundle, learner: LearnerContext, role_slug: str) -> List[V.TrackCourseOut]:
    """A roadmap's courses in its own order, each with that roadmap's weight for
    it and the stage it sits in. The same canonical course appears in every
    roadmap that lists it - there is no per-roadmap copy."""
    template = bundle.catalog.templates.get(role_slug)
    stage_of: Dict[int, str] = {}
    for entry in (template.stages if template else ()):
        for cid in entry.stage.course_ids:
            stage_of.setdefault(cid, entry.stage.slug)
    out: List[V.TrackCourseOut] = []
    for position, cid in enumerate(roadmap_order(bundle, role_slug), 1):
        info = bundle.catalog.courses[cid]
        relation = info.relation_for(role_slug) or "core"
        out.append(V.TrackCourseOut(
            course=course_card(bundle, bundle.courses[cid], learner, role_slug=role_slug),
            track_role=relation, position=position, stage=P._stage_ref(bundle, stage_of.get(cid)),
        ))
    return out
