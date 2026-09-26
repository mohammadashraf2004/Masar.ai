"""
backend/seeds/sync_curriculum.py

Brings an EXISTING database to the curriculum described in `seeds/curriculum.py`.

`seed_learning_paths.py` only ever creates what is missing, so on a database that
already holds a catalogue it cannot change a stage, a template or a course role.
This script does that, deliberately and only for what `curriculum.py` names:

  * catalogues the placeholder levels listed in `SHELL_COURSES` as courses that
    have no lessons (so they are never startable);
  * sets each listed course's role (core / supporting / optional) per career goal;
  * sets the course list of each listed stage, creating stages that are missing;
  * sets the ordered stage list of each listed template.

Safety
------
  * Idempotent. It compares first and writes only what differs, so a second run
    changes nothing and reports nothing.
  * Never deletes a row. A course that leaves a stage, or a stage that leaves a
    template, is *unlinked*: the course and the stage stay, with their ids and
    slugs, so every saved learner path keeps resolving.
  * Never touches a learner: no path, profile, declared skill, enrolment or
    progress row is read or written. Saved paths are snapshots and stay as saved.
  * Everything goes through `catalog_admin`, the validated functions the admin
    API uses, so a prerequisite cycle or an unknown slug is refused here too.
  * One transaction: a failure leaves the database as it was. `--dry-run` runs the
    whole thing and rolls it back, printing what it would have done.

Usage (from backend/, after `alembic upgrade head`):

    python seeds/sync_curriculum.py --dry-run
    python seeds/sync_curriculum.py
"""
import argparse
import os
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session

from app.db.schema_guard import require_migrated_schema
from app.db.session import SessionLocal
import app.models.user             # noqa: F401
import app.models.learning         # noqa: F401
import app.models.progress         # noqa: F401
import app.models.community        # noqa: F401
import app.models.wallet           # noqa: F401
import app.models.auth_token       # noqa: F401
import app.models.answer_submission  # noqa: F401
import app.models.challenge        # noqa: F401
import app.models.exam             # noqa: F401
import app.models.tool_course      # noqa: F401
import app.models.learning_path    # noqa: F401

from app.models.learning_path import (
    COURSE_KIND_TOOL, PREREQ_RECOMMENDED, PREREQ_REQUIRED, CareerRole, Course, PathStage, PathTemplate, Skill,
)
from app.services.curriculum import importer as curriculum_importer
from app.services.curriculum.loaders import read_manifest_prerequisites
from app.services.learning import catalog_admin as admin
from app.services.learning.learning_service import LearningValidationError
from seeds import curriculum as cfg


@dataclass(frozen=True)
class Change:
    kind: str       # course+ | roles | stage+ | stage | template+ | template | skipped
    subject: str
    detail: str

    def __str__(self) -> str:
        return f"  {self.kind:<10} {self.subject:<28} {self.detail}"


def ensure_shell_courses(db: Session) -> List[Change]:
    """Catalogue each placeholder level in `SHELL_COURSES` that is not catalogued
    yet. A shell has no lessons, so the catalogue reports it as not available and
    no path offers it as startable. An existing course is never modified here."""
    changes: List[Change] = []
    for slug, track_slug, order, level, fields in cfg.SHELL_COURSES:
        if db.query(Course).filter(Course.slug == slug).first() is not None:
            continue
        try:
            admin.upsert_course(
                db, slug, source={"kind": "track_level", "track_slug": track_slug, "level_order": order},
                level=level, fields=fields, roles=cfg.roles_for(slug), teaches=[],
            )
        except LearningValidationError as exc:
            if exc.code != "unknown_source":
                raise
            changes.append(Change("skipped", slug, f"no level {order} in track '{track_slug}'"))
            continue
        changes.append(Change("course+", slug, f"{track_slug} level {order}, no lessons (not startable)"))
    return changes


def ensure_curriculum_courses(db: Session) -> List[Change]:
    """Catalogue the course-directory ids that are not catalogued yet.

    Each becomes a `ToolCourse` (an independent course - not a level of a
    career track) with the catalogue `Course` over it. The lesson bodies stay in
    backend/courses; `seeds/import_courses.py` loads them into the same course.
    Until then the course exists, is listed with its metadata and reads as
    "coming soon" (no lessons), so a roadmap can say where it sits.
    """
    changes: List[Change] = []
    from seeds.seed_learning_paths import SKILLS, TOOL_SKILLS

    skill_names = dict(SKILLS)
    required_skills = {
        skill for definition in cfg.COURSE_DIRECTORY_COURSES for skill in definition["skills"]
    }
    for slug in sorted(required_skills):
        if db.query(Skill).filter(Skill.slug == slug).first() is None:
            admin.upsert_skill(
                db, slug, name=skill_names[slug],
                kind="tool" if slug in TOOL_SKILLS else "skill",
            )

    for definition in cfg.COURSE_DIRECTORY_COURSES:
        slug = definition["slug"]
        if db.query(Course).filter(Course.slug == slug).first() is not None:
            continue
        curriculum_importer.ensure_course_record(db, definition)
        changes.append(Change("course+", slug, f"{definition['course_id']}, awaiting content import"))
    return changes


