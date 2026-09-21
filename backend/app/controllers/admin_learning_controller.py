"""
app/controllers/admin_learning_controller.py

Content management for the learning catalogue. Admin only.

    PUT /admin/learning/levels/{slug}          levels
    PUT /admin/learning/fields/{slug}          fields, incl. prerequisites
    PUT /admin/learning/career-goals/{slug}    career goals, incl. skills and fields
    PUT /admin/learning/skills/{slug}
    PUT /admin/learning/courses/{slug}         course <-> field / goal / skill / prerequisite
    PUT /admin/learning/stages/{slug}          a stage and the courses inside it
    PUT /admin/learning/templates/{slug}       a career goal's stage order
    GET /admin/learning/catalog                everything, inactive included
    GET /admin/learning/health                 configuration problems

There is no DELETE: retiring something is `is_active: false`, which takes it
out of the catalogue and out of new paths while every learner's saved path
keeps resolving.

Authorization is `require_admin` on every route — the same dependency the rest
of the admin surface uses — and every write is recorded through
`security_log.admin_action`. Validation (unknown slugs, prerequisite cycles,
duplicate stages) lives in `catalog_admin` and is shared with the seed script;
a failure rolls the whole request back, so a half-applied change is never
visible.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core import security_log
from app.core.authz import require_admin
from app.core.limiter import limiter
from app.db.session import get_db
from app.models.learning_path import (
    ROLE_FIELD_RECOMMENDED, ROLE_FIELD_REQUIRED, SKILL_ASSUMES, SKILL_TEACHES,
    CareerRole, Course, LearningField, LearningFieldPrerequisite, LearningLevel, PathStage,
    PathTemplate, Skill,
)
from app.models.user import User
from app.services.learning import catalog_admin as admin
from app.services.learning.learning_service import LearningValidationError
from app.views.learning_admin import (
    CareerGoalAdminOut, CareerGoalIn, CatalogIssueOut, CourseAdminOut, CourseIn, FieldAdminOut,
    FieldIn, LevelAdminOut, LevelIn, SkillAdminOut, SkillIn, StageAdminOut, StageIn,
    TemplateAdminOut, TemplateIn, TemplateStageOut,
)
from app.views.learning_path import Slug

router = APIRouter(prefix="/admin/learning", tags=["Admin Learning"])


def _apply(db: Session, admin_user: User, action: str, target: str, work):
    """Run one write, roll everything back if it is refused, and audit it."""
    try:
        result = work()
        db.commit()
    except LearningValidationError as exc:
        db.rollback()
        raise HTTPException(status_code=422, detail={"error": exc.code, "message": exc.detail})
    security_log.admin_action(admin_id=admin_user.id, action=action, target=target)
    return result


# ─── Row -> admin view ──────────────────────────────────────────────────────
# Every write answers with the configuration it just saved, expressed in slugs —
# the same statement an admin screen would submit back. It never depends on the
# public catalogue view, so a field or course that was just deactivated (and so
# no longer appears there) still answers.

def _slugs(db: Session):
    return {
        "level": {r.id: r.slug for r in db.query(LearningLevel).all()},
        "field": {r.id: r.slug for r in db.query(LearningField).all()},
        "role": {r.id: r.slug for r in db.query(CareerRole).all()},
        "skill": {r.id: r.slug for r in db.query(Skill).all()},
        "course": {r.id: r.slug for r in db.query(Course).all()},
        "stage": {r.id: r.slug for r in db.query(PathStage).all()},
    }


def _level_out(r: LearningLevel) -> LevelAdminOut:
    return LevelAdminOut(slug=r.slug, name=r.name, name_ar=r.name_ar, description=r.description,
                         description_ar=r.description_ar, rank=r.rank, is_active=r.is_active)


def _field_out(db: Session, r: LearningField, s) -> FieldAdminOut:
    prereqs = db.query(LearningFieldPrerequisite).filter(LearningFieldPrerequisite.field_id == r.id).all()
    return FieldAdminOut(
        slug=r.slug, name=r.name, name_ar=r.name_ar, description=r.description,
        description_ar=r.description_ar, icon=r.icon, min_level=s["level"].get(r.min_level_id),
        prerequisites=[s["field"][p.prerequisite_field_id] for p in prereqs],
        prerequisite_min_required=r.prerequisite_min_required,
        prerequisite_recommended=r.prerequisite_recommended, position=r.position, is_active=r.is_active,
    )


def _goal_out(r: CareerRole, s) -> CareerGoalAdminOut:
    return CareerGoalAdminOut(
        slug=r.slug, title=r.title, title_ar=r.title_ar, description=r.description,
        description_ar=r.description_ar, icon=r.icon, position=r.position, is_active=r.is_active,
        recommended_level=s["level"].get(r.recommended_level_id),
        required_fields=[s["field"][l.field_id] for l in r.field_links if l.relation == ROLE_FIELD_REQUIRED],
        recommended_fields=[s["field"][l.field_id] for l in r.field_links if l.relation == ROLE_FIELD_RECOMMENDED],
        required_skills=[s["skill"][l.skill_id] for l in r.skill_links if l.is_required],
        optional_skills=[s["skill"][l.skill_id] for l in r.skill_links if not l.is_required],
    )


def _course_out(c: Course, s) -> CourseAdminOut:
    return CourseAdminOut(
        slug=c.slug, kind=c.kind, level=s["level"][c.level_id], title=c.title,
        fields=[s["field"][l.field_id] for l in c.field_links],
        roles=[s["role"][l.role_id] for l in c.role_links],
        teaches=[s["skill"][l.skill_id] for l in c.skill_links if l.relation == SKILL_TEACHES],
        assumes=[s["skill"][l.skill_id] for l in c.skill_links if l.relation == SKILL_ASSUMES],
        prerequisites=[s["course"][l.prerequisite_course_id] for l in c.prerequisite_links],
        is_active=c.is_active,
    )


def _stage_out(r: PathStage, s) -> StageAdminOut:
    return StageAdminOut(
        slug=r.slug, title=r.title, title_ar=r.title_ar, phase=r.phase, kind=r.kind,
        courses=[s["course"][l.course_id] for l in r.course_links], is_active=r.is_active,
    )


def _template_out(r: PathTemplate, s) -> TemplateAdminOut:
    return TemplateAdminOut(
        slug=r.slug, title=r.title, title_ar=r.title_ar, career_goal=s["role"].get(r.career_role_id),
        stages=[TemplateStageOut(stage=s["stage"][l.stage_id], field=s["field"].get(l.field_id))
                for l in r.stage_links],
        is_active=r.is_active,
    )


# ─── Writes ─────────────────────────────────────────────────────────────────

@router.put("/levels/{slug}", response_model=LevelAdminOut)
@limiter.limit("60/minute")
def put_level(request: Request, slug: Slug, payload: LevelIn,
              admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    level = _apply(db, admin_user, "learning.level.upsert", slug,
                   lambda: admin.upsert_level(db, slug, **payload.model_dump()))
    return _level_out(level)


@router.put("/skills/{slug}", response_model=SkillAdminOut)
@limiter.limit("60/minute")
def put_skill(request: Request, slug: Slug, payload: SkillIn,
              admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    skill = _apply(db, admin_user, "learning.skill.upsert", slug,
                   lambda: admin.upsert_skill(db, slug, **payload.model_dump()))
    return SkillAdminOut(slug=skill.slug, name=skill.name, name_ar=skill.name_ar, kind=skill.kind)


@router.put("/fields/{slug}", response_model=FieldAdminOut)
@limiter.limit("60/minute")
def put_field(request: Request, slug: Slug, payload: FieldIn,
              admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    field = _apply(db, admin_user, "learning.field.upsert", slug,
                   lambda: admin.upsert_field(db, slug, **payload.model_dump()))
    return _field_out(db, field, _slugs(db))


@router.put("/career-goals/{slug}", response_model=CareerGoalAdminOut)
@limiter.limit("60/minute")
def put_career_goal(request: Request, slug: Slug, payload: CareerGoalIn,
                    admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    role = _apply(db, admin_user, "learning.career_goal.upsert", slug,
                  lambda: admin.upsert_career_goal(db, slug, **payload.model_dump()))
    return _goal_out(role, _slugs(db))


@router.put("/courses/{slug}", response_model=CourseAdminOut)
@limiter.limit("60/minute")
def put_course(request: Request, slug: Slug, payload: CourseIn,
               admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    body = payload.model_dump()
    source = body.pop("source")
    course = _apply(db, admin_user, "learning.course.upsert", slug,
                    lambda: admin.upsert_course(db, slug, source=source, **body))
    return _course_out(course, _slugs(db))


@router.put("/stages/{slug}", response_model=StageAdminOut)
@limiter.limit("60/minute")
def put_stage(request: Request, slug: Slug, payload: StageIn,
              admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    stage = _apply(db, admin_user, "learning.stage.upsert", slug,
                   lambda: admin.upsert_stage(db, slug, **payload.model_dump()))
    return _stage_out(stage, _slugs(db))


@router.put("/templates/{slug}", response_model=TemplateAdminOut)
@limiter.limit("60/minute")
def put_template(request: Request, slug: Slug, payload: TemplateIn,
                 admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    template = _apply(db, admin_user, "learning.template.upsert", slug,
                      lambda: admin.upsert_template(db, slug, **payload.model_dump()))
    return _template_out(template, _slugs(db))


# ─── Reads ──────────────────────────────────────────────────────────────────

@router.get("/catalog")
def get_catalog(admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """The whole configuration, inactive entries included — what an admin screen
    renders. (The public `/learning/*` reads show only what is live.)"""
    s = _slugs(db)
    return {
        "levels": [_level_out(r) for r in db.query(LearningLevel).order_by(LearningLevel.rank).all()],
        "fields": [_field_out(db, r, s) for r in db.query(LearningField).order_by(LearningField.position).all()],
        "career_goals": [_goal_out(r, s) for r in db.query(CareerRole).order_by(CareerRole.position).all()],
        "skills": [SkillAdminOut(slug=r.slug, name=r.name, name_ar=r.name_ar, kind=r.kind)
                   for r in db.query(Skill).order_by(Skill.slug).all()],
        "courses": [_course_out(r, s) for r in db.query(Course).order_by(Course.id).all()],
        "stages": [_stage_out(r, s) for r in db.query(PathStage).order_by(PathStage.id).all()],
        "templates": [_template_out(r, s) for r in db.query(PathTemplate).order_by(PathTemplate.id).all()],
    }


@router.get("/health", response_model=List[CatalogIssueOut])
def get_health(admin_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Configuration problems as data. None of them stops a learner — the path
    generator degrades around each — but each is a promise the catalogue is not
    keeping, and a prerequisite cycle in particular deserves fixing today."""
    return admin.catalog_health(db)
