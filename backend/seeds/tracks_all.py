"""
Seeds all four specialisation tracks and the Full Stack AI Engineer apex track.
Run this instead of (or after) the basic track seed.
"""
from app.models.learning import CareerTrack, TrackLevel, Topic


TRACKS = [
    {
        "slug": "data-analyst",
        "title": "Data Analyst",
        "description": "Master data wrangling, visualisation, and statistical analysis. Build dashboards and derive business insights from raw data.",
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
        "description": "Build and train machine learning models. From supervised learning basics to deep neural networks with PyTorch.",
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
        "description": "Build production AI applications using LLMs, RAG systems, and modern AI APIs. From prompt engineering to full deployment.",
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
        "description": "Deploy, monitor, and maintain ML systems at scale. CI/CD for models, cloud infrastructure, and production reliability.",
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
        "description": "The complete path. Combines data analysis, ML engineering, AI development, and MLOps into a full production AI engineering skillset.",
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
            print(f"  ⚠  Track '{track_data['slug']}' already exists — skipping")
            continue

        track = CareerTrack(
            slug=track_data["slug"],
            title=track_data["title"],
            description=track_data["description"],
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