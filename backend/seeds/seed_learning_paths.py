"""
backend/seeds/seed_learning_paths.py

Seeds the learning-path configuration on top of what migration 011 created.

Migration 011 already holds the controlled vocabulary — the three levels, six
fields and five career goals. This script adds everything that *relates*
them: skills, the prerequisite rule for Multimodal, what each career goal
needs, which existing courses serve which fields and goals, the stages of a
journey, and each career goal's template.

Run after the content seeds (it points at courses that must already exist):

    python seed.py
    python seeds/seed_tool_courses.py            (+ the seed_tool_<name>.py content)
    python seeds/seed_learning_paths.py

Idempotent, and deliberately non-destructive. It only ever *creates what is
missing*: a row that already exists — because an earlier run made it, or
because an admin has since edited it — is left exactly as it is. Re-running
after adding a course to this file adds that course; it never resets anything.
Everything is written through `catalog_admin`, the same validated functions
the admin API uses, so this file cannot produce a prerequisite cycle the API
would refuse.

No new content is invented here. Every course below is an existing track level
or tool course; levels of those with no published lessons are catalogued as
*planned* and appear to learners only once their content lands (see
`is_available` in catalog_service).

The curriculum itself - which goal each course serves and how much (core /
supporting / optional), the stages and each goal's template - is data in
`seeds/curriculum.py`. This script creates it on a fresh database; to bring a
database that ALREADY has a catalogue up to date, run
`python seeds/sync_curriculum.py` (it changes only what curriculum.py names,
deletes nothing and never touches a learner).
"""
import logging
import os
import sys
from typing import Dict, List, Optional

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

from app.models.learning import CareerTrack, DifficultyLevel, Topic
from app.models.learning_path import (
    CareerRole, Course, LearningField, PathStage, PathTemplate, Skill,
)
from app.models.tool_course import ToolCourse, ToolTopic
from app.services.learning import catalog_admin as admin
from seeds.curriculum import COURSE_DIRECTORY_COURSES, STAGES, TEMPLATES, roles_for
from seeds.sync_curriculum import (
    ensure_curriculum_courses, ensure_shell_courses, sync_course_prerequisites, sync_track_workflow,
)

logger = logging.getLogger(__name__)

TRACK_SLUG = "ai-developer"

# ─── Skills ─────────────────────────────────────────────────────────────────
# Names stay in English: they are technical terms, and the interface renders
# them through the terminology dictionary (`findTerm`) rather than through a
# second set of translations kept here.
SKILLS = [
    ("llms", "LLMs"), ("prompt-engineering", "Prompt Engineering"), ("rag", "RAG"),
    ("retrieval", "Retrieval"), ("embeddings", "Embeddings"), ("semantic-search", "Semantic Search"),
    ("vector-databases", "Vector Databases"), ("ai-agents", "AI Agents"), ("mcp", "Model Context Protocol (MCP)"), ("evaluation", "Evaluation"),
    ("observability", "Observability"), ("fastapi", "FastAPI"), ("api-design", "API Design"),
    ("production-deployment", "Production Deployment"), ("system-design", "System Design"),
    ("multimodal", "Multimodal AI"), ("vision-language-models", "Vision-Language Models"),
    ("document-ai", "Document AI"), ("langchain", "LangChain"), ("langgraph", "LangGraph"),
    ("llamaindex", "LlamaIndex"), ("qdrant", "Qdrant"),
    # Required by career goals but taught by no published course yet.
    ("sql", "SQL"), ("data-analysis", "Data Analysis"), ("statistics", "Statistics"),
    ("machine-learning", "Machine Learning"), ("deep-learning", "Deep Learning"),
    ("mlops", "MLOps"), ("computer-vision", "Computer Vision"), ("speech-recognition", "Speech Recognition"),
    ("voice-ai", "Voice AI"), ("text-to-speech", "Text-to-Speech"),
    ("python", "Python"), ("numpy", "NumPy"), ("pandas", "pandas"),
    ("scikit-learn", "scikit-learn"), ("pytorch", "PyTorch"), ("transformers", "Transformers"),
    ("docker", "Docker"), ("ci-cd", "CI/CD"), ("cloud-deployment", "Cloud Deployment"),
]