def sync_curriculum_course_metadata(db: Session) -> List[Change]:
    """Bring directory-course metadata to the current registry.

    A course an earlier layout pointed at an empty, synthetic track level is
    moved onto its own tool course (`importer._adopt_synthetic_source` refuses
    anything that has topics). Real course sources are never re-pointed."""
    changes: List[Change] = []
    for definition in cfg.COURSE_DIRECTORY_COURSES:
        course = db.query(Course).filter(Course.slug == definition["slug"]).first()
        if course is None:
            continue

        moved = course.kind != COURSE_KIND_TOOL
        current_fields = {link.field.slug for link in course.field_links}
        current_roles = {link.role.slug: link.relation for link in course.role_links}
        current_skills = {link.skill.slug for link in course.skill_links if link.relation == "teaches"}
        desired_roles = {item["slug"]: item["relation"] for item in cfg.roles_for(definition["slug"])}
        desired_objectives = [definition["capability"]]
        metadata_changed = (
            course.level.slug != definition["level"]
            or course.title != definition["title"]
            or course.description != definition["capability"]
            or list(course.learning_objectives or []) != desired_objectives
            or current_fields != set(definition["fields"])
            or current_roles != desired_roles
            or current_skills != set(definition["skills"])
        )
        if not (moved or metadata_changed):
            continue

        curriculum_importer.ensure_course_record(db, {**definition, "roles": desired_roles})
        changes.append(Change("course", definition["slug"],
                              "moved onto its own course; metadata reconciled" if moved else "metadata reconciled"))
    return changes


def _describe_roles(current: Dict[str, str], desired: Dict[str, str]) -> str:
    parts = []
    for goal in cfg.GOALS:
        before, after = current.get(goal), desired.get(goal)
        if before == after:
            continue
        parts.append(f"{goal}: {before or '-'} -> {after or '-'}")
    return "; ".join(parts)


def sync_roles(db: Session) -> List[Change]:
    changes: List[Change] = []
    for slug in cfg.COURSE_ROLES:
        course = db.query(Course).filter(Course.slug == slug).first()
        if course is None:
            changes.append(Change("skipped", slug, "not catalogued - roles not set"))
            continue
        current = {link.role.slug: link.relation for link in course.role_links}
        wanted = cfg.roles_for(slug)
        desired = {r["slug"]: r["relation"] for r in wanted}
        if current == desired:
            continue
        admin.set_course_relations(db, course, roles=wanted)
        changes.append(Change("roles", slug, _describe_roles(current, desired)))
    return changes


def sync_course_prerequisites(db: Session, only: Optional[Set[str]] = None) -> List[Change]:
    """Required prerequisites come from the registry (the audited hard
    dependencies the path generator orders by); recommended ones are the other
    courses each manifest names. Nothing is invented: a manifest that names no
    prerequisites adds none, and a name that is not a catalogued course is skipped."""
    changes: List[Change] = []
    catalogued = {slug for (slug,) in db.query(Course.slug).all()}
    for definition in cfg.COURSE_DIRECTORY_COURSES:
        if only is not None and definition["slug"] not in only:
            continue
        course = db.query(Course).filter(Course.slug == definition["slug"]).first()
        if course is None:
            continue
        required = [slug for slug in definition["prerequisites"] if slug in catalogued]
        recommended = [
            course_id.lower() for course_id, _kind in read_manifest_prerequisites(definition["course_id"])
            if course_id.lower() in catalogued and course_id.lower() not in required
            and course_id.lower() != definition["slug"]
        ]
        by_id = {cid: slug for cid, slug in db.query(Course.id, Course.slug).all()}
        current = {
            kind: {by_id[l.prerequisite_course_id] for l in course.prerequisite_links if l.kind == kind}
            for kind in (PREREQ_REQUIRED, PREREQ_RECOMMENDED)
        }
        if current[PREREQ_REQUIRED] == set(required) and current[PREREQ_RECOMMENDED] == set(recommended):
            continue
        admin.set_course_relations(db, course, prerequisites=required, recommended_prerequisites=recommended)
        changes.append(Change(
            "prereq", course.slug,
            f"required [{', '.join(required)}]; recommended [{', '.join(recommended)}]",
        ))
    return changes


