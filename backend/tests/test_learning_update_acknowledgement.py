"""
Acknowledging a product announcement changes nothing about the learner's roadmap or skills.

Kept beside the other learning tests (it needs the seeded catalogue, and shares their ordering)
rather than with the account tests in test_update_acknowledgements.py.
"""
from app.core import releases

from tests.learning_fixtures import *  # noqa: F401,F403
from tests.test_update_acknowledgements import ACK, _legacy_account


def test_acknowledging_leaves_the_roadmap_and_the_skills_exactly_as_they_were(learn_client, learn_db, learn_catalog):
    user = _legacy_account(learn_client, learn_db)
    h = user["headers"]
    assert learn_client.put("/api/v1/learning/my-profile", headers=h, json={
        "level": "intermediate", "fields": ["nlp"], "career_goal": "ai-engineer",
    }).status_code == 200
    assert learn_client.put("/api/v1/learning/my-skills", headers=h, json={"skills": ["llms", "embeddings"]}).status_code == 200
    assert learn_client.put("/api/v1/learning/my-path", headers=h, json={}).status_code == 200

    before = {
        "path": learn_client.get("/api/v1/learning/my-path", headers=h).json(),
        "skills": learn_client.get("/api/v1/learning/my-skills", headers=h).json(),
        "gaps": learn_client.get("/api/v1/learning/my-skill-gaps", headers=h).json(),
    }
    assert learn_client.post(ACK.format(releases.WHATS_NEW), headers=h).status_code == 200
    assert learn_client.post(ACK.format(releases.WHATS_NEW), headers=h).status_code == 200
    after = {
        "path": learn_client.get("/api/v1/learning/my-path", headers=h).json(),
        "skills": learn_client.get("/api/v1/learning/my-skills", headers=h).json(),
        "gaps": learn_client.get("/api/v1/learning/my-skill-gaps", headers=h).json(),
    }
    assert after == before
