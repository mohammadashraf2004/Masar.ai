from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, JSON, ForeignKey, Enum, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class DifficultyLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class CareerTrack(Base):
    """e.g. 'AI Engineer', 'Backend Engineer', 'Data Analyst'"""
    __tablename__ = "career_tracks"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    # Arabic-first content. Nullable throughout: a course that predates the
    # Arabic-first policy keeps working unchanged and simply has no Arabic
    # version to offer. See docs/content/ARABIC_FIRST_GUIDELINES.md.
    title_ar = Column(String, nullable=True)
    description_ar = Column(Text, nullable=True)
    icon = Column(String)
    is_active = Column(Boolean, default=True)
    estimated_weeks = Column(Integer, default=24)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    levels = relationship("TrackLevel", back_populates="track", order_by="TrackLevel.order")
    enrollments = relationship("Enrollment", back_populates="track")


class TrackLevel(Base):
    """e.g. Level 1 - Foundations, Level 2 - Data & ML"""
    __tablename__ = "track_levels"

    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("career_tracks.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    title_ar = Column(String, nullable=True)
    description_ar = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)

    # Relationships
    track = relationship("CareerTrack", back_populates="levels")
    topics = relationship("Topic", back_populates="level", order_by="Topic.order")


class Topic(Base):
    """Individual topic within a level (e.g. PyTorch, CNNs, RAG)"""
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("track_levels.id"), nullable=False)
    title = Column(String, nullable=False)
    slug = Column(String, index=True, nullable=False)
    description = Column(Text)
    title_ar = Column(String, nullable=True)
    description_ar = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.beginner)
    estimated_hours = Column(Float, default=2.0)
    # Prerequisite topic IDs stored as JSON array
    prerequisite_ids = Column(JSON, default=list)
    skill_tags = Column(JSON, default=list)  # e.g. ["python", "pytorch", "tensors"]
    # Terminology dictionary ids this topic teaches, e.g. ["embeddings", "rag"].
    # Drives the vocabulary panel and the job-role mapping; unknown ids are
    # ignored on render rather than failing the page.
    technical_terms = Column(JSON, default=list)

    # Relationships
    level = relationship("TrackLevel", back_populates="topics")
    lessons = relationship("Lesson", back_populates="topic", order_by="Lesson.order")
    exercises = relationship("Exercise", back_populates="topic")
    projects = relationship("Project", back_populates="topic")
    quizzes = relationship("Quiz", back_populates="topic")
    progress_records = relationship("UserProgress", back_populates="topic")


class Lesson(Base):
    """Theory lesson within a topic"""
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # Markdown
    # Arabic-first body. Not a translation of `content` — an Arabic-first
    # lesson is authored here directly, with English terminology preserved
    # inline and code blocks identical to the English version.
    title_ar = Column(String, nullable=True)
    content_ar = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    estimated_minutes = Column(Integer, default=15)
    has_code_examples = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    topic = relationship("Topic", back_populates="lessons")
    tool_topic_id = Column(Integer, ForeignKey("tool_topics.id"), nullable=True)
    tool_topic    = relationship("ToolTopic", back_populates="lessons",
                                 foreign_keys="[Lesson.tool_topic_id]")


class Exercise(Base):
    """Guided coding exercise"""
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    title_ar = Column(String, nullable=True)
    description_ar = Column(Text, nullable=True)
    # starter_code / solution_code have no _ar twin by design: code is
    # identical in every language.
    starter_code = Column(Text)
    solution_code = Column(Text)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.beginner)
    skill_tested = Column(JSON, default=list)

    topic = relationship("Topic", back_populates="exercises")
    tool_topic_id = Column(Integer, ForeignKey("tool_topics.id"), nullable=True)
    tool_topic    = relationship("ToolTopic", back_populates="exercises",
                                 foreign_keys="[Exercise.tool_topic_id]")


class Project(Base):
    """Real-world portfolio project"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    title_ar = Column(String, nullable=True)
    description_ar = Column(Text, nullable=True)
    difficulty = Column(Enum(DifficultyLevel), default=DifficultyLevel.beginner)
    tech_stack = Column(JSON, default=list)  # e.g. ["PyTorch", "FastAPI", "Docker"]
    objectives = Column(JSON, default=list)
    rubric = Column(JSON, default=dict)  # {criterion: max_points}
    starter_repo_url = Column(String, nullable=True)
    estimated_hours = Column(Float, default=8.0)

    topic = relationship("Topic", back_populates="projects")
    submissions = relationship("ProjectSubmission", back_populates="project")
    tool_topic_id = Column(Integer, ForeignKey("tool_topics.id"), nullable=True)
    tool_topic    = relationship("ToolTopic", back_populates="projects",
                                 foreign_keys="[Project.tool_topic_id]")


class Quiz(Base):
    """Knowledge check quiz"""
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=True)
    title = Column(String, nullable=False)
    questions = Column(JSON, nullable=False)
    title_ar = Column(String, nullable=True)
    # Same shape as `questions`. Kept as a separate blob rather than adding
    # per-field _ar keys inside it, so grading never has to care which
    # language the taker read the question in — indices line up 1:1.
    questions_ar = Column(JSON, nullable=True)
    # questions format: [{"question": "...", "options": [...], "correct": 0, "explanation": "..."}]
    passing_score = Column(Integer, default=70)

    topic = relationship("Topic", back_populates="quizzes")
    attempts = relationship("QuizAttempt", back_populates="quiz")
    tool_topic_id = Column(Integer, ForeignKey("tool_topics.id"), nullable=True)
    tool_topic    = relationship("ToolTopic", back_populates="quizzes",
                                 foreign_keys="[Quiz.tool_topic_id]")
