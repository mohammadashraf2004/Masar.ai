from datetime import datetime, timedelta, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core import login_guard, security_log
from app.core.config import settings
from app.core import legal, releases
from app.core.limiter import limiter
from app.core.security import (
    create_access_token_for_user,
    generate_opaque_token,
    get_current_user,
    get_password_hash,
    hash_opaque_token,
    verify_password,
    verify_password_dummy,
)
from app.db.session import get_db
from app.models.auth_token import EmailToken, EmailTokenPurpose
from app.models.user import User
from app.services import tour_service, update_service
from app.services.email.resend_service import send_password_reset_email, send_verification_email
from app.services.wallet.wallet_service import add_credits
from app.views.auth import (
    ForgotPasswordRequest, LegalAcceptance, MessageResponse, ResetPasswordRequest, TokenResponse,
    TourRecordResponse, TourRecordWrite, UserCreate, UserLogin, UserResponse, UserUpdate, VerifyEmailRequest,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

VERIFY_TOKEN_TTL = timedelta(hours=24)
RESET_TOKEN_TTL = timedelta(hours=1)
# The Free plan's one authoritative signup grant. Keep this beside the only
# call site so onboarding cannot accidentally stack several grants.
FREE_PLAN_CREDITS = 40


def _require_legal_acceptance(accept_terms: bool, accept_privacy: bool) -> None:
    if accept_terms is True and accept_privacy is True:
        return
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        detail={
            "error": "legal_acceptance_required",
            "message": "You must accept the Terms of Service and the Privacy Policy to continue.",
        },
    )


def _client_ip(request: Request) -> Optional[str]:
    return request.client.host if request.client else None


def _token_response(user: User) -> TokenResponse:
    return TokenResponse(
        access_token=create_access_token_for_user(user),
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user,
    )


def _issue_email_token(db: Session, user: User, purpose: EmailTokenPurpose, ttl: timedelta) -> str:
    # Any outstanding token of the same purpose is retired first, so a
    # reset link can't be resurrected by requesting a second one — and so
    # a leaked older link stops working the moment the user asks again.
    db.query(EmailToken).filter(
        EmailToken.user_id == user.id,
        EmailToken.purpose == purpose,
        EmailToken.used_at.is_(None),
    ).update({EmailToken.used_at: datetime.now(timezone.utc)}, synchronize_session=False)

    raw = generate_opaque_token()
    db.add(EmailToken(
        user_id=user.id,
        purpose=purpose,
        token_hash=hash_opaque_token(raw),
        expires_at=datetime.now(timezone.utc) + ttl,
    ))
    db.commit()
    # The raw token is returned to the caller for one purpose only:
    # putting it in the outgoing email. It is never logged, never stored,
    # and never returned in an HTTP response.
    return raw


