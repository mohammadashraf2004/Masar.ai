"""
The answer evaluator's feedback policy.

The evaluator used to be told to "nudge them toward it first" on a wrong
answer, which produced vague feedback and no clear verdict. It is now
required to be direct: name the exact mistake, say why it is wrong, name
the concept to reconsider, give one concrete next step — and then stop,
without handing over the worked solution.

WHAT THESE TESTS CAN AND CANNOT PROVE
-------------------------------------
No test here calls a real provider, so none of them proves that a model
*obeys* the policy — that is not unit-testable. What they pin down is the
half that is deterministic and that regressions actually happen in:

  * the policy is genuinely stated in the prompt the model receives
    (a reverted or softened rule fails the suite);
  * the grounding material — question, reference answer, student answer —
    really reaches the model, so feedback *can* be grounded;
  * the reference answer is still marked grading-only, and the two
    legitimate reveal conditions still exist;
  * the structured response contract is unchanged.

Model behaviour itself is verified by evaluating real answers, not here.
"""
import json

import pytest

from app.services.mentor import answer_evaluator_service as svc

QUESTION = "Write a function that returns the average of a list of numbers."
REFERENCE = "def avg(xs):\n    return sum(xs) / len(xs)"
STUDENT_WRONG = "def avg(xs):\n    return sum(xs) / len(xs) + 1"
STUDENT_RIGHT = "def avg(xs):\n    total = 0\n    for x in xs:\n        total += x\n    return total / len(xs)"


class FakeLLM:
    """Captures exactly what the service sends, and replies with whatever
    the test wants back."""

    def __init__(self, reply: str):
        self._reply = reply
        self.system = None
        self.messages = None
        self.max_tokens = None

    def chat(self, system, messages, max_tokens=None):
        self.system = system
        self.messages = messages
        self.max_tokens = max_tokens
        return self._reply


def _json_reply(**overrides) -> str:
    body = {
        "reply": "Your division is right, but you add 1 to the result.",
        "is_correct": False,
        "score": 40,
        "suggested_actions": ["Recheck the return statement"],
    }
    body.update(overrides)
    return json.dumps(body)


def _context(reference=REFERENCE, **overrides) -> dict:
    ctx = {
        "kind": "exercise",
        "title": "Average of a list",
        "prompt": QUESTION,
        "starter_code": "def avg(xs):\n    ...",
        "reference": reference,
        "skill_tags": ["python"],
    }
    ctx.update(overrides)
    return ctx


def _evaluate(llm, user_message=STUDENT_WRONG, history=None, context=None):
    return svc.evaluate_answer(
        llm=llm,
        context=context if context is not None else _context(),
        conversation_history=history or [],
        user_message=user_message,
    )


@pytest.fixture()
def prompt() -> str:
    """The system prompt exactly as the model receives it."""
    llm = FakeLLM(_json_reply())
    _evaluate(llm)
    return llm.system


# ─────────────────────────────────────────────────────────────────────────
# 1. A correct answer is recognised, and not criticised for the sake of it
# ─────────────────────────────────────────────────────────────────────────

def test_a_correct_answer_is_reported_as_correct(monkeypatch):
    llm = FakeLLM(_json_reply(
        reply="Correct — accumulating in a loop and dividing by len(xs) is right.",
        is_correct=True, score=100, suggested_actions=[],
    ))
    result = _evaluate(llm, user_message=STUDENT_RIGHT)

    assert result["is_correct"] is True
    assert result["score"] == 100
    assert result["reply"].startswith("Correct")


def test_the_policy_forbids_manufacturing_criticism(prompt):
    """A correct answer must be allowed to end the exchange."""
    assert "NEVER invent a mistake" in prompt
    assert "Do not manufacture criticism" in prompt
    assert "If the answer is correct, say so plainly and stop" in prompt


def test_a_different_but_valid_approach_counts_as_correct(prompt):
    """STUDENT_RIGHT solves it with a loop rather than sum(); the reference
    is not the only right answer and the prompt has to say so."""
    assert "The\n  reference is one right answer, not the only one." in prompt


# ─────────────────────────────────────────────────────────────────────────
# 2-4. A wrong answer earns a specific mistake, a reason, and a next step
# ─────────────────────────────────────────────────────────────────────────

def test_the_policy_demands_the_specific_mistake(prompt):
    assert "THE MISTAKE" in prompt
    assert "name the exact step, line, term or claim that is wrong" in prompt


def test_the_policy_demands_an_explanation_of_why(prompt):
    assert "WHY IT IS WRONG" in prompt
    assert "the rule or reasoning it violates" in prompt


def test_the_policy_demands_the_concept_to_reconsider(prompt):
    assert "THE CONCEPT TO RECONSIDER" in prompt


def test_the_policy_demands_a_concrete_next_step(prompt):
    assert "THE NEXT STEP" in prompt
    assert "concrete enough to act" in prompt


def test_the_policy_requires_all_four_in_order(prompt):
    """Order matters — mistake, why, concept, next step."""
    assert "give all four of these, in this order" in prompt
    positions = [
        prompt.index("THE MISTAKE"),
        prompt.index("WHY IT IS WRONG"),
        prompt.index("THE CONCEPT TO RECONSIDER"),
        prompt.index("THE NEXT STEP"),
    ]
    assert positions == sorted(positions)