# Skills that are really named products: a learner who knows LangChain has not
# thereby learned RAG, so these are catalogued as 'tool' and offered under their
# own heading. (Migration 013 tags the same slugs on databases that already
# hold them.) Everything else in SKILLS is a capability.
TOOL_SKILLS = {
    "langchain", "langgraph", "llamaindex", "qdrant", "fastapi", "python", "numpy",
    "pandas", "scikit-learn", "pytorch", "transformers", "docker",
}

# The skill tags authors already put on every topic (`topics.skill_tags`,
# `tool_topics.skill_tags`), mapped to catalogue skills. A course's `teaches`
# is the union of its topics' tags through this table — derived from what the
# lessons say they cover, not typed a second time. A tag with no entry (a
# language, a vendor, "career") teaches nothing here on purpose: Python being
# the language of the examples is not a skill the course teaches.
TAG_TO_SKILL = {
    "llm": "llms", "llm-api": "llms", "llm-integration": "llms", "openai": "llms", "chat-models": "llms",
    "prompt-engineering": "prompt-engineering", "system-prompts": "prompt-engineering",
    "zero-shot": "prompt-engineering",
    "rag": "rag",
    "retrieval": "retrieval", "indexing": "retrieval", "sparse-retrieval": "retrieval",
    "bm25": "retrieval", "keyword-search": "retrieval",
    "embeddings": "embeddings", "vectors": "embeddings", "similarity": "embeddings",
    "cosine-similarity": "embeddings", "sentence-transformers": "embeddings",
    "semantic-search": "semantic-search", "vector-search": "semantic-search",
    "vector-database": "vector-databases",
    "ai-agents": "ai-agents", "agentic-systems": "ai-agents", "tool-use": "ai-agents",
    "mcp": "mcp", "model-context-protocol": "mcp",
    "evaluation": "evaluation", "rag-evaluation": "evaluation", "evaluation-datasets": "evaluation",
    "metrics": "evaluation",
    "observability": "observability",
    "fastapi": "fastapi", "api-design": "api-design",
    "production": "production-deployment",
    "multimodal": "multimodal", "vlm": "vision-language-models", "vision": "vision-language-models",
    "image-understanding": "vision-language-models", "document-ai": "document-ai",
    "langchain": "langchain", "langgraph": "langgraph", "llamaindex": "llamaindex", "qdrant": "qdrant",
    "system-design": "system-design", "architecture": "system-design",
    "speech-recognition": "speech-recognition", "asr": "speech-recognition", "stt": "speech-recognition",
    "text-to-speech": "text-to-speech", "tts": "text-to-speech",
    "voice-ai": "voice-ai", "voice-agents": "voice-ai", "real-time-voice": "voice-ai",
}

# ─── What each field and career goal is made of ─────────────────────────────

# Multimodal builds on at least one single modality, ideally two. It is
# `min_level = advanced` in the migration; the rule below is the prerequisite
# half. Changing "any one, ideally two" to something stricter is an edit here
# (or in the admin API), not a code change.
FIELD_RULES = {
    "multimodal": dict(
        prerequisites=["nlp", "computer-vision", "speech"],
        prerequisite_min_required=1,
        prerequisite_recommended=2,
    ),
}

