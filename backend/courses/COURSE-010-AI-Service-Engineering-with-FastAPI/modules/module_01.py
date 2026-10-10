"""M01.L01 — Introduction to Generative AI Services.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 1, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Build a practical mental model of generative AI, understand where it adds "
    "value in applications, identify its production risks, and learn why a web "
    "service layer such as FastAPI is useful for connecting models to real systems."
)

SOURCE_CHAPTER = 1

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Introduction to Generative AI Services",

    "slug": "generative-ai-services-m01-l01",

    "description": (
        "Learn what generative AI is, how major generative model families work at "
        "a high level, why context matters, where GenAI can improve applications, "
        "how an AI service is structured, and what risks must be controlled before "
        "putting generative models into production."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 1.5,

    "skill_tags": [
        "generative-ai",
        "genai-services",
        "fastapi",
        "prompt-context",
        "ai-architecture",
        "ai-safety",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Introduction to Generative AI Services",

        "content": """
# Introduction to Generative AI Services

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L01  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 1 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what generative AI is and distinguish generation from ordinary deterministic computation.
- Describe inference, sampling, randomness, latent space, modality, and multimodality.
- Recognize the major generative model families introduced in the chapter.
- Explain why context-rich prompts usually produce more relevant outputs.
- Identify practical ways GenAI can improve software products and workflows.
- Sketch the main components of a generative AI service.
- Explain why a web framework such as FastAPI can sit between a model and the rest of an application.
- Identify important adoption barriers such as hallucinations, privacy, security, misuse, consistency, and integration risk.
- Describe the major capabilities of the chapter's capstone GenAI service.

---

## 1. What is generative AI?

Generative AI is a branch of machine learning focused on **creating new content from patterns learned from data**.

A useful way to think about it is:

1. A model is trained on examples.
2. Training adjusts the model so it captures useful patterns and relationships in those examples.
3. Later, the trained model is given an input or sampled from.
4. The model produces a new output that resembles the kinds of patterns it learned without simply needing to copy a training example.

Imagine a model trained on many butterfly photographs. During training, it learns statistical relationships that characterize those images: shapes, colors, textures, wing patterns, backgrounds, and many interactions between them.

After training, we can ask the model to produce a new butterfly image. The result can look like a believable member of the learned distribution even though that exact image did not appear in the training set.

### Inference

Using a trained model to produce new content is called **inference**.

Training and inference are different stages:

| Stage | Main purpose |
|---|---|
| Training | Learn useful patterns from data |
| Inference | Use the trained model to generate or predict an output |

### Why generation is probabilistic

A generative system should not return exactly the same output every time simply because the input is similar. The chapter explains that randomness can be introduced during sampling so the system can produce variations.

That means a generative model is often **probabilistic**.

A fixed arithmetic rule such as averaging values is deterministic: the same inputs produce the same result.

A probabilistic generator can produce different valid samples because randomness influences which part of the learned distribution is explored.

[[IMAGE_NEEDED: Generative model training and sampling | A simple two-stage diagram showing a butterfly-image dataset flowing into model training, followed by a trained model being sampled to produce several new butterfly images with visible variation | Learner should notice the separation between training and inference and that generated outputs are related to, but not identical to, the training examples]]

### A useful mental model

Do not think of a generative model as a database that stores a single ready-made answer for every possible request.

A better beginner mental model is:

> **Training learns a probability-rich representation of patterns; inference uses that learned representation to construct a new output.**

---

## 2. Major families of generative models

The chapter introduces several important model families. You do not need to master their mathematics yet. At this stage, focus on the **core idea each family uses to generate data**.

### Variational autoencoders (VAEs)

A VAE learns to compress data into a lower-dimensional mathematical representation called a **latent space**.

It has two important ideas:

- **Encoding:** map complex input data into a compact latent representation.
- **Decoding:** reconstruct or generate data from points in that latent representation.

This makes VAEs useful for thinking about generation as movement through a structured space of learned features.

### Generative adversarial networks (GANs)

A GAN contains two neural networks trained against each other:

- A **generator** tries to create realistic samples.
- A **discriminator** tries to distinguish generated samples from real training data.

The competition pushes the generator toward producing outputs that are increasingly difficult for the discriminator to reject.

After training, the generator is the component used to create new samples.

### Autoregressive models

Autoregressive models generate a sequence one step at a time.

The key idea is:

