"""
backend/seeds/track_ai_developer/level_01_foundations.py

Level 1: AI Engineering Foundations
Topic content for the AI Developer track. Combined with the other level
files by seeds/seed_track_ai_developer.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from common import DifficultyLevel, build_topics, stub_topic  # noqa: F401

LEVEL = {
        "title": "Level 1: AI Engineering Foundations",
        "description": "The mental model, vocabulary, and landscape you need before touching any API: LLMs, tokens, context windows, parameters, providers, and how AI applications are actually architected.",
        "order": 1,
        "topics": [
            {
                "title":            "What Does an AI Developer Actually Build?",
                "slug":              "ai-developer-l1-what-does-ai-developer-build",
                "description":       "The core mental model for this whole track: an AI Developer usually builds applications around existing AI models, rather than training models from scratch.",
                "order":             1,
                "difficulty":        DifficultyLevel.beginner,
                "estimated_hours":   1.0,
                "skill_tags":        ["ai-developer", "llm", "career"],
                "prerequisite_ids":  [],
                "lesson": {
                    "title": "What Does an AI Developer Actually Build?",
                    "content": """# What Does an AI Developer Actually Build?

The goal of this track is not to turn you into an AI researcher. The goal is to understand how an **AI Developer** takes existing models and builds useful applications around them.

## The most important question

A common misconception is:

*"AI Developer = person who trains AI models."*

Not necessarily.

An AI Developer usually **builds applications that use AI models** — they rarely train the models themselves.

## 1. Think about a normal application

Imagine you're building a weather application.

```
User
  ↓
Website / Mobile App
  ↓
Backend
  ↓
Weather API
  ↓
Weather Data
```

The developer doesn't build the entire weather-forecasting system. They use an existing service and build an application *around* it.

AI development is often similar.

## 2. An AI application

Imagine you're building an AI customer-support chatbot. The architecture could be:

```
User
  ↓
Chat Interface
  ↓
Backend
  ↓
LLM
  ↓
Response
  ↓
User
```

The **LLM is the AI model**. Your job as an AI Developer is to build everything around it:

- frontend
- backend
- API integration
- prompts
- conversation memory
- database
- document retrieval
- authentication
- tool calling
- monitoring
- deployment

## 3. Real example

Suppose a company wants: *"Build me an AI assistant that answers questions about our company."*

You could build:

```
                    ┌──────────────┐
                    │     User     │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │  Chat UI     │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   Backend    │
                    └──────┬───────┘
                           ↓
              ┌────────────┴────────────┐
              ↓                         ↓
       ┌──────────────┐          ┌──────────────┐
       │ Company Docs │          │     LLM      │
       └──────────────┘          └──────────────┘
              ↓                         ↑
              └──────→ Context ─────────┘
```

You don't necessarily train the LLM yourself. Instead, you **integrate** the model into the application.

## 4. What does an AI Developer build?

**AI Chatbots** — customer support chatbot, university assistant, coding assistant, personal assistant.

**RAG applications** — RAG means *Retrieval-Augmented Generation*. For example: *"Ask questions about this PDF."*

```
PDF
 ↓
Split into chunks
 ↓
Embeddings
 ↓
Vector Database
 ↓
Retrieve relevant information
 ↓
LLM
 ↓
Answer
```

You've already encountered technologies such as Qdrant, LangChain, LlamaIndex, and LangGraph — these are tools used to build this kind of AI application.

**AI agents** — an agent can use tools. For example:

```
User: "What's the weather tomorrow and send me an email?"
             ↓
          AI Agent
          ↙     ↘
     Weather     Email
       Tool       Tool
          ↘     ↙
           Answer
```

The model decides which tools it needs.

**AI-powered search** — for example, *"Find the most relevant products for a customer looking for a laptop for programming."* This combines Search + Database + Embeddings + LLM.

**AI data applications** — for example, *"Analyze this CSV and explain the important trends."*

```
CSV
 ↓
Python
 ↓
Data Analysis
 ↓
LLM
 ↓
Natural-language explanation
```

## 5. AI Developer vs ML Engineer

This distinction matters a lot.

**ML Engineer** usually focuses on:

```
Data → Training → Models → Evaluation → Deployment
```

They train or fine-tune models.

**AI Developer** usually focuses on:

```
Existing Model → Application → Tools → Data → Users
```

For example:

```
GPT → Prompt → RAG → Tools → FastAPI → Frontend → AI Application
```

Of course, the roles can overlap.

## 6. A simple analogy

Think about building a car.

- The AI **model** is like the *engine*.
- The AI **application** is the *whole car*.

```
                AI APPLICATION
┌────────────────────────────────────┐
│                                    │
│  UI                                │
│  Backend                           │
│  Database                          │
│  Authentication                    │
│  RAG                               │
│  Tools                             │
│  APIs                              │
│                                    │
│       ┌──────────────────┐         │
│       │    AI MODEL      │         │
│       │     ENGINE       │         │
│       └──────────────────┘         │
│                                    │
└────────────────────────────────────┘
```

A powerful engine alone doesn't make a useful car. Likewise, **a powerful LLM alone doesn't make a useful AI product** — the engineering around it matters.

## 7. What you'll learn next

Level 1 starts with understanding the model itself:

```
AI Developer → Models → LLMs → Tokens → Context → Parameters → Cloud/Local → Providers → Architecture
```

Then you'll move into actually building AI applications.

## Key idea to remember

> AI Developer = builds applications *using* AI models. Not: "AI Developer = necessarily trains AI models."
""",
                    "estimated_minutes": 20,
                    "has_code_examples": False,
                },
                "exercises": [
                    {
                        "title": "Design the University Assistant",
                        "description": "Imagine you're asked to build an AI assistant for university students. What could the application contain?\n\nThink about the flow:\n\nUser → ? → ? → ? → LLM → Answer\n\nName 3 things that should exist between the user and the LLM, and briefly explain what each one does. Don't worry if you're unsure — reason from the chatbot and RAG examples in the lesson.",
                        "difficulty": DifficultyLevel.beginner,
                        "skill_tested": ["ai-developer", "system-design"],
                    },
                ],
                "quiz": {
                    "title": "What Does an AI Developer Actually Build? — Knowledge Check",
                    "questions": [
                        {
                            "question": "What does an AI Developer most commonly do?",
                            "options": [
                                "Trains large language models from scratch",
                                "Builds applications around existing AI models",
                                "Only writes research papers about model architectures",
                                "Manages GPU clusters for training jobs",
                            ],
                            "correct": 1,
                            "explanation": "An AI Developer usually integrates and builds around existing models (like GPT or Claude) rather than training models from scratch — that's closer to an ML Engineer's focus.",
                        },
                        {
                            "question": "In the car analogy from the lesson, what does the AI model represent?",
                            "options": [
                                "The whole car",
                                "The steering wheel",
                                "The engine",
                                "The driver",
                            ],
                            "correct": 2,
                            "explanation": "The model is the engine — powerful on its own, but it needs the rest of the car (UI, backend, RAG, tools, auth, etc.) to become a useful product.",
                        },
                        {
                            "question": "What does RAG stand for, and what does it enable?",
                            "options": [
                                "Retrieval-Augmented Generation — answering questions using retrieved external context",
                                "Rapid Application Generation — auto-generating full apps from a prompt",
                                "Random Access Grouping — a database indexing technique",
                                "Response Adjustment Gateway — a rate-limiting layer for APIs",
                            ],
                            "correct": 0,
                            "explanation": "RAG (Retrieval-Augmented Generation) retrieves relevant chunks of information (e.g. from a PDF or a vector database) and feeds them to the LLM as context so it can answer grounded questions.",
                        },
                        {
                            "question": "Which best describes the difference between an ML Engineer's focus and an AI Developer's focus?",
                            "options": [
                                "There is no real difference, the titles are interchangeable",
                                "ML Engineer: Data → Training → Models → Evaluation → Deployment. AI Developer: Existing Model → Application → Tools → Data → Users",
                                "ML Engineer only works on frontend code, AI Developer only works on backend code",
                                "AI Developer trains models, ML Engineer builds applications",
                            ],
                            "correct": 1,
                            "explanation": "ML Engineers typically focus on the data-to-model pipeline (training, evaluation, deployment of the model itself), while AI Developers focus on taking an existing model and building the application, tools, and data flow around it for end users. The roles can overlap.",
                        },
                    ],
                    "passing_score": 70,
                },
                "project": {
                    "title": None,
                    "description": None,
                    "difficulty": DifficultyLevel.intermediate,
                    "tech_stack": [],
                    "objectives": [],
                    "rubric": {},
                    "starter_repo_url": None,
                    "estimated_hours": None,
                },
            },
            {
                "title":            "AI Models vs AI Applications",
                "slug":              "ai-developer-l1-ai-models-vs-ai-applications",
                "description":       "The difference between an AI model (the brain) and an AI application (the complete product built around it) — and why an application can use more than one model.",
                "order":             2,
                "difficulty":        DifficultyLevel.beginner,
                "estimated_hours":   1.0,
                "skill_tags":        ["ai-developer", "llm", "system-design"],
                "prerequisite_ids":  [],
                "lesson": {
                    "title": "AI Models vs AI Applications",
                    "content": """# AI Models vs AI Applications

This is one of the most important concepts in AI Engineering. If you understand this lesson, you'll start seeing AI systems differently.

## 1. The simple difference

- **AI Model** = the brain
- **AI Application** = the complete product that uses the brain

```
GPT model
   ↓
AI Application
   ↓
ChatGPT
```

The model is only one part of the application.

## 2. What is an AI Model?

An AI model is a system that has learned patterns from data. For example, an LLM learns patterns in language.

You give it *"Explain Python to me"* and it generates *"Python is a programming language..."*

The model itself is responsible for understanding the input, processing it, and predicting/generating output. Examples include GPT models, Claude models, Gemini models, Llama models, and Mistral models.

```
INPUT
  ↓
┌──────────────┐
│  AI MODEL    │
└──────────────┘
  ↓
OUTPUT
```

That's the basic model.

## 3. What is an AI Application?

An AI application is a software system built around one or more models. Imagine a *"University AI Assistant"*:

```
                 USER
                   ↓
             ┌───────────┐
             │  Web UI   │
             └─────┬─────┘
                   ↓
             ┌───────────┐
             │  FastAPI  │
             └─────┬─────┘
                   ↓
        ┌──────────┴──────────┐
        ↓                     ↓
   Vector DB                LLM
    (Qdrant)              (GPT)
        ↑                     ↓
        └──── Documents ──────┘
                   ↓
                Answer
```

The LLM is only one component.

## 4. ChatGPT is an excellent example

When you use ChatGPT, you're not simply interacting directly with an LLM — there are many systems around the model:

```
You
 ↓
ChatGPT Interface
 ↓
Backend
 ↓
Conversation Management
 ↓
Safety / Policies
 ↓
Tools
 ↓
Model
 ↓
Response
 ↓
Interface
 ↓
You
```

The underlying model is extremely important. But the application surrounding it makes it *useful*.

## 5. Model vs Application

| AI Model | AI Application |
|---|---|
| Brain | Complete system |
| Processes input | Manages entire workflow |
| Generates predictions | Provides user experience |
| Usually doesn't have a UI | Usually has UI |
| Doesn't necessarily have a database | Can use databases |
| Doesn't necessarily have tools | Can use tools |
| Example: LLM | Example: AI chatbot |

## 6. A real-world analogy: the restaurant

**The chef** prepares food — that's similar to the **AI Model**:

```
Input → Model → Output
```

**The restaurant** has tables, waiters, a menu, a kitchen, payment, a reservation system, delivery, and customer service — that's similar to the **AI Application**:

```
User
 ↓
UI
 ↓
Backend
 ↓
Database
 ↓
Tools
 ↓
AI Model
 ↓
Response
```

The chef is important. But the chef isn't the entire restaurant.

## 7. Why this matters for you

As an AI Engineer, you will often *not* train the model yourself. Instead, you'll take an existing model and build useful systems around it:

```
             Existing LLM
                  ↓
          ┌───────┴───────┐
          ↓               ↓
        RAG             Tools
          ↓               ↓
       Qdrant          APIs
          └───────┬───────┘
                  ↓
               Backend
                  ↓
               Frontend
                  ↓
              AI Product
```

This is where tools like FastAPI, Qdrant, LangChain, LangGraph, LlamaIndex, Python, databases, and APIs become useful.

## 8. Can an application use multiple models?

Absolutely. Imagine an AI application for analyzing documents:

```
Document
   ↓
Embedding Model
   ↓
Vector Database
   ↓
Retriever
   ↓
LLM
   ↓
Answer
```

There are actually different AI models doing different jobs — an **Embedding Model** finds relevant information, and an **LLM** generates the answer.

So an AI application isn't necessarily `Application → One Model`. It can be:

```
Application
    ↓
 ┌──┴─────────────┐
 ↓                ↓
Embedding       LLM
Model           Model
```

## 9. Model ≠ Intelligence Product

This is a very important mindset. Suppose someone gives you a powerful LLM. You still need to answer:

- How does the user interact with it?
- What information should it receive?
- Where does company data come from?
- Does it need tools?
- How do we authenticate users?
- How do we store conversations?
- How do we handle errors?
- How do we monitor it?
- How do we deploy it?

*That's AI Engineering.*

## 10. Simple mental model

```
AI MODEL = Brain

AI APPLICATION = Brain + Data + Tools + Backend + UI + Business Logic + Infrastructure

AI ENGINEERING = Building useful systems around AI models
```

## What you should remember

**"What is an AI model?"** → The AI engine/brain that processes information and produces predictions or generated output.

**"What is an AI application?"** → The complete software system that uses AI models to solve a real problem.
""",
                    "estimated_minutes": 20,
                    "has_code_examples": False,
                },
                "exercises": [
                    {
                        "title": "Model or Application Component?",
                        "description": "You're building an AI PDF Question Answering App using: GPT, Qdrant, FastAPI, an Embedding model, a React UI, and a Python backend.\n\nSort each of these six items into one of two groups: (1) AI Model, or (2) Application Component. For each item, explain in one sentence why it belongs in that group.",
                        "difficulty": DifficultyLevel.beginner,
                        "skill_tested": ["ai-developer", "system-design"],
                    },
                ],
                "quiz": {
                    "title": "AI Models vs AI Applications — Knowledge Check",
                    "questions": [
                        {
                            "question": "Which best describes an AI model?",
                            "options": [
                                "A complete software system with a UI, database, and business logic",
                                "The brain that processes input and generates predictions or output",
                                "A tool for storing and retrieving structured data",
                                "A deployment platform for backend services",
                            ],
                            "correct": 1,
                            "explanation": "The model is the 'brain' — it processes input and produces predictions/output. The application is the full system built around it.",
                        },
                        {
                            "question": "In the restaurant analogy, what does the chef represent?",
                            "options": [
                                "The AI Application",
                                "The AI Model",
                                "The database",
                                "The user",
                            ],
                            "correct": 1,
                            "explanation": "The chef (who prepares the food) maps to the AI Model — important, but not the entire restaurant/application, which also includes tables, waiters, payment, and more.",
                        },
                        {
                            "question": "Can a single AI application use more than one AI model?",
                            "options": [
                                "No, an application can only ever call one model",
                                "Yes — for example, an embedding model for retrieval and an LLM for generation",
                                "Only if the models are from the same provider",
                                "Only in RAG systems, never elsewhere",
                            ],
                            "correct": 1,
                            "explanation": "A document Q&A application, for instance, commonly uses an embedding model to find relevant information and a separate LLM to generate the final answer.",
                        },
                        {
                            "question": "According to the lesson, what does 'AI Engineering' mean?",
                            "options": [
                                "Training large language models from scratch",
                                "Building useful systems around AI models",
                                "Writing academic papers on model architecture",
                                "Only building the frontend of AI chat apps",
                            ],
                            "correct": 1,
                            "explanation": "AI Engineering is about building the data, tools, backend, UI, business logic, and infrastructure around an existing model to turn it into a useful product.",
                        },
                    ],
                    "passing_score": 70,
                },
                "project": {
                    "title": None,
                    "description": None,
                    "difficulty": DifficultyLevel.intermediate,
                    "tech_stack": [],
                    "objectives": [],
                    "rubric": {},
                    "starter_repo_url": None,
                    "estimated_hours": None,
                },
            },
            {
                "title":            "LLMs",
                "slug":              "ai-developer-l1-llms",
                "description":       "What a Large Language Model actually is: how it predicts text token by token, why it's not a database, and how an AI Engineer should think about using one inside an application.",
                "order":             3,
                "difficulty":        DifficultyLevel.beginner,
                "estimated_hours":   1.0,
                "skill_tags":        ["ai-developer", "llm"],
                "prerequisite_ids":  [],
                "lesson": {
                    "title": "LLMs",
                    "content": """# LLMs

Now let's understand one of the most important things in modern AI Engineering: **What is an LLM?**

**LLM = Large Language Model.** Examples include models from OpenAI, Anthropic, Google, Meta, and other providers.

Don't worry about the complicated mathematics yet — we'll build the idea step by step.

## 1. What does an LLM do?

At the simplest level: **an LLM takes text as input and generates text as output.**

```
You: "Explain Python in simple words."
        ↓
      LLM
        ↓
"Python is a programming language
that is easy to learn..."
```

## 2. Why is it called a "Language Model"?

Because the model learns patterns in language. Consider:

*"The sky is ..."* → a language model might predict **"blue"**

*"I drink coffee in the ..."* → it might predict **"morning"**

The model becomes very good at predicting what text should come next.

## 3. The surprising part

An LLM doesn't simply store sentences and retrieve them like a database. Instead, during training, it learns patterns and relationships:

```
Python → programming language
Cairo → Egypt
Paris → France
FastAPI → Python web framework
Qdrant → vector database
```

The model learns relationships between concepts. That's why it can generate *new* sentences, not just recite stored ones.

## 4. How does an LLM generate text?

Starting from *"Python is"*, the model predicts what should come next, one piece at a time:

```
"Python is"
     ↓
   predict
     ↓
" a"
     ↓
"programming"
     ↓
"language"
     ↓
"."
```

Eventually: **"Python is a programming language."**

## 5. Is the model just autocomplete?

A useful beginner mental model: *an LLM is extremely advanced autocomplete.* But don't take that too literally.

Modern LLMs can perform: summarization, translation, coding, classification, reasoning, question answering, extraction, planning, and tool use. They can do this because their training gives them very rich representations of language and concepts.

```
Simple autocomplete
        ↓
predict next word
```

vs.

```
Large-scale learned language system
        ↓
understands patterns
        ↓
predicts next tokens
        ↓
can perform many language-based tasks
```

## 6. What does "Large" mean?

"Large" generally refers to: huge training datasets, many model parameters, and substantial computational requirements. We'll cover parameters properly in a later lesson — for now, just remember: **Large = trained at a very large scale.**

## 7. What happens when YOU send a message?

Suppose you send *"Explain FastAPI"*. The process is roughly:

```
Your text
    ↓
Tokens
    ↓
Numbers
    ↓
LLM
    ↓
Predictions
    ↓
Generated tokens
    ↓
Text
    ↓
Your answer
```

This diagram is extremely important — you'll understand each piece during this level.

## 8. Tokens

You might think the model receives *"Explain FastAPI"* exactly as we see it. Not quite — the text is first converted into **tokens**:

```
"Explain FastAPI"
       ↓
["Explain", " Fast", "API"]
```

The exact tokenization depends on the model. Tokens are then converted into numerical representations that the neural network can process. We'll study tokens properly in the next lesson.

## 9. LLMs don't "think" exactly like humans

When an LLM answers *"What is Python?"*, it isn't necessarily thinking like a human sitting at a desk. At a fundamental level, the model performs mathematical computations to determine likely useful continuations based on its learned parameters and the provided context:

```
Input
 ↓
Neural network computation
 ↓
Probability distribution
 ↓
Next token
 ↓
Repeat
```

## 10. Why can LLMs write code?

Because code is also a form of structured language. During training, models encounter huge amounts of Python, JavaScript, Java, C++, SQL, HTML, and more. They learn patterns such as:

```
def add(a, b):
    return a + b
```

So when you ask *"Write a Python function that adds two numbers"*, the model can generate a likely appropriate sequence.

## 11. LLMs can work with different languages

LLMs can process many human languages — English, Arabic, French, Spanish, German, and more — as well as programming languages. That's particularly useful for AI applications that need multilingual support:

```
Arabic question → LLM → Arabic answer
```

or

```
Arabic question → LLM → English answer
```

## 12. LLM vs Traditional Program

**Traditional program** — you explicitly write the rules:

```
IF temperature > 30
    THEN "Hot"
ELSE
    "Not hot"
```

**LLM** — you provide a prompt:

```
Classify this review as positive or negative:
"The product is amazing!"
```

The model generates **"Positive"**. You didn't explicitly program every possible sentence — the model learned language patterns from training.

## 13. LLM ≠ Database

A database is designed to store and retrieve data. An LLM is designed to process and *generate* information based on learned patterns and context.

```
Database → "Give me record #123" → Exact stored information
```

vs.

```
LLM → "Explain this concept simply" → Generated response
```

That's why AI applications often combine them: **Database + LLM = Useful AI Application.** This becomes especially important when we learn RAG later.

## 14. The AI Engineer's perspective

As an AI Engineer, you don't need to think *"How do I build an LLM from scratch?"* Instead, initially think: *"How can I use an LLM effectively inside an application?"*

```
User → FastAPI → Prompt → LLM API → Response → User
```

Later we'll add Database, Vector DB, RAG, Tools, Agents, Memory, Evaluation, and Monitoring — that's where your AI Engineering skills become valuable.

## The most important mental model

```
          HUMAN TEXT
              ↓
            TOKENS
              ↓
        NUMERICAL INPUT
              ↓
             LLM
              ↓
      PREDICT NEXT TOKEN
              ↓
      PREDICT NEXT TOKEN
              ↓
             ...
              ↓
        GENERATED TEXT
```

You don't need to memorize the mathematics yet. Just understand: **an LLM is a large neural network trained on huge amounts of data to model language and generate text token by token.**

## What you should know before moving on

- LLM = Large Language Model
- It processes language and generates language
- It generates output token by token
- It learns patterns from large-scale training
- It can work with human languages and code
- It is not the same thing as a database
- An AI Engineer usually uses existing LLMs inside applications
""",
                    "estimated_minutes": 25,
                    "has_code_examples": False,
                },
                "exercises": [
                    {
                        "title": "Trace the Pipeline",
                        "description": "You send the prompt \"Write a Python function\" to an LLM. Fill in the missing steps in this pipeline and briefly explain what happens at each step:\n\nText → ? → ? → LLM → ? → Text\n\n(Hint: think about what the raw text is converted into before the model can process it, and what the model produces before it becomes readable text again.)",
                        "difficulty": DifficultyLevel.beginner,
                        "skill_tested": ["ai-developer", "llm"],
                    },
                ],
                "quiz": {
                    "title": "LLMs — Knowledge Check",
                    "questions": [
                        {
                            "question": "What does LLM stand for, and what is its core function?",
                            "options": [
                                "Large Language Model — it stores exact sentences and retrieves them on request",
                                "Large Language Model — it takes text as input and generates text as output, predicted token by token",
                                "Linked Learning Machine — it links documents together for search",
                                "Local Language Manager — it manages language settings for an application",
                            ],
                            "correct": 1,
                            "explanation": "LLM = Large Language Model. Its core function is to take text input and generate text output by predicting the next token repeatedly.",
                        },
                        {
                            "question": "Why is an LLM different from a database?",
                            "options": [
                                "An LLM generates information based on learned patterns and context, while a database stores and retrieves exact stored records",
                                "A database can process natural language, but an LLM cannot",
                                "They are functionally identical, just with different names",
                                "An LLM can only output numbers, not text",
                            ],
                            "correct": 0,
                            "explanation": "A database returns exact stored information (e.g. 'record #123'). An LLM generates a response based on learned patterns and the given context — it doesn't retrieve a pre-stored answer.",
                        },
                        {
                            "question": "Before text is fed into the neural network, what does the LLM pipeline convert it into first?",
                            "options": [
                                "Directly into a final answer",
                                "Into tokens, and then numerical representations",
                                "Into a SQL query",
                                "Into an image embedding",
                            ],
                            "correct": 1,
                            "explanation": "Text is first split into tokens (e.g. 'Explain FastAPI' → ['Explain', ' Fast', 'API']), then converted into numerical representations the model can process.",
                        },
                        {
                            "question": "Why can LLMs write code even though they're 'language' models?",
                            "options": [
                                "Code is also a form of structured language, and models are trained on huge amounts of code",
                                "LLMs have a separate built-in code compiler",
                                "They can't actually write code, only describe it",
                                "Code is converted to plain English before the model sees it",
                            ],
                            "correct": 0,
                            "explanation": "Code (Python, JavaScript, SQL, etc.) is structured language. Since models are trained on large amounts of code, they learn its patterns just like they learn natural language patterns.",
                        },
                    ],
                    "passing_score": 70,
                },
                "project": {
                    "title": None,
                    "description": None,
                    "difficulty": DifficultyLevel.intermediate,
                    "tech_stack": [],
                    "objectives": [],
                    "rubric": {},
                    "starter_repo_url": None,
                    "estimated_hours": None,
                },
            },
            {
                "title":            "Tokens",
                "slug":              "ai-developer-l1-tokens",
                "description":       "How raw text is broken into tokens and converted into numbers an LLM can process, why tokens aren't words, and why token usage matters for cost, context, and multilingual apps.",
                "order":             4,
                "difficulty":        DifficultyLevel.beginner,
                "estimated_hours":   1.0,
                "skill_tags":        ["ai-developer", "llm", "tokens"],
                "prerequisite_ids":  [],
                "lesson": {
                    "title": "Tokens",
                    "content": """# Tokens

