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


def is_admin(user: User) -> bool:
    return _role_of(user) is UserRole.admin


def roles_named(names: Iterable[str]) -> tuple[UserRole, ...]:
    """Small helper for config-driven role lists."""
    return tuple(UserRole(n) for n in names)
