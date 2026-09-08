import logging

from fastapi import APIRouter, Depends, HTTPException, Request, status
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
from app.core.security import get_current_user
from app.services.content.track_availability import require_track_available
from app.core.limiter import limiter
from app.services import get_llm, code_review_service
from app.services.mentor.mentor_service import get_project_hint
from app.services.wallet.wallet_service import deduct_credits, refund_credits
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tracks", tags=["Learning Tracks"])

# A single topic's accumulated self-reported study time. Progress numbers
# feed the engineer scorecard, which is the thing employers are shown, so
# they get the same "don't trust the client" treatment as anything else.
MAX_TOPIC_MINUTES = 100_000


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
        belongs = db.query(Exercise.id).filter(
            Exercise.id == payload.exercise_id,
            Exercise.topic_id == topic_id,
        ).first()
        if not belongs:
            raise HTTPException(status_code=400, detail="That exercise does not belong to this topic")


# ─── Career Tracks ──────────────────────────────────────────────────────

@router.get("/", response_model=List[CareerTrackSummary])
def list_tracks(db: Session = Depends(get_db)):
    return db.query(CareerTrack).filter(CareerTrack.is_active == True).all()


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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Authenticated: this returns the track's entire body of lesson
    content, not a marketing summary. GET /tracks/ stays public for the
    catalogue; the full curriculum is for signed-in users. (The frontend
    already gates every track page behind useAuth, so this closes a hole
    rather than changing behaviour.)"""
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
    return track


# ─── Topic Detail ────────────────────────────────────────────────────────

@router.get("/topics/{topic_id}", response_model=TopicResponse)
def get_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    topic = (
        db.query(Topic)
        .options(
            joinedload(Topic.lessons),
            joinedload(Topic.exercises),
            joinedload(Topic.projects),
            joinedload(Topic.quizzes),
        )
        .filter(Topic.id == topic_id)
        .first()
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
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
    return progress


@router.get("/topics/{topic_id}/progress", response_model=ProgressResponse)
def get_topic_progress(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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

    questions = quiz.questions
    correct_count = 0
    feedback = {}
    # Open-ended questions ("type": "open") aren't graded here at all —
    # they go through /practice/quizzes/{id}/questions/{i}/answer instead,
    # since they need an LLM conversation, not an index comparison. Scoring
    # them as MCQ here would silently miscount them (no "correct" index
    # exists for an open question, so a naive comparison can false-positive).
    mcq_count = 0

    for i, question in enumerate(questions):
        if question.get("type", "mcq") == "open":
            feedback[str(i)] = {"skipped": True, "reason": "open-ended — graded via AI chat, not this submission"}
            continue

        mcq_count += 1
        user_answer = payload.answers.get(str(i))
        correct = question.get("correct")
        is_correct = user_answer == correct
        if is_correct:
            correct_count += 1
        feedback[str(i)] = {
            "correct": is_correct,
            "your_answer": user_answer,
            "correct_answer": correct,
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
    return (
        db.query(QuizAttempt)
        .filter(QuizAttempt.user_id == current_user.id, QuizAttempt.quiz_id == quiz_id)
        .order_by(QuizAttempt.attempted_at.desc())
        .all()
    )


# ─── Project Submission ──────────────────────────────────────────────────

@router.post("/projects/{project_id}/submit", response_model=ProjectSubmissionResponse)
# The only LLM-backed endpoint in the app that isn't metered by the credit
# wallet, so a rate limit is the sole thing standing between one account
# and unbounded inference spend. See the security report — metering this
# through deduct_credits() the way /mentor/* does is the durable fix.
@limiter.limit("10/hour")
def submit_project(
    request: Request,
    project_id: int,
    payload: ProjectSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # The code is the submission; the notes are context the reviewer reads
    # alongside it. `code` is required and non-blank by the request schema,
    # so there is no longer a "saved but nothing to review" outcome.
    context = f"Project: {project.title}. {project.description}"
    if payload.description:
        context += f"\nStudent's notes on their approach: {payload.description}"

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
            extra={"project_id": project_id, "user_id": current_user.id},
        )

    submission = ProjectSubmission(
        user_id=current_user.id,
        project_id=project_id,
        code=payload.code,
        description=payload.description,
        ai_review=ai_review,
        score=ai_review.get("score") if ai_review else None,
        reviewed_at=datetime.utcnow() if ai_review else None,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@router.get("/projects/{project_id}/submissions", response_model=List[ProjectSubmissionResponse])
def my_project_submissions(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
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

    return ProjectHintResponse(**result)