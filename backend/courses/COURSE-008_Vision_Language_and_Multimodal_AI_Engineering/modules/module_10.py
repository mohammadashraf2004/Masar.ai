"""M01.L10 — Any-to-Any Multimodal Models.

One chapter -> one complete learner-facing lesson + inline manual images +
inline exercises + lesson quiz.

Source: Chapter 10, "Any-to-Any Models".
Page numbers were not provided in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M01.L10"
MODULE_ORDER = 1
MODULE_TITLE = "Foundations of Vision and Language"
MODULE_DESCRIPTION = (
    "Understand unified multimodal systems that can consume and generate more "
    "than one modality. Compare unified-vocabulary autoregressive models, "
    "factorized generation heads, hybrid diffusion-based models, and modular "
    "late-conditioning systems; then learn the data-mixing, loss, and staged "
    "training strategies needed to make them work."
)
SOURCE_CHAPTER = 10
SOURCE_PAGES = "Chapter 10 — page numbers not provided"


TOPIC = {
    "title": "Any-to-Any Multimodal Models",
    "slug": "vision-language-m01-l10",
    "description": (
        "Learn how any-to-any systems unify text, images, audio, and video; how "
        "vector quantization, residual codebooks, VAEs, diffusion, trigger tokens, "
        "query interfaces, connectors, and modality-specific generators fit "
        "together; and how to train these systems without one modality or objective "
        "destroying the others."
    ),
    "order": 10,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 6.0,
    "skill_tags": [
        "any-to-any-models",
        "multimodal-generation",
        "vector-quantization",
        "codebooks",
        "vq-vae",
        "residual-vector-quantization",
        "factorized-heads",
        "thinker-talker",
        "continuous-latents",
        "vae",
        "diffusion",
        "classifier-free-guidance",
        "transfusion",
        "block-causal-attention",
        "late-conditioning",
        "conditioning-queries",
        "connectors",
        "diffusion-transformers",
        "multitask-training",
        "dataset-mixtures",
        "staged-training",
        "loss-balancing",
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
        "title": "Any-to-Any Multimodal Models",
        "content": r"""
# Any-to-Any Multimodal Models

> **Lesson:** M01.L10  
> **Module:** Foundations of Vision and Language  
> **Source alignment:** Chapter 10, *Any-to-Any Models*.  
> Page numbers were not included in the supplied source.  
> This lesson is an instructor-authored educational adaptation.

---

## From multimodal understanding to multimodal generation

Earlier VLMs answered questions such as:

```text
image + text
→ text
```

Video-language models extended this to:

```text
video + text
→ text
```

Audio-capable models can add:

```text
audio
→ text
```

But a genuinely broader assistant may need to:

```text
see
hear
read
reason
speak
generate images
generate video
```

inside one system.

The source calls the next frontier **any-to-any models**.

A truly any-to-any system, in the chapter's definition, must support at least:

```text
2 input modalities
and
2 output modalities
```

For example:

```text
INPUT:
text + image + audio

OUTPUT:
text + speech
```

or:

```text
INPUT:
text + image

OUTPUT:
text + generated image
```

The difficult question is not simply:

```text
"Can one model accept many modalities?"
```

It is:

> **How do we represent continuous signals such as images, audio, and video in
> a form that a transformer can both understand and generate?**

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Define an any-to-any model using the chapter's input/output criterion.
- Explain why text, images, audio, and video have different computational characteristics.
- Explain the three competing design pressures: efficiency vs. fidelity, simplicity vs. modularity, and shared representations vs. modality-specific detail.
- Compare unified-vocabulary, hybrid multiobjective, and modular/late-conditioning families.
- Explain vector quantization as a learned codebook lookup.
- Explain how a continuous image/audio representation becomes a discrete token.
- Calculate the vocabulary expansion caused by a visual codebook.
- Explain why large codebooks create a fidelity/computation trade-off.
- Describe a monolithic multimodal autoregressive architecture.
- Explain why Janus-Pro is presented as a transitional rather than perfectly pure monolithic design.
- Explain the difference between continuous perception encoders and discrete generation tokenizers.
- Describe factorized generation heads.
- Explain how trigger tokens hand control from the LLM to modality-specific generators.
- Explain why factorized heads keep the LLM vocabulary cleaner.
- Explain the source's "continuous in, discrete out" pattern.
- Explain residual vector quantization (RVQ).
- Compare sequential and parallel multicodebook generation.
- Describe the Thinker-Talker pattern.
- Explain why hybrid multiobjective models keep text discrete but represent generated media with continuous latents.
- Explain what a variational autoencoder contributes.
- Explain reconstruction and KL-regularization objectives conceptually.
- Distinguish a VAE from a VQ-VAE.
- Explain diffusion training and reverse denoising.
- Explain why diffusion can work for image, video, audio, and action latents.
- Explain Transfusion-style joint processing of discrete text and continuous image latents.
- Explain block-causal multimodal attention.
- Explain why image latent blocks need bidirectional attention while text remains causal.
- Explain classifier-free guidance (CFG).
- Interpret the CFG equation and guidance-scale trade-off.
- Explain late conditioning as "understand, connect, generate."
- Distinguish factorized heads from late conditioning.
- Explain hidden-state queries, CLIP-aligned latents, and hybrid continuous+discrete query interfaces.
- Compare linear, transformer, and dual-path connectors.
- Explain how image/video diffusion and speech/audio generators consume conditioning differently.
- Explain why Qwen-Image-Edit is presented as a modular dual-conditioning example rather than a canonical query-token late-conditioning system.
- Explain task/data imbalance in any-to-any training.
- Distinguish data-side and loss-side balancing.
- Explain connector-first training.
- Explain understanding-before-generation sequential training.
- Explain gradual unmasking for discrete multimodal models.
- Match architecture families to their appropriate training losses.
- Explain why incompatible objectives can cause gradient conflicts.
- Design a staged any-to-any training plan from pretrained components.

---

## 1. The any-to-any problem

The source begins with an important observation.

Humans communicate through many channels:

```text
text
images
speech
sound
video
```

A traditional software system might combine:

```text
vision model
+
audio recognizer
+
language model
+
speech synthesis
+
image generator
+
orchestration code
```

Any-to-any research asks whether more of this can be unified.

The objective is not necessarily to eliminate all specialization.

Instead, it explores different places to draw the boundary between:

```text
shared multimodal reasoning
and
modality-specific representation/generation
```

{{image:any-to-any-unified-model}}

---

## 2. Why modalities do not naturally behave the same

The source emphasizes that the modalities have different structures.

### Text

Naturally discrete:

```text
word/subword/token IDs
```

Autoregressive next-token prediction works naturally.

### Images

High-dimensional and continuous.

Pixels vary smoothly in:

- color;
- intensity;
- position.

The source argues that iterative methods such as diffusion often fit
high-fidelity visual generation better than a tiny discrete vocabulary.

### Audio

Temporal and continuous.

It can be represented as:

- discrete codec codes;
- continuous spectrogram/latent features.

### Video

Adds:

```text
space
+
time
+
huge token/compute requirements
```

This heterogeneity is why "one representation for everything" is difficult.

---

## 3. Three competing design pressures

The chapter describes three tensions.

### Efficiency versus fidelity

A single token-based backbone is efficient and lets us reuse:

- tokenization;
- autoregressive generation;
- cross-entropy training.

But continuous media can lose detail when forced into a small discrete
vocabulary.

### Simplicity versus modularity

One giant model is conceptually elegant.

But tightly coupling:

- language;
- perception;
- generation;

makes components harder to improve independently.

### Shared representation versus modality-specific detail

A shared representation makes cross-modal reasoning easy.

But each modality benefits from its own structure:

```text
images → spatial
audio → temporal/acoustic
video → spatial + temporal
```

Different compromises create the chapter's three architecture families.

---

## 4. The three architectural families

The source introduces:

```text
1. Unified vocabulary models
2. Hybrid multiobjective models
3. Modular / late-conditioning models
```

### Unified vocabulary family

Idea:

```text
turn every modality into discrete codes
→ predict tokens autoregressively
```

Strength:

- conceptually simple;
- low-latency generation relative to iterative diffusion;
- tight autoregressive coordination.

Weakness:

- quantization can reduce media fidelity.

### Hybrid multiobjective family

Idea:

```text
text → discrete autoregressive tokens
media → continuous latents + diffusion/flow
shared transformer
```

Strength:

- strong visual/media fidelity;
- tight cross-modal integration.

Weakness:

- iterative generation;
- multiple objectives;
- more complex training.

### Modular / late-conditioning family

Idea:

```text
MLLM understands what should happen
→ connector
→ specialist generator renders it
```

Strength:

- modular;
- components can be swapped/upgraded.

