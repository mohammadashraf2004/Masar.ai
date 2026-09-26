"""
backend/seeds/curriculum.py

The curriculum as data: which career goal each course serves and how much, the
stages of a journey and what is in them, and each goal's ordered template.

Pure data and pure lookups - no database, no ORM. Two things consume it:

  * `seed_learning_paths.py` creates whatever is missing on a fresh database;
  * `sync_curriculum.py` brings an existing database to this state.

Both read the same lists, so a fresh install and a synced one cannot drift.

What this file is NOT
---------------------
It invents no course. Every slug below is a course that already exists in the
catalogue or a placeholder level/tool course that already exists as a content
source. A course with no lessons is a *shell*: catalogued so a goal can say
where it will sit, never offered to a learner as startable (`is_available` in
`catalog_service` is "has at least one lesson"). Courses that do not exist at
all - ML System Design, ML Design Patterns, the MLOps course - have no record
and no stage; see `PLANNED_SLOTS`.

Roles are per goal, per course
------------------------------
`COURSE_ROLES[course][goal]` is `core`, `supporting` or `optional`. One course
entity, a different weight in each goal - never a copy per goal. The weight is
descriptive: it changes what a course is *called* for a goal, not whether a path
requires it. (Generator rules, course states and progress do not read it.)
"""
from typing import Dict, List, Optional, Sequence, Tuple

CORE, SUPPORTING, OPTIONAL = "core", "supporting", "optional"
_C, _S, _O = CORE, SUPPORTING, OPTIONAL

DATA_ANALYST = "data-analyst"
ML_ENGINEER = "ml-engineer"
AI_DEVELOPER = "ai-developer"
MLOPS_ENGINEER = "mlops-engineer"
AI_ENGINEER = "ai-engineer"
GOALS = (DATA_ANALYST, ML_ENGINEER, AI_DEVELOPER, MLOPS_ENGINEER, AI_ENGINEER)

_DA, _ML, _AID, _OPS, _AIE = GOALS

# ─── Course roles ───────────────────────────────────────────────────────────
# course slug -> {career goal: relation}. A goal that is absent is a goal the
# course does not serve. For a course that already existed, no tag that was
# already there is removed - relations are only added or reweighted.
COURSE_ROLES: Dict[str, Dict[str, str]] = {
    # -- Courses with lessons today: the AI Developer track's ten levels ...
    "ai-engineering-foundations":  {_ML: _S, _AID: _C, _OPS: _O, _AIE: _C},
    "llm-integration":             {_ML: _S, _AID: _C, _OPS: _O, _AIE: _C},
    "prompt-engineering":          {_ML: _O, _AID: _C, _AIE: _C},
    # RAG is an ML Engineer NLP elective, not the identity of that broad
    # track. It remains core for the two LLM-application tracks.
    "rag-knowledge-systems":       {_ML: _O, _AID: _C, _AIE: _C},
    "embeddings-semantic-search":  {_ML: _O, _AID: _C, _AIE: _C},
    "advanced-rag":                {_AID: _C, _AIE: _C},
    "ai-agents-orchestration":     {_AID: _C, _AIE: _C},
    "deployment-integration":      {_ML: _S, _AID: _C, _OPS: _C, _AIE: _C},
    "multimodal-ai":               {_AID: _O, _AIE: _O},
    "ai-evaluation-observability": {_ML: _S, _AID: _C, _OPS: _C, _AIE: _C},
    # -- ... and the tool courses with lessons.
    "langchain":                   {_AID: _C, _AIE: _S},
    "langgraph":                   {_AID: _C, _AIE: _S},
    "llamaindex":                  {_AID: _S, _OPS: _O, _AIE: _S},
    "qdrant":                      {_AID: _S, _OPS: _O, _AIE: _S},
    "fastapi-serving":             {_ML: _S, _AID: _S, _OPS: _C, _AIE: _C},

    # -- Shells that already existed in the catalogue (no lessons yet).
    "openai-api":                  {_AID: _S, _AIE: _S},
    "hugging-face":                {_ML: _S, _AID: _S, _AIE: _S},
    "pinecone":                    {_AID: _O, _AIE: _O},
    "weaviate":                    {_AID: _O, _AIE: _O},
    "mlflow":                      {_ML: _C, _OPS: _C, _AIE: _S},
    "dvc":                         {_ML: _S, _OPS: _C},
    "wandb":                       {_ML: _S, _OPS: _S},
    "airflow":                     {_ML: _O, _OPS: _C},
    "dbt":                         {_DA: _S},
    "great-expectations":          {_DA: _S, _ML: _O},
    "streamlit":                   {_DA: _S, _ML: _O},

    # -- Shells catalogued now, from placeholder levels that already exist in
    #    the legacy tracks (see SHELL_COURSES). No lessons, not startable.
    "python-sql-foundations":      {_DA: _C},
    "data-analysis-pandas":        {_DA: _C},
    "data-visualisation":          {_DA: _C},
    "statistics-for-analysts":     {_DA: _C},
    "bi-dashboards-reporting":     {_DA: _C},
    "ml-fundamentals":             {_DA: _S, _ML: _C, _OPS: _S, _AIE: _C},
    "feature-engineering":         {_ML: _C},
    "deep-learning-pytorch":       {_ML: _C, _AIE: _C},
    "model-evaluation":            {_ML: _C},
    "transformers-fine-tuning":    {_ML: _C},
}

