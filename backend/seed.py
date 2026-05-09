"""
Seed runner
-----------
Run from the backend directory:
    python seed.py

Each seeds/ module seeds one logical section and is safe to call independently.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import SessionLocal, engine, Base
from app.models.learning import CareerTrack

Base.metadata.create_all(bind=engine)

from seeds.track import seed_track
from seeds.level1_foundations import seed_level1
from seeds.level2_data_ml import seed_level2
from seeds.level3_deep_learning import seed_level3
from seeds.level4_ai_engineering import seed_level4
from seeds.level5_production import seed_level5


def run():
    db = SessionLocal()
    try:
        if db.query(CareerTrack).filter(CareerTrack.slug == "ai-engineer").first():
            print("Track already exists — skipping seed.")
            return

        track = seed_track(db)
        seed_level1(db, track)
        seed_level2(db, track)
        seed_level3(db, track)
        seed_level4(db, track)
        seed_level5(db, track)

        db.commit()
        print("✅ All seed data inserted successfully.")
    except Exception as e:
        db.rollback()
        print(f"❌ Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()
