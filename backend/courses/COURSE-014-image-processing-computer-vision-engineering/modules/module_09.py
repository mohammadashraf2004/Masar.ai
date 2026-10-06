"""M09.L01 — Image Restoration: Inverse Problems in Imaging.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 9. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M09.L01"

MODULE_ORDER = 9

MODULE_TITLE = "Image Restoration: Inverse Problems in Imaging"

MODULE_DESCRIPTION = (
    "Learn image restoration as an inverse problem, from inverse and Wiener "
    "deconvolution through Tikhonov regularization, Bayesian interpretation, CLEAN, "
    "sparse dictionary learning, NAFNet, instruction-guided restoration, LaMa and "
    "diffusion inpainting, editing, retouching, and outpainting."
)

SOURCE_CHAPTER = 9

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


TOPIC = {
    "title": "Image Restoration: Inverse Problems in Imaging",

    "slug": "image-processing-m09-l01",

    "description": (
        "A source-aligned lesson on recovering degraded images by modeling the degradation "
        "process, regularizing ill-posed inverse problems, using classical deconvolution and "
        "sparse priors, and applying modern learned and generative restoration models."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 6.5,

    "skill_tags": [
        "image-processing",
        "image-restoration",
        "inverse-problems",
        "deconvolution",
        "psf",
        "inverse-filter",
        "wiener-filter",
        "tikhonov",
        "bayesian-restoration",
        "clean-algorithm",
        "sparse-coding",
        "dictionary-learning",
        "omp",
        "nafnet",
        "instructir",
        "lama",
        "diffusion-inpainting",
        "diffedit",
        "retouching",
        "outpainting",
        "module-09",
    ],

    "prerequisite_ids": ["M08.L01"],

    "lesson": {
        "title": "Image Restoration: Inverse Problems in Imaging",

        "content": r"""
# Image Restoration: Inverse Problems in Imaging

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M09.L01  
> **Module:** Image Restoration: Inverse Problems in Imaging  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 9. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the difference between image enhancement and image restoration.
- Model blur and noise with a point spread function and an additive-noise term.
- Explain why restoration is often an ill-posed inverse problem.
- Apply and critique inverse filtering for known blur kernels.
- Explain how Wiener filtering balances deblurring and noise suppression.
- Explain Tikhonov regularization as data fidelity plus a prior.
- Connect Wiener and Tikhonov restoration to Bayesian MMSE and MAP estimation.
- Explain Högbom CLEAN as a greedy sparse deconvolution method.
- Describe dictionary learning and Orthogonal Matching Pursuit for patch-based denoising.
- Explain why zero-mean patches and overlap averaging are useful.
- Explain the motivation and architecture ideas behind NAFNet.
- Describe instruction-guided restoration with InstructIR.
- Compare DeepFill-style CNN inpainting, LaMa, and diffusion-based inpainting.
- Explain prompt-guided editing with DiffEdit/DDIM inversion.
- Distinguish inpainting, editing, retouching, and outpainting.
- Choose a restoration strategy according to the degradation model, priors, data availability, and fidelity requirements.

---

## 1. Restoration begins with a degradation model

Image enhancement asks:

> How can I make this image look more useful or visually pleasing?

Image restoration asks a stricter question:

> What process degraded the image, and how can I estimate the original image that produced this observation?

The source chapter models degradation as:

```text
g = h * f + n
```

where:

- `f` is the unknown original image,
- `h` is the degradation function or point spread function (PSF),
- `*` denotes convolution,
- `n` is additive noise,
- `g` is the observed degraded image.

Restoration seeks an estimate:

```text
f_hat ≈ f
```

### Why this is an inverse problem

The forward process is:

```text
clean image
   ↓ blur / degradation
   ↓ noise
observed image
```

Restoration tries to move in the opposite direction.

### Why the problem is ill-posed

The source describes the problem in Hadamard's sense:

- a unique solution may not exist,
- small changes in the observation may create large changes in the inverse solution,
- additional constraints or priors may be required.

A blur can destroy or strongly attenuate frequencies.

Noise can then dominate those same frequencies.

So simply "undoing the blur" can become numerically unstable.

### Core restoration tasks

The chapter names several canonical tasks:

- denoising,
- deblurring,
- inpainting,
- dehazing/deraining,
- super-resolution.

### Denoising versus deblurring

Denoising is mainly:

```text
g = f + n
```

Deblurring is mainly:

```text
g = h * f + n
```

The important difference is that deblurring tries to invert a convolutional degradation in addition to handling noise.

---

## 2. Inverse filtering: the simplest deconvolution idea

Using the convolution theorem:

```text
G(u,v) = H(u,v) F(u,v) + N(u,v)
```

If noise were absent and `H` were known:

```text
F_hat = G / H
```

This is the **inverse filter**.

### Why it looks attractive

The blur multiplies the image spectrum by the transfer function.

So dividing by the transfer function seems like a direct undo operation.

### Frequency-domain workflow

```python
F = np.fft.fft2(image)
H = np.fft.fft2(
    np.fft.ifftshift(psf)
)

blurred = np.fft.ifft2(
    F * H
).real
```

For restoration:

```python
eps = 1e-6

G = np.fft.fft2(blurred)

F_hat = G / (H + eps)

restored = np.fft.ifft2(
    F_hat
).real
```

The small `eps` avoids literal division by zero.

### The fundamental instability

Suppose at one frequency:

```text
|H| ≈ 0
```

Then:

```text
1 / |H| -> very large
```

Any small noise at that frequency gets amplified enormously.

That is why inverse filtering works best when:

- blur is accurately known,
- noise is absent or extremely small,
- the transfer function does not approach zero too aggressively.

[[IMAGE_NEEDED: Inverse filtering instability | Show a blur transfer function with near-zero high-frequency values, a noisy spectrum divided by the transfer function, and amplified high-frequency noise in the restored image | Learner should see why small H values cause unstable inversion]]

### Gaussian and motion blur

The chapter demonstrates the same logic for:

- Gaussian blur,
- horizontal motion blur.

The PSF changes, but the deconvolution principle is the same.

---

## 3. Wiener filtering: deblur while accounting for noise

The inverse filter ignores the statistical structure of noise.

The Wiener filter explicitly balances:

- undoing blur,
- suppressing noise amplification.

The source frames it as a **minimum mean square error (MMSE)** estimator.

A standard frequency-domain form contains:

```text
H*
-------------------------
|H|^2 + S_n / S_f
```

where:

- `H*` is the complex conjugate of the blur transfer function,
- `S_n` is noise power spectral density,
- `S_f` is signal power spectral density.

### Intuition

When noise is small:

```text
S_n / S_f -> small
```

the Wiener filter behaves more like inverse filtering.

When noise is strong:

```text
S_n / S_f -> large
```

the filter suppresses unreliable frequencies rather than amplifying them.

[[IMAGE_NEEDED: Inverse vs Wiener deconvolution | Show original, blurred+noisy, inverse-filter restoration with amplified noise, and Wiener restoration balancing sharpness and noise | Learner should understand Wiener filtering as regularized statistical inversion]]

### Why real applications are harder

The original image spectrum is unknown.

The exact noise spectrum is often unknown.

So the source introduces **unsupervised Wiener filtering**, where these quantities or their ratio are estimated from the degraded observation.

With scikit-image:

```python
from skimage import restoration

restored, _ = restoration.unsupervised_wiener(
    degraded,
    psf,
)
```

The main lesson is not that Wiener "knows" the truth.

It estimates a trade-off from assumptions and observed data.

---

## 4. Tikhonov regularization and the Bayesian view

A different strategy is to formulate restoration as optimization.

Instead of directly solving:

```text
H f = g
```

we solve a compromise:

```text
data fidelity
+
regularization
```

A Tikhonov objective has the form:

```text
||Hf - g||^2
+
lambda ||L f||^2
```

where:

- the first term asks the restored image to reproduce the observation after degradation,
- `L` encodes a prior,
- `lambda` controls the regularization strength.

### Meaning of lambda

```text
lambda too small
-> close to unstable inversion
-> noise amplification

lambda too large
-> strong smoothing
-> detail loss
```

This is the classic fidelity-versus-prior trade-off.

### Possible priors

If:

```text
L = identity
```

the solution penalizes overall image energy.

If:

```text
L = gradient operator
```

the solution penalizes roughness.

The chapter connects this idea to broader regularization approaches such as:

- gradient smoothness,
- Laplacian penalties,
- total variation-like priors.

### Fourier-domain form

With circular convolution, a simple Tikhonov solution resembles:

```text
H*
------------------
|H|^2 + lambda
```

This looks similar to the Wiener denominator.

### Wiener versus Tikhonov

| Wiener | Tikhonov |
|---|---|
| statistical estimation | variational optimization |
| uses signal/noise statistics or estimates | uses explicit regularization strength |
| frequency-adaptive SNR interpretation | deterministic prior strength |
| MMSE interpretation | MAP interpretation under Gaussian prior |

### Bayesian interpretation

The source makes the following conceptual distinction:

```text
Wiener -> Bayesian MMSE
Tikhonov -> Bayesian MAP
```

MMSE estimates the conditional expectation.

MAP selects the most probable image under the posterior model.

[[IMAGE_NEEDED: Data fidelity and regularization balance | Show a slider-like diagram from small lambda with noisy/sharp restoration to large lambda with oversmoothed restoration, with a balanced solution in the middle | Learner should see regularization as controlled bias added to stabilize inversion]]

---

## 5. CLEAN: greedy sparse deconvolution

CLEAN was developed for radio astronomy.

Its key prior is:

> The scene can be approximated by a sparse collection of point sources.

If the PSF is known, a point source appears as a shifted copy of that PSF.

So the observed dirty image is treated as a superposition of shifted PSFs.

### Högbom CLEAN

Start with:

```text
residual = dirty image
clean components = 0
```

Repeatedly:

1. locate the strongest residual peak,
2. record a fraction of that peak as a clean component,
3. subtract a scaled, shifted copy of the PSF,
4. repeat until a threshold or iteration limit.

Then:

```text
final image
=
restoring_beam * clean_components
+
final residual
```

### Loop gain

The source recommends a small gain for stability.

A lower gain:

