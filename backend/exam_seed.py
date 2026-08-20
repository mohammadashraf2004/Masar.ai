"""
exam_seed.py — seeds a full 16-question proctored certification exam
Run from backend/ directory:  python exam_seed.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.session import engine, Base, SessionLocal
from app.models.user import User
from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Exercise, Project, Quiz
from app.models.progress import (
    Enrollment, UserProgress, QuizAttempt,
    ProjectSubmission, MentorSession, UserSkillScore
)
from app.models.community import Post, PostLike, PostComment, UserFollow
from app.models.exam import Exam, ExamAttempt, ProctoringEvent, Certificate

Base.metadata.create_all(bind=engine)

QUESTIONS = [
    # ── 1. MCQ ────────────────────────────────────────────────────────────────
    {
        "question_type": "mcq",
        "question_text": "Which Python data structure preserves insertion order and allows O(1) key lookups?",
        "points": 5,
        "order_index": 1,
        "options": ["list", "set", "dict", "tuple"],
        "correct_answer": {"answer": "dict"},
        "explanation": "Since Python 3.7, dicts preserve insertion order and provide O(1) average-case lookups via hashing.",
        "tags": ["python", "data-structures"],
        "difficulty": "easy",
    },
    # ── 2. MCQ ────────────────────────────────────────────────────────────────
    {
        "question_type": "mcq",
        "question_text": "What is the time complexity of training a linear regression model using the Normal Equation on n samples with d features?",
        "points": 5,
        "order_index": 2,
        "options": ["O(n·d)", "O(d³ + n·d²)", "O(n²)", "O(n·log n)"],
        "correct_answer": {"answer": "O(d³ + n·d²)"},
        "explanation": "The Normal Equation requires computing (XᵀX)⁻¹Xᵀy. Matrix inversion is O(d³) and XᵀX multiplication is O(n·d²).",
        "tags": ["ml", "linear-algebra", "complexity"],
        "difficulty": "medium",
    },
    # ── 3. MCQ ────────────────────────────────────────────────────────────────
    {
        "question_type": "mcq",
        "question_text": "Which activation function is most commonly used in the hidden layers of modern deep neural networks due to its resistance to the vanishing gradient problem?",
        "points": 5,
        "order_index": 3,
        "options": ["Sigmoid", "Tanh", "ReLU", "Softmax"],
        "correct_answer": {"answer": "ReLU"},
        "explanation": "ReLU (Rectified Linear Unit) avoids vanishing gradients for positive inputs and is computationally cheap, making it the default choice in hidden layers.",
        "tags": ["deep-learning", "activations"],
        "difficulty": "easy",
    },
    # ── 4. TRUE/FALSE ─────────────────────────────────────────────────────────
    {
        "question_type": "true_false",
        "question_text": "Dropout regularization during inference should use the same dropout probability as during training.",
        "points": 3,
        "order_index": 4,
        "options": ["True", "False"],
        "correct_answer": {"answer": "False"},
        "explanation": "During inference, dropout is disabled (all neurons active) and weights are scaled by (1 - p) to compensate. Only training uses random dropout.",
        "tags": ["deep-learning", "regularization"],
        "difficulty": "medium",
    },
    # ── 5. TRUE/FALSE ─────────────────────────────────────────────────────────
    {
        "question_type": "true_false",
        "question_text": "Transformers process tokens sequentially, one at a time, making them inherently slower to train than RNNs on long sequences.",
        "points": 3,
        "order_index": 5,
        "options": ["True", "False"],
        "correct_answer": {"answer": "False"},
        "explanation": "Transformers process all tokens in parallel via self-attention, which is a key advantage over RNNs for training on long sequences.",
        "tags": ["nlp", "transformers"],
        "difficulty": "medium",
    },
    # ── 6. MULTI ──────────────────────────────────────────────────────────────
    {
        "question_type": "multi",
        "question_text": "Which of the following are valid strategies to combat overfitting in a neural network? (Select ALL that apply)",
        "points": 8,
        "order_index": 6,
        "options": ["Dropout", "Adding more layers", "L2 Regularization", "Early Stopping", "Increasing learning rate", "Data Augmentation"],
        "correct_answer": {"answers": ["Dropout", "L2 Regularization", "Early Stopping", "Data Augmentation"]},
        "explanation": "Dropout, L2 regularization, early stopping, and data augmentation all reduce overfitting. Adding more layers or increasing learning rate typically worsens overfitting.",
        "tags": ["deep-learning", "regularization"],
        "difficulty": "medium",
    },
    # ── 7. MULTI ──────────────────────────────────────────────────────────────
    {
        "question_type": "multi",
        "question_text": "Which of the following are components of the Transformer architecture introduced in 'Attention Is All You Need'? (Select ALL that apply)",
        "points": 8,
        "order_index": 7,
        "options": [
            "Multi-Head Self-Attention",
            "Convolutional layers",
            "Positional Encoding",
            "Feed-Forward sublayers",
            "Recurrent connections",
            "Layer Normalization",
        ],
        "correct_answer": {"answers": ["Multi-Head Self-Attention", "Positional Encoding", "Feed-Forward sublayers", "Layer Normalization"]},
        "explanation": "The original Transformer uses multi-head attention, positional encodings, position-wise feed-forward layers, and layer normalization. It has no CNNs or recurrent connections.",
        "tags": ["nlp", "transformers", "architecture"],
        "difficulty": "hard",
    },
    # ── 8. FILL IN THE BLANK ──────────────────────────────────────────────────
    {
        "question_type": "fill_blank",
        "question_text": "Complete the PyTorch code to compute binary cross-entropy loss for a batch of predictions:",
        "points": 8,
        "order_index": 8,
        "code_template": """import torch