Tokens are one of the most important concepts to understand when working with LLMs. Don't worry — this is actually pretty simple.

## 1. What is a token?

A token is a small piece of text that an LLM processes. A token can be a whole word, part of a word, punctuation, a space combined with text, or sometimes a character or group of characters.

For example, this sentence: *"I love Python!"* might be broken conceptually into:

```
["I", " love", " Python", "!"]
```

The exact tokens depend on the model's tokenizer.

## 2. Token ≠ Word

This is the most important thing. You might think *"I love Python"* contains 3 tokens: `I`, `love`, `Python`. Not necessarily — a tokenizer might split text differently.

For example, *"unbelievable"* could conceptually become:

```
["un", "believ", "able"]
```

So: **a token is not necessarily a word.**

## 3. Why don't models just use words?

Because there are an enormous number of possible words. Imagine trying to create a vocabulary containing every possible word — now add new words, names, typos, URLs, code, and numbers across different languages. The vocabulary would become enormous.

Instead, tokenizers break text into reusable pieces. For example, *"programming"* could be represented using pieces related to `program` + `ming`. This allows the model to handle words it hasn't seen exactly before.

## 4. Simple analogy: LEGO 🧱

Think of tokens as LEGO pieces. You have a limited collection of pieces (🧱 A, 🧱 B, 🧱 C, 🧱 D) that you can combine to build many things.

Similarly, a tokenizer has a vocabulary of tokens that can be combined to represent huge amounts of text:

```
Tokens
  ↓
Combine
  ↓
Text
```

## 5. Text → Tokens → Numbers

The model doesn't directly understand the string `"Hello"`. The overall process is roughly:

```
"Hello"
   ↓
Tokenizer
   ↓
Token
   ↓
Token ID
   ↓
Neural network
```

For example, conceptually:

```
"Hello world!"
      ↓
["Hello", " world", "!"]
      ↓
[15496, 995, 0]
```

Those numbers are called **token IDs**. The actual IDs depend on the tokenizer/model.

## 6. Why numbers?

Computers perform mathematical operations on numbers, so the model needs text to eventually become numerical data:

```
Human language
      ↓
Tokens
      ↓
Token IDs
      ↓
Numerical representations
      ↓
Neural network
```

You don't normally have to do this manually — the model's tokenizer and API handle it for you.

## 7. What happens when you send a prompt?

Suppose you send *"Explain FastAPI"*. The process is approximately:

```
User
 ↓
"Explain FastAPI"
 ↓
Tokenizer
 ↓
Tokens
 ↓
Token IDs
 ↓
LLM
 ↓
Generated token
 ↓
Generated token
 ↓
Generated token
 ↓
...
 ↓
Final response
```

## 8. Tokens affect API cost 💰

This is extremely important for AI Engineers. Many LLM APIs charge based partly on tokens:

```
Input tokens + Output tokens = Total tokens
```

For example: Input = 1,000 tokens, Output = 500 tokens → Total = 1,500 tokens. The exact pricing depends on the model/provider. So when building an AI application, you care about token usage.

## 9. Tokens affect context windows

Tokens are also directly related to **context windows**. Suppose a model has a context window of 100,000 tokens — that means the model can process up to roughly that amount of tokenized input/context according to the model's limits. We'll study context windows in the next lesson.

```
More text → More tokens → More context usage
```

## 10. Tokens affect performance

Imagine you send an enormous prompt — 100 pages of documents, a long conversation, and huge instructions. That produces a very large number of tokens, which can mean higher cost, more processing, approaching the context limit, and potentially slower responses.

AI Engineers often try to send only the information the model actually needs. This is one reason **RAG** is useful — instead of `Send entire database → LLM`, you can do:

```
User question
     ↓
Retrieve relevant information
     ↓
Send only relevant chunks
     ↓
LLM
```

## 11. Tokens and Arabic

This is especially interesting for multilingual AI. Tokenization can differ significantly between languages — *"Hello, how are you?"* and *"مرحباً، كيف حالك؟"* may produce different numbers of tokens.

This matters when building Arabic AI applications because token usage, costs, context consumption, and model quality can all differ across languages.

## 12. Tokens and code

Tokens aren't just for normal text — code is tokenized too. For example:

```
def add(a, b):
    return a + b
```

is also broken into tokens, conceptually something like `def`, `add`, `(`, `a`, `,`, `b`, `)`, `:`, `return`, `a`, `+`, `b`. The actual tokenizer may combine or split these differently.

## 13. Tokens and punctuation

Punctuation can also be represented by tokens. *"Hello!"* could conceptually be `Hello` + `!`. Don't memorize exact tokenization examples, since different models use different tokenizers.

## 14. Tokenizer

The thing responsible for converting text into tokens is called a **tokenizer**:

```
TEXT → TOKENIZER → TOKENS
```

and in the other direction:

```
TOKENS → TOKENIZER → TEXT
```

So: **tokenizer = translator between text and tokens.**

## 15. A useful Python example

Many AI libraries allow you to inspect tokenization:

```python
text = "Hello, how are you?"
tokens = tokenizer.encode(text)
print(tokens)
# [15496, 11, 703, 527, 499, 30]

text = tokenizer.decode(tokens)
print(text)
# "Hello, how are you?"
```

The exact numbers depend on the tokenizer.

## 16. Token budget

You'll often hear AI engineers talk about a **token budget** — how many tokens can/should we use for a particular request?

```
User question + System instructions + Retrieved documents + Conversation history + Model response = Token usage
```

A good AI application manages this carefully.

## 17. The big picture

```
USER → TEXT → TOKENIZER → TOKENS → LLM → GENERATED TOKENS → TEXT → USER
```

That's the fundamental pipeline.

## Easy mental model

- **Token** = a piece of text that the model processes
- **Tokenizer** = converts text ↔ tokens
- **Token IDs** = numerical identifiers for tokens

```
More text → More tokens → More context usage → Potentially more cost
```

## One more important question

If an LLM has a 100,000-token context window, does that mean it can accept exactly 100,000 words? **No** — because tokens ≠ words. A token can be smaller or larger than a word.

## What you should remember

- **Token** = piece of text
- **Tokenizer** = text ↔ tokens
- **Token ID** = numerical identifier for a token
- **Token usage** = important for cost + context
- **Tokenization** = depends on the model
""",
                    "estimated_minutes": 25,
                    "has_code_examples": True,
                },
                "exercises": [
                    {
                        "title": "Why Subwords, and Why It Matters for Arabic",
                        "description": "Two related questions:\n\n1. Explain in your own words why tokenizers split rare or long words like \"unbelievable\" into subword pieces (e.g. [\"un\", \"believ\", \"able\"]) instead of keeping a single token per word.\n2. The lesson mentions that \"Hello, how are you?\" and its Arabic translation \"مرحباً، كيف حالك؟\" may produce a different number of tokens. If you were building an Arabic-first AI assistant and Arabic text consistently used more tokens per sentence than the English equivalent, name two concrete consequences this would have for your application (think about cost and context window usage).",
                        "difficulty": DifficultyLevel.beginner,
                        "skill_tested": ["ai-developer", "tokens", "multilingual"],
                    },
                ],
                "quiz": {
                    "title": "Tokens — Knowledge Check",
                    "questions": [
                        {
                            "question": "Which statement about tokens is correct?",
                            "options": [
                                "A token always corresponds exactly to one whole word",
                                "A token can be a whole word, part of a word, punctuation, or a character group — not necessarily a full word",
                                "A token is only ever a single character",
                                "Tokens are only used for code, never for natural language",
                            ],
                            "correct": 1,
                            "explanation": "Tokens are flexible pieces of text — sometimes a full word, sometimes a subword piece, punctuation, or a character group. Token ≠ word.",
                        },
                        {
                            "question": "Why do tokenizers break text into reusable subword pieces instead of using one token per whole word?",
                            "options": [
                                "It makes the model output longer responses",
                                "A full-word vocabulary would be enormous and couldn't handle new words, names, typos, or multiple languages well",
                                "Subwords are required for the model to understand punctuation",
                                "It has no real benefit, it's just a historical convention",
                            ],
                            "correct": 1,
                            "explanation": "A whole-word vocabulary would need to cover every possible word, name, typo, and language — reusable subword pieces let the model represent words it hasn't seen exactly before.",
                        },
                        {
                            "question": "What converts text into tokens, and what converts tokens back into text?",
                            "options": [
                                "The vector database, in both directions",
                                "The tokenizer, in both directions",
                                "The context window, in both directions",
                                "The FastAPI backend, in both directions",
                            ],
                            "correct": 1,
                            "explanation": "The tokenizer is the translator between text and tokens — it encodes text into tokens/token IDs, and can decode token IDs back into text.",
                        },
                        {
                            "question": "Why do AI Engineers care about token usage in a production application?",
                            "options": [
                                "Tokens have no practical effect on cost or performance",
                                "Because many LLM APIs charge based on tokens, and more tokens can mean higher cost, more processing, and approaching context limits",
                                "Tokens only matter for training a model, never for using one via API",
                                "Token usage only affects the frontend, not the backend",
                            ],
                            "correct": 1,
                            "explanation": "Token usage directly affects API cost (input + output tokens) and how close a request gets to the model's context window limit — this is why techniques like RAG, which send only relevant chunks, are valuable.",
                        },
                    ],
                    "passing_score": 70,
                },
                "project": {
                    "title": None,
                    "description": None,
                    "difficulty": DifficultyLevel.intermediate,
                    "tech_stack": [],
                    "objectives": [],
                    "rubric": {},
                    "starter_repo_url": None,
                    "estimated_hours": None,
                },
            },
            {
                "title":            "Context Windows",
                "slug":              "ai-developer-l1-context-windows",
                "description":       "What a context window actually is, what counts toward it (system prompt, history, retrieved documents, tool results), why it isn't the same as permanent memory, and how RAG and conversation management help manage it.",
                "order":             5,
                "difficulty":        DifficultyLevel.beginner,
                "estimated_hours":   1.0,
                "skill_tags":        ["ai-developer", "llm", "context-window"],
                "prerequisite_ids":  [],
                "lesson": {
                    "title": "Context Windows",
                    "content": """# Context Windows

This is another very important AI Engineering concept. You already learned: **tokens = pieces of text processed by an LLM.** Now we ask: *how many tokens can an LLM handle at once?* That's where the context window comes in.

## 1. What is a context window?

The context window is the maximum amount of information an LLM can consider in one request/conversation context. Think of it as the model's working desk:

```
┌─────────────────────────────────┐
│         CONTEXT WINDOW          │
│                                 │
│  System instructions            │
│  User messages                  │
│  Conversation history           │
│  Documents                      │
│  Tool results                   │
│                                 │
└─────────────────────────────────┘
                 ↓
                LLM
```

Everything you put into that context consumes tokens.

## 2. Simple analogy 🧠

Imagine you're studying at a desk. Your desk can hold a book, notes, a laptop, a notebook — but your desk has a physical limit. If you keep adding more and more items, eventually there isn't enough space.

An LLM's context window works similarly: **context window = how much information the model can work with at once.**

## 3. Context windows are measured in tokens

Remember: tokens ≠ words. So a model might have a context window such as 8K, 32K, 128K, 200K, or 1M+ tokens. The exact limits depend on the model and provider and can change over time.

For now, don't focus on the specific numbers — focus on the concept:

```
Context Window = Maximum amount of tokenized context the model can handle
```

## 4. What counts toward the context?

This is extremely important for AI Engineers. Suppose you send *"Explain this document"* and your application includes a long document. The context might contain system instructions, the user question, conversation history, retrieved documents, tool results, and other context:

```
┌──────────────────────────────┐
│ Context Window               │
│                              │
│ System prompt      1,000     │
│ User question       100      │
│ Chat history       5,000     │
│ RAG documents     20,000     │
│ Tool results       3,000     │
│                              │
│ Total             29,100     │
└──────────────────────────────┘
```

All of this consumes context.

## 5. Why does this matter?

Imagine your application has 10 million words of company documents. Can you simply send all of them to the LLM? Usually **no** — even if the model has a very large context window, sending huge amounts of unnecessary information is inefficient.

Instead, AI Engineers use techniques like retrieval, chunking, summarization, conversation management, context compression, and filtering. This is one reason RAG is so important.

## 6. RAG solves a big context problem

Imagine you have 10,000 documents, and a user asks *"What is our vacation policy?"* You don't want to send all 10,000 documents. Instead:

