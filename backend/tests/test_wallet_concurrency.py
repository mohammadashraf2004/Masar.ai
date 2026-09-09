"""
Regression test for the double-spend race condition found and fixed in
app/services/wallet/wallet_service.py: concurrent deduct_credits() calls
against the same wallet used to be able to both pass the balance check
before either committed.
"""
import threading
import uuid

from app.db.session import SessionLocal
from app.models.user import User
from app.models.wallet import UserWallet, WalletTransaction
from app.core.security import get_password_hash
from app.services.wallet.wallet_service import deduct_credits, get_or_create_wallet


def test_concurrent_deducts_never_go_negative(db):
    setup = SessionLocal()
    user = User(
        email=f"race-{uuid.uuid4().hex[:12]}@example.com",
        full_name="Race Test",
        hashed_password=get_password_hash("x"),
        # deduct_credits refuses unverified accounts; this test is about the
        # row lock, not the verification gate.
        is_verified=True,
    )
    setup.add(user)
    setup.commit()
    setup.refresh(user)
    uid = user.id

    wallet = get_or_create_wallet(uid, setup)
    wallet.credit_balance = 10  # mentor_chat costs 2 -> exactly 5 should succeed
    setup.commit()
    setup.close()

    results = []
    lock = threading.Lock()

    def worker():
        session = SessionLocal()
        try:
            r = deduct_credits(uid, "mentor_chat", session)
            with lock:
                results.append(("ok", r["balance_after"]))
        except Exception as e:
            with lock:
                results.append(("fail", str(e)))
        finally:
            session.close()

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    ok = [r for r in results if r[0] == "ok"]
    assert len(ok) == 5, f"expected exactly 5 successful deducts, got {len(ok)}: {results}"

    check = SessionLocal()
    final = check.query(UserWallet).filter(UserWallet.user_id == uid).first()
    assert final.credit_balance == 0, f"balance went to {final.credit_balance}, should be exactly 0"

    check.query(WalletTransaction).filter(WalletTransaction.wallet_id == final.id).delete()
    check.delete(final)
    check.commit()
    check.query(User).filter(User.id == uid).delete()
    check.commit()
    check.close()
