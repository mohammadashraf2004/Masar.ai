"""
backend/seeds/levels/ai_developer/level_10_ai_evaluation_observability.py

Level 10 of the "AI Developer" career track: AI Evaluation & Observability.

Standalone LEVEL dict, same pattern as level_08_deployment_integration.py.
Import and fold into the LEVELS list consumed by seed_track_ai_developer.py,
or seed directly if the loader supports per-level files.

Model shape (unchanged):
    CareerTrack -> TrackLevel -> Topic -> Lesson / Exercise / Quiz / Project
"""

from app.models.learning import DifficultyLevel

LEVEL = {
    "title":       "Level 10: AI Evaluation & Observability",
    "description": "Move from 'the answer looks good' to measurable evidence: evaluate AI system quality across multiple dimensions, isolate retrieval vs. generation failures in RAG pipelines, and build the feedback loops that protect production systems from silent regressions.",
    "order":       10,
    "topics": [
        {
            "title":            "Why AI Evaluation Matters",
            "slug":              "ai-developer-ai-evaluation-observability-why-ai-evaluation-matters",
            "description":       "Why traditional software testing (exact-match assertions) breaks down for LLM outputs, the multiple independent dimensions of AI answer quality, and how to tell a retrieval failure apart from a generation failure in a RAG pipeline.",
            "order":             1,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "observability", "rag-evaluation"],
            "prerequisite_ids":  [],  # references RAG pipeline concepts already covered in Level 3: RAG Systems
            "lesson": {
                "title": "Why AI Evaluation Matters",
                "content": """You already know how to build AI systems.

Now we need to answer a different engineering question:

*How do I know that my AI system is actually working well?*

That is the purpose of **AI evaluation**.

## 1. What Is AI Evaluation?

AI evaluation is the systematic process of measuring the quality and behavior of an AI system.

Instead of saying:

> "The chatbot seems good."

we want to say:

> "On our evaluation dataset, the system answered 87% of questions correctly, retrieved the correct evidence 92% of the time, and produced grounded answers 89% of the time."

So evaluation turns *"I think it works"* into **measurable evidence**.

## 2. Why Traditional Software Testing Isn't Enough

Consider a normal function:

```
def add(a, b):
    return a + b

assert add(2, 3) == 5
```

There is a clear expected output:

```
Input
  ↓
Program
  ↓
Expected Output
  ↓
Exact Comparison
```

This works extremely well for deterministic software. But consider an LLM:

```
User: What are the graduation requirements?
        ↓
      LLM
        ↓
"To graduate, students must complete..."
```

There may be many acceptable ways to answer. For example:

> **Answer A:** Students must complete all required courses and satisfy the university's graduation requirements.
>
> **Answer B:** Graduation requires completing the required coursework and meeting the applicable academic requirements.
>
> **Answer C:** A student can graduate after fulfilling the required courses and other graduation conditions.

These answers are worded differently, but they could all be correct. Therefore:

**AI evaluation ≠ only exact output comparison.** We need to evaluate *quality*.

## 3. AI Systems Have Multiple Dimensions of Quality

This is one of the most important ideas in this level. An AI answer isn't simply **Correct / Incorrect** — it can be good in one dimension and bad in another.

| Dimension | Question |
|---|---|
| **Correctness** | Is the answer factually correct? |
| **Relevance** | Does it answer the user's question? |
| **Faithfulness** | Is it supported by the provided evidence? |
| **Completeness** | Did it include important information? |
| **Context relevance** | Was the retrieved information useful? |
| **Fluency** | Is it understandable and well-written? |

These dimensions are **not interchangeable**.

## 4. A Very Important Example

Imagine your Arabic university RAG assistant receives:

> "كم عدد الساعات المطلوبة للتخرج؟"

The retriever finds:

> برنامج هندسة الذكاء الاصطناعي يتطلب 160 ساعة معتمدة...

The LLM generates:

> "يتطلب البرنامج 160 ساعة معتمدة للتخرج."

Excellent. The answer is Relevant ✅, Grounded in the context ✅, Factually correct ✅, Concise ✅.

Now imagine the retriever instead finds:

> رسوم الساعة المعتمدة للعام الدراسي...

The LLM answers:

> "عدد الساعات المطلوبة للتخرج هو 160 ساعة."

Suppose 160 is actually correct, but the retrieved context did not contain that information. Now we have an interesting situation:

```
Correct       ✅
Relevant      ✅
Grounded      ❌
```

This is extremely important for RAG evaluation. **The system may have produced the right answer for the wrong reason.**

## 5. Another Example: Fluent but Wrong

User: "What is the credit-hour cost?"

LLM: "The credit hour costs 1,500 EGP."

Sounds perfectly reasonable. The sentence is Fluent ✅, Relevant ✅, Confident-looking ✅. But suppose the actual value is 1,330 EGP. Then:

```
Fluency       ✅
Relevance     ✅
Correctness   ❌
```

This is why a good-sounding answer is not necessarily a good answer.

## 6. RAG Makes Evaluation Even More Interesting

You already understand the RAG pipeline:

```
User Question
      ↓
   Retriever
      ↓
Retrieved Context
      ↓
      LLM
      ↓
Generated Answer
```

Instead of evaluating only the final answer, we can evaluate the individual stages:

- **Retrieval** — Did we retrieve the right information?
- **Context** — Is the retrieved information relevant to the question?
- **Generation** — Did the LLM correctly use the retrieved information?
- **Final Answer** — Is the answer useful, relevant, and correct?

```
                 RAG Evaluation
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
      Retrieval      Context     Generation
          ↓            ↓            ↓
      Accuracy      Relevance   Faithfulness
                                  Relevance
```

This gives us a much more powerful debugging ability.

## 7. Retrieval Failure vs Generation Failure

This distinction will become one of your most important AI engineering skills.

Suppose the correct answer is: "The program requires 160 credit hours."

**Case A — Retrieval Failure.** The retriever returns documents about tuition fees, registration, and course withdrawal. The correct graduation requirement isn't retrieved. The LLM then says "I don't have enough information." **The retriever failed.**

```
Question
   ↓
Retriever ❌
   ↓
Wrong context
   ↓
LLM
```

**Case B — Generation Failure.** The retriever correctly finds "The program requires 160 credit hours." But the LLM answers "The program requires 180 credit hours." Retrieval worked — **the generation stage failed.**

```
Question
   ↓
Retriever ✅
   ↓
Correct context
   ↓
LLM ❌
   ↓
Wrong answer
```

Without evaluation, both cases might simply appear as "the chatbot gave a wrong answer." With evaluation, we can determine **where** the failure occurred. That is much more useful to an AI engineer.

## 8. Evaluation Is Also About Engineering Decisions

Suppose you change your RAG pipeline.

```
Version 1
Embedding
    ↓
Vector Search
    ↓
Top 5
    ↓
LLM
```

Evaluation: Answer quality = 78%. You introduce hybrid search:

```
BM25 + Dense Retrieval
        ↓
       RRF
        ↓
     Top 5
        ↓
       LLM
```

Now: Answer quality = 85%. Great. But what if:

```
General questions       ↑
Arabic questions        ↑
Complex questions       ↓
```

**A single overall score can hide important failures.** That's why we need multiple evaluation dimensions.

## 9. Evaluation Is a Feedback Loop

Think of AI engineering as:

```
        Build System
             ↓
          Evaluate
             ↓
        Find Failures
             ↓
        Improve System
             ↓
          Evaluate
             ↓
        Find Regressions
             ↓
        Improve Again
```

This is much closer to how production AI systems are actually developed. You don't simply Build → Deploy → Done. Instead: **Build → Measure → Debug → Improve → Measure again.**

## 10. Evaluation Dataset = Your AI Test Suite

Later we'll build evaluation datasets. Conceptually:

```
evaluation_case = {
    "question": "How many credit hours are required?",
    "expected_answer": "160",
    "expected_context": "The program requires 160 credit hours."
}
```

Then run your AI system against many cases:

```
100 evaluation questions
        ↓
      AI System
        ↓
    100 answers
        ↓
    Evaluation
        ↓
      Scores
```

This gives you an objective way to compare RAG v1 vs RAG v2 vs RAG v3.

## 11. Why Evaluation Matters in Production

Imagine you deploy your AI assistant. Initially: Accuracy = 90%. Then you make a change — a new embedding model — and deploy it. Suddenly: Accuracy = 82%. Users might start complaining before you even notice.

A proper evaluation system could have detected:

```
Before change: 90%
After change: 82%

⚠️ Regression detected
```

**Evaluation protects your system from silent degradation.**

## 12. Evaluation vs Observability

We will study observability later, but understand this distinction now.

Evaluation asks *"How good is the system?"* — for example: Faithfulness = 91%, Answer Relevance = 87%, Retrieval Recall = 94%.

Observability asks *"What is happening inside the system?"* — for example:

```
Request ID: 82931

Latency: 1.8s
Input tokens: 450
Output tokens: 120
Retriever: 85ms
LLM: 1.5s
Retrieved chunks: 5
Model: ...
Cost: ...
```

A simple mental model:

```
Evaluation
    ↓
How GOOD is it?


Observability
    ↓
What is HAPPENING?
```

We will go much deeper into this later.

## 13. The AI Engineer Mindset

The biggest mindset change is this:

**Beginner mindset:** "The answer looks good."

**AI Engineer mindset:** "How do we know?" Then: "What exactly are we measuring?" And finally: "If the score gets worse, where did the failure happen?"

That's the mindset this entire level is designed to develop.

**One principle to remember: never evaluate only the final answer when you can evaluate the individual stages of the AI system.**""",
                "estimated_minutes": 35,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Diagnose the Failure: Tuition Fees Instead of Course List",
                    "description": """Your RAG system receives:

"What courses are required for graduation?"

The retriever returns completely unrelated information about tuition fees. The LLM responds:

"I cannot find the required courses in the available information."

Answer these three questions, reasoning in your own words (don't worry about metrics yet):

1. Is the retrieval good or bad?
2. Is the LLM's final answer necessarily bad?
3. Is this primarily a retrieval failure or generation failure, and why?""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "rag-debugging", "failure-analysis"],
                },
                {
                    "title": "Build an Evaluation Case",
                    "description": """Write a Python function `make_eval_case(question, expected_answer, expected_context)` that returns an `evaluation_case` dict with exactly the keys `"question"`, `"expected_answer"`, and `"expected_context"`.

Then use it to build a small evaluation set (a list of at least 3 `evaluation_case` dicts) for a university FAQ assistant, covering at least one question where the expected answer and expected context are about different topics than credit hours (to prove you're not just copying the lesson's example).""",
                    "starter_code": """def make_eval_case(question, expected_answer, expected_context):
    # TODO: return the evaluation_case dict
    pass


# TODO: build eval_dataset as a list of 3+ evaluation_case dicts
eval_dataset = []
""",
                    "solution_code": """def make_eval_case(question, expected_answer, expected_context):
    return {
        "question": question,
        "expected_answer": expected_answer,
        "expected_context": expected_context,
    }


eval_dataset = [
    make_eval_case(
        "How many credit hours are required to graduate?",
        "160",
        "The program requires 160 credit hours.",
    ),
    make_eval_case(
        "What is the credit-hour cost?",
        "1,330 EGP",
        "The cost per credit hour is 1,330 EGP.",
    ),
    make_eval_case(
        "What is the deadline to withdraw from a course?",
        "The end of week 10",
        "Students may withdraw from a course until the end of week 10.",
    ),
]
""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "evaluation-datasets", "python"],
                },
            ],
            "quiz": {
                "title": "Why AI Evaluation Matters — Knowledge Check",
                "questions": [
                    {
                        "question": "Why can't AI outputs generally be evaluated with the same exact-match assertion style used for a function like add(2, 3) == 5?",
                        "options": [
                            "Because LLMs are too slow to run in a test suite",
                            "Because multiple differently-worded answers can all be correct, so quality must be judged rather than matched exactly",
                            "Because LLMs never produce the same answer twice, making testing impossible",
                            "Because exact-match testing only works for RAG systems, not plain LLM calls",
                        ],
                        "correct": 1,
                        "explanation": "The lesson shows three differently-worded answers (A, B, C) to the same question that could all be correct. Since there's no single expected output, evaluation must assess quality dimensions rather than do an exact comparison.",
                    },
                    {
                        "question": "In the Arabic university RAG example, the retriever finds a document about credit-hour tuition fees (not graduation requirements), yet the LLM still outputs the factually correct number of required hours. How should this answer be scored?",
                        "options": [
                            "Fully correct across all dimensions, since the final number is right",
                            "Correct and relevant, but not grounded — the system got the right answer for the wrong reason",
                            "Incorrect, because the answer doesn't match the retrieved context word-for-word",
                            "Irrelevant, since the retrieved document was about a different topic",
                        ],
                        "correct": 1,
                        "explanation": "The lesson highlights this exact case: the answer can be Correct ✅, Relevant ✅, but Grounded ❌, because the retrieved context did not actually contain the information the answer relied on.",
                    },
                    {
                        "question": "A RAG system's retriever correctly returns the passage stating a program requires 160 credit hours, but the LLM answers '180 credit hours.' What kind of failure is this?",
                        "options": [
                            "Retrieval failure",
                            "Generation failure",
                            "Context relevance failure",
                            "Observability failure",
                        ],
                        "correct": 1,
                        "explanation": "Retrieval worked (the correct context was found), so the breakdown happened when the LLM used that context to generate an answer — a generation failure, per Case B in the lesson.",
                    },
                    {
                        "question": "A team improves their RAG pipeline's overall answer quality from 78% to 85% by adding hybrid search, but a per-category breakdown shows complex questions actually got worse. What does this illustrate?",
                        "options": [
                            "Hybrid search should never be used in production",
                            "A single overall score can hide important failures, which is why multiple evaluation dimensions matter",
                            "The evaluation dataset must have been built incorrectly",
                            "Complex questions cannot be evaluated with automated methods",
                        ],
                        "correct": 1,
                        "explanation": "The lesson uses this exact scenario to make the point that an aggregate score (78% → 85%) can mask a regression in a specific slice (complex questions), motivating dimension- and segment-level evaluation.",
                    },
                    {
                        "question": "What is the key distinction between AI evaluation and observability, as introduced in this lesson?",
                        "options": [
                            "Evaluation is only for RAG systems; observability is only for plain LLM calls",
                            "Evaluation measures how good the system is; observability describes what is happening inside the system (latency, tokens, cost, etc.)",
                            "Observability replaces the need for evaluation once a system is in production",
                            "Evaluation is done by humans; observability is always fully automated",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's mental model is explicit: Evaluation → 'How GOOD is it?' (e.g., faithfulness, relevance scores) vs. Observability → 'What is HAPPENING?' (e.g., latency, token counts, cost).",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "Evaluation Datasets",
            "slug":              "ai-developer-ai-evaluation-observability-evaluation-datasets",
            "description":       "How to design a representative evaluation dataset for an AI system: the fields an evaluation case should contain, why categories and difficulty labels matter, ground truth, and turning production failures into permanent regression tests.",
            "order":             2,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "evaluation-datasets", "ground-truth"],
            "prerequisite_ids":  [],  # builds on "Why AI Evaluation Matters" (this level, topic 1)
            "lesson": {
                "title": "Evaluation Datasets",
                "content": """Now that you understand why evaluation matters, the next question is:

*What do we evaluate our AI system on?*

The answer is an **evaluation dataset**.

## 1. What Is an Evaluation Dataset?

An evaluation dataset is a collection of test cases designed to measure how well your AI system performs.

For a RAG system, a simple test case might look like:

```
evaluation_case = {
    "question": "How many credit hours are required for graduation?",
    "expected_answer": "160 credit hours",
    "expected_context": "The program requires 160 credit hours for graduation."
}
```

Then you might have Test Case 1, Test Case 2, Test Case 3 ... Test Case 100. **Your evaluation dataset becomes the test suite for your AI system.**

## 2. Why Not Just Test Random Questions?

Suppose you build an academic RAG assistant. You manually ask it "What is the GPA requirement?" and it answers correctly. You think: "Great, it works." But you've tested only one type of question.

A real university assistant might receive questions about GPA requirements, credit hours, course registration, failing a course, prerequisites, tuition cost, graduation requirements, and withdrawal — all very different in shape. Your system might perform very well on some categories and poorly on others.

Therefore: **a good evaluation dataset should represent the situations your AI system will actually encounter.**

## 2. The Evaluation Dataset as a Map of Your System

Think about your production users. They don't all ask the same type of question. So your dataset should cover different dimensions:

```
                 Evaluation Dataset
                        │
       ┌────────────────┼────────────────┐
       ↓                ↓                ↓
   Easy Cases       Normal Cases      Difficult Cases
       │                │                │
       ↓                ↓                ↓
   Edge Cases       Ambiguous        Failure Cases
```

For a RAG assistant, you could organize questions into categories:

- **Category 1 — Simple factual questions.** "How many credit hours are required?"
- **Category 2 — Multi-step questions.** "Can a student register for Course X if they have completed Course Y but not Course Z?"
- **Category 3 — Ambiguous questions.** "What are the requirements?" — Requirements for what?
- **Category 4 — Out-of-scope questions.** "Who will win the World Cup?" — Your academic assistant shouldn't pretend it knows.
- **Category 5 — Difficult questions.** "If a student has completed 120 hours with a GPA of X and failed course Y, can they graduate?"

These cases are extremely valuable because they expose weaknesses.

## 3. What Should an Evaluation Case Contain?

A useful starting structure is:

```
evaluation_case = {
    "question": "...",
    "expected_answer": "...",
    "expected_context": "...",
}
```

**question** — the actual user input, e.g. "How many credit hours are required for graduation?" This is what we send to the AI system.

**expected_answer** — the answer we consider correct, e.g. "160 credit hours." This is often called **ground truth** or a reference answer. Important: ground truth does not always mean there is only one acceptable wording — "160 credit hours" and "The program requires 160 credit hours." could both be correct. That's one reason exact string comparison isn't always enough for AI; we'll study this in the next lessons.

**expected_context** — for RAG, we can also specify the evidence that should support the answer, e.g. "Program graduation requirements: 160 credit hours." Now we can evaluate not just "Did the AI give the correct answer?" but also "Did the retriever find the correct evidence?" This is extremely useful.

## 4. Ground Truth

You will hear this term frequently. **Ground truth** means the information we treat as the correct reference for evaluation. For example, in `{"question": "How many credit hours are required?", "expected_answer": "160"}`, the expected answer *is* the ground truth.

But be careful: ground truth should ideally come from a trusted source, not from an LLM guessing what the answer should be. For your academic assistant, a strong source might be:

```
Official university regulations
        ↓
Human verification
        ↓
Evaluation dataset
```

rather than:

```
LLM
 ↓
Generate expected answer
 ↓
Assume it's correct
```

## 5. Good Evaluation Questions

A good evaluation question should represent something your system is expected to handle. "How many credit hours are required for graduation?" is good. "Tell me something interesting" is not very useful — unless your application is specifically designed for open-ended conversation. **The question should have a reason for existing in the test set.**

## 6. Representative Data

One of the most important concepts is **representativeness**. Imagine your dataset contains 90 easy questions and 10 difficult questions. Your system gets 95/100 correct — looks excellent. But in production, perhaps 40% of users ask difficult questions. Your dataset doesn't represent reality.

So the evaluation dataset should reflect the types of situations the system encounters:

```
Production Distribution
        ≈
Evaluation Distribution
```

Not necessarily perfectly, but reasonably.

## 7. Difficult Cases Are Extremely Valuable

Suppose your system gets these results:

```
Easy questions:       98%
Normal questions:     92%
Difficult questions:  61%
```

If you only test easy questions, you'll think "my RAG system is excellent." But the difficult cases reveal the actual weakness. **Your evaluation dataset should intentionally contain cases designed to break your system.** These are often called **challenge cases** or **adversarial/edge cases**, depending on how they're constructed.

## 8. Failure Cases Are Gold

Suppose a production user asks "Can I graduate if my GPA is 2.1?" and your system incorrectly says "Yes." You investigate and discover a failure. Don't just fix the code and forget the question — add it to the evaluation dataset:

```
evaluation_case = {
    "question": "Can I graduate if my GPA is 2.1?",
    "expected_answer": "...",
    "expected_context": "...",
}
```

Now you've converted a real production failure into a permanent regression test. This creates a powerful loop:

```
Production Failure
       ↓
Investigate
       ↓
Create Evaluation Case
       ↓
Fix System
       ↓
Run Evaluation
       ↓
Prevent Same Failure
```

This is a major production AI engineering practice.

## 9. Don't Only Store Successful Cases

A common mistake is creating a dataset consisting only of normal questions. Instead, include:

```
✅ Normal questions
✅ Difficult questions
✅ Ambiguous questions
✅ Edge cases
✅ Out-of-scope questions
✅ Previously failed questions
```

For example:

```
evaluation_cases = [
    {"question": "...", "expected_answer": "...", "expected_context": "...", "category": "factual"},
    {"question": "...", "expected_answer": "...", "expected_context": "...", "category": "difficult"},
    {"question": "...", "expected_answer": "...", "expected_context": "...", "category": "edge_case"},
]
```

The **category** field isn't required, but it becomes very useful when analyzing failures.

## 10. Why Categories Matter

Imagine your overall evaluation score is 87%. That number alone isn't enough. Suppose we break it down:

```
Factual questions      95%
Prerequisite questions 91%
Multi-hop questions    79%
Ambiguous questions    68%
Out-of-scope           97%
```

Now we immediately know: **ambiguous questions are a weakness.** Without categories, we'd only see 87%. This is why evaluation datasets should contain useful metadata.

## 11. A Better Evaluation Case

A more realistic structure could be:

```
evaluation_case = {
    "id": "case_001",
    "question": "How many credit hours are required for graduation?",
    "expected_answer": "160 credit hours",
    "expected_context": [
        "The program requires 160 credit hours for graduation."
    ],
    "category": "graduation",
    "difficulty": "easy"
}
```

Now we have an ID, question, ground-truth answer, expected evidence, category, and difficulty — this allows much better analysis later.

## 12. Your Dataset Will Evolve

An evaluation dataset isn't something you create once and never touch. A mature AI system continuously adds new cases:

```
Initial dataset
     ↓
100 cases
     ↓
Deploy
     ↓
Find production failure
     ↓
+ 1 case
     ↓
101 cases
     ↓
Another failure
     ↓
+ 1 case
     ↓
102 cases
```

Over time, the dataset becomes a representation of your system's known failure modes. This is extremely valuable.

## 13. Evaluation Dataset vs Training Dataset

Don't confuse these.

**Training dataset** is used to teach a model:

```
Data
 ↓
Training
 ↓
Model
```

**Evaluation dataset** is used to measure a system:

```
Evaluation Cases
 ↓
AI System
 ↓
Results
 ↓
Score
```

The evaluation dataset should ideally be kept separate from whatever data is used to optimize the system. Otherwise you risk building a system that performs well only on the questions you already know.

## 14. A Simple AI Evaluation Pipeline

Eventually, your evaluation process will look something like:

```
                 Evaluation Dataset
                         ↓
                  Run AI System
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
        Retrieved Context       Final Answer
              ↓                     ↓
        Evaluate Retrieval     Evaluate Answer
              ↓                     ↓
              └──────────┬──────────┘
                         ↓
                    Evaluation
                      Report
```

And later we'll add metrics to this pipeline.

## 15. Practical Python Example

Let's create a tiny dataset:

```
evaluation_dataset = [
    {
        "id": "001",
        "question": "How many credit hours are required for graduation?",
        "expected_answer": "160 credit hours",
        "expected_context": "The program requires 160 credit hours.",
        "category": "graduation",
        "difficulty": "easy"
    },
    {
        "id": "002",
        "question": "What is the cost of one credit hour?",
        "expected_answer": "1330 EGP",
        "expected_context": "The cost of one credit hour is 1330 EGP.",
        "category": "tuition",
        "difficulty": "easy"
    }
]
```

We can iterate through it:

```
for case in evaluation_dataset:
    print(case["question"])
```

Output:

```
How many credit hours are required for graduation?
What is the cost of one credit hour?
```

Later, we'll send each question through your RAG pipeline and compare the resulting answer against the appropriate evaluation criteria.

## The Most Important Mental Model

Think of your evaluation dataset as: *a controlled set of questions that represents what your AI system should be able to handle.* And every time your system fails in an important way: **turn that failure into a test case.** That's how an AI evaluation system becomes stronger over time.

**Your evaluation dataset is the test suite of your AI system — and every important production failure should have a chance to become a permanent evaluation case.**""",
                "estimated_minutes": 35,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Design an Evaluation Set for an Arabic University Assistant",
                    "description": """Imagine you're building an Arabic university RAG assistant. Create 5 evaluation cases that you think should be included in its evaluation dataset. For each case, give:

1. Question
2. Expected answer
3. Expected context
4. Category
5. Difficulty

Try to include different types: one easy factual question, one difficult question, one ambiguous question, one out-of-scope question, and one question designed to catch a likely RAG failure. Plain text is enough — you don't need Python for this one.""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "evaluation-datasets", "dataset-design"],
                },
                {
                    "title": "Filter an Evaluation Dataset by Category and Difficulty",
                    "description": """Given a list of evaluation_case dicts (each with "id", "question", "expected_answer", "expected_context", "category", "difficulty"), write a function `filter_cases(dataset, category=None, difficulty=None)` that returns only the cases matching the given category and/or difficulty (ignore a filter if it's None). Then use it to print how many "difficult" cases exist in a sample dataset of at least 6 cases spanning at least 3 categories.""",
                    "starter_code": """evaluation_dataset = [
    # TODO: add at least 6 evaluation_case dicts spanning >= 3 categories
    # and a mix of "easy" / "difficult" / "ambiguous" difficulty labels
]


def filter_cases(dataset, category=None, difficulty=None):
    # TODO: return the filtered list
    pass


# TODO: print the count of "difficult" cases using filter_cases
""",
                    "solution_code": """evaluation_dataset = [
    {"id": "001", "question": "How many credit hours are required?", "expected_answer": "160", "expected_context": "...", "category": "graduation", "difficulty": "easy"},
    {"id": "002", "question": "What is the cost per credit hour?", "expected_answer": "1330 EGP", "expected_context": "...", "category": "tuition", "difficulty": "easy"},
    {"id": "003", "question": "Can I register for Course X without completing Course Y?", "expected_answer": "No, Course Y is a prerequisite.", "expected_context": "...", "category": "registration", "difficulty": "difficult"},
    {"id": "004", "question": "If I have 120 hours and a GPA of 1.9, can I graduate?", "expected_answer": "No, minimum GPA is 2.0.", "expected_context": "...", "category": "graduation", "difficulty": "difficult"},
    {"id": "005", "question": "What are the requirements?", "expected_answer": "Clarification needed: requirements for what?", "expected_context": "...", "category": "ambiguous", "difficulty": "ambiguous"},
    {"id": "006", "question": "Who will win the next World Cup?", "expected_answer": "This is out of scope for the academic assistant.", "expected_context": "...", "category": "out_of_scope", "difficulty": "easy"},
]


def filter_cases(dataset, category=None, difficulty=None):
    result = dataset
    if category is not None:
        result = [c for c in result if c["category"] == category]
    if difficulty is not None:
        result = [c for c in result if c["difficulty"] == difficulty]
    return result


difficult_cases = filter_cases(evaluation_dataset, difficulty="difficult")
print(len(difficult_cases))
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "evaluation-datasets", "python"],
                },
            ],
            "quiz": {
                "title": "Evaluation Datasets — Knowledge Check",
                "questions": [
                    {
                        "question": "Why is it risky to conclude an academic RAG assistant 'works' after manually testing only one question like 'What is the GPA requirement?'",
                        "options": [
                            "Because GPA questions are always answered incorrectly by RAG systems",
                            "Because a single question doesn't reveal how the system performs across the many different question types real users will actually ask",
                            "Because manual testing is always less accurate than automated testing",
                            "Because GPA is not a valid evaluation category",
                        ],
                        "correct": 1,
                        "explanation": "The lesson makes this point directly: testing only one type of question hides how the system performs on the many other categories (registration, prerequisites, tuition, edge cases) that production users actually ask.",
                    },
                    {
                        "question": "An evaluation dataset has 90 easy questions and 10 difficult questions, and the system scores 95/100. In production, 40% of real questions are difficult. What does this scenario illustrate?",
                        "options": [
                            "The evaluation dataset is perfectly fine since the score is high",
                            "The evaluation dataset lacks representativeness — its distribution doesn't match the production distribution",
                            "Difficult questions should be removed from evaluation datasets entirely",
                            "A 95% score always means the system is production-ready",
                        ],
                        "correct": 1,
                        "explanation": "This is the lesson's core representativeness example: a high aggregate score can be misleading when the evaluation dataset's distribution of easy/difficult cases doesn't match what production actually looks like.",
                    },
                    {
                        "question": "A production user asks 'Can I graduate if my GPA is 2.1?' and the system incorrectly answers 'Yes.' According to the lesson, what is the recommended next step after fixing the underlying issue?",
                        "options": [
                            "Delete the question so it doesn't confuse future users",
                            "Add the question as a permanent evaluation case so the same failure can be caught again if it regresses",
                            "Ignore it since it was a one-time production error",
                            "Retrain the underlying LLM on this specific question",
                        ],
                        "correct": 1,
                        "explanation": "This is the 'failure cases are gold' principle: turning a real production failure into a permanent evaluation case closes the loop — Production Failure → Investigate → Create Evaluation Case → Fix → Run Evaluation → Prevent Same Failure.",
                    },
                    {
                        "question": "What is the key difference between a training dataset and an evaluation dataset?",
                        "options": [
                            "There is no difference; they are the same thing with different names",
                            "A training dataset is used to teach a model, while an evaluation dataset is used to measure a system's performance and should ideally stay separate from what's used to optimize it",
                            "Evaluation datasets are always larger than training datasets",
                            "Training datasets only apply to RAG systems, not LLMs",
                        ],
                        "correct": 1,
                        "explanation": "The lesson distinguishes: Training dataset → Data → Training → Model, vs. Evaluation dataset → Evaluation Cases → AI System → Results → Score — and warns against reusing optimization data for evaluation, to avoid overestimating real performance.",
                    },
                    {
                        "question": "Why does adding a 'category' field (e.g. factual, prerequisite, multi-hop, ambiguous, out-of-scope) to evaluation cases matter, even though it's optional?",
                        "options": [
                            "It's required by most databases and has no analytical benefit",
                            "It lets you break an aggregate score down by category, revealing specific weaknesses (e.g. ambiguous questions at 68%) that a single overall score like 87% would hide",
                            "It automatically improves the AI system's accuracy",
                            "It replaces the need for an expected_answer field",
                        ],
                        "correct": 1,
                        "explanation": "The lesson shows exactly this: an 87% overall score looks fine, but breaking it down by category exposes that ambiguous questions score only 68% — a weakness invisible without categories.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "Exact Match",
            "slug":              "ai-developer-ai-evaluation-observability-exact-match",
            "description":       "Your first evaluation metric: how Exact Match works, why it's simple, fast, and deterministic, why it fails on semantically-correct-but-differently-worded answers, and when it's the right tool for structured outputs like IDs, codes, and labels.",
            "order":             3,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "metrics", "exact-match"],
            "prerequisite_ids":  [],  # builds on "Evaluation Datasets" (this level, topic 2)
            "lesson": {
                "title": "Exact Match",
                "content": """Now we move from building evaluation datasets to our first evaluation metric: **Exact Match (EM)**.

It is one of the simplest evaluation metrics, but understanding its limitations is very important for AI engineering.

## 1. What Is Exact Match?

Exact Match asks: *"Is the AI's output exactly the same as the expected answer?"*

```
AI Output
    ↓
Compare with Ground Truth
    ↓
Exactly the same?
   ↙       ↘
 YES       NO
  1         0
```

The simplest implementation is:

```
prediction == expected_answer
```

For example:

```
expected = "160"
prediction = "160"

print(prediction == expected)
```

Output: `True`. So **Exact Match = 1**.

## 2. Simple Example

Suppose our evaluation case is:

```
case = {
    "question": "How many credit hours are required?",
    "expected_answer": "160"
}
```

Our AI generates `prediction = "160"`. Then:

```
score = int(prediction == case["expected_answer"])
print(score)
```

Output: `1`. The answer is an exact match.

## 3. When Exact Match Is Useful

Exact Match is particularly useful when there is a clear, unambiguous expected answer. For example:

- Question: "What is the course code for Machine Learning?" Expected: `CSE251`. Prediction: `CSE251`. Exact Match: `1`.
- Question: "How many credits is the course?" Expected: `3`. Prediction: `3`. Exact Match: `1`.

## 4. Exact Match Can Be Used for Structured Outputs

This is where Exact Match becomes particularly useful. Suppose your AI must classify a question — "How much does one credit hour cost?" — with expected category `"tuition"` and AI output `"tuition"`. Exact Match: `1`.

Another example: expected `"registration"`, prediction `"tuition"` → result `0`. This works well because the possible outputs are controlled.

## 5. The Problem With Exact Match

Now we reach the important part. Consider:

```
Expected: 160 credit hours
AI output: The program requires 160 credit hours.
```

A human would probably say **correct**. But Exact Match compares `"160 credit hours" == "The program requires 160 credit hours."` → `False`. So **Exact Match = 0**, even though the answer is correct.

This demonstrates the fundamental weakness of Exact Match: **it measures textual equality, not necessarily semantic correctness.**

## 6. Another Example

Expected: `1330 EGP`. Prediction: `The cost is 1330 Egyptian pounds.` Human judgment: ✅ correct. Exact Match: ❌ 0. Why? Because the strings are different.

## 7. Wording Can Cause False Failures

Consider: expected `"The course has 3 credit hours."`, prediction `"This course carries 3 credit hours."` These communicate essentially the same information, but `expected == prediction` returns `False`. Exact Match would mark it wrong.

This is called a **false negative** from a string-level perspective. The system may actually be correct, but the metric fails to recognize it.

## 8. Normalization Can Help

Before comparing strings, we can sometimes normalize them:

```
def normalize(text):
    return text.strip().lower()
```

Then:

```
expected = "160"
prediction = " 160 "

print(normalize(expected) == normalize(prediction))
```

Output: `True`. This handles superficial differences.

## 9. A Slightly Better Normalization

We could also remove unnecessary punctuation:

```
import string

def normalize(text):
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text
```

Then `"160 credit hours."` and `"160 credit hours"` both become approximately `"160 credit hours"`. Now Exact Match succeeds.

## 10. But Normalization Doesn't Solve Everything

This is very important. Normalization can solve `"160"` vs `" 160 "`, or `"160 credit hours."` vs `"160 credit hours"`. But it **cannot** solve:

```
Expected: 160 credit hours
Prediction: The program requires 160 credit hours for graduation.
```

The meaning is similar, but the strings are still fundamentally different, and we don't want to keep adding complicated string rules. **At some point we need to evaluate meaning, not just text.** That's where **Semantic Similarity** will come in later.

## 11. Exact Match for RAG

Let's connect this to your RAG knowledge. Suppose:

```
evaluation_case = {
    "question": "How many credit hours are required?",
    "expected_answer": "160"
}
```

The RAG system produces "The program requires 160 credit hours for graduation." Exact Match: `0`. But the answer might be perfectly correct. So using Exact Match alone for an open-ended RAG assistant would give us a misleading evaluation.

This is a crucial engineering principle: **choose a metric based on the type of output you're evaluating.**

## 12. When Exact Match Is Appropriate for RAG

Exact Match can still be useful in RAG. "What is the course code?" → Expected `CSE251`, Generated `CSE251`. Great. "How many credits does CSE251 have?" → Expected `3`, Generated `3`. Again, Exact Match works well.

So the problem isn't "Exact Match is bad." The real lesson is: **Exact Match is appropriate for some outputs and inappropriate for others.**

## 13. Exact Match Over a Dataset

Suppose we have five test cases:

| Case | Expected | Prediction | EM |
|---|---|---|---|
| 1 | 160 | 160 | 1 |
| 2 | 3 | 3 | 1 |
| 3 | 1330 | 1500 | 0 |
| 4 | CSE251 | CSE251 | 1 |
| 5 | 2.5 | 2.3 | 0 |

Correct exact matches = 3, total cases = 5. So **Exact Match = 3/5 = 60%**.

```
EM = number of exact matches
     ------------------------
       total test cases
```

## 14. Why This Metric Is Still Valuable

Even though it is limited, Exact Match has some excellent properties: it is **simple** (easy to understand), **fast** (no model/API required), **deterministic** (same input → same metric), **cheap** (evaluate thousands of cases cheaply), and **reproducible** (different engineers get the same result). That's why it remains useful in many AI evaluation pipelines.

## 15. Exact Match vs Human Judgment

Expected: `160 credit hours`. Prediction: `The student needs 160 credit hours to graduate.` Human judgment: correct. Exact Match: incorrect. This illustrates a fundamental issue in AI evaluation:

```
String Equality
       ≠
Semantic Correctness
```

This distinction will become increasingly important throughout Level 10.

## 16. Practical Python Function

Let's build a tiny Exact Match evaluator:

```
def exact_match(prediction, expected):
    return int(prediction.strip() == expected.strip())
```

Test it:

```
print(exact_match("160", "160"))
```

Output: `1`. And:

```
print(exact_match("The answer is 160", "160"))
```

Output: `0`. Simple.

## 17. Calculating Dataset Accuracy

We can evaluate multiple cases:

```
predictions = ["160", "3", "1330", "CSE251"]
expected = ["160", "3", "1500", "CSE251"]

scores = [
    exact_match(pred, exp)
    for pred, exp in zip(predictions, expected)
]

accuracy = sum(scores) / len(scores)
print(accuracy)
```

Results: `[1, 1, 0, 1]`. Therefore: **Exact Match = 75%**.

## 18. A Critical Engineering Lesson

Suppose you change your prompt. Version 1: Exact Match = 70%. Version 2: Exact Match = 60%. Should you immediately conclude Version 2 is worse? **Not necessarily.** Maybe Version 2 generates more natural answers — Version 1 says `160`, Version 2 says `The program requires 160 credit hours for graduation.` Version 2 may be better for users even though Exact Match decreased.

This is why: **never treat one metric as the complete definition of AI quality.** Later, we'll combine multiple evaluation methods.

## 19. Mental Model

```
Exact Match
     ↓
"Did the output exactly match my reference?"
```

It is excellent when the expected output is precise and exact comparison makes sense — **IDs, codes, labels, numbers, short structured answers, classification outputs.**

It becomes weak when many different wordings can be correct and string equality is too strict — **open-ended answers, RAG explanations, summaries, natural-language responses.**

## Short Summary

Exact Match compares an AI prediction directly against a reference answer (`prediction == expected`). It is simple, fast, deterministic, and cheap — but it measures textual equality, not meaning. Therefore:

```
Exact Match
     ≠
Semantic Correctness
```

It works particularly well for structured outputs such as IDs, labels, codes, and numbers — but it can incorrectly mark a semantically correct natural-language answer as wrong.

**Key takeaway: Exact Match answers "Did the AI produce exactly the expected text?" — not "Did the AI understand and answer correctly?" That distinction is fundamental to AI evaluation.**""",
                "estimated_minutes": 35,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Diagnose an Exact Match Limitation",
                    "description": """Consider this evaluation case:

Question: "How many credit hours are required for graduation?"
Expected answer: "160 credit hours"
AI answer: "Students must complete a total of 160 credit hours to graduate."

Answer in your own words:

1. What would Exact Match score this pair?
2. Is the AI answer actually correct?
3. Why does this example demonstrate a limitation of Exact Match?""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "exact-match", "metric-limitations"],
                },
                {
                    "title": "Implement Exact Match with Normalization",
                    "description": """Write two functions:

1. `normalize(text)` — lowercases, strips whitespace, and removes punctuation from `text`.
2. `exact_match(prediction, expected)` — returns `1` if the normalized `prediction` equals the normalized `expected`, else `0`.

Then compute the Exact Match accuracy (as a fraction, 0.0–1.0) over this list of (prediction, expected) pairs:

```
pairs = [
    ("160", "160"),
    ("160.", " 160 "),
    ("CSE251", "cse251"),
    ("The answer is 160", "160"),
    ("1330", "1500"),
]
```

Print the individual scores and the final accuracy.""",
                    "starter_code": """import string

def normalize(text):
    # TODO: lowercase, strip, and remove punctuation
    pass


def exact_match(prediction, expected):
    # TODO: return 1 or 0 using normalize()
    pass


pairs = [
    ("160", "160"),
    ("160.", " 160 "),
    ("CSE251", "cse251"),
    ("The answer is 160", "160"),
    ("1330", "1500"),
]

# TODO: compute and print individual scores and overall accuracy
""",
                    "solution_code": """import string

def normalize(text):
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text


def exact_match(prediction, expected):
    return int(normalize(prediction) == normalize(expected))


pairs = [
    ("160", "160"),
    ("160.", " 160 "),
    ("CSE251", "cse251"),
    ("The answer is 160", "160"),
    ("1330", "1500"),
]

scores = [exact_match(pred, exp) for pred, exp in pairs]
print(scores)

accuracy = sum(scores) / len(scores)
print(accuracy)
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "exact-match", "python"],
                },
            ],
            "quiz": {
                "title": "Exact Match — Knowledge Check",
                "questions": [
                    {
                        "question": "Expected answer: 'The course has 3 credit hours.' AI answer: 'This course carries 3 credit hours.' What would raw (non-normalized) Exact Match score this pair, and what is this outcome called?",
                        "options": [
                            "Score = 1; this is called a true positive",
                            "Score = 0; this is called a false negative, since the answer is likely correct but the strings differ",
                            "Score = 0; this is called a true negative, since the answer is wrong",
                            "Score = 1; normalization is not needed here",
                        ],
                        "correct": 1,
                        "explanation": "The strings are not identical, so raw Exact Match scores 0 even though the meaning is the same — the lesson calls this a false negative from a string-level perspective.",
                    },
                    {
                        "question": "What CAN basic text normalization (lowercase, strip whitespace, remove punctuation) fix, and what can it NOT fix, according to the lesson?",
                        "options": [
                            "It fixes everything, including differently-worded but semantically equivalent answers",
                            "It fixes superficial differences like casing, extra spaces, or trailing punctuation, but it cannot make 'The program requires 160 credit hours for graduation' match '160 credit hours' — that requires evaluating meaning, not just text",
                            "It fixes nothing; normalization is purely cosmetic and has no effect on Exact Match scoring",
                            "It only works for numeric answers, never for text answers",
                        ],
                        "correct": 1,
                        "explanation": "The lesson is explicit: normalization solves superficial mismatches ('160' vs ' 160 ') but cannot bridge genuinely different wording that conveys the same meaning — that needs semantic similarity, covered later.",
                    },
                    {
                        "question": "For which of the following outputs is Exact Match typically the MOST appropriate metric?",
                        "options": [
                            "A free-form paragraph explaining graduation requirements",
                            "A course code classification output like 'CSE251' or a category label like 'tuition'",
                            "A conversational RAG answer summarizing multiple documents",
                            "An open-ended explanation of why a policy exists",
                        ],
                        "correct": 1,
                        "explanation": "The lesson highlights structured outputs — IDs, codes, labels, numbers, short exact answers, classification outputs — as the cases where Exact Match works well, since there's a single unambiguous correct string.",
                    },
                    {
                        "question": "Given predictions = ['160', '3', '1330', 'CSE251'] and expected = ['160', '3', '1500', 'CSE251'], what is the Exact Match accuracy over this dataset?",
                        "options": ["100%", "75%", "50%", "25%"],
                        "correct": 1,
                        "explanation": "Three of the four pairs match exactly ('160'='160', '3'='3', 'CSE251'='CSE251') and one doesn't ('1330' vs '1500'), giving 3/4 = 75%, matching the lesson's worked example.",
                    },
                    {
                        "question": "A team changes their prompt and Exact Match drops from 70% to 60%, but the new answers are more natural, full sentences instead of bare numbers. What is the correct engineering conclusion?",
                        "options": [
                            "Version 2 is definitively worse and should be reverted immediately",
                            "The drop in Exact Match doesn't necessarily mean Version 2 is worse for users — a single metric shouldn't be treated as the complete definition of AI quality",
                            "Exact Match is a useless metric and should never be used",
                            "The evaluation dataset must be recreated whenever Exact Match changes",
                        ],
                        "correct": 1,
                        "explanation": "The lesson uses this exact scenario to teach that Exact Match can penalize more natural, still-correct answers, and that no single metric should be treated as the full picture of quality — a key reason multiple evaluation methods get combined later.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "Semantic Similarity",
            "slug":              "ai-developer-ai-evaluation-observability-semantic-similarity",
            "description":       "Move beyond textual equality: measure meaning similarity between an AI answer and a reference answer using embeddings and cosine similarity, why thresholds must be calibrated rather than assumed, and why high semantic similarity still doesn't guarantee factual correctness.",
            "order":             4,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "metrics", "semantic-similarity", "embeddings"],
            "prerequisite_ids":  [],  # builds on "Exact Match" (this level, topic 3) and embeddings/RAG concepts from earlier levels
            "lesson": {
                "title": "Semantic Similarity",
                "content": """In the previous lesson, we saw an important limitation: **Exact Match compares text, not meaning.** Now we need a metric that cares more about meaning. That brings us to **Semantic Similarity**.

## 1. What Is Semantic Similarity?

Semantic similarity measures: *how similar are two pieces of text in meaning?* Instead of asking "are the strings identical?" we ask "do these two texts mean approximately the same thing?"

For example:

> Reference: The program requires 160 credit hours.
>
> AI: Students need to complete 160 credit hours to graduate.

The wording is different. But the meaning is very similar. So:

```
Exact Match         → 0
Semantic Similarity → High
```

## 2. Why Do We Need It?

Consider: expected "The course has 3 credit hours." AI output "This course carries three credit hours." A string comparison says **different ❌**. A semantic comparison says **same meaning ✅**. This is much closer to how humans evaluate natural-language answers.

## 3. The Mental Model

The basic idea is:

```
Text
 ↓
Embedding
 ↓
Vector
```

For example:

```
"The course has 3 credit hours."
            ↓
       Embedding Model
            ↓
[0.12, -0.43, 0.81, ...]
```

Another sentence:

```
"This course carries three credits."
            ↓
       Embedding Model
            ↓
[0.10, -0.40, 0.79, ...]
```

If the vectors are close together, their meanings are likely similar:

```
Sentence A
    ↓
Embedding A

Sentence B
    ↓
Embedding B

Embedding A ↔ Embedding B
        ↓
Similarity Score
```

This should already feel familiar — you studied **embeddings** and **semantic search** earlier. We're now using the same underlying idea for evaluation.

## 4. Connection to Your RAG Knowledge

You previously learned:

```
Document
   ↓
Embedding
   ↓
Vector Database
   ↓
Similarity Search
```

Semantic evaluation uses a related idea:

```
Expected Answer
      ↓
   Embedding
      ↓
       ↕
   Similarity
       ↕
      ↓
AI Answer
      ↓
   Embedding
```

The difference is the purpose. **Retrieval** uses similarity to find relevant information. **Evaluation** uses similarity to determine whether two pieces of text have similar meaning.

## 5. Cosine Similarity

A common way to compare embeddings is **cosine similarity**. You don't need to memorize the mathematics yet. Conceptually:

```
Vector A
    ↘
     angle
    ↗
Vector B
```

If the vectors point in similar directions, similarity is high. If they point in very different directions, similarity is low.

```
-1 ───────── 0 ───────── 1
different               similar
```

For many modern text embedding models, practical text similarities are often concentrated in a narrower positive range, so don't interpret the raw number as a universal percentage. A score of `0.85` doesn't automatically mean "the answer is 85% correct." It means the embeddings have a certain degree of similarity according to that particular model and similarity function.

## 6. Simple Python Example

Let's use a sentence-transformer model:

```
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

reference = "The program requires 160 credit hours."
prediction = "Students need to complete 160 credit hours to graduate."

reference_embedding = model.encode(reference)
prediction_embedding = model.encode(prediction)

from sklearn.metrics.pairwise import cosine_similarity

score = cosine_similarity([reference_embedding], [prediction_embedding])[0][0]
print(score)
```

You should expect a relatively high similarity score because the two sentences express essentially the same idea.

## 7. Compare With an Unrelated Answer

Now try `prediction = "The tuition fee is 1330 EGP per credit hour."` Calculate again — the similarity should generally be lower, because the reference discusses graduation credit hours while the prediction discusses tuition cost. These discuss different concepts.

```
Same meaning
     ↓
Higher semantic similarity


Different meaning
     ↓
Lower semantic similarity
```

## 8. But Semantic Similarity Is Not Perfect

This is extremely important. You might think "great, we can just use semantic similarity for everything." **No.** Semantic similarity measures similarity of *meaning*, but similar meaning doesn't necessarily mean correctness.

Consider: reference "The program requires 160 credit hours." AI "The program requires 180 credit hours." These sentences are very similar semantically — both talking about *program + required credit hours*. An embedding-based metric might give them a relatively high similarity score. But `160 ≠ 180` — the AI answer is factually wrong.

This is one of the most important limitations of semantic similarity.

## 9. Semantic Similarity Can Miss Small but Critical Errors

Expected: "The fee is 1330 EGP." AI: "The fee is 1500 EGP." The difference is only one number. Semantically, the sentences are extremely similar. But from an engineering perspective, 1330 is correct and 1500 is wrong — a critical error. Therefore: **high semantic similarity does not guarantee factual correctness.**

## 10. Exact Match vs Semantic Similarity

| Expected | AI Output | Exact Match | Semantic Similarity |
|---|---|---|---|
| 160 | 160 | High | High |
| 160 credit hours | The program requires 160 credit hours. | Low/0 | High |
| 160 credit hours | 180 credit hours | 0 | Potentially high |
| 160 credit hours | Tuition is 1330 EGP. | 0 | Low |

Exact Match is good at detecting exact textual equality. Semantic Similarity is good at detecting similar meaning. **Neither one completely answers "is this answer factually correct?"** That's why we'll need additional evaluation techniques.

## 11. Thresholds

Often we convert a similarity score into a decision:

```
if score >= 0.80:
    print("Semantically similar")
else:
    print("Semantically different")
```

But be careful with the number `0.80` — it is **not a universal threshold**. The appropriate threshold depends on the embedding model, dataset, domain, type of questions, language, expected answer length, and evaluation objective. For your Arabic RAG system, you should not blindly assume that `0.80 = correct`. Instead, you would calibrate a threshold using a labeled evaluation dataset.

## 12. Threshold Calibration

Imagine you manually label 100 answer pairs as "correct semantic match → 1" or "incorrect semantic match → 0", then calculate similarity for each pair. You might discover something like:

```
0.90+     → Usually equivalent
0.75–0.90 → Mixed
<0.75     → Usually different
```

These numbers are only illustrative. You could then choose a threshold based on the actual behavior of your dataset — much better than randomly choosing `threshold = 0.8`.

## 13. Semantic Similarity for RAG

Question: "How many credit hours are required for graduation?" Reference: "The program requires 160 credit hours." RAG output: "Students must complete 160 credit hours to graduate." Semantic similarity: **high ✅**. This gives us evidence that the generated answer is semantically close to the reference. But we still need to ask: *is it actually supported by the retrieved context?* That's a different question.

## 14. Three Different Questions

This is a very important mental model. Given reference "The program requires 160 credit hours." and AI "Students need 160 credit hours to graduate.":

- **Question 1** — Are the texts semantically similar? → **Semantic Similarity**
- **Question 2** — Is the AI answer supported by the retrieved evidence? → **Faithfulness**
- **Question 3** — Is the answer actually correct? → potentially requires ground truth, human verification, LLM-as-a-Judge, or other task-specific metrics.

```
Semantic Similarity
        ↓
"Does it mean something similar?"

Faithfulness
        ↓
"Is it supported by the evidence?"

Correctness
        ↓
"Is the information actually right?"
```

These are different evaluation questions.

## 15. Why This Matters for Your Arabic RAG

Imagine your assistant receives "ما تكلفة الساعة المعتمدة؟" with expected answer "تكلفة الساعة المعتمدة هي 1330 جنيهًا." and AI answer "سعر الساعة المعتمدة يبلغ 1330 جنيه مصري." Exact Match: `0`. Semantic Similarity: **high**. That's useful because Arabic answers can have many valid formulations — different wording, same essential meaning. This is one reason semantic evaluation can be particularly useful for natural-language systems.

## 16. But Language Matters

Embedding quality depends on the embedding model. For Arabic evaluation, you should prefer an embedding model with strong Arabic/multilingual semantic representation rather than assuming every English-focused model will perform equally well. You already have experience with multilingual embedding models — the same principle applies here: **the evaluation model is itself part of the evaluation system.** Changing the embedding model can change your scores. Therefore, document which model you use:

```
EVAL_EMBEDDING_MODEL = "your-multilingual-model"
```

Then keep it consistent when comparing system versions.

## 17. A Simple Evaluation Function

```
def semantic_similarity(reference, prediction, model):
    ref_embedding = model.encode(reference)
    pred_embedding = model.encode(prediction)

    return cosine_similarity([ref_embedding], [pred_embedding])[0][0]
```

Then:

```
score = semantic_similarity(reference, prediction, model)
print(score)
```

Now your evaluation pipeline can produce:

```
Question
   ↓
RAG System
   ↓
Prediction
   ↓
Semantic Similarity
   ↓
Score
```

## 18. Don't Turn Every Metric Into "Accuracy"

Another common mistake is saying "Semantic Similarity = 87%" and interpreting it as "the AI is 87% accurate." That's misleading. Instead say something like "the average semantic similarity score was 0.87 using model X." Why? Because the score is specific to the metric, the embedding model, the dataset, and the implementation. Different evaluation systems can produce different scores.

## 19. Combining Exact Match and Semantic Similarity

A practical evaluation system might use both — Exact Match for structured questions, Semantic Similarity for natural-language answers. You could even report both: `Exact Match: 72%`, `Semantic Similarity: 0.89`. Now you have more information than either metric alone.

## 20. The Big Picture

```
Exact Match
     ↓
"Is the text exactly the same?"

Semantic Similarity
     ↓
"Is the meaning similar?"
```

And later we'll ask **Faithfulness** ("is the answer supported by evidence?") and **Answer Relevance** ("does the answer actually address the question?"). These metrics measure different properties. That is the foundation of serious AI evaluation.

## Short Summary

Semantic Similarity compares the meaning of two texts using representations such as embeddings. It is useful because different sentences can express the same idea. But it has an important limitation: **semantically similar does not necessarily mean factually correct** — "160 credit hours" vs "180 credit hours" are semantically related but the answer is wrong.

**Key takeaway: Exact Match evaluates textual equality; Semantic Similarity evaluates meaning similarity. Neither one alone proves that an AI answer is factually correct. For AI engineering, always ask: "What property of the system does this metric actually measure?"**""",
                "estimated_minutes": 35,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Predict Exact Match vs Semantic Similarity Across Three Cases",
                    "description": """Consider these three cases, all with the same expected answer: "The program requires 160 credit hours."

Case A — AI: "Students must complete 160 credit hours to graduate."
Case B — AI: "The program requires 180 credit hours."
Case C — AI: "The tuition fee is 1330 EGP per credit hour."

For each case, answer:

1. Would Exact Match be high or low?
2. Would Semantic Similarity likely be high or low?
3. Is the AI answer actually correct?
4. What does this teach you about the limitations of Semantic Similarity?""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "semantic-similarity", "metric-limitations"],
                },
                {
                    "title": "Build a Semantic Similarity Evaluator",
                    "description": """Using `sentence-transformers` and `sklearn`, write a function `semantic_similarity(reference, prediction, model)` that encodes both texts and returns their cosine similarity score.

Then write `classify_similarity(score, threshold=0.80)` that returns `"Semantically similar"` if `score >= threshold`, else `"Semantically different"`.

Finally, run both functions on this pair and print the score and classification:

```
reference = "The program requires 160 credit hours."
prediction = "Students need to complete 160 credit hours to graduate."
```""",
                    "starter_code": """from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def semantic_similarity(reference, prediction, model):
    # TODO: encode both texts and return cosine similarity
    pass


def classify_similarity(score, threshold=0.80):
    # TODO: return "Semantically similar" or "Semantically different"
    pass


reference = "The program requires 160 credit hours."
prediction = "Students need to complete 160 credit hours to graduate."

# TODO: compute score, print it, and print the classification
""",
                    "solution_code": """from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def semantic_similarity(reference, prediction, model):
    ref_embedding = model.encode(reference)
    pred_embedding = model.encode(prediction)
    return cosine_similarity([ref_embedding], [pred_embedding])[0][0]


def classify_similarity(score, threshold=0.80):
    return "Semantically similar" if score >= threshold else "Semantically different"


reference = "The program requires 160 credit hours."
prediction = "Students need to complete 160 credit hours to graduate."

score = semantic_similarity(reference, prediction, model)
print(score)
print(classify_similarity(score))
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "semantic-similarity", "embeddings", "python"],
                },
            ],
            "quiz": {
                "title": "Semantic Similarity — Knowledge Check",
                "questions": [
                    {
                        "question": "Reference: 'The course has 3 credit hours.' AI: 'This course carries three credit hours.' What would Exact Match and Semantic Similarity most likely show, respectively?",
                        "options": [
                            "Exact Match: high, Semantic Similarity: low",
                            "Exact Match: low/0, Semantic Similarity: high",
                            "Both would be low",
                            "Both would be high",
                        ],
                        "correct": 1,
                        "explanation": "The strings differ so Exact Match is 0, but the meaning is the same, so embeddings for both sentences would be close together, giving high Semantic Similarity — exactly the motivating example from the lesson.",
                    },
                    {
                        "question": "Reference: 'The program requires 160 credit hours.' AI: 'The program requires 180 credit hours.' What is the key lesson from this example?",
                        "options": [
                            "Semantic Similarity would be low because the numbers differ",
                            "Semantic Similarity could be relatively high even though the answer is factually wrong, showing that high semantic similarity does not guarantee correctness",
                            "Exact Match would correctly catch this error, making Semantic Similarity unnecessary",
                            "This proves Semantic Similarity should never be used for numeric answers",
                        ],
                        "correct": 1,
                        "explanation": "Both sentences discuss the same topic (program + required credit hours) so an embedding model may score them as similar despite 160 ≠ 180 — this is the lesson's central warning about semantic similarity's limitation.",
                    },
                    {
                        "question": "Why does the lesson caution against blindly using a threshold like 0.80 to decide 'semantically similar' vs 'semantically different'?",
                        "options": [
                            "Because cosine similarity scores are always exactly 0 or 1, so no threshold is needed",
                            "Because the appropriate threshold depends on the embedding model, dataset, domain, and language, so it should be calibrated against a labeled evaluation dataset rather than assumed",
                            "Because 0.80 is too low and should always be replaced with 0.95",
                            "Because thresholds only apply to Exact Match, not Semantic Similarity",
                        ],
                        "correct": 1,
                        "explanation": "The lesson is explicit that 0.80 is not a universal threshold — it depends on the embedding model, dataset, domain, and more, and should be calibrated using manually labeled answer pairs rather than picked arbitrarily.",
                    },
                    {
                        "question": "According to the lesson's 'three different questions' mental model, which evaluation question does Semantic Similarity answer, as opposed to Faithfulness or Correctness?",
                        "options": [
                            "Semantic Similarity answers 'is the answer supported by the retrieved evidence?'",
                            "Semantic Similarity answers 'does it mean something similar to the reference?' — a different question from whether it's evidence-supported (Faithfulness) or actually right (Correctness)",
                            "Semantic Similarity answers 'is the information actually right?'",
                            "All three questions are answered identically by Semantic Similarity",
                        ],
                        "correct": 1,
                        "explanation": "The lesson separates these explicitly: Semantic Similarity → 'does it mean something similar?', Faithfulness → 'is it supported by the evidence?', Correctness → 'is the information actually right?'",
                    },
                    {
                        "question": "Why does the lesson recommend documenting which embedding model was used (e.g. EVAL_EMBEDDING_MODEL) and keeping it consistent across evaluations?",
                        "options": [
                            "Because embedding models are interchangeable and documentation is just a formality",
                            "Because the evaluation model is itself part of the evaluation system — changing it can change the similarity scores, making comparisons across system versions unreliable if the model isn't held constant",
                            "Because only Arabic embedding models require documentation",
                            "Because embedding models are deprecated after each use and must be re-selected every time",
                        ],
                        "correct": 1,
                        "explanation": "The lesson states this directly: the evaluation model is part of the evaluation system, and changing the embedding model can change your scores — so it should be documented and kept consistent when comparing versions.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "LLM-as-a-Judge",
            "slug":              "ai-developer-ai-evaluation-observability-llm-as-a-judge",
            "description":       "Use one LLM to evaluate another AI system's output on open-ended criteria (relevance, faithfulness, correctness, completeness) using structured rubrics and pairwise comparison, and why a judge's score is an evaluation signal — never ground truth.",
            "order":             5,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "llm-as-a-judge", "rubrics"],
            "prerequisite_ids":  [],  # builds on "Exact Match" and "Semantic Similarity" (this level, topics 3-4)
            "lesson": {
                "title": "LLM-as-a-Judge",
                "content": """We've seen two important limitations: **Exact Match** checks whether text is exactly the same, and **Semantic Similarity** checks whether two texts have similar meaning. But neither fully answers questions like *"is this answer actually good?"* For open-ended AI systems, we often need a more flexible evaluator. That's where **LLM-as-a-Judge** comes in.

## 1. What Is LLM-as-a-Judge?

LLM-as-a-Judge means using one LLM to evaluate the output of another AI system. Instead of:

```
User
 ↓
AI System
 ↓
Answer
```

we add an evaluator:

```
User
 ↓
AI System
 ↓
Answer
 ↓
Judge LLM
 ↓
Evaluation
```

The judge might receive the question, reference answer, AI answer, and retrieved context, and determine whether the answer is good.

## 2. Why Use an LLM as a Judge?

Because many AI outputs don't have one exact correct string. Consider: question "How many credit hours are required for graduation?" reference "160 credit hours." AI "Students need to complete a total of 160 credit hours before they can graduate." Exact Match: `0 ❌`. Semantic Similarity: `High ✅`. But an evaluator can reason: *"the answer correctly states the required number of credit hours and directly answers the question."* So the judge could give **Score: 5/5**. This makes LLM-as-a-Judge particularly useful for open-ended generation.

## 3. The Mental Model

Think of the judge as another evaluator in your pipeline:

```
                Evaluation
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
  Exact Match   Embeddings    Judge LLM
       ↓            ↓            ↓
   Textual       Semantic      Quality
   equality      similarity    judgment
```

The judge is trying to evaluate higher-level properties such as **correctness**, **relevance**, **completeness**, **style**, and **faithfulness**, depending on the criteria you give it.

## 4. A Simple Example

Question: "What is the cost of one credit hour?" Context: "The cost of one credit hour is 1330 EGP." Answer: "One credit hour costs 1330 EGP." We can ask another LLM to evaluate whether the answer is supported by the context. The judge might return:

```
{
    "score": 5,
    "reason": "The answer directly matches the information in the context."
}
```

## 5. Judge Criteria Matter

This is one of the most important concepts. If you simply ask "is this answer good?" you haven't defined *good*. The judge has to determine what you're asking it to evaluate. Instead, define explicit criteria — for example: evaluate the answer for relevance, correctness, faithfulness to the provided context, and completeness, giving each criterion a score from 1 to 5. Now the judge has a much clearer task.

## 6. A Better Judge Prompt

For a RAG system, we could create something like:

```
judge_prompt = \"\"\"
You are an AI evaluation judge.

Evaluate the following answer.

Question:
{question}

Retrieved Context:
{context}

Answer:
{answer}

Evaluate:

1. Relevance:
Does the answer directly address the question?

2. Faithfulness:
Is every factual claim supported by the context?

3. Correctness:
Does the answer correctly answer the question?

4. Completeness:
Does it include the important information needed?

Return a score from 1 to 5 for each criterion.
\"\"\"
```

The important idea isn't the exact wording. It's: **define what the judge should measure.**

## 7. Structured Judge Output

Don't ask the judge for a giant paragraph if you want to analyze results programmatically. Prefer structured output:

```
{
    "relevance": 5,
    "faithfulness": 5,
    "correctness": 5,
    "completeness": 4
}
```

You could also include a short explanation:

```
{
    "relevance": 5,
    "faithfulness": 5,
    "correctness": 5,
    "completeness": 4,
    "reason": "The answer correctly identifies the required credit hours but does not explain additional graduation requirements."
}
```

Now Python can easily process the result.

## 8. Why Scoring Rubrics Matter

Suppose you ask a judge to score from 1–5. What does a `3` mean? If you haven't defined it, different evaluations can become inconsistent. A better rubric:

```
5 = Excellent   — Fully correct, relevant, grounded, and complete.
4 = Good        — Mostly correct with minor issues.
3 = Acceptable  — Partially correct but has noticeable weaknesses.
2 = Poor        — Significant errors or missing information.
1 = Very poor   — Incorrect, irrelevant, or unsupported.
```

Now the judge has a reference for its decisions. This is called a **rubric**.

## 9. Pairwise Evaluation

LLM judges don't always have to assign an absolute score. Another useful method is **pairwise comparison**. Suppose you have Answer A: "The program requires 160 credit hours." and Answer B: "Students must complete 160 credit hours and satisfy the required curriculum before graduation." Ask "which answer is better?" The judge could return:

```
{
    "winner": "B",
    "reason": "B provides more complete information while remaining relevant."
}
```

This is called **pairwise evaluation**.

## 10. Why Pairwise Comparison Can Be Useful

Sometimes it's easier to answer "which is better?" than "what exact score does this deserve?" Deciding "Version A → 4.2? Version B → 4.5?" is difficult to judge consistently, but "A vs B → B is better" can be easier. This is particularly useful when comparing Prompt V1 vs V2, Model A vs Model B, or RAG pipeline A vs B.

## 11. But the Judge Is NOT Ground Truth

This is probably the most important warning in this lesson. An LLM judge is itself an AI system:

```
AI System
    ↓
Answer
    ↓
Judge LLM
    ↓
Score
```

The judge can be wrong. You must not assume "judge says 5, therefore the answer is definitely correct." Instead: "judge says 5" is **evidence** that the answer appears good. The judge is an evaluation tool, not an unquestionable authority.

## 12. Judge Bias

LLM judges can exhibit biases. They might prefer **longer answers**, thinking "this answer explains more, so it's better" — even when the extra length is unnecessary. They might prefer **more detailed answers** over a perfectly correct concise one like "160 credit hours." They might also prefer **certain writing styles or tones**, which doesn't necessarily mean the answer is objectively better.

## 13. Position Bias in Pairwise Evaluation

Suppose we ask "which answer is better, A or B?" The judge may sometimes favor the answer appearing first. So we can evaluate both orders — A vs B, and B vs A. If the judge says "A wins in A vs B" but "B wins in B vs A," the judge may be inconsistent. This is one reason evaluation should be designed carefully.

## 14. Judge Consistency

Suppose we evaluate the same answer twice: Evaluation 1 → 5, Evaluation 2 → 3. That's concerning. A good evaluation system should investigate judge consistency by measuring agreement between repeated judgments, agreement with human evaluators, agreement across different judges, and stability across prompt variations. The important mindset now is: **a judge's output should itself be validated.**

## 15. Human Evaluation Still Matters

LLM judges are useful, but humans remain important. Imagine your system is used for medical decisions, legal information, financial advice, academic policy, or safety-critical systems — you may need human review for important cases. A useful hierarchy is:

```
Automated Metrics
       ↓
LLM Judge
       ↓
Human Evaluation
```

Not every case needs a human, but automated evaluation should not eliminate human oversight where the stakes are high.

## 16. LLM-as-a-Judge for RAG

Question: "How many credit hours are required?" Context: "The program requires 160 credit hours." Answer: "The program requires 180 credit hours." The judge can evaluate: **Relevance** — the answer addresses the question → High. **Faithfulness** — the answer says 180, but the context says 160 → Low. **Correctness** — the answer is wrong → Low. This demonstrates why multiple criteria are useful — a single "good/bad" would hide the reason for failure.

## 17. Another RAG Example

Context: "The program requires 160 credit hours." Answer: "The program requires 160 credit hours. The tuition is 1330 EGP per credit hour." Suppose the tuition information is not in the provided context. The answer may be: Relevance → High, Correctness → potentially high, Faithfulness → Low. The judge can help identify this distinction — connecting directly to upcoming lessons on Faithfulness, Answer Relevance, and Context Relevance.

## 18. A Simple Python Architecture

```
def evaluate_with_llm_judge(question, context, answer):
    prompt = f\"\"\"
    Evaluate the answer.

    Question:
    {question}

    Context:
    {context}

    Answer:
    {answer}

    Score:
    - Relevance: 1-5
    - Faithfulness: 1-5
    - Correctness: 1-5
    \"\"\"

    result = call_llm(prompt)
    return result
```

Notice something important: we're separating the **AI System** from the **Evaluation System**. That separation is a good engineering practice.

## 19. Judge Model Selection

The judge itself needs to be chosen carefully. The system under test might use Model A, while the judge uses Model B — they don't necessarily have to be the same model. For example: production model → small/cheap model, judge → stronger model, since the judge may need stronger reasoning capabilities than the system being evaluated. But there is a trade-off: a better judge means potentially better evaluation, but also higher cost and higher latency. Judge selection is itself an engineering decision.

## 20. The Judge Can Also Hallucinate

Suppose the context says "The program requires 160 credit hours" and the answer says "The program requires 180 credit hours." A poorly designed judge might incorrectly say "the answer is consistent with the context." That's a judge failure. Therefore: **don't blindly trust automated evaluation — evaluation systems need testing too.**

## 21. Best Practice: Use Multiple Signals

A strong evaluation pipeline doesn't necessarily rely on only one evaluator:

```
                   AI Evaluation
                        │
       ┌────────────────┼────────────────┐
       ↓                ↓                ↓
 Exact Match    Semantic Similarity   LLM Judge
       │                │                │
       └────────────────┼────────────────┘
                        ↓
                  Overall Analysis
```

For RAG, you might eventually combine retrieval metrics, semantic similarity, LLM judge, and human evaluation. Each gives a different perspective.

## 22. The Most Important Mental Model

Remember: **LLM-as-a-Judge is another AI system making an evaluation, not an oracle that knows the truth.** So:

```
AI Output
   ↓
Judge
   ↓
Score
```

does **not** mean "AI Output → Judge → Absolute Truth." Instead: "AI Output → Judge → **Evaluation Signal**." That distinction will protect you from building unreliable evaluation pipelines.

## Short Summary

LLM-as-a-Judge uses an LLM to evaluate another AI system's output. It is useful for evaluating things that are difficult to measure with exact string matching, such as correctness, relevance, faithfulness, completeness, and writing quality. Good judge design requires clear criteria, explicit rubrics, structured outputs, consistent scoring, bias awareness, and validation against human judgments. LLM judges can be wrong and biased, so **never treat the judge's score as unquestionable ground truth.**

**Key takeaway: LLM-as-a-Judge gives us a flexible way to evaluate open-ended AI outputs, but the judge itself must be treated as an imperfect measurement instrument. Think of it like a measuring device: before trusting the measurement, you need to understand how reliable the instrument is.**""",
                "estimated_minutes": 40,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Design Judge Criteria for a Faithfulness Failure",
                    "description": """Your RAG system receives:

Question: "What is the cost of one credit hour?"
Retrieved Context: "The cost of one credit hour is 1330 EGP."
AI Answer: "One credit hour costs 1500 EGP."

Imagine you're designing an LLM judge. Answer:

1. What should the judge score for relevance?
2. What should it score for faithfulness?
3. What should it score for correctness?
4. Why is it better to evaluate these dimensions separately rather than simply asking "Is this answer good?"
5. Why shouldn't you automatically assume the judge's score is ground truth?""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "llm-as-a-judge", "rubric-design"],
                },
                {
                    "title": "Build a Structured Judge Prompt and Parser",
                    "description": """Write a function `build_judge_prompt(question, context, answer)` that returns a prompt string asking the judge to score Relevance, Faithfulness, Correctness, and Completeness, each from 1-5, using the rubric from the lesson (5 = Excellent ... 1 = Very poor), and to return the result as JSON with keys `"relevance"`, `"faithfulness"`, `"correctness"`, `"completeness"`, `"reason"`.

Then write `parse_judge_response(response_text)` that safely parses that JSON string into a Python dict (return `None` if parsing fails instead of raising).

You don't need to actually call an LLM — just build and test the prompt construction and parsing logic using a hardcoded example JSON string.""",
                    "starter_code": """import json

def build_judge_prompt(question, context, answer):
    # TODO: return a prompt string with the rubric and JSON output instructions
    pass


def parse_judge_response(response_text):
    # TODO: parse response_text as JSON, return None on failure
    pass


# TODO: test build_judge_prompt with a sample question/context/answer
# TODO: test parse_judge_response with a hardcoded JSON string and with invalid JSON
""",
                    "solution_code": """import json

def build_judge_prompt(question, context, answer):
    return f\"\"\"
You are an AI evaluation judge.

Evaluate the following answer using this rubric for each criterion (1-5):
5 = Excellent, 4 = Good, 3 = Acceptable, 2 = Poor, 1 = Very poor

Question:
{question}

Retrieved Context:
{context}

Answer:
{answer}

Evaluate:
1. Relevance: Does the answer directly address the question?
2. Faithfulness: Is every factual claim supported by the context?
3. Correctness: Does the answer correctly answer the question?
4. Completeness: Does it include the important information needed?

Return ONLY JSON with keys: relevance, faithfulness, correctness, completeness, reason.
\"\"\"


def parse_judge_response(response_text):
    try:
        return json.loads(response_text)
    except (json.JSONDecodeError, TypeError):
        return None


prompt = build_judge_prompt(
    "What is the cost of one credit hour?",
    "The cost of one credit hour is 1330 EGP.",
    "One credit hour costs 1500 EGP.",
)
print(prompt)

good_response = '{"relevance": 5, "faithfulness": 1, "correctness": 1, "completeness": 4, "reason": "Answer contradicts the context value."}'
print(parse_judge_response(good_response))

bad_response = "not valid json"
print(parse_judge_response(bad_response))
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "llm-as-a-judge", "python"],
                },
            ],
            "quiz": {
                "title": "LLM-as-a-Judge — Knowledge Check",
                "questions": [
                    {
                        "question": "Question: 'How many credit hours are required?' Reference: '160 credit hours.' AI: 'Students need to complete a total of 160 credit hours before they can graduate.' Exact Match scores this 0. Why might LLM-as-a-Judge still score this answer highly?",
                        "options": [
                            "The judge ignores factual content entirely and only checks sentence length",
                            "The judge can reason about whether the answer correctly and directly addresses the question, rather than requiring exact textual equality",
                            "The judge always agrees with whatever Exact Match says",
                            "LLM-as-a-Judge cannot evaluate this type of open-ended answer",
                        ],
                        "correct": 1,
                        "explanation": "This is the lesson's motivating example: the judge can recognize that the answer correctly states the required credit hours and directly answers the question, giving it a high score (5/5) despite Exact Match scoring 0.",
                    },
                    {
                        "question": "Why does the lesson emphasize giving the judge explicit criteria (e.g. relevance, faithfulness, correctness, completeness) instead of just asking 'is this answer good?'",
                        "options": [
                            "Explicit criteria make the judge run faster",
                            "Without defining what 'good' means, the judge's task is ambiguous and evaluations become inconsistent; explicit criteria and rubrics give it a clearer, more reproducible task",
                            "The judge cannot process more than one question at a time",
                            "Explicit criteria are only needed for pairwise evaluation, not absolute scoring",
                        ],
                        "correct": 1,
                        "explanation": "The lesson states that if you don't define 'good,' the judge has to guess what you're asking it to evaluate, and different evaluations can become inconsistent — a scoring rubric fixes this by defining what each score level means.",
                    },
                    {
                        "question": "In pairwise evaluation, a judge says 'A wins' when compared as (A, B), but says 'B wins' when the same two answers are compared as (B, A). What does this reveal?",
                        "options": [
                            "The judge is functioning correctly since the answers were presented differently",
                            "Position bias — the judge may be favoring whichever answer appears first, rather than judging based on content alone",
                            "Answer A is definitely better since it won when presented first",
                            "Pairwise evaluation should never be used because of this issue",
                        ],
                        "correct": 1,
                        "explanation": "The lesson describes exactly this test: evaluating both orderings (A vs B and B vs A) can reveal position bias if the judge's preference flips based on presentation order rather than content.",
                    },
                    {
                        "question": "Why does the lesson warn 'the judge is NOT ground truth'?",
                        "options": [
                            "Because judges never produce useful scores",
                            "Because the judge is itself an AI system that can be wrong or biased, so its score should be treated as an evaluation signal — evidence the answer appears good — not as unquestionable proof of correctness",
                            "Because only human evaluators can use rubrics",
                            "Because ground truth only applies to Exact Match, not to judges",
                        ],
                        "correct": 1,
                        "explanation": "The lesson is explicit: 'Judge says 5' should be read as evidence the answer appears good, not as 'therefore the answer is definitely correct' — the judge is an imperfect measurement instrument, not an oracle.",
                    },
                    {
                        "question": "The lesson describes a scenario where the context says 160 credit hours, the answer says 180, and a poorly designed judge says 'the answer is consistent with the context.' What does this illustrate?",
                        "options": [
                            "Judges are always accurate and this scenario is unrealistic",
                            "The judge itself can hallucinate or fail, which is why evaluation systems need testing too, and automated evaluation shouldn't be blindly trusted",
                            "This proves LLM-as-a-Judge should never be used for RAG systems",
                            "Faithfulness cannot be evaluated by an LLM judge under any circumstances",
                        ],
                        "correct": 1,
                        "explanation": "This is the lesson's 'the judge can also hallucinate' point: a judge can incorrectly validate a wrong answer, which is why evaluation systems themselves need to be tested and not blindly trusted.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "RAG Evaluation",
            "slug":              "ai-developer-ai-evaluation-observability-rag-evaluation",
            "description":       "Evaluate a RAG pipeline stage by stage instead of as a black box: distinguish retrieval failures from generation failures, build RAG-specific evaluation cases and traces, and understand why a correct final answer can still hide a weak retrieval pipeline.",
            "order":             6,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "rag-evaluation", "debugging"],
            "prerequisite_ids":  [],  # builds on Topics 1-5 of this level, and the RAG pipeline from Level 3: RAG Systems
            "lesson": {
                "title": "RAG Evaluation",
                "content": """Now we combine the evaluation concepts we've learned with something you already know well: **RAG**. The goal is to answer a critical engineering question:

*When a RAG system gives a bad answer, how do we know whether retrieval failed or generation failed?*

## 1. Why RAG Needs Special Evaluation

A normal LLM system can be viewed as:

```
Question
   ↓
LLM
   ↓
Answer
```

But RAG has multiple stages:

```
Question
   ↓
Retriever
   ↓
Retrieved Context
   ↓
LLM
   ↓
Answer
```

Therefore, a bad final answer can have different causes:

```
                    Bad Answer
                        │
              ┌─────────┴─────────┐
              ↓                   ↓
       Retrieval Failure    Generation Failure
              ↓                   ↓
       Wrong context        Correct context
                              but wrong answer
```

If you don't evaluate the stages separately, debugging becomes guesswork.

## 2. The Four Main Evaluation Questions

For a RAG system, we can ask four different questions:

1. **Retrieval** — Did we retrieve the right information?
2. **Context** — Is the retrieved information relevant to the question?
3. **Generation** — Did the LLM correctly use the retrieved information?
4. **Final Answer** — Is the final answer useful, relevant, and correct?

```
Question
   │
   ▼
Retriever
   │
   ├── Evaluate Retrieval
   │
   ▼
Context
   │
   ├── Evaluate Context
   │
   ▼
LLM
   │
   ├── Evaluate Generation
   │
   ▼
Answer
   │
   └── Evaluate Final Answer
```

We'll study the individual metrics more deeply in the next lessons (Faithfulness, Context Relevance, Answer Relevance). For now, focus on the architecture.

## 3. Retrieval Failure

User asks "How many credit hours are required for graduation?" The correct evidence is "The program requires 160 credit hours for graduation." But the retriever returns chunks about tuition cost, registration deadlines, and withdrawal policies. The LLM receives the question plus wrong context, and might answer "the available information does not specify the required credit hours." The problem happened **before** the LLM:

```
Question
   ↓
Retriever ❌
   ↓
Wrong Context
   ↓
LLM
   ↓
Answer
```

This is a **retrieval failure**.

## 4. Generation Failure

Now imagine the retriever works perfectly and retrieves "The program requires 160 credit hours for graduation." The LLM receives this — but generates "The program requires 180 credit hours for graduation."

```
Question
   ↓
Retriever ✅
   ↓
Correct Context
   ↓
LLM ❌
   ↓
Wrong Answer
```

This is a **generation failure**.

## 5. Why This Distinction Matters

Suppose your final answer accuracy is 72%. That's not enough information — you need to ask *why* the remaining 28% is wrong. If retrieval failures are 20% and generation failures are 8%, the engineering decision is obvious: **improve retrieval first**. But if retrieval failures are only 5% and generation failures are 23%, your retrieval system may already be strong — the problem is primarily prompting, model behavior, context handling, generation, or answer formatting. This is why stage-level evaluation is so powerful.

## 6. A RAG Evaluation Dataset

Let's extend the evaluation case from Lesson 2:

```
evaluation_case = {
    "question": "How many credit hours are required for graduation?",
    "expected_answer": "160 credit hours",
    "expected_context": [
        "The program requires 160 credit hours for graduation."
    ]
}
```

Now run the RAG system:

```
result = rag_system(evaluation_case["question"])
```

Suppose it returns:

```
result = {
    "answer": "The program requires 160 credit hours.",
    "retrieved_context": [
        "The program requires 160 credit hours for graduation."
    ]
}
```

Now we have enough information to evaluate both retrieval and generation.

## 7. Evaluation Layer

Conceptually:

```
retrieved = result["retrieved_context"]
answer = result["answer"]

expected_context = evaluation_case["expected_context"]
expected_answer = evaluation_case["expected_answer"]
```

Then:

```
Retrieved Context
       ↓
Retrieval Evaluation

Answer + Context
       ↓
Generation Evaluation

Answer + Expected Answer
       ↓
Answer Evaluation
```

Each evaluation asks a different question.

## 8. Retrieval Evaluation

If the expected evidence is "The program requires 160 credit hours for graduation." and the retriever returns exactly that — retrieval succeeded. If instead the retriever returns "The cost of one credit hour is 1330 EGP." — retrieval failed. The important thing is that we can detect this **even before looking at the final answer.**

## 9. Context Evaluation

Consider retrieved context containing: the correct chunk about 160 credit hours, plus chunks about tuition cost, registration deadlines, and available engineering programs. The first chunk is highly relevant; the others are mostly irrelevant to this question. So context evaluation asks: *how useful is the retrieved context for answering this particular question?* This is slightly different from simply asking whether the correct document exists somewhere in the retrieved results. We'll study **Context Relevance** specifically later.

## 10. Generation Evaluation

Suppose the context is "The program requires 160 credit hours for graduation." but the LLM generates "Students need 180 credit hours." We know something went wrong — the retriever successfully provided the correct information. Therefore: Retrieval → Good, Generation → Bad. This is exactly the kind of distinction an AI engineer needs to make.

## 11. Final Answer Evaluation

Question: "How many credit hours are required?" Context: "The program requires 160 credit hours." Answer: "The program requires 160 credit hours." This is Relevant ✅, Correct ✅, Grounded ✅, Useful ✅. A complete evaluation system should be able to capture these different properties.

## 12. Four Different Failure Scenarios

**Scenario A — Everything works.** Retriever → correct context, LLM → correct answer. Result: Retrieval ✅, Context ✅, Generation ✅, Final answer ✅.

**Scenario B — Retrieval fails.** Retriever → wrong context, LLM → reasonable response based on that context. Result: Retrieval ❌, Context ❌, Generation maybe ✅, Final answer ❌. The LLM might have behaved perfectly given bad information.

**Scenario C — Generation fails.** Retriever → correct context, LLM → incorrect answer. Result: Retrieval ✅, Context ✅, Generation ❌, Final answer ❌.

**Scenario D — Correct answer but poor context.** Retriever returns one relevant chunk plus four irrelevant ones. LLM still produces "160 credit hours." Final answer: correct ✅. But retrieval/context quality is inefficient — unnecessary context can increase token usage, latency, cost, introduce distracting information, and potentially increase hallucination risk. **A system can have a correct answer while still having a poor retrieval pipeline.**

## 13. RAG Evaluation Is Not One Number

This is one of the most important ideas in this lesson. Don't think "RAG Score = 85%" and stop. A better evaluation report might look like:

```
Retrieval Recall:       91%
Context Relevance:      86%
Answer Relevance:       94%
Faithfulness:           89%
Exact Match:            72%
```

Now we can understand the system: retrieval is strong, context is moderate, answer is strong, faithfulness is moderate. This tells you much more than a single score.

## 14. The RAG Evaluation Matrix

| Stage | Main Question | Example |
|---|---|---|
| **Retrieval** | Did we find the right evidence? | Correct chunk retrieved |
| **Context** | Is the evidence relevant? | Retrieved chunk answers the question |
| **Generation** | Did the LLM use it correctly? | No contradiction |
| **Answer** | Is the final response good? | Correct and useful |

Later we'll attach specific metrics to these questions.

## 15. Why "Correct Answer" Alone Is Dangerous

Question: "What is the credit-hour cost?" Actual answer: 1330 EGP. Your RAG system responds "The cost is 1330 EGP." Correct — you might conclude "perfect!" But suppose the retriever actually returned one correct document plus four irrelevant ones (registration rules, graduation requirements, withdrawal policy, academic calendar). That's not necessarily terrible, but if your retriever routinely returns 4 irrelevant chunks for every relevant one, you have a retrieval-quality problem that final-answer accuracy may hide. Evaluation should expose this.

## 16. Debugging With Traces

A useful RAG evaluation record can look like:

```
trace = {
    "question": "...",
    "retrieved_chunks": ["...", "...", "..."],
    "retrieval_scores": [0.91, 0.64, 0.51],
    "answer": "...",
    "evaluation": {
        "retrieval": ...,
        "context_relevance": ...,
        "faithfulness": ...,
        "answer_relevance": ...
    }
}
```

Now when a test fails, you can inspect the entire chain. This idea will become important when we reach **Observability** later.

## 17. The Debugging Workflow

When an answer is wrong, don't immediately change the prompt. Instead:

```
Wrong Answer
     ↓
Inspect Retrieved Context
     ↓
Was the correct evidence retrieved?
     │
   ┌─┴─┐
  NO   YES
  ↓     ↓
Retrieval  Inspect Generation
Failure        ↓
           Did LLM use
           evidence correctly?
                │
              ┌─┴─┐
             NO   YES
             ↓     ↓
         Generation  Investigate
           Failure   other factors
```

This prevents random experimentation.

## 18. Example: Academic RAG

Question: "What is the cost of one credit hour?" Expected evidence: "The cost of one credit hour for the academic year is 1330 EGP."

**Test 1** — Retriever finds correct fee information; LLM answers "The credit hour costs 1330 EGP." Everything looks good.

**Test 2** — Retriever returns graduation requirements, course descriptions, and registration policy; LLM answers "I don't have enough information to answer." Don't blame the LLM immediately — **the retriever failed.**

**Test 3** — Retriever finds correct fee information; LLM answers "The credit hour costs 1500 EGP." Retrieval succeeded — **generation failed.** This distinction tells you where to investigate.

## 19. Evaluation as a Diagnostic System

Evaluation isn't only about producing scores — it is also about diagnosis. Instead of "System score = 80%," you want:

```
System
 │
 ├── Retrieval → 91%
 │
 ├── Context → 84%
 │
 ├── Faithfulness → 76%
 │
 └── Answer relevance → 93%
```

Now you can ask "why is faithfulness only 76%?" That leads to investigation — much more useful than simply celebrating a high overall score.

## 20. A Practical Evaluation Architecture

Eventually, a production-quality RAG evaluation system can look like:

```
                  Evaluation Dataset
                         │
                         ▼
                    RAG Pipeline
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
      Retrieval       Context        Generation
          │              │              │
          ▼              ▼              ▼
   Retrieval Metrics  Relevance     Faithfulness
                                      Relevance
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  Evaluation Report
```

And that report can be used to compare RAG v1 vs RAG v2 vs RAG v3.

## 21. What We Are Building Toward

By the end of this level, you should be able to look at a RAG system and say "the final answer quality decreased," then instead of guessing, investigate: did retrieval degrade? Did context relevance decrease? Did the LLM become less faithful? Did answer relevance decrease? Did the prompt change? Did the model change? **That's AI engineering, not just AI application development.**

## Short Summary

RAG should not be evaluated only by looking at the final answer. We should evaluate Retrieval (did we retrieve the right evidence?), Context (is the evidence relevant?), Generation (did the LLM use the evidence correctly?), and Final Answer (is the response correct, relevant, grounded, and useful?).

The most important debugging distinction is: **correct context + wrong answer → generation failure**; **wrong context + wrong answer → retrieval failure**; and sometimes **correct answer + poor retrieval → the final answer may look good, but the RAG pipeline still has a weakness.**

**Key takeaway: Don't treat RAG as a black box. Evaluate the pipeline stage by stage. When a RAG system fails, your first question shouldn't be "why did the LLM hallucinate?" It should be "did the system retrieve the information it needed?" If the answer is no, changing the prompt won't solve the underlying retrieval problem.**""",
                "estimated_minutes": 40,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Diagnose a RAG Failure Chain",
                    "description": """Consider this RAG scenario:

Question: "What is the cost of one credit hour?"
Expected context: "The cost of one credit hour is 1330 EGP."
Retriever returns: "Students must complete 160 credit hours for graduation."
LLM answers: "The cost of one credit hour is 1500 EGP."

Answer:

1. Did retrieval succeed or fail?
2. Did the LLM receive the correct evidence?
3. Is this primarily a retrieval failure or generation failure?
4. If you were the AI engineer, which component would you investigate first?
5. Why would changing the LLM prompt probably not solve the root problem?""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "rag-evaluation", "failure-analysis"],
                },
                {
                    "title": "Build a RAG Failure Classifier",
                    "description": """Write a function `classify_rag_failure(retrieved_context, expected_context, answer, expected_answer)` that returns one of the strings `"success"`, `"retrieval_failure"`, or `"generation_failure"`, using this logic:

- If `expected_context` (a string) is NOT found as a substring in any string within `retrieved_context` (a list of strings) → `"retrieval_failure"`.
- Else if `answer` does not contain `expected_answer` as a substring → `"generation_failure"`.
- Else → `"success"`.

Test it against the three scenarios from section 18 of the lesson (Test 1, 2, and 3) and print the classification for each.""",
                    "starter_code": """def classify_rag_failure(retrieved_context, expected_context, answer, expected_answer):
    # TODO: implement the classification logic described above
    pass


# Test 1: retrieval succeeds, generation succeeds
test_1 = classify_rag_failure(
    ["The cost of one credit hour for the academic year is 1330 EGP."],
    "1330 EGP",
    "The credit hour costs 1330 EGP.",
    "1330",
)

# Test 2: retrieval fails
test_2 = classify_rag_failure(
    ["Graduation requirements...", "Course descriptions...", "Registration policy..."],
    "1330 EGP",
    "I don't have enough information to answer.",
    "1330",
)

# Test 3: retrieval succeeds, generation fails
test_3 = classify_rag_failure(
    ["The cost of one credit hour for the academic year is 1330 EGP."],
    "1330 EGP",
    "The credit hour costs 1500 EGP.",
    "1330",
)

print(test_1, test_2, test_3)
""",
                    "solution_code": """def classify_rag_failure(retrieved_context, expected_context, answer, expected_answer):
    context_found = any(expected_context in chunk for chunk in retrieved_context)
    if not context_found:
        return "retrieval_failure"

    if expected_answer not in answer:
        return "generation_failure"

    return "success"


test_1 = classify_rag_failure(
    ["The cost of one credit hour for the academic year is 1330 EGP."],
    "1330 EGP",
    "The credit hour costs 1330 EGP.",
    "1330",
)

test_2 = classify_rag_failure(
    ["Graduation requirements...", "Course descriptions...", "Registration policy..."],
    "1330 EGP",
    "I don't have enough information to answer.",
    "1330",
)

test_3 = classify_rag_failure(
    ["The cost of one credit hour for the academic year is 1330 EGP."],
    "1330 EGP",
    "The credit hour costs 1500 EGP.",
    "1330",
)

print(test_1, test_2, test_3)
# Expected: success retrieval_failure generation_failure
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "rag-evaluation", "python"],
                },
            ],
            "quiz": {
                "title": "RAG Evaluation — Knowledge Check",
                "questions": [
                    {
                        "question": "A RAG system's retriever returns chunks about tuition, registration, and withdrawal policy — none containing the graduation credit-hour requirement. The LLM then says 'I don't have enough information to answer.' What kind of failure is this?",
                        "options": [
                            "Generation failure, because the LLM should have guessed the answer anyway",
                            "Retrieval failure, because the wrong context reached the LLM before generation even happened",
                            "Final answer failure only, with no clear stage attribution possible",
                            "This is not a failure at all since the LLM was honest about not knowing",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's Scenario B / Test 2 example: when the retriever fails to surface the correct evidence, the problem happens before the LLM even generates a response — this is a retrieval failure.",
                    },
                    {
                        "question": "Why does the lesson insist that a single 'RAG Score = 85%' is not enough, recommending instead a breakdown like Retrieval Recall, Context Relevance, Answer Relevance, and Faithfulness?",
                        "options": [
                            "Because a single score is mathematically impossible to compute for RAG systems",
                            "Because a single aggregate score hides which specific stage is weak, while a breakdown lets you diagnose exactly where to focus improvement effort (e.g. faithfulness at only 76%)",
                            "Because Exact Match should always be reported instead of any other metric",
                            "Because RAG systems cannot be evaluated numerically at all",
                        ],
                        "correct": 1,
                        "explanation": "The lesson makes this the central point of section 13 and 19: an aggregate score doesn't tell you why the system underperforms, while a stage-by-stage breakdown turns evaluation into a diagnostic tool.",
                    },
                    {
                        "question": "In Scenario D, the retriever returns one relevant chunk and four irrelevant chunks, yet the LLM still produces the correct final answer. What does this scenario teach?",
                        "options": [
                            "A correct final answer always means the retrieval pipeline is optimal",
                            "A system can have a correct final answer while still having an inefficient or poor-quality retrieval pipeline, which final-answer accuracy alone would hide",
                            "Irrelevant chunks always cause incorrect final answers",
                            "This scenario is impossible in practice",
                        ],
                        "correct": 1,
                        "explanation": "Scenario D explicitly shows a correct answer despite mostly irrelevant retrieved context — the lesson notes this can still increase cost, latency, and hallucination risk even though the final answer looks fine.",
                    },
                    {
                        "question": "According to the lesson's debugging workflow, what should you check FIRST when a RAG system produces a wrong answer?",
                        "options": [
                            "Immediately rewrite the LLM prompt",
                            "Whether the correct evidence was retrieved at all, before investigating whether the LLM used that evidence correctly",
                            "Switch to a completely different LLM model",
                            "Assume it's a generation failure and adjust temperature settings",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's debugging workflow (section 17) starts with inspecting the retrieved context first — was the correct evidence retrieved? — before moving on to evaluate generation, to avoid random experimentation.",
                    },
                    {
                        "question": "Why does the lesson warn against concluding 'perfect!' just because a RAG system's final answer happens to be correct?",
                        "options": [
                            "Because correct answers are always a coincidence in RAG systems",
                            "Because a correct final answer can coexist with a retriever that routinely returns mostly irrelevant chunks — a retrieval-quality problem that final-answer accuracy alone would mask",
                            "Because correctness should never be evaluated in RAG systems",
                            "Because the LLM is always the source of correctness regardless of retrieval quality",
                        ],
                        "correct": 1,
                        "explanation": "Section 15 gives this exact example: a correct answer with a retriever that returns 4 irrelevant chunks per relevant one still has a retrieval-quality problem, which is why evaluation must look beyond just the final answer.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "Retrieval Metrics",
            "slug":              "ai-developer-ai-evaluation-observability-retrieval-metrics",
            "description":       "Quantify retriever quality directly: Recall, Precision, Hit Rate@K, Recall@K, Precision@K, MRR, and NDCG — what question each metric answers, the recall/precision trade-off as K increases, and why higher retrieval metrics don't always translate into better final answers.",
            "order":             7,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "retrieval-metrics", "rag-evaluation"],
            "prerequisite_ids":  [],  # builds on "RAG Evaluation" (this level, topic 6) and retrieval techniques from earlier levels
            "lesson": {
                "title": "Retrieval Metrics",
                "content": """In the previous lesson, we learned where RAG can fail. Now we need to answer: *how do we measure whether our retriever is actually good?* This is the purpose of **retrieval metrics**.

## 1. What Are Retrieval Metrics?

Retrieval metrics measure the quality of the documents/chunks returned by your retriever. Your RAG pipeline contains:

```
Question
   ↓
Retriever
   ↓
Top-K Documents
   ↓
LLM
```

Before evaluating the LLM, we can evaluate the retriever itself. The fundamental question is: **did the retriever find the information needed to answer the question?**

## 2. The Simplest Example

Suppose the user asks "How many credit hours are required for graduation?" We know the correct chunk is Chunk 7: "The program requires 160 credit hours for graduation." Our retriever returns Top-5:

```
1. Chunk 12 — Tuition fees
2. Chunk 7  — Graduation requirements
3. Chunk 19 — Registration rules
4. Chunk 3  — Course descriptions
5. Chunk 25 — Withdrawal policy
```

The correct chunk appears in the results — retrieval was successful. But now imagine the correct chunk isn't present at all in the Top-5. That's a **retrieval failure**.

## 3. The Most Important Retrieval Concepts

```
                    Retrieval Quality
                          │
             ┌────────────┼────────────┐
             ↓            ↓            ↓
           Recall      Precision      Rank
             │            │            │
             ↓            ↓            ↓
        Did we find?   How much is   How high
                       relevant?     did it appear?
```

For today's lesson, we'll focus on **Recall**, **Precision**, **Hit Rate/Recall@K**, **Precision@K**, **MRR**, and **NDCG**. The formulas are useful, but the question each metric answers is more important.

## 4. Recall

Recall asks: *"Did we retrieve the relevant information that exists?"* Imagine there are 10 relevant documents in the entire database, and our retriever finds 8 of them. Then:

```
Recall = 8 / 10 = 80%
```

The general formula:

```
Recall =
Relevant items retrieved
────────────────────────
All relevant items
```

## 5. Why Recall Matters in RAG

Imagine a university database contains 1000 chunks. For a particular question, there are actually 3 chunks containing the necessary information. Your retriever returns Top-5 and finds 2 of the 3:

```
Recall = 2 / 3 = 66.7%
```

This means the retriever found most, but not all, of the relevant evidence — which can matter especially for questions requiring multiple pieces of information.

## 6. Recall@K

In RAG, we frequently care about the top K retrieved results. So instead of asking "did the retriever find the relevant document somewhere?" we ask "did the retriever find it within the top K results?" This is **Recall@K**. For example, Recall@5 means: how much relevant information was retrieved within the top 5 results?

## 7. Simple Example of Recall@5

Suppose the correct chunks are `{2, 7, 9}`. Our Top-5 retrieval is `[1, 2, 4, 7, 12]`. We retrieved `2` and `7` — 2 out of 3 relevant chunks. Therefore:

```
Recall@5 = 2 / 3 = 66.7%
```

## 8. Hit Rate

For many RAG applications, we don't necessarily need all relevant chunks — sometimes we simply care "did we retrieve at least one relevant chunk?" This is often called **Hit Rate@K**. If relevant chunk = 7, and Top-5 is `[12, 3, 7, 19, 25]`, the correct chunk is present, so `Hit Rate@5 = 1`. If Top-5 were `[12, 3, 19, 25, 31]`, then `Hit Rate@5 = 0`.

## 9. Hit Rate vs Recall

These sound similar, but they're not identical. Suppose relevant = `{2, 7, 9}` and the retriever returns `[1, 2, 4, 7, 12]`. **Hit Rate@5**: at least one relevant chunk was found → `1`. **Recall@5**: two of the three were found → `2/3 = 66.7%`.

```
Hit Rate → Did we find ANY relevant information?
Recall   → How much of the relevant information did we find?
```

This distinction is very useful.

## 10. Precision

Now the opposite question: Precision asks *"of the things we retrieved, how many were relevant?"* Suppose we retrieve 5 chunks, 3 relevant and 2 irrelevant:

```
Precision = 3 / 5 = 60%
```

The formula:

```
Precision =
Relevant retrieved items
────────────────────────
Total retrieved items
```

## 11. Precision@K

Precision@K = how many of the top K results are relevant? Suppose Top-5 is `[Relevant, Relevant, Irrelevant, Irrelevant, Relevant]` — relevant = 3, retrieved = 5:

```
Precision@5 = 3 / 5 = 60%
```

## 12. Recall vs Precision

This distinction is extremely important. **Recall** — did we find the information we needed? **Precision** — how much of what we retrieved was useful?

```
Recall
  ↓
Don't miss important information.


Precision
  ↓
Don't retrieve too much irrelevant information.
```

## 13. RAG Example

Suppose your retriever returns 10 chunks: 8 relevant, 2 irrelevant. `Precision = 8/10 = 80%` — very good. But suppose there were actually 12 relevant chunks in the database: `Recall = 8/12 = 66.7%`. So Precision → 80%, Recall → 66.7%. The system retrieved mostly useful things, but it missed many relevant pieces of information.

## 14. Why Top-K Matters

You might think "I'll just increase K" — from Top-5 to Top-20. You may increase recall, but you can also introduce more irrelevant information. Example: Top-5 has 4 relevant / 1 irrelevant → Precision = 80%. Top-20 has 8 relevant / 12 irrelevant → Precision = 40%. So increasing K can produce Recall ↑, Precision ↓. This is a classic retrieval trade-off.

## 15. Why This Matters for Your RAG Pipeline

You previously worked with BM25, Dense Retrieval, Hybrid Search, RRF, Reranking, and Top-K. Now you can evaluate whether those techniques actually improve retrieval. For example:

```
Dense Retrieval     Recall@5 = 78%
BM25                Recall@5 = 74%
Hybrid Search       Recall@5 = 87%
```

Now we have evidence that hybrid search improved retrieval on this dataset — much better than saying "hybrid search seems better."

## 16. MRR — Mean Reciprocal Rank

Now we care about *where* the correct result appears. If the correct document appears at Rank 1, that's excellent. If it appears at Rank 5, that's less useful because the LLM may only receive the first few results. **MRR** measures how high the first relevant result appears. For one query, Reciprocal Rank = 1/rank:

```
Rank 1 → 1/1 = 1.0
Rank 2 → 1/2 = 0.5
Rank 3 → 1/3 ≈ 0.333
Rank 5 → 1/5 = 0.2
```

Higher is better.

## 17. Why Rank Matters

Retriever A finds the relevant chunk at rank 1 (with 4 irrelevant results after it). Retriever B finds the same relevant chunk at rank 4. Both found the correct document — but Retriever A is much better for a Top-1 or Top-2 pipeline. MRR captures this difference.

## 18. MRR Across Multiple Questions

Suppose we have three questions, with the relevant document found at ranks 1, 2, and 4 respectively. Reciprocal ranks: `1.0`, `0.5`, `0.25`. Average:

```
MRR = (1.0 + 0.5 + 0.25) / 3 = 0.583
```

The higher the MRR, the more consistently relevant results appear near the top.

## 19. NDCG

**NDCG — Normalized Discounted Cumulative Gain.** Don't let the name scare you. The mental model is simple: NDCG evaluates whether the most useful results appear near the top of the ranking. Unlike a simple relevant/not-relevant evaluation, NDCG can handle different levels of relevance, e.g. `5 = Highly relevant, 3 = Relevant, 1 = Slightly relevant, 0 = Irrelevant`. A ranking of `[highly relevant, irrelevant, highly relevant]` is generally better than `[irrelevant, irrelevant, highly relevant]`. NDCG rewards good ranking and discounts lower-ranked results.

## 20. Why NDCG Is Useful for RAG

Not all retrieved chunks are equally useful. For the question "how many credit hours are required for graduation?" we could assign relevance: Chunk A (directly answers) → 3, Chunk B (discusses graduation generally) → 2, Chunk C (mentions credit hours indirectly) → 1, Chunk D (tuition info) → 0. NDCG can evaluate whether the strongest evidence is ranked first — particularly useful for reranker evaluation, search systems, hybrid retrieval, and large retrieval candidate sets.

## 21. A Simple Retrieval Evaluation Dataset

```
evaluation_case = {
    "question": "How many credit hours are required?",
    "relevant_chunks": ["chunk_7"]
}
```

Suppose our retriever returns:

```
retrieved = ["chunk_12", "chunk_7", "chunk_19", "chunk_3", "chunk_25"]
```

We can check whether the correct chunk appears:

```
hit = any(chunk in evaluation_case["relevant_chunks"] for chunk in retrieved)
print(hit)
```

Output: `True`. So `Hit Rate@5 = 1`.

## 22. Simple Recall@K Implementation

If there can be multiple relevant chunks:

```
def recall_at_k(retrieved, relevant, k):
    retrieved_top_k = retrieved[:k]
    relevant_found = set(retrieved_top_k) & set(relevant)
    return len(relevant_found) / len(relevant)
```

Example: `retrieved = ["a", "b", "c", "d", "e"]`, `relevant = ["b", "d", "x"]`. We found `b` and `d` out of `b, d, x`. Therefore:

```
Recall@5 = 2/3 ≈ 0.667
```

## 23. Simple Precision@K

```
def precision_at_k(retrieved, relevant, k):
    retrieved_top_k = retrieved[:k]
    relevant_found = set(retrieved_top_k) & set(relevant)
    return len(relevant_found) / k
```

Using `retrieved = [a, b, c, d, e]`, `relevant = [b, d, x]`, we get 2 relevant / 5 retrieved:

```
Precision@5 = 0.4
```

## 24. Important: Don't Evaluate Retrieval With Only Final Answers

Suppose retrieval quality is poor, but the LLM happens to know the answer from its pretrained knowledge — it could still produce a correct answer. Then: Final answer → Correct, Retrieval → Bad. **If you only measure final answer accuracy, you may completely miss the retrieval problem.** This is why stage-level evaluation matters.

## 25. Evaluating Different Retrieval Strategies

Now you can run controlled experiments across a dataset of, say, 500 questions:

```
Dense                Recall@5 = 81%   MRR = 0.72
BM25                 Recall@5 = 76%   MRR = 0.69
Hybrid + RRF         Recall@5 = 89%   MRR = 0.81
Hybrid + Reranker    Recall@5 = 91%   MRR = 0.87
```

Now you have quantitative evidence for your architecture decisions.

## 26. But Higher Retrieval Metrics Don't Always Mean Better Final Answers

Suppose Retriever A has Recall@5 = 90% and Retriever B has Recall@5 = 85%. You might assume A is better — but perhaps A returns huge amounts of irrelevant information, confusing the LLM. Final answer quality could be A → 82%, B → 88%. So: **optimizing retrieval metrics alone does not guarantee optimal end-to-end RAG performance.** We need both Retrieval Evaluation and Generation Evaluation — exactly why later lessons cover Faithfulness, Answer Relevance, and Context Relevance.

## 27. The Retrieval Metric Cheat Sheet

| Metric | Main Question |
|---|---|
| **Hit Rate@K** | Did we find at least one relevant result? |
| **Recall@K** | How much relevant information did we retrieve? |
| **Precision@K** | How much of what we retrieved was relevant? |
| **MRR** | How high was the first relevant result? |
| **NDCG** | Are the most relevant results ranked near the top? |

This is more important than memorizing formulas.

## 28. The Big Mental Model

```
                    Retriever
                       ↓
                Ranked Results
                       ↓
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       Recall       Precision      Rank
          ↓            ↓            ↓
     Did we find?   How much?    How high?
                                   ↓
                              MRR / NDCG
```

Retrieval metrics evaluate the **retriever**. They don't automatically tell you "the final answer is correct" — that's a separate evaluation problem.

## Short Summary

Retrieval metrics allow us to evaluate the retrieval stage independently from the LLM. **Recall** — did we retrieve the relevant information? **Precision** — how much of what we retrieved was relevant? **Hit Rate@K** — did we retrieve at least one relevant result? **MRR** — how high was the first relevant result? **NDCG** — did the most relevant results appear near the top? These metrics let you compare Dense vs BM25 vs Hybrid vs Hybrid + Reranker using actual evidence rather than intuition.

**Key takeaway: A RAG system can only use evidence that reaches the LLM. Therefore, measure retrieval quality directly instead of judging retrieval only through the final answer. Recall → don't miss useful information. Precision → don't retrieve too much useless information. Ranking → put the most useful information first.**""",
                "estimated_minutes": 40,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Calculate Retrieval Metrics by Hand",
                    "description": """Your retriever has the following relevant chunks for a question: `[A, C, F]`. It returns Top-5: `[B, C, D, F, G]`.

Calculate:

1. Hit Rate@5
2. Recall@5
3. Precision@5

Then answer:

4. Is the retriever good or bad based on these numbers?
5. Would you prefer a retriever that finds the correct chunk at rank 1 or rank 5? Why?
6. Which metric would help measure that ranking difference?""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "retrieval-metrics", "manual-calculation"],
                },
                {
                    "title": "Implement Recall@K, Precision@K, Hit Rate@K, and MRR",
                    "description": """Implement four functions:

1. `hit_rate_at_k(retrieved, relevant, k)` — returns `1` if any of the top-k retrieved items are in `relevant`, else `0`.
2. `recall_at_k(retrieved, relevant, k)` — fraction of `relevant` items found in the top-k retrieved items.
3. `precision_at_k(retrieved, relevant, k)` — fraction of the top-k retrieved items that are relevant.
4. `reciprocal_rank(retrieved, relevant)` — returns `1 / rank` of the first relevant item found in `retrieved` (1-indexed rank), or `0` if none of the relevant items appear at all.

Then compute all four metrics for `retrieved = ["B", "C", "D", "F", "G"]`, `relevant = ["A", "C", "F"]`, `k = 5`, and print the results.""",
                    "starter_code": """def hit_rate_at_k(retrieved, relevant, k):
    # TODO
    pass


def recall_at_k(retrieved, relevant, k):
    # TODO
    pass


def precision_at_k(retrieved, relevant, k):
    # TODO
    pass


def reciprocal_rank(retrieved, relevant):
    # TODO: find the 1-indexed rank of the first relevant item, return 1/rank, or 0 if none found
    pass


retrieved = ["B", "C", "D", "F", "G"]
relevant = ["A", "C", "F"]
k = 5

# TODO: compute and print hit_rate_at_k, recall_at_k, precision_at_k, reciprocal_rank
""",
                    "solution_code": """def hit_rate_at_k(retrieved, relevant, k):
    top_k = retrieved[:k]
    return int(any(item in relevant for item in top_k))


def recall_at_k(retrieved, relevant, k):
    top_k = retrieved[:k]
    found = set(top_k) & set(relevant)
    return len(found) / len(relevant)


def precision_at_k(retrieved, relevant, k):
    top_k = retrieved[:k]
    found = set(top_k) & set(relevant)
    return len(found) / k


def reciprocal_rank(retrieved, relevant):
    for i, item in enumerate(retrieved, start=1):
        if item in relevant:
            return 1 / i
    return 0


retrieved = ["B", "C", "D", "F", "G"]
relevant = ["A", "C", "F"]
k = 5

print("Hit Rate@5:", hit_rate_at_k(retrieved, relevant, k))
print("Recall@5:", recall_at_k(retrieved, relevant, k))
print("Precision@5:", precision_at_k(retrieved, relevant, k))
print("Reciprocal Rank:", reciprocal_rank(retrieved, relevant))
# Expected: Hit Rate@5: 1, Recall@5: 0.667, Precision@5: 0.4, Reciprocal Rank: 0.5 (C found at rank 2)
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "retrieval-metrics", "python"],
                },
            ],
            "quiz": {
                "title": "Retrieval Metrics — Knowledge Check",
                "questions": [
                    {
                        "question": "There are 3 relevant chunks for a question: {2, 7, 9}. A retriever's Top-5 results are [1, 2, 4, 7, 12]. What are Hit Rate@5 and Recall@5?",
                        "options": [
                            "Hit Rate@5 = 0, Recall@5 = 0%",
                            "Hit Rate@5 = 1, Recall@5 ≈ 66.7%",
                            "Hit Rate@5 = 1, Recall@5 = 100%",
                            "Hit Rate@5 = 2, Recall@5 = 40%",
                        ],
                        "correct": 1,
                        "explanation": "At least one relevant chunk (2 or 7) was found, so Hit Rate@5 = 1. Two of the three relevant chunks (2 and 7) were retrieved, giving Recall@5 = 2/3 ≈ 66.7%, exactly matching the lesson's worked example.",
                    },
                    {
                        "question": "A retriever returns 10 chunks: 8 relevant and 2 irrelevant. What is Precision, and what does Precision actually measure?",
                        "options": [
                            "Precision = 80%; it measures how much relevant information exists in the whole database",
                            "Precision = 80%; it measures how much of what was retrieved is actually relevant",
                            "Precision = 20%; it measures how much relevant information was missed",
                            "Precision cannot be computed without knowing the total number of relevant documents in the database",
                        ],
                        "correct": 1,
                        "explanation": "Precision = relevant retrieved / total retrieved = 8/10 = 80%, and it answers 'of the things we retrieved, how many were relevant?' — unlike Recall, it doesn't require knowing the total number of relevant items in the database.",
                    },
                    {
                        "question": "A team increases K from Top-5 to Top-20 for their retriever. What trade-off does the lesson describe as a common result of this change?",
                        "options": [
                            "Both recall and precision always increase together",
                            "Recall tends to increase (more relevant items get a chance to appear) while precision tends to decrease (more irrelevant items get pulled in too)",
                            "Both recall and precision always decrease",
                            "K has no effect on either metric",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's worked example shows precision dropping from 80% (Top-5) to 40% (Top-20) as more irrelevant chunks get included, while recall generally rises — the classic recall/precision trade-off as K increases.",
                    },
                    {
                        "question": "Retriever A finds the relevant document at rank 1; Retriever B finds the same relevant document at rank 4. Both achieve the same Recall@5. Which metric distinguishes A as better for a Top-1 or Top-2 pipeline, and why?",
                        "options": [
                            "Precision@5, because it counts the number of relevant items only",
                            "MRR (Mean Reciprocal Rank), because it rewards the relevant result appearing at a higher rank — 1/1 = 1.0 for rank 1 versus 1/4 = 0.25 for rank 4",
                            "Recall@5, because it already captures rank position",
                            "Hit Rate@5, because it distinguishes between different ranks",
                        ],
                        "correct": 1,
                        "explanation": "The lesson shows Hit Rate and Recall treat both retrievers the same (both found the item somewhere in the top 5), but MRR specifically captures how high the first relevant result appears via reciprocal rank (1/rank).",
                    },
                    {
                        "question": "Retriever A has Recall@5 = 90% but produces final answer accuracy of 82%; Retriever B has Recall@5 = 85% but produces final answer accuracy of 88%. What does this scenario illustrate?",
                        "options": [
                            "Recall@5 is a useless metric and should never be measured",
                            "Optimizing retrieval metrics alone does not guarantee optimal end-to-end RAG performance — retrieval quality and generation quality must both be evaluated",
                            "Retriever B must have a bug since its recall is lower",
                            "Final answer accuracy is always determined solely by Recall@K",
                        ],
                        "correct": 1,
                        "explanation": "This is the lesson's explicit warning in section 26: higher retrieval metrics (like Retriever A's Recall@5) don't always translate into better final answers, e.g. if extra retrieved content confuses the LLM — so both retrieval and generation evaluation are needed.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "Faithfulness",
            "slug":              "ai-developer-ai-evaluation-observability-faithfulness",
            "description":       "Whether an AI answer's claims are actually supported by the retrieved context: the evidence-boundary mental model, faithfulness vs correctness vs answer relevance vs context relevance, claim-level evaluation, and why good retrieval doesn't guarantee faithful generation.",
            "order":             8,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "faithfulness", "rag-evaluation", "hallucination"],
            "prerequisite_ids":  [],  # builds on "RAG Evaluation" and "Retrieval Metrics" (this level, topics 6-7)
            "lesson": {
                "title": "Faithfulness",
                "content": """Now we move from *"did the retriever find useful information?"* to *"did the generated answer actually stay faithful to that information?"* This is one of the most important concepts in RAG evaluation.

## 1. What Is Faithfulness?

Faithfulness measures whether the claims made by the AI's answer are supported by the provided context. In simple terms: **does the answer say only what the evidence supports?**

Context: "The program requires 160 credit hours for graduation." Answer: "Students need 160 credit hours for graduation." The answer is **faithful ✅** because the context supports the claim.

Now, same context, but answer: "Students need 180 credit hours for graduation." The answer is **not faithful ❌** — the context says 160, while the answer says 180.

## 2. The Mental Model

Think of faithfulness as an evidence boundary:

```
              Retrieved Context
                     │
          ┌──────────┴──────────┐
          │                     │
      Supported             Unsupported
       Claims                 Claims
          │                     │
          ▼                     ▼
      Faithful              Hallucination
       Answer
```

The LLM can produce fluent language that goes beyond the evidence. Faithfulness asks: **did it cross the evidence boundary?**

## 3. Faithfulness vs Correctness

This distinction is extremely important. Suppose context says "The university library closes at 8 PM." and the answer says "The library closes at 8 PM." That's Correctness ✅, Faithfulness ✅.

Now imagine the answer says "The university library closes at 8 PM, and it is open every weekend." If the context doesn't mention weekend hours: Correctness → ? (the statement might actually be true in the real world), but Faithfulness → ❌ for that claim, because the question for faithfulness is **is it supported by the supplied context?** This distinction is critical.

## 4. Faithfulness Is About the Context

Context: "The program requires 160 credit hours." Answer: "The program requires 160 credit hours." Faithful. Now suppose the LLM already knows from its pretrained knowledge that the university has five engineering departments. If that information isn't in the retrieved context and the answer adds "...and the university has five engineering departments," that second claim is not grounded in the provided context. So:

```
World knowledge ≠ Retrieved evidence
```

Faithfulness specifically cares about the relationship between **Answer ↕ Context.**

## 5. Why Faithfulness Matters in RAG

The purpose of RAG is often to provide the model with external evidence:

```
User Question
      ↓
Retriever
      ↓
Evidence
      ↓
LLM
      ↓
Answer
```

If the LLM ignores or contradicts the evidence, the RAG system loses one of its main advantages. You could have excellent retrieval → correct context → LLM → **hallucinated answer ❌**. So **good retrieval does not guarantee faithful generation.**

## 6. A Simple Example

Context: "The academic year begins in September." Question: "When does the academic year begin?"

**Answer A**: "The academic year begins in September." Faithfulness → High.

**Answer B**: "The academic year begins in September and ends in June." The context only tells us when it begins. First claim → supported ✅, second claim → unsupported ❌. The answer is only partially faithful.

## 7. Think in Claims

One useful way to evaluate faithfulness is to break the answer into individual claims. Suppose the answer states: "The program requires 160 credit hours. Students must also complete an internship. Graduation requires a minimum GPA of 2.0." Break it down:

```
Claim 1 → 160 credit hours
Claim 2 → Internship required
Claim 3 → Minimum GPA of 2.0
```

Then compare each claim against the context:

```
Context
   ↓
┌───────────────┐
│ Claim 1 → ✅  │
│ Claim 2 → ❌  │
│ Claim 3 → ✅  │
└───────────────┘
```

This is much more precise than simply saying "the answer looks good."

## 8. Faithfulness and Hallucination

A hallucination occurs when an AI generates information that isn't properly supported by the available evidence. For RAG:

```
Retrieved Context
       ↓
      LLM
       ↓
Unsupported claim
```

For example, context: "The course has 3 credit hours." Answer: "The course has 3 credit hours and requires students to complete a final project." If the final-project requirement isn't in the context, the model has introduced unsupported information — a faithfulness problem.

## 9. Contradiction Is Especially Bad

There are different types of faithfulness failure.

**Type 1 — Unsupported information.** Context: "Course = 3 credits." Answer: "The course is 3 credits and has a final exam." If the exam isn't mentioned: unsupported claim ❌.

**Type 2 — Contradiction.** Context: "Course = 3 credits." Answer: "The course is 4 credits." This is worse:

```
Context → 3 credits
Answer  → 4 credits
Contradiction ❌❌
```

A strong evaluation system should identify both, but contradictions deserve particular attention.

## 10. Faithfulness vs Answer Relevance

These are different. **Answer relevance** asks: does the answer address the question? **Faithfulness** asks: is the answer supported by the context?

Question: "How many credit hours are required?" Context: "The program requires 160 credit hours." Answer: "The university was established in 1950." The answer might be factually true, but Answer Relevance → ❌, Faithfulness → ❌.

Now, Answer: "The program requires 180 credit hours." This is Answer Relevance → ✅, Faithfulness → ❌ — it directly answers the question but contradicts the context. A very useful distinction.

## 11. Faithfulness vs Context Relevance

We'll study Context Relevance in a later lesson. For now: **context relevance** asks — is the retrieved information useful for answering the question? **Faithfulness** asks — did the answer actually stay within that information?

Question: "What is the credit-hour cost?" Context: "The credit-hour cost is 1330 EGP." Answer: "The credit-hour cost is 1500 EGP." Context: relevant ✅. Answer: faithful ❌. So:

```
Good context does NOT guarantee Faithful answer
```

## 12. A Useful RAG Matrix

| Context | Answer | Result |
|---|---|---|
| Relevant | Correct & supported | Excellent |
| Relevant | Wrong/unsupported | Faithfulness failure |
| Irrelevant | Correct by coincidence | Retrieval problem |
| Irrelevant | Wrong | Retrieval + answer problem |

This is why evaluating only the final answer is insufficient.

## 13. A Simple Faithfulness Algorithm

Conceptually:

```
Answer
  ↓
Extract claims
  ↓
For each claim:
  ↓
Is it supported by context?
  ↓
Yes / No
```

For example:

```
answer_claims = [
    "The program requires 160 credit hours.",
    "The program requires an internship."
]

context = "The program requires 160 credit hours for graduation."
```

Conceptually: `for claim in answer_claims: check_support(claim, context)`. Result: Claim 1 → supported ✅, Claim 2 → unsupported ❌. This is the core idea behind many automated faithfulness evaluators.

## 14. Simple Rule-Based Example

For demonstration, a very primitive evaluator:

```
def simple_faithfulness(answer, context):
    claims = answer.split(".")
    results = []

    for claim in claims:
        claim = claim.strip()
        if not claim:
            continue

        results.append({
            "claim": claim,
            "supported": claim in context
        })

    return results
```

This is **not** a real semantic faithfulness evaluator. For example, context "The program requires 160 credit hours." and answer "Students must complete 160 credit hours." — the strings are different even though the meaning is supported. So exact string matching is not enough; we need semantic or LLM-based evaluation.

## 15. LLM-Based Faithfulness Evaluation

An LLM judge can evaluate whether claims are supported:

```
judge_prompt = \"\"\"
Determine whether the answer is fully supported by the provided context.

Context:
{context}

Answer:
{answer}

For each factual claim in the answer:
- Identify the claim.
- Determine whether the context supports it.
- Mark it as supported or unsupported.

Return structured JSON.
\"\"\"
```

Potential result:

```
{
    "claims": [
        {"claim": "The program requires 160 credit hours.", "supported": true},
        {"claim": "The program requires an internship.", "supported": false}
    ]
}
```

This gives us a much more useful diagnostic.

## 16. Faithfulness Score

Suppose an answer contains 5 factual claims, and 4 are supported while 1 is unsupported. A simple conceptual score:

```
Faithfulness =
Supported Claims
────────────────
Total Claims
```

So `4/5 = 0.80` or `80%`. This is an intuitive way to think about claim-level faithfulness. Different evaluation frameworks may define their own exact scoring methods, so don't assume every tool uses this exact formula.

## 17. Example With Your Academic Assistant

Question: "What is the cost of one credit hour?" Context: "For the academic year 2025/2026, the cost of one credit hour is 1330 EGP." Answer: "For the 2025/2026 academic year, one credit hour costs 1330 EGP. Students must pay the fees before registration."

Break into claims: Claim 1 (2025/2026 → 1330 EGP) → supported ✅. Claim 2 ("students must pay before registration") → context doesn't say this → ❌. So the answer is not fully faithful.

## 18. Why Fluent Answers Can Be Dangerous

Consider: "For the 2025/2026 academic year, students are required to pay 1330 EGP per credit hour before registration, with fees calculated based on the number of registered credits." This sounds extremely professional. But perhaps the context only says "the cost of one credit hour is 1330 EGP." The generated answer contains several additional claims. This demonstrates an important principle: **fluency is not evidence.** An answer can sound authoritative while being poorly grounded.

## 19. Faithfulness and Your Strict RAG System

You previously worked with strict RAG behavior such as "only answer using retrieved information" and "do not invent details." That's useful at generation time — but now we can evaluate whether that rule actually works. You could measure: before strict prompting → Faithfulness = 82%; after strict prompting → Faithfulness = 94%. Now your prompt change has measurable evidence behind it — much better than "the new prompt seems to reduce hallucinations."

## 20. Important Engineering Principle

A prompt saying "do not hallucinate" doesn't prove that hallucinations won't happen. Likewise, "answer only from the context" doesn't guarantee faithfulness. The engineering approach is:

```
Instruction
   ↓
Run evaluation dataset
   ↓
Measure faithfulness
   ↓
Compare versions
```

This connects directly to Prompt Evaluation and Regression Testing later.

## 21. Faithfulness Is Not the Same as Truth

This is subtle but important. Context: "The university has 10 campuses." Answer: "The university has 10 campuses." Faithful ✅. Now imagine the context itself contains incorrect information — the answer can still be faithful to the context. Therefore:

```
Faithfulness ≠ Absolute truth
```

Faithfulness means the answer is supported by the supplied evidence. Determining whether the evidence itself is correct is a separate problem.

## 22. The Full RAG Evaluation Picture So Far

```
                     RAG Evaluation
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
      Retrieval          Context        Generation
          │                │                │
          ↓                ↓                ↓
     Recall@K          Relevance       Faithfulness
     Precision@K
     MRR
     NDCG
```

Eventually we'll add Answer Relevance, Context Relevance, Prompt Evaluation, Regression Testing, and Observability. Each measures a different part of the system.

## 23. The Debugging Mental Model

When you see a bad answer: **Step 1** — was the right evidence retrieved? If no → retrieval failure. **Step 2** — if yes, did the answer stay faithful to the evidence? If no → generation/faithfulness failure. **Step 3** — did the answer actually address the user's question? That's where Answer Relevance comes in.

```
Wrong Answer
     ↓
Retrieval?
     ↓
Faithfulness?
     ↓
Answer Relevance?
```

## Short Summary

Faithfulness asks: are the claims in the AI answer supported by the retrieved context? A response can be Fluent ✅, Relevant ✅, but Faithful ❌ — because the LLM can generate unsupported information. Important distinctions: **Correctness** — is the answer actually correct? **Faithfulness** — is the answer supported by the provided evidence? **Answer Relevance** — does the answer address the question? **Context Relevance** — is the retrieved evidence useful for the question? These are different dimensions.

**Key takeaway: RAG isn't successful just because the retriever found the right information — the LLM must also use that information faithfully. Context → Evidence → Answer → are the answer's claims supported? If the answer goes beyond the evidence, you have a faithfulness problem.**""",
                "estimated_minutes": 40,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Break an Answer into Claims and Check Faithfulness",
                    "description": """Question: "What is the cost of one credit hour?"

Context: "The cost of one credit hour for the academic year 2025/2026 is 1330 EGP."

AI Answer: "The cost of one credit hour is 1330 EGP. Students must pay the fees before registration, and the university offers discounts for early payment."

Answer:

1. How many factual claims can you identify in the answer?
2. Which claims are supported by the context?
3. Which claims are unsupported?
4. Is the answer fully faithful?
5. Could the answer be relevant but not faithful? Explain.
6. Why is "the answer sounds reasonable" not sufficient for evaluating faithfulness?""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "faithfulness", "claim-analysis"],
                },
                {
                    "title": "Implement a Claim-Level Faithfulness Scorer",
                    "description": """Write a function `faithfulness_score(claims, supported_flags)` that takes a list of claim strings and a parallel list of booleans (`True` if that claim is supported by the context, `False` otherwise), and returns the faithfulness score as `supported_claims / total_claims` (a float between 0 and 1). Raise a `ValueError` if the two lists have different lengths or if `claims` is empty.

Then, given these claims and manually-determined support flags for the academic-assistant example above, compute and print the faithfulness score.""",
                    "starter_code": """def faithfulness_score(claims, supported_flags):
    # TODO: validate inputs and compute supported_claims / total_claims
    pass


claims = [
    "The cost of one credit hour is 1330 EGP.",
    "Students must pay the fees before registration.",
    "The university offers discounts for early payment.",
]

# TODO: determine supported_flags based on the context
# Context: "The cost of one credit hour for the academic year 2025/2026 is 1330 EGP."
supported_flags = []

# TODO: compute and print the faithfulness score
""",
                    "solution_code": """def faithfulness_score(claims, supported_flags):
    if len(claims) != len(supported_flags):
        raise ValueError("claims and supported_flags must be the same length")
    if not claims:
        raise ValueError("claims must not be empty")

    supported_count = sum(1 for flag in supported_flags if flag)
    return supported_count / len(claims)


claims = [
    "The cost of one credit hour is 1330 EGP.",
    "Students must pay the fees before registration.",
    "The university offers discounts for early payment.",
]

# Context only confirms the cost; the other two claims are not mentioned.
supported_flags = [True, False, False]

score = faithfulness_score(claims, supported_flags)
print(score)
# Expected: 0.333... (1 out of 3 claims supported)
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "faithfulness", "python"],
                },
            ],
            "quiz": {
                "title": "Faithfulness — Knowledge Check",
                "questions": [
                    {
                        "question": "Context: 'The university library closes at 8 PM.' Answer: 'The library closes at 8 PM, and it is open every weekend.' If weekend hours aren't mentioned in the context, how should the second claim be scored for faithfulness, even if it happens to be true in reality?",
                        "options": [
                            "Faithful, because the claim is true in the real world",
                            "Not faithful for that claim, because faithfulness asks whether the claim is supported by the supplied context — not whether it's true in general",
                            "Faithful, because the first claim in the answer was supported",
                            "This cannot be evaluated for faithfulness at all",
                        ],
                        "correct": 1,
                        "explanation": "The lesson is explicit: faithfulness is about the context, not real-world truth. Even a true statement is unfaithful if it isn't supported by the supplied context — this is the core faithfulness-vs-correctness distinction.",
                    },
                    {
                        "question": "Context: 'The program requires 160 credit hours.' Answer: 'The university was established in 1950.' What does this example illustrate about the relationship between Answer Relevance and Faithfulness?",
                        "options": [
                            "They always move together — if faithfulness is low, relevance must be high",
                            "An answer can be both irrelevant AND unfaithful at the same time; they are independent dimensions",
                            "This answer is faithful because it might be a true historical fact",
                            "Answer relevance cannot be evaluated without a context",
                        ],
                        "correct": 1,
                        "explanation": "The lesson uses this exact example to show both Answer Relevance and Faithfulness scoring low simultaneously — since the answer doesn't address the question AND isn't grounded in the context, demonstrating they're separate but can both fail together.",
                    },
                    {
                        "question": "Context: 'Course = 3 credits.' Two possible answers: (A) 'The course is 3 credits and has a final exam' (exam not mentioned in context) and (B) 'The course is 4 credits.' Why does the lesson say contradiction (B) deserves particular attention compared to unsupported information (A)?",
                        "options": [
                            "Because (A) is always worse than (B) in every evaluation system",
                            "Because (B) directly conflicts with stated evidence rather than merely adding unstated information, making it a more severe type of faithfulness failure",
                            "Because contradictions are impossible to detect automatically",
                            "Because unsupported information should never be flagged as a faithfulness issue",
                        ],
                        "correct": 1,
                        "explanation": "The lesson distinguishes 'Type 1 — Unsupported information' from 'Type 2 — Contradiction' and states contradictions are worse since the answer actively conflicts with what the context says, not just adds unstated details.",
                    },
                    {
                        "question": "Why does the lesson caution that a naive faithfulness check using exact string matching (checking if a claim string appears verbatim in the context) is 'not enough'?",
                        "options": [
                            "Because exact string matching is too slow to run at scale",
                            "Because a claim can be semantically supported by the context while being worded completely differently (e.g. 'Students must complete 160 credit hours' vs. 'The program requires 160 credit hours'), which exact matching would incorrectly mark as unsupported",
                            "Because faithfulness only applies to numeric claims, not text",
                            "Because context is always shorter than the answer",
                        ],
                        "correct": 1,
                        "explanation": "The lesson demonstrates this directly: differently-worded but semantically equivalent claims would fail a naive 'claim in context' string check, which is why semantic or LLM-based evaluation is needed instead.",
                    },
                    {
                        "question": "Why does the lesson state that 'faithfulness ≠ absolute truth'?",
                        "options": [
                            "Because faithfulness scores are always lower than truth scores",
                            "Because an answer can be faithful to context that itself contains incorrect information — faithfulness measures support by the supplied evidence, not whether that evidence is objectively correct",
                            "Because faithfulness and truth are exactly the same concept with different names",
                            "Because truth can only be measured by LLM-as-a-Judge, never by faithfulness metrics",
                        ],
                        "correct": 1,
                        "explanation": "The lesson gives an explicit example: if the context itself is wrong, an answer that faithfully repeats it is still 'faithful' by this metric's definition — determining whether the evidence itself is correct is a separate problem from faithfulness.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "Answer Relevance",
            "slug":              "ai-developer-ai-evaluation-observability-answer-relevance",
            "description":       "Whether the generated answer actually addresses the user's question: distinguishing relevance from correctness and faithfulness, why over-answering hurts relevance, and the methods (human evaluation, LLM-as-a-Judge, semantic similarity) used to measure it.",
            "order":             9,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "answer-relevance", "rag-evaluation"],
            "prerequisite_ids":  [],  # builds on "Faithfulness" (this level, topic 8) and "LLM-as-a-Judge" / "Semantic Similarity" (topics 4-5)
            "lesson": {
                "title": "Answer Relevance",
                "content": """In the previous lesson, we asked: *is the answer supported by the retrieved context?* That was **Faithfulness**. Now we ask a different question: *does the answer actually answer the user's question?* That's **Answer Relevance**.

## 1. What Is Answer Relevance?

Answer relevance measures how well the generated answer addresses the user's question. In simple terms: **did the AI answer the question the user actually asked?**

Question: "How many credit hours are required for graduation?" Answer: "Students need to complete 160 credit hours." That's highly relevant — question is about graduation credit hours, answer is about graduation credit hours. Relevance → ✅.

## 2. Relevance Is Not the Same as Correctness

Question: "How many credit hours are required for graduation?" Answer: "Students need 180 credit hours." The answer is directly addressing the question. So Answer Relevance → High, Correctness → Low. This is an important distinction: **the answer can be relevant but wrong.**

## 3. Relevance Is Not the Same as Faithfulness

Context: "The program requires 160 credit hours." Question: "How many credit hours are required?" Answer: "Students need 180 credit hours." This is Answer Relevance → High, Faithfulness → Low, Correctness → Low. Why? Because it answers the right question, but the answer isn't supported by the context.

## 4. The Three Dimensions

```
                 AI Answer
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
   Relevance    Faithfulness  Correctness
       ↓            ↓            ↓
 Does it answer? Supported?    Is it true?
```

These dimensions overlap, but they are not interchangeable.

## 5. Example: Correct but Irrelevant

Question: "What is the cost of one credit hour?" Answer: "The program requires 160 credit hours for graduation." Suppose 160 is completely correct. Still: Correctness → High, Relevance → Low — the user didn't ask about graduation requirements. This is an important AI failure: **a factually correct answer can still be useless.**

## 6. Example: Relevant but Unfaithful

Question: "What is the cost of one credit hour?" Context: "The cost is 1330 EGP." Answer: "The cost is 1500 EGP." The answer directly addresses the question — Relevance → High. But it contradicts the context — Faithfulness → Low. So **relevant ≠ faithful.**

## 7. Example: Faithful but Irrelevant

Context: "The cost is 1330 EGP." Question: "How many credit hours are required for graduation?" Answer: "The cost of one credit hour is 1330 EGP." The answer is faithful to the context — Faithfulness → High. But it doesn't answer the question — Answer Relevance → Low. Another reason we need separate evaluation dimensions.

## 8. A Very Useful Matrix

| Answer | Relevance | Faithfulness |
|---|---|---|
| Correctly answers using evidence | High | High |
| Answers question but contradicts evidence | High | Low |
| Gives supported information but ignores question | Low | High |
| Gives unrelated unsupported information | Low | Low |

Your goal is **high relevance + high faithfulness.**

## 9. Why Relevance Matters in Real AI Systems

Imagine a user asks "Can I register this course without passing the prerequisite?" and the system responds "The course is worth 3 credit hours." That might be completely true, but it's useless — the user needed information about prerequisites and registration eligibility, not credit hours. So answer relevance measures whether the AI is solving the user's actual **information need.**

## 10. Short Answers Can Be More Relevant

Answer A: "The required number is 160 credit hours." Answer B: a long paragraph about academic regulations, curriculum, registration requirements, and academic procedures that eventually mentions 160. Both may be correct, but if the user only asks "how many credit hours are required?" Answer A may be more relevant because it directly provides what the user needs. Principle: **more information does not automatically mean more relevance.**

## 11. Relevance and Over-Answering

AI systems sometimes produce a simple answer followed by extra information, more extra information, and unnecessary explanation. For example, asked "what is the credit-hour cost?" the answer starts with "one credit hour costs 1330 EGP" and then adds several unrelated paragraphs about program structure and academic progress. The answer may still be correct, but its relevance decreases because the useful information becomes buried inside unrelated details.

## 12. Directness

One component of relevance is **directness** — does the answer directly address the question? "Is the course worth 3 credit hours?" → "Yes, the course is worth 3 credit hours." is very direct. Compare to "courses in this program have different credit-hour values depending on classification..." — not necessarily wrong, but less direct.

## 13. Completeness vs Relevance

Question: "What are the requirements for graduation?" Answer: "Students must complete 160 credit hours." This is relevant, but it may be incomplete. So Relevance → High, Completeness → potentially Low. This is why relevance alone isn't enough to determine whether an answer is good.

## 14. Answer Relevance in RAG

Our RAG pipeline:

```
Question
   ↓
Retriever
   ↓
Context
   ↓
LLM
   ↓
Answer
```

We can evaluate: Retriever → Retrieval Metrics. Context → Context Relevance. Answer → Faithfulness and Answer Relevance. This gives us increasingly detailed diagnostics.

## 15. A Practical Example

Question: "What is the cost of one credit hour?" Context: "For the academic year 2025/2026, the cost of one credit hour is 1330 EGP."

**Answer A**: "One credit hour costs 1330 EGP." Relevance → High, Faithfulness → High. Excellent.

**Answer B**: "The academic year 2025/2026 has several registration requirements." Relevance → Low, Faithfulness → possibly high (may be supported if such information exists), but doesn't answer the question.

**Answer C**: "One credit hour costs 1500 EGP." Relevance → High, Faithfulness → Low.

## 16. How Can We Measure Answer Relevance?

**Method 1 — Human Evaluation.** Give a human evaluator the question and answer, and ask them to rate from 1 (completely irrelevant) to 5 (highly relevant). Intuitive but expensive.

**Method 2 — LLM-as-a-Judge.** Question + Answer → Judge → Relevance Score, e.g. `{"relevance": 5, "reason": "The answer directly provides the requested credit-hour cost."}`. Scalable, but remember our earlier warning: the judge itself can make mistakes.

**Method 3 — Semantic Similarity.** Compare the question and answer embeddings:

```
Question
   ↓
Embedding ──┐
            │
         Similarity
            │
Answer      │
   ↓        │
Embedding ──┘
```

High similarity can indicate that the answer is semantically related to the question. But this has limitations.

## 17. Why Semantic Similarity Alone Isn't Enough

Question: "How many credit hours are required for graduation?" Answer: "Graduation requirements include credit hours." These texts are semantically related, so similarity could be high — but the answer doesn't actually provide the requested number. Semantic similarity → High, Useful answer → Low. **Semantic similarity is a signal, not a complete relevance evaluator.**

## 18. Another Example

Question: "What is the tuition cost per credit hour?" Answer: "Tuition and credit hours are important parts of university education." Semantic relationship: high. Actual usefulness: very low. The answer talks about the topic without actually answering the question — sometimes called **topic relevance without answer relevance.**

## 19. Relevance Evaluation With a Rubric

A good LLM judge can use a rubric: `5 = directly answers with the required information`, `4 = answers but contains minor unnecessary information`, `3 = partially answers`, `2 = mostly discusses related information but does not answer it`, `1 = completely unrelated`. Then give the judge the question and answer to score.

## 20. Simple Python Example

Conceptually:

```
def evaluate_relevance(question, answer):
    prompt = f\"\"\"
    Evaluate how relevant the answer is to the question.

    Question:
    {question}

    Answer:
    {answer}

    Score from 1 to 5:
    5 = Directly answers the question
    4 = Mostly answers it
    3 = Partially answers it
    2 = Mostly irrelevant
    1 = Completely irrelevant

    Return JSON.
    \"\"\"

    return call_llm(prompt)
```

The important engineering idea isn't the API call — it's: Question + Answer + explicit rubric → relevance evaluation.

## 21. Relevance Can Be Evaluated Without the Context

Notice something interesting: for basic answer relevance, we don't necessarily need the retrieved context. We can evaluate Question + Answer, because we're asking "does the answer address the question?" Whereas faithfulness requires Question + Context + Answer, because we're asking "is the answer supported by the context?" This distinction helps you design modular evaluation systems.

## 22. Query → Answer Relationship

Think of answer relevance as measuring:

```
User Intent
     ↓
Question
     ↓
AI Answer
     ↓
Did the system satisfy the information need?
```

It's not merely "does the answer contain similar words?" It's "does this answer actually fulfill what the user asked for?"

## 23. RAG Failure Example

Question: "What are the prerequisites for Machine Learning?" Retriever finds course description, registration policy, and tuition information. LLM responds "Machine Learning is a 3-credit course." The answer might be factually correct, but Retrieval → ❌, Context → ❌, Answer Relevance → ❌ — the system didn't satisfy the user's request.

Now suppose the retriever actually found "Prerequisite: Probability and Statistics." but the LLM still responds "Machine Learning is a 3-credit course." Now: Retrieval → ✅, Context → relevant, Answer Relevance → ❌, Faithfulness → ❌/not grounded in the useful evidence. This is a **generation problem.**

## 24. The Bigger Evaluation Picture

```
                     RAG Evaluation
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
      Retrieval          Context          Answer
          │                │                │
          ↓                ↓          ┌─────┴─────┐
      Recall@K         Relevance      ↓           ↓
      Precision@K                     Faithfulness Relevance
      MRR
      NDCG
```

Notice how each metric answers a different question.

## 25. A Very Important Engineering Principle

When you see "Answer Quality = 80%," don't immediately ask "how can I make the LLM better?" Instead ask: was the correct evidence retrieved? Was the evidence relevant? Did the LLM stay faithful to it? Did the answer address the user's question? This creates a **diagnostic mindset** rather than a trial-and-error mindset.

## Short Summary

Answer Relevance asks: does the generated answer actually address the user's question? It is different from **Correctness** (is the information actually correct?), **Faithfulness** (is the answer supported by the retrieved context?), and **Context Relevance** (is the retrieved context useful for answering the question?). A response can therefore be correct but irrelevant, relevant but incorrect, relevant but unfaithful, or faithful but irrelevant. A strong RAG answer should ideally be relevant + correct + faithful + complete.

**Key takeaway: An AI answer isn't good merely because it's true — it must solve the user's actual information need. Faithfulness asks "did the answer stay within the evidence?" Answer Relevance asks "did the answer address the question?"**""",
                "estimated_minutes": 40,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Diagnose Relevance, Faithfulness, and Correctness Together",
                    "description": """Question: "What is the prerequisite for the Machine Learning course?"

Retrieved Context: "Prerequisite: Probability and Statistics."

AI Answer: "Machine Learning is a 3-credit course offered to AI Engineering students."

Answer:

1. Is the answer relevant to the question?
2. Is it faithful to the retrieved context?
3. Is it correct, based only on the information we have?
4. What important information did the answer fail to provide?
5. Which component would you investigate first if the retriever actually retrieved the correct prerequisite information?""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "answer-relevance", "failure-analysis"],
                },
                {
                    "title": "Build a Rubric-Based Relevance Prompt and Classifier",
                    "description": """Write a function `build_relevance_prompt(question, answer)` that returns a prompt string using the 5-point rubric from the lesson (5 = directly answers ... 1 = completely unrelated) and asks for a JSON response with keys `"relevance"` (int 1-5) and `"reason"` (string).

Then write `is_relevant_enough(relevance_score, threshold=3)` that returns `True` if `relevance_score >= threshold`, else `False`.

Test `is_relevant_enough` against these three hypothetical judge scores: 5, 3, 1 — using the default threshold — and print the results.""",
                    "starter_code": """def build_relevance_prompt(question, answer):
    # TODO: return a prompt string with the rubric and JSON output instructions
    pass


def is_relevant_enough(relevance_score, threshold=3):
    # TODO: return True/False based on threshold
    pass


prompt = build_relevance_prompt(
    "What is the cost of one credit hour?",
    "One credit hour costs 1330 EGP.",
)
print(prompt)

# TODO: test is_relevant_enough with scores 5, 3, and 1
""",
                    "solution_code": """def build_relevance_prompt(question, answer):
    return f\"\"\"
Evaluate how relevant the answer is to the question.

Question:
{question}

Answer:
{answer}

Score from 1 to 5:
5 = Directly answers the question with the required information
4 = Answers the question but contains minor unnecessary information
3 = Partially answers the question
2 = Mostly discusses related information but does not answer it
1 = Completely unrelated to the question

Return JSON with keys: relevance, reason.
\"\"\"


def is_relevant_enough(relevance_score, threshold=3):
    return relevance_score >= threshold


prompt = build_relevance_prompt(
    "What is the cost of one credit hour?",
    "One credit hour costs 1330 EGP.",
)
print(prompt)

for score in [5, 3, 1]:
    print(score, "->", is_relevant_enough(score))
# Expected: 5 -> True, 3 -> True, 1 -> False
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "answer-relevance", "python"],
                },
            ],
            "quiz": {
                "title": "Answer Relevance — Knowledge Check",
                "questions": [
                    {
                        "question": "Question: 'What is the cost of one credit hour?' Answer: 'The program requires 160 credit hours for graduation.' Assuming '160' is factually correct, how should this be scored?",
                        "options": [
                            "High correctness, high relevance — the answer is accurate so it must be relevant",
                            "High correctness, low relevance — the answer is factually accurate but doesn't address what the user actually asked",
                            "Low correctness, high relevance",
                            "Both correctness and relevance are low",
                        ],
                        "correct": 1,
                        "explanation": "This is the lesson's 'correct but irrelevant' example: a factually accurate statement can still fail to address the user's actual question, demonstrating that correctness and relevance are independent dimensions.",
                    },
                    {
                        "question": "Context: 'The cost is 1330 EGP.' Question: 'What is the cost of one credit hour?' Answer: 'The cost is 1500 EGP.' How should Relevance and Faithfulness be scored here?",
                        "options": [
                            "Relevance: Low, Faithfulness: High",
                            "Relevance: High, Faithfulness: Low — the answer directly addresses the question but contradicts the context",
                            "Both Relevance and Faithfulness are High",
                            "Both Relevance and Faithfulness are Low",
                        ],
                        "correct": 1,
                        "explanation": "The lesson uses this exact example ('relevant but unfaithful'): the answer clearly addresses the cost question (relevance high) but contradicts the stated context value (faithfulness low).",
                    },
                    {
                        "question": "Why does the lesson say 'more information does not automatically mean more relevance,' using the example of a short direct answer (Answer A) vs. a long answer padded with extra context (Answer B)?",
                        "options": [
                            "Because longer answers are always factually wrong",
                            "Because when the user asks a specific question, a concise answer that directly provides what's needed can be more relevant than a longer one where the useful information is buried in unnecessary detail",
                            "Because LLM judges always penalize longer answers regardless of content",
                            "Because relevance can only be measured for answers under 10 words",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's Answer A vs Answer B example makes this point directly: directness and getting to the point can matter more for relevance than sheer amount of information, since burying the answer in extra detail reduces relevance.",
                    },
                    {
                        "question": "Why can Answer Relevance often be evaluated using only the Question and Answer, without needing the retrieved context — unlike Faithfulness?",
                        "options": [
                            "Because Answer Relevance and Faithfulness are actually the same metric under different names",
                            "Because Answer Relevance asks 'does the answer address the question?' (a Question+Answer relationship), while Faithfulness asks 'is the answer supported by the context?' (a Question+Context+Answer relationship)",
                            "Because context is never available when evaluating RAG systems",
                            "Because relevance can only be computed using exact match on the question and answer",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly separates these: relevance is fundamentally a Question-Answer relationship, while faithfulness fundamentally requires the Context as well — a distinction useful for designing modular evaluation systems.",
                    },
                    {
                        "question": "Question: 'What is the tuition cost per credit hour?' Answer: 'Tuition and credit hours are important parts of university education.' Why would semantic similarity alone likely mislabel this as a good answer?",
                        "options": [
                            "Because semantic similarity always gives a score of 0 for unrelated topics",
                            "Because the answer discusses the same general topic as the question (high topic-level semantic similarity) without actually providing the requested cost figure — 'topic relevance without answer relevance'",
                            "Because semantic similarity requires the exact same words to be present",
                            "Because this answer would score low on both semantic similarity and actual usefulness, so there's no risk of mislabeling",
                        ],
                        "correct": 1,
                        "explanation": "The lesson calls this 'topic relevance without answer relevance': the embeddings may be similar because both discuss tuition/credit hours, even though the answer never actually answers the specific question asked.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "Context Relevance",
            "slug":              "ai-developer-ai-evaluation-observability-context-relevance",
            "description":       "How useful the retrieved context actually is for answering a specific question — distinguishing topic relevance from question relevance, chunk-level relevance scoring, context noise and its cost, and how Context Relevance, Faithfulness, and Answer Relevance combine into a full RAG diagnostic model.",
            "order":             10,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "context-relevance", "rag-evaluation"],
            "prerequisite_ids":  [],  # builds on "Faithfulness", "Answer Relevance" (topics 8-9), and retrieval techniques from earlier levels
            "lesson": {
                "title": "Context Relevance",
                "content": """So far we've evaluated: **Retrieval** — did we find useful information? **Faithfulness** — did the answer stay supported by the evidence? **Answer Relevance** — did the answer address the user's question? Now we focus on the middle: **is the context we retrieved actually relevant to the question?**

## 1. What Is Context Relevance?

Context relevance measures how useful the retrieved context is for answering the user's question. In simple terms: *did the retriever give the LLM the right information, rather than just information that happens to be related?*

Question: "What is the prerequisite for Machine Learning?" Retrieved context: "Machine Learning requires Probability and Statistics as a prerequisite." That's highly relevant. But: "Machine Learning is a 3-credit course." — this is about the same course, but it doesn't answer the question. So:

```
Same topic ≠ Relevant evidence
```

## 2. Context Relevance vs Retrieval Metrics

You already learned retrieval metrics. What's the difference? **Retrieval metrics** usually require some form of ground truth — expected relevant chunk `chunk_7`, retrieved `[chunk_12, chunk_7, chunk_19]` → we calculate Recall@K, Precision@K, MRR, NDCG. **Context relevance** can ask "how relevant is this retrieved context to this particular question?" This can be especially useful when relevance isn't easily represented by a simple relevant/not-relevant label.

## 3. The Mental Model

```
User Question
      ↓
   Retriever
      ↓
Retrieved Context
      ↓
      LLM
      ↓
Generated Answer
```

Now put an evaluation checkpoint after retrieval:

```
User Question
      ↓
   Retriever
      ↓
Retrieved Context
      ↓
 ┌───────────────┐
 │ Is context    │
 │ relevant?     │
 └───────────────┘
      ↓
      LLM
```

We're evaluating the **Question → Context** relationship.

## 4. A Simple Example

Question: "What is the cost of one credit hour?"

- Chunk 1: "One credit hour costs 1330 EGP." → Highly relevant ✅
- Chunk 2: "Students must complete 160 credit hours to graduate." → Related topic, but not directly relevant ⚠️
- Chunk 3: "The university was established in 1972." → Irrelevant ❌

## 5. Topic Relevance vs Question Relevance

This is one of the most important ideas. Question: "What is the prerequisite for Machine Learning?" Context "Machine Learning is a 3-credit course in the AI Engineering program." is **topic-related** but doesn't answer the question. Compare: "Probability and Statistics is a prerequisite for Machine Learning." — this is **question-relevant**.

```
Topic relevance    → Talks about the same subject.
Question relevance → Provides information useful for answering the specific question.
```

For RAG, the second one is much more important.

## 6. Context Relevance and Noise

Imagine your retriever returns 10 chunks: 3 relevant, 1 slightly relevant, and 6 irrelevant. The LLM now has a lot of unnecessary information — this is **context noise**. Too much noise can make generation harder. So retrieval isn't simply "find information about the same topic" — it's "find the most useful evidence for this particular question."

## 7. Why Context Relevance Matters

**System A**: 10 retrieved chunks, 8 irrelevant / 2 relevant → LLM. **System B**: 5 retrieved chunks, 4 relevant / 1 irrelevant → LLM. System B may provide a cleaner context even though it retrieves fewer chunks — this can improve generation quality, faithfulness, latency, token usage, and cost. Therefore: **more retrieved context isn't automatically better.**

## 8. Context Relevance and the Context Window

LLMs have a context window. Question + 500 useful tokens vs. Question + 500 useful tokens + 10,000 irrelevant tokens — the second system is potentially wasting context capacity, tokens, money, and processing time. More importantly, irrelevant information can make it harder for the model to identify the evidence that matters. This is why techniques such as **reranking**, **context compression**, **filtering**, and **metadata filtering** can be evaluated using context relevance.

## 9. Context Relevance vs Faithfulness

These are very easy to confuse. **Context Relevance** (Question → Context) asks: is the retrieved context useful for the question? **Faithfulness** (Context → Answer) asks: is the answer supported by the context?

```
Question ─────→ Context     = Context Relevance
Context  ──────→ Answer     = Faithfulness
```

Different relationships.

## 10. A Powerful Example

Question: "What is the prerequisite for Machine Learning?" Retrieved Context: "Machine Learning is a 3-credit course." Generated Answer: "Machine Learning is a 3-credit course."

- Context relevance: Low ❌ — the context doesn't answer the question.
- Faithfulness: High ✅ — the answer accurately reflects the retrieved context.
- Answer relevance: Low ❌ — the answer doesn't answer the user's question.

This gives an important pattern: **the LLM may have generated a perfectly faithful answer to bad context.**

## 11. Another Example

Question: "What is the prerequisite for Machine Learning?" Context: "Probability and Statistics is a prerequisite for Machine Learning." Answer: "Machine Learning requires Probability and Statistics." Now: Context Relevance → High, Faithfulness → High, Answer Relevance → High. This is the ideal case.

## 12. Three-Stage Diagnostic Model

```
                 User Question
                       ↓
                   Retrieval
                       ↓
              ┌────────────────┐
              │ Context        │
              │ Relevant?      │
              └────────────────┘
                       ↓
                     LLM
                       ↓
              ┌────────────────┐
              │ Answer         │
              │ Faithful?      │
              └────────────────┘
                       ↓
              ┌────────────────┐
              │ Answer         │
              │ Relevant?      │
              └────────────────┘
```

This is becoming a real debugging framework.

## 13. Context Relevance at Chunk Level

We can evaluate each retrieved chunk individually rather than the entire context as one block: Chunk 1 → Relevant, Chunk 2 → Irrelevant, Chunk 3 → Highly relevant, Chunk 4 → Partially relevant. This gives detailed information about retrieval quality.

## 14. Simple Relevance Scoring

A simple scale: `0 = completely irrelevant`, `1 = slightly relevant`, `2 = moderately relevant`, `3 = highly relevant`. For "what is the prerequisite for Machine Learning?": Chunk A "Probability and Statistics is a prerequisite." → 3. Chunk B "Machine Learning is worth 3 credits." → 1. Chunk C "The university library closes at 8 PM." → 0. Now we have a relevance profile.

## 15. Average Context Relevance

Suppose the scores are `[3, 3, 2, 0, 0]`. Average: `(3+3+2+0+0)/5 = 1.6`. So the retrieved context contains substantial noise. This kind of score can help compare retrieval configurations.

## 16. But Average Alone Can Hide Problems

System A: `[3, 3, 3, 0, 0]` → average 1.8. System B: `[2, 2, 2, 2, 2]` → average 2.0. Both averages are close, but their behavior is different: System A has excellent evidence mixed with irrelevant chunks; System B has consistently moderate relevance. Therefore, don't reduce evaluation to one number without inspecting the underlying cases. **Metrics summarize behavior; individual examples explain behavior.**

## 17. How Do We Evaluate Context Relevance?

**Approach 1 — Ground Truth.** With labeled data like `{"question": "...", "relevant_chunks": ["chunk_7"]}`, compare retrieved chunks against known relevant chunks — connects to Recall, Precision, MRR, NDCG.

**Approach 2 — Human Evaluation.** A human inspects Question + Retrieved Context and scores 0/1/2. Often useful for building an evaluation dataset — high-quality but expensive at scale.

**Approach 3 — LLM-as-a-Judge.** Ask an evaluator model to score relevance, e.g. `{"score": 3, "reason": "The context directly provides the prerequisite."}`. Again: the judge is an evaluator, not absolute truth — validate judge behavior using human-labeled examples.

## 18. Simple Python Implementation

Conceptually:

```
def evaluate_context_relevance(question, context):
    prompt = f\"\"\"
    Evaluate how relevant the context is for answering the question.

    Question:
    {question}

    Context:
    {context}

    Score:
    0 = irrelevant
    1 = partially relevant
    2 = highly relevant

    Return JSON.
    \"\"\"

    return call_llm(prompt)
```

The important part is the evaluation relationship: Question + Context → Relevance Judge.

## 19. Context Relevance in Hybrid Search

Especially useful for your previous work with BM25, Dense Retrieval, RRF, and Reranking:

```
Dense                Average Context Relevance = 1.8
BM25                 Average Context Relevance = 1.7
Hybrid               Average Context Relevance = 2.2
Hybrid + Reranker    Average Context Relevance = 2.6
```

This gives you evidence that the reranker is improving the quality of the context delivered to the LLM.

## 20. Context Relevance and Reranking

A reranker takes an initial retrieval of many candidates and reorders them into best candidates. Context relevance lets us ask: did reranking actually move the useful evidence toward the top? Before reranking, the ranking might be `[Tuition, Registration, Prerequisite, Graduation]`; after reranking, `[Prerequisite, Course description, Registration, Tuition]`. If the question asks about prerequisites, the second ranking is clearly more useful.

## 21. Context Relevance and Query Rewriting

Suppose the user asks "Can I take ML?" and a query rewriting system transforms it into "What are the prerequisites and registration requirements for the Machine Learning course?" Now evaluate context relevance for the original query's retrieval vs. the rewritten query's retrieval. If context relevance improves significantly, you have evidence that query rewriting helps.

## 22. Context Relevance Is Question-Dependent

A chunk can be relevant to one question but irrelevant to another. "Machine Learning is a 3-credit course." is highly relevant ✅ for "what is the credit value of Machine Learning?" but low relevance ❌ for "what is the prerequisite for Machine Learning?" **Relevance cannot be judged independently of the question.** One of the most important ideas in retrieval evaluation.

## 23. A Realistic Academic Assistant Example

Question: "Can I register Machine Learning without passing Probability and Statistics?" Retriever returns: Chunk 1 (credit hours) → Low, Chunk 2 (prerequisite) → High, Chunk 3 (registration portal) → Moderate, Chunk 4 (credit-hour cost) → Irrelevant. The most important chunk is Chunk 2. If your retriever ranks Chunk 4 first, that's a clear retrieval-quality problem.

## 24. Context Relevance and Context Compression

Suppose you retrieve 10 chunks, then a compression step reduces them to 3 focused chunks. Before: 10 chunks, average relevance = 1.7. After: 3 chunks, average relevance = 2.8. But don't stop there — you also need to check: **did compression accidentally remove important evidence?** This connects back to Recall. You want high relevance **and** preserved necessary evidence, not simply less context.

## 25. Context Relevance vs Context Recall

**Context Recall** — did we retrieve the relevant evidence that we needed? **Context Relevance** — how relevant is the context we retrieved to the question?

```
Recall    → Don't miss important evidence.
Relevance → Don't include unnecessary evidence.
```

This mirrors the precision/recall trade-off you learned earlier.

## 26. The Complete RAG Evaluation Model

```
                         RAG
                          │
                    User Question
                          │
                          ↓
                      Retrieval
                          │
             ┌────────────┴────────────┐
             ↓                         ↓
       Retrieval Metrics        Context Relevance
             │                         │
       Recall@K, MRR, etc.       Is context useful?
             │                         │
             └────────────┬────────────┘
                          ↓
                        LLM
                          │
             ┌────────────┴────────────┐
             ↓                         ↓
       Faithfulness              Answer Relevance
             │                         │
       Supported by context?     Answers question?
```

Now you can diagnose much more precisely.

## 27. Failure Diagnosis

**Case A** — Retrieval bad, context relevance low, answer bad → likely a **retrieval problem**.

**Case B** — Retrieval good, context relevance high, faithfulness low → likely a **generation problem**: the LLM received good evidence but didn't use it correctly.

**Case C** — Context relevance high, faithfulness high, answer relevance low → the model may have faithfully summarized the context but failed to answer the user's actual question.

**Case D** — Retrieval good, context relevance high, faithfulness high, answer relevance high → **that's the target.**

## 28. The Engineering Mindset

Instead of "my RAG isn't working," you can now say: "Retrieval Recall@5 is 91%, but context relevance dropped after increasing K. Faithfulness remains high, but answer relevance decreased." That's a much more professional diagnosis — you're measuring individual components, not treating the AI system as a black box.

## Short Summary

Context Relevance measures how useful the retrieved context is for answering this specific question. Remember: Question → Context = Context Relevance; Context → Answer = Faithfulness; Question → Answer = Answer Relevance. Context can be related to the topic but not useful, partially relevant, highly relevant, or completely irrelevant — and more context isn't necessarily better.

**Key takeaway: The goal of retrieval isn't to find information about the topic. The goal is to find the evidence needed to answer the specific question. Question → did we retrieve the right evidence? (Retrieval Metrics) → is the evidence actually useful? (Context Relevance) → did the LLM stay within that evidence? (Faithfulness) → did it answer the user's question? (Answer Relevance). That is the foundation for debugging RAG systematically.**""",
                "estimated_minutes": 40,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Score Chunk-Level Context Relevance",
                    "description": """Question: "Can I register the Machine Learning course without passing Probability and Statistics?"

The retriever returns:

Chunk A: "Machine Learning is a 3-credit course."
Chunk B: "Probability and Statistics is a prerequisite for Machine Learning."
Chunk C: "Students register courses through the university portal."
Chunk D: "The cost of one credit hour is 1330 EGP."

Answer:

1. Rate each chunk from 0-3 for context relevance (0 = irrelevant, 1 = slightly relevant, 2 = moderately relevant, 3 = highly relevant).
2. Which chunk is the most important evidence?
3. If the retriever returns only [A, C, D], what type of retrieval problem do you have?
4. If it returns [B, A, C, D] but the LLM answers "Machine Learning is a 3-credit course," is the likely problem retrieval or generation?
5. Explain the difference between context relevance, faithfulness, and answer relevance.""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "context-relevance", "chunk-scoring"],
                },
                {
                    "title": "Compute Average Context Relevance and Compare Configurations",
                    "description": """Write a function `average_context_relevance(scores)` that returns the mean of a list of chunk relevance scores (0-3 scale).

Then, given these relevance score lists for four retrieval configurations, compute and print the average for each:

```
dense = [2, 1, 2, 1, 1]
bm25 = [1, 2, 1, 1, 2]
hybrid = [3, 2, 2, 1, 1]
hybrid_reranker = [3, 3, 2, 2, 1]
```

Finally, write one print statement identifying which configuration has the highest average, and explain in a comment why you should still inspect individual scores rather than relying on the average alone (referencing the lesson's System A vs System B example).""",
                    "starter_code": """def average_context_relevance(scores):
    # TODO: return the mean of the scores list
    pass


dense = [2, 1, 2, 1, 1]
bm25 = [1, 2, 1, 1, 2]
hybrid = [3, 2, 2, 1, 1]
hybrid_reranker = [3, 3, 2, 2, 1]

# TODO: compute and print the average for each configuration
# TODO: identify which configuration has the highest average
# TODO: add a comment explaining why averages alone can hide problems
""",
                    "solution_code": """def average_context_relevance(scores):
    return sum(scores) / len(scores)


dense = [2, 1, 2, 1, 1]
bm25 = [1, 2, 1, 1, 2]
hybrid = [3, 2, 2, 1, 1]
hybrid_reranker = [3, 3, 2, 2, 1]

configs = {
    "dense": dense,
    "bm25": bm25,
    "hybrid": hybrid,
    "hybrid_reranker": hybrid_reranker,
}

averages = {name: average_context_relevance(scores) for name, scores in configs.items()}
for name, avg in averages.items():
    print(name, avg)

best = max(averages, key=averages.get)
print("Best average:", best)

# Note: as the lesson's System A [3,3,3,0,0] vs System B [2,2,2,2,2] example shows,
# two configurations can have similar averages while behaving very differently --
# one may mix excellent evidence with irrelevant noise, the other may be
# consistently mediocre. Always inspect the individual scores, not just the mean.
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "context-relevance", "python"],
                },
            ],
            "quiz": {
                "title": "Context Relevance — Knowledge Check",
                "questions": [
                    {
                        "question": "Question: 'What is the prerequisite for Machine Learning?' Context: 'Machine Learning is a 3-credit course in the AI Engineering program.' Why does the lesson say this context has low relevance despite being about the same course?",
                        "options": [
                            "Because the context is factually incorrect",
                            "Because the context is only topic-related, not question-relevant — it discusses the same subject but doesn't provide the information needed to answer the specific question asked",
                            "Because the context is too short to be relevant",
                            "Because context relevance only applies to numeric answers",
                        ],
                        "correct": 1,
                        "explanation": "This is the lesson's central distinction between topic relevance ('talks about the same subject') and question relevance ('provides information useful for answering the specific question') — same topic does not mean relevant evidence.",
                    },
                    {
                        "question": "Context Relevance: Low. Faithfulness: High. Answer Relevance: Low. What does this specific pattern indicate happened in the RAG pipeline?",
                        "options": [
                            "The LLM hallucinated information not present in the context",
                            "The LLM generated a faithful answer, but the context it received wasn't useful for the question in the first place — retrieval/context is the root problem, not generation",
                            "The retriever performed perfectly and the problem is purely in generation",
                            "This pattern is impossible; faithfulness and answer relevance always move together",
                        ],
                        "correct": 1,
                        "explanation": "This is the lesson's 'powerful example': high faithfulness with low context relevance and low answer relevance shows the LLM faithfully used bad context — the LLM did its job correctly given what it was given, but the context itself was the problem.",
                    },
                    {
                        "question": "Why does the lesson warn against relying only on an average context relevance score, using System A [3,3,3,0,0] (avg 1.8) vs System B [2,2,2,2,2] (avg 2.0)?",
                        "options": [
                            "Because averages should never be computed for context relevance",
                            "Because two systems can have similar averages while behaving very differently — one mixing excellent evidence with irrelevant noise, the other consistently mediocre — so individual scores must be inspected to understand actual behavior",
                            "Because System B is always better whenever its average is higher",
                            "Because context relevance scores must always be integers between 0 and 3",
                        ],
                        "correct": 1,
                        "explanation": "The lesson states this directly: 'metrics summarize behavior; individual examples explain behavior' — similar averages can hide very different underlying score distributions and failure patterns.",
                    },
                    {
                        "question": "Why is the statement 'relevance cannot be judged independently of the question' one of the most important ideas in retrieval evaluation, per the lesson's Machine Learning credit-hours example?",
                        "options": [
                            "Because relevance scores are randomly assigned regardless of context",
                            "Because the same chunk (e.g. 'Machine Learning is a 3-credit course') can be highly relevant for one question (credit value) and low relevance for a different question (prerequisites) about the same topic",
                            "Because only numeric chunks can be evaluated for relevance",
                            "Because context relevance is identical to topic relevance",
                        ],
                        "correct": 1,
                        "explanation": "The lesson demonstrates this exact scenario: the same chunk about credit hours is highly relevant when asked about credit value but has low relevance when asked about prerequisites — relevance is inherently question-dependent.",
                    },
                    {
                        "question": "A team compresses 10 retrieved chunks down to 3 focused chunks, and average context relevance improves from 1.7 to 2.8. What additional check does the lesson insist on before declaring this an improvement?",
                        "options": [
                            "No further check is needed since the relevance score improved",
                            "Checking whether the compression step accidentally removed necessary evidence — connecting back to Recall, since you want high relevance AND preserved necessary evidence, not just less context",
                            "Re-running the compression step multiple times until relevance reaches 3.0",
                            "Switching to a completely different embedding model",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly warns: 'did compression accidentally remove important evidence?' — an improved relevance average alone doesn't guarantee nothing important was lost, which is why Recall must also be checked.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "Prompt Evaluation",
            "slug":              "ai-developer-ai-evaluation-observability-prompt-evaluation",
            "description":       "Move from prompt engineering intuition to prompt evaluation evidence: running controlled experiments against a shared evaluation dataset, measuring multiple dimensions per prompt version, inspecting per-example failures, and avoiding blind single-metric optimization.",
            "order":             11,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "prompt-evaluation", "experimentation"],
            "prerequisite_ids":  [],  # builds on Topics 1-10 of this level (evaluation datasets, faithfulness, answer relevance, LLM-as-a-judge, context relevance)
            "lesson": {
                "title": "Prompt Evaluation",
                "content": """You've already learned prompt engineering. Now we're going to change the mindset from *"how can I write a better prompt?"* to *"how can I prove that one prompt is better than another?"* That difference is extremely important in production AI engineering.

## 1. What Is Prompt Evaluation?

Prompt evaluation is the systematic process of testing a prompt against a dataset and measuring how well the AI system performs. Instead of "write prompt → try it manually → looks good → deploy," we want:

```
Prompt V1
    ↓
Evaluation Dataset
    ↓
Run AI System
    ↓
Measure Results
    ↓
Prompt V2
    ↓
Same Dataset
    ↓
Measure Results
    ↓
Compare
```

The key idea: **don't optimize prompts based on a few examples — evaluate them against a consistent test set.**

## 2. Why Prompt Evaluation Matters

LLMs are probabilistic systems. A prompt change can affect many different types of questions. Prompt V1 ("answer the user using the provided context") gets Faithfulness = 87%, Answer Relevance = 89%. You modify it to Prompt V2 ("answer only using information explicitly supported by the context; if insufficient, say so"). Now Faithfulness = 95%, Answer Relevance = 86%. You improved faithfulness but decreased relevance — so which prompt is better? There isn't necessarily one answer; it depends on your system's objectives.

## 3. Prompt Engineering vs Prompt Evaluation

**Prompt Engineering** — designing instructions that make the model behave better. **Prompt Evaluation** — measuring whether those instructions actually improve behavior.

```
Prompt Engineering
        ↓
Create/change prompt
        ↓
Prompt Evaluation
        ↓
Measure behavior
        ↓
Engineering decision
```

You need both.

## 4. Why Manual Testing Isn't Enough

You test a new prompt with three questions and all look great — you might conclude "the new prompt is better." But question 4 is worse, question 5 is worse, question 6 hallucinates, question 7 has wrong format, question 8 refuses unnecessarily. This is why we need an **evaluation dataset**. You learned about evaluation datasets earlier — now we use them to evaluate prompt changes.

## 5. The Basic Prompt Evaluation Loop

```
                  Prompt V1
                     ↓
              Evaluation Set
                     ↓
                 AI System
                     ↓
                 Metrics
                     ↓
                  Results
                     │
                     ↓
                Change Prompt
                     │
                     ↓
                  Prompt V2
                     ↓
              Same Evaluation Set
                     ↓
                 Same Metrics
                     ↓
                  Compare
```

Notice something extremely important: **the dataset and evaluation procedure stay the same.** Otherwise, your comparison isn't reliable.

## 6. Why the Same Dataset Matters

Prompt V1 tested on 100 questions scores 85%. Prompt V2 tested on a different set of 50 easy questions scores 94%. Can we conclude V2 is better? **No** — maybe V2 got an easier dataset. A fair comparison is Prompt V1 → Dataset A → 85%, Prompt V2 → Dataset A → 89%. Now we have a meaningful comparison.

## 7. A Simple Evaluation Dataset

```
evaluation_cases = [
    {"question": "What is the credit-hour cost?", "expected_answer": "1330 EGP"},
    {"question": "What is the prerequisite for Machine Learning?", "expected_answer": "Probability and Statistics"}
]
```

We can run every prompt version against these same questions.

## 8. Adding Context

For RAG:

```
evaluation_case = {
    "question": "What is the prerequisite for Machine Learning?",
    "expected_answer": "Probability and Statistics",
    "expected_context": ["Probability and Statistics is a prerequisite for Machine Learning."]
}
```

Then our system becomes Question + Retrieved Context + Prompt → LLM → Answer, and we can evaluate the answer.

## 9. What Should We Measure?

```
                 Prompt Evaluation
                        │
       ┌────────────────┼────────────────┐
       ↓                ↓                ↓
   Faithfulness    Answer Relevance   Correctness
       │                │                │
       ↓                ↓                ↓
     95%              91%              89%
```

You could also measure Exact Match, Semantic Similarity, retrieval metrics, context relevance, output format correctness, latency, token usage, and cost. The appropriate metrics depend on what your prompt is supposed to accomplish.

## 10. Prompt Evaluation Is Multi-Dimensional

Prompt V1: Faithfulness 90%, Answer relevance 94%, JSON validity 99%. Prompt V2: Faithfulness 96%, Answer relevance 90%, JSON validity 99%. Neither is universally "better" — V2 is +6% faithfulness, -4% answer relevance. Now you have an engineering trade-off.

## 11. Example: Strict RAG Prompt

Prompt V1: "Answer the user's question using the context." Prompt V2: "Answer only using information explicitly supported by the context. If the context does not contain enough information to answer the question, clearly state that the information is unavailable. Do not introduce facts from your own knowledge."

You suspect V2 will reduce hallucinations. Instead of assuming it works, test V1 on 200 evaluation cases and V2 on 200 evaluation cases, then measure Faithfulness, Answer relevance, and Abstention correctness.

## 12. Controlled Experiments

This is essentially a controlled experiment — change one variable while keeping others as consistent as possible: same model, same temperature, same dataset, same retriever, same Top-K, same context. Only change: **prompt.** Then compare. This makes it easier to attribute the difference to the prompt.

## 13. Why Temperature Can Matter

Comparing Prompt V1 (temperature 0.7) with Prompt V2 (temperature 0), and V2 performs better — can you confidently say "the prompt caused the improvement?" **No.** You changed two variables: prompt + temperature. A cleaner experiment keeps temperature fixed. This is the same scientific thinking used in ML experiments.

## 14. Simple Python Evaluation Loop

```
evaluation_cases = [
    {"question": "What is the prerequisite?", "expected_answer": "Probability and Statistics"},
    {"question": "How many credit hours?", "expected_answer": "160"}
]

prompt_v1 = "Answer the question using the context."
prompt_v2 = "Answer only using information supported by the context. If the answer is not available, say so."

def evaluate_prompt(prompt, dataset):
    results = []
    for case in dataset:
        answer = run_ai_system(prompt=prompt, question=case["question"])
        results.append({"question": case["question"], "answer": answer})
    return results

results_v1 = evaluate_prompt(prompt_v1, evaluation_cases)
results_v2 = evaluate_prompt(prompt_v2, evaluation_cases)

score_v1 = evaluate_results(results_v1)
score_v2 = evaluate_results(results_v2)
```

The important pattern: Prompt → Same Dataset → Same Evaluation → Score.

## 15. Per-Example Evaluation Is Extremely Important

Don't only calculate Prompt V1 → 88%, Prompt V2 → 91%. Also inspect individual cases: Question A → both good; Question B → V1 good, V2 bad; Question C → V1 bad, V2 good. This tells you **why** the score changed. **Averages hide failure patterns.**

## 16. Evaluation Dataset Should Contain Different Question Types

A strong prompt evaluation dataset shouldn't contain only easy questions. Include simple factual questions, multi-hop questions, ambiguous questions, questions with missing information, questions requiring refusal, questions with Arabic wording variations, questions containing typos, and questions requiring calculations. This lets you see whether the prompt generalizes.

## 17. Edge Cases Are Extremely Valuable

"What is the tuition fee?" — your context doesn't contain tuition information. A weak prompt may hallucinate "the tuition fee is 50,000 EGP." A better prompt should say "the provided information does not specify the tuition fee." So your evaluation dataset should deliberately include **questions with missing evidence** — extremely useful for testing RAG prompts.

## 18. Prompt Evaluation Can Test Structured Output

Suppose your AI system must return `{"answer": "...", "confidence": 0.95}`. A prompt change might improve answer quality but cause malformed JSON. Measure Semantic quality **and** Schema validity: Prompt V1 → answer quality 91%, valid JSON 97%. Prompt V2 → answer quality 94%, valid JSON 82%. V2 may be worse for production despite better answer quality — this is why AI evaluation is multi-dimensional.

## 19. Prompt Evaluation for Agents

The same concept applies to AI agents with tools (Search, Calculator, Database, Email). When you change the system prompt, evaluate tool selection, tool arguments, final answer, task completion, unnecessary tool calls, and safety behavior. Prompt V1 → correct tool selection 84%. Prompt V2 → correct tool selection 93%. Now you have measurable evidence the prompt improved agent behavior.

## 20. Prompt Evaluation and Regression

V1: Faithfulness = 91%. You improve the prompt: V2: Faithfulness = 95%. Looks great. But Answer relevance: V1 = 93%, V2 = 84%. You accidentally caused a **regression**. Therefore: every prompt change should ideally be evaluated against the existing test suite.

## 21. Evaluation Dataset as a Safety Net

```
                AI System
                    │
                    ↓
             Change Prompt
                    │
                    ↓
             Run Test Suite
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
       Improved             Worse
          ↓                   ↓
      Continue            Investigate
```

This turns prompt engineering from **trial and error** into **engineering iteration.**

## 22. Prompt Versioning

Don't just have a single `system_prompt.txt` overwritten every time. Track versions conceptually:

```
prompts = {
    "v1": "...",
    "v2": "...",
    "v3": "..."
}
```

Then evaluation results can be associated with versions:

| Version | Faithfulness | Relevance | JSON |
|---|---|---|---|
| V1 | 89% | 93% | 99% |
| V2 | 94% | 91% | 99% |
| V3 | 96% | 94% | 95% |

Now you have an experimental history.

## 23. Don't Optimize for One Metric Blindly

Suppose you optimize exclusively for faithfulness — you might create an overly conservative prompt: "if there is any uncertainty, refuse to answer." Faithfulness might become 99%, but answer usefulness could collapse — answer relevance = 70%. **The highest individual metric isn't necessarily the best system.** You need to optimize for the overall product objective.

## 24. A Better Way: Define Evaluation Criteria First

Before modifying a prompt, decide what success means. For example: Primary — Faithfulness ≥ 95%. Secondary — Answer relevance ≥ 90%. Required — JSON validity ≥ 99%. Then evaluate. Much better than "let's tweak the prompt and see what happens."

## 25. Statistical Thinking

Prompt V1 → 90%, Prompt V2 → 91%. Is V2 really better? Maybe — but the difference could be small enough that it doesn't represent a meaningful improvement, especially with a small dataset or noisy judge. 20 evaluation cases can produce unstable percentages, while 1000 carefully selected cases give a much stronger basis for comparison. **Dataset quality and size affect how much confidence you should have in evaluation results.**

## 26. LLM-as-a-Judge in Prompt Evaluation

For each output: Question + Answer + evaluation rubric → judge scores Relevance 1-5, Faithfulness 1-5. Then compare averages across prompt versions. But remember: the judge itself can introduce bias, so use a consistent judge, clear rubrics, validate against human examples, inspect individual cases, and avoid treating judge scores as absolute truth.

## 27. Pairwise Prompt Evaluation

Instead of "how good is V2?" ask "which answer is better: V1 or V2?" Question: "What is the prerequisite?" Answer A: "Probability and Statistics." Answer B: "The course has a prerequisite in mathematics." Judge: A is better. Run this across many questions — useful when absolute scoring is difficult.

## 28. Prompt Evaluation Pipeline

```
             Prompt V1
                 │
                 ↓
        Evaluation Dataset
                 │
                 ↓
          Run AI Pipeline
                 │
                 ↓
          Collect Outputs
                 │
                 ↓
       ┌─────────┼─────────┐
       ↓         ↓         ↓
  Relevance  Faithfulness  Format
       │         │         │
       └─────────┼─────────┘
                 ↓
              Results
                 ↓
          Compare with V2
                 ↓
          Accept / Reject
```

That's prompt evaluation as an engineering process.

## 29. The Most Important Principle

If you change Prompt V1 to V2, manually test 3 examples, and declare "V2 is better" — that's not reliable evaluation. Instead: V1 → 500 cases → metrics, V2 → 500 cases → metrics. Then inspect overall scores + individual failures + failure categories. Now you can make an informed decision.

## 30. Your AI Engineering Workflow

```
                    Change
                      ↓
              Prompt / Model /
              Retriever / Logic
                      ↓
              Evaluation Suite
                      ↓
          ┌───────────┴───────────┐
          ↓                       ↓
       Metrics                 Examples
          ↓                       ↓
   Did it improve?          Why did it change?
          │                       │
          └───────────┬───────────┘
                      ↓
                Engineering
                  Decision
```

This mindset will become essential when we reach Regression Testing.

## Short Summary

Prompt evaluation means systematically measuring how a prompt performs rather than judging it from a few manual examples. The basic workflow: Prompt V1 → Evaluation Dataset → Metrics → Results; Prompt V2 → Same Dataset → Same Metrics → Compare. Important principles: use the same dataset for fair comparison, control other variables when possible, evaluate multiple dimensions, inspect individual failures (not just averages), include difficult and edge cases, version your prompts, don't optimize one metric blindly, and validate LLM judges rather than treating them as ground truth.

**Key takeaway: Prompt engineering creates hypotheses. Prompt evaluation provides evidence. Instead of "I think Prompt V2 is better," you should be able to say "on our 500-case evaluation dataset, Prompt V2 improved faithfulness from 91% to 96% while maintaining answer relevance above our 90% target." That is AI engineering rather than prompt trial-and-error.**""",
                "estimated_minutes": 45,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Compare Two Prompt Versions Against Requirements",
                    "description": """You have an academic RAG assistant.

Prompt V1: "Answer the question using the provided context."
Results on 200 evaluation cases: Faithfulness 90%, Answer Relevance 94%.

Prompt V2: "Answer only using information explicitly supported by the provided context. If the context is insufficient, say that the information is unavailable."
Results: Faithfulness 96%, Answer Relevance 88%.

Answer:

1. Which prompt has better faithfulness?
2. Which has better answer relevance?
3. Is V2 automatically better overall?
4. If your production requirement is Faithfulness ≥ 95% AND Answer Relevance ≥ 90%, does either prompt satisfy both requirements?
5. What would you try next: improve V1, improve V2, or create V3? Why?
6. Why should you run V1 and V2 on the same evaluation dataset?""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "prompt-evaluation", "trade-off-analysis"],
                },
                {
                    "title": "Build a Multi-Metric Prompt Comparison Table",
                    "description": """Write a function `compare_prompt_versions(results)` where `results` is a dict mapping version name to a dict of metric name -> score (0-100), and criteria is a dict mapping metric name -> minimum required score. The function should return a dict mapping version name to `True`/`False` for whether that version meets ALL the given criteria.

Then use it with:

```
results = {
    "v1": {"faithfulness": 90, "answer_relevance": 94, "json_validity": 99},
    "v2": {"faithfulness": 96, "answer_relevance": 88, "json_validity": 99},
    "v3": {"faithfulness": 95, "answer_relevance": 91, "json_validity": 97},
}

criteria = {"faithfulness": 95, "answer_relevance": 90, "json_validity": 99}
```

Print which version(s), if any, satisfy all the criteria.""",
                    "starter_code": """def compare_prompt_versions(results, criteria):
    # TODO: for each version, check if ALL its metrics meet or exceed the criteria
    # return a dict: {version_name: True/False}
    pass


results = {
    "v1": {"faithfulness": 90, "answer_relevance": 94, "json_validity": 99},
    "v2": {"faithfulness": 96, "answer_relevance": 88, "json_validity": 99},
    "v3": {"faithfulness": 95, "answer_relevance": 91, "json_validity": 97},
}

criteria = {"faithfulness": 95, "answer_relevance": 90, "json_validity": 99}

# TODO: call compare_prompt_versions and print which versions pass
""",
                    "solution_code": """def compare_prompt_versions(results, criteria):
    verdicts = {}
    for version, metrics in results.items():
        passes = all(
            metrics.get(metric_name, 0) >= min_score
            for metric_name, min_score in criteria.items()
        )
        verdicts[version] = passes
    return verdicts


results = {
    "v1": {"faithfulness": 90, "answer_relevance": 94, "json_validity": 99},
    "v2": {"faithfulness": 96, "answer_relevance": 88, "json_validity": 99},
    "v3": {"faithfulness": 95, "answer_relevance": 91, "json_validity": 97},
}

criteria = {"faithfulness": 95, "answer_relevance": 90, "json_validity": 99}

verdicts = compare_prompt_versions(results, criteria)
for version, passed in verdicts.items():
    print(version, "->", "PASS" if passed else "FAIL")
# Expected: v1 -> FAIL, v2 -> FAIL, v3 -> FAIL (v3 fails only json_validity: 97 < 99)
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "prompt-evaluation", "python"],
                },
            ],
            "quiz": {
                "title": "Prompt Evaluation — Knowledge Check",
                "questions": [
                    {
                        "question": "Prompt V1 is tested on 100 questions and scores 85%. Prompt V2 is tested on a different set of 50 easier questions and scores 94%. What is the correct conclusion?",
                        "options": [
                            "V2 is clearly the better prompt since it scored higher",
                            "No valid conclusion can be drawn — the comparison is unfair because the two prompts were evaluated on different datasets, so a fair comparison requires running both on the same dataset",
                            "V1 is clearly the better prompt since it was tested on more questions",
                            "Both prompts are equally good since the difference is just 9%",
                        ],
                        "correct": 1,
                        "explanation": "The lesson makes this exact point: comparing scores across different datasets (especially when one is easier) doesn't tell you which prompt is actually better — a fair comparison requires the same dataset for both versions.",
                    },
                    {
                        "question": "A team changes both the prompt and the temperature setting at the same time, and observes improved results. Why can't they confidently attribute the improvement to the prompt change?",
                        "options": [
                            "Because temperature never affects LLM output quality",
                            "Because two variables were changed simultaneously, so the improvement could be due to either the prompt, the temperature, or their interaction — a controlled experiment should change only one variable at a time",
                            "Because prompt evaluation only works with temperature = 1.0",
                            "Because it's impossible to measure the effect of temperature changes",
                        ],
                        "correct": 1,
                        "explanation": "This is the lesson's controlled-experiment principle: changing multiple variables (prompt + temperature) at once makes it impossible to know which change caused the improvement — you must isolate one variable at a time.",
                    },
                    {
                        "question": "Prompt V1 scores 88% overall and Prompt V2 scores 91% overall. Why does the lesson insist on also inspecting per-example results (e.g. Question B: V1 good, V2 bad) rather than relying only on the aggregate scores?",
                        "options": [
                            "Because aggregate scores are always incorrect",
                            "Because averages can hide the fact that a prompt change improved some cases while making others worse, and understanding these individual shifts explains WHY the score changed, not just THAT it changed",
                            "Because per-example inspection is required by law for AI systems",
                            "Because aggregate scores cannot be computed for prompts",
                        ],
                        "correct": 1,
                        "explanation": "The lesson states directly: 'averages hide failure patterns' — per-example inspection reveals cases that got better or worse, which the aggregate score alone cannot show.",
                    },
                    {
                        "question": "A team optimizes a prompt exclusively for faithfulness, achieving 99% faithfulness by making the model refuse to answer whenever there's any uncertainty — but answer relevance collapses to 70%. What principle does this illustrate?",
                        "options": [
                            "Faithfulness should always be the only metric that matters",
                            "The highest score on a single metric isn't necessarily the best system overall — you need to optimize for the overall product objective across multiple dimensions, not blindly maximize one metric",
                            "This is an ideal outcome since faithfulness is the most important RAG metric",
                            "Answer relevance is not a useful metric for production systems",
                        ],
                        "correct": 1,
                        "explanation": "The lesson uses this exact example to warn against blindly optimizing one metric: an overly conservative prompt can achieve near-perfect faithfulness while destroying the system's actual usefulness (answer relevance).",
                    },
                    {
                        "question": "Prompt V1 scores 90% and Prompt V2 scores 91% on a 20-case evaluation dataset. Why does the lesson urge caution before concluding V2 is meaningfully better?",
                        "options": [
                            "Because percentages under 95% should always be rejected",
                            "Because a small dataset (like 20 cases) can produce unstable percentages, so a 1-point difference may not represent a real improvement — larger, carefully selected datasets give a stronger basis for comparison",
                            "Because prompt evaluation cannot be done with fewer than 1000 cases under any circumstances",
                            "Because 91% is always considered a failing score regardless of context",
                        ],
                        "correct": 1,
                        "explanation": "This is the lesson's 'statistical thinking' section: with a small or noisy dataset, small score differences may not be meaningful, and larger datasets (e.g. 1000 cases) provide much more confidence in the comparison.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "Regression Testing",
            "slug":              "ai-developer-ai-evaluation-observability-regression-testing",
            "description":       "Make sure a change that improves one part of an AI system doesn't silently break something else: building a regression suite from your evaluation dataset, protecting critical test cases, evaluation gates and thresholds, and accounting for LLM variability so you don't chase phantom regressions.",
            "order":             12,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "evaluation", "regression-testing", "ci-cd"],
            "prerequisite_ids":  [],  # builds on "Prompt Evaluation" (this level, topic 11) and prior evaluation dimensions (topics 1-10)
            "lesson": {
                "title": "Regression Testing",
                "content": """You've learned how to evaluate a prompt. Now we solve a very important production problem: *how do we make sure a change that improves one part of our AI system doesn't silently break something else?* That's the purpose of **regression testing.**

## 1. What Is Regression Testing?

In traditional software, a **regression** is when a previously working behavior becomes broken after a change. The same idea applies to AI systems. Version 1: Question A ✅, B ✅, C ✅. You modify the prompt. Version 2: Question A ✅, B ❌, C ✅. You introduced a regression — the system improved or changed, but something that previously worked no longer works.

## 2. Why AI Regression Testing Is Different

Traditional software often has deterministic outputs (`assert add(2, 3) == 5`). AI systems are different: Input → LLM → Generated Output, and the output may vary with no single exact correct string. Therefore, **AI regression testing often evaluates behavior and quality, not just exact outputs.**

## 3. The Mental Model

Think of your evaluation dataset as a safety net:

```
                 AI System
                     │
                     ↓
                 Make Change
                     │
                     ↓
              Regression Suite
                     │
          ┌──────────┴──────────┐
          ↓                     ↓
      Still Good?           Something Worse?
          ↓                     ↓
       Deploy               Investigate
```

Your evaluation dataset becomes an automated test suite for AI behavior.

## 4. Simple Example

Five important test questions all pass in Version 1 (A✅ B✅ C✅ D✅ E✅). You change the system prompt. Version 2: A✅ B✅ C❌ D✅ E❌. Even if the overall evaluation score increased, you should investigate.

## 5. The Dangerous Scenario

Version 1: Faithfulness 91%, Answer Relevance 90%. Version 2: Faithfulness 96%, Answer Relevance 92%. Looks excellent — but then you discover Arabic questions: V1 → 94%, V2 → 78%. Your overall score hid a serious regression. **This is why aggregate metrics aren't enough.**

## 6. Evaluation Dataset → Regression Suite

Earlier we called it an **evaluation dataset**. When we repeatedly use it to verify changes, it effectively becomes a **regression test suite**. `evaluation_dataset.json` might contain a list of `{"id": ..., "question": ..., "expected_answer": ...}` entries. Every time you change your AI system: run `evaluation_dataset.json` and compare against the previous baseline.

## 7. What Can Cause a Regression?

A regression isn't necessarily caused by a prompt — it can come from almost anywhere: **prompt change** (V1 → V2), **model change** (Model A → B), **retriever change** (Top-K 5 → 10), **embedding change**, **reranker change**, **chunking change** (chunk size 500 → 800), **data change** (old documents → new documents), or **infrastructure change** (API configuration). Any of these can alter system behavior.

## 8. AI Systems Are Pipelines

Regression testing should consider the entire pipeline:

```
User Question
      ↓
Query Processing
      ↓
Retriever
      ↓
Reranker
      ↓
Context
      ↓
Prompt
      ↓
LLM
      ↓
Answer
```

A change in one component can affect everything downstream. So you can't always isolate the problem by looking only at the final answer.

## 9. Component-Level Regression Testing

Instead of testing only Question → Final Answer, test intermediate stages. **Retrieval**: evaluate Recall@K, Precision@K, MRR, NDCG. **Context**: evaluate Context relevance and context coverage. **Generation**: evaluate Faithfulness, Answer relevance, Correctness. Now you can identify where a regression occurred.

## 10. Example: Debugging a Regression

Before: Retrieval Recall@5 92%, Faithfulness 94%, Answer Relevance 93%. After: Retrieval Recall@5 75%, Faithfulness 83%, Answer Relevance 81%. Everything got worse — strongly suggests the problem may be **upstream** (e.g. embedding model or retriever configuration), rather than the prompt.

## 11. Another Scenario

Before: Retrieval Recall@5 92%, Faithfulness 94%, Answer Relevance 93%. After: Retrieval Recall@5 92% (stable), Faithfulness 82%, Answer Relevance 80%. Retrieval stayed stable — this suggests the problem is probably **downstream** of retrieval: prompt change, model change, generation parameters, context formatting, or output parsing. This is why stage-level evaluation is so powerful.

## 12. Regression Testing Isn't Just "Did the Score Go Down?"

Version 1: 90%. Version 2: 91%. Looks better — but maybe 20% of *critical* cases became worse. A question like "can I register this course without its prerequisite?" might be much more important than "how many credits is the course?" So evaluation should consider **case importance.**

## 13. Critical Test Cases

Mark certain cases as critical: `{"id": "registration_001", "question": "...", "importance": "critical"}`. A regression in that case can block deployment even if the overall score improves. Overall score: 91% → 93% ✅. Critical cases: 98% → 81% ❌. You probably shouldn't deploy.

## 14. Regression Thresholds

Define acceptable limits: `Faithfulness ≥ 95%`, `Answer relevance ≥ 90%`, `Retrieval Recall@5 ≥ 90%`, and "no critical test may regress." Your CI/CD pipeline can then decide:

```
Evaluation
    ↓
All thresholds satisfied?
    │
 ┌──┴──┐
YES    NO
 ↓      ↓
Deploy  Block
```

This is a major step toward production AI engineering.

## 15. Example Evaluation Gate

```
metrics = {"faithfulness": 0.96, "answer_relevance": 0.92, "retrieval_recall": 0.91}
thresholds = {"faithfulness": 0.95, "answer_relevance": 0.90, "retrieval_recall": 0.90}

def passes_evaluation(metrics, thresholds):
    for metric, minimum in thresholds.items():
        if metrics[metric] < minimum:
            return False
    return True
```

Conceptually: `96% ≥ 95% ✅`, `92% ≥ 90% ✅`, `91% ≥ 90% ✅` — deployment allowed.

## 16. Detecting Individual Regressions

Compare outputs case-by-case:

```
previous = {"qa_001": 0.95, "qa_002": 0.91, "qa_003": 0.88}
current  = {"qa_001": 0.97, "qa_002": 0.92, "qa_003": 0.61}
```

`qa_001 → +2%`, `qa_002 → +1%`, `qa_003 → -27%`. Overall performance might still increase, but `qa_003` deserves investigation.

## 17. Failure Categories

When a regression occurs, don't just write "test failed" — categorize it: Retrieval, Hallucination, Missing information, Wrong answer, Irrelevant answer, Formatting, Language, Refusal, Tool usage. Now your evaluation dataset becomes a source of engineering insights.

## 18. Regression Testing for Your Arabic RAG

Dataset: 100 English + 100 Arabic + 50 ambiguous + 50 missing-context + 50 multi-hop = 350 cases. After a prompt change, overall: 91% → 93%. Breakdown: English 93%→95%, Arabic 92%→84%, Missing context 89%→96%, Multi-hop 87%→88%. Now you know: **the new prompt improved missing-context behavior but caused a regression in Arabic questions.** Much more actionable than just "score = 93%."

## 19. Regression Testing and Git

Integrate evaluation with your normal software workflow: Developer modifies prompt → `git commit` → CI pipeline → run evaluation suite → metrics → pass/fail. Your AI evaluation suite becomes part of the repository, alongside `tests/test_api.py`, `tests/test_retrieval.py`, `tests/test_evaluation.py`.

## 20. Regression Testing in CI/CD

```
Developer changes prompt
          ↓
       Git Push
          ↓
      CI Pipeline
          ↓
   Build AI Application
          ↓
   Run Evaluation Suite
          ↓
   ┌──────┴───────┐
   ↓              ↓
 PASS            FAIL
   ↓              ↓
 Deploy        Block Deploy
```

You don't need someone to manually remember "let's test the RAG system before deploying" — the system does it automatically.

## 21. But AI Tests Can Be Flaky

LLM outputs may vary even without a prompt change: Run 1 → good, Run 2 → good, Run 3 → slightly different. This can cause unstable evaluation. Ways to reduce this: lower temperature when appropriate, structured outputs, deterministic evaluation where possible, stable evaluation datasets, robust scoring, and repeated runs for important tests. The goal is to distinguish **real regression** from **normal model variability.**

## 22. Regression Testing and LLM-as-a-Judge

If using an LLM judge, the judge itself can introduce variability: Run 1 → 4/5, Run 2 → 5/5, Run 3 → 4/5. Therefore: don't blindly interpret tiny score changes as meaningful regressions — you need sensible thresholds and validation.

## 23. Golden Test Cases

A **golden test case** is a carefully selected example representing important expected behavior: `{"question": "What is the prerequisite for Machine Learning?", "expected_behavior": "The answer must identify Probability and Statistics."}` You might maintain a collection organized by Retrieval, Hallucination, Arabic, Edge Cases, Safety, Tool Usage, and Formatting. These cases provide a stable core regression suite.

## 24. Regression Testing Isn't Only About Preventing Lower Scores

V1: unknown information → "I don't know." After a prompt change, V2: unknown information → hallucinated answer. Even if the average score barely changes, this is a serious **behavioral regression.** Regression testing should protect important properties, not just aggregate metrics.

## 25. Property-Based AI Testing

Instead of requiring one exact answer, define properties. Property: "the assistant must not answer using unsupported information." Test: context "the course is worth 3 credits," question "who is the university president?" — expected behavior: do not invent an answer. Often more appropriate for AI than exact string matching.

## 26. Regression Testing Across Models

Don't assume a newer model is better. Run the same evaluation dataset against Model A and Model B, then compare quality, cost, latency, failure rate, tool usage, and structured output reliability. A model can be better in one dimension and worse in another.

## 27. Regression Testing Across Retrieval Configurations

Test Top-K=5 vs Top-K=10, or Dense vs Hybrid+Reranking. For each configuration: retrieval metrics + context relevance + faithfulness + answer relevance. Now you're doing system optimization based on evidence.

## 28. The Complete Evaluation Loop

```
                 ┌─────────────────┐
                 │  AI System      │
                 └────────┬────────┘
                          ↓
                    Evaluation
                          ↓
                     Results
                          ↓
                    Find Failure
                          ↓
                     Make Change
                          ↓
                  Regression Suite
                          ↓
                 ┌────────┴────────┐
                 ↓                 ↓
               Better            Worse
                 ↓                 ↓
              Deploy           Investigate
                 │                 │
                 └────────┬────────┘
                          ↓
                    New Evaluation
```

This loop is how AI systems continuously improve without blindly breaking previous behavior.

## 29. A Real Production Example

FastAPI RAG service: `POST /chat → Query processing → Qdrant → Reranker → LLM → Response`. You modify the prompt. Before deployment, run 500 evaluation cases: Faithfulness 94%→96% ✅, Answer Relevance 91%→93% ✅, Retrieval Recall 92%→92% —, Arabic Accuracy 94%→89% ❌, Critical Cases 98%→98% ✅. Clear decision: **don't immediately deploy** — investigate why Arabic performance decreased (prompt wording, stricter output constraints, removed Arabic examples, different model behavior with new instructions). Much better than discovering the problem after users complain.

## 30. The Core Principle

**Every meaningful change to an AI system should be tested against previously known behavior** — prompts, models, retrievers, embeddings, rerankers, chunking, data, tools, agent logic, output schemas. Your evaluation dataset becomes the memory of "what good behavior looked like before this change."

## Short Summary

Regression testing answers: did a change break something that previously worked? For AI systems: Change → Run Evaluation Suite → Compare Against Baseline → Inspect Metrics → Inspect Individual Failures → Deploy/Reject/Investigate. Important principles: AI regression tests often evaluate quality, not exact strings; test the same dataset across versions; measure multiple dimensions; protect critical test cases; evaluate intermediate RAG components when possible; use thresholds and evaluation gates; watch for changes hidden by averages; account for LLM variability; store important cases as a regression suite; integrate evaluation into CI/CD when practical.

**Key takeaway: A good AI system isn't one that improves every time you change it — it's one that improves without silently breaking the behaviors you already trusted. Your evaluation suite is therefore not just a measurement tool. It becomes a safety net for AI development.**""",
                "estimated_minutes": 45,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Diagnose a Regression from Metric Breakdowns",
                    "description": """Your Arabic university RAG system has this baseline:

Version 1: Retrieval Recall@5 92%, Faithfulness 94%, Answer Relevance 93%, Arabic Accuracy 95%.

You change the system prompt. Version 2: Retrieval Recall@5 92%, Faithfulness 97%, Answer Relevance 95%, Arabic Accuracy 86%.

Answer:

1. Did the system improve overall?
2. What regression occurred?
3. Since Retrieval Recall stayed at 92%, is the retriever likely responsible?
4. Which part of the system would you investigate first?
5. Should you deploy Version 2 immediately? Why?
6. Give two regression test cases you would add specifically to protect Arabic behavior.
7. Why is testing only the overall average dangerous?""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "regression-testing", "diagnostic-reasoning"],
                },
                {
                    "title": "Build an Evaluation Gate with Critical-Case Protection",
                    "description": """Write a function `passes_evaluation(metrics, thresholds, critical_case_deltas)` where:

- `metrics` is a dict of metric name -> current score (0.0-1.0).
- `thresholds` is a dict of metric name -> minimum required score.
- `critical_case_deltas` is a dict of critical test case id -> score change (e.g. `-0.05` means it dropped by 5 points).

The function should return `False` (block deployment) if ANY metric is below its threshold, OR if ANY critical case delta is negative (regressed at all). Otherwise return `True` (allow deployment).

Test it with:

```
metrics = {"faithfulness": 0.96, "answer_relevance": 0.92, "retrieval_recall": 0.91}
thresholds = {"faithfulness": 0.95, "answer_relevance": 0.90, "retrieval_recall": 0.90}
critical_case_deltas = {"registration_001": 0.02, "prereq_003": -0.17}
```

and print whether deployment should proceed, explaining which condition caused the result.""",
                    "starter_code": """def passes_evaluation(metrics, thresholds, critical_case_deltas):
    # TODO: return False if any metric is below threshold
    # TODO: return False if any critical case delta is negative
    # TODO: otherwise return True
    pass


metrics = {"faithfulness": 0.96, "answer_relevance": 0.92, "retrieval_recall": 0.91}
thresholds = {"faithfulness": 0.95, "answer_relevance": 0.90, "retrieval_recall": 0.90}
critical_case_deltas = {"registration_001": 0.02, "prereq_003": -0.17}

# TODO: call passes_evaluation and print the result with an explanation
""",
                    "solution_code": """def passes_evaluation(metrics, thresholds, critical_case_deltas):
    for metric, minimum in thresholds.items():
        if metrics.get(metric, 0) < minimum:
            return False

    for case_id, delta in critical_case_deltas.items():
        if delta < 0:
            return False

    return True


metrics = {"faithfulness": 0.96, "answer_relevance": 0.92, "retrieval_recall": 0.91}
thresholds = {"faithfulness": 0.95, "answer_relevance": 0.90, "retrieval_recall": 0.90}
critical_case_deltas = {"registration_001": 0.02, "prereq_003": -0.17}

result = passes_evaluation(metrics, thresholds, critical_case_deltas)
print("Deploy:", result)
if not result:
    print("Blocked because critical case 'prereq_003' regressed by -0.17 even though all metric thresholds were met.")
# Expected: Deploy: False
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "regression-testing", "python"],
                },
            ],
            "quiz": {
                "title": "Regression Testing — Knowledge Check",
                "questions": [
                    {
                        "question": "Version 1: Faithfulness 91%, Answer Relevance 90%. Version 2: Faithfulness 96%, Answer Relevance 92%. But a breakdown reveals Arabic questions dropped from 94% to 78%. What does this scenario demonstrate?",
                        "options": [
                            "Version 2 is unambiguously better since both headline metrics improved",
                            "Aggregate metrics can hide a serious regression in a specific segment (Arabic questions), which is why breaking results down by category is essential before deploying",
                            "Arabic questions should be removed from the evaluation dataset since they cause problems",
                            "Faithfulness and Answer Relevance cannot be measured for Arabic content",
                        ],
                        "correct": 1,
                        "explanation": "This is the lesson's 'dangerous scenario': both headline metrics improved, but a segment-level regression (Arabic accuracy) was completely hidden by the aggregate numbers — exactly why aggregate metrics aren't enough.",
                    },
                    {
                        "question": "Before a change: Retrieval Recall@5 92%, Faithfulness 94%, Answer Relevance 93%. After: Retrieval Recall@5 92% (unchanged), Faithfulness 82%, Answer Relevance 80%. Where should you focus your investigation first?",
                        "options": [
                            "The retriever, since retrieval metrics are always the root cause",
                            "Downstream of retrieval — since retrieval recall stayed stable, the likely causes are prompt changes, model changes, generation parameters, context formatting, or output parsing",
                            "The embedding model, since faithfulness always depends on embeddings",
                            "There's nothing to investigate since retrieval recall didn't change",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's component-level diagnosis: since retrieval stayed stable while faithfulness and answer relevance dropped, the problem is likely downstream of retrieval (prompt, model, or generation-related), not in the retriever itself.",
                    },
                    {
                        "question": "Overall score improves from 91% to 93%, but a 'critical' test case (e.g. registration eligibility) drops from 98% to 81%. According to the lesson, what should happen?",
                        "options": [
                            "Deploy immediately since the overall score improved",
                            "The deployment decision should account for critical case regressions even when the overall average improves — a regression in a critical case can block deployment despite a higher aggregate score",
                            "Critical cases should be excluded from evaluation to avoid blocking deployment",
                            "The overall score is invalid if any single case decreases",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly states that marking cases as 'critical' allows a regression in one of them to block deployment even if the overall score improved — case importance matters, not just the aggregate.",
                    },
                    {
                        "question": "An LLM judge scores the same unchanged system output as 4/5, 5/5, and 4/5 across three separate runs. What does the lesson say this variability implies for regression testing?",
                        "options": [
                            "Any score change of any size should be treated as a confirmed regression",
                            "LLM outputs and LLM judges can both introduce normal variability, so small score fluctuations shouldn't be blindly interpreted as meaningful regressions — sensible thresholds and validation are needed to distinguish real regressions from noise",
                            "LLM-as-a-Judge should never be used for regression testing under any circumstances",
                            "This variability means the underlying AI system is broken and must be rolled back immediately",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly warns about 'flaky' AI tests and judge variability, recommending that small fluctuations not be treated as regressions without sensible thresholds — the goal is distinguishing real regression from normal variability.",
                    },
                    {
                        "question": "V1 responds to unknown information with 'I don't know.' After a prompt change, V2 hallucinates an answer instead — but the average evaluation score barely changes. Why does the lesson call this a serious issue despite the stable average?",
                        "options": [
                            "Because average scores are always meaningless in AI evaluation",
                            "Because regression testing should protect important behavioral properties (like refusing to hallucinate on unknown information), not just aggregate metrics — a property-level regression can happen even when the average score looks stable",
                            "Because hallucination always lowers the average score significantly",
                            "Because this scenario is impossible to detect with any evaluation method",
                        ],
                        "correct": 1,
                        "explanation": "The lesson makes this the point of 'regression testing isn't only about preventing lower scores' — a serious behavioral regression (starting to hallucinate) can occur even when the aggregate score barely shifts, which is why property-based testing matters.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "AI Observability",
            "slug":              "ai-developer-ai-evaluation-observability-ai-observability",
            "description":       "Understand what's actually happening inside a running AI system: logs, metrics, traces, and spans; RAG-specific observability for retrieval and reranking stages; latency percentiles; token/cost tracking; and how observability complements evaluation to move from guess-debugging to systematic root-cause investigation.",
            "order":             13,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "observability", "monitoring", "rag-evaluation", "production"],
            "prerequisite_ids":  [],  # builds on "Regression Testing" (this level, topic 12) and the full RAG evaluation stack (topics 6-11)
            "lesson": {
                "title": "AI Observability",
                "content": """So far, we've focused mainly on evaluation: *"how good is my AI system?"* Now we're moving into **observability**: *"what is actually happening inside my AI system while it is running?"* This distinction is fundamental for production AI engineering.

## 1. What Is AI Observability?

AI observability is the ability to understand the internal behavior and health of an AI system by collecting and analyzing information about its execution.

```
Evaluation
    ↓
How good is the system?

Observability
    ↓
What happened during this request?
Why did it happen?
Where did it fail?
How long did it take?
How much did it cost?
```

For an AI application, observability lets you see beyond User → Answer and understand the entire execution.

## 2. Evaluation vs Observability

**Evaluation** usually happens against a controlled dataset: Evaluation Dataset → AI System → Metrics → Quality. It answers "is the system good?" **Observability** usually focuses on actual system executions: Real User Request → AI System → Trace → Logs + Metrics + Events. It answers "what happened during this request?"

## 2b. Example

A user asks "what are the prerequisites for Machine Learning?" and receives "the prerequisite is Linear Algebra" — wrong. Evaluation tells you Faithfulness ❌, Correctness ❌. But observability helps answer **why**: maybe the query was rewritten to "Machine Learning prerequisites," retrieved three wrong documents, the reranker passed through the wrong context, and the LLM produced a wrong answer from bad context. Now we've identified a likely retrieval failure.

## 3. Observability Is More Than Logging

You might think "I'll just print everything" (`print(question); print(context); print(answer)`). That's useful during development, but production observability is much broader — you want to know what happened, when, how long it took, which component failed, what the model did, what retrieval returned, token usage, and cost. **Logging is one component of observability, not observability itself.**

## 4. The Three Main Pillars

```
             Observability
                  │
       ┌──────────┼──────────┐
       ↓          ↓          ↓
     Logs       Metrics     Traces
```

For AI systems, extend this with AI-specific information: LLM calls, token usage, retrieval results, prompt versions, model versions, tool calls, user feedback, evaluation scores.

## 5. Logs

A log records an event: "2026-09-04 18:30:21 — Request received," "Retriever returned 5 documents," "LLM request completed." Logs answer **"what happened?"**

## 6. Structured Logs

Instead of `print("retrieval took 0.42 seconds")`, produce structured information:

```
log = {
    "event": "retrieval_completed",
    "latency_ms": 420,
    "top_k": 5,
    "query": "machine learning prerequisites"
}
```

Structured logs are much easier to search and analyze — e.g. "find all requests where latency_ms > 1000" or "find all event = retrieval_failed."

## 7. Metrics

A **metric** is a numerical measurement collected over time: requests per minute, error rate, average latency, P95 latency, token usage, cost. E.g. 10,000 requests, 150 errors → error rate 1.5%. Metrics answer **"how is the system behaving overall?"**

## 8. Latency and Percentiles

Latency is how long a request takes. Average alone can hide problems — request 1: 1.2s, request 2: 0.9s, request 3: 4.8s → average 2.3s hides the outlier.

**Percentiles** matter in production: **P50** — half of requests are faster than this (typical request). **P95** — 95% of requests are faster; only the slowest 5% exceed it. **P99** — 99% are faster; only the slowest 1% exceed it. E.g. P50 = 1.2s, P95 = 4.5s, P99 = 10.8s tells you most requests are fast, but some are extremely slow.

## 9. Why Latency Is Special in AI

Traditional APIs might take 10-100ms. AI applications involve embedding → retrieval → reranking → LLM → tool calls → another LLM. Each stage contributes latency:

```
Query embedding     80 ms
Qdrant retrieval    120 ms
Reranking           300 ms
LLM                  1,500 ms
----------------------------
Total                2,000 ms
```

Now you know where time is being spent.

## 10. Traces and Spans

A **trace** represents the execution of a request across multiple components — a timeline:

```
Request
│
├── Query Processing       50ms
│
├── Embedding              80ms
│
├── Qdrant Retrieval      120ms
│
├── Reranking             300ms
│
└── LLM                   1.5s
```

Much more useful than "request took 2 seconds" because you can see where the 2 seconds came from. A **span** represents one operation inside a trace: Trace = entire request; Span = one operation within it (query_rewrite, embedding, retrieval, reranking, LLM).

## 11. RAG Observability

Your existing RAG knowledge becomes extremely useful here. A good observability system can record information about each stage: query rewrite → embedding → vector search → BM25 → RRF → reranker → context → LLM → answer.

## 12. Retrieval Observability

```
retrieval_event = {
    "query": query,
    "top_k": 5,
    "retrieved_doc_ids": ["doc_12", "doc_81", "doc_07"],
    "retrieval_scores": [0.91, 0.87, 0.82]
}
```

When an answer is wrong, you can inspect what documents were actually retrieved.

## 13. Reranker Observability

Suppose the retriever returns `[doc_12, doc_81, doc_07, doc_22, doc_31]` and the reranker produces `doc_81 → 0.94, doc_12 → 0.91, doc_31 → 0.67, doc_07 → 0.42, doc_22 → 0.31`. Observability lets you inspect this and discover, for example, that the correct document was retrieved but ranked too low — very different from "the correct document wasn't retrieved at all." This distinction is crucial for debugging RAG.

## 14. LLM Observability

Useful info per LLM call: model, prompt version, input tokens, output tokens, latency, finish reason, structured output status, error:

```
llm_event = {
    "model": "some-model",
    "prompt_version": "v4",
    "input_tokens": 1820,
    "output_tokens": 240,
    "latency_ms": 1450,
    "status": "success"
}
```

## 15. Token Usage and Cost Observability

LLM APIs often charge based on tokens. One request using 4,000 input + 1,000 output tokens, times 100,000 requests/month, adds up — monitor token usage to see consumption per endpoint and which prompts are unnecessarily large. Similarly, Endpoint A at $0.002/request vs Endpoint B at $0.015/request — investigating B might reveal huge context, large output, and multiple LLM calls. Observability reveals optimization opportunities.

## 16. Error Observability

Instead of just "HTTP 500," you want: which endpoint, which request, which component, which model, which operation, what error, how often:

```
Request ID: abc123
Endpoint: /chat
Stage: reranking
Error: timeout
Latency: 8.2s
```

## 17. Request IDs

Assign every request an ID (e.g. `req_8f72a1`), and every event associated with it carries that ID — retrieval, reranking, LLM, response. You can follow the complete journey of one request.

## 18. User Feedback

Observability shouldn't only capture technical information. 👍/👎, regenerated answer, abandoned conversation, clicked source, reported incorrect answer are all valuable. Technical metrics might show latency good, errors low — but user feedback shows only 62% helpful. Your infrastructure is healthy, but your AI quality may not be.

## 19. AI-Specific Observability

Traditional API observability: latency, errors, throughput. AI Application observability adds: model, prompt version, token usage, cost, retrieval results, retrieval scores, context, tool calls, model output, evaluation scores, user feedback. This is why we call it AI observability.

## 20. Example: Debugging a Bad Answer

User reports "the assistant gave me the wrong answer." Without observability: ❓. With observability: Request ID → Question → Query Rewrite → Retrieved Documents → Reranker Scores → Prompt Version → Model → LLM Response → Final Answer. You can investigate every stage.

## 21. Three Possible Root Causes

**Case A — Retrieval Failure**: correct document not retrieved. **Case B — Context Failure**: correct document retrieved, but irrelevant context dominates (retrieval/reranking/context construction problem). **Case C — Generation Failure**: correct context retrieved, but LLM produces the wrong answer (generation/prompt/model behavior problem). Observability lets you distinguish these.

## 22. Observability + Evaluation

**Evaluation** finds "this answer is wrong." **Observability** helps determine "why was this answer wrong?" Together: Evaluation → detect quality problem → Observability → investigate execution → identify root cause → fix system → Evaluation → verify improvement. One of the most important loops in production AI.

## 23. Example: Your Academic RAG

Faithfulness = 91% tells you there's a quality problem. You inspect traces and discover 80% of failures had correct documents retrieved but the reranker frequently ranked them below irrelevant documents. Now the next engineering task is obvious: investigate the reranker. Without observability, you might randomly change the prompt — inefficient.

## 24. Observability Helps Prevent "Guess Debugging"

Bad AI debugging: answer wrong → change prompt → try again → still wrong → change model → try again → change top_k. That's guessing. Better: answer wrong → inspect trace → did retrieval fail? Yes → fix retrieval. No → inspect generation. That's engineering.

## 25. Observability Doesn't Mean Recording Everything

More data isn't automatically better. Storing huge prompts and documents indefinitely for every request creates high storage costs, privacy risks, security risks, difficult-to-manage data, and huge logs. You need a deliberate observability strategy.

## 26. Sensitive Data

AI applications may process sensitive user information — blindly logging `print(user_message)`, `print(full_context)`, `print(full_model_response)` can be dangerous. Consider redaction, access controls, retention policies, data minimization, encryption, and PII handling. Observability must be designed with security and privacy in mind.

## 27. Sampling

High-traffic systems (e.g. 10 million requests/day) may not need every full trace retained. Strategies: 100% for errors, 100% for critical requests, 100% for evaluation cases, but maybe only 10% for normal requests. The idea: collect enough information to debug and monitor without creating unnecessary cost.

## 28. What Should You Observe?

**Request**: request_id, timestamp, endpoint, user/session identifier. **Retrieval**: query, retriever, top_k, document IDs, scores, latency. **Generation**: model, prompt version, input/output tokens, latency, status. **Result**: answer, evaluation result when available, user feedback. **Infrastructure**: CPU, memory, GPU, errors, throughput.

## 29. A Simple Trace Structure

```
trace = {
    "request_id": "req_123",
    "retrieval": {"latency_ms": 120, "documents": ["doc1", "doc7", "doc9"]},
    "generation": {
        "model": "model-x",
        "prompt_version": "v3",
        "input_tokens": 1800,
        "output_tokens": 220,
        "latency_ms": 1400
    },
    "result": {"status": "success"}
}
```

This is a mental model for what observability captures, not a complete production implementation.

## 30. Observability Dashboard

```
AI SERVICE
─────────────────────────────
Requests/min       1,240
Error Rate          0.8%
P95 Latency         3.2s
Avg Cost            $0.004
─────────────────────────────
RAG
─────────────────────────────
Retrieval Latency   210ms
Reranking Latency   380ms
Retrieval Errors    0.3%
─────────────────────────────
LLM
─────────────────────────────
Input Tokens        2.1M
Output Tokens       340K
LLM Errors          0.5%
─────────────────────────────
```

A high-level view of system health.

## 31. But Dashboards Aren't Enough

A dashboard shows "P95 latency ↑" but you still need to investigate why. Dashboard → P95 latency increased → find slow requests → inspect traces → reranking taking 3 seconds → investigate reranker. That's observability in action.

## 32. The Production Mental Model

```
                    AI SYSTEM
                       │
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
   Retrieval        Generation      Infrastructure
       │               │                │
    Documents        Model          CPU/Memory
    Scores           Tokens         Errors
    Latency          Cost           Throughput
       │               │                │
       └───────────────┼────────────────┘
                       ↓
                    Trace
                       ↓
                 Investigation
```

## 33. Evaluation + Observability + Monitoring

```
              AI SYSTEM
                  │
       ┌──────────┴──────────┐
       ↓                     ↓
   Evaluation          Observability
       ↓                     ↓
How good is it?       What happened?
       │                     │
       └──────────┬──────────┘
                  ↓
            Monitoring
                  ↓
        Is production healthy?
```

These concepts are related but not interchangeable.

## Short Summary

**Evaluation** measures quality — "is the AI system producing good results?" **Observability** shows execution behavior — "what happened inside the system?" **Monitoring** continuously watches system health over time — "is something going wrong in production?" Observability commonly uses logs, metrics, and traces; AI systems add model information, prompt versions, token usage, costs, retrieval results and scores, context, tool calls, user feedback, and evaluation results.

**Key takeaway: Evaluation tells you that something is wrong. Observability helps you understand why. For your RAG systems: bad answer → evaluation detects it → trace inspection → was retrieval wrong? was context irrelevant? did the LLM ignore correct evidence? did a prompt/model change cause it? That is the difference between knowing your AI has a problem and being able to debug the problem.**""",
                "estimated_minutes": 45,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Diagnose a Wrong Answer Using a Trace",
                    "description": """Your production RAG assistant has this trace for request `req_4521`:

Question: "What are the prerequisites for Machine Learning?"

Query Rewrite: "Machine Learning prerequisites" (latency 70ms)

Retrieval: doc_12 → 0.91, doc_44 → 0.88, doc_91 → 0.84, doc_07 → 0.81 (latency 120ms)

Reranking: doc_44 → 0.95, doc_91 → 0.91, doc_12 → 0.42, doc_07 → 0.31 (latency 250ms)

LLM: Model model-X, Prompt v7, Input tokens 2,400, Output tokens 180, latency 1,800ms

Final Answer: "Linear Algebra is required."

You know from your evaluation dataset that the correct answer is "Probability and Statistics," which is contained in doc_12.

Answer:

1. What does observability tell you here that the final answer alone cannot?
2. Was the correct document (doc_12) retrieved?
3. What happened to doc_12 during reranking?
4. Is this primarily a retrieval failure, reranking failure, or generation failure?
5. Which additional information would you want to inspect to confirm your diagnosis?
6. Name three metrics you would put on a production dashboard for this RAG system.""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "observability", "trace-analysis"],
                },
                {
                    "title": "Build a Trace Structure and Latency Percentile Calculator",
                    "description": """Part 1: Write a function `build_trace(request_id, retrieval_docs, retrieval_latency_ms, model, prompt_version, input_tokens, output_tokens, generation_latency_ms, status)` that returns a trace dict matching the structure from the lesson (with `"request_id"`, `"retrieval"`, `"generation"`, and `"result"` keys).

Part 2: Write a function `percentile(latencies, p)` that returns the p-th percentile (0-100) of a list of latency values using simple linear interpolation-free indexing: sort the list, and return the value at index `int(len(sorted_list) * p / 100)` (clamped to the last valid index).

Test `percentile` on `latencies = [800, 900, 1000, 1100, 1200, 4500, 4800, 10800, 1250, 950]` for `p = 50` and `p = 95`, and print both results.""",
                    "starter_code": """def build_trace(request_id, retrieval_docs, retrieval_latency_ms, model,
                 prompt_version, input_tokens, output_tokens,
                 generation_latency_ms, status):
    # TODO: return a trace dict with "request_id", "retrieval", "generation", "result" keys
    pass


def percentile(latencies, p):
    # TODO: sort latencies, return value at index int(len(sorted_list) * p / 100)
    # clamp the index to len(sorted_list) - 1
    pass


trace = build_trace(
    "req_123", ["doc1", "doc7", "doc9"], 120,
    "model-x", "v3", 1800, 220, 1400, "success",
)
print(trace)

latencies = [800, 900, 1000, 1100, 1200, 4500, 4800, 10800, 1250, 950]
print("P50:", percentile(latencies, 50))
print("P95:", percentile(latencies, 95))
""",
                    "solution_code": """def build_trace(request_id, retrieval_docs, retrieval_latency_ms, model,
                 prompt_version, input_tokens, output_tokens,
                 generation_latency_ms, status):
    return {
        "request_id": request_id,
        "retrieval": {
            "latency_ms": retrieval_latency_ms,
            "documents": retrieval_docs,
        },
        "generation": {
            "model": model,
            "prompt_version": prompt_version,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "latency_ms": generation_latency_ms,
        },
        "result": {"status": status},
    }


def percentile(latencies, p):
    sorted_latencies = sorted(latencies)
    index = min(int(len(sorted_latencies) * p / 100), len(sorted_latencies) - 1)
    return sorted_latencies[index]


trace = build_trace(
    "req_123", ["doc1", "doc7", "doc9"], 120,
    "model-x", "v3", 1800, 220, 1400, "success",
)
print(trace)

latencies = [800, 900, 1000, 1100, 1200, 4500, 4800, 10800, 1250, 950]
print("P50:", percentile(latencies, 50))
print("P95:", percentile(latencies, 95))
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "observability", "python"],
                },
            ],
            "quiz": {
                "title": "AI Observability — Knowledge Check",
                "questions": [
                    {
                        "question": "A user receives a wrong answer from a RAG system. Evaluation tells you Faithfulness and Correctness are both ❌. What can observability add that evaluation alone cannot?",
                        "options": [
                            "Nothing — evaluation and observability provide identical information",
                            "Observability can show WHY the answer was wrong by tracing through query rewriting, retrieval, reranking, and generation to pinpoint where the failure occurred",
                            "Observability can only confirm that the answer was wrong, duplicating evaluation",
                            "Observability replaces the need for evaluation entirely",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's core distinction: evaluation detects THAT something is wrong (quality metrics), while observability helps explain WHY by tracing the actual execution path through each pipeline stage.",
                    },
                    {
                        "question": "A dashboard shows average latency of 2.3s, but individual requests are 1.2s, 0.9s, and 4.8s. Why does the lesson recommend using percentiles like P95 instead of relying only on the average?",
                        "options": [
                            "Percentiles are easier to calculate than averages",
                            "The average can hide the fact that a subset of requests (e.g. the slowest 5%) are extremely slow, while percentiles like P95 or P99 explicitly reveal how bad the tail latency is",
                            "Percentiles and averages always produce the same value",
                            "Averages are only used for cost tracking, never for latency",
                        ],
                        "correct": 1,
                        "explanation": "The lesson shows this directly: an average of 2.3s can mask an outlier like 4.8s, while P50/P95/P99 percentiles reveal the distribution — e.g. P50=1.2s but P99=10.8s tells you most requests are fast but some are extremely slow.",
                    },
                    {
                        "question": "A reranker receives 5 retrieved documents including the correct one, but reranks it to position 3 out of 5 with a low score, while irrelevant documents rank higher. Why does the lesson emphasize that this is different from 'the correct document wasn't retrieved at all'?",
                        "options": [
                            "There's no meaningful difference — both cases require the same fix",
                            "These are different failure types: a retrieval failure (never found) requires fixing the retriever, while a reranking failure (found but demoted) requires fixing the reranker — the correct fix depends on distinguishing them",
                            "The reranker can never demote a correct document, so this scenario is impossible",
                            "This distinction only matters for the LLM, not for retrieval-stage debugging",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly calls this distinction 'crucial for debugging RAG' — knowing the document was retrieved but ranked poorly points you toward investigating the reranker, whereas a true retrieval miss points you toward the retriever itself.",
                    },
                    {
                        "question": "Why does the lesson warn against an observability strategy of logging every full prompt, document, and response for every request indefinitely?",
                        "options": [
                            "Because logging is never useful for AI systems",
                            "Because recording everything without a deliberate strategy can create high storage costs, privacy risks, security risks, and unmanageable data volume — observability needs redaction, retention policies, and sometimes sampling",
                            "Because logs can only be stored for a maximum of 24 hours by law",
                            "Because structured logs are always slower to write than plain text logs",
                        ],
                        "correct": 1,
                        "explanation": "The lesson states 'more data isn't automatically better' and lists storage costs, privacy risks, and security risks as reasons to design a deliberate observability strategy rather than logging everything indefinitely.",
                    },
                    {
                        "question": "What is the key difference between 'guess debugging' and the observability-driven debugging approach described in the lesson?",
                        "options": [
                            "Guess debugging is faster and therefore preferred in production",
                            "Guess debugging randomly changes components (prompt, then model, then top_k) hoping something works, while observability-driven debugging inspects the trace first to determine which specific stage failed before making a targeted fix",
                            "There is no difference between the two approaches",
                            "Observability-driven debugging never requires inspecting traces",
                        ],
                        "correct": 1,
                        "explanation": "The lesson contrasts 'bad AI debugging' (change prompt → try again → change model → change top_k, i.e. guessing) with inspecting the trace first to identify whether retrieval failed before deciding what to fix — that's engineering, not guessing.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "Production AI Monitoring",
            "slug":              "ai-developer-ai-evaluation-observability-production-ai-monitoring",
            "description":       "Continuously watch a deployed AI system for quality, cost, and latency degradation: why AI systems drift over time (model, prompt, data, traffic), RAG-specific production signals like no-context rate, alerting, and the loop that turns production failures into permanent evaluation cases.",
            "order":             14,
            "difficulty":        DifficultyLevel.intermediate,
            "estimated_hours":   1.5,
            "skill_tags":        ["ai-developer", "observability", "monitoring", "production", "drift"],
            "prerequisite_ids":  [],  # builds on "Regression Testing" and "AI Observability" (this level, topics 12-13)
            "lesson": {
                "title": "Production AI Monitoring",
                "content": """You've learned: **Evaluation** — how good is the AI system? **Observability** — what happened inside the system? Now we combine them with **production monitoring**. The key question becomes: *"is my AI system continuing to work well after I deploy it?"*

## 1. What Is Production AI Monitoring?

Production AI monitoring means continuously watching an AI system after deployment to detect quality degradation, errors, latency problems, cost increases, retrieval problems, model failures, data changes, and new user failure patterns. The important word is **continuously**. Offline evaluation might tell you "before deployment: Faithfulness = 95%." But what happens three weeks later? Week 1 → 95%, Week 2 → 94%, Week 3 → 89%, Week 4 → 82%. Something changed — production monitoring helps you notice it.

## 2. Why AI Systems Degrade

"If my AI system works today, it will keep working" is a common misconception. AI systems depend on many moving parts: model, prompt, retriever, embeddings, documents, tools, APIs, infrastructure, users, traffic. Any of these can change.

## 3. Model Changes

Your application code (`response = client.generate(...)`) may remain unchanged, but the provider might update or replace the underlying model, and behavior can change: before Faithfulness = 95%, after = 91%. Your code didn't break — the AI behavior changed. Important difference.

## 4. Prompt Changes

You already saw this with regression testing. Prompt V7 works well; a developer deploys Prompt V8 and forgets to run the evaluation suite. Production monitoring might eventually reveal answer relevance ↓ and user complaints ↑. That's why prompt versions should be observable — you want to know which prompt produced this answer.

## 5. Data Changes

Especially important for RAG. Your system indexes "University Regulations 2025," then you add "University Regulations 2026" — users now ask questions involving both, and retrieval behavior may change. New documents may also have different formatting, terminology, structure, OCR errors, or missing metadata. Your RAG system may degrade even though the model hasn't changed.

## 6. New Document Types

Your system was tested with clean PDFs, then production starts receiving scanned PDFs, tables, images, Arabic documents, poor OCR, or long documents. Your previous evaluation may not represent these new inputs — monitoring can reveal a new failure pattern, e.g. Document Q&A accuracy 94% → 76% after many scanned PDFs arrive. Now you have evidence of a data/ingestion problem.

## 7. Traffic Changes

100 requests/day during development becomes 100,000 requests/day after launch. Now you may experience rate limits, queue buildup, increased latency, API failures, higher costs, database load, and GPU memory pressure. Your AI model may be fine while the system around it struggles.

## 8. What Should We Monitor?

```
                 Production Monitoring
                         │
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
    Quality           System            Cost
       │                 │                 │
   Faithfulness       Latency          Token usage
   Relevance          Errors           API cost
   User feedback      Throughput       Requests
```

And for RAG specifically: Retrieval, Context, Generation.

## 9. System Health Metrics

Request volume (requests/minute), error rate (errors/requests), latency (P50/P95/P99), throughput (requests/second). These tell you whether your service is technically healthy.

## 10. AI Quality Metrics

Technical health isn't enough — your API might be 99.99% available while giving terrible answers. Monitor AI-specific quality: Faithfulness, Answer relevance, Correctness, Retrieval recall, Context relevance, Structured-output validity. The challenge is these aren't always available for every production request — we'll discuss why shortly.

## 11. User Feedback Is a Production Signal

👍/👎 tracked over Monday → 91% positive, Tuesday → 90%, Wednesday → 89%, Thursday → 75%. That's a major signal — something changed around Thursday. You can investigate what model, prompt, documents, retrieval configuration, or users/questions changed. This connects user feedback with observability.

## 12. Monitoring RAG Retrieval

Monitor average top-1 score, average top-k score, retrieval latency, no-result rate, number of retrieved documents. Normal Top-1 score = 0.89, suddenly = 0.61 — could indicate query distribution changed, new document types, embedding problem, index problem, or data quality issue. A signal worth investigating.

## 13. "No Good Context" Rate

Especially useful for RAG. Of 10,000 questions, 1,000 have no sufficiently relevant context — that's 10%. If normally you see 2%, something may have changed: indexing failure, missing documents, embedding mismatch, or query distribution shift.

## 14. Monitoring Retrieval Distribution

Normal retrieval scores like `[0.92, 0.90, 0.88, 0.87, 0.85]` shifting to `[0.72, 0.69, 0.65, 0.61, 0.58]` doesn't automatically mean failure, but it's a signal. Observability tells you "something changed." Evaluation can then determine "is the change actually hurting quality?" This distinction is important.

## 15. Production Monitoring Is Not the Same as Offline Evaluation

Offline evaluation: known dataset → controlled environment → measure quality. Production monitoring: real users → real traffic → real inputs → monitor behavior. They complement each other.

## 16. The Monitoring Loop

```
Offline Evaluation
        ↓
Deploy
        ↓
Production Monitoring
        ↓
Detect Anomaly
        ↓
Investigate
        ↓
Create Evaluation Cases
        ↓
Improve System
        ↓
Run Evaluation
        ↓
Deploy
```

This is the complete AI improvement cycle.

## 17. Why Monitoring Alone Isn't Enough

Monitoring shows "answer relevance ↓" — something is getting worse. But you need evaluation to determine how bad it is and which behavior is failing. You might create 50 new evaluation cases from actual production failures, then discover Arabic questions → 72%, English questions → 94%. Now you have a concrete quality problem to fix.

## 18. Production Data Can Improve Your Evaluation Dataset

Original dataset: 100 evaluation cases. After deployment, users encounter new problems — you collect failed questions and add them: Original Dataset + Production Failures → Improved Evaluation Dataset. Now your regression suite becomes more representative of reality.

## 19. Production Failure → Regression Test

A user reports "the assistant incorrectly said that I can register without the prerequisite." Don't just fix the prompt — add the question to your test suite: `{"id": "prod_001", "question": "Can I register without the prerequisite?", "expected_behavior": "The assistant must follow the official registration rules."}` Now future changes must pass this case. One of the most effective ways to improve AI systems.

## 20. Monitoring Cost

50,000 requests/day × 4,000 average tokens/request = 200 million tokens/day. If prompts grow from 4,000 to 6,000 tokens/request, costs can increase significantly. Track input tokens, output tokens, total tokens, cost/request, and total cost.

## 21. Cost Per Successful Request

A more useful metric: how much does it cost to successfully solve a user's problem? System A: $0.01/request, 70% success rate. System B: $0.015/request, 95% success rate. System B costs more per request but might provide better value. **Cost should not be optimized independently of quality.**

## 22. Latency Monitoring

Normal RAG latency P50 = 1.8s, P95 = 3.5s becomes P50 = 2.1s, P95 = 7.8s. You inspect traces and discover Qdrant normal, reranker normal, LLM 5 seconds slower — now you can investigate the LLM/API layer.

## 23. Error Rate Monitoring

Normal error rate 0.5% jumps to 3.8%. Break errors down by endpoint, model, provider, error type, region, time, component. E.g. `/chat → 0.5%, /agent → 1.0%, /document → 8.2%` — now you know where to investigate.

## 24. Alerts

Monitoring becomes much more useful when connected to alerts: `IF error_rate > 5% → Alert`, `IF P95_latency > 5 seconds → Alert`, `IF cost/hour > expected threshold → Alert`, `IF retrieval_no_context_rate > 10% → Alert`. Alerts turn monitoring into an operational system.

## 25. Quality Alerts

Faithfulness baseline = 95%. If sampled production evaluations show Faithfulness = 87%, you might trigger an alert. However, quality metrics often require sampling or asynchronous evaluation because evaluating every request can be expensive.

## 26. Online vs Offline Evaluation

**Offline**: historical/curated dataset → evaluation. **Online**: production request → evaluation/feedback → monitor quality. You can use both — e.g. offline: 500 carefully curated questions; online: 5% of production requests evaluated. Controlled measurement plus real-world monitoring.

## 27. Sampling Production Requests

Evaluating every production response with another LLM may be expensive. 1,000,000 requests/day doesn't require judging all of them — sample 1% for 10,000 evaluations/day, or prioritize errors, low retrieval scores, negative user feedback, long responses, high-cost requests, and critical workflows. This is **targeted sampling.**

## 28. Drift

One of the most important production concepts. **Drift** means the characteristics of the system's inputs or behavior change over time. Before: 80% English, 20% Arabic questions. Later: 50% English, 50% Arabic. If Arabic performance is weaker, overall quality may decline — nothing necessarily "broke," the input distribution changed.

## 29. Query Drift

Before: "course prerequisites," "credit hours," "registration rules." Later: "calculate my GPA," "compare two study plans," "can I graduate this semester?" These may require different retrieval behavior. Monitoring query patterns can reveal this shift.

## 30. Data Drift

2025 regulations become 2026 regulations — old retrieval patterns may no longer be optimal. Monitor document ingestion: number of documents, document versions, failed indexing, missing embeddings, duplicate documents, metadata changes.

## 31. Model Drift / Behavior Drift

Even without retraining, model behavior can change due to provider model updates, model version changes, API changes, or configuration changes. You may notice tool-call success ↓, JSON validity ↓, or faithfulness ↓. Production monitoring can detect these changes.

## 32. Cost Drift

Average cost/request $0.004 becomes $0.009 after a few weeks. Possible causes: larger prompts, more retrieved documents, longer answers, more tool calls, more retries, or a different model. Observability lets you investigate.

## 33. Retry Monitoring

Retries can silently increase cost. 100 requests but 15 require retries means you might effectively make 115+ model/API calls. A sudden increase in retry rate may indicate provider instability, timeouts, rate limits, bad configuration, or network problems.

## 34. Agent Monitoring

For agents, monitor task success rate, tool-call success, number of tool calls, average execution time, failed tool calls, repeated tool calls, unexpected tool usage. Normal average tool calls = 3; after a prompt change, average tool calls = 8. Even if task success remains stable, cost and latency may have exploded — a production problem.

## 35. Multimodal Monitoring

For image → vision model → text extraction → LLM pipelines, monitor image processing failures, unsupported formats, image size, OCR quality, vision model latency, token/image costs, failed uploads. Different AI systems require different observability signals.

## 36. A Production Dashboard

```
╔══════════════════════════════════════════╗
║             AI SERVICE                  ║
╠══════════════════════════════════════════╣
║ Requests/min              1,240         ║
║ Error Rate                 0.8%         ║
║ P95 Latency                3.2 sec      ║
║ Cost / Request             $0.004       ║
╠══════════════════════════════════════════╣
║             RAG                         ║
╠══════════════════════════════════════════╣
║ Retrieval Recall           92%          ║
║ No-context Rate             2.1%        ║
║ Retrieval P95              250 ms       ║
║ Reranker P95               420 ms       ║
╠══════════════════════════════════════════╣
║             QUALITY                     ║
╠══════════════════════════════════════════╣
║ Faithfulness               95%          ║
║ Answer Relevance           92%          ║
║ User Positive Feedback     89%          ║
╚══════════════════════════════════════════╝
```

## 37. Monitoring vs Alerting

**Monitoring** — collecting and analyzing system behavior. **Alerting** — automatically notifying you when something crosses a threshold or pattern. E.g. Monitoring: P95 latency = 7.2s. Alerting: 🚨 P95 latency exceeded 5 sec.

## 38. The AI Incident Workflow

```
Alert
  ↓
Inspect dashboard
  ↓
Identify affected period
  ↓
Inspect traces
  ↓
Identify affected component
  ↓
Create evaluation cases
  ↓
Reproduce problem
  ↓
Fix
  ↓
Run regression suite
  ↓
Deploy
  ↓
Monitor again
```

This is a mature AI engineering workflow.

## 39. The Most Important Connection

```
              OFFLINE
                 │
          Evaluation Dataset
                 ↓
          Evaluate AI System
                 ↓
             Baseline
                 │
                 ↓
              Deploy
                 │
                 ↓
             PRODUCTION
                 │
          ┌──────┴──────┐
          ↓             ↓
    Monitoring      Observability
          ↓             ↓
     Detect issue   Investigate
          │             │
          └──────┬──────┘
                 ↓
        Production Failure
                 ↓
       Add to Evaluation Set
                 ↓
          Fix AI System
                 ↓
        Regression Testing
                 ↓
              Deploy
```

This is the continuous AI engineering loop.

## 40. A Real Example

Two weeks after deployment: P95 latency 3.0s → 4.8s, cost/request $0.004 → $0.006, no-context rate 2% → 7%, negative feedback 8% → 18%. Strong signal something changed. You inspect traces and discover average retrieved chunks went from 5 → 12, because a recent configuration changed top_k from 5 to 12. This caused more context → larger prompts → higher token usage → higher cost → higher LLM latency, and potentially more irrelevant context → worse answer quality. One configuration change caused problems across several dimensions — exactly why production monitoring matters.

## 41. Monitoring Should Lead to Action

Observe → Detect → Understand → Act. E.g. Cost ↑ → inspect token usage → context size ↑ → Top-K changed → revert/optimize. That is useful observability.

## Short Summary

Production AI monitoring continuously tracks the health and behavior of your deployed AI system: **System** (requests, errors, latency, throughput), **AI** (model, prompt version, token usage, cost, output quality), **RAG** (retrieval scores, no-context rate, retrieval latency, reranking behavior, context size), **Agents** (tool calls, task success, tool failures, execution time), **Users** (feedback, regenerations, complaints, abandonment), **Data** (input distribution, document changes, new document types).

**Key takeaway: Offline evaluation tells you whether your system is good before deployment. Production monitoring tells you whether it stays good after deployment. The most powerful loop: Production Failure → Observe → Investigate → Create Evaluation Case → Fix → Regression Test → Deploy → Monitor. This turns real-world failures into permanent improvements.**""",
                "estimated_minutes": 45,
                "has_code_examples": False,
            },
            "exercises": [
                {
                    "title": "Diagnose a Production Degradation Incident",
                    "description": """Your production Arabic RAG system normally has: P95 Latency 3.0 sec, Cost/Request $0.004, No-context Rate 2%, Negative Feedback 8%, Average Retrieved 5 chunks.

After a deployment, you observe: P95 Latency 5.8 sec, Cost/Request $0.007, No-context Rate 6%, Negative Feedback 17%, Average Retrieved 12 chunks.

Answer:

1. Name three things that clearly degraded.
2. What relationship do you see between 5 → 12 chunks and the increased cost/latency?
3. Could retrieving more chunks actually hurt answer quality? Why?
4. What would you inspect first using observability?
5. Would you immediately change the prompt? Why or why not?
6. What evaluation case would you add if users are now complaining about irrelevant answers?
7. After fixing the problem, why should you run the regression suite before redeploying?""",
                    "difficulty": DifficultyLevel.beginner,
                    "skill_tested": ["ai-evaluation", "production-monitoring", "incident-diagnosis"],
                },
                {
                    "title": "Build a Production Alert Evaluator",
                    "description": """Write a function `check_alerts(current_metrics, baseline_metrics, thresholds)` that returns a list of alert strings. `current_metrics` and `baseline_metrics` are dicts with keys `"p95_latency_sec"`, `"cost_per_request"`, `"no_context_rate"`, `"negative_feedback_rate"`. `thresholds` is a dict with the same keys giving the MAXIMUM allowed absolute value for each metric in `current_metrics` (not a delta).

For each metric in `thresholds`, if the current value exceeds the threshold, append an alert string in the format `"ALERT: {metric} is {current_value} (baseline: {baseline_value}, threshold: {threshold_value})"`.

Test it with the numbers from the exercise above (P95 5.8s, cost $0.007, no-context 6%, negative feedback 17%) against thresholds of P95 ≤ 5.0s, cost ≤ $0.006, no-context ≤ 0.05, negative feedback ≤ 0.12, and print all triggered alerts.""",
                    "starter_code": """def check_alerts(current_metrics, baseline_metrics, thresholds):
    # TODO: for each metric in thresholds, compare current_metrics value to the threshold
    # append an alert string if it's exceeded
    pass


current_metrics = {
    "p95_latency_sec": 5.8,
    "cost_per_request": 0.007,
    "no_context_rate": 0.06,
    "negative_feedback_rate": 0.17,
}

baseline_metrics = {
    "p95_latency_sec": 3.0,
    "cost_per_request": 0.004,
    "no_context_rate": 0.02,
    "negative_feedback_rate": 0.08,
}

thresholds = {
    "p95_latency_sec": 5.0,
    "cost_per_request": 0.006,
    "no_context_rate": 0.05,
    "negative_feedback_rate": 0.12,
}

# TODO: call check_alerts and print each alert
""",
                    "solution_code": """def check_alerts(current_metrics, baseline_metrics, thresholds):
    alerts = []
    for metric, max_allowed in thresholds.items():
        current_value = current_metrics.get(metric)
        baseline_value = baseline_metrics.get(metric)
        if current_value is not None and current_value > max_allowed:
            alerts.append(
                f"ALERT: {metric} is {current_value} "
                f"(baseline: {baseline_value}, threshold: {max_allowed})"
            )
    return alerts


current_metrics = {
    "p95_latency_sec": 5.8,
    "cost_per_request": 0.007,
    "no_context_rate": 0.06,
    "negative_feedback_rate": 0.17,
}

baseline_metrics = {
    "p95_latency_sec": 3.0,
    "cost_per_request": 0.004,
    "no_context_rate": 0.02,
    "negative_feedback_rate": 0.08,
}

thresholds = {
    "p95_latency_sec": 5.0,
    "cost_per_request": 0.006,
    "no_context_rate": 0.05,
    "negative_feedback_rate": 0.12,
}

for alert in check_alerts(current_metrics, baseline_metrics, thresholds):
    print(alert)
# Expected: all four alerts trigger, since all current values exceed thresholds
""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "production-monitoring", "python"],
                },
            ],
            "quiz": {
                "title": "Production AI Monitoring — Knowledge Check",
                "questions": [
                    {
                        "question": "An application's code (`response = client.generate(...)`) never changed, but faithfulness dropped from 95% to 91% after the LLM provider updated the underlying model. What does this illustrate?",
                        "options": [
                            "The application must have a bug since the code didn't change",
                            "AI behavior can change even when application code stays the same, because the system depends on external moving parts like the model provider — this is why continuous production monitoring matters, not just pre-deployment testing",
                            "Model providers never update models without notifying developers, so this scenario is unrealistic",
                            "Faithfulness cannot be affected by model changes",
                        ],
                        "correct": 1,
                        "explanation": "The lesson uses this exact example to show that unchanged code doesn't guarantee unchanged behavior — external dependencies like model providers can shift quality without any code change, which is precisely why monitoring must be continuous.",
                    },
                    {
                        "question": "A team notices no-context rate rise from 2% to 10% and top-1 retrieval scores drop from 0.89 to 0.61. According to the lesson, what should happen next?",
                        "options": [
                            "Immediately conclude the model is broken and switch providers",
                            "Treat this as a signal worth investigating — observability shows something changed, but evaluation is needed to determine whether the change is actually hurting quality and why",
                            "Ignore it since retrieval scores naturally fluctuate and are never meaningful",
                            "Immediately change the prompt without investigating retrieval",
                        ],
                        "correct": 1,
                        "explanation": "The lesson distinguishes observability ('something changed') from evaluation ('is the change actually hurting quality?') — a retrieval score drop is a signal to investigate, not an automatic verdict, and the root cause could be several different things (indexing, embeddings, query shift, data quality).",
                    },
                    {
                        "question": "A university RAG system originally sees 80% English / 20% Arabic questions. Over time this shifts to 50% English / 50% Arabic, and overall quality declines because Arabic performance is weaker. What production concept does this describe?",
                        "options": [
                            "A software bug that needs to be patched",
                            "Drift — the characteristics of the system's inputs changed over time, and 'nothing necessarily broke' even though quality declined, because the input distribution shifted",
                            "A regression caused by a recent prompt change",
                            "A retrieval failure caused by missing documents",
                        ],
                        "correct": 1,
                        "explanation": "This is the lesson's explicit definition of drift: the input distribution changes over time, and quality can decline purely because of that shift — 'nothing necessarily broke,' the traffic composition changed.",
                    },
                    {
                        "question": "After investigating a cost and latency spike, a team discovers average retrieved chunks went from 5 to 12 because top_k was recently changed. Why does the lesson highlight this as a good example of production monitoring's value?",
                        "options": [
                            "Because top_k changes never affect cost or latency",
                            "Because one configuration change (top_k) caused a cascade of effects across multiple dimensions — larger prompts, higher token usage, higher cost, higher LLM latency, and potentially worse answer quality from added irrelevant context — all traceable through monitoring and observability together",
                            "Because this proves top_k should always be set to the maximum possible value",
                            "Because this issue could only have been found by manually testing every possible question",
                        ],
                        "correct": 1,
                        "explanation": "The lesson's 'real example' shows exactly this cascade: a single top_k change rippled through cost, latency, and potentially quality — and production monitoring (dashboards + traces) is what let the team trace the symptoms back to the root configuration change.",
                    },
                    {
                        "question": "Why does the lesson recommend 'targeted sampling' (prioritizing errors, low retrieval scores, negative feedback, high-cost requests) rather than evaluating every single production request with an LLM judge?",
                        "options": [
                            "Because targeted sampling always produces more accurate results than full evaluation",
                            "Because evaluating every request (e.g. all of 1,000,000/day) with an LLM judge can be expensive, so sampling — especially prioritizing the requests most likely to reveal problems — gives useful signal at a fraction of the cost",
                            "Because LLM judges cannot process production traffic at all",
                            "Because production requests should never be evaluated, only offline datasets",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly frames this as a cost trade-off: evaluating every request is expensive at scale, so sampling (uniform or targeted toward errors/low-scores/negative-feedback) is a practical way to get useful production quality signal without full-volume judge costs.",
                    },
                ],
                "passing_score": 70,
            },
            "project": None,
        },
        {
            "title":            "AI Evaluation Project",
            "slug":              "ai-developer-ai-evaluation-observability-ai-evaluation-project",
            "description":       "Capstone: design and build a production-style evaluation system for an Arabic academic RAG assistant, combining everything from this level — a representative evaluation dataset, retrieval and generation metrics, failure analysis, regression testing, and an observability-driven evaluation report.",
            "order":             15,
            "difficulty":        DifficultyLevel.advanced,
            "estimated_hours":   3.0,
            "skill_tags":        ["ai-developer", "evaluation", "capstone", "rag-evaluation", "observability"],
            "prerequisite_ids":  [],  # capstone: builds on all Topics 1-14 of this level
            "lesson": {
                "title": "AI Evaluation Project",
                "content": """This is the final lesson of Level 10. Instead of learning another isolated metric, we're going to put the whole evaluation mindset together by designing a production-style evaluation system for an AI application. We'll use a RAG academic assistant because it connects directly to the systems you've already built.

## 1. The Project

We're going to build an evaluation pipeline for **an Arabic university academic assistant using RAG.** The system looks like:

```
User Question
      ↓
Query Processing
      ↓
Retriever
      ↓
Reranker
      ↓
Context
      ↓
LLM
      ↓
Arabic Answer
```

Our evaluation system sits around it:

```
                 Evaluation System
                       │
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
   Retrieval        Generation       Production
       ↓               ↓                ↓
   Recall           Faithfulness     Monitoring
   Precision        Relevance        Feedback
   Context          Correctness      Latency
   Relevance
```

The goal isn't simply "get one score." The goal is: **identify where the AI system succeeds and where it fails.**

## 2. What Are We Trying to Measure?

Consider: "ما هي المتطلبات السابقة لمقرر تعلم الآلة؟" Suppose the correct answer is "مقرر الرياضيات المتقطعة." But our system returns "مقرر الإحصاء والاحتمالات." We need to determine why:

- **Retrieval failure** — the correct document wasn't retrieved.
- **Reranking failure** — the correct document was retrieved but ranked too low.
- **Generation failure** — the correct evidence reached the LLM but the LLM produced the wrong answer.

This is the central idea of the project.

## 3. Step 1 — Build an Evaluation Dataset

We need representative questions. A simple case includes not just `question` and `expected_answer` but also `expected_context`, because we're evaluating retrieval separately from generation:

```
evaluation_dataset = [
    {
        "id": "case_001",
        "question": "ما هي المتطلبات السابقة لمقرر تعلم الآلة؟",
        "expected_answer": "الرياضيات المتقطعة",
        "expected_context": ["course_ml_01"]
    },
    ...
]
```

## 4. Step 2 — Run the AI System

For every test case, run Question → RAG System → Retrieved Documents → Answer, and save the actual result including `retrieved_context` and `answer`. Now we can compare **expected vs actual.**

## 5. Step 3 — Evaluate Retrieval

If expected context `["course_ml_01"]` appears in actual retrieved `["course_12", "course_ml_01", "course_07"]`, retrieval succeeded — even though the final answer might still be wrong. Don't say "the RAG system failed." Instead ask: **which stage failed?**

## 6. Retrieval Recall

Did we retrieve the evidence we needed? Expected `[A]`, retrieved `[A, B, C]` → Recall = 1. Expected `[A]`, retrieved `[B, C, D]` → Recall = 0 — the system never found the required evidence.

## 7. Step 4 — Evaluate Context Relevance

Retrieval recall isn't enough. If A is correct but retrieved is `[A, B, C, D, E, F, G, H, I, J]` — nine documents are irrelevant. That could still cause problems. So we ask: how relevant is the retrieved context to the question?

## 8. Step 5 — Evaluate Faithfulness

If context says "the prerequisite is Discrete Mathematics" but the model answers "the prerequisite is Statistics," that's a faithfulness failure — the answer isn't supported by the retrieved evidence.

## 9. Step 6 — Evaluate Answer Relevance

Question: "ما هي المتطلبات السابقة لمقرر تعلم الآلة؟" Answer: "مقرر تعلم الآلة من مقررات برنامج هندسة الذكاء الاصطناعي." Might be factually true, but doesn't answer the question — Faithfulness potentially okay, Answer relevance ❌. Different dimensions.

## 10. Step 7 — Evaluate Correctness

Compare the answer with the expected answer. Expected "Discrete Mathematics," generated "Discrete Mathematics" → correct. But don't rely exclusively on exact string matching — "الرياضيات المتقطعة هي المتطلب السابق." is semantically equivalent. Use Exact Match, Semantic Similarity, or LLM-as-a-Judge depending on the task.

## 11. Step 8 — Create a Simple Evaluation Function

```
def evaluate_case(case, result):
    return {
        "retrieval": evaluate_retrieval(case["expected_context"], result["retrieved_context"]),
        "answer": evaluate_answer(case["expected_answer"], result["answer"])
    }
```

Architecture: Evaluation Case → AI System → Evaluation Functions → Metrics → Report.

## 12. A Simple Retrieval Metric

```
def retrieval_recall(expected, retrieved):
    expected = set(expected)
    retrieved = set(retrieved)
    found = expected.intersection(retrieved)
    return len(found) / len(expected)
```

`expected = ["A", "B"]`, `retrieved = ["A", "C", "D"]` → `retrieval_recall(...) = 0.5`. We found A but missed B — Recall = 50%.

## 13. Why This Metric Is Useful

Answer quality = 80% alone isn't enough. If retrieval recall = 55%, that's a major clue: many questions fail before the LLM even receives the right evidence. Investigate chunking, embeddings, query rewriting, hybrid retrieval, reranking, and metadata filtering — rather than immediately changing the LLM prompt.

## 14. Build an Evaluation Report

```
Evaluation Results
────────────────────────────
Cases:              100
Retrieval Recall:    91%
Context Relevance:   88%
Faithfulness:        94%
Answer Relevance:    92%
Correctness:         90%
```

Much more informative than a single "Overall Score: 91%."

## 15. Failure Analysis

If Retrieval Recall = 91%, Faithfulness = 94%, Answer Relevance = 92%, but Correctness = 78% — don't conclude "the model is bad." Investigate the failed cases individually, then classify them.

## 16. Failure Categories

`retrieval_failure`, `reranking_failure`, `context_failure`, `generation_failure`, `hallucination`, `incomplete_answer`, `ambiguous_question`, `dataset_error`. E.g. `{"case_id": "case_031", "category": "retrieval_failure", "description": "Correct regulation document was not retrieved."}` Now your evaluation becomes a debugging tool.

## 17. The Failure Matrix

```
                     Generation
                  Good       Bad
               ┌─────────┬─────────┐
Retrieval Good │    ✅   │    ❌   │
               │         │ Gen     │
               ├─────────┼─────────┤
Retrieval Bad  │    ❌   │    ❌   │
               │ Retrieval│ Both   │
               └─────────┴─────────┘
```

This helps answer: where should I focus my engineering effort?

## 18. Step 9 — Evaluate Prompt Versions

Run Prompt V1 and Prompt V2 against exactly the same dataset:

```
                 V1       V2
──────────────────────────────
Retrieval        91%      91%
Faithfulness     88%      94%
Relevance        90%      92%
Correctness      86%      91%
```

Now you have evidence: V2 improved generation quality without changing retrieval. A controlled experiment.

## 19. Step 10 — Regression Testing

V2 Correctness = 91%, V3 Correctness = 93% — looks better. But inspecting individual cases: Case A → V2✅→V3✅, Case B → V2✅→V3❌, Case C → V2❌→V3✅, Case D → V2✅→V3❌. Overall score improved, but you introduced regressions. This is why the evaluation dataset should run automatically whenever the AI system changes.

## 20. The Evaluation Pipeline

```
                  Code / Prompt Change
                          ↓
                  Evaluation Dataset
                          ↓
                    Run AI System
                          ↓
                ┌─────────┴─────────┐
                ↓                   ↓
           Retrieval            Generation
                ↓                   ↓
             Metrics             Metrics
                └─────────┬─────────┘
                          ↓
                    Compare Baseline
                          ↓
                   Pass / Fail
                          ↓
                  Deploy if acceptable
```

## 21. Define Quality Gates

```
quality_gate = {
    "retrieval_recall": 0.90,
    "faithfulness": 0.90,
    "answer_relevance": 0.90
}

if (results["retrieval_recall"] >= 0.90
    and results["faithfulness"] >= 0.90
    and results["answer_relevance"] >= 0.90):
    print("PASS")
else:
    print("FAIL")
```

Now AI evaluation becomes part of engineering rather than subjective inspection.

## 22. But Don't Blindly Trust Thresholds

V1 Faithfulness = 90%, V2 = 91% doesn't automatically mean V2 is better. Also inspect: which cases changed? Did critical cases improve? Did any important cases regress? Is the evaluation dataset representative? Is the judge reliable? A single aggregate number can hide important failures.

## 23. Critical Test Cases

Some questions matter more: "what is the course description?" (normal) vs. "can I graduate this semester?", "can I register without this prerequisite?", "what happens if my GPA is below X?" (critical). A failure in a critical question may matter much more than a failure in a trivial one. Categorize cases with a `"priority": "critical"` field.

## 24. Production Failures Become Evaluation Cases

A real user reports "the assistant told me I could register for a course without satisfying the prerequisite." Don't just fix it — add it to your evaluation dataset with `"priority": "critical"`. Now the same failure should never silently return after another prompt/model change.

## 25. Evaluation + Observability

```
                    AI APPLICATION
                          │
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
    Evaluation       Observability       Monitoring
        │                 │                 │
        ↓                 ↓                 ↓
    Quality           Execution          Production
        │                 │                 │
        └─────────────────┼─────────────────┘
                          ↓
                    Failure Analysis
                          ↓
                    System Improvement
```

This is a mature AI engineering approach.

## 26. What a Real Evaluation System Should Produce

Not just one number — produce overall metrics, per-case results (`case_001 → PASS`, `case_003 → FAIL`), failure categories with counts, version comparisons, and production information (negative feedback, P95 latency, cost/request). Much richer understanding of the system.

## 27. A Minimal Project Architecture

```
ai-evaluation/
│
├── dataset/
│   └── evaluation_cases.json
│
├── evaluation/
│   ├── retrieval.py
│   ├── semantic.py
│   ├── faithfulness.py
│   ├── relevance.py
│   └── judge.py
│
├── runner/
│   └── run_evaluation.py
│
├── results/
│   └── evaluation_results.json
│
└── reports/
    └── report.json
```

The important separation: **AI Application ≠ Evaluation System.** Your application produces outputs; your evaluation system judges those outputs.

## 28. Minimal Evaluation Loop

```
for case in evaluation_dataset:
    result = run_rag(case["question"])

    retrieval_score = evaluate_retrieval(case["expected_context"], result["retrieved_context"])
    answer_score = evaluate_answer(case["expected_answer"], result["answer"])

    save_result(case, retrieval_score, answer_score)
```

Then aggregate and compare with the previous version.

## 29. What You Should NOT Do

Weak: run 10 questions → read answers manually → "looks good 👍." Also weak: one metric → overall score → deploy. Stronger: representative dataset → multiple dimensions → per-case results → failure analysis → regression tests → production monitoring.

## 30. The AI Engineer's Mindset

The most important lesson of this entire level isn't a particular metric. It's this: don't ask "does my AI work?" Ask: **how well does it work? For which questions? Under which conditions? Where does it fail? Why does it fail? Did the latest change improve it? Did the change introduce regressions? Does it remain healthy in production?** That's the evaluation mindset.

## 31. Your Complete AI Quality Loop

```
                    BUILD
                      ↓
               AI Application
                      ↓
                  EVALUATE
                      ↓
        ┌─────────────┼─────────────┐
        ↓             ↓             ↓
    Retrieval      Context       Answer
        ↓             ↓             ↓
     Recall        Relevance    Faithfulness
                                  Relevance
                      ↓
                Regression Test
                      ↓
                   DEPLOY
                      ↓
                OBSERVABILITY
                      ↓
                 MONITORING
                      ↓
              Production Failure
                      ↓
                Failure Analysis
                      ↓
              New Evaluation Case
                      ↓
                    FIX
                      ↓
                  EVALUATE
```

This is the complete lifecycle.

## 32. Final Project Challenge

Build an evaluation system for your Arabic academic RAG. Minimum requirements:

**Dataset** — 20-30 evaluation cases with `id`, `question`, `expected_answer`, `expected_context`, `priority`. Include easy, difficult, multi-hop, and ambiguous questions, edge cases, questions likely to cause hallucinations, and questions from different academic topics.

**Retrieval Evaluation** — measure at least Recall and Precision.

**Generation Evaluation** — measure Semantic similarity, Faithfulness, and Answer relevance. Use LLM-as-a-Judge where appropriate, but don't treat it as absolute truth.

**Regression Testing** — Baseline Version → New Version → Same Dataset → Compare Metrics. Detect regressions at the individual-case level, not just aggregate level.

**Observability** — record at least request_id, question, retrieved_documents, retrieval_scores, model, prompt_version, latency, token_usage, answer, evaluation_results.

**Report** — generate a structured evaluation report showing case counts, retrieval and generation metrics, failure breakdown by category, and regression status (PASS/FAIL).

This project pulls together every metric and mental model from this level into one working evaluation system.""",
                "estimated_minutes": 50,
                "has_code_examples": True,
            },
            "exercises": [
                {
                    "title": "Final Reasoning Exercise",
                    "description": """Before implementing the project, answer these questions:

1. Your RAG system has Retrieval Recall = 95%, Faithfulness = 72%, Answer Relevance = 93%. Where would you investigate first, and why?

2. Another version has Retrieval Recall = 88%, Faithfulness = 91%, Answer Relevance = 92%. Which version would you choose if retrieval is critical for your application, and what additional information would you need before deciding?

3. A new prompt improves the overall score (V1 = 88%, V2 = 92%), but five critical questions that previously passed now fail. Should V2 pass the regression gate? Explain.

4. A production user reports an incorrect answer. Describe the complete workflow from "user complaint" through to "new regression test."

5. Why is this statement wrong: "Our AI system has 95% accuracy, therefore it is production-ready."?""",
                    "difficulty": DifficultyLevel.intermediate,
                    "skill_tested": ["ai-evaluation", "capstone-reasoning", "system-design"],
                },
                {
                    "title": "Build the Core Evaluation Runner",
                    "description": """Implement the core evaluation loop for the capstone project. Write:

1. `retrieval_recall(expected, retrieved)` — as defined in the lesson.
2. `answer_correctness(expected_answer, generated_answer)` — returns `1` if `expected_answer.strip().lower()` is a substring of `generated_answer.strip().lower()`, else `0` (a simple stand-in for a real semantic/LLM-judge check).
3. `evaluate_case(case, result)` — returns a dict `{"id": case["id"], "retrieval_recall": ..., "correctness": ...}` using the two functions above.
4. `run_evaluation(dataset, results_by_id)` — takes the evaluation dataset (list of cases) and a dict mapping case id -> result dict (with `"retrieved_context"` and `"answer"`), and returns a list of per-case evaluation dicts plus a summary dict with average `retrieval_recall` and average `correctness` across all cases.

Test with a small dataset of 3 cases and matching mock results, and print the per-case results and the summary.""",
                    "starter_code": """def retrieval_recall(expected, retrieved):
    # TODO: implement as in the lesson
    pass


def answer_correctness(expected_answer, generated_answer):
    # TODO: simple substring check (case-insensitive, stripped)
    pass


def evaluate_case(case, result):
    # TODO: combine retrieval_recall and answer_correctness into one dict
    pass


def run_evaluation(dataset, results_by_id):
    # TODO: evaluate every case, collect per-case results,
    # and compute average retrieval_recall and average correctness
    pass


dataset = [
    {"id": "case_001", "question": "What is the prerequisite for ML?",
     "expected_answer": "Probability and Statistics", "expected_context": ["course_ml_01"]},
    {"id": "case_002", "question": "How many credit hours for ML?",
     "expected_answer": "3", "expected_context": ["course_ml_01"]},
    {"id": "case_003", "question": "What is the tuition cost per credit hour?",
     "expected_answer": "1330 EGP", "expected_context": ["tuition_2026"]},
]

results_by_id = {
    "case_001": {"retrieved_context": ["course_ml_01", "course_reg_02"],
                 "answer": "The prerequisite is Probability and Statistics."},
    "case_002": {"retrieved_context": ["course_reg_02"],
                 "answer": "The course is worth 3 credit hours."},
    "case_003": {"retrieved_context": ["tuition_2026"],
                 "answer": "The credit hour costs 1500 EGP."},
}

# TODO: call run_evaluation and print per-case results and the summary
""",
                    "solution_code": """def retrieval_recall(expected, retrieved):
    expected = set(expected)
    retrieved = set(retrieved)
    found = expected.intersection(retrieved)
    return len(found) / len(expected)


def answer_correctness(expected_answer, generated_answer):
    return int(expected_answer.strip().lower() in generated_answer.strip().lower())


def evaluate_case(case, result):
    return {
        "id": case["id"],
        "retrieval_recall": retrieval_recall(case["expected_context"], result["retrieved_context"]),
        "correctness": answer_correctness(case["expected_answer"], result["answer"]),
    }


def run_evaluation(dataset, results_by_id):
    per_case = []
    for case in dataset:
        result = results_by_id[case["id"]]
        per_case.append(evaluate_case(case, result))

    avg_recall = sum(c["retrieval_recall"] for c in per_case) / len(per_case)
    avg_correctness = sum(c["correctness"] for c in per_case) / len(per_case)

    summary = {
        "cases": len(per_case),
        "avg_retrieval_recall": avg_recall,
        "avg_correctness": avg_correctness,
    }
    return per_case, summary


dataset = [
    {"id": "case_001", "question": "What is the prerequisite for ML?",
     "expected_answer": "Probability and Statistics", "expected_context": ["course_ml_01"]},
    {"id": "case_002", "question": "How many credit hours for ML?",
     "expected_answer": "3", "expected_context": ["course_ml_01"]},
    {"id": "case_003", "question": "What is the tuition cost per credit hour?",
     "expected_answer": "1330 EGP", "expected_context": ["tuition_2026"]},
]

results_by_id = {
    "case_001": {"retrieved_context": ["course_ml_01", "course_reg_02"],
                 "answer": "The prerequisite is Probability and Statistics."},
    "case_002": {"retrieved_context": ["course_reg_02"],
                 "answer": "The course is worth 3 credit hours."},
    "case_003": {"retrieved_context": ["tuition_2026"],
                 "answer": "The credit hour costs 1500 EGP."},
}

per_case, summary = run_evaluation(dataset, results_by_id)
for c in per_case:
    print(c)
print(summary)
# case_001: recall=1.0 (context found), correctness=1 (answer contains expected)
# case_002: recall=0.0 (context missed), correctness=1 (answer contains "3")
# case_003: recall=1.0 (context found), correctness=0 (1500 != 1330 EGP)
""",
                    "difficulty": DifficultyLevel.advanced,
                    "skill_tested": ["ai-evaluation", "capstone-implementation", "python"],
                },
            ],
            "quiz": {
                "title": "AI Evaluation Project — Knowledge Check",
                "questions": [
                    {
                        "question": "A RAG system has Retrieval Recall = 95%, Faithfulness = 72%, Answer Relevance = 93%. Where does this breakdown suggest you investigate first?",
                        "options": [
                            "The retriever, since retrieval metrics are always the first suspect regardless of the numbers",
                            "Generation/faithfulness, since retrieval is already strong (95%) but faithfulness is comparatively weak (72%) — the LLM is likely receiving good evidence but not staying faithful to it",
                            "The evaluation dataset, since a 72% score always indicates a broken dataset",
                            "Nothing needs investigation since answer relevance is high",
                        ],
                        "correct": 1,
                        "explanation": "With strong retrieval (95%) but comparatively weak faithfulness (72%), the evidence is reaching the LLM but the generation stage isn't staying faithful to it — pointing investigation toward prompting/generation rather than retrieval.",
                    },
                    {
                        "question": "A new prompt raises overall score from 88% to 92%, but five previously-passing critical questions now fail. Per the lesson's regression gate philosophy, what should happen?",
                        "options": [
                            "V2 should automatically pass the regression gate since the overall score improved",
                            "V2 should likely NOT pass the regression gate as-is — critical case regressions can matter more than an aggregate score improvement, and the failures should be investigated before deployment",
                            "Critical questions should be removed from the evaluation dataset since they're causing failures",
                            "The regression gate should be disabled since it's blocking an improvement",
                        ],
                        "correct": 1,
                        "explanation": "This directly echoes the lesson's critical test case and regression testing principles: a higher aggregate score does not excuse regressions in critical cases, which is exactly the scenario the regression gate is designed to catch.",
                    },
                    {
                        "question": "Why does the project's evaluation_case structure store `expected_context` alongside `expected_answer`, rather than just the expected answer?",
                        "options": [
                            "Because expected_context is required by Python dictionaries",
                            "Because storing expected_context allows evaluating retrieval separately from generation — determining whether the correct evidence was found is a different question from whether the final answer is correct",
                            "Because expected_answer alone is never useful for evaluation",
                            "Because expected_context replaces the need for expected_answer entirely",
                        ],
                        "correct": 1,
                        "explanation": "The lesson explicitly notes this: 'we don't only store question/expected_answer, we also store expected_context, because we're evaluating retrieval separately from generation' — enabling stage-level diagnosis rather than only final-answer evaluation.",
                    },
                    {
                        "question": "Why is the statement 'our AI system has 95% accuracy, therefore it is production-ready' considered wrong according to this level's overall teaching?",
                        "options": [
                            "Because 95% accuracy is always too low for any production system",
                            "Because a single aggregate accuracy number doesn't reveal which question types fail, whether critical cases are covered, whether the metric itself is reliable, or how the system behaves under production conditions like drift and cost — production-readiness requires multi-dimensional, ongoing evaluation",
                            "Because accuracy can never be measured for AI systems",
                            "Because 95% accuracy always means the evaluation dataset was too easy",
                        ],
                        "correct": 1,
                        "explanation": "This synthesizes the entire level's core lesson: a single aggregate metric hides failure categories, critical-case behavior, judge reliability, and production dynamics (monitoring, drift, regression) — all of which matter for true production-readiness, not just one number.",
                    },
                    {
                        "question": "According to the project's 'what you should NOT do' section, what makes 'run 10 questions → read answers manually → looks good 👍' an unreliable evaluation approach?",
                        "options": [
                            "Because manual reading is always more accurate than automated metrics",
                            "Because a small, non-representative sample judged subjectively can't reveal failure patterns across question types, doesn't produce reproducible metrics, and misses the systematic, multi-dimensional analysis (retrieval, faithfulness, relevance, regression) needed for reliable evaluation",
                            "Because reading only 10 questions is against Python best practices",
                            "Because manual evaluation is illegal for production AI systems",
                        ],
                        "correct": 1,
                        "explanation": "This connects back to Lesson 2's representativeness principle and the level's repeated emphasis on multi-dimensional, per-case, reproducible evaluation over small-sample subjective judgment — the weak approach lacks all of these properties.",
                    },
                ],
                "passing_score": 70,
            },
            "project": {
                "title": "Arabic Academic RAG Evaluation System",
                "description": "Design and build a production-style evaluation pipeline for an Arabic university academic RAG assistant. The project combines every metric and mental model from Level 10 into one working system: a representative evaluation dataset, stage-separated retrieval and generation metrics, failure categorization, prompt-version comparison with regression detection at the individual-case level, basic observability recording, and a structured evaluation report.",
                "difficulty": DifficultyLevel.advanced,
                "tech_stack": ["Python", "FastAPI (optional API wrapper)", "Qdrant or similar vector DB", "sentence-transformers", "an LLM API for generation and optional LLM-as-a-Judge"],
                "objectives": [
                    "Build an evaluation dataset of 20-30 cases with id, question, expected_answer, expected_context, and priority (normal/critical), covering easy, difficult, multi-hop, ambiguous, and edge-case questions across different academic topics",
                    "Implement retrieval evaluation measuring at least Recall and Precision against expected_context",
                    "Implement generation evaluation measuring Semantic Similarity, Faithfulness, and Answer Relevance, using LLM-as-a-Judge where appropriate without treating it as absolute truth",
                    "Build a failure categorization system (retrieval_failure, reranking_failure, generation_failure, hallucination, incomplete_answer, ambiguous_question, dataset_error) applied to failed cases",
                    "Implement regression testing that compares a baseline version against a new version on the same dataset, detecting regressions at the individual-case level (not just the aggregate score)",
                    "Record basic observability data per case: request_id, question, retrieved_documents, retrieval_scores, model, prompt_version, latency, token_usage, answer, and evaluation_results",
                    "Generate a structured evaluation report showing case counts, retrieval and generation metrics, a failure breakdown by category, prompt-version comparison, and overall regression status (PASS/FAIL) against defined quality gates",
                ],
                "rubric": {
                    "dataset_quality": "Evaluation dataset includes at least 20 cases spanning multiple difficulty levels, question types (including Arabic-language and ambiguous/edge cases), and at least 3 cases marked as critical priority",
                    "retrieval_evaluation": "Recall and Precision are correctly computed per case and aggregated, with results distinguishing retrieval success/failure independently of the final answer",
                    "generation_evaluation": "Faithfulness and Answer Relevance are evaluated using claim-level or LLM-judge-based reasoning (not naive exact-string matching alone), with Semantic Similarity used to compare generated vs. expected answers",
                    "failure_analysis": "Failed cases are categorized into distinct failure types with a failure matrix or breakdown by category, not just a single pass/fail count",
                    "regression_testing": "At least two prompt/system versions are compared on the same dataset, with per-case deltas identified (not only the aggregate score change), and critical-case regressions are flagged even when the aggregate score improves",
                    "observability_and_report": "Each evaluation run produces a structured report (JSON or equivalent) with overall metrics, per-case results, failure category counts, and a clear PASS/FAIL regression verdict against defined quality gate thresholds",
                },
                "starter_repo_url": None,
                "estimated_hours": 12.0,
            },
        },
    ],
}