> Predict the next value using the values that came before it.

For text, that can mean predicting the next token based on the preceding tokens, then repeating the process to continue the sequence.

### Normalizing flow models

Normalizing flows learn transformations between:

- a simple probability distribution, and
- a more complicated data distribution.

Generation can begin with a simple sampled point and transform it into a sample from the learned complex distribution.

### Energy-based models (EBMs)

Energy-based models assign an **energy value** to possible configurations.

The chapter's intuition is:

- observed or desirable data should receive lower energy,
- other configurations should receive higher energy.

Training teaches the model to differentiate these configurations.

### Diffusion models

Diffusion models use a noise-based learning process.

At a high level:

1. Noise is gradually added to training data.
2. The model learns how to reverse that corruption process.
3. During generation, it starts from noise.
4. It progressively removes noise until a structured output emerges.

This gives you an important conceptual contrast:

> VAEs emphasize encoding and decoding through a latent representation, while diffusion models emphasize learning a denoising process.

### Transformers

Transformers are especially important for sequence data such as text.

Their central mechanism is **self-attention**, which helps the model represent relationships between elements in a sequence.

For language, this allows the model to use surrounding context when processing and generating text.

Transformers are widely used as language models because they can model long sequences and relationships within text efficiently.

### Keep the families separate in your mind

At this stage, use this table as a memory aid:

| Model family | Beginner mental model |
|---|---|
| VAE | Compress into latent space, then decode |
| GAN | Generator improves by competing with a discriminator |
| Autoregressive | Generate the next element from previous elements |
| Normalizing flow | Transform a simple distribution into a complex one |
| Energy-based | Learn which configurations should have low or high energy |
| Diffusion | Learn to reverse noise |
| Transformer | Model contextual relationships in sequences using attention |

The source introduces these families together as important approaches you may encounter in GenAI work. You do not yet need to choose between them; the goal here is recognition and conceptual separation.

{{exercise:M01.L01.EX01}}

---

## 3. Latent space, modalities, and multimodal AI

### What is a latent space?

A **latent space** is a compressed mathematical representation that preserves important information about input data.

Suppose an image has thousands or millions of pixel values. Working directly with every pixel is high-dimensional.

An encoder can map that image into a smaller set of numerical values that capture meaningful structure.

Conceptually:

```text
High-dimensional input
        ↓
      Encoder
        ↓
Compact latent representation
        ↓
      Decoder
        ↓
Reconstructed or generated output
```

The important point is not merely that the data becomes smaller.

The latent representation is useful because nearby or related locations in the learned space can represent related learned concepts. Sampling or navigating this space can support generation of new content.

[[IMAGE_NEEDED: VAE latent-space concept | A diagram showing several high-dimensional inputs being encoded into points or clusters in a compact 2D latent-space illustration, with selected latent points decoded into reconstructed or newly generated outputs | Learner should notice that the latent space is a compressed learned representation and that new outputs can be produced by sampling points within it]]

### What is a modality?

A **modality** is a type of data a model can process or generate.

Examples introduced in the chapter include:

- text,
- images,
- audio,
- video,
- point clouds,
- 3D meshes.

A model may be specialized for one modality, or it may support more than one.

### Multimodal models

A **multimodal** model can work with multiple data types.

For example, a multimodal system may accept text and images, or combine text, audio, and visual information.

This matters because real applications rarely exist in only one medium. A support assistant may need text and speech. A design application may combine text instructions with images. A document assistant may need text plus scanned visual layouts.

### Generation is broader than chatbots

Do not reduce generative AI to conversational text.

The chapter gives a much wider view:

- language models can power chatbots and document-processing systems,
- audio models can synthesize speech or music,
- image models can produce visual content,
- video models can generate avatars or other moving content.

The underlying product question is therefore:

> **What kind of information should the user provide, and what modality should the system return?**

---

## 4. Why GenAI changes application design

Traditional software automation often relies on manually coded rules.

For simple cases, that can work very well:

```text
IF condition A is true
THEN perform action B
```

But many real problems contain ambiguity, variation, natural language, visual information, or too many edge cases to describe conveniently with hand-written rules.

Machine learning changed this by allowing systems to learn patterns from examples.

Generative AI extends that shift because it can produce rich outputs such as:

- text,
- code,
- images,
- audio,
- video.

The chapter highlights several application capabilities that can emerge from this.

### 4.1 Facilitating the creative process