# Canonical course directories are catalogue shells until their course-local
# loaders have been integrated with a persistent content source. The catalogue
# slugs are lower-case; `course_id` preserves the frozen ID in each export.
#
# `prerequisites` deliberately contains *only hard dependencies*.  Several
# course manifests also list a broader recommended sequence; the current
# learning-path schema has no soft-prerequisite relation, so encoding those
# recommendations here would incorrectly force an LLM route into MLOps (and
# turn every advanced route into one long, artificial chain).
COURSE_DIRECTORY_COURSES = [
    {
        "course_id": "COURSE-001", "slug": "course-001",
        "title": "Machine Learning Foundations", "track": ML_ENGINEER,
        "level": "beginner", "fields": ["machine-learning"],
        "roles": {_ML: _C, _AID: _S, _OPS: _S, _AIE: _C},
        "skills": ["machine-learning", "python", "scikit-learn"],
        "prerequisites": [], "phase": "foundations", "path_field": None,
        "capability": "Build and evaluate foundational machine-learning models.",
    },
    {
        "course_id": "COURSE-002", "slug": "course-002",
        "title": "Deep Learning Foundations", "track": ML_ENGINEER,
        "level": "intermediate", "fields": ["machine-learning"],
        "roles": {_ML: _C, _AID: _S, _OPS: _S, _AIE: _C},
        "skills": ["deep-learning", "python", "numpy"],
        "prerequisites": ["course-001"], "phase": "foundations", "path_field": None,
        "capability": "Understand neural-network representations, mathematics, and architectures.",
    },
    {
        "course_id": "COURSE-003", "slug": "course-003",
        "title": "Applied Deep Learning", "track": ML_ENGINEER,
        "level": "intermediate", "fields": ["machine-learning"],
        "roles": {_ML: _C, _AID: _S, _AIE: _C},
        "skills": ["deep-learning", "pytorch"],
        "prerequisites": ["course-002"], "phase": "foundations", "path_field": None,
        "capability": "Implement, debug, evaluate, profile, and fine-tune applied PyTorch systems.",
    },
    {
        "course_id": "COURSE-004", "slug": "course-004",
        "title": "Applied NLP with Transformers", "track": ML_ENGINEER,
        "level": "intermediate", "fields": ["nlp"],
        "roles": {_ML: _C, _AID: _S, _AIE: _C},
        "skills": ["transformers", "machine-learning", "evaluation"],
        "prerequisites": ["course-003"],
        "phase": "specialization", "path_field": "nlp",
        "capability": "Build, fine-tune, evaluate, debug, compare, and optimize Transformer NLP systems.",
    },
    {
        "course_id": "COURSE-005", "slug": "course-005",
        "title": "Applied LLM Engineering", "track": AI_DEVELOPER,
        "level": "intermediate", "fields": ["nlp"],
        "roles": {_AID: _C, _AIE: _C},
        "skills": ["llms", "prompt-engineering", "embeddings", "rag", "ai-agents"],
        "prerequisites": ["course-004"],
        "phase": "specialization", "path_field": "nlp",
        "capability": "Build and evaluate LLM applications using embeddings, retrieval, prompting, tools, and adaptation.",
    },
    {
        "course_id": "COURSE-006", "slug": "course-006",
        "title": "Production AI Engineering", "track": MLOPS_ENGINEER,
        "level": "advanced", "fields": ["machine-learning"],
        "roles": {_ML: _S, _AID: _S, _OPS: _C, _AIE: _C},
        "skills": ["evaluation", "observability", "production-deployment", "system-design"],
        "prerequisites": ["course-001"],
        "phase": "engineering", "path_field": None,
        "capability": "Design, evaluate, secure, optimize, and operate production AI systems.",
    },
    {
        "course_id": "COURSE-007", "slug": "course-007",
        "title": "Advanced LLM Systems & Application Architecture", "track": AI_DEVELOPER,
        "level": "advanced", "fields": ["nlp"],
        "roles": {_AID: _S, _AIE: _S},
        "skills": ["llms", "rag", "ai-agents", "system-design", "evaluation"],
        "prerequisites": ["course-005", "course-006"],
        "phase": "specialization", "path_field": "nlp",
        "capability": "Design, adapt, evaluate, and optimize advanced LLM systems and applications.",
    },
    {
        "course_id": "COURSE-008", "slug": "course-008",
        "title": "Vision-Language & Multimodal AI Engineering", "track": AI_ENGINEER,
        "level": "advanced", "fields": ["computer-vision", "multimodal"],
        "roles": {_ML: _O, _AID: _O, _AIE: _C},
        "skills": ["multimodal", "vision-language-models", "deep-learning"],
        "prerequisites": ["course-003"],
        "phase": "multimodal", "path_field": "multimodal",
        "capability": "Build and evaluate vision-language and multimodal AI systems.",
    },
    {
        "course_id": "COURSE-009", "slug": "course-009",
        "title": "Enterprise RAG Engineering", "track": AI_DEVELOPER,
        "level": "advanced", "fields": ["nlp"],
        "roles": {_ML: _O, _AID: _C, _AIE: _S},
        "skills": ["rag", "retrieval", "vector-databases", "evaluation", "observability"],
        "prerequisites": ["course-005"],
        "phase": "specialization", "path_field": "nlp",
        "capability": "Engineer production RAG systems for retrieval quality, grounding, governance, and resilience.",
    },
    {
        "course_id": "COURSE-010", "slug": "course-010",
        "title": "AI Service Engineering with FastAPI", "track": AI_DEVELOPER,
        "level": "intermediate", "fields": ["nlp"],
        "roles": {_AID: _C, _OPS: _C, _AIE: _S},
        "skills": ["fastapi", "api-design", "production-deployment", "python"],
        "prerequisites": ["course-006"],
        "phase": "engineering", "path_field": "nlp",
        "capability": "Design, secure, test, optimize, and deploy backend services for AI applications.",
    },
    {
        "course_id": "COURSE-011", "slug": "course-011",
        "title": "Cloud Deployment & CI/CD for AI Engineers", "track": MLOPS_ENGINEER,
        "level": "advanced", "fields": ["machine-learning"],
        "roles": {_ML: _O, _AID: _S, _OPS: _C, _AIE: _C},
        "skills": ["cloud-deployment", "ci-cd", "docker", "production-deployment"],
        "prerequisites": ["course-006", "course-010"],
        "phase": "engineering", "path_field": None,
        "capability": "Deploy, secure, automate, and operate AI backend services on cloud platforms.",
    },
    {
        "course_id": "COURSE-012", "slug": "course-012",
        "title": "Agentic AI Systems Engineering", "track": AI_DEVELOPER,
        "level": "advanced", "fields": ["nlp"],
        "roles": {_AID: _C, _AIE: _S},
        "skills": ["ai-agents", "langgraph", "evaluation", "system-design"],
        "prerequisites": ["course-005", "course-006", "course-007"],
        "phase": "specialization", "path_field": "nlp",
        "capability": "Design, orchestrate, evaluate, secure, and operate production agentic systems.",
    },
    {
        "course_id": "COURSE-013", "slug": "course-013",
        "title": "Applied Data Analysis with Python", "track": DATA_ANALYST,
        "level": "beginner", "fields": ["data"],
        "roles": {_DA: _C, _ML: _S, _AIE: _S},
        "skills": ["sql", "data-analysis", "statistics", "python", "numpy", "pandas"],
        "prerequisites": [], "phase": "foundations", "path_field": "data",
        "capability": "Load, clean, analyze, visualize, model, and communicate findings from real datasets.",
    },
    {
        "course_id": "COURSE-014", "slug": "course-014",
        "title": "Image Processing & Computer Vision Engineering", "track": ML_ENGINEER,
        "level": "intermediate", "fields": ["computer-vision"],
        "roles": {_ML: _C, _AID: _S, _OPS: _S, _AIE: _C},
        "skills": ["computer-vision"],
        "prerequisites": ["course-001"], "phase": "specialization", "path_field": "computer-vision",
        "capability": "Design, implement, debug, and evaluate classical and modern image-processing and computer-vision pipelines.",
    },
]

