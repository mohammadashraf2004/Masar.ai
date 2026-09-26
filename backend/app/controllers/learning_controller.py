"""
app/controllers/learning_controller.py

The learning-path API.

    Catalogue (public, like GET /tracks/)
      GET  /learning/levels
      GET  /learning/fields
      GET  /learning/career-goals
      GET  /learning/courses            ?level= &field= &career_goal= &q= &difficulty= &category= &skill= &enrolled=
                                        every filter is optional - no career goal or track is ever needed
      GET  /learning/courses/{slug}     (see learning_courses_controller for enroll / readiness / progress)
      GET  /learning/paths
      GET  /learning/paths/{slug}       ?level=
      GET  /learning/skills             ?career_goal= &level= &field=   what to ask "do you know it?" about

    The signed-in learner (named `my-*`, the way /tracks/my-enrollments and
    /exams/my-attempts already are)
      POST /learning/paths/generate
      GET  /learning/my-profile         PUT /learning/my-profile
      GET  /learning/my-path            PUT /learning/my-path
      GET  /learning/my-skills          PUT /learning/my-skills         (save + rebuild the roadmap)
      GET  /learning/my-skill-gaps      what is still missing, measured against the saved roadmap
      GET  /learning/my-progress

Every rule about what a path contains lives in app/services/learning; this
module validates input, calls it, and shapes the response. Nothing here knows
what a "multimodal" field is.

Authorization: the catalogue is public because the equivalent track and tool
listings are and it carries no lesson content. Everything `my-*` and
`generate` requires a signed-in user, and every query is scoped to that user's
id — no path or profile id is ever accepted from the client.
"""
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.content import terminology as T
from app.core.limiter import limiter
from app.core.security import get_current_user, get_optional_user
from app.db.session import get_db
from app.models.user import User
from app.models.billing import CourseEnrollment
from app.models.learning_path import Course
from app.services.billing.access_service import course_access
from app.services.learning import learning_service as svc
from app.services.learning import course_views as CV
from app.services.learning import presenters as P
from app.services.learning.catalog_service import CatalogBundle, load_catalog_bundle
from app.services.learning.path_generator import PathGenerationError
from app.services.learning.progress_service import overview
from app.services.learning.progress_service import course_completion, pct
from app.views.learning_path import (
    CareerGoalOut, CourseCard, CourseDetail, CourseSlug, CourseSummary, FieldOut, GenerateRequest, LevelOut,
    MySkillsOut, PathOut, PathSummaryOut, PathUpdate, ProfileOut, ProfileUpdate, ProgressOut,
    SkillGapsOut, SkillOptionOut, SkillsSavedOut, SkillsUpdate, Slug,
)

router = APIRouter(prefix="/learning", tags=["Learning Paths"])


def _error(status_code: int, code: str, message: str) -> HTTPException:
    """Same `{error, message}` detail the credit and verification gates use, so
    the client has one shape to branch on."""
    return HTTPException(status_code=status_code, detail={"error": code, "message": message})


def _validation(exc: svc.LearningValidationError) -> HTTPException:
    return _error(422, exc.code, exc.detail)


# ─── Catalogue ──────────────────────────────────────────────────────────────

@router.get("/levels", response_model=List[LevelOut])
def list_levels(db: Session = Depends(get_db)):
    bundle = load_catalog_bundle(db)
    return [P.level_out(lv) for lv in bundle.levels.values()]


@router.get("/fields", response_model=List[FieldOut])
def list_fields(db: Session = Depends(get_db)):
    return P.fields_out(load_catalog_bundle(db))


@router.get("/career-goals", response_model=List[CareerGoalOut])
def list_career_goals(db: Session = Depends(get_db)):
    return P.career_goals_out(load_catalog_bundle(db))


@router.get("/skills", response_model=List[SkillOptionOut])
def list_skill_options(
    career_goal: Slug,
    level: Optional[Slug] = None,
    field: List[Slug] = Query(default=[], max_length=12),
    db: Session = Depends(get_db),
):
    """The skills to ask a learner about for this goal, route and level -
    what "Skills & Technologies I know" offers. Derived from the courses the
    route contains, so the list is the catalogue's and never the client's."""
    bundle = load_catalog_bundle(db)
    if career_goal not in bundle.roles:
        raise _error(422, "unknown_career_goal", f"Unknown career goal '{career_goal}'.")
    try:
        return P.skill_options(
            bundle, role_slug=career_goal,
            level_slug=level or P.default_level_slug(bundle, career_goal), field_slugs=field,
        )
    except PathGenerationError as exc:
        raise _error(422, exc.code, exc.detail)


