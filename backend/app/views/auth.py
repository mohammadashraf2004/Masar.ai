from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.security import PASSWORD_MAX_BYTES, PASSWORD_MIN_LENGTH, normalize_email, validate_password_strength
from app.models.user import ExperienceLevel, UserRole

# Anything a user can store and another user's browser might later be
# handed as a link. Only these two schemes are ever safe to put in an
# href: "javascript:" and "data:" both execute in the clicker's origin,
# which — with the access token in localStorage — is account takeover.
_ALLOWED_URL_SCHEMES = {"http", "https"}
MAX_URL_LENGTH = 500


def validate_public_url(value: Optional[str]) -> Optional[str]:
    """Shared by every user-supplied URL field in the API."""
    if value is None:
        return None
    value = value.strip()
    if not value:
        return None
    if len(value) > MAX_URL_LENGTH:
        raise ValueError(f"URL must be at most {MAX_URL_LENGTH} characters")
    parsed = urlparse(value)
    if parsed.scheme.lower() not in _ALLOWED_URL_SCHEMES:
        raise ValueError("URL must start with http:// or https://")
    if not parsed.netloc:
        raise ValueError("URL must include a hostname")
    return value


class _EmailNormalizingModel(BaseModel):
    """Registration, login and password-reset must agree on what counts as
    the same address, or a user who signs up as `Sam@x.com` can't log in
    as `sam@x.com` and `forgot-password` silently finds nobody."""

    @field_validator("email", mode="after", check_fields=False)
    @classmethod
    def _normalize(cls, v: str) -> str:
        return normalize_email(v)


class UserCreate(_EmailNormalizingModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_BYTES)
    experience_level: ExperienceLevel = ExperienceLevel.beginner

    @field_validator("full_name", mode="after")
    @classmethod
    def _clean_name(cls, v: str) -> str:
        v = " ".join(v.split())
        if not v:
            raise ValueError("Name cannot be blank")
        return v

    @field_validator("password", mode="after")
    @classmethod
    def _strong_password(cls, v: str, info) -> str:
        try:
            return validate_password_strength(v, email=info.data.get("email"))
        except ValueError as e:
            raise ValueError(str(e))


class UserLogin(_EmailNormalizingModel):
    email: EmailStr
    # Bounded so an unauthenticated caller can't push megabytes through
    # the bcrypt path; strength is NOT checked here (an existing account
    # may predate the current policy — that's what the reset flow is for).
    password: str = Field(..., min_length=1, max_length=PASSWORD_MAX_BYTES)


class VerifyEmailRequest(BaseModel):
    token: str = Field(..., min_length=16, max_length=512)


class ForgotPasswordRequest(_EmailNormalizingModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=16, max_length=512)
    new_password: str = Field(..., min_length=PASSWORD_MIN_LENGTH, max_length=PASSWORD_MAX_BYTES)

    @field_validator("new_password", mode="after")
    @classmethod
    def _strong_password(cls, v: str) -> str:
        try:
            return validate_password_strength(v)
        except ValueError as e:
            raise ValueError(str(e))


class UserUpdate(BaseModel):
    """The set of fields a user may change about themselves.

    Everything privileged is absent by construction — role, is_active,
    is_verified, token_version, overall_readiness_score, email. The
    controller applies exactly what lands here, so a request body carrying
    `"role": "admin"` is dropped by pydantic before it can reach setattr()
    rather than being filtered out later by a check someone might forget.
    """
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    bio: Optional[str] = Field(None, max_length=2000)
    github_url: Optional[str] = Field(None, max_length=MAX_URL_LENGTH)
    linkedin_url: Optional[str] = Field(None, max_length=MAX_URL_LENGTH)
    experience_level: Optional[ExperienceLevel] = None

    @field_validator("github_url", "linkedin_url", mode="after")
    @classmethod
    def _safe_url(cls, v: Optional[str]) -> Optional[str]:
        return validate_public_url(v)

    @field_validator("full_name", mode="after")
    @classmethod
    def _clean_name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = " ".join(v.split())
        if not v:
            raise ValueError("Name cannot be blank")
        return v


class UserResponse(BaseModel):
    """Never includes hashed_password, token_version, or is_active —
    response_model on the route is what actually enforces that, so any
    future column added to User is excluded by default rather than
    included by default."""
    id: int
    email: str
    full_name: str
    role: UserRole
    experience_level: ExperienceLevel
    is_verified: bool
    bio: Optional[str]
    github_url: Optional[str]
    linkedin_url: Optional[str]
    avatar_url: Optional[str]
    overall_readiness_score: float
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int          # seconds — lets the client refresh/redirect proactively
    user: UserResponse


class MessageResponse(BaseModel):
    message: str
