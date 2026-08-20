"""
app/models/tool_course.py

Standalone tool course models — separate from the CareerTrack system.
Tool courses are flat (no levels): ToolCourse -> ToolTopic -> content.
Content (Lesson, Exercise, Quiz, Project) is shared with the learning models
via nullable tool_topic_id columns added via migration.

Reuses DifficultyLevel from app.models.learning — no new enum needed.
Relationships to CareerTrack are advisory only (related_track_ids for display)
and never auto-complete or skip any track topic.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base
from app.models.learning import DifficultyLevel


class ToolCourse(Base):
    __tablename__ = "tool_courses"

    id                = Column(Integer, primary_key=True, index=True)
    slug              = Column(String, unique=True, index=True, nullable=False)
    title             = Column(String, nullable=False)
    description       = Column(Text, nullable=True)
    icon              = Column(String, nullable=True)
    # Display grouping for the browse page, e.g. "LLM & AI Application Layer",
    # "Vector Databases", "MLOps & Infrastructure", "Data Tools". A plain
    # indexed string rather than an enum — new sections shouldn't need a
    # migration to add.
    category          = Column(String, index=True, nullable=True)
    difficulty        = Column(Enum(DifficultyLevel), default=DifficultyLevel.intermediate)
    estimated_hours   = Column(Float, nullable=True)
    is_active         = Column(Boolean, default=True)
    # Advisory link to CareerTracks — JSON list of track IDs e.g. [2, 3]
    # Used for display only ("relevant to ML Engineer, AI Developer").
    # Never drives unlock or completion logic.
    related_track_ids = Column(JSON, default=list)
    created_at        = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    topics      = relationship("ToolTopic", back_populates="tool_course",
                               order_by="ToolTopic.order")
    enrollments = relationship("ToolEnrollment", back_populates="tool_course")
    completions = relationship("ToolCourseCompletion", back_populates="tool_course")


class ToolTopic(Base):
    __tablename__ = "tool_topics"

    id               = Column(Integer, primary_key=True, index=True)
    tool_course_id   = Column(Integer, ForeignKey("tool_courses.id"), nullable=False)
    title            = Column(String, nullable=False)
    slug             = Column(String, index=True, nullable=False)
    description      = Column(Text, nullable=True)
    order            = Column(Integer, nullable=False)       # "order" not "order_index"
    difficulty       = Column(Enum(DifficultyLevel), default=DifficultyLevel.beginner)
    estimated_hours  = Column(Float, default=2.0)
    skill_tags       = Column(JSON, default=list)            # e.g. ["langchain", "rag"]
    prerequisite_ids = Column(JSON, default=list)            # list of ToolTopic IDs

    # Relationships
    tool_course = relationship("ToolCourse", back_populates="topics")

    # Back-references to shared content tables.
    # FK lives on the content side (tool_topic_id column added via migration).
    lessons   = relationship("Lesson",   back_populates="tool_topic",
                             primaryjoin="Lesson.tool_topic_id   == ToolTopic.id",
                             order_by="Lesson.order")
    exercises = relationship("Exercise", back_populates="tool_topic",
                             primaryjoin="Exercise.tool_topic_id == ToolTopic.id")
    quizzes   = relationship("Quiz",     back_populates="tool_topic",
                             primaryjoin="Quiz.tool_topic_id     == ToolTopic.id")
    projects  = relationship("Project",  back_populates="tool_topic",
                             primaryjoin="Project.tool_topic_id  == ToolTopic.id")
    progress_records = relationship("UserProgress", back_populates="tool_topic",
                             primaryjoin="UserProgress.tool_topic_id == ToolTopic.id")


class ToolEnrollment(Base):
    __tablename__ = "tool_enrollments"

    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id"), nullable=False)
    tool_course_id = Column(Integer, ForeignKey("tool_courses.id"), nullable=False)
    enrolled_at    = Column(DateTime(timezone=True), server_default=func.now())
    completed_at   = Column(DateTime(timezone=True), nullable=True)
    progress_pct   = Column(Float, default=0.0)

    # Relationships
    user        = relationship("User", back_populates="tool_enrollments")
    tool_course = relationship("ToolCourse", back_populates="enrollments")


class ToolCourseCompletion(Base):
    __tablename__ = "tool_course_completions"

    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id"), nullable=False)
    tool_course_id = Column(Integer, ForeignKey("tool_courses.id"), nullable=False)
    completed_at   = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user        = relationship("User", back_populates="tool_completions")
    tool_course = relationship("ToolCourse", back_populates="completions")