COURSE_ROLES.update({course["slug"]: course["roles"] for course in COURSE_DIRECTORY_COURSES})

# The courses that have lessons today. Everything else in COURSE_ROLES is a
# shell. Adding a course to this tuple is a claim that it has lessons; a
# database test checks it against what the catalogue reports available.
COURSES_WITH_LESSONS = (
    "ai-engineering-foundations", "llm-integration", "prompt-engineering", "rag-knowledge-systems",
    "embeddings-semantic-search", "advanced-rag", "ai-agents-orchestration", "deployment-integration",
    "multimodal-ai", "ai-evaluation-observability",
    "langchain", "langgraph", "llamaindex", "qdrant", "fastapi-serving",
)

# All 14 directory courses have a primary placement below.  `course_roles`
# remains broader than a template where that is useful for catalogue discovery:
# an optional ML specialisation, for example, should be discoverable without
# silently becoming part of every ML Engineer journey.
DEFERRED_PLACEMENTS: Dict[str, Dict[str, str]] = {}

# ─── Placeholder levels to catalogue as (empty) courses ─────────────────────
# (course slug, legacy track slug, level order, learner level, fields)
# Each points at a level that already exists in the legacy tracks with a single
# empty topic and no lessons. The catalogue entry takes the level's own title.
# Levels are provisional: they are inert while a course has no lessons, and are
# set for real when the content lands.
SHELL_COURSES: List[Tuple[str, str, int, str, List[str]]] = [
    ("python-sql-foundations",   DATA_ANALYST, 1, "beginner",     ["data"]),
    ("data-analysis-pandas",     DATA_ANALYST, 2, "beginner",     ["data"]),
    ("data-visualisation",       DATA_ANALYST, 3, "beginner",     ["data"]),
    ("statistics-for-analysts",  DATA_ANALYST, 4, "intermediate", ["data"]),
    ("bi-dashboards-reporting",  DATA_ANALYST, 5, "intermediate", ["data"]),
    ("ml-fundamentals",          ML_ENGINEER,  1, "beginner",     ["machine-learning"]),
    ("feature-engineering",      ML_ENGINEER,  2, "intermediate", ["machine-learning"]),
    ("deep-learning-pytorch",    ML_ENGINEER,  3, "intermediate", ["machine-learning"]),
    ("model-evaluation",         ML_ENGINEER,  4, "intermediate", ["machine-learning"]),
    ("transformers-fine-tuning", ML_ENGINEER,  5, "advanced",     ["machine-learning", "nlp"]),
]

