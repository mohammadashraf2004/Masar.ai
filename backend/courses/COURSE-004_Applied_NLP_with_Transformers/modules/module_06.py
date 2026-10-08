"""M01.L05 — Summarization.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-004, Chapter 6.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L05"
MODULE_ORDER = 6
MODULE_TITLE = "Sequence-to-Sequence NLP & Summarization"
MODULE_DESCRIPTION = (
    "Learn how transformer models summarize long text, how summarization quality "
    "is evaluated, and how an encoder-decoder model can be fine-tuned for dialogue summaries."
)

SOURCE_CHAPTER = 6
SOURCE_PAGES = "Chapter 6"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Summarization",
    "slug": "applied-nlp-transformers-m01-l05-summarization",
    "description": (
        "Learn extractive and abstractive summarization, compare transformer summarizers, "
        "evaluate generated summaries with BLEU and ROUGE, and fine-tune PEGASUS on dialogue data."
    ),
    "order": 5,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 2.0,
    "skill_tags": [
        "summarization",
        "sequence-to-sequence",
        "encoder-decoder",
        "pegasus",
        "bart",
        "t5",
        "bleu",
        "rouge",
        "teacher-forcing",
        "gradient-accumulation",
        "module-01",
    ],
    "prerequisite_ids": ["M01.L01", "M01.L02", "M01.L03", "M01.L04"],

    "lesson": {
        "title": "Summarization",

        "content": (
            "# Summarization\n"
            "\n"
            "> **Course:** Applied NLP with Transformers  \n"
            "> **Lesson:** M01.L05  \n"
            "> **Module:** Transformer Foundations  \n"
            "> **Source alignment:** BOOK-004, Chapter 6. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain summarization as a sequence-to-sequence generation task.\n"
            "- Distinguish extractive and abstractive summaries.\n"
            "- Build a simple first-sentences baseline before evaluating large models.\n"
            "- Explain how GPT-2, T5, BART, and PEGASUS approach summarization differently.\n"
            "- Explain why ordinary accuracy is unsuitable for generated summaries.\n"
            "- Describe the intuition behind BLEU, SacreBLEU, ROUGE, and ROUGE-L.\n"
            "- Evaluate a summarization model on a dataset rather than a single example.\n"
            "- Explain domain shift using CNN/DailyMail and SAMSum.\n"
            "- Prepare source and target sequences for seq2seq fine-tuning.\n"
            "- Explain teacher forcing and shifted decoder inputs.\n"
            "- Explain why gradient accumulation is useful when GPU memory is limited.\n"
            "- Judge summaries with both automatic metrics and human inspection.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why summarization is difficult\n"
            "\n"
            "Summarization sounds simple: take a long document and make it shorter.\n"
            "\n"
            "But a good summarizer needs several abilities at once:\n"
            "\n"
            "- understand the important information,\n"
            "- ignore less important details,\n"
            "- preserve the main meaning,\n"
            "- produce fluent language,\n"
            "- avoid inventing unsupported facts,\n"
            "- adapt to the document domain.\n"
            "\n"
            "Summarizing a news article is not the same as summarizing a legal contract "
            "or a chat conversation. The style and information priorities are different.\n"
            "\n"
            "Summarization is naturally framed as a **sequence-to-sequence** task:\n"
            "\n"
            "```text\n"
            "long input text\n"
            "      ↓\n"
            "encoder-decoder transformer\n"
            "      ↓\n"
            "short target summary\n"
            "```\n"
            "\n"
            '{{image:summarization-seq2seq}}'
            '\n'
            "\n"
            "### Extractive versus abstractive summarization\n"
            "\n"
            "**Extractive summarization** selects or copies important portions of the source.\n"
            "\n"
            "**Abstractive summarization** can generate new sentences that express the source "
            "meaning in a shorter way.\n"
            "\n"
            "The CNN/DailyMail summaries used in this chapter are treated as abstractive targets.\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Start with the CNN/DailyMail dataset\n"
            "\n"
            "The chapter begins with CNN/DailyMail, a large summarization dataset containing "
            "roughly 300,000 article-summary pairs.\n"
            "\n"
            "Its main fields are:\n"
            "\n"
            "| Field | Meaning |\n"
            "|---|---|\n"
            "| `article` | Source news article |\n"
            "| `highlights` | Reference summary |\n"
            "| `id` | Unique article identifier |\n"
            "\n"
            "A key characteristic is the large compression ratio. An article may contain "
            "thousands of characters while its reference summary contains only a few lines.\n"
            "\n"
            "```python\n"
            "from datasets import load_dataset\n"
            "\n"
            "dataset = load_dataset('cnn_dailymail', version='3.0.0')\n"
            "print(dataset['train'].column_names)\n"
            "```\n"
            "\n"
            "### The context-length problem\n"
            "\n"
            "Long documents create a practical limitation: many transformer models accept "
            "only a limited number of input tokens.\n"
            "\n"
            "A crude solution is truncation:\n"
            "\n"
            "```text\n"
            "article longer than model limit\n"
            "            ↓\n"
            "keep first N tokens\n"
            "            ↓\n"
            "discard the rest\n"
            "```\n"
            "\n"
            "This is easy, but important information near the end of the document may be lost.\n"
            "\n"
            "[[IMAGE_NEEDED: Long-document truncation problem | "
            "A long article represented as many text blocks, a model context window covering "
            "only the beginning, and later blocks faded or cut off | "
            "Learner should notice that truncation can remove information that may be important "
            "for the final summary]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Always build a simple baseline\n"
            "\n"
            "Before comparing huge transformer models, the chapter creates a very simple "
            "summarization baseline: return the first three sentences.\n"
            "\n"
            "```python\n"
            "from nltk.tokenize import sent_tokenize\n"
            "\n"
            "def three_sentence_summary(text):\n"
            "    return '\\n'.join(sent_tokenize(text)[:3])\n"
            "```\n"
            "\n"
            "Why is this useful?\n"
            "\n"
            "Because a complex model is only valuable if it improves on a reasonable simple "
            "strategy. News articles often place important facts near the beginning, so a "
            "lead-sentence baseline can be surprisingly competitive.\n"
            "\n"
            "A baseline gives you a reference point for answering:\n"
            "\n"
            "> Is the expensive model actually better than something trivial?\n"
            "\n"
            "{{exercise:M01.L05.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Compare several transformer summarizers\n"
            "\n"
            "The chapter compares several model families using the same article excerpt.\n"
            "\n"
            "### GPT-2\n"
            "\n"
            "GPT-2 is a decoder-only text generator, not a model specifically trained for "
            "faithful summarization. The chapter prompts it with `TL;DR:`.\n"
            "\n"
            "```python\n"
            "from transformers import pipeline\n"
            "\n"
            "pipe = pipeline('text-generation', model='gpt2-xl')\n"
            "gpt2_query = sample_text + '\\nTL;DR:\\n'\n"
            "```\n"
            "\n"
            "This can produce summary-like text, but the chapter shows that it may invent "
            "facts because summarization faithfulness was not its dedicated training objective.\n"
            "\n"
            "### T5\n"
            "\n"
            "T5 frames many NLP tasks as **text-to-text** problems. Summarization is one "
            "task in that unified formulation.\n"
            "\n"
            "```text\n"
            "summarize: <ARTICLE>\n"
            "```\n"
            "\n"
            "Using the summarization pipeline hides that prompt formatting for us.\n"
            "\n"
            "### BART\n"
            "\n"
            "BART is an encoder-decoder model trained to reconstruct corrupted input text. "
            "The chapter uses a checkpoint fine-tuned specifically on CNN/DailyMail.\n"
            "\n"
            "### PEGASUS\n"
            "\n"
            "PEGASUS is also an encoder-decoder model, but its pretraining objective is "
            "especially aligned with summarization. It learns to reconstruct important "
            "sentences removed from multi-sentence documents.\n"
            "\n"
            "[[IMAGE_NEEDED: Comparison of summarization model families | "
            "A compact four-column visual for GPT-2, T5, BART, and PEGASUS showing decoder-only "
            "prompting for GPT-2 and encoder-decoder summarization for the other models, with "
            "their pretraining idea summarized beneath each | "
            "Learner should notice that models differ both in architecture and in how closely "
            "their training objective matches summarization]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Why looking at one summary is not enough\n"
            "\n"
            "When the chapter compares one CNN/DailyMail example, the outputs look very different.\n"
            "\n"
            "The GPT-2 continuation is less faithful and includes invented claims. T5, BART, "
            "and PEGASUS are much closer to the reference summary.\n"
            "\n"
            "This qualitative inspection is useful, but it is not sufficient for choosing "
            "a production model.\n"
            "\n"
            "A single example can be unusually easy or unusually hard.\n"
            "\n"
            "So we need:\n"
            "\n"
            "```text\n"
            "many examples\n"
            "+\n"
            "consistent evaluation metric\n"
            "+\n"
            "human inspection\n"
            "```\n"
            "\n"
            "This leads to one of the hardest questions in text generation:\n"
            "\n"
            "> How do we automatically score a generated text when several different wordings "
            "could all be correct?\n"
            "\n"
            "---\n"
            "\n"

            "## 6. BLEU: precision-oriented overlap\n"
            "\n"
            "Exact-match accuracy is too strict for generated language.\n"
            "\n"
            "Two sentences can communicate the same meaning with different words. BLEU tries "
            "to address this by comparing overlapping words and **n-grams** between generated "
            "text and reference text.\n"
            "\n"
            "### Basic intuition\n"
            "\n"
            "BLEU is precision-oriented:\n"
            "\n"
            "```text\n"
            "Of the n-grams the model generated,\n"
            "how many are supported by the reference?\n"
            "```\n"
            "\n"
            "BLEU also clips repeated counts. This prevents a system from receiving a perfect "
            "score simply by repeating one reference word many times.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Reference:  the cat is on the mat\n"
            "Prediction: the the the the the the\n"
            "```\n"
            "\n"
            "Only as many occurrences of `the` as appear in the reference should count.\n"
            "\n"
            "### Brevity penalty\n"
            "\n"
            "Precision alone can reward very short predictions. BLEU therefore includes a "
            "brevity penalty when generated text is shorter than the reference.\n"
            "\n"
            "### SacreBLEU\n"
            "\n"
            "BLEU results can vary when different tokenization procedures are used. "
            "**SacreBLEU** standardizes the tokenization step, making benchmark comparisons "
            "more reproducible.\n"
            "\n"
            "### Limitation\n"
            "\n"
            "BLEU still depends heavily on surface overlap. Synonyms or valid paraphrases can "
            "receive lower scores even when humans consider them correct.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. ROUGE: focus on information covered by the summary\n"
            "\n"
            "ROUGE is especially common for summarization.\n"
            "\n"
            "Its intuition is closer to recall:\n"
            "\n"
            "```text\n"
            "Of the important n-grams in the reference summary,\n"
            "how many did the generated summary recover?\n"
            "```\n"
            "\n"
            "Modern reporting commonly combines precision and recall into an F1-style score.\n"
            "\n"
            "Common ROUGE variants include:\n"
            "\n"
            "| Metric | Main idea |\n"
            "|---|---|\n"
            "| ROUGE-1 | Unigram overlap |\n"
            "| ROUGE-2 | Bigram overlap |\n"
            "| ROUGE-L | Longest common subsequence-based similarity |\n"
            "| ROUGE-Lsum | LCS-style evaluation over the whole summary |\n"
            "\n"
            "### BLEU versus ROUGE intuition\n"
            "\n"
            "```text\n"
            "BLEU  → Did the generation mostly use supported n-grams?\n"
            "ROUGE → Did the generation recover the important reference content?\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: BLEU versus ROUGE intuition | "
            "Two overlapping sets labeled generated n-grams and reference n-grams, with BLEU "
            "highlighting the generated side as precision-oriented and ROUGE highlighting the "
            "reference side as recall-oriented | "
            "Learner should understand the directional difference without memorizing formulas]]\n"
            "\n"
            "The chapter's single-example comparison gives PEGASUS the strongest ROUGE scores "
            "among the compared outputs, but explicitly warns that one example is not reliable "
            "enough for model selection.\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Evaluate on many examples, not one\n"
            "\n"
            "A proper model comparison uses a test set rather than one manually chosen article.\n"
            "\n"
            "The chapter first evaluates the three-sentence baseline on 1,000 sampled "
            "CNN/DailyMail test examples.\n"
            "\n"
            "It then evaluates PEGASUS in batches.\n"
            "\n"
            "A simplified evaluation pattern is:\n"
            "\n"
            "```python\n"
            "def chunks(items, batch_size):\n"
            "    for i in range(0, len(items), batch_size):\n"
            "        yield items[i:i + batch_size]\n"
            "\n"
            "def evaluate_summaries(\n"
            "    dataset,\n"
            "    metric,\n"
            "    model,\n"
            "    tokenizer,\n"
            "    batch_size=8,\n"
            "):\n"
            "    for article_batch, target_batch in zip(\n"
            "        chunks(dataset['article'], batch_size),\n"
            "        chunks(dataset['highlights'], batch_size),\n"
            "    ):\n"
            "        inputs = tokenizer(\n"
            "            article_batch,\n"
            "            max_length=1024,\n"
            "            truncation=True,\n"
            "            padding=True,\n"
            "            return_tensors='pt',\n"
            "        )\n"
            "\n"
            "        summaries = model.generate(\n"
            "            input_ids=inputs['input_ids'],\n"
            "            attention_mask=inputs['attention_mask'],\n"
            "            num_beams=8,\n"
            "            max_length=128,\n"
            "            length_penalty=0.8,\n"
            "        )\n"
            "\n"
            "        decoded = tokenizer.batch_decode(\n"
            "            summaries,\n"
            "            skip_special_tokens=True,\n"
            "        )\n"
            "\n"
            "        metric.add_batch(\n"
            "            predictions=decoded,\n"
            "            references=target_batch,\n"
            "        )\n"
            "\n"
            "    return metric.compute()\n"
            "```\n"
            "\n"
            "### Generation metrics depend on decoding\n"
            "\n"
            "A subtle but important observation from the chapter is that training loss and "
            "ROUGE are not the same thing.\n"
            "\n"
            "Loss is computed from model probabilities under the training objective. ROUGE "
            "is computed from the text produced by a specific decoding strategy.\n"
            "\n"
            "Changing beam size, length penalty, or another generation setting can therefore "
            "change ROUGE without changing the trained model weights.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Domain shift: news summaries are not dialogue summaries\n"
            "\n"
            "Next, the chapter switches from CNN/DailyMail news articles to **SAMSum**, a "
            "dataset containing chat-style dialogues and short human summaries.\n"
            "\n"
            "A dialogue might contain:\n"
            "\n"
            "```text\n"
            "Hannah: Do you have Betty's number?\n"
            "Amanda: I can't find it. Ask Larry.\n"
            "Hannah: I'd rather you text him.\n"
            "```\n"
            "\n"
            "with a reference summary such as:\n"
            "\n"
            "```text\n"
            "Hannah needs Betty's number, but Amanda does not have it.\n"
            "She needs to contact Larry.\n"
            "```\n"
            "\n"
            "A PEGASUS checkpoint fine-tuned on CNN/DailyMail performs much worse on SAMSum.\n"
            "\n"
            "This is **domain shift**.\n"
            "\n"
            "The model knows how to summarize, but the source style and target-summary style "
            "have changed from formal news to conversational dialogue.\n"
            "\n"
            "The chapter reports ROUGE scores around:\n"
            "\n"
            "| Metric | CNN/DailyMail-trained PEGASUS on SAMSum |\n"
            "|---|---:|\n"
            "| ROUGE-1 | 0.296 |\n"
            "| ROUGE-2 | 0.088 |\n"
            "| ROUGE-L | 0.230 |\n"
            "| ROUGE-Lsum | 0.230 |\n"
            "\n"
            "This gives us a baseline before domain-specific fine-tuning.\n"
            "\n"
            "[[IMAGE_NEEDED: Domain shift from news to dialogue | "
            "A side-by-side visual showing a structured news article with headline-style "
            "summary on the left and an informal chat dialogue with abstractive conversational "
            "summary on the right | "
            "Learner should notice that the task name is the same but the data distribution "
            "and desired output style are different]]\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Prepare source and target sequences for fine-tuning\n"
            "\n"
            "Training an encoder-decoder summarizer requires two tokenized sequences:\n"
            "\n"
            "- the **source** dialogue for the encoder,\n"
            "- the **target** summary for the decoder.\n"
            "\n"
            "The chapter observes that most SAMSum dialogues are roughly 100–200 tokens "
            "and summaries are usually much shorter, around 20–40 tokens.\n"
            "\n"
            "A preprocessing function looks conceptually like this:\n"
            "\n"
            "```python\n"
            "def convert_examples_to_features(example_batch):\n"
            "    input_encodings = tokenizer(\n"
            "        example_batch['dialogue'],\n"
            "        max_length=1024,\n"
            "        truncation=True,\n"
            "    )\n"
            "\n"
            "    target_encodings = tokenizer(\n"
            "        text_target=example_batch['summary'],\n"
            "        max_length=128,\n"
            "        truncation=True,\n"
            "    )\n"
            "\n"
            "    return {\n"
            "        'input_ids': input_encodings['input_ids'],\n"
            "        'attention_mask': input_encodings['attention_mask'],\n"
            "        'labels': target_encodings['input_ids'],\n"
            "    }\n"
            "```\n"
            "\n"
            "The key idea is that encoder inputs and decoder targets play different roles, "
            "even though both begin as text.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Teacher forcing: what does the decoder see during training?\n"
            "\n"
            "During generation, the decoder uses its own previously generated tokens.\n"
            "\n"
            "During supervised training, we already know the correct target summary. "
            "A common strategy is **teacher forcing**: feed the decoder the correct previous "
            "target tokens while asking it to predict the next target token.\n"
            "\n"
            "Suppose the target is:\n"
            "\n"
            "```text\n"
            "Transformers are awesome for summarization\n"
            "```\n"
            "\n"
            "The relationship is approximately:\n"
            "\n"
            "| Step | Decoder input so far | Target to predict |\n"
            "|---:|---|---|\n"
            "| 1 | `[START]` | Transformers |\n"
            "| 2 | `[START] Transformers` | are |\n"
            "| 3 | `[START] Transformers are` | awesome |\n"
            "| 4 | `[START] Transformers are awesome` | for |\n"
            "| 5 | `[START] Transformers are awesome for` | summarization |\n"
            "\n"
            "This is often described as **shifting the labels to the right**.\n"
            "\n"
            "The decoder's causal mask prevents it from seeing future target tokens.\n"
            "\n"
            "[[IMAGE_NEEDED: Teacher forcing in an encoder-decoder model | "
            "A training diagram where the encoder receives the source dialogue and the decoder "
            "receives the gold target summary shifted right by one token, with arrows showing "
            "next-token prediction at each decoder position | "
            "Learner should notice that the decoder sees previous correct target tokens during "
            "training but never the current/future target token it is predicting]]\n"
            "\n"
            "### Let the data collator handle the mechanics\n"
            "\n"
            "The chapter uses `DataCollatorForSeq2Seq`, which handles padding and prepares "
            "decoder-side inputs appropriately.\n"
            "\n"
            "```python\n"
            "from transformers import DataCollatorForSeq2Seq\n"
            "\n"
            "seq2seq_data_collator = DataCollatorForSeq2Seq(\n"
            "    tokenizer,\n"
            "    model=model,\n"
            ")\n"
            "```\n"
            "\n"
            "Padding positions in labels are typically set to `-100` so they do not "
            "contribute to the loss.\n"
            "\n"
            "{{exercise:M01.L05.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Fine-tune when the model barely fits in memory\n"
            "\n"
            "Large encoder-decoder models can consume substantial GPU memory.\n"
            "\n"
            "The chapter uses a per-device batch size of 1. A batch that small may make "
            "optimization less stable, so it uses **gradient accumulation**.\n"
            "\n"
            "Suppose:\n"
            "\n"
            "```text\n"
            "per-device batch size = 1\n"
            "gradient accumulation steps = 16\n"
            "```\n"
            "\n"
            "Instead of updating model weights after every example, gradients are accumulated "
            "across 16 small forward/backward passes before one optimizer update.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "microbatch 1  → gradients ┐\n"
            "microbatch 2  → gradients │\n"
            "...\n"
            "microbatch 16 → gradients ┘\n"
            "              ↓\n"
            "       optimizer step\n"
            "```\n"
            "\n"
            "This approximates a larger effective batch while reducing peak memory use.\n"
            "\n"
            "A training configuration from the chapter includes:\n"
            "\n"
            "```python\n"
            "training_args = TrainingArguments(\n"
            "    output_dir='pegasus-samsum',\n"
            "    num_train_epochs=1,\n"
            "    warmup_steps=500,\n"
            "    per_device_train_batch_size=1,\n"
            "    per_device_eval_batch_size=1,\n"
            "    gradient_accumulation_steps=16,\n"
            "    weight_decay=0.01,\n"
            ")\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Fine-tuning PEGASUS on SAMSum\n"
            "\n"
            "Once the source/target examples and seq2seq collator are ready, the model can "
            "be fine-tuned on SAMSum.\n"
            "\n"
            "After fine-tuning, the chapter reports approximately:\n"
            "\n"
            "| Metric | Before SAMSum fine-tuning | After SAMSum fine-tuning |\n"
            "|---|---:|---:|\n"
            "| ROUGE-1 | 0.296 | 0.428 |\n"
            "| ROUGE-2 | 0.088 | 0.201 |\n"
            "| ROUGE-L | 0.230 | 0.341 |\n"
            "| ROUGE-Lsum | 0.230 | 0.341 |\n"
            "\n"
            "The improvement demonstrates that being trained for the general task of "
            "summarization is not enough. Adapting to the **target domain** matters.\n"
            "\n"
            "The resulting model also produces a more abstractive dialogue summary instead "
            "of mostly copying important dialogue lines.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Metrics are useful, but humans still matter\n"
            "\n"
            "BLEU and ROUGE make large-scale comparison possible, but they are not perfect "
            "measures of summary quality.\n"
            "\n"
            "A generated summary can have good lexical overlap while still being misleading. "
            "Another summary may use different wording and receive lower overlap while being "
            "perfectly useful.\n"
            "\n"
            "For important applications, evaluate both:\n"
            "\n"
            "### Automatic signals\n"
            "\n"
            "- ROUGE / other task metrics,\n"
            "- validation loss,\n"
            "- length statistics,\n"
            "- latency and computational cost.\n"
            "\n"
            "### Human qualities\n"
            "\n"
            "- factual faithfulness,\n"
            "- coverage of important information,\n"
            "- conciseness,\n"
            "- fluency,\n"
            "- usefulness for the target user/domain.\n"
            "\n"
            "The chapter's conclusion emphasizes that human judgment remains essential.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Long-document summarization remains difficult\n"
            "\n"
            "What if the source document is longer than the model's context window?\n"
            "\n"
            "There is no single universal solution in the chapter.\n"
            "\n"
            "Truncation is simple but may discard important information. More advanced "
            "approaches can divide documents into pieces, summarize recursively, or use "
            "architectures designed for longer context.\n"
            "\n"
            "The important engineering lesson is:\n"
            "\n"
            "> **Do not silently assume that a summarizer has read information that was "
            "outside its input context.**\n"
            "\n"
            "[[IMAGE_NEEDED: Hierarchical long-document summarization | "
            "A long document split into several chunks, each producing a short partial summary, "
            "followed by a second summarization stage combining those partial summaries | "
            "Learner should see one conceptual alternative to simply truncating a long document]]\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Summarization is just extracting the first sentences\n"
            "\n"
            "> A strong summarizer only needs to copy the most important sentences.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A simple extractive baseline can be useful, but abstractive summarization may "
            "need to combine information and express it in new wording.\n"
            "\n"
            "### Misconception 2: The model with the lowest loss must have the best ROUGE\n"
            "\n"
            "> Training loss completely determines generated summary quality.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "ROUGE depends on the actual decoded text and therefore also on generation settings "
            "such as beam search and length penalty.\n"
            "\n"
            "### Misconception 3: A model trained for summarization works equally well everywhere\n"
            "\n"
            "> A CNN/DailyMail summarizer should automatically work well for chat conversations.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Domain shift changes both the source-text style and the desired summary style. "
            "Fine-tuning on in-domain data can substantially improve performance.\n"
            "\n"
            "### Misconception 4: ROUGE proves factual correctness\n"
            "\n"
            "> High overlap with the reference guarantees that every generated statement is true.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "ROUGE measures textual overlap patterns. Human inspection is still important for "
            "faithfulness, factuality, and usefulness.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Summarization | Producing a shorter representation of a source text |\n"
            "| Extractive summarization | Building a summary largely by selecting source passages |\n"
            "| Abstractive summarization | Generating new text that expresses the source meaning concisely |\n"
            "| Seq2seq | Sequence-to-sequence setup with input and target sequences |\n"
            "| Reference summary | Human or dataset target used to evaluate a generated summary |\n"
            "| Baseline | Simple comparison method used as a minimum performance reference |\n"
            "| BLEU | Precision-oriented n-gram overlap metric commonly used in generation/translation |\n"
            "| SacreBLEU | BLEU implementation with standardized tokenization for reproducibility |\n"
            "| ROUGE | Family of overlap metrics commonly used for summarization |\n"
            "| ROUGE-L | ROUGE variant based on longest common subsequence |\n"
            "| Domain shift | Difference between training/fine-tuning data and target-use data |\n"
            "| Teacher forcing | Training decoder with previous ground-truth target tokens |\n"
            "| Shift-right | Preparing decoder inputs by offsetting target tokens by one position |\n"
            "| Data collator | Batch-preparation component handling padding and labels |\n"
            "| Gradient accumulation | Accumulating gradients across microbatches before an optimizer step |\n"
            "| Length penalty | Decoding parameter affecting preference for shorter/longer generated sequences |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why is summarization a sequence-to-sequence task?\n"
            "2. What is the difference between extractive and abstractive summarization?\n"
            "3. Why is a three-sentence baseline worth evaluating?\n"
            "4. Why does GPT-2 behave differently from a model specifically trained for summarization?\n"
            "5. What is the main intuition behind BLEU?\n"
            "6. Why is ROUGE especially common for summarization?\n"
            "7. Why can a CNN/DailyMail summarizer perform poorly on SAMSum?\n"
            "8. What does teacher forcing give the decoder during training?\n"
            "9. Why are padding target positions often assigned `-100`?\n"
            "10. What problem does gradient accumulation solve?\n"
            "11. Why can ROUGE change when decoding settings change?\n"
            "12. Why should human evaluation remain part of summarization assessment?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A summarization system is more than a model checkpoint: you need a strong "
            "baseline, suitable encoder-decoder architecture, source/target preprocessing, "
            "appropriate decoding, domain-specific fine-tuning, automatic metrics such as "
            "ROUGE, and human checks for faithfulness and usefulness.**\n"
        ),

        "estimated_minutes": 120,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "summarization-problem", "title": "Why summarization is difficult", "order": 1},
            {"id": "cnn-dailymail", "title": "CNN/DailyMail dataset", "order": 2},
            {"id": "baseline", "title": "Build a simple baseline", "order": 3},
            {"id": "models", "title": "Compare transformer summarizers", "order": 4},
            {"id": "qualitative-comparison", "title": "Qualitative comparison", "order": 5},
            {"id": "bleu", "title": "BLEU", "order": 6},
            {"id": "rouge", "title": "ROUGE", "order": 7},
            {"id": "proper-evaluation", "title": "Evaluate on many examples", "order": 8},
            {"id": "domain-shift", "title": "Domain shift", "order": 9},
            {"id": "prepare-seq2seq", "title": "Prepare seq2seq data", "order": 10},
            {"id": "teacher-forcing", "title": "Teacher forcing", "order": 11},
            {"id": "gradient-accumulation", "title": "Gradient accumulation", "order": 12},
            {"id": "fine-tune-results", "title": "Fine-tuning PEGASUS on SAMSum", "order": 13},
            {"id": "human-evaluation", "title": "Human evaluation", "order": 14},
            {"id": "long-documents", "title": "Long-document summarization", "order": 15},
        ],
    },

    "exercises": [
        {
            "id": "M01.L05.EX01",
            "title": "Build and Critique a Summarization Baseline",
            "lesson_code": "M01.L05",
            "section_id": "baseline",
            "placement": "after_section",
            "description": (
                "Practice distinguishing a simple extractive baseline from a true "
                "abstractive summarizer."
            ),
            "instructions": (
                "1. Take any six-sentence news-style paragraph.\n"
                "2. Use the first three sentences as a baseline summary.\n"
                "3. Write a separate two-sentence abstractive summary in your own words.\n"
                "4. Compare which important facts each summary keeps or loses.\n"
                "5. Identify one case where the first-three-sentence baseline would fail.\n"
                "6. Explain why the baseline should still be kept during model evaluation."
            ),
            "expected_output": (
                "A source paragraph, a three-sentence extractive baseline, a shorter "
                "abstractive summary, and a comparison explaining coverage, redundancy, "
                "and one failure mode of the baseline."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "summarization-baselines",
                "extractive-vs-abstractive",
                "evaluation-reasoning",
            ],
        },
        {
            "id": "M01.L05.EX02",
            "title": "Trace Teacher Forcing",
            "lesson_code": "M01.L05",
            "section_id": "teacher-forcing",
            "placement": "after_section",
            "description": (
                "Practice preparing decoder inputs and targets for seq2seq training."
            ),
            "instructions": (
                "1. Use the target summary 'Alice called Bob today'.\n"
                "2. Write the decoder input at each training step, beginning with a start token.\n"
                "3. Write the next target token expected at each step.\n"
                "4. Explain why the gold target is shifted by one position.\n"
                "5. Explain why future target tokens must remain hidden.\n"
                "6. State what should happen to padding labels when computing loss."
            ),
            "expected_output": (
                "A step table showing shifted decoder inputs and next-token targets, plus "
                "an explanation of teacher forcing, causal masking, and ignored padding labels."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "teacher-forcing",
                "seq2seq-training",
                "decoder-inputs",
                "loss-masking",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L05.QZ01",
        "title": "Summarization — Knowledge Check",
        "lesson_code": "M01.L05",
        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L05.Q01",
                "section_id": "summarization-problem",
                "question": "What best describes abstractive summarization?",
                "options": [
                    "Copying only the first sentence from a document.",
                    "Selecting only existing source spans without changing their wording.",
                    "Generating a shorter text that can express source ideas using new wording.",
                    "Predicting one category label for the whole document.",
                ],
                "correct": 2,
                "explanation": (
                    "Abstractive summarization generates a new sequence that expresses "
                    "important source information concisely rather than only copying spans."
                ),
            },
            {
                "id": "M01.L05.Q02",
                "section_id": "rouge",
                "question": (
                    "Why is ROUGE commonly used for summarization?"
                ),
                "options": [
                    "It measures only GPU memory usage.",
                    "It measures overlap with reference content and is designed around "
                    "coverage/recall-oriented comparison.",
                    "It guarantees factual correctness.",
                    "It can only evaluate classification labels.",
                ],
                "correct": 1,
                "explanation": (
                    "ROUGE compares generated and reference summaries using n-gram or "
                    "sequence overlap and is widely used for summarization evaluation."
                ),
            },
            {
                "id": "M01.L05.Q03",
                "section_id": "domain-shift",
                "question": (
                    "Why did a PEGASUS model tuned for CNN/DailyMail perform worse on SAMSum?"
                ),
                "options": [
                    "SAMSum contains no text.",
                    "The task changed from summarization to image classification.",
                    "The source and target distributions changed from news articles to "
                    "informal dialogues and dialogue-style summaries.",
                    "Encoder-decoder models cannot process dialogue.",
                ],
                "correct": 2,
                "explanation": (
                    "This is domain shift: although both datasets involve summarization, "
                    "their text style and desired summary behavior differ."
                ),
            },
            {
                "id": "M01.L05.Q04",
                "section_id": "gradient-accumulation",
                "question": (
                    "What is the main purpose of gradient accumulation in the chapter's "
                    "fine-tuning setup?"
                ),
                "options": [
                    "To remove the decoder from the model.",
                    "To approximate a larger effective batch while keeping each microbatch "
                    "small enough to fit in GPU memory.",
                    "To replace ROUGE with accuracy.",
                    "To increase the model's context window.",
                ],
                "correct": 1,
                "explanation": (
                    "Gradients from several small microbatches are accumulated before an "
                    "optimizer update, reducing peak memory while giving a larger effective batch."
                ),
            },
            {
                "id": "M01.L05.Q05",
                "section_id": "human-evaluation",
                "type": "open",
                "question": (
                    "You are evaluating a customer-support dialogue summarizer. Design a "
                    "small evaluation plan that combines an automatic metric, a baseline, "
                    "generation settings, and human review. Explain what each part protects "
                    "you from missing."
                ),
            },
        ],

        "passing_score": 70,
    },
}
