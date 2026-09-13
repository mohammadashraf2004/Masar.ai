"""
Concurrency tests for the exam subsystem.

These are NOT both regression tests for the same fix. They establish two
different things:

  1. test_concurrent_start_requests_produce_at_most_one_in_progress_attempt
     is the regression test for a CONFIRMED VULNERABILITY (see GATE.md
     Pass 5, P5-1) and its fix: start_exam's "resume or open a new
     attempt" logic was an unguarded read-then-write, and concurrent
     /start calls could open more than one IN_PROGRESS attempt for one
     user+exam. Fails reliably against the pre-fix code; passes reliably
     post-fix (migration 010_exam_attempt_start_race.py +
     ExamAttempt.__table_args__).

  2. test_verifies_preexisting_certificate_uniqueness_survives_concurrent_submit
     is a VERIFICATION test, not tied to any fix made in this audit.
     submit_exam's state-machine guard has the same read-then-write
     shape, but nothing about submit_exam or the Certificate model was
     changed here — this test exists to confirm, under real concurrency
     rather than by inspection alone, that the UNIQUE constraint already
     on Certificate.attempt_id (present since the original schema) is
     sufficient on its own to prevent a double certificate. It was true
     before this audit touched anything and remains true after.

Both use real threads with independent DB sessions, synchronised with a
Barrier so every worker reaches the racy section at the same instant —
the same pattern as test_wallet_concurrency.py / test_challenge_
enrollment_race.py — rather than the shared-session `client` fixture,
which cannot model genuine concurrent connections. A bare `threading.
Thread` race without the barrier is timing-luck (threads can easily fail
to overlap at the SELECT); the barrier is what makes a reproduction
reliable instead of a one-off.
"""
import threading
import uuid
from datetime import datetime, timezone

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from app.controllers.exam_controller import start_exam, submit_exam
from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.challenge import ExamPayment
from app.models.exam import Certificate, Exam, ExamAttempt, ExamStatus
from app.models.learning import CareerTrack
from app.models.user import User
from app.views.exam import ExamSubmit

RACERS = 10