def _matches_text(summary: CourseSummary, surfaces: List[str]) -> bool:
    """Bilingual text match. The query is expanded through the terminology
    dictionary (the same expansion search uses), so "التضمينات" finds a course
    titled "Embeddings" without a second Arabic catalogue."""
    haystack = " ".join(filter(None, [
        summary.title, summary.title_ar, summary.description, summary.description_ar,
        *[s.name for s in summary.skills], *[s.name_ar or "" for s in summary.skills],
    ])).lower()
    return any(surface.lower() in haystack for surface in surfaces)


@router.get("/courses", response_model=List[CourseCard])
def list_courses(
    level: List[Slug] = Query(default=[], max_length=12),
    difficulty: List[Slug] = Query(default=[], max_length=12),
    field: List[Slug] = Query(default=[], max_length=12),
    category: List[Slug] = Query(default=[], max_length=12),
    career_goal: List[Slug] = Query(default=[], max_length=12),
    skill: List[Slug] = Query(default=[], max_length=12),
    q: Optional[str] = Query(None, min_length=2, max_length=120),
    available_only: bool = False,
    enrolled: Optional[bool] = None,
    user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """The course catalogue - every published course, browsable on its own.

    No filter is required; in particular no career goal, so a learner who has
    chosen no track sees the whole catalogue. Filters combine: any-of within one
    dimension, all-of across them - `difficulty=intermediate&category=nlp&category=speech`
    is "intermediate AND (NLP OR Speech)".

      level / difficulty   the course's level (the two names are one filter)
      field / category     its field (NLP, computer vision, ...) - the catalogue's own taxonomy
      career_goal          courses tagged for that roadmap
      skill                courses that teach the skill
      enrolled             true: only my courses; false: only those I am not in (signed in)

    Courses whose content is not published yet are listed (flagged
    `is_available: false`) unless `available_only`. A signed-in learner also gets
    their own `enrollment` and `readiness` on every card; the catalogue itself is public.
    Cards carry no lesson text."""
    bundle = load_catalog_bundle(db)
    surfaces = T.expand_query_surfaces(q) if q else []
    learner = CV.load_learner(db, user, bundle)
    levels = set(level) | set(difficulty)
    fields = set(field) | set(category)

    result: List[CourseCard] = []
    for course_id, info in bundle.catalog.courses.items():
        course = bundle.courses[course_id]
        if available_only and not info.is_available:
            continue
        if levels and course.level.slug not in levels:
            continue
        if fields and not (info.field_slugs & fields):
            continue
        if career_goal and not (info.role_slugs & set(career_goal)):
            continue
        if skill and not (info.teaches & set(skill)):
            continue
        if enrolled is not None:
            mine = CV.enrollment_brief(learner, course_id) is not None
            if mine != enrolled:
                continue
        # A listing filtered to exactly one career goal is a goal context, so
        # each course reports its weight there; with none or several it does not.
        card = CV.course_card(bundle, course, learner, role_slug=career_goal[0] if len(career_goal) == 1 else None)
        if q and not _matches_text(card, surfaces or [q]):
            continue
        result.append(card)
    result.sort(key=lambda c: (c.level.rank, c.id))
    return result


@router.get("/courses/{slug}", response_model=CourseDetail)
def get_course(slug: CourseSlug, user: Optional[User] = Depends(get_optional_user), db: Session = Depends(get_db)):
    """One course, on its own: description, modules, projects, prerequisites and the
    roadmaps it appears in. Public; a signed-in learner also gets their
    enrollment and per-module progress. No lesson text - the course viewer serves
    (and paywalls) that."""
    bundle = load_catalog_bundle(db)
    course = bundle.course_by_slug(slug.lower())
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return CV.course_detail(db, bundle, course, CV.load_learner(db, user, bundle))


@router.get("/courses/{slug}/access")
def get_course_access(
    slug: CourseSlug,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    course = db.query(Course).filter(Course.slug == slug.lower(), Course.is_active.is_(True)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    access = course_access(db, current_user.id, course)
    return {
        "has_access": access.has_access,
        "reason": access.reason,
        "enrollment_id": access.enrollment_id,
    }


@router.get("/my-courses")
def get_my_courses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    enrollments = (
        db.query(CourseEnrollment)
        .join(Course, CourseEnrollment.course_id == Course.id)
        .options(
            joinedload(CourseEnrollment.course).joinedload(Course.tool_course),
            joinedload(CourseEnrollment.course).joinedload(Course.track_level),
        )
        .filter(
            CourseEnrollment.user_id == current_user.id,
            CourseEnrollment.status == "active",
            or_(CourseEnrollment.expires_at.is_(None), CourseEnrollment.expires_at > datetime.now(timezone.utc)),
            Course.is_active.is_(True),
        )
        .order_by(CourseEnrollment.enrolled_at.desc())
        .all()
    )
    courses = [enrollment.course for enrollment in enrollments]
    completion = course_completion(db, current_user.id, courses)
    bundle = load_catalog_bundle(db)
    result = []
    for enrollment in enrollments:
        course = enrollment.course
        if course.id not in bundle.courses:
            continue
        summary = P.course_summary(bundle, course)
        result.append({
            "course_id": course.id,
            "slug": course.slug,
            "title": summary.title,
            "title_ar": summary.title_ar,
            "href": summary.href,
            "progress": pct(completion.get(course.id, 0.0)),
            "enrolled_at": enrollment.enrolled_at,
            "access_type": enrollment.source,
            # Lifecycle (cached on the enrollment; `progress` above is always live).
            "status": enrollment.learning_status,
            "started_at": enrollment.started_at,
            "completed_at": enrollment.completed_at,
            "estimated_hours": summary.estimated_hours,
            "module_count": summary.module_count,
        })
    return result


@router.get("/paths", response_model=List[PathSummaryOut])
def list_paths(db: Session = Depends(get_db)):
    """The journeys the configuration defines — one per career goal and field."""
    return P.path_summaries(load_catalog_bundle(db))


@router.get("/paths/{slug}", response_model=PathOut)
def get_path(slug: Slug, level: Optional[Slug] = None, db: Session = Depends(get_db)):
    """A predefined path such as `ai-engineer-computer-vision`, generated for
    an empty learner. `level` defaults to the career goal's recommended one."""
    bundle = load_catalog_bundle(db)
    parsed = P.parse_path_slug(bundle, slug)
    if parsed is None:
        raise HTTPException(status_code=404, detail="Path not found")
    role_slug, field_slug = parsed
    level_slug = level or P.default_level_slug(bundle, role_slug)
    try:
        generated = svc.generate(
            db, level=level_slug, career_goal=role_slug,
            fields=[field_slug] if field_slug else [], bundle=bundle,
        )
    except svc.LearningValidationError as exc:
        raise _validation(exc)
    return P.present_plan(generated.bundle, generated.plan)


# ─── Generation ─────────────────────────────────────────────────────────────

@router.post("/paths/generate", response_model=PathOut)
@limiter.limit("30/minute")
def generate_path(
    request: Request,
    payload: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Generate a path without saving it — the Explore page's "View path" and
    any what-if. Personalised with the caller's own progress and declared
    skills, so a finished course reads as finished."""
    active = svc.get_current_path(db, current_user.id)
    try:
        generated = svc.generate(
            db, level=payload.level, career_goal=payload.career_goal, fields=payload.fields,
            user=current_user,
            waived=(active.waived_course_ids if active else []),
        )
    except svc.LearningValidationError as exc:
        raise _validation(exc)
    return P.present_plan(
        generated.bundle, generated.plan, completion=generated.completion,
        known_skill_slugs=svc.known_skill_slugs(db, current_user.id, generated.bundle),
    )


# ─── The signed-in learner ──────────────────────────────────────────────────

@router.get("/my-profile", response_model=ProfileOut)
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bundle = load_catalog_bundle(db)
    return _profile_response(db, current_user, bundle)


def _profile_response(db: Session, user: User, bundle: CatalogBundle) -> ProfileOut:
    return P.profile_out(
        bundle, svc.get_profile(db, user.id),
        has_active_path=svc.get_current_path(db, user.id) is not None,
        known_skills=svc.known_skill_slugs(db, user.id, bundle),
    )


@router.put("/my-profile", response_model=ProfileOut)
@limiter.limit("30/minute")
def put_my_profile(
    request: Request,
    payload: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        svc.save_profile(db, current_user, payload)
    except svc.LearningValidationError as exc:
        raise _validation(exc)
    return _profile_response(db, current_user, load_catalog_bundle(db))


def _present_saved(db: Session, user: User, path, bundle: Optional[CatalogBundle] = None) -> PathOut:
    bundle = bundle or load_catalog_bundle(db)
    plan = svc.plan_from_path(path, bundle)
    _, completion = svc.build_user_state(db, user.id, bundle)
    return P.present_plan(
        bundle, plan, completion=completion, saved=path,
        known_skill_slugs=svc.known_skill_slugs(db, user.id, bundle),
    )


@router.get("/my-path", response_model=PathOut)
def get_my_path(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    path = svc.get_current_path(db, current_user.id)
    if path is None:
        # Same convention as GET /tracks/topics/{id}/progress: nothing yet is a 404.
        raise HTTPException(status_code=404, detail="No learning path yet")
    return _present_saved(db, current_user, path)


@router.put("/my-path", response_model=PathOut)
@limiter.limit("20/minute")
def put_my_path(
    request: Request,
    payload: PathUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    waiver_change = payload.waived_course_ids is not None
    if payload.regenerate is True and payload.status is not None:
        raise _error(422, "conflicting_update",
                     "A rebuilt path is always active; send the rebuild and the status change separately.")
    # Unset means "whatever the other keys imply"; waivers only take effect
    # through a rebuild, so they imply one.
    regenerate = waiver_change or (
        payload.regenerate if payload.regenerate is not None else payload.status is None
    )

    bundle = load_catalog_bundle(db)
    active = svc.get_current_path(db, current_user.id)

    if not regenerate:
        path = active
        if path is None:
            raise HTTPException(status_code=404, detail="No learning path yet")
        if payload.status is not None and payload.status != path.status:
            path.status = payload.status
            db.commit()
            db.refresh(path)
        return _present_saved(db, current_user, path, bundle)

    if waiver_change:
        unknown = [cid for cid in payload.waived_course_ids if cid not in bundle.courses]
        if unknown:
            raise _error(422, "unknown_course", f"Unknown course id(s): {', '.join(map(str, unknown))}")

    try:
        path, generated = svc.rebuild_path(
            db, current_user, waived=payload.waived_course_ids if waiver_change else None, bundle=bundle,
        )
    except svc.ProfileIncompleteError as exc:
        raise _error(409, "learning_profile_incomplete", str(exc))
    except svc.LearningValidationError as exc:
        raise _validation(exc)
    return P.present_plan(
        generated.bundle, svc.plan_from_path(path, generated.bundle),
        completion=generated.completion, saved=path,
        known_skill_slugs=svc.known_skill_slugs(db, current_user.id, generated.bundle),
    )


# ─── Skills the learner already knows ───────────────────────────────────────

@router.get("/my-skills", response_model=MySkillsOut)
def get_my_skills(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """What the learner knows (declared, or inferred from finished courses) and
    what they are learning now."""
    bundle = load_catalog_bundle(db)
    return P.my_skills_out(bundle, svc.skills_overview(db, current_user.id, bundle))


@router.put("/my-skills", response_model=SkillsSavedOut)
@limiter.limit("20/minute")
def put_my_skills(
    request: Request,
    payload: SkillsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Save the learner's self-declared skills and, when their profile is
    complete, rebuild the roadmap around them. Only the *future* of the path can
    change: what the learner has finished stays finished, and nothing is ever
    marked as mastered because it was ticked."""
    bundle = load_catalog_bundle(db)
    try:
        svc.set_self_declared_skills(db, current_user, payload.skills, bundle)
        db.commit()
    except svc.LearningValidationError as exc:
        db.rollback()
        raise _validation(exc)

    path_out = None
    if svc.profile_is_complete(svc.get_profile(db, current_user.id)):
        try:
            path, generated = svc.rebuild_path(db, current_user, bundle=bundle)
        except svc.ProfileIncompleteError:
            path = None  # a goal or level since retired: the skills are saved, the path waits
        else:
            path_out = P.present_plan(
                generated.bundle, svc.plan_from_path(path, generated.bundle),
                completion=generated.completion, saved=path,
                known_skill_slugs=svc.known_skill_slugs(db, current_user.id, generated.bundle),
            )
    overview_out = P.my_skills_out(bundle, svc.skills_overview(db, current_user.id, bundle))
    return SkillsSavedOut(**overview_out.model_dump(), path=path_out, roadmap_updated=path_out is not None)


@router.get("/my-skill-gaps", response_model=SkillGapsOut)
def get_my_skill_gaps(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """The skills the learner still lacks for their own roadmap, and how far
    along each is. Measured against the *saved* roadmap and their *declared*
    skills - nothing is inferred - and computed in the domain layer; a learner
    with no roadmap yet gets `available: false`, not an error."""
    path = svc.get_current_path(db, current_user.id)
    bundle = load_catalog_bundle(db)
    if (path is None or path.level is None or path.career_role is None
            or path.level.slug not in bundle.levels or path.career_role.slug not in bundle.roles):
        return SkillGapsOut(available=False)
    plan = svc.plan_from_path(path, bundle)
    _, completion = svc.build_user_state(db, current_user.id, bundle)
    return P.skill_gaps_out(
        bundle, plan, declared=svc.known_skill_slugs(db, current_user.id, bundle), completion=completion,
    )


@router.get("/my-progress", response_model=ProgressOut)
def get_my_progress(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Overall progress and its per-career-goal / per-field / per-skill views.
    Derived from the learner's activity on every call — a course finished once
    counts wherever it belongs, and never twice within one number."""
    bundle = load_catalog_bundle(db)
    _, completion = svc.build_user_state(db, current_user.id, bundle)
    active = svc.get_current_path(db, current_user.id)
    if active is None:
        return ProgressOut(path_pct=None, **overview(bundle.catalog, completion))
    # Taken from the very same presenter GET /my-path uses, so the two endpoints
    # cannot drift: which courses count (required and completed, never optional
    # or waived ones) is decided in exactly one place.
    plan = svc.plan_from_path(active, bundle)
    return P.present_plan(bundle, plan, completion=completion, saved=active).progress
