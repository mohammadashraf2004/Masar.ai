"""
app/services/learning/track_workflow.py

The fixed career-track workflow: Data Analyst, ML Engineer, AI Developer,
MLOps Engineer, AI Engineer — each an explicitly ordered sequence over the
same canonical courses every other learning-path endpoint serves, never a
second copy of them.

Order, role, required-ness and section all come from `course_roles`
(`position`, `relation`, `required`, `section`) — the same association the
rest of the catalogue uses — never from a course's primary key and never
re-derived on the client. This module turns that association plus a
learner's progress into one status per course:

    completed   - finished (>= 100%)
    in_progress - started, not finished
    next        - the first course the learner can start and has not
    locked      - a *required* prerequisite of this course is not finished
    available   - reachable, not started, not (yet) "next"

Only a course's own real prerequisites (`CourseInfo.prerequisite_ids`) lock
it — never its position in this track's workflow, and never an optional
course. An optional course (`role == 'optional'` or `required == False`)
never counts toward `required_total` / `required_completed` and never blocks
a later required course from being available.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

from sqlalchemy.orm import Session

from app.services.learning.catalog_service import CatalogBundle
from app.services.learning.domain import CourseInfo
from app.services.learning.progress_service import course_completion, pct

_DONE = 1.0 - 1e-9


@dataclass(frozen=True)
class WorkflowCourse:
    info: CourseInfo
    role: str
    order: int
    required: bool
    section: Optional[str]
    status: str
    progress_fraction: float


@dataclass(frozen=True)
class Workflow:
    role_slug: str
    courses: List[WorkflowCourse]
    required_total: int
    required_completed: int
    progress_percent: float
    current: Optional[CourseInfo]
    next: Optional[CourseInfo]
    has_sections: bool


def _fraction(completion: Dict[int, float], course_id: int) -> float:
    return completion.get(course_id, 0.0)


def build_workflow(
    db: Session, bundle: CatalogBundle, role_slug: str, user_id: Optional[int] = None,
) -> Optional[Workflow]:
    """The ordered workflow for one career goal, or None when the goal is not
    in the catalogue or has no courses placed in it yet."""
    if role_slug not in bundle.roles:
        return None

    # A role tag by itself is catalogue/discovery metadata. Only a positive
    # workflow position opts a course into this fixed track; legacy courses
    # and tool courses keep their role tags without leaking into the canonical
    # 16-course workflow as position-zero entries.
    members: Sequence[CourseInfo] = sorted(
        (
            info for info in bundle.catalog.courses.values()
            if (placement := info.workflow_for(role_slug)) is not None and placement.position > 0
        ),
        key=lambda info: (info.workflow_for(role_slug).position, info.id),
    )
    if not members:
        return None

    member_by_id = {info.id: info for info in members}
    progress_ids = {info.id for info in members}
    progress_ids.update(pid for info in members for pid in info.prerequisite_ids)
    completion: Dict[int, float] = (
        course_completion(
            db, user_id,
            [bundle.courses[cid] for cid in progress_ids if cid in bundle.courses],
        )
        if user_id else {}
    )

    completed_ids = {cid for cid, fraction in completion.items() if fraction >= _DONE}

    def is_locked(info: CourseInfo) -> bool:
        # Only *required* prerequisites lock a course, and only ones that are
        # themselves catalogued courses today - never this track's own order.
        # A course that this track explicitly marks optional/non-required must
        # never gate a required course later in the same workflow.
        for pid in info.prerequisite_ids:
            if pid not in bundle.catalog.courses:
                continue
            prerequisite = member_by_id.get(pid)
            if prerequisite is not None:
                placement = prerequisite.workflow_for(role_slug)
                if placement is not None and info.workflow_for(role_slug).required and (
                    placement.relation == "optional" or not placement.required
                ):
                    continue
            if pid not in completed_ids:
                return True
        return False

    provisional: List[WorkflowCourse] = []
    for info in members:
        workflow = info.workflow_for(role_slug)
        fraction = _fraction(completion, info.id)
        if info.id in completed_ids:
            status = "completed"
        elif fraction > 0:
            status = "in_progress"
        elif is_locked(info):
            status = "locked"
        else:
            status = "available"
        provisional.append(WorkflowCourse(
            info=info, role=workflow.relation, order=workflow.position,
            required=workflow.required, section=workflow.section,
            status=status, progress_fraction=fraction,
        ))

    # Recommend the first reachable, startable required course. Optional
    # branches are a fallback only when there is no required course to start;
    # they never divert or block the main workflow.
    next_candidate = next(
        (wc.info.id for wc in provisional if wc.status == "available" and wc.required and wc.info.is_available),
        None,
    )
    if next_candidate is None:
        next_candidate = next(
            (wc.info.id for wc in provisional if wc.status == "available" and wc.info.is_available),
            None,
        )
    courses: List[WorkflowCourse] = []
    for wc in provisional:
        if wc.info.id == next_candidate:
            wc = WorkflowCourse(
                info=wc.info, role=wc.role, order=wc.order, required=wc.required,
                section=wc.section, status="next", progress_fraction=wc.progress_fraction,
            )
        courses.append(wc)

    required_courses = [wc for wc in courses if wc.required]
    required_total = len(required_courses)
    required_completed = sum(1 for wc in required_courses if wc.status == "completed")
    # Path completion is deliberately course-based: completed required courses
    # divided by all required courses. Partial lesson progress remains visible
    # on its course node but does not make the path itself look completed.
    progress_percent = pct(required_completed / required_total) if required_total else 0.0

    current = next(
        (wc.info for wc in reversed(courses) if wc.status == "in_progress"),
        None,
    )
    if current is None:
        # No course in progress: the most recently reachable completed one, if
        # any, else nothing started yet.
        completed_in_order = [wc.info for wc in courses if wc.status == "completed"]
        current = completed_in_order[-1] if completed_in_order else None
    next_course = next((wc.info for wc in courses if wc.status == "next"), None)

    return Workflow(
        role_slug=role_slug, courses=courses, required_total=required_total,
        required_completed=required_completed, progress_percent=progress_percent,
        current=current, next=next_course,
        has_sections=any(wc.section for wc in courses),
    )
