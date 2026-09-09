"""
Exam payment references cannot be squatted.

`payment_ref` is typed in by the student after paying offline (Fawry /
InstaPay / mobile wallet). The submit handler used to reject any reference
string that already existed on ANY row in ANY state, which meant anyone
could permanently deny a reference to the person who had actually paid for
it: claim the string first, and the real payer can never file their claim.
The squatter's row stayed `pending` and granted them nothing, so this was
denial of service rather than theft — but the victim's money was gone.

The invariant that actually needed enforcing is narrower:

    at most one CONFIRMED payment per reference

Pending claims are deliberately allowed to collide, because a pending row
is only an unverified assertion; an admin adjudicates against the
provider's records. That shifts the risk to the admin endpoint — confirming
the wrong claimant would be worse than the original DoS — so the
contested case is a 409 with the candidates rather than an arbitrary pick.

See migration 008 and exam_payment_controller.
"""
import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.challenge import ExamPayment
from app.models.exam import Exam
from app.models.learning import CareerTrack
from app.models.user import User, UserRole

STRONG_PASSWORD = "correcthorsebatterystaple"


# ─── helpers ──────────────────────────────────────────────────────────────

def _register(client, prefix="pay"):
    email = f"{prefix}-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Payment Tester", "password": STRONG_PASSWORD,
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    return body["access_token"], body["user"]["id"]


