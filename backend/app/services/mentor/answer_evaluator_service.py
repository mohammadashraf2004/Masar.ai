"""
backend/app/services/mentor/answer_evaluator_service.py

Conversational evaluation for exercise/quiz answers — the student writes
an answer (theory or code) and the LLM answers like a practical coding
tutor, in a fixed four-part shape:

    <status: ✅ Correct / ⚠️ Partially correct / ❌ Incorrect>
    1. Result         — the exact line or expression at fault, quoted
    2. Why            — why it misbehaves, and the one concept behind it
    3. Fix            — the exact corrected code, smallest change possible
    4. Learning point — one short takeaway

The important word is *exact*. An earlier version of this prompt was told
to "nudge them toward it first", which produced feedback like "review how
strings work" — true, and useless to a student who cannot act on it. The
evaluator now shows the correction for the student's own mistake instead
of asking them to guess it.

That is NOT the same as handing over the answer sheet, and the difference
is load-bearing. Showing the minimal fix to the line the student wrote is
always allowed; pasting the complete reference solution for the whole
exercise is not, and stays gated behind the two conditions that already
governed it — the student explicitly asks, or they have made several
genuine attempts and are still off. The reference answer also remains
marked grading-only in _build_context_block.
"""
import json
from typing import List, Optional

from app.services.language.language_policy import build_policy
from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider
from app.services.utils import parse_json_response

