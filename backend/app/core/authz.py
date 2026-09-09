"""
backend/app/core/authz.py

Role-based authorization, in one place.

Authentication (get_current_user) only answers "who is this?". Every
endpoint that does something privileged has to separately answer "is this
person allowed to?" — and before this module those checks were four
copy-pasted `if current_user.role.value != "admin"` lines scattered
across two controllers. One forgotten copy is an admin endpoint open to
every logged-in student, so the check lives here as a dependency and the
controllers just declare which roles they need.

The role is read from the *database row* loaded on this request, never
from a JWT claim: a claim is frozen at token-issuance time, so a user
demoted from admin would keep admin rights until their token expired.
"""
from typing import Iterable

from fastapi import Depends, HTTPException, status

from app.core.security import get_current_user
from app.models.user import User, UserRole


def _role_of(user: User) -> UserRole:
    """Rows created before `role` was made NOT NULL can still carry NULL;
    treat an absent role as the least-privileged one rather than letting
    `user.role.value` raise AttributeError (a 500 on an authz check is a
    fail-open in disguise if anything upstream ever catches it)."""
    return user.role or UserRole.student


def require_roles(*allowed: UserRole):
    """Dependency factory. Usage:

        @router.post("/admin/thing", dependencies=[Depends(require_admin)])

    or, when the handler needs the user object:

        admin: User = Depends(require_roles(UserRole.admin))

    New roles (instructor, moderator) plug in here without touching a
    single endpoint body: add the enum member, then list it in the
    endpoints it should reach.
    """
    allowed_set = set(allowed)

    def _dependency(current_user: User = Depends(get_current_user)) -> User:
        if _role_of(current_user) not in allowed_set:
            # Deliberately identical for "you're a student" and "that
            # resource doesn't exist for you" — a 403 that varies its
            # wording maps out the admin surface for anyone probing it.
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return _dependency


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    return require_roles(UserRole.admin)(current_user)


# ─── Email verification ─────────────────────────────────────────────────────
# Registration hands back a working access token immediately, which is the
# right call for signup UX — but `is_verified` was then stored and never
# read, so a throwaway address could spend the signup credit grant on real
# inference. With LAUNCH_PROMO_CREDITS=500 and mentor_chat at 2 credits
# that is 250 provider calls per disposable mailbox, billed to us.
#
# The gate is therefore drawn around *billable* work only, and it is
# enforced in two places rather than pasted into every controller:
#
#   1. wallet_service.deduct_credits() — the choke point every credit
#      spend already funnels through. Enforcing there means a new billable
#      endpoint is covered the day it is written, with nothing to remember.
#   2. require_verified_user, below — for the two LLM-backed endpoints that
#      are NOT metered by the wallet (project submit, challenge submit), so
#      the guard has to be attached explicitly.
#
# Deliberately NOT gated: login, the verification and password-reset flows
# themselves, profile reads, catalogue browsing, wallet top-ups. Anything a
# user needs in order to *become* verified, or to pay us, has to keep
# working while unverified.

EMAIL_VERIFICATION_REQUIRED = "email_verification_required"


def email_verification_error() -> HTTPException:
    """The single canonical response for "verify your email first".

    403, not 401: the credentials are valid and re-authenticating will not
    help, so a client must not treat this as an expired session and bounce
    the user to the login screen. The machine-readable `error` field is
    what the frontend should branch on; `message` is safe to show as-is.
    """
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "error": EMAIL_VERIFICATION_REQUIRED,
            "message": (
                "Please verify your email address to use this feature. "
                "Check your inbox for the verification link, or request a "
                "new one from your profile."
            ),
        },
    )


def is_email_verified(user: User) -> bool:
    return bool(getattr(user, "is_verified", False))


def require_verified_user(current_user: User = Depends(get_current_user)) -> User:
    """Dependency for billable endpoints that do NOT go through
    deduct_credits() — currently the two LLM calls covered by a flat fee
    rather than per-call metering. Everything metered by the wallet is
    covered by deduct_credits() itself and must not repeat this check."""
    if not is_email_verified(current_user):
        raise email_verification_error()
    return current_user


def is_admin(user: User) -> bool:
    return _role_of(user) is UserRole.admin


def roles_named(names: Iterable[str]) -> tuple[UserRole, ...]:
    """Small helper for config-driven role lists."""
    return tuple(UserRole(n) for n in names)
