"""
app/controllers/learning_courses_controller.py

Independent courses: enroll in any published course, see how ready you are,
take the short readiness check, get recommendations, and browse career
roadmaps - none of which needs a track, a career goal or a saved path.

    Roadmaps (a track is a recommended, ordered set of canonical courses)
      GET   /learning/tracks
      GET   /learning/tracks/{slug}
      GET   /learning/tracks/{slug}/courses

    A course, for the signed-in learner
      POST  /learning/courses/{slug}/enroll
      PATCH /learning/courses/{slug}/enrollment          pause / resume
      GET   /learning/courses/{slug}/progress
      GET   /learning/courses/{slug}/readiness
      GET   /learning/courses/{slug}/readiness-assessment   the questions (no answers)
      POST  /learning/courses/{slug}/readiness-assessment   grade the answers (server-side)

    The learner
      GET   /learning/recommendations
      GET   /learning/my-skill-levels

    A course's figures (the images its lessons place inline)
      GET   /learning/courses/{slug}/assets/{key}?exp=&sig=   the image; the URL a lesson block
                                                              carries is signed, see services/assets/urls

The catalogue endpoints (`GET /learning/courses`, `/courses/{slug}`, `/my-courses`)
stay in `learning_controller`. Every rule - readiness, recommendations, access -
lives in `app/services/learning`; this module validates input, calls it and
shapes the response. Every query is scoped to the authenticated user's id; no
user, enrollment or assessment id is ever accepted from the client.
"""
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from pydantic import StringConstraints
from sqlalchemy.orm import Session

from app.core.limiter import limiter
from app.core.security import get_current_user, get_optional_user
from app.db.session import get_db
from app.models.course_asset import CourseAsset
from app.models.learning_path import Course
from app.models.tool_course import ToolCourse
from app.models.user import User
from app.services.assets.store import get_asset_store
from app.services.assets.urls import is_valid as asset_url_is_valid
from app.services.content.lesson_blocks import KEY_PATTERN
from app.services.learning import course_views as CV
from app.services.learning import enrollment as enrollments
from app.services.learning import presenters as P
from app.services.learning import readiness as R
from app.services.learning import readiness_assessment as RA
from app.services.learning.catalog_service import CatalogBundle, load_catalog_bundle
from app.views import learning_courses as V
from app.views.learning_path import CareerGoalOut, CourseSlug, Slug

router = APIRouter(prefix="/learning", tags=["Learning Courses"])


def _error(status_code: int, code: str, message: str) -> HTTPException:
    return HTTPException(status_code=status_code, detail={"error": code, "message": message})


def _course(bundle: CatalogBundle, slug: str) -> Course:
    course = bundle.course_by_slug(slug.lower())
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


# ─── Roadmaps ───────────────────────────────────────────────────────────────

@router.get("/tracks", response_model=List[CareerGoalOut])
def list_tracks(db: Session = Depends(get_db)):
    """The career roadmaps. A roadmap is guidance - it never gates a course."""
    return P.career_goals_out(load_catalog_bundle(db))


def _track(bundle: CatalogBundle, slug: str):
    goal = next((g for g in P.career_goals_out(bundle) if g.slug == slug), None)
    if goal is None:
        raise HTTPException(status_code=404, detail="Track not found")
    return goal


@router.get("/tracks/{slug}", response_model=V.TrackDetailOut)
def get_track(slug: Slug, user: User | None = Depends(get_optional_user), db: Session = Depends(get_db)):
    bundle = load_catalog_bundle(db)
    goal = _track(bundle, slug)
    learner = CV.load_learner(db, user, bundle)
    return V.TrackDetailOut(**goal.model_dump(), courses=CV.track_courses(bundle, learner, slug))


@router.get("/tracks/{slug}/courses", response_model=List[V.TrackCourseOut])
def get_track_courses(slug: Slug, user: User | None = Depends(get_optional_user), db: Session = Depends(get_db)):
    bundle = load_catalog_bundle(db)
    _track(bundle, slug)
    return CV.track_courses(bundle, CV.load_learner(db, user, bundle), slug)


# ─── Enrollment ─────────────────────────────────────────────────────────────

@router.post("/courses/{slug}/enroll", response_model=V.EnrollOut)
@limiter.limit("30/minute")
def enroll(request: Request, slug: CourseSlug, current_user: User = Depends(get_current_user),
           db: Session = Depends(get_db)):
    """Enroll in a course - no track needed. Idempotent: enrolling twice returns
    the same enrollment. A paid course that has not been bought is refused with
    the same 403 the lessons use; a learner who is not yet ready is *not* refused -
    the response says what to review first and they can start straight away."""
    bundle = load_catalog_bundle(db)
    course = _course(bundle, slug)
    enrollment, created = enrollments.enroll(db, current_user, course, bundle)
    learner = CV.load_learner(db, current_user, bundle)
    readiness = CV.readiness_report(db, bundle, learner, course)
    return V.EnrollOut(
        enrollment=_enrollment_out(learner, course, enrollment), created=created, readiness=readiness,
        start=CV.start_plan(db, bundle, learner, course, readiness),
    )


def _enrollment_out(learner: CV.LearnerContext, course: Course, row) -> V.EnrollmentOut:
    from app.services.learning.progress_service import pct
    return V.EnrollmentOut(
        course_id=course.id, course_slug=course.slug, status=row.learning_status, source=row.source,
        progress_percentage=pct(learner.fraction(course.id)), enrolled_at=row.enrolled_at,
        started_at=row.started_at, completed_at=row.completed_at,
    )


