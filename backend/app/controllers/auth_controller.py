from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.models.auth_token import EmailToken, EmailTokenPurpose
from app.views.auth import (
    UserCreate, UserLogin, UserResponse, TokenResponse, UserUpdate, MessageResponse,
    VerifyEmailRequest, ForgotPasswordRequest, ResetPasswordRequest,
)
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token_for_user,
    get_current_user,
    generate_opaque_token,
    hash_opaque_token,
)
from app.core.limiter import limiter
from app.services.email.resend_service import send_verification_email, send_password_reset_email

router = APIRouter(prefix="/auth", tags=["Authentication"])

VERIFY_TOKEN_TTL = timedelta(hours=24)
RESET_TOKEN_TTL = timedelta(hours=1)


def _issue_email_token(db: Session, user: User, purpose: EmailTokenPurpose, ttl: timedelta) -> str:
    raw = generate_opaque_token()
    db.add(EmailToken(
        user_id=user.id,
        purpose=purpose,
        token_hash=hash_opaque_token(raw),
        expires_at=datetime.now(timezone.utc) + ttl,
    ))
    db.commit()
    return raw


def _consume_email_token(db: Session, raw_token: str, purpose: EmailTokenPurpose) -> User:
    token_hash = hash_opaque_token(raw_token)
    tok = db.query(EmailToken).filter(
        EmailToken.token_hash == token_hash,
        EmailToken.purpose == purpose,
    ).first()
    if not tok or tok.used_at is not None:
        raise HTTPException(status_code=400, detail="Invalid or already-used token")
    if tok.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="This link has expired")

    tok.used_at = datetime.now(timezone.utc)
    user = db.query(User).filter(User.id == tok.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    db.commit()
    return user


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(request: Request, payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        experience_level=payload.experience_level,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    raw = _issue_email_token(db, user, EmailTokenPurpose.verify_email, VERIFY_TOKEN_TTL)
    send_verification_email(user.email, user.full_name, raw)  # best-effort — see resend_service

    token = create_access_token_for_user(user)
    return TokenResponse(access_token=token, user=user)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(request: Request, payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token = create_access_token_for_user(user)
    return TokenResponse(access_token=token, user=user)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_me(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me", response_model=MessageResponse)
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Anonymizes the account rather than hard-deleting the row: PII is
    scrubbed (email/name/bio/social links), the password hash is
    invalidated, and every existing session is revoked (token_version
    bump) — but the row itself stays, since it's referenced by financial
    records (wallet transactions, exam payments) that need to survive
    account deletion for accounting/audit purposes. A hard DELETE here
    would either cascade-destroy those records or fail on the FK
    constraint, neither of which is what "delete my account" should do to
    a paid receipt.
    """
    current_user.email = f"deleted-user-{current_user.id}@deleted.invalid"
    current_user.full_name = "Deleted User"
    current_user.hashed_password = get_password_hash(generate_opaque_token())
    current_user.bio = None
    current_user.github_url = None
    current_user.linkedin_url = None
    current_user.avatar_url = None
    current_user.is_active = False
    current_user.token_version += 1  # revoke every outstanding session/token
    db.commit()
    return MessageResponse(message="Account deleted. You have been logged out everywhere.")


@router.post("/logout-all", response_model=MessageResponse)
def logout_everywhere(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Invalidates every access token issued before this call, on every
    device — the closest a stateless JWT scheme can get to "log out
    everywhere" without a token blocklist."""
    current_user.token_version += 1
    db.commit()
    return MessageResponse(message="Logged out on all devices.")


# ─── Email verification ─────────────────────────────────────────────────────

@router.post("/verify-email", response_model=MessageResponse)
@limiter.limit("10/minute")
def verify_email(request: Request, payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    user = _consume_email_token(db, payload.token, EmailTokenPurpose.verify_email)
    user.is_verified = True
    db.commit()
    return MessageResponse(message="Email verified.")


@router.post("/resend-verification", response_model=MessageResponse)
@limiter.limit("3/minute")
def resend_verification(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.is_verified:
        return MessageResponse(message="Your email is already verified.")
    raw = _issue_email_token(db, current_user, EmailTokenPurpose.verify_email, VERIFY_TOKEN_TTL)
    send_verification_email(current_user.email, current_user.full_name, raw)
    return MessageResponse(message="Verification email sent.")


# ─── Password reset ──────────────────────────────────────────────────────────

@router.post("/forgot-password", response_model=MessageResponse)
@limiter.limit("5/minute")
def forgot_password(request: Request, payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    # Always returns the same message whether or not the email exists —
    # revealing that would let anyone enumerate registered accounts.
    user = db.query(User).filter(User.email == payload.email).first()
    if user and user.is_active:
        raw = _issue_email_token(db, user, EmailTokenPurpose.reset_password, RESET_TOKEN_TTL)
        send_password_reset_email(user.email, user.full_name, raw)
    return MessageResponse(message="If that email is registered, a reset link has been sent.")


@router.post("/reset-password", response_model=MessageResponse)
@limiter.limit("5/minute")
def reset_password(request: Request, payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = _consume_email_token(db, payload.token, EmailTokenPurpose.reset_password)
    user.hashed_password = get_password_hash(payload.new_password)
    user.token_version += 1  # a password reset should also kill every existing session
    db.commit()
    return MessageResponse(message="Password reset. Please log in with your new password.")