Creating something new often starts with an uncomfortable blank page.

A person may need to:

- gather inspiration,
- explore alternatives,
- connect ideas,
- visualize difficult concepts,
- construct a narrative,
- refine an early draft.

GenAI can help with these intermediate steps.

For example, instead of asking a designer to imagine a highly unusual scene entirely mentally, a generative system can turn a detailed description into a visual starting point.

The important lesson is not that the model replaces creativity.

The useful product idea is:

> **A GenAI feature can reduce the friction between an initial idea and something concrete enough to inspect, criticize, and improve.**

[[IMAGE_NEEDED: Hard-to-visualize generated scene | A surreal biomechanical forest containing metallic roots, glowing leaves, gears, digital displays, crystalline ground, organic veins, and a shifting luminous sky, matching the chapter's example concept without requiring exact reproduction of the source figure | Learner should notice how text-to-image generation can make an abstract or difficult-to-visualize description concrete enough to discuss and refine]]

### 4.2 Suggesting contextually relevant solutions

Many real problems are difficult not because no solution exists, but because the correct solution depends on **context**.

The chapter makes a useful claim:

> Context narrows the solution space.

A programming error, for example, may depend on:

- the programming language,
- framework version,
- surrounding code,
- operating system,
- stack trace,
- expected behavior,
- actual behavior.

A short prompt forces the model to guess more of this missing information.

A rich prompt gives the model more evidence about the user's intent.

### 4.3 Personalizing the user experience

Traditional applications usually force users to navigate a predetermined interface.

A GenAI-enabled application can allow users to express intent in natural language.

Imagine a travel application.

Instead of manually selecting many filters, a user might say:

> I want a quiet four-day trip near the sea, with a moderate budget and activities suitable for children.

A language model can help translate that natural-language request into structured preferences, ask follow-up questions, retrieve matching data, and explain recommendations conversationally.

This can make the application feel more like a personal assistant than a static menu system.

### 4.4 Reducing delay in customer support

Traditional scripted chatbots are limited by the paths developers anticipated in advance.

A GenAI support system can potentially:

- retain conversation context,
- use customer preferences,
- create dynamic responses,
- respond to feedback,
- handle a wider range of questions.

However, a production system should not give a model unlimited authority.

A safer design is often:

```text
Customer
   ↓
AI assistant
   ↓
Approved data / business rules / tools
   ↓
Answer or action
   ↓
Escalate when necessary
```

The AI can become the first interaction layer while human agents remain available for uncertain, sensitive, or exceptional cases.

### 4.5 Acting as an interface to complex systems

Many useful systems are difficult for non-specialists to operate directly.

Examples include:

- databases,
- APIs,
- developer tools,
- advanced design applications.

A language model can translate natural-language intent into an instruction that another component understands.

For example:

```text
User request:
"Show me the quarterly performance of my portfolio."

        ↓

Language model interprets intent

        ↓

Controlled query/tool instruction

        ↓

Database or analytics system

        ↓

Result explained to the user
```

The model becomes an **interface**, not necessarily the system that performs the underlying operation.

This distinction becomes important for security.

The model may propose an action, while trusted application code validates and executes it.

### 4.6 Automating administrative work

Some business processes involve documents with varying structures, such as:

- invoices,
- purchase orders,
- remittance documents.

Rigid automation can become fragile when layout or wording changes.

The chapter suggests that generative models can help handle variation, inspect outputs, fill gaps, or flag uncertain cases for manual review.

A strong design principle is:

> **Use AI to handle variation, but preserve validation and human review where mistakes are costly.**

### 4.7 Scaling content generation

GenAI can accelerate:

- brainstorming,
- outlining,
- summarization,
- rewriting,
- drafting,
- idea exploration.

This can move human effort away from repeatedly producing low-level first drafts and toward higher-level concerns such as:

- structure,
- argument,
- taste,
- review,
- correctness,
- style,
- final judgment.

The chapter presents this productivity gain as one reason more applications may include generative features.

---

## 5. Why context-rich prompts matter

A generative model does not automatically know the exact intention behind a short request.

Consider this prompt:

```text
ties
```

What does the user want?

Possibilities include:

- buying clothing,
- learning knot types,
- understanding the word,
- comparing styles,
- something else entirely.

Now compare it with:

```text
Explain three common necktie knots for a beginner and when each is appropriate.
```

The second prompt gives the model much more evidence about:

- the subject,
- the intended task,
- the audience,
- the desired scope.

### The prompt-quality principle

A useful beginner principle from the chapter is:

> **The richer the relevant context, the less the model has to guess about your intent.**

That does not mean longer is always better.

Irrelevant detail can create noise.

The goal is **useful context**.

A strong prompt often contains some combination of:

- the task,
- background information,
- constraints,
- available data,
- desired output,
- audience,
- success criteria.

### From generic to useful

Weak prompt:

```text
Fix my API.
```

Better prompt:

```text
My FastAPI endpoint returns HTTP 422 when I POST this JSON payload.
Here is the request body, the Pydantic schema, and the error response.
Explain the likely mismatch and show the smallest correction.
```

The second request gives the model a much narrower problem to solve.

This same idea applies when building a GenAI application.

Your application can automatically gather useful context from:

- a database,
- a user profile,
- uploaded documents,
- prior conversation history,
- an external API.

Then it can provide that context to the model before generation.

{{exercise:M01.L01.EX02}}

---

## 6. How a generative AI service is built

Calling a model directly is only one small part of a production AI application.

A real service may need to:

- authenticate the user,
- retrieve information,
- call external APIs,
- access databases,
- enrich the prompt,
- enforce permissions,
- call the model,
- validate the output,
- run a tool,
- return a response,
- record conversation history.

This is why the chapter places the generative model behind a **web service layer**.

### The web server as an intermediary

A useful simplified architecture is:

```text
User / Client
     ↓
API Router
     ↓
Authentication + Authorization
     ↓
Context / Data Retrieval
     ↓
Prompt or Instruction Construction
     ↓
Generative Model
     ↓
Validation / Guardrails
     ↓
Response Router
     ↓
User
```

The server may also communicate with:

```text
Databases
External APIs
Vector databases
Internal services
Tool functions
File stores
```

The model should not have to own every responsibility.

The web service coordinates those responsibilities.

{{image:ai-service-architecture}}

### Tool use

A language model can also construct an instruction for another system.

For example:

```text
User:
"Cancel order 8123."

        ↓

Model interprets request

        ↓

Application creates a structured tool request

        ↓

Authorization and validation checks

        ↓

Order service executes the cancellation
```

The critical engineering lesson is this:

> **Understanding a request and executing a privileged action are separate responsibilities.**

A model may help decide *what the user wants*.

Trusted application logic should decide *whether the action is allowed and how it is executed safely*.

{{exercise:M01.L01.EX03}}

---

## 7. Why FastAPI is useful for GenAI services

The chapter compares three well-known Python web frameworks:

| Framework | High-level characterization in the source |
|---|---|
| Django | Mature, full-stack framework with many built-in capabilities |
| Flask | Lightweight and extensible microframework |
| FastAPI | Modern Python framework designed for API development, speed, and developer ergonomics |

The chapter favors FastAPI for GenAI services because it keeps the application in the Python ecosystem while offering API-oriented features.

Important benefits highlighted include:

- data validation,
- type safety,
- automatic API documentation,
- strong performance,
- convenient support for modern API development.

### Why Python matters here

GenAI and machine-learning ecosystems are heavily Python-oriented.

If the web API and the model integration both live in Python, the service can directly use model libraries, data-processing libraries, and supporting AI tooling without crossing language boundaries for every model interaction.

### Why not automatically choose the biggest framework?

A GenAI backend often needs a focused API layer rather than a complete monolithic web application.

A useful engineering question is therefore:

> What is the smallest framework that comfortably provides the API features, validation, concurrency model, and integration points my service needs?

The chapter argues that FastAPI is a strong fit for this role.

### Important boundary

FastAPI does not make a model accurate, safe, or context-aware by itself.

FastAPI helps you build the **service layer** around the model.

You still need architecture for:

- context retrieval,
- security,
- permissions,
- validation,
- guardrails,
- storage,
- monitoring,
- tool execution.

---

## 8. What prevents broader adoption of GenAI services?

Generative AI is powerful, but production systems cannot be designed around capability alone.

They must also be designed around failure.

The chapter identifies several barriers.

### 8.1 Inaccuracy and hallucinations

A generated answer can sound confident and plausible while being incorrect.

The chapter calls fabricated or incorrect information produced by a GenAI model a **hallucination**.

This matters because fluency is not proof of truth.

A user may see a polished answer and assume it is reliable even when the model has generated unsupported details.

This is especially dangerous when the cost of an incorrect answer is high.

### 8.2 Relevance, quality, and consistency

A model may produce:

- generic answers,
- repetitive answers,
- responses that ignore important context,
- outputs of uneven quality,
- inconsistent answers across similar requests.

Production applications usually require more predictable behavior than a casual experimentation environment.

### 8.3 Data privacy

A GenAI system may interact with:

- private customer data,
- company documents,
- internal databases,
- confidential workflows.

Developers must control what information reaches the model and what can leave the system.

### 8.4 Cybersecurity and malicious use

If a model can call tools or access sensitive systems, malicious instructions can become more serious than a bad text response.

The application needs controls around:

- authentication,
- authorization,
- tool permissions,
- input validation,
- output validation,
- access to internal resources.

### 8.5 Integration difficulty

Connecting an AI service to an existing organization can be difficult because of:

- incompatible systems,
- existing workflows,
- technical complexity,
- security requirements,
- privacy requirements,
- the risk of disrupting established processes.

The model itself may be easy to call through an API, while the surrounding integration work is the difficult engineering problem.

### 8.6 Limited autonomy

Organizations may hesitate to give a model direct control over sensitive operations such as:

- payments,
- internal databases,
- irreversible actions.

A safer architecture can keep the model inside a controlled workflow where important actions require deterministic checks or human approval.

### 8.7 Limits of generated content

The chapter also warns that generated outputs may follow common patterns and can become:

- generic,
- repetitive,
- uninspiring,
- incorrect.

So the right product question is not:

> Can the model generate something?

It is:

> Can the complete system generate something useful, relevant, safe, and sufficiently reliable for this specific task?

### Engineering responses

The source points to several categories of mitigation:

- software engineering practices for privacy and security,
- better model inputs and contextual information,
- fine-tuning for particular use cases,
- controls that improve output relevance and consistency,
- guardrails and review around risky behavior.

{{exercise:M01.L01.EX04}}

---

## 9. The capstone service you are building toward

The chapter closes by introducing a GenAI service built around FastAPI.

The project is deliberately broader than a simple chatbot.

It is intended to combine several real production concerns.

### Model capabilities

The service will integrate multiple model types, including:

- a language model for text generation and conversation,
- an audio model for text-to-speech,
- a Stable Diffusion model for image generation.

This reinforces the earlier idea of multiple modalities.

### Real-time responses

The service is intended to return outputs in forms such as:

- text,
- audio,
- images.

### Retrieval-augmented generation

The project will use **RAG** to work with uploaded documents through a vector database.

At a beginner level, the important idea is:

> Retrieve relevant information first, then give that information to the model as context for generation.

### External information and systems

The service will also interact with:

- the web,
- internal databases,
- external systems,
- APIs.

This is how the service can gather information that is not already present in the user's prompt.

### Conversation memory

Conversation history will be stored in a relational database.

This allows the system to preserve useful interaction state rather than treating every message as completely isolated.

### Authentication and authorization

The capstone includes:

- token-based authentication,
- GitHub identity login,
- authorization guards.

Authentication asks:

> Who is the user?

Authorization asks:

> What is that user allowed to access or do?

These are not the same thing.

### Guardrails

The service will include controls designed to reduce misuse and abuse.

This is essential because once a model can retrieve private information or trigger external actions, safety becomes a system-level responsibility.

### User interfaces

The book uses lightweight UI tools such as Streamlit and simple HTML while focusing on API engineering.

The source also notes that real systems may connect the GenAI service to more modular frontend technologies.

### The full mental model

By the end of this chapter, your mental model should look like this:

```text
                    ┌──────────────────┐
                    │       User       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Client / UI    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ FastAPI Service  │
                    └────────┬─────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       │                     │                     │
       ▼                     ▼                     ▼
 Authentication       Context / Retrieval      Guardrails
 Authorization        DBs / APIs / RAG        Validation
       │                     │                     │
       └─────────────────────┼─────────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Generative Model │
                    └────────┬─────────┘
                             │
                             ▼
                    Text / Audio / Image
                    or controlled tool action
```

The key idea is that a production GenAI application is **not just a model**.

It is a software system that surrounds the model with context, permissions, integrations, validation, persistence, and control.

---

## Important misconceptions

### Misconception 1

> A generative AI application is simply a chatbot connected to an LLM API.

### Why this is wrong

A production GenAI service may need authentication, retrieval, databases, APIs, tools, permissions, validation, guardrails, history, and multiple modalities. The model is only one component.

### Misconception 2

> If a generated answer sounds natural and confident, it is probably correct.

### Why this is wrong

Generative models can produce hallucinations: plausible-sounding information that is incorrect or unsupported. Fluency and factual reliability are different properties.

### Misconception 3

> More prompt text always produces a better result.

### Why this is wrong

The useful principle is **relevant context**, not maximum length. A good prompt reduces ambiguity by supplying the information needed to understand the task.

### Misconception 4

> If an LLM can generate a tool instruction, it should be allowed to execute that instruction directly.

### Why this is wrong

Interpretation and execution should be separated. Sensitive actions require application-level validation, permissions, and security controls.

---

## Key terminology

| Term | Meaning |
|---|---|
| Generative AI | Machine-learning systems that create new content using patterns learned from data |
| Trained model | A mathematical model whose parameters have been adjusted using training data |
| Inference | Using a trained model to produce an output |
| Sampling | Selecting or generating an output from the model's learned probability distribution |
| Probabilistic | Involving uncertainty or randomness so multiple outputs may be possible |
| Latent space | A compressed learned mathematical representation of important features in data |
| Modality | A data type such as text, image, audio, video, point cloud, or 3D mesh |
| Multimodal | Able to work with more than one modality |
| Self-attention | A transformer mechanism for representing relationships among elements in a sequence |
| Context | Information that helps narrow the meaning of a request and the relevant solution space |
| Hallucination | Generated information that is made up, unsupported, or factually incorrect |
| RAG | A pattern in which relevant information is retrieved and provided to a model as generation context |
| Authentication | Verifying who a user is |
| Authorization | Determining what an authenticated user is allowed to do |
| Guardrail | A control intended to constrain unsafe, unwanted, or invalid model behavior |

---

## Self-check

Before continuing, make sure you can answer:

1. What is the difference between model training and inference?
2. Why can the same generative system produce different outputs?
3. What is the basic idea behind VAEs, GANs, autoregressive models, diffusion models, and transformers?
4. What information is represented by a latent space?
5. What is the difference between a modality and a multimodal model?
6. Why do context-rich prompts usually produce more relevant responses?
7. Name four ways GenAI can change the design of an application.
8. Why should a generative model be placed behind an application or API control layer?
9. What responsibilities belong to the service layer rather than to the model itself?
10. What is a hallucination, and why is it dangerous in sensitive applications?
11. What is the difference between authentication and authorization?
12. What major capabilities will the capstone project combine?

---

## Retain this idea

**A useful GenAI product is not created by calling a model alone. The real engineering work is building a controlled service around the model that supplies relevant context, connects trusted tools and data, protects users and systems, validates behavior, and turns probabilistic generation into a reliable application capability.**
""",

        "estimated_minutes": 90,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "what-is-generative-ai",
                "title": "What is generative AI?",
                "order": 1,
            },
            {
                "id": "model-families",
                "title": "Major families of generative models",
                "order": 2,
            },
            {
                "id": "latent-space-and-modalities",
                "title": "Latent space, modalities, and multimodal AI",
                "order": 3,
            },
            {
                "id": "why-genai-in-applications",
                "title": "Why GenAI changes application design",
                "order": 4,
            },
            {
                "id": "context-rich-prompts",
                "title": "Why context-rich prompts matter",
                "order": 5,
            },
            {
                "id": "service-architecture",
                "title": "How a generative AI service is built",
                "order": 6,
            },
            {
                "id": "why-fastapi",
                "title": "Why FastAPI is useful for GenAI services",
                "order": 7,
            },
            {
                "id": "adoption-barriers",
                "title": "What prevents broader adoption of GenAI services?",
                "order": 8,
            },
            {
                "id": "capstone",
                "title": "The capstone service you are building toward",
                "order": 9,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Match the Generative Model Family",

            "lesson_code": "M01.L01",

            "section_id": "model-families",

            "placement": "after_section",

            "description": (
                "Practice separating the central ideas behind the major generative "
                "model families introduced in the chapter."
            ),

            "instructions": (
                "Match each scenario to the most appropriate model family from this "
                "lesson: VAE, GAN, autoregressive model, normalizing flow, "
                "energy-based model, diffusion model, or transformer.\n\n"
                "1. A system learns to reverse a gradual corruption-by-noise process.\n"
                "2. A generator improves while competing against a discriminator.\n"
                "3. A model predicts the next element using previous elements.\n"
                "4. A model compresses inputs into a latent representation and decodes them.\n"
                "5. A model uses self-attention to represent contextual relationships in a sequence.\n\n"
                "For each answer, write one sentence explaining the clue that led you "
                "to your choice."
            ),

            "expected_output": (
                "Five model-family matches, each accompanied by a one-sentence justification."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "model-family-recognition",
                "conceptual-reasoning",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Turn a Weak Prompt into a Context-Rich Prompt",

            "lesson_code": "M01.L01",

            "section_id": "context-rich-prompts",

            "placement": "after_section",

            "description": (
                "Practice reducing ambiguity by adding only the context a model needs "
                "to understand the user's intent."
            ),

            "instructions": (
                "Start with this weak prompt:\n\n"
                "`Help me with my API.`\n\n"
                "Rewrite it into a useful prompt for a technical assistant. Include:\n"
                "1. The task or failure.\n"
                "2. Relevant technical context.\n"
                "3. What information or evidence is available.\n"
                "4. The desired form of the answer.\n"
                "5. At least one constraint.\n\n"
                "Then identify which sentence or phrase in your revised prompt provides "
                "each of those five elements."
            ),

            "expected_output": (
                "One context-rich technical prompt plus a short mapping showing the "
                "task, context, evidence, desired output, and constraint."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "prompt-context",
                "intent-clarification",
            ],
        },

        {
            "id": "M01.L01.EX03",

            "title": "Design a Safe GenAI Service Flow",

            "lesson_code": "M01.L01",

            "section_id": "service-architecture",

            "placement": "after_section",

            "description": (
                "Apply the service-layer mental model to a GenAI system that can read "
                "private information and perform a controlled action."
            ),

            "instructions": (
                "Design a simple request flow for this scenario:\n\n"
                "A customer asks an AI assistant to check an order and, if it has not "
                "shipped, cancel it.\n\n"
                "Your flow must include:\n"
                "1. Authentication.\n"
                "2. Authorization.\n"
                "3. Order-data retrieval.\n"
                "4. Model interpretation of the request.\n"
                "5. Deterministic validation before cancellation.\n"
                "6. Tool or service execution.\n"
                "7. Final response to the user.\n\n"
                "For each step, state whether the model or trusted application code "
                "should be primarily responsible."
            ),

            "expected_output": (
                "A seven-step architecture flow with a responsibility assignment for "
                "the model versus trusted application code."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "genai-service-architecture",
                "tool-safety",
                "authorization-reasoning",
            ],
        },

        {
            "id": "M01.L01.EX04",

            "title": "Risk Review for a Customer-Facing GenAI Feature",

            "lesson_code": "M01.L01",

            "section_id": "adoption-barriers",

            "placement": "after_section",

            "description": (
                "Identify production risks and connect each risk to an engineering response."
            ),

            "instructions": (
                "Imagine a company wants to add a GenAI assistant that answers customer "
                "questions using account data and company policy documents.\n\n"
                "Create a table with at least five risks. For each risk, include:\n"
                "1. The failure that could occur.\n"
                "2. Why it matters.\n"
                "3. One control or mitigation suggested by the concepts in this lesson.\n\n"
                "Your risks must include hallucination, privacy, authorization, and "
                "at least two additional risks from the lesson."
            ),

            "expected_output": (
                "A risk table containing at least five rows with failure, impact, and "
                "mitigation columns."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "risk-analysis",
                "genai-safety",
                "production-reasoning",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "Introduction to Generative AI Services — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",

                "section_id": "what-is-generative-ai",

                "question": (
                    "Which statement best describes inference in a generative AI system?"
                ),

                "options": [
                    "Collecting the dataset used to train the model",
                    "Using a trained model to produce a new output",
                    "Writing deterministic business rules by hand",
                    "Compressing all application data into a database",
                ],

                "correct": 1,

                "explanation": (
                    "Inference is the stage in which a trained model is used to "
                    "produce an output. Training is the earlier process in which the "
                    "model learns patterns from data."
                ),
            },

            {
                "id": "M01.L01.Q02",

                "section_id": "model-families",

                "question": (
                    "Which model family is described as learning to reverse a "
                    "noise-adding process during generation?"
                ),

                "options": [
                    "GANs",
                    "Autoregressive models",
                    "Diffusion models",
                    "Energy-based models",
                ],

                "correct": 2,

                "explanation": (
                    "Diffusion models learn a denoising process. Generation starts "
                    "from noise and progressively removes it to produce structured data."
                ),
            },

            {
                "id": "M01.L01.Q03",

                "section_id": "latent-space-and-modalities",

                "question": "What is a modality in the context of generative AI?",

                "options": [
                    "A type of data such as text, image, audio, or video",
                    "A permission assigned to an authenticated user",
                    "A database index used for authentication",
                    "A deterministic function used instead of a model",
                ],

                "correct": 0,

                "explanation": (
                    "A modality is a form or type of data. A multimodal model can "
                    "work with more than one such type."
                ),
            },

            {
                "id": "M01.L01.Q04",

                "section_id": "context-rich-prompts",

                "question": (
                    "Why does adding relevant context to a prompt usually improve the response?"
                ),

                "options": [
                    "It guarantees that the model will never hallucinate",
                    "It gives the model less ambiguity about the user's intent",
                    "It converts a probabilistic model into a deterministic function",
                    "It removes the need for application-level validation",
                ],

                "correct": 1,

                "explanation": (
                    "Relevant context narrows the possible interpretations of the "
                    "request. It can improve relevance, but it does not guarantee "
                    "correctness or eliminate hallucinations."
                ),
            },

            {
                "id": "M01.L01.Q05",

                "section_id": "service-architecture",

                "question": (
                    "Which responsibility is best handled by trusted application code "
                    "rather than delegated entirely to the language model?"
                ),

                "options": [
                    "Understanding a user's natural-language wording",
                    "Suggesting a possible interpretation of a request",
                    "Enforcing whether the user is authorized to perform a sensitive action",
                    "Generating a conversational explanation of a retrieved result",
                ],

                "correct": 2,

                "explanation": (
                    "Authorization is a security control and should be enforced by "
                    "trusted application logic. A model may help interpret intent, "
                    "but it should not be the sole authority for privileged actions."
                ),
            },

            {
                "id": "M01.L01.Q06",

                "section_id": "why-fastapi",

                "question": (
                    "What role does FastAPI primarily play in the architecture described "
                    "in this lesson?"
                ),

                "options": [
                    "It trains every generative model from scratch",
                    "It replaces the need for databases and external APIs",
                    "It provides the web service layer that can expose and coordinate model-backed functionality",
                    "It guarantees that every generated answer is factually correct",
                ],

                "correct": 2,

                "explanation": (
                    "FastAPI is used as the backend web-service layer. It helps expose "
                    "APIs and coordinate application logic around the model, but it "
                    "does not itself guarantee model correctness."
                ),
            },

            {
                "id": "M01.L01.Q07",

                "section_id": "adoption-barriers",

                "question": "What is a hallucination in a GenAI system?",

                "options": [
                    "A model taking too long to load",
                    "A generated statement that is plausible-sounding but incorrect or made up",
                    "A user forgetting their authentication token",
                    "A database failing to return a row",
                ],

                "correct": 1,

                "explanation": (
                    "The chapter uses hallucination for generated information that is "
                    "made up or incorrect. This is especially risky when users may "
                    "mistake fluent output for verified fact."
                ),
            },

            {
                "id": "M01.L01.Q08",

                "section_id": "capstone",

                "question": (
                    "Which combination best reflects the capstone service described in the chapter?"
                ),

                "options": [
                    "Only a text chatbot with no storage or external integrations",
                    "A static website that contains prewritten AI explanations",
                    "A multi-model service with RAG, external integrations, conversation storage, authentication, authorization, and guardrails",
                    "A model-training notebook with no API layer",
                ],

                "correct": 2,

                "explanation": (
                    "The capstone combines multiple model types with retrieval, "
                    "external systems, persistence, identity controls, permissions, "
                    "and guardrails."
                ),
            },

            {
                "id": "M01.L01.Q09",

                "section_id": "capstone",

                "type": "open",

                "question": (
                    "Choose one GenAI feature you would add to an existing application. "
                    "Describe the user request, the context the system should gather, "
                    "the model's role, one tool or data source it may need, and two "
                    "controls required before you would trust the feature in production."
                ),
            },
        ],

        "passing_score": 70,
    },
}
