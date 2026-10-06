"""M07.L01 — Finetuning.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 7, "Finetuning".
Instructor-authored curriculum adaptation based only on the supplied chapter.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M07.L01"

MODULE_ORDER = 7

MODULE_TITLE = "Finetuning"

MODULE_DESCRIPTION = (
    "Learn when and why to finetune foundation models, how finetuning differs "
    "from prompting and RAG, why memory is the central bottleneck, how "
    "quantization and PEFT reduce that bottleneck, how LoRA and QLoRA work, "
    "how model merging extends finetuning, and how to choose practical "
    "finetuning tactics and hyperparameters."
)

SOURCE_CHAPTER = 7

SOURCE_PAGES = "Page range not provided in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Finetuning",

    "slug": "ai-engineering-m07-l01-finetuning",

    "description": (
        "A learner-friendly but technically substantial guide to adapting "
        "foundation models by updating their weights, covering transfer learning, "
        "continued pre-training, supervised and preference finetuning, RAG versus "
        "finetuning, memory math, numerical precision, quantization, PEFT, LoRA, "
        "QLoRA, model merging, and practical training tactics."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 6.0,

    "skill_tags": [
        "finetuning",
        "transfer-learning",
        "continued-pretraining",
        "supervised-finetuning",
        "preference-finetuning",
        "rag-vs-finetuning",
        "backpropagation",
        "memory-estimation",
        "quantization",
        "mixed-precision",
        "peft",
        "lora",
        "qlora",
        "model-merging",
        "hyperparameter-tuning",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Finetuning",

        "content": (
            "# Finetuning\n"
            "\n"
            "> **Course:** AI Engineering Foundations  \n"
            "> **Lesson:** M07.L01  \n"
            "> **Module:** Finetuning  \n"
            "> **Source alignment:** Chapter 7, *Finetuning*. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain finetuning as weight-based model adaptation and relate it to "
            "transfer learning.\n"
            "- Distinguish continued pre-training, supervised finetuning, "
            "preference finetuning, infilling finetuning, and long-context finetuning.\n"
            "- Decide when finetuning is justified and when prompting or RAG should "
            "be tried first.\n"
            "- Distinguish information-based failures from behavior-based failures.\n"
            "- Explain why RAG is often better for facts while finetuning is often "
            "better for form, style, syntax, and behavior.\n"
            "- Explain why finetuning can improve one task while hurting others.\n"
            "- Explain forward pass, backward pass, loss, gradients, optimizer "
            "states, trainable parameters, and frozen parameters.\n"
            "- Estimate the rough memory required for inference and training.\n"
            "- Explain how sequence length, batch size, activations, and KV state "
            "affect memory.\n"
            "- Compare FP32, FP16, BF16, integer formats, and mixed precision.\n"
            "- Explain post-training quantization, quantization-aware training, and "
            "low-precision training.\n"
            "- Explain full finetuning, partial finetuning, and parameter-efficient "
            "finetuning (PEFT).\n"
            "- Distinguish adapter-based PEFT from soft-prompt methods.\n"
            "- Explain the low-rank idea behind LoRA and calculate its trainable "
            "parameter count for a simple matrix.\n"
            "- Reason about LoRA rank, target matrices, alpha/scaling, and "
            "multi-LoRA serving.\n"
            "- Explain how QLoRA combines low-rank adaptation with 4-bit model "
            "storage, NF4, and paged optimizers.\n"
            "- Explain why model merging can support multi-task models and lower "
            "deployment complexity.\n"
            "- Distinguish linear combination, task vectors, SLERP, pruning, "
            "layer stacking, upscaling, and concatenation.\n"
            "- Choose a practical finetuning development path, framework, and "
            "important hyperparameters.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. What finetuning changes\n"
            "\n"
            "Prompting adapts a model by changing what you put **into** the model. "
            "Finetuning adapts a model by changing the model's **weights**.\n"
            "\n"
            "```text\n"
            "Prompt-based adaptation\n"
            "    instructions + examples + context + tools\n"
            "                        |\n"
            "                        v\n"
            "                 unchanged model\n"
            "\n"
            "Finetuning\n"
            "    task-specific training data\n"
            "                        |\n"
            "                        v\n"
            "                 updated weights\n"
            "```\n"
            "\n"
            "You normally start with a **base model** that already knows a great "
            "deal. Your goal is not to teach everything again. It is to make the "
            "existing model work better for a particular task, domain, style, "
            "format, or preference.\n"
            "\n"
            "Finetuning can improve domain capability, safety, structured output, "
            "and instruction following. The chapter especially emphasizes its use "
            "for behavior that is difficult to obtain reliably through prompting alone.\n"
            "\n"
            "[[IMAGE_NEEDED: Prompting versus finetuning | A side-by-side diagram "
            "where prompting changes instructions/context around fixed model "
            "weights while finetuning updates some or all model weights | Learner "
            "should notice that the adaptation happens in different places]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Finetuning as transfer learning\n"
            "\n"
            "Finetuning is a form of **transfer learning**: reuse knowledge learned "
            "from one broad task to learn a related task more efficiently.\n"
            "\n"
            "Foundation models make this especially powerful because pre-training "
            "gives them broad capabilities from enormous datasets. Finetuning can "
            "then specialize that knowledge using far fewer examples than training "
            "a model from scratch.\n"
            "\n"
            "This property is called **sample efficiency**.\n"
            "\n"
            "A useful mental model is:\n"
            "\n"
            "> Pre-training builds a broad capability space; finetuning moves the "
            "model toward the behavior you need inside that space.\n"
            "\n"
            "The chapter also mentions feature-based transfer, where a pre-trained "
            "model produces representations such as embeddings that another model "
            "uses. That is transfer learning too, but it is not weight-updating "
            "finetuning of the original model.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Major types of finetuning\n"
            "\n"
            "Finetuning can mean several different training stages.\n"
            "\n"
            "### Continued pre-training\n"
            "\n"
            "Continue self-supervised training on task- or domain-related raw data.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- Raw legal documents before legal QA finetuning.\n"
            "- Large Vietnamese text collections before Vietnamese summarization.\n"
            "\n"
            "This is useful because raw domain data is cheaper to acquire than "
            "expert-annotated instruction data.\n"
            "\n"
            "### Supervised finetuning (SFT)\n"
            "\n"
            "Train on `(input, desired output)` pairs.\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- Instruction -> response.\n"
            "- Text -> classification label.\n"
            "- Document -> summary.\n"
            "\n"
            "### Preference finetuning\n"
            "\n"
            "Train toward human or AI preferences using comparative data such as:\n"
            "\n"
            "```text\n"
            "(instruction, preferred response, rejected response)\n"
            "```\n"
            "\n"
            "### Infilling finetuning\n"
            "\n"
            "Teach the model to fill missing spans rather than only predict the "
            "next token. This can be useful for editing and code debugging.\n"
            "\n"
            "### Long-context finetuning\n"
            "\n"
            "Adapt the model to operate over longer sequences, potentially "
            "requiring architecture changes such as positional-embedding changes. "
            "The chapter warns that extending long-context performance can also "
            "degrade behavior on shorter sequences.\n"
            "\n"
            "[[IMAGE_NEEDED: Finetuning family | A branching diagram from a "
            "pre-trained model to continued pre-training, supervised finetuning, "
            "preference finetuning, infilling, and long-context finetuning | "
            "Learner should notice that 'finetuning' is an umbrella for several "
            "different training objectives]]\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Reasons to finetune\n"
            "\n"
            "The main reason to finetune is **quality on your specific task**.\n"
            "\n"
            "Useful cases include:\n"
            "\n"
            "- A model performs poorly on a domain or syntax underrepresented in "
            "its original training.\n"
            "- You need highly reliable JSON, YAML, code, or another structured form.\n"
            "- You want output style to follow a consistent internal standard.\n"
            "- You want to mitigate specific biases with carefully curated data.\n"
            "- You want a smaller model specialized enough to replace a much "
            "larger general-purpose model for one task.\n"
            "\n"
            "That last use case can be economically important. A small specialized "
            "model may be faster and cheaper in production than a powerful general "
            "model while still being better on the target task.\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Reasons not to finetune too early\n"
            "\n"
            "Finetuning has costs that prompting does not.\n"
            "\n"
            "### It can degrade other capabilities\n"
            "\n"
            "Improving one task can hurt another. A model specialized aggressively "
            "for one workflow may become worse on other workflows your product needs.\n"
            "\n"
            "### It requires data\n"
            "\n"
            "High-quality instruction data can be expensive, especially when "
            "expert judgment is required.\n"
            "\n"
            "### It requires training knowledge\n"
            "\n"
            "You need to reason about learning rate, batch size, optimizer behavior, "
            "overfitting, validation, and training failures.\n"
            "\n"
            "### It creates a serving problem\n"
            "\n"
            "After training a custom model, you still need a reliable way to deploy "
            "and operate it.\n"
            "\n"
            "### It creates maintenance work\n"
            "\n"
            "New base models keep appearing. Your team must decide when it is worth "
            "migrating, retraining, or abandoning a finetuned model.\n"
            "\n"
            "The chapter's workflow therefore starts with systematic prompting and "
            "evaluation before moving to more expensive adaptation methods.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Domain-specific does not automatically mean finetuned\n"
            "\n"
            "A common mistake is to assume that a domain-specific application "
            "requires a domain-specific trained model.\n"
            "\n"
            "Strong general-purpose models can sometimes outperform specialized "
            "models even inside the specialized domain. Therefore, do not decide "
            "from the label 'domain-specific.' Decide from **your evaluation results**.\n"
            "\n"
            "The practical lesson is:\n"
            "\n"
            "1. Build an application-specific evaluation set.\n"
            "2. Test strong general models.\n"
            "3. Test adaptation methods.\n"
            "4. Compare performance, cost, latency, and operational complexity.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Finetuning versus RAG: facts or behavior?\n"
            "\n"
            "One of the chapter's most useful decision frameworks is to diagnose "
            "**why** the model is failing.\n"
            "\n"
            "### Information-based failure\n"
            "\n"
            "The model does not have the information or has outdated information.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- Private company policy the public model has never seen.\n"
            "- A current event after the model's knowledge cutoff.\n"
            "- A customer record available only in an internal database.\n"
            "\n"
            "This points toward **RAG or tools**.\n"
            "\n"
            "### Behavior-based failure\n"
            "\n"
            "The model has enough information but behaves incorrectly.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- Correct facts, wrong output structure.\n"
            "- Correct content, but irrelevant to the requested task.\n"
            "- Failure on a rare syntax or domain-specific language.\n"
            "- Inconsistent style despite good context.\n"
            "\n"
            "This points more strongly toward **finetuning**.\n"
            "\n"
            "The chapter summarizes the intuition memorably:\n"
            "\n"
            "> **RAG is for facts; finetuning is for form.**\n"
            "\n"
            "That sentence is a heuristic, not an absolute law. RAG and finetuning "
            "can be combined, and either can influence factuality or behavior indirectly.\n"
            "\n"
            "### A sensible adaptation ladder\n"
            "\n"
            "```text\n"
            "Define evaluation\n"
            "      -> prompting\n"
            "      -> more representative few-shot examples\n"
            "      -> simple retrieval if information is missing\n"
            "      -> stronger retrieval if information failures continue\n"
            "      -> finetuning if behavior failures continue\n"
            "      -> combine RAG + finetuning when justified\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: RAG versus finetuning decision tree | A decision tree "
            "starting with model failure, branching into missing/outdated information "
            "toward RAG and behavior/format/style failure toward finetuning, with "
            "a later branch allowing both | Learner should notice that failure "
            "diagnosis should drive the adaptation method]]\n"
            "\n"
            "{{exercise:M07.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Why memory is the central finetuning bottleneck\n"
            "\n"
            "Foundation models are large, but training requires more memory than "
            "inference because training stores additional values used to update weights.\n"
            "\n"
            "The chapter identifies three especially important drivers:\n"
            "\n"
            "- Total number of parameters.\n"
            "- Number of **trainable** parameters.\n"
            "- Numerical representation used for weights, activations, gradients, "
            "and optimizer states.\n"
            "\n"
            "This explains why modern finetuning methods focus on two levers:\n"
            "\n"
            "1. **Train fewer parameters** -> PEFT.\n"
            "2. **Use fewer bits per value** -> quantization / reduced precision.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. Backpropagation and trainable parameters\n"
            "\n"
            "A parameter can be:\n"
            "\n"
            "- **Trainable:** allowed to change during finetuning.\n"
            "- **Frozen:** kept unchanged.\n"
            "\n"
            "Training has two broad phases.\n"
            "\n"
            "### Forward pass\n"
            "\n"
            "Compute the model's output from the input.\n"
            "\n"
            "### Backward pass\n"
            "\n"
            "Use the error signal to determine how trainable weights should change.\n"
            "\n"
            "The simplified loop is:\n"
            "\n"
            "```text\n"
            "input\n"
            " -> forward pass\n"
            " -> prediction\n"
            " -> compare with expected output\n"
            " -> loss\n"
            " -> gradients for trainable parameters\n"
            " -> optimizer update\n"
            "```\n"
            "\n"
            "A **gradient** measures how the loss changes with respect to a trainable "
            "parameter. An **optimizer** such as SGD or Adam uses those gradients "
            "to decide the update.\n"
            "\n"
            "Adam also stores optimizer state, which increases memory use for every "
            "trainable parameter.\n"
            "\n"
            "[[IMAGE_NEEDED: Forward and backward pass | A small neural-network "
            "diagram showing forward activations and backward gradients, with loss "
            "feeding into parameter updates | Learner should notice that training "
            "stores extra information absent from normal inference]]\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Estimating inference memory\n"
            "\n"
            "A rough starting point for model-weight memory is:\n"
            "\n"
            "```text\n"
            "weight memory = number of parameters × bytes per parameter\n"
            "```\n"
            "\n"
            "For a 13B-parameter model stored with 2 bytes per parameter:\n"
            "\n"
            "```text\n"
            "13B × 2 bytes = 26 GB of weights\n"
            "```\n"
            "\n"
            "Inference also requires activations and transformer attention state. "
            "The chapter offers a rough back-of-the-envelope estimate of about "
            "20% extra in some ordinary workloads:\n"
            "\n"
            "```text\n"
            "rough inference memory ≈ N × M × 1.2\n"
            "```\n"
            "\n"
            "For the 13B example:\n"
            "\n"
            "```text\n"
            "26 GB × 1.2 ≈ 31.2 GB\n"
            "```\n"
            "\n"
            "This is only an estimate. Longer context and larger batches increase "
            "activation and attention/KV memory further.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Estimating training memory\n"
            "\n"
            "Training adds memory for gradients and optimizer state:\n"
            "\n"
            "```text\n"
            "training memory\n"
            "  = weights\n"
            "  + activations\n"
            "  + gradients\n"
            "  + optimizer states\n"
            "```\n"
            "\n"
            "For Adam, each trainable parameter has a gradient plus two optimizer "
            "state values. In the chapter's simplified 2-byte example, that creates "
            "three extra stored values per trainable parameter.\n"
            "\n"
            "If all 13B parameters are trainable:\n"
            "\n"
            "```text\n"
            "13B × 3 × 2 bytes = 78 GB\n"
            "```\n"
            "\n"
            "for gradients and optimizer states alone.\n"
            "\n"
            "If only 1B parameters are trainable:\n"
            "\n"
            "```text\n"
            "1B × 3 × 2 bytes = 6 GB\n"
            "```\n"
            "\n"
            "This is the memory logic behind PEFT.\n"
            "\n"
            "### Activation memory\n"
            "\n"
            "Activation memory can become extremely large. One technique to reduce "
            "it is **gradient checkpointing / activation recomputation**:\n"
            "\n"
            "- Store fewer activations.\n"
            "- Recompute them when backward propagation needs them.\n"
            "- Save memory at the cost of extra computation and training time.\n"
            "\n"
            "[[IMAGE_NEEDED: Inference versus training memory | A stacked bar "
            "comparison showing inference memory as weights + activations/KV and "
            "training memory adding gradients + optimizer states + larger activation "
            "requirements | Learner should notice why a model that fits for inference "
            "may still not fit for finetuning]]\n"
            "\n"
            "{{exercise:M07.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Numerical representations: range versus precision\n"
            "\n"
            "Every stored model value consumes bits. More bits generally mean more "
            "memory but can represent values more accurately or over a wider range.\n"
            "\n"
            "Common formats introduced in the chapter include:\n"
            "\n"
            "- FP32: 32-bit floating point.\n"
            "- FP16: 16-bit floating point.\n"
            "- BF16: 16-bit format with different range/precision tradeoffs.\n"
            "- TF32: format used in certain GPU workloads.\n"
            "- INT8 and INT4: low-bit integer representations.\n"
            "\n"
            "Two important ideas are:\n"
            "\n"
            "- **Range:** how large/small a value the format can represent.\n"
            "- **Precision:** how finely the format distinguishes nearby values.\n"
            "\n"
            "BF16 and FP16 use the same total number of bits but distribute them "
            "differently. BF16 has wider range and lower precision than FP16.\n"
            "\n"
            "Using the wrong format for a model can significantly degrade model quality.\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Quantization: reduce bits, reduce memory\n"
            "\n"
            "The chapter uses **quantization** broadly for converting values from "
            "higher precision to lower precision.\n"
            "\n"
            "The memory impact is immediate:\n"
            "\n"
            "```text\n"
            "10B parameters × 4 bytes (32-bit) = 40 GB\n"
            "10B parameters × 2 bytes (16-bit) = 20 GB\n"
            "```\n"
            "\n"
            "### What can be quantized?\n"
            "\n"
            "- Weights.\n"
            "- Activations.\n"
            "- Gradients.\n"
            "- Other training state where supported.\n"
            "\n"
            "Weight quantization is common because model weights consume large "
            "memory and are comparatively stable to quantize.\n"
            "\n"
            "### When can quantization happen?\n"
            "\n"
            "- **Post-training quantization (PTQ):** quantize after training.\n"
            "- **During training:** train in or simulate lower precision.\n"
            "\n"
            "Reduced precision can also improve throughput, but format conversion "
            "and hardware support affect real latency.\n"
            "\n"
            "The tradeoff is that rounding errors and reduced range can hurt quality.\n"
            "\n"
            "[[IMAGE_NEEDED: Quantization memory tradeoff | The same model shown "
            "at 32-bit, 16-bit, 8-bit, and 4-bit with decreasing memory blocks and "
            "a warning that lower precision can introduce numerical error | Learner "
            "should notice the near-linear memory reduction with bits per value]]\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Quantization during training\n"
            "\n"
            "Training is more sensitive to numerical error than inference because "
            "small errors can compound across many weight updates.\n"
            "\n"
            "The chapter distinguishes several approaches.\n"
            "\n"
            "### Quantization-aware training (QAT)\n"
            "\n"
            "Simulate low-precision behavior during training so the model learns to "
            "remain accurate when later served at low precision.\n"
            "\n"
            "QAT does not necessarily reduce training compute because the underlying "
            "training operations may still run at higher precision.\n"
            "\n"
            "### Low-precision training\n"
            "\n"
            "Actually perform some training operations at lower precision to save "
            "memory and compute.\n"
            "\n"
            "### Mixed-precision training\n"
            "\n"
            "Use high precision for sensitive values/operations and lower precision "
            "where it is safe.\n"
            "\n"
            "Automatic mixed precision (AMP) can help frameworks choose appropriate "
            "precision for different operations.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Full finetuning, partial finetuning, and PEFT\n"
            "\n"
            "### Full finetuning\n"
            "\n"
            "Update every parameter.\n"
            "\n"
            "This gives maximum flexibility but also maximum gradient/optimizer "
            "memory and usually requires substantial data and compute.\n"
            "\n"
            "### Partial finetuning\n"
            "\n"
            "Freeze some layers and update others.\n"
            "\n"
            "This reduces memory, but the chapter notes that naive partial "
            "finetuning can require a large fraction of model weights to approach "
            "full-finetuning performance.\n"
            "\n"
            "### Parameter-efficient finetuning (PEFT)\n"
            "\n"
            "PEFT aims to achieve performance close to full finetuning with orders "
            "of magnitude fewer trainable parameters.\n"
            "\n"
            "The important insight is that **trainable parameter count** is not "
            "the same as total model parameter count.\n"
            "\n"
            "For a 7B model in 16-bit precision, the base weights alone are roughly "
            "14 GB. Full finetuning with Adam adds large gradient and optimizer "
            "memory before activations are even counted. PEFT attacks this problem "
            "by keeping most base weights frozen.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Two major PEFT families\n"
            "\n"
            "The chapter organizes common PEFT methods into two broad families.\n"
            "\n"
            "### Adapter-based methods\n"
            "\n"
            "Add small trainable modules or parameter structures to the model while "
            "freezing most original weights.\n"
            "\n"
            "Examples mentioned include:\n"
            "\n"
            "- Early adapter modules.\n"
            "- LoRA.\n"
            "- BitFit.\n"
            "- IA3.\n"
            "- LongLoRA.\n"
            "\n"
            "### Soft-prompt methods\n"
            "\n"
            "Add trainable continuous vectors that guide model behavior.\n"
            "\n"
            "Unlike normal prompts:\n"
            "\n"
            "- They are not human-readable tokens.\n"
            "- They are optimized through backpropagation.\n"
            "\n"
            "Examples include prefix tuning, P-Tuning, and prompt tuning. These "
            "methods differ largely in where the learned soft tokens are inserted.\n"
            "\n"
            "[[IMAGE_NEEDED: Adapter PEFT versus soft prompts | A transformer "
            "diagram with one version showing small trainable adapter modules inside "
            "the network and another showing trainable soft vectors prepended to "
            "model inputs/layers | Learner should notice that both freeze most base "
            "weights but adapt the model at different locations]]\n"
            "\n"
            "---\n"
            "\n"

            "## 17. LoRA: low-rank adaptation\n"
            "\n"
            "**LoRA (Low-Rank Adaptation)** is the most prominent adapter-based "
            "method discussed in the chapter.\n"
            "\n"
            "Instead of updating a large weight matrix `W`, LoRA learns a small "
            "update represented as the product of two skinny matrices.\n"
            "\n"
            "Suppose:\n"
            "\n"
            "```text\n"
            "W has shape n × m\n"
            "A has shape n × r\n"
            "B has shape r × m\n"
            "```\n"
            "\n"
            "Then:\n"
            "\n"
            "```text\n"
            "A × B has shape n × m\n"
            "```\n"
            "\n"
            "so the low-rank update can be added to `W`.\n"
            "\n"
            "During finetuning:\n"
            "\n"
            "- `W` stays frozen.\n"
            "- `A` and `B` are trainable.\n"
            "\n"
            "The rank `r` determines the width of this low-dimensional update.\n"
            "\n"
            "### Why this saves parameters\n"
            "\n"
            "A `9 × 9` matrix has 81 values. Replacing its trainable update with a "
            "`9 × 1` matrix and a `1 × 9` matrix uses only 18 trainable values.\n"
            "\n"
            "The full base matrix is still present, but the training state exists "
            "only for the small LoRA matrices.\n"
            "\n"
            "[[IMAGE_NEEDED: LoRA matrix update | A large frozen matrix W beside "
            "two small trainable matrices A and B whose product forms a low-rank "
            "update added to W | Learner should notice that only A and B receive "
            "gradient updates]]\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Why can such a small update work?\n"
            "\n"
            "The chapter motivates LoRA using the idea of **low intrinsic dimension**.\n"
            "\n"
            "A huge pre-trained model may contain billions of parameters, but "
            "changing its behavior for one downstream task may require movement in "
            "a much smaller effective subspace.\n"
            "\n"
            "This helps explain two surprising facts:\n"
            "\n"
            "- Finetuning can work with far fewer trainable parameters than pre-training.\n"
            "- Finetuning can work with far less data than pre-training.\n"
            "\n"
            "The source also discusses research into low-rank pre-training itself. "
            "That work is promising, but the chapter treats full-rank pre-training "
            "followed by low-rank adaptation as the more established pattern.\n"
            "\n"
            "---\n"
            "\n"

            "## 19. LoRA configuration: what and how much to adapt\n"
            "\n"
            "There are three especially important decisions.\n"
            "\n"
            "### Which weight matrices?\n"
            "\n"
            "For transformers, LoRA is commonly applied to attention matrices:\n"
            "\n"
            "- Query `Wq`.\n"
            "- Key `Wk`.\n"
            "- Value `Wv`.\n"
            "- Output projection `Wo`.\n"
            "\n"
            "It can also be applied to feedforward matrices.\n"
            "\n"
            "Under a fixed trainable-parameter budget, spreading a low rank across "
            "more useful matrices can outperform using a high rank on only one matrix.\n"
            "\n"
            "The chapter notes that if only two attention matrices can be chosen, "
            "query and value are commonly strong candidates.\n"
            "\n"
            "### Rank `r`\n"
            "\n"
            "Smaller rank means fewer trainable parameters. The chapter reports "
            "that values in a relatively small range can often be sufficient, and "
            "that increasing rank indefinitely does not guarantee better performance.\n"
            "\n"
            "### LoRA scaling / alpha\n"
            "\n"
            "A scaling hyperparameter controls how strongly the low-rank update "
            "contributes relative to the frozen base weight. Rank and scaling should "
            "be tuned together rather than in isolation.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Serving LoRA adapters\n"
            "\n"
            "LoRA's modularity creates a deployment advantage.\n"
            "\n"
            "### Option 1: merge before serving\n"
            "\n"
            "Merge the LoRA update into the original matrix before deployment.\n"
            "\n"
            "- Simple inference path.\n"
            "- No LoRA-specific extra computation during inference.\n"
            "- Useful when serving one specialization.\n"
            "\n"
            "### Option 2: keep adapters separate\n"
            "\n"
            "Keep one base model and dynamically apply different LoRA adapters.\n"
            "\n"
            "- Adds some serving overhead.\n"
            "- Dramatically reduces storage when many specializations share one base model.\n"
            "- Makes switching between tasks/customers faster.\n"
            "\n"
            "For many customer-specific models, this can be far more efficient than "
            "storing a full copy of the model for every customer.\n"
            "\n"
            "[[IMAGE_NEEDED: Multi-LoRA serving | One shared base model connected "
            "to many small customer/task adapters that are swapped at runtime | "
            "Learner should notice that the expensive base weights are stored once]]\n"
            "\n"
            "---\n"
            "\n"

            "## 21. QLoRA: quantize the base, train the adapters\n"
            "\n"
            "LoRA makes the **trainable update** small, but the frozen base model "
            "can still consume a great deal of memory.\n"
            "\n"
            "QLoRA attacks that second problem.\n"
            "\n"
            "The chapter describes QLoRA as storing base-model weights in **4-bit "
            "NF4** during finetuning, then dequantizing them to BF16 for forward and "
            "backward computation as needed.\n"
            "\n"
            "It also uses **paged optimizers** to move data between CPU and GPU when "
            "GPU memory pressure becomes high, particularly with long sequences.\n"
            "\n"
            "The combined idea is:\n"
            "\n"
            "```text\n"
            "Frozen base model: aggressively quantized\n"
            "Trainable adaptation: small LoRA matrices\n"
            "Compute: temporarily dequantize where required\n"
            "Memory pressure: paged optimizer support\n"
            "```\n"
            "\n"
            "This made very large-model finetuning possible on much smaller hardware "
            "than naive full finetuning.\n"
            "\n"
            "### The catch\n"
            "\n"
            "Quantization/dequantization saves memory but can increase training time. "
            "Memory efficiency and compute efficiency are not always the same thing.\n"
            "\n"
            "[[IMAGE_NEEDED: LoRA versus QLoRA | Side-by-side diagram where LoRA "
            "uses a higher-precision frozen base plus small adapters, while QLoRA "
            "stores the frozen base in 4-bit NF4 and trains small adapters with "
            "temporary dequantization | Learner should notice that QLoRA reduces "
            "the base-model memory, not merely adapter size]]\n"
            "\n"
            "{{exercise:M07.L01.EX03}}\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Model merging: combine models instead of serving them separately\n"
            "\n"
            "Finetuning customizes one model. **Model merging** combines multiple "
            "models or task-specific updates into a new model.\n"
            "\n"
            "Potential goals include:\n"
            "\n"
            "- Combine capabilities from different specialized models.\n"
            "- Reduce the memory/serving burden of maintaining several separate models.\n"
            "- Create multi-task models.\n"
            "- Combine learning from independently finetuned copies.\n"
            "- Build larger models from existing ones.\n"
            "\n"
            "The chapter treats model merging as promising but more experimental "
            "than mainstream finetuning.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Why merging helps multi-task finetuning\n"
            "\n"
            "Without merging, two common strategies are:\n"
            "\n"
            "### Simultaneous finetuning\n"
            "\n"
            "Mix examples from all tasks into one training dataset.\n"
            "\n"
            "This is simple but learning multiple skills together may require more "
            "data and careful balancing.\n"
            "\n"
            "### Sequential finetuning\n"
            "\n"
            "Train task A, then task B, then task C.\n"
            "\n"
            "The danger is **catastrophic forgetting**: learning a later task can "
            "damage performance on an earlier one.\n"
            "\n"
            "### Parallel finetuning + merging\n"
            "\n"
            "Start from the same base, finetune separate copies independently, then "
            "merge them.\n"
            "\n"
            "This reduces direct sequential interference and can create one model "
            "that carries multiple specializations.\n"
            "\n"
            "Model merging is also attractive for on-device systems, where serving "
            "many separate models may exceed device memory.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Model merging versus ensembling\n"
            "\n"
            "These ideas sound similar but operate at different stages.\n"
            "\n"
            "### Ensemble\n"
            "\n"
            "Keep multiple models separate and combine their **outputs**.\n"
            "\n"
            "```text\n"
            "query -> model A\n"
            "      -> model B\n"
            "      -> model C\n"
            "      -> combine answers\n"
            "```\n"
            "\n"
            "This can improve quality but multiplies inference work.\n"
            "\n"
            "### Model merging\n"
            "\n"
            "Combine **parameters or components** before serving, then run one "
            "resulting model.\n"
            "\n"
            "The goal is to capture useful behavior without paying for several full "
            "inference calls on every request.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Merging by summing: averages and task vectors\n"
            "\n"
            "The simplest merging family adds model parameters together.\n"
            "\n"
            "### Linear combination\n"
            "\n"
            "Average or weighted-average corresponding weights from models.\n"
            "\n"
            "This works especially naturally for models finetuned from the same base.\n"
            "\n"
            "### Task vectors\n"
            "\n"
            "A useful concept is:\n"
            "\n"
            "```text\n"
            "task vector = finetuned weights - base weights\n"
            "```\n"
            "\n"
            "This vector represents the parameter change associated with a task.\n"
            "\n"
            "You can then perform **task arithmetic**:\n"
            "\n"
            "- Add task vectors to combine behavior.\n"
            "- Subtract a task vector to reduce an unwanted capability or behavior.\n"
            "\n"
            "LoRA adapters naturally resemble compact task updates, which makes them "
            "especially convenient for this style of merging.\n"
            "\n"
            "[[IMAGE_NEEDED: Task-vector merging | One base model with two finetuned "
            "models producing delta/task vectors, then the vectors being combined "
            "and added back to the base | Learner should notice that merging can "
            "operate on changes from the shared base rather than raw full weights]]\n"
            "\n"
            "---\n"
            "\n"

            "## 26. SLERP and pruning conflicting updates\n"
            "\n"
            "### SLERP\n"
            "\n"
            "Spherical linear interpolation treats model/task vectors like points "
            "on a sphere and chooses a point along the shortest path between them.\n"
            "\n"
            "The interpolation factor controls which source contributes more.\n"
            "\n"
            "### Pruning redundant task parameters\n"
            "\n"
            "Many weight changes produced by finetuning may be tiny or redundant. "
            "When multiple task vectors are merged, unnecessary changes can "
            "interfere with one another.\n"
            "\n"
            "The chapter discusses approaches such as TIES and DARE that prune or "
            "drop redundant task-vector parameters before merging.\n"
            "\n"
            "The important intuition is:\n"
            "\n"
            "> More merged updates create more opportunities for interference, so "
            "removing weak/conflicting updates can improve the final merged model.\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Layer stacking and model upscaling\n"
            "\n"
            "Instead of adding corresponding weights, **layer stacking** takes "
            "layers from models and arranges them into a new deeper architecture.\n"
            "\n"
            "This approach is sometimes called passthrough or frankenmerging.\n"
            "\n"
            "Potential uses include:\n"
            "\n"
            "- Combining model components.\n"
            "- Building mixture-of-experts structures from dense checkpoints.\n"
            "- Creating a larger model from an existing smaller model.\n"
            "\n"
            "### Model upscaling\n"
            "\n"
            "A team may have new hardware that can host a larger model but not want "
            "to pre-train from scratch. Layers can be duplicated/stacked and selected "
            "layers combined so the resulting model has an intermediate target size.\n"
            "\n"
            "Further training is generally required to make the new architecture work well.\n"
            "\n"
            "[[IMAGE_NEEDED: Layer stacking and upscaling | Two copies of a smaller "
            "model whose layers are partly stacked and partly combined to create a "
            "deeper larger model | Learner should notice that stacking changes the "
            "architecture and normally requires more training]]\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Concatenation\n"
            "\n"
            "Another merging approach concatenates components instead of adding them.\n"
            "\n"
            "For LoRA adapters:\n"
            "\n"
            "```text\n"
            "rank r1 + rank r2 -> merged rank r1 + r2\n"
            "```\n"
            "\n"
            "The problem is that parameter count grows with the combined components. "
            "The chapter therefore does not recommend concatenation when memory "
            "reduction is a primary objective.\n"
            "\n"
            "---\n"
            "\n"

            "## 29. Practical tactic: choose a development path\n"
            "\n"
            "Finetuning requires three broad choices:\n"
            "\n"
            "1. Base model.\n"
            "2. Finetuning method.\n"
            "3. Finetuning framework/service.\n"
            "\n"
            "The chapter describes two useful development paths.\n"
            "\n"
            "### Progression path\n"
            "\n"
            "1. Test the code with a cheap, fast model.\n"
            "2. Test the data on a middle-sized model.\n"
            "3. Experiment with a strong model to estimate achievable performance.\n"
            "4. Run broader comparisons to map the price/performance frontier.\n"
            "\n"
            "### Distillation-style path\n"
            "\n"
            "1. Start with a small dataset and a very strong model.\n"
            "2. Build the best teacher you can.\n"
            "3. Use that model to generate more data.\n"
            "4. Train a cheaper student model on the expanded dataset.\n"
            "\n"
            "The right path depends on budget, data, and what you already learned "
            "during prompt experiments.\n"
            "\n"
            "---\n"
            "\n"

            "## 30. Practical tactic: choose the finetuning method\n"
            "\n"
            "The chapter recommends starting with a method such as LoRA when you "
            "are new to finetuning, then attempting full finetuning if needed and "
            "if resources justify it.\n"
            "\n"
            "Method selection depends on:\n"
            "\n"
            "- Dataset size.\n"
            "- Available GPU memory.\n"
            "- Required quality.\n"
            "- Number of customized models you need.\n"
            "- How those models will be served.\n"
            "\n"
            "PEFT can be particularly attractive with only hundreds or a few "
            "thousand examples. Full finetuning generally needs much more data and compute.\n"
            "\n"
            "If many specialized models share one base, LoRA's modular serving can "
            "be more attractive than maintaining many full finetuned checkpoints.\n"
            "\n"
            "---\n"
            "\n"

            "## 31. Practical tactic: APIs, frameworks, and distributed training\n"
            "\n"
            "A managed finetuning API can be the easiest option:\n"
            "\n"
            "- Upload data.\n"
            "- Choose an available base model.\n"
            "- Run training.\n"
            "- Receive a customized model.\n"
            "\n"
            "The tradeoff is reduced control over base models and training knobs.\n"
            "\n"
            "The chapter names general finetuning frameworks such as:\n"
            "\n"
            "- LLaMA-Factory.\n"
            "- Unsloth.\n"
            "- Hugging Face PEFT.\n"
            "- Axolotl.\n"
            "- LitGPT.\n"
            "\n"
            "For training across multiple machines, distributed-training frameworks "
            "such as DeepSpeed, PyTorch Distributed, and ColossalAI can help.\n"
            "\n"
            "The framework is an implementation choice; the evaluation/data/model "
            "decisions remain your responsibility.\n"
            "\n"
            "---\n"
            "\n"

            "## 32. Hyperparameter: learning rate\n"
            "\n"
            "The **learning rate** controls how large each parameter update is.\n"
            "\n"
            "Think of optimization as walking toward a destination:\n"
            "\n"
            "- Too small -> progress is painfully slow.\n"
            "- Too large -> you overshoot and training can become unstable.\n"
            "\n"
            "The chapter notes that no universal best learning rate exists. It "
            "gives a broad experimental range around `1e-7` to `1e-3` and suggests "
            "using loss behavior as a diagnostic.\n"
            "\n"
            "- Highly fluctuating loss -> learning rate may be too large.\n"
            "- Smooth but extremely slow decline -> learning rate may be too small.\n"
            "\n"
            "A **learning-rate schedule** changes the learning rate across training, "
            "often using larger steps earlier and smaller steps near the end.\n"
            "\n"
            "---\n"
            "\n"

            "## 33. Hyperparameter: batch size and gradient accumulation\n"
            "\n"
            "The **batch size** is the number of examples used to produce one "
            "parameter-update signal.\n"
            "\n"
            "Larger batches can create more stable gradient estimates and process "
            "more examples in parallel, but they require more memory.\n"
            "\n"
            "If the model is so large that only tiny physical batches fit in memory, "
            "use **gradient accumulation**:\n"
            "\n"
            "```text\n"
            "batch 1 -> gradients\n"
            "batch 2 -> add gradients\n"
            "batch 3 -> add gradients\n"
            "batch 4 -> add gradients\n"
            "              |\n"
            "              v\n"
            "          one weight update\n"
            "```\n"
            "\n"
            "This approximates a larger effective batch without loading all examples "
            "at the same time.\n"
            "\n"
            "---\n"
            "\n"

            "## 34. Hyperparameter: number of epochs\n"
            "\n"
            "An **epoch** is one pass through the training dataset.\n"
            "\n"
            "Small datasets may need more epochs because each example needs to be "
            "seen repeatedly. Large datasets may need only a small number of passes.\n"
            "\n"
            "Use training and validation loss together:\n"
            "\n"
            "```text\n"
            "training loss down + validation loss down\n"
            "    -> more training may still help\n"
            "\n"
            "training loss down + validation loss up\n"
            "    -> overfitting warning\n"
            "```\n"
            "\n"
            "The right epoch count is an empirical result, not a fixed rule.\n"
            "\n"
            "---\n"
            "\n"

            "## 35. Hyperparameter: prompt loss weight\n"
            "\n"
            "Instruction-finetuning examples contain both a prompt and a response.\n"
            "\n"
            "During inference, the user provides the prompt; the model is mainly "
            "responsible for generating the response. Therefore, it can make sense "
            "for response tokens to contribute more strongly to training loss.\n"
            "\n"
            "**Prompt loss weight** controls how much prompt tokens contribute "
            "relative to response tokens.\n"
            "\n"
            "- 100% -> prompt and response tokens contribute equally.\n"
            "- 0% -> only response tokens train the model.\n"
            "- Intermediate values -> model learns some from prompt structure but "
            "focuses more on producing the response.\n"
            "\n"
            "The chapter notes a commonly used default around 10%, but the best "
            "value depends on the task and framework.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> A domain-specific application always requires finetuning.\n"
            "\n"
            "**Why this is wrong:** strong general models may already perform well "
            "on the domain. Evaluate first.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Finetuning is the best fix for missing or current information.\n"
            "\n"
            "**Why this is wrong:** missing/private/current facts are often better "
            "handled by RAG or tools.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> A model that fits in GPU memory for inference will also fit for training.\n"
            "\n"
            "**Why this is wrong:** training adds gradients, optimizer states, and "
            "often much larger activation requirements.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> PEFT makes the full base model disappear from memory.\n"
            "\n"
            "**Why this is wrong:** PEFT reduces trainable parameters; the base "
            "weights still exist. QLoRA adds quantization to reduce base-weight memory too.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> Higher LoRA rank always means better quality.\n"
            "\n"
            "**Why this is wrong:** rank beyond a useful range can produce little "
            "benefit and may even contribute to overfitting.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> Quantization always makes training faster.\n"
            "\n"
            "**Why this is wrong:** it reduces memory and can improve throughput, "
            "but quantize/dequantize overhead can increase training time.\n"
            "\n"
            "### Misconception 7\n"
            "\n"
            "> Model merging is the same as ensembling.\n"
            "\n"
            "**Why this is wrong:** merging combines model parameters/components; "
            "ensembling keeps models separate and combines their outputs.\n"
            "\n"
            "### Misconception 8\n"
            "\n"
            "> Once a finetuning framework runs without errors, the hard part is over.\n"
            "\n"
            "**Why this is wrong:** data quality, evaluation, method choice, "
            "hyperparameters, serving, maintenance, and base-model changes remain "
            "major engineering concerns.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Finetuning | Further training a base model by updating some or all weights. |\n"
            "| Transfer learning | Reusing knowledge learned on one task/domain to accelerate learning on another. |\n"
            "| Continued pre-training | Additional self-supervised training on task/domain-related raw data. |\n"
            "| SFT | Supervised finetuning on input-output examples. |\n"
            "| Preference finetuning | Training from comparative preference data. |\n"
            "| Infilling finetuning | Training a model to fill missing spans using surrounding context. |\n"
            "| Trainable parameter | Parameter allowed to change during finetuning. |\n"
            "| Frozen parameter | Parameter kept unchanged during finetuning. |\n"
            "| Forward pass | Computation from model input to prediction. |\n"
            "| Backward pass | Computation used to derive gradients and update trainable weights. |\n"
            "| Loss | Numerical signal describing model error relative to training targets. |\n"
            "| Gradient | Derivative describing how loss changes with respect to a trainable parameter. |\n"
            "| Optimizer state | Extra values maintained by an optimizer such as Adam for weight updates. |\n"
            "| Gradient checkpointing | Recompute activations during backward pass to trade compute for memory. |\n"
            "| FP32 / FP16 / BF16 | Floating-point numerical formats with different memory, range, and precision. |\n"
            "| Quantization | Reducing the precision/number of bits used to represent model values. |\n"
            "| PTQ | Post-training quantization. |\n"
            "| QAT | Quantization-aware training. |\n"
            "| Mixed precision | Using different numerical precision levels for different operations/values. |\n"
            "| Full finetuning | Updating every model parameter. |\n"
            "| Partial finetuning | Updating a subset of existing model parameters. |\n"
            "| PEFT | Parameter-efficient finetuning; adapt with far fewer trainable parameters. |\n"
            "| Adapter | Small trainable module/parameter structure added around a frozen base model. |\n"
            "| Soft prompt | Trainable continuous vectors used to guide behavior. |\n"
            "| LoRA | Low-Rank Adaptation; learns low-rank weight updates through small matrices. |\n"
            "| LoRA rank | Inner dimension r controlling adapter capacity and trainable parameter count. |\n"
            "| Multi-LoRA serving | Serving many small adapters on one shared base model. |\n"
            "| QLoRA | Quantized LoRA method that stores frozen base weights at very low precision during finetuning. |\n"
            "| NF4 | 4-bit NormalFloat format used by QLoRA. |\n"
            "| Paged optimizer | Optimizer strategy that moves data between CPU/GPU under memory pressure. |\n"
            "| Catastrophic forgetting | Losing performance on earlier tasks while training on new tasks. |\n"
            "| Model merging | Combining parameters/components of multiple models into a new model. |\n"
            "| Task vector | Difference between a finetuned model's weights and its base weights. |\n"
            "| SLERP | Spherical linear interpolation for combining vectors/models. |\n"
            "| Layer stacking | Building a new model by stacking selected layers from one or more models. |\n"
            "| Gradient accumulation | Accumulating gradients over multiple small batches before one update. |\n"
            "| Epoch | One pass over the training dataset. |\n"
            "| Prompt loss weight | Relative contribution of prompt tokens to loss during instruction finetuning. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What does finetuning change that prompting does not?\n"
            "2. Why is finetuning a form of transfer learning?\n"
            "3. What is continued pre-training?\n"
            "4. How does SFT differ from preference finetuning?\n"
            "5. When is infilling finetuning useful?\n"
            "6. Why can finetuning hurt unrelated tasks?\n"
            "7. Why should prompting usually be tested systematically first?\n"
            "8. What is the difference between an information failure and a behavior failure?\n"
            "9. Explain the heuristic 'RAG for facts, finetuning for form.'\n"
            "10. Why might RAG and finetuning still be used together?\n"
            "11. What is the difference between a trainable and frozen parameter?\n"
            "12. What additional memory does training need beyond inference?\n"
            "13. Calculate weight memory for a 7B model at 2 bytes per parameter.\n"
            "14. Why can activation memory become a bottleneck?\n"
            "15. How does gradient checkpointing trade compute for memory?\n"
            "16. What is the difference between range and precision in number formats?\n"
            "17. Why can BF16 represent larger values than FP16 despite both using 16 bits?\n"
            "18. What is post-training quantization?\n"
            "19. Why is training more sensitive to low precision than inference?\n"
            "20. What does mixed-precision training try to balance?\n"
            "21. Compare full, partial, and parameter-efficient finetuning.\n"
            "22. What is the difference between adapter-based PEFT and soft prompts?\n"
            "23. In LoRA, which parameters are frozen and which are trained?\n"
            "24. How does LoRA rank affect trainable parameter count?\n"
            "25. Why might a low-rank update be sufficient for downstream adaptation?\n"
            "26. Which transformer matrices are commonly targeted by LoRA?\n"
            "27. Why doesn't increasing LoRA rank indefinitely guarantee improvement?\n"
            "28. When should LoRA weights be merged before serving versus kept separate?\n"
            "29. What problem does QLoRA solve that ordinary LoRA does not fully solve?\n"
            "30. What roles do NF4 and paged optimizers play in QLoRA?\n"
            "31. How is model merging different from ensembling?\n"
            "32. What is catastrophic forgetting and how can parallel finetuning + merging help?\n"
            "33. Define a task vector.\n"
            "34. How can task vectors be added or subtracted?\n"
            "35. What is the intuition behind SLERP?\n"
            "36. Why can pruning task-vector updates improve merging?\n"
            "37. What is layer stacking?\n"
            "38. Why does an upscaled stacked model usually need further training?\n"
            "39. Why is concatenation unattractive when the goal is memory reduction?\n"
            "40. What is the progression path for choosing a base model?\n"
            "41. How does dataset size influence PEFT versus full finetuning?\n"
            "42. What is the tradeoff of using a managed finetuning API?\n"
            "43. What does an unstable loss curve suggest about learning rate?\n"
            "44. Why does batch size increase memory use?\n"
            "45. What does gradient accumulation simulate?\n"
            "46. How can training and validation loss reveal overfitting?\n"
            "47. Why might response tokens receive higher training weight than prompt tokens?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**Finetuning is not simply 'train the model more.' It is an engineering "
            "choice made after diagnosing the application's failures. The strongest "
            "workflow combines evaluation, prompting, retrieval, careful data, "
            "memory-aware training, and the right level of weight adaptation. PEFT, "
            "LoRA, and quantization matter because they make that adaptation feasible "
            "at foundation-model scale.**\n"
        ),

        "estimated_minutes": 360,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "finetuning-big-picture", "title": "What finetuning changes", "order": 1},
            {"id": "transfer-learning", "title": "Finetuning as transfer learning", "order": 2},
            {"id": "finetuning-types", "title": "Types of finetuning", "order": 3},
            {"id": "reasons-to-finetune", "title": "Reasons to finetune", "order": 4},
            {"id": "reasons-not-to-finetune", "title": "Reasons not to finetune too early", "order": 5},
            {"id": "domain-specific-warning", "title": "Domain-specific model warning", "order": 6},
            {"id": "rag-vs-finetuning", "title": "RAG versus finetuning", "order": 7},
            {"id": "memory-bottleneck", "title": "Memory bottleneck", "order": 8},
            {"id": "backpropagation", "title": "Backpropagation and trainable parameters", "order": 9},
            {"id": "inference-memory", "title": "Inference memory", "order": 10},
            {"id": "training-memory", "title": "Training memory", "order": 11},
            {"id": "numerical-representations", "title": "Numerical representations", "order": 12},
            {"id": "quantization", "title": "Quantization", "order": 13},
            {"id": "training-precision", "title": "Quantization during training", "order": 14},
            {"id": "full-partial-peft", "title": "Full, partial, and PEFT", "order": 15},
            {"id": "peft-families", "title": "PEFT families", "order": 16},
            {"id": "lora-intuition", "title": "LoRA", "order": 17},
            {"id": "why-lora-works", "title": "Why LoRA works", "order": 18},
            {"id": "lora-configuration", "title": "LoRA configuration", "order": 19},
            {"id": "lora-serving", "title": "Serving LoRA adapters", "order": 20},
            {"id": "qlora", "title": "QLoRA", "order": 21},
            {"id": "model-merging", "title": "Model merging", "order": 22},
            {"id": "multitask-merging", "title": "Multi-task finetuning and merging", "order": 23},
            {"id": "merging-vs-ensemble", "title": "Merging versus ensembling", "order": 24},
            {"id": "linear-merging", "title": "Linear merging and task vectors", "order": 25},
            {"id": "slerp-pruning", "title": "SLERP and pruning", "order": 26},
            {"id": "layer-stacking", "title": "Layer stacking and upscaling", "order": 27},
            {"id": "concatenation", "title": "Concatenation", "order": 28},
            {"id": "base-model-development-path", "title": "Base-model development path", "order": 29},
            {"id": "method-selection", "title": "Choose a finetuning method", "order": 30},
            {"id": "framework-selection", "title": "Choose a finetuning framework", "order": 31},
            {"id": "learning-rate", "title": "Learning rate", "order": 32},
            {"id": "batch-gradient-accumulation", "title": "Batch size and gradient accumulation", "order": 33},
            {"id": "epochs-overfitting", "title": "Epochs and overfitting", "order": 34},
            {"id": "prompt-loss-weight", "title": "Prompt loss weight", "order": 35},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M07.L01.EX01",

            "title": "Choose Prompting, RAG, Finetuning, or Both",

            "lesson_code": "M07.L01",

            "section_id": "rag-vs-finetuning",

            "placement": "after_section",

            "description": (
                "Diagnose whether application failures are caused by missing "
                "information or by model behavior."
            ),

            "instructions": (
                "For each scenario, choose prompting, RAG/tools, finetuning, or a "
                "combination. Explain the failure mode first.\n\n"
                "1. A support bot does not know today's account balance.\n"
                "2. The bot knows the correct answer but keeps returning prose "
                "instead of required YAML.\n"
                "3. The model cannot answer questions about private company policies.\n"
                "4. The model has the right source documents but writes specifications "
                "that are too vague for engineers.\n"
                "5. The model repeatedly fails on a rare company-specific DSL.\n"
                "6. The model's factual knowledge becomes stale every week.\n"
                "7. The model needs current facts and must always answer using a "
                "strict internal response style.\n"
                "8. For each choice, define the evaluation signal you would use to "
                "verify improvement."
            ),

            "expected_output": (
                "A scenario-by-scenario diagnosis separating information failures "
                "from behavior failures, followed by justified adaptation choices "
                "and evaluation metrics."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "failure-diagnosis",
                "rag-vs-finetuning",
                "adaptation-strategy",
                "evaluation-design",
            ],
        },

        {
            "id": "M07.L01.EX02",

            "title": "Estimate Finetuning Memory",

            "lesson_code": "M07.L01",

            "section_id": "training-memory",

            "placement": "after_section",

            "description": (
                "Practice the chapter's back-of-the-envelope memory calculations "
                "and see why trainable-parameter count matters."
            ),

            "instructions": (
                "Use the chapter's simplified assumptions.\n\n"
                "Model: 7B parameters.\n"
                "Weight format: 2 bytes per parameter.\n"
                "Optimizer: Adam with one gradient plus two optimizer-state values "
                "per trainable parameter, each also 2 bytes.\n\n"
                "1. Calculate base weight memory.\n"
                "2. Estimate rough inference memory using the 1.2 multiplier.\n"
                "3. Calculate gradient + optimizer-state memory if all 7B parameters "
                "are trainable.\n"
                "4. Repeat step 3 if only 100M parameters are trainable.\n"
                "5. Explain what these calculations do not include accurately.\n"
                "6. Explain how gradient checkpointing changes the tradeoff.\n"
                "7. Explain how quantizing the frozen base weights would change the "
                "memory picture.\n"
                "8. Explain why a model that fits for inference can still fail with "
                "CUDA out-of-memory during finetuning."
            ),

            "expected_output": (
                "A short calculation sheet with memory estimates and an explanation "
                "of how PEFT, checkpointing, and quantization attack different "
                "parts of the memory footprint."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "memory-estimation",
                "backpropagation",
                "optimizer-memory",
                "peft",
                "quantization",
            ],
        },

        {
            "id": "M07.L01.EX03",

            "title": "Design a LoRA/QLoRA Finetuning Plan",

            "lesson_code": "M07.L01",

            "section_id": "qlora",

            "placement": "after_section",

            "description": (
                "Design a parameter-efficient finetuning experiment while reasoning "
                "about LoRA configuration and deployment."
            ),

            "instructions": (
                "You need to adapt an open-weight transformer for a specialized "
                "text-to-structured-output task on one 24 GB GPU.\n\n"
                "1. Explain why full finetuning may be difficult.\n"
                "2. Decide whether LoRA or QLoRA is a better first experiment.\n"
                "3. Choose an initial set of target matrices and justify it.\n"
                "4. Choose an initial rank range and explain why higher is not "
                "automatically better.\n"
                "5. Explain the role of the LoRA scaling/alpha parameter.\n"
                "6. Define what you would monitor during training.\n"
                "7. Explain how you would detect overfitting.\n"
                "8. Decide whether to merge the adapter before serving or keep it "
                "separate if you later create 20 customer-specific versions.\n"
                "9. Define a quality, latency, and memory evaluation before deployment.\n"
                "10. State one reason you might eventually try full finetuning."
            ),

            "expected_output": (
                "A practical PEFT experiment plan covering hardware constraints, "
                "LoRA/QLoRA choice, rank, target matrices, training monitoring, "
                "serving strategy, and evaluation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "lora",
                "qlora",
                "peft-design",
                "training-monitoring",
                "deployment-strategy",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M07.L01.QZ01",

        "title": "Finetuning — Knowledge Check",

        "lesson_code": "M07.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M07.L01.Q01",
                "section_id": "finetuning-big-picture",
                "question": "What distinguishes finetuning from prompting?",
                "options": [
                    "Finetuning updates model weights",
                    "Finetuning only changes the system prompt",
                    "Prompting requires backpropagation",
                    "Prompting always creates a new model checkpoint",
                ],
                "correct": 0,
                "explanation": (
                    "Prompting adapts model inputs; finetuning adapts some or all "
                    "model weights through further training."
                ),
            },

            {
                "id": "M07.L01.Q02",
                "section_id": "transfer-learning",
                "question": "Why is finetuning considered transfer learning?",
                "options": [
                    "It reuses capabilities learned during pre-training for a new related task",
                    "It transfers GPU memory to the CPU only",
                    "It copies prompts between users",
                    "It always trains a model from random initialization",
                ],
                "correct": 0,
                "explanation": (
                    "Finetuning starts from knowledge already acquired by the base "
                    "model rather than learning the target task entirely from scratch."
                ),
            },

            {
                "id": "M07.L01.Q03",
                "section_id": "finetuning-types",
                "question": "What is continued pre-training?",
                "options": [
                    "Further self-supervised training on relevant raw data",
                    "Pairwise human-preference optimization only",
                    "Inference using a longer prompt",
                    "A method for merging two LoRA adapters",
                ],
                "correct": 0,
                "explanation": (
                    "Continued pre-training exposes the base model to additional "
                    "domain/task-related unlabeled data using a self-supervised objective."
                ),
            },

            {
                "id": "M07.L01.Q04",
                "section_id": "rag-vs-finetuning",
                "question": (
                    "A model gives outdated answers because its training cutoff is "
                    "old. Which adaptation is the strongest first candidate?"
                ),
                "options": [
                    "RAG or an external information tool",
                    "Increase LoRA rank",
                    "Train only the output projection",
                    "Use more epochs on old data",
                ],
                "correct": 0,
                "explanation": (
                    "The primary failure is missing current information, which "
                    "retrieval/tools can provide directly."
                ),
            },

            {
                "id": "M07.L01.Q05",
                "section_id": "backpropagation",
                "question": "What is a gradient used for during training?",
                "options": [
                    "Estimate how loss changes with respect to a trainable parameter",
                    "Store the tokenizer vocabulary",
                    "Retrieve documents from a vector database",
                    "Measure API latency",
                ],
                "correct": 0,
                "explanation": (
                    "Gradients tell the optimizer how the loss responds to changes "
                    "in trainable parameters."
                ),
            },

            {
                "id": "M07.L01.Q06",
                "section_id": "training-memory",
                "question": (
                    "Why does training normally require much more memory than inference?"
                ),
                "options": [
                    "Training stores gradients and optimizer states in addition to "
                    "weights and activations",
                    "Inference always uses more model parameters",
                    "Training does not use activations",
                    "Inference requires an optimizer",
                ],
                "correct": 0,
                "explanation": (
                    "Backpropagation adds gradient and optimizer-state memory, and "
                    "training can also require substantial activation storage."
                ),
            },

            {
                "id": "M07.L01.Q07",
                "section_id": "numerical-representations",
                "question": "What is the central tradeoff of reduced numerical precision?",
                "options": [
                    "Lower memory/computation at the risk of numerical error or range loss",
                    "Higher memory with perfect accuracy",
                    "More trainable parameters with fewer layers",
                    "Longer prompts with no model changes",
                ],
                "correct": 0,
                "explanation": (
                    "Fewer bits reduce storage and can accelerate computation, but "
                    "rounding and limited range can damage model quality."
                ),
            },

            {
                "id": "M07.L01.Q08",
                "section_id": "training-precision",
                "question": "What is mixed-precision training?",
                "options": [
                    "Using different precision levels for different values/operations",
                    "Training several unrelated models simultaneously",
                    "Using BM25 and vector search together",
                    "Merging several LoRA adapters by concatenation",
                ],
                "correct": 0,
                "explanation": (
                    "Mixed precision preserves higher precision where needed and "
                    "uses lower precision where it is safe."
                ),
            },

            {
                "id": "M07.L01.Q09",
                "section_id": "full-partial-peft",
                "question": "What is the main goal of PEFT?",
                "options": [
                    "Achieve strong adaptation with far fewer trainable parameters",
                    "Remove the base model entirely",
                    "Avoid all model training",
                    "Increase the context window only",
                ],
                "correct": 0,
                "explanation": (
                    "PEFT reduces training memory and compute by updating only a "
                    "small parameter set while keeping most base weights frozen."
                ),
            },

            {
                "id": "M07.L01.Q10",
                "section_id": "peft-families",
                "question": "How do soft prompts differ from ordinary hard prompts?",
                "options": [
                    "Soft prompts are trainable continuous vectors",
                    "Soft prompts are always written in natural language",
                    "Hard prompts require backpropagation",
                    "Hard prompts are stored as optimizer states",
                ],
                "correct": 0,
                "explanation": (
                    "Soft prompts are learned vector representations optimized "
                    "during tuning, rather than human-readable static text."
                ),
            },

            {
                "id": "M07.L01.Q11",
                "section_id": "lora-intuition",
                "question": "In LoRA, what is normally updated during finetuning?",
                "options": [
                    "Small low-rank matrices A and B",
                    "Every parameter in the base model",
                    "Only the tokenizer",
                    "The external retrieval index",
                ],
                "correct": 0,
                "explanation": (
                    "The original weight matrix remains frozen while low-rank "
                    "adapter matrices are trained."
                ),
            },

            {
                "id": "M07.L01.Q12",
                "section_id": "lora-configuration",
                "question": "What does the LoRA rank r primarily control?",
                "options": [
                    "The capacity and parameter count of the low-rank update",
                    "The model's context length",
                    "The number of training examples",
                    "The API rate limit",
                ],
                "correct": 0,
                "explanation": (
                    "Rank determines the inner dimension of the factorized update, "
                    "thereby controlling adapter size/capacity."
                ),
            },

            {
                "id": "M07.L01.Q13",
                "section_id": "lora-serving",
                "question": (
                    "Why keep adapters separate when serving many specializations "
                    "of one base model?"
                ),
                "options": [
                    "One base can be shared while only small adapters are swapped",
                    "It removes all inference latency",
                    "It converts the base model into BM25",
                    "It makes every adapter full-rank",
                ],
                "correct": 0,
                "explanation": (
                    "Multi-LoRA serving avoids storing a separate full model for "
                    "every task/customer."
                ),
            },

            {
                "id": "M07.L01.Q14",
                "section_id": "qlora",
                "question": "What additional memory-saving idea does QLoRA add to LoRA?",
                "options": [
                    "Low-bit quantization of the frozen base model",
                    "Training all base-model weights",
                    "Removing the LoRA adapters",
                    "Replacing training with prompting",
                ],
                "correct": 0,
                "explanation": (
                    "QLoRA preserves small trainable LoRA adapters while storing "
                    "the frozen base weights in a much lower-precision representation."
                ),
            },

            {
                "id": "M07.L01.Q15",
                "section_id": "multitask-merging",
                "question": "What problem can sequential multi-task finetuning create?",
                "options": [
                    "Catastrophic forgetting",
                    "Vector-database recall loss",
                    "Prompt caching",
                    "Tokenization mismatch",
                ],
                "correct": 0,
                "explanation": (
                    "Training on a new task can damage capabilities learned for "
                    "previous tasks."
                ),
            },

            {
                "id": "M07.L01.Q16",
                "section_id": "merging-vs-ensemble",
                "question": "How is model merging different from ensembling?",
                "options": [
                    "Merging combines parameters/components; ensembling combines outputs",
                    "They are exactly the same",
                    "Ensembling updates base-model weights",
                    "Model merging always requires several inference calls per query",
                ],
                "correct": 0,
                "explanation": (
                    "Merged models attempt to produce one combined model, while "
                    "ensembles keep constituent models separate."
                ),
            },

            {
                "id": "M07.L01.Q17",
                "section_id": "linear-merging",
                "question": "What is a task vector?",
                "options": [
                    "The difference between finetuned weights and base weights",
                    "A query embedding used for RAG",
                    "A gradient-accumulation buffer",
                    "A vector of benchmark scores",
                ],
                "correct": 0,
                "explanation": (
                    "Subtracting the base model from a finetuned model isolates the "
                    "parameter update associated with the task."
                ),
            },

            {
                "id": "M07.L01.Q18",
                "section_id": "batch-gradient-accumulation",
                "question": "What does gradient accumulation enable?",
                "options": [
                    "A larger effective batch using several smaller physical batches",
                    "Zero-memory training",
                    "Removal of all optimizer states",
                    "Automatic model merging",
                ],
                "correct": 0,
                "explanation": (
                    "Gradients from multiple small batches can be combined before "
                    "one optimizer update, approximating a larger batch."
                ),
            },

            {
                "id": "M07.L01.Q19",
                "section_id": "epochs-overfitting",
                "question": (
                    "What does decreasing training loss together with increasing "
                    "validation loss usually suggest?"
                ),
                "options": [
                    "Overfitting",
                    "The learning rate is necessarily zero",
                    "The tokenizer is corrupted",
                    "The model needs fewer parameters for inference only",
                ],
                "correct": 0,
                "explanation": (
                    "The model is improving on training examples while generalizing "
                    "worse to held-out data."
                ),
            },

            {
                "id": "M07.L01.Q20",
                "section_id": "prompt-loss-weight",
                "type": "open",
                "question": (
                    "Design a first finetuning experiment for a task where a strong "
                    "base model has the right knowledge but repeatedly fails to "
                    "produce the required specialized structured format. Explain "
                    "why you would or would not use RAG, choose a finetuning method, "
                    "describe memory constraints, pick initial hyperparameters to "
                    "test, and define how you would evaluate whether finetuning "
                    "actually improved the production use case."
                ),
            },
        ],

        "passing_score": 70,
    },
}
