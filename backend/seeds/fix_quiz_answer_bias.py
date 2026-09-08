"""
backend/seeds/fix_quiz_answer_bias.py

Redistributes multiple-choice answer positions across the whole catalogue,
and reports the length bias it cannot fix for you.

Why: in the seeded content the correct option sat at index 1 in ~80% of
questions. "It's usually the second one" scored better than knowing the
material. Option *text* is untouched — only the order changes, and the
answer key is remapped to follow it, so nothing about what the question
asks or what counts as correct changes.

Balanced per quiz, not per question: answers are dealt across the available
option positions within each quiz, so no quiz keeps a dominant index.
Independent per-question hashing was tried first and left a third of the
catalogue still clumped.

Deterministic and idempotent: every seed is derived from question and option
*text* (options sorted), never from the order they are currently stored in,
so re-running lands on the same arrangement instead of reshuffling.

What it does NOT fix: the correct answer being the longest option (~92% of
questions). No transformation can fix that — a distractor only stops being
obviously wrong when someone writes a better one. Those are listed at the
end, worst first, so they can be worked through.

Caveat: `quiz_attempts.feedback` stores the option indices as they were at
the time of the attempt, so historical attempt detail for a reordered
question will point at the wrong option text. Scores already recorded are
unaffected. The script reports how many attempt rows exist before touching
anything.

Run from backend/:
    docker compose exec api python seeds/fix_quiz_answer_bias.py --dry-run
    docker compose exec api python seeds/fix_quiz_answer_bias.py
"""
import argparse
import hashlib
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal
import app.models.user, app.models.learning, app.models.progress        # noqa: F401,E401
import app.models.community, app.models.wallet, app.models.auth_token   # noqa: F401,E401
import app.models.challenge, app.models.exam, app.models.vocabulary     # noqa: F401,E401
from app.models.learning import Quiz
from app.models.progress import QuizAttempt
from app.services.content.quiz_lint import lint_quiz, summarize


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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        attempts = db.query(QuizAttempt).count()
        if attempts and not args.dry_run:
            print(
                f"! {attempts} existing quiz attempts — their stored feedback "
                f"references option positions that are about to change.\n"
                f"  Recorded scores are unaffected.\n"
            )

        quizzes = db.query(Quiz).all()
        before, after, changed_questions, changed_quizzes = [], [], 0, 0

        for quiz in quizzes:
            questions = quiz.questions or []
            before.append(lint_quiz(questions))

            rebuilt, changed = rebalance_quiz(quiz.title or "", questions)
            changed_questions += changed

            if changed:
                changed_quizzes += 1
                if not args.dry_run:
                    # Reassign rather than mutate: SQLAlchemy does not track
                    # in-place edits to a JSON column.
                    quiz.questions = rebuilt

            after.append(lint_quiz(rebuilt))

        if not args.dry_run:
            db.commit()

        summary_before, summary_after = summarize(before), summarize(after)
        verb = "would reorder" if args.dry_run else "reordered"
        print(f"{verb} {changed_questions} questions across {changed_quizzes} quizzes\n")
        print(f"  quizzes with position bias: "
              f"{summary_before['quizzes_with_position_bias']} → "
              f"{summary_after['quizzes_with_position_bias']}")
        print(f"  length-biased questions:    "
              f"{summary_after['length_biased_questions']} / "
              f"{summary_after['questions_checked']} "
              f"({summary_after['length_biased_pct']}%) — unchanged by design\n")

        worst = sorted(
            (
                (finding["ratio"], quiz.title, finding["question"])
                for quiz, report in zip(quizzes, after)
                for finding in report["length_bias"]
            ),
            reverse=True,
        )[:15]

        if worst:
            print("Worst length tells (the correct answer is this many times "
                  "longer than the average distractor):\n")
            for ratio, quiz_title, question in worst:
                print(f"  {ratio:>5.1f}x  [{quiz_title}] {question}")
            print("\nFix these by writing fuller distractors, not by trimming "
                  "the correct answer into something inaccurate.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
