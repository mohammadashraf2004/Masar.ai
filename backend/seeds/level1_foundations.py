"""
backend/seeds/level1_foundations.py

Seeds Level 1, Topic 1 of the AI Engineer track: Advanced Python Data Structures.

Usage:
    cd backend
    conda activate 2helny
    python seeds/level1_foundations.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.db.session import SessionLocal, engine, Base
from app.models.user import User
from app.models.learning import CareerTrack, TrackLevel, Topic, Lesson, Exercise, Project, Quiz, DifficultyLevel
from app.models.progress import Enrollment, UserProgress, QuizAttempt, ProjectSubmission, MentorSession, UserSkillScore, EngineerScorecard
from app.models.community import Post, PostLike, PostComment, UserFollow
from app.models.exam import Exam, ExamAttempt, ProctoringEvent, Certificate
from app.models.wallet import UserWallet, WalletTransaction, CreditPackage
from app.models.challenge import ChallengeProject, ChallengeAttempt, ExamPayment

Base.metadata.create_all(bind=engine)

LESSON_CONTENT = r"""## Advanced Python Data Structures for AI Engineers

As an AI engineer, you write code that processes millions of rows of transaction records from Paymob, ranks thousands of job listings from Wuzzuf, or manages real-time inference queues for a Vezeeta diagnostic model. The difference between a solution that crashes under load and one that scales cleanly often comes down to one decision made in five seconds: which data structure did you reach for?

This lesson covers the four workhorses that separate production-grade Python from tutorial Python: **dicts**, **sets**, **deques**, and **heaps**. We'll look at how they work internally, when to use each, and how they show up in real AI engineering tasks.

---

### 1. Dictionaries — Beyond Basic Key-Value

You already know dicts. But do you know `defaultdict`, `Counter`, and the internal mechanics that make them O(1)?

#### How Python dicts actually work

Python dicts are hash tables. When you write `d["key"]`, Python computes `hash("key")`, finds the bucket, and retrieves the value — all in amortized O(1) time. This holds whether the dict has 10 entries or 10 million.

```python
# Standard dict — good
token_counts = {}
for token in corpus:
    if token not in token_counts:
        token_counts[token] = 0
    token_counts[token] += 1

# Better: defaultdict removes the existence check
from collections import defaultdict

token_counts = defaultdict(int)
for token in corpus:
    token_counts[token] += 1

# Best for counting: Counter does all of this for you
from collections import Counter

token_counts = Counter(corpus)
print(token_counts.most_common(10))  # top 10 tokens
```

#### Counter in AI pipelines

`Counter` is surprisingly powerful in NLP preprocessing. Here's a realistic Arabic tokenization example from a Noon product review pipeline:

```python
from collections import Counter
import re

reviews = [
    "المنتج ممتاز جداً وسعره مناسب",
    "جودة عالية والتوصيل كان سريع",
    "المنتج ممتاز لكن التوصيل تأخر",
]

def tokenize_arabic(text):
    # Remove punctuation, split on whitespace
    return re.findall(r'\b\w+\b', text)

all_tokens = []
for review in reviews:
    all_tokens.extend(tokenize_arabic(review))

vocab = Counter(all_tokens)
print(vocab.most_common(5))
# [('المنتج', 2), ('ممتاز', 2), ('التوصيل', 2), ...]

# Vocabulary size check — critical before tokenizer training
print(f"Unique tokens: {len(vocab)}")
```

#### Nested defaultdict for multi-level structures

```python
# Track model performance per category per language
from collections import defaultdict

metrics = defaultdict(lambda: defaultdict(list))

metrics["sentiment"]["arabic"].append(0.87)
metrics["sentiment"]["english"].append(0.91)
metrics["ner"]["arabic"].append(0.73)

# No KeyError, ever
print(metrics["ner"]["arabic"])  # [0.73]
```

---

### 2. Sets — The Underused Power Tool

Sets are hash tables storing only keys (no values). Operations like `in`, `add`, and `remove` are O(1). Set algebra (`union`, `intersection`, `difference`) is O(min(len(a), len(b))).

#### When sets beat lists