def _auth(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _make_admin(db, user_id: int) -> None:
    db.query(User).filter(User.id == user_id).update({User.role: UserRole.admin})
    db.commit()


@pytest.fixture()
def exam(db):
    """A minimal exam row to hang payments off. Exams belong to a track,
    so one comes along for the ride."""
    track = CareerTrack(
        slug=f"pay-track-{uuid.uuid4().hex[:8]}",
        title="Payment Track",
        estimated_weeks=1,
    )
    db.add(track)
    db.commit()
    db.refresh(track)

    row = Exam(
        track_id=track.id,
        title=f"Cert {uuid.uuid4().hex[:8]}",
        description="test exam",
        questions=[],
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def _submit(client, token, exam_id, ref, method="fawry"):
    return client.post(
        "/api/v1/exam-payments/submit",
        headers=_auth(token),
        json={"exam_id": exam_id, "payment_method": method, "payment_ref": ref},
    )


def _ref() -> str:
    return f"FAWRY-{uuid.uuid4().hex[:10].upper()}"


# ─── the attack ───────────────────────────────────────────────────────────

def test_squatter_cannot_block_the_real_payer(client, db, exam):
    """THE regression. An attacker files a claim on a reference first; the
    person who actually paid must still be able to file theirs."""
    attacker_token, _ = _register(client, "attacker")
    payer_token, payer_id = _register(client, "payer")
    ref = _ref()

    squat = _submit(client, attacker_token, exam.id, ref)
    assert squat.status_code == 200, squat.text

    victim = _submit(client, payer_token, exam.id, ref)
    assert victim.status_code == 200, (
        "the real payer was locked out of their own payment reference"
    )

    rows = db.query(ExamPayment).filter(ExamPayment.payment_ref == ref).all()
    assert len(rows) == 2
    assert {r.status for r in rows} == {"pending"}
    assert payer_id in {r.user_id for r in rows}


def test_squatting_grants_the_squatter_nothing(client, db, exam):
    """A pending claim must not confer exam access on its own."""
    attacker_token, attacker_id = _register(client, "attacker")
    ref = _ref()
    assert _submit(client, attacker_token, exam.id, ref).status_code == 200

    status = client.get(
        f"/api/v1/exam-payments/status/{exam.id}", headers=_auth(attacker_token),
    )
    assert status.status_code == 200
    assert status.json()["paid"] is False


# ─── legitimate behaviour is preserved ────────────────────────────────────

def test_legitimate_payer_submits_successfully(client, db, exam):
    token, user_id = _register(client)
    ref = _ref()

    resp = _submit(client, token, exam.id, ref)
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "pending"
    assert body["ref"] == ref

    row = db.query(ExamPayment).filter(ExamPayment.payment_ref == ref).one()
    assert row.user_id == user_id
    assert row.status == "pending"


def test_same_user_resubmitting_their_own_reference_is_refused(client, db, exam):
    """Idempotency for the honest double-click: one payment, one claim
    row, and a clear message rather than a silent duplicate."""
    token, _ = _register(client)
    ref = _ref()

    assert _submit(client, token, exam.id, ref).status_code == 200

    again = _submit(client, token, exam.id, ref)
    assert again.status_code == 400
    assert "already submitted" in again.json()["detail"].lower()

    assert db.query(ExamPayment).filter(ExamPayment.payment_ref == ref).count() == 1


def test_reference_already_confirmed_is_refused_for_everyone(client, db, exam):
    """Once a reference has actually paid for an exam, it is spent — this
    is the duplicate protection that had to survive the fix."""
    first_token, first_id = _register(client, "first")
    second_token, _ = _register(client, "second")
    ref = _ref()

    assert _submit(client, first_token, exam.id, ref).status_code == 200
    db.query(ExamPayment).filter(ExamPayment.payment_ref == ref).update({"status": "confirmed"})
    db.commit()

    resp = _submit(client, second_token, exam.id, ref)
    assert resp.status_code == 400
    assert "already been used" in resp.json()["detail"].lower()


# ─── admin adjudication ───────────────────────────────────────────────────

def test_admin_confirms_an_uncontested_reference(client, db, exam):
    """The ordinary case — one claim — must be unchanged by all of this."""
    payer_token, payer_id = _register(client, "payer")
    admin_token, admin_id = _register(client, "admin")
    _make_admin(db, admin_id)
    ref = _ref()
    assert _submit(client, payer_token, exam.id, ref).status_code == 200

    resp = client.post(
        f"/api/v1/exam-payments/admin/confirm/{ref}", headers=_auth(admin_token),
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["user_id"] == payer_id

    db.expire_all()
    row = db.query(ExamPayment).filter(ExamPayment.payment_ref == ref).one()
    assert row.status == "confirmed"
    assert row.confirmed_by == "admin"


def test_contested_reference_is_not_confirmed_arbitrarily(client, db, exam):
    """The failure mode introduced by allowing duplicate pending claims:
    confirming whichever row came back first would hand exam access to
    whoever squatted fastest. It must stop and ask instead."""
    attacker_token, attacker_id = _register(client, "attacker")
    payer_token, payer_id = _register(client, "payer")
    admin_token, admin_id = _register(client, "admin")
    _make_admin(db, admin_id)
    ref = _ref()

    assert _submit(client, attacker_token, exam.id, ref).status_code == 200
    assert _submit(client, payer_token, exam.id, ref).status_code == 200

    resp = client.post(
        f"/api/v1/exam-payments/admin/confirm/{ref}", headers=_auth(admin_token),
    )
    assert resp.status_code == 409, resp.text
    detail = resp.json()["detail"]
    assert detail["error"] == "ambiguous_payment_reference"
    candidate_users = {c["user_id"] for c in detail["candidates"]}
    assert candidate_users == {attacker_id, payer_id}

    db.expire_all()
    rows = db.query(ExamPayment).filter(ExamPayment.payment_ref == ref).all()
    assert {r.status for r in rows} == {"pending"}, "a contested reference was confirmed"


def test_admin_can_confirm_the_right_claimant_by_payment_id(client, db, exam):
    """The escape hatch the 409 points at: having checked the provider's
    records, the admin names the claim to confirm."""
    attacker_token, attacker_id = _register(client, "attacker")
    payer_token, payer_id = _register(client, "payer")
    admin_token, admin_id = _register(client, "admin")
    _make_admin(db, admin_id)
    ref = _ref()

    assert _submit(client, attacker_token, exam.id, ref).status_code == 200
    assert _submit(client, payer_token, exam.id, ref).status_code == 200

    payer_row = db.query(ExamPayment).filter(
        ExamPayment.payment_ref == ref, ExamPayment.user_id == payer_id,
    ).one()

    resp = client.post(
        f"/api/v1/exam-payments/admin/confirm/{ref}?payment_id={payer_row.id}",
        headers=_auth(admin_token),
    )
    assert resp.status_code == 200, resp.text
    assert resp.json()["user_id"] == payer_id

    db.expire_all()
    payer_after = db.query(ExamPayment).filter(ExamPayment.id == payer_row.id).one()
    attacker_after = db.query(ExamPayment).filter(
        ExamPayment.payment_ref == ref, ExamPayment.user_id == attacker_id,
    ).one()
    assert payer_after.status == "confirmed"
    assert attacker_after.status == "pending", "the squatter's claim was confirmed too"


def test_squatter_cannot_be_confirmed_after_the_payer_was(client, db, exam):
    """The losing claim must not be confirmable afterwards — that would be
    two exam accesses off one real payment."""
    attacker_token, attacker_id = _register(client, "attacker")
    payer_token, payer_id = _register(client, "payer")
    admin_token, admin_id = _register(client, "admin")
    _make_admin(db, admin_id)
    ref = _ref()

    assert _submit(client, attacker_token, exam.id, ref).status_code == 200
    assert _submit(client, payer_token, exam.id, ref).status_code == 200
    payer_row = db.query(ExamPayment).filter(
        ExamPayment.payment_ref == ref, ExamPayment.user_id == payer_id,
    ).one()
    attacker_row = db.query(ExamPayment).filter(
        ExamPayment.payment_ref == ref, ExamPayment.user_id == attacker_id,
    ).one()

    ok = client.post(
        f"/api/v1/exam-payments/admin/confirm/{ref}?payment_id={payer_row.id}",
        headers=_auth(admin_token),
    )
    assert ok.status_code == 200, ok.text

    second = client.post(
        f"/api/v1/exam-payments/admin/confirm/{ref}?payment_id={attacker_row.id}",
        headers=_auth(admin_token),
    )
    assert second.status_code == 409, second.text

    db.expire_all()
    assert db.query(ExamPayment).filter(
        ExamPayment.payment_ref == ref, ExamPayment.status == "confirmed",
    ).count() == 1


def test_admin_confirm_still_requires_admin(client, db, exam):
    payer_token, _ = _register(client, "payer")
    other_token, _ = _register(client, "other")
    ref = _ref()
    assert _submit(client, payer_token, exam.id, ref).status_code == 200

    resp = client.post(
        f"/api/v1/exam-payments/admin/confirm/{ref}", headers=_auth(other_token),
    )
    assert resp.status_code == 403


# ─── the database is the real guarantee ───────────────────────────────────

def test_database_refuses_two_confirmed_rows_for_one_reference(client, db, exam):
    """The application checks are a courtesy; migration 008's partial
    unique index is what holds when two admins confirm concurrently and
    both application-level checks pass before either commits."""
    attacker_token, _ = _register(client, "attacker")
    payer_token, _ = _register(client, "payer")
    ref = _ref()
    assert _submit(client, attacker_token, exam.id, ref).status_code == 200
    assert _submit(client, payer_token, exam.id, ref).status_code == 200

    rows = db.query(ExamPayment).filter(ExamPayment.payment_ref == ref).all()
    assert len(rows) == 2

    for row in rows:
        row.status = "confirmed"
    with pytest.raises(IntegrityError):
        db.commit()
    db.rollback()


def test_pending_duplicates_are_allowed_by_the_database(client, db, exam):
    """The other half of that index: it must be partial. A plain unique
    index on payment_ref would reintroduce the squatting bug at the schema
    level, where no application fix could reach it."""
    attacker_token, _ = _register(client, "attacker")
    payer_token, _ = _register(client, "payer")
    ref = _ref()

    assert _submit(client, attacker_token, exam.id, ref).status_code == 200
    assert _submit(client, payer_token, exam.id, ref).status_code == 200
    assert db.query(ExamPayment).filter(ExamPayment.payment_ref == ref).count() == 2