Weakness:

- the conditioning interface can become a bottleneck.

{{image:any-to-any-three-families}}

{{exercise:M01.L10.EX01}}

---

## 5. Unified vocabulary models

Transformers naturally consume tokens.

So the unified-vocabulary idea is:

> Make every modality speak in tokens.

For text:

```text
"cat"
→ text token ID
```

For an image:

```text
image patch
→ continuous feature
→ nearest codebook entry
→ visual token ID
```

For audio:

```text
audio chunk
→ code
→ audio token ID
```

Then the transformer can process:

```text
[text][text][visual][visual][audio][text]...
```

using one autoregressive machinery.

---

## 6. Vector quantization: turning continuous signals into tokens

The chapter uses a color analogy.

Instead of representing every possible RGB value:

```text
(127, 45, 203)
```

imagine forcing colors into categories:

```text
red
green
blue
...
```

A learned **codebook** does this in embedding space.

Pipeline:

```text
continuous vector
      ↓
compare to codebook entries
      ↓
nearest reference vector
      ↓
codebook index
      ↓
discrete token
```

The codebook is learned during training.

---

## 7. The codebook as a modality vocabulary

A codebook is a fixed-size table of vectors.

Suppose:

```text
image codebook size = 8,192
```

Then each visual code can be represented by an ID such as:

```text
<vis0>
<vis1>
...
<vis8191>
```

The source gives a vocabulary-expansion example:

```text
text vocabulary = 152,064
image codebook   =   8,192
--------------------------------
unified total    = 160,256
```

Now the autoregressive model learns when to predict:

```text
a text token
or
a visual token
```

from context.

---

## 8. The discrete codebook bottleneck

A small codebook is efficient.

But it cannot express unlimited visual detail.

Larger codebook:

```text
more possible visual states
→ potentially higher fidelity
```

but also:

```text
larger prediction space
more complexity
harder optimization
```

This creates the first recurring any-to-any trade-off:

```text
fidelity
vs
discrete vocabulary complexity
```

The source states that quantized visual encoders often trail continuous
representations in both understanding and generation quality.

---

## 9. Monolithic architecture

In the pure monolithic idea:

```text
one transformer
+
one expanded discrete vocabulary
```

handles:

- text tokens;
- image tokens;
- audio tokens;
- other discrete modalities.

The same next-token machinery predicts all of them.

Conceptually:

```text
prompt:
"Draw a lake at sunset"

transformer:
<vis43> <vis1001> <vis805> ...

decoder:
visual tokens → pixels
```

### Why it is elegant

One sequence.

One autoregressive logic.

Potentially one main loss:

```text
cross-entropy
```

### Why it is difficult

The LLM must simultaneously model:

```text
high-level meaning
and
low-level reconstruction details
```

inside the same discrete prediction space.

---

## 10. Janus-Pro as a transitional design

The source deliberately avoids presenting Janus-Pro as perfectly pure
monolithic architecture.

It fits this section because it uses discrete visual tokens for generation.

But it **decouples visual encoders by role**.

### Perception / understanding side

A high-capacity continuous visual encoder processes images for semantic
understanding.

### Generation side

A VQ-VAE-style tokenizer converts image content into discrete generation codes.

So the system is asymmetric:

```text
UNDERSTANDING:
continuous image representation

GENERATION:
discrete visual codes
```

This reduces the "one encoder must do everything" tension.

{{image:janus-pro-architecture}}

---

## 11. Explicit generation modes

The source shows a model interface where you explicitly choose:

```text
generation_mode="text"
```

or:

```text
generation_mode="image"
```

This supports:

- text QA;
- visual QA;
- text-to-image generation.

But the source notes an important limitation:

> The model does not naturally interleave text and image generation inside one
> continuous stream when generation requires an explicit mode switch.

That motivates a stronger separation of responsibilities.

---

## 12. Factorized generation heads

Factorized heads remove nontext token prediction from the main LLM head.

Instead:

```text
LLM
→ predicts ordinary text tokens
→ predicts special trigger token when another modality is needed
→ specialized head takes over
```

Example:

```text
LLM emits:
<image_start>

image head:
generates image codes

decoder:
codes → pixels
```

Similarly:

```text
<audio_start>
→ audio head
→ codec codes
→ waveform
```

---

## 13. Semantic handoff

The LLM does not need to generate pixels or waveforms.

It provides:

```text
hidden states
=
semantic intent
```

Then a modality-specific head converts that intent into:

- image codes;
- speech codes;
- audio codes.

Simplified source-aligned pseudocode:

```python
def generate_with_factorized_head(
    prompt_tokens,
    llm,
    image_head,
    audio_head,
):
    hidden_states = []

    for token in llm.generate(
        prompt_tokens
    ):
        hidden_states.append(
            llm.last_hidden_state
        )

        if token == "<image_start>":
            h = torch.stack(
                hidden_states
            )

            image_codes = (
                image_head.generate(
                    conditioning=h
                )
            )

            yield image_decoder(
                image_codes
            )

        elif token == "<audio_start>":
            h = torch.stack(
                hidden_states
            )

            audio_codes = (
                audio_head.generate(
                    conditioning=h
                )
            )

            yield audio_decoder(
                audio_codes
            )

        else:
            yield token
```

The exact code is pseudocode.

The architecture idea is the important part.

---

## 14. Why factorize output heads?

The source gives several benefits.

### Separation of concerns

```text
LLM:
what should be generated?

specialist head:
how should it be rendered?
```

### Cleaner LLM vocabulary

The text vocabulary does not need thousands of image/audio tokens.

### Better modality-specific representation

Specialized heads can use richer codec structures.

### Natural interleaving

Because the LLM controls trigger tokens, a system can conceptually produce:

```text
text
→ image
→ more text
→ speech
```

without requiring a global generation-mode switch.

---

## 15. The asymmetric pattern: continuous in, discrete out

The source describes a dominant factorized pattern.

### Input side

Vision/audio/video inputs use continuous encoders:

```text
ViT
SigLIP-style visual encoder
streaming audio encoder
```

These produce dense embeddings.

### Reasoning

The LLM attends to those embeddings.

### Output side

The LLM emits a trigger.

A specialized head predicts discrete codec/codebook tokens.

A decoder renders those codes.

So:

```text
continuous perception
→ language reasoning
→ discrete specialist generation
```

This keeps the LLM's core token vocabulary text-oriented while preserving rich
perception inputs.

---

## 16. Residual vector quantization (RVQ)

A single codebook faces a fidelity ceiling.

The source presents RVQ as a way to combine several smaller codebooks.

Single codebook:

```text
choose 1 code
from 8,192 possibilities
```

RVQ example:

```text
8 codebooks
×
1,024 choices each
```

The combination count is conceptually:

```text
1,024^8
```

This is not the same as expanding the LLM vocabulary to that huge size.

Each codebook is handled as a separate prediction level inside the specialist
head.

### Analogy

Instead of selecting one complete description of a person, choose separate
attributes:

```text
height
hair
eyes
clothing
...
```

The combination gives much richer expressivity.

[[IMAGE_NEEDED: Single codebook versus RVQ |
Show one choice from one large visual codebook versus multiple sequential small
codebooks that refine the representation |
Learner should see how combinatorial expressivity improves without exploding
the LLM vocabulary]]

{{exercise:M01.L10.EX02}}

---

## 17. Sequential and parallel multicodebook generation

The source describes two strategies.

### Sequential: coarse to fine

Predict:

```text
codebook 1
then
codebook 2 conditioned on 1
then
codebook 3 conditioned on previous codes
...
```

Useful when progressive refinement matters.

The source connects this pattern to audio codec generation.

### Parallel

Predict all codebook indices together from the conditioning state.

This can fit image generation where relationships across spatial content matter
more than strict coarse-to-fine codec ordering.

Trade-off:

```text
sequential:
more dependency modeling
slower

parallel:
faster
less sequential refinement
```

---

## 18. Thinker-Talker architecture

The source uses Qwen2.5-Omni as a clear factorized example.

Conceptually:

```text
vision encoder ─┐
audio encoder ──┼→ THINKER / LLM
text input ─────┘
                     ↓
                semantic reasoning
                     ↓
                   TALKER
                     ↓
              speech codec tokens
                     ↓
              streaming decoder
                     ↓
                  waveform
```

The Thinker handles understanding and reasoning.

The Talker handles speech generation.

This is an explicit realization of:

```text
what
versus
how
```

---

## 19. Multimodal input and multimodal output

The source shows a workflow where the model receives:

```text
video
+
audio extracted from video
+
text instruction
```

and generates:

```text
text
+
speech waveform
```

A source-aligned pattern:

```python
inputs = processor.apply_chat_template(
    conversation,
    load_audio_from_video=True,
    use_audio_in_video=True,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
    fps=0.5,
    padding=True,
).to(model.device)

text_ids, audio = model.generate(
    **inputs,
    use_audio_in_video=True,
    thinker_do_sample=False,
    talker_do_sample=True,
)
```

This demonstrates why the chapter calls these systems **any-to-any** rather than
only VLMs.

---

## 20. Hybrid multiobjective models

The hybrid family takes a different position.

Instead of forcing generated media into discrete code tokens:

```text
text stays discrete
media stays continuous
```

The shared transformer must work with both.

The source describes:

```text
text:
autoregressive token prediction

image/audio/video:
continuous latent denoising
```

This yields stronger fidelity but requires iterative generation.

---

## 21. Factorized heads versus hybrid multiobjective

This distinction is easy to confuse.

### Factorized heads

The LLM remains mainly discrete.

When nontext output is needed:

```text
LLM trigger
→ specialist head
→ media representation
```

The main transformer is not itself repeatedly denoising continuous image
latents.

### Hybrid multiobjective

The main transformer directly processes:

```text
text tokens
+
continuous noisy media latents
```

during the diffusion process.

So the main question is:

> **Where does continuous-generation computation happen?**

Factorized:

```text
outside/delegated
```

Hybrid:

```text
inside the shared transformer
```

---

## 22. Variational autoencoders as continuous compressors

Diffusion over raw pixels would be expensive.

A VAE compresses high-dimensional media into a smaller continuous latent.

Pipeline:

```text
input media
→ encoder
→ compact latent z
→ decoder
→ reconstruction
```

{{image:multimodal-vae}}

Examples from the source illustrate compression of:

- images;
- video;
- audio.

The exact compression factor depends on the model.

{{image:multimodal-vae-comparison}}

The role is consistent:

```text
run expensive generation in latent space
instead of raw media space
```

---

## 23. VAE training intuition

The chapter states that VAE training balances:

```text
reconstruction
+
regularization
```

Conceptually:

```text
L_VAE
=
L_reconstruction
+
β × L_KL
```

### Reconstruction term

Encourages the decoder to recreate the input accurately.

### KL term

Encourages the latent distribution to stay near a structured prior.

### β

Controls the trade-off.

Higher regularization:

```text
smoother latent space
```

but can reduce reconstruction sharpness.

### Source formatting note

The uploaded reconstruction equation is truncated after:

```text
||x –
```

The surrounding prose clearly states that this term measures squared
reconstruction error between the original input and its reconstruction.

The lesson keeps that supported interpretation instead of inventing a missing
symbol from the pasted equation.

---

## 24. VAE versus VQ-VAE

A standard VAE has:

```text
continuous latent
```

A VQ-VAE replaces that with:

```text
discrete codebook indices
```

The source also notes that VQ-VAE does not use the same KL regularization term.

Instead it uses a codebook/commitment-style objective that keeps encoder outputs
near codebook entries.

So:

```text
VAE
→ continuous diffusion-friendly latent

VQ-VAE
→ discrete token/codebook-friendly representation
```

This connects directly back to unified-vocabulary models.

---

## 25. Why diffusion solves continuous generation

An LLM predicts from a finite vocabulary.

A continuous image latent can take effectively unlimited values.

Diffusion changes the prediction problem.

Instead of predicting the final latent directly:

```text
start from noise
→ repeatedly predict how to denoise
→ gradually recover structure
```

Two directions matter.

### Forward process during training

```text
clean latent
→ add Gaussian noise
→ more noise
→ nearly pure noise
```

### Reverse process during generation

```text
random noise
→ predict/remove noise
→ cleaner latent
→ final media latent
```

The source states that the denoising model can be trained with mean squared error
between:

```text
actual added noise
and
predicted noise
```

[[IMAGE_NEEDED: Diffusion forward and reverse process |
Show a clean media latent progressively becoming noise during training and the
learned reverse process turning noise back into structured content |
Learner should understand iterative refinement instead of one-shot token
prediction]]

---

## 26. Diffusion is not only for images

The source explicitly generalizes diffusion to:

```text
image latents
video latents
audio spectrogram/latent spaces
robotic action trajectories
```

The denoising principle stays the same.

What changes is:

```text
shape
structure
decoder
```

of the target latent.

This is one reason diffusion is attractive for any-to-any systems.

---

## 27. One transformer, two representation languages

The source presents Transfusion-style architecture as a breakthrough in jointly
handling:

```text
discrete text
+
continuous image latents
```

The shared model uses different losses depending on token/latent type.

Text positions:

```text
cross-entropy
```

Image-latent positions:

```text
denoising MSE
```

Shared transformer parameters receive gradients from both modalities.

The model therefore becomes "bilingual" in:

```text
discrete autoregression
and
continuous denoising
```

---

## 28. Block-causal multimodal attention

Text generation needs causal masking.

A text token should not see future text tokens.

Image denoising needs something different.

All latent patches inside the image block should be able to interact
bidirectionally.

So the source describes a block-causal structure.

Conceptually:

```text
[text before image]
     causal

<BOI>
[image latent patches]
     bidirectional within image
<EOI>

[text after image]
     causal, but can attend to complete earlier image
```

Boundary rule:

```text
text before image
cannot see future image

text after image
can see completed image block
```

[[IMAGE_NEEDED: Block-causal multimodal attention |
Show text tokens with triangular causal attention, an image latent block with
full bidirectional internal attention, and later text attending back to the
entire image block |
Learner should understand why different modality blocks require different masks]]

---

## 29. Hybrid text-to-image generation flow

The source describes this sequence:

```text
prompt
→ text embeddings
→ random Gaussian latent
→ iterative denoising
→ clean continuous latent
→ VAE decoder
→ pixels
```

Unlike pure autoregressive visual token generation:

```text
one token after another
```

the hybrid model repeatedly revisits the noisy latent.

The source gives a typical example of:

```text
20–50 denoising steps
```

for such architectures.

This is a source-reported range, not a universal requirement.

---

## 30. Classifier-free guidance

The source gives:

```text
ε_hat
=
ε_uncond
+
s × (ε_cond - ε_uncond)
```

where:

```text
ε_cond   = prediction with prompt
ε_uncond = prediction without prompt
s        = guidance scale
```

Interpretation:

```text
ε_cond - ε_uncond
```

is the direction added by conditioning.

If:

```text
s = 1
```

you get ordinary conditional prediction.

If:

```text
s > 1
```

the prompt's influence is amplified.

Trade-off:

```text
higher guidance
→ stronger prompt adherence
but
less diversity / possible artifacts
```

The source gives typical guidance ranges as examples.

Treat them as model-dependent settings.

{{exercise:M01.L10.EX03}}

---

## 31. How one model learns conditional and unconditional predictions

Classifier-free guidance does not require a separate classifier.

During training, conditioning is sometimes dropped:

```text
prompt
→ replaced with empty/no condition
```

This teaches the same denoiser to handle:

```text
conditional input
and
unconditional input
```

At inference, run both forms and combine them using the CFG formula.

---

## 32. Simplified diffusion generation

A source-aligned educational version:

```python
def generate_with_diffusion(
    prompt,
    steps=30,
    latent_shape=(...),
    cfg_scale=7.5,
):
    text_embeddings = encode_prompt(
        prompt
    )

    null_embeddings = encode_prompt(
        ""
    )

    latent = torch.randn(
        latent_shape
    )

    timesteps = torch.linspace(
        1000,
        0,
        steps,
    )

    for t in timesteps:
        noise_cond = denoiser(
            latent,
            t,
            context=text_embeddings,
        )

        noise_uncond = denoiser(
            latent,
            t,
            context=null_embeddings,
        )

        noise_pred = (
            noise_uncond
            + cfg_scale
            * (
                noise_cond
                - noise_uncond
            )
        )

        alpha_t = get_alpha_schedule(
            t
        )

        latent = (
            latent
            - (1 - alpha_t)
            * noise_pred
        ) / sqrt(alpha_t)

    return vae_decoder(
        latent
    )
```

The source explicitly labels this as simplified pseudocode.

Its purpose is conceptual:

```text
encode condition
initialize noise
iterate denoising
decode
```

---

## 33. Late conditioning: understand, connect, generate

The third family asks:

> Why tightly integrate everything if strong pretrained components already
> exist?

Architecture:

```text
MLLM
→ semantic query representation
→ connector
→ specialized generator
```

Think:

```text
MLLM:
what should be produced?

generator:
how should it look/sound?
```

Only the bridge may need substantial new training.

This makes late conditioning attractive under limited training budgets.

---

## 34. Factorized heads versus late conditioning

The boundary can be blurry.

The source distinguishes them by architecture and design philosophy.