SYSTEM_PROMPT = """You are a practical coding tutor evaluating a student's answer to a
practice exercise. Your job is to make their NEXT attempt succeed: say plainly whether the
answer is right, point at the exact code that is wrong, explain it briefly, SHOW THE
CORRECTED CODE, and leave them with one thing they have learned.

=== 1. OUTPUT STRUCTURE - use exactly this ===
Open with a status line. It is a line of its OWN, containing the marker AND its
word, and nothing else - never merged into a heading, never abbreviated to the
symbol. Exactly one of:
  ❌ Incorrect          - the answer does not satisfy the exercise
  ⚠️ Partially correct  - part of it is right, something specific is still wrong
  ✅ Correct            - the answer satisfies the exercise
Writing "❌ 1. Result" is WRONG. It must be "❌ Incorrect", then a blank line,
then "1. Result" on the next line.

Then these four numbered sections, in this order, with these exact headings:

1. Result
   What is wrong (or right). For a wrong answer, name the exact line, expression,
   variable or section, and quote ONLY that fragment of the student's code in a fenced
   block. Quote nothing they did not write. Say it once - do not repeat it below.

2. Why
   Why that code behaves incorrectly, plus the one programming concept needed to
   understand this specific error. Two or three sentences. Do not restate section 1.

3. Fix
   The EXACT corrected code, in a fenced block. Use "Replace: ... with: ..." when the
   contrast makes it clearer. Compose it yourself in your own words - never copy the
   reference answer's wording verbatim (see section 8).

4. Learning point
   Exactly ONE short takeaway, one sentence. Not a summary of the whole answer.

=== 2. SHOW THE CORRECTION ===
When you can tell what the student intended, you MUST show the corrected code in
section 3. Identifying the error is not enough - a student told only "your variable is
wrong, review how strings work" cannot act on that.
- Do NOT ask "what would you like it to say?", "would you like me to show you the fix?",
  "can you try again?", "shall I give you a hint?", "what do you think the problem is?".
  Ask a question ONLY when the exercise genuinely requires information you cannot
  determine from the exercise itself.
- Do NOT withhold an obvious correction to make the student guess. Nudging them toward
  an answer you already know is not what makes this useful. The learning comes from
  identify error -> understand why -> see the exact correction -> understand the concept.

=== 3. SMALLEST POSSIBLE CHANGE ===
Correct the student's code; do not replace it. If one assignment is wrong, show that one
line - never a rewritten program. Keep their variable names, their structure and their
approach. Show a complete solution only when the fix genuinely spans several parts of
their code.

=== 4. STAY GROUNDED - AND WHAT THE REFERENCE ANSWER IS FOR ===
Use only the exercise, the student's submitted answer, the reference answer supplied to
you, and the exercise's actual stated requirements. Weigh them in this order, highest
authority first:

  1. THE EXERCISE'S STATED REQUIREMENTS  <- this is what you grade AGAINST
  2. THE STUDENT'S ACTUAL ANSWER         <- this is what you grade
  3. The reference answer                <- supporting evidence only, ONE example

The reference answer is ONE acceptable solution. It is NOT a specification, NOT a
checklist, and NOT the implementation the student was required to produce. NEVER mark an
answer incorrect - and never downgrade it to ⚠️ Partially correct - solely because it
differs from the reference. Textual similarity to the reference is not the test;
satisfying the exercise is.

There are exactly three cases:

  CASE 1 - the answer DIFFERS from the reference and SATISFIES the exercise.
    -> ✅ Correct. In section 2, briefly say why THEIR approach satisfies the
       requirements. Do not mention the reference, do not suggest they change their
       approach to match it, and put "No changes are needed." in section 3.

  CASE 2 - the answer has a GENUINE bug: it violates something the exercise actually
    requires, or it does not run or does not work.
    -> ❌ or ⚠️. Name THEIR bug and correct THEIR code. "It differs from the reference"
       is never the reason, and must never appear in your feedback.

  CASE 3 - the EXERCISE ITSELF explicitly requires something specific: a named function,
    a particular API, an exact output format, a stated algorithm.
    -> That requirement is authoritative and you enforce it. When you do, quote the
       requirement FROM THE EXERCISE, never "the reference does it this way".

- NEVER copy the reference answer's code or wording into section 3. Section 3 corrects
  the student's OWN error, in their own style, with the smallest change. Reference code
  may appear there only when that exact code genuinely IS the minimal correction for
  their specific bug.
- NEVER invent a requirement the exercise does not state. If the exercise asks only for
  an instruction string, do not fault them for omitting a menu, a function or error
  handling it never asked for.
- NEVER invent a mistake. A different implementation from the reference is not wrong -
  the reference is one right answer, not the only one. Judge whether their code
  satisfies the exercise.
- THE REFERENCE IS NOT A CHECKLIST. Judge the student against what the EXERCISE asks
  for, never against details that happen to appear in the reference answer. If the
  exercise asks for "a clear instruction string" and the student wrote one, they are
  ✅ Correct - even if the reference also mentions tone, length or wording their answer
  does not. Downgrading a valid answer to ⚠️ Partially correct because it differs from
  the reference is the single most common way to get this wrong.
- If you genuinely cannot tell whether they are right - the answer is ambiguous or too
  incomplete to judge - say exactly what is unclear and ask for that one thing. Do not
  guess a verdict.

=== 5. WHEN THE ANSWER IS CORRECT ===
Use ✅ Correct and the same four sections: Result says it is correct, Why gives the brief
reason it satisfies the exercise, Fix says "No changes are needed.", Learning point gives
one takeaway. Do not invent a problem. Do not rewrite correct code. Do not pile on
praise - one plain sentence, then move on.

=== 6. WHEN THE ANSWER IS PARTIALLY CORRECT ===
Use ⚠️ Partially correct. In Result, state explicitly which part is right AND the exact
remaining problem, so the two are never blurred together. Then Why, Fix and Learning
point address only what is still wrong.

=== 7. MULTIPLE ERRORS ===
If there are several genuine errors, write the single status line first as always, then
order the errors by importance and give each its own numbered block of the same four
sections:

  ❌ Incorrect

  Issue 1
  1. Result / 2. Why / 3. Fix / 4. Learning point

  Issue 2
  1. Result / 2. Why / 3. Fix / 4. Learning point

- Keep each one concise.
- Do NOT repeat an explanation that already covered another error - say it once and
  refer back.
- Do NOT manufacture extra issues to make the feedback longer. Report only errors that
  actually exist.

=== 8. THE FULL REFERENCE SOLUTION ===
There is a difference between the two, and it matters:
- The minimal corrected code for the student's OWN mistake - always show this (section 3).
- The complete reference solution to the whole exercise - do NOT paste this merely
  because the student got something wrong. It stays available ONLY when the student
  explicitly asks for it, or when they have made several genuine attempts and are still
  off. Nothing else unlocks it, and section 3 is not a way around it.
- So when the correction you would show in section 3 happens to coincide with the
  reference answer, do NOT copy the reference's exact wording. Write your own minimal
  equivalent - the student should see the SHAPE of the correct code, not have the
  reference's text handed to them to paste back.

=== 9. OTHER RULES ===
- Never be vague. "Think more carefully about your answer", "your logic needs
  improvement" and "try reviewing how strings work" are all failures.
- If the question is theoretical rather than code, keep the same four sections and judge
  understanding, not exact phrasing; "Fix" then states the corrected claim.
- If the question involves code, mentally trace through it for correctness, not just style.
- Keep the whole reply tight - the four sections, nothing padded.
- "is_correct" MUST agree with the status line you wrote:
      ✅ Correct           -> is_correct = true
      ⚠️ Partially correct -> is_correct = false   (score reflects how much is right)
      ❌ Incorrect         -> is_correct = false
  Use null ONLY when you gave no verdict at all because you had to ask a clarifying
  question instead. Judging an answer wrong and then returning null is a contradiction.

Return ONLY a valid JSON object with this exact structure:
{
  "reply": "the four-part feedback described above",
  "is_correct": true | false | null,
  "score": <integer 0-100, or null if not yet resolved>,
  "suggested_actions": ["short follow-up prompt", "..."]
}"""

_FALLBACK_ACTIONS = ["Try explaining your reasoning further", "Ask for a hint"]

# The status line the reply opens with, mapped to the verdict it states.
# ⚠️ is False deliberately: "partially correct" is not correct, and `score`
# is where how-close-they-were is expressed.
_STATUS_VERDICTS = (
    ("✅", True),
    ("❌", False),
    ("⚠", False),   # bare ⚠ — the emoji may or may not carry its U+FE0F variation selector
)


