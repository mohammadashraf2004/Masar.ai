"""
app/models/learning_path.py

The personalised-learning domain: Level -> Field -> Career goal -> Learning path.

How this relates to what already exists
---------------------------------------
Nothing here replaces or alters `career_tracks`, `track_levels`, `topics`,
`tool_courses` or any progress table. Those keep holding the *content* and the
learner's *activity*. This module adds the layer that describes how that
content is *used*: which level a course suits, which fields and career goals it
serves, what it teaches and assumes, and how a learner's journey through it is
laid out.

`Course` is a thin catalogue facade over one existing content source — either
a `ToolCourse` or a `TrackLevel`. It never copies lessons, and it never
duplicates a course per language or per field: many-to-many tables carry the
relationships, and the `*_ar` twins follow the same Arabic-first convention as
every other content table (nullable, English is the fallback).

Vocabularies are rows, not enums, so a new field or career goal is data and
never a deploy. Selections stored on a learner (`LearningProfile.field_slugs`)
are slugs rather than foreign keys: slugs are the stable public identity, and
they survive a field being renamed, reordered or deactivated.

Status-like columns are plain strings guarded by CHECK constraints rather than
native Postgres enums. Adding a value to a native enum needs its own migration
and cannot run inside a transaction on older servers; a CHECK is one line.
"""
from sqlalchemy import (
    Boolean, CheckConstraint, Column, DateTime, Float, ForeignKey, Index,
    Integer, JSON, String, Text, UniqueConstraint, text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.session import Base

# ─── Vocabulary constants ───────────────────────────────────────────────────
# Structural values that code branches on. The *rows* they describe are data.

COURSE_KIND_TOOL = "tool_course"
COURSE_KIND_TRACK_LEVEL = "track_level"
COURSE_KINDS = (COURSE_KIND_TOOL, COURSE_KIND_TRACK_LEVEL)

SKILL_TEACHES = "teaches"   # completing the course grants the skill
SKILL_ASSUMES = "assumes"   # the course expects the skill beforehand

ROLE_FIELD_REQUIRED = "required"        # a foundation the goal cannot skip
ROLE_FIELD_RECOMMENDED = "recommended"  # a specialisation route the goal suits

# How much a course matters to one career goal (`course_roles.relation`). One
# course, many goals, a different weight in each. Descriptive only: the path
# generator, course states and progress never read it.
COURSE_ROLE_CORE = "core"
COURSE_ROLE_SUPPORTING = "supporting"
COURSE_ROLE_OPTIONAL = "optional"
COURSE_ROLE_RELATIONS = (COURSE_ROLE_CORE, COURSE_ROLE_SUPPORTING, COURSE_ROLE_OPTIONAL)

# Sections group a goal's workflow on screen (AI Engineer's apex path is the
# one goal that needs them today). `None` means "no section" - a simpler
# goal's workflow reads as one flat, ordered list.
TRACK_SECTIONS = (
    "foundations", "language-generative-ai", "application-production",
    "advanced-ai-systems", "specializations",
)

# A course prerequisite is `required` (the path generator orders the roadmap by it -
# what every prerequisite has always been) or `recommended` (advice only: read by
# readiness and recommendations, never by the path generator). Neither blocks a
# learner from enrolling.
PREREQ_REQUIRED = "required"
PREREQ_RECOMMENDED = "recommended"
PREREQ_KINDS = (PREREQ_REQUIRED, PREREQ_RECOMMENDED)

# Onboarding answers, ordered from least to most experienced.
PROGRAMMING_EXPERIENCE = ("none", "basic", "comfortable", "professional")
AI_EXPERIENCE = ("none", "basics", "projects", "applications")

PATH_ACTIVE = "active"
PATH_PAUSED = "paused"
PATH_ARCHIVED = "archived"
PATH_STATUSES = (PATH_ACTIVE, PATH_PAUSED, PATH_ARCHIVED)

# What a Skill *is*. A skill is a capability ("RAG"); a tool is a named product
# that helps deliver one ("LangChain"). Knowing a tool is not knowing the skill
# it is used for, so the two are kept apart and the UI can present them apart.
SKILL_KIND_SKILL = "skill"
SKILL_KIND_TOOL = "tool"
SKILL_KINDS = (SKILL_KIND_SKILL, SKILL_KIND_TOOL)

# A learner's relationship to a skill, and where that claim came from. `known`
# from `self_declared` is the learner saying so - it is not evidence. The other
# values exist so confidence can be *upgraded* later (practice, AI grading,
# an assessment) without a schema change: a row is never "verified" by a
# boolean, it carries the source of the claim.
LEARNER_SKILL_KNOWN = "known"
LEARNER_SKILL_LEARNING = "learning"
LEARNER_SKILL_MASTERED = "mastered"
LEARNER_SKILL_STATUSES = (LEARNER_SKILL_KNOWN, LEARNER_SKILL_LEARNING, LEARNER_SKILL_MASTERED)

LEARNER_SKILL_SELF_DECLARED = "self_declared"
LEARNER_SKILL_ASSESSMENT = "assessment"
LEARNER_SKILL_COURSE_COMPLETION = "course_completion"
LEARNER_SKILL_SOURCES = (
    LEARNER_SKILL_SELF_DECLARED, LEARNER_SKILL_ASSESSMENT, LEARNER_SKILL_COURSE_COMPLETION,
)

PROFILE_SOURCE_ONBOARDING = "onboarding"
PROFILE_SOURCE_MIGRATED = "migrated"


def _in(column: str, values) -> str:
    return f"{column} IN ({', '.join(repr(v) for v in values)})"


# ─── Levels ─────────────────────────────────────────────────────────────────

class LearningLevel(Base):
    """Beginner / Intermediate / Advanced. `rank` is what code compares —
    never the slug — so a new level slots in without touching any rule."""
    __tablename__ = "learning_levels"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    name_ar = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    description_ar = Column(Text, nullable=True)
    rank = Column(Integer, nullable=False, unique=True)
    is_active = Column(Boolean, nullable=False, default=True, server_default=text("true"))


# ─── Fields ─────────────────────────────────────────────────────────────────

class LearningField(Base):
    """A specialisation: Data, ML, NLP, Computer Vision, Speech, Multimodal.

    Prerequisites are a threshold rule over a set of fields, not a fixed
    chain: the learner should have at least `prerequisite_min_required` of
    `prerequisites`, and ideally `prerequisite_recommended`. Multimodal lists
    NLP, Computer Vision and Speech with min 1 / recommended 2 — "any one
    modality, ideally two" — and a stricter or looser rule is a data change.
    """
    __tablename__ = "learning_fields"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    name_ar = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    description_ar = Column(Text, nullable=True)
    # A key the frontend resolves to an icon; the backend never sees a component.
    icon = Column(String, nullable=True)
    # The lowest level this field is offered at without a prerequisite route.
    # NULL means every level. Below it the API advises rather than blocks.
    min_level_id = Column(Integer, ForeignKey("learning_levels.id"), nullable=True)
    prerequisite_min_required = Column(Integer, nullable=False, default=1, server_default=text("1"))
    prerequisite_recommended = Column(Integer, nullable=False, default=1, server_default=text("1"))
    position = Column(Integer, nullable=False, default=0, server_default=text("0"))
    is_active = Column(Boolean, nullable=False, default=True, server_default=text("true"))

    min_level = relationship("LearningLevel")
    # Read-only convenience; writes go through LearningFieldPrerequisite so the
    # association rows have exactly one owner.
    prerequisites = relationship(
        "LearningField",
        secondary="learning_field_prerequisites",
        primaryjoin="LearningField.id == LearningFieldPrerequisite.field_id",
        secondaryjoin="LearningField.id == LearningFieldPrerequisite.prerequisite_field_id",
        order_by="LearningField.position",
        viewonly=True,
    )


class LearningFieldPrerequisite(Base):
    __tablename__ = "learning_field_prerequisites"
    __table_args__ = (
        CheckConstraint("field_id <> prerequisite_field_id", name="ck_field_prereq_not_self"),
    )

    field_id = Column(Integer, ForeignKey("learning_fields.id", ondelete="CASCADE"), primary_key=True)
    prerequisite_field_id = Column(Integer, ForeignKey("learning_fields.id", ondelete="CASCADE"), primary_key=True)


# ─── Skills ─────────────────────────────────────────────────────────────────

class Skill(Base):
    """A named capability courses teach and career goals require. This is the
    catalogue vocabulary; it is deliberately separate from the free-text
    `industry_skills` labels on tool courses (what a recruiter searches for)
    and from `UserSkillScore` (a measured score for one learner)."""
    __tablename__ = "skills"
    __table_args__ = (
        CheckConstraint(_in("kind", SKILL_KINDS), name="ck_skills_kind"),
    )

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    name_ar = Column(String, nullable=True)
    # 'skill' (a capability) or 'tool' (a product used to apply one).
    kind = Column(String, nullable=False, default=SKILL_KIND_SKILL, server_default=SKILL_KIND_SKILL)


# ─── Career goals ───────────────────────────────────────────────────────────

class CareerRole(Base):
    """A career goal. The five slugs match the five legacy `career_tracks`
    rows one-to-one, which is what lets an old enrolment map onto a goal —
    but a goal is *not* a track and owns no lessons. There is deliberately no
    foreign key to `career_tracks`: the two are related by slug, and the goal
    must keep working if a legacy track is ever retired."""
    __tablename__ = "career_roles"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    title_ar = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    description_ar = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
    recommended_level_id = Column(Integer, ForeignKey("learning_levels.id"), nullable=True)
    position = Column(Integer, nullable=False, default=0, server_default=text("0"))
    is_active = Column(Boolean, nullable=False, default=True, server_default=text("true"))

    recommended_level = relationship("LearningLevel")
    field_links = relationship("CareerRoleField", cascade="all, delete-orphan")
    skill_links = relationship("CareerRoleSkill", cascade="all, delete-orphan")


class CareerRoleField(Base):
    __tablename__ = "career_role_fields"
    __table_args__ = (
        CheckConstraint(_in("relation", (ROLE_FIELD_REQUIRED, ROLE_FIELD_RECOMMENDED)),
                        name="ck_career_role_fields_relation"),
    )

    role_id = Column(Integer, ForeignKey("career_roles.id", ondelete="CASCADE"), primary_key=True)
    field_id = Column(Integer, ForeignKey("learning_fields.id", ondelete="CASCADE"), primary_key=True)
    relation = Column(String, nullable=False, default=ROLE_FIELD_RECOMMENDED)

    field = relationship("LearningField")


class CareerRoleSkill(Base):
    __tablename__ = "career_role_skills"

    role_id = Column(Integer, ForeignKey("career_roles.id", ondelete="CASCADE"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True)
    is_required = Column(Boolean, nullable=False, default=True, server_default=text("true"))

    skill = relationship("Skill")


# ─── Courses ────────────────────────────────────────────────────────────────

class Course(Base):
    """The catalogue entry for one learnable unit.

    Points at exactly one existing content source (see the CHECK below). The
    title/description columns are *optional overrides*: left NULL they fall
    back to the source, so a catalogue title only exists where the source's
    own ("Level 3: RAG & Knowledge Systems") is not what a learner should see.
    """
    __tablename__ = "courses"
    __table_args__ = (
        CheckConstraint(
            "(kind = 'tool_course' AND tool_course_id IS NOT NULL AND track_level_id IS NULL) OR "
            "(kind = 'track_level' AND track_level_id IS NOT NULL AND tool_course_id IS NULL)",
            name="ck_courses_exactly_one_source",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    kind = Column(String, nullable=False)
    tool_course_id = Column(Integer, ForeignKey("tool_courses.id"), unique=True, nullable=True)
    track_level_id = Column(Integer, ForeignKey("track_levels.id"), unique=True, nullable=True)

    title = Column(String, nullable=True)
    title_ar = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    description_ar = Column(Text, nullable=True)
    level_id = Column(Integer, ForeignKey("learning_levels.id"), nullable=False)
    # NULL = derive from the source's topics.
    estimated_hours = Column(Float, nullable=True)
    learning_objectives = Column(JSON, nullable=True)
    learning_objectives_ar = Column(JSON, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, server_default=text("true"))
    # Free accounts receive two ordered lesson previews; full-course access
    # comes from Pro or a preserved course entitlement.
    is_free = Column(Boolean, nullable=False, default=False, server_default=text("false"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    level = relationship("LearningLevel")
    tool_course = relationship("ToolCourse")
    track_level = relationship("TrackLevel")
    field_links = relationship("CourseField", cascade="all, delete-orphan")
    role_links = relationship("CourseRole", cascade="all, delete-orphan")
    skill_links = relationship("CourseSkill", cascade="all, delete-orphan")
    prerequisite_links = relationship(
        "CoursePrerequisite", cascade="all, delete-orphan",
        foreign_keys="CoursePrerequisite.course_id",
    )


class CourseField(Base):
    __tablename__ = "course_fields"

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    field_id = Column(Integer, ForeignKey("learning_fields.id", ondelete="CASCADE"), primary_key=True, index=True)

    field = relationship("LearningField")


class CourseRole(Base):
    """A course serves a career goal, with a weight: `core`, `supporting` or
    `optional`. The row is the only place the weight lives, so a course is never
    copied per goal - it is one entity with a different relation in each.

    `position`, `required` and `section` are this same row's answer to "where
    does this course sit in this goal's workflow": an explicit, server-owned
    order (never the course's own primary key, never alphabetical), whether it
    gates that goal's required-completion math, and - for a goal whose
    workflow reads as sections (AI Engineer) - which one. A goal with no
    sections leaves every row's `section` NULL."""
    __tablename__ = "course_roles"
    __table_args__ = (
        CheckConstraint(_in("relation", COURSE_ROLE_RELATIONS), name="ck_course_roles_relation"),
        CheckConstraint(
            "section IS NULL OR " + _in("section", TRACK_SECTIONS), name="ck_course_roles_section"),
    )

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(Integer, ForeignKey("career_roles.id", ondelete="CASCADE"), primary_key=True, index=True)
    relation = Column(String, nullable=False, default=COURSE_ROLE_CORE, server_default=COURSE_ROLE_CORE)
    # This course's ordinal position in this goal's workflow; the API sorts by
    # this column, never by course id. Zero means the relation is catalogue
    # metadata only and is not part of a fixed track workflow.
    position = Column(Integer, nullable=False, default=0, server_default=text("0"))
    # Whether this course gates the goal's required-completion percentage.
    # Optional courses (role='optional' or required=false) never lower it and
    # never block progression to a later required course.
    required = Column(Boolean, nullable=False, default=True, server_default=text("true"))
    section = Column(String, nullable=True)

    role = relationship("CareerRole")


class CourseSkill(Base):
    __tablename__ = "course_skills"
    __table_args__ = (
        CheckConstraint(_in("relation", (SKILL_TEACHES, SKILL_ASSUMES)), name="ck_course_skills_relation"),
    )

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), primary_key=True, index=True)
    relation = Column(String, primary_key=True, default=SKILL_TEACHES)

    skill = relationship("Skill")


class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisites"
    __table_args__ = (
        CheckConstraint("course_id <> prerequisite_course_id", name="ck_course_prereq_not_self"),
        CheckConstraint(_in("kind", PREREQ_KINDS), name="ck_course_prerequisites_kind"),
    )

    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    prerequisite_course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True)
    kind = Column(String, nullable=False, default=PREREQ_REQUIRED, server_default=PREREQ_REQUIRED)


# ─── Path configuration ─────────────────────────────────────────────────────

class PathStage(Base):
    """A reusable chapter of a journey — Foundations, Deep Learning, RAG
    Engineering. Which courses it holds is data (`path_stage_courses`); which
    journeys include it, and for which fields, is the template's business."""
    __tablename__ = "path_stages"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    title_ar = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    description_ar = Column(Text, nullable=True)
    # foundations | specialization | engineering | multimodal | career — used to
    # group stages on screen; nothing in the generator branches on it.
    phase = Column(String, nullable=False, default="specialization", server_default="specialization")
    # 'learning' stages hold courses; 'capstone' marks the culminating project.
    kind = Column(String, nullable=False, default="learning", server_default="learning")
    is_active = Column(Boolean, nullable=False, default=True, server_default=text("true"))

    course_links = relationship(
        "PathStageCourse", cascade="all, delete-orphan", order_by="PathStageCourse.position",
    )


class PathStageCourse(Base):
    __tablename__ = "path_stage_courses"

    stage_id = Column(Integer, ForeignKey("path_stages.id", ondelete="CASCADE"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), primary_key=True, index=True)
    position = Column(Integer, nullable=False, default=0, server_default=text("0"))

    course = relationship("Course")


class PathTemplate(Base):
    """The journey shape for one career goal: an ordered list of stages, some
    of which apply only when a given field is part of the learner's route.
    `career_role_id` NULL is the fallback template for a goal that has none of
    its own. This is the "path configuration" — routes such as
    *AI Engineer — Computer Vision* are this template filtered to one field,
    never a hard-coded list in a component."""
    __tablename__ = "path_templates"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True, nullable=False)
    career_role_id = Column(Integer, ForeignKey("career_roles.id"), unique=True, nullable=True)
    title = Column(String, nullable=False)
    title_ar = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    description_ar = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True, server_default=text("true"))

    role = relationship("CareerRole")
    stage_links = relationship(
        "PathTemplateStage", cascade="all, delete-orphan", order_by="PathTemplateStage.position",
    )


class PathTemplateStage(Base):
    __tablename__ = "path_template_stages"
    __table_args__ = (
        UniqueConstraint("template_id", "stage_id", name="uq_path_template_stage"),
    )

    id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey("path_templates.id", ondelete="CASCADE"), nullable=False, index=True)
    stage_id = Column(Integer, ForeignKey("path_stages.id", ondelete="CASCADE"), nullable=False)
    position = Column(Integer, nullable=False, default=0, server_default=text("0"))
    # NULL = part of every route; set = only when this field is in the route.
    field_id = Column(Integer, ForeignKey("learning_fields.id"), nullable=True)

    stage = relationship("PathStage")
    field = relationship("LearningField")