def _consume_email_token(
    db: Session, raw_token: str, purpose: EmailTokenPurpose, ip: Optional[str]
) -> User:
    token_hash = hash_opaque_token(raw_token)
    tok = db.query(EmailToken).filter(
        EmailToken.token_hash == token_hash,
        EmailToken.purpose == purpose,
    ).with_for_update().first()

    # One generic message for "no such token", "already used" and "wrong
    # purpose" — distinguishing them tells an attacker holding a guessed
    # value which half of the guess was right.
    if not tok or tok.used_at is not None:
        security_log.token_consume_failed(purpose=purpose.value, ip=ip, reason="unknown_or_used")
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    if tok.expires_at < datetime.now(timezone.utc):
        security_log.token_consume_failed(purpose=purpose.value, ip=ip, reason="expired")
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Marked used before the caller gets to act on it: single-use is the
    # whole point, and a row lock plus an immediate write is what makes
    # two concurrent redemptions of the same link resolve to one winner.
    tok.used_at = datetime.now(timezone.utc)
    user = db.query(User).filter(User.id == tok.user_id).first()
    if not user or not user.is_active:
        db.commit()
        security_log.token_consume_failed(purpose=purpose.value, ip=ip, reason="no_active_user")
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    db.commit()
    return user


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(request: Request, payload: UserCreate, db: Session = Depends(get_db)):
    ip = _client_ip(request)
    # Checked before anything else, and on the server: the checkbox in the
    # browser is a convenience, not a control. Nothing is created without it.
    _require_legal_acceptance(payload.accept_terms, payload.accept_privacy)
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        # Deliberate trade-off, documented in the security report: this
        # does reveal that an address is registered. Every alternative
        # (silently "succeeding", emailing the owner instead) is worse UX
        # for a self-serve signup, and the same fact is discoverable from
        # any signup form that refuses duplicates. The rate limit above is
        # what keeps it from being a bulk enumeration oracle.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Acceptance is written in the same INSERT as the account, so there is no
    # window in which an account exists without its record. Versions come from
    # server configuration; the request has no say in them.
    accepted_at = datetime.now(timezone.utc)
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=get_password_hash(payload.password),
        experience_level=payload.experience_level,
        terms_version=legal.TERMS_VERSION, terms_accepted_at=accepted_at,
        privacy_version=legal.PRIVACY_VERSION, privacy_accepted_at=accepted_at,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        # Two concurrent registrations for the same address: the unique
        # index on users.email is the real arbiter, the SELECT above is
        # only a fast path. Without this, one of the two racers would get
        # a 500 (and, before the index existed, a duplicate account).
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    db.refresh(user)

    add_credits(
        user.id, FREE_PLAN_CREDITS, db,
        payment_method="admin", description="Free plan — 40 welcome credits",
        transaction_type="bonus",
    )

    raw = _issue_email_token(db, user, EmailTokenPurpose.verify_email, VERIFY_TOKEN_TTL)
    send_verification_email(user.email, user.full_name, raw)  # best-effort — see resend_service

    security_log.registration(user_id=user.id, email=user.email, ip=ip)
    security_log.legal_accepted(user_id=user.id, terms_version=legal.TERMS_VERSION,
                                privacy_version=legal.PRIVACY_VERSION, via="register")
    return _token_response(user)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(request: Request, payload: UserLogin, db: Session = Depends(get_db)):
    ip = _client_ip(request)

    # Per-account lockout, on top of the per-IP limit above. The IP limit
    # alone does nothing against credential stuffing spread across many
    # source addresses.
    wait = login_guard.seconds_until_unlocked(payload.email, ip)
    if wait:
        security_log.auth_lockout(email=payload.email, ip=ip, failures=settings.LOGIN_MAX_FAILURES)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed attempts. Try again later.",
            headers={"Retry-After": str(wait)},
        )

    user = db.query(User).filter(User.email == payload.email).first()

    # Both branches below must cost the same wall-clock time. Returning
    # early on "no such user" skips bcrypt entirely, and the resulting
    # ~250ms difference is a reliable, scriptable oracle for which
    # addresses hold accounts.
    if user is None or not user.is_active:
        verify_password_dummy()
        password_ok = False
    else:
        password_ok = verify_password(payload.password, user.hashed_password)

    if not user or not user.is_active or not password_ok:
        failures = login_guard.record_failure(payload.email, ip)
        security_log.auth_failure(
            email=payload.email, ip=ip,
            reason="bad_credentials" if user else "unknown_account",
        )
        if failures >= settings.LOGIN_MAX_FAILURES:
            security_log.auth_lockout(email=payload.email, ip=ip, failures=failures)
        # One message for every failure mode — "no such user", "wrong
        # password" and "deactivated" are indistinguishable to the caller.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    login_guard.record_success(payload.email, ip)
    security_log.auth_success(user_id=user.id, email=user.email, ip=ip)
    return _token_response(user)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/accept-legal", response_model=UserResponse)