- subtracts more cautiously,
- needs more iterations.

### Why CLEAN works

It matches the PSF shape greedily.

The source connects it conceptually to **matching pursuit**:

```text
dictionary atoms = shifted PSFs
```

At each iteration, the algorithm selects the atom best matching the current residual.

[[IMAGE_NEEDED: Högbom CLEAN workflow | Show dirty astronomical image, PSF, strongest residual peak selection, subtraction of shifted PSF, accumulated sparse clean components, restoring beam, and final restored image | Learner should understand CLEAN as greedy PSF matching under a sparsity prior]]

### When it is a good fit

CLEAN is especially suitable when:

- the scene is sparse,
- objects are point-like,
- the PSF has sidelobes.

It is less natural for smoothly varying extended scenes.

---

## 6. Sparse representations and dictionary learning

Another restoration prior is:

> Small natural-image patches can often be represented using only a few atoms from an overcomplete dictionary.

For a vectorized patch `x`:

```text
x ≈ D alpha
```

where:

- `D` is a dictionary,
- `alpha` is sparse.

### Sparse coding

A sparse code uses only a few nonzero coefficients.

The ideal combinatorial sparse problem is hard, so the chapter uses **Orthogonal Matching Pursuit (OMP)** as a greedy approximation.

OMP repeatedly:

1. finds the atom most correlated with the current residual,
2. adds it to the active set,
3. recomputes coefficients by projection,
4. updates the residual.

### Dictionary learning

Dictionary learning alternates:

```text
fix D
-> estimate sparse codes

fix codes
-> update D
```

This lets the dictionary adapt to image structures such as:

- edges,
- textures,
- repeated local patterns.

### Why zero-mean patches?

The source removes the patch mean before sparse coding.

This separates:

```text
DC / brightness information
```

from:

```text
texture / structural variation
```

The mean is added back after reconstruction.

### Patch reconstruction

The workflow is:

```text
noisy image
    ↓
extract overlapping patches
    ↓
zero mean
    ↓
OMP sparse coding
    ↓
dictionary reconstruction
    ↓
add patch means back
    ↓
overlap-average patches
    ↓
restored image
```

[[IMAGE_NEEDED: Dictionary-learning denoising | Show noisy image, overlapping 8×8 patches, learned dictionary atoms, sparse coefficient vector with few nonzeros, reconstructed patches, and overlap-averaged restored image | Learner should understand sparse restoration as projection onto learned local structure]]

### Important trade-offs

The chapter highlights:

- patch size,
- stride/overlap,
- number of atoms,
- sparsity level,
- dictionary-training data,
- aggregation method,
- memory and computation.

Lower sparsity can denoise more strongly but may remove detail.

---

## 7. Learned priors with NAFNet

Classical methods write the prior explicitly.

Deep restoration learns an implicit prior from data.

The network learns:

```text
degraded image
   -> restored image
```

from training examples.

### NAFNet

The source introduces **Nonlinear Activation Free Network (NAFNet)** for denoising.

Its distinguishing idea is that it removes standard nonlinear activations such as ReLU/GELU and relies on:

- convolution,
- layer normalization,
- multiplicative gating,
- residual/encoder-decoder structure.

The source describes a simple gating mechanism that multiplies feature groups element-wise.

### Statistical interpretation

For paired noisy/clean training examples and squared error, the source links learned denoising to a data-driven MMSE estimator.

### Pretrained inference workflow

```text
noisy image
    ↓ preprocessing/tensor conversion
pretrained NAFNet
    ↓
restored tensor
    ↓
output image
```

Large inputs can be processed in grids/patches when needed.

[[IMAGE_NEEDED: Classical prior vs learned prior | Show Tikhonov as explicit formula/prior on one side and NAFNet learning degraded-to-clean mapping from pairs on the other | Learner should understand the shift from hand-designed priors to data-learned priors]]

The lesson focus is the model idea and inference pipeline, not memorizing repository setup commands.

---

## 8. Instruction-guided restoration with InstructIR

Task-specific restoration assumes we already know the degradation:

```text
denoise
deblur
derain
...
```

InstructIR adds natural-language control.

Instead of only:

```text
restored = model(image)
```

the problem becomes:

```text
restored = model(image, instruction)
```

Examples from the source include instructions such as:

```text
remove the raindrops but preserve the background
```

or:

```text
remove the little dots
```

### Architecture idea

The source combines:

1. a language encoder,
2. an instruction/degradation embedding head,
3. a restoration network receiving both image and text information.

The objective combines terms for:

- pixel fidelity,
- perceptual quality,
- degradation/instruction prediction.

### Why this changes the restoration problem

The model can use user intent when multiple plausible operations are possible.

This moves restoration toward multimodal conditional inference.

[[IMAGE_NEEDED: InstructIR multimodal restoration | Show degraded image plus natural-language instruction entering image-restoration and language branches, fused representation, and restored output | Learner should understand restoration conditioned jointly on image evidence and user intent]]

### Gradio interface

The chapter also demonstrates a simple interface:

```text
image upload + text prompt
        ↓
InstructIR
        ↓
restored image
```

This is an important product pattern for interactive restoration systems.

