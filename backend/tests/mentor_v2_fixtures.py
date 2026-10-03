"""Shared setup for the Mentor v2 endpoint tests.

The provider is always a FakeLLM: it returns scripted replies, records
every prompt it was sent, and never makes a network call.
"""
import json
import uuid

from app.db.session import SessionLocal
from app.models.learning import CareerTrack, DifficultyLevel, Exercise, Lesson, Quiz, Topic, TrackLevel
from app.models.wallet import TransactionType, UserWallet, WalletTransaction
from tests.conftest import verify_registered

MESSAGE = "/api/v1/mentor/message"
QUIZ_ANSWER = "/api/v1/mentor/quiz/answer"

SOLUTION = (
    'def chat(msg, thread_id="user-42"):\n'
    '    config = {"configurable": {"thread_id": thread_id}}\n'
    '    return graph.invoke({"messages": [msg]}, config)\n'
)
CORRECT_OPTION = "After every node in the graph"
QUIZ_QUESTION = {
    "question": "When does LangGraph call the checkpointer?",
    "options": [CORRECT_OPTION, "Only at the end of graph.invoke", "Only when a tool is called"],
    "correct": 0,
    "explanation": "Saving a snapshot per node is what lets a run resume mid-graph.",
    "skill": "Checkpointers",
}
LESSON_BODY = (
    "# Persistent memory\n\n"
    "Every call to graph.invoke starts from an empty state, so the agent forgets the previous message.\n\n"
    "## The checkpointer\n\n"
    "The checkpointer captures a snapshot of the graph state and stores it under a key called thread_id. "
    "Calling the graph again with the same thread_id resumes from the last snapshot.\n\n"
    "```python\ngraph = builder.compile(checkpointer=MemorySaver())\n```\n"
)


class FakeLLM:
    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    def chat(self, system, messages, max_tokens):
        self.calls.append({"system": system, "messages": messages, "max_tokens": max_tokens})
        if not self.replies:
            raise AssertionError("FakeLLM called more times than scripted")
        nxt = self.replies.pop(0)
        if isinstance(nxt, Exception):
            raise nxt
        return nxt

    def prompts(self) -> str:
        return "\n".join(c["system"] + "\n" + "\n".join(m["content"] for m in c["messages"]) for c in self.calls)


def blocks_json(*blocks) -> str:
    return json.dumps({"blocks": list(blocks)}, ensure_ascii=False)


def install_llm(monkeypatch, replies) -> FakeLLM:
    from app.controllers import mentor_v2_controller

    fake = FakeLLM(replies)
    monkeypatch.setattr(mentor_v2_controller, "get_llm", lambda: fake)
    return fake


def register(client):
    email = f"mv2-{uuid.uuid4().hex[:12]}@example.com"
    resp = client.post("/api/v1/auth/register", json={
        "email": email, "full_name": "Mentor V2", "password": "correct-horse-battery-staple-7",
    })
    assert resp.status_code == 201, resp.text
    body = resp.json()
    verify_registered(client, body["user"]["id"])
    return {"Authorization": f"Bearer {body['access_token']}"}, body["user"]["id"]


def make_course() -> dict:
    db = SessionLocal()
    try:
        track = CareerTrack(slug=f"mv2-{uuid.uuid4().hex[:8]}", title="AI Engineer", estimated_weeks=1)
        db.add(track)
        db.flush()
        level = TrackLevel(track_id=track.id, title="Agents", order=1)
        db.add(level)
        db.flush()
        topic = Topic(level_id=level.id, title="LangGraph", slug=f"lg-{uuid.uuid4().hex[:8]}", order=1,
                      difficulty=DifficultyLevel.beginner, estimated_hours=1.0,
                      prerequisite_ids=[], skill_tags=["langgraph"])
        db.add(topic)
        db.flush()
        lesson6 = Lesson(topic_id=topic.id, title="Conditional edges", order=6,
                         content="Conditional edges route the graph to different nodes based on state.")
        lesson7 = Lesson(topic_id=topic.id, title="Persistent memory", order=7, content=LESSON_BODY)
        db.add_all([lesson6, lesson7])
        exercise = Exercise(topic_id=topic.id, title="Agent with memory",
                            description="Make the second test pass: the agent must remember the user's name.",
                            starter_code="def chat(msg):\n    return graph.invoke({'messages': [msg]})\n",
                            solution_code=SOLUTION)
        quiz = Quiz(topic_id=topic.id, title="Memory check", passing_score=70, questions=[QUIZ_QUESTION])
        db.add_all([exercise, quiz])
        db.commit()
        return {"topic": topic.id, "lesson": lesson7.id, "lesson6": lesson6.id,
                "exercise": exercise.id, "quiz": quiz.id}
    finally:
        db.close()


def wallet(db, user_id) -> UserWallet:
    db.expire_all()
    return db.query(UserWallet).filter(UserWallet.user_id == user_id).one()


def txs(db, user_id, kind: TransactionType):
    return (
        db.query(WalletTransaction)
        .join(UserWallet, WalletTransaction.wallet_id == UserWallet.id)
        .filter(UserWallet.user_id == user_id, WalletTransaction.transaction_type == kind)
        .all()
    )
