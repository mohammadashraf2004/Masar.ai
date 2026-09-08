"""
Provider-backed evaluation of the answer evaluator. OPT-IN — skipped by default.

tests/test_answer_evaluator_policy.py proves the four-part policy reaches
the model. It cannot prove the model obeys it. This module closes that gap
the only way it can be closed: by sending real student answers to a real
provider and checking the shape of what comes back.

It is skipped unless you ask for it, because it costs tokens and depends on
a third party being up:

    RUN_LIVE_EVALUATOR_TESTS=1 pytest tests/test_answer_evaluator_live.py -s

`-s` matters — every case prints the feedback it received, so the point of
running this is as much to READ the output as to watch the assertions pass.
The assertions are deliberately structural (is there a status marker, are
all four sections present, does section 3 contain a fenced code block);
asserting on exact wording would only produce a flaky test that says
nothing about quality. Judging quality is the human's job here.

Uses whatever provider app.core.config is configured for.

MEASURED RESULTS — read this before treating a failure as a code bug
--------------------------------------------------------------------
All on GENERATION_MODEL_ID=gpt-4o-mini, 2026-09-08.

BEFORE the context block was reordered: 5/8. Three failures, one cause —
the model treated the reference answer as a specification. It marked a
valid instruction string ⚠️ Partially correct for omitting wording that
appeared only in the reference, and pasted the reference's own sentence
into section 3. Three rounds of system-prompt strengthening ("THE REFERENCE
IS NOT A CHECKLIST", a cross-reference from section 3, a rewritten label on
the reference itself) moved it not at all. gpt-4o passed the same prompt,
which looked like a model-capability ceiling.

It was not. The cause was POSITIONAL: the reference sat immediately before
the student's answer in the same flat list, so the two were adjacent and
the natural reading was to diff them. Reordering the block into
requirements → student answer → reference, with the reference explicitly
demoted, fixed on gpt-4o-mini what no amount of instruction had.

AFTER: 8/8, 8/8, and 7/8 across three consecutive full runs.
  * The valid-alternative cases — the actual bug — passed 5/5 in a
    dedicated re-run, returning ✅ Correct / is_correct=True / score=100.

The one intermittent failure was then investigated and turned out to be a
FALSE POSITIVE in the test, not evaluator behaviour. It asserted that a
single sentence from the reference never appeared anywhere in the reply,
which is not what "dumping the reference" means. Six sampled evaluations
of the NameError answer all produced a minimal Fix — exactly two fenced
code lines (the student's broken line, then the corrected one), never
reproducing the `elif` line the student already had right, never
containing the whole reference. The sample that tripped the assertion had
written its own string and merely shared a trailing sentence with the
reference. See test_live_feedback_does_not_dump_the_whole_reference, which
now measures the scope of the Fix instead.

Nothing here is xfail-ed: this module exists to report what the configured
model actually does. A red run is still a sample rather than a proof — but
re-check whether the test is measuring the right thing before changing the
evaluator, because last time it was not.

GENERATION_MODEL_ID is deliberately unchanged: it is shared by every AI
feature in the app, so switching it is a cost decision, not a fix.
"""
import os
import re

import pytest

from app.services import get_llm
from app.services.mentor import answer_evaluator_service as svc

pytestmark = pytest.mark.skipif(
    os.environ.get("RUN_LIVE_EVALUATOR_TESTS") != "1",
    reason="opt-in: set RUN_LIVE_EVALUATOR_TESTS=1 (calls a real provider, costs tokens)",
)

SECTIONS = ("1. Result", "2. Why", "3. Fix", "4. Learning point")
STATUS_MARKERS = ("❌ Incorrect", "⚠️ Partially correct", "✅ Correct")

