"""M01.L04 — Text Generation.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-004, Chapter 5.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L04"
MODULE_ORDER = 5
MODULE_TITLE = "Controlled Text Generation & Decoding"
MODULE_DESCRIPTION = (
    "Understand how causal language models generate text token by token and how "
    "decoding strategies control coherence, repetition, diversity, and compute."
)

SOURCE_CHAPTER = 5
SOURCE_PAGES = "Chapter 5"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Text Generation",
    "slug": "applied-nlp-transformers-m01-l04-text-generation",
    "description": (
        "Learn how autoregressive transformer models generate text and compare "
        "greedy search, beam search, temperature sampling, top-k sampling, and "
        "nucleus sampling."
    ),
    "order": 4,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 1.75,
    "skill_tags": [
        "text-generation",
        "causal-language-modeling",
        "gpt",
        "decoding",
        "greedy-search",
        "beam-search",
        "temperature",
        "top-k",
        "top-p",
        "sampling",
        "module-01",
    ],
    "prerequisite_ids": ["M01.L01", "M01.L02", "M01.L03"],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Text Generation",

        "content": (
            "# Text Generation\n"
            "\n"
            "> **Course:** Applied NLP with Transformers  \n"
            "> **Lesson:** M01.L04  \n"
            "> **Module:** Transformer Foundations  \n"
            "> **Source alignment:** BOOK-004, Chapter 5. This lesson is an "
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
            "- Explain how a causal language model generates text one token at a time.\n"
            "- Distinguish model prediction from the decoding strategy used to choose tokens.\n"
            "- Implement the basic logic of greedy decoding.\n"
            "- Explain why greedy search can produce repetitive or locally optimal text.\n"
            "- Explain beam search and why sequence log probabilities are useful.\n"
            "- Use an n-gram repetition constraint to reduce repeated phrases.\n"
            "- Explain how temperature changes a next-token probability distribution.\n"
            "- Compare top-k and nucleus/top-p sampling.\n"
            "- Choose a reasonable decoding family for deterministic versus creative tasks.\n"
            "- Explain why text generation is more computationally expensive than one-pass "
            "classification.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. What does a language model actually generate?\n"
            "\n"
            "A language model does not write a whole paragraph in one operation.\n"
            "\n"
            "At each generation step, it receives the text produced so far and predicts "
            "a probability distribution over the possible **next tokens**.\n"
            "\n"
            "Suppose the prompt is:\n"
            "\n"
            "```text\n"
            "Transformers are the\n"
            "```\n"
            "\n"
            "The model might assign probabilities such as:\n"
            "\n"
            "```text\n"
            "most       0.085\n"
            "only       0.050\n"
            "best       0.047\n"
            "ultimate   0.022\n"
            "...\n"
            "```\n"
            "\n"
            "A **decoding strategy** decides which candidate token to choose.\n"
            "\n"
            "After a token is selected, it is appended to the prompt:\n"
            "\n"
            "```text\n"
            "Transformers are the most\n"
            "```\n"
            "\n"
            "The updated sequence is sent through the model again, a new next-token "
            "distribution is produced, another token is chosen, and the process repeats.\n"
            "\n"
            "Generation stops when the model produces an end-of-sequence token or when "
            "a configured length limit is reached.\n"
            "\n"
            '{{image:autoregressive-generation-loop}}'
            '\n'
            "\n"
            "### The first key distinction\n"
            "\n"
            "The language model produces **scores/probabilities**. The decoding algorithm "
            "decides how those probabilities are turned into an actual text sequence.\n"
            "\n"
            "That is why the same model and prompt can produce very different text when "
            "we change the decoding settings.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Causal language modeling\n"
            "\n"
            "GPT-style models are **autoregressive**, also called **causal language models**.\n"
            "\n"
            "Their training objective is simple to state:\n"
            "\n"
            "> Given all previous tokens, predict the next token.\n"
            "\n"
            "For a sequence:\n"
            "\n"
            "```text\n"
            "x1, x2, x3, ..., xn\n"
            "```\n"
            "\n"
            "the probability of the complete sequence can be decomposed into conditional "
            "next-token probabilities:\n"
            "\n"
            "```text\n"
            "P(sequence)\n"
            "=\n"
            "P(x1) × P(x2 | x1) × P(x3 | x1,x2) × ... × P(xn | x1,...,x(n-1))\n"
            "```\n"
            "\n"
            "You do not need to memorize the equation. Remember the idea:\n"
            "\n"
            "**a long sequence is built from many next-token decisions.**\n"
            "\n"
            "This differs from masked-language modeling such as BERT's training objective. "
            "A causal model predicts from past context, whereas a masked encoder can use "
            "context on both sides of a masked position.\n"
            "\n"
            "### Conditional text generation\n"
            "\n"
            "Generated text depends strongly on the initial prompt. We therefore often call "
            "this **conditional generation**: the continuation is conditioned on the text "
            "already provided.\n"
            "\n"
            "{{exercise:M01.L04.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Greedy search: always choose the current winner\n"
            "\n"
            "The simplest decoder is **greedy search**.\n"
            "\n"
            "At each step:\n"
            "\n"
            "1. compute the next-token probabilities,\n"
            "2. select the token with the highest probability,\n"
            "3. append it to the sequence,\n"
            "4. repeat.\n"
            "\n"
            "### Simplified implementation\n"
            "\n"
            "```python\n"
            "import torch\n"
            "from transformers import AutoModelForCausalLM, AutoTokenizer\n"
            "\n"
            "device = 'cuda' if torch.cuda.is_available() else 'cpu'\n"
            "model_name = 'gpt2'\n"
            "\n"
            "tokenizer = AutoTokenizer.from_pretrained(model_name)\n"
            "model = AutoModelForCausalLM.from_pretrained(model_name).to(device)\n"
            "\n"
            "prompt = 'Transformers are the'\n"
            "input_ids = tokenizer(prompt, return_tensors='pt').input_ids.to(device)\n"
            "\n"
            "with torch.no_grad():\n"
            "    for _ in range(8):\n"
            "        outputs = model(input_ids=input_ids)\n"
            "\n"
            "        # Distribution for the next token only\n"
            "        next_token_logits = outputs.logits[:, -1, :]\n"
            "        next_token_id = torch.argmax(next_token_logits, dim=-1)\n"
            "\n"
            "        input_ids = torch.cat(\n"
            "            [input_ids, next_token_id.unsqueeze(-1)],\n"
            "            dim=-1,\n"
            "        )\n"
            "\n"
            "print(tokenizer.decode(input_ids[0]))\n"
            "```\n"
            "\n"
            "The built-in generation API performs the same type of deterministic decoding "
            "when sampling is disabled:\n"
            "\n"
            "```python\n"
            "output = model.generate(\n"
            "    input_ids,\n"
            "    max_new_tokens=8,\n"
            "    do_sample=False,\n"
            ")\n"
            "```\n"
            "\n"
            "### Why greedy search is attractive\n"
            "\n"
            "- simple,\n"
            "- deterministic,\n"
            "- relatively inexpensive,\n"
            "- always chooses the locally most probable next token.\n"
            "\n"
            "### Why greedy search can fail\n"
            "\n"
            "The locally best token is not guaranteed to lead to the best complete sequence.\n"
            "\n"
            "Imagine two paths:\n"
            "\n"
            "```text\n"
            "Step 1\n"
            "A = 0.60\n"
            "B = 0.40\n"
            "\n"
            "Step 2\n"
            "after A: best continuation = 0.20\n"
            "after B: best continuation = 0.90\n"
            "```\n"
            "\n"
            "Greedy search chooses A immediately because `0.60 > 0.40`. But the strongest "
            "two-step B path has probability:\n"
            "\n"
            "```text\n"
            "0.40 × 0.90 = 0.36\n"
            "```\n"
            "\n"
            "while the A path gives:\n"
            "\n"
            "```text\n"
            "0.60 × 0.20 = 0.12\n"
            "```\n"
            "\n"
            "Greedy search cannot go back and reconsider the earlier decision.\n"
            "\n"
            "For longer free-form text, another common problem is **repetition**.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Beam search: keep several promising paths alive\n"
            "\n"
            "Beam search tries to avoid committing to only one token path too early.\n"
            "\n"
            "If the number of beams is `b`, the decoder keeps the `b` most promising "
            "partial sequences at each step.\n"
            "\n"
            "For example, with two beams:\n"
            "\n"
            "```text\n"
            "Prompt\n"
            " ├── candidate A\n"
            " └── candidate B\n"
            "\n"
            "Next step:\n"
            " A ── A1, A2, ...\n"
            " B ── B1, B2, ...\n"
            "\n"
            "Keep the best two extended sequences.\n"
            "Repeat.\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Beam search with two beams | "
            "A small search tree showing a prompt expanding into candidate tokens, then "
            "multiple second-step candidates, with only the two highest-scoring partial "
            "sequences retained after each step | "
            "Learner should notice that beam search explores several paths rather than "
            "committing to one greedy continuation immediately]]\n"
            "\n"
            "Using the generation API:\n"
            "\n"
            "```python\n"
            "output_beam = model.generate(\n"
            "    input_ids,\n"
            "    max_new_tokens=80,\n"
            "    num_beams=5,\n"
            "    do_sample=False,\n"
            ")\n"
            "```\n"
            "\n"
            "Increasing the number of beams can explore more alternatives, but it also "
            "increases generation cost because several partial sequences must be maintained.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 5
            # ----------------------------------------------------------------

            "## 5. Why beam search uses log probabilities\n"
            "\n"
            "To score a complete generated sequence, we could multiply all of its "
            "conditional token probabilities.\n"
            "\n"
            "But multiplying many probabilities causes a numerical problem: each probability "
            "is between 0 and 1, so the product can become unimaginably small.\n"
            "\n"
            "For example:\n"
            "\n"
            "```python\n"
            "0.5 ** 1024\n"
            "```\n"
            "\n"
            "produces a value extremely close to zero.\n"
            "\n"
            "Instead, we use **log probabilities**.\n"
            "\n"
            "The useful identity is:\n"
            "\n"
            "```text\n"
            "log(a × b × c) = log(a) + log(b) + log(c)\n"
            "```\n"
            "\n"
            "So instead of multiplying hundreds of tiny values, we sum their logarithms.\n"
            "\n"
            "A simplified helper is:\n"
            "\n"
            "```python\n"
            "import torch.nn.functional as F\n"
            "\n"
            "def log_probs_from_logits(logits, labels):\n"
            "    logp = F.log_softmax(logits, dim=-1)\n"
            "    return torch.gather(\n"
            "        logp,\n"
            "        2,\n"
            "        labels.unsqueeze(2),\n"
            "    ).squeeze(-1)\n"
            "```\n"
            "\n"
            "### Higher log probability means more probable\n"
            "\n"
            "Log probabilities are usually negative. A value such as `-55` is therefore "
            "higher than `-87` and represents a more probable sequence under the model.\n"
            "\n"
            "But an important warning follows:\n"
            "\n"
            "**the sequence with the better model probability is not automatically the "
            "sequence humans will prefer.**\n"
            "\n"
            "The chapter's beam-search example receives a better log probability than its "
            "greedy output, yet can still contain undesirable repetition.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 6
            # ----------------------------------------------------------------

            "## 6. Controlling repetition with an n-gram constraint\n"
            "\n"
            "Greedy and beam decoding can fall into repetitive patterns.\n"
            "\n"
            "One simple control is `no_repeat_ngram_size`.\n"
            "\n"
            "An **n-gram** is a sequence of `n` tokens. If `n=2`, we are tracking token "
            "pairs. The decoder can block candidate tokens that would recreate an already "
            "generated 2-gram.\n"
            "\n"
            "```python\n"
            "output_beam = model.generate(\n"
            "    input_ids,\n"
            "    max_new_tokens=80,\n"
            "    num_beams=5,\n"
            "    do_sample=False,\n"
            "    no_repeat_ngram_size=2,\n"
            ")\n"
            "```\n"
            "\n"
            "This may reduce repetition even when the resulting sequence has a lower model "
            "log probability.\n"
            "\n"
            "That teaches an important generation principle:\n"
            "\n"
            "> **Optimizing model probability alone is not identical to optimizing useful "
            "text quality.**\n"
            "\n"
            "For tasks such as translation or summarization, deterministic search plus "
            "repetition controls can be useful when stable output matters more than creativity.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 7
            # ----------------------------------------------------------------

            "## 7. Sampling: allow more than one possible future\n"
            "\n"
            "Greedy and ordinary beam search are deterministic. If you give them the same "
            "model, prompt, and settings, they tend to choose the same result.\n"
            "\n"
            "Sampling changes the rule. Instead of always selecting the highest-probability "
            "token, we **sample from the probability distribution**.\n"
            "\n"
            "A high-probability token is still more likely to be selected, but another "
            "plausible token may occasionally be chosen.\n"
            "\n"
            "This creates diversity.\n"
            "\n"
            "### Temperature\n"
            "\n"
            "Temperature rescales the logits before softmax:\n"
            "\n"
            "```text\n"
            "probabilities = softmax(logits / temperature)\n"
            "```\n"
            "\n"
            "Think of temperature as controlling how strongly the model prefers the current "
            "leaders.\n"
            "\n"
            "| Temperature behavior | Effect |\n"
            "|---|---|\n"
            "| Lower | Distribution becomes sharper; high-probability tokens dominate |\n"
            "| Higher | Distribution becomes flatter; lower-probability tokens become more competitive |\n"
            "\n"
            "So:\n"
            "\n"
            "```text\n"
            "lower temperature  → usually more conservative/coherent\n"
            "higher temperature → usually more varied/risky\n"
            "```\n"
            "\n"
            "Example:\n"
            "\n"
            "```python\n"
            "output = model.generate(\n"
            "    input_ids,\n"
            "    max_new_tokens=80,\n"
            "    do_sample=True,\n"
            "    temperature=0.7,\n"
            "    top_k=0,\n"
            ")\n"
            "```\n"
            "\n"
            "The chapter illustrates that excessively high temperature can promote rare "
            "tokens so strongly that the generated text becomes incoherent.\n"
            "\n"
            "[[IMAGE_NEEDED: Temperature changes token probabilities | "
            "Three probability distributions over the same candidate tokens for low, medium, "
            "and high temperature, with low temperature sharply concentrated and high "
            "temperature flatter | "
            "Learner should notice that temperature changes the distribution rather than "
            "directly specifying which token must be selected]]\n"
            "\n"
            "{{exercise:M01.L04.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 8
            # ----------------------------------------------------------------

            "## 8. Top-k sampling: cut off the long tail\n"
            "\n"
            "Sampling from the entire vocabulary has a weakness. Even a very unlikely token "
            "has some chance of eventually being sampled.\n"
            "\n"
            "When generating many tokens, small risks accumulate. One strange token can send "
            "the continuation in a poor direction.\n"
            "\n"
            "**Top-k sampling** limits sampling to the `k` highest-probability tokens at each "
            "generation step.\n"
            "\n"
            "If:\n"
            "\n"
            "```text\n"
            "k = 50\n"
            "```\n"
            "\n"
            "the decoder throws away every candidate except the current top 50, renormalizes "
            "the remaining probabilities, and samples from that smaller set.\n"
            "\n"
            "```python\n"
            "output_topk = model.generate(\n"
            "    input_ids,\n"
            "    max_new_tokens=80,\n"
            "    do_sample=True,\n"
            "    top_k=50,\n"
            ")\n"
            "```\n"
            "\n"
            "### Limitation\n"
            "\n"
            "`k` is fixed even though the uncertainty of the model changes from one token "
            "position to another.\n"
            "\n"
            "Sometimes only a few continuations are plausible. At another position, many "
            "continuations may be reasonable. A fixed cutoff cannot adapt to this difference.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 9
            # ----------------------------------------------------------------

            "## 9. Nucleus sampling: choose a probability mass, not a fixed count\n"
            "\n"
            "**Nucleus sampling**, also called **top-p sampling**, creates a dynamic candidate "
            "set.\n"
            "\n"
            "Suppose:\n"
            "\n"
            "```text\n"
            "top_p = 0.90\n"
            "```\n"
            "\n"
            "The algorithm:\n"
            "\n"
            "1. sorts candidate tokens from highest to lowest probability,\n"
            "2. starts adding them to the candidate set,\n"
            "3. stops once their cumulative probability reaches roughly 90%,\n"
            "4. samples from that selected nucleus.\n"
            "\n"
            "If one token is overwhelmingly likely, the candidate set may be very small. "
            "If the model is uncertain, the set can contain many tokens.\n"
            "\n"
            "```python\n"
            "output_topp = model.generate(\n"
            "    input_ids,\n"
            "    max_new_tokens=80,\n"
            "    do_sample=True,\n"
            "    top_p=0.90,\n"
            ")\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Top-k versus top-p sampling | "
            "A sorted next-token probability distribution with one fixed vertical cutoff "
            "illustrating top-k and one cumulative-probability threshold illustrating top-p | "
            "Learner should notice that top-k keeps a fixed number of tokens while top-p "
            "adapts the number of candidates to the shape of the distribution]]\n"
            "\n"
            "### Combine top-k and top-p\n"
            "\n"
            "The two constraints can also be combined. For example:\n"
            "\n"
            "```python\n"
            "output = model.generate(\n"
            "    input_ids,\n"
            "    max_new_tokens=80,\n"
            "    do_sample=True,\n"
            "    top_k=50,\n"
            "    top_p=0.90,\n"
            ")\n"
            "```\n"
            "\n"
            "Conceptually this says:\n"
            "\n"
            "> Sample from a high-probability nucleus, but do not let the candidate pool "
            "grow beyond the top 50 tokens.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 10
            # ----------------------------------------------------------------

            "## 10. Which decoding method should you use?\n"
            "\n"
            "There is no universally best decoder. The correct choice depends on what kind "
            "of output you need.\n"
            "\n"
            "| Need | Reasonable direction |\n"
            "|---|---|\n"
            "| Stable, deterministic short output | Greedy or another deterministic strategy |\n"
            "| Search among several likely sequences | Beam search |\n"
            "| Reduce repeated phrases in deterministic generation | Repetition constraints such as n-gram blocking |\n"
            "| More diverse continuation | Sampling |\n"
            "| More conservative sampling | Lower temperature |\n"
            "| More varied sampling | Higher temperature, used carefully |\n"
            "| Avoid sampling from very unlikely tail tokens | Top-k or top-p |\n"
            "| Adaptive candidate-set size | Top-p |\n"
            "\n"
            "The chapter contrasts precise tasks with more creative generation. A task where "
            "you strongly prefer a stable high-probability answer calls for a different "
            "decoding strategy from story generation or open-ended conversation.\n"
            "\n"
            "### Do not confuse decoding with factuality\n"
            "\n"
            "A decoding strategy controls **which continuation is selected from the model's "
            "distribution**. It does not make the underlying model know whether a generated "
            "claim is true.\n"
            "\n"
            "A fluent high-probability continuation can still contain invented information.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 11
            # ----------------------------------------------------------------

            "## 11. Why text generation is computationally expensive\n"
            "\n"
            "For ordinary sequence classification, we can often obtain a prediction from "
            "one model forward pass.\n"
            "\n"
            "Autoregressive generation is iterative:\n"
            "\n"
            "```text\n"
            "generate token 1\n"
            "      ↓\n"
            "generate token 2\n"
            "      ↓\n"
            "generate token 3\n"
            "      ↓\n"
            "...\n"
            "```\n"
            "\n"
            "We need model computation for every generated token. Beam search increases the "
            "work further because several candidate sequences are tracked.\n"
            "\n"
            "This matters when deploying generation systems at scale. Generation quality is "
            "only one part of the engineering problem; latency, memory, throughput, and cost "
            "also matter.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 12
            # ----------------------------------------------------------------

            "## 12. Put the whole generation process together\n"
            "\n"
            "Use this mental model whenever you work with a generative transformer:\n"
            "\n"
            "```text\n"
            "Prompt\n"
            "  ↓\n"
            "Tokenizer\n"
            "  ↓\n"
            "Current token IDs\n"
            "  ↓\n"
            "Causal language model\n"
            "  ↓\n"
            "Next-token logits\n"
            "  ↓\n"
            "Softmax / adjusted probability distribution\n"
            "  ↓\n"
            "Decoding rule\n"
            "  ├── greedy\n"
            "  ├── beam search\n"
            "  └── sampling\n"
            "       ├── temperature\n"
            "       ├── top-k\n"
            "       └── top-p\n"
            "  ↓\n"
            "Choose next token\n"
            "  ↓\n"
            "Append token and repeat\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Complete text-generation decoding workflow | "
            "A single flowchart from prompt and tokenizer through model logits, probability "
            "adjustments, decoding choices, selected token, and the feedback loop into the "
            "next generation step | "
            "Learner should see clearly that the model and decoder are separate parts of the "
            "generation system]]\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Misconceptions
            # ----------------------------------------------------------------

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: The model generates a whole answer at once\n"
            "\n"
            "> The network predicts the finished paragraph in a single forward pass.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Autoregressive models generate iteratively. Each selected token becomes part "
            "of the context for the next prediction.\n"
            "\n"
            "### Misconception 2: Greedy search always finds the most probable complete sequence\n"
            "\n"
            "> Choosing the best token at every step guarantees the best final text.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A locally optimal token can lead to a poor later path. Beam search explores "
            "multiple partial sequences to reduce this limitation.\n"
            "\n"
            "### Misconception 3: Higher temperature makes the model smarter\n"
            "\n"
            "> Increasing temperature improves model knowledge or reasoning.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Temperature only reshapes the probability distribution used for sampling. "
            "Higher values increase randomness and can eventually reduce coherence.\n"
            "\n"
            "### Misconception 4: A higher model probability always means better text\n"
            "\n"
            "> The sequence with the best log probability must be the most useful human output.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Probability is the model's preference, not a complete human-quality metric. "
            "Repetition, usefulness, factuality, and task requirements also matter.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Key terminology
            # ----------------------------------------------------------------

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Autoregressive model | Model that predicts the next token using previous context |\n"
            "| Causal language model | Autoregressive language model whose prediction cannot use future tokens |\n"
            "| Conditional generation | Generation conditioned on an initial prompt/context |\n"
            "| Logit | Raw model score before probability normalization |\n"
            "| Softmax | Function that turns logits into a normalized probability distribution |\n"
            "| Decoding | Process for selecting output tokens from model scores/probabilities |\n"
            "| Greedy search | Chooses the highest-probability token at every step |\n"
            "| Beam search | Maintains several high-scoring partial sequences during decoding |\n"
            "| Beam | One partial candidate sequence in beam search |\n"
            "| Log probability | Logarithm of probability; allows sequence scores to be summed stably |\n"
            "| n-gram | Sequence of n consecutive tokens |\n"
            "| Sampling | Randomly selecting tokens according to an adjusted probability distribution |\n"
            "| Temperature | Parameter controlling how peaked or flat the sampling distribution is |\n"
            "| Top-k | Sampling only from the k highest-probability tokens |\n"
            "| Top-p / nucleus | Sampling from the smallest high-probability set reaching a probability mass p |\n"
            "| EOS | End-of-sequence token used to indicate completion |\n"
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
            "1. Why does autoregressive generation require repeated model calls?\n"
            "2. What is the difference between the language model and the decoder?\n"
            "3. Why can greedy search miss a better complete sequence?\n"
            "4. What extra work does beam search perform?\n"
            "5. Why are log probabilities used to compare long sequences?\n"
            "6. What problem can `no_repeat_ngram_size` help reduce?\n"
            "7. What happens to the sampling distribution when temperature increases?\n"
            "8. How does top-k differ from top-p?\n"
            "9. Why might you prefer sampling for a creative task?\n"
            "10. Why does a fluent generated continuation not guarantee factual correctness?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**A causal language model supplies probabilities for the next token; the "
            "decoding strategy determines how those probabilities become text. Greedy "
            "search, beam search, temperature, top-k, and top-p are therefore different "
            "ways of navigating the same model distribution, each trading off stability, "
            "compute, repetition, and diversity.**\n"
        ),

        "estimated_minutes": 105,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "generation-intuition",
                "title": "What does a language model actually generate?",
                "order": 1,
            },
            {
                "id": "causal-lm",
                "title": "Causal language modeling",
                "order": 2,
            },
            {
                "id": "greedy-search",
                "title": "Greedy search",
                "order": 3,
            },
            {
                "id": "beam-search",
                "title": "Beam search",
                "order": 4,
            },
            {
                "id": "log-probabilities",
                "title": "Why beam search uses log probabilities",
                "order": 5,
            },
            {
                "id": "repetition",
                "title": "Controlling repetition",
                "order": 6,
            },
            {
                "id": "sampling-temperature",
                "title": "Sampling and temperature",
                "order": 7,
            },
            {
                "id": "top-k",
                "title": "Top-k sampling",
                "order": 8,
            },
            {
                "id": "top-p",
                "title": "Nucleus sampling",
                "order": 9,
            },
            {
                "id": "strategy-selection",
                "title": "Choosing a decoding method",
                "order": 10,
            },
            {
                "id": "compute-cost",
                "title": "Generation compute cost",
                "order": 11,
            },
            {
                "id": "mental-model",
                "title": "Complete generation mental model",
                "order": 12,
            },
        ],
    },

    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L04.EX01",
            "title": "Trace Autoregressive Generation",
            "lesson_code": "M01.L04",
            "section_id": "causal-lm",
            "placement": "after_section",
            "description": (
                "Practice thinking about text generation as repeated next-token prediction "
                "rather than one-shot paragraph generation."
            ),
            "instructions": (
                "1. Start with the prompt: 'Machine learning can'.\n"
                "2. Imagine the model's top next-token candidates are 'help' = 0.50, "
                "'be' = 0.30, and 'learn' = 0.20.\n"
                "3. Using greedy decoding, select the next token.\n"
                "4. Write the new input sequence that is sent back to the model.\n"
                "5. Suppose the next distribution is 'solve' = 0.45, 'people' = 0.35, "
                "'systems' = 0.20. Select the next token.\n"
                "6. Explain why the second distribution cannot be known before the first "
                "token has been selected and appended."
            ),
            "expected_output": (
                "A two-step generation trace. Greedy decoding first chooses 'help', giving "
                "'Machine learning can help', then chooses 'solve', giving "
                "'Machine learning can help solve', plus an explanation that each new token "
                "changes the context used for the next prediction."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "autoregressive-generation",
                "causal-language-modeling",
                "greedy-decoding",
            ],
        },

        {
            "id": "M01.L04.EX02",
            "title": "Choose a Decoding Strategy",
            "lesson_code": "M01.L04",
            "section_id": "sampling-temperature",
            "placement": "after_section",
            "description": (
                "Match decoding behavior to different product requirements instead of "
                "treating one generation setting as universally best."
            ),
            "instructions": (
                "For each scenario below, choose a reasonable starting decoding strategy "
                "and explain your choice:\n"
                "1. Generate one short, stable completion for a structured deterministic task.\n"
                "2. Generate a creative story continuation where variety is desirable.\n"
                "3. Generate a long continuation that keeps repeating the same phrase.\n"
                "4. You are sampling but occasionally obtain bizarre very-low-probability words.\n"
                "5. Compare top-k=50 with top-p=0.9 in one sentence."
            ),
            "expected_output": (
                "A short strategy table. Answers should connect deterministic generation "
                "with greedy/beam-style search, creative generation with sampling, repetition "
                "with an n-gram constraint, unlikely tail tokens with top-k/top-p, and explain "
                "that top-k fixes candidate count while top-p adapts it to probability mass."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "decoding-strategy",
                "temperature",
                "top-k",
                "top-p",
                "generation-tradeoffs",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L04.QZ01",
        "title": "Text Generation — Knowledge Check",
        "lesson_code": "M01.L04",
        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L04.Q01",
                "section_id": "generation-intuition",
                "question": (
                    "What happens immediately after an autoregressive decoder selects a "
                    "new token?"
                ),
                "options": [
                    "The whole generated paragraph is discarded.",
                    "The token is appended to the current sequence and becomes context for "
                    "the next prediction.",
                    "The model switches from causal attention to bidirectional attention.",
                    "All vocabulary probabilities are permanently fixed.",
                ],
                "correct": 1,
                "explanation": (
                    "Autoregressive generation is iterative. Each selected token becomes "
                    "part of the input context for the following next-token prediction."
                ),
            },

            {
                "id": "M01.L04.Q02",
                "section_id": "greedy-search",
                "question": "What is the defining rule of greedy decoding?",
                "options": [
                    "Sample uniformly from the vocabulary.",
                    "Keep every possible sequence until generation ends.",
                    "Choose the highest-probability next token at each step.",
                    "Always choose the second-highest-probability token.",
                ],
                "correct": 2,
                "explanation": (
                    "Greedy decoding makes the locally highest-probability choice at every "
                    "step, without keeping alternative paths."
                ),
            },

            {
                "id": "M01.L04.Q03",
                "section_id": "log-probabilities",
                "question": (
                    "Why are log probabilities convenient when scoring long generated sequences?"
                ),
                "options": [
                    "They turn every token probability into a positive integer.",
                    "They allow products of many small probabilities to be represented as "
                    "sums, reducing numerical underflow problems.",
                    "They guarantee that the text is factually correct.",
                    "They remove the need to compute token probabilities.",
                ],
                "correct": 1,
                "explanation": (
                    "The probability of a sequence involves multiplying many conditional "
                    "probabilities. Taking logs changes the product into a numerically safer sum."
                ),
            },

            {
                "id": "M01.L04.Q04",
                "section_id": "top-p",
                "question": "What is the main difference between top-k and top-p sampling?",
                "options": [
                    "Top-k keeps a fixed number of high-probability tokens, while top-p "
                    "keeps a variable-size set whose cumulative probability reaches a threshold.",
                    "Top-p is deterministic while top-k cannot sample.",
                    "Top-k changes model weights while top-p changes tokenizer vocabulary.",
                    "They are two names for exactly the same algorithm.",
                ],
                "correct": 0,
                "explanation": (
                    "Top-k applies a fixed candidate-count cutoff. Top-p adapts the number "
                    "of candidates according to how probability mass is distributed at the "
                    "current generation step."
                ),
            },

            {
                "id": "M01.L04.Q05",
                "section_id": "strategy-selection",
                "type": "open",
                "question": (
                    "A product needs two generation modes: a stable short-answer mode and "
                    "a creative story mode. Propose a starting decoding approach for each. "
                    "Explain how temperature, top-k/top-p, beam search, and repetition "
                    "controls influence your decision."
                ),
            },
        ],

        "passing_score": 70,
    },
}
