"""M12.L01 — Fine-Tuning Generation Models.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Chapter 12; page range not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M12.L01"

MODULE_ORDER = 12

MODULE_TITLE = "Fine-Tuning Generation Models"

MODULE_DESCRIPTION = (
    "Learn how pretrained generative language models are adapted through supervised "
    "fine-tuning and preference tuning. Explore full fine-tuning, PEFT, adapters, "
    "LoRA, QLoRA, instruction data formatting, generative-model evaluation, reward "
    "models, RLHF, PPO, DPO, and practical alignment workflows."
)

SOURCE_CHAPTER = 12

SOURCE_PAGES = "Page range not provided in supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Fine-Tuning Generation Models",

    "slug": "llm-foundations-m12-l01",

    "description": (
        "A practical guide to adapting pretrained text-generation models. The lesson "
        "covers the three-stage LLM training pipeline, supervised instruction tuning, "
        "parameter-efficient fine-tuning with adapters and LoRA, quantized LoRA, "
        "evaluation of generative models, reward-model-based preference tuning, PPO, "
        "DPO, and the SFT-plus-preference-tuning workflow."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 4.0,

    "skill_tags": [
        "generative-finetuning",
        "sft",
        "instruction-tuning",
        "peft",
        "adapters",
        "lora",
        "qlora",
        "quantization",
        "nf4",
        "bitsandbytes",
        "trl",
        "generative-evaluation",
        "perplexity",
        "rouge",
        "bleu",
        "bertscore",
        "benchmarks",
        "llm-as-a-judge",
        "human-evaluation",
        "rlhf",
        "reward-models",
        "ppo",
        "dpo",
        "preference-tuning",
        "alignment",
        "orpo",
        "module-12",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M02.L01",
        "M03.L01",
        "M04.L01",
        "M05.L01",
        "M06.L01",
        "M07.L01",
        "M08.L01",
        "M09.L01",
        "M10.L01",
        "M11.L01",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Fine-Tuning Generation Models",

        "content": (
            r"""
# Fine-Tuning Generation Models

> **Course:** Large Language Models Foundations  
> **Lesson:** M12.L01  
> **Module:** Fine-Tuning Generation Models  
> **Source alignment:** Chapter 12, “Fine-Tuning Generation Models.” Page numbers were not included in the supplied chapter text. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the three common stages in creating a high-quality LLM:
  **pretraining, supervised fine-tuning, and preference tuning**.
- Explain why a base language model may continue text instead of following instructions.
- Explain how supervised fine-tuning turns a base model into an instruction-following model.
- Compare **full fine-tuning** with **parameter-efficient fine-tuning (PEFT)**.
- Explain the purpose of adapters.
- Explain the intuition behind **Low-Rank Adaptation (LoRA)**.
- Explain why LoRA can store task-specific changes separately from the base model.
- Explain the role of rank `r`, `lora_alpha`, dropout, and target modules.
- Explain why quantization reduces memory requirements.
- Explain the central idea of **QLoRA**.
- Describe 4-bit NF4 quantization, double quantization, and low-precision loading at a high level.
- Format instruction data using a chat template.
- Build the mental model of instruction tuning with QLoRA.
- Explain gradient accumulation, gradient checkpointing, learning-rate scheduling, and paged optimizers conceptually.
- Explain how LoRA adapters can be merged with a base model.
- Explain why evaluating generative models requires multiple complementary methods.
- Explain the strengths and limitations of perplexity, ROUGE, BLEU, and BERTScore.
- Explain what public benchmarks and leaderboards can and cannot tell us.
- Explain **LLM-as-a-judge** and pairwise automated evaluation.
- Explain why human evaluation remains important.
- Explain Goodhart’s Law in the context of LLM evaluation.
- Define **preference tuning / alignment**.
- Explain what a reward model does.
- Explain how preference datasets are constructed from chosen and rejected generations.
- Explain the three broad stages of reward-model-based preference tuning.
- Explain the high-level role of PPO in RLHF.
- Explain why DPO avoids training a separate reward model.
- Explain how a frozen reference model and a trainable model are used in DPO.
- Describe the chapter’s SFT + DPO workflow.
- Explain why alignment methods still inherit the quality and bias of their preference data.
- Decide when full fine-tuning, LoRA, QLoRA, SFT, or preference tuning is appropriate.

---

## 1. The three-stage path from base model to aligned assistant

The chapter begins with a very useful mental model.

A high-quality generative LLM is commonly created through three broad stages:

```text
1. Pretraining / language modeling
2. Supervised fine-tuning (SFT)
3. Preference tuning / alignment
```

Each stage solves a different problem.

### Stage 1 — Learn language

The model learns:

```text
What token is likely to come next?
```

### Stage 2 — Learn to follow instructions

The model learns:

```text
Given this user request,
what response should I generate?
```

### Stage 3 — Learn preferred behavior

The model learns:

```text
Among plausible responses,
which kinds do humans or the target system prefer?
```

{{image:three-stage-llm-training}}

The important idea is:

> Pretraining teaches broad language capability; SFT teaches task-following behavior; preference tuning shapes which acceptable behaviors are preferred.

---

## 2. Stage 1 — Pretraining creates the base model

During causal language modeling, the model receives text such as:

```text
Large language models are trained to
```

and predicts:

```text
the next token
```

Then it repeats the process.

This is **self-supervised learning** because the target token comes from the text itself.

No human needs to write a separate label for every training example.

Conceptually:

```text
massive unlabeled text
      ↓
next-token prediction
      ↓
base / foundation model
```

The base model learns:

- syntax,
- semantics,
- factual associations,
- writing patterns,
- broad linguistic structure.

But this does not automatically make it a good assistant.

---

## 3. A base model is a completion engine, not automatically an instruction follower

Suppose you ask:

```text
What is the capital of France?
```

A pure base model was trained to continue text.

So it might produce something resembling:

```text
What is the capital of Germany?
What is the capital of Italy?
...
```

instead of:

```text
Paris.
```

That behavior is not necessarily a failure of language modeling.

The model is doing what pretraining taught it:

```text
predict plausible continuation
```

rather than:

```text
obey user intent
```

[[IMAGE_NEEDED: Base model continuation versus instruction model | Show the same user question sent to a base model that continues with more questions and an instruction-tuned model that answers directly | Learner should understand why instruction following is a separate learned behavior]]

---

## 4. Stage 2 — Supervised Fine-Tuning teaches instruction following

SFT uses labeled examples containing:

```text
instruction / user input
+
desired response
```

Example:

```text
User:
Explain gradient descent simply.

Assistant:
Gradient descent is an optimization method that...
```

The model still trains with next-token prediction.

The difference is that the training examples are structured as desired conversations or instruction-response pairs.

Conceptually:

```text
base model
+
instruction-response examples
      ↓
supervised fine-tuning
      ↓
instruction-following model
```

[[IMAGE_NEEDED: SFT training example | Show user instruction + desired assistant response converted into a training sequence where the model learns to predict the response tokens conditioned on the user message | Learner should see that SFT still uses token prediction but on curated instruction data]]

---

## 5. Full fine-tuning updates all model parameters

In **full fine-tuning**:

```text
all trainable model weights
→ receive gradient updates
```

This gives maximum adaptation capacity.

But it is expensive.

Costs include:

- GPU memory,
- training time,
- optimizer-state memory,
- checkpoint storage,
- deployment complexity for multiple task-specific variants.

The chapter contrasts this with the smaller labeled datasets used for fine-tuning.

