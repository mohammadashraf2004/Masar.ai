from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Project


def seed_level3(db, track: CareerTrack):
    level = TrackLevel(
        track_id=track.id,
        title="Deep Learning",
        description="PyTorch, CNNs, Transformers, Fine-tuning",
        order=3,
    )
    db.add(level)
    db.flush()

    topic = Topic(
        level_id=level.id,
        title="PyTorch Fundamentals",
        slug="pytorch-fundamentals",
        description="Tensors, autograd, training loops, CNNs",
        order=1,
        difficulty="intermediate",
        estimated_hours=20,
        prerequisite_ids=[],
        skill_tags=["pytorch", "deep-learning", "tensors", "neural-networks"],
    )
    db.add(topic)
    db.flush()

    db.add(Lesson(
        topic_id=topic.id,
        title="Tensors & Autograd",
        order=1,
        estimated_minutes=30,
        has_code_examples=True,
        content="""## PyTorch Tensors & Autograd

Tensors are the fundamental data unit in PyTorch — like NumPy arrays but GPU-capable and differentiable.

### Creating Tensors

```python
import torch

x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
w = torch.randn(3, 4)              # random weights
b = torch.zeros(4)                  # bias initialised to zero

device = "cuda" if torch.cuda.is_available() else "cpu"
x = x.to(device)
```

### Autograd — Automatic Differentiation

```python
x = torch.tensor(3.0, requires_grad=True)
y = x ** 2 + 2 * x + 1            # y = x² + 2x + 1

y.backward()                        # compute dy/dx
print(x.grad)                       # tensor(8.) — dy/dx = 2x + 2 = 8 at x=3
```

### Training Loop Pattern

```python
for epoch in range(100):
    optimizer.zero_grad()            # 1. clear gradients
    output = model(X)                # 2. forward pass
    loss = criterion(output, y)      # 3. compute loss
    loss.backward()                  # 4. backprop
    optimizer.step()                 # 5. update weights
```

Memorise this pattern — every PyTorch training loop follows it.
""",
    ))

    db.add(Project(
        topic_id=topic.id,
        title="Brain Tumor MRI Classifier",
        description=(
            "Build a CNN that classifies brain MRI scans into 4 categories: "
            "glioma, meningioma, pituitary tumor, and no tumor. Deploy as a web app."
        ),
        difficulty="intermediate",
        tech_stack=["PyTorch", "torchvision", "FastAPI", "PIL", "matplotlib"],
        objectives=[
            "Load and preprocess MRI image dataset",
            "Build CNN architecture (Conv → Pool → FC)",
            "Train with data augmentation",
            "Achieve >85% validation accuracy",
            "Deploy with FastAPI image upload endpoint",
        ],
        rubric={
            "model_accuracy": 40,
            "architecture_design": 20,
            "training_quality": 15,
            "deployment": 15,
            "code_clarity": 10,
        },
        estimated_hours=12,
        starter_repo_url="https://github.com/SartajBhuvaji/Brain-Tumor-Classification-DataSet",
    ))

    print(f"  ✓ Level 3: {level.title} — topic: {topic.title}")
