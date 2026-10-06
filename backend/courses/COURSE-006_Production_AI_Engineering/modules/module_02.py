"""M02.L01 — Understanding Foundation Models.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 2, "Understanding Foundation Models".
Instructor-authored curriculum adaptation based only on the supplied chapter.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M02.L01"

MODULE_ORDER = 2

MODULE_TITLE = "Understanding Foundation Models"

MODULE_DESCRIPTION = (
    "Understand the major design decisions behind foundation models: training "
    "data, model architecture, model scale, post-training, sampling, structured "
    "outputs, and the probabilistic behaviors that affect downstream AI "
    "applications."
)

SOURCE_CHAPTER = 2

SOURCE_PAGES = "Page range not provided in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Understanding Foundation Models",

    "slug": "ai-engineering-m02-l01-understanding-foundation-models",

    "description": (
        "A learner-friendly but technically meaningful guide to how foundation "
        "models are shaped by their data, architecture, scale, alignment, and "
        "sampling process—and how those choices affect real AI applications."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.0,

    "skill_tags": [
        "foundation-models",
        "training-data",
        "transformers",
        "attention",
        "model-scaling",
        "mixture-of-experts",
        "post-training",
        "sft",
        "rlhf",
        "sampling",
        "structured-outputs",
        "hallucination",
        "ai-engineering",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Understanding Foundation Models",

        "content": (
            "# Understanding Foundation Models\n"
            "\n"
            "> **Course:** AI Engineering Foundations  \n"
            "> **Lesson:** M02.L01  \n"
            "> **Module:** Understanding Foundation Models  \n"
            "> **Source alignment:** Chapter 2, *Understanding Foundation Models*. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain how training-data distribution affects model capability, "
            "bias, language quality, and domain performance.\n"
            "- Explain why data quality, quantity, and diversity must be considered "
            "together.\n"
            "- Describe why multilingual models can perform differently across "
            "languages and why tokenization affects cost and latency.\n"
            "- Explain why domain-specific models can outperform general-purpose "
            "models on specialized tasks.\n"
            "- Describe why the transformer replaced earlier sequence-to-sequence "
            "architectures for many language-model workloads.\n"
            "- Explain attention using query, key, and value vectors.\n"
            "- Distinguish the prefill and decode stages of autoregressive inference.\n"
            "- Describe the main components of a transformer block.\n"
            "- Explain what model size, training tokens, and FLOPs tell you about "
            "a model's scale.\n"
            "- Explain dense, sparse, and mixture-of-experts models at a high level.\n"
            "- Apply the intuition behind compute-optimal scaling and understand "
            "why bigger is not automatically better.\n"
            "- Distinguish pre-training, supervised finetuning, and preference "
            "finetuning.\n"
            "- Explain the purpose of RLHF, DPO, RLAIF, reward models, and "
            "comparison data.\n"
            "- Explain how logits become probabilities and how a model samples "
            "tokens.\n"
            "- Reason about temperature, top-k, top-p, stopping conditions, and "
            "test-time compute.\n"
            "- Compare methods for producing structured outputs.\n"
            "- Explain why foundation-model outputs are probabilistic and how "
            "this leads to inconsistency and hallucinations.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. The big picture: what shapes a foundation model?\n"
            "\n"
            "You do not need to know how to train a frontier foundation model "
            "from scratch to build useful applications with one. However, you do "
            "need enough understanding to answer practical questions such as:\n"
            "\n"
            "- Why does one model perform better in one language than another?\n"
            "- Why can a smaller model sometimes outperform a larger model?\n"
            "- Why are some models easier to deploy?\n"
            "- Why do two runs of the same model produce different answers?\n"
            "- Why can a model follow instructions well even though pre-training "
            "only teaches next-token prediction?\n"
            "\n"
            "The chapter groups many of these differences into four major areas:\n"
            "\n"
            "```text\n"
            "Foundation-model behavior\n"
            "        |\n"
            "        +-- Training data\n"
            "        +-- Architecture and model size\n"
            "        +-- Post-training / alignment\n"
            "        +-- Sampling at inference time\n"
            "```\n"
            "\n"
            "A useful mental model is this:\n"
            "\n"
            "**Data determines what the model had a chance to learn. Architecture "
            "and scale determine how much it can represent and how efficiently it "
            "works. Post-training shapes how it responds to people. Sampling "
            "controls how one particular output is chosen.**\n"
            "\n"
            '{{image:foundation-model-design-map}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 2. Training data determines what the model can learn\n"
            "\n"
            "A model learns patterns from its training data. If a capability, "
            "language, domain, or data pattern is missing from that data, the "
            "model has little reason to become good at it.\n"
            "\n"
            "This sounds obvious, but it has major consequences for foundation "
            "models because they need enormous datasets. Model developers often "
            "cannot collect exactly the dataset they would ideally want, so they "
            "use large available sources such as web crawls.\n"
            "\n"
            "### Available data is not automatically good data\n"
            "\n"
            "The chapter uses Common Crawl and Google's cleaned C4 subset as "
            "important examples. Web-scale data can contain useful knowledge, but "
            "it can also contain clickbait, misinformation, propaganda, hateful "
            "content, low-quality pages, and duplicated or noisy material.\n"
            "\n"
            "This creates an important engineering lesson:\n"
            "\n"
            "> **A huge dataset is not automatically a good dataset.**\n"
            "\n"
            "If your model learns from whatever is easiest to collect, it may "
            "become strong on common internet tasks while remaining weak on the "
            "tasks your application actually needs.\n"
            "\n"
            "### More data is not always better\n"
            "\n"
            "More data usually requires more compute. Worse, adding low-quality "
            "data can fail to improve the model. A smaller collection of carefully "
            "curated data can sometimes be more useful than a much larger noisy "
            "collection.\n"
            "\n"
            "The chapter ultimately emphasizes three goals for training data:\n"
            "\n"
            "1. **Quantity** — enough data to learn rich patterns.\n"
            "2. **Quality** — useful, accurate, relevant examples.\n"
            "3. **Diversity** — broad coverage rather than a narrow slice of the "
            "world.\n"
            "\n"
            "These goals can conflict. Curating better data can cost more. Adding "
            "diversity can make filtering harder. Scaling quantity increases "
            "compute requirements.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Multilingual models and low-resource languages\n"
            "\n"
            "Internet data is not evenly distributed across languages. The source "
            "chapter notes that English occupies a very large share of Common "
            "Crawl, while many languages spoken by millions of people occupy only "
            "a tiny fraction.\n"
            "\n"
            "Languages with limited training-data availability are commonly "
            "described as **low-resource languages**.\n"
            "\n"
            "### Why under-representation matters\n"
            "\n"
            "If the model sees far more English than another language during "
            "training, it has more opportunities to learn English vocabulary, "
            "grammar, factual associations, and problem-solving patterns expressed "
            "in English. This can lead to lower quality in under-represented "
            "languages.\n"
            "\n"
            "Under-representation is not the only factor. Language structure, "
            "cultural context, and other properties can also affect difficulty.\n"
            "\n"
            "### Why 'translate everything to English' is imperfect\n"
            "\n"
            "A common workaround is:\n"
            "\n"
            "```text\n"
            "user language -> translate to English -> run model -> translate back\n"
            "```\n"
            "\n"
            "This can help, but it has two major weaknesses:\n"
            "\n"
            "1. The translation step already requires strong understanding of the "
            "original language.\n"
            "2. Translation can discard information that does not map cleanly "
            "between languages, such as culturally or socially meaningful "
            "pronouns and relationships.\n"
            "\n"
            "### Tokenization affects latency and cost\n"
            "\n"
            "Different languages can require very different numbers of tokens to "
            "express the same meaning. Because model inference cost and latency "
            "often scale with token count, a language that tokenizes inefficiently "
            "can be slower and more expensive to serve.\n"
            "\n"
            "This is an important application-design lesson: **multilingual "
            "quality is not only a translation problem; it can also be a "
            "tokenization, cost, and latency problem.**\n"
            "\n"
            "[[IMAGE_NEEDED: Uneven multilingual representation | A simple bar "
            "chart contrasting one highly represented language with several "
            "low-resource languages in a web-scale dataset | Learner should notice "
            "that model exposure to languages can differ dramatically and that "
            "this can influence downstream performance]]\n"
            "\n"
            "---\n"
            "\n"

            "## 4. General-purpose versus domain-specific models\n"
            "\n"
            "General-purpose foundation models can perform across many domains "
            "because their training data contains a wide range of topics. But "
            "specialized tasks may involve data that is rare, private, expensive, "
            "or structurally different from normal web data.\n"
            "\n"
            "Examples in the chapter include drug discovery and cancer screening. "
            "Protein structures, genomic data, X-rays, and medical scans are not "
            "well represented by ordinary public webpages.\n"
            "\n"
            "For such tasks, teams may need **domain-specific datasets** and "
            "sometimes domain-specific models. Another practical path is to "
            "finetune a general-purpose model using specialized data.\n"
            "\n"
            "The decision is not simply 'general model good, specialized model "
            "better.' It depends on the problem, available data, privacy, cost, "
            "and the performance required.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. From seq2seq to transformers\n"
            "\n"
            "To understand why transformers became dominant, it helps to see what "
            "came before them.\n"
            "\n"
            "Earlier **sequence-to-sequence (seq2seq)** systems commonly used "
            "recurrent neural networks (RNNs). An encoder processed the input "
            "sequence, and a decoder generated an output sequence.\n"
            "\n"
            "A simplified version looked like this:\n"
            "\n"
            "```text\n"
            "input tokens -> RNN encoder -> final hidden state -> RNN decoder -> output tokens\n"
            "```\n"
            "\n"
            "The chapter highlights two limitations of basic seq2seq systems.\n"
            "\n"
            "### Limitation 1: a compressed representation bottleneck\n"
            "\n"
            "The decoder could rely heavily on the encoder's final hidden state. "
            "The chapter compares this to answering detailed questions about an "
            "entire book using only a summary of the book.\n"
            "\n"
            "### Limitation 2: sequential processing\n"
            "\n"
            "RNNs process sequence positions one after another. A long input means "
            "waiting for earlier steps before processing later ones. This limits "
            "parallelism and makes long-sequence processing slower.\n"
            "\n"
            "The transformer addresses both issues using **attention** and by "
            "removing the RNN requirement.\n"
            "\n"
            "[[IMAGE_NEEDED: Seq2seq versus transformer | A side-by-side diagram "
            "showing an RNN encoder-decoder compressing input into a sequential "
            "representation versus a transformer where output generation can "
            "attend directly to relevant previous tokens | Learner should notice "
            "that attention gives the model richer access to earlier information "
            "and that transformer input processing is more parallelizable]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Attention: query, key, and value\n"
            "\n"
            "Attention lets the model decide which previous tokens matter most "
            "when computing a new representation or generating the next token.\n"
            "\n"
            "The chapter introduces three vectors:\n"
            "\n"
            "- **Query (Q):** what the current computation is looking for.\n"
            "- **Key (K):** a representation used to determine whether a previous "
            "token is relevant to the query.\n"
            "- **Value (V):** the information associated with that previous token.\n"
            "\n"
            "### A library analogy\n"
            "\n"
            "Imagine you are answering a question from a large book:\n"
            "\n"
            "- The **query** is the information you need.\n"
            "- A **key** is like an index entry telling you whether a page is "
            "relevant.\n"
            "- The **value** is the content you actually retrieve from that page.\n"
            "\n"
            "The model compares the query with keys. Tokens whose keys are more "
            "relevant receive more attention, causing their values to contribute "
            "more strongly to the output.\n"
            "\n"
            "The chapter expresses the learned projections as:\n"
            "\n"
            "```text\n"
            "K = x W_K\n"
            "V = x W_V\n"
            "Q = x W_Q\n"
            "```\n"
            "\n"
            "where `x` is the input representation and the W matrices are learned "
            "model parameters.\n"
            "\n"
            "### Multi-head attention\n"
            "\n"
            "Transformers normally use multiple attention heads. Instead of one "
            "attention calculation trying to capture every relationship, different "
            "heads can focus on different groups or patterns in the sequence.\n"
            "\n"
            "The results from the heads are combined and transformed again before "
            "the model continues to the next computation stage.\n"
            "\n"
            "### Why long context is expensive\n"
            "\n"
            "Previous tokens need key and value representations. As context grows, "
            "more of these vectors must be computed and stored. This is one reason "
            "long-context transformer inference creates substantial memory and "
            "compute pressure.\n"
            "\n"
            "[[IMAGE_NEEDED: Query-Key-Value attention | A simplified attention "
            "diagram with one query comparing against several keys, producing "
            "attention weights that determine how strongly the corresponding "
            "values contribute to the result | Learner should notice the "
            "difference between deciding relevance with Q/K and retrieving "
            "information through V]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Prefill and decode: what happens during inference\n"
            "\n"
            "Transformer-based autoregressive inference has two useful stages to "
            "understand.\n"
            "\n"
            "### Prefill\n"
            "\n"
            "The model processes the input tokens and builds the intermediate "
            "state needed to generate the first output token. Input processing can "
            "be parallelized across the prompt much more than RNN-style sequential "
            "processing.\n"
            "\n"
            "### Decode\n"
            "\n"
            "The model then generates output **one token at a time**. The next "
            "token depends on the previous sequence, so autoregressive decoding "
            "remains sequential.\n"
            "\n"
            "```text\n"
            "Prompt\n"
            "  |\n"
            "  +--> PREFILL: process prompt context\n"
            "  |\n"
            "  +--> DECODE: token 1 -> token 2 -> token 3 -> ...\n"
            "```\n"
            "\n"
            "This distinction matters for optimization because prefill and decode "
            "have different computational characteristics.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. What is inside a transformer?\n"
            "\n"
            "A transformer model is built from repeated **transformer blocks**. "
            "The exact implementation varies, but the chapter highlights two major "
            "modules inside a block.\n"
            "\n"
            "### Attention module\n"
            "\n"
            "The attention module uses the query, key, value, and output-projection "
            "weight matrices.\n"
            "\n"
            "### MLP / feedforward module\n"
            "\n"
            "The MLP contains linear transformations separated by nonlinear "
            "activation functions. The nonlinearity lets the network learn "
            "patterns that cannot be represented by a stack of purely linear "
            "transformations.\n"
            "\n"
            "One simple activation mentioned in the chapter is ReLU:\n"
            "\n"
            "```text\n"
            "ReLU(x) = max(0, x)\n"
            "```\n"
            "\n"
            "A transformer model also typically has:\n"
            "\n"
            "- An **embedding module** before the transformer blocks, converting "
            "tokens and positions into vectors.\n"
            "- An **output / unembedding layer** after the blocks, mapping the "
            "model representation into scores over vocabulary tokens.\n"
            "\n"
            "Important architecture dimensions include:\n"
            "\n"
            "- Model hidden dimension.\n"
            "- Number of transformer blocks / layers.\n"
            "- Feedforward dimension.\n"
            "- Vocabulary size.\n"
            "- Context length.\n"
            "\n"
            "[[IMAGE_NEEDED: Simplified transformer architecture | A vertical "
            "diagram showing token/position embeddings, repeated transformer "
            "blocks containing attention and MLP modules, then an output layer "
            "producing token scores | Learner should notice that a transformer "
            "is a stack of repeated blocks rather than a single attention "
            "operation]]\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Transformers are dominant, but not the only architecture\n"
            "\n"
            "The transformer is highly successful, but it also has limitations, "
            "especially around long sequences and memory/computation growth.\n"
            "\n"
            "The chapter discusses alternative approaches such as:\n"
            "\n"
            "- **RWKV:** an RNN-based model designed to benefit from parallelized "
            "training while avoiding some transformer context limitations in "
            "theory.\n"
            "- **State space models (SSMs):** architectures developed for efficient "
            "long-sequence modeling.\n"
            "- **S4:** an efficiency-focused SSM development.\n"
            "- **H3:** an approach adding mechanisms for recalling and comparing "
            "sequence information.\n"
            "- **Mamba:** a selective state-space architecture designed for "
            "efficient sequence modeling and favorable long-sequence scaling.\n"
            "- **Jamba:** a hybrid architecture combining transformer and Mamba "
            "layers.\n"
            "\n"
            "The important lesson is not to memorize model names. It is to "
            "understand **why alternatives exist**: researchers want architectures "
            "that retain strong model quality while improving memory, long-context "
            "handling, or computational efficiency.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Model size: parameters are important, but incomplete\n"
            "\n"
            "A model's parameter count is often used as shorthand for its size. "
            "For example, '7B' means roughly seven billion parameters.\n"
            "\n"
            "More parameters generally provide more learning capacity within the "
            "same model family, but parameter count alone does **not** tell you "
            "which model is best.\n"
            "\n"
            "### Parameter count and memory\n"
            "\n"
            "Parameter count gives a rough estimate of the memory needed just to "
            "store weights. If a model has 7 billion parameters and each parameter "
            "uses 2 bytes, the weights alone require at least about 14 GB.\n"
            "\n"
            "Real inference memory can be higher because inference also needs "
            "intermediate state and other memory.\n"
            "\n"
            "### Dense versus sparse models\n"
            "\n"
            "A **dense model** generally uses all of its model parameters in the "
            "normal computation path.\n"
            "\n"
            "A **sparse model** has many parameters that are inactive or zero for "
            "some computation, allowing the nominal parameter count to be larger "
            "than the amount of work actually performed.\n"
            "\n"
            "### Mixture of experts (MoE)\n"
            "\n"
            "A mixture-of-experts model divides parameters into groups called "
            "experts. Only a subset of experts is activated for each token.\n"
            "\n"
            "That means you should distinguish:\n"
            "\n"
            "- **Total parameters:** all parameters available in the model.\n"
            "- **Active parameters:** parameters actually used for a given token.\n"
            "\n"
            "A model can therefore have a very large total parameter count while "
            "requiring computation closer to a much smaller model per token.\n"
            "\n"
            "[[IMAGE_NEEDED: Dense model versus mixture of experts | A simple "
            "diagram where every block is active in a dense model, while a router "
            "sends each token to only a small subset of expert blocks in an MoE "
            "model | Learner should notice the difference between total and "
            "active parameters]]\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Three numbers for understanding model scale\n"
            "\n"
            "The chapter gives three especially useful numbers.\n"
            "\n"
            "### 1. Number of parameters\n"
            "\n"
            "A rough proxy for the model's learning capacity and storage/compute "
            "requirements.\n"
            "\n"
            "### 2. Number of training tokens\n"
            "\n"
            "A proxy for how much language-model training experience the model "
            "received. This is not necessarily identical to the raw dataset size.\n"
            "\n"
            "If a dataset contains 1 trillion tokens and the model trains over it "
            "for two full epochs, the training-token count is 2 trillion.\n"
            "\n"
            "### 3. Number of FLOPs used for training\n"
            "\n"
            "**FLOP** means floating-point operation. The total number of FLOPs "
            "helps describe the computational work required for training.\n"
            "\n"
            "Do not confuse:\n"
            "\n"
            "- **FLOPs:** a count of operations performed for a task.\n"
            "- **FLOP/s:** operations per second, a measure of hardware throughput.\n"
            "\n"
            "Hardware utilization matters too. A GPU's advertised peak throughput "
            "does not mean a real training job sustains that throughput all the "
            "time.\n"
            "\n"
            "### Why model size and data size belong together\n"
            "\n"
            "A huge model trained on almost no data can perform poorly. More "
            "capacity helps only if the training setup provides enough useful data "
            "for the model to learn from.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Scaling laws and compute-optimal training\n"
            "\n"
            "Training large models is a budgeting problem as much as a modeling "
            "problem. Compute costs money, so teams need to decide how to allocate "
            "a fixed compute budget between model size and training data.\n"
            "\n"
            "The chapter introduces the **Chinchilla scaling law**. Its core "
            "intuition is that model size and training-token count should grow "
            "together rather than scaling one while starving the other.\n"
            "\n"
            "The chapter gives the approximate rule from the Chinchilla study:\n"
            "\n"
            "```text\n"
            "training tokens ≈ 20 × number of model parameters\n"
            "```\n"
            "\n"
            "So, using that rule of thumb:\n"
            "\n"
            "```text\n"
            "3 billion parameters -> approximately 60 billion training tokens\n"
            "```\n"
            "\n"
            "This is not a universal law for every modern architecture, sparse "
            "model, or synthetic-data regime. It is a useful illustration of a "
            "more general principle: **a model can be under-trained if its size "
            "grows faster than its useful data.**\n"
            "\n"
            "### Inverse scaling\n"
            "\n"
            "Bigger models often perform better, but not every task improves "
            "monotonically with size. Researchers have identified some cases where "
            "larger models can perform worse, though the chapter notes that strong "
            "real-world inverse-scaling results were difficult to establish.\n"
            "\n"
            "### Scaling extrapolation\n"
            "\n"
            "Large-model training is so expensive that developers may get only a "
            "small number of full training attempts. Researchers therefore study "
            "smaller models and try to predict which hyperparameters will transfer "
            "well to much larger models.\n"
            "\n"
            "Remember the distinction:\n"
            "\n"
            "- **Parameter:** learned during training.\n"
            "- **Hyperparameter:** configured by people, such as number of layers, "
            "learning rate, batch size, or number of epochs.\n"
            "\n"
            "### Scaling bottlenecks\n"
            "\n"
            "The chapter highlights two visible constraints on continued scaling:\n"
            "\n"
            "1. **Training data:** high-quality public human-generated data is "
            "finite, while model datasets have grown rapidly.\n"
            "2. **Electricity:** data centers and training clusters require large "
            "amounts of energy.\n"
            "\n"
            "It also raises a further concern: more of the web is being filled "
            "with AI-generated data, so future models may increasingly encounter "
            "outputs produced by earlier models.\n"
            "\n"
            "{{exercise:M02.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Post-training: turning a completion model into a useful assistant\n"
            "\n"
            "Self-supervised pre-training primarily teaches a model to predict "
            "tokens. That creates capability, but not necessarily the behavior "
            "users expect from an assistant.\n"
            "\n"
            "For example, if a pre-trained completion model sees:\n"
            "\n"
            "```text\n"
            "How to make pizza\n"
            "```\n"
            "\n"
            "it might continue the phrase, add another question, or provide a "
            "recipe. Pure next-token prediction does not inherently mean 'answer "
            "the user's request helpfully.'\n"
            "\n"
            "The chapter describes post-training as commonly having two stages:\n"
            "\n"
            "```text\n"
            "Pre-trained model\n"
            "      |\n"
            "      v\n"
            "Supervised finetuning (SFT)\n"
            "      |\n"
            "      v\n"
            "Preference finetuning\n"
            "      |\n"
            "      v\n"
            "Assistant behavior better aligned with user preferences\n"
            "```\n"
            "\n"
            "### Pre-training versus post-training\n"
            "\n"
            "A useful intuition from the chapter is:\n"
            "\n"
            "- **Pre-training:** learn capabilities and statistical knowledge from "
            "large amounts of data.\n"
            "- **Post-training:** make those capabilities easier and safer to use "
            "in the kinds of interactions people actually want.\n"
            "\n"
            "[[IMAGE_NEEDED: Pre-training to post-training pipeline | A three-stage "
            "diagram showing self-supervised pre-training, supervised finetuning, "
            "and preference finetuning | Learner should notice that conversational "
            "behavior is shaped after the base model has already learned broad "
            "capabilities]]\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Supervised finetuning (SFT)\n"
            "\n"
            "In supervised finetuning, the model is trained on high-quality "
            "**demonstration data**—examples of prompts paired with desirable "
            "responses.\n"
            "\n"
            "```text\n"
            "(prompt, good response)\n"
            "```\n"
            "\n"
            "The idea is similar to demonstration or behavior cloning: show the "
            "model examples of how a useful assistant should behave so that it "
            "learns to reproduce those patterns.\n"
            "\n"
            "A good SFT dataset should cover the range of request types the model "
            "is expected to handle—for example, question answering, summarization, "
            "translation, or other target behaviors.\n"
            "\n"
            "### Why high-quality SFT data is expensive\n"
            "\n"
            "Generating strong demonstration answers can require critical "
            "thinking, research, judgment, and domain knowledge. This is much more "
            "demanding than simple labeling tasks such as marking an image category.\n"
            "\n"
            "The quality and demographics of labelers therefore matter because the "
            "model learns from the behavior they demonstrate.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Preference finetuning, RLHF, DPO, and RLAIF\n"
            "\n"
            "SFT teaches a model how to respond, but it does not fully resolve "
            "which responses people should prefer when multiple possible answers "
            "exist.\n"
            "\n"
            "This is difficult because **human preference is not universal**. "
            "Different people and cultures can disagree about tone, values, "
            "safety, controversial topics, and what counts as a good response.\n"
            "\n"
            "The goal of preference finetuning is to push model behavior toward "
            "responses that score better under a chosen preference process.\n"
            "\n"
            "The chapter mentions several approaches:\n"
            "\n"
            "- **RLHF:** reinforcement learning from human feedback.\n"
            "- **DPO:** Direct Preference Optimization.\n"
            "- **RLAIF:** reinforcement learning from AI feedback.\n"
            "\n"
            "### RLHF in two major steps\n"
            "\n"
            "The chapter presents RLHF at a high level as:\n"
            "\n"
            "1. Train a **reward model** to score responses.\n"
            "2. Further optimize the assistant model to generate responses that "
            "receive higher reward-model scores.\n"
            "\n"
            "### Why comparison data is useful\n"
            "\n"
            "Asking a person to assign an absolute quality score can be "
            "inconsistent. It can be easier to show two responses and ask:\n"
            "\n"
            "```text\n"
            "Which response is better: A or B?\n"
            "```\n"
            "\n"
            "This creates comparison data in the form:\n"
            "\n"
            "```text\n"
            "(prompt, winning_response, losing_response)\n"
            "```\n"
            "\n"
            "The reward model learns to assign a higher score to preferred "
            "responses.\n"
            "\n"
            "### Optimizing against the reward model\n"
            "\n"
            "After the reward model is trained, the assistant can be further "
            "optimized so that its generated responses receive high reward. The "
            "chapter discusses PPO as one reinforcement-learning algorithm used "
            "for this process.\n"
            "\n"
            "### Important limitation\n"
            "\n"
            "A mathematical reward process is only an approximation of diverse "
            "human preferences. Preference finetuning can improve usability, but "
            "it is not a perfect solution to alignment.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Sampling fundamentals: from logits to the next token\n"
            "\n"
            "After training is finished, a model still needs a rule for deciding "
            "what to output. That is where **sampling** enters.\n"
            "\n"
            "For the next token, a language model produces one numerical score "
            "for every token in its vocabulary. These raw scores are called "
            "**logits**.\n"
            "\n"
            "Logits are not probabilities. They can be negative and they do not "
            "sum to one. A **softmax** transformation can convert them into a "
            "probability distribution.\n"
            "\n"
            "```text\n"
            "hidden state\n"
            "    -> logits for vocabulary\n"
            "    -> softmax\n"
            "    -> token probabilities\n"
            "    -> sampling rule\n"
            "    -> chosen next token\n"
            "```\n"
            "\n"
            "### Greedy sampling\n"
            "\n"
            "The simplest approach is always to choose the token with the highest "
            "probability. This is often called greedy decoding/sampling.\n"
            "\n"
            "Greedy choice can be appropriate for some tasks, but for open-ended "
            "language generation it can make outputs repetitive or uninteresting.\n"
            "\n"
            "[[IMAGE_NEEDED: Logits to sampled token | A pipeline showing a vector "
            "of raw logits, softmax converting them to probabilities, and one "
            "token being selected according to a sampling strategy | Learner "
            "should notice that the model first scores all candidate tokens and "
            "sampling happens only after those scores are produced]]\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Temperature: controlling probability sharpness\n"
            "\n"
            "**Temperature** changes the shape of the probability distribution "
            "before sampling.\n"
            "\n"
            "The chapter describes the intuition this way:\n"
            "\n"
            "- **Lower temperature:** concentrate more probability on the most "
            "likely tokens -> more predictable output.\n"
            "- **Higher temperature:** spread more probability toward less likely "
            "tokens -> more diverse and potentially more creative output.\n"
            "\n"
            "Temperature operates by dividing logits by a temperature value before "
            "softmax.\n"
            "\n"
            "The chapter uses a simple two-logit example `[1, 2]`:\n"
            "\n"
            "- At temperature 1, the probabilities are approximately `[0.27, 0.73]`.\n"
            "- At temperature 0.5, they become approximately `[0.12, 0.88]`.\n"
            "\n"
            "So lower temperature makes the larger logit dominate more strongly.\n"
            "\n"
            "When an API exposes temperature `0`, the practical behavior is often "
            "to choose the highest-logit token directly rather than literally "
            "divide logits by zero.\n"
            "\n"
            "### Log probabilities\n"
            "\n"
            "Model providers may expose **logprobs**, which are probabilities "
            "represented in logarithmic form. Log space is useful because token "
            "probabilities can become extremely small and because products of "
            "probabilities become sums of log probabilities.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Top-k, top-p, and min-p\n"
            "\n"
            "Temperature reshapes probabilities. Other sampling methods restrict "
            "which tokens are eligible at all.\n"
            "\n"
            "### Top-k\n"
            "\n"
            "Keep only the `k` tokens with the highest logits/probabilities, then "
            "sample from this smaller set.\n"
            "\n"
            "A small `k` gives the model fewer possible next tokens and therefore "
            "tends to make output more predictable.\n"
            "\n"
            "### Top-p / nucleus sampling\n"
            "\n"
            "Instead of keeping a fixed number of tokens, sort tokens from most to "
            "least probable and keep the smallest set whose cumulative probability "
            "reaches a threshold `p`.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "yes   = 0.70\n"
            "maybe = 0.22\n"
            "no    = 0.06\n"
            "other = 0.02\n"
            "```\n"
            "\n"
            "With `top_p = 0.90`, the candidate set would include `yes` and "
            "`maybe`, because their cumulative probability already exceeds 0.90.\n"
            "\n"
            "Unlike top-k, the number of allowed candidates changes with the "
            "context.\n"
            "\n"
            "### Min-p\n"
            "\n"
            "A related strategy requires candidate tokens to pass a minimum "
            "probability threshold.\n"
            "\n"
            "[[IMAGE_NEEDED: Top-k versus top-p | A token-probability bar chart "
            "showing top-k selecting a fixed number of highest tokens while top-p "
            "selects however many tokens are needed to reach a cumulative "
            "probability threshold | Learner should notice that top-k fixes the "
            "count while top-p adapts the count to the distribution]]\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Stopping conditions and test-time compute\n"
            "\n"
            "### Stopping conditions\n"
            "\n"
            "Autoregressive models can continue generating token after token. "
            "Longer outputs increase latency and compute cost, so applications "
            "often define stopping rules.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- Maximum token length.\n"
            "- End-of-sequence token.\n"
            "- Application-specific stop strings.\n"
            "\n"
            "Be careful: stopping too early can produce malformed output, such as "
            "JSON missing a closing bracket.\n"
            "\n"
            "### Test-time compute\n"
            "\n"
            "Instead of generating one answer, an application can generate "
            "multiple candidates and choose among them.\n"
            "\n"
            "This can improve quality because more attempts increase the chance of "
            "finding a strong answer. But it also increases inference cost.\n"
            "\n"
            "Common ideas from the chapter include:\n"
            "\n"
            "- **Best of N:** sample several complete responses and select the best.\n"
            "- **Beam search:** maintain a fixed number of promising candidate "
            "sequences during generation.\n"
            "- **Reward model / verifier:** score candidates and select the "
            "highest-quality one.\n"
            "- **Average logprob:** compare candidates using their average token "
            "log probability rather than raw total log probability, which would "
            "bias against longer outputs.\n"
            "- **Majority / self-consistency style selection:** solve an exact-answer "
            "task several times and choose the most frequent answer.\n"
            "- **Application heuristics:** select the shortest valid answer, first "
            "valid answer, valid SQL query, or another task-specific criterion.\n"
            "\n"
            "### More samples are not free\n"
            "\n"
            "Generating two responses is roughly twice the generation work of "
            "generating one. Test-time compute is therefore a tradeoff between "
            "quality and cost/latency.\n"
            "\n"
            "The chapter also emphasizes **robustness**: a robust model should not "
            "change dramatically under small input variations. When a model is "
            "brittle, multiple attempts can sometimes reduce failure rates.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Getting structured outputs reliably\n"
            "\n"
            "Many applications need machine-readable outputs such as JSON, YAML, "
            "CSV, regex, or a fixed set of labels. A response that is 'almost "
            "valid JSON' may still break your program.\n"
            "\n"
            "The chapter describes several approaches.\n"
            "\n"
            "### Approach 1: Prompting\n"
            "\n"
            "Tell the model clearly which format to produce and show examples if "
            "helpful. This is the simplest first step, but it cannot guarantee "
            "perfect compliance.\n"
            "\n"
            "### Approach 2: Validation / extra model call\n"
            "\n"
            "Generate an answer, then use another model step to validate or repair "
            "it. This can improve validity but adds cost and latency.\n"
            "\n"
            "### Approach 3: Post-processing\n"
            "\n"
            "If errors are predictable and simple—for example, a missing closing "
            "character—a deterministic parser or repair script can fix them "
            "cheaply.\n"
            "\n"
            "### Approach 4: Constrained sampling\n"
            "\n"
            "Filter the model's candidate logits so it can sample only tokens that "
            "remain valid under a target grammar.\n"
            "\n"
            "For example, a JSON grammar can restrict which tokens are legal after "
            "an opening brace or inside a string.\n"
            "\n"
            "Constrained sampling is more reliable but requires grammar support and "
            "can add complexity and latency.\n"
            "\n"
            "### Approach 5: Finetuning\n"
            "\n"
            "Train the model on many examples that follow the desired format. This "
            "can make format adherence much more reliable than prompting alone.\n"
            "\n"
            "For classification, you can even modify the architecture with a "
            "classifier head so that only predefined classes can be produced.\n"
            "\n"
            "A useful escalation path is:\n"
            "\n"
            "```text\n"
            "Prompting\n"
            "   -> repair / validation\n"
            "   -> constrained sampling\n"
            "   -> finetuning / architecture changes when needed\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Constrained sampling for structured output | A "
            "diagram showing raw logits over many tokens being filtered by a "
            "grammar so that only tokens valid for the target structure remain "
            "before sampling | Learner should notice that invalid tokens can be "
            "prevented during generation instead of repaired afterward]]\n"
            "\n"
            "{{exercise:M02.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 21. The probabilistic nature of AI\n"
            "\n"
            "Sampling means a model can produce different outputs for the same "
            "input. This is very different from traditional deterministic "
            "software, where the same input normally follows the same programmed "
            "path.\n"
            "\n"
            "The probabilistic nature is both useful and difficult:\n"
            "\n"
            "- It supports creativity and varied generations.\n"
            "- It can produce inconsistency.\n"
            "- It can contribute to factual unreliability and hallucinations.\n"
            "\n"
            "A foundation model represents many possible continuations, including "
            "rare and undesirable ones. If a continuation has non-zero probability, "
            "sampling can potentially surface it.\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Inconsistency\n"
            "\n"
            "The chapter describes two forms of inconsistency.\n"
            "\n"
            "### Same input, different outputs\n"
            "\n"
            "You send exactly the same prompt twice and receive substantially "
            "different answers.\n"
            "\n"
            "Possible mitigations include:\n"
            "\n"
            "- Cache the response when identical inputs should return identical "
            "results.\n"
            "- Fix temperature, top-k, and top-p settings.\n"
            "- Fix a random seed when the serving stack supports it.\n"
            "\n"
            "Even then, perfect reproducibility is not guaranteed because hardware "
            "and serving implementation details can influence computation.\n"
            "\n"
            "### Slightly different input, drastically different output\n"
            "\n"
            "A tiny wording or formatting change produces a very different result. "
            "This is harder to solve because it reflects model brittleness rather "
            "than only sampling randomness.\n"
            "\n"
            "Careful prompting and memory/context design can help, but the broader "
            "lesson is to **evaluate robustness rather than assuming it**.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Hallucinations: why fluent text can still be wrong\n"
            "\n"
            "A hallucination is an output that is not grounded in facts. This is "
            "especially dangerous in applications where factual correctness is "
            "critical.\n"
            "\n"
            "The chapter emphasizes that hallucination is not explained by random "
            "sampling alone. It discusses two hypotheses.\n"
            "\n"
            "### Hypothesis 1: self-delusion / snowballing\n"
            "\n"
            "After the model generates a wrong statement, later tokens are "
            "conditioned on that generated statement. The model can therefore "
            "continue building on its own mistake as if the mistake were part of "
            "the original context.\n"
            "\n"
            "```text\n"
            "wrong early assumption\n"
            "      -> next token conditioned on wrong assumption\n"
            "      -> more supporting-looking text\n"
            "      -> larger hallucinated story\n"
            "```\n"
            "\n"
            "### Hypothesis 2: mismatch between labeler knowledge and model knowledge\n"
            "\n"
            "During supervised finetuning, labelers can write answers using facts "
            "they know. If the base model does not actually contain or reliably "
            "represent that knowledge, imitation training may encourage it to "
            "produce an answer style even when it lacks the necessary factual "
            "basis.\n"
            "\n"
            "### Mitigation ideas discussed in the chapter\n"
            "\n"
            "- Train or reward the model to distinguish supplied evidence from "
            "its own generated tokens.\n"
            "- Use factual/counterfactual training signals.\n"
            "- Ask for verification or sources.\n"
            "- Use reward objectives that penalize fabrication more strongly.\n"
            "- Prompt the model to acknowledge uncertainty.\n"
            "- Prefer concise answers when unnecessary generation increases risk.\n"
            "- Improve context construction.\n"
            "\n"
            "The chapter also cautions that no single technique completely solves "
            "hallucination. Some alignment methods can improve overall preference "
            "while not improving every factuality metric.\n"
            "\n"
            "[[IMAGE_NEEDED: Snowballing hallucination | A causal chain showing an "
            "initial incorrect generated assumption followed by several later "
            "tokens/statements that become increasingly wrong because they are "
            "conditioned on the first mistake | Learner should notice how an early "
            "error can compound during autoregressive generation]]\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> The largest model is always the best model.\n"
            "\n"
            "**Why this is wrong:** performance depends on architecture, training "
            "data, training amount, post-training, and task fit. Larger models also "
            "cost more to serve and can be harder to deploy.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> More training data always improves a model.\n"
            "\n"
            "**Why this is wrong:** low-quality, irrelevant, or badly distributed "
            "data can waste compute and fail to improve the target task.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> Temperature changes what the model knows.\n"
            "\n"
            "**Why this is wrong:** temperature changes the distribution used for "
            "sampling; it does not add knowledge or retrain model weights.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> Post-training gives the model all of its knowledge.\n"
            "\n"
            "**Why this is wrong:** pre-training is where broad capabilities and "
            "statistical knowledge are primarily learned. Post-training mainly "
            "shapes how those capabilities are expressed to users.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> Setting temperature to zero guarantees a completely deterministic "
            "application.\n"
            "\n"
            "**Why this is wrong:** reducing sampling randomness improves "
            "consistency, but serving hardware, implementation details, and input "
            "sensitivity can still produce variation.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> Valid-looking structured output is automatically correct.\n"
            "\n"
            "**Why this is wrong:** grammar validity and factual/semantic "
            "correctness are separate properties. Perfect JSON can still contain "
            "the wrong answer.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Training-data distribution | How examples are spread across languages, domains, tasks, styles, and other categories. |\n"
            "| Low-resource language | A language with relatively limited training-data availability. |\n"
            "| Domain-specific model | A model designed or adapted for a specialized data domain or task. |\n"
            "| Transformer | A neural architecture built around attention and highly parallelizable input processing. |\n"
            "| Attention | A mechanism that weights which previous representations matter for the current computation. |\n"
            "| Query (Q) | Representation of what the current attention computation is looking for. |\n"
            "| Key (K) | Representation used to measure a token's relevance to a query. |\n"
            "| Value (V) | Information contributed by a token after relevance is determined. |\n"
            "| Prefill | Inference stage that processes the input context and prepares state for generation. |\n"
            "| Decode | Autoregressive stage that generates output one token at a time. |\n"
            "| Transformer block | Repeated model unit containing attention and feedforward/MLP computation. |\n"
            "| Parameter | A value learned by the model during training. |\n"
            "| Hyperparameter | A user-configured setting controlling architecture or training. |\n"
            "| Dense model | A model whose normal computation uses its parameter blocks broadly rather than routing through sparse experts. |\n"
            "| Sparse model | A model where only part of the full parameter set may be active or non-zero for computation. |\n"
            "| Mixture of experts (MoE) | Sparse architecture that routes each token through only a subset of expert parameter groups. |\n"
            "| Training token | A token actually processed during model training; repeated epochs count tokens repeatedly. |\n"
            "| FLOP | One floating-point operation; total FLOPs measure computational work. |\n"
            "| FLOP/s | Floating-point operations per second; a throughput measure. |\n"
            "| Scaling law | An empirical relationship linking model/data/compute scale to expected training behavior or performance. |\n"
            "| SFT | Supervised finetuning on prompt-response demonstrations. |\n"
            "| Preference finetuning | Further training intended to favor responses judged preferable under a preference process. |\n"
            "| RLHF | Reinforcement learning from human feedback. |\n"
            "| DPO | Direct Preference Optimization, a preference-optimization approach. |\n"
            "| RLAIF | Reinforcement learning from AI feedback. |\n"
            "| Reward model | A model that assigns a quality/preference score to a response. |\n"
            "| Logit | Raw model score for a possible output token before probability normalization. |\n"
            "| Softmax | Function commonly used to convert logits into a probability distribution. |\n"
            "| Logprob | Probability represented in log space. |\n"
            "| Temperature | Sampling control that changes how sharp or flat the token probability distribution is. |\n"
            "| Top-k | Sampling from only the k highest-scoring candidates. |\n"
            "| Top-p | Sampling from the smallest high-probability candidate set whose cumulative probability reaches p. |\n"
            "| Test-time compute | Spending additional inference compute, often by generating/evaluating multiple outputs. |\n"
            "| Constrained sampling | Restricting candidate tokens so generated output obeys a grammar or other constraint. |\n"
            "| Robustness | Stability of model behavior under small changes in the input. |\n"
            "| Hallucination | Generated content that is not grounded in facts. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why can a huge web dataset still produce a model that is weak for your application?\n"
            "2. How can language representation affect both model quality and inference cost?\n"
            "3. Why might a domain-specific model outperform a general-purpose model?\n"
            "4. What two problems of basic seq2seq systems helped motivate transformers?\n"
            "5. Explain Q, K, and V using your own analogy.\n"
            "6. What is the difference between prefill and decode?\n"
            "7. What are the two major modules in a typical transformer block?\n"
            "8. Why does parameter count alone not determine model quality?\n"
            "9. What is the difference between total and active parameters in an MoE model?\n"
            "10. What do parameters, training tokens, and FLOPs each tell you?\n"
            "11. What is the intuition behind compute-optimal scaling?\n"
            "12. What is the difference between a parameter and a hyperparameter?\n"
            "13. Why are training data and electricity potential scaling bottlenecks?\n"
            "14. What does SFT teach that plain next-token pre-training does not directly guarantee?\n"
            "15. Why is comparison data useful for training a reward model?\n"
            "16. How do RLHF and DPO relate to preference finetuning?\n"
            "17. What is the difference between a logit and a probability?\n"
            "18. What happens to output diversity when temperature decreases?\n"
            "19. How do top-k and top-p differ?\n"
            "20. Why can test-time compute improve quality, and what does it cost?\n"
            "21. Compare prompting, post-processing, constrained sampling, and finetuning for structured outputs.\n"
            "22. What are the two forms of inconsistency discussed in the chapter?\n"
            "23. Explain snowballing hallucination in your own words.\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A foundation model's behavior is not determined by one thing called "
            "'intelligence.' It is the result of data distribution, architecture, "
            "scale, post-training, and sampling. Understanding those pieces helps "
            "you choose models intelligently, predict their failure modes, and "
            "design more reliable AI applications.**\n"
        ),

        "estimated_minutes": 240,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "big-picture", "title": "What shapes a foundation model?", "order": 1},
            {"id": "training-data", "title": "Training data", "order": 2},
            {"id": "multilingual-models", "title": "Multilingual models", "order": 3},
            {"id": "domain-specific-models", "title": "Domain-specific models", "order": 4},
            {"id": "seq2seq-to-transformer", "title": "From seq2seq to transformers", "order": 5},
            {"id": "attention", "title": "Attention: query, key, and value", "order": 6},
            {"id": "prefill-decode", "title": "Prefill and decode", "order": 7},
            {"id": "transformer-block", "title": "Inside a transformer", "order": 8},
            {"id": "alternative-architectures", "title": "Alternative architectures", "order": 9},
            {"id": "model-size", "title": "Model size", "order": 10},
            {"id": "scale-numbers", "title": "Three numbers for model scale", "order": 11},
            {"id": "scaling-laws", "title": "Scaling laws", "order": 12},
            {"id": "post-training", "title": "Post-training", "order": 13},
            {"id": "sft", "title": "Supervised finetuning", "order": 14},
            {"id": "preference-finetuning", "title": "Preference finetuning", "order": 15},
            {"id": "sampling-fundamentals", "title": "Sampling fundamentals", "order": 16},
            {"id": "temperature", "title": "Temperature", "order": 17},
            {"id": "top-k-top-p", "title": "Top-k, top-p, and min-p", "order": 18},
            {"id": "stopping-and-test-time-compute", "title": "Stopping and test-time compute", "order": 19},
            {"id": "structured-outputs", "title": "Structured outputs", "order": 20},
            {"id": "probabilistic-nature", "title": "The probabilistic nature of AI", "order": 21},
            {"id": "inconsistency", "title": "Inconsistency", "order": 22},
            {"id": "hallucinations", "title": "Hallucinations", "order": 23},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M02.L01.EX01",

            "title": "Choose the Better Foundation Model",

            "lesson_code": "M02.L01",

            "section_id": "scaling-laws",

            "placement": "after_section",

            "description": (
                "Practice reasoning about training data, model architecture, "
                "scale, and deployment tradeoffs instead of choosing a model "
                "from parameter count alone."
            ),

            "instructions": (
                "Imagine you are choosing between two models for an Arabic "
                "domain-specific assistant.\n\n"
                "Model A: 70B dense parameters, mostly English web data, very "
                "strong English benchmark scores, expensive inference.\n"
                "Model B: 13B parameters, substantially more Arabic and domain "
                "data, lower memory requirement, weaker general English scores.\n\n"
                "1. List at least four pieces of information you would need before "
                "making the decision.\n"
                "2. Explain why 70B versus 13B is not enough information.\n"
                "3. Explain how language distribution and tokenization might affect "
                "quality, cost, and latency.\n"
                "4. Explain how training-token count matters alongside parameter count.\n"
                "5. State one reason Model B could outperform Model A for this "
                "specific application.\n"
                "6. State one reason Model A could still be preferable.\n"
                "7. Propose a small evaluation you would run before deployment."
            ),

            "expected_output": (
                "A short model-selection analysis that discusses training data, "
                "language coverage, model size, training amount, serving cost, "
                "latency, task fit, and evaluation rather than relying on model "
                "parameter count alone."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "training-data-reasoning",
                "model-selection",
                "model-scaling",
                "multilingual-ai",
                "deployment-tradeoffs",
            ],
        },

        {
            "id": "M02.L01.EX02",

            "title": "Design a Reliable Structured-Output Pipeline",

            "lesson_code": "M02.L01",

            "section_id": "structured-outputs",

            "placement": "after_section",

            "description": (
                "Use sampling and structured-output concepts to design a more "
                "reliable extraction workflow."
            ),

            "instructions": (
                "You are building an application that extracts invoice fields and "
                "must return valid JSON.\n\n"
                "1. Define the required JSON fields.\n"
                "2. Describe your first prompting approach.\n"
                "3. Explain what you would do if 5% of outputs are invalid JSON.\n"
                "4. Compare deterministic post-processing with constrained sampling.\n"
                "5. Explain when you would consider finetuning.\n"
                "6. Choose a temperature strategy and justify it.\n"
                "7. Decide whether top-k or top-p matters for this task and explain why.\n"
                "8. Define a stopping rule that reduces the chance of truncated JSON.\n"
                "9. Describe how you would use validation or test-time compute if "
                "the extraction itself is sometimes wrong even when the JSON is valid.\n"
                "10. Identify one hallucination risk and one inconsistency risk."
            ),

            "expected_output": (
                "A structured design for an invoice-extraction pipeline that "
                "separates format validity from factual correctness and uses "
                "appropriate prompting, sampling, validation, and reliability "
                "controls."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "sampling-strategy",
                "structured-output-design",
                "reliability",
                "hallucination-awareness",
                "ai-application-engineering",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M02.L01.QZ01",

        "title": "Understanding Foundation Models — Knowledge Check",

        "lesson_code": "M02.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M02.L01.Q01",
                "section_id": "training-data",
                "question": (
                    "Which statement best reflects the chapter's treatment of "
                    "training data?"
                ),
                "options": [
                    "The largest dataset is always the best dataset",
                    "Training-data quantity matters, but quality and diversity "
                    "also affect model capability",
                    "Web data is automatically clean enough for any task",
                    "Training data matters only for small models",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter emphasizes quantity, quality, and diversity "
                    "rather than treating raw dataset size as sufficient."
                ),
            },

            {
                "id": "M02.L01.Q02",
                "section_id": "multilingual-models",
                "question": (
                    "Why can the same meaning cost more to process in one language "
                    "than another?"
                ),
                "options": [
                    "Every language uses a different neural network",
                    "Different tokenizers can require different numbers of tokens "
                    "for equivalent content",
                    "The model always translates everything to English",
                    "Only English uses autoregressive generation",
                ],
                "correct": 1,
                "explanation": (
                    "Inference cost and latency can scale with token count, and "
                    "tokenization efficiency can differ substantially by language."
                ),
            },

            {
                "id": "M02.L01.Q03",
                "section_id": "seq2seq-to-transformer",
                "question": (
                    "Which transformer property directly addresses the sequential "
                    "input-processing bottleneck of RNN-based seq2seq systems?"
                ),
                "options": [
                    "Input tokens can be processed with much greater parallelism",
                    "The transformer removes all matrix operations",
                    "The transformer generates all output tokens simultaneously",
                    "The transformer requires no training data",
                ],
                "correct": 0,
                "explanation": (
                    "Transformers remove the RNN requirement, allowing input "
                    "processing to be much more parallelizable. Autoregressive "
                    "output generation is still sequential."
                ),
            },

            {
                "id": "M02.L01.Q04",
                "section_id": "attention",
                "question": (
                    "In the chapter's attention explanation, what role does the "
                    "key vector primarily play?"
                ),
                "options": [
                    "It stores the final sampled token",
                    "It helps determine how relevant a previous token is to the query",
                    "It defines the model's training dataset",
                    "It replaces the value vector entirely",
                ],
                "correct": 1,
                "explanation": (
                    "The query is compared with keys to determine relevance; the "
                    "associated values provide the information that contributes "
                    "to the attention result."
                ),
            },

            {
                "id": "M02.L01.Q05",
                "section_id": "prefill-decode",
                "question": (
                    "Which statement correctly distinguishes prefill and decode?"
                ),
                "options": [
                    "Prefill generates all output tokens; decode trains the model",
                    "Prefill processes input context; decode generates output "
                    "tokens autoregressively",
                    "Prefill performs RLHF; decode performs SFT",
                    "They are two names for the same training stage",
                ],
                "correct": 1,
                "explanation": (
                    "Prefill processes prompt context and creates state for "
                    "generation, while decode produces output sequentially."
                ),
            },

            {
                "id": "M02.L01.Q06",
                "section_id": "model-size",
                "question": (
                    "Why can an MoE model have many total parameters without using "
                    "all of them for each token?"
                ),
                "options": [
                    "MoE deletes parameters after training",
                    "A router activates only a subset of experts for each token",
                    "All parameters are stored as text",
                    "MoE models do not use neural-network weights",
                ],
                "correct": 1,
                "explanation": (
                    "Mixture-of-experts architectures route each token through only "
                    "a subset of expert parameter groups."
                ),
            },

            {
                "id": "M02.L01.Q07",
                "section_id": "scale-numbers",
                "question": (
                    "Which three numbers does the chapter highlight as useful "
                    "signals of model scale?"
                ),
                "options": [
                    "Parameters, training tokens, and training FLOPs",
                    "Temperature, top-k, and top-p",
                    "Accuracy, recall, and precision",
                    "Prompt length, answer length, and user count",
                ],
                "correct": 0,
                "explanation": (
                    "Parameter count approximates capacity, training tokens "
                    "approximate training exposure, and FLOPs approximate compute "
                    "used for training."
                ),
            },

            {
                "id": "M02.L01.Q08",
                "section_id": "scaling-laws",
                "question": (
                    "What is the main intuition behind compute-optimal scaling?"
                ),
                "options": [
                    "Always maximize parameter count regardless of data",
                    "Balance model size and training data under a fixed compute budget",
                    "Use the highest temperature during training",
                    "Remove the need for evaluation",
                ],
                "correct": 1,
                "explanation": (
                    "Scaling laws help reason about allocating finite compute "
                    "between model capacity and training data rather than blindly "
                    "maximizing one dimension."
                ),
            },

            {
                "id": "M02.L01.Q09",
                "section_id": "sft",
                "question": (
                    "What is demonstration data in supervised finetuning?"
                ),
                "options": [
                    "Only unlabeled web pages",
                    "Prompt-response examples showing desired behavior",
                    "The model's GPU utilization logs",
                    "Random logits sampled before training",
                ],
                "correct": 1,
                "explanation": (
                    "SFT commonly uses high-quality prompt-response pairs to teach "
                    "the model useful conversational behavior."
                ),
            },

            {
                "id": "M02.L01.Q10",
                "section_id": "preference-finetuning",
                "question": (
                    "Why is pairwise comparison data useful for a reward model?"
                ),
                "options": [
                    "People can often choose which of two responses is better more "
                    "consistently than assign perfect absolute scores",
                    "It guarantees universal human agreement",
                    "It removes the need for any model training",
                    "It makes all responses deterministic",
                ],
                "correct": 0,
                "explanation": (
                    "Relative comparison can be easier and more consistent than "
                    "independent absolute scoring, though disagreement still exists."
                ),
            },

            {
                "id": "M02.L01.Q11",
                "section_id": "sampling-fundamentals",
                "question": "What is a logit?",
                "options": [
                    "A raw model score for a possible output before probability normalization",
                    "A guaranteed factual answer",
                    "A human preference label",
                    "A model parameter count",
                ],
                "correct": 0,
                "explanation": (
                    "A language model produces logits over vocabulary tokens; a "
                    "function such as softmax converts them into probabilities."
                ),
            },

            {
                "id": "M02.L01.Q12",
                "section_id": "temperature",
                "question": (
                    "What generally happens when sampling temperature decreases?"
                ),
                "options": [
                    "Probability becomes more concentrated on high-logit tokens",
                    "The model gains new training knowledge",
                    "The vocabulary becomes larger",
                    "The model performs post-training automatically",
                ],
                "correct": 0,
                "explanation": (
                    "Lower temperature makes the distribution sharper and outputs "
                    "more predictable; it does not change the model's learned weights."
                ),
            },

            {
                "id": "M02.L01.Q13",
                "section_id": "top-k-top-p",
                "question": "What is the main difference between top-k and top-p?",
                "options": [
                    "Top-k keeps a fixed number of candidates; top-p keeps enough "
                    "high-probability candidates to reach a cumulative threshold",
                    "Top-p changes model weights; top-k does not",
                    "Top-k is training; top-p is inference",
                    "There is no difference",
                ],
                "correct": 0,
                "explanation": (
                    "Top-k fixes the number of eligible candidates, while top-p "
                    "adapts the candidate count to the probability distribution."
                ),
            },

            {
                "id": "M02.L01.Q14",
                "section_id": "stopping-and-test-time-compute",
                "question": (
                    "What is the main tradeoff of generating multiple responses "
                    "and selecting the best one?"
                ),
                "options": [
                    "Potentially better output quality at the cost of more inference compute",
                    "Lower model quality but free inference",
                    "Automatic retraining with no extra cost",
                    "Elimination of all hallucinations",
                ],
                "correct": 0,
                "explanation": (
                    "Test-time compute can improve the chance of a good result but "
                    "requires additional generation and selection work."
                ),
            },

            {
                "id": "M02.L01.Q15",
                "section_id": "structured-outputs",
                "question": (
                    "Which method can prevent invalid next tokens from being "
                    "sampled according to a target grammar?"
                ),
                "options": [
                    "Constrained sampling",
                    "Increasing dataset size only",
                    "Randomly increasing temperature",
                    "Removing the output parser",
                ],
                "correct": 0,
                "explanation": (
                    "Constrained sampling filters candidate tokens according to "
                    "the grammar or structural constraints of the target output."
                ),
            },

            {
                "id": "M02.L01.Q16",
                "section_id": "inconsistency",
                "question": (
                    "Why does setting sampling variables consistently not "
                    "guarantee perfect reproducibility?"
                ),
                "options": [
                    "Serving and hardware details can still influence computation, "
                    "and models can also be sensitive to small input changes",
                    "Sampling variables are used only during pre-training",
                    "The model loses its vocabulary after inference",
                    "Temperature always changes model weights",
                ],
                "correct": 0,
                "explanation": (
                    "Sampling control improves consistency but does not remove all "
                    "sources of nondeterminism or model brittleness."
                ),
            },

            {
                "id": "M02.L01.Q17",
                "section_id": "hallucinations",
                "type": "open",
                "question": (
                    "Explain snowballing hallucination using a simple example. "
                    "Then name two mitigation ideas discussed in the lesson and "
                    "explain why neither should be treated as a perfect guarantee."
                ),
            },
        ],

        "passing_score": 70,
    },
}