```
10,000 Documents
       ↓
   Vector DB
       ↓
User Question
       ↓
   Retrieval
       ↓
Relevant Documents
       ↓
      LLM
       ↓
     Answer
```

Maybe only 5 relevant chunks are sent to the LLM. Much better.

## 7. Context window ≠ memory

This distinction is very important. A context window is what the model can access in the *current* context — it doesn't automatically mean *"the model permanently remembers everything."*

A conversation being in context right now doesn't mean the model permanently stores every detail from it. AI applications implement their own memory using databases, conversation history, vector databases, summaries, and user profiles.

```
Context ≠ Permanent Memory
```

## 8. Chat history consumes context

Suppose you have a long conversation with many exchanges. If your application keeps sending the *entire* conversation every time — message 1, message 2, ... message 100 — the context keeps growing. Eventually you may need to manage the history.

## 9. How do AI applications manage long conversations?

**Technique 1 — Keep recent messages.** Instead of all 100 messages, send only the last 10.

**Technique 2 — Summarize old messages.**

```
100 messages → Summary → Short context
```

**Technique 3 — Store information externally.**

```
Conversation → Database → Retrieve relevant information → LLM
```

## 10. Context window vs output limit

These are related but not exactly the same thing. Imagine a model has a context capacity of 100,000 tokens, and your request contains 90,000 input tokens — you don't necessarily have another full 100,000 tokens available for the response. The available input/output limits depend on the specific model/API:

```
Context capacity
┌──────────────────────────────────┐
│ Input context │ Output response │
└──────────────────────────────────┘
```

## 11. What happens if context is too large?

Depending on the API/model and how your application is implemented, you can encounter errors or need to reduce/truncate the context. For example, if your context is 150,000 tokens but the model limit is 100,000, you have a problem — you can't simply send everything. You need to reduce it:

```
150K
 ↓
Remove irrelevant information
 ↓
Retrieve important sections
 ↓
Summarize
 ↓
50K
 ↓
LLM
```

## 12. This is an AI Engineering problem

This is where AI Engineering becomes more than *"call an LLM API."* A beginner might build `User → LLM → Answer`. An AI Engineer thinks:

```
User
 ↓
Understand request
 ↓
Retrieve relevant information
 ↓
Manage context
 ↓
Construct prompt
 ↓
Call model
 ↓
Validate output
 ↓
Return answer
```

## 13. Example: University Assistant

Imagine your university assistant has a 500-page regulations document, and a student asks *"How many credit hours do I need to graduate?"*

**Bad architecture:** `500 pages → LLM → Answer`

**Better architecture:**

```
Student Question
      ↓
Retriever
      ↓
Relevant section
      ↓
LLM
      ↓
Answer
```

The LLM doesn't need to read the entire document for every question.

## 14. Context window and RAG

```
Large knowledge base
       ↓
     RAG
       ↓
Retrieve relevant information
       ↓
Small useful context
       ↓
     LLM
```

RAG isn't only about "giving the model knowledge" — it's also a powerful way to control what enters the context window.

## 15. Context window and tokens

Connecting the last two lessons:

```
Text → Tokens → Context Window → LLM
```

That's the big picture.

## Easy mental model

Remember the desk analogy: **context window = the model's working desk.** A small desk holds less information at once; a large desk holds more. But even with a huge desk, you shouldn't cover it with irrelevant papers — that's exactly how good AI applications should handle context.

## Worked example

Imagine an LLM can handle **100,000 tokens**. Your application sends:

- System instructions = 5,000
- Chat history = 20,000
- Retrieved documents = 60,000
- User question = 2,000

Total: 5,000 + 20,000 + 60,000 + 2,000 = **87,000 tokens** — you're using 87% of the 100K context capacity. If you keep adding information, you may run into the model's limits. A smart AI Engineer might reduce the retrieved documents or summarize old conversation history.

## What you should remember

**Context window** = the amount of tokenized context a model can handle for a request/conversation.

```
More text → More tokens → More context usage
```

```
Large knowledge base → Retrieval → Relevant context → LLM
```

Also remember: **context window ≠ permanent memory.**
""",
                    "estimated_minutes": 25,
                    "has_code_examples": False,
                },
                "exercises": [
                    {
                        "title": "Will It Fit? Token Budget Check",
                        "description": "A model has a context window of 128,000 tokens. Your application needs to send:\n\n- System instructions = 3,000 tokens\n- Conversation history = 45,000 tokens\n- Retrieved documents (RAG) = 70,000 tokens\n- User question = 1,500 tokens\n\n1. Calculate the total token usage and the percentage of the 128K context window it consumes.\n2. Is this a safe amount of headroom, or too close to the limit? Justify your answer, keeping in mind the model also needs room to generate a response.\n3. Suggest two concrete changes to the application (referencing techniques from the lesson) that would reduce token usage without losing the information the user actually needs.",
                        "difficulty": DifficultyLevel.beginner,
                        "skill_tested": ["ai-developer", "context-window", "rag"],
                    },
                ],
                "quiz": {
                    "title": "Context Windows — Knowledge Check",
                    "questions": [
                        {
                            "question": "What is a context window?",
                            "options": [
                                "The permanent memory of the model across all conversations",
                                "The maximum amount of tokenized information the model can consider in one request/conversation",
                                "A UI panel that shows the conversation history",
                                "The number of API calls allowed per minute",
                            ],
                            "correct": 1,
                            "explanation": "The context window is the maximum amount of tokenized context (system prompt, messages, documents, tool results, etc.) the model can handle at once — like a working desk with limited space.",
                        },
                        {
                            "question": "Why is 'context window ≠ permanent memory' an important distinction?",
                            "options": [
                                "Because the context window is always larger than any memory system",
                                "Because information in the current context isn't automatically remembered by the model in future conversations — persistence requires the application to implement its own memory (databases, summaries, etc.)",
                                "Because context windows only apply to images, not text",
                                "Because memory and context windows are exactly the same thing, just different names",
                            ],
                            "correct": 1,
                            "explanation": "What's in the context window is only available for the current request/conversation. If you want the model to 'remember' things long-term, the application needs to store and reintroduce that information later — that's not automatic.",
                        },
                        {
                            "question": "How does RAG help with the context window problem?",
                            "options": [
                                "It increases the model's maximum context window size",
                                "It retrieves and sends only the relevant chunks of information instead of the entire knowledge base, keeping context usage small and focused",
                                "It removes the need for a context window entirely",
                                "It compresses the LLM itself to use less memory",
                            ],
                            "correct": 1,
                            "explanation": "RAG retrieves only the relevant documents/chunks for a given question instead of sending an entire knowledge base, which controls what enters the context window and keeps token usage manageable.",
                        },
                        {
                            "question": "A model has a context capacity of 100,000 tokens and your request already uses 90,000 input tokens. What does this imply?",
                            "options": [
                                "You still have a full separate 100,000 tokens available for the output response",
                                "The remaining space available for the model's output response is limited, since input and output share the same overall capacity",
                                "The model will automatically expand its context window to fit the response",
                                "Output tokens never count against the context window",
                            ],
                            "correct": 1,
                            "explanation": "Context capacity is shared between input and output (the exact split depends on the model/API) — a large input leaves less room for the response, so AI Engineers need to understand these limits.",
                        },
                    ],
                    "passing_score": 70,
                },
                "project": {
                    "title": None,
                    "description": None,
                    "difficulty": DifficultyLevel.intermediate,
                    "tech_stack": [],
                    "objectives": [],
                    "rubric": {},
                    "starter_repo_url": None,
                    "estimated_hours": None,
                },
            },
            {
                "title":            "Parameters",
                "slug":              "ai-developer-l1-parameters",
                "description":       "What model parameters actually are (learned numerical values, not stored facts), what '7B' means, parameters vs hyperparameters, and why AI Engineers care about parameter count when choosing a model.",
                "order":             6,
                "difficulty":        DifficultyLevel.beginner,
                "estimated_hours":   1.0,
                "skill_tags":        ["ai-developer", "llm", "parameters"],
                "prerequisite_ids":  [],
                "lesson": {
                    "title": "Parameters",
                    "content": """# Parameters

Now we're going to understand one of the words you'll hear constantly in AI: *"This is a 7B model."* / *"This model has 70B parameters."* What does that actually mean? Let's make it simple.

## 1. What is a parameter?

A parameter is a numerical value inside a neural network that is learned during training. You can think of parameters as the model's learned internal settings.

```
Training Data
     ↓
   Training
     ↓
┌──────────────────┐
│  Model Parameters │
│  0.32             │
│ -1.17             │
│  0.004            │
│  2.51             │
│  ...              │
└──────────────────┘
```

A modern LLM can have billions of these values.

## 2. Simple analogy: millions of knobs 🎛️

Imagine a giant machine with billions of tiny knobs. During training, the model adjusts these knobs so it gets better at its task:

```
Training
   ↓
Adjust billions of parameters
   ↓
Trained model
```

Those learned values are the model's parameters.

## 3. Why does a model need parameters?

Because parameters allow the neural network to represent patterns. During training the model encounters huge amounts of information and learns relationships such as `Python → programming`, `Cairo → Egypt`, `cat → animal`, `FastAPI → web framework`. These aren't stored as simple dictionary entries — the model learns complex statistical relationships through its parameters.

## 4. What does "7B" mean?

If someone says **"7B model"**, it usually means approximately **7 billion parameters**:

```
1B = 1 billion
7B = 7 billion
13B = 13 billion
70B = 70 billion
```

So: `7B model ≈ 7,000,000,000 parameters`.

## 5. Does more parameters always mean better?

**No.** This is an important misconception. You might think `70B > 7B, therefore 70B is always better` — not necessarily.

Model quality depends on many things: training data, training method, architecture, parameter count, fine-tuning, reasoning capabilities, inference techniques, context handling, task, and quantization. A smaller modern model can outperform a larger older model on some tasks.

**Parameter count is useful information, but it is not a complete measure of model quality.**

## 6. More parameters usually means more resources

Larger models generally require more computational resources — a 7B model is smaller and easier to run than a 70B model, which needs much more memory and compute. This matters when deciding *"should I run this model locally or use an API?"* — the topic of the next lesson.

## 7. Parameters take memory

Suppose a model has 7 billion parameters. Each parameter needs memory to store its numerical value, and the amount of memory depends on numerical precision. Very roughly:

```
FP32 → 4 bytes / parameter
FP16 → 2 bytes / parameter
INT8 → 1 byte / parameter
```

So a 7B model at FP16 requires roughly `7 billion × 2 bytes ≈ 14 GB` just for the parameter weights. Real inference can require additional memory for things like activations, the KV cache, and runtime overhead — so actual GPU RAM requirements can be higher.

## 8. Why quantization is useful

Instead of storing parameters at higher precision, you can sometimes represent them using fewer bits — e.g. `FP16 → INT8 → INT4`. This can dramatically reduce memory usage:

```
Large model
     ↓
Quantization
     ↓
Smaller memory footprint
     ↓
Easier local inference
```

There can be quality trade-offs, but quantization is extremely useful for running models locally.

## 9. Parameters vs Hyperparameters

Don't confuse these two.

**Parameters** — learned by the model during training (weights, biases). You normally don't manually choose their final values.

**Hyperparameters** — settings chosen by humans during training or inference: learning rate, batch size, number of training epochs, temperature, max output tokens.

```
Parameters = learned
Hyperparameters = configured
```

## 10. What about temperature?

You may have already seen `temperature=0.7`. This is **not** a model parameter in the usual sense — it's an inference setting that influences how the model samples/generates output:

```
temperature = lower → more predictable output
temperature = higher → more variation/randomness
```

We'll study model parameters/settings more when we start using APIs.

## 11. Parameters are not "stored knowledge"

Don't think *"the model has 7 billion parameters, therefore it has 7 billion facts."* That's incorrect. Parameters are numerical values used throughout the neural network. Knowledge and capabilities *emerge* from the patterns encoded across many parameters — think of parameters as the model's learned configuration rather than a simple database of facts.

## 12. Parameters and training

The simplified training process:

```
Training Data
      ↓
   Model
      ↓
Prediction
      ↓
Compare with target
      ↓
Calculate error
      ↓
Adjust parameters
      ↓
Repeat, repeat, repeat...
```

After enormous amounts of training: billions of learned parameters → trained LLM.

## 13. Parameters and inference

Once training is finished, you normally don't change the model's parameters every time you ask a question:

```
Trained Parameters
       ↓
      LLM
       ↓
User Prompt
       ↓
Response
```

The model uses the learned parameters to generate the answer.

## 14. Training vs Inference

**Training** — the model learns: `Data → Adjust parameters → Model learns`

**Inference** — the trained model generates an answer: `Prompt → Trained model → Answer`