```python
# Deduplicating a list of seen document IDs — O(n) with set, O(n²) with list
seen_ids = set()
unique_docs = []

for doc in document_stream:
    if doc["id"] not in seen_ids:
        seen_ids.add(doc["id"])
        unique_docs.append(doc)
```

#### Set algebra for data pipeline validation

```python
expected_columns = {"user_id", "age", "governorate", "income_bracket", "churn"}
actual_columns   = set(df.columns)

missing  = expected_columns - actual_columns
extra    = actual_columns - expected_columns
overlap  = expected_columns & actual_columns

if missing:
    raise ValueError(f"Pipeline missing required columns: {missing}")
if extra:
    print(f"Warning: unexpected columns will be dropped: {extra}")
```

#### frozenset as a dict key

Regular sets are mutable and can't be used as dict keys. `frozenset` is immutable and hashable:

```python
# Cache results for a feature combination
feature_cache = {}

def compute_expensive_features(feature_names):
    ...  # assume this function exists — e.g. calls a feature store API

def get_features(feature_names):
    key = frozenset(feature_names)
    if key not in feature_cache:
        feature_cache[key] = compute_expensive_features(feature_names)
    return feature_cache[key]
```

---

### 3. Deques — Fast Queues for Streaming Pipelines

A `deque` (double-ended queue) from `collections` supports O(1) `appendleft`, `append`, `popleft`, and `pop`. A regular list is O(n) for left-side operations because every element shifts.

```python
from collections import deque

# Sliding window — a pattern you'll use constantly in time-series AI
def rolling_average(stream, window_size=5):
    window = deque(maxlen=window_size)  # auto-evicts oldest
    for value in stream:
        window.append(value)
        if len(window) == window_size:
            yield sum(window) / window_size

# Real-time transaction fraud signal from Paymob data
transaction_amounts = [120, 85, 200, 95, 110, 5000, 90, 100]
for avg in rolling_average(transaction_amounts):
    print(f"{avg:.1f}")
```

#### BFS with deque

Deques are the correct structure for breadth-first search — relevant when traversing knowledge graphs or dependency trees:

```python
from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()  # O(1) — never use list.pop(0)
        if node not in visited:
            visited.add(node)
            order.append(node)
            queue.extend(graph.get(node, []))

    return order
```

---

### 4. Heaps — Priority Queues Without the Boilerplate

Python's `heapq` module implements a **min-heap**: the smallest element is always at index 0, retrievable in O(1). Push and pop are O(log n).

```python
import heapq

# Always import heapq — there's no Heap class, just functions on a list
scores = []
heapq.heappush(scores, (0.92, "model_v3"))
heapq.heappush(scores, (0.87, "model_v1"))
heapq.heappush(scores, (0.95, "model_v2"))

best = heapq.heappop(scores)  # (0.87, 'model_v1') — smallest first
```

#### Max-heap pattern (negate the value)

```python
# Track top-k most similar documents (higher similarity = better)
import heapq
from sklearn.metrics.pairwise import cosine_similarity

def top_k_similar(query_embedding, doc_embeddings, k=5):
    heap = []
    for doc_id, emb in doc_embeddings.items():
        sim = cosine_similarity(query_embedding, emb)
        # Negate similarity to turn min-heap into max-heap
        heapq.heappush(heap, (-sim, doc_id))

    return [heapq.heappop(heap) for _ in range(min(k, len(heap)))]
```

#### nlargest / nsmallest — convenience wrappers

```python
import heapq

model_results = [
    {"model": "arabic-bert", "f1": 0.83},
    {"model": "camelbert",   "f1": 0.89},
    {"model": "arabert",     "f1": 0.86},
    {"model": "marbert",     "f1": 0.91},
]

top_2 = heapq.nlargest(2, model_results, key=lambda x: x["f1"])
# [{'model': 'marbert', 'f1': 0.91}, {'model': 'camelbert', 'f1': 0.89}]
```

---

### Choosing the Right Structure

| Task | Use |
|------|-----|
| Counting tokens, labels, categories | `Counter` |
| Grouping without KeyError | `defaultdict` |
| Membership test (is this ID seen?) | `set` |
| Deduplication | `set` |
| FIFO queue, sliding window | `deque` |
| Priority queue, top-k | `heapq` |
| Ordered insertion + fast lookup | `dict` (Python 3.7+ preserves order) |

