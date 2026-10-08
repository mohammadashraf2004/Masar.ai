"""
Seeds the five career tracks: four role tracks and AI Engineer.

These are the curriculum containers. The learning *path* a learner follows is
built from their level, fields and career goal (see seed_learning_paths.py and
docs/learning/ARCHITECTURE.md) — AI Engineer is a career goal with several
specialization routes, not the unlock for completing the other tracks.
Run this instead of (or after) the basic track seed.
"""
from app.models.learning import CareerTrack, TrackLevel, Topic


TRACKS = [
    {
        "slug": "data-analyst",
        "title": "Data Analyst",
        "title_ar": "محلل بيانات",
        "description": "SQL, data cleaning, statistical analysis, and decision-ready dashboards.",
        "description_ar": "SQL، تنظيف البيانات، التحليل الإحصائي، ولوحات المؤشرات التي تُقنع أصحاب القرار.",
        "icon": "📊",
        "estimated_weeks": 12,
        "levels": [
            {"title": "Python & SQL foundations",   "skill_tags": ["python", "sql", "pandas"]},
            {"title": "Data analysis with Pandas",  "skill_tags": ["pandas", "numpy", "data-cleaning"]},
            {"title": "Data visualisation",         "skill_tags": ["matplotlib", "seaborn", "plotly"]},
            {"title": "Statistics for analysts",    "skill_tags": ["statistics", "hypothesis-testing"]},
            {"title": "BI dashboards & reporting",  "skill_tags": ["powerbi", "tableau", "reporting"]},
        ]
    },
    {
        "slug": "ml-engineer",
        "title": "ML Engineer",
        "title_ar": "مهندس تعلّم آلي",
        "description": "From feature engineering to training, evaluating, and serving models.",
        "description_ar": "من هندسة الخصائص إلى تدريب النماذج وتقييمها ونشرها كخدمة.",
        "icon": "🧠",
        "estimated_weeks": 16,
        "levels": [
            {"title": "ML fundamentals",            "skill_tags": ["scikit-learn", "supervised-learning"]},
            {"title": "Feature engineering",        "skill_tags": ["feature-engineering", "preprocessing"]},
            {"title": "Deep learning with PyTorch", "skill_tags": ["pytorch", "neural-networks", "cnn"]},
            {"title": "Model evaluation",           "skill_tags": ["evaluation", "metrics", "cross-validation"]},
            {"title": "Transformers & fine-tuning", "skill_tags": ["transformers", "huggingface", "fine-tuning"]},
        ]
    },
    {
        "slug": "ai-developer",
        "title": "AI Developer",
        "title_ar": "مطوّر ذكاء اصطناعي",
        "description": "Integrate LLMs into real products with APIs, prompts, tools, and chat interfaces.",
        "description_ar": "دمج LLMs في منتجات حقيقية: APIs، الـ prompts، الأدوات، وواجهات المحادثة.",
        "icon": "⚡",
        "estimated_weeks": 14,
        "levels": [
            {"title": "LLM integration",            "skill_tags": ["openai", "anthropic", "llm-api"]},
            {"title": "Prompt engineering",         "skill_tags": ["prompting", "chain-of-thought", "few-shot"]},
            {"title": "RAG systems",                "skill_tags": ["rag", "embeddings", "retrieval"]},
            {"title": "Vector databases",           "skill_tags": ["pgvector", "chromadb", "pinecone"]},
            {"title": "AI app deployment",          "skill_tags": ["fastapi", "deployment", "production"]},
        ]
    },
    {
        "slug": "mlops-engineer",
        "title": "MLOps Engineer",
        "title_ar": "مهندس MLOps",
        "description": "Model CI/CD, monitoring, version management, and reliable operation at scale.",
        "description_ar": "خطوط CI/CD للنماذج، المراقبة، إدارة الإصدارات، والتشغيل على نطاق واسع.",
        "icon": "🔧",
        "estimated_weeks": 10,
        "levels": [
            {"title": "Docker & containerisation",  "skill_tags": ["docker", "containers"]},
            {"title": "CI/CD for ML",               "skill_tags": ["github-actions", "cicd", "testing"]},
            {"title": "Cloud deployment",           "skill_tags": ["aws", "gcp", "cloud"]},
            {"title": "Model monitoring",           "skill_tags": ["monitoring", "drift-detection", "logging"]},
            {"title": "Experiment tracking",        "skill_tags": ["mlflow", "wandb", "experiments"]},
        ]
    },
    {
        "slug": "ai-engineer",
        "title": "AI Engineer",
        "title_ar": "مهندس ذكاء اصطناعي",
        "description": "RAG, stateful agents, evaluation, and deployment — the broadest route into AI Engineering.",
        "description_ar": "RAG، وكلاء بحالة مستمرة، التقييم، والنشر — المسار الأشمل لوظيفة AI Engineer.",
        "icon": "🤖",
        "estimated_weeks": 24,
        "levels": [
            {"title": "Advanced Python",            "skill_tags": ["python", "oop", "async"]},
            {"title": "Data & ML",                  "skill_tags": ["pandas", "scikit-learn", "ml"]},
            {"title": "Deep learning",              "skill_tags": ["pytorch", "cnn", "transformers"]},
            {"title": "NLP & LLMs",                 "skill_tags": ["nlp", "rag", "llm"]},
            {"title": "Production AI",              "skill_tags": ["docker", "mlops", "monitoring"]},
        ]
    },
]


def seed_all_tracks(db) -> None:
    from app.models.learning import CareerTrack

    for track_data in TRACKS:
        existing = db.query(CareerTrack).filter(CareerTrack.slug == track_data["slug"]).first()
        if existing:
            existing.title = track_data["title"]
            existing.title_ar = track_data["title_ar"]
            existing.description = track_data["description"]
            existing.description_ar = track_data["description_ar"]
            existing.icon = track_data["icon"]
            existing.estimated_weeks = track_data["estimated_weeks"]
            print(f"  ✓ Track '{track_data['slug']}' metadata updated")
            continue

        track = CareerTrack(
            slug=track_data["slug"],
            title=track_data["title"],
            title_ar=track_data["title_ar"],
            description=track_data["description"],
            description_ar=track_data["description_ar"],
            icon=track_data["icon"],
            estimated_weeks=track_data["estimated_weeks"],
        )
        db.add(track)
        db.flush()

        for i, level_data in enumerate(track_data["levels"]):
            level = TrackLevel(
                track_id=track.id,
                title=level_data["title"],
                description="",
                order=i + 1,
            )
            db.add(level)
            db.flush()

            topic = Topic(
                level_id=level.id,
                title=level_data["title"],
                slug=f"{track_data['slug']}-{level_data['title'].lower().replace(' ', '-').replace('&', 'and')}",
                description="",
                order=1,
                difficulty="intermediate",
                estimated_hours=8,
                prerequisite_ids=[],
                skill_tags=level_data["skill_tags"],
            )
            db.add(topic)

        print(f"  ✓ Track: {track_data['title']}")

    db.commit()
    print("\n✅ All tracks seeded.")