@router.patch("/courses/{slug}/enrollment", response_model=V.EnrollmentOut)
@limiter.limit("30/minute")
def update_enrollment(request: Request, slug: CourseSlug, payload: V.EnrollmentUpdate,
                      current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bundle = load_catalog_bundle(db)
    course = _course(bundle, slug)
    row = enrollments.set_paused(db, current_user, course, payload.status == "paused")
    return _enrollment_out(CV.load_learner(db, current_user, bundle), course, row)


@router.get("/courses/{slug}/progress", response_model=V.CourseProgressOut)
def get_progress(slug: CourseSlug, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bundle = load_catalog_bundle(db)
    course = _course(bundle, slug)
    return CV.course_progress(db, bundle, CV.load_learner(db, current_user, bundle), course)


# ─── Readiness ──────────────────────────────────────────────────────────────

@router.get("/courses/{slug}/readiness", response_model=V.ReadinessOut)
def get_readiness(slug: CourseSlug, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """What this learner already knows for this course, what is missing and what
    to study first - from their own progress, quiz results and earlier checks.
    Advice only: it never blocks enrollment."""
    bundle = load_catalog_bundle(db)
    course = _course(bundle, slug)
    return CV.readiness_report(db, bundle, CV.load_learner(db, current_user, bundle), course)


@router.get("/courses/{slug}/readiness-assessment", response_model=V.AssessmentOut)
def get_assessment(slug: CourseSlug, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """The short check for this course: real questions from its prerequisites'
    quizzes, without answers."""
    bundle = load_catalog_bundle(db)
    course = _course(bundle, slug)
    questions = RA.select_questions(db, bundle, course)
    if not questions:
        raise _error(404, "assessment_unavailable", "This course has no readiness check.")
    return V.AssessmentOut(
        course_id=course.id, course_slug=course.slug, question_count=len(questions),
        estimated_minutes=RA.estimated_minutes(len(questions)),
        questions=[V.AssessmentQuestionOut(
            id=q.id, skill=P.skill_out(bundle.skills[q.skill]), question=q.question, question_ar=q.question_ar,
            options=list(q.options), options_ar=list(q.options_ar) if q.options_ar else None,
        ) for q in questions if q.skill in bundle.skills],
    )


@router.post("/courses/{slug}/readiness-assessment", response_model=V.AssessmentResultOut)
@limiter.limit("20/minute")
def submit_assessment(request: Request, slug: CourseSlug, payload: V.AssessmentSubmit,
                      current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Grade a submission. The score is computed here from the server's copy of
    the check; the request cannot carry one."""
    bundle = load_catalog_bundle(db)
    course = _course(bundle, slug)
    try:
        outcome = RA.grade(db, bundle, current_user, course, payload.answers)
    except RA.AssessmentInvalid as exc:
        raise _error(422, exc.code, exc.detail)
    learner = CV.load_learner(db, current_user, bundle)     # includes the check just stored
    return V.AssessmentResultOut(
        assessment_id=outcome.assessment_id, score=outcome.score, correct_count=outcome.correct_count,
        question_count=outcome.question_count, skill_results=outcome.skill_results,
        questions=[V.QuestionResultOut(id=r.id, correct=r.correct, explanation=r.explanation)
                   for r in outcome.questions],
        readiness=CV.readiness_report(db, bundle, learner, course),
    )


# ─── The learner ────────────────────────────────────────────────────────────

@router.get("/recommendations", response_model=V.RecommendationsOut)
def get_recommendations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Continue / recommended next / build your foundations / completed, each with
    the reason. Works with no career goal; a goal, when there is one, only sharpens it."""
    bundle = load_catalog_bundle(db)
    return CV.recommendations_out(db, bundle, CV.load_learner(db, current_user, bundle))


@router.get("/my-skill-levels", response_model=V.SkillLevelsOut)
def get_skill_levels(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    bundle = load_catalog_bundle(db)
    learner = CV.load_learner(db, current_user, bundle)
    levels = R.skill_levels(bundle, learner.evidence)
    profile = learner.profile
    return V.SkillLevelsOut(
        levels=levels,
        skills=[V.SkillLevelOut(skill=P.skill_out(bundle.skills[s]), level=lv) for s, lv in levels.items()
                if s in bundle.skills],
        programming_experience=profile.programming_experience if profile else None,
        ai_experience=profile.ai_experience if profile else None,
    )


# ─── Course figures ─────────────────────────────────────────────────────────

AssetKey = Annotated[str, StringConstraints(pattern=rf"^{KEY_PATTERN}$", max_length=120)]


@router.get("/courses/{slug}/assets/{key}")
def get_course_asset(
    request: Request, slug: CourseSlug, key: AssetKey,
    exp: int = Query(..., ge=0), sig: str = Query(..., min_length=8, max_length=128),
    db: Session = Depends(get_db),
):
    """One figure of one course. There is no login on this route because an `<img>`
    cannot send one: the signed URL (minted only into lesson responses the learner
    is allowed to read) is the credential, and it expires. The figure is looked up
    by (course, key) in the database - a request never names a file - and the store
    refuses anything that is not inside its root. `ETag` + `If-None-Match` make a
    repeat visit a 304."""
    if not asset_url_is_valid(slug.lower(), key, exp, sig):
        raise HTTPException(status_code=403, detail="This image link is invalid or has expired.")
    asset = (
        db.query(CourseAsset).join(ToolCourse, ToolCourse.id == CourseAsset.tool_course_id)
        .filter(ToolCourse.slug == slug.lower(), CourseAsset.key == key).first()
    )
    if asset is None:
        raise HTTPException(status_code=404, detail="Image not found")
    etag = f'"{asset.sha256}"'
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304, headers={"ETag": etag})
    response = get_asset_store().response(asset.storage_key, mime_type=asset.mime_type, etag=asset.sha256)
    if response is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return response
