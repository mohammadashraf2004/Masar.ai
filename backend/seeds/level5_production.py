from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Project


def seed_level5(db, track: CareerTrack):
    level = TrackLevel(
        track_id=track.id,
        title="Production AI",
        description="Docker, Cloud, Monitoring, MLOps basics",
        order=5,
    )
    db.add(level)
    db.flush()

    topic = Topic(
        level_id=level.id,
        title="MLOps Fundamentals",
        slug="mlops-fundamentals",
        description="Deploy, monitor, and maintain ML systems in production",
        order=1,
        difficulty="advanced",
        estimated_hours=15,
        prerequisite_ids=[],
        skill_tags=["mlops", "docker", "monitoring", "ci-cd", "cloud"],
    )
    db.add(topic)
    db.flush()

    db.add(Lesson(
        topic_id=topic.id,
        title="Dockerising ML Applications",
        order=1,
        estimated_minutes=25,
        has_code_examples=True,
        content="""## Docker for ML Applications

Docker ensures your model runs identically everywhere: local, staging, production.

### Dockerfile for ML API

```dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose for Full Stack

```yaml
version: "3.9"
services:
  api:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      DATABASE_URL: postgresql://postgres:pass@db:5432/mydb
    depends_on:
      db:
        condition: service_healthy

  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      retries: 5
```

### Key Rules
1. One process per container
2. Use `.dockerignore` (exclude venv, __pycache__, .env)
3. Never hardcode secrets — use environment variables
""",
    ))

    db.add(Project(
        topic_id=topic.id,
        title="End-to-End ML Pipeline",
        description=(
            "Build a complete ML pipeline: data ingestion → training → evaluation → "
            "API deployment → monitoring. Use a real dataset of your choice."
        ),
        difficulty="advanced",
        tech_stack=["Python", "FastAPI", "Docker", "PostgreSQL", "GitHub Actions", "Prometheus"],
        objectives=[
            "Automated data ingestion and preprocessing",
            "Model training with experiment tracking",
            "Automated evaluation and model comparison",
            "REST API deployment with Docker",
            "Basic monitoring: latency, prediction distribution",
            "CI/CD pipeline with GitHub Actions",
        ],
        rubric={
            "pipeline_completeness": 30,
            "model_quality": 20,
            "deployment": 20,
            "monitoring": 15,
            "ci_cd": 15,
        },
        estimated_hours=20,
    ))

    print(f"  ✓ Level 5: {level.title} — topic: {topic.title}")
