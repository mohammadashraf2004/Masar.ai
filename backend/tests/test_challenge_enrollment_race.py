"""
Regression test for the enroll_challenge TOCTOU closed by migration
009_challenge_enrollment_race.

POST /challenges/{slug}/enroll used to check "not already enrolled",
charge the wallet, and insert the ChallengeAttempt row as three
unserialised steps. N concurrent requests for the same user+challenge
could all pass the check before any of them inserted, so all N could
charge the wallet (deduct_credits' row lock only serialises the charges
against each other, it does not stop there being N of them) and all N
could insert an ENROLLED attempt, double/triple/N-charging one logical
enrolment.

Mirrors test_wallet_concurrency.py's pattern: real threads, each with its
own SQLAlchemy session, calling the controller function directly (the
`client`/`db` fixtures share one session across "requests", which is not
a useful stand-in for genuine concurrent connections).
"""
import threading
import uuid

import pytest
from fastapi import HTTPException

from app.controllers.challenge_controller import enroll_challenge
from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.challenge import ChallengeAttempt, ChallengeDifficulty, ChallengeProject, ChallengeStatus
from app.models.user import User
from app.models.wallet import UserWallet
from app.services.wallet.wallet_service import add_credits

ENROLL_COST = 25
RACERS = 10


@pytest.fixture()
def challenge(db) -> ChallengeProject:
    ch = ChallengeProject(
        title="Race Challenge",
        slug=f"race-chal-{uuid.uuid4().hex[:8]}",
        description="Clean it.",
        difficulty=ChallengeDifficulty.beginner,
        credit_cost=ENROLL_COST,
        passing_score=70.0,
        max_attempts=3,
        is_active=True,
        dirty_dataset=[{"a": 1}],
        dataset_description="x",
        grading_rubric=[{"criterion": "x", "weight": 100}],
        hints=[],
        tags=[],
    )
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return ch


def test_concurrent_enroll_requests_produce_exactly_one_active_attempt(challenge):
    setup = SessionLocal()
    user = User(
        email=f"race-enroll-{uuid.uuid4().hex[:12]}@example.com",
        full_name="Race Enroll",
        hashed_password=get_password_hash("x"),
        is_verified=True,
    )
    setup.add(user)
    setup.commit()
    setup.refresh(user)
    uid = user.id
    add_credits(uid, ENROLL_COST * RACERS, setup, description="race test funds")
    setup.close()

    results = []
    lock = threading.Lock()

    def worker():
        session = SessionLocal()
        try:
            u = session.query(User).filter(User.id == uid).one()
            r = enroll_challenge(slug=challenge.slug, current_user=u, db=session)
            with lock:
                results.append(("ok", r))
        except HTTPException as e:
            with lock:
                results.append(("denied", e.status_code))
        except Exception as e:  # pragma: no cover - would indicate a real bug
            with lock:
                results.append(("error", repr(e)))
        finally:
            session.close()

    threads = [threading.Thread(target=worker) for _ in range(RACERS)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    oks = [r for r in results if r[0] == "ok"]
    assert len(oks) == 1, f"expected exactly one successful enrolment, got: {results}"
    assert not [r for r in results if r[0] == "error"], results
    # A loser is denied one of two ways depending on scheduling: the
    # ordinary pre-check (400, "already enrolled" — no charge made at
    # all) if it runs after the winner already committed, or the
    # unique-index collision (503, caught by enroll_challenge's own
    # except block and refunded) if it raced into the TOCTOU window
    # ahead of the winner's insert. Both are safe outcomes; what the
    # assertions below actually pin down is that neither leaves a second
    # active attempt or a net double-charge behind.
    assert all(r[1] in (400, 503) for r in results if r[0] == "denied"), results

    check = SessionLocal()
    try:
        active_attempts = check.query(ChallengeAttempt).filter(
            ChallengeAttempt.user_id == uid,
            ChallengeAttempt.challenge_id == challenge.id,
            ChallengeAttempt.status == ChallengeStatus.enrolled,
        ).all()
        assert len(active_attempts) == 1, (
            f"database holds {len(active_attempts)} active enrolments for one "
            "user+challenge — the unique index did not serialise the race"
        )

        wallet = check.query(UserWallet).filter(UserWallet.user_id == uid).one()
        assert wallet.credit_balance == ENROLL_COST * RACERS - ENROLL_COST, (
            "wallet was net-charged for more than the one surviving enrolment "
            "— a loser's charge was not fully refunded"
        )
    finally:
        check.close()