---

## 9. DeepFill-style and diffusion-based inpainting

Inpainting fills missing or corrupted image regions.

The chapter contrasts older CNN approaches such as DeepFill with diffusion-based generation.

### DeepFill-style CNN inpainting

The source describes classic CNN inpainting as using ideas such as:

- encoder-decoder networks,
- contextual attention,
- partial/constrained convolution-style reasoning.

Strengths:

- fast inference,
- good structured-hole filling.

Limitations:

- can struggle with unconstrained missing content,
- may be weaker at global semantic consistency.

### Diffusion-based inpainting

Diffusion treats completion as conditional generative sampling.

A model gradually denoises a representation while being conditioned on:

- the known image,
- the mask,
- often a text prompt.

### Forward process

The chapter introduces the standard idea:

```text
clean latent/image
    ↓ progressive noise
noisy latent
```

### Reverse process

A neural network predicts/removes noise step by step.

Text guidance modifies the denoising prediction so generated content better follows the prompt.

### Masked generation

The key inpainting principle is:

```text
known region -> preserve
masked region -> generate
```

The source emphasizes careful mask alignment, prompt design, inference steps, guidance strength, memory management, and artifact inspection.

[[IMAGE_NEEDED: Diffusion inpainting pipeline | Show damaged image, binary mask, encoded latent with masked region noised, text-conditioned denoising UNet, and final completed image | Learner should see that only the masked region should be synthesized while context remains consistent]]

### Important limitation

A plausible generated region is not guaranteed to be the historical truth.

For forensic or scientific exact recovery, generative inpainting may be inappropriate.

---

## 10. LaMa for large-mask inpainting

The chapter then presents **Large Mask Inpainting (LaMa)**.

LaMa is designed for:

- large holes,
- high-resolution content,
- long-range/global image structure.

### Why ordinary local receptive fields can struggle

If a hole is large, the most useful context may be far away from the missing region.

A local-only network may not see enough of the scene.

### Fourier/global operations

The source emphasizes LaMa's use of frequency/Fourier-style global operations to provide a large effective receptive field.

This helps model:

- long lines,
- repeated patterns,
- global illumination,
- scene-wide consistency.

### Simple inference workflow

With a wrapper:

```python
from simple_lama_inpainting import SimpleLama

model = SimpleLama()

output = model(
    image,
    mask,
)
```

Typical convention:

```text
white mask -> region to fill
black mask -> region to preserve
```

The source recommends confirming the wrapper's exact mask convention.

[[IMAGE_NEEDED: LaMa large-mask inpainting | Show original image with a large missing region, binary mask, local-context challenge, global/Fourier receptive-field concept, and completed result | Learner should understand why long-range context matters for large holes]]

### Strengths and risks

Strengths:

- large holes,
- global coherence,
- single forward pass,
- resolution robustness.

Risks:

- hallucinated content,
- color/lighting mismatch,
- geometry errors,
- no guarantee of exact truth.

---

## 11. Diffusion editing with DiffEdit and DDIM inversion

The chapter distinguishes **editing** from ordinary missing-region restoration.

Image editing changes selected content according to a target instruction.

### DiffEdit workflow

The source demonstrates:

1. load a source image,
2. define source and target prompts,
3. generate a semantic mask,
4. invert the real image into diffusion latent space using DDIM inversion,
5. regenerate the masked content toward the target prompt.

Conceptually:

```text
source image
    ↓ DDIM inversion
latent trajectory
    ↓ semantic mask + target prompt
diffusion editing
    ↓
edited image
```

### Why inversion matters

A real image is not automatically on the exact latent trajectory needed for controlled generation.

DDIM inversion approximately maps it into a latent/noise trajectory so later generation can preserve much of the original structure.

[[IMAGE_NEEDED: DiffEdit workflow | Show original image, source/target prompts, automatically inferred mask, DDIM inversion to latent space, target-conditioned denoising, and edited output | Learner should understand mask inference and latent inversion as separate steps]]

The source contrasts deterministic DDIM-style inversion with stochastic DDPM-style diffusion at a high level.

---

## 12. Inpainting, editing, and retouching are related but different

These operations can all use generative models, but their intent differs.

### Inpainting

Goal:

```text
fill a missing/masked interior region
```

Input:

- image,
- explicit mask,
- optional prompt.

### Editing

Goal:

```text
change selected content intentionally
```

Input may include:

- image,
- target prompt,
- explicit or inferred mask.

### Retouching

Goal:

```text
refine existing image
while preserving core content
```

The chapter uses image-to-image diffusion at **low strength**.

Low strength:

- adds little noise,
- preserves original structure more strongly.

Higher strength:

- enables larger semantic changes,
- moves from retouching toward editing.

[[IMAGE_NEEDED: Inpainting vs editing vs retouching | Show three branches from one source image: masked hole filling, object replacement via prompt, and low-strength whole-image retouch with mostly preserved structure | Learner should distinguish the task objective, not just the model family]]

---

## 13. Outpainting: generating beyond the original frame

Outpainting extends an image outside its original boundaries.

The workflow is:

1. create a larger canvas,
2. paste the original image into it,
3. mark new regions with a mask,
4. use an inpainting/generative model to synthesize the added area.