As an AI Engineer, you'll spend a lot of time dealing with inference:

```
User → Your application → LLM inference → Answer
```

## 15. A simple analogy

Imagine you're teaching someone mathematics. **Training** is giving them 100,000 exercises — they learn patterns, and their internal knowledge changes (like adjusting parameters). **Inference** is later asking *"What is 15 × 8?"* — they use what they learned to answer. You aren't retraining them from scratch for every question.

## 16. Why AI Engineers care about parameter count

Because it affects practical decisions. Suppose you're choosing between Model A (3B), Model B (8B), and Model C (70B). You need to think about: **quality** (which performs best for the task), **cost** (which is affordable), **hardware** (can your GPU handle it), **latency** (how fast it responds), and **deployment** (can you run it locally). Model selection is an engineering decision.

## 17. The big picture so far

```
LLM
 ↓
contains billions of learned parameters
 ↓
parameters encode learned patterns
 ↓
model receives tokens
 ↓
model generates tokens
```

Putting everything together:

```
USER
 ↓
TEXT
 ↓
TOKENS
 ↓
CONTEXT WINDOW
 ↓
LLM
 │
 ├── Parameters
 │
 └── Learned patterns
 ↓
GENERATED TOKENS
 ↓
TEXT
 ↓
USER
```

That's the foundation.

## What you should remember

- **Parameter** = learned numerical value inside a neural network
- **7B** = approximately 7 billion parameters
- **More parameters ≠ automatically better model**
- **More parameters → generally more compute/memory requirements**
- **Training** = learn parameters. **Inference** = use learned parameters to generate output.
""",
                    "estimated_minutes": 25,
                    "has_code_examples": False,
                },
                "exercises": [
                    {
                        "title": "Choosing a Model by Parameter Count Alone?",
                        "description": "A teammate says: \"Let's just always pick the model with the most parameters — 70B will always beat 8B.\"\n\n1. Explain why this reasoning is flawed, using at least two factors from the lesson besides parameter count that affect model quality.\n2. A 7B model at FP16 precision needs roughly 14 GB of memory just for its weights. If you quantize that same model to INT8, roughly how much memory would the weights need instead? Show the reasoning, not just the number.\n3. Give one concrete scenario where a smaller model (e.g. 8B) would be the better engineering choice over a larger one (e.g. 70B), even if the 70B model scores slightly higher on a benchmark.",
                        "difficulty": DifficultyLevel.beginner,
                        "skill_tested": ["ai-developer", "parameters", "model-selection"],
                    },
                ],
                "quiz": {
                    "title": "Parameters — Knowledge Check",
                    "questions": [
                        {
                            "question": "What is a model parameter?",
                            "options": [
                                "A setting chosen by a human, such as temperature",
                                "A numerical value inside a neural network that is learned during training",
                                "A single word stored in the model's vocabulary",
                                "A configuration file used to deploy the model",
                            ],
                            "correct": 1,
                            "explanation": "Parameters (weights and biases) are learned automatically during training — they are the model's internal, learned settings, not something a human manually configures.",
                        },
                        {
                            "question": "What does '13B' most commonly refer to?",
                            "options": [
                                "13 billion training examples",
                                "13 billion tokens processed per second",
                                "Approximately 13 billion parameters",
                                "13 billion users of the model",
                            ],
                            "correct": 2,
                            "explanation": "'13B' is shorthand for approximately 13 billion parameters in the model.",
                        },
                        {
                            "question": "Is it true that a model with more parameters is always better?",
                            "options": [
                                "Yes, parameter count alone determines quality",
                                "No — quality also depends on training data, architecture, fine-tuning, and other factors; a smaller modern model can outperform a larger older one",
                                "Yes, but only for coding tasks",
                                "No, parameter count has no relationship to model capability at all",
                            ],
                            "correct": 1,
                            "explanation": "Parameter count is one useful signal but not a complete measure of quality — training data, architecture, fine-tuning, and other factors matter too.",
                        },
                        {
                            "question": "Which of these is a hyperparameter rather than a learned model parameter?",
                            "options": [
                                "A weight learned during training",
                                "temperature",
                                "A bias value learned during training",
                                "The internal numerical values adjusted through backpropagation",
                            ],
                            "correct": 1,
                            "explanation": "Temperature is an inference setting chosen by a human (a hyperparameter), not one of the model's learned weights/biases.",
                        },
                    ],
                    "passing_score": 70,
                },
                "project": {
                    "title": None,
                    "description": None,
                    "difficulty": DifficultyLevel.intermediate,
                    "tech_stack": [],
                    "objectives": [],
                    "rubric": {},
                    "starter_repo_url": None,
                    "estimated_hours": None,
                },
            },
            {
                "title":            "Cloud vs Local Models",
                "slug":              "ai-developer-l1-cloud-vs-local-models",
                "description":       "The trade-offs between using a cloud-hosted LLM API and running a model on your own hardware: cost, control, privacy, scaling, and why you should start with cloud APIs while learning.",
                "order":             7,
                "difficulty":        DifficultyLevel.beginner,
                "estimated_hours":   1.0,
                "skill_tags":        ["ai-developer", "llm", "deployment"],
                "prerequisite_ids":  [],
                "lesson": {
                    "title": "Cloud vs Local Models",
                    "content": """# Cloud vs Local Models ☁️💻

Now we're getting into a real AI Engineering decision. You have an AI model — the question is: **where should it run?** There are two main choices: **Cloud Model** or **Local Model**. Let's make this very simple.

## 1. Cloud Models ☁️

A cloud model runs on someone else's servers. Your application sends a request to an AI provider:

```
Your App
   ↓
Internet
   ↓
AI Provider
   ↓
GPU Servers
   ↓
LLM
   ↓
Response
   ↓
Your App
```

You don't need to own the GPU.

## 2. Example

Suppose your application wants an LLM to answer *"Explain FastAPI."* Your backend might conceptually do:

```python
response = client.responses.create(
    model="some-model",
    input="Explain FastAPI simply."
)
```

Your application sends the request to the provider, the provider runs the model, and returns the answer. You are using **cloud inference**.

## 3. Local Models 💻

A local model runs on hardware you control:

```
Your Computer
      ↓
GPU / CPU
      ↓
Local LLM
      ↓
Response
```

You might download an open-weight model and run it using tools such as Ollama, llama.cpp, vLLM, or Transformers:

```
Your App
   ↓
Local Model Server
   ↓
GPU
   ↓
LLM
```

## 4. Simple analogy

Imagine you need a car. **Cloud** is like using a taxi — you don't own the car, you pay for using it (`You → Taxi service → Car`). **Local** is like owning your own car (`You → Your car`) — you have more control, but you're responsible for maintenance, fuel, repairs, and parking. AI models work similarly.

## 5. Cloud Model Advantages

✅ **No powerful GPU required** — your laptop can send a prompt to the cloud and get an answer from a powerful GPU, even without a strong GPU of its own.

✅ **Easy to start** — usually: get an API key → install SDK → call model. This is why cloud APIs are excellent when you're learning AI Engineering.

✅ **Access to powerful models** — cloud providers can operate very large models that would be difficult or expensive to run on a normal computer.

✅ **Scaling** — as your application grows from 10 users to 1,000 to 100,000, cloud infrastructure can scale much more easily than a single local machine.

## 6. Cloud Model Disadvantages

❌ **You pay for usage** — more requests + more tokens = higher cost.

❌ **Internet required** — no network connection means no normal API request.

❌ **Less control** — you don't control the provider's entire infrastructure or model internals; you're consuming a service.

## 7. Local Model Advantages

✅ **More control** — you control model files, the inference server, hardware, configuration, and the deployment environment.

✅ **Can work offline** — once everything is downloaded and configured, no external API is necessarily required.

✅ **Privacy** — for some applications, keeping data inside your own infrastructure can be important. Instead of `Company Data → External API`, you could have `Company Data → Your Infrastructure → Local Model`. The actual privacy/security characteristics depend on how the system is deployed and managed.

✅ **No per-token API bill** — if you're running your own hardware, you're not paying a provider's per-token inference fee. But that doesn't mean local inference is free — you still have electricity, hardware, storage, maintenance, and engineering costs.

## 8. Local Model Disadvantages

❌ **Hardware requirements** — large models can require a lot of memory (recall: a 7B model already needs significant memory), and a very large model may require multiple GPUs.

❌ **You manage everything** — with cloud, the provider handles GPUs, infrastructure, model serving, and scaling. With local/self-hosted, *you* handle GPUs, the server, the model, deployment, monitoring, and scaling — much more engineering work.

## 9. Cloud vs Local

| | ☁️ Cloud | 💻 Local |
|---|---|---|
| GPU required by you | Usually no | Usually yes for good performance |
| Setup | Easy | More complicated |
| Cost | Usage-based | Hardware + operating costs |
| Privacy/control | Less control | More control |
| Internet | Usually required | Can work offline |
| Scaling | Easier | Your responsibility |
| Maintenance | Provider handles much of it | You handle it |
| Model choice | Provider-dependent | Open-weight models you can run |

## 10. What should YOU use while learning?

**Start with cloud APIs.** Why? Because you want to learn:

```
Python → API → Prompt → LLM → Response
```

without spending hours dealing with CUDA, VRAM, drivers, quantization, and GPU memory management. Those things are useful later, but they shouldn't distract you from the fundamentals.

## 11. Then learn local models

Once you understand cloud APIs, learn `Cloud → Local → Self-hosted`. For example:

```
Phase 1: OpenAI / Anthropic / Google APIs
Phase 2: Ollama
Phase 3: Transformers / llama.cpp / vLLM
```

This gives you both sides of AI Engineering.

## 12. A very useful architecture

A production application might even support both:

```
                    AI APPLICATION
                           ↓
                    Model Interface
                     ↙           ↘
                    ↓             ↓
                 Cloud          Local
                  Model          Model
                    ↓             ↓
                 Provider       GPU Server
```

Then your application can choose: `Development → Local`, `Production → Cloud`, or `Sensitive data → Local`, `General tasks → Cloud`, depending on requirements.

## 13. Example: University AI Assistant

**Option A — Cloud:** `Student → FastAPI → Qdrant → Cloud LLM → Answer`

**Option B — Local:** `Student → FastAPI → Qdrant → Local LLM → Answer`

Notice: most of the application stays the same. Only the model infrastructure changes. That's a powerful AI Engineering idea.

## 14. Cloud API vs Local Model

**Cloud** — you say: *"Give me access to this model."* The provider handles the difficult infrastructure.

**Local** — you say: *"I'll run the model myself."* Now you need to think about the model, weights, memory, GPU, inference engine, API server, and monitoring.

## 15. One important term: Self-hosting

**Self-hosting** means you operate the model yourself rather than relying entirely on a provider's hosted inference service:

```
Cloud API: Your App → Provider → Model
Self-hosted: Your App → Your Server → Model
```

Your server could be your PC, a company server, a cloud GPU VM, or a private data center. So local and self-hosted are related but not identical — a model running on your rented cloud GPU is still generally self-hosted, even though it isn't physically on your laptop.

## Easy mental model

**Cloud** — someone else runs the GPU for you: `Your App → Internet → Provider → LLM`

**Local** — you run the model on hardware you control: `Your App → Your Hardware → LLM`

**Self-hosted** — you operate the model infrastructure yourself, whether that's your PC or a server.

## What you should remember

- **Cloud** = provider runs the model
- **Local** = model runs on your hardware
- **Self-hosted** = you operate the model infrastructure

