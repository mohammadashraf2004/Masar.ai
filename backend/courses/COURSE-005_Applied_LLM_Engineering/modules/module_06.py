"""M06.L01 — Prompt Engineering.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Chapter 6; page range not provided in the supplied source text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M06.L01"

MODULE_ORDER = 6

MODULE_TITLE = "Prompt Engineering"

MODULE_DESCRIPTION = (
    "Learn how to work effectively with generative language models through "
    "generation controls, prompt structure, instruction design, in-context "
    "learning, prompt chaining, reasoning-oriented prompting, self-consistency, "
    "tree-style exploration, and robust output verification."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Page range not provided in supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Prompt Engineering",

    "slug": "llm-foundations-m06-l01",

    "description": (
        "A practical, learner-friendly guide to controlling and improving "
        "generative LLM behavior through model parameters, structured prompts, "
        "examples, chained prompts, reasoning-oriented techniques, and output "
        "validation or grammar-constrained generation."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.0,

    "skill_tags": [
        "prompt-engineering",
        "text-generation",
        "temperature",
        "top-p",
        "top-k",
        "chat-templates",
        "instruction-prompting",
        "few-shot-learning",
        "in-context-learning",
        "prompt-chaining",
        "reasoning-prompts",
        "self-consistency",
        "tree-of-thought",
        "output-verification",
        "structured-output",
        "constrained-decoding",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M02.L01",
        "M03.L01",
        "M04.L01",
        "M05.L01",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Prompt Engineering",

        "content": (
            r"""
# Prompt Engineering

> **Course:** Large Language Models Foundations  
> **Lesson:** M06.L01  
> **Module:** Prompt Engineering  
> **Source alignment:** Chapter 6, “Prompt Engineering.” Page numbers were not included in the supplied chapter text. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what prompt engineering is and why it is iterative.
- Load and use a generative language model through a text-generation pipeline.
- Explain the purpose of a model’s **chat template** and role tokens.
- Distinguish deterministic generation from sampling.
- Explain the effect of **temperature**, **top-p**, and **top-k**.
- Choose generation settings that suit tasks such as factual extraction, email drafting, brainstorming, and creative writing.
- Break a prompt into reusable components such as **persona, instruction, context, format, audience, tone, and data**.
- Write more specific instructions instead of vague requests.
- Explain why instruction placement can matter in long prompts.
- Distinguish **zero-shot**, **one-shot**, and **few-shot** prompting.
- Use examples to teach both task behavior and output format.
- Break complex tasks into multiple prompts using **prompt chaining**.
- Explain reasoning-oriented prompting techniques without assuming generated explanations reveal a model’s hidden internal process.
- Explain the intuition behind **self-consistency** and tree-style exploration.
- Identify why production systems must validate generated output.
- Distinguish soft guidance through examples from hard constraints through grammar or constrained decoding.
- Validate JSON output instead of assuming that a request for JSON guarantees valid JSON.
- Design prompts and output controls as parts of a complete application rather than isolated strings.

---

## 1. What is prompt engineering?

A generative language model predicts text from the input it receives.

That input is the **prompt**.

Prompt engineering is the process of deliberately designing that input so the model is more likely to produce useful output for your task.

At its simplest:

```text
Prompt
  ↓
Generative model
  ↓
Response
```

But a useful prompt often communicates more than a question.

It may specify:

```text
what to do
why to do it
what information to use
who the answer is for
what tone to use
what format to return
what the model should avoid
```

The chapter makes an important point:

> Prompt engineering is an iterative process, not a search for one universally perfect prompt.

A prompt that works well for one model may work less well for another because models differ in training, instruction tuning, context handling, and generation behavior.

{{image:prompt-engineering-feedback-loop}}

---

## 2. Start with the model, not only the prompt

Prompt quality matters, but prompts operate inside a model’s capabilities.

The chapter begins by asking whether to use:

```text
proprietary/API-hosted model
or
open/local model
```

Each has tradeoffs.

### Open/local models

Potential benefits:

- more control,
- local execution,
- easier experimentation with model internals,
- no per-request provider dependency.

Potential costs:

- hardware requirements,
- setup complexity,
- local inference optimization.

### Proprietary/API-hosted models

Potential benefits:

- easy access to large models,
- provider-managed infrastructure,
- no requirement to host weights locally.

Potential costs:

- usage charges,
- rate limits,
- less transparency and control,
- external data handling considerations.

The chapter recommends learning with a smaller foundation model and uses Phi-3-mini as its practical example.

The general learning principle is:

> Start with a model small enough that you can experiment rapidly and understand the behavior before scaling up.

---

## 3. Load a text-generation model

The chapter uses Hugging Face Transformers:

```python
import torch

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    pipeline,
)
```

Load the model:

```python
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    device_map="cuda",
    torch_dtype="auto",
    trust_remote_code=True,
)
```

Load its tokenizer:

```python
tokenizer = AutoTokenizer.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct"
)
```

Create the text-generation pipeline:

```python
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    return_full_text=False,
    max_new_tokens=500,
    do_sample=False,
)
```

This pipeline handles several operations for us:

```text
chat messages
→ prompt template
→ tokenization
→ generation
→ decoding
```

### Basic message

```python
messages = [
    {
        "role": "user",
        "content": "Create a funny joke about chickens.",
    }
]

output = pipe(messages)

print(output[0]["generated_text"])
```

The visible input looks simple, but the model does not necessarily receive that exact string.

A chat model normally expects a specific conversation format.

---

## 4. Chat templates are part of the interface

The chapter inspects the model’s chat template:

```python
prompt = pipe.tokenizer.apply_chat_template(
    messages,
    tokenize=False,
)

print(prompt)
```

The source example becomes something conceptually like:

```text
<s><|user|>
Create a funny joke about chickens.<|end|>
<|assistant|>
```

Those tokens communicate structure.

For example:

```text
<|user|>
```

marks the user’s message.

```text
<|assistant|>
```

marks where the assistant response begins.

```text
<|end|>
```

marks a message boundary/end.

This is why you should not treat chat formatting as decoration.

The model was trained to interpret a particular structure.

