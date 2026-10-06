"""M01.L01 — Hello Transformers.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-004, Chapter 1, pages not provided in the supplied source extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "Transformer Foundations & First Applications"

MODULE_DESCRIPTION = (
    "Build an intuitive mental model of transformers by connecting sequence models, "
    "attention, transfer learning, pretrained models, common NLP pipelines, and the "
    "Hugging Face ecosystem."
)

SOURCE_CHAPTER = 1

SOURCE_PAGES = "Not provided in the supplied source extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Hello Transformers",

    "slug": "applied-nlp-transformers-m01-l01",

    "description": (
        "Understand why transformers changed NLP, how attention and transfer learning "
        "fit together, and how pretrained transformer pipelines can solve common text "
        "tasks with only a small amount of code."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 1.5,

    "skill_tags": [
        "nlp",
        "transformers",
        "attention",
        "transfer-learning",
        "hugging-face",
        "pipelines",
        "module-01",
    ],

    "prerequisite_ids": [],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Hello Transformers",

        "content": (
            "# Hello Transformers\n"
            "\n"
            "> **Course:** Applied NLP with Transformers  \n"
            "> **Lesson:** M01.L01  \n"
            "> **Module:** Transformer Foundations & First Applications  \n"
            "> **Source alignment:** BOOK-004, Chapter 1. Page numbers were not "
            "provided in the supplied source extract. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the problem the Transformer architecture was designed to improve.\n"
            "- Describe the encoder-decoder pattern and its information bottleneck.\n"
            "- Explain attention and self-attention at an intuitive level.\n"
            "- Describe how pretraining and fine-tuning enable transfer learning in NLP.\n"
            "- Distinguish the basic roles of GPT-style and BERT-style models.\n"
            "- Use the Hugging Face `pipeline()` API for several common NLP tasks.\n"
            "- Identify the main pieces of the Hugging Face ecosystem.\n"
            "- Recognize practical limitations of transformer models.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why transformers mattered\n"
            "\n"
            "Before transformers became dominant, recurrent neural networks such as "
            "RNNs and LSTMs were common choices for text and other sequential data. "
            "They process a sequence step by step and carry information forward through "
            "a hidden state. This makes them naturally suited to ordered data, but it "
            "also means much of their computation is sequential.\n"
            "\n"
            "The Transformer introduced a different idea: instead of relying on "
            "recurrence to move information through a sentence one step at a time, it "
            "uses attention as the central mechanism for relating tokens to one another. "
            "This change made training more parallelizable and became a foundation for "
            "models such as GPT and BERT.\n"
            "\n"
            "A useful mental model is:\n"
            "\n"
            "```text\n"
            "RNN/LSTM era: sequence -> step -> step -> step -> representation\n"
            "Transformer era: tokens -> attention across tokens -> contextual representations\n"
            "```\n"
            "\n"
            "The architecture alone was not the whole story. Its impact grew dramatically "
            "when it was combined with transfer learning: train a model broadly first, "
            "then adapt it to a specific task instead of building every NLP system from "
            "scratch.\n"
            "\n"
            "[[IMAGE_NEEDED: Transformer evolution timeline | A simple chronological "
            "timeline showing the 2017 Transformer paper, ULMFiT, GPT, BERT, and the "
            "subsequent expansion of transformer models | Learner should notice that "
            "modern transformer NLP emerged from the combination of a new architecture "
            "and practical transfer-learning methods]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Encoder-decoder models before transformers\n"
            "\n"
            "Many sequence problems map one sequence to another. Machine translation is "
            "the classic example: an English sentence goes in, and a sentence in another "
            "language comes out. The input and output can have different lengths, so a "
            "fixed one-input/one-output model is not enough.\n"
            "\n"
            "The encoder-decoder framework separates the job into two parts:\n"
            "\n"
            "1. **Encoder:** reads the input sequence and builds a numerical representation.\n"
            "2. **Decoder:** uses that representation to generate the output sequence.\n"
            "\n"
            "With recurrent models, the encoder reads tokens one after another and updates "
            "its hidden state. In the simplest version, only the final hidden state is "
            "passed to the decoder.\n"
            "\n"
            "### Easy example\n"
            "\n"
            "Imagine compressing this sentence into one vector:\n"
            "\n"
            "```text\n"
            "The package I ordered last week arrived damaged this morning.\n"
            "```\n"
            "\n"
            "The decoder must rely on that compressed representation to generate a "
            "translation. For short inputs this can work well. For long inputs, important "
            "details from the beginning can become difficult to preserve.\n"
            "\n"
            "This is the **information bottleneck**: one fixed representation is expected "
            "to carry everything the decoder may need.\n"
            "\n"
            "[[IMAGE_NEEDED: RNN unrolled through time | A recurrent network shown both "
            "as a feedback loop and as an unrolled sequence of hidden states h1, h2, h3, "
            "h4 | Learner should notice that each step depends on the state produced by "
            "the previous step]]\n"
            "\n"
            "[[IMAGE_NEEDED: Encoder-decoder bottleneck | An RNN encoder reading several "
            "input tokens into a final hidden-state vector, followed by an RNN decoder "
            "generating output tokens one at a time | Learner should notice that the "
            "single final encoder state forms a narrow information bottleneck between "
            "input and output]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Attention: let the decoder look back\n"
            "\n"
            "Attention reduces the bottleneck by giving the decoder access to all of the "
            "encoder's hidden states instead of only the final one. The decoder does not "
            "treat every hidden state equally. At each output step, it assigns larger "
            "weights to the input positions that appear most relevant.\n"
            "\n"
            "Suppose a translation model is generating one word in the target language. "
            "The model can focus strongly on the source word or phrase that best helps "
            "produce that particular output. On the next output step, the attention "
            "pattern can change.\n"
            "\n"
            "### Think of attention as a weighted lookup\n"
            "\n"
            "For a simplified input with four states:\n"
            "\n"
            "```text\n"
            "Encoder states:   h1     h2     h3     h4\n"
            "Attention weight: 0.05   0.15   0.70   0.10\n"
            "```\n"
            "\n"
            "The decoder is effectively saying: *for this output step, h3 matters most*. "
            "The exact weights are learned by the model.\n"
            "\n"
            "Attention was especially useful for translation because words that correspond "
            "to one another may appear in different positions in different languages. The "
            "model can learn these alignments instead of depending on position alone.\n"
            "\n"
            "[[IMAGE_NEEDED: Attention alignment matrix | A heatmap with source-language "
            "tokens on one axis and target-language tokens on the other, with darker cells "
            "showing stronger attention weights | Learner should notice that strong cells "
            "can connect corresponding words even when their positions differ between "
            "languages]]\n"
            "\n"
            "### From attention to self-attention\n"
            "\n"
            "Recurrent encoder-decoder models with attention still process the sequence "
            "recurrently. The Transformer removes recurrence and relies on **self-attention**. "
            "Instead of a decoder only attending to encoder states, tokens within the same "
            "layer can attend to other tokens in that layer.\n"
            "\n"
            "For example, in a sentence such as:\n"
            "\n"
            "```text\n"
            "The robot picked up the box because it was blocking the door.\n"
            "```\n"
            "\n"
            "a contextual representation of `it` can be influenced by other relevant "
            "tokens in the sentence. Later lessons will explain the actual query, key, "
            "value computations. For now, remember the central idea: **self-attention lets "
            "a token build its representation by considering other tokens in the same "
            "sequence.**\n"
            "\n"
            "[[IMAGE_NEEDED: Transformer self-attention overview | A simplified Transformer "
            "encoder-decoder diagram showing self-attention blocks followed by feed-forward "
            "networks, without detailed equations | Learner should notice that recurrence "
            "is removed and attention is the main mechanism connecting token information]]\n"
            "\n"
            "{{exercise:M01.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Transfer learning: learn broadly, then specialize\n"
            "\n"
            "A powerful architecture is useful, but training a large NLP model from scratch "
            "for every application would still require enormous amounts of data and compute. "
            "Transfer learning solves this by reusing knowledge learned during an earlier "
            "training stage.\n"
            "\n"
            "The basic pattern is:\n"
            "\n"
            "```text\n"
            "large general corpus -> pretraining -> pretrained model\n"
            "                                      |\n"
            "                                      v\n"
            "small task dataset  -> adaptation / fine-tuning -> task model\n"
            "```\n"
            "\n"
            "The same idea had already become important in computer vision. A model first "
            "learns general visual features from a large dataset, then those learned weights "
            "are adapted to a smaller downstream task. NLP needed a similarly effective "
            "pretraining strategy.\n"
            "\n"
            "[[IMAGE_NEEDED: Training from scratch versus transfer learning | Side-by-side "
            "diagram comparing a task model trained only on a small labeled dataset with a "
            "pretrained model adapted to that same downstream task | Learner should notice "
            "that transfer learning reuses general knowledge instead of relearning "
            "everything from the task dataset]]\n"
            "\n"
            "### ULMFiT's three-stage idea\n"
            "\n"
            "ULMFiT helped show a practical transfer-learning path for NLP. Its workflow can "
            "be understood as three stages:\n"
            "\n"
            "1. **Pretraining:** learn language patterns on a large general corpus using a "
            "language-modeling objective.\n"
            "2. **Domain adaptation:** continue language-model training on text closer to "
            "the target domain.\n"
            "3. **Fine-tuning:** add or adapt a task-specific prediction layer and train for "
            "the final task.\n"
            "\n"
            "The important insight is that unlabeled text itself can provide a learning "
            "signal. A language model can learn by predicting missing or upcoming words, so "
            "we do not need humans to label every sentence used during pretraining.\n"
            "\n"
            "[[IMAGE_NEEDED: ULMFiT three-stage workflow | A three-step flow labeled "
            "pretraining, domain adaptation, and task fine-tuning | Learner should notice "
            "how a broadly pretrained language model is progressively specialized]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. GPT and BERT: two influential transformer directions\n"
            "\n"
            "The source chapter introduces GPT and BERT as two major early examples of "
            "combining Transformer components with pretraining. They use different parts "
            "of the original encoder-decoder architecture and different language-modeling "
            "objectives.\n"
            "\n"
            "| Model family | Main Transformer part highlighted in the chapter | Pretraining idea | Intuition |\n"
            "|---|---|---|---|\n"
            "| GPT | Decoder | Predict upcoming text | Learn to continue a sequence |\n"
            "| BERT | Encoder | Predict masked words | Learn bidirectional context around missing tokens |\n"
            "\n"
            "### Masked language modeling\n"
            "\n"
            "A BERT-style training example might look like:\n"
            "\n"
            "```text\n"
            "The customer opened the [MASK] and found the wrong item.\n"
            "```\n"
            "\n"
            "The model learns to predict a plausible token for the masked position using "
            "context from both sides.\n"
            "\n"
            "### Next-token language modeling\n"
            "\n"
            "A GPT-style objective instead asks the model to predict what comes next:\n"
            "\n"
            "```text\n"
            "The package arrived -> damaged\n"
            "```\n"
            "\n"
            "These simplified examples are not descriptions of every modern model. They "
            "are mental models for the two pretraining directions introduced in this "
            "chapter.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Your first transformer applications with pipelines\n"
            "\n"
            "Using a research model directly can involve many steps: implementing or "
            "loading the architecture, loading pretrained weights, tokenizing inputs, "
            "running inference, and postprocessing outputs. The Hugging Face Transformers "
            "library provides standardized interfaces that hide much of this repetitive "
            "work.\n"
            "\n"
            "For a beginner, the easiest entry point is `pipeline()`. A pipeline bundles "
            "the preprocessing, model inference, and task-specific postprocessing needed "
            "for a supported task.\n"
            "\n"
            "### 6.1 Text classification\n"
            "\n"
            "```python\n"
            "from transformers import pipeline\n"
            "\n"
            "classifier = pipeline(\"text-classification\")\n"
            "result = classifier(\"The replacement arrived broken again.\")\n"
            "print(result)\n"
            "```\n"
            "\n"
            "For sentiment analysis, a returned item typically contains a label and a "
            "score. The score represents the model's confidence according to that model's "
            "output; it should not be treated as a guarantee of correctness.\n"
            "\n"
            "### 6.2 Named entity recognition\n"
            "\n"
            "Named entity recognition, or NER, identifies spans representing things such "
            "as people, organizations, and locations.\n"
            "\n"
            "```python\n"
            "ner = pipeline(\"ner\", aggregation_strategy=\"simple\")\n"
            "entities = ner(\"Maya ordered a laptop from Acme in Berlin.\")\n"
            "print(entities)\n"
            "```\n"
            "\n"
            "A tokenizer may split a word into smaller tokens. Aggregation helps combine "
            "related token predictions into a more natural entity span. The mechanics of "
            "tokenization are studied in the next chapter.\n"
            "\n"
            "### 6.3 Extractive question answering\n"
            "\n"
            "In extractive question answering, the answer is selected directly from a "
            "provided context.\n"
            "\n"
            "```python\n"
            "reader = pipeline(\"question-answering\")\n"
            "context = \"The customer wants a replacement for the damaged laptop.\"\n"
            "question = \"What does the customer want?\"\n"
            "answer = reader(question=question, context=context)\n"
            "print(answer[\"answer\"])\n"
            "```\n"
            "\n"
            "This is called **extractive** because the predicted answer is a span from the "
            "context rather than newly written text.\n"
            "\n"
            "### 6.4 Summarization\n"
            "\n"
            "Summarization takes a longer text and produces a shorter version intended to "
            "preserve the most relevant information. Unlike classification or extractive "
            "QA, the model generates text.\n"
            "\n"
            "```python\n"
            "summarizer = pipeline(\"summarization\")\n"
            "summary = summarizer(long_text, max_length=60)\n"
            "print(summary[0][\"summary_text\"])\n"
            "```\n"
            "\n"
            "Because generated text can contain mistakes or omit important details, the "
            "output still needs evaluation for your use case.\n"
            "\n"
            "### 6.5 Translation\n"
            "\n"
            "Translation is also a generation task. A pipeline can use a model trained for "
            "a particular language pair.\n"
            "\n"
            "```python\n"
            "translator = pipeline(\n"
            "    \"translation_en_to_de\",\n"
            "    model=\"Helsinki-NLP/opus-mt-en-de\",\n"
            ")\n"
            "translated = translator(\"Your order has been shipped.\")\n"
            "print(translated[0][\"translation_text\"])\n"
            "```\n"
            "\n"
            "### 6.6 Text generation\n"
            "\n"
            "A text-generation model continues a prompt. This can support workflows such "
            "as autocomplete or drafting, but generated continuations are not guaranteed "
            "to be correct, appropriate, or factual.\n"
            "\n"
            "```python\n"
            "generator = pipeline(\"text-generation\")\n"
            "prompt = \"Customer service response: We are sorry about the damaged item.\"\n"
            "completion = generator(prompt, max_length=80)\n"
            "print(completion[0][\"generated_text\"])\n"
            "```\n"
            "\n"
            "### One pattern behind all six examples\n"
            "\n"
            "```text\n"
            "raw text\n"
            "   -> tokenizer / preprocessing\n"
            "   -> pretrained or fine-tuned transformer\n"
            "   -> task-specific postprocessing\n"
            "   -> usable prediction or generated text\n"
            "```\n"
            "\n"
            "The pipeline API hides most of these details, but later lessons will open the "
            "box so you can control each stage yourself.\n"
            "\n"
            "{{exercise:M01.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 7. The Hugging Face ecosystem\n"
            "\n"
            "A transformer project needs more than a model. You may need model weights, "
            "tokenization, datasets, evaluation, and training infrastructure. The chapter "
            "introduces an ecosystem designed to make those pieces work together.\n"
            "\n"
            "### The Hub\n"
            "\n"
            "The Hugging Face Hub provides pretrained models and other reusable resources. "
            "Model and dataset cards help document what a resource is, how it was created, "
            "and how it should be used. This matters because picking a model should be an "
            "informed engineering decision, not simply choosing the first search result.\n"
            "\n"
            "### Transformers\n"
            "\n"
            "The Transformers library provides standardized model APIs and task-specific "
            "components, including the high-level pipelines used earlier.\n"
            "\n"
            "### Tokenizers\n"
            "\n"
            "Models do not directly consume raw sentences. Tokenizers split and transform "
            "text into token-level numerical inputs. Tokens may correspond to whole words, "
            "parts of words, or punctuation.\n"
            "\n"
            "### Datasets\n"
            "\n"
            "The Datasets library helps load, process, cache, and work with datasets through "
            "a standard interface. The chapter also highlights techniques such as memory "
            "mapping for working efficiently with data that may be larger than available RAM.\n"
            "\n"
            "### Accelerate\n"
            "\n"
            "Accelerate helps reduce infrastructure-specific boilerplate when moving "
            "training code between environments such as a laptop and more powerful "
            "multi-device hardware.\n"
            "\n"
            "[[IMAGE_NEEDED: Hugging Face ecosystem map | A simple hub-and-spoke diagram "
            "connecting the Hub with Transformers, Tokenizers, Datasets, and Accelerate | "
            "Learner should notice that a practical NLP workflow is an ecosystem of "
            "interoperating tools rather than only a model architecture]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Transformers are powerful, not magical\n"
            "\n"
            "The chapter closes by emphasizing several real limitations. Treating a "
            "transformer as a universal solution is a mistake.\n"
            "\n"
            "| Challenge | What it means in practice |\n"
            "|---|---|\n"
            "| Language coverage | High-quality pretrained resources are easier to find for some languages than for low-resource languages. |\n"
            "| Data availability | Transfer learning reduces labeled-data needs, but many tasks still require task-relevant examples. |\n"
            "| Long documents | Self-attention can become computationally expensive as input length grows. |\n"
            "| Opacity | It can be difficult to explain exactly why a deep model produced a particular prediction. |\n"
            "| Bias | Models can learn undesirable patterns and biases from their pretraining data. |\n"
            "\n"
            "These are engineering constraints, not side notes. They affect which model "
            "you choose, what data you collect, how you evaluate it, and where human "
            "review may be necessary.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Attention and self-attention are exactly the same thing\n"
            "\n"
            "> Attention always means a decoder looking at encoder outputs.\n"
            "\n"
            "That describes one important encoder-decoder use of attention, but "
            "self-attention operates among representations in the same sequence/layer. "
            "The Transformer relies heavily on self-attention rather than recurrence.\n"
            "\n"
            "### Misconception 2: A pretrained model is automatically good for my task\n"
            "\n"
            "> If a model is pretrained, I can trust it without task-specific evaluation.\n"
            "\n"
            "Pretraining gives useful general representations, but the model still needs "
            "to be selected, adapted when necessary, and evaluated on data that reflects "
            "your real application.\n"
            "\n"
            "### Misconception 3: A pipeline score is proof that the prediction is correct\n"
            "\n"
            "> A confidence score of 0.95 means the answer is 95% certain to be true.\n"
            "\n"
            "The score is a model output associated with its prediction. It does not turn "
            "the prediction into a guaranteed fact and should be interpreted in the "
            "context of the model and task.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| RNN | A recurrent neural network that carries state from one sequence step to the next. |\n"
            "| Encoder | A component that converts an input sequence into useful internal representations. |\n"
            "| Decoder | A component that generates an output sequence from internal representations and previous outputs. |\n"
            "| Hidden state | A learned numerical representation that carries information through a sequence model. |\n"
            "| Attention | A mechanism that assigns different importance weights to available representations. |\n"
            "| Self-attention | Attention in which representations within the same sequence/layer interact with one another. |\n"
            "| Pretraining | Training a model on a broad objective and large corpus before adapting it to a downstream task. |\n"
            "| Fine-tuning | Continuing training so a pretrained model becomes specialized for a target task or domain. |\n"
            "| Language modeling | Learning to predict linguistic elements, such as upcoming or masked tokens, from context. |\n"
            "| Pipeline | A high-level API that combines preprocessing, model inference, and postprocessing for a task. |\n"
            "| Token | A unit produced by tokenization; it may be a word, word piece, character, or punctuation symbol. |\n"
            "| Named entity recognition | The task of locating and categorizing entities such as people, organizations, and places. |\n"
            "| Extractive QA | Question answering in which the answer is selected directly from the supplied context. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why can a single final encoder state become a bottleneck for long sequences?\n"
            "2. What does attention add to an encoder-decoder model?\n"
            "3. How is self-attention different from the recurrent processing used by an RNN?\n"
            "4. What is the difference between pretraining and fine-tuning?\n"
            "5. What broad distinction does this chapter make between GPT and BERT?\n"
            "6. What does `pipeline()` hide from the beginner?\n"
            "7. Which Hugging Face component would you associate with tokenization? With datasets? With training infrastructure?\n"
            "8. Name three real-world limitations that should be considered before deploying a transformer.\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**The transformer revolution came from more than one invention: attention-based "
            "architectures made sequence modeling more flexible and parallelizable, while "
            "pretraining and transfer learning made powerful language models reusable across "
            "many downstream tasks. High-level tools such as Hugging Face pipelines make "
            "those models easy to try, but good NLP engineering still requires understanding "
            "the model, data, task, and limitations.**\n"
        ),

        "estimated_minutes": 90,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "why-transformers",
                "title": "Why transformers mattered",
                "order": 1,
            },
            {
                "id": "encoder-decoder",
                "title": "Encoder-decoder models before transformers",
                "order": 2,
            },
            {
                "id": "attention",
                "title": "Attention: let the decoder look back",
                "order": 3,
            },
            {
                "id": "transfer-learning",
                "title": "Transfer learning: learn broadly, then specialize",
                "order": 4,
            },
            {
                "id": "gpt-bert",
                "title": "GPT and BERT",
                "order": 5,
            },
            {
                "id": "pipelines",
                "title": "Your first transformer applications with pipelines",
                "order": 6,
            },
            {
                "id": "hugging-face-ecosystem",
                "title": "The Hugging Face ecosystem",
                "order": 7,
            },
            {
                "id": "challenges",
                "title": "Transformers are powerful, not magical",
                "order": 8,
            },
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Trace the Information Flow",

            "lesson_code": "M01.L01",

            "section_id": "attention",

            "placement": "after_section",

            "description": (
                "Compare a basic recurrent encoder-decoder model with an attention-based "
                "version and explain why attention helps."
            ),

            "instructions": (
                "1. Consider the sentence: 'The camera that I ordered last month arrived damaged.'\n"
                "2. Describe what information the final encoder state would need to preserve "
                "in a simple encoder-decoder model.\n"
                "3. Now imagine the decoder is generating the translated word corresponding "
                "to 'camera'. Explain which encoder position you would expect to receive a "
                "large attention weight.\n"
                "4. In 2-3 sentences, explain why access to all encoder states can reduce the "
                "information bottleneck.\n"
                "5. Finally, state one difference between this encoder-decoder attention and "
                "self-attention."
            ),

            "expected_output": (
                "A short written explanation identifying the information bottleneck, the "
                "likely attended source position, and the distinction between attention "
                "across encoder-decoder components and self-attention within a sequence."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "encoder-decoder-reasoning",
                "attention-intuition",
                "self-attention-distinction",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Choose the Right NLP Pipeline",

            "lesson_code": "M01.L01",

            "section_id": "pipelines",

            "placement": "after_section",

            "description": (
                "Match realistic NLP requirements to the pipeline task that best represents "
                "the problem."
            ),

            "instructions": (
                "For each scenario, choose one of these task types: text classification, "
                "NER, extractive question answering, summarization, translation, or text generation.\n\n"
                "1. Detect whether a product review is positive or negative.\n"
                "2. Extract company and city names from support tickets.\n"
                "3. Answer 'When will my order arrive?' from a supplied shipping-policy paragraph.\n"
                "4. Reduce a long complaint to three key sentences.\n"
                "5. Convert an English support message to German.\n"
                "6. Draft a possible continuation of a customer-service reply.\n\n"
                "Then choose any two scenarios and sketch the corresponding `pipeline()` "
                "call in Python. Explain what type of output you expect."
            ),

            "expected_output": (
                "Six correct task mappings plus two small Python pipeline examples and a "
                "brief description of their expected outputs."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "task-identification",
                "hugging-face-pipelines",
                "nlp-application-reasoning",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "Hello Transformers — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",

                "section_id": "encoder-decoder",

                "question": (
                    "Why can the final hidden state in a simple recurrent encoder-decoder "
                    "become a bottleneck?"
                ),

                "options": [
                    "It prevents the decoder from producing more than one token.",
                    "It must compress the information from the whole input sequence into one fixed representation.",
                    "It forces every input token to have the same embedding.",
                    "It removes the need for a decoder.",
                ],

                "correct": 1,

                "explanation": (
                    "In the simple architecture described in the chapter, the decoder relies "
                    "on the encoder's final hidden state. Long inputs make it difficult for "
                    "one fixed representation to preserve every useful detail."
                ),
            },

            {
                "id": "M01.L01.Q02",

                "section_id": "attention",

                "question": "What is the main purpose of attention in the encoder-decoder example?",

                "options": [
                    "To give every encoder state exactly the same importance.",
                    "To eliminate the need for any numerical representation.",
                    "To let the decoder weight encoder states differently depending on what it is generating.",
                    "To convert every sequence into a single character.",
                ],

                "correct": 2,

                "explanation": (
                    "Attention allows the decoder to focus more strongly on the encoder "
                    "states that are relevant to the current output step."
                ),
            },

            {
                "id": "M01.L01.Q03",

                "section_id": "transfer-learning",

                "question": "Which sequence best represents the transfer-learning idea introduced in the lesson?",

                "options": [
                    "Pretrain broadly, then adapt or fine-tune for a downstream task.",
                    "Label every possible sentence, then remove the model weights.",
                    "Train a new architecture from scratch for every input sentence.",
                    "Skip pretraining and use only randomly initialized task heads.",
                ],

                "correct": 0,

                "explanation": (
                    "Transfer learning reuses knowledge acquired during broad pretraining and "
                    "then adapts that model to a more specific task or domain."
                ),
            },

            {
                "id": "M01.L01.Q04",

                "section_id": "pipelines",

                "question": (
                    "You have a paragraph and want the model to return the exact text span "
                    "that answers a question. Which task best matches this requirement?"
                ),

                "options": [
                    "Text generation",
                    "Named entity recognition",
                    "Sentiment classification",
                    "Extractive question answering",
                ],

                "correct": 3,

                "explanation": (
                    "Extractive question answering selects an answer span directly from the "
                    "provided context."
                ),
            },

            {
                "id": "M01.L01.Q05",

                "section_id": "challenges",

                "type": "open",

                "question": (
                    "Your team wants to use a transformer to process very long documents in "
                    "a low-resource language and make an important business decision. Name "
                    "three challenges from this lesson that should be investigated before "
                    "deployment, and explain why each matters."
                ),
            },
        ],

        "passing_score": 70,
    },
}