# required_fields = foundations the goal cannot skip; recommended_fields = the
# specialisation routes it suits. Skills: what the goal is judged on.
ROLE_RULES = {
    "data-analyst": dict(
        required_fields=["data"], recommended_fields=["machine-learning"],
        required_skills=["sql", "data-analysis", "statistics"], optional_skills=[],
    ),
    "ml-engineer": dict(
        required_fields=["machine-learning"], recommended_fields=["data", "nlp", "computer-vision", "speech"],
        required_skills=["machine-learning", "evaluation"], optional_skills=["deep-learning", "mlops"],
    ),
    "ai-developer": dict(
        required_fields=[], recommended_fields=["nlp", "multimodal"],
        required_skills=["llms", "prompt-engineering", "rag"], optional_skills=["ai-agents", "fastapi"],
    ),
    "mlops-engineer": dict(
        required_fields=["machine-learning"], recommended_fields=["data"],
        required_skills=["production-deployment", "machine-learning"], optional_skills=["observability", "fastapi"],
    ),
    # A goal in its own right, with several specialisation routes — not the sum
    # of the other four. Its required skills are the ones every route shares.
    "ai-engineer": dict(
        required_fields=["machine-learning"],
        recommended_fields=["nlp", "computer-vision", "speech", "multimodal"],
        required_skills=["evaluation", "production-deployment"],
        optional_skills=["llms", "rag", "ai-agents", "multimodal", "machine-learning"],
    ),
}

# ─── Courses ────────────────────────────────────────────────────────────────
# (track level order, slug, title, title_ar, level, fields)
#
# Levels are the modal difficulty of each level's topics (topics.difficulty),
# with two deliberate overrides: "Advanced RAG" is advanced because its name and
# its prerequisites say so, and "Multimodal AI" is advanced because Multimodal
# is defined as an advanced field. A course whose level disagreed with its
# field would be classed "below level" for exactly the learners it is for.
TRACK_LEVEL_COURSES = [
    (1, "ai-engineering-foundations", "AI Engineering Foundations", "أسس هندسة الذكاء الاصطناعي",
     "beginner", []),
    (2, "llm-integration", "LLM Integration", "دمج الـ LLMs في التطبيقات",
     "beginner", ["nlp"]),
    (3, "rag-knowledge-systems", "RAG & Knowledge Systems", "أنظمة RAG والمعرفة",
     "intermediate", ["nlp"]),
    (4, "prompt-engineering", "Prompt Engineering", "هندسة الـ Prompts",
     "intermediate", ["nlp"]),
    (5, "embeddings-semantic-search", "Embeddings & Semantic Search", "الـ Embeddings والبحث الدلالي",
     "intermediate", ["nlp"]),
    (6, "advanced-rag", "Advanced RAG", "RAG المتقدم",
     "advanced", ["nlp"]),
    (7, "ai-agents-orchestration", "AI Agents & Orchestration", "الـ AI Agents والـ Orchestration",
     "intermediate", ["nlp"]),
    (8, "deployment-integration", "Deployment & Integration Frameworks", "النشر وأطر التكامل",
     "advanced", []),
    (9, "multimodal-ai", "Multimodal AI", "الذكاء الاصطناعي متعدد الوسائط",
     "advanced", ["multimodal"]),
    (10, "ai-evaluation-observability", "AI Evaluation & Observability", "تقييم الـ AI ومراقبته",
     "intermediate", []),
]

# Prerequisites between the track's own levels — a track is sequential by
# design. Tool courses carry none: the tools page promises "no prerequisites".
PREREQUISITES = {
    "llm-integration": ["ai-engineering-foundations"],
    "rag-knowledge-systems": ["llm-integration"],
    "prompt-engineering": ["llm-integration"],
    "embeddings-semantic-search": ["llm-integration"],
    "advanced-rag": ["rag-knowledge-systems", "embeddings-semantic-search"],
    "ai-agents-orchestration": ["llm-integration"],
    "deployment-integration": ["llm-integration"],
    "multimodal-ai": ["llm-integration"],
    "ai-evaluation-observability": ["rag-knowledge-systems"],
}