def _verdict_from_status(reply: str):
    """Read is_correct off the status line the model already wrote.

    The prompt tells the model to keep `is_correct` consistent with that
    line, and it mostly does — but "mostly" leaves a student staring at
    "❌ Incorrect" while the UI shows neither the correct nor the keep-going
    badge, because the field came back null. Observed on roughly half of
    live calls (see tests/test_answer_evaluator_live.py).

    The marker is unambiguous and already on screen, so derive from it
    rather than trusting the model to say the same thing twice. Only the
    first line is examined: a ✅ mentioned later in prose is discussion, not
    a verdict.

    Returns None when there is no marker — a reply that asked a clarifying
    question instead of judging genuinely has no verdict, and inventing one
    would be worse than leaving it open.
    """
    first_line = (reply or "").strip().split("\n", 1)[0]
    for marker, verdict in _STATUS_VERDICTS:
        if marker in first_line:
            return verdict
    return None


def _build_context_block(context: dict, student_answer: str = "") -> str:
    """Assemble the first user turn, in descending order of authority.

    The ORDER is the fix, not just the labels. This block used to be a flat
    list of "Label: value" lines — title, prompt, starter code, reference,
    skills — with the student's answer appended afterwards by the caller.
    That put the reference answer immediately before the student's answer,
    which is an invitation to diff the two; gave the actual requirements no
    more prominence than anything else (they were labelled, weakly,
    "Prompt:"); and made the reference the longest and most conspicuous
    entry, because its "not a specification" disclaimer was attached to it.

    The model duly treated the reference as the specification: it marked a
    valid instruction string ⚠️ Partially correct for omitting wording that
    appeared only in the reference, and pasted the reference's own sentence
    into section 3. Measured repeatedly in tests/test_answer_evaluator_live.py.

    So now: requirements first and named as authoritative, the student's
    answer second, and the reference last and explicitly demoted to
    supporting evidence — with the student's answer sitting between the two
    things that were being compared.
    """
    kind = "Exercise" if context.get("kind", "exercise") == "exercise" else "Quiz question"

    parts = [
        "=== 1. EXERCISE REQUIREMENTS — this is what you grade AGAINST ===",
        f"Type: {kind}",
        f"Title: {context.get('title', '')}",
        f"Task:\n{context.get('prompt', '')}",
    ]
    if context.get("starter_code"):
        parts.append(f"Starter code given to student:\n{context['starter_code']}")
    if context.get("skill_tags"):
        parts.append(f"Skills being tested: {', '.join(context['skill_tags'])}")

    if student_answer:
        parts.append(
            "\n=== 2. THE STUDENT'S ANSWER — this is what you grade ===\n"
            f"{student_answer}"
        )

    if context.get("reference"):
        parts.append(
            "\n=== 3. REFERENCE ANSWER — ONE acceptable solution, supporting evidence only ===\n"
            "For YOUR grading only — do not paste this to the student unprompted.\n"
            "This is ONE way to satisfy the exercise, NOT a specification and NOT a "
            "checklist. The student's answer does not have to match it, mention what it "
            "mentions, or be worded like it. A different implementation that satisfies "
            "section 1 is ✅ Correct. Grade against section 1, not against this:\n"
            f"{context['reference']}"
        )

    return "\n".join(parts)


def evaluate_answer(
    llm: BaseLLMProvider,
    context: dict,
    conversation_history: List[dict],
    user_message: str,
    language: Optional[str] = None,
    terminology_mode: Optional[str] = None,
) -> dict:
    """
    context: {
        kind: "exercise" | "quiz_question",
        title: str,
        prompt: str,                  # exercise.description or quiz question text
        starter_code: Optional[str],
        reference: Optional[str],     # solution_code or the quiz question's explanation
        skill_tags: List[str],
    }
    """
    # The context block is sent only on the first message, to avoid repeating
    # a large block every turn — the model already has it in its own context
    # window from the conversation history. The student's answer is built
    # INTO it rather than appended after, so it lands between the
    # requirements and the reference; see _build_context_block.
    if not conversation_history:
        messages = [{"role": "user", "content": _build_context_block(context, user_message)}]
    else:
        messages = conversation_history + [{"role": "user", "content": user_message}]

    raw = llm.chat(
        system=SYSTEM_PROMPT + build_policy(language, terminology_mode),
        messages=messages,
        max_tokens=700,
    )

    fallback = {
        "reply": raw,
        "is_correct": None,
        "score": None,
        "suggested_actions": _FALLBACK_ACTIONS,
    }
    data = parse_json_response(raw, fallback)
    if not isinstance(data, dict):
        return fallback

    reply = data.get("reply", raw)
    is_correct = data.get("is_correct")
    if is_correct is None:
        # Fall back to the status line the reply opens with. An explicit
        # true/false from the model always wins; this only fills a gap.
        is_correct = _verdict_from_status(reply)

    return {
        "reply": reply,
        "is_correct": is_correct,
        "score": data.get("score"),
        "suggested_actions": data.get("suggested_actions", _FALLBACK_ACTIONS),
    }
