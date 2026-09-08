"""
The answer evaluator's feedback policy.

The evaluator answers in a fixed four-part shape — a status line, then
Result / Why / Fix / Learning point — and section 3 must carry the EXACT
corrected code for the student's own mistake. It used to be told to "nudge
them toward it first", which produced feedback like "review how strings
work": true, and useless to a student who cannot act on it.

WHAT THESE TESTS CAN AND CANNOT PROVE
-------------------------------------
No test in this module calls a real provider, so none of them proves that a
model *obeys* the policy. They verify that the instructions reach the model
and that the plumbing around them is right — which is where regressions
actually happen:

  * every rule is genuinely present in the prompt the model receives, so a
    reverted or softened policy fails the suite;
  * the grounding material — question, reference answer, student answer —
    really reaches the model, so feedback *can* be grounded;
  * the reference solution is still gated, and still marked grading-only;
  * the structured response contract is unchanged.

For actual generated feedback on real student answers, see
tests/test_answer_evaluator_live.py, which is opt-in and calls a provider.
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
        "reply": "❌ Incorrect\n\n1. Result\n...\n2. Why\n...\n3. Fix\n...\n4. Learning point\n...",
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


def _flat(text: str) -> str:
    """Collapse runs of whitespace, so an assertion about a sentence does not
    also assert where that sentence happens to wrap in the source."""
    return " ".join(text.split())


@pytest.fixture()
def flat(prompt) -> str:
    """The prompt with its line wrapping flattened away."""
    return _flat(prompt)


# ─────────────────────────────────────────────────────────────────────────
# 1-3. The three status markers
# ─────────────────────────────────────────────────────────────────────────

def test_an_incorrect_answer_requires_the_incorrect_marker(prompt):
    assert "❌ Incorrect" in prompt
    assert "the answer does not satisfy the exercise" in prompt


def test_a_partially_correct_answer_requires_its_own_marker(prompt):
    assert "⚠️ Partially correct" in prompt
    assert "part of it is right, something specific is still wrong" in prompt


def test_a_correct_answer_requires_the_correct_marker(prompt):
    assert "✅ Correct" in prompt
    assert "the answer satisfies the exercise" in prompt


def test_the_status_line_comes_first_and_stands_alone(flat):
    assert "Open with a status line." in flat
    assert "It is a line of its OWN, containing the marker AND its word" in flat
    # Measured live: the model merged the two into "❌ 1. Result" and dropped
    # the word, because the multiple-errors example showed that shape.
    assert 'Writing "❌ 1. Result" is WRONG.' in flat


# ─────────────────────────────────────────────────────────────────────────
# 4-8. The four sections, and what each must contain
# ─────────────────────────────────────────────────────────────────────────

SECTIONS = ["1. Result", "2. Why", "3. Fix", "4. Learning point"]


def test_all_four_sections_are_required(prompt):
    for section in SECTIONS:
        assert section in prompt, f"{section} missing from the required structure"


def test_the_four_sections_are_required_in_order(prompt):
    positions = [prompt.index(s) for s in SECTIONS]
    assert positions == sorted(positions)
    assert "in this order, with these exact headings" in prompt


def test_result_requires_the_specific_code_location(flat):
    assert "name the exact line, expression, variable or section" in flat
    assert "quote ONLY that fragment of the student's code" in flat


def test_why_requires_a_brief_grounded_explanation(flat):
    assert "Why that code behaves incorrectly" in flat
    assert "the one programming concept needed to understand this specific error" in flat
    assert "Do not restate section 1." in flat


def test_fix_requires_the_exact_corrected_code(flat):
    """The heart of this change — identifying the error is not enough."""
    assert "The EXACT corrected code, in a fenced block." in flat
    assert "you MUST show the corrected code in section 3" in flat
    assert "Identifying the error is not enough" in flat


def test_learning_point_requires_exactly_one_takeaway(prompt):
    assert "Exactly ONE short takeaway, one sentence." in prompt


# ─────────────────────────────────────────────────────────────────────────
# 9-11. Vagueness, questions, and minimal changes
# ─────────────────────────────────────────────────────────────────────────

def test_vague_feedback_is_explicitly_forbidden(flat):
    assert "Never be vague." in flat
    for banned in (
        "Think more carefully about your answer",
        "your logic needs improvement",
        "try reviewing how strings work",
    ):
        assert banned in flat, f"missing named counter-example: {banned!r}"


def test_unnecessary_follow_up_questions_are_forbidden(flat):
    for banned in (
        "what would you like it to say?",
        "would you like me to show you the fix?",
        "can you try again?",
        "shall I give you a hint?",
        "what do you think the problem is?",
    ):
        assert banned in flat, f"missing banned question: {banned!r}"
    assert "Ask a question ONLY when the exercise genuinely requires information" in flat


def test_minimal_corrections_are_required(flat):
    assert "SMALLEST POSSIBLE CHANGE" in flat
    assert "Correct the student's code; do not replace it." in flat
    assert "never a rewritten program" in flat
    assert "Keep their variable names, their structure and their approach." in flat


# ─────────────────────────────────────────────────────────────────────────
# 12-13. Grounding, and not criticising a correct answer
# ─────────────────────────────────────────────────────────────────────────

def test_inventing_requirements_is_forbidden(flat):
    assert "NEVER invent a requirement the exercise does not state." in flat
    # The concrete case from the rewrite-for-tone exercise.
    assert "do not fault them for omitting a menu" in flat


def test_inventing_mistakes_is_forbidden(flat):
    assert "NEVER invent a mistake." in flat
    assert "A different implementation from the reference is not wrong" in flat
    assert "the reference is one right answer, not the only one" in flat


def test_the_reference_is_not_treated_as_a_checklist(flat):
    """Measured live: the model downgraded a perfectly valid answer to
    ⚠️ Partially correct for omitting a detail that appeared only in the
    reference, never in the exercise."""
    assert "THE REFERENCE IS NOT A CHECKLIST." in flat
    assert "never against details that happen to appear in the reference answer" in flat
    assert "is the single most common way to get this wrong" in flat


def test_the_fix_must_not_copy_the_reference_wording(flat):
    """Also measured live: section 3 pasted the reference's exact sentence,
    handing the student the answer to paste back."""
    assert "Compose it yourself in your own words - never copy the reference answer's wording verbatim" in flat
    assert "Write your own minimal equivalent" in flat


def test_a_correct_answer_is_not_artificially_criticised(flat):
    assert "Do not invent a problem." in flat
    assert "Do not rewrite correct code." in flat
    assert 'Fix says "No changes are needed."' in flat


def test_excessive_praise_is_forbidden(flat):
    assert "Do not pile on praise" in flat


def test_an_unjudgeable_answer_asks_rather_than_guessing(flat):
    assert "say exactly what is unclear and ask for that one thing." in flat
    assert "Do not guess a verdict." in flat


def test_a_correct_answer_is_reported_as_correct():
    """Schema side: a true verdict passes through untouched."""
    llm = FakeLLM(_json_reply(
        reply="✅ Correct\n\n1. Result\nYour answer is correct.\n2. Why\n…\n3. Fix\nNo changes are needed.\n4. Learning point\n…",
        is_correct=True, score=100, suggested_actions=[],
    ))
    result = _evaluate(llm, user_message=STUDENT_RIGHT)
    assert result["is_correct"] is True
    assert result["score"] == 100
    assert result["reply"].startswith("✅ Correct")


# ─────────────────────────────────────────────────────────────────────────
# 14-15. Partially correct, and multiple errors
# ─────────────────────────────────────────────────────────────────────────

def test_partially_correct_must_separate_right_from_wrong(flat):
    assert "state explicitly which part is right AND the exact remaining problem" in flat
    assert "so the two are never blurred together" in flat


def test_multiple_errors_are_ordered_and_not_repetitive(flat):
    assert "MULTIPLE ERRORS" in flat
    assert "order the errors by importance" in flat
    assert "Do NOT repeat an explanation that already covered another error" in flat


def test_multiple_errors_still_carry_one_status_line(flat):
    """Each issue is numbered, but the status line is written once, first —
    not folded into every heading."""
    assert "write the single status line first as always" in flat
    assert "Issue 1" in flat and "Issue 2" in flat


def test_extra_issues_must_not_be_manufactured(flat):
    assert "Do NOT manufacture extra issues to make the feedback longer." in flat
    assert "Report only errors that actually exist." in flat


# ─────────────────────────────────────────────────────────────────────────
# 16-17. The old rule is gone; the reference solution is still protected
# ─────────────────────────────────────────────────────────────────────────

def test_the_old_nudge_rule_is_gone(prompt):
    """The rule this change replaced. If it comes back, the evaluator stops
    showing corrections and this is the test that says so."""
    assert "nudge them toward it first" not in prompt


def test_withholding_an_obvious_correction_is_forbidden(flat):
    assert "Do NOT withhold an obvious correction to make the student guess." in flat
    assert "identify error -> understand why -> see the exact correction" in flat


def test_the_minimal_fix_and_the_full_solution_are_distinguished(flat):
    """The distinction the whole change rests on: correcting the student's
    own line is always allowed; dumping the answer sheet is not."""
    assert "The minimal corrected code for the student's OWN mistake - always show this" in flat
    assert "The complete reference solution to the whole exercise - do NOT paste this merely" in flat
    assert "section 3 is not a way around it" in flat


def test_the_two_legitimate_reveal_conditions_are_preserved(flat):
    """The pre-existing mechanism controlling a legitimate reveal is
    unchanged: an explicit request, or several genuine attempts. Nothing was
    removed, bypassed, or added."""
    assert "ONLY when the student explicitly asks for it" in flat
    assert "made several genuine attempts and are still off" in flat
    assert "Nothing else unlocks it" in flat


def test_the_reference_answer_is_still_marked_grading_only():
    """The other half of the same mechanism, in the context block rather
    than the system prompt."""
    block = svc._build_context_block(_context(), STUDENT_WRONG)
    assert "YOUR grading only — do not paste this to the student unprompted" in block


# ─────────────────────────────────────────────────────────────────────────
# Grounding material actually reaches the model
# ─────────────────────────────────────────────────────────────────────────

def test_question_reference_and_student_answer_all_reach_the_model():
    llm = FakeLLM(_json_reply())
    _evaluate(llm)

    sent = llm.messages[0]["content"]
    assert QUESTION in sent, "the question never reached the model"
    assert REFERENCE in sent, "the reference answer never reached the model"
    assert STUDENT_WRONG in sent, "the student's answer never reached the model"
    assert "THE STUDENT'S ANSWER" in sent


# ─────────────────────────────────────────────────────────────────────────
# The reference answer is evidence, not a specification
#
# Measured failure this addresses: a valid instruction string that differed
# from the reference was marked ⚠️ Partially correct for omitting wording
# that appeared only in the reference, and section 3 pasted the reference's
# own sentence back. See tests/test_answer_evaluator_live.py.
# ─────────────────────────────────────────────────────────────────────────

def test_the_context_orders_requirements_answer_then_reference():
    """Ordering is the fix, not just the labels. The requirements come
    first, the student's answer second, and the reference last — so the two
    things that were being diffed are no longer adjacent."""
    block = svc._build_context_block(_context(), STUDENT_WRONG)

    req = block.index("1. EXERCISE REQUIREMENTS")
    answer = block.index("2. THE STUDENT'S ANSWER")
    ref = block.index("3. REFERENCE ANSWER")
    assert req < answer < ref, "context sections are out of priority order"


def test_the_requirements_are_labelled_as_what_to_grade_against():
    block = svc._build_context_block(_context(), STUDENT_WRONG)
    assert "this is what you grade AGAINST" in block
    # The requirements used to be labelled, weakly, "Prompt:".
    assert "Task:" in block


def test_the_context_calls_the_reference_one_acceptable_solution():
    block = svc._build_context_block(_context(), STUDENT_WRONG)
    assert "ONE acceptable solution, supporting evidence only" in block
    assert "This is ONE way to satisfy the exercise" in block


def test_the_context_denies_the_reference_specification_status():
    block = svc._build_context_block(_context(), STUDENT_WRONG)
    assert "NOT a specification and NOT a checklist" in block
    assert "does not have to match it" in block
    assert "Grade against section 1, not against this" in block


def test_the_context_says_a_different_valid_answer_is_correct():
    block = svc._build_context_block(_context(), STUDENT_WRONG)
    assert "A different implementation that satisfies section 1 is ✅ Correct." in block


def test_the_context_still_works_without_a_student_answer():
    """The student's answer is optional so the exercise half can be built
    and inspected on its own; nothing should crash or emit an empty
    section 2."""
    block = svc._build_context_block(_context())
    assert "1. EXERCISE REQUIREMENTS" in block
    assert "2. THE STUDENT'S ANSWER" not in block
    assert "3. REFERENCE ANSWER" in block


def test_the_prompt_states_the_evaluation_priority_order(flat):
    assert "Weigh them in this order, highest authority first:" in flat
    order = [
        flat.index("1. THE EXERCISE'S STATED REQUIREMENTS"),
        flat.index("2. THE STUDENT'S ACTUAL ANSWER"),
        flat.index("3. The reference answer"),
    ]
    assert order == sorted(order)
    assert "supporting evidence only, ONE example" in flat


def test_the_prompt_forbids_failing_an_answer_for_differing(flat):
    assert "NEVER mark an answer incorrect - and never downgrade it to ⚠️ Partially correct - solely because it differs from the reference" in flat
    assert "Textual similarity to the reference is not the test; satisfying the exercise is." in flat


def test_case_one_a_valid_alternative_is_correct(flat):
    assert "CASE 1 - the answer DIFFERS from the reference and SATISFIES the exercise." in flat
    assert "briefly say why THEIR approach satisfies the requirements" in flat
    assert "do not suggest they change their approach to match it" in flat


def test_case_two_a_genuine_bug_is_still_identified(flat):
    assert "CASE 2 - the answer has a GENUINE bug" in flat
    assert "Name THEIR bug and correct THEIR code." in flat
    assert '"It differs from the reference" is never the reason' in flat


def test_case_three_explicit_exercise_requirements_are_authoritative(flat):
    assert "CASE 3 - the EXERCISE ITSELF explicitly requires something specific" in flat
    assert "That requirement is authoritative and you enforce it." in flat
    assert 'quote the requirement FROM THE EXERCISE, never "the reference does it this way"' in flat


def test_the_fix_section_must_address_the_students_own_error(flat):
    assert "Section 3 corrects the student's OWN error, in their own style" in flat


def test_the_fix_section_must_not_paste_reference_code(flat):
    assert "NEVER copy the reference answer's code or wording into section 3." in flat
    assert "only when that exact code genuinely IS the minimal correction for their specific bug" in flat


def test_grounding_sources_are_enumerated_in_the_prompt(flat):
    assert "Use only the exercise, the student's submitted answer, the reference answer" in flat
    assert "the exercise's actual stated requirements" in flat


def test_skill_tags_and_starter_code_are_included_when_present():
    block = svc._build_context_block(_context())
    assert "Starter code given to student:" in block
    assert "Skills being tested: python" in block


def test_a_question_with_no_reference_still_builds_a_clean_block():
    """Not every quiz question carries an explanation — the block must not
    invent an empty reference section."""
    block = svc._build_context_block(_context(reference=None), STUDENT_WRONG)
    assert "reference" not in block.lower()
    assert QUESTION in block
    assert STUDENT_WRONG in block


def test_follow_up_turns_carry_the_conversation_not_a_fresh_context():
    """On turn two the history is sent instead of re-sending the whole
    context block — unchanged behaviour, asserted so the grounding tests
    above cannot quietly start covering the wrong path."""
    llm = FakeLLM(_json_reply())
    history = [
        {"role": "user", "content": "first attempt"},
        {"role": "assistant", "content": "❌ Incorrect …"},
    ]
    _evaluate(llm, user_message="second attempt", history=history)

    assert llm.messages == history + [{"role": "user", "content": "second attempt"}]


# ─────────────────────────────────────────────────────────────────────────
# 18. The structured response contract is unchanged
# ─────────────────────────────────────────────────────────────────────────

SCHEMA_KEYS = {"reply", "is_correct", "score", "suggested_actions"}


def test_the_response_schema_is_unchanged():
    result = _evaluate(FakeLLM(_json_reply()))
    assert set(result) == SCHEMA_KEYS
    assert result["is_correct"] is False
    assert result["score"] == 40
    assert result["suggested_actions"] == ["Recheck the return statement"]


def test_the_four_part_feedback_travels_in_the_reply_field():
    """No new field was added for it — the structure lives in `reply`, which
    is what the frontend already renders."""
    result = _evaluate(FakeLLM(_json_reply()))
    for section in SECTIONS:
        assert section in result["reply"]


def test_the_prompt_still_specifies_that_exact_schema(prompt):
    for key in SCHEMA_KEYS:
        assert f'"{key}"' in prompt, f"{key} dropped from the documented output shape"


def test_null_verdict_is_still_allowed_mid_conversation():
    """No status marker means no verdict was given — a clarifying question,
    not a judgement. That still comes back as null."""
    result = _evaluate(FakeLLM(_json_reply(
        reply="Which of the two loops did you mean? I cannot tell from this.",
        is_correct=None, score=None,
    )))
    assert result["is_correct"] is None
    assert result["score"] is None


# ─── is_correct derived from the status line ──────────────────────────────
# The model is told to keep `is_correct` consistent with the status marker
# and does so only about half the time (measured live), which left the UI
# showing no verdict badge under a reply that plainly said "❌ Incorrect".

@pytest.mark.parametrize("marker, expected", [
    ("✅ Correct", True),
    ("❌ Incorrect", False),
    ("⚠️ Partially correct", False),
])
def test_a_null_verdict_is_recovered_from_the_status_line(marker, expected):
    result = _evaluate(FakeLLM(_json_reply(
        reply=f"{marker}\n\n1. Result\n…\n2. Why\n…\n3. Fix\n…\n4. Learning point\n…",
        is_correct=None,
    )))
    assert result["is_correct"] is expected


@pytest.mark.parametrize("marker, stated", [
    ("✅ Correct", False),
    ("❌ Incorrect", True),
])
def test_an_explicit_verdict_always_wins_over_the_marker(marker, stated):
    """Derivation fills a gap; it never overrules the model."""
    result = _evaluate(FakeLLM(_json_reply(reply=f"{marker}\n\n1. Result\n…", is_correct=stated)))
    assert result["is_correct"] is stated


def test_a_marker_appearing_later_in_prose_is_not_a_verdict():
    """Only the first line is a status line. A ✅ inside the explanation is
    discussion, and must not flip a wrong answer to correct."""
    result = _evaluate(FakeLLM(_json_reply(
        reply="❌ Incorrect\n\n1. Result\nThe ✅ Correct version would divide by len(xs).",
        is_correct=None,
    )))
    assert result["is_correct"] is False


def test_derivation_survives_a_missing_variation_selector():
    """The warning sign is U+26A0 with an optional U+FE0F. Both spellings
    must read as the same verdict."""
    for marker in ("⚠️ Partially correct", "⚠ Partially correct"):
        result = _evaluate(FakeLLM(_json_reply(reply=f"{marker}\n\n1. Result\n…", is_correct=None)))
        assert result["is_correct"] is False, f"{marker!r} not recognised"


def test_the_prompt_ties_the_verdict_to_the_status_line(flat):
    assert '"is_correct" MUST agree with the status line you wrote' in flat
    assert "Judging an answer wrong and then returning null is a contradiction." in flat


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
