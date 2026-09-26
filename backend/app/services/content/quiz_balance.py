"""
app/services/content/quiz_balance.py

Deterministic re-ordering of multiple-choice options so the correct answer is not
predictable from its position. Option *text* is never edited - only the order,
with the answer key remapped to follow it - and every seed is derived from text,
so applying it twice lands on the same arrangement.

Used by `seeds/fix_quiz_answer_bias.py` (the whole catalogue) and by the
curriculum importer, so imported quizzes are balanced the moment they arrive and a
re-import is still a no-op. See that script's docstring for why position bias
matters and what this cannot fix.
"""
import hashlib
import random


def _seed(*parts: str) -> int:
    """Order-independent seed built from text only — never from the current
    option order. That is what makes a re-run a no-op instead of another
    reshuffle."""
    digest = hashlib.sha256("␞".join(parts).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big")


def _eligible(question) -> bool:
    """MCQ, answerable, and unambiguous to reorder."""
    if not isinstance(question, dict):
        return False
    options = question.get("options")
    correct = question.get("correct")
    if not isinstance(options, list) or len(options) < 2:
        return False
    if not isinstance(correct, int) or not (0 <= correct < len(options)):
        return False
    texts = [str(o) for o in options]
    # Duplicate option texts make "which index is the answer" ambiguous once
    # the order changes. Rare — leave those for a human.
    return len(set(texts)) == len(texts)


def _target_positions(count: int, width: int, rng: random.Random) -> list:
    """A balanced sequence of answer positions for one quiz.

    Per-question hashing was not enough: independent draws still clumped, and
    a third of quizzes kept a dominant index. Dealing out shuffled blocks of
    0..width-1 spreads the answers evenly *within* each quiz, which is the
    level a student actually perceives a pattern at.
    """
    positions = []
    while len(positions) < count:
        block = list(range(width))
        rng.shuffle(block)
        positions.extend(block)
    return positions[:count]


def rebalance_quiz(quiz_title: str, questions: list) -> tuple:
    """Return (questions, changed_count) with answers spread across positions.

    Option *text* is never edited — only the order, with the answer key
    remapped to follow it.
    """
    eligible = [i for i, q in enumerate(questions or []) if _eligible(q)]
    if not eligible:
        return list(questions or []), 0

    widths = [len(questions[i]["options"]) for i in eligible]
    rng = random.Random(
        _seed(quiz_title, *(str(questions[i].get("question", "")) for i in eligible))
    )
    targets = _target_positions(len(eligible), max(widths), rng)

    rebuilt = list(questions)
    changed = 0

    for order, index in enumerate(eligible):
        question = questions[index]
        texts = [str(o) for o in question["options"]]
        correct_text = texts[question["correct"]]
        target = targets[order] % len(texts)

        # Distractors go in a deterministic order derived from their own
        # text, so the arrangement does not depend on how they arrived.
        distractors = sorted(t for t in texts if t != correct_text)
        random.Random(_seed(*sorted(texts))).shuffle(distractors)

        ordered = distractors[:target] + [correct_text] + distractors[target:]
        if ordered == texts:
            continue

        updated = dict(question)
        updated["options"] = ordered
        updated["correct"] = target
        rebuilt[index] = updated
        changed += 1

    return rebuilt, changed