Conceptually:

```text
original domain Ω
inside
larger domain Ω'
```

The model generates:

```text
Ω' - Ω
```

using:

- visible original context,
- text prompt,
- diffusion prior.

### Difference from inpainting

```text
inpainting  -> fills holes inside the original domain
outpainting -> creates content outside the original domain
```

[[IMAGE_NEEDED: Outpainting canvas expansion | Show original image centered in a larger blank canvas, mask over added borders, diffusion generation in the new area, and final extended scene | Learner should see outpainting as inpainting over newly created canvas regions]]

### Source mask caution

The supplied chapter contains more than one mask convention in its generative examples. For any specific library/pipeline, verify whether white means "replace" or "preserve" before running inference.

This is an important engineering lesson:

> Do not assume mask polarity is universal across libraries.

---

## 14. Choosing a restoration strategy

The methods in this chapter differ mainly by what prior knowledge they use.

| Situation | Reasonable starting point from this chapter |
|---|---|
| Known blur, almost no noise | Inverse filtering |
| Known blur with noise | Wiener |
| Need deterministic explicit regularization | Tikhonov |
| Sparse point sources + known PSF | CLEAN |
| Patch structure / interpretable sparse prior | Dictionary learning + OMP |
| Learned denoising from pretrained model | NAFNet |
| User describes desired restoration | InstructIR |
| Large masked hole | LaMa |
| Semantic masked completion | Diffusion inpainting |
| Prompt-driven object/content replacement | DiffEdit |
| Subtle whole-image refinement | Low-strength diffusion retouch |
| Extend beyond image boundary | Outpainting |

A good restoration engineer asks:

```text
What is the degradation model?
What is known about the PSF/noise?
What prior is justified?
Is hallucination acceptable?
Is exact fidelity required?
How much compute is available?
```

