"""
backend/seeds/seed_track_ai_developer.py

Orchestrator for the "AI Developer" career track seed data.

The actual level content lives one file per level in
seeds/track_ai_developer/ (level_01_foundations.py ... level_10_ai_evaluation.py)
to keep individual files manageable. This script just imports each level's
LEVEL dict, combines them into LEVELS, and runs the shared seed() function
from seeds/track_ai_developer/common.py.

Run from backend/:
    docker compose exec api python seeds/seed_track_ai_developer.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "track_ai_developer"))

from common import SessionLocal, seed  # noqa: E402
from level_01_foundations import LEVEL as LEVEL_1
from level_02_llm_integration import LEVEL as LEVEL_2
from level_03_rag_knowledge_systems import LEVEL as LEVEL_3
from level_04_prompt_engineering import LEVEL as LEVEL_4
from level_05_embeddings_semantic_search import LEVEL as LEVEL_5
from level_06_advanced_rag import LEVEL as LEVEL_6
from level_07_ai_agents import LEVEL as LEVEL_7
from level_08_deployment_integration import LEVEL as LEVEL_8
from level_09_multimodal_ai import LEVEL as LEVEL_9
from level_10_ai_evaluation_observability import LEVEL as LEVEL_10

LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5, LEVEL_6, LEVEL_7, LEVEL_8, LEVEL_9, LEVEL_10]


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db, LEVELS)
    finally:
        db.close()