def sync_stages(db: Session) -> List[Change]:
    changes: List[Change] = []
    catalogued = {slug for (slug,) in db.query(Course.slug).all()}
    for slug, title, title_ar, phase, kind, courses in cfg.STAGES:
        wanted = [c for c in courses if c in catalogued]
        row = db.query(PathStage).filter(PathStage.slug == slug).first()
        if row is None:
            admin.upsert_stage(db, slug, title=title, title_ar=title_ar, phase=phase, kind=kind, courses=wanted)
            changes.append(Change("stage+", slug, ", ".join(wanted) or "(no courses yet)"))
            continue
        current = [link.course.slug for link in row.course_links]
        if current == wanted:
            continue
        # Only the course list is managed; a stage's title, phase and state stay as they are.
        admin.upsert_stage(
            db, slug, title=row.title, title_ar=row.title_ar, description=row.description,
            description_ar=row.description_ar, phase=row.phase, kind=row.kind, courses=wanted,
            is_active=row.is_active,
        )
        changes.append(Change("stage", slug, f"[{', '.join(current)}] -> [{', '.join(wanted)}]"))
    return changes


def _entries(stages: List[Tuple[str, Optional[str]]]) -> List[Dict[str, Optional[str]]]:
    return [{"stage": s, "field": f} for s, f in stages]


def sync_templates(db: Session) -> List[Change]:
    changes: List[Change] = []
    goals = {slug for (slug,) in db.query(CareerRole.slug).all()}
    stages = {slug for (slug,) in db.query(PathStage.slug).all()}
    for slug, goal, title, title_ar, template_stages in cfg.TEMPLATES:
        if goal not in goals:
            changes.append(Change("skipped", slug, f"career goal '{goal}' is not in the catalogue"))
            continue
        wanted = [(s, f) for s, f in template_stages if s in stages]
        row = db.query(PathTemplate).filter(PathTemplate.slug == slug).first()
        if row is None:
            admin.upsert_template(db, slug, title=title, title_ar=title_ar, career_goal=goal, stages=_entries(wanted))
            changes.append(Change("template+", slug, " > ".join(s for s, _ in wanted)))
            continue
        current = [(link.stage.slug, link.field.slug if link.field else None) for link in row.stage_links]
        if current == wanted:
            continue
        admin.upsert_template(
            db, slug, title=row.title, title_ar=row.title_ar, description=row.description,
            description_ar=row.description_ar, career_goal=goal, stages=_entries(wanted), is_active=row.is_active,
        )
        dropped = [s for s, _ in current if s not in {w for w, _ in wanted}]
        added = [s for s, _ in wanted if s not in {c for c, _ in current}]
        changes.append(Change(
            "template", slug,
            f"{len(current)} -> {len(wanted)} stages; +[{', '.join(added)}] unlinked [{', '.join(dropped)}]"
            + ("; order changed" if not dropped and not added else ""),
        ))
    return changes


def sync_curriculum(db: Session, *, dry_run: bool = False, commit: bool = True) -> List[Change]:
    """Apply the curriculum to `db`; returns what changed (empty when already in
    sync). With `dry_run` nothing is kept. `commit=False` leaves the transaction to
    the caller (the importer syncs inside its own)."""
    try:
        changes = [
            *ensure_shell_courses(db),
            *ensure_curriculum_courses(db),
            *sync_curriculum_course_metadata(db),
            *sync_roles(db),
            *sync_course_prerequisites(db),
            *sync_stages(db),
            *sync_templates(db),
        ]
        if dry_run:
            db.rollback()
        elif commit:
            db.commit()
    except Exception:
        db.rollback()
        raise
    return changes


def main() -> None:
    parser = argparse.ArgumentParser(description="Bring the catalogue to the curriculum in seeds/curriculum.py.")
    parser.add_argument("--dry-run", action="store_true", help="show what would change and write nothing")
    args = parser.parse_args()

    require_migrated_schema()
    session = SessionLocal()
    try:
        changes = sync_curriculum(session, dry_run=args.dry_run)
    finally:
        session.close()

    for change in changes:
        print(change)
    counts: Dict[str, int] = {}
    for change in changes:
        counts[change.kind] = counts.get(change.kind, 0) + 1
    summary = ", ".join(f"{kind} {n}" for kind, n in sorted(counts.items())) or "already in sync"
    print(f"\n{'DRY RUN - nothing written. ' if args.dry_run else ''}Changes: {summary}")


if __name__ == "__main__":
    main()