### Factorized head

The generator/head is tightly coupled to a specific LLM.

It reads the LLM's hidden states directly and often participates in the same
forward/generation system.

### Late conditioning

The MLLM and generator are intentionally independent.

The connector translates between them.

This supports:

```text
swap image generator
without retraining MLLM

swap TTS engine
without changing reasoning model
```

So the question is not only:

```text
"What is frozen?"
```

It is:

> **Was the generator designed as a replaceable external specialist or as a
> native output component of this LLM?**

---

## 35. Query-based late-conditioning pipeline

The source gives four parts.

### 1. Input sequence

```text
text prompt tokens
+
learnable query tokens
```

### 2. MLLM

Processes the sequence and produces:

- text output;
- query states.

Conceptually:

```text
Q ∈ R^(S × D)
```

where `S` is the number of query vectors.

### 3. Connector

Maps query states into the format expected by the generator.

Could be:

- MLP;
- projection;
- transformer bridge;
- cross-attention adapter.

### 4. Generator

Examples:

- image diffusion transformer;
- video diffusion model;
- TTS engine.

{{image:late-conditioning-architecture}}

---

## 36. Trigger tokens in late conditioning

The system may use tokens such as:

```text
<image>
<speech>
<video>
```

to signal generation intent.

Then the orchestration logic:

```text
detect trigger
→ extract corresponding query states
→ run connector
→ invoke matching generator
→ return media
```

This resembles factorized heads at a surface level.

The architectural distinction is the independence/swappability of the external
generator.

---

## 37. Conditioning interface options

The source presents three query-space designs.

### Hidden-state queries

Use the MLLM's internal representations directly.

Strength:

- flexible;
- compatible with frozen MLLMs.

Cost:

- connector may need to learn a difficult representation translation.

### CLIP-aligned latents

Both sides use a CLIP-like representation space.

Strength:

- easier alignment;
- faster convergence.

Limitation:

- bounded by what that representation captures.

### Hybrid continuous + discrete

Use:

```text
continuous query vectors
+
discrete layout/visual codes
```

Strengths from the source include:

- stronger prompt adherence;
- sharper text/layout control.

Cost:

- more complex training/loss design.

---

## 38. Connectors: translating between representation spaces

The source lists three broad connector types.

### Linear / small MLP

Roughly:

```text
a few million parameters
```

Best when spaces are already fairly aligned.

### Transformer bridge

Much larger.

Can perform richer semantic translation between mismatched spaces.

### Dual-path connector

Combines:

```text
continuous feature path
+
discrete token path
```

Useful when continuous conditioning alone lacks precision.

The source provides approximate parameter ranges as examples.

Treat those ranges as architecture examples, not hard rules.

---

## 39. How different generators use conditioning

Different output modalities consume semantic instructions differently.

### Image diffusion

Query vectors become attention context.

Each denoising block repeatedly attends to them.

### Video diffusion

Same general principle, but conditioning must guide:

```text
space
+
time
```

### Speech / TTS

The generator can consume:

- text;
- speaker identity;
- prosody controls;
- emotion/control tokens.

### General audio

Codec/vocoder systems consume appropriate acoustic representations or codes.

The lesson:

> "Conditioning" is not one universal tensor contract. The interface depends on
> the target generator.

---

## 40. Qwen-Image-Edit as a modular dual-conditioning example

The source is very careful here.

It says this system is **not** a pure query-token late-conditioning model.

Instead, it illustrates the same separation principle.

Two conditioning streams:

### Semantic stream

A frozen multimodal model produces hidden states representing:

```text
what the user wants changed
```

### Reconstructive/spatial stream

A VAE encodes the source image into latents representing:

```text
what should be preserved
```

Both condition an MMDiT diffusion renderer.

So:

```text
semantic control
+
appearance-preserving control
→
diffusion editing
```

{{image:qwen-image-edit-architecture}}

---

## 41. Making the conditioning boundary explicit

The source highlights a useful implementation pattern.

Instead of hiding everything inside one pipeline call:

```python
out = pipe(
    image=img,
    prompt=instruction,
)
```

first obtain conditioning embeddings:

```python
prompt_embeds, prompt_embeds_mask = (
    pipe.encode_prompt(
        prompt=instruction,
        image=img,
    )
)
```

Then feed those embeddings into the renderer.

Conceptually:

```text
instruction + source image
→ semantic representation

semantic representation
→ diffusion renderer
```

This makes the architecture boundary visible in code.

---

## 42. Modularity is powerful—but interfaces can bottleneck

Late conditioning makes components replaceable.

Benefits:

```text
upgrade image generator
upgrade speech engine
preserve MLLM
reuse connector strategy
```

But a narrow interface can lose fine-grained information.

So late conditioning trades:

```text
maximum integration
for
maximum flexibility
```

The source contrasts this with hybrid models where text and continuous media
share the same attention layers repeatedly.

---

## 43. Why any-to-any training is hard

Now multiple tasks compete inside one training system.

Examples:

### Perception → text

- captioning;
- VQA;
- transcription.

### Text → media

- text-to-image;
- text-to-video;
- text-to-speech.

### Editing

- image editing;
- style transfer;
- inpainting.

These tasks have different:

- token counts;
- losses;
- data scale;
- difficulty;
- target modalities.

If one dominates the mixture, the model can over-specialize.

---

## 44. Token count itself can create hidden imbalance

Suppose:

```text
caption sample:
256 image tokens + 20 output text tokens

conversation sample:
200+ text tokens

video sample:
potentially very long multimodal sequence
```

A dataset percentage does not directly equal a gradient contribution.

Video can dominate batches simply through sequence length.

Text can dominate if almost all samples are text-only.

Any-to-any training therefore needs deliberate mixture design.

---

## 45. Data-side balancing

Control what the model sees.

The source suggests strategies such as:

- oversample underrepresented tasks;
- cap very long sequences;
- ensure batches reflect target capabilities;
- keep general-purpose data during specialization.

The objective is to avoid:

```text
one modality swallowing the training signal
```

and to reduce catastrophic forgetting.

---

## 46. Loss-side balancing

Even with balanced examples, losses can have different magnitudes.

You can weight:

```text
L_total
=
w_text × L_text
+
w_image × L_image
+
w_audio × L_audio
+ ...
```

The source suggests starting simply, then adjusting based on validation.

It also mentions automated techniques such as:

- gradient-magnitude balancing;
- uncertainty-based task weighting.

The key idea:

```text
data mixture controls examples
loss weights control gradient influence
```

{{exercise:M01.L10.EX04}}

---

## 47. Staged training: divide and conquer

The source argues that training everything together from scratch often causes
interference.

Three patterns are highlighted:

```text
1. connector-first
2. understanding before generation
3. gradual unmasking for discrete models
```

---

## 48. Connector-first alignment

Freeze strong pretrained backbones:

```text
LLM
vision encoder
audio encoder
```

Train only the adapter/connector.

Example:

```text
vision encoder
→ small MLP
→ LLM embedding space
```

Why?

The new modality learns how to communicate with the LLM before broad
multimodal gradients are allowed to alter stable pretrained capabilities.

---

## 49. Understanding before generation

The source presents sequential training as a strong strategy.

### Phase 1

Train understanding tasks:

- VQA;
- captioning;
- perception.

### Phase 2

Freeze the MLLM.

Train a generator conditioned on its outputs.

Reason:

```text
text cross-entropy
and
diffusion MSE
```

can pull shared parameters in conflicting directions.

Separating stages reduces negative transfer.

The source cites BLIP3-o as an example of this philosophy.

{{image:joint-vs-sequential-multimodal-training}}

---

## 50. Gradual unmasking for discrete multimodal models

Early visual/audio code predictions may be effectively noisy.

The source suggests:

```text
start with nontext token loss masked/downweighted
→ gradually increase its weight
```

This lets the language structure stabilize before the model receives the full
difficulty of large multimodal codebooks.

This is analogous to curriculum learning:

```text
easy/stable objective first
→ harder coupled objective later
```

---

## 51. Staging in a Thinker-Talker system

The source describes an example where the system begins from strong pretrained
components.

The Talker/speech side goes through stages such as:

```text
speech continuation
→ stability tuning
→ multispeaker/style tuning
```

The Thinker may be frozen during specialization.

This reflects the broader rule:

> Add generation capabilities without unnecessarily degrading an already-good
> reasoning model.

---

## 52. Architecture-specific losses

Different families require different supervision.

### Unified discrete autoregressive

Main idea:

```text
cross-entropy over discrete tokens
```

Elegant because one categorical prediction objective can cover modalities.

But codebook design creates fidelity/optimization pressure.

### Hybrid multiobjective

Two objective types:

```text
text:
cross-entropy

continuous media:
diffusion/noise MSE
```

The source warns that they should not be forced through one shared output head.

Use modality-appropriate outputs/heads so incompatible targets do not collide at
the final prediction layer.

### Late conditioning

Parameter sets are more separated.

Typical pattern:

```text
MLLM understanding loss
separate from
generator diffusion/flow loss
```

This isolation makes gradient conflicts easier to manage.

---

## 53. A source-table nuance about factorized heads

One source comparison table describes the factorized-head side using language
like:

```text
"single objective: cross-entropy over unified vocabulary"
```

Elsewhere, the same chapter carefully explains that factorized heads keep the
LLM vocabulary text-based and delegate media-code prediction to specialized
heads.

The more consistent architectural takeaway from the chapter is:

```text
generation remains discrete/autoregressive on the factorized side
but
the modality codes are handled by specialized heads rather than being part of
one monolithic LLM vocabulary
```

The lesson preserves both source ideas and avoids collapsing factorized heads
back into the monolithic vocabulary design.

---

## 54. Start from strong pretrained components

The chapter's training cheat sheet strongly recommends:

```text
do not train everything from scratch
```

Start from:

- capable LLM;
- pretrained vision encoder;
- pretrained audio encoder;
- capable diffusion/TTS generator.

Then train:

- connectors;
- adapters;
- modality-specific heads;
- staged specializations.

This reduces cost and protects existing capabilities.

---

## 55. Monitor several capabilities simultaneously

Any-to-any training can improve one skill while silently damaging another.

The source recommends monitoring multiple metric families.

Examples:

### Understanding

```text
VQA accuracy
```

### Generation

```text
FID
CLIP-style alignment score
```

### Language preservation

```text
language benchmark / perplexity
```

If:

```text
image quality ↑
language ability ↓
```

then the problem may be:

- mixture;
- loss weighting;
- learning rate;
- staging.

---

## 56. Task-aware learning rates

Stable pretrained components should generally change less aggressively than
newly initialized components.

The source suggests the pattern:

```text
lower LR:
pretrained backbone

higher LR:
new connector / adapter
```

This aligns optimization speed with parameter maturity.

The exact factor should be validated for the actual model.

---

## 57. Choosing an any-to-any architecture

### Choose unified discrete/autoregressive when

- latency matters strongly;
- output can tolerate quantization limits;
- one autoregressive generation framework is attractive;
- generated media may serve as intermediate reasoning or lower-fidelity output.

### Choose factorized heads when

- you want autoregressive orchestration;
- you want a clean text vocabulary;
- you want modality-specific code generators;
- natural interleaving matters.

### Choose hybrid multiobjective when

- high media fidelity matters most;
- slower iterative generation is acceptable;
- you can manage multiple objectives and more complex training.

### Choose late conditioning when

- modularity matters;
- training budget is limited;
- strong pretrained MLLM and generator already exist;
- you want to swap generation components independently.

No family wins every trade-off.

---

## 58. Evaluate any-to-any systems as a portfolio of capabilities

Do not judge one scalar metric.

Evaluate:

### Understanding

- text quality;
- visual QA;
- audio understanding;
- video understanding.

### Generation

- image quality;
- speech quality;
- video quality;
- prompt adherence.

### Alignment

Does generated media match the semantic intent?

### Interleaving

Can the system transition correctly between text and media outputs?

### Preservation

Did adding one modality damage another?

### Efficiency

Measure:

- latency;
- memory;
- diffusion steps;
- token counts;
- generation throughput.

### Modularity

For late-conditioning designs:

- can generator replacement work without retraining the MLLM?
- how much connector retraining is required?

---

## 59. Source-specific implementation and notation notes

The chapter intentionally covers bleeding-edge systems and warns that library
environments may conflict.

### Separate notebooks

The source splits examples into separate environments because model-family
dependencies can conflict.

That is an engineering lesson itself:

```text
research multimodal stacks are not yet fully standardized
```

### Janus-Pro classification

The source places Janus-Pro under monolithic architecture for its discrete
generation vocabulary, but explicitly calls it transitional because perception
and generation use different encoders.

### Qwen-Image-Edit classification

The source explicitly says it is not a canonical query-token late-conditioning
model.

It is used because it demonstrates the same semantic-understanding-versus-
rendering separation.

### VAE equation formatting

The pasted reconstruction formula is incomplete.

The surrounding prose supports the interpretation as reconstruction error, but
the lesson does not pretend the missing symbol was present in the source.

### Diffusion code

The diffusion implementation is simplified pseudocode.

It teaches:

```text
condition
noise
timesteps
denoise
decode
```

not a production scheduler implementation.

### Family/loss terminology

Some source tables use broad labels that can blur the boundary between
monolithic discrete-token and factorized-head architectures.

The lesson preserves the chapter's more detailed architectural distinctions.

---

## 60. The complete any-to-any mental model

The entire chapter can be summarized as one question:

```text
HOW DO WE BRIDGE
DISCRETE LANGUAGE
AND
CONTINUOUS WORLD SIGNALS?
```

Three answers:

```text
A. DISCRETIZE EVERYTHING

image/audio/video
→ codebooks
→ tokens
→ autoregressive model

simple + fast
but fidelity bottleneck
```

```text
B. LET ONE TRANSFORMER SPEAK TWO REPRESENTATION TYPES

text
→ discrete tokens + cross-entropy

media
→ continuous latents + diffusion MSE

tightly integrated + high fidelity
but slower + harder to train
```

```text
C. KEEP REASONING AND RENDERING MODULAR

MLLM
→ semantic queries
→ connector
→ specialist generator

flexible + component-swappable
but interface can bottleneck alignment
```

And inside the discrete/autoregressive family:

```text
MONOLITHIC
LLM predicts media tokens itself

FACTORIZED HEADS
LLM decides what/when
specialist head generates modality codes
```

Training principle:

```text
start from pretrained components
→ align connectors
→ stabilize understanding
→ add generation
→ balance data
→ balance losses
→ monitor every modality
```

The central idea is:

> **Any-to-any architecture is fundamentally a decision about where to place the
> boundary between shared semantic reasoning and modality-specific
> representation/rendering.**

{{exercise:M01.L10.EX05}}

{{exercise:M01.L10.EX06}}

---

## Important misconceptions

### Misconception 1: "Any multimodal model is any-to-any."

Not under the source's definition.

The model should handle at least two input modalities and two output modalities.

### Misconception 2: "Text, image, audio, and video can all be represented optimally in the same way."

Their computational and structural properties differ.

### Misconception 3: "Unified vocabulary means continuous media stays continuous."

No.

The defining idea is discretizing media into code tokens.

### Misconception 4: "A larger codebook solves visual fidelity for free."

Larger prediction spaces increase training and computational burden.

### Misconception 5: "Janus-Pro is a perfectly pure monolithic model."

The source explicitly calls it transitional because it decouples perception and
generation encoders.

### Misconception 6: "Factorized heads put image/audio tokens in the LLM vocabulary."

The source's factorized design keeps the LLM vocabulary cleaner and delegates
modality-code generation to specialized heads.

### Misconception 7: "RVQ means one enormous vocabulary."

No.

Multiple smaller codebooks create combinatorial representation capacity.

### Misconception 8: "Hybrid multiobjective and factorized heads are the same because both can use specialized generation."

No.

The hybrid family's main transformer itself processes continuous noisy latents
during iterative denoising.

### Misconception 9: "A VAE and VQ-VAE have the same latent type."

VAE latents are continuous.

VQ-VAE uses discrete codebook entries.

### Misconception 10: "Diffusion predicts the final image in one step."

It iteratively refines noise into a clean latent.

### Misconception 11: "Text and image latent blocks should use the same attention mask."

The source's hybrid design uses causal text attention and bidirectional
within-image attention.

### Misconception 12: "Higher CFG scale is always better."

Stronger guidance can reduce diversity and create artifacts.

### Misconception 13: "Factorized heads and late conditioning differ only because one is frozen."

The deeper distinction is architectural coupling versus independent/swappable
generators.

### Misconception 14: "Late conditioning has no downside."

Its connector/query interface can limit fine-grained alignment.

### Misconception 15: "One dataset ratio is enough to balance any-to-any training."

Sequence length and loss magnitude can create hidden imbalance even when sample
counts look balanced.

### Misconception 16: "Train everything jointly from scratch for maximum integration."

The source repeatedly recommends staging to reduce interference.

---

## Key terminology

