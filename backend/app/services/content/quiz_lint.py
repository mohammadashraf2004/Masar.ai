"""
app/services/content/quiz_lint.py

Detects answerable-without-knowing patterns in multiple-choice quizzes.

Two tells, both measured across the seeded catalogue and both severe there:

  * **Length.** The correct option is the longest one. It happens because
    the correct answer gets written as a full explanation while the
    distractors get written as throwaway phrases. A student who has learned
    nothing but "pick the long one" scores far above chance.
  * **Position.** The correct option sits at the same index across a quiz —
    "it's usually B".

Neither is about the content being wrong; both are about the *shape* of the
options leaking the answer. This module reports them so an author can fix
the shape, and so a regression is visible before it ships.

Position is mechanically fixable (see seeds/fix_quiz_answer_bias.py, which
reorders options and remaps the answer key). Length is not: making a
distractor longer means writing a better distractor, which is an authoring
job, not a transformation.
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Dict, List, Optional, Sequence

#: A correct option this much longer than the average distractor is a tell
#: a student can act on, even without noticing they are doing it.
LENGTH_RATIO_THRESHOLD = 1.4

#: Below this many questions, "they're all at index 1" is chance, not a pattern.
MIN_QUESTIONS_FOR_POSITION_CHECK = 4

#: Share of questions allowed to sit at one index before it reads as a habit.
POSITION_CONCENTRATION_THRESHOLD = 0.6


def _mcq_questions(questions: Sequence[dict]) -> List[dict]:
    """Only multiple-choice questions have an option shape to leak."""
    return [
        q
        for q in questions or []
        if isinstance(q, dict)
        and isinstance(q.get("options"), list)
        and len(q["options"]) > 1
        and isinstance(q.get("correct"), int)
        and 0 <= q["correct"] < len(q["options"])
    ]


def question_length_bias(question: dict) -> Optional[Dict[str, Any]]:
    """The length tell for one question, or None when the options are even."""
    options = [str(o) for o in question["options"]]
    correct_index = question["correct"]
    correct_len = len(options[correct_index])
    distractors = [len(o) for i, o in enumerate(options) if i != correct_index]
    if not distractors:
        return None

    average = sum(distractors) / len(distractors)
    is_longest = correct_len >= max(distractors)
    ratio = correct_len / average if average else float("inf")

    if not (is_longest and ratio >= LENGTH_RATIO_THRESHOLD):
        return None

    return {
        "question": question.get("question", "")[:120],
        "correct_length": correct_len,
        "average_distractor_length": round(average, 1),
        "ratio": round(ratio, 2),
        "message": (
            f"The correct option is {ratio:.1f}x longer than the average "
            f"distractor and is the longest on offer — a student can pick it "
            f"without reading it. Tighten the correct answer, or give the "
            f"distractors the same weight."
        ),
    }


def lint_quiz(questions: Sequence[dict]) -> Dict[str, Any]:
    """Report both tells for one quiz's `questions` blob."""
    mcq = _mcq_questions(questions)
    report: Dict[str, Any] = {
        "questions_checked": len(mcq),
        "length_bias": [],
        "position_bias": None,
    }
    if not mcq:
        return report

    report["length_bias"] = [
        finding for finding in (question_length_bias(q) for q in mcq) if finding
    ]

    if len(mcq) >= MIN_QUESTIONS_FOR_POSITION_CHECK:
        positions = Counter(q["correct"] for q in mcq)
        index, count = positions.most_common(1)[0]
        share = count / len(mcq)
        if share >= POSITION_CONCENTRATION_THRESHOLD:
            report["position_bias"] = {
                "index": index,
                "count": count,
                "total": len(mcq),
                "share": round(share, 2),
                "message": (
                    f"{count} of {len(mcq)} answers sit at option "
                    f"{index + 1}. Reorder the options — "
                    f"seeds/fix_quiz_answer_bias.py does this safely."
                ),
            }

    return report


def summarize(reports: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Roll several quiz reports up into catalogue-level numbers."""
    checked = sum(r["questions_checked"] for r in reports)
    biased = sum(len(r["length_bias"]) for r in reports)
    return {
        "quizzes": len(reports),
        "questions_checked": checked,
        "length_biased_questions": biased,
        "length_biased_pct": round(100 * biased / checked, 1) if checked else 0.0,
        "quizzes_with_position_bias": sum(1 for r in reports if r["position_bias"]),
    }
