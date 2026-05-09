from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole, ExperienceLevel


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=8)
    experience_level: ExperienceLevel = ExperienceLevel.beginner


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    experience_level: Optional[ExperienceLevel] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    experience_level: ExperienceLevel
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
    user: UserResponse


class MessageResponse(BaseModel):
    message: str