| Term | Meaning |
|---|---|
| Any-to-any model | Model handling multiple input modalities and multiple output modalities |
| Unified vocabulary | One discrete token space expanded to include nontext modality codes |
| Vector quantization | Mapping a continuous vector to its nearest learned codebook vector |
| Codebook | Learned table of reference vectors whose indices act as discrete codes |
| Monolithic model | Main autoregressive model directly predicts modality tokens |
| Factorized head | Specialized output head triggered by the LLM to generate nontext codes |
| Trigger token | Special token such as `<image>` or `<audio>` signaling a modality handoff |
| Continuous in, discrete out | Continuous perception embeddings with discrete specialist generation codes |
| RVQ | Residual vector quantization using multiple codebooks |
| Thinker-Talker | Split between semantic reasoning and speech-code generation |
| Hybrid multiobjective | Shared transformer handles discrete text and continuous media latents with different objectives |
| VAE | Autoencoder with continuous structured latent space |
| VQ-VAE | Autoencoder whose latent is quantized through a codebook |
| Diffusion | Iterative denoising process used to generate continuous latent media |
| Denoising MSE | Error between true and predicted noise |
| Block-causal attention | Mask combining causal text with bidirectional media blocks |
| CFG | Classifier-free guidance combining conditional and unconditional predictions |
| Guidance scale | Strength of prompt influence in CFG |
| Late conditioning | MLLM semantics passed through a connector to independent generators |
| Query states | Semantic vectors produced by the MLLM for downstream conditioning |
| Connector | Module translating MLLM representations into generator conditioning |
| DiT | Diffusion transformer |
| MMDiT | Multimodal diffusion transformer |
| Data-side balancing | Controlling which tasks/modalities appear in training batches |
| Loss-side balancing | Controlling relative gradient contribution of different objectives |
| Connector-first training | Freeze backbones and train modality bridges first |
| Sequential training | Stabilize understanding before training generation |
| Gradual unmasking | Slowly increase nontext/discrete modality loss contribution |
| Gradient conflict | Different objectives pushing shared parameters in incompatible directions |

---

## Self-check

Before moving on, make sure you can answer:

1. What makes a system any-to-any under the source definition?
2. Why does text naturally fit autoregressive token prediction?
3. Why are images more difficult to represent in a small vocabulary?
4. Why can audio be modeled as either continuous or discrete?
5. Why is video especially expensive?
6. What are the three design pressures in the chapter?
7. What are the three main architecture families?
8. What is vector quantization?
9. What is a codebook?
10. How does a codebook index become a visual token?
11. Why does vocabulary expansion happen in monolithic designs?
12. What is the codebook fidelity bottleneck?
13. Why does the source call Janus-Pro transitional?
14. What is different between its perception and generation sides?
15. What is a factorized generation head?
16. What does a trigger token do?
17. Why can factorized heads preserve a cleaner text vocabulary?
18. What does "continuous in, discrete out" mean?
19. What is RVQ?
20. Why does RVQ avoid one gigantic LLM vocabulary?
21. What is sequential RVQ generation?
22. What is parallel multicodebook generation?
23. What does the Thinker do?
24. What does the Talker do?
25. What makes a hybrid multiobjective model different from a factorized-head model?
26. What is the purpose of a VAE?
27. What two goals does VAE training balance?
28. What is the conceptual role of the KL term?
29. What is the difference between VAE and VQ-VAE?
30. What happens during diffusion's forward process?
31. What happens during the reverse process?
32. What target does the denoising MSE compare?
33. How can diffusion generalize beyond images?
34. How does a Transfusion-style model handle both discrete and continuous positions?
35. Why does text use causal attention?
36. Why can image latent patches use bidirectional attention within their block?
37. What is classifier-free guidance?
38. What does `ε_cond - ε_uncond` represent intuitively?
39. What happens when the guidance scale becomes too large?
40. How is a single denoiser trained to support CFG?
41. What is late conditioning?
42. What are the four parts of the query-based late-conditioning pipeline?
43. How does late conditioning differ from factorized heads?
44. What is a hidden-state query interface?
45. What is a CLIP-aligned conditioning interface?
46. Why might a hybrid continuous+discrete interface improve layout/text fidelity?
47. When is a linear connector enough?
48. When might a transformer bridge be useful?
49. How do diffusion generators consume query conditioning?
50. How does speech/TTS conditioning differ?
51. Why is Qwen-Image-Edit not presented as canonical query-token late conditioning?
52. What does its semantic stream represent?
53. What does its VAE stream preserve?
54. Why can sample percentages hide training imbalance?
55. What is data-side balancing?
56. What is loss-side balancing?
57. Why train connectors before full joint optimization?
58. Why might understanding-before-generation preserve capability?
59. What is gradual unmasking?
60. Why can cross-entropy and diffusion MSE conflict?
61. Which family offers the cleanest parameter separation?
62. Why start from pretrained components?
63. Why monitor multiple capabilities simultaneously?
64. Why use lower learning rates on stable pretrained backbones?
65. Which architecture would you choose for maximum modularity?
66. Which architecture would you choose when high media fidelity is the main goal?
67. Which architecture is attractive when low-latency discrete generation matters?
68. What is the central boundary-design question in any-to-any modeling?

---

## Retain this idea

