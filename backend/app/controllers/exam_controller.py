import uuid
from datetime import datetime, timedelta, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.core import security_log
from app.core.authz import is_admin
from app.db.session import get_db
from app.models.challenge import ExamPayment
from app.models.user import User
from app.models.exam import (
    Exam, ExamAttempt, ProctoringEvent,
    Certificate, ExamStatus, ViolationType,
)
from app.views.exam import (
    ExamInfoResponse, ExamSessionResponse, ExamQuestion,
    ExamSubmit, ViolationReport,
    ExamResultResponse, QuestionResult,
    CertificateResponse, AttemptSummary,
)
from app.core.security import get_current_user

router = APIRouter(prefix="/exams", tags=["Exams & Certification"])

# Max violations before attempt is flagged regardless of score
MAX_VIOLATIONS_BEFORE_FLAG = 5

# Clock skew / last-request-in-flight allowance on the exam deadline.
SUBMIT_GRACE_SECONDS = 60


def _has_paid_for_exam(db: Session, user: User, exam_id: int) -> bool:
    """Certification exams are paid (see exam_payment_controller /
    payments_controller). Until now this was checked ONLY by the frontend
    before it called /start — so anyone who could issue an HTTP request
    could take a paid exam, pass it, and be issued a real certificate for
    free. Access control belongs here, where a client can't skip it."""
    if is_admin(user):
        return True
    return db.query(ExamPayment).filter(
        ExamPayment.user_id == user.id,
        ExamPayment.exam_id == exam_id,
        ExamPayment.status == "confirmed",
    ).first() is not None


def _require_paid_exam(db: Session, user: User, exam_id: int) -> None:
    if not _has_paid_for_exam(db, user, exam_id):
        security_log.authz_denied(
            user_id=user.id, path=f"/exams/{exam_id}", reason="exam_payment_required",
        )
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="This certification exam requires a confirmed payment before it can be started.",
        )


def _deadline(attempt: ExamAttempt, exam: Exam) -> datetime:
    started = attempt.started_at
    if started.tzinfo is None:
        started = started.replace(tzinfo=timezone.utc)
    return started + timedelta(minutes=exam.duration_minutes)


# ─── List exams for a track ───────────────────────────────────────────────────

@router.get("/track/{track_id}", response_model=List[ExamInfoResponse])
def list_exams_for_track(
    track_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    exams = db.query(Exam).filter(
        Exam.track_id == track_id,
        Exam.is_active == True,
    ).all()

    result = []
    for exam in exams:
        attempts = db.query(ExamAttempt).filter(
            ExamAttempt.exam_id == exam.id,
            ExamAttempt.user_id == current_user.id,
        ).all()

        attempts_used = len(attempts)
        passed_already = any(a.passed for a in attempts)
        can_attempt = (
            not passed_already and
            attempts_used < exam.max_attempts
        )

        result.append(ExamInfoResponse(
            id=exam.id,
            track_id=exam.track_id,
            title=exam.title,
            description=exam.description,
            duration_minutes=exam.duration_minutes,
            passing_score=exam.passing_score,
            max_attempts=exam.max_attempts,
            total_questions=len(exam.questions),
            attempts_used=attempts_used,
            can_attempt=can_attempt,
        ))

    return result


# ─── Start exam (creates attempt) ─────────────────────────────────────────────

@router.post("/{exam_id}/start", response_model=ExamSessionResponse)
def start_exam(
    exam_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.is_active == True).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    _require_paid_exam(db, current_user, exam_id)

    # Check eligibility
    attempts = db.query(ExamAttempt).filter(
        ExamAttempt.exam_id == exam_id,
        ExamAttempt.user_id == current_user.id,
    ).all()

    if any(a.passed for a in attempts):
        raise HTTPException(status_code=400, detail="You already passed this exam")

    if len(attempts) >= exam.max_attempts:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum attempts ({exam.max_attempts}) reached"
        )

    # Check for in-progress attempt
    in_progress = next(
        (a for a in attempts if a.status == ExamStatus.in_progress), None
    )
    if in_progress:
        # Resume existing attempt — but only while it is still inside its
        # own window. Without this an attempt sits "in progress" forever,
        # which turns a 60-minute timed exam into an untimed one: start
        # it, go research every answer, come back tomorrow and resume.
        if datetime.now(timezone.utc) > _deadline(in_progress, exam):
            in_progress.status = ExamStatus.failed
            in_progress.passed = False
            in_progress.score = in_progress.score or 0
            in_progress.submitted_at = datetime.now(timezone.utc)
            db.commit()
            raise HTTPException(
                status_code=400,
                detail="Your previous attempt ran out of time and has been closed.",
            )
        attempt = in_progress
    else:
        attempt = ExamAttempt(
            exam_id=exam_id,
            user_id=current_user.id,
            status=ExamStatus.in_progress,
            started_at=datetime.now(timezone.utc),
        )
        db.add(attempt)
        try:
            db.commit()
        except IntegrityError:
            # A concurrent /start for this same user+exam won the race —
            # `uq_exam_attempts_one_in_progress` (migration 010) is what
            # actually stops two IN_PROGRESS rows existing at once; this
            # is just turning that into the same "resume" outcome the
            # sequential path already gives, instead of a bare 409. Two
            # simultaneous requests both wanting to start the same exam
            # should both land in the one attempt that won, not one of
            # them erroring.
            db.rollback()
            attempt = db.query(ExamAttempt).filter(
                ExamAttempt.exam_id == exam_id,
                ExamAttempt.user_id == current_user.id,
                ExamAttempt.status == ExamStatus.in_progress,
            ).first()
            if attempt is None:
                # The winner's attempt was already resolved (finished or
                # expired) between our failed insert and this re-read —
                # vanishingly unlikely, but fail closed with a message the
                # caller can act on rather than a raw 500.
                raise HTTPException(
                    status_code=409,
                    detail="Could not start this exam right now — please try again.",
                )
        else:
            db.refresh(attempt)

    # Strip correct answers before sending to client
    questions = [
        ExamQuestion(
            id=q["id"],
            question=q["question"],
            options=q["options"],
            points=q.get("points", 1),
            type=q.get("type", "mcq"),
        )
        for q in exam.questions
    ]

    return ExamSessionResponse(
        attempt_id=attempt.id,
        exam_id=exam.id,
        title=exam.title,
        duration_minutes=exam.duration_minutes,
        questions=questions,
        started_at=attempt.started_at,
    )


