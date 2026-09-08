import hashlib
import secrets
import unicodedata
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db

# bcrypt at cost 12 (~250ms/hash on typical server hardware) — high enough
# to make offline cracking of a leaked hash expensive, low enough not to
# turn /auth/login into its own DoS amplifier.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

TOKEN_TYPE_ACCESS = "access"

# bcrypt only ever hashes the first 72 *bytes* of input and (in newer
# backends) errors outright on longer input. Rejecting at the schema layer
# keeps that implementation detail from becoming either a silent
# truncation or a 500. It also caps the CPU an unauthenticated caller can
# burn per request.
PASSWORD_MIN_LENGTH = 10
PASSWORD_MAX_BYTES = 72

# Not a substitute for a real breach corpus (see the report: the
# HaveIBeenPwned k-anonymity API is the production answer) — this just
# blocks the handful that show up in every credential-stuffing list.
_COMMON_PASSWORDS = {
    "password", "password1", "password123", "passw0rd", "123456789", "1234567890",
    "qwertyuiop", "letmein123", "welcome123", "admin12345", "iloveyou1",
    "changeme123", "football12", "sunshine12", "princess12", "monkey1234",
    "abc12345678", "qwerty12345", "1q2w3e4r5t", "trustno1234",
}


def normalize_email(email: str) -> str:
    """One canonical spelling per address, applied identically on
    registration, login and password reset. Without this, Alice@x.com and
    alice@x.com are two separate accounts that the user experiences as one
    broken one — and "email already registered" stops being a reliable
    duplicate check."""
    return unicodedata.normalize("NFKC", email).strip().lower()


def validate_password_strength(password: str, *, email: Optional[str] = None) -> str:
    """Raises ValueError with a user-safe message; returns the password
    unchanged when acceptable."""
    if len(password) < PASSWORD_MIN_LENGTH:
        raise ValueError(f"Password must be at least {PASSWORD_MIN_LENGTH} characters")
    if len(password.encode("utf-8")) > PASSWORD_MAX_BYTES:
        raise ValueError(f"Password must be at most {PASSWORD_MAX_BYTES} bytes")
    if not password.strip():
        raise ValueError("Password cannot be only whitespace")
    lowered = password.lower()
    if lowered in _COMMON_PASSWORDS:
        raise ValueError("That password is too common — please choose another")
    if len(set(password)) < 5:
        raise ValueError("Password must use at least 5 different characters")
    if email:
        local_part = normalize_email(email).split("@")[0]
        if len(local_part) >= 4 and local_part in lowered:
            raise ValueError("Password must not contain your email address")
    return password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # Malformed/legacy hash in the DB, or over-long input reaching the
        # bcrypt backend. Never let this surface as a 500 on the login path.
        return False


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# A pre-computed hash of a value nobody can supply. Verifying against it
# when the email doesn't exist makes the "no such user" path cost the same
# ~250ms as the "wrong password" path, so response time stops revealing
# which addresses are registered.
_DUMMY_HASH = pwd_context.hash("not-a-real-password-" + secrets.token_hex(16))


def verify_password_dummy() -> None:
    """Burn one bcrypt verification to equalise login timing."""
    pwd_context.verify("timing-equaliser", _DUMMY_HASH)


def generate_opaque_token() -> str:
    """A random, unguessable token for one-time links (email verification,
    password reset) — not a JWT, since it needs to be single-use and
    invalidatable independent of the access-token flow."""
    return secrets.token_urlsafe(32)


def hash_opaque_token(token: str) -> str:
    """Only this hash is ever stored — same principle as password hashing."""
    return hashlib.sha256(token.encode()).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    now = datetime.now(timezone.utc)
    to_encode = data.copy()
    to_encode.update({
        "exp": now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)),
        "iat": now,
        "nbf": now,
        "iss": settings.JWT_ISSUER,
        "aud": settings.JWT_AUDIENCE,
        "typ": TOKEN_TYPE_ACCESS,
        "jti": secrets.token_urlsafe(12),
    })
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token_for_user(user) -> str:
    """Standard access token for a User row — always embeds the current
    token_version so a password change / logout-everywhere / account
    deletion immediately invalidates tokens issued before it, even though
    JWTs are otherwise stateless.

    Deliberately carries nothing but identity: no email, no name, no role.
    A JWT payload is base64, not encrypted — anything in it is readable by
    anyone holding the token. Role in particular is re-read from the
    database on every request (see get_current_user) so a demotion takes
    effect immediately instead of whenever the token happens to expire.
    """
    return create_access_token(data={"sub": str(user.id), "tv": user.token_version})


def decode_token(token: str) -> Optional[dict]:
    """Full verification: signature, expiry, not-before, issuer and
    audience, with the required claims asserted present rather than
    merely checked-if-present.

    `algorithms` is pinned to the single configured algorithm. Trusting
    the token's own `alg` header instead is the classic
    algorithm-confusion bug — an attacker flips HS256 to "none", or
    RS256 to HS256 and signs with the public key.
    """
    try:
        return jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            issuer=settings.JWT_ISSUER,
            audience=settings.JWT_AUDIENCE,
            options={
                # A token missing any of these is rejected outright, so a
                # stripped-claims token can't slip past a check that only
                # validates the claim when it happens to be there.
                "require": ["exp", "iat", "nbf", "iss", "aud", "sub"],
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iat": True,
                "verify_iss": True,
                "verify_aud": True,
                "verify_signature": True,
            },
        )
    except (jwt.PyJWTError, ValueError, TypeError):
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    from app.models.user import User

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    # A verification/reset/refresh token must never be accepted as an
    # access token, even though all of them would be signed by this key.
    if payload.get("typ") != TOKEN_TYPE_ACCESS:
        raise credentials_exception

    user_id = payload.get("sub")
    if not isinstance(user_id, str) or not user_id.isdigit():
        # A non-numeric `sub` used to reach int() and raise ValueError —
        # a 500 an unauthenticated caller could trigger at will.
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    # Tokens issued before a password change / logout-everywhere / account
    # deletion carry the old token_version and must stop working now, even
    # though they haven't expired yet.
    if payload.get("tv") != user.token_version:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
