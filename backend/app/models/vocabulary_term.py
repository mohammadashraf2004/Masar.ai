"""
app/models/vocabulary_term.py

The global AI Vocabulary dictionary. A concept such as "Embedding" exists as
exactly one row here, no matter how many of the 15 curriculum courses teach
it; `VocabularyTermAssociation` is what says which course/module/lesson each
term appears in.

Courses, modules and lessons are addressed by the same `source_key` strings
the curriculum importer already writes onto `ToolTopic.source_key` /
`Lesson.source_key` (`"COURSE-005/M005-01"`, lesson ids like `"L005-001"`).
Associations are kept as plain strings rather than foreign keys into
`tool_courses`/`tool_topics`/`lessons` on purpose: two parallel schemas
(`ToolCourse` and the legacy `CareerTrack` tree) can both hold a course's
actual content, and a term's curriculum mapping should not have to pick one.
Resolving a term's "learn this concept" link to a real, currently-imported
lesson happens at read time, against whichever schema has that source_key.
"""
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class VocabularyTerm(Base):
    __tablename__ = "vocabulary_terms"

    id = Column(Integer, primary_key=True, index=True)
    # The stable identity: what `UserTermProgress.term_id` and the old
    # ai_terms.json dictionary keyed on. New terms get a slugified English name.
    slug = Column(String(80), unique=True, nullable=False, index=True)

    term_en = Column(String(160), nullable=False)
    term_ar = Column(String(160), nullable=False)
    acronym = Column(String(40), nullable=True)
    # Alternate surface forms ("RAG", "retrieval augmented generation", ...),
    # used for search and to stop near-duplicate terms being seeded twice.
    aliases = Column(JSON, nullable=False, default=list)

    category = Column(String(60), nullable=True, index=True)
    difficulty = Column(String(20), nullable=False, default="intermediate", index=True)
    tags = Column(JSON, nullable=False, default=list)

    definition_en = Column(Text, nullable=False)
    definition_ar = Column(Text, nullable=False)
    explanation_simple_ar = Column(Text, nullable=True)
    why_it_matters_ar = Column(Text, nullable=True)
    example_ar = Column(Text, nullable=True)

    # Where the definition itself came from (a lesson source_key, a course
    # manifest, ...) — for authors, never shown verbatim to a learner.
    source_references = Column(JSON, nullable=False, default=list)

    # First meaningful instructional introduction, decided by content review,
    # not by the first string match. Nullable: a term added by hand before any
    # course teaches it yet has neither.
    first_course_key = Column(String(20), nullable=True, index=True)
    first_lesson_key = Column(String(20), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True, server_default="true")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    relations = relationship(
        "VocabularyTermRelation",
        foreign_keys="VocabularyTermRelation.term_id",
        cascade="all, delete-orphan",
    )
    associations = relationship(
        "VocabularyTermAssociation",
        cascade="all, delete-orphan",
    )


class VocabularyTermRelation(Base):
    """A directed "see also" edge. Seeded in both directions where the
    relationship is symmetric (Embedding <-> Vector Search), left one-way
    where it isn't (RAG -> Retrieval, but not every mention of Retrieval
    should surface RAG)."""

    __tablename__ = "vocabulary_term_relations"
    __table_args__ = (
        UniqueConstraint("term_id", "related_term_id", name="uq_vocab_term_relation"),
    )

    id = Column(Integer, primary_key=True, index=True)
    term_id = Column(Integer, ForeignKey("vocabulary_terms.id", ondelete="CASCADE"), nullable=False, index=True)
    related_term_id = Column(Integer, ForeignKey("vocabulary_terms.id", ondelete="CASCADE"), nullable=False, index=True)

    related_term = relationship("VocabularyTerm", foreign_keys=[related_term_id])


class VocabularyTermAssociation(Base):
    """Where a term is taught. `course_key` is always set; `module_key` and
    `lesson_key` narrow it, matching the curriculum's own id convention."""

    __tablename__ = "vocabulary_term_associations"
    __table_args__ = (
        UniqueConstraint(
            "term_id", "course_key", "module_key", "lesson_key",
            name="uq_vocab_term_association",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    term_id = Column(Integer, ForeignKey("vocabulary_terms.id", ondelete="CASCADE"), nullable=False, index=True)
    course_key = Column(String(20), nullable=False, index=True)
    module_key = Column(String(20), nullable=True)
    lesson_key = Column(String(20), nullable=True)