---

> **Ready to practice?** Try Exercise 1 — *Token Frequency Analyzer for Arabic Reviews* — to apply Counter and set operations on a real Noon.com review corpus.

---

## Key Takeaways

- **Dict lookups are O(1)** because of hash tables — use `defaultdict` and `Counter` to eliminate boilerplate around counting and grouping.
- **Sets** give you O(1) membership testing and powerful set algebra; use them for deduplication, column validation, and vocabulary operations.
- **Deques** replace lists when you need to append or pop from both ends efficiently — especially for sliding windows and BFS.
- **Heaps** are the right tool for priority queues and top-k queries; remember that Python's `heapq` is a min-heap, so negate values for max-heap behavior.
- In production AI systems, the wrong data structure inside a hot loop can turn a 2-second inference pipeline into a 20-minute one — always think about complexity before you type.
"""

EXERCISES = [
    {
        "title": "Token Frequency Analyzer for Arabic Reviews",
        "difficulty": DifficultyLevel.intermediate,
        "description": "You're building a preprocessing module for a sentiment analysis pipeline on Noon.com product reviews (Arabic + English mixed). Write a function `analyze_corpus(reviews)` that takes a list of review strings and returns a dict with:\n- `top_tokens`: list of (token, count) tuples for the 10 most common tokens\n- `unique_count`: total number of unique tokens\n- `hapax_legomena`: list of tokens that appear exactly once (rare words — important for vocabulary pruning)\n\nUse Counter and set operations. Do not use any for-loop to count (use Counter directly).",
        "starter_code": "from collections import Counter\nimport re\n\ndef tokenize(text: str) -> list[str]:\n    \"\"\"Lowercase and extract word tokens (handles Arabic + Latin).\"\"\"\n    return re.findall(r'\\b\\w+\\b', text.lower())\n\ndef analyze_corpus(reviews: list[str]) -> dict:\n    \"\"\"\n    Args:\n        reviews: list of review strings (Arabic/English mixed)\n    Returns:\n        dict with keys: top_tokens, unique_count, hapax_legomena\n    \"\"\"\n    # YOUR CODE HERE\n    pass\n\n\n# Test\nif __name__ == \"__main__\":\n    sample_reviews = [\n        \"المنتج ممتاز جداً وسعره مناسب للجميع\",\n        \"جودة عالية والتوصيل كان سريع جداً\",\n        \"المنتج ممتاز لكن التوصيل تأخر كثيراً\",\n        \"great product fast delivery love it\",\n        \"product quality is great but expensive\",\n    ]\n    result = analyze_corpus(sample_reviews)\n    print(\"Top tokens:\", result[\"top_tokens\"])\n    print(\"Unique count:\", result[\"unique_count\"])\n    print(\"Hapax legomena:\", result[\"hapax_legomena\"])\n",
        "solution_code": "from collections import Counter\nimport re\n\ndef tokenize(text: str) -> list[str]:\n    return re.findall(r'\\b\\w+\\b', text.lower())\n\ndef analyze_corpus(reviews: list[str]) -> dict:\n    all_tokens = []\n    for review in reviews:\n        all_tokens.extend(tokenize(review))\n\n    counts = Counter(all_tokens)\n\n    return {\n        \"top_tokens\": counts.most_common(10),\n        \"unique_count\": len(counts),\n        \"hapax_legomena\": [token for token, count in counts.items() if count == 1],\n    }\n",
        "skill_tested": ["python", "collections", "counter", "nlp-preprocessing"],
    },
    {
        "title": "Sliding Window Anomaly Detector",
        "difficulty": DifficultyLevel.intermediate,
        "description": "You're building a real-time fraud signal layer for Paymob's transaction stream. Write a generator function `flag_anomalies(transactions, window=10, threshold=3.0)` that:\n1. Maintains a sliding window of the last `window` transaction amounts using a deque\n2. For each new transaction, computes the window mean and std\n3. Yields a dict `{\"amount\": ..., \"z_score\": ..., \"flagged\": bool}` where `flagged=True` if the z-score exceeds `threshold`\n4. Yields nothing (skips) until the window is full\n\nDo not import numpy — use only math and collections.",
        "starter_code": "from collections import deque\nimport math\n\ndef flag_anomalies(transactions: list[float], window: int = 10, threshold: float = 3.0):\n    \"\"\"\n    Generator that flags anomalous transactions using a sliding z-score window.\n\n    Args:\n        transactions: list of transaction amounts (EGP)\n        window: sliding window size\n        threshold: z-score above which a transaction is flagged\n\n    Yields:\n        dict with keys: amount, z_score, flagged\n    \"\"\"\n    # YOUR CODE HERE\n    pass\n\n\n# Test\nif __name__ == \"__main__\":\n    import random\n    random.seed(42)\n    amounts = [random.uniform(50, 500) for _ in range(20)]\n    amounts[15] = 9999.0  # inject an anomaly\n\n    for result in flag_anomalies(amounts, window=10, threshold=2.5):\n        status = \"FLAGGED\" if result[\"flagged\"] else \"OK\"\n        print(f\"Amount: {result['amount']:8.2f} EGP | z={result['z_score']:.2f} | {status}\")\n",
        "solution_code": "from collections import deque\nimport math\n\ndef flag_anomalies(transactions: list[float], window: int = 10, threshold: float = 3.0):\n    buf = deque(maxlen=window)\n\n    for amount in transactions:\n        buf.append(amount)\n\n        if len(buf) < window:\n            continue  # not enough data yet\n\n        mean = sum(buf) / len(buf)\n        variance = sum((x - mean) ** 2 for x in buf) / len(buf)\n        std = math.sqrt(variance) if variance > 0 else 1e-9\n\n        z_score = abs(amount - mean) / std\n\n        yield {\n            \"amount\": amount,\n            \"z_score\": round(z_score, 4),\n            \"flagged\": z_score > threshold,\n        }\n",
        "skill_tested": ["python", "deque", "streaming-data", "anomaly-detection"],
    },
    {
        "title": "Top-K Model Ranker with Heap",
        "difficulty": DifficultyLevel.advanced,
        "description": "You're running an AutoML experiment for Instabug's crash classification system. Each experiment produces a dict with model name, F1 score, latency (ms), and memory usage (MB). Write a class `ModelLeaderboard` that:\n1. Accepts new experiment results via `.add(result_dict)`\n2. Maintains an internal min-heap\n3. Exposes `.top_k(k, metric='f1')` that returns the k best models sorted by the given metric (higher is better for f1, lower is better for latency and memory)\n4. Exposes `.worst_k(k, metric='f1')` that returns the k worst models\n5. Stores at most `max_size` results (evict the worst by f1 when full)\n\nDo not sort the full list on every call — use heapq operations.",
        "starter_code": "import heapq\nfrom typing import Literal\n\nclass ModelLeaderboard:\n    \"\"\"\n    Efficient leaderboard for ML experiment results using a heap.\n    \"\"\"\n\n    def __init__(self, max_size: int = 100):\n        self.max_size = max_size\n        self._heap = []  # min-heap by f1\n        self._counter = 0  # tiebreaker\n\n    def add(self, result: dict) -> None:\n        \"\"\"\n        Add an experiment result.\n        result must have keys: model_name, f1, latency_ms, memory_mb\n        \"\"\"\n        # YOUR CODE HERE\n        pass\n\n    def top_k(self, k: int, metric: Literal['f1', 'latency_ms', 'memory_mb'] = 'f1') -> list[dict]:\n        \"\"\"\n        Return the k best models by metric.\n        Higher is better for f1; lower is better for latency_ms and memory_mb.\n        \"\"\"\n        # YOUR CODE HERE\n        pass\n\n    def worst_k(self, k: int, metric: Literal['f1', 'latency_ms', 'memory_mb'] = 'f1') -> list[dict]:\n        \"\"\"\n        Return the k worst models by metric.\n        \"\"\"\n        # YOUR CODE HERE\n        pass\n\n\n# Test\nif __name__ == \"__main__\":\n    lb = ModelLeaderboard(max_size=5)\n\n    experiments = [\n        {\"model_name\": \"arabic-bert-base\",  \"f1\": 0.83, \"latency_ms\": 45,  \"memory_mb\": 420},\n        {\"model_name\": \"camelbert-msa\",     \"f1\": 0.89, \"latency_ms\": 52,  \"memory_mb\": 510},\n        {\"model_name\": \"arabert-v2\",        \"f1\": 0.86, \"latency_ms\": 38,  \"memory_mb\": 390},\n        {\"model_name\": \"marbert\",           \"f1\": 0.91, \"latency_ms\": 60,  \"memory_mb\": 550},\n        {\"model_name\": \"distilbert-arabic\", \"f1\": 0.79, \"latency_ms\": 22,  \"memory_mb\": 260},\n        {\"model_name\": \"xlm-roberta\",       \"f1\": 0.93, \"latency_ms\": 88,  \"memory_mb\": 720},\n    ]\n\n    for exp in experiments:\n        lb.add(exp)\n\n    print(\"Top 3 by F1:\",        lb.top_k(3, 'f1'))\n    print(\"Top 3 by latency:\",   lb.top_k(3, 'latency_ms'))\n    print(\"Worst 2 by memory:\",  lb.worst_k(2, 'memory_mb'))\n",
        "solution_code": "import heapq\nfrom typing import Literal\n\nclass ModelLeaderboard:\n    def __init__(self, max_size: int = 100):\n        self.max_size = max_size\n        self._heap = []  # (f1, counter, result_dict) — min-heap by f1\n        self._counter = 0\n\n    def add(self, result: dict) -> None:\n        entry = (result['f1'], self._counter, result)\n        self._counter += 1\n\n        if len(self._heap) < self.max_size:\n            heapq.heappush(self._heap, entry)\n        else:\n            if result['f1'] > self._heap[0][0]:\n                heapq.heapreplace(self._heap, entry)\n\n    def _all_results(self) -> list[dict]:\n        return [entry[2] for entry in self._heap]\n\n    def top_k(self, k: int, metric: Literal['f1', 'latency_ms', 'memory_mb'] = 'f1') -> list[dict]:\n        reverse = metric == 'f1'\n        return heapq.nlargest(k, self._all_results(), key=lambda x: x[metric]) if reverse \\\n               else heapq.nsmallest(k, self._all_results(), key=lambda x: x[metric])\n\n    def worst_k(self, k: int, metric: Literal['f1', 'latency_ms', 'memory_mb'] = 'f1') -> list[dict]:\n        reverse = metric == 'f1'\n        return heapq.nsmallest(k, self._all_results(), key=lambda x: x[metric]) if reverse \\\n               else heapq.nlargest(k, self._all_results(), key=lambda x: x[metric])\n",
        "skill_tested": ["python", "heapq", "data-structures", "mlops"],
    },
]

QUIZ_QUESTIONS = [
    {
        "question": "What is the average-case time complexity of looking up a key in a Python dictionary?",
        "options": ["O(n)", "O(log n)", "O(1)", "O(n log n)"],
        "correct": 2,
        "explanation": "Python dicts are implemented as hash tables. A hash function maps the key to a bucket index in O(1), so lookup, insertion, and deletion are all O(1) on average. Worst case (many hash collisions) degrades to O(n), but Python's hash function is designed to make this extremely rare."
    },
    {
        "question": "Which collection is the most efficient for checking whether a user ID has already been processed in a deduplication pipeline?",
        "options": ["list", "tuple", "set", "dict with None values"],
        "correct": 2,
        "explanation": "set membership testing (x in my_set) is O(1) because sets are hash tables storing only keys. list membership testing (x in my_list) is O(n) because it scans every element. A dict with None values would also be O(1), but set is the idiomatic and more memory-efficient choice."
    },
    {
        "question": "You need to append items to both ends of a sequence and pop from both ends — frequently, inside a hot loop. Which structure should you use?",
        "options": ["list", "deque", "heap", "array"],
        "correct": 1,
        "explanation": "deque (collections.deque) supports O(1) append/pop from both ends. list.insert(0, x) and list.pop(0) are O(n) because every element must shift. For a sliding window or FIFO/LIFO queue, deque is always the correct choice."
    },
    {
        "question": "What does collections.Counter('abracadabra').most_common(2) actually return in CPython?",
        "options": [
            "[('a', 1), ('b', 1)]",
            "[('a', 5), ('b', 2)]",
            "[('r', 2), ('c', 1)]",
            "[('a', 5), ('r', 2)]"
        ],
        "correct": 1,
        "explanation": "In 'abracadabra': a=5, b=2, r=2, c=1, d=1. Counter preserves first-insertion order for ties (Python 3.7+ dict ordering). 'b' first appears at index 1, 'r' first appears at index 2, so among the count-2 items 'b' sorts before 'r'. most_common(2) returns [('a', 5), ('b', 2)]."
    },
    {
        "question": "Python's heapq module implements which type of heap?",
        "options": [
            "Max-heap — largest element at index 0",
            "Min-heap — smallest element at index 0",
            "Balanced BST",
            "Fibonacci heap"
        ],
        "correct": 1,
        "explanation": "heapq always implements a min-heap: heap[0] is always the smallest element. To simulate a max-heap, the standard pattern is to negate values: push -value and negate again on pop. There is no built-in max-heap in Python's standard library."
    },
    {
        "question": "You want to use a set as a dictionary key to cache results for a combination of features. What do you need to do?",
        "options": [
            "Nothing — sets are hashable by default",
            "Convert the set to a list first",
            "Convert the set to a frozenset",
            "Use a tuple of sorted set elements"
        ],
        "correct": 2,
        "explanation": "Regular sets are mutable and therefore unhashable — they cannot be used as dict keys or added to other sets. frozenset is the immutable, hashable counterpart. Both tuple and frozenset work as dict keys, but frozenset is the semantically correct choice when the order of features doesn't matter."
    },
    {
        "question": "What is the output of this code?\n\nfrom collections import defaultdict\nd = defaultdict(list)\nd['key'].append(1)\nd['key'].append(2)\nprint(d['missing'])",
        "options": [
            "KeyError: 'missing'",
            "None",
            "[]",
            "0"
        ],
        "correct": 2,
        "explanation": "defaultdict(list) uses list as its factory function. Accessing a missing key automatically calls list() to create an empty list and assigns it — no KeyError is raised. So d['missing'] returns [] and also inserts that empty list into d. This is the key behavior that makes defaultdict useful for grouping."
    },
    {
        "question": "In a streaming AI pipeline, you want to compute the rolling average of the last 20 inference latency measurements. Which is the most efficient implementation?",
        "options": [
            "Append to a list and slice [-20:] each iteration",
            "Use a deque with maxlen=20",
            "Use a heap of size 20",
            "Use a Counter and divide by count"
        ],
        "correct": 1,
        "explanation": "deque(maxlen=20) automatically evicts the oldest element when the window is full, making append O(1). The list slice approach works but creates a new list object on every iteration (O(window_size) memory allocation) and the slice itself is O(k). deque is the idiomatic and efficient solution for sliding windows."
    }
]

PROJECT = {
    "title": "Instabug Crash Report Deduplicator & Prioritizer",
    "description": "Instabug collects millions of crash reports from mobile apps across Egypt and the MENA region. Your task is to build a crash report processing pipeline in pure Python (no pandas, no numpy) that deduplicates reports, groups them by crash signature, and surfaces the most critical issues using a priority queue.\n\nYou are given a list of crash report dicts from crash_reports.json (provided). Each report has the following structure:\n\n{\n  \"report_id\": \"CR-00412\",\n  \"app_name\": \"Breadfast\",\n  \"crash_signature\": \"NullPointerException:CartFragment.java:88\",\n  \"severity\": \"critical\",\n  \"affected_users\": 1240,\n  \"country\": \"EG\",\n  \"timestamp\": \"2024-11-03T14:22:00Z\"\n}\n\nYour pipeline must produce a final report showing the top 5 most impactful crash groups.",
    "difficulty": DifficultyLevel.intermediate,
    "tech_stack": ["Python", "pytest", "heapq", "collections"],
    "objectives": [
        "Load crash_reports.json and deserialize into a list of dicts.",
        "Deduplicate reports by report_id using a set — log how many duplicates were removed.",
        "Group unique reports by crash_signature using a defaultdict(list).",
        "For each crash group, compute: total_affected_users (sum), report_count (len), severity_score (critical=3, high=2, medium=1, low=0), and a composite priority_score = total_affected_users * severity_score.",
        "Use a min-heap to maintain the top 5 crash groups by priority_score without sorting the full list.",
        "Output the top 5 groups as a formatted report to stdout, showing rank, signature, priority_score, total affected users, and report count.",
        "Write at least 3 unit tests using pytest covering: deduplication logic, grouping correctness, and heap ordering.",
    ],
    "rubric": {
        "Correct use of set for O(1) deduplication": 15,
        "Correct use of defaultdict(list) for grouping": 15,
        "Heap operations used for top-5 selection (not sorted())": 20,
        "Priority score formula applied correctly": 20,
        "Readable output with all required fields": 15,
        "Meaningful pytest tests (not just smoke tests)": 15,
    },
    "estimated_hours": 5.0,
}


def seed_topic(db, track_id: int = None):
    """Seeds Level 1 / Topic 1 for the AI Engineer track."""

    if track_id is None:
        track = db.query(CareerTrack).filter(CareerTrack.slug == "ai-engineer").first()
        if not track:
            print("AI Engineer track not found. Run seed_tracks.py first.")
            return
        track_id = track.id

    # ── Level ──────────────────────────────────────────────────────────────
    level = db.query(TrackLevel).filter(
        TrackLevel.track_id == track_id,
        TrackLevel.order == 1,
    ).first()
    if not level:
        level = TrackLevel(
            track_id=track_id,
            title="Level 1: Advanced Python & Software Engineering",
            description="Production-grade Python skills for AI engineering: data structures, async, testing, and design patterns.",
            order=1,
        )
        db.add(level)
        db.flush()

    # ── Topic ──────────────────────────────────────────────────────────────
    topic = db.query(Topic).filter(
        Topic.level_id == level.id,
        Topic.order == 1,
    ).first()
    if not topic:
        topic = Topic(
            level_id=level.id,
            title="Advanced Python Data Structures",
            slug="advanced-python-data-structures",
            description="Master dicts, sets, deques, and heaps for production AI pipelines.",
            order=1,
            difficulty=DifficultyLevel.intermediate,
            estimated_hours=3.0,
            prerequisite_ids=[],
            skill_tags=["python", "data-structures", "collections", "heapq"],
        )
        db.add(topic)
        db.flush()

    # ── Lesson ─────────────────────────────────────────────────────────────
    existing_lesson = db.query(Lesson).filter(Lesson.topic_id == topic.id).first()
    if not existing_lesson:
        db.add(Lesson(
            topic_id=topic.id,
            title="Advanced Python Data Structures for AI Engineers",
            content=LESSON_CONTENT,
            order=1,
            estimated_minutes=50,
            has_code_examples=True,
        ))

    # ── Exercises ──────────────────────────────────────────────────────────
    existing_exercises = db.query(Exercise).filter(Exercise.topic_id == topic.id).count()
    if existing_exercises == 0:
        for ex in EXERCISES:
            db.add(Exercise(topic_id=topic.id, **ex))

    # ── Quiz ───────────────────────────────────────────────────────────────
    existing_quiz = db.query(Quiz).filter(Quiz.topic_id == topic.id).first()
    if not existing_quiz:
        db.add(Quiz(
            topic_id=topic.id,
            title="Advanced Python Data Structures — Knowledge Check",
            questions=QUIZ_QUESTIONS,
            passing_score=70,
        ))

    # ── Project ────────────────────────────────────────────────────────────
    existing_project = db.query(Project).filter(Project.topic_id == topic.id).first()
    if not existing_project:
        db.add(Project(topic_id=topic.id, **PROJECT))

    db.commit()
    print(f"Seeded Level 1 / Topic 1 — '{topic.title}' (topic_id={topic.id})")
    print(f"  Lesson: 1 | Exercises: {len(EXERCISES)} | Quiz: {len(QUIZ_QUESTIONS)} questions | Project: 1")


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_topic(db)
    finally:
        db.close()