"""
backend/wallet_seed.py
Seeds credit packages and grants 50 free starter credits to all existing users.
Run: python wallet_seed.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import engine, Base, SessionLocal
from app.models.user import User
from app.models.wallet import UserWallet, WalletTransaction, CreditPackage
# import all models so Base.metadata is complete
from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Exercise, Project, Quiz
from app.models.progress import Enrollment, UserProgress, QuizAttempt, ProjectSubmission, MentorSession, UserSkillScore, EngineerScorecard
from app.models.community import Post, PostLike, PostComment, UserFollow
from app.models.exam import Exam, ExamAttempt, ProctoringEvent, Certificate

Base.metadata.create_all(bind=engine)

PACKAGES = [
    {
        "name": "Starter",
        "credits": 100,
        "egp_price": 50.0,
        "bonus_credits": 0,
        "is_popular": False,
        "description": "Perfect for trying out the platform. 100 credits to explore AI mentor, code reviews, and more.",
    },
    {
        "name": "Standard",
        "credits": 350,
        "egp_price": 150.0,
        "bonus_credits": 20,
        "is_popular": True,
        "description": "Most popular. 370 credits (350 + 20 bonus) for serious learners preparing for job applications.",
    },
    {
        "name": "Pro",
        "credits": 800,
        "egp_price": 300.0,
        "bonus_credits": 100,
        "is_popular": False,
        "description": "Full access. 900 credits (800 + 100 bonus) for complete exam prep and full track completion.",
    },
]


def seed_wallet():
    db = SessionLocal()
    try:
        # ── Seed packages ─────────────────────────────────────────────────────
        existing = db.query(CreditPackage).count()
        if existing == 0:
            for pkg in PACKAGES:
                db.add(CreditPackage(**pkg))
            db.commit()
            print(f"✅  Seeded {len(PACKAGES)} credit packages")
        else:
            print(f"ℹ️   Credit packages already exist ({existing}), skipping")

        # ── Grant 50 free starter credits to all existing users ───────────────
        users = db.query(User).all()
        granted = 0
        for user in users:
            wallet = db.query(UserWallet).filter(UserWallet.user_id == user.id).first()
            if not wallet:
                wallet = UserWallet(
                    user_id=user.id,
                    credit_balance=50,
                    lifetime_purchased=50,
                    lifetime_spent=0,
                )
                db.add(wallet)
                db.flush()
                tx = WalletTransaction(
                    wallet_id=wallet.id,
                    transaction_type="bonus",
                    status="confirmed",
                    credits=50,
                    description="Welcome bonus — 50 free credits",
                    action_type=None,
                    balance_after=50,
                )
                db.add(tx)
                granted += 1

        db.commit()
        print(f"✅  Granted 50 welcome credits to {granted} users")

        # ── Print summary ─────────────────────────────────────────────────────
        print("\n📦  Credit packages:")
        for pkg in db.query(CreditPackage).all():
            total = pkg.credits + pkg.bonus_credits
            print(f"    {pkg.name:10} — {pkg.egp_price:.0f} EGP → {total} credits {'⭐ Popular' if pkg.is_popular else ''}")

    except Exception as e:
        db.rollback()
        print(f"❌  Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_wallet()