Cloud is usually easier. Local/self-hosted gives you more control.
""",
                    "estimated_minutes": 25,
                    "has_code_examples": True,
                },
                "exercises": [
                    {
                        "title": "Pick the Right Deployment for the Scenario",
                        "description": "For each scenario below, decide whether a cloud API, a local/self-hosted model, or a hybrid approach is most appropriate, and justify your answer in 1-2 sentences using ideas from the lesson:\n\n1. You're a solo developer learning AI Engineering and building your first chatbot prototype this weekend.\n2. A hospital wants an AI assistant that processes patient records and must keep all data inside its own infrastructure for compliance reasons.\n3. A startup's AI feature just went viral and traffic jumped from 50 to 50,000 daily users overnight.\n4. A company wants to use a powerful model for most tasks, but a specific subset of requests involves confidential internal documents that can never leave company infrastructure.",
                        "difficulty": DifficultyLevel.beginner,
                        "skill_tested": ["ai-developer", "deployment", "system-design"],
                    },
                ],
                "quiz": {
                    "title": "Cloud vs Local Models — Knowledge Check",
                    "questions": [
                        {
                            "question": "What is the main advantage of a cloud model for someone just learning AI Engineering?",
                            "options": [
                                "It's always free to use",
                                "It requires no powerful GPU and is easy to start with (API key, SDK, call model)",
                                "It never requires an internet connection",
                                "It gives you full control over the model's internal weights",
                            ],
                            "correct": 1,
                            "explanation": "Cloud APIs let you get started quickly without needing to own or manage GPU hardware — ideal while you're focused on learning the fundamentals of building with LLMs.",
                        },
                        {
                            "question": "Which is a genuine disadvantage of local/self-hosted models compared to cloud models?",
                            "options": [
                                "You have less control over the infrastructure",
                                "You cannot use open-weight models locally",
                                "You are responsible for hardware, deployment, monitoring, and scaling yourself",
                                "Local models can never work offline",
                            ],
                            "correct": 2,
                            "explanation": "With local/self-hosted models, you take on the engineering work the cloud provider would otherwise handle: GPUs, serving, deployment, monitoring, and scaling.",
                        },
                        {
                            "question": "A company requires that sensitive documents never leave their own infrastructure. Which approach best fits this constraint?",
                            "options": [
                                "A cloud API only, since cloud providers are always compliant",
                                "A self-hosted / local model for the sensitive workload, potentially combined with cloud for general tasks",
                                "There is no way to address this requirement with AI models",
                                "Increasing the model's context window size",
                            ],
                            "correct": 1,
                            "explanation": "Keeping data inside the company's own infrastructure is exactly the scenario where a self-hosted/local model (possibly in a hybrid setup) is appropriate, depending on the company's security and compliance needs.",
                        },
                        {
                            "question": "What does 'self-hosting' mean, according to the lesson?",
                            "options": [
                                "Running a model exclusively on your personal laptop",
                                "Operating the model infrastructure yourself, whether on your PC, a company server, or a rented cloud GPU VM",
                                "Using any cloud provider's hosted API",
                                "A model that hosts its own training data",
                            ],
                            "correct": 1,
                            "explanation": "Self-hosting means you operate the model yourself rather than relying entirely on a provider's hosted inference service — the hardware could be your PC, a company server, or even a rented cloud GPU.",
                        },
                    ],
                    "passing_score": 70,
                },
                "project": {
                    "title": None,
                    "description": None,
                    "difficulty": DifficultyLevel.intermediate,
                    "tech_stack": [],
                    "objectives": [],
                    "rubric": {},
                    "starter_repo_url": None,
                    "estimated_hours": None,
                },
            },
            {
                "title":            "Model Providers",
                "slug":              "ai-developer-l1-model-providers",
                "description":       "What a model provider is, provider vs model vs application, how to actually choose a model for a task using engineering criteria instead of hype, open-weight models, provider lock-in, and model abstraction.",
                "order":             8,
                "difficulty":        DifficultyLevel.beginner,
                "estimated_hours":   1.0,
                "skill_tags":        ["ai-developer", "llm", "model-providers"],
                "prerequisite_ids":  [],
                "lesson": {
                    "title": "Model Providers",
                    "content": """# Model Providers

Now you know what an AI model is, what an LLM is, tokens, context windows, parameters, and cloud vs local models. Now we need to understand: **where do these models come from, and how do I choose one?**

## 1. What is a model provider?

A model provider is a company or organization that develops and/or hosts AI models and gives you access to them:

```
AI Developer
     ↓
Model Provider
     ↓
AI Model
     ↓
Your Application
```

Examples include providers such as OpenAI, Anthropic, Google, Mistral, and Cohere. There are also organizations that release open-weight models, such as Meta and others.

## 2. Provider vs Model

This distinction is very important:

```
Provider: OpenAI      → Model: GPT model
Provider: Anthropic   → Model: Claude model
Organization: Meta    → Model family: Llama
```

So: **provider/organization ≠ model.** A provider can offer multiple models.

## 3. Think about smartphones 📱

Apple is the company; the iPhone (iPhone 16, iPhone 17, ...) is the product. Similarly:

```
AI Company → Model Family → Specific Model
```

For example: `Anthropic → Claude → Specific Claude model`.

## 4. Why are there so many models?

Because different models have different strengths — one might excel at coding, another at reasoning, another at fast classification, another at multilingual tasks, another at cheap high-volume requests, another at running locally. There isn't necessarily one model that's best for everything.

## 5. Choosing a model is an engineering decision

Suppose you're building a **Customer Support AI**. You need to ask:

1. **Quality** — can the model answer correctly?
2. **Cost** — can you afford thousands or millions of requests?
3. **Speed** — how quickly does it respond?
4. **Context** — can it handle your required context?
5. **Capabilities** — does it support structured output, tool calling, vision, multimodal input, streaming?
6. **Availability** — can you access it through an API?
7. **Privacy** — does the deployment satisfy your requirements?

## 6. Example

Imagine three models: **Model A** (cheap, fast, medium quality), **Model B** (expensive, slow, very high quality), **Model C** (local, free per request, requires GPU). There is no universal answer — for 10 million simple classifications, Model A might make sense; for complex reasoning, Model B; for a sensitive internal application, Model C might be appropriate if quality and infrastructure meet requirements.

## 7. API access

One of the easiest ways to use a model is through an API:

```
Your Application
       ↓
      API
       ↓
Model Provider
       ↓
      Model
       ↓
    Response
```

Your Python application doesn't need to know how the provider's entire GPU infrastructure works — it simply sends a request.

## 8. What does the API request contain?

Conceptually:

```python
response = client.responses.create(
    model="model-name",
    input="Explain Python simply."
)
```

You provide the model, input, instructions, and optional parameters. The provider runs the model and returns the result.

## 9. Model providers often provide more than models

A modern AI platform can provide models, embeddings, speech, vision, image generation, moderation, tool calling, streaming, and fine-tuning. So when you choose a provider, you're often choosing an **ecosystem**, not just a model.

## 10. What are open-weight models?

Be careful with the term "open-source LLM" — there are different licensing and access models. An **open-weight model** generally means the model's learned weights are made available for others to download and run, subject to its license:

```
Download model → Your hardware → Run model
```

This is different from `Your App → Provider API → Provider infrastructure`.

## 11. Why would you use an open-weight model?

Because you can potentially have more control:

```
Model weights → Your server → Your application
```

Useful for privacy requirements, offline applications, customization, research, avoiding provider lock-in, and controlling infrastructure. But it also means you take on more responsibility.

## 12. Cloud API vs Open-Weight

| | Hosted API | Open-weight / self-hosted |
|---|---|---|
| Setup | Easy | More work |
| GPU | Provider's | Yours |
| Control | Lower | Higher |
| Infrastructure | Provider manages | You manage |
| Scaling | Easier | Your responsibility |
| Customization | Depends on provider | Often greater |
| Offline | Usually no | Possible |
| Maintenance | Lower | Higher |

## 13. Provider lock-in

Imagine your entire application is built around one provider's API:

```
Your Application → Provider A → Model
```

If you later want to switch to Provider B, you may need to change your code. A good AI Engineer tries to make the application architecture flexible:

```
             Your Application
                    ↓
             Model Interface
              ↙         ↘
             ↓           ↓
        Provider A   Provider B
```

Now changing models becomes easier.

## 14. Model abstraction

Instead of spreading provider-specific code everywhere (`provider_a.generate(...)` repeated all over your codebase), you can create your own interface:

```python
llm.generate(prompt)
```

Then your application can potentially switch implementations:

```
llm
 ↓
 ├── Provider A
 ├── Provider B
 └── Local Model
```

This becomes especially valuable in production.

## 15. How do you choose a provider?

A simple checklist:

- **Step 1 — What task?** Chat? Coding? Classification? RAG? Agents? Vision?
- **Step 2 — What quality?** Basic, good, very high?
- **Step 3 — What latency?** Real-time? Normal? Batch?
- **Step 4 — What budget?** Cheap, medium, expensive?
- **Step 5 — What infrastructure?** Cloud API? Local? Self-hosted?
- **Step 6 — What capabilities?** Tools? Structured output? Vision? Long context? Streaming?

## 16. Don't choose a model just because it's popular

This is a very important professional habit. Don't say *"everyone uses Model X, so I'll use Model X."* Instead, **test the models against your actual task** — create 100 test questions, compare Model A/B/C, and measure accuracy, latency, cost, output quality, and failure rate. That's much more useful than simply looking at benchmark numbers.

## 17. A real AI Engineer workflow

Test Model A → RAG evaluation → Score. Test Model B → RAG evaluation → Score. Test Model C → RAG evaluation → Score. Then:

```
Quality + Cost + Latency + Reliability = Model Decision
```

This is engineering, not guessing.

## 18. One application can use multiple providers

You don't have to use only one:

```
                AI Application
                      ↓
       ┌──────────────┼──────────────┐
       ↓              ↓              ↓
     LLM A          LLM B        Embedding Model
       ↓              ↓              ↓
   Provider A     Provider B    Provider C
```

You might use one model for generation, another for embeddings, another for reranking. This is common in more advanced AI systems.

## 19. The big picture

```
AI Application
      ↓
Model Interface
      ↓
┌───────────────┐
│ Model Provider│
└───────┬───────┘
        ↓
      Model
        ↓
     Output
```

or with a flexible architecture:

```
AI Application
      ↓
Model Interface
   ↙       ↓       ↘
Cloud A  Cloud B   Local
   ↓       ↓         ↓
 Model    Model     Model
```

This is a much more flexible architecture.

## Easy mental model

1. **Provider** — who provides/hosts the model.
2. **Model** — the actual AI system doing the inference.
3. **Application** — your software using the model to solve a problem.

```
Provider → Model → Your Application → User
```

## What you should remember

There is no universally best LLM. **The best model is the model that best fits your application's requirements.**

**Provider ≠ Model ≠ Application**
""",
                    "estimated_minutes": 25,
                    "has_code_examples": True,
                },
                "exercises": [
                    {
                        "title": "Choose a Provider Setup for the Scenario",
                        "description": "You're building an AI chatbot for a company. You receive only about 100 users per day but need extremely high-quality answers. You're evaluating three options:\n\nA: Very powerful but expensive\nB: Cheap and fast\nC: Open-weight model you can self-host\n\n1. Walk through the 6-step provider-choice checklist from the lesson (task, quality, latency, budget, infrastructure, capabilities) and use it to justify which option (A, B, or C) fits this scenario best.\n2. Now suppose the company later wants to reduce provider lock-in risk. Sketch (in words or a simple diagram) how you'd restructure the application so switching providers later doesn't require rewriting your AI logic everywhere.",
                        "difficulty": DifficultyLevel.beginner,
                        "skill_tested": ["ai-developer", "model-providers", "system-design"],
                    },
                ],
                "quiz": {
                    "title": "Model Providers — Knowledge Check",
                    "questions": [
                        {
                            "question": "What is the relationship between a provider and a model?",
                            "options": [
                                "A provider and a model are always the same thing",
                                "A provider is a company/organization that develops and/or hosts models, and can offer multiple different models",
                                "A model always belongs to exactly one application and no provider",
                                "A provider is a type of vector database",
                            ],
                            "correct": 1,
                            "explanation": "Provider ≠ model. A single provider (e.g. Anthropic) can offer multiple models (e.g. different Claude models), similar to how Apple offers multiple iPhone models.",
                        },
                        {
                            "question": "According to the lesson, what is the right way to choose a model for your application?",
                            "options": [
                                "Always pick whichever model is most popular or most talked about",
                                "Always pick the model with the largest parameter count",
                                "Test candidate models against your actual task and measure accuracy, latency, cost, and failure rate",
                                "Pick randomly since all models perform the same",
                            ],
                            "correct": 2,
                            "explanation": "The lesson stresses testing models against your real use case with concrete criteria (quality, cost, latency, capabilities, privacy) rather than choosing based on popularity or benchmark hype alone.",
                        },
                        {
                            "question": "What does 'provider lock-in' refer to, and how can it be mitigated?",
                            "options": [
                                "It refers to a security vulnerability in the model, mitigated by encryption",
                                "It refers to being tightly coupled to one provider's API, mitigated by adding a model interface/abstraction layer",
                                "It refers to a provider refusing new customers, mitigated by using open-weight models only",
                                "It refers to a model's context window limit, mitigated by chunking",
                            ],
                            "correct": 1,
                            "explanation": "Provider lock-in happens when application code is written directly against one provider's API. A model abstraction/interface layer (e.g. a generic llm.generate(prompt)) makes it easier to switch providers later.",
                        },
                        {
                            "question": "What does 'open-weight model' generally mean?",
                            "options": [
                                "A model that can only be accessed through a paid API",
                                "A model whose learned weights are made available to download and run, subject to its license",
                                "A model that has no parameters",
                                "A model that is always free of any usage restrictions",
                            ],
                            "correct": 1,
                            "explanation": "Open-weight generally means the trained weights are downloadable and runnable by others, subject to the specific license — it's distinct from a fully hosted API-only model.",
                        },
                    ],
                    "passing_score": 70,
                },
                "project": {
                    "title": None,
                    "description": None,
                    "difficulty": DifficultyLevel.intermediate,
                    "tech_stack": [],
                    "objectives": [],
                    "rubric": {},
                    "starter_repo_url": None,
                    "estimated_hours": None,
                },
            },
            {
                "title":            "LLM Application Architecture",
                "slug":              "ai-developer-l1-llm-application-architecture",
                "description":       "How all the pieces you've learned so far (frontend, backend, prompt, database, vector database, tools, model provider) fit together into a complete LLM application, using a RAG-based university assistant as a running example.",
                "order":             9,
                "difficulty":        DifficultyLevel.beginner,
                "estimated_hours":   1.5,
                "skill_tags":        ["ai-developer", "llm", "architecture", "rag"],
                "prerequisite_ids":  [],
                "lesson": {
                    "title": "LLM Application Architecture",
                    "content": """# LLM Application Architecture 🏗️