# Slots that intentionally have NO record: nothing exists to point at, and
# inventing an empty course to hold the place would make the catalogue look
# further along than it is. Phase 2 adds each as a real course, together with
# its stage and template entry.
PLANNED_SLOTS: Dict[str, str] = {
    "ml-system-design": "ML Engineer, MLOps (between NLP/Transformers and production)",
    "ml-design-patterns": "MLOps (after ML System Design)",
    "mlops": "MLOps / production ML, and the AI Engineer 'Production AI / ML Systems' stage",
}

# ─── Stages ─────────────────────────────────────────────────────────────────
# (slug, title, title_ar, phase, kind, course slugs in order)
# A stage listing courses with no lessons is fine: they count as upcoming and
# the stage reads "coming soon" until content lands. Existing stage slugs are
# kept - saved learner paths refer to them.
STAGES: List[Tuple[str, str, str, str, str, List[str]]] = [
    ("foundations", "AI Foundations", "أسس الذكاء الاصطناعي", "foundations", "learning",
     ["ai-engineering-foundations"]),
    ("data-foundations", "Data Foundations", "أسس البيانات", "foundations", "learning",
     ["python-sql-foundations", "data-analysis-pandas"]),
    ("data-analysis", "Data Analysis & Reporting", "تحليل البيانات والتقارير", "specialization", "learning",
     ["data-visualisation", "statistics-for-analysts", "bi-dashboards-reporting"]),
    ("data-tooling", "Data Tooling", "أدوات البيانات", "engineering", "learning",
     ["dbt", "great-expectations", "streamlit"]),
    ("machine-learning", "Machine Learning", "تعلّم الآلة", "foundations", "learning",
     ["ml-fundamentals"]),
    ("feature-engineering", "Feature Engineering", "هندسة الـ Features", "foundations", "learning",
     ["feature-engineering"]),
    ("deep-learning", "Deep Learning", "التعلّم العميق", "foundations", "learning",
     ["deep-learning-pytorch"]),
    ("model-evaluation", "Model Evaluation", "تقييم النماذج", "foundations", "learning",
     ["model-evaluation"]),
    ("nlp-transformers", "NLP & Transformers", "الـ NLP والـ Transformers", "specialization", "learning",
     ["transformers-fine-tuning", "hugging-face"]),
    ("nlp-llm", "NLP & LLM Engineering", "هندسة NLP والـ LLMs", "specialization", "learning",
     ["llm-integration", "prompt-engineering", "langchain", "openai-api"]),
    ("rag", "RAG Engineering", "هندسة الـ RAG", "specialization", "learning",
     ["rag-knowledge-systems", "embeddings-semantic-search", "advanced-rag", "llamaindex",
      "qdrant", "pinecone", "weaviate"]),
    ("agents", "AI Agents", "الـ AI Agents", "specialization", "learning",
     ["ai-agents-orchestration", "langgraph"]),
    ("computer-vision", "Computer Vision", "الرؤية الحاسوبية", "specialization", "learning", []),
    ("advanced-cv", "Advanced Computer Vision", "الرؤية الحاسوبية المتقدمة", "specialization", "learning", []),
    ("vision-language", "Vision-Language Models", "نماذج الرؤية واللغة", "specialization", "learning", []),
    ("audio-processing", "Audio Processing", "معالجة الصوت", "specialization", "learning", []),
    ("speech-recognition", "Speech Recognition", "التعرّف على الكلام", "specialization", "learning", []),
    ("text-to-speech", "Text-to-Speech", "تحويل النص إلى كلام", "specialization", "learning", []),
    ("voice-ai", "Voice AI", "الذكاء الاصطناعي الصوتي", "specialization", "learning", []),
    ("realtime-voice-agents", "Real-time Voice Agents", "وكلاء صوتيون في الزمن الحقيقي",
     "specialization", "learning", []),
    ("multimodal", "Multimodal AI Engineering", "هندسة الذكاء الاصطناعي متعدد الوسائط", "multimodal", "learning",
     ["multimodal-ai"]),
    # The production content that exists today (levels 8 and 10) is about
    # deploying and evaluating LLM applications, so it sits in an NLP-gated
    # stage of its own. Left in the generic stage it dragged LLM and RAG
    # prerequisites into a Computer Vision learner's route.
    ("llm-production", "Deploying & Evaluating LLM Systems", "نشر أنظمة الـ LLMs وتقييمها", "engineering",
     "learning", ["deployment-integration", "ai-evaluation-observability"]),
    ("mlops-tooling", "MLOps Tooling", "أدوات الـ MLOps", "engineering", "learning",
     ["mlflow", "wandb", "dvc", "airflow"]),
    ("production", "MLOps & Production AI", "الـ MLOps والـ AI في بيئة الإنتاج", "engineering", "learning",
     ["fastapi-serving"]),
    # Supporting LLM knowledge for goals that are not LLM goals. These sit at the
    # END of their paths and only when the learner picked NLP.
    ("llm-applications", "LLM Applications", "تطبيقات الـ LLMs", "specialization", "learning",
     ["ai-engineering-foundations", "llm-integration", "prompt-engineering",
      "rag-knowledge-systems", "embeddings-semantic-search"]),
    ("llm-systems", "LLM Systems", "أنظمة الـ LLMs", "specialization", "learning",
     ["ai-engineering-foundations", "llm-integration", "llamaindex", "qdrant"]),
    ("capstone-data-analyst", "Data Analyst Capstone", "المشروع الختامي: محلل بيانات", "career", "capstone", []),
    ("capstone-ml-engineer", "ML Engineer Capstone", "المشروع الختامي: مهندس تعلّم آلة", "career", "capstone", []),
    ("capstone-ai-developer", "AI Developer Capstone", "المشروع الختامي: مطوّر تطبيقات ذكاء اصطناعي",
     "career", "capstone", []),
    ("capstone-mlops-engineer", "MLOps Engineer Capstone", "المشروع الختامي: مهندس MLOps", "career", "capstone", []),
    ("capstone-ai-engineer", "AI Engineer Capstone", "المشروع الختامي: مهندس ذكاء اصطناعي",
     "career", "capstone", []),
]

