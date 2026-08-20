"""
Seed runner — run from backend/ directory:
    python seed.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal, engine, Base

# ── Import ALL models before create_all so SQLAlchemy
#    can resolve every relationship() string reference ──
import app.models.user         # noqa: F401
import app.models.learning     # noqa: F401
import app.models.progress     # noqa: F401
import app.models.community    # noqa: F401
import app.models.wallet       # noqa: F401
import app.models.auth_token   # noqa: F401
import app.models.challenge    # noqa: F401
import app.models.exam         # noqa: F401
import app.models.tool_course  # noqa: F401

Base.metadata.create_all(bind=engine)

from seeds.tracks_all import seed_all_tracks

db = SessionLocal()
try:
    print("Seeding all tracks...\n")
    seed_all_tracks(db)
except Exception as e:
    db.rollback()
    print(f"\n✗ Failed: {e}")
    raise
finally:
    db.close()