[[IMAGE_NEEDED: Chat template transformation | Show a Python messages list with user/assistant roles on the left and the model-specific serialized prompt with special role and end tokens on the right | Learner should notice that the chat API/pipeline transforms conversational messages into a model-specific token sequence]]

### Practical rule

When a library provides the model’s official chat template, prefer using it instead of manually guessing the special-token format.

---

## 5. Prompt wording is not the only control

The same prompt can produce different outputs depending on generation settings.

Recall from Chapter 3:

```text
model
→ scores candidate next tokens
→ decoding process chooses one
```

Prompt engineering changes **what information and instructions** the model receives.

Generation parameters change **how candidate tokens are selected**.

Both affect the final output.

The chapter focuses on:

- `do_sample`,
- `temperature`,
- `top_p`,
- `top_k`.

---

## 6. Deterministic selection versus sampling

If:

```python
do_sample=False
```

the pipeline avoids stochastic sampling and behaves more deterministically.

At a simplified level:

```text
candidate      relative score
--------------------------------
car            very high
truck          high
vehicle        medium
elephant       very low
```

A deterministic decoder tends to select the strongest candidate.

With sampling enabled:

```python
do_sample=True
```

lower-ranked but still plausible candidates can sometimes be selected.

That creates variety.

[[IMAGE_NEEDED: Deterministic versus sampled next-token selection | Show one probability distribution over candidate next tokens; left path always selects the highest candidate, right path samples among candidates according to adjusted probabilities | Learner should distinguish model probabilities from the decoding policy that chooses the actual output token]]

### Important mental model

```text
PROMPT
controls what the model is asked

SAMPLING SETTINGS
control how the model chooses among candidate continuations
```

These are different levers.

---

## 7. Temperature: control how sharp the choice feels

The chapter describes **temperature** as a control over output randomness or creativity.

A lower temperature generally concentrates selection around highly likely tokens.

A higher temperature makes lower-probability candidates more competitive.

Conceptually:

```text
LOW TEMPERATURE

car       ███████████████████
truck     ████
vehicle   ██
elephant  tiny
```

versus:

```text
HIGHER TEMPERATURE

car       ███████████
truck     ███████
vehicle   █████
elephant  ██
```

The exact probabilities depend on the model and implementation, but the learning intuition is:

```text
lower temperature
→ more conservative / repeatable

higher temperature
→ more varied / surprising
```

### Example

```python
output = pipe(
    messages,
    do_sample=True,
    temperature=1.0,
)
```

Repeated runs can produce different text.

[[IMAGE_NEEDED: Temperature comparison | Show the same candidate-token distribution at low and high temperature, with low temperature sharply concentrated on top choices and high temperature flatter across more alternatives | Learner should understand temperature as reshaping the distribution rather than directly adding random words]]

### Match temperature to the task

For tasks requiring predictable output:

```text
classification
structured extraction
factual transformation
format-sensitive automation
```

lower randomness is often attractive.

For tasks such as:

```text
brainstorming
creative writing
idea generation
```

more variation may be useful.

---

## 8. top-p and top-k: restrict the candidate pool

Temperature changes the shape of the distribution.

`top_p` and `top_k` restrict which candidates are considered.

### top-p — nucleus sampling

With top-p sampling, the model considers the smallest high-probability candidate set whose cumulative probability reaches a threshold.

Simplified distribution:

```text
A  0.40
B  0.30
C  0.15
D  0.10
E  0.05
```

If:

```text
top_p = 0.70
```

the candidate nucleus may include:

```text
A + B
```

because:

```text
0.40 + 0.30 = 0.70
```

If:

```text
top_p = 1.0
```

all candidates remain eligible.

### top-k

`top_k` instead limits the number of candidates directly.

Example:

```text
top_k = 3
```

means only the three highest-scoring tokens are considered for sampling.

[[IMAGE_NEEDED: top-p versus top-k | Show one ranked token probability list; highlight a cumulative-probability nucleus for top-p and exactly the top K entries for top-k | Learner should understand that top-p uses probability mass while top-k uses a fixed candidate count]]

### Use them intentionally

The chapter’s high-level examples connect:

```text
high randomness + large candidate pool
→ brainstorming / diverse generation

low randomness + narrower candidate pool
→ more focused generation
```

Do not treat one configuration as universally optimal.

The best settings depend on the task.

---

## 9. The basic ingredients of a prompt

A prompt can be as small as:

```text
The capital of France is
```

The model may simply continue the text.

But task-oriented prompting usually needs more structure.

The minimum useful decomposition is often:

```text
instruction
+
data
```

Example:

```text
Instruction:
Classify the sentiment as positive or negative.

Data:
The movie was beautifully acted but painfully slow.
```

You can further add an output indicator:

```text
Text:
The movie was beautifully acted but painfully slow.

Sentiment:
```

This nudges the model toward a compact classification-style completion.

[[IMAGE_NEEDED: Prompt anatomy basics | Show a prompt divided into three labeled blocks—Instruction, Data, and Output Indicator—with arrows showing how each constrains the model response | Learner should see that a prompt can be designed from modular components]]

### Why modular thinking helps

Instead of asking:

```text
"Is this a good prompt?"
```

ask:

```text
Is the instruction clear?
Is the data separated?
Is the desired output obvious?
Is important context missing?
```

This turns prompt improvement into an engineering process.

---

## 10. Specificity: say what success looks like

Compare:

```text
Write a description for a product.
```

with:

```text
Write a formal product description in no more than two sentences.
Focus on the product's practical benefit.
```

The second prompt reduces ambiguity.

Specificity can define:

- task,
- length,
- scope,
- output labels,
- allowed sources,
- target audience,
- tone,
- format,
- constraints.

The core principle is:

> If a requirement matters to the application, communicate it explicitly.

Do not expect the model to infer all hidden requirements.

### Handling uncertainty

The chapter suggests instructions such as:

```text
If you do not know the answer, say "I don't know."
```

as one way to reduce unsupported answers.

This does not guarantee factual correctness, but it communicates an abstention behavior the application prefers.

For high-stakes systems, prompt wording alone is not sufficient verification; later sections explain why outputs must also be checked.

---

## 11. Prompt order can matter

The chapter discusses evidence that language models can pay less attention to information buried in the middle of long contexts.