def test_the_policy_rejects_vague_feedback_by_example(prompt):
    """The old rule produced exactly this kind of reply, so the prompt
    carries it as a named counter-example."""
    assert "Think more carefully about your answer." in prompt
    assert "Be direct, never vague" in prompt


def test_the_student_writes_the_correction_themselves(prompt):
    assert "let the student produce the corrected answer themselves" in prompt


# ─────────────────────────────────────────────────────────────────────────
# 5. Being wrong does not unlock the worked solution
# ─────────────────────────────────────────────────────────────────────────

def test_being_wrong_does_not_unlock_the_solution(prompt):
    assert "Do NOT hand over the full reference answer/solution merely because" in prompt
    assert "the worked solution is not" in prompt


def test_the_old_nudge_rule_is_gone(prompt):
    """The rule this change replaced. If it comes back, the feedback goes
    vague again and this is the test that says so."""
    assert "nudge them toward it first" not in prompt


def test_the_two_legitimate_reveal_conditions_are_preserved(prompt):
    """The pre-existing mechanism controlling a legitimate reveal is
    unchanged: an explicit request, or several genuine attempts. Nothing
    was removed or bypassed, and nothing new was added."""
    assert "ONLY when the student explicitly asks for it" in prompt
    assert "made several genuine attempts and are still off" in prompt
    assert "Nothing else unlocks it." in prompt


def test_the_reference_answer_is_still_marked_grading_only():
    """The other half of the same mechanism, in the context block rather
    than the system prompt."""
    block = svc._build_context_block(_context())
    assert "for YOUR grading only — do not paste this to the student unprompted" in block


# ─────────────────────────────────────────────────────────────────────────
# 6. Feedback can be grounded — the material actually reaches the model
# ─────────────────────────────────────────────────────────────────────────

def test_question_reference_and_student_answer_all_reach_the_model():
    llm = FakeLLM(_json_reply())
    _evaluate(llm)

    sent = llm.messages[0]["content"]
    assert QUESTION in sent, "the question never reached the model"
    assert REFERENCE in sent, "the reference answer never reached the model"
    assert STUDENT_WRONG in sent, "the student's answer never reached the model"
    assert "Student's answer:" in sent


def test_grounding_is_demanded_in_the_prompt(prompt):
    assert "Judge only what the student actually wrote" in prompt
    assert "Name or quote the specific part of their answer" in prompt


def test_skill_tags_and_starter_code_are_included_when_present():
    block = svc._build_context_block(_context())
    assert "Starter code given to student:" in block
    assert "Skills being tested: python" in block


def test_a_question_with_no_reference_still_builds_a_clean_block():
    """Not every quiz question carries an explanation — the block must not
    invent an empty 'Reference answer' section."""
    block = svc._build_context_block(_context(reference=None))
    assert "Reference answer" not in block
    assert QUESTION in block


def test_an_unjudgeable_answer_asks_rather_than_guessing(prompt):
    assert "Do not guess a verdict." in prompt


def test_follow_up_turns_carry_the_conversation_not_a_fresh_context():
    """On turn two the history is sent instead of re-sending the whole
    context block — unchanged behaviour, asserted so the grounding tests
    above cannot quietly start covering the wrong path."""
    llm = FakeLLM(_json_reply())
    history = [
        {"role": "user", "content": "first attempt"},
        {"role": "assistant", "content": "not quite"},
    ]
    _evaluate(llm, user_message="second attempt", history=history)

    assert llm.messages == history + [{"role": "user", "content": "second attempt"}]


# ─────────────────────────────────────────────────────────────────────────
# 7. The structured response contract is unchanged
# ─────────────────────────────────────────────────────────────────────────

SCHEMA_KEYS = {"reply", "is_correct", "score", "suggested_actions"}


def test_the_response_schema_is_unchanged():
    result = _evaluate(FakeLLM(_json_reply()))
    assert set(result) == SCHEMA_KEYS
    assert result["reply"] == "Your division is right, but you add 1 to the result."
    assert result["is_correct"] is False
    assert result["score"] == 40
    assert result["suggested_actions"] == ["Recheck the return statement"]


def test_the_prompt_still_specifies_that_exact_schema(prompt):
    for key in SCHEMA_KEYS:
        assert f'"{key}"' in prompt, f"{key} dropped from the documented output shape"


def test_null_verdict_is_still_allowed_mid_conversation():
    result = _evaluate(FakeLLM(_json_reply(is_correct=None, score=None)))
    assert result["is_correct"] is None
    assert result["score"] is None


def test_a_non_json_reply_still_returns_the_schema():
    """Unchanged fallback: a provider that ignores the JSON contract still
    yields a usable answer in the same shape."""
    result = _evaluate(FakeLLM("I could not format that as JSON, but you add 1 too many."))
    assert set(result) == SCHEMA_KEYS
    assert result["reply"] == "I could not format that as JSON, but you add 1 too many."
    assert result["is_correct"] is None
    assert result["suggested_actions"] == svc._FALLBACK_ACTIONS


def test_a_json_array_reply_falls_back_cleanly():
    result = _evaluate(FakeLLM("[1, 2, 3]"))
    assert set(result) == SCHEMA_KEYS
    assert result["is_correct"] is None


def test_the_token_budget_is_unchanged():
    llm = FakeLLM(_json_reply())
    _evaluate(llm)
    assert llm.max_tokens == 700
