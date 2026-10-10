import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Exercise, Project, Quiz
from app.models.progress import Enrollment, UserProgress, QuizAttempt, ProjectSubmission, ProgressStatus
from app.views.learning import (
    CareerTrackResponse, CareerTrackSummary,
    EnrollRequest, EnrollmentResponse,
    ProgressUpdate, ProgressResponse,
    QuizSubmit, QuizAttemptResponse,
    ProjectSubmit, ProjectSubmissionResponse,
    ProjectHintRequest, ProjectHintResponse,
    TopicResponse,
)
from app.core.authz import require_verified_user
from app.core.security import get_current_user, get_optional_user
from app.services.content.track_availability import require_track_available
from app.core.config import settings
from app.core.limiter import limiter
from app.services import get_llm, code_review_service
from app.services.mentor.mentor_service import get_project_hint
from app.services.wallet.wallet_service import deduct_credits, refund_credits
from app.services.billing.redaction import redact_topic
from app.services.billing.access_service import (
    course_access, course_for_track_topic, free_lesson_ids, free_preview_content_ids, require_content_access,
    require_course_access, require_lesson_access,
)
from app.models.learning_path import Course
from app.services.learning import enrollment as course_enrollment
from app.services.learning import track_catalog
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tracks", tags=["Learning Tracks"])

# A single topic's accumulated self-reported study time. Progress numbers
# feed the engineer scorecard, which is the thing employers are shown, so
# they get the same "don't trust the client" treatment as anything else.
MAX_TOPIC_MINUTES = 100_000


def _redact_locked_track(track: CareerTrack, user_id: int, db: Session):
    """Keep curriculum metadata visible while removing paid lesson bodies."""
    data = CareerTrackResponse.model_validate(track).model_dump()
    courses = {
        course.track_level_id: course for course in db.query(Course).filter(
            Course.track_level_id.in_([level.id for level in track.levels]),
            Course.is_active.is_(True),
        ).all()
    }
    for level in data["levels"]:
        course = courses.get(level["id"])
        if not course or course_access(db, user_id, course).has_access:
            continue
        free_ids = free_lesson_ids(db, course)
        free_exercise_ids, free_quiz_ids = free_preview_content_ids(db, course)
        for topic in level["topics"]:
            redact_topic(topic, course.slug, free_lesson_ids=free_ids,
                         free_exercise_ids=free_exercise_ids, free_quiz_ids=free_quiz_ids)
    return data


def _validate_progress_targets(db: Session, payload: ProgressUpdate, *, topic_id: int) -> None:
    """A lesson/exercise id may only be marked complete against the topic
    it actually belongs to.

    Without this the ids are just numbers the client picks: a caller could
    POST the same topic 50 times with 50 arbitrary lesson ids and have the
    completion logic (which only counts list length against the topic's
    lesson count) mark the topic — and, upstream, the course — finished
    without opening a single lesson.
    """
    if payload.lesson_id is not None:
        belongs = db.query(Lesson.id).filter(
            Lesson.id == payload.lesson_id,
            Lesson.topic_id == topic_id,
        ).first()
        if not belongs:
            raise HTTPException(status_code=400, detail="That lesson does not belong to this topic")

    if payload.exercise_id is not None:
        exercise = db.query(Exercise).filter(
            Exercise.id == payload.exercise_id,
            Exercise.topic_id == topic_id,
        ).first()
        if not exercise:
            raise HTTPException(status_code=400, detail="That exercise does not belong to this topic")
        if exercise.exercise_type == "code" or exercise.starter_code:
            raise HTTPException(status_code=409, detail={"code": "SUBMIT_CODE_TO_COMPLETE"})


# ─── Career Tracks ──────────────────────────────────────────────────────