STAGES.extend(
    (course["slug"], course["title"], course["title"], course["phase"], "learning", [course["slug"]])
    for course in COURSE_DIRECTORY_COURSES
)

# ─── Templates ──────────────────────────────────────────────────────────────
# One journey per career goal: an ordered list of (stage, field). A stage tied
# to a field appears only when that field is in the learner's route; `None`
# means every route. "AI Engineer - Computer Vision" is this template filtered
# to `computer-vision` - there is no separate list for it anywhere.
_AI_ENGINEER_STAGES: List[Tuple[str, Optional[str]]] = [
    ("foundations", None), ("machine-learning", None), ("deep-learning", None),
    ("nlp-llm", "nlp"), ("rag", "nlp"), ("agents", "nlp"), ("llm-production", "nlp"),
    ("computer-vision", "computer-vision"), ("advanced-cv", "computer-vision"),
    ("vision-language", "computer-vision"),
    ("audio-processing", "speech"), ("speech-recognition", "speech"), ("text-to-speech", "speech"),
    ("voice-ai", "speech"), ("realtime-voice-agents", "speech"),
    ("multimodal", "multimodal"),
    ("production", None), ("capstone-ai-engineer", None),
]

# (template slug, career goal, title, title_ar, [(stage, field)])
TEMPLATES: List[Tuple[str, str, str, str, List[Tuple[str, Optional[str]]]]] = [
    ("data-analyst-path", DATA_ANALYST, "Data Analyst path", "مسار محلل بيانات", [
        ("data-foundations", "data"), ("data-analysis", "data"), ("data-tooling", "data"),
        ("capstone-data-analyst", None),
    ]),
    ("ml-engineer-path", ML_ENGINEER, "ML Engineer path", "مسار مهندس تعلّم آلة", [
        ("machine-learning", None), ("feature-engineering", None), ("deep-learning", None),
        ("model-evaluation", None), ("nlp-transformers", "nlp"),
        ("computer-vision", "computer-vision"), ("advanced-cv", "computer-vision"),
        ("audio-processing", "speech"), ("speech-recognition", "speech"),
        ("mlops-tooling", None), ("production", None),
        ("llm-applications", "nlp"),
        ("capstone-ml-engineer", None),
    ]),
    ("ai-developer-path", AI_DEVELOPER, "AI Developer path", "مسار مطوّر تطبيقات ذكاء اصطناعي", [
        ("foundations", None), ("nlp-llm", "nlp"), ("rag", "nlp"), ("agents", "nlp"),
        ("llm-production", "nlp"), ("multimodal", "multimodal"), ("production", None),
        ("capstone-ai-developer", None),
    ]),
    ("mlops-engineer-path", MLOPS_ENGINEER, "MLOps Engineer path", "مسار مهندس MLOps", [
        ("machine-learning", None), ("mlops-tooling", None), ("production", None),
        ("capstone-mlops-engineer", None),
    ]),
    ("ai-engineer-path", AI_ENGINEER, "AI Engineer path", "مسار مهندس ذكاء اصطناعي", _AI_ENGINEER_STAGES),
]