**Any-to-any systems are not defined by one universal architecture. Their central
design decision is where continuous media should become discrete, where
continuous generation should happen, and how tightly rendering should be
coupled to semantic reasoning. Unified-vocabulary models maximize simplicity,
hybrid diffusion models maximize integration and fidelity, and late-conditioning
systems maximize modularity.**
""",

        "estimated_minutes": 360,
        "has_code_examples": True,
        "has_manual_image_requests": True,
        "sections": [
            {"id": "problem", "title": "The any-to-any problem", "order": 1},
            {"id": "modality-differences", "title": "Why modalities differ", "order": 2},
            {"id": "three-pressures", "title": "Three competing design pressures", "order": 3},
            {"id": "three-families", "title": "The three architecture families", "order": 4},
            {"id": "unified-vocab", "title": "Unified vocabulary models", "order": 5},
            {"id": "vector-quantization", "title": "Vector quantization", "order": 6},
            {"id": "codebook", "title": "Codebooks as modality vocabularies", "order": 7},
            {"id": "codebook-bottleneck", "title": "The codebook bottleneck", "order": 8},
            {"id": "monolithic", "title": "Monolithic architecture", "order": 9},
            {"id": "janus", "title": "Janus-Pro as a transitional design", "order": 10},
            {"id": "janus-modes", "title": "Explicit generation modes", "order": 11},
            {"id": "factorized-heads", "title": "Factorized generation heads", "order": 12},
            {"id": "semantic-handoff", "title": "Semantic handoff", "order": 13},
            {"id": "factorized-benefits", "title": "Benefits of factorized heads", "order": 14},
            {"id": "continuous-in-discrete-out", "title": "Continuous in, discrete out", "order": 15},
            {"id": "rvq", "title": "Residual vector quantization", "order": 16},
            {"id": "rvq-generation", "title": "Sequential and parallel code generation", "order": 17},
            {"id": "thinker-talker", "title": "Thinker-Talker architecture", "order": 18},
            {"id": "omni-inference", "title": "Multimodal input and output", "order": 19},
            {"id": "hybrid", "title": "Hybrid multiobjective models", "order": 20},
            {"id": "factorized-vs-hybrid", "title": "Factorized heads versus hybrid", "order": 21},
            {"id": "vae", "title": "Variational autoencoders", "order": 22},
            {"id": "vae-loss", "title": "VAE training intuition", "order": 23},
            {"id": "vqvae", "title": "VAE versus VQ-VAE", "order": 24},
            {"id": "diffusion", "title": "Diffusion for continuous generation", "order": 25},
            {"id": "diffusion-modalities", "title": "Diffusion across modalities", "order": 26},
            {"id": "transfusion", "title": "Unifying discrete and continuous representations", "order": 27},
            {"id": "block-causal", "title": "Block-causal multimodal attention", "order": 28},
            {"id": "hybrid-generation", "title": "Hybrid generation flow", "order": 29},
            {"id": "cfg", "title": "Classifier-free guidance", "order": 30},
            {"id": "cfg-training", "title": "Training for CFG", "order": 31},
            {"id": "diffusion-pseudocode", "title": "Diffusion pseudocode", "order": 32},
            {"id": "late-conditioning", "title": "Late conditioning", "order": 33},
            {"id": "factorized-vs-late", "title": "Factorized heads versus late conditioning", "order": 34},
            {"id": "late-pipeline", "title": "Query-based conditioning pipeline", "order": 35},
            {"id": "late-triggers", "title": "Generation trigger tokens", "order": 36},
            {"id": "query-spaces", "title": "Conditioning interface options", "order": 37},
            {"id": "connectors", "title": "Connector architectures", "order": 38},
            {"id": "generator-conditioning", "title": "How generators consume conditioning", "order": 39},
            {"id": "qwen-edit", "title": "Dual-conditioning image editing", "order": 40},
            {"id": "conditioning-handoff", "title": "Explicit conditioning handoff", "order": 41},
            {"id": "modularity-tradeoff", "title": "The modularity trade-off", "order": 42},
            {"id": "training-problem", "title": "Why any-to-any training is hard", "order": 43},
            {"id": "data-imbalance", "title": "Hidden data imbalance", "order": 44},
            {"id": "data-side", "title": "Data-side balancing", "order": 45},
            {"id": "loss-side", "title": "Loss-side balancing", "order": 46},
            {"id": "staged-training", "title": "Staged training", "order": 47},
            {"id": "connector-first", "title": "Connector-first alignment", "order": 48},
            {"id": "understanding-first", "title": "Understanding before generation", "order": 49},
            {"id": "gradual-unmasking", "title": "Gradual unmasking", "order": 50},
            {"id": "omni-staging", "title": "Thinker-Talker staging", "order": 51},
            {"id": "architecture-losses", "title": "Architecture-specific losses", "order": 52},
            {"id": "source-table-nuance", "title": "Factorized-head loss nuance", "order": 53},
            {"id": "pretrained-components", "title": "Start from pretrained components", "order": 54},
            {"id": "training-monitoring", "title": "Monitor multiple capabilities", "order": 55},
            {"id": "task-aware-lr", "title": "Task-aware learning rates", "order": 56},
            {"id": "family-choice", "title": "Choosing an architecture family", "order": 57},
            {"id": "evaluation", "title": "Any-to-any evaluation", "order": 58},
            {"id": "source-notes", "title": "Source-specific notes", "order": 59},
            {"id": "complete-mental-model", "title": "Complete any-to-any mental model", "order": 60},
        ],
    },

    "exercises": [
        {
            "id": "M01.L10.EX01",
            "title": "Choose the architecture family",
            "lesson_code": "M01.L10",
            "section_id": "three-families",
            "placement": "after_section",
            "description": (
                "Match product requirements to unified-vocabulary, hybrid, or "
                "late-conditioning designs."
            ),
            "instructions": (
                ('1. Choose the most appropriate family for each scenario:\n'
                 '   - A. Low-latency system where generated images are rough reasoning aids.\n'
                 '   - B. Image-generation product where visual fidelity matters more than speed.\n'
                 '   - C. Startup with a strong frozen MLLM and an existing diffusion generator, with little budget for full multimodal training.\n'
                 '2. For each, justify the choice using fidelity, latency, modularity, and training complexity.')
            ),
            "expected_output": (
                "A three-row decision table with family, rationale, and main trade-off."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "architecture-selection",
                "multimodal-generation",
                "tradeoff-analysis",
            ],
        },
        {
            "id": "M01.L10.EX02",
            "title": "Compare one codebook with RVQ",
            "lesson_code": "M01.L10",
            "section_id": "rvq",
            "placement": "after_section",
            "description": (
                "Build intuition for why factorized heads can use multiple codebooks."
            ),
            "instructions": (
                "Compare:\n"
                "A. One codebook with 8,192 possible codes.\n"
                "B. Six codebooks with 512 possible codes each.\n"
                "1. State the number of choices at one codebook level.\n"
                "2. Compute the conceptual combination count 512^6.\n"
                "3. Explain why this does NOT require adding 512^6 tokens to the LLM vocabulary.\n"
                "4. Explain sequential coarse-to-fine versus parallel prediction."
            ),
            "expected_output": (
                "A short numerical comparison plus an architecture explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "vector-quantization",
                "rvq",
                "factorized-heads",
            ],
        },
        {
            "id": "M01.L10.EX03",
            "title": "Reason about classifier-free guidance",
            "lesson_code": "M01.L10",
            "section_id": "cfg",
            "placement": "after_section",
            "description": (
                "Interpret conditional and unconditional noise predictions."
            ),
            "instructions": (
                ('1. For one scalar component, suppose:\n'
                 '2. ε_uncond = 0.20\n'
                 '3. ε_cond = 0.50\n'
                 '4. Compute ε_hat for s=1, s=3, and s=7.5 using:\n'
                 '5. ε_hat = ε_uncond + s(ε_cond - ε_uncond).\n'
                 '6. Then explain what increasing s does conceptually and why very high guidance may hurt diversity or create artifacts.')
            ),
            "expected_output": (
                "Three calculations plus a prompt-adherence versus diversity explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "diffusion",
                "classifier-free-guidance",
                "generation",
            ],
        },
        {
            "id": "M01.L10.EX04",
            "title": "Balance an any-to-any training mixture",
            "lesson_code": "M01.L10",
            "section_id": "loss-side",
            "placement": "after_section",
            "description": (
                "Reason about sample balance, token balance, and loss balance together."
            ),
            "instructions": (
                ('1. You are training on:\n'
                 '   - 60% text-only conversations,\n'
                 '   - 20% image-VQA,\n'
                 '   - 10% text-to-image,\n'
                 '   - 10% video QA.\n'
                 '2. Video samples contain 8x more input tokens than text samples.\n'
                 '3. Design a better balancing strategy using data-side and loss-side controls. Explain how you would detect whether text, video, or generation is dominating.')
            ),
            "expected_output": (
                "A revised mixture/weighting plan plus the validation metrics you would monitor."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "dataset-mixtures",
                "loss-balancing",
                "multitask-training",
            ],
        },
        {
            "id": "M01.L10.EX05",
            "title": "Design a see-hear-speak assistant",
            "lesson_code": "M01.L10",
            "section_id": "complete-mental-model",
            "placement": "after_section",
            "description": (
                "Synthesize the architecture choices into one any-to-any assistant."
            ),
            "instructions": (
                ('1. Design a system that can receive text, images, and video-with-audio, then return text and spoken answers.\n'
                 '2. Choose unified vocabulary, factorized heads, hybrid, or late conditioning.\n'
                 '3. Specify:\n'
                 '   - perception encoders,\n'
                 '   - reasoning component,\n'
                 '   - output handoff,\n'
                 '   - speech generation path,\n'
                 '   - what is frozen/trainable,\n'
                 '   - training stages,\n'
                 '   - losses,\n'
                 '   - metrics.\n'
                 "4. Justify the architecture using the source's trade-offs.")
            ),
            "expected_output": (
                "An architecture diagram or structured specification with training plan."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "any-to-any-design",
                "factorized-heads",
                "staged-training",
            ],
        },
        {
            "id": "M01.L10.EX06",
            "title": "Compare tightly integrated and modular generation",
            "lesson_code": "M01.L10",
            "section_id": "complete-mental-model",
            "placement": "after_section",
            "description": (
                "Compare hybrid multiobjective and late-conditioning systems."
            ),
            "instructions": (
                ('1. You have the same frozen MLLM and want high-quality image generation.\n'
                 '2. Design two versions:\n'
                 '   - A. A tightly integrated hybrid transformer that directly denoises continuous image latents.\n'
                 '   - B. A late-conditioning pipeline with MLLM query states, connector, and a swappable diffusion generator.\n'
                 '3. Compare training difficulty, fidelity/alignment, generator replaceability, gradient conflict risk, and inference flow.')
            ),
            "expected_output": (
                "A side-by-side architecture comparison and final trade-off summary."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "hybrid-multiobjective",
                "late-conditioning",
                "architecture-comparison",
            ],
        },
    ],

    "quiz": {
        "id": "M01.L10.QZ01",
        "title": "Any-to-Any Multimodal Models — Knowledge Check",
        "lesson_code": "M01.L10",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M01.L10.Q01",
                "section_id": "problem",
                "question": "What minimum capability does the source require for a model to be called truly any-to-any?",
                "options": [
                    "At least two input modalities and two output modalities",
                    "Only image input and text output",
                    "One modality in both directions",
                    "At least ten modalities",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter explicitly defines any-to-any using multiple input and output modalities."
                ),
            },
            {
                "id": "M01.L10.Q02",
                "section_id": "three-families",
                "question": "Which family converts modalities into discrete codes and reuses autoregressive token prediction?",
                "options": [
                    "Unified vocabulary models",
                    "Late-conditioning models only",
                    "Pure diffusion-only models",
                    "Retrieval systems",
                ],
                "correct": 0,
                "explanation": (
                    "Unified-vocabulary systems tokenize nontext signals through codebooks."
                ),
            },
            {
                "id": "M01.L10.Q03",
                "section_id": "vector-quantization",
                "question": "What does vector quantization do?",
                "options": [
                    "Maps a continuous representation to the nearest learned codebook entry",
                    "Creates a diffusion timestep",
                    "Adds Gaussian noise to text",
                    "Builds a FAISS index",
                ],
                "correct": 0,
                "explanation": (
                    "The codebook index becomes the discrete modality token."
                ),
            },
            {
                "id": "M01.L10.Q04",
                "section_id": "codebook-bottleneck",
                "question": "What is the central codebook trade-off?",
                "options": [
                    "Small codebooks are efficient but can limit fidelity; larger codebooks improve expressivity but increase complexity.",
                    "Larger codebooks always make training easier.",
                    "Small codebooks contain continuous values only.",
                    "Codebook size affects only text grammar.",
                ],
                "correct": 0,
                "explanation": (
                    "Quantization forces continuous variation into a finite set of representations."
                ),
            },
            {
                "id": "M01.L10.Q05",
                "section_id": "janus",
                "question": "Why does the source call Janus-Pro a transitional architecture?",
                "options": [
                    "It uses discrete visual tokens for generation but separates the understanding and generation encoders.",
                    "It has no visual encoder.",
                    "It is purely late conditioning.",
                    "It supports only text.",
                ],
                "correct": 0,
                "explanation": (
                    "Its generation side is discrete/autoregressive while its perception side uses a separate continuous encoder."
                ),
            },
            {
                "id": "M01.L10.Q06",
                "section_id": "factorized-heads",
                "question": "What is the defining idea of factorized generation heads?",
                "options": [
                    "The LLM emits a handoff/trigger and a specialized head generates modality-specific codes.",
                    "The LLM vocabulary must contain every possible pixel.",
                    "All outputs are produced by one text softmax.",
                    "No pretrained components are used.",
                ],
                "correct": 0,
                "explanation": (
                    "The semantic decision remains in the LLM while rendering is delegated."
                ),
            },
            {
                "id": "M01.L10.Q07",
                "section_id": "rvq",
                "question": "Why is RVQ attractive for factorized heads?",
                "options": [
                    "Multiple small codebooks create rich combinations without bloating the LLM vocabulary.",
                    "It removes all discrete representations.",
                    "It requires one huge codebook.",
                    "It is a text-only tokenizer.",
                ],
                "correct": 0,
                "explanation": (
                    "The specialist head handles codebook stacks outside the core text vocabulary."
                ),
            },
            {
                "id": "M01.L10.Q08",
                "section_id": "thinker-talker",
                "question": "In the Thinker-Talker pattern, what does the Talker do?",
                "options": [
                    "Generates speech/audio codes from semantic guidance",
                    "Builds image retrieval indexes",
                    "Performs only OCR",
                    "Quantizes the LLM weights",
                ],
                "correct": 0,
                "explanation": (
                    "The Thinker reasons; the Talker handles modality-specific speech generation."
                ),
            },
            {
                "id": "M01.L10.Q09",
                "section_id": "factorized-vs-hybrid",
                "question": "What distinguishes hybrid multiobjective models from factorized heads?",
                "options": [
                    "The shared transformer directly processes continuous media latents during denoising.",
                    "Hybrid models never use text.",
                    "Factorized heads always use diffusion inside the LLM.",
                    "There is no architectural difference.",
                ],
                "correct": 0,
                "explanation": (
                    "Continuous media generation is integrated into the shared transformer in the hybrid family."
                ),
            },
            {
                "id": "M01.L10.Q10",
                "section_id": "vae",
                "question": "What is the role of a VAE in diffusion-based media generation?",
                "options": [
                    "Compress high-dimensional media into a smaller continuous latent and decode it back.",
                    "Convert every image to a text token.",
                    "Provide a vector database.",
                    "Replace all attention layers.",
                ],
                "correct": 0,
                "explanation": (
                    "Diffusion can operate on a much smaller learned latent rather than raw media."
                ),
            },
            {
                "id": "M01.L10.Q11",
                "section_id": "vqvae",
                "question": "What is the main latent-space difference between a VAE and VQ-VAE?",
                "options": [
                    "A VAE uses continuous latents; a VQ-VAE quantizes latents into discrete codebook entries.",
                    "Both always use identical continuous latents.",
                    "A VQ-VAE has no encoder.",
                    "A VAE is text-only.",
                ],
                "correct": 0,
                "explanation": (
                    "That difference connects VAEs to diffusion and VQ-VAEs to discrete-token generation."
                ),
            },
            {
                "id": "M01.L10.Q12",
                "section_id": "diffusion",
                "question": "What is learned during diffusion training according to the source?",
                "options": [
                    "A model predicts the noise that was added to the latent.",
                    "A model predicts one final visual code only.",
                    "The model learns only text vocabulary.",
                    "The model performs nearest-neighbor search.",
                ],
                "correct": 0,
                "explanation": (
                    "The denoiser learns to reverse corruption at different noise levels."
                ),
            },
            {
                "id": "M01.L10.Q13",
                "section_id": "block-causal",
                "question": "Why do image latent patches use bidirectional attention inside their block in the source's hybrid design?",
                "options": [
                    "Denoising benefits from interactions among all patches of the image block.",
                    "Images must be generated as text.",
                    "Future text tokens must be visible.",
                    "It removes diffusion.",
                ],
                "correct": 0,
                "explanation": (
                    "The image is refined as a joint latent block rather than left-to-right text."
                ),
            },
            {
                "id": "M01.L10.Q14",
                "section_id": "cfg",
                "question": "What happens conceptually when CFG guidance scale is increased?",
                "options": [
                    "Prompt influence is amplified, often improving adherence but potentially reducing diversity.",
                    "The prompt is ignored.",
                    "The model becomes purely unconditional.",
                    "The codebook becomes smaller.",
                ],
                "correct": 0,
                "explanation": (
                    "CFG moves further in the direction defined by conditional versus unconditional predictions."
                ),
            },
            {
                "id": "M01.L10.Q15",
                "section_id": "factorized-vs-late",
                "question": "What best distinguishes late conditioning from a tightly factorized head?",
                "options": [
                    "The generator is designed as an independent, swappable system connected through a learned interface.",
                    "Late conditioning has no generator.",
                    "Factorized heads never use LLM hidden states.",
                    "Late conditioning requires one unified vocabulary.",
                ],
                "correct": 0,
                "explanation": (
                    "Modularity and architectural independence are the key design commitment."
                ),
            },
            {
                "id": "M01.L10.Q16",
                "section_id": "query-spaces",
                "question": "What is an advantage of CLIP-aligned conditioning latents in the source?",
                "options": [
                    "MLLM and generator already share a more compatible representation space, improving convergence.",
                    "They guarantee unlimited expressivity.",
                    "They eliminate all connectors in every architecture.",
                    "They make diffusion one-step.",
                ],
                "correct": 0,
                "explanation": (
                    "Alignment is easier when both sides already use a similar embedding language."
                ),
            },
            {
                "id": "M01.L10.Q17",
                "section_id": "data-imbalance",
                "question": "Why can sample percentages be misleading in any-to-any training?",
                "options": [
                    "Different modalities can contribute very different token counts and gradient magnitudes per sample.",
                    "All samples always have equal length.",
                    "Only text produces gradients.",
                    "Video has fewer tokens than text by definition.",
                ],
                "correct": 0,
                "explanation": (
                    "Long video or multimodal sequences can dominate even if they are a smaller fraction of examples."
                ),
            },
            {
                "id": "M01.L10.Q18",
                "section_id": "understanding-first",
                "question": "Why train understanding before generation in the source's staged strategy?",
                "options": [
                    "To reduce interference between text-understanding objectives and continuous-generation objectives.",
                    "To prevent the model from learning perception.",
                    "To remove pretrained components.",
                    "To make every parameter randomly initialized.",
                ],
                "correct": 0,
                "explanation": (
                    "Staging helps preserve established capabilities while adding generation."
                ),
            },
            {
                "id": "M01.L10.Q19",
                "section_id": "architecture-losses",
                "question": "Which pair of objectives characterizes the hybrid multiobjective family?",
                "options": [
                    "Cross-entropy for text and denoising MSE for continuous media",
                    "Only cosine similarity",
                    "Only classification loss",
                    "No training objective",
                ],
                "correct": 0,
                "explanation": (
                    "Hybrid systems must supervise both discrete language and continuous latent denoising."
                ),
            },
            {
                "id": "M01.L10.Q20",
                "section_id": "complete-mental-model",
                "type": "open",
                "question": (
                    "Design an assistant that can understand text, images, video, and audio, "
                    "then return text, speech, and generated images. Compare how you would "
                    "implement it using (1) unified discrete generation, (2) factorized heads, "
                    "(3) a hybrid diffusion-based transformer, and (4) late conditioning. "
                    "Explain representation choices, output handoffs, losses, training stages, "
                    "latency/fidelity trade-offs, and component replaceability."
                ),
            },
        ],
        "passing_score": 70,
    },
}