import torch.nn as ___BLANK_1___

predictions = torch.tensor([0.9, 0.2, 0.8, 0.1])
targets = torch.tensor([1.0, 0.0, 1.0, 0.0])

criterion = nn.___BLANK_2___()
loss = criterion(___BLANK_3___, targets)
print(f"Loss: {loss.item():.4f}")""",
        "correct_answer": {"blanks": ["nn", "BCELoss", "predictions"]},
        "explanation": "torch.nn (imported as nn) provides BCELoss. The criterion takes predictions first, then targets.",
        "tags": ["pytorch", "loss-functions"],
        "difficulty": "medium",
    },
    # ── 9. FILL IN THE BLANK ──────────────────────────────────────────────────
    {
        "question_type": "fill_blank",
        "question_text": "Complete the scikit-learn pipeline that standardizes features then trains a logistic regression:",
        "points": 8,
        "order_index": 9,
        "code_template": """from sklearn.pipeline import ___BLANK_1___
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ('scaler', ___BLANK_2___()),
    ('clf', LogisticRegression(max_iter=___BLANK_3___))
])
pipe.fit(X_train, y_train)""",
        "correct_answer": {"blanks": ["Pipeline", "StandardScaler", "1000"]},
        "explanation": "Pipeline chains transformers and an estimator. StandardScaler normalizes features. max_iter=1000 avoids convergence warnings on most datasets.",
        "tags": ["sklearn", "pipelines"],
        "difficulty": "easy",
    },
    # ── 10. CODE ──────────────────────────────────────────────────────────────
    {
        "question_type": "code",
        "question_text": (
            "Write a Python function `cosine_similarity(a, b)` that computes the cosine similarity "
            "between two non-zero NumPy vectors without using sklearn. "
            "Return a float rounded to 4 decimal places."
        ),
        "points": 12,
        "order_index": 10,
        "starter_code": """import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    # Your implementation here
    pass

# Test
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
print(cosine_similarity(a, b))  # Expected: 0.9746
""",
        "correct_answer": {
            "keywords": ["dot", "norm", "np.linalg", "round"],
            "reference": """import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return round(float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))), 4)
""",
        },
        "language": "python",
        "explanation": "Cosine similarity = dot(a,b) / (||a|| × ||b||). np.dot and np.linalg.norm are the standard NumPy tools.",
        "tags": ["numpy", "linear-algebra", "nlp"],
        "difficulty": "medium",
    },
    # ── 11. CODE ──────────────────────────────────────────────────────────────
    {
        "question_type": "code",
        "question_text": (
            "Implement a PyTorch custom Dataset class called `TextDataset` that takes a list of "
            "(text, label) tuples and implements `__len__` and `__getitem__`. "
            "`__getitem__` should return a dict with keys 'text' (str) and 'label' (int)."
        ),
        "points": 12,
        "order_index": 11,
        "starter_code": """import torch