A useful practical strategy is to place critical instructions prominently:

```text
near the beginning
or
near the end
```

rather than hiding them among large amounts of unrelated text.

For long prompts, structure also helps:

```text
# Task
...

# Constraints
...

# Context
...

# Input
...

# Output format
...
```

This is easier for humans to audit and can make requirements clearer to the model.

### Do not overinterpret this as a universal law

Model behavior changes across architectures and context lengths.

Treat prompt order as something to test empirically for the model and task you deploy.

---

## 12. Build prompts from reusable components

The chapter lists several common prompt components.

### Persona

What role should the model adopt?

```text
You are an expert in large language models.
```

### Instruction

What should it do?

```text
Summarize the key findings of the paper.
```

### Context

Why is the task being done?

```text
The summary should help researchers quickly identify the paper's most important contribution.
```

### Format

How should the result be structured?

```text
Use bullet points for the method, followed by one concise results paragraph.
```

### Audience

Who will read the result?

```text
The audience is busy ML researchers.
```

### Tone

How should it sound?

```text
Use a professional and clear tone.
```

### Data

What content should the model process?

```text
Text to summarize:
...
```

[[IMAGE_NEEDED: Modular prompt components | Show a prompt assembled from separate labeled blocks: Persona, Instruction, Context, Format, Audience, Tone, and Data | Learner should see prompt design as composable rather than as one unstructured paragraph]]

### Example assembly

```python
persona = (
    "You are an expert in Large Language Models. "
    "You excel at breaking down complex papers "
    "into digestible summaries.\n"
)

instruction = (
    "Summarize the key findings of the paper provided.\n"
)

context = (
    "Extract the most crucial points that help researchers "
    "understand the contribution quickly.\n"
)

data_format = (
    "Use bullet points for the method, followed by a concise "
    "paragraph describing the main results.\n"
)

audience = (
    "The summary is for busy researchers following recent "
    "Large Language Model work.\n"
)

tone = "Use a professional and clear tone.\n"

text = "MY TEXT TO SUMMARIZE"

data = f"Text to summarize: {text}"

query = (
    persona
    + instruction
    + context
    + data_format
    + audience
    + tone
    + data
)
```

The lesson is not that every prompt must contain all seven components.

The lesson is that you can add, remove, reorder, and test components deliberately.

---

## 13. Prompt engineering is controlled experimentation

A strong workflow is:

```text
1. Define what success means.
2. Write the simplest prompt that expresses the task.
3. Test on representative examples.
4. Record failures.
5. Change one or a small number of components.
6. Test again.
7. Compare results.
```

Avoid randomly changing everything at once.

Otherwise you will not know what improved or damaged performance.

### Build a prompt evaluation set

For a real application, keep representative examples such as:

```text
easy case
ambiguous case
long input
short input
edge case
adversarial or malformed input
format-sensitive case
```

Then compare prompt versions across the same examples.

This turns prompt engineering from intuition into evaluation.

---

## 14. In-context learning: show the task instead of only describing it

Sometimes an instruction is difficult to explain precisely.

Examples can communicate expected behavior directly.

This is **in-context learning**.

The chapter distinguishes:

```text
zero-shot
→ no examples

one-shot
→ one example

few-shot
→ two or more examples
```

[[IMAGE_NEEDED: Zero-shot one-shot few-shot | Three prompt diagrams: instruction only, instruction plus one demonstration, and instruction plus several demonstrations | Learner should understand that the difference is the number of examples supplied in the current context]]

### Why examples help

An example teaches both:

```text
what the task means
and
what the output should look like
```

Suppose the task uses a made-up word.

Instead of only defining:

```text
A Gigamuru is a Japanese musical instrument.
```

you can demonstrate:

```text
User:
A Gigamuru is a type of Japanese musical instrument.
Give an example sentence.

Assistant:
I have a Gigamuru that my uncle gave me as a gift.
```

Then ask the same kind of question for a second invented word.

The model can infer the pattern from the interaction.

---

## 15. Examples can teach structure, not only meaning

Few-shot prompting is also useful for output formatting.

Suppose you need exactly:

```json
{
  "description": "...",
  "name": "...",
  "armor": "...",
  "weapon": "..."
}
```

Providing a concrete example can make the desired schema easier to follow than saying only:

```text
Return JSON.
```

But remember:

> Examples are guidance, not a hard guarantee.

A model can still produce malformed output, add fields, or stop early.

This distinction becomes important in production systems.

---

## 16. Prompt chaining: solve a large task as smaller tasks

A single prompt can become overloaded.

Instead, break the job into stages.

The chapter gives a product-creation example.

One possible chain is:

```text
product features
      ↓
Prompt 1
      ↓
product name + slogan
      ↓
Prompt 2
      ↓
sales pitch
```

The output of one call becomes input to the next.

[[IMAGE_NEEDED: Prompt chaining pipeline | Show product features entering Prompt 1 to generate name/slogan, then those outputs plus original features entering Prompt 2 to generate a sales pitch | Learner should see how intermediate outputs become inputs to later stages]]

### Example

First stage:

```python
product_prompt = [
    {
        "role": "user",
        "content": (
            "Create a name and slogan for a chatbot "
            "that leverages LLMs."
        ),
    }
]

outputs = pipe(product_prompt)

product_description = outputs[0]["generated_text"]
```

Second stage:

```python
sales_prompt = [
    {
        "role": "user",
        "content": (
            "Generate a very short sales pitch for "
            f"the following product: {product_description}"
        ),
    }
]

outputs = pipe(sales_prompt)

sales_pitch = outputs[0]["generated_text"]
```

### Why chaining can help

Each stage has a narrower job.

That means you can independently control:

```text
instructions
generation length
temperature
format
validation
```

for each stage.

It also makes debugging easier.

If the final sales pitch is poor, you can inspect whether the problem came from:

```text
the name
the slogan
or
the pitch generation
```

---

## 17. Useful chaining patterns

The chapter mentions several patterns.

### Response validation

```text
generator
   ↓
draft output
   ↓
validator / checker
   ↓
accept or revise
```

### Parallel generation

```text
same task
  ↙  ↓  ↘
A   B   C
 \  |  /
  merge
```