# ─── Report proctoring violation ──────────────────────────────────────────────

@router.post("/attempts/{attempt_id}/violation", status_code=200)
def report_violation(
    attempt_id: int,
    payload: ViolationReport,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.status == ExamStatus.in_progress,
    ).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Active attempt not found")

    event = ProctoringEvent(
        attempt_id=attempt_id,
        violation=payload.violation,
        description=payload.description,
    )
    db.add(event)

    attempt.violations_count += 1
    if payload.violation == ViolationType.tab_switch:
        attempt.tab_switches += 1
    elif payload.violation in (ViolationType.face_not_visible, ViolationType.multiple_faces):
        attempt.face_warnings += 1

    db.commit()

    return {
        "violations_count": attempt.violations_count,
        "warning": attempt.violations_count >= MAX_VIOLATIONS_BEFORE_FLAG - 1,
    }


# ─── Submit exam ──────────────────────────────────────────────────────────────

@router.post("/attempts/{attempt_id}/submit", response_model=ExamResultResponse)
def submit_exam(
    attempt_id: int,
    payload: ExamSubmit,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id,
    ).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.status != ExamStatus.in_progress:
        raise HTTPException(status_code=400, detail="Attempt already submitted")

    exam = db.query(Exam).filter(Exam.id == attempt.exam_id).first()

    # The exam was paid for at /start; re-checking here means a refund or
    # a reversed/charged-back payment can't be outrun by an attempt that
    # was already open.
    _require_paid_exam(db, current_user, attempt.exam_id)

    now = datetime.now(timezone.utc)
    if now > _deadline(attempt, exam) + timedelta(seconds=SUBMIT_GRACE_SECONDS):
        attempt.status = ExamStatus.failed
        attempt.passed = False
        attempt.score = 0
        attempt.submitted_at = now
        db.commit()
        raise HTTPException(status_code=400, detail="Time limit exceeded — this attempt is closed.")

    # Elapsed time is computed from the server-recorded start, never taken
    # from payload.time_spent_seconds: that number is supplied by the same
    # client being timed, so it can claim any duration it likes.
    started = attempt.started_at if attempt.started_at.tzinfo else attempt.started_at.replace(tzinfo=timezone.utc)
    elapsed_seconds = max(0, int((now - started).total_seconds()))

    questions = exam.questions

    # Grade
    total_points = sum(q.get("points", 1) for q in questions)
    earned_points = 0
    question_results = []

    for q in questions:
        qid = str(q["id"])
        user_answer = payload.answers.get(qid)
        correct = q["correct"]
        is_correct = user_answer == correct
        if is_correct:
            earned_points += q.get("points", 1)

        question_results.append(QuestionResult(
            question_id=q["id"],
            question=q["question"],
            your_answer=user_answer,
            correct_answer=correct,
            is_correct=is_correct,
            explanation=q.get("explanation", ""),
            points=q.get("points", 1),
        ))

    score = round((earned_points / total_points) * 100, 1) if total_points > 0 else 0
    passed = score >= exam.passing_score

    # Flag if too many violations even if passed
    if passed and attempt.violations_count >= MAX_VIOLATIONS_BEFORE_FLAG:
        final_status = ExamStatus.flagged
        passed = False
    elif passed:
        final_status = ExamStatus.passed
    else:
        final_status = ExamStatus.failed

    attempt.status = final_status
    attempt.answers = payload.answers
    attempt.score = score
    attempt.passed = passed
    attempt.submitted_at = now
    attempt.time_spent_seconds = elapsed_seconds

    # Issue certificate if passed
    cert_id = None
    if final_status == ExamStatus.passed:
        cert_id = str(uuid.uuid4())
        cert = Certificate(
            attempt_id=attempt.id,
            user_id=current_user.id,
            track_id=exam.track_id,
            certificate_id=cert_id,
            score=score,
        )
        db.add(cert)

    db.commit()

    return ExamResultResponse(
        attempt_id=attempt.id,
        status=final_status,
        score=score,
        passed=passed,
        passing_score=exam.passing_score,
        violations_count=attempt.violations_count,
        tab_switches=attempt.tab_switches,
        face_warnings=attempt.face_warnings,
        time_spent_seconds=elapsed_seconds,
        question_results=question_results,
        certificate_id=cert_id,
    )


