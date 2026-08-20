from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime,
    Text, ForeignKey, Enum, UniqueConstraint, JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.session import Base


class PostType(str, enum.Enum):
    problem   = "problem"    # asking for help
    project   = "project"    # sharing a project
    achievement = "achievement"  # milestone / win
    resource  = "resource"   # sharing a useful link or tip
    discussion = "discussion" # general topic


class Post(Base):
    __tablename__ = "community_posts"

    id          = Column(Integer, primary_key=True, index=True)
    author_id   = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_type   = Column(Enum(PostType), nullable=False, default=PostType.discussion)
    title       = Column(String(200), nullable=False)
    content     = Column(Text, nullable=False)
    # optional extras
    github_url  = Column(String, nullable=True)
    image_url   = Column(String, nullable=True)
    tags        = Column(JSON, default=list)        # ["python", "pytorch"]
    # counters — denormalised for speed
    likes_count    = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)
    is_pinned   = Column(Boolean, default=False)
    created_at  = Column(DateTime(timezone=True), server_default=func.now())
    updated_at  = Column(DateTime(timezone=True), onupdate=func.now())

    author   = relationship("User",    back_populates="posts")
    likes    = relationship("PostLike",    back_populates="post", cascade="all, delete-orphan")
    comments = relationship("PostComment", back_populates="post", cascade="all, delete-orphan",
                            order_by="PostComment.created_at")


class PostLike(Base):
    __tablename__ = "community_post_likes"
    __table_args__ = (UniqueConstraint("user_id", "post_id"),)

    id      = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    post = relationship("Post", back_populates="likes")


class PostComment(Base):
    __tablename__ = "community_post_comments"

    id        = Column(Integer, primary_key=True, index=True)
    post_id   = Column(Integer, ForeignKey("community_posts.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content   = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    post   = relationship("Post",  back_populates="comments")
    author = relationship("User",  back_populates="comments")


class UserFollow(Base):
    """User A follows User B."""
    __tablename__ = "community_user_follows"
    __table_args__ = (UniqueConstraint("follower_id", "following_id"),)

    id           = Column(Integer, primary_key=True, index=True)
    follower_id  = Column(Integer, ForeignKey("users.id"), nullable=False)
    following_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())