This can produce multiple candidate ideas before synthesis.

### Long-form writing

A large writing task can be decomposed into:

```text
summary
→ characters
→ outline
→ scenes
→ dialogue
```

Instead of asking for an entire complex artifact in one generation.

### Engineering principle

Prompt chaining introduces more calls and more state, but it also gives you:

```text
modularity
observability
specialization
independent validation
```

This becomes a stepping stone toward larger LLM systems and agentic workflows.

---

{{exercise:M06.L01.EX01}}

---

## 18. Reasoning-oriented prompting

The chapter next explores prompting methods designed to improve performance on tasks requiring multiple intermediate steps.

It discusses these behaviors using an analogy to slower, deliberate reasoning.

A crucial caution for learners:

> A model-generated explanation is visible output, not a guaranteed transcript of the model's hidden internal computation.

It can still be useful as a structured problem-solving artifact.

The practical objective is to give the model a sequence of intermediate steps or subproblems that can improve the final result.

---

## 19. Chain-of-thought-style prompting: create intermediate steps

The chapter introduces **chain-of-thought prompting** through worked examples.

For a simple arithmetic problem:

```text
Roger has 5 tennis balls.
He buys 2 cans.
Each can contains 3 balls.
How many does he have?
```

a demonstrated solution can break the task into:

```text
2 cans × 3 balls = 6
5 existing + 6 new = 11
answer = 11
```

Then a new problem is presented with the expectation of a similarly structured explanation.

The useful engineering intuition is:

```text
hard task
↓
explicit intermediate substeps
↓
final answer
```

This can help with tasks where solving everything in one jump is difficult.

[[IMAGE_NEEDED: Reasoning-oriented prompt structure | Show problem → intermediate substeps/calculations → final answer, with a note that the visible explanation is generated output rather than a guaranteed view of hidden internal computation | Learner should understand the purpose of structured intermediate reasoning without confusing it with model internals]]

### Zero-shot reasoning instruction

The chapter also demonstrates an instruction such as:

```text
Let's think step-by-step.
```

rather than giving an example.

This can encourage the model to produce a structured explanation.

For application design, it is often more useful to ask for **specific intermediate artifacts** than a generic reasoning phrase.

For example:

```text
1. Extract the known quantities.
2. State the formula.
3. Substitute the values.
4. Calculate the result.
5. Return the final answer.
```

That structure is easier to evaluate.

---

## 20. Self-consistency: sample several candidate solutions

Sampling introduces variation.

One run may make a mistake while another succeeds.

Self-consistency uses multiple sampled solutions.

Conceptually:

```text
same problem
  ↓
sample 1 → answer A
sample 2 → answer B
sample 3 → answer A
sample 4 → answer A
sample 5 → answer C
  ↓
aggregate / vote
  ↓
answer A
```

[[IMAGE_NEEDED: Self-consistency voting | Show one prompt branching into several independently sampled reasoning/output paths and then a majority-vote or aggregation node | Learner should see how repeated sampling trades additional compute for robustness]]

### Why sampling matters

If all runs are deterministic and identical, repeated calls add no diversity.

Self-consistency is most relevant when generation settings allow alternative paths.

### Cost tradeoff

If you generate `n` candidate solutions:

```text
roughly n times more generation work
```

is required before aggregation.

So self-consistency can improve reliability in some settings but is slower and more expensive.

---

## 21. Tree-style exploration: consider multiple intermediate possibilities

Some problems have branching possibilities.

Instead of choosing one intermediate step immediately, a system can explore several candidates.

Conceptually:

```text
start
 ├─ idea A
 │   ├─ A1
 │   └─ A2
 ├─ idea B
 │   ├─ B1
 │   └─ B2
 └─ idea C
     ├─ C1
     └─ C2
```

Then evaluate:

```text
Which branches look promising?
Which should be pruned?
Which should continue?
```

The chapter discusses **tree-of-thought** as a method inspired by this process.

[[IMAGE_NEEDED: Tree-style solution exploration | Show one problem branching into several candidate intermediate ideas, each evaluated, weak branches pruned, and promising branches expanded toward a final answer | Learner should see the contrast between one linear solution path and deliberate branch exploration]]

### Why it can help

Tree-style exploration can be useful for:

```text
creative ideation
planning
story design
search problems
multi-step decision spaces
```

### Why it can be expensive

A true branching search may require many model calls.

More branches mean:

```text
more generation
more evaluation
more latency
more cost
```

The chapter also discusses single-prompt simulations of multiple experts.

Those can be creative and useful, but they are not equivalent to a full external search procedure with independently evaluated branches.

---

## 22. Production systems must verify output

A demo can tolerate messy text.

A production application often cannot.

The chapter gives four broad reasons to validate model output.

### Structured output

The application may require:

```text
JSON
XML
CSV
specific fields
database-ready values
```

### Valid output

Even if the structure is valid, the content may violate allowed choices.

Example:

```text
allowed:
positive
negative

model returns:
mixed
```

The string is readable but invalid for the application.

### Safety and policy constraints

An application may require checks for:

- profanity,
- PII,
- harmful content,
- bias or stereotypes,
- domain-specific prohibited content.

### Accuracy

The model may produce:

```text
well-written
confident
incorrect
```

text.

Validation can include factual checks, consistency checks, source verification, or task-specific business rules.

[[IMAGE_NEEDED: Generation plus validation architecture | Show LLM generation flowing through separate checks for schema, allowed values, safety/policy, and factual/task validation before output is accepted | Learner should understand that production reliability requires layers beyond prompting]]

---

## 23. Three ways to control output

The chapter groups output control into:

```text
1. Examples
2. Grammar / constrained generation
3. Fine-tuning
```

This chapter focuses on the first two.

### Examples

Examples guide behavior.

They tell the model:

```text
"This is what a good output looks like."
```

### Grammar / constrained generation

Constraints can prevent invalid tokens or structures from being emitted.

They tell the decoder:

```text
"Only outputs matching these rules are legal."
```

### Fine-tuning

Fine-tuning changes the model parameters to better produce desired behavior.

The chapter postpones that topic to a later chapter.

The key distinction is:

```text
examples
→ soft guidance

grammar
→ harder decoding constraint

fine-tuning
→ changes learned model behavior
```

