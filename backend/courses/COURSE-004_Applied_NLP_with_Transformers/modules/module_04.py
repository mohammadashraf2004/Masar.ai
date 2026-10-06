"""M01.L03 — Multilingual Named Entity Recognition.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-004, Chapter 4.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L03"
MODULE_ORDER = 1
MODULE_TITLE = "Transformer Foundations"
MODULE_DESCRIPTION = (
    "Move from transformer architecture to practical multilingual NLP by building, "
    "fine-tuning, evaluating, and debugging a multilingual named entity recognizer."
)

SOURCE_CHAPTER = 4
SOURCE_PAGES = "Chapter 4"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Multilingual Named Entity Recognition",
    "slug": "applied-nlp-transformers-m01-l03-multilingual-ner",
    "description": (
        "Build a multilingual named entity recognition system with XLM-RoBERTa, "
        "learn how token labels are aligned after subword tokenization, fine-tune "
        "a token-classification model, analyze its errors, and study zero-shot "
        "cross-lingual transfer."
    ),
    "order": 3,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 2.0,
    "skill_tags": [
        "named-entity-recognition",
        "multilingual-nlp",
        "xlm-roberta",
        "token-classification",
        "sentencepiece",
        "cross-lingual-transfer",
        "zero-shot-transfer",
        "error-analysis",
        "hugging-face",
        "module-01",
    ],
    "prerequisite_ids": ["M01.L01", "M01.L02"],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Multilingual Named Entity Recognition",

        "content": (
            "# Multilingual Named Entity Recognition\n"
            "\n"
            "> **Course:** Applied NLP with Transformers  \n"
            "> **Lesson:** M01.L03  \n"
            "> **Module:** Transformer Foundations  \n"
            "> **Source alignment:** BOOK-004, Chapter 4. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Learning outcomes
            # ----------------------------------------------------------------

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain named entity recognition as a token-classification problem.\n"
            "- Read and interpret IOB2 entity labels such as `B-PER`, `I-ORG`, and `O`.\n"
            "- Explain why multilingual transformers can transfer knowledge across languages.\n"
            "- Describe the main differences between WordPiece and SentencePiece tokenization.\n"
            "- Explain why NER labels must be realigned after subword tokenization.\n"
            "- Use `word_ids()` and the `-100` ignore label to prepare NER training data.\n"
            "- Explain the body-and-head design used by transformer model classes.\n"
            "- Build a token-classification head on top of an XLM-R/RoBERTa encoder.\n"
            "- Evaluate NER using precision, recall, and F1 rather than naive token accuracy.\n"
            "- Perform useful error analysis using token loss, class loss, and bad examples.\n"
            "- Explain zero-shot cross-lingual transfer and when it may be useful.\n"
            "- Compare monolingual, zero-shot, and multilingual fine-tuning strategies.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. The problem: one NER system, many languages\n"
            "\n"
            "Imagine that your application receives documents in several languages. "
            "You want to extract people, companies, and locations from all of them.\n"
            "\n"
            "One approach is to maintain a separate model for every language. That can "
            "be expensive: each model needs training data, deployment, monitoring, "
            "updates, and debugging.\n"
            "\n"
            "A multilingual transformer gives us another option. A single model can be "
            "pretrained on text from many languages and later fine-tuned for one task.\n"
            "\n"
            "The chapter uses **XLM-RoBERTa (XLM-R)** for multilingual named entity "
            "recognition.\n"
            "\n"
            "### What is named entity recognition?\n"
            "\n"
            "NER identifies spans of text that represent entities such as:\n"
            "\n"
            "- **PER** — person\n"
            "- **ORG** — organization\n"
            "- **LOC** — location\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Jeff Dean works at Google in California.\n"
            "```\n"
            "\n"
            "A useful annotation is:\n"
            "\n"
            "| Token | Label |\n"
            "|---|---|\n"
            "| Jeff | B-PER |\n"
            "| Dean | I-PER |\n"
            "| works | O |\n"
            "| at | O |\n"
            "| Google | B-ORG |\n"
            "| in | O |\n"
            "| California | B-LOC |\n"
            "\n"
            "### Understanding IOB2\n"
            "\n"
            "The labels use the **IOB2** scheme:\n"
            "\n"
            "- `B-` means **beginning** of an entity.\n"
            "- `I-` means **inside** the same entity.\n"
            "- `O` means the token is **outside** any entity.\n"
            "\n"
            "So a two-word person such as `Jeff Dean` becomes `B-PER`, `I-PER`.\n"
            "\n"
            "[[IMAGE_NEEDED: IOB2 named entity labeling | "
            "A short sentence with tokens shown in boxes and colored labels underneath for "
            "B-PER, I-PER, B-ORG, B-LOC, and O | "
            "Learner should notice that B marks the start of an entity span, I continues it, "
            "and O means the token is not part of an entity]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Build a multilingual NER dataset\n"
            "\n"
            "The chapter uses the **PAN-X / WikiANN** portion of the XTREME benchmark. "
            "It contains multilingual Wikipedia sentences annotated with entity tags.\n"
            "\n"
            "The running scenario uses four languages associated with Switzerland:\n"
            "\n"
            "| Language | Code | Sample proportion used in the chapter |\n"
            "|---|---:|---:|\n"
            "| German | `de` | 62.9% |\n"
            "| French | `fr` | 22.9% |\n"
            "| Italian | `it` | 8.4% |\n"
            "| English | `en` | 5.9% |\n"
            "\n"
            "This deliberately creates an **imbalanced multilingual dataset**. That is "
            "useful because real production datasets are often imbalanced too: labeled "
            "examples can be much easier to obtain for one language than another.\n"
            "\n"
            "### Loading the language subsets\n"
            "\n"
            "```python\n"
            "from collections import defaultdict\n"
            "from datasets import DatasetDict, load_dataset\n"
            "\n"
            "langs = ['de', 'fr', 'it', 'en']\n"
            "fracs = [0.629, 0.229, 0.084, 0.059]\n"
            "panx_ch = defaultdict(DatasetDict)\n"
            "\n"
            "for lang, frac in zip(langs, fracs):\n"
            "    ds = load_dataset('xtreme', name=f'PAN-X.{lang}')\n"
            "\n"
            "    for split in ds:\n"
            "        panx_ch[lang][split] = (\n"
            "            ds[split]\n"
            "            .shuffle(seed=0)\n"
            "            .select(range(int(frac * ds[split].num_rows)))\n"
            "        )\n"
            "```\n"
            "\n"
            "In the chapter's sample, this creates many more German training examples "
            "than French, Italian, or English examples. German is therefore used as the "
            "source language for the first cross-lingual experiments.\n"
            "\n"
            "### Inspect labels before training\n"
            "\n"
            "A dataset may store NER tags as integer IDs. Convert them back to readable "
            "names before trusting the data.\n"
            "\n"
            "```python\n"
            "tags = panx_ch['de']['train'].features['ner_tags'].feature\n"
            "\n"
            "def create_tag_names(batch):\n"
            "    return {\n"
            "        'ner_tags_str': [tags.int2str(idx) for idx in batch['ner_tags']]\n"
            "    }\n"
            "\n"
            "panx_de = panx_ch['de'].map(create_tag_names)\n"
            "```\n"
            "\n"
            "This is an important machine-learning habit: **look at your labels as humans "
            "would read them before you start training**.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Why multilingual transformers can transfer across languages\n"
            "\n"
            "A multilingual transformer is trained on text from many languages using a "
            "shared model. XLM-R uses masked language modeling and a large multilingual "
            "pretraining corpus.\n"
            "\n"
            "The surprising result is that the model can learn representations that are "
            "useful across languages even though we do not explicitly tell it that a German "
            "word and a French word express similar concepts.\n"
            "\n"
            "This enables **cross-lingual transfer**.\n"
            "\n"
            "### Zero-shot cross-lingual transfer\n"
            "\n"
            "In this chapter's workflow:\n"
            "\n"
            "```text\n"
            "fine-tune on labeled German NER data\n"
            "                 ↓\n"
            "evaluate directly on French / Italian / English\n"
            "                 ↓\n"
            "no labeled target-language training examples used\n"
            "```\n"
            "\n"
            "That is zero-shot cross-lingual transfer in the sense used here.\n"
            "\n"
            "It can be particularly useful when the target language has little labeled data.\n"
            "\n"
            "[[IMAGE_NEEDED: Zero-shot cross-lingual transfer | "
            "A flow diagram where one multilingual XLM-R model is fine-tuned on labeled German "
            "NER data and then evaluated directly on French, Italian, and English without "
            "target-language fine-tuning | "
            "Learner should notice that the task labels stay the same while the language changes]]\n"
            "\n"
            "{{exercise:M01.L03.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Tokenization matters more in NER than it first appears\n"
            "\n"
            "XLM-R uses **SentencePiece** tokenization rather than the WordPiece tokenizer "
            "used by BERT in the chapter's comparison.\n"
            "\n"
            "Consider:\n"
            "\n"
            "```text\n"
            "Jack Sparrow loves New York!\n"
            "```\n"
            "\n"
            "A tokenizer may split words into smaller **subwords**. This is useful for "
            "handling large vocabularies and unfamiliar words, but it creates a special "
            "problem for NER: our labels are usually defined per original word, while the "
            "model receives subword tokens.\n"
            "\n"
            "### The tokenizer pipeline\n"
            "\n"
            "It is useful to think of tokenization as four stages:\n"
            "\n"
            "1. **Normalization** — clean or normalize the raw string.\n"
            "2. **Pretokenization** — split text into preliminary units where appropriate.\n"
            "3. **Tokenizer model** — apply a subword algorithm such as WordPiece, BPE, or Unigram.\n"
            "4. **Postprocessing** — add model-specific special tokens and final formatting.\n"
            "\n"
            "[[IMAGE_NEEDED: Tokenizer pipeline | "
            "A four-stage pipeline labeled normalization, pretokenization, subword tokenizer "
            "model, and postprocessing, using one short multilingual-friendly example | "
            "Learner should notice that subword splitting is only one stage of the complete "
            "tokenization process]]\n"
            "\n"
            "### SentencePiece intuition\n"
            "\n"
            "SentencePiece operates directly on text and is designed to work without relying "
            "on language-specific whitespace rules. In the token display used by the chapter, "
            "the `▁` character indicates that a token begins after whitespace.\n"
            "\n"
            "For example, a token sequence may look like:\n"
            "\n"
            "```text\n"
            "<s> ▁Jack ▁Spar row ▁love s ▁New ▁York ! </s>\n"
            "```\n"
            "\n"
            "XLM-R uses `<s>` and `</s>` as sequence boundary tokens.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 5
            # ----------------------------------------------------------------

            "## 5. NER is token classification\n"
            "\n"
            "In sequence classification, we normally need one prediction for the entire "
            "input. NER is different: we need a prediction for **every relevant token**.\n"
            "\n"
            "An encoder produces a hidden state for each token:\n"
            "\n"
            "```text\n"
            "token 1 → hidden state 1 → tag distribution\n"
            "token 2 → hidden state 2 → tag distribution\n"
            "token 3 → hidden state 3 → tag distribution\n"
            "...\n"
            "```\n"
            "\n"
            "The same linear classification head is applied independently to every token "
            "representation.\n"
            "\n"
            "[[IMAGE_NEEDED: Sequence classification versus token classification | "
            "Side-by-side diagrams: sequence classification uses one pooled representation "
            "for one label, while NER sends every token hidden state through the same classifier "
            "to produce one entity label per token | "
            "Learner should notice the difference between one prediction per sequence and one "
            "prediction per token]]\n"
            "\n"
            "### Body + head\n"
            "\n"
            "Transformer implementations commonly separate the network into:\n"
            "\n"
            "- **Body:** embeddings and transformer layers that produce contextual hidden states.\n"
            "- **Head:** task-specific layers that transform those hidden states into predictions.\n"
            "\n"
            "That separation is powerful because we can reuse a pretrained body and replace "
            "only the head for a new downstream task.\n"
            "\n"
            "```text\n"
            "Pretrained XLM-R body\n"
            "        ↓\n"
            "token hidden states\n"
            "        ↓\n"
            "dropout + linear classification head\n"
            "        ↓\n"
            "NER logits for each token\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 6
            # ----------------------------------------------------------------

            "## 6. Build a custom XLM-R token-classification model\n"
            "\n"
            "The chapter uses XLM-R's RoBERTa-compatible architecture to demonstrate how "
            "a custom token-classification model can be created.\n"
            "\n"
            "A simplified version looks like this:\n"
            "\n"
            "```python\n"
            "import torch.nn as nn\n"
            "from transformers import XLMRobertaConfig\n"
            "from transformers.modeling_outputs import TokenClassifierOutput\n"
            "from transformers.models.roberta.modeling_roberta import (\n"
            "    RobertaModel,\n"
            "    RobertaPreTrainedModel,\n"
            ")\n"
            "\n"
            "class XLMRobertaForTokenClassification(RobertaPreTrainedModel):\n"
            "    config_class = XLMRobertaConfig\n"
            "\n"
            "    def __init__(self, config):\n"
            "        super().__init__(config)\n"
            "        self.num_labels = config.num_labels\n"
            "        self.roberta = RobertaModel(config, add_pooling_layer=False)\n"
            "        self.dropout = nn.Dropout(config.hidden_dropout_prob)\n"
            "        self.classifier = nn.Linear(config.hidden_size, config.num_labels)\n"
            "        self.init_weights()\n"
            "\n"
            "    def forward(\n"
            "        self,\n"
            "        input_ids=None,\n"
            "        attention_mask=None,\n"
            "        labels=None,\n"
            "        **kwargs,\n"
            "    ):\n"
            "        outputs = self.roberta(\n"
            "            input_ids,\n"
            "            attention_mask=attention_mask,\n"
            "            **kwargs,\n"
            "        )\n"
            "\n"
            "        sequence_output = self.dropout(outputs[0])\n"
            "        logits = self.classifier(sequence_output)\n"
            "\n"
            "        loss = None\n"
            "        if labels is not None:\n"
            "            loss_fct = nn.CrossEntropyLoss()\n"
            "            loss = loss_fct(\n"
            "                logits.view(-1, self.num_labels),\n"
            "                labels.view(-1),\n"
            "            )\n"
            "\n"
            "        return TokenClassifierOutput(\n"
            "            loss=loss,\n"
            "            logits=logits,\n"
            "            hidden_states=outputs.hidden_states,\n"
            "            attentions=outputs.attentions,\n"
            "        )\n"
            "```\n"
            "\n"
            "### What is important here?\n"
            "\n"
            "The custom class does **not** rebuild the transformer from scratch.\n"
            "\n"
            "It:\n"
            "\n"
            "1. reuses the pretrained RoBERTa/XLM-R body,\n"
            "2. keeps one hidden state per token,\n"
            "3. applies dropout,\n"
            "4. maps each token's hidden vector to `num_labels` logits,\n"
            "5. optionally computes cross-entropy loss when labels are provided.\n"
            "\n"
            "### Configure label mappings\n"
            "\n"
            "```python\n"
            "index2tag = {idx: tag for idx, tag in enumerate(tags.names)}\n"
            "tag2index = {tag: idx for idx, tag in enumerate(tags.names)}\n"
            "\n"
            "from transformers import AutoConfig\n"
            "\n"
            "xlmr_config = AutoConfig.from_pretrained(\n"
            "    'xlm-roberta-base',\n"
            "    num_labels=tags.num_classes,\n"
            "    id2label=index2tag,\n"
            "    label2id=tag2index,\n"
            ")\n"
            "```\n"
            "\n"
            "For seven NER labels, model logits for a sequence of ten tokens have shape:\n"
            "\n"
            "```text\n"
            "[batch_size, num_tokens, num_tags]\n"
            "[1, 10, 7]\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 7
            # ----------------------------------------------------------------

            "## 7. The crucial step: align word labels with subword tokens\n"
            "\n"
            "This is one of the most important practical ideas in the chapter.\n"
            "\n"
            "Suppose the original dataset contains the word:\n"
            "\n"
            "```text\n"
            "Einwohnern\n"
            "```\n"
            "\n"
            "The tokenizer may split it into two subwords:\n"
            "\n"
            "```text\n"
            "▁Einwohner   n\n"
            "```\n"
            "\n"
            "But the dataset contains **one label for the original word**, not two labels.\n"
            "\n"
            "The convention used in this lesson is:\n"
            "\n"
            "- assign the word's label to its **first subword**,\n"
            "- ignore later subwords of the same word,\n"
            "- ignore special tokens such as `<s>` and `</s>`.\n"
            "\n"
            "### Why `word_ids()` helps\n"
            "\n"
            "When tokenizing a list of already separated words, the tokenizer can tell us "
            "which original word produced each subword token:\n"
            "\n"
            "```python\n"
            "tokenized_input = xlmr_tokenizer(\n"
            "    words,\n"
            "    is_split_into_words=True,\n"
            ")\n"
            "\n"
            "word_ids = tokenized_input.word_ids()\n"
            "```\n"
            "\n"
            "Conceptually, the result might look like:\n"
            "\n"
            "| Token | Word ID | Training label |\n"
            "|---|---:|---|\n"
            "| `<s>` | None | IGN |\n"
            "| `▁Einwohner` | 0 | O |\n"
            "| `n` | 0 | IGN |\n"
            "| `▁Google` | 1 | B-ORG |\n"
            "| `</s>` | None | IGN |\n"
            "\n"
            "### Why use `-100`?\n"
            "\n"
            "PyTorch's cross-entropy loss ignores targets whose ID equals its default "
            "`ignore_index`, which is `-100`.\n"
            "\n"
            "So we can mark special tokens and repeated subwords with `-100` and prevent "
            "them from contributing to training loss.\n"
            "\n"
            "```python\n"
            "def tokenize_and_align_labels(examples):\n"
            "    tokenized_inputs = xlmr_tokenizer(\n"
            "        examples['tokens'],\n"
            "        truncation=True,\n"
            "        is_split_into_words=True,\n"
            "    )\n"
            "\n"
            "    aligned_labels = []\n"
            "\n"
            "    for batch_idx, word_labels in enumerate(examples['ner_tags']):\n"
            "        word_ids = tokenized_inputs.word_ids(batch_index=batch_idx)\n"
            "        previous_word_idx = None\n"
            "        label_ids = []\n"
            "\n"
            "        for word_idx in word_ids:\n"
            "            if word_idx is None or word_idx == previous_word_idx:\n"
            "                label_ids.append(-100)\n"
            "            else:\n"
            "                label_ids.append(word_labels[word_idx])\n"
            "\n"
            "            previous_word_idx = word_idx\n"
            "\n"
            "        aligned_labels.append(label_ids)\n"
            "\n"
            "    tokenized_inputs['labels'] = aligned_labels\n"
            "    return tokenized_inputs\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Word-to-subword NER label alignment | "
            "A word-level NER sequence above a subword-tokenized sequence, with arrows from "
            "each original word to its subwords; first subwords receive the real label and "
            "later subwords/special tokens receive -100/IGN | "
            "Learner should notice that tokenization changes sequence length, so labels must "
            "be explicitly realigned before training]]\n"
            "\n"
            "{{exercise:M01.L03.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 8
            # ----------------------------------------------------------------

            "## 8. Evaluate NER with entity-aware metrics\n"
            "\n"
            "For NER, ordinary token accuracy can be misleading.\n"
            "\n"
            "Most tokens often belong to the `O` class. A weak model can therefore obtain "
            "a deceptively high token accuracy simply by predicting `O` frequently.\n"
            "\n"
            "NER is commonly evaluated with:\n"
            "\n"
            "- **precision** — when the model predicts an entity, how often is it correct?\n"
            "- **recall** — how many true entities did the model recover?\n"
            "- **F1-score** — harmonic mean of precision and recall.\n"
            "\n"
            "Entity evaluation is stricter than independent token evaluation because the "
            "entity span should be correct.\n"
            "\n"
            "The chapter uses `seqeval` for this purpose.\n"
            "\n"
            "```python\n"
            "from seqeval.metrics import f1_score\n"
            "\n"
            "def compute_metrics(eval_pred):\n"
            "    y_pred, y_true = align_predictions(\n"
            "        eval_pred.predictions,\n"
            "        eval_pred.label_ids,\n"
            "    )\n"
            "    return {'f1': f1_score(y_true, y_pred)}\n"
            "```\n"
            "\n"
            "Before passing predictions to the metric, ignored `-100` labels should be removed.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 9
            # ----------------------------------------------------------------

            "## 9. Fine-tune XLM-R for German NER\n"
            "\n"
            "The first experiment fine-tunes the multilingual model on the German PAN-X "
            "training data.\n"
            "\n"
            "A token-classification data collator is useful because both the input sequence "
            "and the label sequence must be padded consistently.\n"
            "\n"
            "```python\n"
            "from transformers import DataCollatorForTokenClassification\n"
            "\n"
            "data_collator = DataCollatorForTokenClassification(xlmr_tokenizer)\n"
            "```\n"
            "\n"
            "The collator pads label positions with `-100`, which means padding tokens are "
            "ignored by the loss function.\n"
            "\n"
            "A simplified training setup is:\n"
            "\n"
            "```python\n"
            "from transformers import Trainer, TrainingArguments\n"
            "\n"
            "training_args = TrainingArguments(\n"
            "    output_dir='xlm-roberta-base-finetuned-panx-de',\n"
            "    num_train_epochs=3,\n"
            "    per_device_train_batch_size=24,\n"
            "    per_device_eval_batch_size=24,\n"
            "    evaluation_strategy='epoch',\n"
            "    weight_decay=0.01,\n"
            ")\n"
            "\n"
            "trainer = Trainer(\n"
            "    model_init=model_init,\n"
            "    args=training_args,\n"
            "    data_collator=data_collator,\n"
            "    compute_metrics=compute_metrics,\n"
            "    train_dataset=panx_de_encoded['train'],\n"
            "    eval_dataset=panx_de_encoded['validation'],\n"
            "    tokenizer=xlmr_tokenizer,\n"
            ")\n"
            "\n"
            "trainer.train()\n"
            "```\n"
            "\n"
            "In the chapter's experiment, the validation F1 rises across the three epochs "
            "to roughly **0.86**. The exact value is less important than the workflow: "
            "prepare aligned labels, fine-tune, evaluate, and then inspect failures.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 10
            # ----------------------------------------------------------------

            "## 10. Error analysis: do not trust one good F1 score\n"
            "\n"
            "A strong aggregate metric does not prove that your model or dataset is healthy.\n"
            "\n"
            "Possible hidden problems include:\n"
            "\n"
            "- accidentally ignoring too many labels,\n"
            "- a bug in the metric function,\n"
            "- majority-class dominance from the `O` label,\n"
            "- systematic confusion between `B-` and `I-` labels,\n"
            "- incorrect or inconsistent annotations in the dataset.\n"
            "\n"
            "### Inspect loss per token\n"
            "\n"
            "Instead of calculating only one loss for an entire batch, calculate loss with "
            "`reduction='none'`. This lets you identify tokens that repeatedly produce large "
            "losses.\n"
            "\n"
            "```python\n"
            "from torch.nn.functional import cross_entropy\n"
            "\n"
            "loss = cross_entropy(\n"
            "    output.logits.view(-1, 7),\n"
            "    labels.view(-1),\n"
            "    reduction='none',\n"
            ")\n"
            "```\n"
            "\n"
            "You can then group by token, entity class, or sequence.\n"
            "\n"
            "### What did the chapter find?\n"
            "\n"
            "The analysis revealed several useful patterns:\n"
            "\n"
            "- frequent words may accumulate high **total** loss simply because they appear often,\n"
            "- some punctuation and rare tokens can have high **average** loss,\n"
            "- `B-ORG` was particularly difficult in the German experiment,\n"
            "- the model often confused `B-ORG` with `I-ORG`,\n"
            "- several high-loss samples exposed questionable dataset annotations.\n"
            "\n"
            "One striking lesson is that **error analysis can reveal dataset problems, not "
            "just model problems**.\n"
            "\n"
            "The chapter notes examples where clearly recognizable names are given surprising "
            "labels by automatically generated annotations. Such automatically derived labels "
            "are sometimes described as a **silver standard**, in contrast with carefully "
            "human-reviewed gold-standard labels.\n"
            "\n"
            "[[IMAGE_NEEDED: NER error-analysis dashboard | "
            "A conceptual figure containing three panels: highest-loss tokens, a normalized "
            "confusion matrix highlighting B-ORG versus I-ORG confusion, and one high-loss "
            "sequence with token labels and predictions | "
            "Learner should notice that useful error analysis moves from aggregate score to "
            "class-level, token-level, and example-level investigation]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 11
            # ----------------------------------------------------------------

            "## 11. Test zero-shot transfer across languages\n"
            "\n"
            "After fine-tuning on German, the model is evaluated directly on the test sets "
            "of the other languages.\n"
            "\n"
            "The chapter reports approximately:\n"
            "\n"
            "| Fine-tuned on | Evaluated on | F1 |\n"
            "|---|---|---:|\n"
            "| German | German | 0.868 |\n"
            "| German | French | 0.714 |\n"
            "| German | Italian | 0.692 |\n"
            "| German | English | 0.589 |\n"
            "\n"
            "The important fact is not that every target language performs equally well. "
            "It does not.\n"
            "\n"
            "The important fact is that the model can make meaningful predictions in "
            "languages for which it received **no labeled NER fine-tuning examples**.\n"
            "\n"
            "### What controls transfer quality?\n"
            "\n"
            "Cross-lingual transfer depends on factors such as:\n"
            "\n"
            "- how much the target language was represented during pretraining,\n"
            "- linguistic similarity to the fine-tuning language,\n"
            "- script and tokenization differences,\n"
            "- domain differences,\n"
            "- label quality and training-set size.\n"
            "\n"
            "Do not assume language-family similarity alone guarantees a particular ranking. "
            "The chapter's English result is a good reminder that empirical evaluation matters.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 12
            # ----------------------------------------------------------------

            "## 12. When is zero-shot transfer worth using?\n"
            "\n"
            "Suppose you can label some French examples. Should you fine-tune a French model "
            "immediately, or reuse the German-fine-tuned model zero-shot?\n"
            "\n"
            "The chapter answers this experimentally by fine-tuning XLM-R on increasingly "
            "large French subsets.\n"
            "\n"
            "With only **250 labeled French examples**, the direct French fine-tuning result "
            "is far below the German-to-French zero-shot result in the chapter's experiment.\n"
            "\n"
            "As more labeled French examples are added, the directly fine-tuned model improves. "
            "The chapter observes that zero-shot transfer remains competitive until roughly "
            "**750 target-language training examples** in that specific experiment.\n"
            "\n"
            "The lesson is not that 750 is a universal threshold. It is that there is a "
            "practical tradeoff:\n"
            "\n"
            "```text\n"
            "little labeled target-language data\n"
            "        → multilingual zero-shot transfer may be attractive\n"
            "\n"
            "more labeled target-language data\n"
            "        → direct target-language fine-tuning becomes increasingly competitive\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Zero-shot versus target-language fine-tuning curve | "
            "A learning curve with number of French labeled training examples on the x-axis, "
            "F1 on the y-axis, a horizontal line for German-to-French zero-shot performance, "
            "and an increasing line for direct French fine-tuning | "
            "Learner should notice that the preferred strategy can change as labeled target-"
            "language data becomes available]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 13
            # ----------------------------------------------------------------

            "## 13. Fine-tune on multiple languages together\n"
            "\n"
            "Instead of choosing between German-only and French-only training, we can combine "
            "training corpora from several languages.\n"
            "\n"
            "The chapter concatenates dataset splits and fine-tunes one XLM-R model on the "
            "combined multilingual data.\n"
            "\n"
            "```python\n"
            "from datasets import DatasetDict, concatenate_datasets\n"
            "\n"
            "def concatenate_splits(corpora):\n"
            "    multi_corpus = DatasetDict()\n"
            "\n"
            "    for split in corpora[0].keys():\n"
            "        multi_corpus[split] = concatenate_datasets(\n"
            "            [corpus[split] for corpus in corpora]\n"
            "        ).shuffle(seed=42)\n"
            "\n"
            "    return multi_corpus\n"
            "```\n"
            "\n"
            "### German + French experiment\n"
            "\n"
            "After combining German and French training data, the chapter reports about:\n"
            "\n"
            "| Evaluated on | F1 after German+French training |\n"
            "|---|---:|\n"
            "| German | 0.866 |\n"
            "| French | 0.868 |\n"
            "| Italian | 0.815 |\n"
            "| English | 0.677 |\n"
            "\n"
            "Adding French training data improves French performance substantially and also "
            "helps the unseen Italian and English test sets in this experiment.\n"
            "\n"
            "### Train on all four languages\n"
            "\n"
            "The chapter's summary table compares three strategies:\n"
            "\n"
            "| Training strategy | de | fr | it | en |\n"
            "|---|---:|---:|---:|---:|\n"
            "| German only | 0.8677 | 0.7141 | 0.6923 | 0.5890 |\n"
            "| Each language separately | 0.8677 | 0.8505 | 0.8192 | 0.7068 |\n"
            "| All languages together | 0.8682 | 0.8647 | 0.8575 | 0.7870 |\n"
            "\n"
            "For this dataset and setup, multilingual joint training gives the strongest "
            "overall cross-language results.\n"
            "\n"
            "The broader lesson is:\n"
            "\n"
            "> **A multilingual model is not only useful for zero-shot transfer. It can also "
            "share useful learning signals when several languages are fine-tuned together.**\n"
            "\n"
            "[[IMAGE_NEEDED: Multilingual fine-tuning comparison | "
            "A simple grouped bar chart comparing German-only, each-language, and all-language "
            "fine-tuning across de, fr, it, and en using the chapter's F1 values | "
            "Learner should notice that joint multilingual training improves the overall balance "
            "across languages in this experiment]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 14
            # ----------------------------------------------------------------

            "## 14. Turn the chapter into a practical workflow\n"
            "\n"
            "A useful way to remember the entire chapter is as one engineering loop:\n"
            "\n"
            "```text\n"
            "1. Choose a multilingual pretrained model\n"
            "            ↓\n"
            "2. Inspect multilingual NER data and IOB2 labels\n"
            "            ↓\n"
            "3. Tokenize words into subwords\n"
            "            ↓\n"
            "4. Realign word-level labels to subword tokens\n"
            "            ↓\n"
            "5. Fine-tune a token-classification head\n"
            "            ↓\n"
            "6. Evaluate with entity-aware F1\n"
            "            ↓\n"
            "7. Analyze high-loss classes, tokens, and sequences\n"
            "            ↓\n"
            "8. Test cross-lingual transfer\n"
            "            ↓\n"
            "9. Decide whether to collect more target-language data\n"
            "            ↓\n"
            "10. Consider multilingual joint fine-tuning\n"
            "```\n"
            "\n"
            "This workflow is more valuable than memorizing individual API calls. APIs may "
            "change, but the reasoning steps remain useful.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Misconceptions
            # ----------------------------------------------------------------

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: One original word always equals one model token\n"
            "\n"
            "> NER labels can be copied directly onto tokenizer output positions.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Subword tokenization can split one word into multiple tokens. The training labels "
            "must be realigned, and ignored positions must be handled explicitly.\n"
            "\n"
            "### Misconception 2: A high token accuracy proves that NER is good\n"
            "\n"
            "> If most individual tokens are correct, entity extraction must be reliable.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The `O` class is often dominant, and entity boundaries matter. Entity-level "
            "precision, recall, and F1 provide a more useful evaluation.\n"
            "\n"
            "### Misconception 3: Zero-shot transfer means the model was never trained\n"
            "\n"
            "> A zero-shot French prediction means the model has never seen language data before.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "XLM-R was pretrained on multilingual text. In the chapter, 'zero-shot' means no "
            "labeled French examples were used during NER fine-tuning before French evaluation.\n"
            "\n"
            "### Misconception 4: Model errors always mean the model is bad\n"
            "\n"
            "> Every high-loss example must be fixed by changing the architecture.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "High-loss examples may expose mislabeled, inconsistent, or automatically generated "
            "training annotations. Error analysis should inspect both model and data.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Terminology
            # ----------------------------------------------------------------

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| NER | Named entity recognition; finding and labeling entity spans in text |\n"
            "| IOB2 | Tagging format using B for beginning, I for inside, and O for outside |\n"
            "| Token classification | Predicting a class label for individual token positions |\n"
            "| Multilingual transformer | One pretrained transformer trained on text from many languages |\n"
            "| Cross-lingual transfer | Reusing learned representations from one language on another |\n"
            "| Zero-shot cross-lingual transfer | Evaluating on a target language without labeled target-language fine-tuning data |\n"
            "| XLM-R | XLM-RoBERTa, the multilingual encoder used in the chapter |\n"
            "| SentencePiece | Language-agnostic subword tokenization approach used by XLM-R |\n"
            "| Subword | A token that represents part of an original word |\n"
            "| `word_ids()` | Tokenizer mapping from subword positions back to original word indices |\n"
            "| `-100` label | Ignore value used so some token positions do not contribute to cross-entropy loss |\n"
            "| Model body | Task-independent pretrained transformer representation layers |\n"
            "| Model head | Task-specific prediction layers attached to the body |\n"
            "| Precision | Fraction of predicted entities that are correct |\n"
            "| Recall | Fraction of true entities that are recovered |\n"
            "| F1-score | Harmonic mean of precision and recall |\n"
            "| Silver-standard labels | Labels generated automatically rather than carefully human-verified |\n"
            "| Error analysis | Investigation of systematic prediction and dataset failures |\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Self-check
            # ----------------------------------------------------------------

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What do `B-PER`, `I-PER`, and `O` mean?\n"
            "2. Why can multilingual pretraining enable transfer between languages?\n"
            "3. What problem does SentencePiece/subword tokenization create for NER labels?\n"
            "4. Why do repeated subwords often receive the label `-100` during training?\n"
            "5. What is the difference between a transformer body and a task head?\n"
            "6. Why can ordinary token accuracy be misleading for NER?\n"
            "7. What did high-loss examples reveal about the PAN-X annotations?\n"
            "8. What does zero-shot German-to-French transfer mean in this chapter?\n"
            "9. Why might target-language fine-tuning eventually beat zero-shot transfer as "
            "more labeled data becomes available?\n"
            "10. Why can multilingual joint fine-tuning improve languages that were not the "
            "largest part of the training corpus?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**Multilingual NER is not only about choosing XLM-R. The critical engineering "
            "work is aligning word labels with subword tokens, evaluating entities correctly, "
            "inspecting errors, and choosing between zero-shot, monolingual, and multilingual "
            "fine-tuning based on the labeled data available for each language.**\n"
        ),

        "estimated_minutes": 120,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "multilingual-ner",
                "title": "The problem: one NER system, many languages",
                "order": 1,
            },
            {
                "id": "dataset",
                "title": "Build a multilingual NER dataset",
                "order": 2,
            },
            {
                "id": "cross-lingual-intuition",
                "title": "Why multilingual transformers transfer across languages",
                "order": 3,
            },
            {
                "id": "tokenization",
                "title": "Tokenization matters in NER",
                "order": 4,
            },
            {
                "id": "token-classification",
                "title": "NER is token classification",
                "order": 5,
            },
            {
                "id": "custom-model",
                "title": "Build a custom XLM-R token classifier",
                "order": 6,
            },
            {
                "id": "label-alignment",
                "title": "Align word labels with subword tokens",
                "order": 7,
            },
            {
                "id": "evaluation",
                "title": "Evaluate NER with entity-aware metrics",
                "order": 8,
            },
            {
                "id": "fine-tuning",
                "title": "Fine-tune XLM-R for German NER",
                "order": 9,
            },
            {
                "id": "error-analysis",
                "title": "Error analysis",
                "order": 10,
            },
            {
                "id": "zero-shot-results",
                "title": "Test zero-shot transfer across languages",
                "order": 11,
            },
            {
                "id": "zero-shot-vs-labeled",
                "title": "When is zero-shot transfer worth using?",
                "order": 12,
            },
            {
                "id": "multilingual-training",
                "title": "Fine-tune on multiple languages together",
                "order": 13,
            },
            {
                "id": "production-workflow",
                "title": "Practical multilingual NER workflow",
                "order": 14,
            },
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L03.EX01",
            "title": "Design a Cross-Lingual NER Strategy",
            "lesson_code": "M01.L03",
            "section_id": "cross-lingual-intuition",
            "placement": "after_section",
            "description": (
                "Choose a reasonable multilingual NER strategy when labeled data is "
                "abundant in one language but scarce in another."
            ),
            "instructions": (
                "1. Assume you have 12,000 labeled German NER sentences and only 100 labeled "
                "French sentences.\n"
                "2. Explain why training a German-only monolingual model is not sufficient "
                "for the whole product.\n"
                "3. Explain why a multilingual pretrained model is useful.\n"
                "4. Describe how you would test German-to-French zero-shot transfer.\n"
                "5. Name the metric you would use to compare strategies.\n"
                "6. State what evidence would make you decide to collect more French labels."
            ),
            "expected_output": (
                "A short experiment plan containing source language, target language, "
                "fine-tuning strategy, French evaluation procedure, entity-level F1 metric, "
                "and a decision rule for collecting more target-language labels."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "cross-lingual-transfer",
                "experiment-design",
                "ner-evaluation",
            ],
        },

        {
            "id": "M01.L03.EX02",
            "title": "Align IOB2 Labels After Subword Tokenization",
            "lesson_code": "M01.L03",
            "section_id": "label-alignment",
            "placement": "after_section",
            "description": (
                "Practice the most important preprocessing step in transformer-based NER: "
                "mapping word-level labels onto subword tokens."
            ),
            "instructions": (
                "1. Start with the words ['New', 'York', 'University'] and labels "
                "['B-ORG', 'I-ORG', 'I-ORG'].\n"
                "2. Assume the tokenizer produces ['<s>', '▁New', '▁York', "
                "'▁Univers', 'ity', '</s>'].\n"
                "3. Assign a word ID to every produced token.\n"
                "4. Assign the original label only to the first subword of each word.\n"
                "5. Assign -100 to special tokens and to the later 'ity' subword.\n"
                "6. Explain why assigning I-ORG to both '▁Univers' and 'ity' would change "
                "the training objective used by this lesson."
            ),
            "expected_output": (
                "A token / word-ID / aligned-label table. The special tokens and the second "
                "subword of University should use -100, while the first subword should keep "
                "I-ORG."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "subword-tokenization",
                "label-alignment",
                "iob2",
                "token-classification",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L03.QZ01",
        "title": "Multilingual Named Entity Recognition — Knowledge Check",
        "lesson_code": "M01.L03",
        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L03.Q01",
                "section_id": "multilingual-ner",
                "question": (
                    "In IOB2 tagging, what does the label I-ORG mean?"
                ),
                "options": [
                    "The token begins a person entity.",
                    "The token is inside an organization entity that has already begun.",
                    "The token is outside every entity.",
                    "The token begins a location entity.",
                ],
                "correct": 1,
                "explanation": (
                    "`I-ORG` marks a token inside an organization span after the entity "
                    "has begun. A beginning token would use `B-ORG`."
                ),
            },

            {
                "id": "M01.L03.Q02",
                "section_id": "label-alignment",
                "question": (
                    "Why are many subword positions assigned the label -100 during "
                    "token-classification training?"
                ),
                "options": [
                    "To tell the tokenizer to delete the subword permanently.",
                    "To convert the subword into an O entity.",
                    "To make PyTorch ignore that position when computing cross-entropy loss.",
                    "To mark the token as belonging to every entity class.",
                ],
                "correct": 2,
                "explanation": (
                    "The loss function ignores targets equal to its ignore index. In this "
                    "workflow, `-100` prevents special tokens and repeated subwords from "
                    "contributing to the loss."
                ),
            },

            {
                "id": "M01.L03.Q03",
                "section_id": "evaluation",
                "question": (
                    "Why is entity-level F1 generally more informative than naive token "
                    "accuracy for NER?"
                ),
                "options": [
                    "Because NER never has an O label.",
                    "Because the majority O class can make token accuracy look good even "
                    "when entity detection and boundaries are poor.",
                    "Because F1 ignores every incorrect prediction.",
                    "Because token accuracy cannot be computed for transformer models.",
                ],
                "correct": 1,
                "explanation": (
                    "NER datasets often contain many non-entity tokens. Predicting O often "
                    "can inflate token accuracy while the system still misses or breaks "
                    "important entity spans."
                ),
            },

            {
                "id": "M01.L03.Q04",
                "section_id": "error-analysis",
                "question": (
                    "What is one reason to inspect the highest-loss NER examples even when "
                    "the overall F1 score is strong?"
                ),
                "options": [
                    "High-loss examples can reveal systematic model errors or bad dataset labels.",
                    "High-loss examples prove that the tokenizer should always be removed.",
                    "Only high-loss examples are used during inference.",
                    "A strong F1 score makes validation data unnecessary.",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter's analysis finds both model confusions and suspicious "
                    "annotations. Error analysis is therefore useful for debugging the whole "
                    "model-data pipeline."
                ),
            },

            {
                "id": "M01.L03.Q05",
                "section_id": "multilingual-training",
                "type": "open",
                "question": (
                    "You have a multilingual NER application with abundant German labels, "
                    "moderate French labels, and almost no Italian labels. Describe an "
                    "experiment comparing zero-shot transfer, language-specific fine-tuning, "
                    "and joint multilingual fine-tuning. State what you would evaluate before "
                    "choosing a production strategy."
                ),
            },
        ],

        "passing_score": 70,
    },
}