Now we're going to put everything together. You've learned AI models, LLMs, tokens, context windows, parameters, cloud vs local, and model providers. Now the big question is: **how do we turn an LLM into a real application?**

## 1. The simplest LLM application

At the beginning, an AI application can be incredibly simple:

```
User → Your Application → LLM → Response → User
```

For example: `User: "Explain Python."` — your application sends the request to an LLM and returns the answer. That's already an AI application.

## 2. A more realistic application

Real applications usually have more components:

```
                    USER
                      ↓
                 ┌─────────┐
                 │ Frontend│
                 └────┬────┘
                      ↓
                 ┌─────────┐
                 │ Backend │
                 └────┬────┘
                      ↓
               ┌──────────────┐
               │ AI Workflow  │
               └──────┬───────┘
                      ↓
                    LLM
                      ↓
                  Response
                      ↓
                   User
```

Let's understand each piece.

## 3. Frontend 🖥️

The frontend is what the user interacts with — built with React, Next.js, Vue, plain HTML/CSS/JavaScript, or mobile applications. The frontend doesn't necessarily talk directly to the LLM:

```
Frontend → Backend → LLM
```

## 4. Backend ⚙️

The backend handles your application's logic:

```
Frontend → FastAPI → LLM
```

The backend might handle authentication, users, prompts, model calls, databases, RAG, tools, logging, error handling, and rate limiting. This is where your Python/FastAPI knowledge becomes extremely useful.

## 5. The LLM

The LLM is the AI engine. Your backend sends system instructions + user message + relevant context to the model, and the model generates a response:

```
Backend → Prompt → LLM → Generated tokens → Response
```

## 6. Prompt

The prompt tells the model what you want — instructions, user input, context, retrieved documents, tool results. For example:

```
You are a helpful programming tutor.

Explain the following concept in simple language.

User question:
What is FastAPI?
```

## 7. Database 🗄️

Many AI applications need a normal database — for users, conversations, messages, settings, subscriptions. You might use PostgreSQL, MySQL, SQLite, or MongoDB. The database stores application data.

## 8. Vector Database

Now we're getting into RAG. Suppose your AI assistant needs to answer questions from documents:

```
Documents → Chunking → Embeddings → Vector Database
```

Examples include Qdrant, Chroma, FAISS, and Milvus. Then:

```
User Question → Embedding → Vector Search → Relevant Chunks → LLM
```

This allows the application to retrieve useful information before asking the LLM to answer.

## 9. Tools 🔧

An LLM by itself can't necessarily perform every action you want. Your application can give it tools:

```
LLM
 ↓
 ├── Search tool
 ├── Calculator
 ├── Database
 ├── Weather API
 └── Email tool
```

The model can decide it needs a tool, depending on how the application is designed. For example, *"What's 1847 × 392?"* could route through: `LLM → Calculator → Result → LLM → Answer`.

## 10. Complete architecture

Now let's combine everything:

```
                         USER
                           ↓
                    ┌────────────┐
                    │  Frontend  │
                    └─────┬──────┘
                          ↓
                    ┌────────────┐
                    │   FastAPI  │
                    │   Backend  │
                    └─────┬──────┘
                          ↓
                  ┌───────────────┐
                  │  AI Workflow  │
                  └───────┬───────┘
                          ↓
              ┌───────────┼───────────┐
              ↓           ↓           ↓
           Database      RAG         Tools
              ↓           ↓           ↓
              │       Vector DB      APIs
              │           ↓           │
              └───────────┼───────────┘
                          ↓
                        Prompt
                          ↓
                         LLM
                          ↓
                       Response
                          ↓
                      Backend
                          ↓
                      Frontend
                          ↓
                         USER
```

This is the general idea behind many real AI applications.

## 11. A concrete example: AI University Assistant

A student asks: *"How many credit hours do I need to graduate?"*

```
Student
   ↓
Web UI
   ↓
FastAPI
   ↓
Question
   ↓
Retriever
   ↓
Qdrant
   ↓
Relevant university document
   ↓
Prompt
   ↓
LLM
   ↓
Answer
   ↓
FastAPI
   ↓
Web UI
   ↓
Student
```

Notice: the LLM didn't magically know the university regulations. Your application retrieved the relevant information and provided it to the model. **That's AI Engineering.**

## 12. Why we don't send everything to the LLM

Imagine the university has 500 pages and the user asks one question. You don't want `500 pages → LLM`. Instead:

```
500 pages → Index documents → Search → Find relevant chunks → LLM
```

This is **RAG — Retrieval-Augmented Generation.** You'll study this much more deeply later.

## 13. Application architecture has layers

- **Layer 1 — User Interface:** React / Next.js
- **Layer 2 — API:** FastAPI
- **Layer 3 — AI Logic:** Prompt, RAG, Tools, Agents
- **Layer 4 — Models:** LLM, Embedding Model, Reranker
- **Layer 5 — Data:** PostgreSQL, Qdrant, Files
- **Layer 6 — Infrastructure:** Docker, Cloud, GPU, Monitoring

```
┌─────────────────────────┐
│ UI                      │
├─────────────────────────┤
│ API                     │
├─────────────────────────┤
│ AI Logic                │
├─────────────────────────┤
│ Models                  │
├─────────────────────────┤
│ Data                    │
├─────────────────────────┤
│ Infrastructure          │
└─────────────────────────┘
```

## 14. Where does LangChain fit?

Mostly in the AI application / AI workflow layer:

```
FastAPI → LangChain → Retriever → Prompt → LLM
```

LangChain isn't the model — it's a framework that helps you connect components.

## 15. Where does LangGraph fit?

LangGraph is useful when your AI workflow becomes more complex — for example, an agent that searches, analyzes, uses a tool, checks, and produces a final answer. You can represent this as a workflow/graph:

```
        Agent
       ↙     ↘
   Search    Tool
       ↘     ↙
        Analyze
           ↓
         Answer
```

## 16. Where does Qdrant fit?

Qdrant is a vector database:

```
Documents → Embeddings → Qdrant → Retriever → LLM
```

Remember: **Qdrant ≠ LLM, LangChain ≠ LLM, FastAPI ≠ LLM.** They are components around the model.

## 17. Where does the model provider fit?

Cloud model: `Your Application → FastAPI → LLM API → Provider → Model`

Local model: `Your Application → FastAPI → Local Model Server → Model`

The rest of your application can remain largely the same.

## 18. A production-style architecture

```
                        USER
                          ↓
                     Frontend
                          ↓
                       API
                          ↓
                 Authentication
                          ↓
                    AI Service
                          ↓
              ┌───────────┼───────────┐
              ↓           ↓           ↓
           Memory        RAG         Tools
              ↓           ↓           ↓
           Database     Qdrant      External APIs
              └──────────┬───────────┘
                         ↓
                       Prompt
                         ↓
                    Model Router
                    ↙         ↘
                   ↓           ↓
                Cloud        Local
                 LLM           LLM
                   ↘           ↙
                      Response
                         ↓
                      Validation
                         ↓
                       API
                         ↓
                     Frontend
                         ↓
                        USER
```

Don't worry if this looks complicated — you're not expected to memorize it. The important idea: **an LLM is one component inside a larger software system.**

## 19. The AI Engineer's job

An AI Engineer decides: which model? How much context and what information should reach the model? How to retrieve data (Qdrant? BM25? Hybrid search?)? How to call tools (search, database, calculator, API)? How to expose the system (FastAPI)? How to deploy it (Docker, Cloud, GPU)? How to evaluate it (accuracy, latency, cost)?

That's why AI Engineering is a combination of **Software Engineering + AI/ML + Data + APIs + Infrastructure.**

## 20. The most important architecture to remember

```
             USER
               ↓
            FRONTEND
               ↓
            BACKEND
               ↓
          AI WORKFLOW
          ↙    ↓     ↘
        RAG   TOOLS  MEMORY
          ↘    ↓     ↙
              LLM
               ↓
            RESPONSE
               ↓
             USER
```

That's the mental model we'll use throughout your AI Engineer journey.

## What you should remember

An LLM application is not just an LLM. It's usually:

```
Application
│
├── Frontend
├── Backend
├── Database
├── AI Workflow
│   ├── Prompting
│   ├── RAG
│   ├── Tools
│   └── Memory
├── Models
│   ├── LLM
│   └── Embedding Model
└── Infrastructure
```

**AI Engineering is about connecting these pieces into a reliable system that solves a real problem.**
""",
                    "estimated_minutes": 30,
                    "has_code_examples": False,
                },
                "exercises": [
                    {
                        "title": "Arrange the \"Chat with my PDF\" Architecture",
                        "description": "You're building \"Chat with my PDF\" and have these components available: React, FastAPI, Qdrant, LLM, Embedding Model, PDF.\n\n1. Arrange these components into a full request flow, from the PDF being ingested to the user receiving an answer. Be specific about the order and what each component does at each stage.\n2. Identify which layer (from the lesson's 6-layer model: UI, API, AI Logic, Models, Data, Infrastructure) each of the 6 components belongs to.\n3. Explain in 2-3 sentences why sending the entire PDF directly to the LLM on every question would be a poor architecture choice, using ideas from this lesson and the Context Windows lesson.",
                        "difficulty": DifficultyLevel.beginner,
                        "skill_tested": ["ai-developer", "architecture", "rag", "system-design"],
                    },
                ],
                "quiz": {
                    "title": "LLM Application Architecture — Knowledge Check",
                    "questions": [
                        {
                            "question": "In a typical AI application, does the frontend usually talk directly to the LLM?",
                            "options": [
                                "Yes, always, to reduce latency",
                                "No — the frontend usually talks to the backend, which then calls the LLM",
                                "Only if the frontend is built in React",
                                "The frontend replaces the need for a backend entirely",
                            ],
                            "correct": 1,
                            "explanation": "The typical flow is Frontend → Backend → LLM. The backend handles logic like authentication, prompts, RAG, and tool calls before involving the model.",
                        },
                        {
                            "question": "In the university assistant example, why does the application use a vector database (Qdrant) instead of sending the entire 500-page document to the LLM every time?",
                            "options": [
                                "Vector databases make the LLM smarter",
                                "To retrieve only the relevant chunks for a given question, avoiding wasted tokens, cost, and context window usage",
                                "Because LLMs cannot process PDF files at all",
                                "Because vector databases replace the need for an LLM entirely",
                            ],
                            "correct": 1,
                            "explanation": "This is RAG: retrieving only the relevant chunks (via the vector database) keeps the context small, relevant, and efficient, instead of sending an entire large document with every request.",
                        },
                        {
                            "question": "Which statement correctly reflects the relationship between LangChain, Qdrant, FastAPI, and the LLM?",
                            "options": [
                                "They are all different names for the same underlying LLM",
                                "LangChain, Qdrant, and FastAPI are components around the model — they are not the LLM itself",
                                "FastAPI is a type of LLM used for backend tasks",
                                "Qdrant is a prompting framework, and LangChain is a database",
                            ],
                            "correct": 1,
                            "explanation": "LangChain is a framework for connecting components, Qdrant is a vector database, and FastAPI is a backend framework — none of them are the LLM itself; they sit around it in the architecture.",
                        },
                        {
                            "question": "What is the core idea behind the 'most important architecture to remember' (User → Frontend → Backend → AI Workflow [RAG/Tools/Memory] → LLM → Response → User)?",
                            "options": [
                                "The LLM should always be the very first component a user interacts with",
                                "An LLM is one component inside a larger software system that includes RAG, tools, and memory around it",
                                "RAG, Tools, and Memory are optional add-ons that most applications don't need",
                                "The frontend and backend can be skipped if the LLM is powerful enough",
                            ],
                            "correct": 1,
                            "explanation": "The core lesson is that a real LLM application is a full system — frontend, backend, and an AI workflow (RAG, tools, memory) — with the LLM as just one component, not the entire application.",
                        },
                    ],
                    "passing_score": 70,
                },
                "project": {
                    "title": None,
                    "description": None,
                    "difficulty": DifficultyLevel.intermediate,
                    "tech_stack": [],
                    "objectives": [],
                    "rubric": {},
                    "starter_repo_url": None,
                    "estimated_hours": None,
                },
            },
        ] + [
            {
                "title":            "Mini Project",
                "slug":              "ai-developer-l1-mini-project",
                "description":       "Build your first real AI application: a small CLI text assistant that can summarize, explain, or translate text using a cloud LLM API — bringing together everything from Level 1.",
                "order":             10,
                "difficulty":        DifficultyLevel.beginner,
                "estimated_hours":   2.0,
                "skill_tags":        ["ai-developer", "llm", "project", "prompt-design"],
                "prerequisite_ids":  [],
                "lesson": {
                    "title": "Mini Project: Build Your First AI Application",
                    "content": """# Mini Project: Build Your First AI Application

