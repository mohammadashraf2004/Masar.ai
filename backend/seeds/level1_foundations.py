from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Exercise, Project, Quiz


def seed_level1(db, track: CareerTrack):
    level = TrackLevel(
        track_id=track.id,
        title="Foundations",
        description="Python, Git, Linux, APIs, SQL",
        order=1,
    )
    db.add(level)
    db.flush()

    topic = Topic(
        level_id=level.id,
        title="Python for AI",
        slug="python-for-ai",
        description="Master Python fundamentals with an AI engineering focus",
        order=1,
        difficulty="beginner",
        estimated_hours=10,
        prerequisite_ids=[],
        skill_tags=["python", "programming", "data-structures"],
    )
    db.add(topic)
    db.flush()

    db.add(Lesson(
        topic_id=topic.id,
        title="Python Data Structures",
        order=1,
        estimated_minutes=20,
        has_code_examples=True,
        content="""## Python Data Structures for AI

Understanding data structures is foundational to AI engineering.

### Lists & NumPy Arrays
Lists are flexible but slow for numerical computation. NumPy arrays are fast because they're stored contiguously in memory.

```python
import numpy as np

data = [1, 2, 3, 4, 5]          # Python list — slow for math
arr  = np.array([1, 2, 3, 4, 5]) # NumPy array — fast, vectorized
print(arr * 2)  # [2, 4, 6, 8, 10] — element-wise, no loop needed
```

### Dictionaries
Used everywhere: configs, API responses, model outputs.

```python
model_config = {"model": "gpt-4", "temperature": 0.7, "max_tokens": 1000}
```

### Key Takeaway
For AI work, always prefer vectorized operations over Python loops.
""",
    ))

    db.add(Exercise(
        topic_id=topic.id,
        title="Build a simple data pipeline",
        description=(
            "Write a Python function that takes a list of numbers, normalizes them to [0, 1], "
            "and returns a NumPy array. This is the most common pre-processing step before "
            "feeding data to any ML model."
        ),
        starter_code="""import numpy as np

def normalize(data: list) -> np.ndarray:
    # Your code here
    # Hint: (x - min) / (max - min)
    pass

print(normalize([10, 20, 30, 40, 50]))
# Expected: [0.   0.25 0.5  0.75 1.  ]
""",
        solution_code="""import numpy as np

def normalize(data: list) -> np.ndarray:
    arr = np.array(data, dtype=float)
    return (arr - arr.min()) / (arr.max() - arr.min())
""",
        difficulty="beginner",
        skill_tested=["python", "numpy", "normalization"],
    ))

    db.add(Quiz(
        topic_id=topic.id,
        title="Python Fundamentals Check",
        passing_score=70,
        questions=[
            {
                "question": "What is the output of: np.array([1,2,3]) * 2?",
                "options": ["[2, 4, 6]", "[1, 2, 3, 1, 2, 3]", "Error", "[6]"],
                "correct": 0,
                "explanation": "NumPy arrays support element-wise operations, so each element is multiplied by 2.",
            },
            {
                "question": "Why are NumPy arrays preferred over Python lists for ML?",
                "options": [
                    "They use less RAM always",
                    "They support vectorized C-optimized operations",
                    "They can hold more elements",
                    "Python lists don't support numbers",
                ],
                "correct": 1,
                "explanation": "NumPy operations are implemented in C and run in contiguous memory.",
            },
        ],
    ))

    db.add(Project(
        topic_id=topic.id,
        title="Data Analysis CLI Tool",
        description=(
            "Build a command-line tool that reads a CSV file, computes statistics "
            "(mean, std, min, max) per column, detects missing values, and outputs a clean summary report."
        ),
        difficulty="beginner",
        tech_stack=["Python", "Pandas", "argparse"],
        objectives=[
            "Read CSV files with error handling",
            "Compute descriptive statistics",
            "Detect and report missing values",
            "Format and print a clean report",
        ],
        rubric={
            "correct_statistics": 30,
            "handles_edge_cases": 20,
            "clean_code": 25,
            "error_handling": 15,
            "documentation": 10,
        },
        estimated_hours=4,
    ))

    print(f"  ✓ Level 1: {level.title} — topic: {topic.title}")
