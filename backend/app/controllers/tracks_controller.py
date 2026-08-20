from fastapi import APIRouter, Depends, HTTPException, status
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
    TopicResponse,
)
from app.core.security import get_current_user
from app.services import get_llm, code_review_service
from datetime import datetime

router = APIRouter(prefix="/tracks", tags=["Learning Tracks"])


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
    return (
        db.query(Enrollment)
        .options(joinedload(Enrollment.track))
        .filter(Enrollment.user_id == current_user.id, Enrollment.is_active == True)
        .all()
    )


# ─── Track detail — AFTER all literal routes ────────────────────────────

@router.get("/{slug}", response_model=CareerTrackResponse)
def get_track(slug: str, db: Session = Depends(get_db)):
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
        progress.time_spent_minutes = (progress.time_spent_minutes or 0) + payload.time_spent_minutes

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

    for i, question in enumerate(questions):
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

    score = (correct_count / len(questions)) * 100 if questions else 0
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


# ─── Project Submission ──────────────────────────────────────────────────

@router.post("/projects/{project_id}/submit", response_model=ProjectSubmissionResponse)
def submit_project(
    project_id: int,
    payload: ProjectSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    ai_review = None
    if payload.description:
        llm = get_llm()
        ai_review = code_review_service.review_code(
            llm=llm,
            code=payload.description,
            language="python",
            context=f"Project: {project.title}. {project.description}",
        )

    submission = ProjectSubmission(
        user_id=current_user.id,
        project_id=project_id,
        github_url=payload.github_url,
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