{{exercise:M09.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Restoration is just another word for enhancement.

### Why this is wrong

The source distinguishes restoration by its use of an explicit or implicit degradation model and an attempt to recover the underlying clean image.

### Misconception 2

> If the blur kernel is known, inverse filtering always solves deblurring.

### Why this is wrong

Near-zero transfer-function values make inversion unstable and amplify noise.

### Misconception 3

> Wiener filtering simply sharpens more carefully.

### Why this is incomplete

Wiener filtering is a statistical estimator balancing inverse filtering against signal/noise uncertainty.

### Misconception 4

> Regularization only makes optimization slower.

### Why this is wrong

Regularization stabilizes ill-posed inversion by adding prior assumptions.

### Misconception 5

> CLEAN is a general-purpose best method for every blurred photograph.

### Why this is wrong

Its strongest prior is sparse point-like structure and PSF-shaped components.

### Misconception 6

> Sparse coding uses every dictionary atom a little.

### Why this is wrong

The core assumption is that each patch uses only a small number of active atoms.

### Misconception 7

> A pretrained restoration model no longer contains a prior.

### Why this is wrong

The prior is implicit in the learned parameters and training distribution.

### Misconception 8

> Generative inpainting recovers the exact missing historical pixels.

### Why this is wrong

It synthesizes plausible content conditioned on context and, often, text. The generated content may never have existed in the original scene.

### Misconception 9

> Inpainting, editing, retouching, and outpainting are interchangeable names.

### Why this is wrong

They differ in region, intent, amount of allowed change, and conditioning.

### Misconception 10

> Mask polarity is the same in every inpainting library.

### Why this is wrong

Different APIs can define white/black mask semantics differently. Always verify the specific pipeline.

---

## Key terminology

| Term | Meaning |
|---|---|
| Image restoration | Recovering an estimate of an undegraded image from a modeled degraded observation |
| Inverse problem | Estimating an unknown cause from observed effects |
| Ill-posed | Problem lacking uniqueness, stability, or sufficient constraints |
| PSF | Point spread function describing blur response |
| Deconvolution | Reversing convolutional blur |
| Inverse filter | Frequency-domain division by the blur transfer function |
| Wiener filter | MMSE-oriented deconvolution balancing blur inversion and noise |
| PSD | Power spectral density |
| Tikhonov regularization | Data-fidelity plus quadratic prior optimization |
| Regularization parameter | Weight controlling fidelity-prior trade-off |
| MAP | Maximum a posteriori estimation |
| MMSE | Minimum mean square error estimation |
| CLEAN | Greedy PSF-subtraction sparse deconvolution |
| Loop gain | Fraction of a residual peak subtracted per CLEAN iteration |
| Sparse representation | Approximation using few active dictionary atoms |
| Dictionary learning | Joint estimation of atoms and sparse codes |
| OMP | Orthogonal Matching Pursuit |
| Overcomplete dictionary | Dictionary containing more atoms than signal dimensions |
| NAFNet | Nonlinear Activation Free image-restoration network |
| InstructIR | Instruction-conditioned image restoration model |
| Inpainting | Filling missing/masked image regions |
| DeepFill | CNN-family semantic inpainting approach |
| LaMa | Large-mask inpainting architecture using global/Fourier operations |
| Diffusion model | Generative model based on progressive noising and learned denoising |
| Classifier-free guidance | Combining conditional/unconditional predictions to strengthen prompt guidance |
| DDIM inversion | Approximate mapping of a real image into a diffusion latent trajectory |
| DiffEdit | Prompt-based diffusion editing with inferred masks |
| Retouching | Refinement while largely preserving source content |
| Outpainting | Generating plausible content outside the original image frame |

---

## Self-check

Before continuing, make sure you can answer:

1. What does the degradation model `g = h * f + n` represent?
2. Why is image restoration often ill-posed?
3. What makes restoration different from enhancement in the source framing?
4. Why does inverse filtering amplify noise?
5. What does the Wiener filter do when noise is strong?
6. Why are signal/noise PSD estimates difficult in real applications?
7. What is the role of `lambda` in Tikhonov regularization?
8. How is Tikhonov related to a smoothness prior?
9. What is the MMSE interpretation of Wiener filtering?
10. What is the MAP interpretation of Tikhonov?
11. What prior does Högbom CLEAN assume?
12. What does CLEAN subtract at each iteration?
13. Why is loop gain usually kept below one?
14. What does a restoring beam do?
15. What is a sparse code?
16. Why does OMP update a residual repeatedly?
17. Why are patch means removed before dictionary learning?
18. Why do overlapping patches need aggregation?
19. What kind of prior is learned by NAFNet?
20. What is unusual about NAFNet's activation design?
21. How does InstructIR condition restoration on user intent?
22. What is the key difference between DeepFill-style and diffusion-based inpainting?
23. Why are diffusion inpainting outputs not guaranteed to be historically correct?
24. Why does LaMa help with large holes?
25. What mask convention caution must be checked before inpainting?
26. What does DDIM inversion enable in DiffEdit?
27. How does editing differ from inpainting?
28. How does retouching strength control preservation versus transformation?
29. How does outpainting differ from inpainting?
30. Which restoration methods are most interpretable?
31. Which methods depend most strongly on training data?
32. When should generative restoration be avoided?

---

## Retain this idea

**Image restoration is fundamentally about priors. Classical methods write the degradation and prior explicitly, sparse methods assume compact representations, deep networks learn priors from data, and generative models add powerful semantic priors. The more freedom the prior has to invent content, the more carefully you must distinguish plausible reconstruction from faithful recovery.**
        """,

        "estimated_minutes": 390,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "inverse-problem-foundations", "title": "Restoration Begins with a Degradation Model", "order": 1},
            {"id": "inverse-filter", "title": "Inverse Filtering: The Simplest Deconvolution Idea", "order": 2},
            {"id": "wiener-filter", "title": "Wiener Filtering: Deblur While Accounting for Noise", "order": 3},
            {"id": "tikhonov-bayesian", "title": "Tikhonov Regularization and the Bayesian View", "order": 4},
            {"id": "clean-deconvolution", "title": "CLEAN: Greedy Sparse Deconvolution", "order": 5},
            {"id": "sparse-representations", "title": "Sparse Representations and Dictionary Learning", "order": 6},
            {"id": "nafnet", "title": "Learned Priors with NAFNet", "order": 7},
            {"id": "instructir", "title": "Instruction-Guided Restoration with InstructIR", "order": 8},
            {"id": "diffusion-inpainting", "title": "DeepFill-Style and Diffusion-Based Inpainting", "order": 9},
            {"id": "lama", "title": "LaMa for Large-Mask Inpainting", "order": 10},
            {"id": "diffedit-editing", "title": "Diffusion Editing with DiffEdit and DDIM Inversion", "order": 11},
            {"id": "inpainting-editing-retouching", "title": "Inpainting, Editing, and Retouching Are Related but Different", "order": 12},
            {"id": "outpainting", "title": "Outpainting: Generating Beyond the Original Frame", "order": 13},
            {"id": "method-selection", "title": "Choosing a Restoration Strategy", "order": 14},
        ],
    },

    "exercises": [
        {
            "id": "M09.L01.EX01",

            "title": "Compare Classical Deblurring Strategies",

            "lesson_code": "M09.L01",

            "section_id": "tikhonov-bayesian",

            "placement": "after_section",

            "description": (
                "Compare inverse filtering, Wiener restoration, and Tikhonov regularization "
                "under controlled blur and noise."
            ),

            "instructions": (
                "1. Load one grayscale image normalized to [0,1].\n"
                "2. Create a known PSF such as a box blur or motion-blur kernel.\n"
                "3. Blur the image and then create at least two observations: blur-only and "
                "blur-plus-Gaussian-noise.\n"
                "4. Apply inverse filtering to both observations and inspect high-frequency "
                "noise amplification.\n"
                "5. Apply unsupervised Wiener restoration to the noisy observation.\n"
                "6. Implement or use a Tikhonov-style restoration at three lambda values.\n"
                "7. Compute PSNR or MSE against the clean image for all restorations.\n"
                "8. Compare the sharpness-versus-noise trade-off visually and numerically.\n"
                "9. Explain why the inverse filter can be best in a nearly noise-free case "
                "yet fail badly after noise is added.\n"
                "10. State whether your preferred method relies on statistical estimation "
                "or explicit regularization."
            ),

            "expected_output": (
                "A notebook or script showing the clean, blurred, noisy, inverse-filter, "
                "Wiener, and several Tikhonov outputs plus a small metric table and an "
                "explanation of instability and regularization."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "psf",
                "inverse-filter",
                "wiener-filter",
                "tikhonov",
                "fft-deconvolution",
                "regularization",
                "psnr",
                "inverse-problem-reasoning",
            ],
        },

        {
            "id": "M09.L01.EX02",

            "title": "Build a Restoration Decision Lab",

            "lesson_code": "M09.L01",

            "section_id": "method-selection",

            "placement": "after_section",

            "description": (
                "Connect classical, sparse, learned, and generative restoration by matching "
                "each method to the prior and failure mode it assumes."
            ),

            "instructions": (
                "1. Prepare four degraded cases: a known blur, additive noise, a masked hole, "
                "and a prompt-driven edit or canvas extension.\n"
                "2. For the known blur, choose Wiener or Tikhonov and justify the choice.\n"
                "3. For additive noise, run either dictionary/OMP denoising or a pretrained "
                "NAFNet-style denoiser if available.\n"
                "4. For the masked hole, compare a non-prompt inpainting method such as LaMa "
                "with a prompt-conditioned diffusion inpainting workflow, if resources allow.\n"
                "5. For the semantic task, document a DiffEdit, InstructIR, retouching, or "
                "outpainting workflow from the chapter.\n"
                "6. For every method, write down its prior: explicit degradation model, "
                "sparsity, learned dataset prior, language condition, or generative prior.\n"
                "7. Record at least one likely failure mode for every method.\n"
                "8. Identify which outputs may hallucinate content and which are intended to "
                "remain conservative reconstructions.\n"
                "9. Add a short note explaining when generative inpainting would be "
                "inappropriate for scientific, forensic, or exact-recovery use.\n"
                "10. Finish with a problem-to-method decision table."
            ),

            "expected_output": (
                "A notebook/report containing at least one classical restoration, one "
                "sparse/learned restoration, one masked completion workflow, and a decision "
                "table linking each method to its assumptions, strengths, and failure modes."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "restoration-method-selection",
                "sparse-priors",
                "learned-priors",
                "generative-inpainting",
                "hallucination-awareness",
                "evaluation",
                "system-design",
            ],
        },
    ],

    "quiz": {
        "id": "M09.L01.QZ01",

        "title": "Image Restoration: Inverse Problems in Imaging — Knowledge Check",

        "lesson_code": "M09.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M09.L01.Q01",
                "section_id": "inverse-problem-foundations",
                "question": "What distinguishes restoration from enhancement in the chapter?",
                "options": [
                    "Restoration uses a model or prior about the degradation process",
                    "Restoration only changes brightness",
                    "Enhancement always recovers exact original pixels",
                    "Restoration cannot use neural networks",
                ],
                "correct": 0,
                "explanation": (
                    "The source frames restoration as estimating the original image by "
                    "incorporating knowledge of how the observation was degraded."
                ),
            },

            {
                "id": "M09.L01.Q02",
                "section_id": "inverse-filter",
                "question": "Why is direct inverse filtering unstable when H is close to zero?",
                "options": [
                    "Division amplifies small noise/errors dramatically",
                    "It automatically removes all noise",
                    "It prevents Fourier transforms",
                    "It changes grayscale into RGB",
                ],
                "correct": 0,
                "explanation": (
                    "Small transfer-function magnitudes create very large inverse gains."
                ),
            },

            {
                "id": "M09.L01.Q03",
                "section_id": "wiener-filter",
                "question": (
                    "How does Wiener filtering behave when the estimated noise contribution is high?"
                ),
                "options": [
                    "It suppresses unreliable frequencies more strongly",
                    "It becomes exact inverse division everywhere",
                    "It removes the PSF from the model",
                    "It always sharpens more aggressively",
                ],
                "correct": 0,
                "explanation": (
                    "The Wiener denominator reduces gain where the signal-to-noise ratio is poor."
                ),
            },

            {
                "id": "M09.L01.Q04",
                "section_id": "tikhonov-bayesian",
                "question": "What does increasing Tikhonov lambda generally do?",
                "options": [
                    "Strengthens the prior/regularization and can oversmooth details",
                    "Removes the need for a degradation model",
                    "Guarantees exact recovery",
                    "Always increases high-frequency gain",
                ],
                "correct": 0,
                "explanation": (
                    "Larger regularization emphasizes smoothness/prior consistency over data fidelity."
                ),
            },

            {
                "id": "M09.L01.Q05",
                "section_id": "tikhonov-bayesian",
                "question": "Which Bayesian interpretation does the source assign to Tikhonov?",
                "options": [
                    "MAP estimation",
                    "MMSE expectation",
                    "K-means clustering",
                    "Nearest-neighbor interpolation",
                ],
                "correct": 0,
                "explanation": (
                    "With a Gaussian prior, Tikhonov corresponds to a MAP estimate."
                ),
            },

            {
                "id": "M09.L01.Q06",
                "section_id": "clean-deconvolution",
                "question": "What does Högbom CLEAN subtract at each iteration?",
                "options": [
                    "A scaled, shifted copy of the PSF at the strongest residual peak",
                    "The entire image mean",
                    "A random Fourier coefficient",
                    "A learned neural feature map",
                ],
                "correct": 0,
                "explanation": (
                    "CLEAN greedily removes PSF-shaped contributions and records sparse components."
                ),
            },

            {
                "id": "M09.L01.Q07",
                "section_id": "sparse-representations",
                "question": "What is the key sparse-coding assumption for an image patch?",
                "options": [
                    "It can be approximated by only a few active dictionary atoms",
                    "It requires every atom with equal weight",
                    "It must be constant",
                    "It can only contain noise",
                ],
                "correct": 0,
                "explanation": (
                    "Sparse coding intentionally limits the number of nonzero coefficients."
                ),
            },

            {
                "id": "M09.L01.Q08",
                "section_id": "sparse-representations",
                "question": "Why are overlapping reconstructed patches averaged?",
                "options": [
                    "To combine multiple local estimates and reduce seams/block artifacts",
                    "To create a blur kernel",
                    "To remove the dictionary",
                    "To estimate a text prompt",
                ],
                "correct": 0,
                "explanation": (
                    "Many patches cover the same pixel, so aggregation combines their estimates."
                ),
            },

            {
                "id": "M09.L01.Q09",
                "section_id": "nafnet",
                "question": "What architectural idea is emphasized for NAFNet in the source?",
                "options": [
                    "Replacing standard nonlinear activations with simple multiplicative gating",
                    "Using only hand-designed inverse filters",
                    "Removing all convolution",
                    "Operating without learned parameters",
                ],
                "correct": 0,
                "explanation": (
                    "The source highlights NAFNet's activation-free design with simple gating."
                ),
            },

            {
                "id": "M09.L01.Q10",
                "section_id": "instructir",
                "question": "What additional input does InstructIR use beyond the degraded image?",
                "options": [
                    "A natural-language restoration instruction",
                    "Only a fixed PSF",
                    "A JPEG quality number only",
                    "A Laplacian kernel only",
                ],
                "correct": 0,
                "explanation": (
                    "InstructIR conditions restoration on language describing the user's intended operation."
                ),
            },

            {
                "id": "M09.L01.Q11",
                "section_id": "diffusion-inpainting",
                "question": (
                    "What is the key conceptual difference between generative inpainting and exact inverse restoration?"
                ),
                "options": [
                    "Generative inpainting may synthesize plausible content that is not the true missing content",
                    "Generative inpainting never uses context",
                    "Exact inverse restoration always uses text prompts",
                    "There is no difference",
                ],
                "correct": 0,
                "explanation": (
                    "A generative model samples plausible completions from learned priors."
                ),
            },

            {
                "id": "M09.L01.Q12",
                "section_id": "lama",
                "question": "Why is LaMa especially useful for large missing regions?",
                "options": [
                    "Its global/Fourier-style operations provide long-range context",
                    "It only looks at one neighboring pixel",
                    "It requires no mask",
                    "It is an inverse Fourier division filter",
                ],
                "correct": 0,
                "explanation": (
                    "The source emphasizes the global receptive field enabled by Fourier-style operations."
                ),
            },

            {
                "id": "M09.L01.Q13",
                "section_id": "diffedit-editing",
                "question": "What role does DDIM inversion play in DiffEdit?",
                "options": [
                    "It maps the real image approximately into the diffusion latent trajectory for structure-preserving editing",
                    "It computes a Wiener PSD",
                    "It learns a sparse dictionary",
                    "It detects blur using Laplacian variance",
                ],
                "correct": 0,
                "explanation": (
                    "Inversion provides a latent starting point associated with the source image."
                ),
            },

            {
                "id": "M09.L01.Q14",
                "section_id": "inpainting-editing-retouching",
                "question": "What is the intended effect of a low diffusion strength during retouching?",
                "options": [
                    "Preserve most source structure while allowing small refinements",
                    "Completely replace the image",
                    "Delete all known pixels",
                    "Force a binary output",
                ],
                "correct": 0,
                "explanation": (
                    "Low strength introduces less perturbation, keeping the output closer to the source."
                ),
            },

            {
                "id": "M09.L01.Q15",
                "section_id": "outpainting",
                "question": "What makes outpainting different from inpainting?",
                "options": [
                    "Outpainting generates content in an expanded domain outside the original frame",
                    "Outpainting cannot use masks",
                    "Inpainting always changes the entire image",
                    "Outpainting is only a denoising method",
                ],
                "correct": 0,
                "explanation": (
                    "The canvas is enlarged and the newly added regions are generated from context."
                ),
            },

            {
                "id": "M09.L01.Q16",
                "section_id": "method-selection",
                "type": "open",
                "question": (
                    "You have four tasks: deblur a noisy image with an approximately known "
                    "PSF, denoise repeated textures, repair a large missing photo region, and "
                    "remove an object according to a text instruction. Choose one method "
                    "from this lesson for each task. For every choice, state the prior it "
                    "uses, one expected strength, and one important failure mode."
                ),
            },
        ],

        "passing_score": 70,
    },
}