Congratulations — you've finished the foundations. Now let's use everything you've learned to build something real: an **AI Text Assistant**. It will take a user's text and ask an LLM to help with it.

## 1. What are we building?

Our application will support three actions:

1. Summarize text
2. Explain text simply
3. Translate text

For example: `User: "Explain this simply: 'Machine learning is a subset of artificial intelligence...'"` — the application sends the request to the LLM, which returns something like *"Machine learning is a way for computers to learn patterns from data."*

## 2. Our architecture

We're intentionally keeping this small:

```
                 USER
                   ↓
             ┌──────────┐
             │ Python   │
             │   App    │
             └────┬─────┘
                  ↓
              Prompt
                  ↓
             ┌──────────┐
             │   LLM    │
             └────┬─────┘
                  ↓
              Response
                  ↓
                 USER
```

This is your first real LLM application.

## 3. What did we learn that appears here?

Almost everything from Level 1: **AI Application** (our Python program), **LLM** (the model we call), **Tokens** (our input/output are tokenized internally), **Context** (the prompt becomes part of the model's context), **Parameters** (the model uses its learned parameters to generate the response), **Cloud** (we use a cloud model API), **Provider** (the API belongs to a model provider), and **Architecture** (`Application → API → Model → Response`).

## 4. Step 1 — Install the SDK

For a cloud provider, you normally install its Python SDK. For example:

```bash
pip install openai
```

## 5. Step 2 — API key

You'll need an API key from your provider. **Never** put the API key directly in your source code.

❌ Don't do:

```python
api_key = "my-secret-key"
```

Instead use an environment variable:

```bash
export OPENAI_API_KEY="your-api-key"
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-api-key"
```

## 6. Step 3 — Create the client

```python
from openai import OpenAI

client = OpenAI()
```

The SDK reads the API key from the environment.

## 7. Step 4 — Send a request

```python
response = client.responses.create(
    model="YOUR_MODEL",
    input="Explain Python in simple words."
)

print(response.output_text)
```

The exact model name depends on the models currently available to your account/provider. The important concept:

```
Your Python code → API request → LLM → Response
```

## 8. Let's make it interactive

```python
from openai import OpenAI

client = OpenAI()

question = input("Ask the AI: ")

response = client.responses.create(
    model="YOUR_MODEL",
    input=question
)

print("\\nAI:")
print(response.output_text)
```

Now you have a tiny AI application.

## 9. What happens internally?

Suppose you enter *"What is FastAPI?"*:

```
input() → "What is FastAPI?" → OpenAI API → Model → Generated tokens → Text response → print()
```

That's it — you have just built an AI application.

## 10. Let's make it more useful

Instead of letting the user ask anything, let's give the application a specific role — an **AI Programming Tutor**:

```python
from openai import OpenAI

client = OpenAI()

question = input("Ask your programming question: ")

prompt = f\"\"\"
You are a programming tutor.

Explain concepts in simple language.
Use small examples when useful.

Student question:
{question}
\"\"\"

response = client.responses.create(
    model="YOUR_MODEL",
    input=prompt
)

print("\\nAI Tutor:")
print(response.output_text)
```

Now we've added an important AI Engineering concept: **prompt design**.

## 11. Why is the prompt important?

Compare `"Explain FastAPI."` with:

```
You are a programming tutor.

Explain FastAPI to a beginner.
Use simple language.
Give one small example.
Avoid unnecessary technical details.

Question:
What is FastAPI?
```

The second prompt gives the model more guidance, so it can produce a response that better matches your application's purpose.

## 12. Add our three features

Let's make the user choose an action:

```
              USER
                ↓
           Choose Action
          ↙      ↓      ↘
    Summarize  Explain  Translate
          ↘      ↓      ↙
              Prompt
                ↓
               LLM
                ↓
             Response
```

A simple implementation:

```python
from openai import OpenAI

client = OpenAI()

print("1. Summarize")
print("2. Explain simply")
print("3. Translate to English")

choice = input("Choose: ")
text = input("\\nEnter text: ")

if choice == "1":
    instruction = "Summarize the text briefly."

elif choice == "2":
    instruction = "Explain the text in very simple language."

elif choice == "3":
    instruction = "Translate the text to English."

else:
    print("Invalid choice.")
    exit()

prompt = f\"\"\"
{instruction}

Text:
{text}
\"\"\"

response = client.responses.create(
    model="YOUR_MODEL",
    input=prompt
)

print("\\nResult:")
print(response.output_text)
```

Now it's a small but real AI application.

## 13. What did YOU build?

```
┌────────────────────────────┐
│      AI TEXT ASSISTANT     │
├────────────────────────────┤
│                            │
│  1. Summarize              │
│  2. Explain                │
│  3. Translate              │
│                            │
│            ↓               │
│         Prompt             │
│            ↓               │
│           LLM              │
│            ↓               │
│         Response           │
│                            │
└────────────────────────────┘
```

That's the beginning of AI Engineering.

## 14. What is missing?

Our application is useful, but still very basic. A production AI application might add:

```
Authentication → FastAPI → Prompt Management → RAG → Tools → LLM → Output Validation → Logging → Monitoring
```

We'll learn these concepts in later levels.

## 15. The most important lesson

Look at what we *didn't* do: ❌ train an LLM, ❌ build a transformer from scratch, ❌ collect billions of documents, ❌ buy GPUs, ❌ implement neural network mathematics.

Instead:

```
Python → API → Existing LLM → AI Application
```

That's exactly the mindset of an AI Developer / AI Engineer.

## Level 1 Complete! 🧠

You've now learned the foundation: What AI Developers Build → Models vs Applications → LLMs → Tokens → Context Windows → Parameters → Cloud vs Local → Model Providers → Application Architecture → Mini Project.

The whole thing can be summarized as:

```
                    AI ENGINEERING

                         USER
                           ↓
                       Application
                           ↓
                       AI Workflow
                      ↙    ↓     ↘
                   Data   Tools   Prompt
                      ↘    ↓     ↙
                          LLM
                           ↓
                       Response
                           ↓
                          USER
```

## Level 1 Final Mental Model

If you remember only one diagram, remember this:

```
                    ┌──────────────┐
                    │     USER     │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │ APPLICATION  │
                    │              │
                    │ Frontend     │
                    │ Backend      │
                    │ AI Logic     │
                    │ RAG          │
                    │ Tools        │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │     LLM      │
                    │              │
                    │ Parameters   │
                    │ Context      │
                    │ Tokens       │
                    └──────┬───────┘
                           ↓
                    ┌──────────────┐
                    │   RESPONSE   │
                    └──────────────┘
```

The model is the engine. The application is the complete machine.
""",
                    "estimated_minutes": 40,
                    "has_code_examples": True,
                },
                "exercises": [
                    {
                        "title": "Add a Fourth Action: Rewrite for Tone",
                        "description": "Extend the AI Text Assistant with a 4th menu option: \"Rewrite in a different tone\" (e.g. formal, friendly, or concise).\n\n1. Write the new menu branch (the `elif choice == \"4\":` block) including a clear `instruction` string.\n2. The lesson emphasizes that prompt design matters. Write two versions of the instruction for this new action — a weak, vague one and a strong, specific one — and explain in 2-3 sentences why the strong version would produce more consistent results.\n3. Bonus (optional, no starter code required): describe how you'd ask the user which tone they want, and how you'd insert that choice into the prompt.",
                        "starter_code": "if choice == \"1\":\n    instruction = \"Summarize the text briefly.\"\nelif choice == \"2\":\n    instruction = \"Explain the text in very simple language.\"\nelif choice == \"3\":\n    instruction = \"Translate the text to English.\"\nelif choice == \"4\":\n    # TODO: add your rewrite-for-tone instruction here\n    instruction = None\nelse:\n    print(\"Invalid choice.\")\n    exit()\n",
                        "difficulty": DifficultyLevel.beginner,
                        "skill_tested": ["ai-developer", "prompt-design", "python"],
                    },
                ],
                "quiz": {
                    "title": "Mini Project — Knowledge Check",
                    "questions": [
                        {
                            "question": "Why should an API key never be hardcoded directly into source code (e.g. api_key = \"my-secret-key\")?",
                            "options": [
                                "Hardcoding makes the API calls slower",
                                "It's a security risk — the key could leak (e.g. via version control) and should instead be read from an environment variable",
                                "The SDK technically cannot read a hardcoded key",
                                "It has no real downside, it's just a style preference",
                            ],
                            "correct": 1,
                            "explanation": "Hardcoded secrets are easy to accidentally commit to source control or expose. Reading from an environment variable keeps the key out of the codebase.",
                        },
                        {
                            "question": "In the project's architecture (Python App → Prompt → LLM → Response), what role does the 'Prompt' step play?",
                            "options": [
                                "It trains the model on the user's text",
                                "It packages the instruction and user text into the input sent to the LLM",
                                "It stores the conversation permanently in a database",
                                "It converts the LLM's response into tokens",
                            ],
                            "correct": 1,
                            "explanation": "The prompt is how the application communicates what it wants — combining an instruction (e.g. 'summarize briefly') with the user's text before sending it to the LLM.",
                        },
                        {
                            "question": "Comparing a vague prompt ('Explain FastAPI.') to a detailed one (role + audience + format instructions), what does the lesson say about the detailed version?",
                            "options": [
                                "It always costs less in tokens",
                                "It gives the model more guidance, producing a response that better matches the application's purpose",
                                "It has no effect on the output, only on formatting",
                                "It prevents the model from making any factual errors",
                            ],
                            "correct": 1,
                            "explanation": "A more specific prompt (giving the model a role, audience, and format constraints) helps steer the model's output toward what the application actually needs — this is prompt design.",
                        },
                        {
                            "question": "What did the AI Developer in this project NOT need to do to build a working AI Text Assistant?",
                            "options": [
                                "Write Python code to call an API",
                                "Design a prompt for the task",
                                "Train a large language model from scratch",
                                "Handle the user's choice of action",
                            ],
                            "correct": 2,
                            "explanation": "The whole point of the mini project is that you built a real AI application without training a model, building a transformer, or buying GPUs — you used Python, an API, and an existing LLM.",
                        },
                    ],
                    "passing_score": 70,
                },
                "project": {
                    "title": "AI Text Assistant",
                    "description": "Build a command-line AI Text Assistant in Python that lets a user choose one of three actions — summarize, explain simply, or translate to English — and applies that action to text they provide, using a cloud LLM API. This project ties together every Level 1 concept: models vs applications, tokens/context flowing through the API call, cloud providers, and prompt design.",
                    "difficulty": DifficultyLevel.beginner,
                    "tech_stack": ["Python", "LLM Provider SDK (e.g. OpenAI or Anthropic)", "Environment Variables"],
                    "objectives": [
                        "Install and configure an LLM provider SDK, reading the API key from an environment variable (never hardcoded)",
                        "Create an API client and send a basic prompt to the LLM, printing the response",
                        "Build an interactive CLI that accepts free-form user input and returns a model-generated answer",
                        "Implement a menu with three actions (Summarize / Explain simply / Translate to English), each mapped to a distinct instruction string",
                        "Construct a well-designed prompt that combines the chosen instruction with the user's text, and explain why prompt wording affects output quality",
                        "(Stretch) Add a 4th action of your own design (e.g. rewrite in a different tone) following the same pattern",
                    ],
                    "rubric": {
                        "functionality": "The app runs, accepts input, correctly routes to summarize/explain/translate, and returns a sensible LLM response for each action",
                        "security": "The API key is read from an environment variable, not hardcoded in the source file",
                        "prompt_design": "Each action uses a clear, specific instruction (not just the raw user text) demonstrating deliberate prompt design",
                        "code_quality": "Code is readable, has sensible variable names, and handles an invalid menu choice gracefully",
                        "understanding": "The learner can explain, in their own words, how their code maps to the Application → Prompt → LLM → Response architecture from the lesson",
                    },
                    "starter_repo_url": None,
                    "estimated_hours": 2.0,
                },
            },
        ],
    }