Pretraining:

```text
very large unlabeled corpus
```

Fine-tuning:

```text
smaller labeled task dataset
```

---

## 6. Parameter-Efficient Fine-Tuning: adapt less of the model

PEFT asks:

> Can we adapt model behavior without updating every original parameter?

Instead of training billions of weights, we train a small number of additional or derived parameters.

Conceptually:

```text
large base model
mostly frozen

+
small trainable component
```

Benefits:

- less GPU memory,
- faster training,
- smaller task-specific checkpoints,
- easier swapping among specializations.

[[IMAGE_NEEDED: Full fine-tuning versus PEFT | Show a full model with every block highlighted as trainable beside a mostly frozen model with only small adapter/LoRA components highlighted | Learner should understand PEFT as reducing the trainable parameter set]]

---

## 7. Adapters: insert small trainable modules

An adapter approach adds small neural modules inside Transformer blocks.

Conceptually:

```text
Transformer block
├── attention
├── small adapter
├── feedforward
└── small adapter
```

Most original Transformer parameters remain frozen.

Only adapter parameters are updated.

The chapter cites early adapter work showing that a small percentage of trainable parameters could approach full fine-tuning performance on benchmark tasks.

The key insight is:

> Task specialization can often be represented by a much smaller parameter update than the entire base model.

---

## 8. Adapters make specialization modular

Imagine one base model with:

```text
adapter A → medical task
adapter B → NER task
adapter C → legal task
```

Instead of storing three complete copies of the base model:

```text
base model
+
small task adapters
```

can be stored separately.

[[IMAGE_NEEDED: Swappable adapters | Show one shared frozen Transformer backbone with several small adapter sets that can be swapped for medical, NER, and legal tasks | Learner should understand the storage and modularity benefit]]

This same modularity idea will reappear with LoRA.

---

## 9. LoRA: represent weight updates with low-rank matrices

**Low-Rank Adaptation (LoRA)** takes a different approach.

Instead of inserting conventional adapter layers, LoRA approximates the **change** to a large weight matrix using two much smaller matrices.

Suppose the base model contains a matrix:

```text
W
```

LoRA keeps `W` frozen and learns an update:

```text
ΔW = B × A
```

where `A` and `B` are low-rank matrices.

The effective weight becomes:

```text
W' = W + ΔW
```

[[IMAGE_NEEDED: LoRA matrix update | Show large frozen matrix W plus a low-rank update ΔW formed by multiplying two narrow matrices A and B, producing effective weight W + ΔW | Learner should understand that LoRA learns a compact weight change rather than replacing the full matrix]]

---

## 10. Why low rank saves parameters

Imagine a:

```text
10 × 10
```

matrix.

That contains:

```text
100 values
```

A rank-1 style decomposition could use:

```text
10 × 1
and
1 × 10
```

which uses:

```text
20 values
```

instead of 100.

More generally, for a matrix of size:

```text
d × d
```

a rank-`r` update uses approximately:

```text
d × r
+
r × d
```

parameters.

When:

```text
r << d
```

the savings can be very large.

### Source consistency note

The supplied chapter gives a large-model example that says “rank 8” but then describes matrices as `12,288 × 2` while reporting roughly `197K` parameters. The reported parameter count corresponds to rank 8, not rank 2.

The lesson to retain is the low-rank scaling relationship—not the inconsistent dimension text in that example.

---

## 11. LoRA does not need to modify every matrix

A Transformer contains many weight matrices, including projections used in attention and feedforward layers.

LoRA can target only selected modules.

For example:

```text
query projection
value projection
key projection
output projection
feedforward projections
```

The choice changes:

```text
trainable parameter count
training cost
adaptation capacity
```

This is another PEFT tradeoff.

---

## 12. Understand the main LoRA hyperparameters

The chapter later uses a configuration containing:

```text
r
lora_alpha
lora_dropout
target_modules
```

### `r`

The rank of the low-rank update.

Higher `r`:

```text
more trainable capacity
more memory
more parameters
```

Lower `r`:

```text
more compression
less adaptation capacity
```

### `lora_alpha`

Scales the LoRA update.

Conceptually, it controls how strongly the learned update contributes relative to the frozen base weights.

### `lora_dropout`

Regularizes LoRA training.

### `target_modules`

Defines which model matrices receive LoRA updates.

---

## 13. Quantization reduces the memory needed for base weights

Model parameters are stored as numbers.

Typical formats include:

```text
32-bit float
16-bit float
8-bit representations
4-bit representations
```

Reducing precision means:

```text
fewer bits per weight
→ less memory
```

but also:

```text
less numerical precision
```

[[IMAGE_NEEDED: Numerical precision and memory | Show one weight represented in 32-bit, 16-bit, 8-bit, and 4-bit forms with decreasing memory use and increasing approximation | Learner should understand the core quantization tradeoff]]

Quantization helps:

- inference,
- loading large models,
- and, with methods such as QLoRA, fine-tuning.

---

## 14. Naive quantization can collapse nearby values

Suppose several high-precision weights are:

```text
0.512
0.518
0.523
```

A crude low-bit mapping might map all of them to:

```text
0.5
```

Now their distinctions are lost.

Quantization therefore needs a mapping strategy that preserves useful information as well as possible.

The chapter introduces QLoRA’s use of more careful quantization techniques to reduce this damage.

---

## 15. QLoRA: quantize the base model, train LoRA updates

QLoRA combines:

```text
Q = Quantization
+
LoRA
```

High-level architecture:

```text
base model weights
→ loaded in low precision
→ kept frozen

LoRA parameters
→ small
→ trainable
```

This produces major memory savings.

[[IMAGE_NEEDED: QLoRA architecture | Show frozen 4-bit base model weights with small trainable LoRA matrices attached to selected projection layers | Learner should understand why QLoRA can fine-tune models that would otherwise exceed available VRAM]]

The chapter describes 4-bit normalized-float-style quantization and related techniques.

---

## 16. Blockwise and distribution-aware quantization

Rather than treating every weight identically across the entire model, blockwise quantization handles groups of values.

The chapter’s intuition is:

```text
different local ranges
→ different quantization mappings
```

This can represent weights more faithfully than one global mapping.

It also discusses taking advantage of the typical distribution of neural-network weights when designing low-bit representations.

The result is a better balance between:

```text
compression
and
reconstruction accuracy
```

---

## 17. NF4 and double quantization in the chapter

The chapter’s QLoRA configuration uses:

```python
BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
    bnb_4bit_use_double_quant=True,
)
```

Conceptually:

```text
load_in_4bit
→ store base model in 4-bit representation

nf4
→ normalized 4-bit quantization scheme

float16 compute
→ perform computations at higher precision than storage

double quantization
→ quantize additional quantization-related values for more savings
```

Treat exact API names as source-era implementation details.

The architectural principle is:

> Store the frozen base model cheaply while training a small high-value adaptation.

---

## 18. Instruction tuning requires correctly formatted conversations

A base model will not learn chat behavior if the training data does not clearly distinguish:

```text
user
assistant
system
message boundaries
```

The chapter uses a TinyLlama-compatible chat template.

Conceptually:

```text
<|user|>
instruction
</s>
<|assistant|>
desired response
</s>
```

[[IMAGE_NEEDED: Instruction-tuning chat template | Show raw conversation messages being serialized into model-specific user/assistant tokens and end-of-message markers | Learner should connect chat templates from Chapter 6 with SFT training data]]

The exact special tokens depend on the model.

The important rule is:

> Fine-tuning data should follow the interface format the target model is expected to use.

---

## 19. The chapter’s instruction dataset

The source uses a subset of:

```text
UltraChat
```

and selects:

```text
3,000 conversations
```

for a manageable demonstration.

Each example becomes a serialized conversation containing:

- user turns,
- assistant turns,
- special role markers.

The chapter explicitly notes that using more data may improve results but increases training cost.

---

## 20. Start from a base TinyLlama checkpoint

The chapter fine-tunes a small Llama-family model:

```text
TinyLlama
```

The selected checkpoint is treated as a base/pretrained model rather than a fully instruction-aligned assistant.

This makes it suitable for demonstrating:

```text
before SFT
versus
after SFT
```

behavior.

---

## 21. Load the base model in 4-bit form

The source loads the model with a quantization configuration.

The chapter reports that quantization substantially reduces the VRAM needed just to load the model.

The exact memory usage depends on:

- model size,
- implementation,
- device,
- optimizer/training state.

The conceptual point is:

```text
quantized loading
→ lower base-model memory
→ more room for training
```

Do not confuse:

```text
memory to load the model
```

with:

```text
total memory required during training
```

Training still requires additional memory.

---

## 22. Attach LoRA to the selected model modules

The chapter defines:

```python
LoraConfig(
    lora_alpha=32,
    lora_dropout=0.1,
    r=64,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
        "k_proj",
        "gate_proj",
        "v_proj",
        "up_proj",
        "q_proj",
        "o_proj",
        "down_proj",
    ],
)
```

Then conceptually:

```text
prepare quantized model
→ attach LoRA parameters
→ train only the PEFT components
```

This transforms the model from:

```text
frozen quantized base
```

into:

```text
frozen quantized base
+
trainable low-rank updates
```

---

## 23. Configure efficient training

The chapter uses training settings including:

```text
batch size = 2
gradient accumulation = 4
paged AdamW
learning rate = 2e-4
cosine scheduler
1 epoch
FP16
gradient checkpointing
```

Each serves a purpose.

### Small per-device batch

Reduces immediate memory pressure.

### Gradient accumulation

Instead of updating after every tiny batch:

```text
batch 1 gradients
+
batch 2 gradients
+
batch 3 gradients
+
batch 4 gradients
→ optimizer step
```

This approximates a larger effective batch.

[[IMAGE_NEEDED: Gradient accumulation | Show four small mini-batches processed sequentially, gradients accumulated, then one optimizer update | Learner should understand how small-memory training can emulate a larger batch size]]

---

## 24. Gradient checkpointing trades compute for memory

During backpropagation, intermediate activations consume substantial memory.

Gradient checkpointing stores fewer of them and recomputes some during backward passes.

Conceptually:

```text
less activation memory
but
more recomputation
```

This makes larger-model fine-tuning possible on smaller hardware at the cost of extra compute.

---

## 25. Learning-rate scheduling changes the update size over time

The chapter uses a cosine learning-rate schedule.

The broad idea is:

```text
start carefully
increase to useful learning rate
then gradually decay
```

This can stabilize optimization.

Exact schedules should be treated as hyperparameters, not universal recipes.

---

## 26. Train with an SFT-specific trainer

The source uses:

```text
SFTTrainer
```

from TRL.

Conceptually it receives:

```text
model
instruction dataset
text field
tokenizer
training arguments
sequence length
PEFT configuration
```

Then:

```python
trainer.train()
```

updates the LoRA parameters using instruction-formatted examples.

The base model weights remain largely frozen under the PEFT setup.

---

## 27. LoRA weights can remain separate or be merged

After training, the LoRA adapter is saved separately.

Conceptually:

```text
base model
+
LoRA adapter
```

can be deployed together.

Or the update can be merged:

```text
W + ΔW
→ merged model weights
```

The chapter demonstrates loading the adapter and merging it into the base model.

[[IMAGE_NEEDED: LoRA adapter merge | Show frozen base model and separate LoRA adapter being combined into one merged model for inference | Learner should understand adapter-only storage versus merged deployment]]

This is operationally convenient when you want one standalone model artifact.

---

## 28. After SFT, the model behaves more like an assistant

The chapter asks the tuned model:

```text
Tell me something about Large Language Models.
```

and shows it producing a direct explanatory answer.

This contrasts with a raw base model that might continue text rather than interpret the string as an instruction.

The important result is behavioral:

```text
before SFT
→ completion behavior

after SFT
→ instruction-following behavior
```

---

## 29. Generative-model evaluation is inherently multidimensional

A classifier often has a clear target label.

A generator can produce many valid answers.

Suppose two answers are both correct.

One may be:

```text
clear and concise
```

while the other is:

```text
verbose and confusing
```

A single metric may not capture that difference.

The chapter therefore emphasizes:

> There is no one universally perfect metric for generative models.

Evaluation should match the intended use case.

---

## 30. Word-level and sequence-level metrics

The chapter mentions:

```text
perplexity
ROUGE
BLEU
BERTScore
```

These compare generated text with expected/reference text in different ways.

They can be useful.

But they do not fully measure:

- correctness,
- usefulness,
- reasoning quality,
- creativity,
- safety,
- domain fit.

Use them as signals, not final truth.

---

## 31. Perplexity measures predictive surprise

Perplexity is connected directly to language modeling.

If the model assigns high probability to the correct next token, it is less “surprised.”

Conceptually:

```text
lower perplexity
→ model predicts the observed text more confidently
```

[[IMAGE_NEEDED: Perplexity intuition | Show a phrase ending before the next token, with one model assigning high probability to the correct continuation and another distributing probability poorly | Learner should understand perplexity as next-token predictive confidence]]

However:

> A model with lower perplexity is not automatically safer, more useful, more truthful, or better at every downstream task.

---

## 32. Public benchmarks evaluate different capabilities

The source lists examples such as:

```text
MMLU
GLUE
TruthfulQA
GSM8K
HellaSwag
HumanEval
```

These cover different abilities.

For example:

```text
GSM8K
→ grade-school math problems

HumanEval
→ programming tasks

TruthfulQA
→ truthfulness-oriented QA
```

A benchmark result is meaningful only relative to:

```text
what that benchmark measures
```

---

## 33. Leaderboards aggregate benchmarks—but can become targets

Leaderboards combine several benchmark scores to compare models.

They are convenient.

But the chapter warns about:

- benchmark overfitting,
- contamination,
- weak connection to niche real-world use cases,
- expensive evaluation.

A model ranked highly overall may still be poor for your specific domain.

---

## 34. LLM-as-a-judge evaluates open-ended quality

Some qualities are difficult to measure with exact token overlap.

An evaluation model can instead read a response and score properties such as:

- helpfulness,
- clarity,
- relevance,
- completeness.

A common design is pairwise comparison:

```text
Prompt
 ├─ Model A response
 └─ Model B response
        ↓
judge model
        ↓
which is better?
```

[[IMAGE_NEEDED: LLM-as-a-judge pairwise evaluation | Show two candidate model responses to one prompt being compared by a separate judge model that returns a preference | Learner should understand automated qualitative comparison]]

This is scalable.

But the judge is also a model.

It can have:

- biases,
- blind spots,
- position preferences,
- style preferences,
- domain limitations.

---

## 35. Human evaluation remains essential

Humans can judge dimensions that benchmarks may miss.

Examples:

```text
Was this actually useful?
Would I trust this in my workflow?
Did it follow my domain conventions?
Was the explanation understandable?
```