# ─── The exercise under test ─────────────────────────────────────────────
# Deliberately the real "Add a Fourth Action: Rewrite for Tone" exercise
# from seeds/track_ai_developer/level_01_foundations.py, because it is the
# one whose feedback prompted this change. The starter code below is the
# repository's; the answers are what a student submits.
TONE_EXERCISE = {
    "kind": "exercise",
    "title": "Add a Fourth Action: Rewrite for Tone",
    "prompt": (
        "Extend the AI Text Assistant with a 4th menu option: "
        '"Rewrite in a different tone" (e.g. formal, friendly, or concise).\n\n'
        "1. Write the new menu branch (the `elif choice == \"4\":` block) "
        "including a clear `instruction` string."
    ),
    "starter_code": (
        'elif choice == "4":\n'
        "    # TODO: add your rewrite-for-tone instruction here\n"
        "    instruction = None\n"
    ),
    "reference": (
        'elif choice == "4":\n'
        '    instruction = "Rewrite the text below in a formal tone. '
        'Preserve the original meaning and approximate length."\n'
    ),
    "skill_tags": ["ai-developer", "prompt-design", "python"],
}

# An undefined bare name — the submission that started all this.
ANSWER_NAMEERROR = 'elif choice == "4":\n    instruction = jdjvlkx\n'

# Correct, and deliberately NOT identical to the reference.
ANSWER_CORRECT = (
    'elif choice == "4":\n'
    '    instruction = "Rewrite the text in a friendly, casual tone while keeping '
    'the same meaning."\n'
)

# A real string, but so vague it does not satisfy "a clear instruction".
ANSWER_PARTIAL = 'elif choice == "4":\n    instruction = "Rewrite it."\n'


def _run(answer: str, context=None) -> dict:
    return svc.evaluate_answer(
        llm=get_llm(),
        context=context or TONE_EXERCISE,
        conversation_history=[],
        user_message=answer,
    )


def _report(label: str, answer: str, result: dict) -> str:
    reply = result["reply"]
    print(f"\n{'=' * 72}\n{label}\n{'=' * 72}")
    print(f"--- submitted ---\n{answer}")
    print(f"--- is_correct={result['is_correct']}  score={result['score']} ---")
    print(reply)
    return reply


def _assert_four_part(reply: str):
    missing = [s for s in SECTIONS if s not in reply]
    assert not missing, f"missing sections {missing} in:\n{reply}"
    assert any(m in reply for m in STATUS_MARKERS), f"no status marker in:\n{reply}"


# ─────────────────────────────────────────────────────────────────────────

def test_live_schema_is_respected():
    result = _run(ANSWER_NAMEERROR)
    assert set(result) == {"reply", "is_correct", "score", "suggested_actions"}
    assert isinstance(result["reply"], str) and result["reply"].strip()
    assert result["is_correct"] in (True, False, None)
    assert result["score"] is None or 0 <= result["score"] <= 100


def test_live_undefined_name_gets_the_four_part_structure():
    result = _run(ANSWER_NAMEERROR)
    reply = _report("NameError submission — instruction = jdjvlkx", ANSWER_NAMEERROR, result)

    _assert_four_part(reply)
    assert "❌ Incorrect" in reply, "an undefined name should not be graded correct"
    assert result["is_correct"] is False


def test_live_undefined_name_gets_an_exact_correction():
    """The whole point of the change: section 3 must carry runnable code,
    not 'review how strings work'."""
    reply = _report(
        "Exact-correction check", ANSWER_NAMEERROR, _run(ANSWER_NAMEERROR),
    )
    fix = reply.split("3. Fix", 1)[1].split("4. Learning point", 1)[0]
    assert "```" in fix, f"section 3 has no fenced code block:\n{fix}"
    # The corrected line has to assign a *string* to instruction.
    assert re.search(r"instruction\s*=\s*[\"']", fix), (
        f"section 3 never shows the corrected assignment:\n{fix}"
    )


def test_live_correct_answer_is_not_criticised():
    result = _run(ANSWER_CORRECT)
    reply = _report("Correct submission (differs from the reference)", ANSWER_CORRECT, result)

    _assert_four_part(reply)
    assert "✅ Correct" in reply, (
        "a valid instruction string that differs from the reference was not "
        f"accepted:\n{reply}"
    )
    assert result["is_correct"] is True


