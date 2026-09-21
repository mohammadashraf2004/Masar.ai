"""learning levels, fields, career goals, catalogue courses and learning paths

Adds the layer that turns "which role track am I on" into "where am I, what
interests me, where do I want to go":

    Level -> Field(s) -> Career goal -> Learning path

Purely additive. No existing table is altered, and no existing row is touched:
`career_tracks`, `track_levels`, `topics`, `tool_courses`, `enrollments` and
every progress table stay exactly as they are, so enrolments, quizzes, coding
exercises, projects, exams and certificates keep working unchanged.

`courses` is a catalogue *facade* over one existing content source (a
`tool_courses` row or a `track_levels` row, enforced by a CHECK) — it holds
the relationships (level, fields, career goals, skills, prerequisites) and
none of the content, so nothing is duplicated per language or per field.

Reference vocabulary
--------------------
This migration also inserts three small controlled vocabularies: the three
levels, the six fields and the five career goals. They are structural rather
than content: onboarding cannot render without them, and migration 012 needs
the career-goal ids to map legacy enrolments onto goals. Only names, short
descriptions and ordering are inserted here — the *relationships* between
them (prerequisites, skills, courses, stages) are configuration, and belong to
`seeds/seed_learning_paths.py`, which never overwrites a row it did not
create. The values below are a frozen snapshot on purpose: a migration must
not change meaning when the seed later evolves.

Revision ID: 011_learning_paths
Revises: 010_exam_attempt_start_race
Create Date: 2026-09-19

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '011_learning_paths'
down_revision: Union[str, None] = '010_exam_attempt_start_race'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


_TRUE = sa.text('true')
_ZERO = sa.text('0')


def _pk_id():
    return sa.Column('id', sa.Integer(), nullable=False)


def upgrade() -> None:
    # ── Vocabularies ──────────────────────────────────────────────────────
    op.create_table(
        'learning_levels',
        _pk_id(),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('name_ar', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('description_ar', sa.Text(), nullable=True),
        sa.Column('rank', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=_TRUE),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('rank', name='uq_learning_levels_rank'),
    )
    op.create_index('ix_learning_levels_id', 'learning_levels', ['id'])
    op.create_index('ix_learning_levels_slug', 'learning_levels', ['slug'], unique=True)

    op.create_table(
        'learning_fields',
        _pk_id(),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('name_ar', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('description_ar', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(), nullable=True),
        sa.Column('min_level_id', sa.Integer(), nullable=True),
        sa.Column('prerequisite_min_required', sa.Integer(), nullable=False, server_default=sa.text('1')),
        sa.Column('prerequisite_recommended', sa.Integer(), nullable=False, server_default=sa.text('1')),
        sa.Column('position', sa.Integer(), nullable=False, server_default=_ZERO),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=_TRUE),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['min_level_id'], ['learning_levels.id'],
                                name='fk_learning_fields_min_level_id_learning_levels'),
    )
    op.create_index('ix_learning_fields_id', 'learning_fields', ['id'])
    op.create_index('ix_learning_fields_slug', 'learning_fields', ['slug'], unique=True)

    op.create_table(
        'learning_field_prerequisites',
        sa.Column('field_id', sa.Integer(), nullable=False),
        sa.Column('prerequisite_field_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('field_id', 'prerequisite_field_id'),
        sa.ForeignKeyConstraint(['field_id'], ['learning_fields.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['prerequisite_field_id'], ['learning_fields.id'], ondelete='CASCADE'),
        sa.CheckConstraint('field_id <> prerequisite_field_id', name='ck_field_prereq_not_self'),
    )

    op.create_table(
        'skills',
        _pk_id(),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('name_ar', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_skills_id', 'skills', ['id'])
    op.create_index('ix_skills_slug', 'skills', ['slug'], unique=True)

    op.create_table(
        'career_roles',
        _pk_id(),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('title_ar', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('description_ar', sa.Text(), nullable=True),
        sa.Column('icon', sa.String(), nullable=True),
        sa.Column('recommended_level_id', sa.Integer(), nullable=True),
        sa.Column('position', sa.Integer(), nullable=False, server_default=_ZERO),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=_TRUE),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['recommended_level_id'], ['learning_levels.id'],
                                name='fk_career_roles_recommended_level_id_learning_levels'),
    )
    op.create_index('ix_career_roles_id', 'career_roles', ['id'])
    op.create_index('ix_career_roles_slug', 'career_roles', ['slug'], unique=True)

    op.create_table(
        'career_role_fields',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('field_id', sa.Integer(), nullable=False),
        sa.Column('relation', sa.String(), nullable=False, server_default='recommended'),
        sa.PrimaryKeyConstraint('role_id', 'field_id'),
        sa.ForeignKeyConstraint(['role_id'], ['career_roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['field_id'], ['learning_fields.id'], ondelete='CASCADE'),
        sa.CheckConstraint("relation IN ('required', 'recommended')", name='ck_career_role_fields_relation'),
    )

    op.create_table(
        'career_role_skills',
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('is_required', sa.Boolean(), nullable=False, server_default=_TRUE),
        sa.PrimaryKeyConstraint('role_id', 'skill_id'),
        sa.ForeignKeyConstraint(['role_id'], ['career_roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
    )

    # ── Courses ───────────────────────────────────────────────────────────
    op.create_table(
        'courses',
        _pk_id(),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('kind', sa.String(), nullable=False),
        sa.Column('tool_course_id', sa.Integer(), nullable=True),
        sa.Column('track_level_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('title_ar', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('description_ar', sa.Text(), nullable=True),
        sa.Column('level_id', sa.Integer(), nullable=False),
        sa.Column('estimated_hours', sa.Float(), nullable=True),
        sa.Column('learning_objectives', sa.JSON(), nullable=True),
        sa.Column('learning_objectives_ar', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=_TRUE),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['tool_course_id'], ['tool_courses.id'], name='fk_courses_tool_course_id_tool_courses'),
        sa.ForeignKeyConstraint(['track_level_id'], ['track_levels.id'], name='fk_courses_track_level_id_track_levels'),
        sa.ForeignKeyConstraint(['level_id'], ['learning_levels.id'], name='fk_courses_level_id_learning_levels'),
        sa.UniqueConstraint('tool_course_id', name='uq_courses_tool_course_id'),
        sa.UniqueConstraint('track_level_id', name='uq_courses_track_level_id'),
        sa.CheckConstraint(
            "(kind = 'tool_course' AND tool_course_id IS NOT NULL AND track_level_id IS NULL) OR "
            "(kind = 'track_level' AND track_level_id IS NOT NULL AND tool_course_id IS NULL)",
            name='ck_courses_exactly_one_source',
        ),
    )
    op.create_index('ix_courses_id', 'courses', ['id'])
    op.create_index('ix_courses_slug', 'courses', ['slug'], unique=True)

    op.create_table(
        'course_fields',
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('field_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('course_id', 'field_id'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['field_id'], ['learning_fields.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_course_fields_field_id', 'course_fields', ['field_id'])

    op.create_table(
        'course_roles',
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('course_id', 'role_id'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['role_id'], ['career_roles.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_course_roles_role_id', 'course_roles', ['role_id'])

    op.create_table(
        'course_skills',
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('skill_id', sa.Integer(), nullable=False),
        sa.Column('relation', sa.String(), nullable=False, server_default='teaches'),
        sa.PrimaryKeyConstraint('course_id', 'skill_id', 'relation'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['skill_id'], ['skills.id'], ondelete='CASCADE'),
        sa.CheckConstraint("relation IN ('teaches', 'assumes')", name='ck_course_skills_relation'),
    )
    op.create_index('ix_course_skills_skill_id', 'course_skills', ['skill_id'])

    op.create_table(
        'course_prerequisites',
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('prerequisite_course_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('course_id', 'prerequisite_course_id'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['prerequisite_course_id'], ['courses.id'], ondelete='CASCADE'),
        sa.CheckConstraint('course_id <> prerequisite_course_id', name='ck_course_prereq_not_self'),
    )

    # ── Path configuration ────────────────────────────────────────────────
    op.create_table(
        'path_stages',
        _pk_id(),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('title_ar', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('description_ar', sa.Text(), nullable=True),
        sa.Column('phase', sa.String(), nullable=False, server_default='specialization'),
        sa.Column('kind', sa.String(), nullable=False, server_default='learning'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=_TRUE),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_path_stages_id', 'path_stages', ['id'])
    op.create_index('ix_path_stages_slug', 'path_stages', ['slug'], unique=True)

    op.create_table(
        'path_stage_courses',
        sa.Column('stage_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.Integer(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False, server_default=_ZERO),
        sa.PrimaryKeyConstraint('stage_id', 'course_id'),
        sa.ForeignKeyConstraint(['stage_id'], ['path_stages.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_path_stage_courses_course_id', 'path_stage_courses', ['course_id'])

    op.create_table(
        'path_templates',
        _pk_id(),
        sa.Column('slug', sa.String(), nullable=False),
        sa.Column('career_role_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('title_ar', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('description_ar', sa.Text(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=_TRUE),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['career_role_id'], ['career_roles.id'],
                                name='fk_path_templates_career_role_id_career_roles'),
        sa.UniqueConstraint('career_role_id', name='uq_path_templates_career_role_id'),
    )
    op.create_index('ix_path_templates_id', 'path_templates', ['id'])
    op.create_index('ix_path_templates_slug', 'path_templates', ['slug'], unique=True)

    op.create_table(
        'path_template_stages',
        _pk_id(),
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.Column('stage_id', sa.Integer(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False, server_default=_ZERO),
        sa.Column('field_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['template_id'], ['path_templates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['stage_id'], ['path_stages.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['field_id'], ['learning_fields.id'],
                                name='fk_path_template_stages_field_id_learning_fields'),
        sa.UniqueConstraint('template_id', 'stage_id', name='uq_path_template_stage'),
    )
    op.create_index('ix_path_template_stages_template_id', 'path_template_stages', ['template_id'])

    # ── The learner ───────────────────────────────────────────────────────
    op.create_table(
        'learning_profiles',
        _pk_id(),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('level_id', sa.Integer(), nullable=True),
        sa.Column('career_role_id', sa.Integer(), nullable=True),
        sa.Column('field_slugs', sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column('known_skill_slugs', sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column('onboarding_completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('source', sa.String(), nullable=False, server_default='onboarding'),
        sa.Column('migrated_from', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE',
                                name='fk_learning_profiles_user_id_users'),
        sa.ForeignKeyConstraint(['level_id'], ['learning_levels.id'],
                                name='fk_learning_profiles_level_id_learning_levels'),
        sa.ForeignKeyConstraint(['career_role_id'], ['career_roles.id'],
                                name='fk_learning_profiles_career_role_id_career_roles'),
        sa.UniqueConstraint('user_id', name='uq_learning_profiles_user_id'),
    )
    op.create_index('ix_learning_profiles_id', 'learning_profiles', ['id'])

    op.create_table(
        'learning_paths',
        _pk_id(),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('level_id', sa.Integer(), nullable=False),
        sa.Column('career_role_id', sa.Integer(), nullable=False),
        sa.Column('field_slugs', sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column('status', sa.String(), nullable=False, server_default='active'),
        sa.Column('template_slug', sa.String(), nullable=True),
        sa.Column('stages', sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column('advisories', sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column('waived_course_ids', sa.JSON(), nullable=False, server_default=sa.text("'[]'::json")),
        sa.Column('estimated_hours', sa.Float(), nullable=False, server_default=sa.text('0')),
        sa.Column('generated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE',
                                name='fk_learning_paths_user_id_users'),
        sa.ForeignKeyConstraint(['level_id'], ['learning_levels.id'],
                                name='fk_learning_paths_level_id_learning_levels'),
        sa.ForeignKeyConstraint(['career_role_id'], ['career_roles.id'],
                                name='fk_learning_paths_career_role_id_career_roles'),
        sa.CheckConstraint("status IN ('active', 'paused', 'archived')", name='ck_learning_paths_status'),
    )
    op.create_index('ix_learning_paths_id', 'learning_paths', ['id'])
    op.create_index('ix_learning_paths_user_id', 'learning_paths', ['user_id'])
    # One live path per learner; archived rows may pile up freely.
    op.create_index(
        'uq_learning_paths_one_active', 'learning_paths', ['user_id'],
        unique=True, postgresql_where=sa.text("status = 'active'"),
    )

    _seed_vocabulary()


# ─── Frozen reference vocabulary ─────────────────────────────────────────────
# (slug, name, name_ar, description, description_ar, rank)
_LEVELS = [
    ('beginner', 'Beginner', 'مبتدئ',
     'New to programming or AI, and you want to start from the basics.',
     'جديد على البرمجة أو الـ AI، وتريد أن تبدأ من الأساسيات.', 1),
    ('intermediate', 'Intermediate', 'متوسط',
     'You write Python and know the basics of machine learning or AI.',
     'تكتب Python وتعرف أساسيات الـ Machine Learning أو الـ AI.', 2),
    ('advanced', 'Advanced', 'متقدم',
     'You have built real ML or AI projects and want depth and specialization.',
     'بنيت مشاريع ML أو AI حقيقية وتريد التعمق والتخصص.', 3),
]

# (slug, name, name_ar, description, description_ar, icon, min_level_slug, position)
_FIELDS = [
    ('data', 'Data & Analytics', 'تحليل البيانات',
     'Wrangle, analyze and visualize data to answer real business questions.',
     'معالجة البيانات وتحليلها وعرضها للإجابة عن أسئلة العمل الحقيقية.',
     'bar-chart', None, 1),
    ('machine-learning', 'Machine Learning', 'تعلّم الآلة',
     'Train, evaluate and improve models, from classical ML to deep learning.',
     'تدريب النماذج وتقييمها وتحسينها، من الـ ML الكلاسيكي إلى الـ Deep Learning.',
     'brain', None, 2),
    ('nlp', 'NLP & LLMs', 'معالجة اللغة الطبيعية والـ LLMs',
     'Build with language: LLMs, prompting, retrieval, RAG and agents.',
     'البناء فوق اللغة: الـ LLMs والـ Prompting والـ Retrieval والـ RAG والـ Agents.',
     'message-square', None, 3),
    ('computer-vision', 'Computer Vision', 'الرؤية الحاسوبية',
     'Teach systems to understand images and video.',
     'تعليم الأنظمة فهم الصور والفيديو.',
     'eye', None, 4),
    ('speech', 'Speech & Voice AI', 'الصوت والكلام',
     'Recognize speech, generate voices and build voice conversations.',
     'التعرّف على الكلام وتوليد الأصوات وبناء محادثات صوتية.',
     'mic', None, 5),
    ('multimodal', 'Multimodal AI', 'الذكاء الاصطناعي متعدد الوسائط',
     'Combine text, vision and audio in one system. An advanced path that builds on at least one modality.',
     'دمج النص والصورة والصوت في نظام واحد. مسار متقدم يبني على وسيلة واحدة على الأقل.',
     'layers', 'advanced', 6),
]

# (slug, title, title_ar, description, description_ar, icon, recommended_level_slug, position)
_ROLES = [
    ('data-analyst', 'Data Analyst', 'محلل بيانات',
     'Turn raw data into insight, dashboards and decisions.',
     'تحويل البيانات الخام إلى رؤى ولوحات معلومات وقرارات.',
     'bar-chart', 'beginner', 1),
    ('ml-engineer', 'ML Engineer', 'مهندس تعلّم آلة',
     'Build, train and evaluate machine learning models.',
     'بناء نماذج الـ Machine Learning وتدريبها وتقييمها.',
     'brain', 'intermediate', 2),
    ('ai-developer', 'AI Developer', 'مطوّر تطبيقات ذكاء اصطناعي',
     'Ship products on top of LLMs and AI APIs.',
     'بناء منتجات فوق الـ LLMs وواجهات الـ AI.',
     'code', 'intermediate', 3),
    ('mlops-engineer', 'MLOps Engineer', 'مهندس MLOps',
     'Deploy, monitor and operate ML systems reliably.',
     'نشر أنظمة الـ ML ومراقبتها وتشغيلها بموثوقية.',
     'server', 'intermediate', 4),
    ('ai-engineer', 'AI Engineer', 'مهندس ذكاء اصطناعي',
     'Design and ship complete AI systems end to end, in the specialization you choose: '
     'NLP, Computer Vision, Speech or Multimodal.',
     'تصميم أنظمة الذكاء الاصطناعي المتكاملة وإطلاقها من البداية للنهاية، في التخصص الذي تختاره: '
     'NLP أو الرؤية الحاسوبية أو الصوت أو الوسائط المتعددة.',
     'layers', 'intermediate', 5),
]


def _seed_vocabulary() -> None:
    bind = op.get_bind()
    levels = sa.table(
        'learning_levels',
        sa.column('slug'), sa.column('name'), sa.column('name_ar'),
        sa.column('description'), sa.column('description_ar'), sa.column('rank'),
    )
    op.bulk_insert(levels, [
        dict(slug=s, name=n, name_ar=na, description=d, description_ar=da, rank=r)
        for s, n, na, d, da, r in _LEVELS
    ])
    level_id = {
        row.slug: row.id
        for row in bind.execute(sa.text('SELECT id, slug FROM learning_levels'))
    }

    fields = sa.table(
        'learning_fields',
        sa.column('slug'), sa.column('name'), sa.column('name_ar'),
        sa.column('description'), sa.column('description_ar'), sa.column('icon'),
        sa.column('min_level_id'), sa.column('position'),
    )
    op.bulk_insert(fields, [
        dict(slug=s, name=n, name_ar=na, description=d, description_ar=da, icon=i,
             min_level_id=level_id[ml] if ml else None, position=p)
        for s, n, na, d, da, i, ml, p in _FIELDS
    ])

    roles = sa.table(
        'career_roles',
        sa.column('slug'), sa.column('title'), sa.column('title_ar'),
        sa.column('description'), sa.column('description_ar'), sa.column('icon'),
        sa.column('recommended_level_id'), sa.column('position'),
    )
    op.bulk_insert(roles, [
        dict(slug=s, title=t, title_ar=ta, description=d, description_ar=da, icon=i,
             recommended_level_id=level_id[rl], position=p)
        for s, t, ta, d, da, i, rl, p in _ROLES
    ])


def downgrade() -> None:
    # Reverse dependency order. Dropping the tables removes the vocabulary
    # rows with them; nothing outside this migration referenced them.
    op.drop_index('uq_learning_paths_one_active', table_name='learning_paths')
    op.drop_index('ix_learning_paths_user_id', table_name='learning_paths')
    op.drop_index('ix_learning_paths_id', table_name='learning_paths')
    op.drop_table('learning_paths')

    op.drop_index('ix_learning_profiles_id', table_name='learning_profiles')
    op.drop_table('learning_profiles')

    op.drop_index('ix_path_template_stages_template_id', table_name='path_template_stages')
    op.drop_table('path_template_stages')
    op.drop_index('ix_path_templates_slug', table_name='path_templates')
    op.drop_index('ix_path_templates_id', table_name='path_templates')
    op.drop_table('path_templates')
    op.drop_index('ix_path_stage_courses_course_id', table_name='path_stage_courses')
    op.drop_table('path_stage_courses')
    op.drop_index('ix_path_stages_slug', table_name='path_stages')
    op.drop_index('ix_path_stages_id', table_name='path_stages')
    op.drop_table('path_stages')

    op.drop_table('course_prerequisites')
    op.drop_index('ix_course_skills_skill_id', table_name='course_skills')
    op.drop_table('course_skills')
    op.drop_index('ix_course_roles_role_id', table_name='course_roles')
    op.drop_table('course_roles')
    op.drop_index('ix_course_fields_field_id', table_name='course_fields')
    op.drop_table('course_fields')
    op.drop_index('ix_courses_slug', table_name='courses')
    op.drop_index('ix_courses_id', table_name='courses')
    op.drop_table('courses')

    op.drop_table('career_role_skills')
    op.drop_table('career_role_fields')
    op.drop_index('ix_career_roles_slug', table_name='career_roles')
    op.drop_index('ix_career_roles_id', table_name='career_roles')
    op.drop_table('career_roles')
    op.drop_index('ix_skills_slug', table_name='skills')
    op.drop_index('ix_skills_id', table_name='skills')
    op.drop_table('skills')
    op.drop_table('learning_field_prerequisites')
    op.drop_index('ix_learning_fields_slug', table_name='learning_fields')
    op.drop_index('ix_learning_fields_id', table_name='learning_fields')
    op.drop_table('learning_fields')
    op.drop_index('ix_learning_levels_slug', table_name='learning_levels')
    op.drop_index('ix_learning_levels_id', table_name='learning_levels')
    op.drop_table('learning_levels')