The chapter points to pairwise human voting systems such as Chatbot Arena as an example of preference-based evaluation.

But even crowdsourced human preference is not automatically equal to:

```text
your own product requirements
```

So production evaluation should include users and experts who represent the intended domain.

---

## 36. Goodhart’s Law: do not optimize blindly for one metric

The chapter quotes the idea:

```text
When a measure becomes a target,
it ceases to be a good measure.
```

Suppose we optimize only:

```text
grammatical correctness
```

A model could maximize that by returning the same safe sentence every time.

The metric improves.

The product becomes useless.

[[IMAGE_NEEDED: Goodhart's Law in LLM evaluation | Show a model optimizing one metric upward while broader usefulness drops, illustrating benchmark gaming/over-optimization | Learner should understand why evaluation needs multiple independent perspectives]]

The lesson:

> Metrics should guide improvement, not replace judgment.

---

{{exercise:M12.L01.EX01}}

---

## 37. Stage 3 — Preference tuning shapes which answers are preferred

After SFT, the model can follow instructions.

But several responses may all be valid.

For:

```text
What is an LLM?
```

you may prefer:

```text
a clear, detailed explanation
```

over:

```text
"It is a large language model."
```

Preference tuning uses data that tells the model:

```text
this response is preferred
over
that response
```

The objective is not just:

```text
Can the model answer?
```

but:

```text
Does it answer in the desired way?
```

---

## 38. Preferences can be represented as scores or comparisons

A human evaluator can score a response.

Conceptually:

```text
prompt
+
generated answer
      ↓
human preference evaluator
      ↓
score
```

High score:

```text
encourage similar behavior
```

Low score:

```text
discourage similar behavior
```

Doing this manually for every training step would be expensive.

So the chapter introduces a **reward model**.

---

## 39. Reward models automate preference scoring

A reward model takes:

```text
prompt
+
candidate response
```

and returns:

```text
one scalar score
```

Conceptually:

```text
(prompt, answer)
→ reward model
→ quality/preference score
```

[[IMAGE_NEEDED: Reward model | Show prompt + generated response entering a reward model derived from an instruction-tuned model, with the language-modeling head replaced by a scalar scoring head | Learner should understand how generative output can be converted into a trainable preference score]]

The reward model does not generate the final answer.

It judges candidate answers.

---

## 40. Preference data often contains chosen and rejected responses

A common dataset format is:

```text
prompt
chosen response
rejected response
```

Important nuance:

```text
rejected
```

does not always mean terrible.

It may mean:

```text
both are acceptable,
but one is preferred
```

This relative signal is often easier for humans to provide than an absolute score.

---

## 41. One way to collect preference data

For each prompt:

```text
generate response A
generate response B
```

Then ask a human:

```text
Which do you prefer?
```

The result becomes:

```text
chosen
rejected
```

[[IMAGE_NEEDED: Preference data collection | Show one prompt sent to the same model twice to create response A and B, then a human chooses one as preferred | Learner should see how pairwise feedback becomes training data]]

Repeating this creates a preference dataset.

---

## 42. Train the reward model to rank chosen above rejected

For one preference example:

```text
prompt + chosen
→ reward score chosen

prompt + rejected
→ reward score rejected
```

Training encourages:

```text
reward(chosen)
>
reward(rejected)
```

The reward model learns human preference patterns from many such comparisons.

---

## 43. The classic reward-model-based alignment pipeline

The chapter summarizes three broad steps:

```text
1. Collect preference data
2. Train reward model
3. Fine-tune the LLM using reward-model feedback
```

This is the classic RLHF-style architecture.

[[IMAGE_NEEDED: Reward-model-based RLHF pipeline | Show preference collection → reward model training → policy/LLM optimization with reward feedback | Learner should understand the full alignment loop]]

Some systems may use multiple reward models.

For example:

```text
helpfulness reward
safety reward
```

This separates different preference dimensions.

---

## 44. PPO uses reward feedback to optimize the instruction-tuned model

The chapter introduces:

```text
Proximal Policy Optimization
```

or:

```text
PPO
```

as a reinforcement-learning method used in reward-model-based LLM alignment.

At a high level:

```text
LLM generates
→ reward model scores
→ PPO updates LLM
```

The optimization tries to improve reward while controlling how aggressively the model changes.

The chapter notes that this style of method was used in early ChatGPT alignment.

The important lesson is architectural, not to master PPO mathematics here.

---

## 45. Reward-model-based PPO is powerful but complex

PPO-style preference tuning may require:

```text
instruction model
reward model
reference/baseline behavior
reinforcement-learning machinery
```

That creates:

- more memory use,
- more training components,
- more hyperparameters,
- more failure modes.

The chapter therefore introduces a simpler alternative:

```text
DPO
```

---

## 46. DPO: optimize preferences directly

**Direct Preference Optimization (DPO)** avoids explicitly training a separate reward model.

The training data still contains:

```text
prompt
chosen response
rejected response
```

But the training process compares probabilities under:

```text
frozen reference model
and
trainable model
```

The objective pushes the trainable model toward:

```text
higher relative preference for chosen responses
```

and away from:

```text
rejected responses
```

[[IMAGE_NEEDED: DPO versus reward-model RLHF | Left side shows preference data → reward model → PPO → LLM; right side shows preference data directly comparing frozen reference and trainable model probabilities | Learner should see why DPO removes the explicit reward-model training stage]]

---

## 47. DPO uses generation probabilities as the comparison signal

For a response, the model assigns probabilities token by token.

Conceptually:

```text
P(token1)
×
P(token2 | token1)
×
...
```

In practice, training works with log probabilities.

DPO compares how the trainable model changes the relative preference for:

```text
chosen
versus
rejected
```

relative to the reference model.

You do not need to memorize the full DPO equation to understand the architecture.

The essential concept is:

> Make the tuned model relatively more confident in preferred generations without requiring a separately learned scalar reward model.

---

## 48. Prepare alignment data for DPO

The chapter’s dataset contains:

```text
system
input/prompt
chosen
rejected
```

It formats them into:

```text
prompt
chosen response
rejected response
```

using the same model-specific conversation style.

This reinforces a recurring lesson:

> Data format must match the model interface.

The chapter also filters examples by quality/status criteria before training.

Data quality matters just as much in preference tuning as it does in supervised fine-tuning.

---

## 49. Preference tuning starts from an already instruction-tuned model

This ordering matters.

DPO is not being used in the chapter to teach the model basic chat structure from scratch.

The model has already undergone:

```text
SFT
```

Then DPO adjusts its preferences.

Conceptually:

```text
base model
 ↓
SFT
 ↓
instruction model
 ↓
DPO
 ↓
preference-aligned instruction model
```

[[IMAGE_NEEDED: SFT then DPO | Show a base model first receiving instruction tuning and then preference tuning, with each stage labeled by the type of data it uses | Learner should understand why instruction following and preference alignment are separate capabilities]]

---

## 50. The chapter also applies PEFT to DPO

The source again uses:

```text
quantized model loading
+
LoRA
```

for preference tuning.

This means QLoRA is not limited to the SFT stage.

It can also reduce the memory requirements of later adaptation stages.

The architecture remains:

```text
frozen/quantized base
+
trainable LoRA update
```

but now the training objective is preference-based rather than instruction imitation.

---

## 51. DPO training introduces its own configuration

The chapter uses a DPO configuration including:

```text
learning rate
max training steps
warmup ratio
gradient accumulation
FP16
gradient checkpointing
```

and DPO-specific trainer settings including:

```text
beta
max prompt length
max total length
```

### Warmup

The source describes gradually increasing the learning rate during the early portion of training.

This can reduce instability at the beginning of optimization.

### `beta`

At a high level, DPO’s `beta` controls how strongly the optimization balances preference changes relative to the reference behavior.

Treat it as a tuning parameter rather than a universal constant.

---

## 52. Merge the SFT and DPO adaptations

The chapter ends with two adaptation stages:

```text
SFT LoRA adapter
DPO LoRA adapter
```

It merges them sequentially.

Conceptually:

```text
base model
+
SFT adapter
→ SFT model

SFT model
+
DPO adapter
→ aligned model
```

This gives a final model that has learned:

```text
how to follow instructions
and
which response styles/preferences to favor
```

---

## 53. SFT + DPO improves behavior but requires two training loops

The chapter explicitly notes the cost:

```text
SFT training
+
DPO training
```

means two optimization stages.

That brings:

- more compute,
- more tuning,
- more data preparation,
- more checkpoints/adapters.

Newer methods attempt to simplify the process.

The source mentions:

```text
ORPO
```

as one example that combines aspects of SFT and preference optimization.

Treat that as an example of the broader trend toward simpler alignment pipelines.

---

## 54. Preference tuning does not create an objective definition of “good”

This is a critical conceptual point.

Preference tuning learns from:

```text
the preferences encoded in its data
```

If evaluators prefer:

```text
verbosity
```

the model may become more verbose.

If labels contain:

- bias,
- inconsistent standards,
- domain mistakes,
- reward hacking opportunities,

the trained behavior may reflect those problems.

Alignment means:

```text
align to a preference signal
```

not:

```text
discover universal truth
```

This is why preference-data design and evaluation matter enormously.

---

## 55. Compare the main fine-tuning methods

| Method | What changes? | Main advantage | Main cost/risk |
|---|---|---|---|
| Full fine-tuning | Most/all model parameters | Maximum adaptation capacity | High memory, compute, storage |
| Adapters | Small inserted modules | Modular task specialization | Extra architectural components |
| LoRA | Low-rank weight updates | Small trainable parameter count | Capacity depends on rank/targets |
| QLoRA | Quantized frozen base + LoRA | Much lower memory requirement | Added quantization complexity |
| SFT | Behavior learned from instruction-response pairs | Teaches instruction following | Copies patterns/limitations of SFT data |
| Reward-model + PPO | Policy optimized from learned reward | Flexible preference optimization | Complex and expensive |
| DPO | Direct chosen-vs-rejected optimization | Simpler preference tuning | Depends strongly on preference data/reference setup |

---

## 56. A practical decision guide

### You have substantial compute and need maximum task adaptation

Consider:

```text
full fine-tuning
```

### You need multiple small specializations on one base model

Consider:

```text
adapters
or
LoRA
```

### GPU memory is the main constraint

Consider:

```text
QLoRA
```

### The base model does not reliably follow instructions

Use:

```text
SFT / instruction tuning
```

### The model follows instructions but produces undesirable response styles

Consider:

```text
preference tuning
```

### You want preference tuning without a separately trained reward model

Consider:

```text
DPO-style training
```

The correct choice depends on:

- data,
- compute,
- desired behavior,
- deployment architecture,
- evaluation requirements.

---

## 57. Put the complete chapter together

The full chapter pipeline can be summarized as:

### Stage A — Base model

```text
large unlabeled corpus
→ next-token pretraining
→ base LLM
```

### Stage B — Instruction tuning

```text
base LLM
+
instruction-response data
+
full fine-tuning or PEFT/QLoRA
→ instruction model
```

### Stage C — Evaluation

```text
word-level metrics
benchmarks
LLM judge
human evaluation
domain tests
```

### Stage D — Preference tuning

Either:

```text
preference data
→ reward model
→ PPO
→ aligned LLM
```

or:

```text
preference data
+
reference model
→ DPO
→ aligned LLM
```

### Stage E — Deployment validation

Evaluate:

- instruction following,
- task quality,
- domain accuracy,
- safety behavior,
- latency,
- memory,
- cost,
- preference consistency.

[[IMAGE_NEEDED: Complete generative fine-tuning lifecycle | Show pretraining → base LLM → SFT with LoRA/QLoRA option → instruction model → evaluation → reward-model/PPO or DPO preference tuning → aligned model → deployment evaluation | Learner should use this as the final mental map for Chapter 12]]

---

{{exercise:M12.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> A base language model is already an instruction-following assistant.

### Why this is wrong

Pretraining primarily teaches next-token prediction. Instruction following is learned through later adaptation such as SFT.

---

### Misconception 2

> SFT uses a completely different prediction mechanism from language modeling.

### Why this is wrong

SFT still trains next-token prediction; the important change is that the training sequence is organized around labeled instruction-response examples.

---

### Misconception 3

> PEFT means the base model is small.

### Why this is wrong

The base model can still be huge. PEFT means only a small parameter subset is trained.

---

### Misconception 4

> LoRA replaces the original base weight matrices.

### Why this is wrong

The base matrices are typically frozen and LoRA learns a low-rank update that is added to them.

---

### Misconception 5

> Higher LoRA rank is always better.

### Why this is wrong

Higher rank increases adaptation capacity but also increases memory, parameter count, and compute.

---

### Misconception 6

> Quantization only matters for inference.

### Why this is wrong

QLoRA uses quantized base weights specifically to reduce fine-tuning memory requirements.

---

### Misconception 7

> A low perplexity model must be more useful.

### Why this is wrong

Perplexity measures language-model predictive confidence, not every quality dimension such as correctness, helpfulness, safety, or creativity.

---

### Misconception 8

> A high public leaderboard rank guarantees the model is best for my application.

### Why this is wrong

Public benchmarks can differ from your domain and may be subject to overfitting or contamination.

---

### Misconception 9

> LLM-as-a-judge removes the need for human evaluation.

### Why this is wrong

Judge models have their own biases and limitations. Humans remain important for domain-specific and preference-sensitive evaluation.

---

### Misconception 10

> Preference tuning discovers universally correct preferences.

### Why this is wrong

It learns the preferences represented by the training data and evaluators.

---

### Misconception 11

> DPO requires training a separate scalar reward model.

### Why this is wrong

DPO directly optimizes chosen versus rejected responses using the trainable and reference models.

---

### Misconception 12

> SFT and DPO solve the same problem.

### Why this is wrong

SFT teaches desired response behavior from demonstrations; DPO further adjusts which responses are preferred among alternatives.

---

## Key terminology

| Term | Meaning |
|---|---|
| Base model | Pretrained generative model optimized primarily through language modeling |
| Language modeling | Learning to predict tokens from preceding context |
| SFT | Supervised Fine-Tuning using labeled instruction-response examples |
| Instruction tuning | SFT focused on teaching a model to follow user instructions |
| Full fine-tuning | Updating all or most model parameters |
| PEFT | Parameter-Efficient Fine-Tuning |
| Adapter | Small trainable module inserted into a mostly frozen model |
| LoRA | Low-Rank Adaptation; trains compact low-rank weight updates |
| Rank `r` | Dimensionality/capacity of the LoRA update |
| `lora_alpha` | Scaling factor controlling LoRA update strength |
| Target modules | Model matrices/layers that receive LoRA updates |
| Quantization | Representing weights with reduced numerical precision |
| QLoRA | Quantized base model combined with LoRA fine-tuning |
| NF4 | Normalized 4-bit quantization format used in the chapter’s QLoRA example |
| Double quantization | Quantization of additional quantization-related values for further memory savings |
| Gradient accumulation | Combining gradients across several mini-batches before one optimizer step |
| Gradient checkpointing | Saving memory by recomputing some activations during backward passes |
| Perplexity | Metric reflecting how surprised a language model is by observed text |
| ROUGE | Reference-overlap-oriented generation metric, often used for summarization |
| BLEU | N-gram-overlap-oriented generation metric, historically common in translation |
| BERTScore | Semantic/reference similarity metric based on contextual representations |
| Benchmark | Standardized evaluation dataset/task |
| LLM-as-a-judge | Using another LLM to assess generated output |
| Human evaluation | People judging outputs according to task quality or preference |
| Goodhart’s Law | Warning that optimizing directly for a measure can distort its usefulness |
| Preference tuning | Fine-tuning based on preferred versus less-preferred behavior |
| Alignment | Adapting model behavior toward specified human/system preferences |
| Reward model | Model producing a scalar preference/quality score for a response |
| Chosen response | Preferred response in a preference pair |
| Rejected response | Less-preferred response in a preference pair |
| RLHF | Reinforcement Learning from Human Feedback |
| PPO | Proximal Policy Optimization |
| DPO | Direct Preference Optimization |
| Reference model | Frozen model used as a behavioral baseline during DPO |
| ORPO | Preference-optimization approach mentioned by the chapter that combines SFT/preference ideas in one process |

---

## Self-check

Before moving on, make sure you can answer:

1. What are the three major LLM training stages described in the chapter?
2. Why might a base model continue a question instead of answering it?
3. What does SFT teach that pretraining does not directly teach?
4. How does full fine-tuning differ from PEFT?
5. What problem do adapters solve?
6. What does LoRA learn?
7. Why can a low-rank update use far fewer parameters than a full weight matrix?
8. What does the LoRA rank control?
9. What does `lora_alpha` influence?
10. What are target modules?
11. What does quantization trade?
12. Why is QLoRA memory-efficient?
13. What is NF4 in the chapter’s setup?
14. Why must instruction data follow the target chat template?
15. What does gradient accumulation accomplish?
16. What tradeoff does gradient checkpointing make?
17. Why might LoRA weights be kept separately from the base model?
18. Why might you merge a LoRA adapter before deployment?
19. Why is generative-model evaluation more difficult than ordinary classification evaluation?
20. What does perplexity measure?
21. Why is perplexity insufficient by itself?
22. Name at least four benchmarks mentioned by the chapter.
23. What problem can arise when a benchmark becomes a training target?
24. What is LLM-as-a-judge?
25. Why is human evaluation still important?
26. What is preference tuning?
27. What does a reward model output?
28. What is the difference between chosen and rejected responses?
29. What are the three broad stages of reward-model-based preference tuning?
30. What is PPO used for in the chapter?
31. Why is PPO-style RLHF relatively complex?
32. What does DPO remove from the classic reward-model pipeline?
33. What is the role of the frozen reference model in DPO?
34. Why does the chapter perform SFT before DPO?
35. How can QLoRA be used during both SFT and preference tuning?
36. What does ORPO attempt to simplify?
37. Design an end-to-end plan for adapting a base model into a domain-specific assistant under limited GPU memory.

---

## Retain this idea

**Fine-tuning a generative model is not one operation but a sequence of behavior-shaping stages. Pretraining gives the model broad language capability. Supervised fine-tuning teaches it how to respond to instructions. PEFT methods such as LoRA reduce the number of trainable parameters, and QLoRA further reduces memory by quantizing the frozen base model. Evaluation must combine task-specific metrics, benchmarks, automated judges, and human judgment rather than relying on one score. Preference tuning then refines which acceptable responses the model should favor, either through reward-model-based RLHF/PPO or direct methods such as DPO. The quality of every stage depends heavily on its data, objective, and evaluation—not just on model size.**
"""
        ),

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "three-stage-roadmap", "title": "The three-stage path from base model to aligned assistant", "order": 1},
            {"id": "pretraining", "title": "Stage 1 — Pretraining creates the base model", "order": 2},
            {"id": "base-model-behavior", "title": "A base model is a completion engine, not automatically an instruction follower", "order": 3},
            {"id": "sft", "title": "Stage 2 — Supervised Fine-Tuning teaches instruction following", "order": 4},
            {"id": "full-finetuning", "title": "Full fine-tuning updates all model parameters", "order": 5},
            {"id": "peft", "title": "Parameter-Efficient Fine-Tuning: adapt less of the model", "order": 6},
            {"id": "adapters", "title": "Adapters: insert small trainable modules", "order": 7},
            {"id": "adapter-swapping", "title": "Adapters make specialization modular", "order": 8},
            {"id": "lora", "title": "LoRA: represent weight updates with low-rank matrices", "order": 9},
            {"id": "low-rank-intuition", "title": "Why low rank saves parameters", "order": 10},
            {"id": "lora-what-to-target", "title": "LoRA does not need to modify every matrix", "order": 11},
            {"id": "lora-config", "title": "Understand the main LoRA hyperparameters", "order": 12},
            {"id": "quantization", "title": "Quantization reduces the memory needed for base weights", "order": 13},
            {"id": "quantization-problem", "title": "Naive quantization can collapse nearby values", "order": 14},
            {"id": "qlora", "title": "QLoRA: quantize the base model, train LoRA updates", "order": 15},
            {"id": "blockwise-quantization", "title": "Blockwise and distribution-aware quantization", "order": 16},
            {"id": "nf4", "title": "NF4 and double quantization in the chapter", "order": 17},
            {"id": "instruction-data", "title": "Instruction tuning requires correctly formatted conversations", "order": 18},
            {"id": "ultrachat", "title": "The chapter’s instruction dataset", "order": 19},
            {"id": "tinyllama", "title": "Start from a base TinyLlama checkpoint", "order": 20},
            {"id": "model-quantization-code", "title": "Load the base model in 4-bit form", "order": 21},
            {"id": "apply-lora", "title": "Attach LoRA to the selected model modules", "order": 22},
            {"id": "training-config", "title": "Configure efficient training", "order": 23},
            {"id": "gradient-checkpointing", "title": "Gradient checkpointing trades compute for memory", "order": 24},
            {"id": "lr-scheduler", "title": "Learning-rate scheduling changes the update size over time", "order": 25},
            {"id": "sfttrainer", "title": "Train with an SFT-specific trainer", "order": 26},
            {"id": "merge-lora", "title": "LoRA weights can remain separate or be merged", "order": 27},
            {"id": "instruction-result", "title": "After SFT, the model behaves more like an assistant", "order": 28},
            {"id": "eval-problem", "title": "Generative-model evaluation is inherently multidimensional", "order": 29},
            {"id": "word-metrics", "title": "Word-level and sequence-level metrics", "order": 30},
            {"id": "perplexity", "title": "Perplexity measures predictive surprise", "order": 31},
            {"id": "benchmarks", "title": "Public benchmarks evaluate different capabilities", "order": 32},
            {"id": "leaderboards", "title": "Leaderboards aggregate benchmarks—but can become targets", "order": 33},
            {"id": "llm-judge", "title": "LLM-as-a-judge evaluates open-ended quality", "order": 34},
            {"id": "human-eval", "title": "Human evaluation remains essential", "order": 35},
            {"id": "goodhart", "title": "Goodhart’s Law: do not optimize blindly for one metric", "order": 36},
            {"id": "preference-tuning", "title": "Stage 3 — Preference tuning shapes which answers are preferred", "order": 37},
            {"id": "preference-score", "title": "Preferences can be represented as scores or comparisons", "order": 38},
            {"id": "reward-model", "title": "Reward models automate preference scoring", "order": 39},
            {"id": "preference-data", "title": "Preference data often contains chosen and rejected responses", "order": 40},
            {"id": "collect-preferences", "title": "One way to collect preference data", "order": 41},
            {"id": "train-reward-model", "title": "Train the reward model to rank chosen above rejected", "order": 42},
            {"id": "rlhf-pipeline", "title": "The classic reward-model-based alignment pipeline", "order": 43},
            {"id": "ppo", "title": "PPO uses reward feedback to optimize the instruction-tuned model", "order": 44},
            {"id": "ppo-cost", "title": "Reward-model-based PPO is powerful but complex", "order": 45},
            {"id": "dpo", "title": "DPO: optimize preferences directly", "order": 46},
            {"id": "dpo-logprobs", "title": "DPO uses generation probabilities as the comparison signal", "order": 47},
            {"id": "dpo-data", "title": "Prepare alignment data for DPO", "order": 48},
            {"id": "dpo-model", "title": "Preference tuning starts from an already instruction-tuned model", "order": 49},
            {"id": "dpo-qlora", "title": "The chapter also applies PEFT to DPO", "order": 50},
            {"id": "dpo-config", "title": "DPO training introduces its own configuration", "order": 51},
            {"id": "merge-two-adapters", "title": "Merge the SFT and DPO adaptations", "order": 52},
            {"id": "sft-dpo-cost", "title": "SFT + DPO improves behavior but requires two training loops", "order": 53},
            {"id": "alignment-data-risk", "title": "Preference tuning does not create an objective definition of good", "order": 54},
            {"id": "method-comparison", "title": "Compare the main fine-tuning methods", "order": 55},
            {"id": "decision-guide", "title": "A practical decision guide", "order": 56},
            {"id": "end-to-end", "title": "Put the complete chapter together", "order": 57},
            {"id": "misconceptions", "title": "Important misconceptions", "order": 58},
            {"id": "terminology", "title": "Key terminology", "order": 59},
            {"id": "self-check", "title": "Self-check", "order": 60},
            {"id": "retain", "title": "Retain this idea", "order": 61},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M12.L01.EX01",

            "title": "Design and Evaluate a QLoRA Instruction-Tuning Experiment",

            "lesson_code": "M12.L01",

            "section_id": "goodhart",

            "placement": "after_section",

            "description": (
                "Design an instruction-tuning experiment that connects data formatting, "
                "QLoRA configuration, memory-efficient training, and multidimensional evaluation."
            ),

            "instructions": (
                "Assume you have a small base generative model and 5,000 instruction-response "
                "examples for a domain assistant.\n"
                "1. Define the chat/instruction template and show one formatted example.\n"
                "2. Explain why the base model should use the same interface format during inference.\n"
                "3. Define a 4-bit QLoRA setup at a conceptual level: quantized base weights, "
                "LoRA rank, alpha, dropout, and target modules.\n"
                "4. Explain how you would choose a rank and what tradeoff increasing it creates.\n"
                "5. Define training batch size and gradient accumulation, and compute the "
                "effective batch size.\n"
                "6. Decide whether to use gradient checkpointing and justify the memory/compute tradeoff.\n"
                "7. Define at least four evaluation dimensions. Include one automatic "
                "reference-based metric, one task benchmark/check, one LLM-judge-style "
                "evaluation, and one human evaluation.\n"
                "8. Create five custom prompts that represent your real deployment domain.\n"
                "9. Compare the base and SFT model on those prompts.\n"
                "10. Explain one way a benchmark-only optimization strategy could mislead you."
            ),

            "expected_output": (
                "A complete QLoRA/SFT experiment design including formatted data, PEFT "
                "configuration, effective batch calculation, memory-saving choices, "
                "evaluation rubric, domain prompts, and a base-versus-SFT comparison plan."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "instruction-tuning",
                "qlora",
                "lora-configuration",
                "gradient-accumulation",
                "evaluation-design",
                "human-evaluation",
                "goodharts-law",
            ],
        },

        {
            "id": "M12.L01.EX02",

            "title": "Design an SFT + Preference-Tuning Pipeline",

            "lesson_code": "M12.L01",

            "section_id": "end-to-end",

            "placement": "after_section",

            "description": (
                "Design a realistic pipeline that takes a base model through instruction "
                "tuning, preference data collection, and DPO-style alignment."
            ),

            "instructions": (
                "Assume you want to adapt a small open base model into a customer-support assistant.\n"
                "1. Define the SFT dataset schema and give two instruction-response examples.\n"
                "2. Decide between full fine-tuning and QLoRA for SFT and explain why.\n"
                "3. Define the behavior you want the SFT model to learn before preference tuning.\n"
                "4. Create a preference-data schema containing prompt, chosen, and rejected responses.\n"
                "5. Write three example preference pairs where both answers are plausible "
                "but one is better according to a clear policy.\n"
                "6. Explain how a reward-model + PPO solution would use those preferences.\n"
                "7. Explain how DPO would use the same preferences without training a separate reward model.\n"
                "8. Define at least five evaluation dimensions for the final model, including "
                "task correctness, instruction following, safety/policy adherence, style, and latency.\n"
                "9. Define what data-quality checks must run before DPO training.\n"
                "10. Explain what you would monitor to detect over-alignment, reward hacking, "
                "verbosity drift, or loss of useful base-model capabilities."
            ),

            "expected_output": (
                "An end-to-end architecture from base model through SFT and DPO, including "
                "dataset schemas, PEFT choice, preference examples, PPO-versus-DPO comparison, "
                "evaluation plan, and alignment-risk monitoring."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "sft",
                "preference-data",
                "reward-models",
                "ppo",
                "dpo",
                "alignment",
                "evaluation",
                "risk-analysis",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M12.L01.QZ01",

        "title": "Fine-Tuning Generation Models — Knowledge Check",

        "lesson_code": "M12.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M12.L01.Q01",
                "section_id": "three-stage-roadmap",
                "question": "Which ordering matches the chapter’s common LLM training pipeline?",
                "options": [
                    "Preference tuning → pretraining → SFT",
                    "Pretraining → supervised fine-tuning → preference tuning",
                    "SFT → tokenization → clustering",
                    "Quantization → pretraining → retrieval",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter presents language-model pretraining first, then instruction "
                    "tuning/SFT, then preference tuning."
                ),
            },
            {
                "id": "M12.L01.Q02",
                "section_id": "base-model-behavior",
                "question": "Why might a base model continue a question instead of directly answering it?",
                "options": [
                    "Because pretraining primarily teaches next-token continuation rather than instruction-following behavior.",
                    "Because base models cannot generate text.",
                    "Because tokenizers remove question marks.",
                    "Because preference tuning happens before pretraining.",
                ],
                "correct": 0,
                "explanation": (
                    "A base model learns plausible text continuation. SFT later teaches "
                    "the conversational instruction-following pattern."
                ),
            },
            {
                "id": "M12.L01.Q03",
                "section_id": "sft",
                "question": "What is the main purpose of supervised fine-tuning in this chapter?",
                "options": [
                    "Teach a base generative model to follow instructions using instruction-response examples.",
                    "Compress the tokenizer vocabulary.",
                    "Create only image embeddings.",
                    "Replace language modeling with clustering.",
                ],
                "correct": 0,
                "explanation": (
                    "SFT conditions next-token learning on curated instruction-response "
                    "demonstrations."
                ),
            },
            {
                "id": "M12.L01.Q04",
                "section_id": "peft",
                "question": "What problem is PEFT designed to reduce?",
                "options": [
                    "The cost of updating the entire model during task adaptation.",
                    "The number of training examples to exactly zero.",
                    "The need for a tokenizer.",
                    "The model context window.",
                ],
                "correct": 0,
                "explanation": (
                    "PEFT trains a much smaller parameter subset while retaining the "
                    "large pretrained model."
                ),
            },
            {
                "id": "M12.L01.Q05",
                "section_id": "lora",
                "question": "What does LoRA learn?",
                "options": [
                    "A compact low-rank update to frozen model weight matrices.",
                    "A completely new tokenizer.",
                    "Only a scalar reward score.",
                    "A vector database index.",
                ],
                "correct": 0,
                "explanation": (
                    "LoRA represents the task-specific weight change using small low-rank matrices."
                ),
            },
            {
                "id": "M12.L01.Q06",
                "section_id": "lora-config",
                "question": "What does increasing LoRA rank `r` generally do?",
                "options": [
                    "Increases adaptation capacity and trainable parameter count.",
                    "Removes all LoRA parameters.",
                    "Forces the base model to 1-bit precision.",
                    "Prevents target-module selection.",
                ],
                "correct": 0,
                "explanation": (
                    "A larger rank provides a richer update but reduces the efficiency advantage."
                ),
            },
            {
                "id": "M12.L01.Q07",
                "section_id": "qlora",
                "question": "What is the central QLoRA idea?",
                "options": [
                    "Keep the base model quantized/frozen while training small LoRA updates.",
                    "Train every base-model parameter in float64.",
                    "Remove the Transformer layers.",
                    "Use only a reward model.",
                ],
                "correct": 0,
                "explanation": (
                    "QLoRA combines low-precision base-model storage with parameter-efficient LoRA training."
                ),
            },
            {
                "id": "M12.L01.Q08",
                "section_id": "instruction-data",
                "question": "Why should SFT data use the model’s expected chat template?",
                "options": [
                    "The role and message-boundary structure is part of the model interface the model learns to respond to.",
                    "Templates increase model parameter count.",
                    "Templates replace the training objective.",
                    "Templates eliminate the need for a tokenizer.",
                ],
                "correct": 0,
                "explanation": (
                    "Correct role formatting teaches and preserves the intended conversational interface."
                ),
            },
            {
                "id": "M12.L01.Q09",
                "section_id": "training-config",
                "question": "What does gradient accumulation allow?",
                "options": [
                    "Accumulating gradients across several small mini-batches before one optimizer step.",
                    "Changing chosen responses into rejected responses.",
                    "Merging two tokenizers.",
                    "Removing all optimizer state.",
                ],
                "correct": 0,
                "explanation": (
                    "Gradient accumulation simulates a larger effective batch without "
                    "requiring all examples in memory at once."
                ),
            },
            {
                "id": "M12.L01.Q10",
                "section_id": "gradient-checkpointing",
                "question": "What tradeoff does gradient checkpointing make?",
                "options": [
                    "Less activation memory in exchange for additional recomputation.",
                    "More memory with less compute.",
                    "Lower data quality for better tokenization.",
                    "Fewer model layers for more parameters.",
                ],
                "correct": 0,
                "explanation": (
                    "Some intermediate activations are recomputed during backward passes "
                    "instead of being kept in memory."
                ),
            },
            {
                "id": "M12.L01.Q11",
                "section_id": "perplexity",
                "question": "What does perplexity primarily measure?",
                "options": [
                    "How well the model predicts observed token sequences.",
                    "Human preference for response style.",
                    "GPU memory consumption.",
                    "Whether citations are correct.",
                ],
                "correct": 0,
                "explanation": (
                    "Perplexity is tied to next-token likelihood and predictive surprise."
                ),
            },
            {
                "id": "M12.L01.Q12",
                "section_id": "goodhart",
                "question": "What lesson does Goodhart’s Law provide for LLM evaluation?",
                "options": [
                    "Optimizing aggressively for one metric can make that metric less representative of true overall quality.",
                    "Only one metric should ever be used.",
                    "Human evaluation is unnecessary.",
                    "Benchmark scores cannot be measured.",
                ],
                "correct": 0,
                "explanation": (
                    "A model can game or overfit a target measure while losing useful capabilities elsewhere."
                ),
            },
            {
                "id": "M12.L01.Q13",
                "section_id": "reward-model",
                "question": "What does a reward model output?",
                "options": [
                    "A scalar score representing the quality/preference of a response for a prompt.",
                    "A full vector index.",
                    "A new tokenizer vocabulary.",
                    "Only the next token.",
                ],
                "correct": 0,
                "explanation": (
                    "Reward models convert prompt-response pairs into a preference-related scalar."
                ),
            },
            {
                "id": "M12.L01.Q14",
                "section_id": "preference-data",
                "question": "What is the common structure of preference-training data described in the chapter?",
                "options": [
                    "Prompt + chosen response + rejected response",
                    "Image + label only",
                    "Document + cluster ID",
                    "Token + embedding dimension",
                ],
                "correct": 0,
                "explanation": (
                    "Pairwise preferences indicate which of two candidate responses is preferred."
                ),
            },
            {
                "id": "M12.L01.Q15",
                "section_id": "rlhf-pipeline",
                "question": "What are the three broad stages in reward-model-based preference tuning?",
                "options": [
                    "Collect preference data → train reward model → use reward model to fine-tune the LLM",
                    "Pretrain tokenizer → build vector database → cluster responses",
                    "SFT → image generation → NER",
                    "Quantize → delete base model → retrain tokenizer",
                ],
                "correct": 0,
                "explanation": (
                    "This is the classic reward-model-based alignment structure described "
                    "in the source."
                ),
            },
            {
                "id": "M12.L01.Q16",
                "section_id": "dpo",
                "question": "What does DPO remove compared with classic reward-model + PPO alignment?",
                "options": [
                    "The need to train a separate scalar reward model.",
                    "The need for any preference data.",
                    "The need for a language model.",
                    "The use of chosen and rejected responses.",
                ],
                "correct": 0,
                "explanation": (
                    "DPO directly uses preference pairs and reference/trainable model "
                    "probabilities instead of first learning a reward model."
                ),
            },
            {
                "id": "M12.L01.Q17",
                "section_id": "dpo-model",
                "question": "Why does the chapter apply DPO after SFT?",
                "options": [
                    "SFT first teaches instruction-following behavior; DPO then adjusts which acceptable responses are preferred.",
                    "DPO cannot process text before SFT tokenization.",
                    "SFT quantizes the model automatically.",
                    "Preference data is only available during pretraining.",
                ],
                "correct": 0,
                "explanation": (
                    "The two stages solve different behavioral problems and are therefore applied sequentially."
                ),
            },
            {
                "id": "M12.L01.Q18",
                "section_id": "end-to-end",
                "type": "open",
                "question": (
                    "Design a complete low-memory fine-tuning pipeline that starts from a "
                    "base generative model and ends with a preference-aligned assistant. "
                    "Include instruction data, chat templating, QLoRA, SFT, evaluation, "
                    "preference-data collection, DPO, adapter merging, and at least four "
                    "risks or checks you would monitor before deployment."
                ),
            },
        ],

        "passing_score": 70,
    },
}