# ─── Get attempt result ───────────────────────────────────────────────────────

@router.get("/attempts/{attempt_id}/result", response_model=ExamResultResponse)
def get_result(
    attempt_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = db.query(ExamAttempt).filter(
        ExamAttempt.id == attempt_id,
        ExamAttempt.user_id == current_user.id,
    ).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.status == ExamStatus.in_progress:
        raise HTTPException(status_code=400, detail="Exam still in progress")

    exam = db.query(Exam).filter(Exam.id == attempt.exam_id).first()
    questions = exam.questions
    answers = attempt.answers or {}

    question_results = []
    for q in questions:
        qid = str(q["id"])
        user_answer = answers.get(qid)
        correct = q["correct"]
        question_results.append(QuestionResult(
            question_id=q["id"],
            question=q["question"],
            your_answer=user_answer,
            correct_answer=correct,
            is_correct=user_answer == correct,
            explanation=q.get("explanation", ""),
            points=q.get("points", 1),
        ))

    cert = db.query(Certificate).filter(
        Certificate.attempt_id == attempt_id
    ).first()

    return ExamResultResponse(
        attempt_id=attempt.id,
        status=attempt.status,
        score=attempt.score or 0,
        passed=attempt.passed or False,
        passing_score=exam.passing_score,
        violations_count=attempt.violations_count,
        tab_switches=attempt.tab_switches,
        face_warnings=attempt.face_warnings,
        time_spent_seconds=attempt.time_spent_seconds,
        question_results=question_results,
        certificate_id=cert.certificate_id if cert else None,
    )


# ─── My attempts ─────────────────────────────────────────────────────────────

@router.get("/my-attempts", response_model=List[AttemptSummary])
def my_attempts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id
    ).order_by(ExamAttempt.started_at.desc()).all()


# ─── Verify certificate (public) ─────────────────────────────────────────────

@router.get("/certificates/{certificate_id}", response_model=CertificateResponse)
def verify_certificate(
    certificate_id: str,
    db: Session = Depends(get_db),
):
    cert = db.query(Certificate).options(
        joinedload(Certificate.user),
        joinedload(Certificate.track),
    ).filter(Certificate.certificate_id == certificate_id).first()

    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    return CertificateResponse(
        certificate_id=cert.certificate_id,
        track_title=cert.track.title,
        user_name=cert.user.full_name,
        score=cert.score,
        issued_at=cert.issued_at,
        is_valid=cert.is_valid,
    )


# ─── My certificates ─────────────────────────────────────────────────────────

@router.get("/my-certificates", response_model=List[CertificateResponse])
def my_certificates(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    certs = db.query(Certificate).options(
        joinedload(Certificate.track),
    ).filter(
        Certificate.user_id == current_user.id,
        Certificate.is_valid == True,
    ).all()

    return [
        CertificateResponse(
            certificate_id=c.certificate_id,
            track_title=c.track.title,
            user_name=current_user.full_name,
            score=c.score,
            issued_at=c.issued_at,
            is_valid=c.is_valid,
        )
        for c in certs
    ]