@router.get("/", response_model=List[CareerTrackSummary])
def list_tracks(
    current_user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    tracks = db.query(CareerTrack).filter(CareerTrack.is_active == True).all()
    return track_catalog.catalogue(db, tracks, current_user)


# ─── Enrollment — MUST come before /{slug} to avoid route collision ─────

@router.post("/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll(
    payload: EnrollRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    track = db.query(CareerTrack).filter(CareerTrack.id == payload.track_id).first()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")

    # The tracks page hides unpublished tracks, but this endpoint takes a
    # track id straight from the client, so the rule is enforced here as
    # well — and against the slug on the row the id resolved to, never one
    # the caller sent. Before the enrolment row is built, so a rejection
    # writes nothing.
    require_track_available(track, user_id=current_user.id)

    existing = db.query(Enrollment).filter(
        Enrollment.user_id == current_user.id,
        Enrollment.track_id == payload.track_id,
        Enrollment.is_active == True,
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this track")

    enrollment = Enrollment(
        user_id=current_user.id,
        track_id=payload.track_id,
        target_job_title=payload.target_job_title,
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get("/my-enrollments", response_model=List[EnrollmentResponse])
def my_enrollments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Joined to CareerTrack (not just eager-loaded) so a retired track is
    # excluded. Without this, retiring a track leaves a ghost card on every
    # enrolled user's dashboard that 404s when clicked, because GET
    # /tracks/{slug} filters on is_active too. The enrollment row is kept —
    # it's history, and it comes back if the track is re-activated.
    return (
        db.query(Enrollment)
        .join(CareerTrack, Enrollment.track_id == CareerTrack.id)
        .options(joinedload(Enrollment.track))
        .filter(
            Enrollment.user_id == current_user.id,
            Enrollment.is_active == True,
            CareerTrack.is_active == True,
        )
        .all()
    )


# ─── Track detail — AFTER all literal routes ────────────────────────────

@router.get("/{slug}", response_model=CareerTrackResponse)
def get_track(
    slug: str,
    current_user: User | None = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    """Public catalogue detail; lesson bodies remain authenticated.

    A guest receives the timeline/roles/projects projection and no legacy
    levels. Signed-in learners retain the older curriculum response, redacted
    according to course access, alongside the new projection.
    """
    track = (
        db.query(CareerTrack)
        .options(
            joinedload(CareerTrack.levels)
                .joinedload(TrackLevel.topics)
                .joinedload(Topic.lessons),
            joinedload(CareerTrack.levels)
                .joinedload(TrackLevel.topics)
                .joinedload(Topic.exercises),
            joinedload(CareerTrack.levels)
                .joinedload(TrackLevel.topics)
                .joinedload(Topic.projects),
            joinedload(CareerTrack.levels)
                .joinedload(TrackLevel.topics)
                .joinedload(Topic.quizzes),
        )
        .filter(CareerTrack.slug == slug, CareerTrack.is_active == True)
        .first()
    )
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    result = track_catalog.detail(db, track, current_user)
    if current_user is None:
        result["levels"] = []
    else:
        legacy = _redact_locked_track(track, current_user.id, db)
        # Preserve the authenticated curriculum contract while adding the compact
        # catalogue/detail projection used by the new screen.
        result["levels"] = legacy["levels"]
    return result


# ─── Topic Detail ────────────────────────────────────────────────────────

@router.get("/topics/{topic_id}", response_model=TopicResponse)
def get_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Joined up to the track and filtered on is_active, the same rule GET
    # /tracks/{slug} applies. Without it this was the one read path where
    # deactivating a track did not take content offline: topic ids are
    # small sequential integers, so a caller could enumerate them and pull
    # the full body — lessons, exercises, projects and quizzes — of a track
    # that had been retired or was not published yet.
    #
    # The miss is reported as the ordinary "Topic not found", identical to
    # a topic id that does not exist, so the response does not tell a
    # prober which inactive tracks are real.
    #
    # Enrollment is deliberately NOT checked here. In this product,
    # authentication is the access boundary and enrolment records intent
    # and progress; the track page renders the whole curriculum for any
    # signed-in user. See track_availability.require_track_available,
    # which gates enrolment only.
    topic = (
        db.query(Topic)
        .join(TrackLevel, Topic.level_id == TrackLevel.id)
        .join(CareerTrack, TrackLevel.track_id == CareerTrack.id)
        .options(
            joinedload(Topic.lessons),
            joinedload(Topic.exercises),
            joinedload(Topic.projects),
            joinedload(Topic.quizzes),
        )
        .filter(Topic.id == topic_id, CareerTrack.is_active == True)
        .first()
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    course = course_for_track_topic(db, topic.id)
    if course and not course_access(db, current_user.id, course).has_access:
        # Reuse the track serializer so preview lessons remain readable while
        # every other body is redacted consistently.
        data = TopicResponse.model_validate(topic).model_dump()
        free_exercise_ids, free_quiz_ids = free_preview_content_ids(db, course)
        redact_topic(data, course.slug, free_lesson_ids=free_lesson_ids(db, course),
                     free_exercise_ids=free_exercise_ids, free_quiz_ids=free_quiz_ids)
        return data
    return topic


# ─── Progress Tracking ───────────────────────────────────────────────────

@router.post("/topics/{topic_id}/progress", response_model=ProgressResponse)
def update_progress(
    topic_id: int,
    payload: ProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not db.query(Topic.id).filter(Topic.id == topic_id).first():
        raise HTTPException(status_code=404, detail="Topic not found")
    _validate_progress_targets(db, payload, topic_id=topic_id)
    course = course_for_track_topic(db, topic_id)
    if course:
        if payload.lesson_id is not None:
            require_lesson_access(db, current_user.id, db.query(Lesson).filter(Lesson.id == payload.lesson_id).one())
        elif payload.exercise_id is not None:
            require_content_access(db, current_user.id, db.query(Exercise).filter(Exercise.id == payload.exercise_id).one())
        else:
            require_course_access(db, current_user.id, course)

    # Scoped to current_user.id on both read and write, so there is no id
    # in the request a caller could change to touch someone else's row.
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.topic_id == topic_id,
    ).first()

    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            topic_id=topic_id,
            status=ProgressStatus.in_progress,
            started_at=datetime.utcnow(),
        )
        db.add(progress)

    if payload.lesson_id and payload.lesson_id not in (progress.lessons_completed or []):
        progress.lessons_completed = (progress.lessons_completed or []) + [payload.lesson_id]

    if payload.exercise_id and payload.exercise_id not in (progress.exercises_completed or []):
        progress.exercises_completed = (progress.exercises_completed or []) + [payload.exercise_id]

    if payload.time_spent_minutes:
        progress.time_spent_minutes = min(
            MAX_TOPIC_MINUTES,
            (progress.time_spent_minutes or 0) + payload.time_spent_minutes,
        )

    db.commit()
    db.refresh(progress)
    if course:
        # Working in a course enrolls the learner and moves their lifecycle forward.
        course_enrollment.sync_lifecycle(db, current_user.id, course)
    return progress


@router.get("/topics/{topic_id}/progress", response_model=ProgressResponse)
def get_topic_progress(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    course = course_for_track_topic(db, topic_id)
    if course:
        require_course_access(db, current_user.id, course)
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.topic_id == topic_id,
    ).first()
    if not progress:
        raise HTTPException(status_code=404, detail="No progress found for this topic")
    return progress


# ─── Quiz ────────────────────────────────────────────────────────────────

@router.post("/quizzes/{quiz_id}/submit", response_model=QuizAttemptResponse)
def submit_quiz(
    quiz_id: int,
    payload: QuizSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    require_content_access(db, current_user.id, quiz)

    # Authored content, so a bad shape here is a content bug rather than
    # attacker input — but it must not turn a student's submission into a
    # 500 with an opaque error id and a lost attempt. Anything that isn't a
    # list of questions grades as an empty quiz.
    questions = quiz.questions if isinstance(quiz.questions, list) else []
    correct_count = 0
    feedback = {}
    # Open-ended questions ("type": "open") aren't graded here at all —
    # they go through /practice/quizzes/{id}/questions/{i}/answer instead,
    # since they need an LLM conversation, not an index comparison. Scoring
    # them as MCQ here would silently miscount them (no "correct" index
    # exists for an open question, so a naive comparison can false-positive).
    mcq_count = 0

    for i, question in enumerate(questions):
        # A malformed entry (a bare string, a null) used to reach
        # question.get() and raise AttributeError. Excluded from the
        # denominator rather than awarded — an ungradable question must
        # never become a free mark, and must never cost one either.
        if not isinstance(question, dict):
            feedback[str(i)] = {
                "skipped": True,
                "reason": "this question could not be graded",
            }
            continue

        if question.get("type", "mcq") == "open":
            feedback[str(i)] = {"skipped": True, "reason": "open-ended — graded via AI chat, not this submission"}
            continue

        mcq_count += 1
        user_answer = payload.answers.get(str(i))
        correct = question.get("correct")
        is_correct = user_answer == correct
        if is_correct:
            correct_count += 1
        # `correct_answer` is deliberately absent. The taker learns whether
        # they were right and reads the explanation, but the key itself
        # stays server-side: returning it made one throwaway submission
        # (POST with `{}`) a complete answer-key dump, which is exactly
        # what QuizResponse strips from every read path, and the attempt
        # row then replayed it through GET /quizzes/{id}/attempts forever.
        # Nothing is stored here that isn't safe to hand back.
        feedback[str(i)] = {
            "correct": is_correct,
            "your_answer": user_answer,
            "explanation": question.get("explanation", ""),
        }

    score = (correct_count / mcq_count) * 100 if mcq_count else 0
    passed = score >= quiz.passing_score

    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        answers=payload.answers,
        score=score,
        passed=passed,
        feedback=feedback,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt


@router.get("/quizzes/{quiz_id}/attempts", response_model=List[QuizAttemptResponse])
def my_quiz_attempts(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz:
        require_content_access(db, current_user.id, quiz)
    return (
        db.query(QuizAttempt)
        .filter(QuizAttempt.user_id == current_user.id, QuizAttempt.quiz_id == quiz_id)
        .order_by(QuizAttempt.attempted_at.desc())
        .all()
    )


# ─── Project Submission ──────────────────────────────────────────────────

@router.post("/projects/{project_id}/submit", response_model=ProjectSubmissionResponse)
# LLM-backed but NOT metered by the credit wallet, so the two controls that
# bound inference spend here are both on this decorator stack: the rate
# limit, and require_verified_user. The verification gate lives in
# deduct_credits() for every metered endpoint; this one never calls it, so
# the dependency has to be attached explicitly or an unverified throwaway
# account would reach the provider for free. Metering this through
# deduct_credits() the way /mentor/* does remains the durable fix, but it
# changes what the feature costs a student and is a pricing decision.
#
# The rate limit below is keyed on the client address (limiter.client_key).
# On top of it, an account may have at most PROJECT_REVIEW_LIMIT_PER_DAY
# AI-reviewed submissions in any rolling 24 hours (release decision
# 2026-10-07), so rotating source addresses no longer buys unlimited reviews.
# See _reserve_review_slot.
@limiter.limit("10/hour")
def submit_project(
    request: Request,
    project_id: int,
    payload: ProjectSubmit,
    current_user: User = Depends(require_verified_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    require_content_access(db, current_user.id, project)

    # The code is the submission; the notes are context the reviewer reads
    # alongside it. `code` is required and non-blank by the request schema,
    # so there is no longer a "saved but nothing to review" outcome.
    context = f"Project: {project.title}. {project.description}"
    if payload.description:
        context += f"\nStudent's notes on their approach: {payload.description}"
    user_id = current_user.id

    # Reserve this account's review slot before calling the provider: the row
    # is the count, so a request refused here or failing above never counts,
    # and concurrent requests cannot all see a free slot.
    submission = _reserve_review_slot(db, user_id, project_id, payload)

    ai_review = None
    # A provider outage must not cost the student their submission. The
    # row is what matters — the review is an enrichment, and the client
    # already renders the "saved, no review yet" case.
    try:
        llm = get_llm()
        ai_review = code_review_service.review_code(
            llm=llm,
            code=payload.code,
            language="python",
            context=context,
        )
    except Exception:
        logger.exception(
            "project review failed; saving submission without one",
            extra={"project_id": project_id, "user_id": user_id},
        )

    if ai_review:
        submission.ai_review = ai_review
        submission.score = ai_review.get("score")
        submission.reviewed_at = datetime.utcnow()
        db.commit()
    db.refresh(submission)
    return submission


PROJECT_REVIEW_WINDOW = timedelta(hours=24)
_PROJECT_REVIEW_LOCK = 7201  # pg_advisory_xact_lock namespace for these reservations


def _reserve_review_slot(db: Session, user_id: int, project_id: int, payload: "ProjectSubmit") -> ProjectSubmission:
    """Insert the submission this AI review will fill in, or refuse with 429 when the account
    already has PROJECT_REVIEW_LIMIT_PER_DAY submissions in the rolling 24 hours. The
    per-account advisory lock makes count-and-insert atomic across workers."""
    db.execute(text("SELECT pg_advisory_xact_lock(:ns, :uid)"), {"ns": _PROJECT_REVIEW_LOCK, "uid": user_id})
    since = datetime.now(timezone.utc) - PROJECT_REVIEW_WINDOW
    recent = (
        db.query(ProjectSubmission.submitted_at)
        .filter(ProjectSubmission.user_id == user_id, ProjectSubmission.submitted_at >= since)
        .order_by(ProjectSubmission.submitted_at.asc())
        .all()
    )
    limit = settings.PROJECT_REVIEW_LIMIT_PER_DAY
    if len(recent) >= limit:
        db.rollback()
        # The slot frees when the oldest submission that keeps the count at the limit ages out.
        oldest = recent[len(recent) - limit][0]
        if oldest.tzinfo is None:
            oldest = oldest.replace(tzinfo=timezone.utc)
        retry_after = max(1, int((oldest + PROJECT_REVIEW_WINDOW - datetime.now(timezone.utc)).total_seconds()) + 1)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={"code": "PROJECT_REVIEW_LIMIT", "limit": limit, "window_hours": 24, "retry_after": retry_after},
            headers={"Retry-After": str(retry_after)},
        )
    submission = ProjectSubmission(
        user_id=user_id, project_id=project_id, code=payload.code, description=payload.description,
    )
    db.add(submission)
    db.commit()  # releases the lock; the row now counts for every other request
    return submission


@router.get("/projects/{project_id}/submissions", response_model=List[ProjectSubmissionResponse])
def my_project_submissions(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        require_content_access(db, current_user.id, project)
    return (
        db.query(ProjectSubmission)
        .filter(
            ProjectSubmission.user_id == current_user.id,
            ProjectSubmission.project_id == project_id,
        )
        .order_by(ProjectSubmission.submitted_at.desc())
        .all()
    )


@router.post("/projects/{project_id}/hint", response_model=ProjectHintResponse)
# Metered AND rate-limited, unlike submit_project above. The credit charge
# is the real control on inference spend (see deduct_credits); the rate
# limit just keeps one stuck student from emptying their wallet in a
# minute of frustrated clicking. Same 20/hour the challenge hint uses.
@limiter.limit("20/hour")
def project_hint(
    request: Request,
    project_id: int,
    payload: ProjectHintRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """A Socratic hint for a project the student is stuck on. Costs 1 credit.

    Deliberately mirrors POST /challenges/{slug}/hint rather than inventing
    a second help mechanism — same request shape, same response shape, same
    "guide, don't solve" prompt contract. The one difference is that this
    one goes through wallet_service.deduct_credits instead of adjusting the
    wallet inline, so it gets the row lock, the promo-expiry check and the
    denial metric for free.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    require_content_access(db, current_user.id, project)

    # Charged before the call. Raises 402 with the standard
    # insufficient_credits payload the client already knows how to render.
    deduct_credits(current_user.id, "project_hint", db)

    try:
        result = get_project_hint(
            llm=get_llm(),
            project_title=project.title,
            project_description=project.description,
            objectives=project.objectives or [],
            tech_stack=project.tech_stack or [],
            stuck_on=payload.stuck_on,
            code=payload.code,
            hints_already_given=payload.previous_hints,
            language=payload.language,
            terminology_mode=payload.terminology_mode,
        )
        # Built inside the try: a model answer the response schema rejects is as
        # undelivered as a provider error, and must not become a charged 500.
        response = ProjectHintResponse(**result)
    except Exception:
        # The student paid for a hint they did not get. Refunding is the
        # honest outcome, and it keeps a provider outage from quietly
        # draining wallets one click at a time.
        logger.exception(
            "project hint failed; refunding the credit",
            extra={"project_id": project_id, "user_id": current_user.id},
        )
        refund_credits(
            current_user.id, "project_hint", db,
            reason=f"Refund: hint unavailable for {project.title}",
        )
        raise HTTPException(
            status_code=503,
            detail="The hint service is unavailable right now. Your credit was refunded.",
        )

    return response