@limiter.limit("20/minute")
def accept_legal(
    request: Request,
    payload: LegalAcceptance,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Accept the Terms and Privacy Policy as currently published - used by
    accounts that predate them, or that last accepted an older version. The
    versions recorded are the server's current ones, whatever the client
    thinks it saw."""
    _require_legal_acceptance(payload.accept_terms, payload.accept_privacy)
    if not current_user.requires_legal_acceptance:
        # Already on the current versions (a double click, a second tab, a
        # retried request): there is nothing new to record, and rewriting the
        # timestamps would replace the moment they really accepted.
        return current_user
    accepted_at = datetime.now(timezone.utc)
    current_user.terms_version, current_user.terms_accepted_at = legal.TERMS_VERSION, accepted_at
    current_user.privacy_version, current_user.privacy_accepted_at = legal.PRIVACY_VERSION, accepted_at
    db.commit()
    db.refresh(current_user)
    security_log.legal_accepted(user_id=current_user.id, terms_version=legal.TERMS_VERSION,
                                privacy_version=legal.PRIVACY_VERSION, via="reaccept")
    return current_user


@router.post("/updates/{release_id}/acknowledge", response_model=UserResponse)
@limiter.limit("30/minute")
def acknowledge_update(
    request: Request,
    release_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Say that the signed-in account has seen a product announcement.

    Only announcements the server knows are accepted, so an account cannot
    pre-dismiss one that has not shipped. Repeating it is harmless. Returns the
    account, whose `pending_updates` no longer lists it.
    """
    if release_id not in releases.KNOWN_RELEASES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown update")
    update_service.acknowledge(db, current_user.id, release_id)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("/me/tours", response_model=List[TourRecordResponse])
def list_my_tours(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Every walkthrough record the signed-in account has, in one call — the
    client fetches this once on load rather than once per tour."""
    return tour_service.list_records(db, current_user.id)


@router.get("/me/tours/{tour_id}", response_model=TourRecordResponse)
def get_my_tour(
    tour_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if tour_id not in tour_service.KNOWN_TOUR_IDS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown tour")
    record = tour_service.get_record(db, current_user.id, tour_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not seen")
    return record


@router.put("/me/tours/{tour_id}", response_model=TourRecordResponse)
@limiter.limit("60/minute")
def put_my_tour(
    request: Request,
    tour_id: str,
    payload: TourRecordWrite,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upsert the signed-in account's record for one tour. Idempotent, and safe
    to retry: see app.services.tour_service.upsert for the last-write-wins rule
    that makes a queued, out-of-order retry harmless."""
    if tour_id not in tour_service.KNOWN_TOUR_IDS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unknown tour")
    return tour_service.upsert(db, current_user.id, tour_id, payload.status, payload.version, payload.at)


@router.patch("/me", response_model=UserResponse)
def update_me(
    payload: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # exclude_unset means only fields the client actually sent are
    # applied; UserUpdate's field list is what keeps privileged columns
    # (role, is_active, is_verified, token_version, email) unreachable
    # from here no matter what the request body contains.
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
    user_id = current_user.id
    current_user.email = f"deleted-user-{user_id}@deleted.invalid"
    current_user.full_name = "Deleted User"
    current_user.hashed_password = get_password_hash(generate_opaque_token())
    current_user.bio = None
    current_user.github_url = None
    current_user.linkedin_url = None
    current_user.avatar_url = None
    current_user.is_active = False
    current_user.token_version += 1  # revoke every outstanding session/token
    # Any unredeemed verify/reset link would otherwise still resolve to
    # this row after deletion.
    db.query(EmailToken).filter(
        EmailToken.user_id == user_id,
        EmailToken.used_at.is_(None),
    ).update({EmailToken.used_at: datetime.now(timezone.utc)}, synchronize_session=False)
    db.commit()
    security_log.account_deleted(user_id=user_id)
    return MessageResponse(message="Account deleted. You have been logged out everywhere.")


@router.post("/logout-all", response_model=MessageResponse)
def logout_everywhere(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Invalidates every access token issued before this call, on every
    device — the closest a stateless JWT scheme can get to "log out
    everywhere" without a token blocklist.

    Note there is deliberately no per-token /logout endpoint: with a
    stateless JWT there is nothing server-side to delete, so the client
    discarding the token is the logout, and this is the escape hatch for
    when the token may already be in someone else's hands.
    """
    current_user.token_version += 1
    db.commit()
    security_log.sessions_revoked(user_id=current_user.id, via="logout_all")
    return MessageResponse(message="Logged out on all devices.")


# ─── Email verification ─────────────────────────────────────────────────────

@router.post("/verify-email", response_model=MessageResponse)
@limiter.limit("10/minute")
def verify_email(request: Request, payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    user = _consume_email_token(db, payload.token, EmailTokenPurpose.verify_email, _client_ip(request))
    user.is_verified = True
    db.commit()
    security_log.email_verified(user_id=user.id, ip=_client_ip(request))
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
    ip = _client_ip(request)
    user = db.query(User).filter(User.email == payload.email).first()
    if user and user.is_active:
        raw = _issue_email_token(db, user, EmailTokenPurpose.reset_password, RESET_TOKEN_TTL)
        send_password_reset_email(user.email, user.full_name, raw)
    security_log.password_reset_requested(email=payload.email, ip=ip, account_exists=bool(user))
    return MessageResponse(message="If that email is registered, a reset link has been sent.")


@router.post("/reset-password", response_model=MessageResponse)
@limiter.limit("5/minute")
def reset_password(request: Request, payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    ip = _client_ip(request)
    user = _consume_email_token(db, payload.token, EmailTokenPurpose.reset_password, ip)
    user.hashed_password = get_password_hash(payload.new_password)
    user.token_version += 1  # a password reset should also kill every existing session
    db.commit()
    # Clears any lockout the attack that prompted the reset may have left
    # on the legitimate owner.
    login_guard.record_success(user.email, ip)
    security_log.password_changed(user_id=user.id, via="reset", ip=ip)
    security_log.sessions_revoked(user_id=user.id, via="password_reset")
    return MessageResponse(message="Password reset. Please log in with your new password.")
