"""M01.L02 — Transformer Anatomy.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
BOOK-004, Chapter 3.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L02"
MODULE_ORDER = 3
MODULE_TITLE = "Transformer Internals for Applied NLP"
MODULE_DESCRIPTION = (
    "Build an intuitive and practical understanding of transformer internals: "
    "self-attention, multi-head attention, feed-forward layers, normalization, "
    "positional embeddings, encoder/decoder differences, and model families."
)

SOURCE_CHAPTER = 3
SOURCE_PAGES = "Chapter 3"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Transformer Anatomy",
    "slug": "applied-nlp-transformers-m01-l02-transformer-anatomy",
    "description": (
        "Understand how a transformer turns tokens into contextual representations, "
        "implement the core attention operations in PyTorch, assemble a simple encoder, "
        "and distinguish encoder-only, decoder-only, and encoder-decoder models."
    ),
    "order": 2,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 1.75,
    "skill_tags": [
        "transformers",
        "self-attention",
        "multi-head-attention",
        "pytorch",
        "encoder",
        "decoder",
        "positional-embeddings",
        "nlp",
    ],
    "prerequisite_ids": ["M01.L01"],

    "lesson": {
        "title": "Transformer Anatomy",

        "content": (
            "# Transformer Anatomy\n"
            "\n"
            "> **Course:** Applied NLP with Transformers  \n"
            "> **Lesson:** M01.L02  \n"
            "> **Module:** Transformer Foundations  \n"
            "> **Source alignment:** BOOK-004, Chapter 3. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain the roles of the transformer encoder and decoder.\n"
            "- Distinguish encoder-only, decoder-only, and encoder-decoder models.\n"
            "- Explain self-attention using contextualized token representations.\n"
            "- Describe query, key, and value vectors without treating them as magic.\n"
            "- Implement simplified scaled dot-product attention in PyTorch.\n"
            "- Explain why transformers use multiple attention heads.\n"
            "- Describe feed-forward layers, skip connections, and layer normalization.\n"
            "- Explain why positional information must be added to token embeddings.\n"
            "- Describe causal masking in a transformer decoder.\n"
            "- Connect common transformer families to their architectural branch.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. The transformer at a glance\n"
            "\n"
            "A transformer is easier to understand when you stop thinking of it as "
            "one enormous neural network and instead see it as a stack of repeated "
            "building blocks.\n"
            "\n"
            "The original Transformer has two major parts:\n"
            "\n"
            "- **Encoder:** reads the input sequence and produces a contextual vector "
            "for every input token.\n"
            "- **Decoder:** uses those representations, together with the tokens it has "
            "already generated, to predict the next output token.\n"
            "\n"
            "For a translation system, the encoder can read the complete source sentence. "
            "The decoder then generates the translated sentence one token at a time until "
            "it produces an end-of-sequence token or reaches a length limit.\n"
            "\n"
            "### Three common transformer families\n"
            "\n"
            "| Architecture | Main behavior | Typical uses | Examples from the chapter |\n"
            "|---|---|---|---|\n"
            "| Encoder-only | Reads the whole input context | Classification, NER, extractive QA | BERT, RoBERTa, DistilBERT |\n"
            "| Decoder-only | Predicts the next token from previous tokens | Text generation | GPT family |\n"
            "| Encoder-decoder | Maps one sequence to another | Translation, summarization | T5, BART |\n"
            "\n"
            "The important distinction is the **attention pattern**. Encoder representations "
            "can normally use context from both sides of a token. Decoder generation must "
            "prevent a position from seeing future tokens.\n"
            "\n"
            '{{image:transformer-encoder-decoder-overview}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 2. What happens inside an encoder layer?\n"
            "\n"
            "A transformer encoder is a stack of nearly identical encoder layers. Each "
            "layer receives one vector per token and returns one vector per token with the "
            "same hidden size.\n"
            "\n"
            "The layer has two major computational sublayers:\n"
            "\n"
            "1. **Multi-head self-attention** — lets each token gather information from "
            "other tokens in the sequence.\n"
            "2. **Position-wise feed-forward network** — transforms each token representation "
            "independently after attention has mixed contextual information.\n"
            "\n"
            "Skip connections and layer normalization are wrapped around these operations to "
            "make deep networks easier to train.\n"
            "\n"
            "### A useful mental model\n"
            "\n"
            "Imagine the token `apple` entering the encoder. Before attention, its embedding "
            "does not yet know whether the sentence is talking about fruit or a technology "
            "company. After attention mixes information from nearby words such as `phone`, "
            "`keynote`, or `orchard`, the representation can become context-specific.\n"
            "\n"
            "[[IMAGE_NEEDED: Transformer encoder layer zoom | "
            "One encoder block showing multi-head self-attention, residual connection, layer "
            "normalization, feed-forward network, and the second residual/normalization path | "
            "Learner should notice that attention and the feed-forward network are separate "
            "stages and that the hidden dimension is preserved across the block]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Self-attention: turning fixed embeddings into contextual embeddings\n"
            "\n"
            "Token embeddings begin as lookup-table representations. That means the same token "
            "ID starts with the same vector wherever it appears. But language is contextual.\n"
            "\n"
            "Consider the word **flies**:\n"
            "\n"
            "- `time flies like an arrow`\n"
            "- `fruit flies like a banana`\n"
            "\n"
            "The token spelling is the same, but its role and meaning differ. Self-attention "
            "solves this by allowing the representation of each token to become a weighted "
            "combination of information from the other tokens in the same sequence.\n"
            "\n"
            "A token that is being updated does not treat every other token equally. It learns "
            "attention weights that say, roughly, **how much information should I collect from "
            "this position?**\n"
            "\n"
            "So self-attention can be viewed as a learned weighted averaging operation. The "
            "result is a **contextualized embedding**.\n"
            "\n"
            "[[IMAGE_NEEDED: Contextualized meaning of flies | "
            "Two short sentences containing the word 'flies', with attention links from "
            "'flies' to context words such as 'time' and 'arrow' in one sentence and 'fruit' "
            "and 'banana' in the other | "
            "Learner should notice that the same token can receive different contextual "
            "representations depending on surrounding words]]\n"
            "\n"
            "### Why attention matters\n"
            "\n"
            "Without contextual mixing, a token representation is mostly a static identity. "
            "With self-attention, it becomes a representation of the token **in this sentence**.\n"
            "\n"
            "{{exercise:M01.L02.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Queries, keys, and values without the mystery\n"
            "\n"
            "Every token embedding is projected into three learned vectors:\n"
            "\n"
            "- **Query (Q):** what information this position is looking for.\n"
            "- **Key (K):** what information this position advertises for matching.\n"
            "- **Value (V):** the information this position can contribute if attended to.\n"
            "\n"
            "A useful analogy is information retrieval. A query is like a search request, keys "
            "are the searchable labels, and values are the content returned after good matches "
            "are found.\n"
            "\n"
            "The analogy is imperfect because self-attention is soft: every key can contribute "
            "to some degree rather than producing a single exact match.\n"
            "\n"
            "### Scaled dot-product attention\n"
            "\n"
            "The common computation follows four steps:\n"
            "\n"
            "1. Project token embeddings into Q, K, and V vectors.\n"
            "2. Compare queries with keys using dot products.\n"
            "3. Scale the scores and apply softmax to obtain normalized attention weights.\n"
            "4. Use those weights to combine the value vectors.\n"
            "\n"
            "A compact mathematical form is:\n"
            "\n"
            "```text\n"
            "Attention(Q, K, V) = softmax(QK^T / sqrt(d_k)) V\n"
            "```\n"
            "\n"
            "The division by `sqrt(d_k)` keeps dot-product magnitudes under control as the "
            "vector dimension grows. Softmax then turns the scores into normalized weights.\n"
            "\n"
            "[[IMAGE_NEEDED: Scaled dot-product attention pipeline | "
            "A left-to-right diagram with Q and K entering a dot product, division by sqrt(d_k), "
            "softmax producing attention weights, and multiplication with V producing the output | "
            "Learner should notice that Q and K determine relevance while V supplies the "
            "information that is actually aggregated]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Build simplified self-attention in PyTorch\n"
            "\n"
            "Let us implement the chapter's simplified version step by step. We will use the "
            "same tensor shape convention throughout:\n"
            "\n"
            "```text\n"
            "[batch_size, sequence_length, hidden_dimension]\n"
            "```\n"
            "\n"
            "Suppose token embeddings have shape `[1, 5, 768]`. If we temporarily use the same "
            "tensor for Q, K, and V, the attention score matrix becomes `[1, 5, 5]`: every "
            "token is compared with every token.\n"
            "\n"
            "```python\n"
            "import torch\n"
            "import torch.nn.functional as F\n"
            "from math import sqrt\n"
            "\n"
            "def scaled_dot_product_attention(query, key, value, mask=None):\n"
            "    dim_k = query.size(-1)\n"
            "    scores = torch.bmm(query, key.transpose(1, 2)) / sqrt(dim_k)\n"
            "\n"
            "    if mask is not None:\n"
            "        scores = scores.masked_fill(mask == 0, float('-inf'))\n"
            "\n"
            "    weights = F.softmax(scores, dim=-1)\n"
            "    return torch.bmm(weights, value)\n"
            "```\n"
            "\n"
            "### Read the code line by line\n"
            "\n"
            "- `key.transpose(1, 2)` changes the last two dimensions so each query can be "
            "compared with all keys.\n"
            "- `torch.bmm()` performs matrix multiplication independently for every example "
            "in the batch.\n"
            "- dividing by `sqrt(dim_k)` stabilizes the score scale.\n"
            "- `softmax(..., dim=-1)` converts each row of scores into weights that sum to 1.\n"
            "- multiplying the weights by `value` produces the updated token representations.\n"
            "\n"
            "This is the core idea behind attention: **compare, normalize, combine**.\n"
            "\n"
            "### Shape check\n"
            "\n"
            "For five tokens:\n"
            "\n"
            "```text\n"
            "Q:       [1, 5, 768]\n"
            "K:       [1, 5, 768]\n"
            "scores:  [1, 5,   5]\n"
            "weights: [1, 5,   5]\n"
            "V:       [1, 5, 768]\n"
            "output:  [1, 5, 768]\n"
            "```\n"
            "\n"
            "The sequence still has five positions, and each output position still has a "
            "768-dimensional vector, but those vectors now contain mixed context.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Why multi-head attention?\n"
            "\n"
            "One attention distribution tends to emphasize one pattern at a time. A transformer "
            "therefore learns several attention heads in parallel.\n"
            "\n"
            "Each head has its own learned Q, K, and V projections. This allows different heads "
            "to capture different relationships. One head may become useful for nearby modifiers, "
            "another for long-distance grammatical relationships, and another for a different "
            "semantic pattern. These roles are learned rather than manually assigned.\n"
            "\n"
            "### One attention head\n"
            "\n"
            "```python\n"
            "from torch import nn\n"
            "\n"
            "class AttentionHead(nn.Module):\n"
            "    def __init__(self, embed_dim, head_dim):\n"
            "        super().__init__()\n"
            "        self.q = nn.Linear(embed_dim, head_dim)\n"
            "        self.k = nn.Linear(embed_dim, head_dim)\n"
            "        self.v = nn.Linear(embed_dim, head_dim)\n"
            "\n"
            "    def forward(self, hidden_state):\n"
            "        return scaled_dot_product_attention(\n"
            "            self.q(hidden_state),\n"
            "            self.k(hidden_state),\n"
            "            self.v(hidden_state),\n"
            "        )\n"
            "```\n"
            "\n"
            "### Combine several heads\n"
            "\n"
            "```python\n"
            "class MultiHeadAttention(nn.Module):\n"
            "    def __init__(self, config):\n"
            "        super().__init__()\n"
            "        embed_dim = config.hidden_size\n"
            "        num_heads = config.num_attention_heads\n"
            "        head_dim = embed_dim // num_heads\n"
            "\n"
            "        self.heads = nn.ModuleList([\n"
            "            AttentionHead(embed_dim, head_dim)\n"
            "            for _ in range(num_heads)\n"
            "        ])\n"
            "        self.output_linear = nn.Linear(embed_dim, embed_dim)\n"
            "\n"
            "    def forward(self, hidden_state):\n"
            "        x = torch.cat([h(hidden_state) for h in self.heads], dim=-1)\n"
            "        return self.output_linear(x)\n"
            "```\n"
            "\n"
            "The head outputs are concatenated and passed through a final linear layer so the "
            "result returns to the model's hidden dimension.\n"
            "\n"
            "[[IMAGE_NEEDED: Multi-head attention | "
            "One input sequence splitting into several parallel attention heads, each with its "
            "own Q/K/V projections, followed by concatenation and a final linear projection | "
            "Learner should notice that heads process the same sequence in parallel but can "
            "learn different attention patterns]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Feed-forward networks, residual paths, and layer normalization\n"
            "\n"
            "Attention mixes information **between positions**. The feed-forward network then "
            "transforms each token representation independently.\n"
            "\n"
            "A typical transformer feed-forward block contains two linear layers with a "
            "nonlinear activation such as GELU between them. The intermediate layer is usually "
            "larger than the hidden dimension.\n"
            "\n"
            "```python\n"
            "class FeedForward(nn.Module):\n"
            "    def __init__(self, config):\n"
            "        super().__init__()\n"
            "        self.linear_1 = nn.Linear(config.hidden_size, config.intermediate_size)\n"
            "        self.linear_2 = nn.Linear(config.intermediate_size, config.hidden_size)\n"
            "        self.gelu = nn.GELU()\n"
            "        self.dropout = nn.Dropout(config.hidden_dropout_prob)\n"
            "\n"
            "    def forward(self, x):\n"
            "        x = self.linear_1(x)\n"
            "        x = self.gelu(x)\n"
            "        x = self.linear_2(x)\n"
            "        return self.dropout(x)\n"
            "```\n"
            "\n"
            "### Skip connections\n"
            "\n"
            "Instead of replacing the old representation completely, a residual or skip "
            "connection adds the sublayer's result back to its input:\n"
            "\n"
            "```text\n"
            "new_x = x + sublayer(x)\n"
            "```\n"
            "\n"
            "This creates a direct path for information and gradients through a deep network.\n"
            "\n"
            "### Pre-norm versus post-norm\n"
            "\n"
            "The original Transformer used a post-normalization arrangement. The chapter also "
            "describes pre-normalization, where normalization is applied before attention or "
            "the feed-forward sublayer. The latter is commonly used because it tends to make "
            "training more stable.\n"
            "\n"
            "A pre-norm encoder layer can look like this:\n"
            "\n"
            "```python\n"
            "class TransformerEncoderLayer(nn.Module):\n"
            "    def __init__(self, config):\n"
            "        super().__init__()\n"
            "        self.layer_norm_1 = nn.LayerNorm(config.hidden_size)\n"
            "        self.layer_norm_2 = nn.LayerNorm(config.hidden_size)\n"
            "        self.attention = MultiHeadAttention(config)\n"
            "        self.feed_forward = FeedForward(config)\n"
            "\n"
            "    def forward(self, x):\n"
            "        hidden_state = self.layer_norm_1(x)\n"
            "        x = x + self.attention(hidden_state)\n"
            "        x = x + self.feed_forward(self.layer_norm_2(x))\n"
            "        return x\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Pre-norm versus post-norm | "
            "Side-by-side encoder-block diagrams showing where layer normalization sits relative "
            "to the residual connection in pre-norm and post-norm arrangements | "
            "Learner should focus on the ordering difference rather than memorizing every arrow]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Why transformers need positional information\n"
            "\n"
            "Self-attention can compare every token with every other token, but by itself it "
            "does not know that token 1 came before token 2. A weighted set operation has no "
            "built-in notion of sequence order.\n"
            "\n"
            "Transformers therefore inject positional information into the token representations.\n"
            "\n"
            "A straightforward implementation learns a position embedding for each position and "
            "adds it to the token embedding:\n"
            "\n"
            "```text\n"
            "final_input_embedding = token_embedding + position_embedding\n"
            "```\n"
            "\n"
            "### Learnable positional embeddings\n"
            "\n"
            "```python\n"
            "class Embeddings(nn.Module):\n"
            "    def __init__(self, config):\n"
            "        super().__init__()\n"
            "        self.token_embeddings = nn.Embedding(\n"
            "            config.vocab_size, config.hidden_size\n"
            "        )\n"
            "        self.position_embeddings = nn.Embedding(\n"
            "            config.max_position_embeddings, config.hidden_size\n"
            "        )\n"
            "        self.layer_norm = nn.LayerNorm(config.hidden_size, eps=1e-12)\n"
            "        self.dropout = nn.Dropout()\n"
            "\n"
            "    def forward(self, input_ids):\n"
            "        seq_length = input_ids.size(1)\n"
            "        position_ids = torch.arange(seq_length).unsqueeze(0)\n"
            "\n"
            "        token_embeddings = self.token_embeddings(input_ids)\n"
            "        position_embeddings = self.position_embeddings(position_ids)\n"
            "\n"
            "        x = token_embeddings + position_embeddings\n"
            "        x = self.layer_norm(x)\n"
            "        return self.dropout(x)\n"
            "```\n"
            "\n"
            "The chapter also discusses alternatives:\n"
            "\n"
            "- **Absolute positional representations:** encode each absolute location.\n"
            "- **Relative positional representations:** encode the distance or relationship "
            "between token positions and modify attention accordingly.\n"
            "\n"
            "[[IMAGE_NEEDED: Token plus position embeddings | "
            "A sequence showing token embeddings and position embeddings being added element-wise "
            "before entering the encoder stack | "
            "Learner should notice that attention receives both token identity information and "
            "sequence-order information]]\n"
            "\n"
            "{{exercise:M01.L02.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Assemble the encoder and attach a classification head\n"
            "\n"
            "At this point we have the major ingredients required for a simple encoder:\n"
            "\n"
            "1. token + position embeddings,\n"
            "2. repeated encoder layers,\n"
            "3. contextual hidden states for every token.\n"
            "\n"
            "```python\n"
            "class TransformerEncoder(nn.Module):\n"
            "    def __init__(self, config):\n"
            "        super().__init__()\n"
            "        self.embeddings = Embeddings(config)\n"
            "        self.layers = nn.ModuleList([\n"
            "            TransformerEncoderLayer(config)\n"
            "            for _ in range(config.num_hidden_layers)\n"
            "        ])\n"
            "\n"
            "    def forward(self, input_ids):\n"
            "        x = self.embeddings(input_ids)\n"
            "        for layer in self.layers:\n"
            "            x = layer(x)\n"
            "        return x\n"
            "```\n"
            "\n"
            "The result is one contextual hidden state per token. That body can then be adapted "
            "to a downstream task by attaching a task-specific head.\n"
            "\n"
            "For sequence classification, the chapter demonstrates using the hidden state at "
            "the first token position and feeding it into a linear classifier:\n"
            "\n"
            "```python\n"
            "class TransformerForSequenceClassification(nn.Module):\n"
            "    def __init__(self, config):\n"
            "        super().__init__()\n"
            "        self.encoder = TransformerEncoder(config)\n"
            "        self.dropout = nn.Dropout(config.hidden_dropout_prob)\n"
            "        self.classifier = nn.Linear(config.hidden_size, config.num_labels)\n"
            "\n"
            "    def forward(self, input_ids):\n"
            "        x = self.encoder(input_ids)[:, 0, :]\n"
            "        x = self.dropout(x)\n"
            "        return self.classifier(x)\n"
            "```\n"
            "\n"
            "This illustrates a recurring transformer design pattern:\n"
            "\n"
            "```text\n"
            "task-independent pretrained body + task-specific head\n"
            "```\n"
            "\n"
            "---\n"
            "\n"

            "## 10. What changes in the decoder?\n"
            "\n"
            "The decoder resembles the encoder, but it must solve an additional problem: during "
            "next-token prediction it must not look at future target tokens.\n"
            "\n"
            "A decoder layer therefore includes:\n"
            "\n"
            "- **masked multi-head self-attention**, and\n"
            "- in an encoder-decoder transformer, **encoder-decoder attention**.\n"
            "\n"
            "### Causal masking\n"
            "\n"
            "Suppose we have five target positions. A lower-triangular mask is:\n"
            "\n"
            "```text\n"
            "1 0 0 0 0\n"
            "1 1 0 0 0\n"
            "1 1 1 0 0\n"
            "1 1 1 1 0\n"
            "1 1 1 1 1\n"
            "```\n"
            "\n"
            "Position 3 can use positions 1, 2, and 3, but it cannot inspect positions 4 or 5.\n"
            "\n"
            "In code, masked positions can be replaced with negative infinity before softmax:\n"
            "\n"
            "```python\n"
            "scores = scores.masked_fill(mask == 0, float('-inf'))\n"
            "weights = F.softmax(scores, dim=-1)\n"
            "```\n"
            "\n"
            "After softmax, those masked locations receive zero attention weight.\n"
            "\n"
            "### Encoder-decoder attention\n"
            "\n"
            "In cross-attention, the decoder provides the **queries**, while the encoder output "
            "provides the **keys and values**. This lets the decoder decide which source tokens "
            "are relevant while generating each target token.\n"
            "\n"
            "[[IMAGE_NEEDED: Transformer decoder with causal mask | "
            "A decoder layer showing masked self-attention first and encoder-decoder attention "
            "second, plus a small triangular attention mask | "
            "Learner should notice that self-attention cannot see future target positions while "
            "cross-attention can read encoder outputs]]\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Meet the transformer families\n"
            "\n"
            "Once you understand the three architecture branches, the large collection of model "
            "names becomes easier to organize.\n"
            "\n"
            "### Encoder branch\n"
            "\n"
            "- **BERT:** encoder-only model trained with masked-token prediction and a next-"
            "sentence objective in the chapter's description.\n"
            "- **DistilBERT:** a smaller BERT-family model created using knowledge distillation.\n"
            "- **RoBERTa:** modifies BERT's pretraining recipe, including removing the next-"
            "sentence objective.\n"
            "- **XLM / XLM-R:** multilingual encoder approaches.\n"
            "- **ALBERT:** reduces parameter usage through factorization and parameter sharing.\n"
            "- **ELECTRA:** trains a discriminator to detect replaced tokens rather than only "
            "predicting masked tokens.\n"
            "- **DeBERTa:** separates content and relative-position information in attention.\n"
            "\n"
            "### Decoder branch\n"
            "\n"
            "- **GPT:** combines a transformer decoder with language-model pretraining.\n"
            "- **GPT-2:** scales the approach and generates longer coherent sequences.\n"
            "- **CTRL:** introduces control tokens to influence generated text style.\n"
            "- **GPT-3:** demonstrates strong few-shot behavior at much larger scale.\n"
            "- **GPT-Neo / GPT-J:** GPT-like open models described in the chapter.\n"
            "\n"
            "### Encoder-decoder branch\n"
            "\n"
            "- **T5:** expresses many NLP tasks as text-to-text problems.\n"
            "- **BART:** learns to reconstruct original text from corrupted input sequences.\n"
            "- **M2M-100:** supports multilingual many-to-many translation.\n"
            "- **BigBird:** introduces sparse attention to handle longer contexts more efficiently.\n"
            "\n"
            "[[IMAGE_NEEDED: Transformer family tree | "
            "A three-branch family tree with encoder-only, decoder-only, and encoder-decoder "
            "at the top, then representative models from the chapter under each branch | "
            "Learner should use the diagram to categorize models by architecture rather than "
            "memorizing an unstructured list of names]]\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: Attention is just a lookup of one matching token\n"
            "\n"
            "> A query chooses exactly one key and copies its value.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Attention is normally a soft weighted combination. Many positions can contribute "
            "simultaneously, each with a different learned weight.\n"
            "\n"
            "### Misconception 2: Multi-head attention means we manually assign a linguistic "
            "job to each head\n"
            "\n"
            "> Head 1 is always grammar, head 2 is always sentiment, and so on.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The heads are learned from data. Different heads can capture different patterns, "
            "but those roles are not hand-programmed into the architecture.\n"
            "\n"
            "### Misconception 3: Self-attention already knows word order\n"
            "\n"
            "> Because every token attends to every other token, position is automatically known.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The attention computation alone does not encode absolute sequence order. Transformers "
            "need positional information or an attention mechanism that explicitly models positions.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Hidden state | The vector representation maintained for a token inside the model |\n"
            "| Contextualized embedding | A token representation updated using information from its context |\n"
            "| Query | Learned projection representing what a token position is seeking |\n"
            "| Key | Learned projection used to determine relevance to a query |\n"
            "| Value | Learned projection containing information to aggregate after relevance is computed |\n"
            "| Attention score | Raw query-key similarity before softmax normalization |\n"
            "| Attention weight | Normalized importance assigned to a value vector |\n"
            "| Attention head | One independently projected attention computation |\n"
            "| Multi-head attention | Parallel attention heads followed by concatenation and projection |\n"
            "| Feed-forward layer | Per-position neural network applied after attention |\n"
            "| Residual connection | Direct path that adds a sublayer output back to its input |\n"
            "| Layer normalization | Normalization operation used to stabilize transformer training |\n"
            "| Positional embedding | Vector that injects token-position information |\n"
            "| Causal mask | Mask preventing decoder positions from attending to future tokens |\n"
            "| Cross-attention | Attention where decoder queries attend to encoder keys and values |\n"
            "| Task-specific head | Output layer attached to a reusable transformer body for a task |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why can the word `flies` receive different representations in two sentences?\n"
            "2. What is the difference between the roles of Q/K and V in attention?\n"
            "3. Why do we divide attention scores by `sqrt(d_k)` before softmax?\n"
            "4. Why is one attention head often not enough?\n"
            "5. What does a feed-forward layer do that attention does not?\n"
            "6. Why are positional embeddings necessary?\n"
            "7. What information is blocked by a causal mask?\n"
            "8. When would you expect an encoder-only model versus an encoder-decoder model?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A transformer repeatedly turns token embeddings into richer contextual "
            "representations: attention mixes information across tokens, feed-forward layers "
            "transform each position, positional signals preserve order, and masking controls "
            "which information a position is allowed to use.**\n"
        ),

        "estimated_minutes": 105,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "big-picture", "title": "The transformer at a glance", "order": 1},
            {"id": "encoder", "title": "What happens inside an encoder layer?", "order": 2},
            {"id": "self-attention", "title": "Self-attention", "order": 3},
            {"id": "qkv", "title": "Queries, keys, and values", "order": 4},
            {"id": "attention-code", "title": "Build simplified self-attention in PyTorch", "order": 5},
            {"id": "multi-head", "title": "Why multi-head attention?", "order": 6},
            {"id": "ffn-norm", "title": "Feed-forward networks and normalization", "order": 7},
            {"id": "position", "title": "Positional information", "order": 8},
            {"id": "assemble-encoder", "title": "Assemble the encoder", "order": 9},
            {"id": "decoder", "title": "What changes in the decoder?", "order": 10},
            {"id": "model-family", "title": "Meet the transformer families", "order": 11},
        ],
    },

    "exercises": [
        {
            "id": "M01.L02.EX01",
            "title": "Reason About Contextual Attention",
            "lesson_code": "M01.L02",
            "section_id": "self-attention",
            "placement": "after_section",
            "description": (
                "Practice reasoning about which context tokens should influence a token's "
                "meaning before working with attention mathematically."
            ),
            "instructions": (
                "1. Consider the sentences 'time flies like an arrow' and "
                "'fruit flies like a banana'.\n"
                "2. For the token 'flies' in each sentence, identify two nearby tokens that "
                "could help disambiguate its meaning.\n"
                "3. Explain why a fixed embedding for 'flies' is insufficient.\n"
                "4. Describe, in words, how self-attention could produce two different "
                "contextualized representations."
            ),
            "expected_output": (
                "A short comparison naming useful context tokens for each sentence and an "
                "explanation of how attention changes the representation of 'flies'."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "self-attention-intuition",
                "contextual-embeddings",
                "reasoning",
            ],
        },
        {
            "id": "M01.L02.EX02",
            "title": "Trace Shapes Through a Mini Encoder",
            "lesson_code": "M01.L02",
            "section_id": "position",
            "placement": "after_section",
            "description": (
                "Trace tensor shapes and explain why each transformer component preserves or "
                "changes specific dimensions."
            ),
            "instructions": (
                "1. Assume batch_size=2, seq_len=6, hidden_size=768, and num_heads=12.\n"
                "2. Write the shape of the token embeddings.\n"
                "3. Compute the dimension of one attention head.\n"
                "4. Write the shape of the attention-score matrix for one head.\n"
                "5. Write the final shape after concatenating all heads.\n"
                "6. Explain why adding positional embeddings does not change the tensor shape.\n"
                "7. State which dimension a sequence-classification head eventually reduces "
                "to the number of labels."
            ),
            "expected_output": (
                "A small shape table plus a brief explanation. Expected key values include "
                "head_dim=64, embeddings=[2,6,768], one-head scores=[2,6,6], and concatenated "
                "multi-head output=[2,6,768]."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "tensor-shapes",
                "multi-head-attention",
                "positional-embeddings",
                "transformer-architecture",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L02.QZ01",
        "title": "Transformer Anatomy — Knowledge Check",
        "lesson_code": "M01.L02",
        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L02.Q01",
                "section_id": "self-attention",
                "question": (
                    "What is the main reason self-attention can represent the same word "
                    "differently in different sentences?"
                ),
                "options": [
                    "It assigns a new vocabulary ID to the word in every sentence.",
                    "It combines information from surrounding token representations using learned weights.",
                    "It removes all surrounding tokens before encoding the word.",
                    "It replaces every token embedding with its position index.",
                ],
                "correct": 1,
                "explanation": (
                    "Self-attention uses the surrounding sequence to build a contextualized "
                    "representation. The vocabulary ID itself does not need to change."
                ),
            },
            {
                "id": "M01.L02.Q02",
                "section_id": "qkv",
                "question": (
                    "In scaled dot-product attention, what primarily determines the relevance "
                    "score between two token positions?"
                ),
                "options": [
                    "The dot product between a query and a key.",
                    "The sum of two value vectors.",
                    "The position embedding alone.",
                    "The classifier's output logits.",
                ],
                "correct": 0,
                "explanation": (
                    "Queries are compared with keys using dot products. After scaling and "
                    "softmax, those scores become attention weights that combine the values."
                ),
            },
            {
                "id": "M01.L02.Q03",
                "section_id": "multi-head",
                "question": "Why does a transformer use multiple attention heads?",
                "options": [
                    "To make every token use exactly the same attention pattern.",
                    "To avoid using query, key, and value projections.",
                    "To let different learned projections capture multiple relationships in parallel.",
                    "To remove the need for a feed-forward network.",
                ],
                "correct": 2,
                "explanation": (
                    "Different heads have independent projections, allowing the model to learn "
                    "several useful attention patterns in parallel."
                ),
            },
            {
                "id": "M01.L02.Q04",
                "section_id": "decoder",
                "question": "What problem does a causal attention mask solve in a decoder?",
                "options": [
                    "It prevents the model from reading the source sequence.",
                    "It prevents a token from attending to future target tokens.",
                    "It forces all attention weights to be equal.",
                    "It removes positional information from the decoder.",
                ],
                "correct": 1,
                "explanation": (
                    "During autoregressive prediction, a decoder must base each position only "
                    "on the current and previous target positions, not future answers."
                ),
            },
            {
                "id": "M01.L02.Q05",
                "section_id": "model-family",
                "type": "open",
                "question": (
                    "You need to design two systems: (A) a named-entity recognizer that labels "
                    "tokens in an existing sentence and (B) a summarizer that maps a document "
                    "to a new text sequence. Which transformer architecture family would you "
                    "naturally consider for each, and why?"
                ),
            },
        ],

        "passing_score": 70,
    },
}
