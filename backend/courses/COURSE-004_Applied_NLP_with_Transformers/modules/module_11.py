"""M01.L09 — Future Directions.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-004, Chapter 11.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L09"
MODULE_ORDER = 11
MODULE_TITLE = "Transformer Frontiers: Scaling, Efficient Attention & Multimodal Systems"
MODULE_DESCRIPTION = (
    "Explore the research directions that push transformers beyond their original "
    "limits: scaling, efficient attention, long-context processing, vision, tables, "
    "audio, and multimodal learning."
)

SOURCE_CHAPTER = 11
SOURCE_PAGES = "Chapter 11"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Future Directions",
    "slug": "applied-nlp-transformers-m01-l09-future-directions",
    "description": (
        "Understand the chapter's research frontier: transformer scaling laws, the practical "
        "costs of large models, sparse and linearized attention, vision and table transformers, "
        "speech models, and multimodal systems such as VQA, LayoutLM, DALL-E, and CLIP."
    ),
    "order": 9,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 2.0,
    "skill_tags": [
        "scaling-laws",
        "efficient-attention",
        "sparse-attention",
        "linear-attention",
        "vision-transformers",
        "table-question-answering",
        "speech-recognition",
        "multimodal-transformers",
        "clip",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
        "M01.L06",
        "M01.L07",
        "M01.L08",
    ],

    "lesson": {
        "title": "Future Directions",

        "content": (
            "# Future Directions\n"
            "\n"
            "> **Course:** Applied NLP with Transformers  \n"
            "> **Lesson:** M01.L09  \n"
            "> **Module:** Transformer Foundations  \n"
            "> **Source alignment:** BOOK-004, Chapter 11. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text. The chapter reflects the transformer research landscape "
            "described by the source at the time it was written.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the chapter's argument for scaling model size, data, and compute together.\n"
            "- Describe scaling laws and their power-law intuition.\n"
            "- Explain why large-model training creates infrastructure, cost, data, evaluation, "
            "and deployment challenges.\n"
            "- Explain why standard self-attention becomes expensive for long sequences.\n"
            "- Describe global, band, dilated, random, and block-local sparse attention patterns.\n"
            "- Explain how Longformer and BigBird combine sparse attention patterns.\n"
            "- Explain the core idea behind linearized attention.\n"
            "- Describe how transformers can process images using iGPT and Vision Transformer.\n"
            "- Explain how TAPAS enables natural-language questions over tables.\n"
            "- Describe wav2vec 2.0 and the role of self-supervised speech pretraining.\n"
            "- Explain how multimodal systems combine vision and language.\n"
            "- Compare VQA-style models, LayoutLM, DALL-E, and CLIP at a conceptual level.\n"
            "- Identify practical ways to continue learning after completing the course.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Three directions pushing transformers forward\n"
            "\n"
            "The chapter closes the book by shifting from established transformer applications "
            "to open research directions.\n"
            "\n"
            "It focuses on three broad themes:\n"
            "\n"
            "1. **Scaling transformers** — larger models, larger datasets, and more compute.\n"
            "2. **Making attention more efficient** — especially for long sequences.\n"
            "3. **Going beyond text** — applying transformers to vision, tables, audio, and "
            "multiple modalities at once.\n"
            "\n"
            "These three directions attack different limitations:\n"
            "\n"
            "| Limitation | Research direction |\n"
            "|---|---|\n"
            "| Performance ceiling | Scale model/data/compute |\n"
            "| Long-sequence cost | Efficient attention |\n"
            "| Text-only understanding | Vision, audio, tables, multimodal models |\n"
            "\n"
            '{{image:transformer-research-directions}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 2. The scaling mindset and the 'bitter lesson'\n"
            "\n"
            "The chapter opens with Richard Sutton's argument that general methods that can "
            "effectively exploit more computation often outperform systems that depend heavily "
            "on hand-designed human knowledge.\n"
            "\n"
            "The chapter connects this idea to transformers.\n"
            "\n"
            "Early BERT and GPT descendants often introduced architectural or objective changes. "
            "But the source observes that some of the strongest models of its period were instead "
            "very large versions of relatively simple transformer designs.\n"
            "\n"
            "The broad lesson is not:\n"
            "\n"
            "> Architecture no longer matters.\n"
            "\n"
            "It is:\n"
            "\n"
            "> **General methods that continue improving as compute and data scale can be extremely powerful.**\n"
            "\n"
            "The chapter notes that model parameter counts increased by several orders of magnitude "
            "in only a few years after the original Transformer architecture.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Scaling laws: performance changes predictably with scale\n"
            "\n"
            "Scaling laws study how language-model loss changes when we vary three major quantities:\n"
            "\n"
            "- **N** — model size / number of parameters,\n"
            "- **D** — dataset size,\n"
            "- **C** — compute budget.\n"
            "\n"
            "The chapter describes empirical relationships where test loss follows a smooth "
            "power-law pattern as these quantities increase.\n"
            "\n"
            "On a log-log plot, a power law becomes approximately linear.\n"
            "\n"
            "This matters because a smaller, cheaper experiment can sometimes help estimate "
            "how a much larger training run might behave.\n"
            "\n"
            "### Main conclusions from the chapter\n"
            "\n"
            "#### Scale model, data, and compute together\n"
            "\n"
            "Increasing only one dimension can lead to diminishing returns. The chapter argues "
            "for coordinated scaling of model capacity, training data, and compute.\n"
            "\n"
            "#### Larger models can be more sample-efficient\n"
            "\n"
            "A larger model may reach a given performance level in fewer training steps than a "
            "smaller model.\n"
            "\n"
            "#### Early trends can be useful\n"
            "\n"
            "The smoothness of scaling curves makes extrapolation possible, at least approximately.\n"
            "\n"
            "[[IMAGE_NEEDED: Scaling laws on log-log axes | "
            "Three small charts showing test loss decreasing smoothly as compute, dataset size, "
            "and model size increase, with approximately straight trends on log-log axes | "
            "Learner should notice the similar power-law shape across N, D, and C]]\n"
            "\n"
            "{{exercise:M01.L09.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Scaling is not 'just add more layers'\n"
            "\n"
            "Large-model scaling introduces engineering and organizational problems that do "
            "not appear in small experiments.\n"
            "\n"
            "The chapter highlights five major challenges.\n"
            "\n"
            "### Infrastructure\n"
            "\n"
            "Training across hundreds or thousands of accelerators requires distributed systems, "
            "fast communication, careful orchestration, and specialized engineering skills.\n"
            "\n"
            "### Cost\n"
            "\n"
            "Large training runs can cost millions of dollars. Experiment design therefore "
            "becomes a resource-planning problem as well as a modeling problem.\n"
            "\n"
            "### Dataset curation\n"
            "\n"
            "Huge datasets are difficult to clean and audit. Problems include:\n"
            "\n"
            "- low-quality text,\n"
            "- social bias,\n"
            "- licensing constraints,\n"
            "- personal information,\n"
            "- expensive preprocessing.\n"
            "\n"
            "### Model evaluation\n"
            "\n"
            "A large model must be tested on downstream capability, bias, toxicity, and other "
            "undesirable behavior. Evaluation itself can become expensive.\n"
            "\n"
            "### Deployment\n"
            "\n"
            "Serving a model that occupies tens or hundreds of gigabytes creates memory, latency, "
            "and infrastructure challenges even after training is complete.\n"
            "\n"
            "This connects back to the production optimization methods studied earlier: "
            "distillation, quantization, pruning, and optimized inference runtimes.\n"
            "\n"
            "[[IMAGE_NEEDED: Scaling challenge stack | "
            "A vertical stack labeled infrastructure, cost, dataset curation, model evaluation, "
            "and deployment surrounding a very large language model | "
            "Learner should notice that scaling affects the entire ML lifecycle, not only training]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Why self-attention becomes a long-sequence bottleneck\n"
            "\n"
            "Standard self-attention compares token positions pairwise.\n"
            "\n"
            "For a sequence of length `n`, the model conceptually considers an `n × n` attention "
            "matrix.\n"
            "\n"
            "So if sequence length doubles:\n"
            "\n"
            "```text\n"
            "n      → n² comparisons\n"
            "2n     → 4n² comparisons\n"
            "```\n"
            "\n"
            "This quadratic behavior makes long documents, speech, video, and high-resolution "
            "visual inputs expensive.\n"
            "\n"
            "Efficient-attention research tries to avoid calculating every possible query-key pair.\n"
            "\n"
            "[[IMAGE_NEEDED: Quadratic self-attention growth | "
            "Attention matrices for short, medium, and long sequences shown growing from small "
            "square to much larger square, with n² highlighted | "
            "Learner should notice that doubling sequence length roughly quadruples the pairwise "
            "attention-score space]]\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Sparse attention: do not compare every token with every token\n"
            "\n"
            "One way to reduce attention cost is to calculate only a subset of query-key pairs.\n"
            "\n"
            "The chapter describes several reusable sparsity patterns.\n"
            "\n"
            "### Global attention\n"
            "\n"
            "A few special tokens can attend to all other tokens.\n"
            "\n"
            "### Band attention\n"
            "\n"
            "Each token mainly attends to nearby positions, producing a diagonal band.\n"
            "\n"
            "### Dilated attention\n"
            "\n"
            "A token attends to regularly spaced positions, skipping some intermediate tokens.\n"
            "\n"
            "### Random attention\n"
            "\n"
            "Each query also attends to a selected set of random positions.\n"
            "\n"
            "### Block-local attention\n"
            "\n"
            "The sequence is divided into blocks, and attention is concentrated within blocks.\n"
            "\n"
            "[[IMAGE_NEEDED: Atomic sparse attention patterns | "
            "Five small attention matrices showing global, band, dilated, random, and block-local "
            "patterns using filled cells for calculated scores and blank cells for skipped scores | "
            "Learner should compare how each pattern reduces the number of pairwise calculations]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Combine sparse patterns: Longformer and BigBird\n"
            "\n"
            "Practical sparse-attention models often combine several atomic patterns.\n"
            "\n"
            "The chapter gives two examples:\n"
            "\n"
            "### Longformer\n"
            "\n"
            "Combines local/band attention with selected global-attention positions.\n"
            "\n"
            "### BigBird\n"
            "\n"
            "Combines local attention, global attention, and random attention.\n"
            "\n"
            "These sparse patterns allow the models described by the source to handle sequences "
            "up to 4,096 tokens—much longer than BERT's usual 512-token limit.\n"
            "\n"
            "The chapter also mentions data-driven sparsity, where token relationships determine "
            "which positions should interact. Reformer, for example, uses hashing to group similar "
            "tokens.\n"
            "\n"
            "[[IMAGE_NEEDED: Longformer and BigBird compound sparsity | "
            "Two attention matrices side by side: Longformer showing local band plus global rows/"
            "columns, and BigBird adding random sparse links | "
            "Learner should notice that practical efficient-attention models combine multiple "
            "sparsity patterns]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Linearized attention: change the order of operations\n"
            "\n"
            "Sparse attention keeps the attention idea but removes many pairwise comparisons.\n"
            "\n"
            "Linearized attention takes another route: restructure the similarity computation "
            "so the expensive `n × n` matrix does not need to be formed in the same way.\n"
            "\n"
            "The chapter describes kernel-based decompositions that allow parts of the attention "
            "calculation to be rearranged and computed more efficiently.\n"
            "\n"
            "You do not need to memorize the derivation. Retain the intuition:\n"
            "\n"
            "```text\n"
            "standard attention:\n"
            "build pairwise token interactions first\n"
            "\n"
            "linearized attention:\n"
            "rearrange/decompose operations to avoid explicit quadratic work\n"
            "```\n"
            "\n"
            "The chapter cites models such as **Linear Transformer** and **Performer** as examples.\n"
            "\n"
            "[[IMAGE_NEEDED: Standard versus linearized attention | "
            "A side-by-side computational diagram: standard attention explicitly forms a QK^T "
            "matrix, while linearized attention applies feature maps and rearranged matrix "
            "products without materializing the full pairwise matrix | "
            "Learner should focus on the structural difference rather than the detailed algebra]]\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Why go beyond text?\n"
            "\n"
            "Text is powerful, but it is an incomplete representation of the world.\n"
            "\n"
            "The chapter highlights several limitations of text-only learning.\n"
            "\n"
            "### Human reporting bias\n"
            "\n"
            "What people write about is not always proportional to what happens in reality.\n"
            "\n"
            "### Common sense\n"
            "\n"
            "Many everyday truths are rarely written down because humans assume them.\n"
            "\n"
            "### Facts\n"
            "\n"
            "A probabilistic language model can generate incorrect statements and is not a "
            "reliable factual database by itself.\n"
            "\n"
            "### Modality\n"
            "\n"
            "Text-only models cannot directly perceive audio, images, layouts, or structured tables.\n"
            "\n"
            "Multimodal models try to connect language with additional sources of information.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Treat images as sequences: iGPT\n"
            "\n"
            "One early way to extend transformer ideas into vision is to treat an image as a "
            "sequence of pixel values.\n"
            "\n"
            "iGPT applies a GPT-like autoregressive objective:\n"
            "\n"
            "```text\n"
            "previous pixel values\n"
            "       ↓\n"
            "predict the next pixel value\n"
            "```\n"
            "\n"
            "After large-scale image pretraining, the model can complete partial images and "
            "its representations can also support classification.\n"
            "\n"
            "The larger idea is important:\n"
            "\n"
            "> The transformer architecture is not fundamentally limited to word tokens; "
            "other data can also be represented as sequences.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Vision Transformer: turn image patches into tokens\n"
            "\n"
            "Vision Transformer (ViT) follows a BERT-like idea rather than a pixel-by-pixel GPT idea.\n"
            "\n"
            "The pipeline is:\n"
            "\n"
            "```text\n"
            "image\n"
            "  ↓ split into fixed-size patches\n"
            "patches\n"
            "  ↓ linear projection\n"
            "patch embeddings\n"
            "  + position embeddings\n"
            "  ↓\n"
            "transformer encoder\n"
            "```\n"
            "\n"
            "An image patch plays a role similar to a token in NLP.\n"
            "\n"
            "[[IMAGE_NEEDED: Vision Transformer patch pipeline | "
            "An image divided into equal square patches, each patch converted to an embedding, "
            "position embeddings added, then all patch tokens entering a transformer encoder | "
            "Learner should notice the analogy between image patches and text tokens]]\n"
            "\n"
            "The chapter notes that ViT becomes especially strong when pretrained on larger image datasets.\n"
            "\n"
            "It also demonstrates that using an image-classification pipeline feels similar to "
            "the NLP pipelines used earlier in the book.\n"
            "\n"
            "### Video extension\n"
            "\n"
            "Video adds a time dimension to vision. The chapter mentions TimeSformer, which "
            "uses separate spatial and temporal attention mechanisms.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Ask natural-language questions about tables with TAPAS\n"
            "\n"
            "Many real-world facts live in structured tables rather than free text.\n"
            "\n"
            "TAPAS adapts the transformer architecture to table question answering.\n"
            "\n"
            "A user can ask questions such as:\n"
            "\n"
            "```text\n"
            "What is the total number of pages?\n"
            "Which chapter starts on page 74?\n"
            "How many chapters have more than 20 pages?\n"
            "```\n"
            "\n"
            "The model can select cells and, when necessary, predict an aggregation operation "
            "such as:\n"
            "\n"
            "- `SUM`,\n"
            "- `AVERAGE`,\n"
            "- `COUNT`,\n"
            "- or no aggregation.\n"
            "\n"
            "[[IMAGE_NEEDED: TAPAS table question answering | "
            "A small table, a natural-language question above it, selected cells highlighted, "
            "and an optional aggregator such as SUM or COUNT producing the final answer | "
            "Learner should notice that answering may require both cell selection and aggregation]]\n"
            "\n"
            "This makes structured data more accessible to users who may not know SQL or Python.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Speech-to-text with wav2vec 2.0\n"
            "\n"
            "Transformers can also process audio.\n"
            "\n"
            "The chapter introduces **wav2vec 2.0**, which combines convolutional processing "
            "with transformer layers for automatic speech recognition (ASR).\n"
            "\n"
            "A key idea is **self-supervised pretraining on unlabeled audio**.\n"
            "\n"
            "This can reduce the amount of transcribed speech needed for downstream training.\n"
            "\n"
            "A high-level pipeline is:\n"
            "\n"
            "```text\n"
            "audio waveform\n"
            "   ↓\n"
            "feature extraction\n"
            "   ↓\n"
            "transformer representation learning\n"
            "   ↓\n"
            "speech transcription\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: wav2vec 2.0 speech-recognition pipeline | "
            "An audio waveform entering convolutional feature extraction, then transformer "
            "context layers, then producing a text transcription | "
            "Learner should notice the combination of low-level audio feature processing and "
            "transformer-based contextual representation learning]]\n"
            "\n"
            "The chapter then mentions **wav2vec-U**, which explores speech recognition using "
            "unlabeled speech and unlabeled text without requiring aligned speech-text pairs.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Multimodal transformers combine information sources\n"
            "\n"
            "A multimodal model processes more than one type of input at once.\n"
            "\n"
            "The chapter highlights several important combinations.\n"
            "\n"
            "### Vision + language for question answering\n"
            "\n"
            "Models such as LXMERT and VisualBERT combine image features with natural-language "
            "questions to predict answers.\n"
            "\n"
            "### Text + image + layout for documents\n"
            "\n"
            "LayoutLM targets scanned business documents such as receipts, invoices, and forms.\n"
            "\n"
            "It uses multiple information sources:\n"
            "\n"
            "- text,\n"
            "- visual features,\n"
            "- spatial/layout coordinates.\n"
            "\n"
            "This is useful because document meaning often depends on **where** something appears "
            "on the page, not only on the words themselves.\n"
            "\n"
            "[[IMAGE_NEEDED: Multimodal document understanding with LayoutLM | "
            "A scanned invoice with text boxes and coordinates feeding text, visual, and layout "
            "embeddings into one transformer | "
            "Learner should notice that document understanding combines what the text says with "
            "where it appears and what the page looks like]]\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Text-to-image generation with DALL-E\n"
            "\n"
            "The chapter presents DALL-E as a generative vision-language model.\n"
            "\n"
            "Its high-level idea is to treat language and image information as tokens in a "
            "single autoregressive modeling framework.\n"
            "\n"
            "```text\n"
            "text prompt tokens\n"
            "      +\n"
            "image representation tokens\n"
            "      ↓\n"
            "autoregressive transformer\n"
            "      ↓\n"
            "generated image\n"
            "```\n"
            "\n"
            "The conceptual leap is important: the same sequence-modeling idea that predicts "
            "next text tokens can be extended to generate visual content.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. CLIP: align image and text embeddings\n"
            "\n"
            "CLIP uses a different multimodal objective.\n"
            "\n"
            "It has:\n"
            "\n"
            "- an image encoder,\n"
            "- a text encoder.\n"
            "\n"
            "Both produce embeddings in a shared space.\n"
            "\n"
            "During training, matching image-caption pairs are pulled closer together while "
            "mismatched pairs are pushed apart.\n"
            "\n"
            "This is **contrastive learning**.\n"
            "\n"
            "```text\n"
            "image ─► image encoder ─► image vector\n"
            "                               ╲\n"
            "                                similarity\n"
            "                               ╱\n"
            "text  ─► text encoder  ─► text vector\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: CLIP contrastive learning | "
            "A batch of images and captions encoded into vectors with a similarity matrix; "
            "matching image-caption pairs highlighted along the diagonal and mismatched pairs "
            "shown off-diagonal | "
            "Learner should notice that training rewards matching pairs and separates mismatches]]\n"
            "\n"
            "### Zero-shot image classification\n"
            "\n"
            "At inference time, class descriptions can be written as text:\n"
            "\n"
            "```text\n"
            "a photo of a transformer\n"
            "a photo of a robot\n"
            "a photo of agi\n"
            "```\n"
            "\n"
            "The image embedding is compared against each text embedding. The closest text "
            "description becomes the predicted class.\n"
            "\n"
            "This mirrors the zero-shot ideas studied earlier in the course: natural-language "
            "descriptions can define new classes without retraining a dedicated classification head.\n"
            "\n"
            "{{exercise:M01.L09.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Where should you go after this course?\n"
            "\n"
            "The chapter closes with practical suggestions for continuing to learn.\n"
            "\n"
            "### Join community events\n"
            "\n"
            "Participating in open-source sprints exposes you to real datasets, models, and "
            "collaborative engineering.\n"
            "\n"
            "### Build your own project\n"
            "\n"
            "A project reveals gaps in understanding that are easy to miss while reading.\n"
            "\n"
            "### Implement or contribute a model\n"
            "\n"
            "Working close to an architecture teaches how configuration, tokenization, modeling, "
            "training, and inference fit together.\n"
            "\n"
            "### Teach what you learned\n"
            "\n"
            "Writing a technical explanation or tutorial forces you to organize concepts clearly.\n"
            "\n"
            "The chapter's final message is not that transformers are finished. It is the opposite: "
            "the architecture is still being stretched toward larger scales, longer contexts, "
            "new modalities, and new combinations of modalities.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Scaling means only increasing parameter count\n"
            "\n"
            "> Bigger N alone is enough.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The chapter emphasizes model size, dataset size, and compute budget together.\n"
            "\n"
            "### Misconception 2: Sparse attention simply deletes context\n"
            "\n"
            "> Efficient attention models cannot retain long-range information.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Sparse designs combine local and selected long-range/global connections so the "
            "model can preserve important distant interactions while avoiding all pairwise scores.\n"
            "\n"
            "### Misconception 3: Transformers only work with text tokens\n"
            "\n"
            "> Attention requires words as input.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Images can be represented as pixels or patches, audio as learned feature sequences, "
            "and tables as structured tokenized inputs.\n"
            "\n"
            "### Misconception 4: A text-only model has direct access to reliable world facts\n"
            "\n"
            "> If a model produces fluent language, its outputs are a factual database.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The chapter explicitly notes that probabilistic language models can produce "
            "factually incorrect text and may lack grounding in other modalities.\n"
            "\n"
            "### Misconception 5: Multimodal learning is just concatenating raw inputs\n"
            "\n"
            "> Feed image pixels and text characters together and the problem is solved.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Successful multimodal systems need suitable encoders, representations, and "
            "objectives that align information across modalities.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Scaling law | Empirical relationship between model performance and scale variables |\n"
            "| N | Model size / parameter count in the scaling-law discussion |\n"
            "| D | Dataset size in the scaling-law discussion |\n"
            "| C | Compute budget in the scaling-law discussion |\n"
            "| Power law | Relationship that appears approximately linear on log-log axes |\n"
            "| Quadratic attention | Standard attention cost that grows roughly with n² sequence interactions |\n"
            "| Sparse attention | Attention that computes only selected query-key interactions |\n"
            "| Global attention | Selected positions attend broadly across the sequence |\n"
            "| Band attention | Attention restricted to nearby token positions |\n"
            "| Dilated attention | Attention over spaced positions with gaps |\n"
            "| Random attention | Attention to a sampled subset of positions |\n"
            "| Block-local attention | Attention mainly within predefined sequence blocks |\n"
            "| Linearized attention | Reformulated attention avoiding the standard explicit quadratic interaction pattern |\n"
            "| ViT | Vision Transformer using image patches as token-like inputs |\n"
            "| TAPAS | Transformer model for natural-language interaction with tables |\n"
            "| ASR | Automatic speech recognition |\n"
            "| wav2vec 2.0 | Self-supervised speech representation model with transformer context layers |\n"
            "| Multimodal model | Model that combines more than one data modality |\n"
            "| LayoutLM | Model combining text, visual, and layout information for documents |\n"
            "| Contrastive learning | Objective that pulls matching representations together and pushes mismatches apart |\n"
            "| CLIP | Image-text model trained using contrastive alignment |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What are N, D, and C in the chapter's scaling-law discussion?\n"
            "2. Why can scaling laws be useful before running the largest experiment?\n"
            "3. Name three practical challenges created by large-model scaling.\n"
            "4. Why does ordinary self-attention become expensive for long sequences?\n"
            "5. What is the difference between band, global, and random sparse attention?\n"
            "6. How does linearized attention differ conceptually from sparse attention?\n"
            "7. How does ViT turn an image into transformer inputs?\n"
            "8. What extra capability does TAPAS add beyond normal text QA?\n"
            "9. Why is unlabeled speech useful for wav2vec 2.0 pretraining?\n"
            "10. What three modalities does LayoutLM combine?\n"
            "11. What is CLIP's contrastive objective trying to accomplish?\n"
            "12. How can CLIP perform zero-shot image classification?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**The future directions in this chapter extend transformers along three axes: "
            "scale models/data/compute to improve capability, redesign attention so long inputs "
            "become practical, and represent non-text modalities as sequences or aligned "
            "embeddings so one architecture can reason across text, vision, tables, and audio.**\n"
        ),

        "estimated_minutes": 120,
        "has_code_examples": False,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "future-overview", "title": "Three transformer research directions", "order": 1},
            {"id": "bitter-lesson", "title": "The scaling mindset", "order": 2},
            {"id": "scaling-laws", "title": "Scaling laws", "order": 3},
            {"id": "scaling-challenges", "title": "Challenges with scaling", "order": 4},
            {"id": "attention-bottleneck", "title": "The self-attention bottleneck", "order": 5},
            {"id": "sparse-attention", "title": "Sparse attention", "order": 6},
            {"id": "longformer-bigbird", "title": "Longformer and BigBird", "order": 7},
            {"id": "linear-attention", "title": "Linearized attention", "order": 8},
            {"id": "beyond-text", "title": "Why go beyond text?", "order": 9},
            {"id": "vision-igpt", "title": "iGPT", "order": 10},
            {"id": "vit", "title": "Vision Transformer", "order": 11},
            {"id": "tables", "title": "Table QA with TAPAS", "order": 12},
            {"id": "speech", "title": "Speech-to-text with wav2vec 2.0", "order": 13},
            {"id": "multimodal", "title": "Multimodal transformers", "order": 14},
            {"id": "dalle", "title": "Text-to-image generation", "order": 15},
            {"id": "clip", "title": "CLIP", "order": 16},
            {"id": "where-next", "title": "Where to go next", "order": 17},
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L09.EX01",
            "title": "Reason About Scaling",
            "lesson_code": "M01.L09",
            "section_id": "scaling-laws",
            "placement": "after_section",
            "description": (
                "Practice distinguishing model size, data size, and compute instead of "
                "treating scaling as a single variable."
            ),
            "instructions": (
                "Consider three hypothetical experiments:\n"
                "A. Double model parameters but keep training data and compute nearly fixed.\n"
                "B. Double dataset size but keep the model too small to use the extra data well.\n"
                "C. Increase model size, dataset size, and compute together.\n\n"
                "1. Identify which experiment most closely follows the chapter's scaling-law advice.\n"
                "2. Explain why changing only one variable can lead to diminishing returns.\n"
                "3. List two non-modeling costs that become harder as scale increases.\n"
                "4. Explain why a small pilot run may still be useful before a huge run."
            ),
            "expected_output": (
                "A short comparison selecting experiment C, explaining coordinated scaling, "
                "naming challenges such as infrastructure/cost/data curation, and describing "
                "how smooth scaling trends can support rough extrapolation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "scaling-laws",
                "model-data-compute-tradeoffs",
                "research-reasoning",
            ],
        },
        {
            "id": "M01.L09.EX02",
            "title": "Match a Transformer to a New Modality",
            "lesson_code": "M01.L09",
            "section_id": "clip",
            "placement": "after_section",
            "description": (
                "Practice connecting different transformer extensions to the kind of data "
                "and task they are designed to handle."
            ),
            "instructions": (
                "Match each problem to the most relevant model family discussed in the lesson:\n"
                "1. Classify an image using text-defined classes.\n"
                "2. Ask natural-language aggregation questions over a business table.\n"
                "3. Transcribe speech audio into text.\n"
                "4. Extract information from a scanned invoice using text position and visuals.\n"
                "5. Process a very long document more efficiently than full quadratic attention.\n\n"
                "For each answer, explain the representation or attention idea that makes it fit."
            ),
            "expected_output": (
                "A mapping such as CLIP, TAPAS, wav2vec 2.0, LayoutLM, and a sparse-attention "
                "model such as Longformer/BigBird, each with a one-sentence explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "multimodal-transformers",
                "model-selection",
                "efficient-attention",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L09.QZ01",
        "title": "Future Directions — Knowledge Check",
        "lesson_code": "M01.L09",
        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L09.Q01",
                "section_id": "scaling-laws",
                "question": (
                    "Which three quantities are central to the scaling-law discussion in the chapter?"
                ),
                "options": [
                    "Model size, dataset size, and compute budget.",
                    "Tokenizer speed, file size, and optimizer name.",
                    "Number of labels, batch ID, and CPU clock.",
                    "Vocabulary alphabet, table rows, and image width.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter discusses empirical scaling relationships using model size N, "
                    "dataset size D, and compute budget C."
                ),
            },
            {
                "id": "M01.L09.Q02",
                "section_id": "sparse-attention",
                "question": (
                    "What is the basic goal of sparse attention?"
                ),
                "options": [
                    "Compute every possible query-key score twice.",
                    "Restrict attention to selected token pairs so long sequences require fewer computations.",
                    "Remove all position information.",
                    "Replace transformers with recurrent neural networks.",
                ],
                "correct": 1,
                "explanation": (
                    "Sparse attention skips many query-key interactions while retaining selected "
                    "local, global, random, or block-based connections."
                ),
            },
            {
                "id": "M01.L09.Q03",
                "section_id": "vit",
                "question": (
                    "How does Vision Transformer convert an image into transformer-style inputs?"
                ),
                "options": [
                    "It converts every image directly into one integer class before attention.",
                    "It splits the image into patches, projects them into embeddings, adds position "
                    "information, and feeds them to a transformer encoder.",
                    "It translates the image into audio first.",
                    "It requires a separate CNN output for every word in the vocabulary.",
                ],
                "correct": 1,
                "explanation": (
                    "ViT treats image patches as token-like units, embeds them, adds positional "
                    "information, and processes them with a transformer encoder."
                ),
            },
            {
                "id": "M01.L09.Q04",
                "section_id": "clip",
                "question": (
                    "What is the core training idea behind CLIP?"
                ),
                "options": [
                    "Predict masked table cells only.",
                    "Train matching image-text pairs to have similar embeddings while separating mismatched pairs.",
                    "Use only a language decoder and no image representation.",
                    "Generate speech waveforms from text labels.",
                ],
                "correct": 1,
                "explanation": (
                    "CLIP uses contrastive learning to align matching image and text embeddings "
                    "in a shared representation space."
                ),
            },
            {
                "id": "M01.L09.Q05",
                "section_id": "where-next",
                "type": "open",
                "question": (
                    "Choose one limitation of standard transformers—scaling cost, long-sequence "
                    "attention, or text-only modality—and design a small project that explores "
                    "one solution from this lesson. Explain the model/technique, the dataset or "
                    "input type you would use, and what success metric you would measure."
                ),
            },
        ],

        "passing_score": 70,
    },
}