# (tool course slug, fields, extra skills it will teach once written)
# The level is the tool course's own declared difficulty. Which career goals a
# course serves, and how much, is `COURSE_ROLES` in seeds/curriculum.py.
TOOL_COURSE_TAGS = [
    ("langchain",          ["nlp"], []),
    ("langgraph",          ["nlp"], []),
    ("llamaindex",         ["nlp"], []),
    ("openai-api",         ["nlp"], ["llms"]),
    ("hugging-face",       ["nlp", "machine-learning"], []),
    ("pinecone",           ["nlp"], ["vector-databases"]),
    ("qdrant",             ["nlp"], []),
    ("weaviate",           ["nlp", "multimodal"], ["vector-databases"]),
    ("mlflow",             ["machine-learning"], ["mlops"]),
    ("dvc",                ["machine-learning", "data"], ["mlops"]),
    ("wandb",              ["machine-learning"], []),
    ("fastapi-serving",    [], []),
    ("airflow",            ["data", "machine-learning"], ["mlops"]),
    ("dbt",                ["data"], ["sql", "data-analysis"]),
    ("great-expectations", ["data"], ["data-analysis"]),
    ("streamlit",          ["data", "machine-learning"], []),
]

# ─── Stages, templates and course roles ────────────────────────────────────
# Live in seeds/curriculum.py, shared with seeds/sync_curriculum.py (which brings an
# existing database to the same state). STAGES, TEMPLATES and `roles_for` are imported
# at the top of this file.

# ─── Helpers ────────────────────────────────────────────────────────────────

_LEVEL_BY_DIFFICULTY = {
    DifficultyLevel.beginner: "beginner",
    DifficultyLevel.intermediate: "intermediate",
    DifficultyLevel.advanced: "advanced",
}


def _taught_skills(tags: List[str], extra: List[str]) -> List[str]:
    derived = {TAG_TO_SKILL[t] for t in tags if t in TAG_TO_SKILL}
    return sorted(derived | set(extra))


def _track_level_tags(db: Session, level_id: int) -> List[str]:
    tags: List[str] = []
    for (skill_tags,) in db.query(Topic.skill_tags).filter(Topic.level_id == level_id).all():
        tags.extend(skill_tags or [])
    return tags


def _tool_course_tags(db: Session, tool_course_id: int) -> List[str]:
    tags: List[str] = []
    for (skill_tags,) in db.query(ToolTopic.skill_tags).filter(ToolTopic.tool_course_id == tool_course_id).all():
        tags.extend(skill_tags or [])
    return tags


# ─── Seeding ────────────────────────────────────────────────────────────────