---

## 24. Asking for JSON is not the same as guaranteeing JSON

Suppose you write:

```text
Create a character profile for an RPG game in JSON format.
```

The model may begin correctly and then:

- omit a closing brace,
- stop before completing a field,
- add markdown fences,
- add unexpected attributes,
- produce values that violate your schema.

The chapter shows exactly this kind of failure when generation stops partway through a JSON object.

### Improve with an example

A more explicit template is:

```text
Return only this structure:

{
  "description": "A SHORT DESCRIPTION",
  "name": "THE CHARACTER'S NAME",
  "armor": "ONE PIECE OF ARMOR",
  "weapon": "ONE OR MORE WEAPONS"
}
```

This often improves consistency.

But:

> Prompt examples still do not guarantee syntactically valid JSON.

Your application should parse and validate the result.

---

## 25. Grammar-constrained generation

A stronger technique is to constrain token generation itself.

Suppose the only valid outputs are:

```text
positive
neutral
negative
```

A prompt can request those words.

But a model might still generate:

```text
mostly positive
```

or:

```text
I think it is positive.
```

A constrained decoder can restrict the legal next-token paths so only valid outputs can be produced.

Conceptually:

```text
ordinary generation:
all vocabulary tokens may be candidates

constrained generation:
only tokens allowed by the grammar/schema
remain eligible
```

[[IMAGE_NEEDED: Normal sampling versus constrained sampling | Left side shows a wide set of possible next tokens including invalid outputs; right side shows a grammar filter removing illegal candidates so only schema-valid tokens can be selected | Learner should understand that constraints act during decoding rather than merely asking the model politely]]

This is a major production insight:

> If structure is a hard requirement, enforce it mechanically where possible instead of relying only on natural-language instructions.

---

## 26. JSON-constrained generation example

The chapter demonstrates JSON-constrained output using `llama-cpp-python` and a GGUF version of Phi-3.

Load the model:

```python
from llama_cpp.llama import Llama

llm = Llama.from_pretrained(
    repo_id="microsoft/Phi-3-mini-4k-instruct-gguf",
    filename="*fp16.gguf",
    n_gpu_layers=-1,
    n_ctx=2048,
    verbose=False,
)
```

Then request JSON output:

```python
output = llm.create_chat_completion(
    messages=[
        {
            "role": "user",
            "content": (
                "Create a warrior for an RPG "
                "in JSON format."
            ),
        },
    ],
    response_format={
        "type": "json_object"
    },
    temperature=0,
)["choices"][0]["message"]["content"]
```

Finally, actually parse it:

```python
import json

parsed = json.loads(output)

json_output = json.dumps(
    parsed,
    indent=4,
)

print(json_output)
```

The parsing step is crucial.

If:

```python
json.loads(output)
```

succeeds, you have evidence that the string is syntactically valid JSON.

### Syntax validity is not semantic validity

Even valid JSON could contain:

```json
{
  "sentiment": "banana"
}
```

when your allowed values are:

```text
positive
neutral
negative
```

So production validation may need several layers:

```text
1. valid syntax
2. valid schema
3. allowed values
4. business rules
5. safety checks
6. factual/task verification
```

---

## 27. Design a robust generation pipeline

Prompt engineering works best when combined with validation.

A strong application pattern is:

```text
INPUT
  ↓
construct prompt
  ↓
generate
  ↓
parse
  ↓
validate structure
  ↓
validate allowed values
  ↓
validate task rules
  ↓
accept / retry / repair / escalate
```

Do not collapse all these responsibilities into one giant prompt.

### Example: sentiment API

Requirement:

```text
Output exactly one label:
positive
neutral
negative
```

A robust design might use:

```text
Prompt:
Classify the sentiment.

Decoder:
Restrict output to allowed labels.

Parser:
Normalize output.

Validator:
Reject anything outside allowed enum.

Monitoring:
Record failures and edge cases.
```

That is stronger than:

```text
"Please return only positive, neutral, or negative."
```

alone.

---

{{exercise:M06.L01.EX02}}

---

## 28. A practical prompt-engineering decision guide

When a model is giving poor results, diagnose the failure before adding random prompt text.

### If the task is unclear

Improve:

```text
instruction
context
examples
```

### If the output is too long or unfocused

Improve:

```text
scope
length constraint
format
generation settings
```

### If output varies too much

Consider:

```text
lower randomness
more explicit examples
structured outputs
```

### If the model misunderstands the format

Use:

```text
one-shot/few-shot examples
explicit schema
constrained generation
parser validation
```

### If a task is too complex

Use:

```text
task decomposition
prompt chaining
intermediate structured artifacts
```

### If several plausible reasoning paths exist

Consider:

```text
multiple candidate generations
self-consistency
branch exploration
external scoring/verification
```

### If correctness is critical

Do not rely on prompt wording alone.

Add:

```text
source grounding
tool checks
business rules
parsers
validators
human review where appropriate
```

---

## Important misconceptions

### Misconception 1

> Prompt engineering is about discovering one magical sentence.

### Why this is wrong

It is an iterative design and evaluation process involving instructions, examples, context, structure, generation settings, and validation.

---

### Misconception 2

> Temperature adds creativity by inserting random words.

### Why this is wrong

Temperature changes the relative distribution used when sampling next-token candidates. The model still samples from candidates produced by its learned probability structure.

---

### Misconception 3

> top-p and temperature are the same thing.

### Why this is wrong

Temperature reshapes candidate probabilities, while top-p restricts the candidate set according to cumulative probability mass.

---

### Misconception 4

> A persona automatically gives the model expert-level factual knowledge.

### Why this is wrong

A persona changes framing and response style. It does not create knowledge the model lacks or guarantee correctness.

---

### Misconception 5

> Few-shot examples permanently train the model.

### Why this is wrong

In-context examples guide behavior within the current context. They do not update the model weights.

---

### Misconception 6

> Breaking a task into multiple prompts is always cheaper.

### Why this is wrong

Prompt chaining can improve modularity and quality, but it requires additional model calls and therefore increases latency and compute/API usage.

---

### Misconception 7

> A generated step-by-step explanation is guaranteed to reveal the model's true hidden reasoning process.

