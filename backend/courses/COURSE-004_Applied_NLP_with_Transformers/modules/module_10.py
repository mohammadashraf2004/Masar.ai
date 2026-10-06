"""M01.L10 — Training Transformers from Scratch.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-004, Chapter 10.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L10"
MODULE_ORDER = 1
MODULE_TITLE = "Transformer Foundations"
MODULE_DESCRIPTION = (
    "Build a transformer language model from scratch by constructing a large corpus, "
    "training a domain-specific tokenizer, initializing a causal language model with "
    "fresh weights, and scaling training across multiple GPUs."
)

SOURCE_CHAPTER = 10
SOURCE_PAGES = "Chapter 10"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Training Transformers from Scratch",
    "slug": "applied-nlp-transformers-m01-l10-training-transformers-from-scratch",
    "description": (
        "Learn the full pretraining pipeline by building CodeParrot: create and stream a "
        "large Python corpus, train a byte-level BPE tokenizer, choose a causal-language-model "
        "objective, initialize GPT-style models from configuration, construct constant-length "
        "training sequences, distribute training with Accelerate, and evaluate generated code."
    ),
    "order": 10,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 2.5,
    "skill_tags": [
        "pretraining",
        "causal-language-modeling",
        "large-datasets",
        "streaming",
        "memory-mapping",
        "tokenizer-training",
        "byte-level-bpe",
        "distributed-training",
        "accelerate",
        "perplexity",
        "code-generation",
        "module-01",
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
        "M01.L09",
    ],

    "lesson": {
        "title": "Training Transformers from Scratch",

        "content": (
            "# Training Transformers from Scratch\n"
            "\n"
            "> **Course:** Applied NLP with Transformers  \n"
            "> **Lesson:** M01.L10  \n"
            "> **Module:** Transformer Foundations  \n"
            "> **Source alignment:** BOOK-004, Chapter 10. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Decide when training from scratch may be justified instead of fine-tuning.\n"
            "- Explain how pretraining-corpus quality affects model behavior.\n"
            "- Describe important legal, privacy, bias, duplication, and quality concerns in "
            "large automatically collected datasets.\n"
            "- Explain memory mapping and streaming for datasets larger than RAM or disk capacity.\n"
            "- Explain why a tokenizer trained on the wrong domain can waste context length.\n"
            "- Describe byte-level BPE and why it fits source code well.\n"
            "- Train a new tokenizer from an iterator over a representative corpus sample.\n"
            "- Compare causal LM, masked LM, and sequence-to-sequence pretraining objectives.\n"
            "- Initialize a GPT-style language model from configuration rather than pretrained weights.\n"
            "- Prepare constant-length causal-LM sequences efficiently.\n"
            "- Explain how Hugging Face Accelerate adapts a PyTorch loop for multi-GPU training.\n"
            "- Explain gradient accumulation, gradient checkpointing, and data parallelism.\n"
            "- Track validation loss and perplexity during pretraining.\n"
            "- Evaluate code-generation models qualitatively and with executable tests.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. When should you train from scratch?\n"
            "\n"
            "Most of this course has relied on **transfer learning** because labeled task data "
            "is usually limited. Starting from a pretrained transformer is normally much cheaper "
            "than creating one yourself.\n"
            "\n"
            "Chapter 10 explores the opposite situation: you have a very large domain corpus and "
            "want to build a language model specialized for it.\n"
            "\n"
            "The running project is **CodeParrot**, a GPT-like model trained to generate Python code.\n"
            "\n"
            "Training from scratch becomes more interesting when:\n"
            "\n"
            "- you have an enormous amount of domain data,\n"
            "- the domain is substantially different from the corpora used by available models,\n"
            "- an existing tokenizer represents your domain inefficiently,\n"
            "- you have enough compute to pretrain a model,\n"
            "- you need control over the pretraining corpus and tokenizer.\n"
            "\n"
            "A useful decision rule is:\n"
            "\n"
            "```text\n"
            "small/medium domain corpus\n"
            "        → adapt or fine-tune an existing model\n"
            "\n"
            "very large, distinct corpus + sufficient compute\n"
            "        → consider tokenizer + model pretraining from scratch\n"
            "```\n"
            "\n"
            '{{image:fine-tuning-vs-training-from-scratch}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 2. The model inherits the corpus\n"
            "\n"
            "A pretrained model learns patterns from whatever you place in its pretraining corpus.\n"
            "\n"
            "That includes useful patterns—but also defects.\n"
            "\n"
            "The chapter highlights problems discovered in large public corpora such as:\n"
            "\n"
            "- unwanted machine-translated material,\n"
            "- filtering choices that disproportionately remove some language varieties,\n"
            "- explicit-content filtering that can erase legitimate vocabulary,\n"
            "- copyright problems,\n"
            "- genre imbalance,\n"
            "- over- or underrepresentation of populations and topics.\n"
            "\n"
            "This means dataset design is part of model design.\n"
            "\n"
            "A model trained on a skewed corpus can reproduce that skew in its generations.\n"
            "\n"
            "The chapter illustrates this by comparing similarly sized GPT and GPT-2 models "
            "trained on different corpora and observing noticeably different styles in generated text.\n"
            "\n"
            "The key lesson is:\n"
            "\n"
            "> **Pretraining data influences what the model treats as normal language.**\n"
            "\n"
            "[[IMAGE_NEEDED: Corpus-to-model behavior pipeline | "
            "A large dataset containing useful patterns plus bias/noise/copyright/privacy risks "
            "feeding pretraining, followed by a model whose generated outputs reflect both the "
            "useful and undesirable corpus patterns | "
            "Learner should notice that corpus choices propagate into model behavior]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Build a large Python-code corpus\n"
            "\n"
            "To train CodeParrot, the chapter collects Python files from public GitHub repositories.\n"
            "\n"
            "The source uses Google BigQuery because GitHub's REST API is rate-limited and the "
            "pretraining task needs far more data than an ordinary API workflow can conveniently provide.\n"
            "\n"
            "The extraction process filters for things such as:\n"
            "\n"
            "- public/open-source repositories,\n"
            "- Python files,\n"
            "- nonbinary content,\n"
            "- files within a selected size range,\n"
            "- license metadata.\n"
            "\n"
            "The chapter reports processing roughly **2.6 TB** of source data to extract about "
            "**26.8 million files**, producing around **50 GB of compressed JSON**.\n"
            "\n"
            "That scale changes the engineering problem completely.\n"
            "\n"
            "### Do not treat 'public' as 'clean'\n"
            "\n"
            "Before training on source code, the chapter recommends considering:\n"
            "\n"
            "- duplicated files,\n"
            "- low-quality repositories,\n"
            "- licensing,\n"
            "- credentials, passwords, keys, or other personal information,\n"
            "- language balance,\n"
            "- comments/docstrings in natural language,\n"
            "- noisy or generated code.\n"
            "\n"
            "For the educational experiment, the chapter intentionally keeps preprocessing simpler, "
            "but it emphasizes that production corpus curation should be stricter.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Process datasets larger than RAM\n"
            "\n"
            "A 50 GB compressed dataset can expand to far more than typical workstation RAM.\n"
            "\n"
            "The chapter uses two dataset-loading techniques:\n"
            "\n"
            "### Memory mapping\n"
            "\n"
            "The dataset is stored in an efficient on-disk representation. Instead of loading "
            "everything into RAM, the process accesses the file through mapped memory.\n"
            "\n"
            "The chapter's example reports an on-disk cache of about **183.68 GB** while the "
            "Python process uses only a few GB of RAM.\n"
            "\n"
            "### Streaming\n"
            "\n"
            "If even the local disk cannot hold the processed corpus, examples can be read "
            "incrementally from compressed files or directly from a remote dataset.\n"
            "\n"
            "```python\n"
            "from datasets import load_dataset\n"
            "\n"
            "streamed_dataset = load_dataset(\n"
            "    'transformersbook/codeparrot',\n"
            "    split='train',\n"
            "    streaming=True,\n"
            ")\n"
            "```\n"
            "\n"
            "A streamed dataset behaves like an iterable rather than an ordinary random-access array.\n"
            "\n"
            "So this works naturally:\n"
            "\n"
            "```python\n"
            "example = next(iter(streamed_dataset))\n"
            "```\n"
            "\n"
            "but arbitrary indexing is not the main access pattern.\n"
            "\n"
            "[[IMAGE_NEEDED: Memory mapping versus streaming | "
            "Two side-by-side workflows: memory mapping shows a large local Arrow/cache file "
            "accessed through small memory windows, while streaming shows remote compressed "
            "files sending only the current batch to RAM | "
            "Learner should notice that both avoid loading the complete corpus into memory]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Why train a domain-specific tokenizer?\n"
            "\n"
            "A pretrained model and its tokenizer are a matched pair.\n"
            "\n"
            "If you use an existing model, you generally must use the tokenizer it was pretrained with.\n"
            "\n"
            "But when training a **new** model, an unrelated tokenizer can be wasteful.\n"
            "\n"
            "Examples from the chapter illustrate the problem:\n"
            "\n"
            "- a tokenizer trained on filtered web text may split ordinary words unexpectedly,\n"
            "- a tokenizer trained only on French may represent English inefficiently,\n"
            "- a natural-language tokenizer may handle Python indentation poorly.\n"
            "\n"
            "Inefficient tokenization matters because transformer context is measured in **tokens**, "
            "not characters.\n"
            "\n"
            "If one tokenizer needs twice as many tokens to represent the same code, you effectively "
            "lose half of the useful content that fits inside a fixed context window.\n"
            "\n"
            "### Tokenizer quality is not only vocabulary size\n"
            "\n"
            "The chapter suggests metrics such as:\n"
            "\n"
            "- **subword fertility** — average number of subtokens per original word,\n"
            "- **continued-word proportion** — fraction of words split into multiple pieces,\n"
            "- coverage/unknown-token measures,\n"
            "- robustness to noisy or misspelled inputs,\n"
            "- ultimately, downstream model performance.\n"
            "\n"
            "{{exercise:M01.L10.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Byte-level BPE is a good fit for code\n"
            "\n"
            "Python syntax depends on whitespace, especially indentation.\n"
            "\n"
            "A tokenizer that removes or normalizes whitespace aggressively could destroy useful "
            "structure.\n"
            "\n"
            "The chapter therefore starts from a GPT-2-style **byte-level BPE** tokenizer.\n"
            "\n"
            "### Why byte level?\n"
            "\n"
            "UTF-8 text can be represented using only 256 byte values as the basic alphabet.\n"
            "\n"
            "This guarantees that arbitrary Unicode input can be represented without requiring "
            "a gigantic character vocabulary.\n"
            "\n"
            "### Why BPE on top of bytes?\n"
            "\n"
            "Using individual bytes alone would make sequences extremely long.\n"
            "\n"
            "Byte-Pair Encoding learns frequent combinations and turns them into larger tokens.\n"
            "\n"
            "The result is a middle ground:\n"
            "\n"
            "```text\n"
            "tiny byte vocabulary\n"
            "      +\n"
            "learned frequent byte combinations\n"
            "      ↓\n"
            "compact vocabulary that can still represent any text\n"
            "```\n"
            "\n"
            "In GPT-2's tokenizer display, special visible characters can represent whitespace "
            "or newline bytes. This lets the tokenizer preserve code formatting.\n"
            "\n"
            "[[IMAGE_NEEDED: Byte-level BPE for Python code | "
            "A short indented Python function mapped first into byte-aware symbols for spaces "
            "and newlines, then frequent byte combinations merged into larger BPE tokens | "
            "Learner should notice that indentation and line breaks remain represented rather "
            "than being discarded]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Train the tokenizer on representative code\n"
            "\n"
            "A tokenizer does not need to see the entire 50 GB corpus to learn useful frequency "
            "statistics. It needs a sufficiently large and representative sample.\n"
            "\n"
            "The chapter retrains a GPT-2-style tokenizer from an iterator:\n"
            "\n"
            "```python\n"
            "dataset = load_dataset(\n"
            "    'transformersbook/codeparrot-train',\n"
            "    split='train',\n"
            "    streaming=True,\n"
            ")\n"
            "\n"
            "def batch_iterator(batch_size=10):\n"
            "    iterator = iter(dataset)\n"
            "    for _ in range(20000):\n"
            "        yield [next(iterator)['content'] for _ in range(batch_size)]\n"
            "\n"
            "code_tokenizer = gpt2_tokenizer.train_new_from_iterator(\n"
            "    batch_iterator(),\n"
            "    vocab_size=32768,\n"
            "    initial_alphabet=base_vocab,\n"
            ")\n"
            "```\n"
            "\n"
            "The code-trained vocabulary learns useful patterns such as:\n"
            "\n"
            "- indentation widths,\n"
            "- Python keywords,\n"
            "- common code fragments,\n"
            "- ordinary English words that appear frequently in comments/docstrings.\n"
            "\n"
            "The larger tokenizer studied in the chapter encodes the code corpus with roughly "
            "half as many tokens as the generic GPT-2 tokenizer in its comparison.\n"
            "\n"
            "That effectively increases usable context while also reducing compute per source character.\n"
            "\n"
            "[[IMAGE_NEEDED: Generic versus code-trained tokenizer | "
            "The same Python function tokenized by a generic GPT-2 tokenizer and by the custom "
            "CodeParrot tokenizer, with token counts shown below | "
            "Learner should notice that the domain tokenizer groups indentation and common code "
            "patterns more efficiently]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Choose the pretraining objective before the architecture\n"
            "\n"
            "The best architecture depends on what you want the model to learn.\n"
            "\n"
            "The chapter compares three objectives.\n"
            "\n"
            "### Causal language modeling (CLM)\n"
            "\n"
            "Predict the next token from previous tokens.\n"
            "\n"
            "```text\n"
            "def area(a, b):\n"
            "    return  → predict next token\n"
            "```\n"
            "\n"
            "This maps naturally to **code autocompletion**, so a GPT-style decoder-only model "
            "is a strong fit.\n"
            "\n"
            "### Masked language modeling (MLM)\n"
            "\n"
            "Mask or corrupt tokens and reconstruct the originals.\n"
            "\n"
            "This is well suited to learning general representations for later downstream tasks "
            "and corresponds to BERT-like encoder pretraining.\n"
            "\n"
            "### Sequence-to-sequence training\n"
            "\n"
            "Create paired inputs and outputs, such as:\n"
            "\n"
            "```text\n"
            "code → documentation\n"
            "documentation → code\n"
            "```\n"
            "\n"
            "This naturally matches encoder-decoder architectures such as T5 or BART.\n"
            "\n"
            "[[IMAGE_NEEDED: Three pretraining objectives for code | "
            "Three side-by-side mini diagrams: CLM predicts future code with a decoder, MLM "
            "reconstructs masked code with an encoder, and seq2seq maps code to comments or "
            "comments to code with an encoder-decoder | "
            "Learner should notice that task objective determines the appropriate architecture]]\n"
            "\n"
            "CodeParrot targets autocompletion, so the chapter chooses **causal language modeling**.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Initialize a model with fresh weights\n"
            "\n"
            "This is where training from scratch differs most clearly from fine-tuning.\n"
            "\n"
            "Instead of:\n"
            "\n"
            "```python\n"
            "AutoModelForCausalLM.from_pretrained(...)\n"
            "```\n"
            "\n"
            "we load a model **configuration** and initialize new random weights:\n"
            "\n"
            "```python\n"
            "from transformers import AutoConfig, AutoModelForCausalLM\n"
            "\n"
            "config = AutoConfig.from_pretrained(\n"
            "    'gpt2',\n"
            "    vocab_size=len(code_tokenizer),\n"
            ")\n"
            "\n"
            "model = AutoModelForCausalLM.from_config(config)\n"
            "```\n"
            "\n"
            "The chapter constructs two GPT-style sizes:\n"
            "\n"
            "| Variant | Approximate parameter count |\n"
            "|---|---:|\n"
            "| Small CodeParrot | 111 million |\n"
            "| Large CodeParrot | 1.53 billion |\n"
            "\n"
            "The model architecture may reuse GPT-2 hyperparameters, but the **weights are not "
            "pretrained GPT-2 weights**.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Feed the model full constant-length sequences\n"
            "\n"
            "GPU training is most efficient when batches have uniform shapes.\n"
            "\n"
            "But source files have very different lengths.\n"
            "\n"
            "The chapter solves this by:\n"
            "\n"
            "1. reading several source files,\n"
            "2. tokenizing them,\n"
            "3. inserting an end-of-sequence token between files,\n"
            "4. concatenating everything into one long token stream,\n"
            "5. splitting that stream into fixed-size chunks such as 1,024 tokens.\n"
            "\n"
            "```text\n"
            "file A tokens + EOS + file B tokens + EOS + file C tokens\n"
            "                         ↓\n"
            "very long token stream\n"
            "                         ↓\n"
            "[1024] [1024] [1024] [1024] ...\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Constant-length CLM preprocessing | "
            "Several code files of different lengths are tokenized and concatenated with EOS "
            "markers, then sliced into equal 1024-token chunks | "
            "Learner should notice that file boundaries are preserved with EOS tokens while "
            "training sequences stay fully packed]]\n"
            "\n"
            "This avoids large amounts of padding and keeps the training computation focused "
            "on real tokens.\n"
            "\n"
            "The chapter estimates the average characters-per-token ratio to decide how much "
            "raw text should be buffered before tokenizing and chunking.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Scale a PyTorch training loop with Accelerate\n"
            "\n"
            "The chapter uses Hugging Face Accelerate because training a large language model "
            "requires more control than the earlier high-level examples.\n"
            "\n"
            "The important changes to an ordinary PyTorch loop are small.\n"
            "\n"
            "```python\n"
            "from accelerate import Accelerator\n"
            "\n"
            "accelerator = Accelerator()\n"
            "\n"
            "model, optimizer, dataloader = accelerator.prepare(\n"
            "    model,\n"
            "    optimizer,\n"
            "    dataloader,\n"
            ")\n"
            "\n"
            "for batch in dataloader:\n"
            "    loss = model(batch, labels=batch).loss\n"
            "    accelerator.backward(loss)\n"
            "    optimizer.step()\n"
            "    optimizer.zero_grad()\n"
            "```\n"
            "\n"
            "Accelerate handles many infrastructure-specific details so the same training code "
            "can run on different distributed setups.\n"
            "\n"
            "The chapter also uses mixed precision in its large training configuration.\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Build the complete pretraining loop\n"
            "\n"
            "The chapter's custom loop includes more than just forward and backward passes.\n"
            "\n"
            "It brings together:\n"
            "\n"
            "- streamed train/validation datasets,\n"
            "- constant-length dataloaders,\n"
            "- AdamW optimizer,\n"
            "- cosine learning-rate schedule,\n"
            "- warmup steps,\n"
            "- weight decay,\n"
            "- gradient accumulation,\n"
            "- validation loss and perplexity,\n"
            "- checkpoint saving,\n"
            "- TensorBoard / Weights & Biases logging,\n"
            "- Hub versioning.\n"
            "\n"
            "A simplified core is:\n"
            "\n"
            "```python\n"
            "model.train()\n"
            "\n"
            "for step, batch in enumerate(train_dataloader, start=1):\n"
            "    loss = model(batch, labels=batch).loss\n"
            "    loss = loss / gradient_accumulation_steps\n"
            "\n"
            "    accelerator.backward(loss)\n"
            "\n"
            "    if step % gradient_accumulation_steps == 0:\n"
            "        optimizer.step()\n"
            "        lr_scheduler.step()\n"
            "        optimizer.zero_grad()\n"
            "```\n"
            "\n"
            "Training code for a large model is therefore not just the neural network. "
            "The surrounding infrastructure is part of the experiment.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Fit large training jobs into limited GPU memory\n"
            "\n"
            "The chapter uses two related memory techniques.\n"
            "\n"
            "### Gradient accumulation\n"
            "\n"
            "If a desired batch is too large to fit at once, process several microbatches and "
            "delay the optimizer update.\n"
            "\n"
            "```text\n"
            "microbatch 1 ┐\n"
            "microbatch 2 │ accumulate gradients\n"
            "...          │\n"
            "microbatch N ┘\n"
            "       ↓\n"
            "optimizer step\n"
            "```\n"
            "\n"
            "### Gradient checkpointing\n"
            "\n"
            "Normally, training stores many intermediate activations from the forward pass so "
            "they are available during backpropagation.\n"
            "\n"
            "Gradient checkpointing stores fewer activations and recomputes some of them later.\n"
            "\n"
            "Trade-off:\n"
            "\n"
            "```text\n"
            "less GPU memory\n"
            "      ↕\n"
            "more computation / slower training\n"
            "```\n"
            "\n"
            "The chapter reports roughly a 20% slowdown for the memory saving in its setup.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Data Distributed Parallelism (DDP)\n"
            "\n"
            "Accelerate uses data parallelism for the chapter's multi-GPU training run.\n"
            "\n"
            "Each GPU keeps its own model copy.\n"
            "\n"
            "The process is:\n"
            "\n"
            "1. each worker/GPU receives a different batch,\n"
            "2. each model copy runs forward and backward passes,\n"
            "3. gradients are averaged across workers,\n"
            "4. each worker applies the same averaged update,\n"
            "5. training continues with new batches.\n"
            "\n"
            "[[IMAGE_NEEDED: Four-GPU data parallel training | "
            "A main data stream splits into four batches sent to four GPUs, each GPU contains "
            "the same model, local gradients flow into an averaging/reduce operation, and the "
            "averaged gradient is sent back to all four model copies | "
            "Learner should notice that data is divided while each GPU maintains a synchronized "
            "copy of the model]]\n"
            "\n"
            "DDP increases throughput and effective batch size, but it assumes the model itself "
            "can fit on one worker. If the model is too large for a single GPU, more advanced "
            "model-parallel strategies are required.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Track validation loss and perplexity\n"
            "\n"
            "During causal-LM pretraining, the chapter monitors validation loss and **perplexity**.\n"
            "\n"
            "Perplexity can be computed from cross-entropy loss:\n"
            "\n"
            "```text\n"
            "perplexity = exp(loss)\n"
            "```\n"
            "\n"
            "Lower perplexity means the model assigns higher probability to the correct next tokens.\n"
            "\n"
            "A simplified evaluation loop is:\n"
            "\n"
            "```python\n"
            "model.eval()\n"
            "losses = []\n"
            "\n"
            "for batch in eval_dataloader:\n"
            "    with torch.no_grad():\n"
            "        output = model(batch, labels=batch)\n"
            "    losses.append(output.loss)\n"
            "\n"
            "eval_loss = torch.stack(losses).mean()\n"
            "perplexity = torch.exp(eval_loss)\n"
            "```\n"
            "\n"
            "The chapter evaluates whenever a checkpoint is saved and once more at the end.\n"
            "\n"
            "[[IMAGE_NEEDED: Training loss and perplexity curves | "
            "Two conceptual curves over processed tokens showing training loss and validation "
            "perplexity decreasing, with separate small-model and large-model curves | "
            "Learner should notice that the larger model improves faster with respect to tokens "
            "processed even though the wall-clock training run is longer]]\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Launch the actual multi-GPU run\n"
            "\n"
            "The training script is launched with Accelerate rather than from a notebook cell.\n"
            "\n"
            "The source workflow is approximately:\n"
            "\n"
            "```text\n"
            "clone model repository\n"
            "install dependencies\n"
            "authenticate experiment logging\n"
            "configure Accelerate\n"
            "launch training script\n"
            "```\n"
            "\n"
            "The chapter's experiment uses:\n"
            "\n"
            "| Setting | Value |\n"
            "|---|---|\n"
            "| Environment | Multi-GPU |\n"
            "| Machines | 1 |\n"
            "| Processes | 16 |\n"
            "| FP16 | Yes |\n"
            "| GPUs | 16 A100 GPUs, 40 GB each |\n"
            "\n"
            "The reported training times are roughly:\n"
            "\n"
            "- **24 hours** for the smaller model,\n"
            "- **7 days** for the larger model.\n"
            "\n"
            "This motivates an essential production/research habit:\n"
            "\n"
            "> **Debug the entire pipeline on a small model and cheap infrastructure before "
            "starting the expensive full-scale run.**\n"
            "\n"
            "{{exercise:M01.L10.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Inspect code generations qualitatively\n"
            "\n"
            "After training, the chapter uses a text-generation pipeline to inspect code completions.\n"
            "\n"
            "Examples include prompts asking the model to:\n"
            "\n"
            "- calculate the area of a rectangle,\n"
            "- extract URLs from HTML,\n"
            "- translate a simple Python implementation into NumPy,\n"
            "- construct a Scikit-learn random forest.\n"
            "\n"
            "The generated candidates are not always correct, which is exactly why qualitative "
            "inspection matters.\n"
            "\n"
            "The model can produce several completions for the same prompt by sampling:\n"
            "\n"
            "```python\n"
            "generation = pipeline(\n"
            "    'text-generation',\n"
            "    model='transformersbook/codeparrot-small',\n"
            ")\n"
            "\n"
            "outputs = generation(\n"
            "    prompt,\n"
            "    do_sample=True,\n"
            "    temperature=0.4,\n"
            "    top_p=0.95,\n"
            "    num_return_sequences=4,\n"
            ")\n"
            "```\n"
            "\n"
            "This connects directly to the decoding methods learned earlier in the course.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Evaluate code by executing it, not only comparing text\n"
            "\n"
            "A text-overlap metric such as BLEU is a poor fit for code generation.\n"
            "\n"
            "Why?\n"
            "\n"
            "Two programs can be functionally equivalent while using different:\n"
            "\n"
            "- variable names,\n"
            "- helper functions,\n"
            "- formatting,\n"
            "- control structures.\n"
            "\n"
            "A lexical metric may punish those harmless differences.\n"
            "\n"
            "Code has a stronger evaluation tool: **unit tests**.\n"
            "\n"
            "```text\n"
            "prompt\n"
            "  ↓\n"
            "generate several candidate programs\n"
            "  ↓\n"
            "run hidden unit tests\n"
            "  ↓\n"
            "count how many candidates behave correctly\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Functional evaluation for generated code | "
            "A programming prompt branches into several generated code candidates; each candidate "
            "runs through the same unit-test suite, producing pass/fail results; the final metric "
            "is based on functional success rather than text overlap | "
            "Learner should notice that semantic correctness of code is best checked by execution]]\n"
            "\n"
            "The chapter points to this executable-evaluation style as a much better systematic "
            "measure for code models than n-gram overlap.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. The complete from-scratch training pipeline\n"
            "\n"
            "Put the chapter together as one engineering workflow:\n"
            "\n"
            "```text\n"
            "1. Define the domain and downstream objective\n"
            "              ↓\n"
            "2. Gather a very large corpus\n"
            "              ↓\n"
            "3. Audit quality, licensing, duplication, bias, privacy\n"
            "              ↓\n"
            "4. Stream / memory-map the corpus\n"
            "              ↓\n"
            "5. Train a domain-specific tokenizer\n"
            "              ↓\n"
            "6. Evaluate tokenizer efficiency\n"
            "              ↓\n"
            "7. Choose the pretraining objective\n"
            "              ↓\n"
            "8. Initialize model from configuration\n"
            "              ↓\n"
            "9. Build fully packed constant-length batches\n"
            "              ↓\n"
            "10. Debug on a small model\n"
            "              ↓\n"
            "11. Scale with Accelerate / distributed training\n"
            "              ↓\n"
            "12. Track loss, perplexity, checkpoints\n"
            "              ↓\n"
            "13. Inspect generations\n"
            "              ↓\n"
            "14. Evaluate the real downstream behavior\n"
            "```\n"
            "\n"
            "Training the neural network is only one stage. Corpus engineering, tokenization, "
            "data loading, distributed systems, monitoring, and evaluation are equally important.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Training from scratch is just fine-tuning for more epochs\n"
            "\n"
            "> Load a pretrained checkpoint and run a lot of training.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "From-scratch pretraining initializes fresh model weights and may use a newly trained "
            "tokenizer. Fine-tuning begins from pretrained weights.\n"
            "\n"
            "### Misconception 2: More pretraining data is automatically better\n"
            "\n"
            "> If the corpus is huge, quality no longer matters.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The model learns corpus defects too. Noise, bias, duplication, licensing problems, "
            "and sensitive information all become part of the pretraining risk.\n"
            "\n"
            "### Misconception 3: Any tokenizer is good enough\n"
            "\n"
            "> Tokenization only changes preprocessing, not model efficiency.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "An inefficient tokenizer consumes more context tokens and increases transformer "
            "computation. A domain-specific tokenizer can represent the same source more compactly.\n"
            "\n"
            "### Misconception 4: Multi-GPU training means splitting one model into pieces\n"
            "\n"
            "> Every GPU stores a different portion of the network in ordinary DDP.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "In data parallelism, each worker keeps a model copy and processes different data. "
            "Gradients are synchronized across workers.\n"
            "\n"
            "### Misconception 5: Low perplexity proves the code is correct\n"
            "\n"
            "> If the language model predicts tokens well, every generated program must work.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Perplexity evaluates token prediction. Functional code quality requires execution-based "
            "tests or other downstream evaluation.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Pretraining from scratch | Training fresh model weights on a large corpus before downstream adaptation |\n"
            "| Pretraining corpus | Large dataset used to learn general/domain representations |\n"
            "| Memory mapping | Accessing large on-disk data through mapped memory instead of fully loading RAM |\n"
            "| Streaming | Reading examples incrementally without materializing the full dataset locally |\n"
            "| Byte-level tokenizer | Tokenizer whose base alphabet represents byte values |\n"
            "| BPE | Byte-Pair Encoding; builds larger tokens by repeatedly merging frequent token pairs |\n"
            "| Subword fertility | Average number of subtokens used to encode a word |\n"
            "| Causal language modeling | Predicting future/next tokens from previous context |\n"
            "| Masked language modeling | Reconstructing intentionally masked or corrupted tokens |\n"
            "| Sequence-to-sequence | Mapping an input sequence to a separate output sequence |\n"
            "| Fresh initialization | Creating model weights from configuration instead of loading a checkpoint |\n"
            "| EOS | End-of-sequence marker used to separate documents/examples |\n"
            "| Constant-length dataset | Dataset yielding fixed-size fully packed token sequences |\n"
            "| Accelerate | Library that simplifies mixed-precision and distributed training setup |\n"
            "| Gradient accumulation | Combining gradients across microbatches before an optimizer update |\n"
            "| Gradient checkpointing | Trading recomputation time for lower activation memory use |\n"
            "| DDP | Distributed Data Parallelism with synchronized model replicas across workers |\n"
            "| Perplexity | Exponentiated language-model cross-entropy loss; lower is better |\n"
            "| Functional evaluation | Measuring generated code by executing tests rather than only comparing text |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. When would training from scratch be more reasonable than ordinary fine-tuning?\n"
            "2. Why can corpus bias affect model generations?\n"
            "3. What is the difference between memory mapping and streaming?\n"
            "4. Why does tokenizer efficiency affect effective context length?\n"
            "5. Why is byte-level BPE useful for Python code?\n"
            "6. How does causal LM differ from masked LM and seq2seq training?\n"
            "7. What does `from_config()` mean compared with `from_pretrained()`?\n"
            "8. Why concatenate documents with EOS markers before chunking?\n"
            "9. What does Accelerate's `prepare()` step do conceptually?\n"
            "10. How do gradient accumulation and gradient checkpointing solve different problems?\n"
            "11. What gets synchronized in DDP?\n"
            "12. Why is unit-test evaluation stronger than BLEU for code generation?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Training a transformer from scratch is a complete systems project: the corpus "
            "determines what the model can learn, the tokenizer determines how efficiently that "
            "corpus is represented, the objective determines the architecture, and scalable data "
            "loading plus distributed training determine whether pretraining is computationally "
            "possible. Model quality must finally be judged on the real downstream behavior—not "
            "only on pretraining loss.**\n"
        ),

        "estimated_minutes": 150,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-from-scratch", "title": "When should you train from scratch?", "order": 1},
            {"id": "corpus-quality", "title": "The model inherits the corpus", "order": 2},
            {"id": "code-corpus", "title": "Build a large Python-code corpus", "order": 3},
            {"id": "large-datasets", "title": "Process datasets larger than RAM", "order": 4},
            {"id": "tokenizer-domain", "title": "Why train a domain-specific tokenizer?", "order": 5},
            {"id": "byte-bpe", "title": "Byte-level BPE for source code", "order": 6},
            {"id": "train-tokenizer", "title": "Train the tokenizer", "order": 7},
            {"id": "pretraining-objectives", "title": "Choose the pretraining objective", "order": 8},
            {"id": "initialize-model", "title": "Initialize fresh model weights", "order": 9},
            {"id": "constant-length", "title": "Build constant-length CLM sequences", "order": 10},
            {"id": "accelerate", "title": "Scale training with Accelerate", "order": 11},
            {"id": "training-loop", "title": "Build the complete training loop", "order": 12},
            {"id": "memory-techniques", "title": "Gradient accumulation and checkpointing", "order": 13},
            {"id": "ddp", "title": "Distributed Data Parallelism", "order": 14},
            {"id": "evaluation", "title": "Track validation loss and perplexity", "order": 15},
            {"id": "training-run", "title": "Launch the multi-GPU run", "order": 16},
            {"id": "qualitative-eval", "title": "Inspect code generations", "order": 17},
            {"id": "code-evaluation", "title": "Evaluate generated code functionally", "order": 18},
            {"id": "full-pipeline", "title": "Complete from-scratch pipeline", "order": 19},
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L10.EX01",
            "title": "Compare Tokenizer Efficiency",
            "lesson_code": "M01.L10",
            "section_id": "tokenizer-domain",
            "placement": "after_section",
            "description": (
                "Practice reasoning about why tokenizer choice affects transformer context "
                "and compute in a domain such as Python code."
            ),
            "instructions": (
                "Suppose a generic tokenizer encodes a Python file into 1,800 tokens while "
                "your code-specific tokenizer encodes the same file into 950 tokens.\n"
                "1. Which tokenizer fits more source code into a 1,024-token model context?\n"
                "2. Explain why fewer tokens can reduce self-attention computation.\n"
                "3. Identify two Python-specific structures your tokenizer should preserve.\n"
                "4. Name two tokenizer metrics from the lesson you could inspect.\n"
                "5. Explain why downstream model performance should still be the final test."
            ),
            "expected_output": (
                "A short comparison showing that the code tokenizer nearly fits the whole file "
                "inside one context, plus reasoning about sequence length, indentation/newlines, "
                "subword fertility/continued-word rate, and downstream validation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "tokenizer-training",
                "context-efficiency",
                "byte-level-bpe",
                "evaluation",
            ],
        },

        {
            "id": "M01.L10.EX02",
            "title": "Design a Safe Small-to-Large Training Run",
            "lesson_code": "M01.L10",
            "section_id": "training-run",
            "placement": "after_section",
            "description": (
                "Practice designing a staged pretraining workflow before spending large "
                "amounts of compute."
            ),
            "instructions": (
                "You want to train a 1.5B-parameter code model on a multi-GPU cluster.\n"
                "1. Describe a small-model dry run you would complete first.\n"
                "2. List the dataset, tokenizer, dataloader, optimizer, logging, and checkpoint "
                "behaviors that must be verified.\n"
                "3. Explain when you would use gradient accumulation.\n"
                "4. Explain when you would use gradient checkpointing.\n"
                "5. State what metrics you would monitor during pretraining.\n"
                "6. Describe one functional downstream evaluation after training."
            ),
            "expected_output": (
                "A staged launch checklist that validates the entire pipeline on a smaller "
                "model before scaling, monitors loss/perplexity, and evaluates generated code "
                "with executable tests."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "distributed-training",
                "gradient-accumulation",
                "gradient-checkpointing",
                "pretraining-evaluation",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L10.QZ01",
        "title": "Training Transformers from Scratch — Knowledge Check",
        "lesson_code": "M01.L10",
        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L10.Q01",
                "section_id": "why-from-scratch",
                "question": (
                    "Which situation most strongly supports considering transformer pretraining "
                    "from scratch?"
                ),
                "options": [
                    "You have 200 labeled examples and a strong pretrained model already matches the domain.",
                    "You have a massive specialized corpus, a poor fit with available pretrained "
                    "tokenizers/models, and sufficient compute.",
                    "You need to change only the classification threshold.",
                    "You want faster inference without changing training data.",
                ],
                "correct": 1,
                "explanation": (
                    "From-scratch pretraining becomes most reasonable when the corpus is large, "
                    "the domain differs meaningfully from existing pretrained models, and the "
                    "required computational resources are available."
                ),
            },

            {
                "id": "M01.L10.Q02",
                "section_id": "large-datasets",
                "question": (
                    "What is the main advantage of dataset streaming?"
                ),
                "options": [
                    "It requires the complete dataset to fit in RAM.",
                    "It allows examples to be read incrementally without materializing the "
                    "entire dataset locally.",
                    "It automatically labels every example.",
                    "It removes the need for a tokenizer.",
                ],
                "correct": 1,
                "explanation": (
                    "Streaming reads examples on demand, which makes very large or remote "
                    "datasets usable without storing or loading everything at once."
                ),
            },

            {
                "id": "M01.L10.Q03",
                "section_id": "pretraining-objectives",
                "question": (
                    "Why does the chapter choose causal language modeling for CodeParrot?"
                ),
                "options": [
                    "Because its target application is next-token code autocompletion.",
                    "Because causal language modeling requires labeled class IDs.",
                    "Because it can only be used with encoder-decoder models.",
                    "Because masked language modeling cannot process code tokens.",
                ],
                "correct": 0,
                "explanation": (
                    "Code autocompletion naturally matches a next-token prediction objective, "
                    "making a GPT-style causal decoder an appropriate architecture."
                ),
            },

            {
                "id": "M01.L10.Q04",
                "section_id": "ddp",
                "question": (
                    "What happens in ordinary distributed data parallel training?"
                ),
                "options": [
                    "Each GPU stores a different quarter of the model and never communicates.",
                    "Each GPU keeps a model replica, processes different data, and synchronizes "
                    "gradients with the other workers.",
                    "Only one GPU performs backward propagation while the rest stay idle.",
                    "Every worker trains a completely independent model with no synchronization.",
                ],
                "correct": 1,
                "explanation": (
                    "DDP replicates the model across workers, divides data among them, and "
                    "averages/synchronizes gradients so all replicas receive equivalent updates."
                ),
            },

            {
                "id": "M01.L10.Q05",
                "section_id": "code-evaluation",
                "type": "open",
                "question": (
                    "You trained a code-completion transformer from scratch. Design an evaluation "
                    "plan containing one language-model metric, one qualitative analysis, and one "
                    "functional code metric. Explain why no single one of the three is sufficient."
                ),
            },
        ],

        "passing_score": 70,
    },
}
