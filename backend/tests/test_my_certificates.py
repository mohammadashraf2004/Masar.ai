"""
GET /exams/my-certificates must say which exam each certificate was earned in.

The exam picker in the frontend marks an exam "Certified" by looking its id up in
the holder's certificates. The serializer never returned an exam id, so that lookup
matched nothing, ever, and the picker fell back on attempt history alone. The public
verification lookup, on the other hand, must not start returning it.
"""
import uuid
from datetime import datetime, timezone

import pytest

from app.controllers.exam_controller import my_certificates, verify_certificate
from app.core.security import get_password_hash
from app.models.exam import Certificate, Exam, ExamAttempt, ExamStatus
from app.models.learning import CareerTrack
from app.models.user import User


def _certificate(db, *, valid: bool = True):
    suffix = uuid.uuid4().hex[:8]
    track = CareerTrack(slug=f"cert-list-track-{suffix}", title=f"Track {suffix}", estimated_weeks=1)
    db.add(track)
    db.flush()
    exam = Exam(
        track_id=track.id, title="Certification exam", duration_minutes=30, passing_score=50, max_attempts=3,
        questions=[{"id": 1, "question": "2+2?", "options": ["3", "4"], "correct": 1, "points": 1, "type": "mcq"}],
    )
    user = User(
        email=f"cert-list-{suffix}@example.com", full_name="Layan Al-Harbi",
        hashed_password=get_password_hash("x"), is_verified=True,
    )
    db.add_all([exam, user])
    db.flush()
    attempt = ExamAttempt(
        exam_id=exam.id, user_id=user.id, status=ExamStatus.passed, score=88.0, passed=True,
        started_at=datetime.now(timezone.utc), submitted_at=datetime.now(timezone.utc),
    )
    db.add(attempt)
    db.flush()
    cert = Certificate(
        attempt_id=attempt.id, user_id=user.id, track_id=track.id,
        certificate_id=str(uuid.uuid4()), score=88.0, is_valid=valid,
    )
    db.add(cert)
    db.commit()
    return user, exam, cert


def test_the_holders_list_names_the_exam_each_certificate_was_earned_in(db):
    user, exam, cert = _certificate(db)

    listed = my_certificates(current_user=user, db=db)

    assert [c.certificate_id for c in listed] == [cert.certificate_id]
    assert listed[0].exam_id == exam.id


def test_the_public_lookup_does_not_expose_the_exam_id(db):
    _, _, cert = _certificate(db)

    looked_up = verify_certificate(certificate_id=cert.certificate_id, db=db)

    assert looked_up.certificate_id == cert.certificate_id
    assert looked_up.exam_id is None


def test_a_revoked_certificate_is_not_listed_so_it_cannot_mark_an_exam_certified(db):
    user, _, _ = _certificate(db, valid=False)

    assert my_certificates(current_user=user, db=db) == []