@pytest.fixture()
def paid_exam(db):
    suffix = uuid.uuid4().hex[:8]
    track = CareerTrack(slug=f"race-exam-track-{suffix}", title="T", estimated_weeks=1)
    db.add(track)
    db.flush()
    exam = Exam(
        track_id=track.id, title="Race Exam", duration_minutes=60,
        passing_score=50, max_attempts=3,
        questions=[
            {"id": 1, "question": "2+2?", "options": ["3", "4"], "correct": 1,
             "explanation": "arithmetic", "points": 1, "type": "mcq"},
        ],
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


def _make_paid_user(db, exam_id) -> int:
    user = User(
        email=f"race-exam-{uuid.uuid4().hex[:12]}@example.com",
        full_name="Race Exam Tester",
        hashed_password=get_password_hash("x"),
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.add(ExamPayment(
        user_id=user.id, exam_id=exam_id, egp_amount=150.0,
        payment_method="fawry", payment_ref=f"race-{uuid.uuid4().hex[:8]}",
        status="confirmed", confirmed_at=datetime.now(timezone.utc),
    ))
    db.commit()
    return user.id


# ─────────────────────────────────────────────────────────────────────────
# 1. Confirmed vulnerability + fix: two concurrent /start calls
# ─────────────────────────────────────────────────────────────────────────

def test_concurrent_start_requests_produce_at_most_one_in_progress_attempt(paid_exam):
    """Regression test for P5-1 (GATE.md Pass 5). Pre-fix, this failed
    reliably (every run, once the Barrier forced real overlap): more
    than one IN_PROGRESS ExamAttempt for one user+exam. Post-fix
    (migration 010 + the IntegrityError handling added to start_exam),
    it passes reliably.
    """
    setup = SessionLocal()
    uid = _make_paid_user(setup, paid_exam.id)
    setup.close()

    results = []
    lock = threading.Lock()
    barrier = threading.Barrier(RACERS)

    def worker():
        session = SessionLocal()
        try:
            u = session.query(User).filter(User.id == uid).one()
            barrier.wait()
            r = start_exam(exam_id=paid_exam.id, current_user=u, db=session)
            with lock:
                results.append(("ok", r))
        except HTTPException as e:
            with lock:
                results.append(("denied", e.status_code))
        except Exception as e:  # pragma: no cover
            with lock:
                results.append(("error", repr(e)))
        finally:
            session.close()

    threads = [threading.Thread(target=worker) for _ in range(RACERS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not [r for r in results if r[0] == "error"], results
    oks = [r for r in results if r[0] == "ok"]
    # Every "ok" response must point at the SAME attempt (start_exam is
    # meant to resume an existing in-progress attempt, not open a second
    # one) — the interesting invariant is not "exactly one 200", it's
    # "never two different attempt ids".
    attempt_ids = {r[1].attempt_id for r in oks}
    assert len(attempt_ids) == 1, f"start_exam opened more than one attempt: {results}"

    check = SessionLocal()
    try:
        in_progress = check.query(ExamAttempt).filter(
            ExamAttempt.user_id == uid,
            ExamAttempt.exam_id == paid_exam.id,
            ExamAttempt.status == ExamStatus.in_progress,
        ).all()
        assert len(in_progress) == 1, (
            f"database holds {len(in_progress)} in-progress attempts for one "
            "user+exam from concurrent /start calls"
        )
    finally:
        check.close()


# ─────────────────────────────────────────────────────────────────────────
# 2. Verification (no fix made here): two concurrent /submit calls
# ─────────────────────────────────────────────────────────────────────────

def test_verifies_preexisting_certificate_uniqueness_survives_concurrent_submit(paid_exam):
    """NOT a regression test for a fix made in this audit — nothing in
    submit_exam or the Certificate model changed. It documents, and
    holds the line on, an invariant that already existed:
    `Certificate.attempt_id` is UNIQUE.

    submit_exam's state-machine guard (`status != in_progress -> 400`)
    is the same kind of unguarded read-then-write as start_exam's, so two
    concurrent submits of the SAME attempt can both read `in_progress`
    before either commits. What is different from P5-1, and why this was
    not filed as a second confirmed vulnerability: if both racers proceed
    to grade and both pass, the pre-existing UNIQUE constraint on
    `Certificate.attempt_id` is what stops a double certificate — and it
    already did, before this audit touched anything. This test proves
    that under real concurrency rather than trusting the schema on faith.

    submit_exam has no try/except of its own around the certificate
    insert — in the real app, a losing racer's IntegrityError is caught
    by main.py's app-wide handler and turned into a safe 409, never a
    500 the caller sees raw. Calling the controller function directly
    (bypassing that middleware, the only way to get real concurrent DB
    sessions instead of the shared-session `client` fixture) means this
    test sees that same IntegrityError as a raised exception instead of
    a 409 response — so it is treated below as the safe-denial outcome it
    actually is, and only a genuinely different kind of exception counts
    as a bug.
    """
    setup = SessionLocal()
    uid = _make_paid_user(setup, paid_exam.id)
    attempt = ExamAttempt(
        exam_id=paid_exam.id, user_id=uid, status=ExamStatus.in_progress,
        started_at=datetime.now(timezone.utc),
    )
    setup.add(attempt)
    setup.commit()
    setup.refresh(attempt)
    attempt_id = attempt.id
    setup.close()

    results = []
    lock = threading.Lock()
    barrier = threading.Barrier(RACERS)

    def worker():
        session = SessionLocal()
        try:
            u = session.query(User).filter(User.id == uid).one()
            barrier.wait()
            r = submit_exam(
                attempt_id=attempt_id,
                payload=ExamSubmit(answers={"1": 1}, time_spent_seconds=10),
                current_user=u,
                db=session,
            )
            with lock:
                results.append(("ok", r))
        except HTTPException as e:
            with lock:
                results.append(("denied", e.status_code))
        except IntegrityError as e:
            # The database invariant doing exactly its job: a losing
            # racer's certificate insert violates the UNIQUE constraint
            # on attempt_id. In the real app this is caught by main.py's
            # IntegrityError handler and turned into a 409 — safe, just
            # not visible as that response shape when calling the
            # controller function directly instead of through the app.
            session.rollback()
            with lock:
                results.append(("db_invariant_blocked", str(e.__class__.__name__)))
        except Exception as e:
            with lock:
                results.append(("error", repr(e)))
        finally:
            session.close()

    threads = [threading.Thread(target=worker) for _ in range(RACERS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Only a genuinely unexpected exception type counts as a bug here —
    # an IntegrityError is the database invariant succeeding, not failing.
    errors = [r for r in results if r[0] == "error"]
    assert not errors, f"submit_exam raised an unexpected error: {errors}"

    check = SessionLocal()
    try:
        certs = check.query(Certificate).filter(Certificate.attempt_id == attempt_id).all()
        assert len(certs) <= 1, f"more than one certificate exists for one attempt: {len(certs)}"

        final = check.query(ExamAttempt).filter(ExamAttempt.id == attempt_id).one()
        assert final.status in (ExamStatus.passed, ExamStatus.failed, ExamStatus.flagged)
    finally:
        check.close()
