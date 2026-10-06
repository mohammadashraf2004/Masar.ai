"""A course's figures: the images its lessons place with `{{image:<key>}}`.

The row is the *description* of an asset (what it shows, its alt text and caption,
what type it is and how big) plus the storage key that says where the bytes are.
Lesson text never holds a path or a URL - only the key - so moving the files from
the course folder to object storage is a change to `storage_key` and the store in
`app.services.assets`, not to any lesson.
"""
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base


class CourseAsset(Base):
    __tablename__ = "course_assets"
    __table_args__ = (UniqueConstraint("tool_course_id", "key", name="uq_course_assets_course_key"),)

    id = Column(Integer, primary_key=True, index=True)
    tool_course_id = Column(Integer, ForeignKey("tool_courses.id", ondelete="CASCADE"), nullable=False, index=True)
    # Lowercase words joined by hyphens; what a lesson's figure marker names.
    key = Column(String(120), nullable=False)
    asset_type = Column(String(20), nullable=False, default="image", server_default="image")
    # Where the bytes are, relative to the store's root (for the local store: the
    # courses folder). Never sent to a client.
    storage_key = Column(String(500), nullable=False)
    mime_type = Column(String(60), nullable=False)
    byte_size = Column(BigInteger, nullable=False)
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    # Content hash: the HTTP ETag, and how a re-import notices a replaced file.
    sha256 = Column(String(64), nullable=False)
    alt = Column(Text, nullable=False)
    caption = Column(Text, nullable=True)
    # The same picture serves both languages; only what is said about it differs. An empty
    # Arabic value falls back to the English one when a lesson is read.
    alt_ar = Column(Text, nullable=True)
    caption_ar = Column(Text, nullable=True)
    # Shown to the learner only when the manifest sets it.
    figure_number = Column(String(40), nullable=True)
    # Where the figure came from in the course's source material. Kept for the
    # authors; never sent to a client.
    source_reference = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    tool_course = relationship("ToolCourse")