def test_live_correct_answer_does_not_invent_requirements():
    """The exercise asks only for an instruction string. Faulting the student
    for not building a tone-selection menu is the invented-requirement
    failure the prompt forbids."""
    reply = _report("Invented-requirement check", ANSWER_CORRECT, _run(ANSWER_CORRECT))
    lowered = reply.lower()
    assert "no changes are needed" in lowered, (
        f"a correct answer should need no changes:\n{reply}"
    )


def test_live_feedback_asks_no_unnecessary_questions():
    reply = _report("No-questions check", ANSWER_NAMEERROR, _run(ANSWER_NAMEERROR))
    lowered = reply.lower()
    for banned in (
        "would you like me to show",
        "can you try again",
        "what do you think the problem is",
        "shall i give you a hint",
    ):
        assert banned not in lowered, f"asked a forbidden question ({banned!r}):\n{reply}"


def _fix_section(reply: str) -> str:
    """Just section 3. The earlier version of the test below searched the
    whole reply, so wording quoted in section 1 or discussed in section 2
    was blamed on the Fix."""
    if "3. Fix" not in reply:
        return ""
    chunk = reply.split("3. Fix", 1)[1]
    return chunk.split("4. Learning point", 1)[0]


def _fenced_code_lines(text: str) -> list:
    """Non-blank lines inside ``` fences — the code the Fix actually offers,
    without the prose around it."""
    lines, in_fence = [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence and line.strip():
            lines.append(line.strip())
    return lines


def test_live_feedback_does_not_dump_the_whole_reference():
    """The Fix must be the minimal correction for THIS student's bug.

    What this deliberately does NOT test: textual overlap with the
    reference. The student's bug is an undefined name, so the minimal fix
    is necessarily `instruction = "<some string>"` — and any sensible
    string for this exercise will read a lot like the reference's, because
    the reference is itself just a sensible string for this exercise.
    Overlap there is legitimate and is not evidence of anything.

    The previous version of this test asserted that one sentence from the
    reference ("Preserve the original meaning and approximate length.")
    never appeared anywhere in the reply. That failed roughly one run in
    eight while the Fix was provably minimal. Measured over six samples:
    every Fix carried exactly two fenced code lines — the student's broken
    line and the corrected one — none reproduced the `elif` line the
    student already had right, and none contained the whole reference. The
    one sample that tripped the old assertion had composed its own string
    ("a different tone", where the reference says "a formal tone") and
    merely shared the trailing sentence. That was a false positive.

    So this now measures SCOPE, which is what "dumping the reference"
    actually means: is the Fix bigger than the student's mistake?
    """
    reply = _report("Fix-scope check", ANSWER_NAMEERROR, _run(ANSWER_NAMEERROR))
    fix = _fix_section(reply)
    assert fix.strip(), f"no section 3 to inspect:\n{reply}"

    code = _fenced_code_lines(fix)

    # 1. The reference, whole, must not be sitting in section 3.
    ref_lines = [l.strip() for l in TONE_EXERCISE["reference"].strip().splitlines() if l.strip()]
    assert not all(l in fix for l in ref_lines), (
        f"section 3 reproduces the entire reference solution:\n{fix}"
    )

    # 2. The student's only bug is the `instruction = ...` line. Rewriting
    #    the `elif` line they already had right means the fix outgrew the
    #    mistake — that is what replacing their implementation looks like.
    corrections = [l for l in code if l != "instruction = jdjvlkx"]
    assert not any(l.startswith('elif choice') for l in corrections), (
        f"section 3 rewrites code the student already had correct:\n{fix}"
    )

    # 3. A one-line bug earns a small fix. Generous bound: the broken line,
    #    the corrected line, and a little framing — not a program.
    assert len(code) <= 4, (
        f"section 3 offers {len(code)} lines of code for a one-line bug:\n{fix}"
    )


def test_live_partial_answer_separates_right_from_wrong():
    """Advisory: a vague-but-valid string is a judgement call, so this only
    asserts the structure holds and prints the verdict for a human to read."""
    result = _run(ANSWER_PARTIAL)
    reply = _report("Vague-but-valid submission", ANSWER_PARTIAL, result)
    _assert_four_part(reply)
