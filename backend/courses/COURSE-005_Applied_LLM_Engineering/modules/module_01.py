"""M01.L01 — An Introduction to Large Language Models.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Chapter 1; page range not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "Language AI and LLM Foundations"

MODULE_DESCRIPTION = (
    "Build an intuitive foundation for Language AI and large language models by "
    "tracing the evolution from bag-of-words and embeddings to attention, "
    "Transformers, BERT, GPT, LLM training, applications, responsible use, "
    "model access, and first text generation."
)

SOURCE_CHAPTER = 1

SOURCE_PAGES = "Page range not provided in supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "An Introduction to Large Language Models",

    "slug": "llm-foundations-m01-l01",

    "description": (
        "A beginner-friendly but substantial introduction to Language AI and "
        "large language models, including representations, attention, "
        "Transformers, BERT versus GPT, training, applications, responsible "
        "use, model access, and a first generation example with Transformers."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 1.85,

    "skill_tags": [
        "language-ai",
        "large-language-models",
        "embeddings",
        "attention",
        "transformers",
        "bert",
        "gpt",
        "llm-training",
        "responsible-ai",
        "hugging-face-transformers",
        "module-01",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # INLINE IMAGE RULES
    # =======================================================================
    #
    # Images are requested inline using [[IMAGE_NEEDED: ...]] placeholders.
    # The course author adds the actual image files manually later.
    # Each request appears immediately after the explanation it supports.
    #
    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "An Introduction to Large Language Models",

        "content": (
            "# An Introduction to Large Language Models\n"
            "\n"
            "> **Course:** Large Language Models Foundations  \n"
            "> **Lesson:** M01.L01  \n"
            "> **Module:** Language AI and LLM Foundations  \n"
            "> **Source alignment:** Chapter 1, “An Introduction to Large Language Models.” Page numbers were not included in the supplied chapter text. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"
            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain what **Language AI** is and how it relates to NLP and large language models.\n"
            "- Describe the progression from **bag-of-words** to **embeddings**, **attention**, and **Transformers**.\n"
            "- Distinguish between **representation models** such as BERT and **generative models** such as GPT.\n"
            "- Explain **pretraining**, **fine-tuning/post-training**, **parameters**, **context length**, and **autoregressive generation** in learner-friendly terms.\n"
            "- Match common Language AI problems to suitable model families and techniques.\n"
            "- Discuss practical concerns including hardware, model access, privacy, bias, reliability, intellectual property, and regulation.\n"
            "- Load a small generative model and tokenizer with Hugging Face Transformers and generate a first response.\n"
            "- Read an LLM system as a set of components rather than treating “the LLM” as one mysterious black box.\n"
            "\n"
            "---\n"
            "\n"
            "## 1. Language AI: the bigger field around LLMs\n"
            "\n"
            "Large language models became widely visible through products such as ChatGPT, but the chapter’s first important idea is that **Language AI is larger than chatbots and larger than LLMs**.\n"
            "\n"
            "Language AI is the part of artificial intelligence concerned with systems that can **understand, process, represent, retrieve, classify, or generate human language**. The chapter notes that this term overlaps strongly with natural language processing (NLP), especially because modern NLP is dominated by machine-learning approaches.\n"
            "\n"
            "A useful mental model is:\n"
            "\n"
            "```text\n"
            "Artificial Intelligence\n"
            "└── Language AI / NLP\n"
            "    ├── Text representation\n"
            "    ├── Classification\n"
            "    ├── Clustering\n"
            "    ├── Semantic search\n"
            "    ├── Retrieval\n"
            "    ├── Translation\n"
            "    ├── Text generation\n"
            "    └── Large language model applications\n"
            "```\n"
            "\n"
            "An LLM therefore belongs inside a broader language-processing ecosystem. A strong LLM application may also depend on a tokenizer, an embedding model, a retrieval system, external documents, tools, or other components.\n"
            "\n"
            "### Why this matters\n"
            "\n"
            "If you think “Language AI = chatbot,” you will miss many useful solutions. A customer-support system, for example, might need:\n"
            "\n"
            "1. an embedding model to represent tickets,\n"
            "2. a clustering method to discover common issue types,\n"
            "3. a retrieval system to fetch relevant documentation, and\n"
            "4. a generative model to write a final answer.\n"
            "\n"
            "The generative model is only one part of the system.\n"
            "\n"
            "[[IMAGE_NEEDED: Language AI landscape | A simple map showing Language AI as the broader field, with branches for representation, classification, clustering, semantic search/retrieval, translation, and generation/LLMs | Learner should notice that LLMs are one important part of Language AI rather than the entire field]]\n"
            "\n"
            "### A short historical perspective\n"
            "\n"
            "The chapter describes a progression in how computers work with language. The recurring problem is simple to state:\n"
            "\n"
            "> Computers need numerical representations, but human language is full of meaning, ambiguity, order, and context.\n"
            "\n"
            "Many major advances in Language AI can be understood as attempts to build better representations of language and better ways to use context.\n"
            "\n"
            "The broad progression in this chapter is:\n"
            "\n"
            "```text\n"
            "Bag-of-words\n"
            "      ↓\n"
            "Dense word embeddings\n"
            "      ↓\n"
            "Sequence models\n"
            "      ↓\n"
            "Attention\n"
            "      ↓\n"
            "Transformer\n"
            "      ↓\n"
            "Encoder-only models (e.g., BERT)\n"
            "and decoder-only models (e.g., GPT)\n"
            "      ↓\n"
            "Modern LLM systems\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Recent history of Language AI | A timeline-style figure showing the progression from bag-of-words to word2vec, sequence models with attention, Transformers, BERT, GPT, and modern LLM systems | Learner should notice that modern LLMs emerged through a sequence of improvements in representation and context handling]]\n"
            "\n"
            "---\n"
            "\n"
            "## 2. From bag-of-words to semantic embeddings\n"
            "\n"
            "Before a model can learn from text, the text needs to become numbers.\n"
            "\n"
            "### 2.1 Bag-of-words: count words, ignore most structure\n"
            "\n"
            "Bag-of-words is a classic way to represent text numerically. The basic process is:\n"
            "\n"
            "1. **Tokenize** the text into words or subwords.\n"
            "2. Build a **vocabulary** containing the unique tokens.\n"
            "3. Count how often each vocabulary item appears in each text.\n"
            "4. Store those counts as a numeric vector.\n"
            "\n"
            "Imagine these two sentences:\n"
            "\n"
            "```text\n"
            "Sentence A: \"cats chase mice\"\n"
            "Sentence B: \"dogs chase cats\"\n"
            "```\n"
            "\n"
            "A possible vocabulary is:\n"
            "\n"
            "```text\n"
            "[cats, chase, mice, dogs]\n"
            "```\n"
            "\n"
            "Then the sentences can be represented as counts:\n"
            "\n"
            "```text\n"
            "Sentence A → [1, 1, 1, 0]\n"
            "Sentence B → [1, 1, 0, 1]\n"
            "```\n"
            "\n"
            "The computer now has numbers it can process.\n"
            "\n"
            "This is valuable because it transforms unstructured text into a structured vector representation. But it has a major limitation: **the representation does not really understand meaning**. It mainly records which words are present and how often they occur.\n"
            "\n"
            "For example, bag-of-words does not naturally capture that two different words can be semantically related. It also throws away much of the sequence information that makes language meaningful.\n"
            "\n"
            "[[IMAGE_NEEDED: Bag-of-words pipeline | A four-stage diagram: two input sentences → tokenization → combined vocabulary → count vectors | Learner should notice that the method converts text into numbers by counting tokens, but does not encode rich meaning or context]]\n"
            "\n"
            "### 2.2 Dense embeddings: represent meaning, not just counts\n"
            "\n"
            "The chapter then introduces **word2vec**, released in 2013, as an influential step toward semantic representations.\n"
            "\n"
            "Instead of representing a word by a long sparse vector of counts, word2vec learns a **dense vector embedding** for each word.\n"
            "\n"
            "An embedding is a vector designed to capture useful properties of the data. In language, the goal is for semantically related words to receive representations that are closer to one another.\n"
            "\n"
            "The key intuition from the chapter is:\n"
            "\n"
            "> Words that tend to appear in similar contexts can learn similar representations.\n"
            "\n"
            "During training, word2vec considers neighboring words. The learned vectors are adjusted so that words appearing in similar surroundings become more similar in the learned space.\n"
            "\n"
            "You can imagine the result conceptually like this:\n"
            "\n"
            "```text\n"
            "Meaning space\n"
            "\n"
            "fruit region:      apple   orange   banana\n"
            "\n"
            "people region:     baby    child    adult\n"
            "\n"
            "place region:      city    village  country\n"
            "```\n"
            "\n"
            "The real embedding dimensions do **not** normally correspond to clean human-readable properties such as “fruitness” or “human-ness.” The chapter uses that kind of explanation only as an intuition. In practice, the dimensions work together in ways that are difficult to interpret individually.\n"
            "\n"
            "### 2.3 Similarity becomes measurable\n"
            "\n"
            "Once text is represented as vectors, we can compare vectors using distance or similarity measures. That allows a system to estimate whether two words—or with other embedding models, two sentences or documents—are semantically related.\n"
            "\n"
            "This idea becomes fundamental later for:\n"
            "\n"
            "- classification,\n"
            "- clustering,\n"
            "- semantic search,\n"
            "- retrieval-augmented generation.\n"
            "\n"
            "[[IMAGE_NEEDED: Semantic embedding space | A 2D conceptual projection with related words grouped close together and unrelated words farther apart | Learner should notice that semantic similarity is represented by geometric closeness, while remembering that real embeddings usually have many dimensions]]\n"
            "\n"
            "### 2.4 Embeddings can represent different levels of text\n"
            "\n"
            "Not all embeddings represent single words.\n"
            "\n"
            "The chapter distinguishes examples such as:\n"
            "\n"
            "- **word embeddings** — one vector per word,\n"
            "- **sentence embeddings** — one vector for a sentence,\n"
            "- **document-level representations** — one vector or representation for a larger document.\n"
            "\n"
            "The important principle is that the *unit being represented* can change.\n"
            "\n"
            "---\n"
            "\n"
            "## 3. Context, sequence, attention, and the Transformer\n"
            "\n"
            "Dense embeddings improved semantic representation, but early word embeddings such as word2vec are **static**.\n"
            "\n"
            "That creates a problem with ambiguous words.\n"
            "\n"
            "Consider:\n"
            "\n"
            "```text\n"
            "\"I deposited money at the bank.\"\n"
            "\"I sat on the bank of the river.\"\n"
            "```\n"
            "\n"
            "The word `bank` has a different meaning in each sentence. A static word embedding gives the word the same stored representation in both cases.\n"
            "\n"
            "Language models therefore need a way to use **context**.\n"
            "\n"
            "### 3.1 Sequence models: encode then decode\n"
            "\n"
            "The chapter introduces recurrent neural networks (RNNs) as an important step in processing sequences.\n"
            "\n"
            "For translation, a classic sequence-to-sequence system uses:\n"
            "\n"
            "- an **encoder** to process the input sentence,\n"
            "- a **decoder** to generate the output sentence.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "English input\n"
            "\"I love llamas\"\n"
            "      ↓\n"
            "    Encoder\n"
            "      ↓\n"
            "context representation\n"
            "      ↓\n"
            "    Decoder\n"
            "      ↓\n"
            "Dutch output\n"
            "\"Ik hou van lama's\"\n"
            "```\n"
            "\n"
            "Generation is **autoregressive**: when producing the next output token, the system uses what it has already generated.\n"
            "\n"
            "A simplified view is:\n"
            "\n"
            "```text\n"
            "Generate token 1\n"
            "      ↓\n"
            "Use token 1 to help generate token 2\n"
            "      ↓\n"
            "Use tokens 1–2 to help generate token 3\n"
            "      ↓\n"
            "...\n"
            "```\n"
            "\n"
            "### 3.2 The bottleneck: one context representation\n"
            "\n"
            "A simple encoder-decoder approach may compress the input sequence into one context representation. The chapter explains that this becomes difficult for longer sentences because a single representation must carry all relevant information.\n"
            "\n"
            "### 3.3 Attention: focus on the relevant parts\n"
            "\n"
            "Attention improves this process by allowing the model to give different importance to different input positions.\n"
            "\n"
            "During translation, when the decoder is generating the translated form of “llamas,” it should focus strongly on the input word “llamas” and much less on unrelated input words.\n"
            "\n"
            "That is the central intuition:\n"
            "\n"
            "> **Attention lets the model decide which parts of the sequence matter most for the current computation.**\n"
            "\n"
            "[[IMAGE_NEEDED: Attention in translation | An encoder-decoder translation diagram with visible attention links between source and target words, including a strong link between “llamas” and its translated form | Learner should notice that the decoder can focus on the most relevant source token instead of relying only on one compressed context vector]]\n"
            "\n"
            "### 3.4 The Transformer: attention becomes the main architecture\n"
            "\n"
            "The 2017 Transformer architecture made attention the central mechanism and removed recurrence.\n"
            "\n"
            "The chapter emphasizes a practical advantage: compared with recurrent processing, Transformer training can process sequence positions more in parallel, which greatly improves training efficiency.\n"
            "\n"
            "The original Transformer contains:\n"
            "\n"
            "```text\n"
            "Encoder stack → represents the input\n"
            "Decoder stack → generates the output\n"
            "```\n"
            "\n"
            "Inside an encoder block, the chapter highlights:\n"
            "\n"
            "1. **self-attention**\n"
            "2. a **feedforward neural network**\n"
            "\n"
            "Self-attention allows positions in the same sequence to interact with one another.\n"
            "\n"
            "A simple intuition:\n"
            "\n"
            "```text\n"
            "\"The animal didn't cross the street because it was tired.\"\n"
            "\n"
            "To understand \"it\",\n"
            "the model can relate that position to other positions in the sentence.\n"
            "```\n"
            "\n"
            "The example above is an explanatory analogy; the source chapter’s main point is that self-attention can look across positions in the sequence rather than processing only one token at a time.\n"
            "\n"
            "### 3.5 Why the decoder masks the future\n"
            "\n"
            "During text generation, the model should not “peek” at future tokens that it is supposed to predict.\n"
            "\n"
            "So decoder self-attention masks future positions.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Current position can use:\n"
            "token 1 ✓\n"
            "token 2 ✓\n"
            "token 3 ✓\n"
            "future token 4 ✗\n"
            "future token 5 ✗\n"
            "```\n"
            "\n"
            "This preserves the autoregressive generation process.\n"
            "\n"
            "[[IMAGE_NEEDED: Transformer encoder-decoder mental model | A simplified Transformer diagram with stacked encoder blocks on the left, stacked decoder blocks on the right, self-attention inside both, encoder-to-decoder attention, and a mask over future decoder positions | Learner should notice the difference between encoding the full input and autoregressively generating output without looking ahead]]\n"
            "\n"
            "---\n"
            "\n"
            "## 4. Two major Transformer families: representation and generation\n"
            "\n"
            "Once the Transformer existed, researchers could keep only the parts needed for a task.\n"
            "\n"
            "The chapter focuses on two highly influential families.\n"
            "\n"
            "### 4.1 Encoder-only models: represent language\n"
            "\n"
            "BERT, introduced in 2018, uses the **encoder** side of the Transformer.\n"
            "\n"
            "Its main strength is representation.\n"
            "\n"
            "The chapter describes BERT as learning contextual representations and being useful for tasks such as:\n"
            "\n"
            "- classification,\n"
            "- clustering,\n"
            "- semantic search,\n"
            "- feature extraction.\n"
            "\n"
            "BERT training uses **masked language modeling**: part of the input is hidden, and the model learns to predict what is missing.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Input:\n"
            "\"The cat sat on the [MASK].\"\n"
            "\n"
            "Training target:\n"
            "\"mat\"\n"
            "```\n"
            "\n"
            "By repeatedly solving this kind of task across large text corpora, the model learns representations that capture context.\n"
            "\n"
            "The chapter also discusses the `[CLS]` classification token, which can serve as a representation of the overall input when adapting BERT to classification tasks.\n"
            "\n"
            "### 4.2 Pretraining then fine-tuning\n"
            "\n"
            "A major benefit of BERT-like pretrained models is that a large amount of general language learning happens before you work on your own task.\n"
            "\n"
            "Then you can adapt the pretrained model to a narrower problem.\n"
            "\n"
            "```text\n"
            "Large general text corpus\n"
            "        ↓\n"
            "     Pretraining\n"
            "        ↓\n"
            "Pretrained language model\n"
            "        ↓\n"
            " Fine-tuning on your task\n"
            "        ↓\n"
            "Task-specific model\n"
            "```\n"
            "\n"
            "This is **transfer learning**: reuse general knowledge learned during pretraining instead of starting from zero.\n"
            "\n"
            "### 4.3 Decoder-only models: generate language\n"
            "\n"
            "GPT-1, also introduced in 2018, uses a **decoder-only** Transformer architecture.\n"
            "\n"
            "Its primary strength is generation.\n"
            "\n"
            "A generative model receives text and predicts a continuation. With additional training to follow instructions, it can behave like a conversational assistant.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Prompt:\n"
            "\"Explain embeddings in one sentence.\"\n"
            "\n"
            "Model:\n"
            "predict next token → then next token → then next token → ...\n"
            "```\n"
            "\n"
            "This is why generative models are often described as **completion models**.\n"
            "\n"
            "### 4.4 Parameters and scaling\n"
            "\n"
            "The chapter gives the historical progression:\n"
            "\n"
            "- GPT-1: 117 million parameters,\n"
            "- GPT-2: 1.5 billion parameters,\n"
            "- GPT-3: 175 billion parameters.\n"
            "\n"
            "A **parameter** is a learned numerical value inside the model. Collectively, parameters encode what the training process has learned.\n"
            "\n"
            "The chapter uses this growth to illustrate the rapid increase in model scale.\n"
            "\n"
            "### 4.5 Context length\n"
            "\n"
            "A generative model cannot process unlimited text at once.\n"
            "\n"
            "The **context length** or **context window** is the maximum number of tokens the model can handle in its active context.\n"
            "\n"
            "If the model has a larger context window, more text can potentially be included at once.\n"
            "\n"
            "Because generation is autoregressive, newly generated tokens also become part of the growing context.\n"
            "\n"
            "### 4.6 Representation model vs generative model\n"
            "\n"
            "A practical comparison:\n"
            "\n"
            "| Question | Representation model | Generative model |\n"
            "|---|---|---|\n"
            "| Main goal | Represent/understand text | Generate text |\n"
            "| Typical architecture in this chapter | Encoder-only | Decoder-only |\n"
            "| Example | BERT | GPT |\n"
            "| Common output | Embedding, class features, scores | Tokens/text |\n"
            "| Useful for | Classification, clustering, semantic search | Completion, instruction following, chat |\n"
            "\n"
            "The chapter uses the terms **representation models** and **generative models** as a useful distinction, while also noting that the definition of “large language model” is not fixed forever.\n"
            "\n"
            "[[IMAGE_NEEDED: BERT versus GPT architecture | A side-by-side conceptual diagram showing BERT as an encoder-only stack producing representations and GPT as a decoder-only stack producing text token by token | Learner should notice that both are Transformer-based but optimized for different primary roles]]\n"
            "\n"
            "{{exercise:M01.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"
            "## 5. What counts as a “large language model”?\n"
            "\n"
            "The phrase **large language model** sounds precise, but the chapter argues that its definition moves over time.\n"
            "\n"
            "Why?\n"
            "\n"
            "Because “large” is relative.\n"
            "\n"
            "A model considered huge in one period may later look small. A smaller model may also become very capable through better architecture, training, or data.\n"
            "\n"
            "The chapter deliberately uses a broad definition. It includes not only very large generative decoder-only systems, but also smaller models and representation models when they are important to the Language AI ecosystem.\n"
            "\n"
            "The practical lesson is:\n"
            "\n"
            "> Do not let the label decide what a model can do. Look at the model’s actual behavior, architecture, training, outputs, and use case.\n"
            "\n"
            "### Foundation/base models\n"
            "\n"
            "The chapter uses **foundation model** or **base model** for a model after broad pretraining.\n"
            "\n"
            "A base model has learned language patterns but may not yet be trained to follow human instructions well.\n"
            "\n"
            "An **instruct** or **chat** model is further adapted to follow directions and participate in conversations.\n"
            "\n"
            "A simple progression is:\n"
            "\n"
            "```text\n"
            "Raw large text corpus\n"
            "        ↓\n"
            "Language-model pretraining\n"
            "        ↓\n"
            "Base / foundation model\n"
            "        ↓\n"
            "Fine-tuning or post-training\n"
            "        ↓\n"
            "Instruct / chat / task-adapted model\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: LLM training paradigm | A two-stage diagram contrasting traditional one-step task training with LLM pretraining on broad text followed by fine-tuning/post-training for a narrower task or instruction following | Learner should notice that expensive general pretraining is reused, while adaptation happens afterward]]\n"
            "\n"
            "---\n"
            "\n"
            "## 6. What can LLM systems actually do?\n"
            "\n"
            "The chapter gives several examples that are useful because they show that not every problem should be solved by the same type of model.\n"
            "\n"
            "### 6.1 Sentiment classification\n"
            "\n"
            "Problem:\n"
            "\n"
            "```text\n"
            "Input: \"The delivery was fast and the product is excellent.\"\n"
            "Output: Positive\n"
            "```\n"
            "\n"
            "This is a classification problem.\n"
            "\n"
            "According to the chapter, both encoder-only and decoder-only models can be used, either through pretrained models or through task-specific fine-tuning.\n"
            "\n"
            "### 6.2 Discovering common topics in support tickets\n"
            "\n"
            "Suppose you have thousands of ticket messages but no predefined labels.\n"
            "\n"
            "You might use representation models to group similar tickets and a generative model to help label or describe the discovered topics.\n"
            "\n"
            "The system might produce groups such as:\n"
            "\n"
            "```text\n"
            "Cluster A → login problems\n"
            "Cluster B → payment failures\n"
            "Cluster C → delivery questions\n"
            "```\n"
            "\n"
            "The important lesson is that one application can combine multiple model types.\n"
            "\n"
            "### 6.3 Semantic search and document retrieval\n"
            "\n"
            "Keyword search looks for literal word overlap.\n"
            "\n"
            "Semantic search uses embeddings to retrieve text that is close in meaning.\n"
            "\n"
            "That becomes useful when an LLM needs external information.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "User question\n"
            "      ↓\n"
            "Embedding / retrieval system\n"
            "      ↓\n"
            "Relevant documents\n"
            "      ↓\n"
            "Generative LLM\n"
            "      ↓\n"
            "Answer using retrieved context\n"
            "```\n"
            "\n"
            "This idea is a foundation for **retrieval-augmented generation (RAG)**, which the chapter points to for later study.\n"
            "\n"
            "### 6.4 LLM chatbot with tools and documents\n"
            "\n"
            "A useful chatbot may combine:\n"
            "\n"
            "- prompt engineering,\n"
            "- retrieval,\n"
            "- external tools,\n"
            "- fine-tuning,\n"
            "- a generative model.\n"
            "\n"
            "This is another reminder that an LLM application is often a **system**, not a single model.\n"
            "\n"
            "### 6.5 Multimodal tasks\n"
            "\n"
            "The chapter also mentions systems that combine language with other modalities such as images.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Input:\n"
            "photo of ingredients in a refrigerator\n"
            "\n"
            "Possible task:\n"
            "generate a recipe based on what is visible\n"
            "```\n"
            "\n"
            "This expands the concept from pure text processing to multimodal AI.\n"
            "\n"
            "---\n"
            "\n"
            "## 7. Responsible LLM development is part of the engineering\n"
            "\n"
            "The chapter treats responsible use as a core part of working with LLMs, not an optional extra.\n"
            "\n"
            "### 7.1 Bias and fairness\n"
            "\n"
            "Training data may contain social or historical biases.\n"
            "\n"
            "A model can learn these patterns and reproduce or amplify them.\n"
            "\n"
            "The chapter also points out a practical challenge: training datasets are often not fully available to users, so it may be difficult to know exactly which biases are present.\n"
            "\n"
            "### 7.2 Transparency and accountability\n"
            "\n"
            "LLM output can look convincingly human.\n"
            "\n"
            "That creates questions such as:\n"
            "\n"
            "- Does the user know they are interacting with an AI system?\n"
            "- Is a human reviewing high-impact decisions?\n"
            "- Who is responsible when the system causes harm?\n"
            "\n"
            "The chapter uses medical applications as an example of a setting where these questions are especially important.\n"
            "\n"
            "### 7.3 Incorrect or harmful generation\n"
            "\n"
            "A language model does not automatically produce ground truth.\n"
            "\n"
            "It may output incorrect information confidently.\n"
            "\n"
            "So fluent language should never be treated as proof of correctness.\n"
            "\n"
            "A strong engineering habit is:\n"
            "\n"
            "```text\n"
            "Fluent output ≠ verified output\n"
            "```\n"
            "\n"
            "### 7.4 Intellectual property\n"
            "\n"
            "The chapter raises open questions about ownership and similarity to training data.\n"
            "\n"
            "The key learner takeaway is not that there is one simple answer, but that LLM applications can create intellectual-property concerns that need to be considered.\n"
            "\n"
            "### 7.5 Regulation\n"
            "\n"
            "The chapter notes that governments have begun regulating AI and foundation-model applications. Regulation can affect how systems are developed and deployed.\n"
            "\n"
            "Because regulation changes over time, treat the chapter’s named regulatory examples as a snapshot of the source at the time it was written.\n"
            "\n"
            "### A practical responsibility checklist\n"
            "\n"
            "Before deploying an LLM feature, ask:\n"
            "\n"
            "```text\n"
            "1. What data goes into the system?\n"
            "2. Could the data contain sensitive information?\n"
            "3. Can the output be wrong in a harmful way?\n"
            "4. Is human review needed?\n"
            "5. Could the model reproduce unfair patterns?\n"
            "6. Do users know they are interacting with AI?\n"
            "7. Are there legal, licensing, or regulatory constraints?\n"
            "```\n"
            "\n"
            "This checklist is an instructor-authored study aid derived from the chapter’s responsible-use themes.\n"
            "\n"
            "---\n"
            "\n"
            "## 8. How we access LLMs: hosted proprietary models vs open models\n"
            "\n"
            "The chapter presents two major ways to work with language models.\n"
            "\n"
            "### 8.1 Proprietary/private models through an API\n"
            "\n"
            "A proprietary model does not expose its full weights and architecture publicly.\n"
            "\n"
            "You generally interact with it through an **API**.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "Your application\n"
            "      ↓ request\n"
            "Provider API\n"
            "      ↓\n"
            "Hosted model\n"
            "      ↓ response\n"
            "Your application\n"
            "```\n"
            "\n"
            "Advantages discussed in the chapter include:\n"
            "\n"
            "- you do not need to host the model yourself,\n"
            "- you do not need a powerful local GPU just to run inference,\n"
            "- setup is easier,\n"
            "- the provider handles infrastructure.\n"
            "\n"
            "Trade-offs discussed include:\n"
            "\n"
            "- usage can cost money,\n"
            "- you have less direct control over the model,\n"
            "- self-hosting and direct access may not be possible,\n"
            "- data is sent to the provider, which can matter for sensitive workloads.\n"
            "\n"
            "### 8.2 Open models\n"
            "\n"
            "Open models make model weights and architecture available to users under their respective licenses.\n"
            "\n"
            "The chapter emphasizes that licenses differ, and that “open model” and “open source” can be debated terms because code, data, weights, or commercial permissions may not all be available in the same way.\n"
            "\n"
            "With an open model, you may be able to:\n"
            "\n"
            "- download it,\n"
            "- run it locally,\n"
            "- inspect more of the system,\n"
            "- fine-tune it,\n"
            "- keep sensitive data on your own infrastructure.\n"
            "\n"
            "The trade-off is that local execution requires suitable hardware and more technical setup.\n"
            "\n"
            "[[IMAGE_NEEDED: Hosted API versus local open model | A side-by-side diagram: application → external provider API → hosted proprietary model, versus application → locally hosted open model on user hardware | Learner should notice the trade-off between convenience/provider-managed compute and local control/privacy/hardware responsibility]]\n"
            "\n"
            "### 8.3 Hardware and VRAM\n"
            "\n"
            "The chapter repeatedly emphasizes GPU memory.\n"
            "\n"
            "**VRAM** is memory available on the GPU.\n"
            "\n"
            "Whether a model fits depends on several factors, including:\n"
            "\n"
            "- model size,\n"
            "- architecture,\n"
            "- compression/quantization,\n"
            "- context size,\n"
            "- software backend.\n"
            "\n"
            "The chapter therefore warns that there is no one universal VRAM rule for every model.\n"
            "\n"
            "It also frames the book around learners with limited compute resources and uses smaller models and hosted notebook environments to keep experiments accessible.\n"
            "\n"
            "### 8.4 Frameworks are tools, not the foundation\n"
            "\n"
            "The chapter mentions tools such as:\n"
            "\n"
            "- Hugging Face Transformers,\n"
            "- llama.cpp,\n"
            "- LangChain,\n"
            "- local chat interfaces such as LM Studio and related tools.\n"
            "\n"
            "But its teaching goal is not to memorize every framework.\n"
            "\n"
            "The stronger goal is to understand the recurring concepts so that learning another framework becomes easier.\n"
            "\n"
            "---\n"
            "\n"
            "## 9. Generate your first text with Transformers\n"
            "\n"
            "The chapter ends with a practical example using **Phi-3-mini**.\n"
            "\n"
            "The most important system insight is that when you use a generative language model, you normally need at least:\n"
            "\n"
            "1. the **model**,\n"
            "2. its **tokenizer**.\n"
            "\n"
            "### 9.1 Why the tokenizer is separate\n"
            "\n"
            "The tokenizer converts input text into tokens that the model can process.\n"
            "\n"
            "Think of the flow as:\n"
            "\n"
            "```text\n"
            "Human text\n"
            "   ↓\n"
            "Tokenizer\n"
            "   ↓\n"
            "Token IDs\n"
            "   ↓\n"
            "Generative model\n"
            "   ↓\n"
            "Generated token IDs\n"
            "   ↓\n"
            "Tokenizer decoding\n"
            "   ↓\n"
            "Human-readable text\n"
            "```\n"
            "\n"
            "The chapter will study tokenization more deeply later, but you already need to recognize its role.\n"
            "\n"
            "### 9.2 Load the model and tokenizer\n"
            "\n"
            "The source chapter uses this model identifier:\n"
            "\n"
            "```text\n"
            "microsoft/Phi-3-mini-4k-instruct\n"
            "```\n"
            "\n"
            "Its example loads the model and tokenizer with Hugging Face Transformers:\n"
            "\n"
            "```python\n"
            "from transformers import AutoModelForCausalLM, AutoTokenizer\n"
            "\n"
            "model = AutoModelForCausalLM.from_pretrained(\n"
            "    \"microsoft/Phi-3-mini-4k-instruct\",\n"
            "    device_map=\"cuda\",\n"
            "    torch_dtype=\"auto\",\n"
            "    trust_remote_code=True,\n"
            ")\n"
            "\n"
            "tokenizer = AutoTokenizer.from_pretrained(\n"
            "    \"microsoft/Phi-3-mini-4k-instruct\"\n"
            ")\n"
            "```\n"
            "\n"
            "### What each important piece means\n"
            "\n"
            "`AutoModelForCausalLM`\n"
            "\n"
            "- loads a model designed for causal/autoregressive language generation.\n"
            "\n"
            "`AutoTokenizer`\n"
            "\n"
            "- loads the tokenizer associated with the model.\n"
            "\n"
            "`device_map=\"cuda\"`\n"
            "\n"
            "- the chapter assumes an NVIDIA GPU and places the model on CUDA.\n"
            "\n"
            "`torch_dtype=\"auto\"`\n"
            "\n"
            "- lets the loading process choose an appropriate tensor type automatically.\n"
            "\n"
            "`trust_remote_code=True`\n"
            "\n"
            "- allows model-specific code supplied by the model repository to be used. In real projects, this setting deserves conscious trust and security review before enabling it.\n"
            "\n"
            "The last sentence is an instructor-authored safety note about the meaning of the setting; the source example itself enables the option.\n"
            "\n"
            "### 9.3 Build a generation pipeline\n"
            "\n"
            "The chapter then uses `pipeline` to bundle the model, tokenizer, and generation process:\n"
            "\n"
            "```python\n"
            "from transformers import pipeline\n"
            "\n"
            "generator = pipeline(\n"
            "    \"text-generation\",\n"
            "    model=model,\n"
            "    tokenizer=tokenizer,\n"
            "    return_full_text=False,\n"
            "    max_new_tokens=500,\n"
            "    do_sample=False,\n"
            ")\n"
            "```\n"
            "\n"
            "Three parameters are especially important in the chapter:\n"
            "\n"
            "#### `return_full_text=False`\n"
            "\n"
            "Return only the newly generated output rather than repeating the original prompt.\n"
            "\n"
            "#### `max_new_tokens=500`\n"
            "\n"
            "Limit the number of newly generated tokens.\n"
            "\n"
            "This prevents uncontrolled generation from continuing too long.\n"
            "\n"
            "#### `do_sample=False`\n"
            "\n"
            "Disable sampling.\n"
            "\n"
            "The chapter explains that this makes generation choose the most probable next token rather than sampling from alternatives.\n"
            "\n"
            "Later sampling settings can make outputs more varied or creative.\n"
            "\n"
            "### 9.4 Send a chat-style message\n"
            "\n"
            "The prompt is represented as a list of dictionaries:\n"
            "\n"
            "```python\n"
            "messages = [\n"
            "    {\n"
            "        \"role\": \"user\",\n"
            "        \"content\": \"Create a funny joke about chickens.\",\n"
            "    }\n"
            "]\n"
            "```\n"
            "\n"
            "Then generate:\n"
            "\n"
            "```python\n"
            "output = generator(messages)\n"
            "print(output[0][\"generated_text\"])\n"
            "```\n"
            "\n"
            "The exact generated wording may vary across model/software conditions, but the important learning target is the pipeline:\n"
            "\n"
            "```text\n"
            "message\n"
            "  ↓\n"
            "tokenizer\n"
            "  ↓\n"
            "model\n"
            "  ↓\n"
            "generation settings\n"
            "  ↓\n"
            "generated text\n"
            "```\n"
            "\n"
            "### 9.5 Read the code as a system\n"
            "\n"
            "Do not memorize the lines mechanically.\n"
            "\n"
            "Instead, be able to answer:\n"
            "\n"
            "- Which object converts text into tokens?\n"
            "- Which object contains the learned model parameters?\n"
            "- Which component organizes generation?\n"
            "- Which setting limits output length?\n"
            "- Which setting controls whether sampling is used?\n"
            "- Where does the user prompt enter the system?\n"
            "\n"
            "If you can answer those questions, you understand the example rather than merely copying it.\n"
            "\n"
            "{{exercise:M01.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"
            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> “An LLM is basically the same thing as a chatbot.”\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A chatbot is an application or interaction style. An LLM is a model. A chatbot may contain an LLM plus retrieval, tools, conversation management, safety layers, and other components.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> “Embeddings store human-readable concepts in each individual dimension.”\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The chapter explicitly warns that this is only an intuition. Real embedding dimensions are usually not clean, individually interpretable concepts. Meaning emerges from the vector as a whole.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> “BERT and GPT are the same because both use Transformers.”\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "They are both Transformer-based, but the chapter emphasizes different architectures and primary goals: BERT is encoder-only and representation-focused, while GPT is decoder-only and generation-focused.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> “If an LLM answers confidently, the answer must be correct.”\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The chapter states that LLMs can confidently generate incorrect information. Fluency is not verification.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> “More model parameters automatically tell me whether a model is useful for my task.”\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The chapter uses parameter growth to explain scaling, but it also argues that labels such as “large” are moving targets. Practical usefulness depends on what the model does, how it was trained, and the task you need to solve.\n"
            "\n"
            "---\n"
            "\n"
            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Artificial intelligence (AI) | Computer systems designed to perform tasks associated with intelligent behavior. |\n"
            "| Language AI | The AI subfield focused on understanding, processing, representing, and generating human language. |\n"
            "| NLP | Natural language processing; closely related to what the chapter calls Language AI. |\n"
            "| Token | A unit of text processed by a language model, such as a word, subword, or other text fragment depending on the tokenizer. |\n"
            "| Tokenization | Splitting or converting text into tokens for model processing. |\n"
            "| Vocabulary | The set of token units used by a representation or tokenizer. |\n"
            "| Bag-of-words | A text representation based mainly on token occurrence/counts. |\n"
            "| Vector | An ordered list of numeric values. |\n"
            "| Embedding | A vector representation intended to capture useful meaning or properties of data. |\n"
            "| Semantic similarity | Similarity based on meaning rather than only exact word overlap. |\n"
            "| Neural network | A layered computational model with learned weighted connections. |\n"
            "| Parameter | A numerical value learned by a model during training. |\n"
            "| RNN | Recurrent neural network; a neural architecture designed to process sequences. |\n"
            "| Encoder | A component focused on converting input into useful internal representations. |\n"
            "| Decoder | A component focused on generating an output sequence. |\n"
            "| Autoregressive generation | Generating a sequence step by step while conditioning on earlier generated tokens. |\n"
            "| Attention | A mechanism that lets a model weight which parts of a sequence are most relevant. |\n"
            "| Self-attention | Attention among positions within the same sequence. |\n"
            "| Transformer | An architecture centered on attention rather than recurrence. |\n"
            "| BERT | An influential encoder-only Transformer model focused on contextual representation. |\n"
            "| Masked language modeling | A training task where hidden parts of the input are predicted. |\n"
            "| GPT | A family of decoder-only Generative Pre-trained Transformers focused on generation. |\n"
            "| Representation model | A model used mainly to encode language into useful representations such as embeddings. |\n"
            "| Generative model | A model used mainly to generate text or other outputs. |\n"
            "| Pretraining | Broad initial training, usually on a large corpus, before task-specific adaptation. |\n"
            "| Foundation/base model | A broadly pretrained model before or apart from narrower task adaptation. |\n"
            "| Fine-tuning | Additional training that adapts a pretrained model to a specific task or behavior. |\n"
            "| Context window | The maximum active token context the model can process. |\n"
            "| Semantic search | Retrieval based on meaning, often using embedding similarity. |\n"
            "| RAG | Retrieval-augmented generation: combining retrieval of external information with generation. |\n"
            "| API | An interface through which software communicates with another service or system. |\n"
            "| VRAM | GPU memory available for storing and processing model data. |\n"
            "| Quantization | A model-compression approach mentioned by the chapter for reducing resource needs. |\n"
            "\n"
            "---\n"
            "\n"
            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer these without looking back:\n"
            "\n"
            "1. Why does Language AI include more than generative LLMs?\n"
            "2. What information does bag-of-words preserve, and what important information does it lose?\n"
            "3. Why are dense embeddings more useful for semantic similarity than raw word counts?\n"
            "4. Why is a static word embedding insufficient for a word such as “bank”?\n"
            "5. What problem did attention address in sequence-to-sequence models?\n"
            "6. Why can Transformer training be more parallel than recurrent processing?\n"
            "7. What is the main role of an encoder-only model such as BERT?\n"
            "8. What is the main role of a decoder-only model such as GPT?\n"
            "9. What does “autoregressive” mean during text generation?\n"
            "10. What is the difference between a base/foundation model and an instruct/chat model?\n"
            "11. Give one example where an embedding model and a generative model could be used together.\n"
            "12. Why should fluent LLM output not automatically be treated as factual?\n"
            "13. What is one advantage and one trade-off of using a hosted proprietary model?\n"
            "14. What is one advantage and one trade-off of running an open model locally?\n"
            "15. In the Phi-3 example, what jobs are performed by the tokenizer, model, and generation pipeline?\n"
            "\n"
            "---\n"
            "\n"
            "## Retain this idea\n"
            "\n"
            "**Modern Language AI is best understood as an evolution of representations and context handling: we moved from counting words, to learning semantic vectors, to using attention and Transformers, and then specialized those Transformers into representation-focused and generation-focused models. Real LLM applications combine these models with tokenizers, retrieval, tools, infrastructure, and responsible engineering choices.**\n"
        ),

        "estimated_minutes": 110,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "language-ai",
                "title": "Language AI: the bigger field around LLMs",
                "order": 1,
            },
            {
                "id": "representations",
                "title": "From bag-of-words to semantic embeddings",
                "order": 2,
            },
            {
                "id": "attention-transformers",
                "title": "Context, sequence, attention, and the Transformer",
                "order": 3,
            },
            {
                "id": "model-families",
                "title": "Two major Transformer families: representation and generation",
                "order": 4,
            },
            {
                "id": "what-is-an-llm",
                "title": "What counts as a large language model?",
                "order": 5,
            },
            {
                "id": "applications",
                "title": "What can LLM systems actually do?",
                "order": 6,
            },
            {
                "id": "responsible-use",
                "title": "Responsible LLM development is part of the engineering",
                "order": 7,
            },
            {
                "id": "using-models",
                "title": "How we access LLMs: hosted proprietary models vs open models",
                "order": 8,
            },
            {
                "id": "first-generation",
                "title": "Generate your first text with Transformers",
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

            "title": "Trace the Evolution of Language Representations",

            "lesson_code": "M01.L01",

            "section_id": "model-families",

            "placement": "after_section",

            "description": (
                "Build a mental model of how Language AI progressed from simple "
                "count-based representations to contextual Transformer models."
            ),

            "instructions": (
                "1. Create a table with these rows: bag-of-words, word2vec, "
                "RNN encoder-decoder, attention, Transformer, BERT, and GPT.\n"
                "2. For each row, write what the method/model primarily adds "
                "compared with the previous stage.\n"
                "3. Mark whether the representation is mainly static or contextual "
                "where that distinction makes sense.\n"
                "4. For BERT and GPT, state the primary architecture family and "
                "main role described in the lesson.\n"
                "5. Finish with 3-5 sentences explaining why attention and the "
                "Transformer were major turning points."
            ),

            "expected_output": (
                "A comparison table covering all seven stages plus a concise "
                "written explanation of the progression."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "language-representation",
                "attention",
                "transformer-architecture",
                "bert-vs-gpt",
                "conceptual-reasoning",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Read and Explain a First LLM Generation Pipeline",

            "lesson_code": "M01.L01",

            "section_id": "first-generation",

            "placement": "after_section",

            "description": (
                "Use the Phi-3 example from the chapter to demonstrate that you "
                "understand the role of the tokenizer, model, pipeline, prompt, "
                "and generation settings."
            ),

            "instructions": (
                "1. Copy the model/tokenizer and pipeline code from the lesson "
                "into a notebook or Python file.\n"
                "2. Label the line that loads the model and the line that loads "
                "the tokenizer.\n"
                "3. In your own words, explain return_full_text, max_new_tokens, "
                "and do_sample.\n"
                "4. Replace the chicken-joke prompt with a short educational "
                "prompt of your choice.\n"
                "5. If you have suitable hardware or a compatible notebook "
                "environment, run it and record the output. If you cannot run it, "
                "trace the expected data flow from prompt to generated text.\n"
                "6. Identify one practical concern from this lesson that matters "
                "before using a model in a real application."
            ),

            "expected_output": (
                "An annotated code snippet or notebook, a short explanation of "
                "the generation parameters, the changed prompt, optional runtime "
                "output, and one practical deployment/responsibility note."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "tokenizer-role",
                "model-loading",
                "text-generation",
                "generation-parameters",
                "llm-system-thinking",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "An Introduction to Large Language Models — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",
                "section_id": "language-ai",
                "question": (
                    "Which statement best matches the chapter's view of Language AI?"
                ),
                "options": [
                    "It refers only to chatbots built with very large models.",
                    "It is the broader field of technologies for understanding, processing, representing, and generating human language.",
                    "It is another name only for decoder-only Transformers.",
                    "It refers only to rule-based language systems.",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter treats Language AI as the broader field. LLMs, "
                    "retrieval systems, representation models, and other language "
                    "technologies can all contribute to it."
                ),
            },

            {
                "id": "M01.L01.Q02",
                "section_id": "representations",
                "question": (
                    "What is the main weakness of bag-of-words emphasized in the lesson?"
                ),
                "options": [
                    "It cannot convert text into numbers.",
                    "It requires a GPU for every sentence.",
                    "It largely ignores semantic meaning and rich context.",
                    "It can only represent images.",
                ],
                "correct": 2,
                "explanation": (
                    "Bag-of-words is useful precisely because it converts text to "
                    "numeric vectors, but it mainly records token occurrence/counts "
                    "and does not capture meaning and context well."
                ),
            },

            {
                "id": "M01.L01.Q03",
                "section_id": "attention-transformers",
                "question": (
                    "What is the core intuition behind attention?"
                ),
                "options": [
                    "The model gives different importance to different sequence positions depending on what is relevant.",
                    "The model permanently removes all earlier tokens.",
                    "The model converts every word into the same vector.",
                    "The model avoids using context.",
                ],
                "correct": 0,
                "explanation": (
                    "Attention allows the model to focus more strongly on sequence "
                    "positions that are relevant to the current computation."
                ),
            },

            {
                "id": "M01.L01.Q04",
                "section_id": "model-families",
                "question": (
                    "Which pairing best matches the primary roles used in the chapter?"
                ),
                "options": [
                    "BERT: decoder-only generation; GPT: encoder-only representation",
                    "BERT: bag-of-words retrieval; GPT: static word embeddings",
                    "BERT: image generation; GPT: clustering only",
                    "BERT: encoder-only representation; GPT: decoder-only generation",
                ],
                "correct": 3,
                "explanation": (
                    "The lesson follows the chapter's distinction: BERT-like "
                    "encoder-only models are representation-focused, while GPT-like "
                    "decoder-only models are generation-focused."
                ),
            },

            {
                "id": "M01.L01.Q05",
                "section_id": "what-is-an-llm",
                "question": (
                    "Why does the chapter avoid using a rigid parameter threshold to define an LLM?"
                ),
                "options": [
                    "Because parameters are unrelated to neural networks.",
                    "Because what counts as 'large' changes over time and capability is not captured by one fixed size boundary.",
                    "Because every language model has exactly the same number of parameters.",
                    "Because only tokenizers have parameters.",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter treats 'large' as a moving and somewhat arbitrary "
                    "term, so it focuses on model behavior and role rather than a "
                    "single permanent parameter cutoff."
                ),
            },

            {
                "id": "M01.L01.Q06",
                "section_id": "applications",
                "question": (
                    "Which example best illustrates combining a representation system with a generative model?"
                ),
                "options": [
                    "Use semantic retrieval to find relevant documents, then give them to a generative model to answer a question.",
                    "Count words and stop before using any model.",
                    "Use only a GPU memory monitor to classify text.",
                    "Replace the tokenizer with a spreadsheet.",
                ],
                "correct": 0,
                "explanation": (
                    "Semantic retrieval can use embeddings/representation models "
                    "to find relevant information, while a generative model can use "
                    "that retrieved context to produce an answer."
                ),
            },

            {
                "id": "M01.L01.Q07",
                "section_id": "responsible-use",
                "question": (
                    "Which statement is safest and most consistent with the chapter?"
                ),
                "options": [
                    "A fluent answer from an LLM should be considered verified.",
                    "Bias is impossible if a model has many parameters.",
                    "LLM output can be incorrect even when expressed confidently.",
                    "Responsible-use concerns apply only to open models.",
                ],
                "correct": 2,
                "explanation": (
                    "The chapter explicitly warns that LLMs do not necessarily "
                    "produce ground truth and can confidently output incorrect text."
                ),
            },

            {
                "id": "M01.L01.Q08",
                "section_id": "using-models",
                "question": (
                    "What is a major trade-off when comparing a hosted proprietary model with a locally run open model?"
                ),
                "options": [
                    "Hosted models never use APIs, while open models always do.",
                    "Hosted models reduce local infrastructure needs, while local open models can provide more direct control but require suitable hardware and setup.",
                    "Local models never require memory.",
                    "Open models cannot be fine-tuned.",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter contrasts provider-managed convenience with the "
                    "control and privacy potential of local models, which also bring "
                    "hardware and setup responsibilities."
                ),
            },

            {
                "id": "M01.L01.Q09",
                "section_id": "first-generation",
                "question": (
                    "In the chapter's Phi-3 example, what is the tokenizer's main job?"
                ),
                "options": [
                    "Convert input text into tokens the model can process.",
                    "Provide GPU VRAM.",
                    "Replace the model's learned parameters.",
                    "Verify every generated claim as factual.",
                ],
                "correct": 0,
                "explanation": (
                    "The tokenizer prepares text for the model by converting it "
                    "into tokenized form; it is a separate but essential component "
                    "of the generation pipeline."
                ),
            },

            {
                "id": "M01.L01.Q10",
                "section_id": "first-generation",
                "type": "open",
                "question": (
                    "Design a simple Language AI application of your own. State "
                    "whether it needs a representation model, a generative model, "
                    "retrieval, or a combination, and justify your choices using "
                    "concepts from this lesson."
                ),
            },
        ],

        "passing_score": 70,
    },
}