def seed_learning_catalog(db: Session) -> Dict[str, int]:
    """Create whatever of the configuration above is missing. Returns how many
    rows of each kind it created. Commits once, at the end."""
    created: Dict[str, int] = {k: 0 for k in ("skills", "fields", "roles", "courses", "stages", "templates")}

    try:
        for slug, name in SKILLS:
            if db.query(Skill).filter(Skill.slug == slug).first() is None:
                admin.upsert_skill(db, slug, name=name, kind="tool" if slug in TOOL_SKILLS else "skill")
                created["skills"] += 1

        for slug, rule in FIELD_RULES.items():
            field = db.query(LearningField).filter(LearningField.slug == slug).first()
            if field is None:
                logger.warning("field '%s' is missing — was migration 011 applied?", slug)
                continue
            if not admin.field_has_prerequisites(db, field):
                field.prerequisite_min_required = rule["prerequisite_min_required"]
                field.prerequisite_recommended = rule["prerequisite_recommended"]
                admin.set_field_prerequisites(db, field, rule["prerequisites"])
                created["fields"] += 1

        for slug, rule in ROLE_RULES.items():
            role = db.query(CareerRole).filter(CareerRole.slug == slug).first()
            if role is None:
                logger.warning("career goal '%s' is missing — was migration 011 applied?", slug)
                continue
            if not role.field_links and not role.skill_links:
                admin.set_role_relations(db, role, **rule)
                created["roles"] += 1

        new_courses: List[str] = []

        track = db.query(CareerTrack).filter(CareerTrack.slug == TRACK_SLUG).first()
        levels_by_order = {l.order: l for l in track.levels} if track else {}
        if track is None:
            logger.warning("track '%s' not found; its levels are not catalogued", TRACK_SLUG)
        for order, slug, title, title_ar, level, fields in TRACK_LEVEL_COURSES:
            source = levels_by_order.get(order)
            if source is None or db.query(Course).filter(Course.slug == slug).first():
                continue
            admin.upsert_course(
                db, slug, source={"kind": "track_level", "track_slug": TRACK_SLUG, "level_order": order},
                level=level, title=title, title_ar=title_ar,
                fields=fields, roles=roles_for(slug), teaches=_taught_skills(_track_level_tags(db, source.id), []),
            )
            new_courses.append(slug)
            created["courses"] += 1

        for source_slug, fields, extra in TOOL_COURSE_TAGS:
            source = db.query(ToolCourse).filter(ToolCourse.slug == source_slug).first()
            if source is None or db.query(Course).filter(Course.slug == source_slug).first():
                continue
            admin.upsert_course(
                db, source_slug, source={"kind": "tool_course", "slug": source_slug},
                level=_LEVEL_BY_DIFFICULTY.get(source.difficulty, "intermediate"),
                fields=fields, roles=roles_for(source_slug),
                teaches=_taught_skills(_tool_course_tags(db, source.id), extra),
            )
            new_courses.append(source_slug)
            created["courses"] += 1

        # Placeholder levels of the other tracks, catalogued as courses with no
        # lessons - never startable until content lands (see seeds/curriculum.py).
        for change in ensure_shell_courses(db):
            if change.kind == "course+":
                created["courses"] += 1

        directory_course_changes = ensure_curriculum_courses(db)
        created["courses"] += sum(change.kind == "course+" for change in directory_course_changes)

        # Second pass: prerequisites reference other courses, so they can only
        # be written once every course above exists.
        for slug in new_courses:
            wanted = PREREQUISITES.get(slug)
            if wanted:
                course = db.query(Course).filter(Course.slug == slug).first()
                present = [s for s in wanted if db.query(Course).filter(Course.slug == s).first()]
                admin.set_course_relations(db, course, prerequisites=present)

        # A course-directory course gets its required prerequisites from the registry and its
        # recommended ones from its own manifest - the very rule `sync_curriculum` applies.
        sync_course_prerequisites(
            db, only={change.subject for change in directory_course_changes if change.kind == "course+"},
        )

        # The five fixed career tracks' explicit order/required/section - see
        # seeds/curriculum.py:TRACK_WORKFLOWS. Idempotent, safe to run again by
        # `sync_curriculum.py` on an already-seeded database.
        sync_track_workflow(db)

        known_courses = {c.slug for c in db.query(Course).all()}
        for slug, title, title_ar, phase, kind, courses in STAGES:
            if db.query(PathStage).filter(PathStage.slug == slug).first():
                continue
            admin.upsert_stage(
                db, slug, title=title, title_ar=title_ar, phase=phase, kind=kind,
                courses=[c for c in courses if c in known_courses],
            )
            created["stages"] += 1

        for slug, role_slug, title, title_ar, stages in TEMPLATES:
            if db.query(PathTemplate).filter(PathTemplate.slug == slug).first():
                continue
            if db.query(CareerRole).filter(CareerRole.slug == role_slug).first() is None:
                continue
            admin.upsert_template(
                db, slug, title=title, title_ar=title_ar, career_goal=role_slug,
                stages=[{"stage": s, "field": f} for s, f in stages],
            )
            created["templates"] += 1

        db.commit()
    except Exception:
        db.rollback()
        raise
    return created


if __name__ == "__main__":
    require_migrated_schema()
    session = SessionLocal()
    try:
        report = seed_learning_catalog(session)
        for kind, count in report.items():
            print(f"  {kind:<10} +{count}")
        print("Done.")
    finally:
        session.close()