from torch.utils.data import Dataset

class TextDataset(Dataset):
    def __init__(self, data: list[tuple[str, int]]):
        # Your code here
        pass

    def __len__(self):
        # Your code here
        pass

    def __getitem__(self, idx: int):
        # Your code here
        pass

# Test
ds = TextDataset([("hello world", 1), ("foo bar", 0)])
print(len(ds))          # 2
print(ds[0])            # {'text': 'hello world', 'label': 1}
""",
        "correct_answer": {
            "keywords": ["self.data", "__len__", "__getitem__", "text", "label"],
            "reference": """class TextDataset(Dataset):
    def __init__(self, data):
        self.data = data
    def __len__(self):
        return len(self.data)
    def __getitem__(self, idx):
        text, label = self.data[idx]
        return {'text': text, 'label': int(label)}
""",
        },
        "language": "python",
        "explanation": "PyTorch Datasets must implement __len__ and __getitem__. Storing data as self.data then indexing it is the standard pattern.",
        "tags": ["pytorch", "datasets"],
        "difficulty": "medium",
    },
    # ── 12. ORDERING ──────────────────────────────────────────────────────────
    {
        "question_type": "ordering",
        "question_text": "Arrange the steps of a standard supervised ML pipeline in the correct order (drag to reorder):",
        "points": 8,
        "order_index": 12,
        "options": [
            "Define the problem & success metric",
            "Collect & label data",
            "Exploratory Data Analysis (EDA)",
            "Feature engineering & preprocessing",
            "Split into train / validation / test sets",
            "Select and train a baseline model",
            "Hyperparameter tuning",
            "Evaluate on the test set",
            "Deploy & monitor",
        ],
        "correct_answer": {
            "order": [
                "Define the problem & success metric",
                "Collect & label data",
                "Exploratory Data Analysis (EDA)",
                "Feature engineering & preprocessing",
                "Split into train / validation / test sets",
                "Select and train a baseline model",
                "Hyperparameter tuning",
                "Evaluate on the test set",
                "Deploy & monitor",
            ]
        },
        "explanation": "The standard ML workflow runs from problem definition through data collection, EDA, feature engineering, splitting, training, tuning, evaluation, and finally deployment.",
        "tags": ["ml-workflow", "best-practices"],
        "difficulty": "easy",
    },
    # ── 13. ORDERING ──────────────────────────────────────────────────────────
    {
        "question_type": "ordering",
        "question_text": "Order the steps of the Transformer's attention mechanism from input to output:",
        "points": 8,
        "order_index": 13,
        "options": [
            "Project input into Q, K, V matrices",
            "Compute raw attention scores: Q·Kᵀ",
            "Scale scores by 1/√d_k",
            "Apply softmax to get attention weights",
            "Multiply weights by V to get output",
            "Concatenate multi-heads and project",
        ],
        "correct_answer": {
            "order": [
                "Project input into Q, K, V matrices",
                "Compute raw attention scores: Q·Kᵀ",
                "Scale scores by 1/√d_k",
                "Apply softmax to get attention weights",
                "Multiply weights by V to get output",
                "Concatenate multi-heads and project",
            ]
        },
        "explanation": "Attention: (1) project to Q/K/V, (2) compute scores Q·Kᵀ, (3) scale by 1/√d_k, (4) softmax, (5) weight V, (6) concat and project for multi-head.",
        "tags": ["transformers", "attention"],
        "difficulty": "hard",
    },
    # ── 14. SHORT ANSWER ──────────────────────────────────────────────────────
    {
        "question_type": "short",
        "question_text": (
            "Explain the difference between batch normalization and layer normalization. "
            "When would you prefer layer normalization over batch normalization, and why?"
        ),
        "points": 10,
        "order_index": 14,
        "correct_answer": {
            "keywords": [
                "batch normalization", "layer normalization",
                "across samples", "across features",
                "small batch", "NLP", "transformer",
                "variable length", "RNN",
            ],
            "min_keywords": 4,
        },
        "explanation": "BatchNorm normalizes across the batch dimension (statistics depend on batch size); LayerNorm normalizes across the feature dimension (per-sample). LayerNorm is preferred for NLP/Transformers where batch sizes can be small or sequences are variable-length.",
        "tags": ["deep-learning", "normalization"],
        "difficulty": "hard",
    },
    # ── 15. SHORT ANSWER ──────────────────────────────────────────────────────
    {
        "question_type": "short",
        "question_text": (
            "What is the 'attention is all you need' insight? Describe in 2–3 sentences "
            "why self-attention is powerful for sequence modeling compared to recurrence."
        ),
        "points": 10,
        "order_index": 15,
        "correct_answer": {
            "keywords": [
                "self-attention", "parallel", "long-range", "dependencies",
                "O(1) path length", "recurrence", "sequential", "gradient",
                "constant", "distance",
            ],
            "min_keywords": 4,
        },
        "explanation": "Self-attention captures any-distance token relationships in O(1) operations (vs O(n) for RNNs), enables full parallelism during training, and avoids vanishing gradient over long sequences.",
        "tags": ["nlp", "transformers", "attention"],
        "difficulty": "hard",
    },
    # ── 16. MCQ ───────────────────────────────────────────────────────────────
    {
        "question_type": "mcq",
        "question_text": "In the context of large language models, what does 'RLHF' stand for and what problem does it primarily solve?",
        "points": 5,
        "order_index": 16,
        "options": [
            "Recursive Learning from Human Feedback — speeds up pretraining",
            "Reinforcement Learning from Human Feedback — aligns model outputs with human preferences",
            "Regularized Loss with Human Fine-tuning — reduces hallucinations via regularization",
            "Recurrent Layer with Hybrid Features — improves long-context understanding",
        ],
        "correct_answer": {"answer": "Reinforcement Learning from Human Feedback — aligns model outputs with human preferences"},
        "explanation": "RLHF trains a reward model on human preference rankings, then uses PPO (or similar RL) to fine-tune the LLM to maximize that reward, aligning outputs with human values and reducing harmful/unhelpful responses.",
        "tags": ["llm", "alignment", "rlhf"],
        "difficulty": "medium",
    },
]


def seed_exam():
    db = SessionLocal()
    try:
        # ── Find the AI Engineer track ────────────────────────────────────────
        track = db.query(CareerTrack).filter(
            CareerTrack.slug == "ai-engineer"
        ).first()

        if not track:
            # Fall back to the first available track
            track = db.query(CareerTrack).first()
            if not track:
                print("❌  No career tracks found. Run seed_tracks.py first.")
                return

        print(f"✅  Using track: {track.name} (id={track.id})")

        # ── Remove any existing exam for this track ───────────────────────────
        existing = db.query(Exam).filter(Exam.track_id == track.id).first()
        if existing:
            db.delete(existing)
            db.commit()
            print("🗑   Removed existing exam for this track.")

        # ── Create the exam ───────────────────────────────────────────────────
        total_points = sum(q["points"] for q in QUESTIONS)
        passing_score = int(total_points * 0.70)   # 70% to pass

        exam = Exam(
            track_id=track.id,
            title="AI Engineer Certification Exam",
            description=(
                "Prove your readiness to work as a professional AI Engineer. "
                "This proctored exam covers Python, ML theory, deep learning, "
                "NLP/Transformers, and practical coding. Webcam and fullscreen "
                "are required. You have 90 minutes and a maximum of 5 violations."
            ),
            duration_minutes=90,
            passing_score=passing_score,
            total_points=total_points,
            questions=QUESTIONS,
            is_active=True,
            max_attempts=3,
            proctoring_required=True,
        )
        db.add(exam)
        db.commit()
        db.refresh(exam)

        print(f"\n🎉  Exam seeded successfully!")
        print(f"    ID            : {exam.id}")
        print(f"    Title         : {exam.title}")
        print(f"    Questions     : {len(QUESTIONS)}")
        print(f"    Total points  : {total_points}")
        print(f"    Passing score : {passing_score} ({passing_score/total_points*100:.0f}%)")
        print(f"    Duration      : {exam.duration_minutes} min")
        print(f"\n    ➜  Visit http://localhost:3000/exam/{exam.id}")

    except Exception as e:
        db.rollback()
        print(f"❌  Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_exam()