# ─── The learner ────────────────────────────────────────────────────────────

class LearningProfile(Base):
    """What a learner told us: where they are, what interests them, where they
    want to go. Every column is nullable because a profile can be partial — a
    migrated enrolment knows a career goal and nothing else, and nothing here
    may be guessed to fill the gap. `onboarding_completed_at` is the single
    switch for "ask them to finish the new onboarding"."""
    __tablename__ = "learning_profiles"
    __table_args__ = (
        CheckConstraint(
            "programming_experience IS NULL OR " + _in("programming_experience", PROGRAMMING_EXPERIENCE),
            name="ck_learning_profiles_programming_experience"),
        CheckConstraint(
            "ai_experience IS NULL OR " + _in("ai_experience", AI_EXPERIENCE),
            name="ck_learning_profiles_ai_experience"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    level_id = Column(Integer, ForeignKey("learning_levels.id"), nullable=True)
    career_role_id = Column(Integer, ForeignKey("career_roles.id"), nullable=True)
    field_slugs = Column(JSON, nullable=False, default=list)
    # The two onboarding questions. Self-reported starting points, never evidence:
    # readiness may use them as a weak prior and never as proof.
    programming_experience = Column(String, nullable=True)
    ai_experience = Column(String, nullable=True)
    # DEPRECATED - no longer read or written. Migration 013 copied these into
    # `learner_skills`, which is the source of truth (it records status and
    # source per skill). The column stays so the migration is reversible and no
    # data is destroyed; a later release can drop it.
    known_skill_slugs = Column(JSON, nullable=False, default=list)
    onboarding_completed_at = Column(DateTime(timezone=True), nullable=True)
    source = Column(String, nullable=False, default=PROFILE_SOURCE_ONBOARDING)
    # What a migrated profile was derived from, so the derivation is auditable.
    migrated_from = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User")
    level = relationship("LearningLevel")
    career_role = relationship("CareerRole")


class LearnerSkill(Base):
    """One learner's relationship to one skill.

    Onboarding writes `status='known', source='self_declared'`: the learner said
    so. That is deliberately weaker than "mastered" and is never presented as a
    qualification. Later evidence (practice, AI-graded work, an assessment,
    finishing a course) can raise the *source* and *status* of the same row -
    `self_declared -> assessment`, `known -> mastered` - without a new table.

    Only `known` and `mastered` rows count as knowing the skill when a path is
    built; `learning` is recorded for display and does not waive anything.
    """
    __tablename__ = "learner_skills"
    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_learner_skills_user_skill"),
        CheckConstraint(_in("status", LEARNER_SKILL_STATUSES), name="ck_learner_skills_status"),
        CheckConstraint(_in("source", LEARNER_SKILL_SOURCES), name="ck_learner_skills_source"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False, default=LEARNER_SKILL_KNOWN, server_default=LEARNER_SKILL_KNOWN)
    source = Column(String, nullable=False, default=LEARNER_SKILL_SELF_DECLARED,
                    server_default=LEARNER_SKILL_SELF_DECLARED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    skill = relationship("Skill")


class LearningPath(Base):
    """A learner's journey, saved. `stages` is a snapshot of *membership and
    order only* — stage slugs, course ids, required/optional/waived flags.
    Titles, translations and progress are resolved live from the catalogue and
    from the learner's activity, so a renamed course or a newly finished
    lesson never leaves a stale copy behind. Regenerating archives the old
    row instead of overwriting it."""
    __tablename__ = "learning_paths"
    __table_args__ = (
        CheckConstraint(_in("status", PATH_STATUSES), name="ck_learning_paths_status"),
        # One live path per learner. Partial, so any number of archived rows
        # can accumulate (same pattern as uq_exam_attempts_one_in_progress).
        Index("uq_learning_paths_one_active", "user_id", unique=True,
              postgresql_where=text("status = 'active'")),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    level_id = Column(Integer, ForeignKey("learning_levels.id"), nullable=False)
    career_role_id = Column(Integer, ForeignKey("career_roles.id"), nullable=False)
    field_slugs = Column(JSON, nullable=False, default=list)
    status = Column(String, nullable=False, default=PATH_ACTIVE, server_default=PATH_ACTIVE)
    template_slug = Column(String, nullable=True)
    stages = Column(JSON, nullable=False, default=list)
    advisories = Column(JSON, nullable=False, default=list)
    waived_course_ids = Column(JSON, nullable=False, default=list)
    estimated_hours = Column(Float, nullable=False, default=0.0)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    level = relationship("LearningLevel")
    career_role = relationship("CareerRole")


class ReadinessAssessment(Base):
    """One short readiness check a learner took before a course.

    The questions are drawn server-side from the quizzes of the course's
    prerequisite courses (real curriculum questions, never generated), and the
    score is computed here from the stored `answers` - the client never sends
    a score. `skill_results` is `{skill slug: fraction correct}` and is the only
    thing readiness reads back."""
    __tablename__ = "readiness_assessments"
    __table_args__ = (
        Index("ix_readiness_assessments_user_course", "user_id", "course_id", "created_at"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)
    question_count = Column(Integer, nullable=False)
    correct_count = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)                     # 0-100
    skill_results = Column(JSON, nullable=False, default=dict)
    answers = Column(JSON, nullable=False, default=dict)      # {"<quiz id>:<index>": selected option}
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    course = relationship("Course")
