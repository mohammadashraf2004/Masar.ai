"""
Covers the multiple-choice answer-shape checks and the reordering that fixes
the position half of them.

The bug these exist for: across the seeded catalogue the correct option sat
at index 1 in ~80% of questions and was the longest option in ~92%. Either
tell alone lets a student outscore someone who actually studied, so the
quizzes were measuring option shape rather than knowledge.

The reordering must be boring and safe — it changes the order of options and
nothing else — so the tests below are mostly about what it must *not* do.
"""
import importlib.util
from pathlib import Path

from app.services.content.quiz_lint import lint_quiz, question_length_bias, summarize

# The fixer is a maintenance script under seeds/, not an importable package.
_SPEC = importlib.util.spec_from_file_location(
    "fix_quiz_answer_bias",
    Path(__file__).resolve().parents[1] / "seeds" / "fix_quiz_answer_bias.py",
)
fixer = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(fixer)


def _quiz(n_questions=8, n_options=4, correct_index=1):
    """A quiz with every answer parked at the same position — the exact
    pattern the catalogue had."""
    return [
        {
            "question": f"Question {i}?",
            "options": [f"q{i} option {j}" for j in range(n_options)],
            "correct": correct_index,
            "explanation": "because",
        }
        for i in range(n_questions)
    ]


# ─── Reordering: what it must never break ────────────────────────────────


def test_reordering_preserves_the_correct_answer_text():
    """The only property that really matters: the answer key must still
    point at the same words it pointed at before."""
    questions = _quiz()
    expected = [q["options"][q["correct"]] for q in questions]

    rebuilt, changed = fixer.rebalance_quiz("Quiz", questions)

    assert changed > 0
    assert [q["options"][q["correct"]] for q in rebuilt] == expected


def test_reordering_keeps_the_same_set_of_options():
    questions = _quiz()
    rebuilt, _ = fixer.rebalance_quiz("Quiz", questions)
    for before, after in zip(questions, rebuilt):
        assert sorted(before["options"]) == sorted(after["options"])
        # Everything that is not the option order is left alone.
        assert before["question"] == after["question"]
        assert before["explanation"] == after["explanation"]


def test_reordering_spreads_answers_across_positions():
    questions = _quiz(n_questions=12, n_options=4, correct_index=1)
    assert lint_quiz(questions)["position_bias"] is not None

    rebuilt, _ = fixer.rebalance_quiz("Quiz", questions)

    assert lint_quiz(rebuilt)["position_bias"] is None
    assert len({q["correct"] for q in rebuilt}) > 1


def test_reordering_is_idempotent():
    """Re-running the script must be a no-op, not another reshuffle — the
    seeds are derived from option *text*, not from current order."""
    questions = _quiz()
    once, _ = fixer.rebalance_quiz("Quiz", questions)
    twice, changed = fixer.rebalance_quiz("Quiz", once)
    assert changed == 0
    assert twice == once


def test_reordering_skips_what_it_cannot_map_safely():
    questions = [
        # Duplicate option text — which index is "the answer" stops being
        # well defined once the order changes.
        {"question": "Dup?", "options": ["same", "same", "other"], "correct": 0},
        # Open-ended: no options to reorder.
        {"question": "Explain RAG.", "type": "open", "explanation": "..."},
        # Answer key out of range.
        {"question": "Broken?", "options": ["a", "b"], "correct": 7},
    ]
    rebuilt, changed = fixer.rebalance_quiz("Quiz", questions)
    assert changed == 0
    assert rebuilt == questions


def test_reordering_handles_an_empty_quiz():
    assert fixer.rebalance_quiz("Quiz", []) == ([], 0)
    assert fixer.rebalance_quiz("Quiz", None) == ([], 0)


# ─── Lint: length ────────────────────────────────────────────────────────


def test_length_bias_is_flagged_when_the_answer_is_the_long_one():
    question = {
        "question": "What is RAG?",
        "options": [
            "A database",
            "An architecture that lets an LLM retrieve external documents "
            "before generating an answer, so the response is grounded in "
            "real sources rather than the model's memory",
            "A GPU",
        ],
        "correct": 1,
    }
    finding = question_length_bias(question)
    assert finding is not None
    assert finding["ratio"] > 1.4


def test_evenly_weighted_options_are_not_flagged():
    question = {
        "question": "Which stage embeds the documents?",
        "options": [
            "Indexing, which converts each chunk into a vector",
            "Retrieval, which searches the stored vectors",
            "Generation, which writes the final answer",
        ],
        "correct": 0,
    }
    assert question_length_bias(question) is None


def test_a_short_correct_answer_is_never_a_length_tell():
    question = {
        "question": "Which database stores vectors?",
        "options": [
            "Qdrant",
            "A relational database with a full-text index over the raw documents",
            "A message queue that buffers documents before they are processed",
        ],
        "correct": 0,
    }
    assert question_length_bias(question) is None


# ─── Lint: reporting ─────────────────────────────────────────────────────


def test_position_bias_needs_enough_questions_to_be_a_pattern():
    """Two questions both answered at index 1 is chance, not a habit."""
    assert lint_quiz(_quiz(n_questions=2))["position_bias"] is None
    assert lint_quiz(_quiz(n_questions=8))["position_bias"] is not None


def test_open_ended_questions_are_ignored():
    report = lint_quiz([{"question": "Explain embeddings.", "type": "open"}])
    assert report["questions_checked"] == 0
    assert report["length_bias"] == []
    assert report["position_bias"] is None


def test_summary_rolls_up_across_quizzes():
    reports = [lint_quiz(_quiz()), lint_quiz(_quiz(n_questions=4))]
    summary = summarize(reports)
    assert summary["quizzes"] == 2
    assert summary["questions_checked"] == 12
    assert summary["quizzes_with_position_bias"] == 2
