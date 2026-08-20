from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from app.models.community import PostType


# ─── Author mini-profile embedded in posts ────────────────────────────────────
class AuthorMini(BaseModel):
    id: int
    full_name: str
    experience_level: str
    overall_readiness_score: float
    avatar_url: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Comment ──────────────────────────────────────────────────────────────────
class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=2000)


class CommentResponse(BaseModel):
    id: int
    author: AuthorMini
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Post ─────────────────────────────────────────────────────────────────────
class PostCreate(BaseModel):
    post_type: PostType = PostType.discussion
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=10, max_length=10000)
    github_url: Optional[str] = None
    image_url: Optional[str] = None
    tags: List[str] = []


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    github_url: Optional[str] = None
    tags: Optional[List[str]] = None


class PostResponse(BaseModel):
    id: int
    post_type: PostType
    title: str
    content: str
    github_url: Optional[str]
    image_url: Optional[str]
    tags: List[str]
    likes_count: int
    comments_count: int
    is_pinned: bool
    created_at: datetime
    updated_at: Optional[datetime]
    author: AuthorMini
    liked_by_me: bool = False          # injected per-request
    comments: List[CommentResponse] = []

    class Config:
        from_attributes = True


class PostListResponse(BaseModel):
    posts: List[PostResponse]
    total: int
    page: int
    per_page: int


# ─── Follow ───────────────────────────────────────────────────────────────────
class FollowResponse(BaseModel):
    following_id: int
    is_following: bool


# ─── Leaderboard ──────────────────────────────────────────────────────────────
class LeaderboardEntry(BaseModel):
    rank: int
    user: AuthorMini
    posts_count: int
    likes_received: int
    readiness_score: float


class LeaderboardResponse(BaseModel):
    entries: List[LeaderboardEntry]