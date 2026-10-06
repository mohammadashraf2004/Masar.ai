"""M09.L01 — How Transformers Work.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 9.
Instructor-authored curriculum adaptation.

Quality improvements applied from learner feedback:
- balanced quiz-answer positions
- explicit train/eval/no_grad/device best practices
- realistic study-time estimate
- short learning checkpoints after dense concept clusters
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M09.L01"
MODULE_ORDER = 9
MODULE_TITLE = "Transformers & Generative Sequence Models"
MODULE_DESCRIPTION = (
    "Build intuition from simple probabilistic character generation to self-supervised "
    "next-token learning, embeddings, attention, causal masking, transformer decoders, "
    "encoder and encoder-decoder variants, tokenization, and Vision Transformers."
)

SOURCE_CHAPTER = 9
SOURCE_PAGES = "Chapter 9 (page range not provided in source excerpt)"


TOPIC = {
    "title": "How Transformers Work",
    "slug": "applied-deep-learning-m09-l01",
    "description": (
        "A step-by-step journey from character-level probabilistic generation to modern "
        "Transformer architecture, including self-supervised next-token prediction, "
        "embeddings, scaled causal self-attention, multi-head attention, positional "
        "embeddings, layer normalization, tokenization, and Vision Transformers."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 6.0,
    "skill_tags": [
        "generative-ai",
        "language-modeling",
        "self-supervised-learning",
        "bigram-model",
        "next-token-prediction",
        "embeddings",
        "autoregressive-generation",
        "attention",
        "self-attention",
        "query-key-value",
        "causal-mask",
        "scaled-dot-product-attention",
        "multi-head-attention",
        "transformer",
        "decoder",
        "encoder",
        "encoder-decoder",
        "positional-embeddings",
        "layer-normalization",
        "tokenization",
        "vision-transformer",
        "module-09",
    ],
    "prerequisite_ids": ["M08.L01"],

    "lesson": {
        "title": "How Transformers Work",
        "content": (
            "# How Transformers Work\n\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M09.L01  \n"
            "> **Module:** Transformers & Generative Sequence Models  \n"
            "> **Source alignment:** *Deep Learning with PyTorch, Second Edition*, Chapter 9. "
            "This lesson is an instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n\n"
            "> **Study expectation:** This is a dense chapter. A realistic first pass is about **6 hours**, "
            "including code tracing, checkpoints, and exercises. Do not try to memorize the full Transformer "
            "in one sitting; understand the progression from one model to the next.\n\n"
            "---\n\n"

            "## Learning outcomes\n\n"
            "By the end of this lesson, you should be able to:\n\n"
            "- Explain the text-generation problem as probabilistic next-token prediction.\n"
            "- Define vocabulary, token, sequence, and special boundary tokens.\n"
            "- Explain why uniform random character sampling produces poor language.\n"
            "- Build and interpret a character bigram model.\n"
            "- Explain self-supervised learning in the context of next-token prediction.\n"
            "- Describe data sparsity and why n-gram tables scale poorly.\n"
            "- Create input-target sequence pairs from unlabeled text.\n"
            "- Pad variable-length sequences and ignore padded targets in the loss.\n"
            "- Use `nn.Embedding` as a trainable lookup table.\n"
            "- Explain autoregressive generation.\n"
            "- Explain why static embeddings alone cannot fully represent context.\n"
            "- Define query, key, and value vectors in attention.\n"
            "- Implement basic dot-product self-attention.\n"
            "- Explain batching, causal masking, and scaling in causal self-attention.\n"
            "- Use `F.scaled_dot_product_attention` appropriately.\n"
            "- Explain multi-head attention, residual connections, positional embeddings, and layer normalization.\n"
            "- Build the conceptual structure of a GPT-style decoder.\n"
            "- Distinguish decoder-only, encoder-only, and encoder-decoder Transformers.\n"
            "- Explain how tokenization turns raw text into model-ready token IDs.\n"
            "- Explain why Transformers can operate on tokens other than text, including image patches.\n"
            "- Describe the main data flow of a Vision Transformer.\n\n"
            "---\n\n"

            "## 1. From prediction to generation\n\n"
            "Earlier chapters focused mainly on regression and classification. In those tasks, each input "
            "is associated with a relatively clear target: predict a number or select a class.\n\n"
            "Generation looks different because the set of possible outputs is enormous. A text model can "
            "produce many different valid continuations, and there is rarely one uniquely correct sentence.\n\n"
            "The chapter's key idea is that generation becomes manageable when we model **structure statistically**.\n\n"
            "Instead of programming explicit grammar rules, we learn patterns from examples and estimate what "
            "is likely to come next.\n\n"
            "This is the bridge from simple statistical generation to modern language models.\n\n"
            "[[IMAGE_NEEDED: Prediction versus generation | Left side shows regression/classification with one "
            "input leading to a constrained target; right side shows a text prefix branching into many plausible "
            "next-token continuations | Learner should notice that generation is handled by modeling a probability "
            "distribution rather than selecting one permanently fixed answer]]\n\n"
            "The chapter uses early rule-based systems such as ELIZA as historical contrast: convincing language-like "
            "behavior can be produced without genuinely modeling rich conversational context. Transformers address the "
            "context problem using learned representations and attention rather than hand-authored response rules.\n\n"
            "---\n\n"

            "## 2. Learn hidden structure instead of writing the rules by hand\n\n"
            "Natural data contains recurring but difficult-to-program patterns. In language these include spelling, "
            "word order, syntax, semantic relationships, style, and long-range dependencies.\n\n"
            "The chapter describes these hidden regularities as **latent structure**.\n\n"
            "A generative model tries to learn enough of this structure to assign useful probabilities to possible "
            "continuations and then sample new sequences that resemble the training distribution without simply using "
            "a handcrafted template.\n\n"
            "The same broad concept extends beyond text to music and images: learn structure from examples, then use "
            "the learned statistical model to generate new content.\n\n"
            "---\n\n"

            "## 3. Motivating problem: generate human names one character at a time\n\n"
            "The chapter starts deliberately small: generate realistic English names character by character.\n\n"
            "This lets us understand the same core ideas used by larger language models without beginning with huge vocabularies "
            "or billions of parameters.\n\n"
            "### Vocabulary\n\n"
            "A **vocabulary** is the set of distinct elements the model can recognize and produce.\n\n"
            "For the simple name model:\n\n"
            "```python\n"
            "vocab = '$abcdefghijklmnopqrstuvwxyz'\n"
            "vocab_size = len(vocab)\n\n"
            "ch_to_i = {char: i for i, char in enumerate(vocab)}\n"
            "i_to_ch = {i: char for i, char in enumerate(vocab)}\n"
            "```\n\n"
            "Each vocabulary element is a **token**.\n\n"
            "The `$` token is special: it represents a name boundary. So:\n\n"
            "```text\n"
            "ada -> $ada$\n"
            "```\n\n"
            "becomes a sequence of integer token IDs.\n\n"
            "[[IMAGE_NEEDED: Vocabulary tokens and encoded sequence | A small character vocabulary mapping letters "
            "and the $ boundary token to integer IDs, then the name $ada$ shown as its token-ID sequence | Learner "
            "should notice the distinction between raw characters, tokens, and integer model inputs]]\n\n"
            "---\n\n"

            "## 4. Baseline: sample every character with equal probability\n\n"
            "The simplest generator can assign every vocabulary item the same probability.\n\n"
            "```python\n"
            "equal_probs = F.softmax(torch.ones(vocab_size), dim=0)\n"
            "```\n\n"
            "Then sample repeatedly:\n\n"
            "```python\n"
            "random_int = torch.multinomial(equal_probs, 1).item()\n"
            "```\n\n"
            "This creates sequences, but they usually do not resemble names.\n\n"
            "Why? Because real language is not uniform.\n\n"
            "- some characters are much more common than others,\n"
            "- some characters rarely occur in certain positions,\n"
            "- some character pairs are common,\n"
            "- sequence length is structured too.\n\n"
            "The failure of the random baseline teaches us what the model must learn: **conditional structure**.\n\n"
            "---\n\n"

            "## 5. Bigram model: use the previous character as context\n\n"
            "A **bigram model** estimates the probability of one token following another.\n\n"
            "Conceptually:\n\n"
            "```text\n"
            "P(next_character | current_character)\n"
            "```\n\n"
            "With 27 tokens, we can store pair statistics in a `27 × 27` matrix.\n\n"
            "```python\n"
            "bigram = torch.zeros((vocab_size, vocab_size))\n\n"
            "for name in names:\n"
            "    for ch1, ch2 in zip(name, name[1:]):\n"
            "        i = ch_to_i[ch1]\n"
            "        j = ch_to_i[ch2]\n"
            "        bigram[i, j] += 1\n"
            "```\n\n"
            "Each row tells us which characters tend to follow one current character.\n\n"
            "[[IMAGE_NEEDED: Character bigram matrix | A small heatmap-style matrix where rows are current characters "
            "and columns are possible next characters, with darker cells for more likely transitions | Learner should "
            "notice that generation now depends on the previous token rather than a single global distribution]]\n\n"
            "Generation then repeatedly samples from the row associated with the most recently generated character.\n\n"
            "The results are better than uniform random sampling, but they still often produce unrealistic names because one character "
            "of context is a severe limitation.\n\n"

            "### Learning checkpoint 1 — Can you explain the progression?\n\n"
            "Before continuing, answer these without looking back:\n\n"
            "1. Why does uniform random sampling fail?\n"
            "2. What information does one row of a bigram matrix represent?\n"
            "3. Why can a bigram model still produce unrealistic names?\n\n"
            "If any answer feels vague, reread sections 3–5 before moving on.\n\n"
            "---\n\n"

            "## 6. Self-supervised learning: targets can come from the data itself\n\n"
            "Previous supervised tasks used externally provided labels. Here, a raw sequence already contains the information "
            "needed to define a learning target.\n\n"
            "If the model sees a prefix, the next token in the original sequence becomes the target.\n\n"
            "For:\n\n"
            "```text\n"
            "$ada$\n"
            "```\n\n"
            "we can construct:\n\n"
            "| Input prefix | Target |\n"
            "|---|---|\n"
            "| `$` | `a` |\n"
            "| `$a` | `d` |\n"
            "| `$ad` | `a` |\n"
            "| `$ada` | `$` |\n\n"
            "No human needed to label these individual examples. The sequence provides its own supervision.\n\n"
            "This is the chapter's central **self-supervised learning** pattern.\n\n"
            "It is powerful because massive amounts of text can be turned into training examples automatically.\n\n"
            "---\n\n"

            "## 7. Why lookup-table language models do not scale\n\n"
            "The bigram table grows with the number of possible token pairs.\n\n"
            "For vocabulary size `V`:\n\n"
            "```text\n"
            "bigram combinations = V²\n"
            "```\n\n"
            "If we condition on two previous tokens instead:\n\n"
            "```text\n"
            "trigram-style combinations = V³\n"
            "```\n\n"
            "The number grows rapidly as vocabulary size or context length increases.\n\n"
            "This creates **data sparsity**: many possible combinations appear rarely or never, so a pure lookup table cannot "
            "estimate them reliably.\n\n"
            "Neural networks offer a different strategy. They represent tokens using learned dense vectors and use shared model "
            "parameters to generalize across related patterns rather than storing an independent probability for every possible context.\n\n"
            "---\n\n"

            "## 8. Convert sequences into model-ready training tensors\n\n"
            "First encode every character:\n\n"
            "```python\n"
            "encode = lambda word: torch.tensor([ch_to_i[c] for c in word])\n"
            "```\n\n"
            "Then create shifted targets so that the model predicts the next token.\n\n"
            "For example:\n\n"
            "```text\n"
            "input : [$, a, d, a, $]\n"
            "target: [a, d, a, $]\n"
            "```\n\n"
            "Variable-length names must be padded to form rectangular batch tensors.\n\n"
            "The source uses:\n\n"
            "- input padding value `0`,\n"
            "- target padding value `-1`,\n"
            "- `ignore_index=-1` in cross-entropy so padded target positions do not contribute to loss.\n\n"
            "```python\n"
            "loss = F.cross_entropy(\n"
            "    logits.view(-1, logits.shape[-1]),\n"
            "    labels.view(-1),\n"
            "    ignore_index=-1,\n"
            ")\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Shifted next-token targets with padding | Several names of different lengths shown as "
            "rectangular input and target tensors, with targets shifted left and padded target cells marked -1/ignored | "
            "Learner should notice how one raw sequence becomes many next-token learning positions]]\n\n"
            "---\n\n"

            "## 9. Embeddings: learn a vector for every token\n\n"
            "Integer token IDs are identifiers, not meaningful continuous measurements.\n\n"
            "`nn.Embedding` converts each token ID into a learned dense vector:\n\n"
            "```python\n"
            "embedding_dim = 3\n"
            "embedding = nn.Embedding(vocab_size, embedding_dim)\n\n"
            "example_input = torch.tensor([1, 1, 0, 2])\n"
            "input_embd = embedding(example_input)\n"
            "```\n\n"
            "The embedding layer behaves like a trainable lookup table. If the input contains four token IDs and embedding dimension is 3, "
            "the output shape is:\n\n"
            "```text\n"
            "4 × 3\n"
            "```\n\n"
            "Repeated token IDs retrieve the same current embedding vector.\n\n"
            "During training, backpropagation updates those vectors so the representation becomes useful for the task.\n\n"
            "[[IMAGE_NEEDED: Embedding lookup table | Token IDs indexing rows of a learnable embedding matrix and returning dense vectors | "
            "Learner should notice that embeddings are trainable parameters, not fixed handcrafted encodings]]\n\n"
            "---\n\n"

            "## 10. First neural language model: embeddings plus an MLP\n\n"
            "The chapter next replaces the probability table with a neural network.\n\n"
            "The basic strategy is:\n\n"
            "```text\n"
            "token IDs\n"
            " -> embeddings\n"
            " -> flatten a prefix representation\n"
            " -> hidden linear layer + activation\n"
            " -> vocabulary-sized logits\n"
            "```\n\n"
            "The output dimension equals vocabulary size because each output position needs one score per possible next token.\n\n"
            "The chapter's `SequenceMLP` explicitly constructs prefix representations of increasing length and uses a hidden layer to predict "
            "the next character at every valid position.\n\n"
            "This already generalizes better than a direct bigram lookup because learned weights are shared across many training examples.\n\n"
            "---\n\n"

            "## 11. A cleaner training loop for sequence models\n\n"
            "The chapter's training loop follows the familiar pattern. For Masar production lessons, use a slightly cleaner version that "
            "makes model mode and device handling explicit:\n\n"
            "```python\n"
            "def train_steps(model, optimizer, get_batch, device, num_steps=10_000):\n"
            "    model.train()\n\n"
            "    for step in range(1, num_steps + 1):\n"
            "        inputs, labels = get_batch()\n"
            "        inputs = inputs.to(device)\n"
            "        labels = labels.to(device)\n\n"
            "        optimizer.zero_grad(set_to_none=True)\n\n"
            "        logits = model(inputs)\n"
            "        loss = F.cross_entropy(\n"
            "            logits.reshape(-1, logits.shape[-1]),\n"
            "            labels.reshape(-1),\n"
            "            ignore_index=-1,\n"
            "        )\n\n"
            "        loss.backward()\n"
            "        optimizer.step()\n"
            "```\n\n"
            "Why these details matter:\n\n"
            "- `model.train()` makes training mode explicit.\n"
            "- inputs and labels are moved to the same device as the model.\n"
            "- `zero_grad(set_to_none=True)` is a clean way to clear old gradients.\n"
            "- `reshape` expresses the intention to combine batch and sequence positions for cross-entropy.\n"
            "- padded targets stay excluded with `ignore_index=-1`.\n\n"
            "For evaluation or generation, use `model.eval()` and disable gradients where appropriate.\n\n"
            "{{exercise:M09.L01.EX01}}\n\n"
            "---\n\n"

            "## 12. Autoregressive generation\n\n"
            "After training a next-token predictor, generation becomes a loop:\n\n"
            "```text\n"
            "start token\n"
            " -> predict next-token distribution\n"
            " -> sample one token\n"
            " -> append it to the sequence\n"
            " -> feed the longer sequence back into the model\n"
            " -> repeat\n"
            "```\n\n"
            "This is called **autoregressive generation** because the model uses previously generated outputs as part of the next input.\n\n"
            "A production-friendly generation skeleton is:\n\n"
            "```python\n"
            "@torch.no_grad()\n"
            "def generate(model, start_tokens, max_new_tokens):\n"
            "    model.eval()\n"
            "    sequence = start_tokens\n\n"
            "    for _ in range(max_new_tokens):\n"
            "        logits = model(sequence)\n"
            "        next_logits = logits[:, -1, :]\n"
            "        probs = F.softmax(next_logits, dim=-1)\n"
            "        next_token = torch.multinomial(probs, num_samples=1)\n"
            "        sequence = torch.cat((sequence, next_token), dim=1)\n\n"
            "    return sequence\n"
            "```\n\n"
            "Sampling rather than always choosing the largest logit allows different outputs to be produced from the same model.\n\n"
            "---\n\n"

            "## 13. What learned embeddings can reveal\n\n"
            "Because the chapter intentionally uses a 3-dimensional character embedding, the learned vectors can be plotted directly.\n\n"
            "After training, structurally similar characters can move into related regions of embedding space. The source observes grouping patterns "
            "such as vowels appearing closer to one another and the special boundary token separating from ordinary letters.\n\n"
            "Do not interpret every embedding coordinate as a clean human concept. The important idea is that training organizes representations in "
            "whatever geometry helps the prediction task.\n\n"

            "### Learning checkpoint 2 — Representation learning\n\n"
            "You should now be able to explain:\n\n"
            "1. how raw text creates its own next-token targets,\n"
            "2. why padded targets need to be ignored,\n"
            "3. what an embedding layer learns,\n"
            "4. how autoregressive generation reuses model outputs.\n\n"
            "If those four ideas are clear, attention will be much easier to understand.\n\n"
            "---\n\n"

            "## 14. Why embeddings alone are not enough\n\n"
            "A standard token embedding is **static**: the same token ID retrieves the same vector no matter where it appears.\n\n"
            "But the importance and role of a token can depend on surrounding context.\n\n"
            "Attention introduces a dynamic computation in which each position can decide which other positions matter most for its current representation.\n\n"
            "The chapter's analogy is a spotlight: the model can direct more focus toward the sequence positions that are most relevant right now.\n\n"
            "---\n\n"

            "## 15. Query, key, and value\n\n"
            "Attention uses three learned views of the sequence:\n\n"
            "- **Query (Q):** what this position is looking for.\n"
            "- **Key (K):** what each position advertises for matching.\n"
            "- **Value (V):** the information that will actually be combined when a match is important.\n\n"
            "[[IMAGE_NEEDED: Query-key-value intuition | A sequence of token representations transformed into Q, K, and V rows; one query "
            "compares against all keys and then retrieves a weighted mixture of the corresponding values | Learner should distinguish "
            "matching information (Q/K) from retrieved content (V)]]\n\n"
            "The Q, K, and V vectors come from learned linear projections of the input representations.\n\n"
            "---\n\n"

            "## 16. Dot-product self-attention step by step\n\n"
            "For an input matrix `x` with one row per sequence position:\n\n"
            "```python\n"
            "query = query_proj(x)\n"
            "key = key_proj(x)\n"
            "value = value_proj(x)\n"
            "```\n\n"
            "Then compare every query with every key:\n\n"
            "```python\n"
            "scores = query @ key.T\n"
            "```\n\n"
            "Normalize each row:\n\n"
            "```python\n"
            "weights = F.softmax(scores, dim=-1)\n"
            "```\n\n"
            "Finally, mix the value vectors:\n\n"
            "```python\n"
            "output = weights @ value\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Dot-product self-attention matrix flow | Q multiplied by K-transpose to produce an N×N score matrix, "
            "softmax producing row-normalized attention weights, then multiplication by V producing contextualized outputs | Learner "
            "should notice that each output position is a weighted combination of value vectors from the sequence]]\n\n"
            "Because the sequence attends to itself, this is **self-attention**.\n\n"
            "{{exercise:M09.L01.EX02}}\n\n"
            "---\n\n"

            "## 17. Causal attention: do not let the model peek into the future\n\n"
            "For autoregressive generation, token position `t` should only depend on positions up to `t`.\n\n"
            "If position `t` can attend to future ground-truth tokens during training, the model would receive information that will not exist when generating new text.\n\n"
            "A **causal mask** blocks those future positions.\n\n"
            "```python\n"
            "mask = torch.tril(torch.ones(seq_len, seq_len))\n"
            "scores = scores.masked_fill(mask == 0, float('-inf'))\n"
            "```\n\n"
            "After softmax, positions containing negative infinity receive probability zero.\n\n"
            "[[IMAGE_NEEDED: Causal attention matrix | A lower-triangular attention grid where each row may attend to itself and earlier tokens "
            "but all future-token cells are blocked | Learner should notice why the matrix is triangular in an autoregressive decoder]]\n\n"
            "---\n\n"

            "## 18. Why scale the attention scores?\n\n"
            "Dot products can grow in magnitude as the key/query dimension grows. Very large magnitudes can push softmax toward extremely sharp outputs, "
            "which can make optimization numerically awkward.\n\n"
            "Scaled dot-product attention divides scores by:\n\n"
            "```text\n"
            "sqrt(d_k)\n"
            "```\n\n"
            "where `d_k` is the key/query feature dimension.\n\n"
            "Conceptually:\n\n"
            "```python\n"
            "scores = (q @ k.transpose(-2, -1)) / math.sqrt(q.shape[-1])\n"
            "```\n\n"
            "The full causal version is therefore:\n\n"
            "```text\n"
            "QKᵀ\n"
            " -> scale\n"
            " -> causal mask\n"
            " -> softmax\n"
            " -> weighted sum of V\n"
            "```\n\n"
            "---\n\n"

            "## 19. Prefer PyTorch's optimized attention primitive in real code\n\n"
            "After implementing attention manually for learning, the chapter verifies it against:\n\n"
            "```python\n"
            "F.scaled_dot_product_attention(\n"
            "    query,\n"
            "    key,\n"
            "    value,\n"
            "    is_causal=True,\n"
            ")\n"
            "```\n\n"
            "The built-in function performs the same core operation while using optimized implementations when available.\n\n"
            "> **Learning rule:** understand the manual implementation once; use the optimized framework implementation in production unless you have a specific reason not to.\n\n"
            "---\n\n"

            "## 20. Replace prefix flattening with attention\n\n"
            "The chapter then builds an `AttentionMLP`:\n\n"
            "```text\n"
            "token IDs\n"
            " -> token embeddings\n"
            " -> Q/K/V projections\n"
            " -> causal attention\n"
            " -> MLP\n"
            " -> vocabulary logits\n"
            "```\n\n"
            "The important improvement is architectural: each position can combine information from relevant earlier positions directly instead of representing context by manually flattening every prefix.\n\n"
            "Attention weights can also be visualized as an `N × N` matrix to inspect where each position places its focus.\n\n"
            "These visualizations can be educational, but attention weight alone should not automatically be treated as a complete explanation of a model's reasoning.\n\n"

            "### Learning checkpoint 3 — Attention mechanics\n\n"
            "Without code, explain the following pipeline aloud:\n\n"
            "```text\n"
            "embedding -> Q/K/V -> similarity scores -> mask -> scale -> softmax -> weighted V sum\n"
            "```\n\n"
            "Then answer: **why is the mask necessary specifically for autoregressive generation?**\n\n"
            "Do not move to the Transformer block until this sequence makes sense.\n\n"
            "---\n\n"

            "## 21. From attention to the Transformer\n\n"
            "The Transformer architecture popularized attention as the central mechanism for sequence modeling.\n\n"
            "The original architecture contains an encoder and a decoder, but the chapter starts with the **decoder** because decoder-only architectures are the natural fit for generative next-token modeling.\n\n"
            "A decoder block extends causal self-attention with additional components:\n\n"
            "- multi-head attention,\n"
            "- residual connections,\n"
            "- layer normalization,\n"
            "- a feed-forward MLP.\n\n"
            "---\n\n"

            "## 22. Multi-head attention\n\n"
            "One attention calculation produces one pattern of relationships.\n\n"
            "Multi-head attention splits the representation into several parallel heads. Each head has its own projected Q, K, and V subspace and can learn a different attention pattern.\n\n"
            "A simplified shape transformation is:\n\n"
            "```text\n"
            "B × T × D\n"
            " -> B × T × H × D_head\n"
            " -> B × H × T × D_head\n"
            "```\n\n"
            "where:\n\n"
            "- `B` = batch size,\n"
            "- `T` = sequence length,\n"
            "- `D` = embedding dimension,\n"
            "- `H` = number of heads,\n"
            "- `D_head = D / H`.\n\n"
            "After attention, head outputs are concatenated back into the model embedding dimension.\n\n"
            "[[IMAGE_NEEDED: Multi-head self-attention | One token sequence projected into several parallel attention heads, each producing "
            "its own contextual representation, then head outputs concatenated back together | Learner should notice that multiple heads "
            "let the same sequence be analyzed through different learned relationship patterns]]\n\n"
            "---\n\n"

            "## 23. Transformers need positional information\n\n"
            "Self-attention processes relationships between token representations, but by itself it does not provide the model with a sufficient built-in notion of sequence position.\n\n"
            "A decoder therefore adds **positional embeddings** to token embeddings:\n\n"
            "```python\n"
            "char_embd = self.char_embedding(x)\n"
            "pos_embd = self.positional_embedding(torch.arange(seq_len, device=x.device))\n"
            "x = char_embd + pos_embd\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Token embedding plus positional embedding | For each sequence position, a token vector and position vector "
            "are added element-wise before entering Transformer blocks | Learner should notice that content identity and sequence location "
            "are represented together]]\n\n"
            "Without positional information, the model would lose important ordering information needed for language.\n\n"
            "---\n\n"

            "## 24. Residual connections and layer normalization\n\n"
            "Chapter 8 introduced residual connections for deep CNNs. Transformers use the same broad idea to help information and gradients flow through deep stacks.\n\n"
            "Conceptually:\n\n"
            "```python\n"
            "x = norm_1(x + attention_output)\n"
            "x = norm_2(x + mlp(x))\n"
            "```\n\n"
            "The chapter also introduces **LayerNorm**.\n\n"
            "Batch normalization normalizes using statistics across a batch/channel arrangement. Layer normalization instead normalizes across features within each position/sample representation, making it naturally suited to sequence models where batch composition and sequence handling differ from image CNNs.\n\n"
            "[[IMAGE_NEEDED: BatchNorm versus LayerNorm | A small tensor diagram highlighting BatchNorm statistics across examples versus LayerNorm "
            "statistics across feature dimensions for each token representation | Learner should notice that LayerNorm does not depend on other "
            "samples in the minibatch in the same way BatchNorm does]]\n\n"
            "---\n\n"

            "## 25. Build a GPT-style Transformer block\n\n"
            "A simplified block in the chapter performs:\n\n"
            "```text\n"
            "input\n"
            " -> Q/K/V projections\n"
            " -> split into heads\n"
            " -> causal scaled dot-product attention\n"
            " -> merge heads\n"
            " -> residual + LayerNorm\n"
            " -> feed-forward MLP\n"
            " -> residual + LayerNorm\n"
            " -> output\n"
            "```\n\n"
            "A structural skeleton is:\n\n"
            "```python\n"
            "class TransformerBlock(nn.Module):\n"
            "    def __init__(self, n_embd, num_heads=4, n_hidden=64):\n"
            "        super().__init__()\n"
            "        assert n_embd % num_heads == 0\n\n"
            "        self.num_heads = num_heads\n"
            "        self.head_dim = n_embd // num_heads\n\n"
            "        self.query_proj = nn.Linear(n_embd, n_embd)\n"
            "        self.key_proj = nn.Linear(n_embd, n_embd)\n"
            "        self.value_proj = nn.Linear(n_embd, n_embd)\n\n"
            "        self.mlp = nn.Sequential(\n"
            "            nn.Linear(n_embd, n_hidden),\n"
            "            nn.ReLU(),\n"
            "            nn.Linear(n_hidden, n_embd),\n"
            "        )\n\n"
            "        self.norm_1 = nn.LayerNorm(n_embd)\n"
            "        self.norm_2 = nn.LayerNorm(n_embd)\n"
            "```\n\n"
            "The embedding dimension must be divisible by the number of heads so each head receives a consistent feature width.\n\n"
            "{{exercise:M09.L01.EX03}}\n\n"
            "---\n\n"

            "## 26. Stack Transformer blocks into a decoder language model\n\n"
            "The full character-level decoder combines:\n\n"
            "```text\n"
            "token embedding\n"
            "+ positional embedding\n"
            " -> Transformer block\n"
            " -> Transformer block\n"
            " -> ...\n"
            " -> output projection to vocabulary logits\n"
            "```\n\n"
            "A simplified model is:\n\n"
            "```python\n"
            "class Transformer(nn.Module):\n"
            "    def __init__(self, n_embd, vocab_size, block_size, num_blocks=6):\n"
            "        super().__init__()\n"
            "        self.char_embedding = nn.Embedding(vocab_size, n_embd)\n"
            "        self.positional_embedding = nn.Embedding(block_size, n_embd)\n"
            "        self.transformer_blocks = nn.Sequential(\n"
            "            *[TransformerBlock(n_embd) for _ in range(num_blocks)]\n"
            "        )\n"
            "        self.output_proj = nn.Linear(n_embd, vocab_size)\n"
            "```\n\n"
            "The output still has one vocabulary-sized logit vector per sequence position, so the same next-token cross-entropy objective remains applicable.\n\n"

            "### Learning checkpoint 4 — What actually changed?\n\n"
            "Compare these three models:\n\n"
            "```text\n"
            "bigram table\n"
            "embedding + MLP\n"
            "Transformer decoder\n"
            "```\n\n"
            "All three ultimately estimate a next-token distribution. What changes is **how much context they can represent and how flexibly they share information across positions**.\n\n"
            "---\n\n"

            "## 27. Encoder-only Transformers\n\n"
            "A Transformer encoder is similar to the decoder block but does **not** use causal masking in ordinary bidirectional encoding.\n\n"
            "That means a token representation can use information from tokens on both its left and right.\n\n"
            "This makes encoder models well suited to understanding-oriented tasks such as:\n\n"
            "- sentiment classification,\n"
            "- spam detection,\n"
            "- topic classification,\n"
            "- producing context-aware sequence representations.\n\n"
            "The source uses BERT as the familiar encoder-model example.\n\n"
            "---\n\n"

            "## 28. Encoder-decoder Transformers\n\n"
            "The original Transformer combines an encoder and decoder.\n\n"
            "Conceptually:\n\n"
            "```text\n"
            "source sequence\n"
            " -> encoder representations\n"
            " -> decoder attends to encoder information\n"
            " -> generated target sequence\n"
            "```\n\n"
            "In encoder-decoder attention, the decoder's query comes from the decoder side while keys and values can come from encoder outputs.\n\n"
            "This is **cross-attention** because the attention relationship is between two different representation sequences.\n\n"
            "[[IMAGE_NEEDED: Encoder-decoder Transformer and cross-attention | Source tokens flow through an encoder; decoder tokens use causal "
            "self-attention and a separate cross-attention connection into encoder outputs | Learner should distinguish self-attention inside "
            "one sequence from cross-attention between decoder queries and encoder keys/values]]\n\n"
            "Machine translation is the chapter's main motivating application.\n\n"
            "---\n\n"

            "## 29. Tokenization: move beyond individual characters\n\n"
            "Character tokens are useful for teaching, but practical language systems often work with word or subword units.\n\n"
            "A tokenizer turns raw text into numeric token IDs through a pipeline such as:\n\n"
            "```text\n"
            "raw text\n"
            " -> normalization\n"
            " -> pre-tokenization\n"
            " -> tokenization model\n"
            " -> token IDs\n"
            "```\n\n"
            "The chapter demonstrates a word-level tokenizer using the Hugging Face `tokenizers` library and an `[UNK]` token for unseen vocabulary items.\n\n"
            "It also notes that alternative methods such as Byte Pair Encoding and WordPiece address limitations of simple word-level vocabularies.\n\n"
            "[[IMAGE_NEEDED: Tokenization pipeline | Raw sentence entering normalization and splitting, then tokens mapped into vocabulary IDs "
            "with an unknown-token fallback | Learner should notice that tokenizer design defines the units the Transformer actually receives]]\n\n"
            "---\n\n"

            "## 30. The same Transformer can generate word-level text\n\n"
            "One important abstraction in the source is that the Transformer mainly sees **token IDs**.\n\n"
            "Whether a token represents:\n\n"
            "- a character,\n"
            "- a word,\n"
            "- a subword,\n"
            "- or another discrete unit,\n\n"
            "the high-level Transformer mechanics remain similar.\n\n"
            "The chapter tokenizes *The Odyssey*, builds fixed-length input windows and one-token-shifted target windows, and trains the same decoder-style architecture to generate longer text.\n\n"
            "The generated output is imperfect, but it contains recognizable vocabulary and style from the training corpus—evidence that the model has learned statistical structure beyond isolated names.\n\n"
            "{{exercise:M09.L01.EX04}}\n\n"
            "---\n\n"

            "## 31. Vision Transformers: images can become token sequences too\n\n"
            "The Transformer is not inherently a text-only architecture.\n\n"
            "A Vision Transformer (ViT) divides an image into patches and treats each patch as a token-like unit.\n\n"
            "A simplified flow is:\n\n"
            "```text\n"
            "image\n"
            " -> fixed-size patches\n"
            " -> flatten/project each patch into an embedding\n"
            " -> prepend a learnable [CLS] token\n"
            " -> add positional embeddings\n"
            " -> Transformer encoder blocks\n"
            " -> use [CLS] representation for classification\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Vision Transformer patch pipeline | An image divided into a grid of patches; each patch flattened/projected into "
            "a token embedding, a CLS token prepended, positional embeddings added, then the sequence passed into Transformer encoder blocks | "
            "Learner should notice that image patches play the same structural role as sequence tokens]]\n\n"
            "For image classification, the `[CLS]` token can aggregate global information through self-attention and feed the final classification head.\n\n"
            "Other visual tasks may use more of the patch outputs rather than discarding them.\n\n"

            "### Learning checkpoint 5 — One architecture, many token types\n\n"
            "Explain why the following can all be modeled as sequences:\n\n"
            "- characters,\n"
            "- words/subwords,\n"
            "- image patches.\n\n"
            "The shared abstraction is not 'text'; it is **a sequence of token representations whose relationships can be modeled with attention**.\n\n"
            "---\n\n"

            "## 32. The complete mental model\n\n"
            "The chapter's full progression can be compressed into this chain:\n\n"
            "```text\n"
            "random token sampling\n"
            "    ↓\n"
            "bigram probabilities\n"
            "    ↓\n"
            "self-supervised next-token examples\n"
            "    ↓\n"
            "trainable token embeddings\n"
            "    ↓\n"
            "MLP language model\n"
            "    ↓\n"
            "self-attention with Q/K/V\n"
            "    ↓\n"
            "scaled causal self-attention\n"
            "    ↓\n"
            "multi-head attention\n"
            "    ↓\n"
            "residual + LayerNorm + MLP\n"
            "    ↓\n"
            "stacked Transformer decoder\n"
            "    ↓\n"
            "encoder / encoder-decoder variants\n"
            "    ↓\n"
            "different tokenization schemes\n"
            "    ↓\n"
            "text tokens or image-patch tokens\n"
            "```\n\n"
            "The most important insight is that modern Transformer systems are built from familiar ingredients—embeddings, linear layers, softmax, "
            "residual connections, normalization, and gradient descent—combined around the attention mechanism.\n\n"
            "{{exercise:M09.L01.EX05}}\n\n"
            "---\n\n"

            "## Important misconceptions\n\n"
            "### Misconception 1: Self-supervised learning means there is no target\n\n"
            "There is a target. The difference is that the target is automatically derived from the raw data, such as the next token in the same sequence.\n\n"
            "### Misconception 2: Token IDs are meaningful continuous numbers\n\n"
            "Token IDs are identifiers. Their numeric distance has no direct semantic meaning. Embeddings turn those IDs into learnable continuous representations.\n\n"
            "### Misconception 3: An embedding changes depending on context\n\n"
            "A normal embedding lookup gives the same base vector for the same token ID. Context-dependent representations emerge after contextual operations such as attention.\n\n"
            "### Misconception 4: Query, key, and value are three different input sequences in self-attention\n\n"
            "In self-attention they are learned projections of the same underlying sequence representation. In cross-attention, they can come from different sources.\n\n"
            "### Misconception 5: Causal masking is optional for autoregressive training\n\n"
            "Without a causal restriction, a position could use future tokens during training, creating information leakage that will not be available during generation.\n\n"
            "### Misconception 6: Softmax attention weights are the model's complete explanation\n\n"
            "Attention maps show one internal weighting operation, but they do not by themselves fully explain all information processing across layers and components.\n\n"
            "### Misconception 7: Transformers automatically know token order\n\n"
            "Position information must be supplied through positional embeddings or another positional mechanism.\n\n"
            "### Misconception 8: Decoder-only and encoder-only Transformers differ only in what we call them\n\n"
            "Causal masking changes information flow. Encoder-style attention can generally use both past and future context; autoregressive decoder self-attention blocks future positions.\n\n"
            "### Misconception 9: Transformers are only for NLP\n\n"
            "Anything represented as a useful token sequence can potentially use Transformer-style attention, including image patches in ViTs.\n\n"
            "---\n\n"

            "## Key terminology\n\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Vocabulary | Set of discrete tokens recognized by a model/tokenizer. |\n"
            "| Token | Basic discrete unit consumed or generated by a sequence model. |\n"
            "| Sequence | Ordered list of tokens. |\n"
            "| Special token | Token with a structural role such as boundary or unknown-token handling. |\n"
            "| Bigram | Pair of adjacent tokens used in a one-step context model. |\n"
            "| Self-supervised learning | Training where targets are derived automatically from the raw data. |\n"
            "| Data sparsity | Many possible discrete combinations are rarely or never observed. |\n"
            "| Embedding | Learned dense vector associated with a token/entity. |\n"
            "| Autoregressive generation | Generating one token at a time while feeding previous generated tokens back as context. |\n"
            "| Attention | Mechanism that computes weighted combinations of information based on learned relevance. |\n"
            "| Query | Projection representing what one position seeks. |\n"
            "| Key | Projection representing what one position offers for matching. |\n"
            "| Value | Content mixed according to attention weights. |\n"
            "| Self-attention | Attention where Q/K/V originate from the same sequence representation. |\n"
            "| Cross-attention | Attention where queries and key/value information originate from different sequences/sources. |\n"
            "| Causal mask | Restriction preventing an autoregressive position from using future tokens. |\n"
            "| Scaled dot-product attention | QKᵀ attention with score scaling, softmax, and weighted values. |\n"
            "| Attention head | One parallel attention subspace in multi-head attention. |\n"
            "| Multi-head attention | Multiple attention heads computed in parallel and merged. |\n"
            "| Positional embedding | Representation encoding sequence position. |\n"
            "| Layer normalization | Normalization across feature dimensions within a representation. |\n"
            "| Residual connection | Addition of a block input to its transformed output. |\n"
            "| Transformer block | Attention + residual/normalization + feed-forward processing unit. |\n"
            "| Decoder-only Transformer | Causally masked Transformer used for autoregressive generation. |\n"
            "| Encoder-only Transformer | Bidirectional Transformer representation model without decoder-style causal masking. |\n"
            "| Encoder-decoder Transformer | Architecture where a decoder also attends to representations produced by an encoder. |\n"
            "| Tokenizer | Component converting raw data such as text into token IDs and back. |\n"
            "| `[UNK]` | Special token representing vocabulary items unknown to a word-level tokenizer. |\n"
            "| Vision Transformer | Transformer architecture treating image patches as tokens. |\n"
            "| `[CLS]` token | Learnable token commonly used to aggregate a sequence representation for classification. |\n\n"
            "---\n\n"

            "## Self-check\n\n"
            "1. Why is generation naturally modeled with probability distributions?\n"
            "2. What are vocabulary, token, and sequence?\n"
            "3. Why does a uniform character distribution produce unrealistic names?\n"
            "4. What conditional probability does a bigram model estimate?\n"
            "5. Why is next-token prediction self-supervised?\n"
            "6. What causes data sparsity in n-gram tables?\n"
            "7. How are sequence targets created by shifting the input?\n"
            "8. Why are padded target values ignored in cross-entropy?\n"
            "9. What does `nn.Embedding` learn?\n"
            "10. Why can two identical token IDs retrieve identical base embeddings?\n"
            "11. What makes generation autoregressive?\n"
            "12. Why should generation use `model.eval()` and usually `torch.no_grad()`?\n"
            "13. What limitation of static embeddings motivates attention?\n"
            "14. What are Q, K, and V conceptually?\n"
            "15. How do `Q @ K.T` scores become attention weights?\n"
            "16. Why do attention weights sum to 1 along the attended dimension?\n"
            "17. Why is causal masking necessary for next-token generation?\n"
            "18. Why are attention logits divided by `sqrt(d_k)`?\n"
            "19. What does `F.scaled_dot_product_attention` replace from the manual implementation?\n"
            "20. Why can attention represent context more flexibly than flattened fixed prefixes?\n"
            "21. What does multi-head attention add over one attention head?\n"
            "22. Why must embedding dimension be divisible by number of heads in the chapter's implementation?\n"
            "23. Why do Transformers need positional information?\n"
            "24. What roles do residual connections and LayerNorm play in Transformer blocks?\n"
            "25. What shape does a decoder output need for next-token cross-entropy over a vocabulary?\n"
            "26. What is the core difference between encoder and decoder self-attention?\n"
            "27. What is cross-attention in an encoder-decoder Transformer?\n"
            "28. Why can the same architecture operate on character tokens or word tokens?\n"
            "29. What problem does an `[UNK]` token address in a simple word-level tokenizer?\n"
            "30. How does a Vision Transformer convert an image into a token sequence?\n"
            "31. What is the purpose of the `[CLS]` token in the chapter's ViT explanation?\n"
            "32. What single modeling objective connects the bigram model, MLP model, attention model, and decoder Transformer?\n\n"
            "---\n\n"

            "## Retain this idea\n\n"
            "**Transformers are not magic objects disconnected from earlier deep-learning concepts. They are built from familiar pieces—"
            "token embeddings, linear projections, softmax, residual connections, normalization, MLPs, and gradient-based learning—organized "
            "around attention so that each token representation can dynamically incorporate relevant context. The same next-token objective can "
            "grow from a tiny bigram model into a powerful autoregressive Transformer by progressively improving how context is represented.**\n"
        ),

        "estimated_minutes": 360,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "generation-problem", "title": "From prediction to generation", "order": 1},
            {"id": "latent-structure", "title": "Learning latent structure", "order": 2},
            {"id": "name-generation", "title": "Character-level name generation", "order": 3},
            {"id": "uniform-baseline", "title": "Uniform random baseline", "order": 4},
            {"id": "bigram", "title": "Bigram model", "order": 5},
            {"id": "self-supervised", "title": "Self-supervised next-token learning", "order": 6},
            {"id": "bigram-limits", "title": "Limits of lookup-table language models", "order": 7},
            {"id": "training-data", "title": "Generating training tensors", "order": 8},
            {"id": "embeddings", "title": "Learned token embeddings", "order": 9},
            {"id": "sequence-mlp", "title": "Embedding + MLP language model", "order": 10},
            {"id": "training-best-practices", "title": "Sequence-model training best practices", "order": 11},
            {"id": "autoregressive-generation", "title": "Autoregressive generation", "order": 12},
            {"id": "embedding-visualization", "title": "Visualizing learned embeddings", "order": 13},
            {"id": "why-attention", "title": "Why attention", "order": 14},
            {"id": "qkv", "title": "Query, key, and value", "order": 15},
            {"id": "dot-product-attention", "title": "Dot-product self-attention", "order": 16},
            {"id": "causal-attention", "title": "Causal masking", "order": 17},
            {"id": "scaled-attention", "title": "Scaled attention", "order": 18},
            {"id": "pytorch-attention", "title": "PyTorch optimized attention", "order": 19},
            {"id": "attention-model", "title": "Attention-based sequence model", "order": 20},
            {"id": "transformer", "title": "From attention to Transformers", "order": 21},
            {"id": "multihead", "title": "Multi-head attention", "order": 22},
            {"id": "positional-embeddings", "title": "Positional embeddings", "order": 23},
            {"id": "residual-layernorm", "title": "Residual connections and LayerNorm", "order": 24},
            {"id": "transformer-block", "title": "GPT-style Transformer block", "order": 25},
            {"id": "decoder-model", "title": "Decoder language model", "order": 26},
            {"id": "encoder", "title": "Encoder-only Transformers", "order": 27},
            {"id": "encoder-decoder", "title": "Encoder-decoder Transformers", "order": 28},
            {"id": "tokenization", "title": "Tokenization", "order": 29},
            {"id": "word-generation", "title": "Generating word-level text", "order": 30},
            {"id": "vision-transformer", "title": "Vision Transformers", "order": 31},
            {"id": "complete-transformer-mental-model", "title": "Complete Transformer mental model", "order": 32},
        ],
    },

    "exercises": [
        {
            "id": "M09.L01.EX01",
            "title": "Build Self-Supervised Next-Token Training Data",
            "lesson_code": "M09.L01",
            "section_id": "training-best-practices",
            "placement": "after_section",
            "description": (
                "Turn variable-length character sequences into padded next-token training tensors and train one clean optimization step."
            ),
            "instructions": (
                "Use a tiny list such as `['ada', 'mona', 'ali']` and a character vocabulary with a boundary token.\n"
                "1. Encode each name as integer IDs with start/end boundaries.\n"
                "2. Construct shifted next-token targets.\n"
                "3. Pad inputs with the boundary/pad value and targets with `-1`.\n"
                "4. Build a small embedding + MLP model.\n"
                "5. Run one training step using `model.train()`, device-consistent tensors, "
                "`optimizer.zero_grad(set_to_none=True)`, cross-entropy with `ignore_index=-1`, backward, and step.\n"
                "6. Print the tensor shapes and explain which positions contribute to loss."
            ),
            "expected_output": (
                "Encoded/padded input and target tensors, one working training step, and an explanation of self-supervised targets."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "self-supervised-learning",
                "padding",
                "next-token-prediction",
                "cross-entropy",
                "training-loop",
            ],
        },
        {
            "id": "M09.L01.EX02",
            "title": "Implement Causal Self-Attention by Hand",
            "lesson_code": "M09.L01",
            "section_id": "dot-product-attention",
            "placement": "after_section",
            "description": "Implement the core attention math and inspect its matrices.",
            "instructions": (
                "Create a tensor `x` shaped `(1, 4, 8)` and three learned or random linear projections for Q, K, and V.\n"
                "1. Compute `Q @ K.transpose(-2, -1)`.\n"
                "2. Divide by `sqrt(d_k)`.\n"
                "3. Build a lower-triangular causal mask.\n"
                "4. Fill forbidden future positions with `-inf`.\n"
                "5. Apply softmax along the last dimension.\n"
                "6. Multiply the attention weights by V.\n"
                "7. Verify that each attention row sums to approximately 1.\n"
                "8. Compare your output with `F.scaled_dot_product_attention(..., is_causal=True)` using `torch.allclose`."
            ),
            "expected_output": (
                "Working causal-attention code, score/weight/output shapes, row-sum checks, and equivalence verification."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "query-key-value",
                "causal-mask",
                "scaled-dot-product-attention",
                "matrix-multiplication",
            ],
        },
        {
            "id": "M09.L01.EX03",
            "title": "Trace a Multi-Head Transformer Block",
            "lesson_code": "M09.L01",
            "section_id": "transformer-block",
            "placement": "after_section",
            "description": "Practice the shape transformations inside a decoder block.",
            "instructions": (
                "Use batch size `B=2`, sequence length `T=6`, embedding size `D=32`, and `H=4` heads.\n"
                "1. State `D_head`.\n"
                "2. Start with an input tensor `(2,6,32)`.\n"
                "3. Project Q/K/V.\n"
                "4. Reshape each to `(B,H,T,D_head)`.\n"
                "5. Apply causal scaled dot-product attention.\n"
                "6. Merge the heads back to `(B,T,D)`.\n"
                "7. Apply one residual addition and LayerNorm.\n"
                "8. Pass through an MLP that returns dimension `D`, add the second residual, and normalize.\n"
                "9. Print every shape and explain why residual additions require matching dimensions."
            ),
            "expected_output": (
                "A working Transformer-block trace with all intermediate shapes and residual-shape reasoning."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "multi-head-attention",
                "tensor-shapes",
                "layer-normalization",
                "residual-connections",
            ],
        },
        {
            "id": "M09.L01.EX04",
            "title": "Compare Tokenization Granularities",
            "lesson_code": "M09.L01",
            "section_id": "word-generation",
            "placement": "after_section",
            "description": "Reason about character-, word-, and subword-level tokenization.",
            "instructions": (
                "Take a short paragraph containing common words, punctuation, one rare name, and one invented word.\n"
                "1. Tokenize it at the character level.\n"
                "2. Create a simple whitespace word-level vocabulary and encode it with an `[UNK]` fallback.\n"
                "3. Identify which information each method preserves well and where it becomes inefficient.\n"
                "4. Explain why subword approaches such as BPE can provide a compromise between tiny character vocabularies "
                "and brittle word-level vocabularies.\n"
                "5. Estimate how the sequence length and vocabulary size change under each approach."
            ),
            "expected_output": (
                "Three tokenization analyses with token sequences, vocabulary/length comparisons, and trade-off discussion."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "tokenization",
                "vocabulary",
                "unknown-token",
                "subwords",
            ],
        },
        {
            "id": "M09.L01.EX05",
            "title": "Transformer Architecture Decision Map",
            "lesson_code": "M09.L01",
            "section_id": "complete-transformer-mental-model",
            "placement": "after_section",
            "description": (
                "Connect decoder-only, encoder-only, encoder-decoder, and Vision Transformer designs to their information-flow requirements."
            ),
            "instructions": (
                "For each task below, choose the most conceptually appropriate architecture family from the chapter and justify the choice:\n"
                "1. generate the continuation of a text prompt,\n"
                "2. classify a review as positive or negative,\n"
                "3. translate an English sentence into another language,\n"
                "4. classify an image using patch tokens.\n"
                "For each case, state whether causal masking is needed, where positional information is required, "
                "and whether self-attention or cross-attention is involved."
            ),
            "expected_output": (
                "A four-row comparison table covering architecture, masking, positional information, and attention type."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "decoder",
                "encoder",
                "encoder-decoder",
                "vision-transformer",
                "cross-attention",
            ],
        },
    ],

    "quiz": {
        "id": "M09.L01.QZ01",
        "title": "How Transformers Work — Knowledge Check",
        "lesson_code": "M09.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M09.L01.Q01",
                "section_id": "name-generation",
                "question": "What is a token in the chapter's language-modeling setup?",
                "options": [
                    "A gradient stored by the optimizer.",
                    "A discrete vocabulary element represented for model input/output.",
                    "A complete neural-network layer.",
                    "The final loss value after training.",
                ],
                "correct": 1,
                "explanation": "Tokens are the discrete units that make up model sequences.",
            },
            {
                "id": "M09.L01.Q02",
                "section_id": "bigram",
                "question": "What does a bigram model primarily estimate?",
                "options": [
                    "The probability of an entire dataset.",
                    "The embedding dimension needed for every token.",
                    "The number of attention heads.",
                    "The probability of a next token conditioned on the previous token.",
                ],
                "correct": 3,
                "explanation": "A bigram model uses one preceding token as its context.",
            },
            {
                "id": "M09.L01.Q03",
                "section_id": "self-supervised",
                "question": "Why is next-token prediction self-supervised in this chapter?",
                "options": [
                    "The target token is derived directly from the raw sequence itself.",
                    "The model trains without any loss function.",
                    "A human labels every token position.",
                    "Only validation data is used for learning.",
                ],
                "correct": 0,
                "explanation": "The next token already present in the sequence provides the training target automatically.",
            },
            {
                "id": "M09.L01.Q04",
                "section_id": "bigram-limits",
                "question": "What problem appears when n-gram tables grow across large vocabularies and long contexts?",
                "options": [
                    "Every possible sequence occurs equally often.",
                    "Embeddings become impossible to differentiate.",
                    "The number of possible combinations grows rapidly and many remain rare or unseen.",
                    "Softmax can no longer produce probabilities.",
                ],
                "correct": 2,
                "explanation": "Combinatorial growth creates severe sparsity in explicit lookup-table probability models.",
            },
            {
                "id": "M09.L01.Q05",
                "section_id": "embeddings",
                "question": "What does `nn.Embedding(vocab_size, embedding_dim)` learn?",
                "options": [
                    "A causal mask for every sequence.",
                    "A dense vector associated with each vocabulary index.",
                    "One probability table per training example.",
                    "The batch size.",
                ],
                "correct": 1,
                "explanation": "An embedding layer is a trainable lookup table from token IDs to dense vectors.",
            },
            {
                "id": "M09.L01.Q06",
                "section_id": "autoregressive-generation",
                "question": "What makes generation autoregressive?",
                "options": [
                    "The model predicts all future tokens without using prior outputs.",
                    "The optimizer changes after each token.",
                    "Only one embedding dimension is used.",
                    "Previously generated tokens are fed back as context for later predictions.",
                ],
                "correct": 3,
                "explanation": "Autoregressive generation builds the sequence one token at a time using its own earlier outputs.",
            },
            {
                "id": "M09.L01.Q07",
                "section_id": "qkv",
                "question": "Which attention component contains the content that is actually mixed into the output?",
                "options": [
                    "Query",
                    "Key",
                    "Value",
                    "Mask",
                ],
                "correct": 2,
                "explanation": "Queries and keys determine relevance; values are combined according to those relevance weights.",
            },
            {
                "id": "M09.L01.Q08",
                "section_id": "dot-product-attention",
                "question": "What does `Q @ K.T` produce in simple self-attention?",
                "options": [
                    "Pairwise similarity scores between query and key positions.",
                    "The final token IDs.",
                    "A batch-normalization statistic.",
                    "The vocabulary itself.",
                ],
                "correct": 0,
                "explanation": "The matrix contains attention compatibility scores between positions.",
            },
            {
                "id": "M09.L01.Q09",
                "section_id": "causal-attention",
                "question": "Why are future attention positions filled with `-inf` before softmax?",
                "options": [
                    "To make future tokens more likely.",
                    "To increase the embedding dimension.",
                    "To force every row to have identical values.",
                    "So future positions receive zero probability after softmax.",
                ],
                "correct": 3,
                "explanation": "The causal mask prevents information leakage from future tokens.",
            },
            {
                "id": "M09.L01.Q10",
                "section_id": "scaled-attention",
                "question": "Why divide attention dot products by `sqrt(d_k)`?",
                "options": [
                    "To convert token IDs into words.",
                    "To control score magnitude before softmax and improve numerical/training behavior.",
                    "To remove the causal mask.",
                    "To change the batch size.",
                ],
                "correct": 1,
                "explanation": "Scaling keeps dot-product magnitudes better behaved as vector dimension grows.",
            },
            {
                "id": "M09.L01.Q11",
                "section_id": "multihead",
                "question": "What is the main idea of multi-head attention?",
                "options": [
                    "Compute several attention subspaces in parallel and combine their outputs.",
                    "Use a separate dataset for every token.",
                    "Run the same attention output multiple times without new parameters.",
                    "Replace positional embeddings with batch normalization.",
                ],
                "correct": 0,
                "explanation": "Different heads can learn different relationship patterns over the same sequence.",
            },
            {
                "id": "M09.L01.Q12",
                "section_id": "positional-embeddings",
                "question": "Why add positional embeddings to token embeddings?",
                "options": [
                    "To create target labels.",
                    "To reduce vocabulary size.",
                    "To provide sequence-order information that token identity alone does not supply.",
                    "To disable attention between tokens.",
                ],
                "correct": 2,
                "explanation": "Position information lets the Transformer distinguish where tokens occur in the sequence.",
            },
            {
                "id": "M09.L01.Q13",
                "section_id": "encoder",
                "question": "What most directly distinguishes ordinary encoder self-attention from an autoregressive decoder's self-attention?",
                "options": [
                    "Encoders never use embeddings.",
                    "Encoder attention is generally not causally masked and can use context from both directions.",
                    "Decoders cannot use residual connections.",
                    "Encoders cannot contain MLP layers.",
                ],
                "correct": 1,
                "explanation": "The decoder's causal mask blocks future positions; encoder attention can normally use the full sequence.",
            },
            {
                "id": "M09.L01.Q14",
                "section_id": "encoder-decoder",
                "question": "In encoder-decoder cross-attention, where do the decoder's keys and values come from conceptually?",
                "options": [
                    "Only from positional embeddings.",
                    "From the optimizer state.",
                    "From the tokenizer vocabulary table.",
                    "From representations produced by the encoder.",
                ],
                "correct": 3,
                "explanation": "Decoder queries attend to key/value information supplied by encoder outputs.",
            },
            {
                "id": "M09.L01.Q15",
                "section_id": "vision-transformer",
                "question": "How does a Vision Transformer turn an image into a Transformer-compatible sequence?",
                "options": [
                    "It treats every RGB channel as one complete sentence.",
                    "It converts the whole image into one scalar token.",
                    "It divides the image into patches and embeds the patches as tokens.",
                    "It first converts the image into character strings.",
                ],
                "correct": 2,
                "explanation": "ViTs represent fixed-size image patches as token embeddings before Transformer encoding.",
            },
            {
                "id": "M09.L01.Q16",
                "section_id": "complete-transformer-mental-model",
                "type": "open",
                "question": (
                    "Explain the conceptual progression from a bigram model to a decoder-only Transformer. "
                    "Your answer should identify what each major step adds: embeddings, self-attention, causal masking, "
                    "multi-head attention, positional information, residual connections, LayerNorm, and stacked blocks."
                ),
            },
        ],
        "passing_score": 70,
    },
}
