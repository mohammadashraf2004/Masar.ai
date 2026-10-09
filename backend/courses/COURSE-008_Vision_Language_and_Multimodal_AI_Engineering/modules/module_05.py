"""M01.L05 — Post-Training Vision-Language Models.

One chapter -> one complete learner-facing lesson + inline manual images +
inline exercises + lesson quiz.

Source: Chapter 5, "Post-Training Vision Language Models".
Page numbers were not provided in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M01.L05"
MODULE_ORDER = 1
MODULE_TITLE = "Foundations of Vision and Language"
MODULE_DESCRIPTION = (
    "Adapt a pretrained VLM efficiently using supervised fine-tuning, LoRA/DoRA, "
    "quantization and QLoRA, then understand multimodal alignment through RLHF, "
    "DPO, MPO, and GRPO."
)
SOURCE_CHAPTER = 5
SOURCE_PAGES = "Chapter 5 — page numbers not provided"


TOPIC = {
    "title": "Post-Training Vision-Language Models",
    "slug": "vision-language-m01-l05",
    "description": (
        "Learn how modern VLMs are adapted after pretraining: supervised fine-tuning, "
        "prompt masking, parameter-efficient fine-tuning with LoRA and DoRA, "
        "quantization and QLoRA, TRL-based SFT, human-preference alignment, "
        "reward models, PPO, DPO, MPO, online preference optimization, GRPO, "
        "and verifiable rewards."
    ),
    "order": 5,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 5.0,
    "skill_tags": [
        "vlm-post-training",
        "supervised-fine-tuning",
        "sft",
        "prompt-masking",
        "peft",
        "lora",
        "dora",
        "quantization",
        "qlora",
        "bitsandbytes",
        "trl",
        "rlhf",
        "reward-model",
        "ppo",
        "dpo",
        "mpo",
        "grpo",
        "rlvr",
        "multimodal-alignment",
    ],
    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
    ],

    "lesson": {
        "title": "Post-Training Vision-Language Models",
        "content": r"""
# Post-Training Vision-Language Models

> **Lesson:** M01.L05  
> **Module:** Foundations of Vision and Language  
> **Source alignment:** Chapter 5, *Post-Training Vision Language Models*.  
> Page numbers were not included in the supplied source.  
> This lesson is an instructor-authored educational adaptation.

---

## Why post-training matters

Earlier lessons focused on how a VLM is assembled and trained.

But in practical work, you rarely begin with a completely untrained model.

More often, you begin with:

```text
a pretrained vision encoder
+
a pretrained language model
+
a multimodal model that already understands many image-language relationships
```

Then you adapt that model to behave the way you need.

That adaptation stage is **post-training**.

The source presents three major ingredients:

```text
1. Supervised fine-tuning (SFT)
2. Alignment / preference optimization
3. Reinforcement learning with verifiable rewards (RLVR)
```

A useful mental model is:

```text
PRETRAINED MODEL
       ↓
SFT
"learn the task and instruction format"
       ↓
ALIGNMENT
"prefer better responses"
       ↓
VERIFIABLE-RL when appropriate
"optimize against automatically checkable rewards"
```

This lesson will also cover the efficiency techniques that make this practical:

```text
LoRA
DoRA
quantization
QLoRA
PEFT
TRL
```

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain how post-training differs from broad pretraining.
- Format multimodal supervised examples as system/user/assistant conversations.
- Explain the purpose of chat templates and generation-trigger tokens.
- Explain why prompt masking prevents the model from wasting loss on user/system input.
- Define matrix rank intuitively.
- Explain the core LoRA update \(W' = W + BA\) and why it reduces trainable parameters.
- Explain the role of LoRA rank and alpha.
- Explain how DoRA separates magnitude from direction.
- Describe the trade-off between full fine-tuning and parameter-efficient fine-tuning.
- Explain why quantization reduces memory use.
- Compare FP32, FP16/BF16, int8 and low-bit representations at a conceptual level.
- Explain the idea behind QLoRA and NF4.
- Build the conceptual steps of a TRL SFT pipeline.
- Explain the purpose of a reward model in RLHF.
- Distinguish a policy model from a reference model.
- Explain why KL regularization is added during alignment.
- Explain the difference between PPO-style RLHF and DPO.
- Interpret chosen/rejected preference data.
- Explain the high-level DPO objective and the role of beta.
- Explain how MPO combines preference and generation objectives.
- Explain why online preference generation can reduce distribution mismatch.
- Explain the core GRPO loop.
- Explain the idea of reinforcement learning with verifiable rewards.
- Choose an appropriate post-training method for a concrete VLM adaptation task.
- Recognize implementation inconsistencies in example training code before running expensive jobs.

---

## 1. A map of post-training

Suppose you already have a general VLM.

It can:

- describe images;
- answer basic questions;
- understand common objects;
- follow some instructions.

But you need it to become better at:

```text
document QA
medical imagery
computer use
industrial inspection
robot instructions
or another specialized task
```

You could retrain every parameter.

But that may be:

- expensive;
- memory intensive;
- slow;
- unnecessary.

So modern post-training asks two separate questions.

### Question 1 — What should the model learn to do?

This is often answered with **SFT**.

```text
prompt + image → desired response
```

### Question 2 — Which response should the model prefer?

This is the domain of **alignment**.

```text
response A vs response B
→ which one is better?
```

### Question 3 — Can correctness be checked automatically?

If yes, the task may support a **verifiable reward**.

Examples in the source include things like:

- mathematical correctness;
- code results.

[[IMAGE_NEEDED: Post-training roadmap |
Show pretrained VLM branching into SFT, preference alignment, and verifiable-reward optimization, with LoRA/DoRA/QLoRA shown as efficiency tools underneath |
Learner should distinguish the learning objective from the efficiency method]]

---

## 2. Supervised fine-tuning

Supervised fine-tuning is supervised learning applied to a pretrained model.

You provide:

```text
input
+
target output
```

and optimize the model so that the target becomes more likely.

For a VLM:

```text
image
+
user instruction
→
assistant answer
```

Example:

```text
Image: a document page

User:
"What date is shown on this letter?"

Assistant:
"1/8/93"
```

The model already understands language and images.

Fine-tuning teaches it:

- the target task;
- the desired response style;
- the domain;
- the instruction format.

### Fine-tuning does not necessarily mean "learn a totally new capability"

It may instead:

- improve an existing capability;
- specialize it;
- make output more reliable;
- adapt the model to your domain.

---

## 3. Multimodal chat formatting

A multimodal SFT example often contains several roles.

Conceptually:

```text
SYSTEM
"You are a helpful assistant."

USER
[image]
"Describe this image."

ASSISTANT
"This is the image of a bee."
```

The source demonstrates this using a Transformers processor.

A simplified version is:

```python
from transformers import AutoProcessor

processor = AutoProcessor.from_pretrained(
    "Qwen/Qwen3-VL-8B-Instruct"
)

messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are a helpful assistant.",
            }
        ],
    },
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "IMAGE_SOURCE",
            },
            {
                "type": "text",
                "text": "Describe this image.",
            },
        ],
    },
]
```

The processor's chat template can insert model-specific special tokens.

The source shows a rendered form conceptually similar to:

```text
<system-start>
You are a helpful assistant.
<system-end>

<user-start>
<vision-start><image><vision-end>
Describe this image.
<user-end>

<assistant-start>
```

### Why use a processor?

Without it, you would have to manually understand:

- role tokens;
- visual placeholders;
- generation markers;
- model-specific formatting rules.

That is easy to get wrong.

### Training and inference are formatted differently

During **inference**, you usually need a generation marker:

```text
assistant starts here →
```

because the response does not exist yet.

During **training**, the target assistant response already exists.

So the conversation includes it directly.

Example:

```python
messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "image": "IMAGE_SOURCE"},
            {"type": "text", "text": "Describe this image."},
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "This is the image of a bee.",
            }
        ],
    },
]
```

[[IMAGE_NEEDED: Multimodal SFT chat template |
Show system → user(image + text) → assistant(target answer), and distinguish inference formatting from training formatting |
Learner should understand where the target response lives during supervised training]]

---

## 4. Prompt masking: train on the answer, not the prompt

If we train an autoregressive model on the whole formatted sequence, it could
receive loss on:

```text
system prompt
user prompt
image placeholder tokens
assistant response
```

But our main objective is usually:

> Given the context, generate the correct assistant answer.

So we mask the prompt portion.

Conceptually:

```text
SYSTEM TOKENS      → ignore
USER TOKENS        → ignore
IMAGE INPUT        → ignore as language targets
ASSISTANT ANSWER   → compute loss
```

A label sequence might look like:

```text
[-100, -100, -100, -100, 512, 912, 44, 2]
```

where:

```text
-100 → do not include this position in cross-entropy loss
```

This is called **prompt masking**.

### Why it matters

Without prompt masking, the model spends training signal on reproducing the
question and system instructions.

That is not normally the behavior we want to optimize.

The source notes that TRL handles this kind of training behavior for the
workflow it demonstrates.

{{exercise:M01.L05.EX01}}

---

## 5. Parameter-efficient fine-tuning

A large VLM may contain billions of parameters.

Full fine-tuning means computing and storing updates for a large fraction of
them.

This requires substantial:

- GPU memory;
- optimizer memory;
- gradient storage;
- compute.

**Parameter-Efficient Fine-Tuning (PEFT)** reduces this burden.

The core idea is:

> Keep most pretrained parameters frozen and train only a small set of new or
> selected parameters.

The chapter focuses on:

- LoRA;
- DoRA.

---

## 6. Matrix rank: the intuition you need for LoRA

Suppose a weight matrix is:

```text
W ∈ R^(d × k)
```

A full update:

```text
ΔW
```

also has:

```text
d × k
```

entries.

LoRA assumes that the useful update can often be represented by a much
lower-rank structure.

Instead of directly training:

```text
ΔW ∈ R^(d × k)
```

we train two smaller matrices:

```text
B ∈ R^(d × r)
A ∈ R^(r × k)
```

Then:

```text
ΔW = BA
```

with:

```text
r << min(d, k)
```

### What does rank mean intuitively?

Rank is the number of independent directions/components needed to represent a
matrix transformation.

You can think of:

```text
small rank
→ stronger compression
→ fewer trainable parameters

large rank
→ more expressive update
→ more trainable parameters
```

---

## 7. LoRA: learn a low-rank update

The original pretrained matrix stays frozen:

```text
W
```

LoRA adds:

```text
ΔW = BA
```

so the effective weight becomes:

```text
W' = W + scale × BA
```

The source describes the scale as:

```text
alpha / r
```

where:

- `alpha` controls adapter contribution;
- `r` is the rank.

### Parameter-count intuition

Suppose:

```text
W shape = 4096 × 4096
```

Full matrix:

```text
16,777,216 parameters
```

If LoRA uses:

```text
r = 8
```

then:

```text
B: 4096 × 8 = 32,768
A: 8 × 4096 = 32,768
```

Total adapter parameters:

```text
65,536
```

instead of more than 16 million for that matrix.

This is why LoRA can drastically reduce trainable parameter count.

{{image:lora-low-rank-adaptation}}

### Choosing rank

Higher rank:

- more expressive;
- more memory;
- more trainable parameters.

Lower rank:

- cheaper;
- more constrained.

The source gives small values such as:

```text
2
4
8
```

as common examples for experimentation.

These are not universal optimum values.

---

## 8. DoRA: separate magnitude and direction

The source presents **DoRA** as an extension of LoRA.

Instead of treating a weight only as one matrix, DoRA decomposes it into:

```text
magnitude
+
direction
```

Then:

- magnitude remains trainable;
- direction receives a LoRA-style low-rank update.

Conceptually:

```text
original weight
   ↓
magnitude × direction
                 ↓
          low-rank update
```

This gives the adaptation more control over how the pretrained weight changes.

{{image:dora-weight-decomposition}}

### PEFT trade-off

The source emphasizes an important caveat:

```text
PEFT updates fewer parameters
```

so it may learn less than full fine-tuning in some settings.

But it also tends to keep the adapted model closer to its starting point.

That can mean:

```text
less adaptation
+
less forgetting
```

This is a trade-off, not simply "PEFT is always better."

---

## 9. Injecting LoRA/DoRA adapters with PEFT

The source demonstrates a configuration like:

```python
from peft import LoraConfig, get_peft_model

peft_config = LoraConfig(
    r=8,
    lora_alpha=8,
    lora_dropout=0.1,
    target_modules=[
        "down_proj",
        "o_proj",
        "k_proj",
        "q_proj",
        "gate_proj",
        "up_proj",
        "v_proj",
    ],
    use_dora=True,
    init_lora_weights="gaussian",
)

peft_model = get_peft_model(
    model,
    peft_config,
)
```

### What each option means

#### `r`

Low-rank dimension.

#### `lora_alpha`

Controls adapter update scaling.

#### `lora_dropout`

Regularization applied in the adapter path.

#### `target_modules`

Which linear layers receive adapters.

#### `use_dora=True`

Switches from ordinary LoRA behavior to DoRA-style adaptation in the source's
example.

### Trainable-parameter inspection

The source shows an example where only a tiny percentage of the full model
becomes trainable.

The important lesson is:

> Always inspect the actual trainable parameter count rather than assuming your
> adapter configuration worked.

{{exercise:M01.L05.EX02}}

---

## 10. Quantization: reduce numerical precision

Another way to reduce memory is to store weights using fewer bits.

Common representations discussed in the chapter include:

```text
FP32
FP16
BF16
INT8
lower-bit formats such as 4-bit NF4
```

### The central trade-off

```text
higher precision
→ more memory
→ wider numeric representation

lower precision
→ less memory
→ possible approximation error
```

Quantization can make a model fit on hardware that could not otherwise store
it.

### 8-bit intuition

The source describes a mixed approach where:

- most computation can use lower-precision values;
- outlier values receive higher-precision treatment;
- results are dequantized back into a higher-precision computation path.

The exact library implementation is more complex than this teaching summary.

The stable concept is:

> Quantization compresses numerical representation to save memory while trying
> to preserve model quality.

### Source wording caution

The supplied chapter cites a performance number for an 8-bit quantization study,
but the sentence is incomplete in the provided text ("results in 0.36%
performance"). This lesson does **not** infer the missing wording.

---

## 11. QLoRA: quantized base model + trainable LoRA adapters

QLoRA combines:

```text
quantized frozen model
+
trainable low-rank adapters
```

The source describes the base model using 4-bit **NF4**.

### Why this helps

If the large pretrained weight matrices are:

- quantized;
- frozen;

then they need much less memory than a full-precision trainable copy.

Only the adapters are optimized.

### NF4

The source introduces **NormalFloat 4-bit (NF4)** as a 4-bit quantization method
designed for weight distributions associated with neural-network parameters.

The exact quantization mathematics is deferred by the source to a later chapter.

For this lesson, retain:

```text
NF4
→ low-bit representation for frozen model weights
```

### Double quantization

The source explains:

1. quantize model weights;
2. quantize the scaling constants used by that quantization.

That produces another memory saving.

### Example configuration

```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)
```

Then:

```python
model = AutoModelForImageTextToText.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    quantization_config=quantization_config,
)
```

### Mental model

```text
large frozen model
      ↓
stored in 4-bit form
      +
small trainable LoRA/DoRA adapter
      ↓
much smaller training-memory requirement
```

[[IMAGE_NEEDED: QLoRA memory concept |
Show a large frozen base model compressed to 4-bit NF4 with small full/trainable adapter matrices attached, contrasting it with a full-precision full-fine-tune |
Learner should understand which parameters are quantized, frozen, and trainable]]

---

## 12. TRL as a post-training toolkit

The chapter uses **TRL** to tie together:

- SFT;
- preference optimization;
- PEFT adapters;
- quantized loading;
- trainer abstractions.

A training stack can look like:

```text
Transformers
   ↓
model + processor

bitsandbytes
   ↓
quantized model loading

PEFT
   ↓
LoRA / DoRA adapters

TRL
   ↓
SFT / DPO / other trainer
```

This does not remove the need to understand the training process.

It reduces boilerplate.

---

## 13. End-to-end multimodal SFT example

The source demonstrates document VQA fine-tuning.

### Step 1 — Load a document QA dataset

The useful fields are:

```text
image
question
answers
```

### Step 2 — Convert each example to chat format

A source-aligned transformation is:

```python
def fill_template(sample):
    return {
        "images": [
            sample["image"]
        ],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": sample["image"],
                    },
                    {
                        "type": "text",
                        "text": sample["question"],
                    },
                ],
            },
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": sample["answers"][0],
                    }
                ],
            },
        ],
    }
```

### Step 3 — Quantize the base model

Use:

```text
4-bit NF4
+
double quantization
+
BF16 compute
```

as in the source example.

### Step 4 — Add adapters

Use `LoraConfig`.

### Step 5 — Configure training

The source uses an `SFTConfig` containing parameters such as:

- output directory;
- epochs;
- batch size;
- gradient accumulation;
- warmup;
- learning rate;
- weight decay;
- BF16;
- logging;
- checkpoint behavior.

### Step 6 — Train

Conceptually:

```python
from trl import SFTTrainer

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=eval_ds,
    peft_config=peft_config,
)

trainer.train()
```

### Important implementation lesson

A good trainer abstraction does not save you from:

- dataset mistakes;
- bad chat formatting;
- incorrect labels;
- wrong processor behavior;
- bad evaluation design.

Always inspect examples before training.

{{exercise:M01.L05.EX03}}

---

## 14. From instruction following to alignment

SFT teaches:

```text
"When the user asks X, a good answer looks like Y."
```

But not every desirable property is captured by one ground-truth string.

Two answers can both be factually plausible while differing in:

- usefulness;
- clarity;
- completeness;
- style;
- safety;
- preference.

This motivates **alignment**.

The source presents a common progression:

```text
pretraining
   ↓
SFT
   ↓
preference alignment
```

Alignment introduces data such as:

```text
prompt
chosen response
rejected response
```

---

## 15. RLHF: learn a reward from human preferences

The source introduces RLHF through three broad stages:

```text
1. Pretrain + SFT the model
2. Train a reward model
3. Optimize the policy against that reward
```

### 15.1 Why pairwise preference?

Humans may disagree about what a score of:

```text
7 / 10
```

means.

It is often easier to ask:

```text
Which response is better?

A or B?
```

This produces pairwise preference data:

```text
chosen
rejected
```

### 15.2 Reward model

The reward model receives:

```text
prompt + response
```

and outputs a scalar.

Conceptually:

```text
good preferred response → higher score
rejected response       → lower score
```

The policy model is then optimized to generate responses with better reward.

{{image:rlhf-training-pipeline}}

---

## 16. Reinforcement-learning terms in language-model alignment

The source maps RL terminology to language generation.

### State

Conversation context.

### Action

A generated token or sequence decision.

### Policy

The model that produces tokens.

### Reward

Signal indicating how desirable the response is.

### Policy model

The model currently being optimized.

### Reference model

A frozen or fixed model used to keep optimization anchored to the pre-alignment
behavior.

These terms become essential in PPO, DPO, and GRPO discussions.

---

## 17. Why KL regularization is used

Suppose reward optimization says:

```text
"maximize reward"
```

The model may discover strange ways to exploit the reward function.

This is called reward hacking in the general sense.

So the source introduces a penalty based on the difference between:

```text
policy distribution
and
reference distribution
```

using KL divergence.

A simplified source-aligned reward form is:

```text
r = r_reward - lambda × KL(policy || reference)
```

Interpretation:

```text
reward term
→ move toward preferred behavior

KL penalty
→ do not move too far from the reference model
```

### Why this matters

The goal is not:

```text
maximize reward at any cost
```

The goal is:

```text
improve preference
while preserving useful language/model behavior
```

---

## 18. PPO-style RLHF

Historically, PPO has been widely used for RLHF-style policy optimization.

The source explains it using the concept of **advantage**.

### Intuition

If a response performs:

```text
better than expected
```

increase the probability of similar behavior.

If it performs:

```text
worse than expected
```

decrease that probability.

The advantage captures:

```text
actual reward - expected reward
```

at a high conceptual level.

PPO then uses a controlled update so the policy does not change too abruptly.

### Complexity

PPO-style RLHF can involve:

- policy model;
- reference model;
- reward model;
- value estimation;
- online generation;
- policy updates.

That complexity helped motivate simpler preference methods.

---

## 19. Direct Preference Optimization

**DPO** removes the need to train a separate reward model.

The training example becomes:

```text
prompt x
chosen response y_w
rejected response y_l
```

DPO directly trains the policy so that the chosen response becomes more likely
relative to the rejected response, while comparing behavior to a reference
model.

### Why DPO is attractive

The source emphasizes:

- simpler setup;
- less compute;
- no separate reward-model training stage.

### DPO data

A multimodal DPO example can contain:

```text
image
prompt
chosen assistant answer
rejected assistant answer
```

{{image:rlhf-vs-dpo}}

---

## 20. Understanding DPO beta

The source introduces a DPO hyperparameter:

```text
beta
```

and describes it as controlling how much the policy moves relative to the
reference model.

The chapter's stated intuition is:

```text
higher beta → more conservative
lower beta  → more aggressive movement toward preference
```

The main educational point:

> Preference optimization is not only about which answer wins. It also controls
> how strongly the adapted policy is allowed to diverge from the reference.

You should treat beta as a hyperparameter requiring empirical validation for
your task.

---

## 21. Mixed Preference Optimization

The source presents **MPO** as adding multiple objectives.

Conceptually:

```text
MPO loss
=
DPO-style preference loss
+
BCO loss
+
SFT generation loss
```

### DPO component

Teaches relative preference:

```text
chosen > rejected
```

### BCO component

Helps model absolute quality of chosen and rejected examples separately.

### SFT component

Keeps teaching the preferred generation itself.

The source gives an example weighting:

```text
sigmoid/DPO: 0.8
BCO:         0.2
SFT:         1.0
```

These are source-specific settings, not universal defaults.

### Why combine objectives?

One signal says:

```text
which response is preferred
```

another says:

```text
how good/bad each response is
```

and generation loss reinforces:

```text
how to produce the desired answer
```

---

## 22. Offline versus online preference data

### Offline DPO

Preference pairs are prepared before training.

Problem:

The model being trained changes over time.

Eventually, its current generations may differ from the model that originally
generated the preference candidates.

This creates a distribution mismatch.

### Online DPO

Conceptually:

```text
current policy receives prompt
      ↓
generates fresh responses
      ↓
judge/model labels preference
      ↓
current policy updates
```

The preference data stays closer to the current policy's actual behavior.

{{image:online-dpo}}

### Trade-off

Online methods require generation during training.

That makes them more computationally involved.

---

## 23. Multimodal preference datasets

The source shows a preference sample with four main components:

```text
prompt
images
chosen
rejected
```

{{image:multimodal-preference-dataset}}

Conceptually:

```python
sample = {
    "images": [image],
    "prompt": [
        {
            "role": "user",
            "content": [
                {"type": "image", "text": None},
                {
                    "type": "text",
                    "text": "Describe the image.",
                },
            ],
        }
    ],
    "chosen": [
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Preferred response",
                }
            ],
        }
    ],
    "rejected": [
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Rejected response",
                }
            ],
        }
    ],
}
```

### Image normalization

The chapter converts grayscale images to RGB before training.

This is a practical data-quality detail.

The lesson:

> Alignment code can be correct while media preprocessing is inconsistent.

Always normalize the input format expected by the processor/model.

### Source code naming inconsistency

The supplied source loads variables named:

```text
train_ds
test_ds
```

but later some code snippets refer to:

```text
train_dataset
test_dataset
```

This lesson normalizes them conceptually to one naming convention.

Do not copy such variable mismatches into your training script.

---

## 24. DPO/MPO with TRL

The source configures a `DPOTrainer`.

For ordinary DPO, the default preference loss can be used.

For the source's MPO-style configuration, it supplies multiple losses:

```python
from trl import DPOConfig

training_args = DPOConfig(
    output_dir="Qwen3-VL-2B-MPO",
    loss_type=[
        "sigmoid",
        "bco_pair",
        "sft",
    ],
    loss_weights=[
        0.8,
        0.2,
        1.0,
    ],
)
```

Then:

```python
from trl import DPOTrainer

trainer = DPOTrainer(
    model=peft_model,
    args=training_args,
    train_dataset=train_ds,
    eval_dataset=test_ds,
)

trainer.train()
```

### What changes between DPO and MPO?

In the source's workflow:

```text
same broad data format
same trainer family
different loss composition
```

That is useful engineering leverage.

---

## 25. Reinforcement learning with verifiable rewards

Human preference is not the only possible reward source.

For some tasks, correctness can be checked automatically.

Examples given by the source include:

```text
mathematics
code
```

Instead of:

```text
human says response A is better than response B
```

you can use:

```text
reward = passed verifier?
```

This is **reinforcement learning with verifiable rewards (RLVR)**.

### Why it can scale

Automatic verification can be much cheaper than human preference labeling.

But it only works when the target property is genuinely verifiable.

Not every desirable behavior has a simple objective checker.

For example:

```text
"Is this explanation empathetic and clear?"
```

is much harder to verify automatically than:

```text
"Does this code pass all unit tests?"
```

---

## 26. Group Relative Policy Optimization

The source introduces **GRPO** through a group of generated answers.

A high-level loop is:

```text
question
   ↓
generate multiple answers
   ↓
score every answer
   ↓
compare each answer to the group
   ↓
compute relative advantage
   ↓
update policy
```

### Group normalization

Suppose rewards are:

```text
[0.2, 0.9, 0.5, 0.1]
```

GRPO compares each response to the group statistics.

Conceptually:

```text
advantage
=
(response reward - group mean)
/
group standard deviation
```

A response above the group mean receives positive relative advantage.

A below-average response receives negative relative advantage.

### Why this is useful

It avoids some of the machinery associated with PPO's value estimation.

The source still notes KL regularization against a reference model.

{{image:ppo-vs-grpo}}

{{exercise:M01.L05.EX04}}

---

## 27. Online generation is a systems problem too

Methods such as online DPO and GRPO need fresh generations during training.

That means training now includes an inference workload.

The source describes two patterns:

### Colocated

```text
same GPU
→ training + generation
```

### Separate serving

```text
training GPU(s)
      ↕ requests
vLLM inference GPU
```

This creates a systems-design decision:

```text
simpler hardware arrangement
vs
better separation of training and generation workloads
```

So alignment is not only an optimization algorithm.

It also affects:

- serving infrastructure;
- GPU allocation;
- throughput;
- synchronization.

---

## 28. Choosing the right post-training method

A useful decision flow is:

### Case A — You have good input-target examples

Use:

```text
SFT
```

Example:

```text
document image + question → correct answer
```

### Case B — Full fine-tuning is too expensive

Use:

```text
LoRA / DoRA
```

possibly with quantization.

### Case C — Memory is the bottleneck

Consider:

```text
quantization
+
QLoRA-style training
```

### Case D — You have chosen/rejected preferences

Use a direct preference method such as:

```text
DPO
```

or the source's MPO-style combined objective.

### Case E — You have online scoring or preference generation

Consider an online preference/RL method.

### Case F — Correctness can be verified automatically

Consider:

```text
RLVR-style optimization
```

possibly with a group-based policy optimization method.

### Do not confuse objective and efficiency technique

This is essential.

```text
SFT / DPO / GRPO
→ training objective / optimization paradigm

LoRA / DoRA / QLoRA
→ how to make training more parameter/memory efficient
```

You can combine them.

Example:

```text
DPO objective
+
QLoRA parameterization
```

---

## 29. Practical debugging rules before expensive training

### 29.1 Inspect the rendered chat

Do not assume the processor created the correct format.

Print one example.

Check:

- system role;
- user role;
- image placeholder;
- assistant target;
- generation markers.

### 29.2 Verify the loss region

Make sure prompt tokens are masked when that is your desired objective.

### 29.3 Count trainable parameters

After PEFT injection:

```text
expected tiny trainable percentage?
```

If not, your target-module configuration may be wrong.

### 29.4 Inspect the actual image format

Check:

```text
RGB vs grayscale
resolution
number of images
```

### 29.5 Validate chosen/rejected examples

Preference data must genuinely contain:

```text
better response
worse response
```

Poor preference labels teach poor preferences.

### 29.6 Check variable names and dataset splits

The supplied source itself contains naming inconsistencies between
`train_ds`/`test_ds` and later `train_dataset`/`test_dataset`.

This is a good reminder:

> Notebook prose is not a substitute for running a clean end-to-end script.

### 29.7 Evaluate behavior, not just loss

Post-training can improve one target behavior and damage another.

Compare:

- base model;
- SFT model;
- aligned model.

Use held-out examples.

{{exercise:M01.L05.EX05}}

---

## 30. The complete post-training pipeline

Here is the chapter as one system:

```text
1. START WITH A PRETRAINED VLM
            ↓

2. PREPARE TARGET DATA
image + prompt + answer
            ↓

3. FORMAT WITH PROCESSOR
system/user/assistant roles
visual placeholders
            ↓

4. CHOOSE TRAINING OBJECTIVE
SFT
or
preference optimization
or
verifiable reward
            ↓

5. CHOOSE EFFICIENCY METHOD
full fine-tune
or LoRA / DoRA
or QLoRA
            ↓

6. TRAIN
TRL / trainer abstraction
            ↓

7. EVALUATE
target task
general capabilities
qualitative generations
            ↓

8. ALIGN IF NEEDED
chosen/rejected preferences
or reward signal
            ↓

9. RE-EVALUATE
helpfulness
task success
regressions
```

The chapter's deeper message is:

> Post-training is not one technique. It is a toolbox for shaping an already
> capable model.

---

## Important misconceptions

### Misconception 1: "Post-training means training a VLM from scratch."

No.

Post-training starts from an already capable model and adapts it.

### Misconception 2: "SFT and alignment are identical."

SFT teaches desired responses from target examples.

Alignment uses preference/reward signals to push the model toward more desirable
behavior.

### Misconception 3: "During multimodal SFT, the model should learn to reproduce the user prompt."

Usually not.

Prompt masking lets the loss focus on the assistant response.

### Misconception 4: "LoRA trains the original weight matrix directly."

LoRA freezes the base weight and trains low-rank adapter matrices that create an
update.

### Misconception 5: "Higher LoRA rank is always better."

Higher rank increases expressivity but also parameters and memory.

The correct rank depends on the adaptation problem and constraints.

### Misconception 6: "PEFT must outperform full fine-tuning."

Not necessarily.

It is an efficiency trade-off.

The source explicitly notes that adapter-based methods may learn less while also
forgetting less.

### Misconception 7: "Quantization is lossless compression."

No.

It reduces numerical precision and can introduce approximation error.

### Misconception 8: "QLoRA means the adapters themselves must be stored in 4-bit."

The key source concept is a low-bit frozen base model with trainable adapter
weights on top.

### Misconception 9: "DPO requires a trained reward model."

That is exactly what DPO is intended to avoid.

It directly optimizes from preference pairs.

### Misconception 10: "Chosen/rejected data is the same as SFT data."

SFT provides a desired target.

Preference data compares at least two candidate responses.

### Misconception 11: "KL regularization is the reward."

It is a regularizing penalty that keeps the policy from moving too far away from
the reference behavior.

### Misconception 12: "GRPO only generates one answer per question."

The group is central: multiple candidate answers are generated and compared
relative to one another.

### Misconception 13: "Every alignment task can use verifiable rewards."

No.

RLVR requires an output property that can actually be checked reliably.

---

## Key terminology

| Term | Meaning |
|---|---|
| Post-training | Adaptation stage applied after broad pretrained capability exists |
| SFT | Supervised fine-tuning using prompt-target examples |
| Chat template | Model-specific formatting of roles, images, and special tokens |
| Generation prompt | Marker indicating where assistant generation should begin |
| Prompt masking | Removing input/prompt positions from language-generation loss |
| PEFT | Parameter-efficient fine-tuning |
| Rank | Number of independent dimensions/components in a matrix transformation |
| LoRA | Low-rank adaptation using trainable A and B matrices |
| LoRA alpha | Scaling hyperparameter controlling adapter contribution |
| DoRA | Weight-decomposed low-rank adaptation separating magnitude and direction |
| Quantization | Representing model values using lower numerical precision |
| QLoRA | Low-bit frozen model combined with trainable LoRA-style adapters |
| NF4 | 4-bit NormalFloat representation discussed in QLoRA |
| Double quantization | Quantizing quantization scaling constants as well as weights |
| PEFT library | Hugging Face library implementing adapter-based fine-tuning methods |
| TRL | Library providing trainers/objectives for SFT and alignment workflows |
| Alignment | Training that steers outputs toward preferred behavior |
| RLHF | Reinforcement learning from human feedback |
| Reward model | Model that scores responses according to learned preferences |
| Policy model | Model being optimized |
| Reference model | Anchoring model used to regularize policy behavior |
| KL divergence | Measure of distributional difference used as a regularization term |
| PPO | Policy optimization method historically used in RLHF |
| Preference pair | Chosen and rejected responses for the same prompt |
| DPO | Direct Preference Optimization |
| Beta | DPO hyperparameter controlling policy/reference trade-off in the source framing |
| MPO | Mixed preference objective combining preference, BCO and generation losses |
| Online DPO | Preference optimization using newly generated responses during training |
| RLVR | Reinforcement learning with automatically verifiable rewards |
| GRPO | Group Relative Policy Optimization |
| Advantage | Signal indicating performance relative to a baseline or group |
| Online generation | Generating fresh candidate outputs during alignment training |

---

## Self-check

Before moving on, make sure you can answer:

1. What is post-training?
2. What does SFT teach a pretrained VLM?
3. Why are multimodal chat templates useful?
4. Why is `add_generation_prompt=True` useful during inference but not needed in
   the same way when the assistant target is already supplied during training?
5. What is prompt masking?
6. Why should image/input tokens normally not be assistant-language targets?
7. What does PEFT try to save?
8. What does matrix rank represent intuitively?
9. What are the shapes of LoRA matrices A and B?
10. Why does LoRA reduce trainable parameter count?
11. What does LoRA alpha control?
12. What is the conceptual difference between LoRA and DoRA?
13. Why can PEFT forget less than full fine-tuning?
14. What is quantization?
15. What trade-off comes from lower precision?
16. What does QLoRA combine?
17. What does NF4 refer to?
18. Why is double quantization called "double"?
19. What role does TRL play?
20. What fields are needed for a basic multimodal SFT example?
21. What is a reward model?
22. Why are pairwise human preferences useful?
23. What is the policy model?
24. What is the reference model?
25. Why add a KL penalty?
26. What role does advantage play in PPO-style RL?
27. How does DPO differ from reward-model-based RLHF?
28. What are chosen and rejected responses?
29. What does beta control in the source's DPO explanation?
30. What three components does the source's MPO objective combine?
31. What is the difference between offline and online DPO?
32. Why can online preference methods be more expensive?
33. What makes a reward "verifiable"?
34. Why does GRPO generate a group of answers?
35. Why should the base model and post-trained model both be evaluated?
36. Why is checking trainable parameter count important?

---

## Retain this idea

**Post-training is the process of shaping an already capable multimodal model
into the model you actually need. SFT teaches target behavior, PEFT and
quantization make adaptation affordable, and preference or verifiable-reward
methods steer which outputs the model should favor. The engineering challenge is
choosing the right objective, data format, efficiency method, and evaluation
together.**
""",

        "estimated_minutes": 300,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "post-training-map", "title": "A map of post-training", "order": 1},
            {"id": "sft", "title": "Supervised fine-tuning", "order": 2},
            {"id": "multimodal-chat-format", "title": "Multimodal chat formatting", "order": 3},
            {"id": "prompt-masking", "title": "Prompt masking", "order": 4},
            {"id": "peft", "title": "Parameter-efficient fine-tuning", "order": 5},
            {"id": "rank", "title": "Matrix rank intuition", "order": 6},
            {"id": "lora", "title": "LoRA", "order": 7},
            {"id": "dora", "title": "DoRA", "order": 8},
            {"id": "peft-code", "title": "PEFT adapter configuration", "order": 9},
            {"id": "quantization", "title": "Quantization", "order": 10},
            {"id": "qlora", "title": "QLoRA", "order": 11},
            {"id": "trl", "title": "TRL toolkit", "order": 12},
            {"id": "sft-example", "title": "End-to-end multimodal SFT", "order": 13},
            {"id": "alignment", "title": "From SFT to alignment", "order": 14},
            {"id": "rlhf", "title": "RLHF", "order": 15},
            {"id": "rl-basics", "title": "RL terms for language models", "order": 16},
            {"id": "kl", "title": "KL regularization", "order": 17},
            {"id": "ppo", "title": "PPO-style RLHF", "order": 18},
            {"id": "dpo", "title": "Direct Preference Optimization", "order": 19},
            {"id": "dpo-beta", "title": "DPO beta", "order": 20},
            {"id": "mpo", "title": "Mixed Preference Optimization", "order": 21},
            {"id": "online-dpo", "title": "Online preference optimization", "order": 22},
            {"id": "dpo-data-code", "title": "Multimodal preference datasets", "order": 23},
            {"id": "dpo-trainer", "title": "DPO/MPO with TRL", "order": 24},
            {"id": "rlvr", "title": "Verifiable rewards", "order": 25},
            {"id": "grpo", "title": "Group Relative Policy Optimization", "order": 26},
            {"id": "online-generation", "title": "Online generation infrastructure", "order": 27},
            {"id": "method-selection", "title": "Choosing the right method", "order": 28},
            {"id": "debugging", "title": "Practical debugging rules", "order": 29},
            {"id": "complete-pipeline", "title": "The complete post-training pipeline", "order": 30},
        ],
    },

    "exercises": [
        {
            "id": "M01.L05.EX01",
            "title": "Build and mask a multimodal SFT example",
            "lesson_code": "M01.L05",
            "section_id": "prompt-masking",
            "placement": "after_section",
            "description": (
                "Practice distinguishing multimodal context tokens from assistant target tokens."
            ),
            "instructions": (
                "Create one SFT sample containing a system prompt, one image, one user "
                "question, and one assistant answer. Then write a conceptual label mask "
                "showing which positions should be ignored and which should contribute "
                "to next-token loss. Explain why."
            ),
            "expected_output": (
                "A formatted conversation plus a token-region table marking system/user/"
                "image input as ignored and assistant response as trainable."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "sft",
                "chat-template",
                "prompt-masking",
                "multimodal-training",
            ],
        },
        {
            "id": "M01.L05.EX02",
            "title": "Compare full fine-tuning with LoRA",
            "lesson_code": "M01.L05",
            "section_id": "peft-code",
            "placement": "after_section",
            "description": (
                "Quantify why low-rank adapters reduce trainable parameter count."
            ),
            "instructions": (
                "Assume one frozen matrix W has shape 4096×4096.\n"
                "1. Count parameters in a full update.\n"
                "2. For LoRA r=8, count parameters in B (4096×8) and A (8×4096).\n"
                "3. Compute the ratio of LoRA parameters to full-update parameters.\n"
                "4. Explain what changes when r increases from 8 to 32."
            ),
            "expected_output": (
                "A calculation table comparing full update and LoRA, followed by a short "
                "expressivity-versus-cost explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "lora",
                "rank",
                "parameter-counting",
                "peft",
            ],
        },
        {
            "id": "M01.L05.EX03",
            "title": "Design a QLoRA document-VQA SFT run",
            "lesson_code": "M01.L05",
            "section_id": "sft-example",
            "placement": "after_section",
            "description": (
                "Combine dataset formatting, quantization, PEFT, and supervised training."
            ),
            "instructions": (
                "You have document images with question/answer pairs and limited GPU memory.\n"
                "Design a training plan including:\n"
                "1. chat-example structure,\n"
                "2. processor use,\n"
                "3. 4-bit base-model loading,\n"
                "4. LoRA/DoRA adapter configuration,\n"
                "5. loss masking,\n"
                "6. train/eval split,\n"
                "7. one qualitative evaluation after training."
            ),
            "expected_output": (
                "An ordered training recipe from raw example to evaluation, identifying "
                "which model parameters are frozen, quantized, and trainable."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "qlora",
                "sft",
                "peft",
                "quantization",
                "evaluation",
            ],
        },
        {
            "id": "M01.L05.EX04",
            "title": "Calculate group-relative advantages",
            "lesson_code": "M01.L05",
            "section_id": "grpo",
            "placement": "after_section",
            "description": (
                "Practice the central normalization intuition behind GRPO."
            ),
            "instructions": (
                "A prompt produces four answers with rewards [2, 6, 4, 8].\n"
                "1. Compute the mean reward.\n"
                "2. Compute the population standard deviation.\n"
                "3. Compute each z-score (reward - mean)/std.\n"
                "4. Identify which responses receive positive versus negative relative "
                "advantage.\n"
                "5. Explain why this is a relative signal rather than an absolute one."
            ),
            "expected_output": (
                "Mean, standard deviation, four normalized scores, and a short explanation "
                "of group-relative comparison."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "grpo",
                "advantage",
                "reward-normalization",
            ],
        },
        {
            "id": "M01.L05.EX05",
            "title": "Choose a post-training strategy",
            "lesson_code": "M01.L05",
            "section_id": "debugging",
            "placement": "after_section",
            "description": (
                "Select appropriate objectives and efficiency methods for different tasks."
            ),
            "instructions": (
                ('1. For each case, choose SFT, DPO/MPO-style preference training, RLVR/GRPO-style training, LoRA/DoRA, QLoRA, or a combination:\n'
                 '   - A. 20K image-question-answer examples, 16 GB GPU.\n'
                 '   - B. Human-ranked pairs of two multimodal responses.\n'
                 '   - C. Geometry problems where answers can be automatically checked.\n'
                 '   - D. A large model that already performs well but needs a tiny domain adapter.\n'
                 '2. Explain both the objective and efficiency method separately.')
            ),
            "expected_output": (
                "A four-row table with task, training objective, efficiency method, and "
                "justification."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "method-selection",
                "sft",
                "dpo",
                "rlvr",
                "qlora",
            ],
        },
        {
            "id": "M01.L05.EX06",
            "title": "Audit a post-training run before launch",
            "lesson_code": "M01.L05",
            "section_id": "complete-pipeline",
            "placement": "after_section",
            "description": (
                "Create a preflight checklist for a multimodal post-training experiment."
            ),
            "instructions": (
                ('1. Write a checklist covering:\n'
                 '   - one rendered training example,\n'
                 '   - image mode/shape,\n'
                 '   - loss mask,\n'
                 '   - trainable parameter count,\n'
                 '   - quantization configuration,\n'
                 '   - train/eval split,\n'
                 '   - preference-data correctness if used,\n'
                 '   - baseline comparison,\n'
                 '   - regression evaluation.\n'
                 '2. For each check, explain what failure it can catch.')
            ),
            "expected_output": (
                "A preflight table containing check, expected condition, and failure prevented."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "training-debugging",
                "evaluation",
                "post-training",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L05.QZ01",
        "title": "Post-Training Vision-Language Models — Knowledge Check",
        "lesson_code": "M01.L05",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L05.Q01",
                "section_id": "post-training-map",
                "question": "What best describes post-training?",
                "options": [
                    "Training every model from random initialization",
                    "Adapting an already capable pretrained model toward desired tasks or behavior",
                    "Only compressing model files",
                    "Only collecting more raw images",
                ],
                "correct": 1,
                "explanation": (
                    "Post-training starts from an existing pretrained model and shapes its "
                    "behavior or task performance."
                ),
            },
            {
                "id": "M01.L05.Q02",
                "section_id": "sft",
                "question": "What supervision does SFT use?",
                "options": [
                    "Prompt/input paired with a desired target response",
                    "No target signal at all",
                    "Only a scalar reward with no examples",
                    "Only image embeddings without language",
                ],
                "correct": 0,
                "explanation": (
                    "SFT is supervised learning using explicit target outputs."
                ),
            },
            {
                "id": "M01.L05.Q03",
                "section_id": "prompt-masking",
                "question": "Why is prompt masking useful?",
                "options": [
                    "It prevents the model from seeing the image.",
                    "It focuses language-model loss on the desired assistant response rather than reproducing the input prompt.",
                    "It increases every token's loss.",
                    "It converts preference data into images.",
                ],
                "correct": 1,
                "explanation": (
                    "Prompt masking removes context/input positions from the target loss."
                ),
            },
            {
                "id": "M01.L05.Q04",
                "section_id": "lora",
                "question": "How does LoRA reduce trainable parameter count?",
                "options": [
                    "It removes the entire language model.",
                    "It represents the update using two small low-rank matrices while freezing the base weight.",
                    "It trains only image pixels.",
                    "It stores every weight twice.",
                ],
                "correct": 1,
                "explanation": (
                    "The low-rank factors A and B are much smaller than a full dense update."
                ),
            },
            {
                "id": "M01.L05.Q05",
                "section_id": "lora",
                "question": "What generally happens when LoRA rank r increases?",
                "options": [
                    "Trainable parameter count increases and the adapter can represent richer updates.",
                    "Trainable parameter count always becomes zero.",
                    "The base model is deleted.",
                    "Quantization automatically becomes 2-bit.",
                ],
                "correct": 0,
                "explanation": (
                    "Rank controls the adapter's low-dimensional capacity and cost."
                ),
            },
            {
                "id": "M01.L05.Q06",
                "section_id": "dora",
                "question": "What conceptual distinction does DoRA introduce?",
                "options": [
                    "It separates weight magnitude and direction for adaptation.",
                    "It eliminates the visual encoder.",
                    "It turns every image into text before training.",
                    "It trains only the tokenizer.",
                ],
                "correct": 0,
                "explanation": (
                    "The source presents DoRA as decomposing magnitude and direction, then "
                    "applying low-rank adaptation to the directional component."
                ),
            },
            {
                "id": "M01.L05.Q07",
                "section_id": "quantization",
                "question": "What is the main purpose of quantization in this chapter?",
                "options": [
                    "Reduce memory by representing weights with lower numerical precision",
                    "Increase every model parameter to FP64",
                    "Replace supervised data",
                    "Create preference pairs",
                ],
                "correct": 0,
                "explanation": (
                    "Lower-bit representations reduce model memory requirements."
                ),
            },
            {
                "id": "M01.L05.Q08",
                "section_id": "qlora",
                "question": "What does QLoRA combine?",
                "options": [
                    "A quantized frozen base model with trainable low-rank adapters",
                    "Only full fine-tuning and no adapters",
                    "A reward model with ASR",
                    "Video sampling with OCR",
                ],
                "correct": 0,
                "explanation": (
                    "QLoRA uses low-bit base weights while training LoRA-style adapters."
                ),
            },
            {
                "id": "M01.L05.Q09",
                "section_id": "trl",
                "question": "What role does TRL play in the source workflow?",
                "options": [
                    "It provides trainer abstractions for SFT and alignment methods.",
                    "It is an image file format.",
                    "It replaces all datasets with synthetic images.",
                    "It is only a tokenizer.",
                ],
                "correct": 0,
                "explanation": (
                    "TRL wraps several post-training objectives in configurable trainer APIs."
                ),
            },
            {
                "id": "M01.L05.Q10",
                "section_id": "rlhf",
                "question": "What does a reward model learn from human preference data?",
                "options": [
                    "A scalar score indicating how preferred a prompt-response pair is",
                    "The JPEG compression ratio",
                    "Only the tokenizer vocabulary",
                    "The number of image patches",
                ],
                "correct": 0,
                "explanation": (
                    "The reward model maps prompt/response content to a learned preference score."
                ),
            },
            {
                "id": "M01.L05.Q11",
                "section_id": "kl",
                "question": "Why is KL regularization used during alignment?",
                "options": [
                    "To encourage the policy to stay reasonably close to reference behavior",
                    "To delete the reference model",
                    "To make every response identical",
                    "To turn SFT data into preference pairs",
                ],
                "correct": 0,
                "explanation": (
                    "KL penalizes excessive divergence from the reference model."
                ),
            },
            {
                "id": "M01.L05.Q12",
                "section_id": "dpo",
                "question": "What major component does DPO avoid compared with PPO-style RLHF?",
                "options": [
                    "A separately trained reward model",
                    "Preference data",
                    "A policy model",
                    "A reference model",
                ],
                "correct": 0,
                "explanation": (
                    "DPO directly uses chosen/rejected preferences instead of first training "
                    "an explicit reward model."
                ),
            },
            {
                "id": "M01.L05.Q13",
                "section_id": "dpo-beta",
                "question": "In the source's explanation, what does DPO beta control?",
                "options": [
                    "How conservatively the policy moves relative to the reference model",
                    "The image width",
                    "The number of dataset shards",
                    "The tokenizer language",
                ],
                "correct": 0,
                "explanation": (
                    "Beta controls the strength of the policy/reference trade-off in the "
                    "chapter's DPO explanation."
                ),
            },
            {
                "id": "M01.L05.Q14",
                "section_id": "mpo",
                "question": "Which losses does the source's MPO formulation combine?",
                "options": [
                    "Preference/sigmoid loss, BCO loss, and SFT generation loss",
                    "Only MSE",
                    "Only OCR loss and segmentation loss",
                    "Only contrastive loss",
                ],
                "correct": 0,
                "explanation": (
                    "The source combines relative preference, BCO, and generation objectives."
                ),
            },
            {
                "id": "M01.L05.Q15",
                "section_id": "online-dpo",
                "question": "What is the defining feature of online DPO in the source?",
                "options": [
                    "Preference candidates are generated during training from the current policy.",
                    "All preferences are permanently fixed before training.",
                    "No model generations are needed.",
                    "Only supervised labels are used.",
                ],
                "correct": 0,
                "explanation": (
                    "Online DPO refreshes response candidates while the policy is evolving."
                ),
            },
            {
                "id": "M01.L05.Q16",
                "section_id": "rlvr",
                "question": "What makes RLVR possible?",
                "options": [
                    "A task has an automatically checkable reward or correctness signal.",
                    "Every response must be human-ranked.",
                    "The model has no reference behavior.",
                    "No outputs are generated.",
                ],
                "correct": 0,
                "explanation": (
                    "RLVR relies on a verifier such as a correctness checker rather than "
                    "human preference for every training signal."
                ),
            },
            {
                "id": "M01.L05.Q17",
                "section_id": "grpo",
                "question": "Why does GRPO generate multiple responses for the same prompt?",
                "options": [
                    "To compute rewards and advantages relative to the response group",
                    "To avoid using any reward signal",
                    "To duplicate the dataset for storage",
                    "To remove all policy updates",
                ],
                "correct": 0,
                "explanation": (
                    "The group's reward statistics provide the relative baseline for each answer."
                ),
            },
            {
                "id": "M01.L05.Q18",
                "section_id": "method-selection",
                "question": "Which statement correctly separates objective from efficiency method?",
                "options": [
                    "DPO is an objective; QLoRA is an efficiency strategy that can be used with it.",
                    "QLoRA and DPO are exactly the same objective.",
                    "LoRA is a reward model.",
                    "SFT is a quantization format.",
                ],
                "correct": 0,
                "explanation": (
                    "Preference/SFT methods define what is optimized, while LoRA/QLoRA "
                    "change how efficiently parameters are adapted."
                ),
            },
            {
                "id": "M01.L05.Q19",
                "section_id": "debugging",
                "question": "Why should you print trainable parameter counts after PEFT injection?",
                "options": [
                    "To verify that the intended small adapter subset is actually trainable",
                    "To increase the model size",
                    "To convert grayscale images",
                    "To generate preference labels",
                ],
                "correct": 0,
                "explanation": (
                    "A wrong target-module configuration can silently train more or fewer "
                    "parameters than intended."
                ),
            },
            {
                "id": "M01.L05.Q20",
                "section_id": "complete-pipeline",
                "type": "open",
                "question": (
                    "You have a pretrained VLM and 30,000 multimodal domain examples plus "
                    "5,000 chosen/rejected preference pairs, but limited GPU memory. Design "
                    "a two-stage post-training plan. Explain the SFT data format, loss masking, "
                    "LoRA/DoRA or QLoRA choice, preference-training method, reference model "
                    "role, and how you would evaluate regressions."
                ),
            },
        ],
        "passing_score": 70,
    },
}
