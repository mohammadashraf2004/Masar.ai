from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Project


def seed_level2(db, track: CareerTrack):
    level = TrackLevel(
        track_id=track.id,
        title="Data & ML",
        description="NumPy, Pandas, ML basics, evaluation metrics",
        order=2,
    )
    db.add(level)
    db.flush()

    topic = Topic(
        level_id=level.id,
        title="Machine Learning Fundamentals",
        slug="ml-fundamentals",
        description="Core ML concepts: supervised learning, model evaluation, overfitting",
        order=1,
        difficulty="intermediate",
        estimated_hours=15,
        prerequisite_ids=[],   # filled dynamically when IDs are known
        skill_tags=["machine-learning", "scikit-learn", "model-evaluation"],
    )
    db.add(topic)
    db.flush()

    db.add(Lesson(
        topic_id=topic.id,
        title="Supervised Learning & Evaluation",
        order=1,
        estimated_minutes=25,
        has_code_examples=True,
        content="""## Supervised Learning

In supervised learning, you train a model on labeled examples (input → output pairs).

### The ML Pipeline

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
```

### The Overfitting Trap
99% training accuracy, 60% test accuracy = memorised instead of learned.

**Solutions**: more data, regularisation, simpler model.

### Key Metrics
- **Accuracy** — % correct (misleading with imbalanced classes)
- **Precision** — of predicted positives, how many are truly positive?
- **Recall** — of actual positives, how many did we find?
- **F1** — harmonic mean of precision and recall
""",
    ))

    db.add(Project(
        topic_id=topic.id,
        title="Spam Email Classifier",
        description=(
            "Build and deploy a spam email classifier. Train on the SpamAssassin dataset, "
            "evaluate properly, and expose it as a FastAPI endpoint."
        ),
        difficulty="intermediate",
        tech_stack=["Python", "Scikit-learn", "FastAPI", "Pandas"],
        objectives=[
            "Preprocess and vectorise email text (TF-IDF)",
            "Train at least 2 models and compare metrics",
            "Achieve >95% F1 on test set",
            "Expose prediction via FastAPI POST endpoint",
            "Write a clear README with results",
        ],
        rubric={
            "model_performance": 35,
            "code_quality": 25,
            "api_implementation": 20,
            "documentation": 10,
            "error_handling": 10,
        },
        estimated_hours=8,
    ))

    print(f"  ✓ Level 2: {level.title} — topic: {topic.title}")
