from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint
from sqlalchemy.sql import func

from app.db.session import Base


class MentorQuizTranslation(Base):
    """The text of one authored quiz question in the other UI language.

    The authored course quizzes are in one language (today all of them are English, with no
    Arabic twin), so a learner reading Masar in the other language would be asked an
    unreadable question. The mentor translates a question the first time it is needed and
    keeps the result here, so each question is translated once per language, not per learner.

    Display only. It holds question, options and explanation and nothing that grades: the
    answer key stays on the authored `Quiz` row, and option *positions* are identical to the
    authored question (the translation is rejected otherwise), so an option id means the same
    thing in both languages. `source_hash` is the hash of the authored text the translation
    was made from; when an author edits the question the stale translation is replaced.
    """
    __tablename__ = "mentor_quiz_translations"
    __table_args__ = (
        UniqueConstraint("quiz_id", "question_index", "language", name="uq_mentor_quiz_translation"),
    )

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    question_index = Column(Integer, nullable=False)
    language = Column(String(2), nullable=False)
    source_hash = Column(String(64), nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