_COURSE_STAGES_BY_GOAL = {
    _DA: {
        "data-foundations": [("course-013", "data")],
    },
    _ML: {
        "machine-learning": [("course-001", None), ("course-013", "data")],
        "deep-learning": [("course-002", None), ("course-003", None)],
        "nlp-transformers": [("course-004", "nlp")],
        "computer-vision": [("course-014", "computer-vision")],
    },
    _AID: {
        "foundations": [("course-001", None), ("course-002", None), ("course-003", None)],
        "nlp-llm": [("course-004", "nlp"), ("course-005", "nlp")],
        "llm-production": [
            ("course-006", "nlp"), ("course-007", "nlp"), ("course-009", "nlp"),
            ("course-010", "nlp"), ("course-011", "nlp"), ("course-012", "nlp"),
        ],
        "multimodal": [("course-008", "multimodal")],
    },
    _OPS: {
        "machine-learning": [("course-001", None), ("course-002", None)],
        "production": [("course-006", None), ("course-010", None), ("course-011", None)],
    },
    _AIE: {
        "machine-learning": [("course-001", None), ("course-013", "data")],
        "deep-learning": [("course-002", None), ("course-003", None)],
        "nlp-llm": [("course-004", "nlp"), ("course-005", "nlp")],
        "llm-production": [
            ("course-006", "nlp"), ("course-007", "nlp"), ("course-009", "nlp"),
            ("course-010", "nlp"), ("course-011", "nlp"), ("course-012", "nlp"),
        ],
        "computer-vision": [("course-014", "computer-vision")],
        "multimodal": [("course-008", "multimodal")],
    },
}