### Why this is wrong

It is generated text that may serve as a useful structured explanation, but it should not be treated as a verified transcript of hidden internal computation.

---

### Misconception 8

> Asking for JSON guarantees valid JSON.

### Why this is wrong

Natural-language instructions are soft guidance. The model may still produce invalid or incomplete output.

---

### Misconception 9

> If JSON parses successfully, the output must be correct.

### Why this is wrong

Syntactic validity does not guarantee correct values, correct semantics, factual accuracy, or compliance with application rules.

---

## Key terminology

| Term | Meaning |
|---|---|
| Prompt | Input given to a generative model |
| Prompt engineering | Iterative design of prompts to improve task performance and output behavior |
| Chat template | Model-specific serialization of roles/messages using special tokens |
| Sampling | Selecting an output token from a probability distribution |
| Temperature | Parameter that adjusts how concentrated or varied sampled token probabilities are |
| top-p | Nucleus-sampling threshold based on cumulative probability mass |
| top-k | Sampling restriction to the K highest-scoring candidate tokens |
| Instruction prompting | Explicitly telling the model what task to perform |
| Persona | Prompt component describing the role/style the model should adopt |
| Context | Supporting information explaining the situation or purpose |
| Format | Required structure of the response |
| Audience | Intended reader/user of the generated output |
| Tone | Desired style or voice |
| Zero-shot prompting | Performing a task without demonstrations in the prompt |
| One-shot prompting | Providing one demonstration |
| Few-shot prompting | Providing multiple demonstrations |
| In-context learning | Using examples in the current prompt/context to guide behavior |
| Prompt chaining | Feeding outputs from one model call into later model calls |
| Reasoning-oriented prompting | Prompt structures that request or demonstrate intermediate problem-solving artifacts |
| Self-consistency | Sampling several candidate solutions and aggregating their final results |
| Tree-style exploration | Exploring multiple intermediate branches before selecting/continuing promising ones |
| Output verification | Checking generated content against required rules |
| Structured output | Output following a machine-readable structure such as JSON |
| Grammar constraint | Rule restricting which token sequences are valid during decoding |
| Constrained decoding | Token selection that enforces a grammar/schema or allowed output space |
| Exponential backoff | Retry strategy with progressively longer waits, relevant to external API rate limits |
| Schema validation | Checking that structured output has required fields/types/constraints |

---

## Self-check

Before moving on, make sure you can answer:

1. What is prompt engineering?
2. Why is it better understood as an iterative process than as a search for one perfect prompt?
3. What does a chat template do?
4. Why should a chat model normally use the template it was trained with?
5. What does `do_sample=False` change conceptually?
6. How does low temperature differ from high temperature?
7. How does top-p differ from top-k?
8. What are the basic instruction and data components of a prompt?
9. What does an output indicator do?
10. Name at least five modular prompt components.
11. Why does specificity matter?
12. Why can prompt order matter in long contexts?
13. What is the difference between zero-shot, one-shot, and few-shot prompting?
14. Why can examples improve output formatting?
15. What is prompt chaining?
16. What is one advantage and one cost of prompt chaining?
17. What is the purpose of reasoning-oriented prompting?
18. What important caveat applies to generated step-by-step explanations?
19. What is self-consistency?
20. Why is self-consistency more expensive than a single generation?
21. What is tree-style exploration trying to accomplish?
22. Why must production systems validate model output?
23. Why does asking for JSON not guarantee valid JSON?
24. What is the difference between example-based guidance and grammar-constrained generation?
25. Why should valid JSON still be checked against a schema or allowed values?
26. Design a robust pipeline for a model that must output one of three allowed labels.

---

## Retain this idea

