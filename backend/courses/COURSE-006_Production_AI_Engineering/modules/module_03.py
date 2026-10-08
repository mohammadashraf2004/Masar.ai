"""M03.L01 — Evaluation Methodology.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 3, "Evaluation Methodology".
Instructor-authored curriculum adaptation based only on the supplied chapter.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M03.L01"

MODULE_ORDER = 3

MODULE_TITLE = "Evaluation Methodology"

MODULE_DESCRIPTION = (
    "Learn how to evaluate open-ended foundation-model systems using language-model "
    "metrics, functional correctness, reference-based similarity, embeddings, AI "
    "judges, human evaluation, and comparative evaluation—while understanding the "
    "limitations and failure modes of each approach."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Page range not provided in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Evaluation Methodology",

    "slug": "ai-engineering-m03-l01-evaluation-methodology",

    "description": (
        "A practical introduction to systematic evaluation for foundation-model "
        "applications, covering exact and subjective evaluation, perplexity, "
        "functional correctness, similarity metrics, embeddings, AI-as-a-judge, "
        "judge bias, and comparative model evaluation."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.0,

    "skill_tags": [
        "ai-evaluation",
        "foundation-models",
        "cross-entropy",
        "perplexity",
        "functional-correctness",
        "semantic-similarity",
        "embeddings",
        "ai-as-a-judge",
        "comparative-evaluation",
        "model-ranking",
        "evaluation-bias",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Evaluation Methodology",

        "content": (
            "# Evaluation Methodology\n"
            "\n"
            "> **Course:** AI Engineering Foundations  \n"
            "> **Lesson:** M03.L01  \n"
            "> **Module:** Evaluation Methodology  \n"
            "> **Source alignment:** Chapter 3, *Evaluation Methodology*. "
            "This lesson is an instructor-authored curriculum adaptation rather "
            "than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why evaluating foundation models is harder than evaluating "
            "traditional close-ended ML systems.\n"
            "- Design evaluation around a system's likely failure modes rather "
            "than relying on ad-hoc prompts or visual inspection.\n"
            "- Explain entropy, cross entropy, bits-per-character, bits-per-byte, "
            "and perplexity at an intuitive level.\n"
            "- Interpret what low and high perplexity mean and identify important "
            "limitations of perplexity.\n"
            "- Distinguish exact evaluation from subjective evaluation.\n"
            "- Use functional correctness when a task has an automatically "
            "verifiable outcome.\n"
            "- Distinguish exact match, lexical similarity, and semantic similarity.\n"
            "- Explain embeddings and cosine similarity at a practical level.\n"
            "- Explain how AI-as-a-judge works and how to design a judge prompt.\n"
            "- Identify major AI-judge limitations including inconsistency, "
            "criteria ambiguity, cost, latency, and bias.\n"
            "- Distinguish stronger, weaker, self-, and specialized judges.\n"
            "- Explain pointwise versus comparative evaluation.\n"
            "- Explain how pairwise model comparisons can be turned into rankings.\n"
            "- Describe important limitations of public comparative leaderboards.\n"
            "- Explain why a comparative win rate does not automatically tell you "
            "whether a model is good enough for your product.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why evaluation is a core part of AI engineering\n"
            "\n"
            "AI systems can fail in ways that create real harm. The supplied "
            "chapter opens with examples of severe failures caused by incorrect or "
            "unsafe model outputs. This is why evaluation is not a final check "
            "added after development—it is part of the engineering process itself.\n"
            "\n"
            "A useful principle from the chapter is:\n"
            "\n"
            "> **You cannot evaluate a system well unless you understand how the "
            "system can fail.**\n"
            "\n"
            "That means evaluation should begin with questions such as:\n"
            "\n"
            "- Where can the model produce incorrect information?\n"
            "- Where can a tool call fail?\n"
            "- Which mistakes are harmless and which are catastrophic?\n"
            "- Which outputs require domain expertise to validate?\n"
            "- What parts of the system are currently invisible to monitoring?\n"
            "\n"
            "Sometimes the system itself must be redesigned so failures become "
            "observable and measurable.\n"
            "\n"
            "### Why 'eyeballing' is not enough\n"
            "\n"
            "A common early-stage practice is to try a few favorite prompts and "
            "judge whether the outputs look good. This can help during exploration, "
            "but it is not a reliable evaluation methodology because the prompts "
            "may not represent actual application needs or failure modes.\n"
            "\n"
            "Systematic evaluation creates a repeatable way to compare changes and "
            "understand whether the system is actually improving.\n"
            "\n"
            '{{image:evaluation-around-failure-modes}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 2. Why foundation models are difficult to evaluate\n"
            "\n"
            "The chapter gives several reasons foundation-model evaluation is "
            "harder than traditional ML evaluation.\n"
            "\n"
            "### Challenge 1: stronger systems require stronger evaluators\n"
            "\n"
            "It is easy to recognize an obviously wrong elementary answer. It is "
            "much harder to evaluate sophisticated mathematics, legal reasoning, "
            "technical research, or a coherent long-form summary. Evaluation can "
            "therefore require fact-checking, reasoning, or domain expertise.\n"
            "\n"
            "### Challenge 2: open-ended tasks have many valid answers\n"
            "\n"
            "A classifier might choose from three labels. An open-ended assistant "
            "can produce countless valid responses to the same prompt. There may "
            "be no single ground-truth string against which to compare the output.\n"
            "\n"
            "### Challenge 3: many models are black boxes\n"
            "\n"
            "If you do not know the training data, architecture, or training "
            "process, you have fewer clues about expected strengths and weaknesses. "
            "You must infer behavior mostly from outputs.\n"
            "\n"
            "### Challenge 4: benchmarks become saturated\n"
            "\n"
            "As models improve, older benchmarks become less useful because many "
            "models approach perfect scores. Newer, harder benchmarks must then be "
            "introduced.\n"
            "\n"
            "### Challenge 5: general-purpose models expand the scope of evaluation\n"
            "\n"
            "Evaluation is no longer only 'how well does this model perform on the "
            "task it was trained for?' It also involves discovering new capabilities "
            "and limitations across many tasks.\n"
            "\n"
            "These challenges explain why automatic evaluation is attractive—but "
            "also why no single metric is sufficient.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Language-model metrics: why they still matter\n"
            "\n"
            "Many foundation models contain a language-model component. Language "
            "models are trained to predict tokens, so metrics that measure "
            "predictive quality can reveal useful information about the underlying "
            "model.\n"
            "\n"
            "The chapter focuses on four closely related metrics:\n"
            "\n"
            "- Entropy\n"
            "- Cross entropy\n"
            "- Perplexity\n"
            "- Bits-per-character (BPC) / bits-per-byte (BPB)\n"
            "\n"
            "These metrics are especially useful during model training and "
            "finetuning, but they can also support model comparison, contamination "
            "detection, deduplication, and abnormal-text detection.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Entropy and cross entropy\n"
            "\n"
            "### Entropy\n"
            "\n"
            "Entropy describes how much uncertainty or information is present in a "
            "distribution. Intuitively, the harder the next token is to predict, "
            "the higher the entropy.\n"
            "\n"
            "Imagine a toy language where only two tokens are possible. Choosing "
            "among two equally likely possibilities requires less information than "
            "choosing among four equally likely possibilities.\n"
            "\n"
            "A lower-entropy sequence is more predictable. A higher-entropy "
            "sequence carries more uncertainty about what comes next.\n"
            "\n"
            "### Cross entropy\n"
            "\n"
            "A language model tries to learn the probability distribution of its "
            "training data. **Cross entropy** measures how difficult it is for the "
            "model's learned distribution to predict data from the real "
            "distribution.\n"
            "\n"
            "At a conceptual level:\n"
            "\n"
            "```text\n"
            "cross entropy\n"
            "    = unavoidable uncertainty in the data\n"
            "    + error caused by the model not matching the data distribution\n"
            "```\n"
            "\n"
            "The second part can be described with KL divergence. If the model "
            "learned the data distribution perfectly, the divergence term would "
            "be zero and cross entropy would equal the data's entropy.\n"
            "\n"
            "Language-model training therefore attempts to reduce cross entropy.\n"
            "\n"
            "### BPC and BPB\n"
            "\n"
            "Different models can use different tokenization schemes, so "
            "bits-per-token may not be directly comparable. Two alternatives are:\n"
            "\n"
            "- **Bits per character (BPC):** normalize by the number of characters.\n"
            "- **Bits per byte (BPB):** normalize by bytes, avoiding some character "
            "encoding differences.\n"
            "\n"
            "The chapter also connects cross entropy to compression: a model that "
            "predicts text well can represent that text more efficiently.\n"
            "\n"
            "[[IMAGE_NEEDED: Entropy and cross entropy intuition | A visual with "
            "two probability distributions: a predictable two-choice distribution "
            "and a less predictable multi-choice distribution, plus a second panel "
            "showing a model distribution approximating a true data distribution | "
            "Learner should notice that entropy belongs to the data distribution "
            "while cross entropy also reflects model mismatch]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Perplexity: uncertainty about the next token\n"
            "\n"
            "Perplexity is an exponential transformation of cross entropy. It can "
            "be interpreted as a measure of how uncertain the model is when "
            "predicting what comes next.\n"
            "\n"
            "For example, if a perfectly learned toy language has four equally "
            "likely next-token choices, its perplexity is 4.\n"
            "\n"
            "### How to interpret perplexity\n"
            "\n"
            "**Lower perplexity** means the model finds the data easier to predict. "
            "**Higher perplexity** means greater uncertainty.\n"
            "\n"
            "But perplexity values are context-dependent. The chapter highlights "
            "three important factors:\n"
            "\n"
            "1. **More structured data usually has lower perplexity.** Code or "
            "markup can be more predictable than everyday language.\n"
            "2. **Larger vocabularies can increase perplexity.** More possible next "
            "tokens make prediction harder.\n"
            "3. **Longer context can lower perplexity.** More context gives the "
            "model additional clues about what comes next.\n"
            "\n"
            "### What perplexity is useful for\n"
            "\n"
            "- Tracking language-model training.\n"
            "- Roughly comparing underlying language-model capability.\n"
            "- Detecting potential benchmark contamination: memorized text may "
            "produce unusually low perplexity.\n"
            "- Data deduplication: very predictable new text may be too similar to "
            "existing data.\n"
            "- Detecting abnormal or unusual text.\n"
            "\n"
            "### Important limitation\n"
            "\n"
            "Perplexity is not always a good downstream metric for post-trained "
            "assistants. SFT and preference optimization can make a model more "
            "useful for tasks while worsening next-token perplexity. This is a "
            "good example of why an evaluation metric must match the behavior you "
            "actually care about.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Exact versus subjective evaluation\n"
            "\n"
            "The chapter separates evaluation into **exact** and **subjective** "
            "methods.\n"
            "\n"
            "### Exact evaluation\n"
            "\n"
            "An exact evaluation rule gives an unambiguous result once the inputs "
            "are fixed. Examples include:\n"
            "\n"
            "- Does the code pass its tests?\n"
            "- Does the generated SQL return the correct rows?\n"
            "- Does the answer exactly match the expected label?\n"
            "- What is the cosine similarity between two fixed embeddings?\n"
            "\n"
            "### Subjective evaluation\n"
            "\n"
            "A subjective evaluation depends on an evaluator's judgment. Examples "
            "include:\n"
            "\n"
            "- How helpful is this response?\n"
            "- Is this explanation coherent?\n"
            "- Which of two answers is better written?\n"
            "\n"
            "AI-as-a-judge is subjective because changing the judge model, prompt, "
            "or sampling settings can change the result.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Functional correctness: does the system actually work?\n"
            "\n"
            "**Functional correctness** evaluates whether the generated solution "
            "performs the intended function.\n"
            "\n"
            "This is powerful because it evaluates the result that actually "
            "matters rather than whether the output merely looks similar to a "
            "reference.\n"
            "\n"
            "### Example: code generation\n"
            "\n"
            "Suppose the model generates a Python function for greatest common "
            "divisor. Instead of judging whether the code looks reasonable, run "
            "the code against test cases.\n"
            "\n"
            "```text\n"
            "prompt -> generated function -> execute tests -> pass/fail\n"
            "```\n"
            "\n"
            "This is the same principle software engineering already uses in unit "
            "testing.\n"
            "\n"
            "### pass@k\n"
            "\n"
            "For coding benchmarks, a model can generate `k` solutions for each "
            "problem. A problem counts as solved if at least one of those solutions "
            "passes all tests.\n"
            "\n"
            "```text\n"
            "pass@k = fraction of problems solved by at least one of k attempts\n"
            "```\n"
            "\n"
            "As `k` increases, the model has more chances to succeed, so pass@k "
            "typically increases.\n"
            "\n"
            "Functional correctness also applies to any task with a measurable "
            "objective: games, scheduling, optimization, or successful completion "
            "of a workflow.\n"
            "\n"
            "Its limitation is that not every open-ended task has an easily "
            "automatable success condition.\n"
            "\n"
            "[[IMAGE_NEEDED: Functional correctness evaluation | A flow diagram "
            "showing an AI-generated solution being executed or applied to several "
            "test cases, producing pass/fail results | Learner should notice that "
            "the system is judged by behavior rather than textual resemblance]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Reference-based evaluation\n"
            "\n"
            "When functional correctness is unavailable, a common alternative is "
            "to compare the generated response against one or more **reference "
            "responses**.\n"
            "\n"
            "A reference example has the conceptual form:\n"
            "\n"
            "```text\n"
            "(input, reference response or responses)\n"
            "```\n"
            "\n"
            "References may be human-generated or AI-generated and reviewed by "
            "humans.\n"
            "\n"
            "The chapter discusses three hand-designed comparison approaches:\n"
            "\n"
            "1. Exact match.\n"
            "2. Lexical similarity.\n"
            "3. Semantic similarity.\n"
            "\n"
            "Each solves a different problem and fails in different ways.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Exact match\n"
            "\n"
            "Exact match is appropriate when the expected response is short and "
            "precise.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- Simple arithmetic.\n"
            "- Trivia-style questions.\n"
            "- Account balances.\n"
            "- Short fill-in-the-blank tasks.\n"
            "\n"
            "A common variant accepts a response if it **contains** the reference "
            "answer. This is convenient but dangerous. If the expected answer is "
            "`1929`, a longer generated answer can include `1929` while still "
            "being factually wrong in another detail.\n"
            "\n"
            "Exact match becomes increasingly unsuitable as tasks become more "
            "open-ended because many different phrasings can be equally correct.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Lexical similarity\n"
            "\n"
            "Lexical similarity measures how much two texts overlap in surface "
            "form.\n"
            "\n"
            "### Edit distance / fuzzy matching\n"
            "\n"
            "One approach counts the number of edits required to transform one "
            "string into another. Common operations include:\n"
            "\n"
            "- Deletion.\n"
            "- Insertion.\n"
            "- Substitution.\n"
            "- Sometimes transposition.\n"
            "\n"
            "### N-gram similarity\n"
            "\n"
            "Instead of comparing only individual tokens, compare sequences of "
            "tokens called **n-grams**.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "My cats scare the mice\n"
            "```\n"
            "\n"
            "has bigrams such as `my cats`, `cats scare`, `scare the`, and "
            "`the mice`.\n"
            "\n"
            "Well-known lexical metrics include BLEU, ROUGE, METEOR++, TER, and "
            "CIDEr.\n"
            "\n"
            "### Limitation\n"
            "\n"
            "Surface overlap is not the same as correctness. A correct answer can "
            "use different wording and receive a poor lexical score. Conversely, "
            "an incorrect answer can reuse much of the same wording and receive a "
            "high score.\n"
            "\n"
            "The quality of reference data also matters. Missing or incorrect "
            "references can punish valid model outputs.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Semantic similarity and embeddings\n"
            "\n"
            "Semantic similarity asks whether two pieces of content mean similar "
            "things, even if they use different words.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "\"What's up?\"\n"
            "\"How are you?\"\n"
            "```\n"
            "\n"
            "have little lexical overlap but related meaning.\n"
            "\n"
            "### Embeddings\n"
            "\n"
            "An **embedding** is a numerical vector designed to capture useful "
            "properties or meaning from the original data.\n"
            "\n"
            "```text\n"
            "text -> embedding model -> [0.11, 0.02, 0.54, ...]\n"
            "```\n"
            "\n"
            "Real embeddings often contain hundreds or thousands of dimensions.\n"
            "\n"
            "The goal is that semantically similar items have nearby vectors.\n"
            "\n"
            "### Cosine similarity\n"
            "\n"
            "One common way to compare embeddings is cosine similarity. For "
            "vectors A and B:\n"
            "\n"
            "```text\n"
            "cosine_similarity(A, B) = (A · B) / (||A|| ||B||)\n"
            "```\n"
            "\n"
            "Higher similarity indicates more similar vector direction.\n"
            "\n"
            "### Embeddings beyond evaluation\n"
            "\n"
            "The chapter notes that embeddings also support:\n"
            "\n"
            "- Retrieval and search.\n"
            "- Ranking.\n"
            "- Clustering.\n"
            "- Anomaly detection.\n"
            "- Deduplication.\n"
            "- Recommender systems.\n"
            "- RAG.\n"
            "\n"
            "Embedding spaces can also be multimodal. CLIP, for example, maps "
            "images and text into a joint space so a text query can be compared "
            "directly with image embeddings.\n"
            "\n"
            "[[IMAGE_NEEDED: Semantic embedding space | A 2D conceptual embedding "
            "plot where semantically related sentences cluster together even when "
            "their wording differs, while unrelated sentences appear far apart | "
            "Learner should notice that semantic similarity operates on meaning "
            "rather than word overlap]]\n"
            "\n"
            "### Limitation\n"
            "\n"
            "Semantic similarity depends on the embedding model. Poor embeddings "
            "can produce misleading similarity scores. The numerical similarity "
            "calculation is exact once embeddings are fixed, but the embedding "
            "representation itself reflects modeling choices.\n"
            "\n"
            "{{exercise:M03.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. AI as a judge\n"
            "\n"
            "**AI as a judge** means using an AI model to evaluate AI-generated "
            "responses.\n"
            "\n"
            "The approach is attractive because AI judges can be faster, cheaper, "
            "and easier to scale than human evaluation. They can also work without "
            "reference answers.\n"
            "\n"
            "An AI judge can evaluate criteria such as:\n"
            "\n"
            "- Correctness.\n"
            "- Relevance.\n"
            "- Coherence.\n"
            "- Faithfulness / groundedness.\n"
            "- Toxicity.\n"
            "- Helpfulness.\n"
            "- Style or role consistency.\n"
            "\n"
            "### Three common judge setups\n"
            "\n"
            "**1. Pointwise judgment**\n"
            "\n"
            "```text\n"
            "question + generated answer -> score / label\n"
            "```\n"
            "\n"
            "**2. Reference-based judgment**\n"
            "\n"
            "```text\n"
            "question + reference answer + generated answer -> judgment\n"
            "```\n"
            "\n"
            "**3. Pairwise judgment**\n"
            "\n"
            "```text\n"
            "question + answer A + answer B -> A / B / tie\n"
            "```\n"
            "\n"
            "The same underlying model can behave as a different judge when the "
            "judge prompt or sampling settings change.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Designing an AI judge\n"
            "\n"
            "A useful judge prompt should clearly specify:\n"
            "\n"
            "1. **The task** — what should be evaluated?\n"
            "2. **The criteria** — what exactly counts as good or bad?\n"
            "3. **The scoring system** — labels, discrete numbers, or continuous "
            "scores.\n"
            "4. **Examples** — examples of outputs and the desired judgments.\n"
            "\n"
            "### Classification versus numerical scores\n"
            "\n"
            "The chapter notes that language models often perform better with "
            "textual classes than with numerical scoring. If numerical scoring is "
            "needed, small discrete ranges such as 1–5 are commonly easier than "
            "wide or continuous ranges.\n"
            "\n"
            "Examples are valuable because they demonstrate what a score means in "
            "practice.\n"
            "\n"
            "### The judge is a system, not just a model\n"
            "\n"
            "A judge should be versioned as:\n"
            "\n"
            "```text\n"
            "judge = model + prompt + sampling/configuration\n"
            "```\n"
            "\n"
            "Changing any of those parts can change the evaluation result.\n"
            "\n"
            "[[IMAGE_NEEDED: AI judge system | A diagram showing generated answer "
            "plus evaluation prompt entering a judge model, which returns a score "
            "and explanation, with model version, prompt version, and sampling "
            "settings labeled as parts of the judge | Learner should notice that "
            "the judge is more than the underlying model name]]\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Limitations and biases of AI judges\n"
            "\n"
            "AI judges are useful, but the chapter strongly warns against treating "
            "them as objective truth.\n"
            "\n"
            "### Inconsistency\n"
            "\n"
            "The same judge can produce different results across runs or prompt "
            "variations. Adding evaluation examples can improve consistency, but "
            "consistency does not guarantee accuracy—a judge can make the same "
            "mistake consistently.\n"
            "\n"
            "### Criteria ambiguity\n"
            "\n"
            "Terms such as `faithfulness`, `relevance`, and `quality` are not "
            "standardized. Different tools can use different prompts and scoring "
            "systems for what appears to be the same metric.\n"
            "\n"
            "Therefore, scores from different judge implementations should not be "
            "assumed comparable.\n"
            "\n"
            "### Judge drift\n"
            "\n"
            "If the judge model or prompt changes over time, evaluation scores can "
            "change even when the application itself has not changed. This makes "
            "versioning essential.\n"
            "\n"
            "### Cost and latency\n"
            "\n"
            "Every judge call adds inference work. Multiple criteria can multiply "
            "cost. Running judges synchronously before returning a response also "
            "adds latency.\n"
            "\n"
            "Possible cost controls include using cheaper judges or evaluating only "
            "a subset of production traffic through spot-checking.\n"
            "\n"
            "### Self-bias\n"
            "\n"
            "A model can prefer outputs generated by itself.\n"
            "\n"
            "### Position bias\n"
            "\n"
            "A pairwise judge may favor the first response. One mitigation is to "
            "repeat comparisons with answer order swapped.\n"
            "\n"
            "### Verbosity bias\n"
            "\n"
            "A judge may prefer a longer answer even when the longer answer "
            "contains factual errors.\n"
            "\n"
            "### Privacy and IP concerns\n"
            "\n"
            "If a proprietary external model acts as judge, evaluation data must "
            "be sent to that provider. This can create privacy or commercial-use "
            "concerns depending on the application.\n"
            "\n"
            "The chapter's practical conclusion is important: **AI judges should "
            "be supplemented with exact evaluation, human evaluation, or both.**\n"
            "\n"
            "---\n"
            "\n"

            "## 15. What models can act as judges?\n"
            "\n"
            "The judge can be stronger, equal to, or weaker than the model being "
            "judged.\n"
            "\n"
            "### Stronger judge\n"
            "\n"
            "A stronger model may make more accurate judgments, but it can be "
            "expensive or slow. One practical design is to use a cheaper model for "
            "generation and a stronger model to evaluate a sample of responses.\n"
            "\n"
            "### Self-evaluation\n"
            "\n"
            "A model can critique its own answer. Self-bias means this should not "
            "be treated as independent evaluation, but self-critique can still be "
            "useful for sanity checking or revision.\n"
            "\n"
            "### Weaker judge\n"
            "\n"
            "Judging can sometimes be easier than generating. This creates the "
            "possibility that a smaller specialized evaluator can judge a stronger "
            "general model effectively on a narrow criterion.\n"
            "\n"
            "### Specialized judges\n"
            "\n"
            "The chapter highlights three important categories:\n"
            "\n"
            "- **Reward model:** scores a `(prompt, response)` pair.\n"
            "- **Reference-based judge:** compares a generated response with one "
            "or more references.\n"
            "- **Preference model:** chooses which of two responses is preferred.\n"
            "\n"
            "A small specialized judge can be more useful than a large general "
            "judge when the evaluation criterion is narrow and well defined.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Pointwise versus comparative evaluation\n"
            "\n"
            "When evaluating several models, there are two broad strategies.\n"
            "\n"
            "### Pointwise evaluation\n"
            "\n"
            "Evaluate each model independently, compute a score for each one, and "
            "rank the models by those scores.\n"
            "\n"
            "```text\n"
            "Model A -> 4.2\n"
            "Model B -> 3.9\n"
            "Model C -> 4.5\n"
            "```\n"
            "\n"
            "### Comparative evaluation\n"
            "\n"
            "Show two outputs side by side and ask which one is better.\n"
            "\n"
            "```text\n"
            "Prompt\n"
            "  -> Model A response\n"
            "  -> Model B response\n"
            "Evaluator chooses A / B / tie\n"
            "```\n"
            "\n"
            "For subjective outputs, pairwise comparison can be easier than "
            "assigning an absolute score.\n"
            "\n"
            "### Preference is not correctness\n"
            "\n"
            "This is one of the most important warnings in the chapter. Some "
            "questions should be judged by factual correctness, not user "
            "preference. If users do not know the correct answer, asking them to "
            "choose which answer they 'prefer' can create misleading feedback.\n"
            "\n"
            "Comparative evaluation works best when evaluators are capable of "
            "judging the task—for example, when AI is helping an expert with work "
            "the expert already understands.\n"
            "\n"
            "### Comparative evaluation is not A/B testing\n"
            "\n"
            "- **Comparative evaluation:** the evaluator sees multiple responses "
            "at the same time.\n"
            "- **A/B testing:** a user typically sees only one system variant at "
            "a time and downstream behavior is compared statistically.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Turning pairwise comparisons into model rankings\n"
            "\n"
            "Each pairwise comparison is a **match**. Over many matches, you can "
            "compute the empirical win rate of one model against another.\n"
            "\n"
            "With only two models, ranking is simple: the model that wins more "
            "often ranks higher.\n"
            "\n"
            "With many models, pairwise results can form a complicated network. "
            "Rating algorithms are used to turn those comparisons into scores and "
            "rankings.\n"
            "\n"
            "The chapter mentions algorithms such as:\n"
            "\n"
            "- Elo.\n"
            "- Bradley-Terry.\n"
            "- TrueSkill.\n"
            "\n"
            "The resulting ranking can be understood as a **predictive model**: if "
            "A ranks above B, the ranking implies that A should be preferred over "
            "B more often in future comparable matches.\n"
            "\n"
            "There is no universally true ranking independent of prompts, "
            "evaluators, and use case. Different rating algorithms can also "
            "produce different rankings.\n"
            "\n"
            "[[IMAGE_NEEDED: Pairwise comparison graph | Several model nodes "
            "connected by pairwise matches with win rates, followed by a rating "
            "algorithm producing a ranked list | Learner should notice that "
            "ranking is inferred from a network of comparisons rather than one "
            "absolute score per model]]\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Limitations of comparative evaluation\n"
            "\n"
            "Comparative evaluation is useful, but the chapter identifies several "
            "major limitations.\n"
            "\n"
            "### Scalability\n"
            "\n"
            "As the number of models grows, the number of possible model pairs "
            "grows quickly. Collecting enough comparisons for every pair becomes "
            "expensive.\n"
            "\n"
            "Ranking systems often rely on assumptions such as transitivity:\n"
            "\n"
            "```text\n"
            "A > B and B > C  -> assume A > C\n"
            "```\n"
            "\n"
            "But human preferences and model strengths may not always be "
            "transitive across tasks and evaluators.\n"
            "\n"
            "### New models change the comparison problem\n"
            "\n"
            "A newly introduced model must be compared with enough existing "
            "models to position it reliably. Private models may require a private "
            "comparison process.\n"
            "\n"
            "### Lack of standardization and quality control\n"
            "\n"
            "Crowdsourced public comparisons can contain:\n"
            "\n"
            "- Weak or trivial prompts.\n"
            "- Users who do not fact-check responses.\n"
            "- Different definitions of what 'better' means.\n"
            "- Malicious or noisy votes.\n"
            "- Prompt distributions that do not match your actual application.\n"
            "\n"
            "A general public leaderboard may therefore fail to predict which "
            "model is best for a specialized application such as RAG over internal "
            "documents.\n"
            "\n"
            "### Comparative performance is not absolute performance\n"
            "\n"
            "If model B beats model A 51% of the time, that does not tell you:\n"
            "\n"
            "- Whether either model meets your quality threshold.\n"
            "- How many customer requests B can resolve.\n"
            "- Whether B's improvement justifies a higher cost.\n"
            "\n"
            "Comparative evaluation answers **which is preferred**, not "
            "**whether this system is good enough for the business**.\n"
            "\n"
            "### Why comparative evaluation still matters\n"
            "\n"
            "Despite these limitations, pairwise evaluation remains valuable "
            "because humans often find comparison easier than absolute scoring. It "
            "can also continue discriminating between models even after fixed "
            "benchmarks become saturated.\n"
            "\n"
            "For offline evaluation it can complement benchmarks. For online "
            "evaluation it can complement A/B testing.\n"
            "\n"
            "{{exercise:M03.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> One high benchmark score proves that a model is good for my application.\n"
            "\n"
            "**Why this is wrong:** public benchmarks may be saturated, "
            "contaminated, misaligned with your use case, or unable to represent "
            "your specific failure modes.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> If an answer sounds fluent, it is probably correct.\n"
            "\n"
            "**Why this is wrong:** sophisticated errors can sound coherent. "
            "Evaluation may require fact-checking, execution, references, or "
            "domain expertise.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> A lower perplexity always means a better assistant.\n"
            "\n"
            "**Why this is wrong:** perplexity measures token prediction, while "
            "post-training can improve task behavior even if perplexity worsens.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> High lexical similarity means the answer is correct.\n"
            "\n"
            "**Why this is wrong:** lexical overlap measures wording, not "
            "functional correctness or factual accuracy.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> AI-as-a-judge produces objective scores.\n"
            "\n"
            "**Why this is wrong:** results depend on the judge model, prompt, "
            "sampling settings, and biases.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> A public leaderboard tells me which model I should deploy.\n"
            "\n"
            "**Why this is wrong:** leaderboard prompts, evaluators, and criteria "
            "may not match your product, and comparative ranking says nothing "
            "about your absolute usefulness threshold, cost, or latency.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Evaluation | Systematic measurement of system quality, risk, capability, and failure. |\n"
            "| Ground truth | Expected or canonical reference output used for comparison. |\n"
            "| Entropy | Average uncertainty or information in a distribution. |\n"
            "| Cross entropy | Measure of how difficult data is for a model distribution to predict. |\n"
            "| Perplexity | Exponential form of cross entropy; interpretable as predictive uncertainty. |\n"
            "| BPC | Bits per character. |\n"
            "| BPB | Bits per byte. |\n"
            "| Functional correctness | Evaluation based on whether the output performs the intended function. |\n"
            "| pass@k | Fraction of benchmark problems solved by at least one of k generated attempts. |\n"
            "| Exact match | Binary comparison requiring generated output to match a reference exactly. |\n"
            "| Lexical similarity | Similarity based on surface text overlap. |\n"
            "| Edit distance | Number of edit operations required to transform one string into another. |\n"
            "| N-gram | Sequence of n tokens used for overlap-based comparison. |\n"
            "| Semantic similarity | Similarity based on meaning rather than wording. |\n"
            "| Embedding | Numerical vector intended to capture meaningful properties of data. |\n"
            "| Cosine similarity | Vector similarity based on the angle between two vectors. |\n"
            "| AI judge | AI system used to evaluate AI-generated outputs. |\n"
            "| Pointwise evaluation | Evaluating each response/model independently. |\n"
            "| Pairwise evaluation | Comparing two responses directly and choosing a preferred one. |\n"
            "| Reward model | Specialized judge that scores a prompt-response pair. |\n"
            "| Preference model | Judge that predicts which of two responses is preferred. |\n"
            "| Self-bias | Tendency of a model judge to favor its own outputs. |\n"
            "| Position bias | Tendency to favor an answer because of where it appears. |\n"
            "| Verbosity bias | Tendency to favor longer answers independent of quality. |\n"
            "| Win rate | Fraction of pairwise matches won by one model over another. |\n"
            "| Elo / Bradley-Terry / TrueSkill | Algorithms that can convert pairwise results into model ratings/rankings. |\n"
            "| Benchmark saturation | Situation where models approach perfect scores and a benchmark loses discriminatory power. |\n"
            "| Data contamination | Evaluation data appearing in model training data, making scores less trustworthy. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why should evaluation start from failure modes?\n"
            "2. Why are open-ended models harder to evaluate than classifiers?\n"
            "3. What does entropy describe?\n"
            "4. What extra idea does cross entropy add beyond entropy?\n"
            "5. What does lower perplexity mean?\n"
            "6. Why can perplexity be misleading for post-trained assistants?\n"
            "7. When is functional correctness the preferred evaluation method?\n"
            "8. What does pass@k measure?\n"
            "9. Why does exact match fail for many open-ended tasks?\n"
            "10. How does lexical similarity differ from semantic similarity?\n"
            "11. What is an embedding?\n"
            "12. Why can cosine similarity still be misleading if the embedding model is poor?\n"
            "13. What are the three common ways to use an AI judge?\n"
            "14. Why should an AI judge be versioned as model + prompt + configuration?\n"
            "15. Name three common AI-judge biases or limitations.\n"
            "16. Why might a small specialized judge outperform a larger general judge for one criterion?\n"
            "17. What is the difference between pointwise and comparative evaluation?\n"
            "18. Why is preference not always the same as correctness?\n"
            "19. What role do Elo or Bradley-Terry style algorithms play in comparative evaluation?\n"
            "20. Why does a 51% pairwise win rate not prove that a model is production-ready?\n"
            "21. Why might a public leaderboard fail to predict performance in your RAG application?\n"
            "22. Why should automatic evaluation usually be supplemented with human evaluation or another evaluation method?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**There is no universal evaluation metric for foundation-model "
            "applications. Good evaluation starts from the failures and outcomes "
            "that matter for your system, then combines the most appropriate exact, "
            "subjective, automated, comparative, and human signals while keeping "
            "their limitations visible.**\n"
        ),

        "estimated_minutes": 240,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-evaluation-matters", "title": "Why evaluation matters", "order": 1},
            {"id": "evaluation-challenges", "title": "Evaluation challenges", "order": 2},
            {"id": "language-model-metrics", "title": "Language-model metrics", "order": 3},
            {"id": "entropy-cross-entropy", "title": "Entropy and cross entropy", "order": 4},
            {"id": "perplexity", "title": "Perplexity", "order": 5},
            {"id": "exact-vs-subjective", "title": "Exact versus subjective evaluation", "order": 6},
            {"id": "functional-correctness", "title": "Functional correctness", "order": 7},
            {"id": "reference-based-evaluation", "title": "Reference-based evaluation", "order": 8},
            {"id": "exact-match", "title": "Exact match", "order": 9},
            {"id": "lexical-similarity", "title": "Lexical similarity", "order": 10},
            {"id": "semantic-similarity", "title": "Semantic similarity and embeddings", "order": 11},
            {"id": "ai-as-judge", "title": "AI as a judge", "order": 12},
            {"id": "judge-prompting", "title": "Designing an AI judge", "order": 13},
            {"id": "judge-limitations", "title": "AI judge limitations and biases", "order": 14},
            {"id": "judge-model-choice", "title": "Choosing judge models", "order": 15},
            {"id": "comparative-evaluation", "title": "Pointwise versus comparative evaluation", "order": 16},
            {"id": "ranking-models", "title": "Ranking models from comparisons", "order": 17},
            {"id": "comparative-limitations", "title": "Comparative evaluation limitations", "order": 18},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M03.L01.EX01",

            "title": "Choose the Right Evaluation Metric",

            "lesson_code": "M03.L01",

            "section_id": "semantic-similarity",

            "placement": "after_section",

            "description": (
                "Practice matching evaluation methods to different types of AI "
                "tasks instead of using one metric everywhere."
            ),

            "instructions": (
                "For each task below, choose the strongest first-choice evaluation "
                "method from functional correctness, exact match, lexical "
                "similarity, semantic similarity, or human/AI judgment. Explain "
                "your choice and one limitation.\n\n"
                "1. Generate a Python function that must pass unit tests.\n"
                "2. Answer 'What is 13 + 29?'.\n"
                "3. Translate a paragraph where many phrasings can be correct.\n"
                "4. Summarize a policy document while preserving its meaning.\n"
                "5. Generate a marketing slogan whose quality is primarily stylistic.\n"
                "6. Search a document collection for passages meaning the same as "
                "a natural-language query.\n"
                "7. For one task, explain why using BLEU or ROUGE alone could "
                "produce a misleading result."
            ),

            "expected_output": (
                "A table or structured answer mapping each task to an evaluation "
                "method, with justification and at least one limitation for each."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "metric-selection",
                "functional-correctness",
                "reference-evaluation",
                "semantic-similarity",
                "evaluation-reasoning",
            ],
        },

        {
            "id": "M03.L01.EX02",

            "title": "Design an Evaluation Strategy for a RAG Assistant",

            "lesson_code": "M03.L01",

            "section_id": "comparative-limitations",

            "placement": "after_section",

            "description": (
                "Design a multi-method evaluation plan that reflects real product "
                "risks rather than relying on one leaderboard or judge."
            ),

            "instructions": (
                "Imagine you are building a RAG assistant over internal company "
                "documents.\n\n"
                "1. Identify four important failure modes.\n"
                "2. Choose at least one exact evaluation signal.\n"
                "3. Choose one reference-based or semantic similarity signal.\n"
                "4. Design one AI-judge criterion and define its scoring system.\n"
                "5. State the judge model/prompt/configuration information that "
                "must be versioned.\n"
                "6. Explain how you would test for position or verbosity bias if "
                "you use pairwise judging.\n"
                "7. Describe where human evaluation is still necessary.\n"
                "8. Explain why a public chatbot leaderboard is insufficient for "
                "selecting the model for this application.\n"
                "9. If Model B beats Model A 55% of the time, explain what extra "
                "information you still need before switching.\n"
                "10. Define one absolute usefulness threshold for the system."
            ),

            "expected_output": (
                "A concise evaluation plan combining system-specific failure "
                "analysis, exact metrics, judge-based evaluation, human review, "
                "versioning, comparative signals, and an absolute deployment "
                "threshold."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "evaluation-design",
                "rag-evaluation",
                "ai-judge-design",
                "comparative-evaluation",
                "risk-analysis",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M03.L01.QZ01",

        "title": "Evaluation Methodology — Knowledge Check",

        "lesson_code": "M03.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M03.L01.Q01",
                "section_id": "why-evaluation-matters",
                "question": (
                    "What should primarily guide the design of an evaluation "
                    "strategy for an AI application?"
                ),
                "options": [
                    "The metrics that are easiest to compute",
                    "The system's important failure modes and desired outcomes",
                    "The benchmark with the highest social-media visibility",
                    "Only the model provider's reported score",
                ],
                "correct": 1,
                "explanation": (
                    "Evaluation should be designed around where the system can fail "
                    "and what outcomes actually matter."
                ),
            },

            {
                "id": "M03.L01.Q02",
                "section_id": "evaluation-challenges",
                "question": (
                    "Why does open-ended generation make ground-truth evaluation difficult?"
                ),
                "options": [
                    "Open-ended models cannot generate text",
                    "There can be many valid responses to the same input",
                    "Ground truth is forbidden for foundation models",
                    "Open-ended models always return deterministic answers",
                ],
                "correct": 1,
                "explanation": (
                    "A comprehensive list of all valid open-ended responses is "
                    "usually impossible to curate."
                ),
            },

            {
                "id": "M03.L01.Q03",
                "section_id": "perplexity",
                "question": "What does lower perplexity generally indicate?",
                "options": [
                    "The model finds the evaluated sequence easier to predict",
                    "The response is guaranteed factually correct",
                    "The model has more parameters",
                    "The model is always better after RLHF",
                ],
                "correct": 0,
                "explanation": (
                    "Perplexity measures predictive uncertainty. Lower perplexity "
                    "means the sequence is easier for the model to predict."
                ),
            },

            {
                "id": "M03.L01.Q04",
                "section_id": "functional-correctness",
                "question": (
                    "What is the best example of functional correctness evaluation?"
                ),
                "options": [
                    "Comparing generated code wording to a reference solution",
                    "Running generated code against test cases",
                    "Counting overlapping words in two answers",
                    "Asking whether the code explanation sounds professional",
                ],
                "correct": 1,
                "explanation": (
                    "Functional correctness asks whether the generated artifact "
                    "actually performs the intended behavior."
                ),
            },

            {
                "id": "M03.L01.Q05",
                "section_id": "functional-correctness",
                "question": "What does pass@k measure?",
                "options": [
                    "The percentage of tokens with probability above k",
                    "The fraction of problems solved by at least one of k generated attempts",
                    "The lexical overlap of k reference answers",
                    "The number of judges who agree",
                ],
                "correct": 1,
                "explanation": (
                    "A problem is solved if at least one of the k generated "
                    "solutions passes all required tests."
                ),
            },

            {
                "id": "M03.L01.Q06",
                "section_id": "lexical-similarity",
                "question": (
                    "What is the main weakness of lexical similarity for open-ended answers?"
                ),
                "options": [
                    "It cannot compare text at all",
                    "Surface wording overlap does not necessarily reflect correctness or meaning",
                    "It always requires model logits",
                    "It is impossible to automate",
                ],
                "correct": 1,
                "explanation": (
                    "Correct responses can use different wording, while incorrect "
                    "responses can still overlap strongly with references."
                ),
            },

            {
                "id": "M03.L01.Q07",
                "section_id": "semantic-similarity",
                "question": "What does an embedding aim to represent?",
                "options": [
                    "Only the raw characters in their original order",
                    "Meaningful properties of data in numerical vector form",
                    "The model's API cost",
                    "A binary correct/incorrect label only",
                ],
                "correct": 1,
                "explanation": (
                    "Embeddings are numerical vector representations intended to "
                    "capture useful semantic properties of the original data."
                ),
            },

            {
                "id": "M03.L01.Q08",
                "section_id": "ai-as-judge",
                "question": (
                    "Why is AI-as-a-judge considered subjective in the chapter?"
                ),
                "options": [
                    "Its result can depend on the judge model and prompt",
                    "It cannot produce scores",
                    "It never uses criteria",
                    "It is performed only by humans",
                ],
                "correct": 0,
                "explanation": (
                    "Changing the judge model, prompt, or configuration can change "
                    "the judgment."
                ),
            },

            {
                "id": "M03.L01.Q09",
                "section_id": "judge-prompting",
                "question": (
                    "Which set best describes what a judge prompt should define?"
                ),
                "options": [
                    "Task, evaluation criteria, scoring system, and examples",
                    "Only the model name",
                    "Only the expected answer length",
                    "GPU type and batch size only",
                ],
                "correct": 0,
                "explanation": (
                    "A useful judge needs an explicit task, criteria, scoring "
                    "system, and preferably examples."
                ),
            },

            {
                "id": "M03.L01.Q10",
                "section_id": "judge-limitations",
                "question": (
                    "What is verbosity bias in an AI judge?"
                ),
                "options": [
                    "Preferring a longer response even when it is not better",
                    "Always selecting the first answer",
                    "Preferring outputs generated by another model",
                    "Rejecting all numerical scores",
                ],
                "correct": 0,
                "explanation": (
                    "Verbosity bias means length itself can influence the judge's "
                    "preference independent of true quality."
                ),
            },

            {
                "id": "M03.L01.Q11",
                "section_id": "judge-limitations",
                "question": (
                    "Why is an improvement from a 90% judge score last month to "
                    "92% this month difficult to interpret if the judge changed?"
                ),
                "options": [
                    "The application improvement is confounded with judge drift",
                    "Scores above 90% are invalid",
                    "AI judges cannot output percentages",
                    "The model must have been retrained",
                ],
                "correct": 0,
                "explanation": (
                    "If the judge model or prompt changed, the score difference "
                    "may reflect a different evaluator rather than a better application."
                ),
            },

            {
                "id": "M03.L01.Q12",
                "section_id": "comparative-evaluation",
                "question": (
                    "When is preference-based pairwise evaluation most defensible?"
                ),
                "options": [
                    "When evaluators understand the task well enough to judge the outputs",
                    "When users have no idea which answer is correct",
                    "When factual correctness does not matter",
                    "When only one response is shown",
                ],
                "correct": 0,
                "explanation": (
                    "Preference signals are most useful when the evaluator is able "
                    "to assess the task and the quality difference meaningfully."
                ),
            },

            {
                "id": "M03.L01.Q13",
                "section_id": "ranking-models",
                "question": (
                    "What is the purpose of Elo, Bradley-Terry, or TrueSkill in "
                    "comparative model evaluation?"
                ),
                "options": [
                    "Convert pairwise comparison outcomes into ratings/rankings",
                    "Compute token perplexity",
                    "Generate embeddings",
                    "Train the model's tokenizer",
                ],
                "correct": 0,
                "explanation": (
                    "These algorithms turn networks of pairwise outcomes into "
                    "scores that can be used to rank models."
                ),
            },

            {
                "id": "M03.L01.Q14",
                "section_id": "comparative-limitations",
                "type": "open",
                "question": (
                    "Model B beats Model A in 55% of pairwise comparisons. Explain "
                    "why this is not enough information to decide whether to replace "
                    "A with B in production. Include at least four additional "
                    "factors or evaluation signals you would need."
                ),
            },
        ],

        "passing_score": 70,
    },
}