def _with_course_stages(goal: str, stages: List[Tuple[str, Optional[str]]]) -> List[Tuple[str, Optional[str]]]:
    """Insert canonical course stages immediately after their prerequisite stage."""
    result: List[Tuple[str, Optional[str]]] = []
    for stage in stages:
        result.append(stage)
        result.extend(_COURSE_STAGES_BY_GOAL[goal].get(stage[0], []))
    return result


TEMPLATES = [
    (slug, goal, title, title_ar, _with_course_stages(goal, stages))
    for slug, goal, title, title_ar, stages in TEMPLATES
]


# ─── Lookups (pure) ─────────────────────────────────────────────────────────

def roles_for(course_slug: str) -> List[Dict[str, str]]:
    """`[{"slug": goal, "relation": relation}]` in the goals' own order - the
    shape `catalog_admin.upsert_course(roles=...)` takes."""
    weights = COURSE_ROLES[course_slug]
    return [{"slug": goal, "relation": weights[goal]} for goal in GOALS if goal in weights]


def stage_courses(stage_slug: str) -> List[str]:
    return next(list(courses) for slug, _t, _a, _p, _k, courses in STAGES if slug == stage_slug)


def template_stages(goal: str) -> List[Tuple[str, Optional[str]]]:
    return next(list(stages) for _slug, g, _t, _a, stages in TEMPLATES if g == goal)


def template_courses(goal: str, fields: Optional[Sequence[str]] = None) -> List[str]:
    """Course slugs a goal's template lists, in path order. With `fields`, only the
    stages that route would show; without, every stage the template has."""
    routed = None if fields is None else set(fields)
    seen: List[str] = []
    for stage_slug, field in template_stages(goal):
        if routed is not None and field is not None and field not in routed:
            continue
        for course in stage_courses(stage_slug):
            if course not in seen:
                seen.append(course)
    return seen