**Prompt engineering is not merely clever wording. It is the deliberate design of the complete interaction between an application and a generative model: the task instruction, context, examples, output format, audience, tone, generation settings, multi-step workflow, and verification layer. Prompts guide behavior; decoding settings shape variability; examples demonstrate expectations; chaining decomposes complexity; and validation or grammar constraints make outputs safer to consume programmatically.**
"""
        ),

        "estimated_minutes": 180,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-prompt-engineering", "title": "What is prompt engineering?", "order": 1},
            {"id": "choosing-model", "title": "Start with the model, not only the prompt", "order": 2},
            {"id": "load-model", "title": "Load a text-generation model", "order": 3},
            {"id": "chat-template", "title": "Chat templates are part of the interface", "order": 4},
            {"id": "generation-controls", "title": "Prompt wording is not the only control", "order": 5},
            {"id": "sampling", "title": "Deterministic selection versus sampling", "order": 6},
            {"id": "temperature", "title": "Temperature: control how sharp the choice feels", "order": 7},
            {"id": "top-p-top-k", "title": "top-p and top-k: restrict the candidate pool", "order": 8},
            {"id": "prompt-anatomy", "title": "The basic ingredients of a prompt", "order": 9},
            {"id": "specificity", "title": "Specificity: say what success looks like", "order": 10},
            {"id": "instruction-order", "title": "Prompt order can matter", "order": 11},
            {"id": "complex-components", "title": "Build prompts from reusable components", "order": 12},
            {"id": "prompt-iteration", "title": "Prompt engineering is controlled experimentation", "order": 13},
            {"id": "in-context-learning", "title": "In-context learning: show the task instead of only describing it", "order": 14},
            {"id": "few-shot-format", "title": "Examples can teach structure, not only meaning", "order": 15},
            {"id": "prompt-chaining", "title": "Prompt chaining: solve a large task as smaller tasks", "order": 16},
            {"id": "chain-patterns", "title": "Useful chaining patterns", "order": 17},
            {"id": "reasoning-intro", "title": "Reasoning-oriented prompting", "order": 18},
            {"id": "cot", "title": "Chain-of-thought-style prompting: create intermediate steps", "order": 19},
            {"id": "self-consistency", "title": "Self-consistency: sample several candidate solutions", "order": 20},
            {"id": "tree-exploration", "title": "Tree-style exploration: consider multiple intermediate possibilities", "order": 21},
            {"id": "verification", "title": "Production systems must verify output", "order": 22},
            {"id": "three-controls", "title": "Three ways to control output", "order": 23},
            {"id": "json-example", "title": "Asking for JSON is not the same as guaranteeing JSON", "order": 24},
            {"id": "constrained-decoding", "title": "Grammar-constrained generation", "order": 25},
            {"id": "llama-cpp-json", "title": "JSON-constrained generation example", "order": 26},
            {"id": "verification-pipeline", "title": "Design a robust generation pipeline", "order": 27},
            {"id": "decision-guide", "title": "A practical prompt-engineering decision guide", "order": 28},
            {"id": "misconceptions", "title": "Important misconceptions", "order": 29},
            {"id": "terminology", "title": "Key terminology", "order": 30},
            {"id": "self-check", "title": "Self-check", "order": 31},
            {"id": "retain", "title": "Retain this idea", "order": 32},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M06.L01.EX01",

            "title": "Engineer and Evaluate a Prompt Iteratively",

            "lesson_code": "M06.L01",

            "section_id": "chain-patterns",

            "placement": "after_section",

            "description": (
                "Practice prompt construction, generation controls, few-shot examples, "
                "and modular iteration using a repeatable evaluation set."
            ),

            "instructions": (
                "Choose one task such as summarization, sentiment classification, "
                "product-description generation, or information extraction.\n"
                "1. Create 8–12 representative test inputs for the task.\n"
                "2. Write a minimal zero-shot prompt containing only an instruction "
                "and the input data.\n"
                "3. Run or conceptually evaluate the prompt on every test input and "
                "record at least three failure modes.\n"
                "4. Create a second version by adding explicit output requirements "
                "such as length, format, allowed labels, or tone.\n"
                "5. Create a third version using one or more examples.\n"
                "6. Compare deterministic generation with a sampling configuration "
                "appropriate to the task.\n"
                "7. Change only one major prompt component at a time and record its "
                "effect.\n"
                "8. If the task has multiple stages, create a chained version with "
                "at least two prompts and inspect the intermediate output.\n"
                "9. Build a simple evaluation table covering correctness, format "
                "compliance, consistency, and usefulness.\n"
                "10. Conclude which prompt components materially improved this specific "
                "task and which added complexity without measurable benefit."
            ),

            "expected_output": (
                "A notebook or written experiment containing at least three prompt "
                "versions, a fixed evaluation set, generation settings, observed "
                "failures, a comparison table, and a short evidence-based explanation "
                "of the final prompt design."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "prompt-decomposition",
                "specificity",
                "few-shot-learning",
                "generation-controls",
                "prompt-evaluation",
                "prompt-chaining",
            ],
        },

        {
            "id": "M06.L01.EX02",

            "title": "Build a Robust Structured-Output Pipeline",

            "lesson_code": "M06.L01",

            "section_id": "verification-pipeline",

            "placement": "after_section",

            "description": (
                "Move beyond prompt-only control by designing parsing and validation "
                "for machine-consumable LLM output."
            ),

            "instructions": (
                "Design a model call that extracts a support ticket into the following "
                "fields: `category`, `priority`, `summary`, and `needs_human`.\n"
                "1. Define the allowed values for `category` and `priority`.\n"
                "2. Write a clear prompt describing the schema and input ticket.\n"
                "3. Add one valid example output.\n"
                "4. Generate or mock three model outputs: one valid, one syntactically "
                "invalid JSON, and one syntactically valid JSON containing an invalid "
                "category.\n"
                "5. Parse the output as JSON.\n"
                "6. Validate required keys and data types.\n"
                "7. Validate enum values and at least one business rule.\n"
                "8. Define what the application should do on validation failure "
                "(retry, repair, fallback, or human review).\n"
                "9. Explain how grammar-constrained decoding would reduce some failure "
                "modes but would not guarantee factual correctness.\n"
                "10. Produce the final end-to-end pipeline diagram or ordered steps."
            ),

            "expected_output": (
                "A schema definition, prompt, example output, three test cases, parsing "
                "and validation logic or pseudocode, failure-handling policy, and an "
                "explanation of the difference between syntactic and semantic validity."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "structured-output",
                "few-shot-formatting",
                "json-validation",
                "schema-validation",
                "constrained-decoding",
                "production-llm-design",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M06.L01.QZ01",

        "title": "Prompt Engineering — Knowledge Check",

        "lesson_code": "M06.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M06.L01.Q01",
                "section_id": "why-prompt-engineering",
                "question": "Which description best matches prompt engineering?",
                "options": [
                    "Finding one magical phrase that works for every model and task",
                    "Iteratively designing model input to improve task behavior and output quality",
                    "Changing the model weights after every user message",
                    "Only increasing the prompt length",
                ],
                "correct": 1,
                "explanation": (
                    "Prompt engineering is an iterative design and evaluation process, "
                    "not a single universal wording trick."
                ),
            },
            {
                "id": "M06.L01.Q02",
                "section_id": "chat-template",
                "question": "Why does a chat template matter?",
                "options": [
                    "It communicates role and message structure in the format the chat model expects.",
                    "It replaces model weights.",
                    "It guarantees factual accuracy.",
                    "It increases GPU VRAM.",
                ],
                "correct": 0,
                "explanation": (
                    "Chat templates serialize messages into the role/special-token "
                    "format used during model training and inference."
                ),
            },
            {
                "id": "M06.L01.Q03",
                "section_id": "temperature",
                "question": "What is the general effect of increasing temperature during sampling?",
                "options": [
                    "It always shortens output.",
                    "It makes lower-probability candidates relatively more competitive, usually increasing variation.",
                    "It removes the tokenizer.",
                    "It forces greedy decoding.",
                ],
                "correct": 1,
                "explanation": (
                    "Higher temperature generally flattens the effective sampling "
                    "distribution and allows more varied token choices."
                ),
            },
            {
                "id": "M06.L01.Q04",
                "section_id": "top-p-top-k",
                "question": "How does top-p differ from top-k?",
                "options": [
                    "top-p selects by cumulative probability mass, while top-k limits the fixed number of top candidates.",
                    "top-p controls prompt length while top-k controls context length.",
                    "top-p changes model weights while top-k changes the tokenizer.",
                    "They are exactly the same parameter under two names.",
                ],
                "correct": 0,
                "explanation": (
                    "Nucleus sampling uses a probability-mass threshold; top-k uses "
                    "a fixed candidate count."
                ),
            },
            {
                "id": "M06.L01.Q05",
                "section_id": "prompt-anatomy",
                "question": "What are the two most basic components of a task-oriented prompt in this lesson?",
                "options": [
                    "Instruction and data",
                    "Temperature and GPU",
                    "Tokenizer and model weights",
                    "Precision and recall",
                ],
                "correct": 0,
                "explanation": (
                    "A useful basic prompt communicates what to do and what data the "
                    "instruction applies to."
                ),
            },
            {
                "id": "M06.L01.Q06",
                "section_id": "specificity",
                "question": "Why is specificity valuable in prompts?",
                "options": [
                    "It reduces ambiguity about what output satisfies the task.",
                    "It guarantees the model knows every fact.",
                    "It removes the need for evaluation.",
                    "It makes every response deterministic.",
                ],
                "correct": 0,
                "explanation": (
                    "Clear task, scope, length, format, and other requirements reduce "
                    "the model's freedom to interpret the request incorrectly."
                ),
            },
            {
                "id": "M06.L01.Q07",
                "section_id": "complex-components",
                "question": "Which item is NOT one of the modular prompt components discussed in the chapter?",
                "options": [
                    "Audience",
                    "Tone",
                    "Context",
                    "Gradient optimizer",
                ],
                "correct": 3,
                "explanation": (
                    "The chapter discusses persona, instruction, context, format, "
                    "audience, tone, and data—not training optimizers."
                ),
            },
            {
                "id": "M06.L01.Q08",
                "section_id": "in-context-learning",
                "question": "What is few-shot prompting?",
                "options": [
                    "Updating the model weights using a few training examples",
                    "Providing multiple task demonstrations in the current context",
                    "Generating only a few tokens",
                    "Using a small language model",
                ],
                "correct": 1,
                "explanation": (
                    "Few-shot prompting supplies examples inside the prompt/context "
                    "without modifying model parameters."
                ),
            },
            {
                "id": "M06.L01.Q09",
                "section_id": "prompt-chaining",
                "question": "What is prompt chaining?",
                "options": [
                    "Using exactly the same prompt forever",
                    "Using the output of one prompt/model call as input to a later stage",
                    "Combining all model layers into one",
                    "Removing intermediate outputs",
                ],
                "correct": 1,
                "explanation": (
                    "Prompt chaining decomposes a task into sequential stages where "
                    "earlier outputs become later inputs."
                ),
            },
            {
                "id": "M06.L01.Q10",
                "section_id": "reasoning-intro",
                "question": (
                    "What caution should be applied to a model-generated step-by-step explanation?"
                ),
                "options": [
                    "It can be useful as a structured explanation but should not automatically be treated as a verified transcript of hidden internal reasoning.",
                    "It is always mathematically correct.",
                    "It always reveals the model's private internal state exactly.",
                    "It should never contain intermediate calculations.",
                ],
                "correct": 0,
                "explanation": (
                    "Visible reasoning-style text can support structured problem solving, "
                    "but it is generated output rather than guaranteed access to hidden internals."
                ),
            },
            {
                "id": "M06.L01.Q11",
                "section_id": "self-consistency",
                "question": "What is the basic idea behind self-consistency?",
                "options": [
                    "Use one deterministic output and never re-evaluate it.",
                    "Sample multiple candidate solutions and aggregate their final answers.",
                    "Remove all randomness from the model permanently.",
                    "Fine-tune the model on its own outputs.",
                ],
                "correct": 1,
                "explanation": (
                    "Self-consistency gains robustness by generating several diverse "
                    "paths and aggregating the resulting answers."
                ),
            },
            {
                "id": "M06.L01.Q12",
                "section_id": "tree-exploration",
                "question": "What distinguishes tree-style exploration from one linear reasoning path?",
                "options": [
                    "It explores and evaluates multiple intermediate branches before continuing.",
                    "It removes all intermediate steps.",
                    "It only works for translation.",
                    "It requires no additional generation.",
                ],
                "correct": 0,
                "explanation": (
                    "Tree-style methods consider alternative intermediate states, keep "
                    "promising ones, and prune weaker branches."
                ),
            },
            {
                "id": "M06.L01.Q13",
                "section_id": "verification",
                "question": "Which is a valid reason to verify model output in production?",
                "options": [
                    "To ensure required structure and allowed values are respected",
                    "To make the tokenizer unnecessary",
                    "To guarantee the model becomes larger",
                    "To remove all application code",
                ],
                "correct": 0,
                "explanation": (
                    "Production outputs often need schema, value, safety, and task "
                    "validation before an application can safely consume them."
                ),
            },
            {
                "id": "M06.L01.Q14",
                "section_id": "constrained-decoding",
                "question": "How is constrained decoding stronger than simply asking the model to follow a format?",
                "options": [
                    "It restricts which token sequences are permitted during generation.",
                    "It updates the model's pretraining dataset.",
                    "It increases the embedding dimension.",
                    "It removes the need to parse output.",
                ],
                "correct": 0,
                "explanation": (
                    "Grammar or schema constraints can make invalid token paths "
                    "unavailable instead of merely requesting compliance in natural language."
                ),
            },
            {
                "id": "M06.L01.Q15",
                "section_id": "llama-cpp-json",
                "question": "What does successful JSON parsing prove?",
                "options": [
                    "The content is factually correct.",
                    "The output satisfies every business rule.",
                    "The text is syntactically valid JSON.",
                    "The model used the correct hidden reasoning.",
                ],
                "correct": 2,
                "explanation": (
                    "Parsing verifies syntax. Semantic correctness and application "
                    "constraints require additional validation."
                ),
            },
            {
                "id": "M06.L01.Q16",
                "section_id": "verification-pipeline",
                "type": "open",
                "question": (
                    "Design a prompt and validation strategy for an application that "
                    "must classify a customer message as exactly one of `billing`, "
                    "`technical`, or `account`. Explain the prompt structure, generation "
                    "settings, whether you would use examples, how you would constrain "
                    "or parse the output, and what should happen if validation fails."
                ),
            },
        ],

        "passing_score": 70,
    },
}
