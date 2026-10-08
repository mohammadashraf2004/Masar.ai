"""Server-owned presentation of career tracks backed by canonical courses.

The catalogue metadata comes from ``CareerTrack`` and every course/progress
fact comes from the canonical ``course_roles`` workflow.  There is deliberately
no second, hand-written curriculum here.
"""
from __future__ import annotations

from typing import Any, Iterable, Optional

from sqlalchemy.orm import Session

from app.models.exam import Certificate
from app.models.learning import CareerTrack
from app.models.learning_path import CareerRole, LearningProfile
from app.models.progress import Enrollment
from app.models.user import User
from app.services.learning.catalog_service import CatalogBundle, load_catalog_bundle
from app.services.learning.track_workflow import Workflow, build_workflow


TRACK_ORDER = ("data-analyst", "ml-engineer", "ai-developer", "mlops-engineer", "ai-engineer")


def _profile_role(db: Session, user: Optional[User]) -> Optional[str]:
    if user is None:
        return None
    row = db.query(LearningProfile).filter(LearningProfile.user_id == user.id).first()
    if row is None or row.career_role_id is None:
        return None
    role = db.query(CareerRole.slug).filter(CareerRole.id == row.career_role_id).first()
    return role[0] if role else None


def _legacy_enrollments(db: Session, user: Optional[User]) -> dict[int, Enrollment]:
    if user is None:
        return {}
    return {
        row.track_id: row for row in db.query(Enrollment).filter(
            Enrollment.user_id == user.id, Enrollment.is_active.is_(True),
        ).all()
    }


def _progress(workflow: Optional[Workflow], enrollment: Optional[Enrollment]) -> float:
    required = [row.progress_fraction for row in workflow.courses if row.required] if workflow else []
    live = round(sum(required) / len(required) * 100, 1) if required else 0.0
    legacy = float(enrollment.completion_percentage or 0) if enrollment else 0.0
    return min(100.0, max(live, legacy))


def _course_href(workflow: Optional[Workflow], *, start: bool) -> str:
    if workflow is None or not workflow.courses:
        return "/courses"
    if start:
        target = next((c for c in workflow.courses if c.info.is_available), workflow.courses[0])
        return f"/courses/{target.info.slug}"
    target = workflow.current or workflow.next
    if target is None:
        target = next((c.info for c in workflow.courses if c.info.is_available), workflow.courses[0].info)
    return f"/courses/{target.slug}/learn"


def _card(track: CareerTrack, *, workflow: Optional[Workflow], enrollment: Optional[Enrollment],
          profile_role: Optional[str]) -> dict[str, Any]:
    progress = _progress(workflow, enrollment)
    engaged = profile_role == track.slug or enrollment is not None or progress > 0
    status = "done" if progress >= 100 else "current" if engaged else "open"
    href = "/certificates" if status == "done" else _course_href(workflow, start=status == "open")
    return {
        "id": track.id, "slug": track.slug, "title": track.title,
        "title_en": track.title, "title_ar": track.title_ar or track.title,
        "description": track.description or "", "description_ar": track.description_ar,
        "icon": track.icon, "estimated_weeks": track.estimated_weeks,
        "stack": [], "level": None,
        "stage_count": 0,
        "course_count": len(workflow.courses) if workflow else 0,
        "hours": round(sum(row.info.estimated_hours for row in workflow.courses)) if workflow else 0,
        "progress": progress, "status": status, "cta_href": href,
    }


def catalogue(db: Session, tracks: Iterable[CareerTrack], user: Optional[User]) -> list[dict[str, Any]]:
    bundle = load_catalog_bundle(db)
    profile_role = _profile_role(db, user)
    enrollments = _legacy_enrollments(db, user)
    result = []
    for track in tracks:
        workflow = build_workflow(db, bundle, track.slug, user.id if user else None)
        result.append(_card(
            track, workflow=workflow, enrollment=enrollments.get(track.id), profile_role=profile_role,
        ))
    result.sort(key=lambda row: TRACK_ORDER.index(row["slug"]) if row["slug"] in TRACK_ORDER else 99)
    return result


def detail(db: Session, track: CareerTrack, user: Optional[User]) -> dict[str, Any]:
    bundle: CatalogBundle = load_catalog_bundle(db)
    workflow = build_workflow(db, bundle, track.slug, user.id if user else None)
    enrollment = _legacy_enrollments(db, user).get(track.id)
    card = _card(track, workflow=workflow, enrollment=enrollment, profile_role=_profile_role(db, user))
    required_total = workflow.required_total if workflow else 0

    cert = None
    if user is not None:
        cert = db.query(Certificate).filter(
            Certificate.user_id == user.id, Certificate.track_id == track.id, Certificate.is_valid.is_(True),
        ).order_by(Certificate.issued_at.desc()).first()
    exam = {"status": "passed", "score": cert.score, "unlock_after_stage": required_total} if cert else {
        "status": "available" if card["progress"] >= 100 else "locked",
        "score": None, "unlock_after_stage": required_total,
    }
    return {
        **card,
        "levels": track.levels,
        "stages": [],
        "projects": [],
        "roles": [track.title],
        "exam": exam,
    }
