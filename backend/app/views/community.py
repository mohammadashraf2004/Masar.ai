from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.models.community import PostType
from app.views.auth import MAX_URL_LENGTH, validate_public_url


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
class _PostUrlValidation(BaseModel):
    """github_url and image_url are stored, then handed to other users'
    browsers as an href / img src. A "javascript:" or "data:text/html"
    value there executes in the *viewer's* origin — and with the access
    token in localStorage that is a one-click account takeover, i.e.
    stored XSS. Rejecting non-http(s) schemes at the API is the fix that
    holds regardless of which client renders the post."""

    @field_validator("github_url", "image_url", mode="after", check_fields=False)
    @classmethod
    def _safe_url(cls, v: Optional[str]) -> Optional[str]:
        return validate_public_url(v)

    @field_validator("tags", mode="after", check_fields=False)
    @classmethod
    def _clean_tags(cls, v):
        if v is None:
            return v
        cleaned = [t.strip()[:40] for t in v if isinstance(t, str) and t.strip()]
        return cleaned[:10]


class PostCreate(_PostUrlValidation):
    post_type: PostType = PostType.discussion
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=10, max_length=10000)
    github_url: Optional[str] = Field(None, max_length=MAX_URL_LENGTH)
    image_url: Optional[str] = Field(None, max_length=MAX_URL_LENGTH)
    tags: List[str] = Field(default_factory=list, max_length=10)


class PostUpdate(_PostUrlValidation):
    """No is_pinned / likes_count / comments_count / author_id here on
    purpose: update_post applies exactly the fields this model accepts,
    so anything absent is unreachable from a client-supplied body."""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    content: Optional[str] = Field(None, min_length=10, max_length=10000)
    github_url: Optional[str] = Field(None, max_length=MAX_URL_LENGTH)
    tags: Optional[List[str]] = Field(None, max_length=10)


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