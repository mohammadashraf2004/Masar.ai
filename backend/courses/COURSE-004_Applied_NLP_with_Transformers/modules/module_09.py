"""M01.L08 — Dealing with Few to No Labels.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-004, Chapter 9.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L08"
MODULE_ORDER = 9
MODULE_TITLE = "NLP with Few or No Labels"
MODULE_DESCRIPTION = (
    "Learn how to build useful NLP classifiers when labeled data is scarce by "
    "using zero-shot learning, augmentation, embeddings, few-shot prompting, "
    "domain adaptation, and unlabeled-data methods."
)

SOURCE_CHAPTER = 9
SOURCE_PAGES = "Chapter 9"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Dealing with Few to No Labels",
    "slug": "applied-nlp-transformers-m01-l08-few-to-no-labels",
    "description": (
        "Choose practical NLP strategies for no-label, few-label, and unlabeled-data "
        "settings using zero-shot classification, data augmentation, embedding search, "
        "transformer fine-tuning, domain adaptation, UDA, and uncertainty-aware self-training."
    ),
    "order": 8,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 2.25,
    "skill_tags": [
        "few-shot-learning",
        "zero-shot-learning",
        "multilabel-classification",
        "data-augmentation",
        "embeddings",
        "faiss",
        "domain-adaptation",
        "masked-language-modeling",
        "uda",
        "self-training",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
        "M01.L06",
        "M01.L07",
    ],

    "lesson": {
        "title": "Dealing with Few to No Labels",

        "content": (
            "# Dealing with Few to No Labels\n"
            "\n"
            "> **Course:** Applied NLP with Transformers  \n"
            "> **Lesson:** M01.L08  \n"
            "> **Module:** Transformer Foundations  \n"
            "> **Source alignment:** BOOK-004, Chapter 9. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Choose an NLP strategy based on how much labeled and unlabeled data you have.\n"
            "- Explain multilabel classification and encode multilabel targets.\n"
            "- Build a simple Naive Bayes baseline before using transformers.\n"
            "- Explain zero-shot classification with masked language models and NLI models.\n"
            "- Tune top-k and threshold rules for multilabel zero-shot predictions.\n"
            "- Use text data augmentation carefully in low-data settings.\n"
            "- Classify examples using pretrained embeddings and nearest-neighbor search.\n"
            "- Explain why FAISS is useful for vector similarity search.\n"
            "- Fine-tune a vanilla transformer for multilabel classification.\n"
            "- Explain in-context and few-shot learning with prompts.\n"
            "- Perform domain adaptation with masked-language-model training on unlabeled text.\n"
            "- Explain unsupervised data augmentation (UDA).\n"
            "- Explain uncertainty-aware self-training (UST) and pseudo-labeling.\n"
            "- Design a low-label experimentation workflow instead of assuming one method is best.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Start with the amount of supervision you actually have\n"
            "\n"
            "When a new NLP project begins, one of the first questions is:\n"
            "\n"
            "> **How much labeled data do we have?**\n"
            "\n"
            "The chapter organizes the answer as a decision tree.\n"
            "\n"
            "### Case A — no labeled data\n"
            "\n"
            "Start with a **zero-shot** method. It gives you a baseline without task-specific "
            "fine-tuning.\n"
            "\n"
            "### Case B — a few labeled examples\n"
            "\n"
            "Consider methods such as:\n"
            "\n"
            "- simple supervised baselines,\n"
            "- data augmentation,\n"
            "- embedding-based nearest-neighbor classification,\n"
            "- vanilla transformer fine-tuning,\n"
            "- in-context/few-shot prompting.\n"
            "\n"
            "### Case C — a few labels plus lots of unlabeled text\n"
            "\n"
            "You can do even more:\n"
            "\n"
            "- domain-adaptive language-model training,\n"
            "- unsupervised data augmentation,\n"
            "- uncertainty-aware self-training.\n"
            "\n"
            "### Case D — many labeled examples\n"
            "\n"
            "Standard supervised fine-tuning becomes a natural choice.\n"
            "\n"
            '{{image:low-label-method-decision-tree}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 2. Case study: automatically tag GitHub issues\n"
            "\n"
            "The chapter uses GitHub issues from the Transformers repository as the running task.\n"
            "\n"
            "Each issue has:\n"
            "\n"
            "- a title,\n"
            "- a body/description,\n"
            "- zero, one, or several labels.\n"
            "\n"
            "Example labels include topics such as:\n"
            "\n"
            "```text\n"
            "tokenization\n"
            "new model\n"
            "model training\n"
            "usage\n"
            "pipeline\n"
            "tensorflow or tf\n"
            "pytorch\n"
            "documentation\n"
            "examples\n"
            "```\n"
            "\n"
            "Because one issue may receive multiple labels, this is a **multilabel** problem.\n"
            "\n"
            "That differs from ordinary multiclass classification:\n"
            "\n"
            "```text\n"
            "multiclass:\n"
            "one example → exactly one class\n"
            "\n"
            "multilabel:\n"
            "one example → zero, one, or many labels\n"
            "```\n"
            "\n"
            "The cleaned dataset used for the experiment has very few labeled issues compared "
            "with the large number of unlabeled issues. That is exactly the scenario this chapter "
            "is designed to study.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Prepare multilabel data carefully\n"
            "\n"
            "Before testing low-data methods, the chapter cleans and restructures the dataset.\n"
            "\n"
            "Important steps include:\n"
            "\n"
            "1. keep only useful label names,\n"
            "2. combine issue title and body into one text field,\n"
            "3. remove duplicate issue texts,\n"
            "4. separate labeled and unlabeled examples,\n"
            "5. create balanced train/validation/test splits for the labeled subset.\n"
            "\n"
            "### Encode labels as multi-hot vectors\n"
            "\n"
            "For nine possible labels, an issue might become:\n"
            "\n"
            "```text\n"
            "[0, 0, 0, 1, 0, 1, 0, 0, 0]\n"
            "```\n"
            "\n"
            "A `1` means the label is present; `0` means it is absent.\n"
            "\n"
            "```python\n"
            "from sklearn.preprocessing import MultiLabelBinarizer\n"
            "\n"
            "mlb = MultiLabelBinarizer()\n"
            "mlb.fit([all_labels])\n"
            "\n"
            "encoded = mlb.transform([\n"
            "    ['tokenization', 'new model'],\n"
            "    ['pytorch'],\n"
            "])\n"
            "```\n"
            "\n"
            "### Why balanced splitting is harder\n"
            "\n"
            "A multilabel example can contribute to several label distributions at once. "
            "Simple random splitting can accidentally create validation or test sets where "
            "rare labels are poorly represented.\n"
            "\n"
            "The chapter uses iterative multilabel splitting to approximate balanced distributions.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Use learning curves, not one training-set size\n"
            "\n"
            "The chapter deliberately trains with progressively larger labeled subsets.\n"
            "\n"
            "The goal is not only to ask:\n"
            "\n"
            "> Which method has the best final score?\n"
            "\n"
            "but also:\n"
            "\n"
            "> Which method works best when I have 10 labels? 30? 100? 200?\n"
            "\n"
            "This produces a **learning curve**:\n"
            "\n"
            "```text\n"
            "F1\n"
            "▲\n"
            "|                         ____\n"
            "|                   _____/\n"
            "|              ____/\n"
            "|        _____/\n"
            "|_______/\n"
            "+------------------------------► labeled examples\n"
            "```\n"
            "\n"
            "Low-data methods can dominate at the left side of the graph even if ordinary "
            "fine-tuning eventually catches up when more labels become available.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Build a simple baseline first\n"
            "\n"
            "The chapter starts with a Naive Bayes baseline using bag-of-words features.\n"
            "\n"
            "Why begin with such a simple model?\n"
            "\n"
            "- it trains quickly,\n"
            "- it is easy to debug,\n"
            "- it can work surprisingly well,\n"
            "- it tells us whether a transformer is truly adding value.\n"
            "\n"
            "For multilabel classification, the chapter trains one binary classifier per label.\n"
            "\n"
            "```python\n"
            "from sklearn.feature_extraction.text import CountVectorizer\n"
            "from sklearn.naive_bayes import MultinomialNB\n"
            "from skmultilearn.problem_transform import BinaryRelevance\n"
            "\n"
            "vectorizer = CountVectorizer()\n"
            "X_train = vectorizer.fit_transform(train_texts)\n"
            "X_test = vectorizer.transform(test_texts)\n"
            "\n"
            "classifier = BinaryRelevance(\n"
            "    classifier=MultinomialNB()\n"
            ")\n"
            "classifier.fit(X_train, y_train)\n"
            "```\n"
            "\n"
            "### Micro versus macro F1\n"
            "\n"
            "The chapter evaluates both:\n"
            "\n"
            "- **micro F1** — aggregates decisions across all labels and is influenced more by "
            "frequent labels,\n"
            "- **macro F1** — computes label-level F1 and averages equally, revealing how the "
            "classifier handles rare classes.\n"
            "\n"
            "Always looking at both is useful when label frequencies are highly imbalanced.\n"
            "\n"
            "{{exercise:M01.L08.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Zero-shot idea #1: turn classification into a fill-mask problem\n"
            "\n"
            "When there are no task labels, one creative option is to reuse a masked language model.\n"
            "\n"
            "Suppose a movie description is followed by:\n"
            "\n"
            "```text\n"
            "The movie is about [MASK].\n"
            "```\n"
            "\n"
            "A masked language model can score candidate words such as:\n"
            "\n"
            "```text\n"
            "animals\n"
            "cars\n"
            "```\n"
            "\n"
            "The classifier is created indirectly through the **prompt** rather than a newly "
            "trained classification head.\n"
            "\n"
            "This example teaches a broader principle:\n"
            "\n"
            "> Sometimes a pretrained model's original task can be reformulated so it behaves "
            "like the new task without parameter updates.\n"
            "\n"
            "This fill-mask trick is intuitive, but natural-language inference offers a more "
            "general zero-shot classification method.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Zero-shot classification with natural language inference\n"
            "\n"
            "An NLI model receives:\n"
            "\n"
            "- a **premise**,\n"
            "- a **hypothesis**,\n"
            "\n"
            "and predicts whether the hypothesis is:\n"
            "\n"
            "- entailment,\n"
            "- neutral,\n"
            "- contradiction.\n"
            "\n"
            "We can convert classification into NLI by using the document as the premise and "
            "creating a hypothesis for every candidate label.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Premise:\n"
            "Add a new CANINE architecture to the Transformers library ...\n"
            "\n"
            "Hypothesis:\n"
            "This example is about a new model.\n"
            "```\n"
            "\n"
            "A high entailment score suggests that the label fits the text.\n"
            "\n"
            "```python\n"
            "from transformers import pipeline\n"
            "\n"
            "zero_shot = pipeline('zero-shot-classification')\n"
            "\n"
            "result = zero_shot(\n"
            "    text,\n"
            "    candidate_labels=all_labels,\n"
            "    multi_label=True,\n"
            ")\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: NLI zero-shot classification | "
            "One issue text acts as the premise and branches into several hypotheses such as "
            "'This example is about new model', '...tokenization', and '...documentation'; "
            "each receives an entailment score | "
            "Learner should notice that no task-specific classifier is trained; class names "
            "are expressed directly in natural language]]\n"
            "\n"
            "### Label wording matters\n"
            "\n"
            "The hypothesis must carry semantic meaning. Labels such as `Class 1` tell the model "
            "almost nothing, while labels such as `new model` or `documentation` give useful clues.\n"
            "\n"
            "The chapter also notes that the hypothesis template itself can influence performance.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Convert zero-shot scores into multilabel predictions\n"
            "\n"
            "An NLI zero-shot model returns a score for each label. We still need a rule for "
            "turning scores into predicted labels.\n"
            "\n"
            "Two options from the chapter are:\n"
            "\n"
            "### Top-k\n"
            "\n"
            "Always select the `k` highest-scoring labels.\n"
            "\n"
            "### Threshold\n"
            "\n"
            "Select every label whose score exceeds a chosen threshold.\n"
            "\n"
            "These rules create different precision/recall behavior.\n"
            "\n"
            "A low threshold predicts many labels:\n"
            "\n"
            "```text\n"
            "higher recall\n"
            "lower precision\n"
            "```\n"
            "\n"
            "A very high threshold predicts few labels:\n"
            "\n"
            "```text\n"
            "higher precision\n"
            "lower recall\n"
            "```\n"
            "\n"
            "For this dataset, the chapter finds that **top-1** works best among the tested "
            "top-k rules because most labeled issues have only one selected label.\n"
            "\n"
            "The larger lesson is to tune the output rule on a small validation set, even when "
            "the model itself is used zero-shot.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Few labels: multiply examples with data augmentation\n"
            "\n"
            "Once a few labeled examples are available, data augmentation can create synthetic "
            "variants while preserving the original label.\n"
            "\n"
            "Common approaches include:\n"
            "\n"
            "### Back translation\n"
            "\n"
            "```text\n"
            "English → another language → English\n"
            "```\n"
            "\n"
            "### Token perturbations\n"
            "\n"
            "- synonym replacement,\n"
            "- word insertion,\n"
            "- word swapping,\n"
            "- word deletion.\n"
            "\n"
            "Text augmentation is more dangerous than image augmentation because tiny word "
            "changes can reverse meaning.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Are elephants heavier than mice?\n"
            "Are mice heavier than elephants?\n"
            "```\n"
            "\n"
            "Only a small token reordering changes the answer completely.\n"
            "\n"
            "For longer GitHub issues, however, modest perturbations are less likely to change "
            "the high-level topic label.\n"
            "\n"
            "[[IMAGE_NEEDED: Text data augmentation examples | "
            "One source sentence branching into synonym replacement, random insertion, random "
            "swap, random deletion, and back-translation variants | "
            "Learner should notice that augmentation attempts to vary surface form while "
            "preserving the original class label]]\n"
            "\n"
            "In the chapter's experiment, a small amount of augmentation improves the Naive "
            "Bayes baseline by several F1 points.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Use embeddings as a lookup table\n"
            "\n"
            "Another few-label strategy avoids fine-tuning completely.\n"
            "\n"
            "The process is:\n"
            "\n"
            "1. embed every labeled training text,\n"
            "2. embed the new query text,\n"
            "3. find the nearest labeled examples,\n"
            "4. aggregate their labels.\n"
            "\n"
            "```text\n"
            "labeled text ─► embedding ─┐\n"
            "labeled text ─► embedding ─┼─► vector index\n"
            "labeled text ─► embedding ─┘\n"
            "\n"
            "new issue ─► embedding ─► nearest neighbors ─► labels\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Embedding nearest-neighbor classifier | "
            "Several labeled text points represented in embedding space, a new query point, "
            "and lines connecting it to its nearest neighbors whose labels are aggregated | "
            "Learner should notice that the pretrained representation does the heavy lifting "
            "without updating model weights]]\n"
            "\n"
            "The chapter uses a GPT-2 variant trained on Python code because the GitHub issues "
            "contain technical text and code.\n"
            "\n"
            "### Mean pooling\n"
            "\n"
            "Transformer encoders return one vector per token. To build one vector for the whole "
            "issue, the chapter averages token vectors while excluding padding positions.\n"
            "\n"
            "```python\n"
            "def mean_pooling(model_output, attention_mask):\n"
            "    token_embeddings = model_output[0]\n"
            "    mask = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()\n"
            "\n"
            "    summed = (token_embeddings * mask).sum(1)\n"
            "    counts = mask.sum(1).clamp(min=1e-9)\n"
            "    return summed / counts\n"
            "```\n"
            "\n"
            "The best embedding model is domain-dependent, so evaluation matters more than "
            "assuming one checkpoint will always produce the strongest semantic representation.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. FAISS makes vector lookup scalable\n"
            "\n"
            "Brute-force nearest-neighbor search compares a query vector with every stored vector.\n"
            "\n"
            "That becomes expensive as the dataset grows.\n"
            "\n"
            "FAISS provides efficient similarity-search structures for dense vectors.\n"
            "\n"
            "One intuition explained in the chapter is to partition vectors into clusters:\n"
            "\n"
            "```text\n"
            "all vectors\n"
            "   ↓ k-means\n"
            "cluster 1   cluster 2   cluster 3 ...\n"
            "   ↓\n"
            "compare query with cluster centers\n"
            "   ↓\n"
            "search only promising cluster(s)\n"
            "```\n"
            "\n"
            "This can reduce the number of comparisons dramatically.\n"
            "\n"
            "[[IMAGE_NEEDED: FAISS clustered vector index | "
            "A 2D embedding space partitioned into several regions around centroid points, "
            "with one query vector first matched to a centroid and then compared with vectors "
            "inside that region | "
            "Learner should notice how partitioning avoids comparing the query with every "
            "stored embedding]]\n"
            "\n"
            "In the chapter's nearest-neighbor classifier, two key hyperparameters are:\n"
            "\n"
            "- `k`: how many neighbors to retrieve,\n"
            "- `m`: how many of those neighbors must contain a label before assigning it.\n"
            "\n"
            "With the full labeled training set, the chapter finds a strong setting around "
            "`k=15` and `m=5` for its validation experiment.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Fine-tune a vanilla transformer when labels become sufficient\n"
            "\n"
            "Once you have some labeled examples, the obvious transformer baseline is normal "
            "supervised fine-tuning.\n"
            "\n"
            "For multilabel classification, the model configuration is set accordingly:\n"
            "\n"
            "```python\n"
            "from transformers import AutoConfig, AutoModelForSequenceClassification\n"
            "\n"
            "config = AutoConfig.from_pretrained('bert-base-uncased')\n"
            "config.num_labels = len(all_labels)\n"
            "config.problem_type = 'multi_label_classification'\n"
            "\n"
            "model = AutoModelForSequenceClassification.from_pretrained(\n"
            "    'bert-base-uncased',\n"
            "    config=config,\n"
            ")\n"
            "```\n"
            "\n"
            "Unlike mutually exclusive multiclass classification, each output label receives "
            "its own probability after a sigmoid transformation.\n"
            "\n"
            "A simple decision rule is:\n"
            "\n"
            "```python\n"
            "from scipy.special import expit as sigmoid\n"
            "\n"
            "probabilities = sigmoid(logits)\n"
            "predictions = (probabilities > 0.5).astype(float)\n"
            "```\n"
            "\n"
            "The chapter observes that vanilla BERT becomes competitive around several dozen "
            "labeled examples, while performance is unstable with extremely tiny slices because "
            "the label distribution can be poorly represented.\n"
            "\n"
            "That is exactly why learning curves are useful.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. In-context and few-shot learning with prompts\n"
            "\n"
            "There is a middle ground between zero-shot prompting and parameter fine-tuning.\n"
            "\n"
            "A sufficiently capable language model can sometimes infer a task from examples "
            "included directly in the prompt.\n"
            "\n"
            "Zero-shot translation prompt:\n"
            "\n"
            "```text\n"
            "Translate English to French:\n"
            "thanks =>\n"
            "```\n"
            "\n"
            "Few-shot version:\n"
            "\n"
            "```text\n"
            "Translate English to French:\n"
            "hello => bonjour\n"
            "goodbye => au revoir\n"
            "thanks =>\n"
            "```\n"
            "\n"
            "The model parameters do not change; the examples become temporary context.\n"
            "\n"
            "The chapter discusses this as an emerging way to exploit a few labeled examples "
            "without necessarily training a conventional task head.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Large unlabeled corpora are valuable\n"
            "\n"
            "Suppose you have only a few labeled GitHub issues but thousands of unlabeled ones.\n"
            "\n"
            "The unlabeled corpus teaches the model what your **domain language** looks like:\n"
            "\n"
            "- technical terminology,\n"
            "- code snippets,\n"
            "- framework names,\n"
            "- issue-report style,\n"
            "- domain-specific phrasing.\n"
            "\n"
            "BERT was pretrained on general-purpose corpora, not specifically on GitHub issue text.\n"
            "\n"
            "Instead of training a language model from scratch, we can continue language-model "
            "training on the target-domain corpus.\n"
            "\n"
            "This is **domain adaptation**.\n"
            "\n"
            "```text\n"
            "general pretrained BERT\n"
            "        ↓\n"
            "masked-LM training on unlabeled GitHub issues\n"
            "        ↓\n"
            "domain-adapted BERT\n"
            "        ↓\n"
            "small labeled classification set\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Domain-adaptive language-model training | "
            "A pipeline from general BERT pretraining to continued masked-language-model "
            "training on many unlabeled GitHub issues, then to a small supervised classifier | "
            "Learner should notice that unlabeled domain text is used before the task-specific "
            "fine-tuning stage]]\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Continue masked-language-model training on the domain\n"
            "\n"
            "For BERT, domain adaptation can reuse the masked-language-model objective.\n"
            "\n"
            "The chapter uses `DataCollatorForLanguageModeling` to mask tokens dynamically "
            "when each training batch is constructed.\n"
            "\n"
            "```python\n"
            "from transformers import DataCollatorForLanguageModeling\n"
            "\n"
            "data_collator = DataCollatorForLanguageModeling(\n"
            "    tokenizer=tokenizer,\n"
            "    mlm_probability=0.15,\n"
            ")\n"
            "```\n"
            "\n"
            "Why generate masks dynamically?\n"
            "\n"
            "- target labels do not need to be stored separately,\n"
            "- the same sentence can receive different masked positions across epochs,\n"
            "- special tokens can be excluded from prediction.\n"
            "\n"
            "The training label convention again uses `-100` for positions that should not "
            "contribute to the loss.\n"
            "\n"
            "Example:\n"
            "\n"
            "| Position | Input token | Training target |\n"
            "|---|---|---|\n"
            "| `[CLS]` | `[CLS]` | -100 |\n"
            "| transformers | transformers | -100 |\n"
            "| are | are | -100 |\n"
            "| awesome | awesome | -100 |\n"
            "| `!` | `[MASK]` | original token ID for `!` |\n"
            "| `[SEP]` | `[SEP]` | -100 |\n"
            "\n"
            "After continued MLM training, the chapter loads the adapted checkpoint into a "
            "multilabel classifier.\n"
            "\n"
            "The adapted model improves over vanilla BERT, especially in the low-label regime.\n"
            "\n"
            "{{exercise:M01.L08.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Advanced method: unsupervised data augmentation (UDA)\n"
            "\n"
            "UDA uses both labeled and unlabeled examples.\n"
            "\n"
            "Its central assumption is:\n"
            "\n"
            "> A small, meaning-preserving perturbation of an unlabeled example should not "
            "radically change the model's prediction.\n"
            "\n"
            "The training objective combines:\n"
            "\n"
            "1. ordinary supervised loss on labeled examples,\n"
            "2. a **consistency loss** on unlabeled examples and their augmented variants.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "unlabeled text ───────────────► model ─► distribution A\n"
            "      │\n"
            "      └─ augmentation ────────► model ─► distribution B\n"
            "\n"
            "                 minimize difference(A, B)\n"
            "```\n"
            "\n"
            "The chapter describes KL divergence as the tool used to enforce prediction "
            "consistency.\n"
            "\n"
            "[[IMAGE_NEEDED: Unsupervised data augmentation consistency training | "
            "One unlabeled example branches into original and augmented text; both enter the "
            "same model and their output distributions are connected by a consistency/KL loss, "
            "alongside a normal supervised loss from labeled examples | "
            "Learner should notice that UDA extracts a training signal from unlabeled text "
            "without inventing hard labels for every example]]\n"
            "\n"
            "UDA can work very well with few labels, but it requires an augmentation pipeline "
            "and additional forward passes, so training is more expensive.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Advanced method: uncertainty-aware self-training (UST)\n"
            "\n"
            "UST takes a teacher-student approach.\n"
            "\n"
            "### Step 1\n"
            "\n"
            "Train a teacher on the labeled data.\n"
            "\n"
            "### Step 2\n"
            "\n"
            "Use the teacher to create **pseudo-labels** for unlabeled examples.\n"
            "\n"
            "### Step 3\n"
            "\n"
            "Train a student using those pseudo-labeled examples.\n"
            "\n"
            "### Step 4\n"
            "\n"
            "Promote the trained student to become the next teacher and repeat.\n"
            "\n"
            "The special feature of UST is that it estimates uncertainty.\n"
            "\n"
            "The same example is passed through the model several times with dropout enabled. "
            "If predictions vary greatly, the model is uncertain. If they remain stable, "
            "confidence is stronger.\n"
            "\n"
            "The chapter describes using this uncertainty signal with BALD to decide which "
            "pseudo-labeled samples are most useful.\n"
            "\n"
            "[[IMAGE_NEEDED: Uncertainty-aware self-training loop | "
            "Labeled data trains a teacher; the teacher predicts pseudo-labels with uncertainty "
            "estimation on unlabeled data; selected pseudo-labeled examples train a student; "
            "the student becomes the next teacher and the loop repeats | "
            "Learner should notice both the iterative teacher-student cycle and the role of "
            "uncertainty in selecting pseudo-labels]]\n"
            "\n"
            "The chapter reports that this family of methods can approach the performance of "
            "models trained with far more labeled examples, though it is substantially more "
            "complex than ordinary domain adaptation.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Which method should you choose?\n"
            "\n"
            "There is no universal winner.\n"
            "\n"
            "| Situation | Good methods to test early |\n"
            "|---|---|\n"
            "| No task labels | Zero-shot NLI / prompt-based baseline |\n"
            "| Very few labels | Baseline + augmentation + embeddings + few-shot methods |\n"
            "| Dozens/hundreds of labels | Compare simple models and vanilla transformer fine-tuning |\n"
            "| Few labels + lots of unlabeled domain text | Domain-adaptive MLM training |\n"
            "| Need to squeeze more from unlabeled data | UDA or UST |\n"
            "\n"
            "Other factors matter too:\n"
            "\n"
            "- label noise,\n"
            "- domain similarity to the pretrained model,\n"
            "- class imbalance,\n"
            "- compute budget,\n"
            "- annotation cost,\n"
            "- engineering complexity.\n"
            "\n"
            "The chapter's practical recommendation is to establish an evaluation pipeline "
            "and iterate quickly.\n"
            "\n"
            "Sometimes labeling a few hundred high-quality examples is cheaper and more reliable "
            "than implementing a very complex semi-supervised training method.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: No training labels means machine learning is impossible\n"
            "\n"
            "> If we cannot fine-tune a classifier, there is nothing useful to try.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Pretrained models can support zero-shot classification, semantic embedding lookup, "
            "and other forms of transfer without task-specific parameter updates.\n"
            "\n"
            "### Misconception 2: More complex models should be tried before simple baselines\n"
            "\n"
            "> A transformer is automatically a better starting point than Naive Bayes.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A simple baseline is fast, useful for debugging, and may already solve the task well.\n"
            "\n"
            "### Misconception 3: Zero-shot performance does not require any labeled examples at all\n"
            "\n"
            "> We never need labeled data if the zero-shot pipeline runs.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The model parameters may not require labeled task training, but a small labeled "
            "validation/test set is still extremely useful for deciding whether the method works "
            "and for tuning thresholds or prompt wording.\n"
            "\n"
            "### Misconception 4: Data augmentation always preserves meaning\n"
            "\n"
            "> Randomly changing words creates harmless extra training data.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Text meaning can change after tiny perturbations. Augmentation policies must be "
            "tested for the specific task and input style.\n"
            "\n"
            "### Misconception 5: Unlabeled data has no value for supervised classification\n"
            "\n"
            "> Only examples with labels can improve the classifier.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Unlabeled domain text can improve the language representation through domain "
            "adaptation and can support semi-supervised methods such as UDA and UST.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Low-resource / low-label setting | Task with little labeled training data |\n"
            "| Multilabel classification | Example may belong to multiple classes simultaneously |\n"
            "| Multi-hot vector | Binary vector indicating which labels are present |\n"
            "| Micro F1 | F1 calculated globally over decisions; influenced by frequent labels |\n"
            "| Macro F1 | Average of per-label F1 scores; gives equal weight to each label |\n"
            "| Zero-shot classification | Apply a pretrained model to a new task without task-specific fine-tuning |\n"
            "| NLI | Natural language inference: entailment, neutral, or contradiction between premise/hypothesis |\n"
            "| Hypothesis template | Natural-language pattern used to express candidate labels in zero-shot NLI |\n"
            "| Data augmentation | Creating altered training examples intended to preserve labels |\n"
            "| Back translation | Translate away from and then back into the source language |\n"
            "| Embedding lookup | Classify by retrieving similar labeled examples in vector space |\n"
            "| Mean pooling | Average token embeddings into one sequence embedding |\n"
            "| FAISS | Library for efficient similarity search over dense vectors |\n"
            "| In-context learning | Infer a task from instructions/examples inside the prompt without updating weights |\n"
            "| Domain adaptation | Continue training a pretrained model on target-domain data |\n"
            "| MLM | Masked language modeling; predict intentionally masked tokens |\n"
            "| Pseudo-label | Label generated by a model for an unlabeled example |\n"
            "| UDA | Unsupervised data augmentation with consistency training |\n"
            "| UST | Uncertainty-aware self-training using teacher/student pseudo-labeling |\n"
            "| BALD | Uncertainty-based sampling method used in the UST description |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What changes in your strategy when you move from zero labels to a few labels?\n"
            "2. How does multilabel classification differ from multiclass classification?\n"
            "3. Why track both micro and macro F1?\n"
            "4. How can an NLI model perform zero-shot classification?\n"
            "5. Why do label names and hypothesis wording matter in zero-shot NLI?\n"
            "6. Why can text augmentation be risky?\n"
            "7. How can embeddings classify a new text without model fine-tuning?\n"
            "8. What problem does FAISS solve?\n"
            "9. Why can vanilla transformer fine-tuning be unstable with extremely few examples?\n"
            "10. What does domain-adaptive MLM training learn from unlabeled text?\n"
            "11. What consistency assumption drives UDA?\n"
            "12. How does UST use uncertainty when generating pseudo-labels?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Scarce labels do not imply one fixed solution. Start with the supervision you "
            "have, establish a simple baseline, test zero-shot or embedding methods when labels "
            "are scarce, fine-tune when enough labels appear, and use unlabeled domain text for "
            "adaptation or semi-supervised learning. The best method is the one that wins on a "
            "carefully designed evaluation for your data and constraints.**\n"
        ),

        "estimated_minutes": 135,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "decision-tree", "title": "Choose a method from available supervision", "order": 1},
            {"id": "github-tagger", "title": "GitHub issue tagging case study", "order": 2},
            {"id": "prepare-data", "title": "Prepare multilabel data", "order": 3},
            {"id": "training-slices", "title": "Use learning curves", "order": 4},
            {"id": "naive-bayes", "title": "Build a simple baseline", "order": 5},
            {"id": "masked-zero-shot", "title": "Fill-mask zero-shot intuition", "order": 6},
            {"id": "nli-zero-shot", "title": "NLI zero-shot classification", "order": 7},
            {"id": "zero-shot-threshold", "title": "Turn zero-shot scores into labels", "order": 8},
            {"id": "augmentation", "title": "Data augmentation", "order": 9},
            {"id": "embedding-lookup", "title": "Embedding lookup", "order": 10},
            {"id": "faiss", "title": "Efficient similarity search with FAISS", "order": 11},
            {"id": "vanilla-finetune", "title": "Fine-tune a vanilla transformer", "order": 12},
            {"id": "few-shot-prompts", "title": "In-context and few-shot prompting", "order": 13},
            {"id": "unlabeled-data", "title": "Leverage unlabeled domain data", "order": 14},
            {"id": "mlm-adaptation", "title": "Masked-LM domain adaptation", "order": 15},
            {"id": "uda", "title": "Unsupervised data augmentation", "order": 16},
            {"id": "ust", "title": "Uncertainty-aware self-training", "order": 17},
            {"id": "method-selection", "title": "Choose the right low-label method", "order": 18},
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L08.EX01",
            "title": "Choose a Strategy from the Label Budget",
            "lesson_code": "M01.L08",
            "section_id": "naive-bayes",
            "placement": "after_section",
            "description": (
                "Practice mapping available labeled and unlabeled data to sensible first experiments."
            ),
            "instructions": (
                "For each scenario, choose two methods from the lesson that you would test first "
                "and explain why:\n"
                "1. You have zero task labels and 50,000 unlabeled support tickets.\n"
                "2. You have 25 labeled tickets and no additional unlabeled corpus.\n"
                "3. You have 100 labeled tickets and 200,000 unlabeled tickets from the same domain.\n"
                "4. You have 20,000 clean labeled examples.\n"
                "5. State which evaluation metrics you would use if the task is multilabel and imbalanced."
            ),
            "expected_output": (
                "A scenario-to-method table using combinations such as zero-shot NLI, embedding "
                "lookup, augmentation, vanilla fine-tuning, domain adaptation, UDA/UST, plus "
                "micro and macro F1 for evaluation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "low-data-strategy",
                "zero-shot-learning",
                "domain-adaptation",
                "multilabel-evaluation",
            ],
        },
        {
            "id": "M01.L08.EX02",
            "title": "Design a Domain-Adaptation Experiment",
            "lesson_code": "M01.L08",
            "section_id": "mlm-adaptation",
            "placement": "after_section",
            "description": (
                "Practice using unlabeled domain text before supervised classifier fine-tuning."
            ),
            "instructions": (
                "1. Assume you have BERT-base, 80 labeled cybersecurity tickets, and 100,000 "
                "unlabeled cybersecurity tickets.\n"
                "2. Define a vanilla BERT fine-tuning baseline.\n"
                "3. Define a second experiment that first performs masked-language-model domain "
                "adaptation on the unlabeled tickets.\n"
                "4. Fine-tune the same multilabel classifier on the same 80 labels.\n"
                "5. Compare both experiments using identical validation/test splits and metrics.\n"
                "6. Explain what result would convince you that domain adaptation was useful."
            ),
            "expected_output": (
                "A two-arm experiment plan where only the additional MLM domain-adaptation stage "
                "changes, followed by the same supervised classifier training and micro/macro F1 "
                "comparison."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "masked-language-modeling",
                "domain-adaptation",
                "experimental-design",
                "few-shot-classification",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L08.QZ01",
        "title": "Dealing with Few to No Labels — Knowledge Check",
        "lesson_code": "M01.L08",
        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L08.Q01",
                "section_id": "nli-zero-shot",
                "question": (
                    "How can an NLI model be reused for zero-shot classification?"
                ),
                "options": [
                    "Treat the input as a premise and convert each candidate label into a "
                    "natural-language hypothesis, then use entailment scores.",
                    "Retrain all model weights on every candidate class before inference.",
                    "Use only the tokenizer vocabulary size as the class score.",
                    "Replace every document with its first word.",
                ],
                "correct": 0,
                "explanation": (
                    "Zero-shot NLI reformulates classification as entailment between the "
                    "input premise and hypotheses such as 'This example is about {label}'."
                ),
            },
            {
                "id": "M01.L08.Q02",
                "section_id": "embedding-lookup",
                "question": (
                    "What is the main idea behind embedding-based classification in the chapter?"
                ),
                "options": [
                    "Fine-tune a new transformer layer for every training example.",
                    "Embed labeled examples and classify a new example using labels from its "
                    "nearest neighbors in vector space.",
                    "Discard pretrained representations and use random vectors.",
                    "Convert every label into a single token and ignore the text.",
                ],
                "correct": 1,
                "explanation": (
                    "The method reuses pretrained embeddings as a semantic lookup space, so "
                    "classification can work without task-specific model fine-tuning."
                ),
            },
            {
                "id": "M01.L08.Q03",
                "section_id": "mlm-adaptation",
                "question": (
                    "Why can masked-language-model domain adaptation help when labeled data is scarce?"
                ),
                "options": [
                    "It lets the model learn target-domain language patterns from large amounts "
                    "of unlabeled text before supervised fine-tuning.",
                    "It automatically produces perfect ground-truth labels.",
                    "It prevents the model from reading domain-specific vocabulary.",
                    "It replaces the downstream classifier with a search engine.",
                ],
                "correct": 0,
                "explanation": (
                    "Continued MLM training adapts the pretrained representation to the "
                    "language distribution of the target domain without requiring labels."
                ),
            },
            {
                "id": "M01.L08.Q04",
                "section_id": "uda",
                "question": (
                    "What assumption is central to unsupervised data augmentation?"
                ),
                "options": [
                    "Every augmented sentence should receive a random new class.",
                    "A meaning-preserving perturbation of an unlabeled example should produce "
                    "a similar model prediction.",
                    "Only labeled examples should influence training.",
                    "The augmented text must be identical to the source text.",
                ],
                "correct": 1,
                "explanation": (
                    "UDA adds a consistency objective that encourages predictions on original "
                    "and slightly augmented unlabeled examples to remain similar."
                ),
            },
            {
                "id": "M01.L08.Q05",
                "section_id": "method-selection",
                "type": "open",
                "question": (
                    "You need to build a multilabel classifier with 60 labeled examples and "
                    "50,000 unlabeled examples from the same specialized domain. Design a staged "
                    "experiment that includes a simple baseline, zero-shot or embedding method, "
                    "vanilla transformer fine-tuning, domain adaptation, and one advanced "
                    "semi-supervised method. Explain how learning curves and micro/macro F1 "
                    "would guide the final choice."
                ),
            },
        ],

        "passing_score": 70,
    },
}
