"""M13.L01 — Generative AI in Image Processing and Computer Vision.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 13. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.

Important implementation note:
Some model names, hosted checkpoints, repositories, and API syntax in the source are
version-sensitive. This lesson preserves the chapter's concepts and source-aligned
examples; always verify current library/API documentation before executing external
service or repository examples.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M13.L01"

MODULE_ORDER = 13

MODULE_TITLE = "Generative AI in Image Processing and Computer Vision"

MODULE_DESCRIPTION = (
    "Learn the evolution of generative vision from conditional GANs and VAEs through "
    "image-to-image translation, StyleGAN and generative restoration, DDPM and latent "
    "diffusion, Stable Diffusion, instruction and structure-guided editing, SDXL, "
    "identity/pose conditioning, and multimodal image-generation and vision workflows."
)

SOURCE_CHAPTER = 13

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


TOPIC = {
    "title": "Generative AI in Image Processing and Computer Vision",

    "slug": "image-processing-m13-l01",

    "description": (
        "A source-aligned capstone lesson on conditional generative models, latent spaces, "
        "image translation, face synthesis/restoration, diffusion models, controllable "
        "generation, multimodal image editing and understanding, and practical generative "
        "computer-vision workflows."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 8.0,

    "skill_tags": [
        "generative-ai",
        "computer-vision",
        "cgan",
        "cvae",
        "pix2pix",
        "cyclegan",
        "stylegan",
        "gfpgan",
        "ddpm",
        "latent-diffusion",
        "stable-diffusion",
        "instructpix2pix",
        "controlnet",
        "sdxl",
        "ip-adapter",
        "image-generation",
        "image-editing",
        "inpainting",
        "vision-language",
        "multimodal-ai",
        "visual-question-answering",
        "module-13",
    ],

    "prerequisite_ids": ["M12.L01"],

    "lesson": {
        "title": "Generative AI in Image Processing and Computer Vision",

        "content": r"""
# Generative AI in Image Processing and Computer Vision

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M13.L01  
> **Module:** Generative AI in Image Processing and Computer Vision  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 13. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

> **Version note:** Several demonstrations in the source use hosted checkpoints, external repositories, and commercial APIs. These interfaces can change. Learn the architecture and workflow first; verify the current documentation before executing any external-service example.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the shift from discriminative vision to generative vision.
- Explain how conditional GANs control generation with labels or attributes.
- Explain projection discrimination, hinge loss, spectral normalization, EMA, and FID at a practical level.
- Describe CVAE encoder, latent distribution, reparameterization, decoder, reconstruction loss, and KL regularization.
- Compare cGANs and CVAEs in stability, sharpness, and latent-space structure.
- Distinguish paired Pix2Pix training from unpaired CycleGAN training.
- Explain cycle consistency and why it discourages arbitrary domain mappings.
- Explain StyleGAN latent spaces, interpolation, style mixing, inversion, and real-image editing.
- Explain how GFPGAN uses a generative facial prior for blind face restoration.
- Explain forward and reverse diffusion in DDPMs.
- Explain why latent diffusion is more computationally efficient than pixel-space diffusion.
- Describe Stable Diffusion as VAE + text encoder + denoising U-Net + scheduler.
- Explain instruction-guided image editing with InstructPix2Pix.
- Explain structural control with ControlNet.
- Describe practical SDXL workflows: text-to-image, image-to-image, restoration, style conversion, super-resolution, and inpainting.
- Explain how IP-Adapter and ControlNet can combine reference appearance with pose/geometry constraints.
- Explain the source's DALL·E 2/3 comparison at a conceptual level.
- Describe multimodal image understanding, generation, editing, inpainting, VQA, and multi-image workflows exposed through image/vision APIs.
- Explain hybrid classical + generative workflows such as edge-guided editing.
- Distinguish plausible generated/restored content from verified ground truth.
- Explain how generative and multimodal systems can be applied in industrial inspection, remote sensing, medical education, and scientific visualization.

---

## 1. From understanding images to generating them

Earlier computer-vision tasks ask questions such as:

```text
What is this image?
Where is the object?
Which pixels belong to it?
```

Generative vision adds new questions:

```text
Can I create a new image?
Can I change this image?
Can I fill missing content?
Can I translate one visual domain into another?
Can I control geometry, style, identity, or semantics?
```

A useful chapter map is:

```text
GANs / VAEs
    ↓
learn controllable latent representations

Pix2Pix / CycleGAN
    ↓
translate between visual domains

StyleGAN / GFPGAN
    ↓
high-fidelity synthesis + generative priors

DDPM / latent diffusion
    ↓
generate by iterative denoising

Stable Diffusion / SDXL
    ↓
text-conditioned latent generation

ControlNet / IP-Adapter
    ↓
explicit structural + visual conditioning

multimodal image/vision systems
    ↓
natural-language generation, editing, analysis
```

[[IMAGE_NEEDED: Evolution of generative vision | Show a timeline/flow from cGAN/CVAE → Pix2Pix/CycleGAN → StyleGAN/GFPGAN → DDPM/LDM → Stable Diffusion/SDXL → ControlNet/IP-Adapter → multimodal image APIs | Learner should see increasingly flexible conditioning and control]]

The chapter's unifying concept is **conditioning**.

A generative model is more useful when we can tell it:

- which class,
- which visual domain,
- which text concept,
- which input image,
- which pose,
- which edge map,
- which reference identity,
- which region to edit.

---

## 2. Conditional GANs: generation through competition

A standard GAN contains two networks.

### Generator

The generator maps random noise to a synthetic image:

```text
z -> G(z)
```

### Discriminator

The discriminator decides whether an input is:

```text
real
or
generated
```

The networks compete.

As the discriminator becomes better at detecting fake images, the generator receives pressure to create more realistic outputs.

### Why conditioning matters

A normal GAN has limited control over what it creates.

A conditional GAN supplies a condition `y`.

The generator becomes:

```text
G(z, y)
```

and the discriminator judges:

```text
D(x, y)
```

For Fashion-MNIST:

```text
y = shoe, bag, dress, ...
```

so a learner can request a specific category.

### Label embeddings

The source converts class labels into learned vectors.

Conceptually:

```text
class ID
   ↓ embedding
continuous class representation
       +
random latent z
       ↓
generator
```

### Projection discriminator

The source uses a projection term to measure compatibility between image features and the requested label.

The discriminator score contains two ideas:

```text
Is this image realistic?
Does this image match the supplied class?
```

This is stronger than merely asking real/fake.

[[IMAGE_NEEDED: Conditional GAN architecture | Show latent z and class label y entering the generator; real/generated images plus the same label entering a projection discriminator with realism + class-compatibility scoring | Learner should understand that conditioning affects both generation and discrimination]]

### GAN stabilization in the source

The chapter uses several practical improvements.

**Spectral normalization**

Constrains discriminator weight behavior to stabilize gradients.

**Hinge loss**

Reduces some instability associated with the original GAN objective.

**EMA generator**

Maintains an exponential moving average of generator parameters:

```text
theta_ema
=
beta * theta_ema
+
(1-beta) * theta
```

The EMA model often produces more stable evaluation samples.

### FID

Fréchet Inception Distance compares feature distributions of:

- real images,
- generated images.

Interpretation:

```text
lower FID
-> generated distribution closer to real distribution
```

But the source also notes that FID is not a perfect substitute for human judgment.

---

## 3. Conditional VAE: a probabilistic latent space

A Conditional Variational Autoencoder also supports controlled generation, but it does not use an adversarial discriminator.

Its three main parts are:

```text
encoder
reparameterization
decoder
```

### Encoder

The encoder receives:

```text
image x
+
class y
```

and predicts a Gaussian latent distribution:

```text
mu(x,y)
sigma(x,y)
```

### Reparameterization trick

Direct random sampling blocks ordinary gradient flow.

The VAE rewrites sampling as:

```text
z =
mu
+
sigma * epsilon

epsilon ~ N(0, I)
```

Randomness is isolated in `epsilon`, while `mu` and `sigma` remain differentiable.

### Decoder

The decoder receives:

```text
latent z
+
class condition y
```

and reconstructs or generates an image.

### CVAE loss

Two goals compete:

```text
reconstruction loss
+
beta * KL divergence
```

**Reconstruction**

Keep the decoded image faithful to the data.

**KL regularization**

Keep the latent distribution near a known prior, usually a standard Gaussian.

This encourages:

- continuity,
- smooth interpolation,
- meaningful sampling.

[[IMAGE_NEEDED: CVAE architecture | Show image + class label entering encoder → mu/logvar → reparameterization z → decoder + same class label → reconstruction, with reconstruction loss and KL regularization arrows | Learner should understand why the latent space becomes smooth and sampleable]]

### cGAN versus CVAE

| cGAN | CVAE |
|---|---|
| adversarial training | probabilistic reconstruction |
| often sharper images | often smoother images |
| training can be unstable | usually easier to optimize |
| mode collapse possible | explicit latent regularization |
| strong realism objective | interpretable/continuous latent structure |

Neither model is universally "better."

The choice depends on whether the priority is:

- perceptual sharpness,
- training stability,
- latent interpretability,
- conditional control.

---

## 4. Latent interpolation and semantic manifolds

A latent space is useful when nearby vectors produce related images.

### Fixed latent, changing condition

In a conditional model, keep `z` fixed and interpolate between class embeddings.

Example:

```text
Sneaker
  ↓ gradual condition interpolation
Ankle Boot
```

This isolates the role of the condition.

### Fixed condition, changing latent

Keep the class fixed while interpolating between latent codes.

This explores variation inside one semantic category.

### Why interpolation is important

A smooth transition suggests the model has learned a structured manifold rather than memorizing disconnected training examples.

The chapter visualizes generated samples with t-SNE to inspect class organization.

[[IMAGE_NEEDED: Conditional latent traversal | Show a row transitioning between two Fashion-MNIST classes and a second row varying style within one fixed class, plus a small t-SNE cluster view | Learner should distinguish semantic class control from within-class latent variation]]

---

## 5. Pix2Pix and CycleGAN: translating visual domains

Image-to-image translation learns:

```text
source image
→ target-domain image
```

Examples:

- sketch → photograph,
- map → satellite view,
- summer → winter,
- horse → zebra.

### Pix2Pix

Pix2Pix requires paired examples:

```text
(x, y)
```

where `x` and `y` correspond spatially.

Its objective combines:

```text
adversarial loss
+
reconstruction loss
```

The adversarial term encourages realism.

The reconstruction term encourages correspondence with the paired target.

### CycleGAN

CycleGAN learns from unpaired collections.

Suppose:

```text
X = horse images
Y = zebra images
```

It learns two mappings:

```text
G: X -> Y
F: Y -> X
```

Cycle consistency requires:

```text
F(G(x)) ≈ x
G(F(y)) ≈ y
```

This discourages the model from changing content arbitrarily.

[[IMAGE_NEEDED: Pix2Pix versus CycleGAN | Show paired input-target examples for Pix2Pix with one generator/discriminator path; beside it show unpaired horse/zebra collections with two generators and cycle-consistency loops | Learner should remember paired correspondence versus unpaired reversible translation]]

### Source trade-off

```text
paired data available
-> Pix2Pix can use direct correspondence

paired data unavailable
-> CycleGAN offers more flexible training
```

CycleGAN's freedom can also introduce:

- texture artifacts,
- imperfect fine details,
- changes not strictly justified by the source image.

---

## 6. StyleGAN: high-fidelity synthesis and semantic control

StyleGAN introduces a style-based generator with an intermediate latent representation.

The source emphasizes:

```text
Z space
-> mapping network
-> W-style representation
-> layer-wise synthesis
```

This improves semantic control.

### StyleGAN3

The chapter focuses on StyleGAN3's reduction of aliasing artifacts.

Its design treats synthesis more carefully as a signal-processing problem.

The source links this to:

- translation consistency,
- rotation consistency,
- improved structural stability.

### Latent interpolation

Two random seeds produce two latent points.

Interpolating:

```text
z(alpha)
=
(1-alpha) z1
+
alpha z2
```

creates a smooth sequence of synthetic faces.

### Style mixing

Different generator layers control different levels of abstraction.

The source demonstrates mixing styles so:

```text
early layers
-> coarse face structure / pose

later layers
-> fine texture / hair / lighting
```

This provides controllable semantic combinations.

[[IMAGE_NEEDED: StyleGAN latent and style mixing | Show z→mapping→W styles→synthesis layers, plus a grid where row latent controls coarse structure and column latent controls fine appearance | Learner should understand layer-wise semantic control]]

### StyleGANEX and inversion

Generation from random latent codes is only one direction.

Real-image editing requires:

```text
real image
→ latent representation
→ generator reconstruction
```

This is GAN inversion.

The source's StyleGANEX example uses encoder-based prediction plus latent/feature/noise refinement.

Once two real faces are inverted, their latent codes can be interpolated to create smooth morphing.

---

## 7. GFPGAN: generative priors for face restoration

Traditional restoration tries to recover detail from the degraded pixels.

GFPGAN adds a powerful learned prior:

```text
What should a realistic face look like?
```

The degradation model is conceptually:

```text
degraded face
=
unknown degradation(clean face)
+
noise
```

The model combines restoration with a pretrained face generator/manifold.

The source describes losses involving:

- reconstruction,
- perceptual similarity,
- adversarial realism,
- identity preservation.

[[IMAGE_NEEDED: GFPGAN restoration | Show low-quality face → restoration encoder/network → pretrained StyleGAN facial prior → reconstructed face → paste-back into original image | Learner should understand how a strong learned facial prior can recreate plausible detail]]

### Important interpretation

A generative prior can produce convincing facial detail.

That detail can be **plausible** rather than a guaranteed recovery of historically exact pixels.

This matters when restoration is used for:

- archives,
- evidence,
- scientific records.

---

## 8. DDPMs: generation by learning to remove noise

Diffusion models use a fundamentally different training idea from GANs.

Instead of:

```text
latent vector -> image
```

in one direct generator, they learn:

```text
noise -> slightly cleaner
     -> cleaner
     -> ...
     -> image
```

### Forward diffusion

Start with clean data:

```text
x0
```

and gradually add Gaussian noise:

```text
x0 -> x1 -> x2 -> ... -> xT
```

At large `T`, the image becomes close to random noise.

A closed-form expression allows sampling a noisy state directly from `x0` using the cumulative noise schedule.

### Reverse diffusion

Train a network to predict the noise in:

```text
x_t
```

Then a scheduler uses that prediction to compute a less noisy state.

Starting from random noise:

```text
x_T
→ x_(T-1)
→ ...
→ x_0
```

a realistic image can emerge.

[[IMAGE_NEEDED: DDPM forward and reverse processes | Show clean image progressively corrupted to Gaussian noise across timesteps, then a U-Net+scheduler iteratively reversing the process from noise back to a synthesized image | Learner should see generation as repeated denoising]]

### Why diffusion became important

The source emphasizes:

- stable training relative to adversarial competition,
- expressive generation,
- high image quality.

Trade-off:

- many denoising steps can make sampling computationally expensive.

---

## 9. Latent diffusion: denoise a compressed image representation

Pixel-space diffusion on high-resolution images is expensive.

Latent Diffusion Models first compress the image.

```text
image x
  ↓ VAE encoder
latent z
  ↓ diffusion
denoised latent
  ↓ VAE decoder
image
```

### Why it is cheaper

A latent tensor contains far fewer values than the original image.

The source gives the intuition that a large RGB image can be compressed by tens of times before diffusion.

### VAE compression

An AutoencoderKL predicts a latent distribution.

A latent sample is decoded back into an image.

The reconstruction should retain most visually important information.

### Latent interpolation

Encode two images:

```text
z1, z2
```

then interpolate:

```text
z(alpha)
=
(1-alpha) z1
+
alpha z2
```

and decode.

Smooth changes show meaningful latent continuity.

[[IMAGE_NEEDED: Pixel diffusion vs latent diffusion | Show high-resolution pixel-space diffusion on left; on right VAE encoder compresses image to small latent grid, diffusion happens there, then decoder reconstructs image | Learner should see why latent diffusion reduces compute]]

---

## 10. Stable Diffusion: text-conditioned latent denoising

Stable Diffusion combines several modules.

```text
text prompt
  ↓ text encoder
text embedding
          \
random latent noise
      ↓
denoising U-Net + scheduler
      ↓
clean latent
      ↓
VAE decoder
      ↓
generated image
```

### Text conditioning

A text encoder maps the prompt into a semantic representation.

The U-Net predicts noise while conditioned on:

- current noisy latent,
- diffusion timestep,
- text embedding.

This makes the reverse process prompt-dependent.

### Inference steps

Generation starts from random latent noise.

Each reverse step removes predicted noise.

More steps are not automatically "better" for every model; the appropriate range depends on the trained scheduler/model.

[[IMAGE_NEEDED: Stable Diffusion architecture | Show text prompt→text encoder, random latent→U-Net denoising loop with scheduler and cross-attention, VAE decoder→image | Learner should understand the four-module latent diffusion pipeline]]

### Prompt control

Changing the prompt moves generation toward a different semantic solution while the overall denoising mechanism remains the same.

---

## 11. InstructPix2Pix: edit an existing image with language

Text-to-image generation begins from noise.

Image editing begins from an existing image.

InstructPix2Pix receives:

```text
input image
+
editing instruction
```

Examples:

```text
"turn this sketch into a realistic product photo"
"change the lighting"
"make this scene look like winter"
```

### Architecture intuition

The input image is encoded into latent features.

The instruction becomes a language embedding.

The denoising model is conditioned on both.

So the target is:

```text
preserve important source structure
+
apply requested semantic change
```

[[IMAGE_NEEDED: InstructPix2Pix editing | Show source sketch and text instruction entering an image-conditioned diffusion pipeline, then a realistic edited handbag/product output that preserves silhouette and layout | Learner should see editing as source-conditioned generation rather than generation from scratch]]

### Control trade-off

Stronger instruction guidance can improve requested transformation while also increasing the risk of changing details the user wanted preserved.

---

## 12. ControlNet: separate semantic intent from geometry

A text prompt describes what should be generated.

But text alone often gives weak control over exact structure.

ControlNet adds an external structural signal such as:

- Canny edges,
- depth,
- segmentation map,
- sketch,
- keypoints,
- human pose.

### Source example: horse → zebra

1. extract Canny edges from the original horse,
2. use those edges as ControlNet input,
3. provide a prompt requesting a zebra,
4. generate while preserving the edge-constrained geometry.

Conceptually:

```text
text
-> semantic change

edge map
-> shape / pose / composition

diffusion model
-> combined result
```

[[IMAGE_NEEDED: ControlNet Canny guidance | Show original horse, Canny edge control image, text prompt "zebra", ControlNet branch injecting structure into Stable Diffusion U-Net, and generated zebra preserving pose/composition | Learner should understand structure and semantics as separate conditioning sources]]

### Why this matters

ControlNet allows generative systems to retain:

- composition,
- pose,
- object silhouette,
- geometric layout,

while changing:

- style,
- class,
- texture,
- appearance.

---

## 13. Practical Stable Diffusion and SDXL workflows

The source treats diffusion as a toolbox, not only a text-to-image generator.

### SDXL-Turbo text-to-image

Distilled diffusion reduces the number of denoising steps needed for fast generation.

The source describes:

```text
traditional pipeline
-> many reverse steps

turbo/distilled pipeline
-> very few steps
```

This supports interactive prototyping.

### Typography generation

The chapter demonstrates poster generation containing text.

The important idea is that newer image generators improve:

- prompt understanding,
- layout,
- typography,

although text rendering can still fail.

### Image-to-image refinement

An initial concept image can be passed into another diffusion stage with a low/moderate transformation strength.

This enables:

```text
rough concept
→ detailed concept
```

while preserving the broad composition.

### Face/photo restoration

Image-to-image diffusion can be prompted to:

- remove scratches,
- improve sharpness,
- improve lighting,
- preserve identity.

Again, plausible detail is not guaranteed to equal historically exact detail.

### Style transformation

Combine:

```text
ControlNet structural guidance
+
style prompt
```

to preserve geometry while changing rendering style.

### Super-resolution

A diffusion upscaler can synthesize plausible high-frequency detail.

This differs from fixed interpolation.

### Inpainting

A mask marks the region to change.

The model generates new content consistent with:

- surrounding context,
- prompt.

[[IMAGE_NEEDED: Diffusion application grid | Show six panels: fast text-to-image, typography poster, image-to-image refinement, restoration, style conversion with structural control, super-resolution, and inpainting | Learner should recognize one diffusion family solving many image-processing tasks through different conditioning]]

---

## 14. IP-Adapter + ControlNet: appearance and pose as separate controls

Text alone often fails to preserve a specific visual identity or reference appearance.

IP-Adapter introduces visual conditioning from a reference image.

ControlNet introduces geometric conditioning.

The source combines three signals:

```text
text prompt
-> semantic description

reference image
-> identity / appearance

OpenPose skeleton
-> body pose / geometry
```

### IP-Adapter scale

A control parameter adjusts the influence of the reference image.

Conceptually:

```text
higher reference influence
-> stronger appearance preservation
-> less freedom

lower reference influence
-> more text-driven variation
```

### Pose control

An OpenPose map acts as a geometric blueprint.

It constrains the generated subject's body pose.

[[IMAGE_NEEDED: IP-Adapter plus ControlNet | Show text prompt, reference portrait, OpenPose skeleton entering one diffusion pipeline and producing several portraits with similar appearance but the target pose | Learner should understand independent semantic, appearance, and geometric conditioning]]

### Why this architecture is important

It introduces modular controllability.

Different conditioning channels can independently describe:

- what,
- who/which appearance,
- where/how posed.

---

## 15. DALL·E 2 and DALL·E 3 in the source chapter

The source uses hosted image-generation APIs to compare prompt-based output quality.

Its experiment evaluates the same prompts across DALL·E 2 and DALL·E 3.

The comparison considers:

- prompt fidelity,
- composition,
- scene complexity,
- object consistency,
- visual realism,
- typography,
- diversity.

The source reports DALL·E 3 as generally stronger for:

- detailed prompts,
- multi-object composition,
- coherent spatial relationships,
- text rendering.

[[IMAGE_NEEDED: Same-prompt generation comparison | Show one complex prompt above two rows of generated images labeled DALL·E 2 and DALL·E 3, with callouts for composition, prompt adherence, and typography | Learner should focus on evaluation dimensions rather than API syntax]]

### Important implementation note

The exact hosted model names, API endpoints, response formats, pricing, and availability shown in any book can change over time.

The durable lesson is:

```text
same prompt set
+
controlled comparison
+
qualitative/quantitative criteria
=
model benchmarking
```

---

## 16. Unified multimodal workflows: understanding and editing

The chapter then combines two capabilities:

```text
vision understanding
+
image generation/editing
```

### Image understanding

A multimodal vision model receives:

```text
image
+
question/instruction
```

and returns text.

Applications shown in the source include:

- captioning,
- visual search,
- accessibility,
- document/image indexing,
- structured reporting.

### Image editing

A generative image model receives:

```text
existing image
+
instruction
```

and modifies the image.

Applications include:

- relighting,
- recoloring,
- enhancement,
- style transformation,
- content modification.

[[IMAGE_NEEDED: Multimodal understand-and-edit loop | Show input image → vision model → textual assessment/instruction plan → image editing model → edited result, with arrows indicating text and image information flow | Learner should see reasoning/understanding and image synthesis as complementary capabilities]]

### Keep concepts separate

A vision-language model that **describes** an image is not the same component as an image generator that **creates/edits** an image.

The source explicitly distinguishes these roles.

---

## 17. Hybrid classical computer vision + generative editing

One of the chapter's strongest practical patterns combines deterministic image processing with generative synthesis.

### Edge-guided editing

1. OpenCV extracts Canny edges.
2. The edge-derived region becomes a mask/control signal.
3. A generative editor modifies only the selected structure.

This combines:

```text
classical CV
-> exact geometric signal

generative model
-> visually rich synthesis
```

[[IMAGE_NEEDED: Classical-plus-generative hybrid | Show original image→Canny edge detector→binary/RGBA edge mask→generative editing prompt→glowing artistic edge result | Learner should see traditional CV used as controllable preprocessing for generative AI]]

### Why hybrid systems are useful

Generative models are flexible.

Classical image-processing methods are often:

- deterministic,
- interpretable,
- precise.

Combining them can provide both:

```text
control + creativity
```

---

## 18. Generative editing applications in the source

The chapter demonstrates many image-editing patterns.

### Explicit-mask inpainting

```text
image + mask + prompt
-> fill selected region
```

### Prompt-controlled style transfer

A prompt can specify both:

- artistic style,
- how strongly geometry should be preserved.

### Restoration

The chapter demonstrates a two-stage pattern:

```text
vision model
-> assess degradation

image generator/editor
-> perform restoration
```

### Multi-image composition

Several source images can contribute concepts to one output.

### E-commerce enhancement

A product can be placed into:

- studio background,
- professional lighting,
- advertising-style presentation.

### Colorization

A grayscale image can be transformed into a plausible color image.

### Sketch or painting → photorealistic image

The model preserves broad structure while synthesizing realistic:

- materials,
- texture,
- lighting.

### Local object editing

Example concept:

```text
"change this yellow car to red"
```

while preserving the rest of the scene.

### Object removal

The model reconstructs plausible background after removing the requested subject.

### Background replacement

The foreground is kept while a new environment is synthesized.

### Scene transformation

The source includes:

- night → day,
- summer → winter.

[[IMAGE_NEEDED: Prompt-driven editing taxonomy | Show one source image branching into colorization, object recolor, object removal, background replacement, style transfer, restoration, and seasonal transformation | Learner should distinguish local edits, masked edits, global appearance changes, and full scene transformations]]

### Important interpretation

When a model fills missing pixels or reconstructs hidden background, it creates a plausible visual solution.

Do not treat generated hidden content as verified evidence of what was originally there.

---

## 19. Vision-language analysis: VQA, inspection, remote sensing, and medical education

The source demonstrates multimodal understanding beyond ordinary captions.

### Visual Question Answering

Pipeline:

```text
encode/provide image
+
ask a natural-language question
→ answer
```

This can make image analysis accessible through conversational interfaces.

### Industrial inspection

The source asks a vision model to inspect manufactured items and return structured JSON with fields such as:

- defect type,
- location,
- severity,
- confidence,
- overall summary.

This illustrates a useful engineering pattern:

```text
visual reasoning
+
structured output schema
```

[[IMAGE_NEEDED: Industrial inspection with structured output | Show manufactured parts image entering a vision-language model and producing a structured defect table/JSON with location, severity, confidence, and summary | Learner should see multimodal models as report-generating assistants rather than only classifiers]]

### Remote-sensing change detection

Two satellite images are compared.

The prompt asks for changes such as:

- new/removed structures,
- road changes,
- construction,
- vegetation,
- water,
- urban expansion.

The output is structured into a change report.

This does not replace precise geospatial measurement.

It demonstrates high-level multimodal comparison.

### Medical-image description

The source uses a multimodal model for a **non-diagnostic** educational description of an MRI.

It asks for:

- visible anatomy,
- orientation,
- structures,
- observations,
- limitations.

The chapter explicitly states that human expert review remains essential for diagnosis.

[[IMAGE_NEEDED: Multimodal visual analysis domains | Show VQA image+question, factory inspection image+JSON, before/after satellite images+change report, and MRI+non-diagnostic educational description | Learner should see the same image-language interface applied across very different domains]]

---

## 20. Scientific visual generation and the chapter capstone

The chapter ends with chemistry-oriented examples.

### Educational figure generation

A prompt requests an infographic comparing:

- `sp`,
- `sp²`,
- `sp³`

hybridization, including:

- geometry,
- bond angle,
- examples.

This demonstrates generative AI as a scientific communication tool.

### Image → reasoning → image

Another example begins from a molecule image.

The workflow is:

```text
molecule image
→ multimodal analysis / reasoning
→ proposed design concept
→ generated 2D visual
```

The important systems concept is the **multimodal loop**:

```text
visual input
→ textual/structured reasoning
→ new visual output
```

[[IMAGE_NEEDED: Multimodal scientific workflow | Show scientific image/diagram entering a vision-language model, structured reasoning in the middle, then generated educational/scientific visualization | Learner should understand image→reasoning→image as a reusable workflow pattern]]

### Verification is essential

For scientific content, generated diagrams and proposed structures should be validated against authoritative domain knowledge before educational, research, or professional use.

---

## Choosing the right generative paradigm

| Goal | Good starting point from this chapter |
|---|---|
| Controlled class generation | cGAN / CVAE |
| Stable interpretable latent space | CVAE |
| Highest GAN-style visual sharpness | cGAN / StyleGAN family |
| Paired image translation | Pix2Pix |
| Unpaired domain translation | CycleGAN |
| Synthetic face generation/control | StyleGAN |
| Blind face restoration | GFPGAN |
| Learn generative denoising process | DDPM |
| Efficient high-resolution diffusion | Latent diffusion |
| Text-to-image | Stable Diffusion / SDXL / hosted image model |
| Edit image using language | InstructPix2Pix / multimodal image editor |
| Preserve explicit geometry | ControlNet |
| Preserve reference appearance + control pose | IP-Adapter + ControlNet |
| Fill selected region | Inpainting |
| Fast interactive diffusion | Distilled/Turbo diffusion |
| Analyze image and return text/JSON | Vision-language model |
| Classical structural control + generative appearance | Hybrid CV + generative editing |

{{exercise:M13.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Generative AI means only text-to-image generation.

### Why this is wrong

The chapter includes conditional generation, translation, restoration, editing, inpainting, super-resolution, multimodal understanding, and structured visual analysis.

### Misconception 2

> A cGAN generator alone decides whether an image matches the requested class.

### Why this is wrong

The source conditions both generator and discriminator; the projection discriminator explicitly evaluates image-label compatibility.

### Misconception 3

> CVAE latent sampling prevents backpropagation.

### Why this is wrong

The reparameterization trick separates randomness from differentiable distribution parameters.

### Misconception 4

> Pix2Pix and CycleGAN require the same kind of training data.

### Why this is wrong

Pix2Pix is paired; CycleGAN is designed for unpaired domains.

### Misconception 5

> Latent interpolation is just pixel blending.

### Why this is wrong

The interpolation happens in a learned representation and is decoded through the generator.

### Misconception 6

> GFPGAN can prove the exact original appearance of a degraded face.

### Why this is wrong

A generative prior reconstructs plausible facial detail; exact historical recovery is not guaranteed.

### Misconception 7

> Diffusion generates an image in one neural-network pass.

### Why this is wrong

Standard DDPM-style generation is an iterative reverse-denoising process.

### Misconception 8

> Latent diffusion and pixel-space diffusion require the same computational scale.

### Why this is wrong

Latent diffusion works on a compressed representation, dramatically reducing the number of values being denoised.

### Misconception 9

> Stable Diffusion is only a U-Net.

### Why this is wrong

The chapter's pipeline combines a text encoder, VAE, denoising U-Net, and scheduler.

### Misconception 10

> Text prompts alone provide exact geometric control.

### Why this is wrong

ControlNet exists specifically to inject explicit structural constraints such as edges, depth, masks, or poses.

### Misconception 11

> IP-Adapter and ControlNet solve the same conditioning problem.

### Why this is wrong

IP-Adapter provides reference-image appearance information; ControlNet provides structural/geometry constraints.

### Misconception 12

> A diffusion super-resolution model simply interpolates existing pixels.

### Why this is wrong

The source describes it as generating plausible high-frequency detail.

### Misconception 13

> Inpainting recovers hidden pixels with certainty.

### Why this is wrong

It synthesizes a plausible completion from context and priors.

### Misconception 14

> Vision understanding models and image-generation models are the same component.

### Why this is wrong

The source distinguishes multimodal language models for analysis from specialized image-generation/editing models.

### Misconception 15

> Generated scientific or medical outputs can be accepted without expert verification.

### Why this is wrong

The source explicitly keeps medical use non-diagnostic and states that expert review remains essential.

---

## Key terminology

| Term | Meaning |
|---|---|
| Generative model | Model that learns a data distribution and can produce new samples |
| Latent variable | Compact hidden representation controlling generated content |
| GAN | Generator-discriminator adversarial framework |
| cGAN | GAN conditioned on labels/attributes/text |
| Projection discriminator | Discriminator using feature-condition compatibility score |
| Spectral normalization | Weight normalization used to stabilize adversarial training |
| EMA | Exponential Moving Average of model parameters |
| FID | Feature-distribution distance between real and generated images |
| VAE | Probabilistic encoder-decoder latent-variable model |
| CVAE | VAE conditioned on class/attribute information |
| Reparameterization trick | Differentiable latent sampling formulation |
| KL divergence | Distribution mismatch term used in VAE regularization |
| Pix2Pix | Paired image-to-image translation framework |
| CycleGAN | Unpaired image-to-image translation with cycle consistency |
| Cycle consistency | Requirement that translating there and back reconstructs the source |
| StyleGAN | Style-based high-fidelity generator |
| GAN inversion | Mapping a real image into a generator's latent representation |
| GFPGAN | Generative facial-prior restoration system |
| DDPM | Denoising Diffusion Probabilistic Model |
| Forward diffusion | Progressive addition of noise |
| Reverse diffusion | Learned progressive denoising |
| Scheduler | Component controlling diffusion timesteps/update equations |
| Latent diffusion | Diffusion performed in a compressed learned latent space |
| VAE decoder | Module reconstructing an image from latent representation |
| Stable Diffusion | Text-conditioned latent diffusion framework |
| InstructPix2Pix | Instruction-conditioned diffusion image editor |
| ControlNet | Structural conditioning network for diffusion |
| SDXL | Larger Stable Diffusion family model |
| Distillation | Training a faster model/process from a slower generative process |
| IP-Adapter | Visual-reference conditioning adapter for diffusion |
| OpenPose control | Human-pose skeletal signal used for structural conditioning |
| Inpainting | Generating/replacing content inside a selected region |
| Image-to-image | Generation conditioned on an existing source image |
| VQA | Visual Question Answering |
| Multimodal model | Model operating across multiple data types such as text and images |
| Structured output | Model output constrained to fields such as JSON/table schema |
| Hybrid CV workflow | Combining deterministic image-processing signals with generative models |

---

## Self-check

Before continuing, make sure you can answer:

1. What distinguishes generative vision from classification/detection?
2. What are the generator and discriminator trying to learn?
3. Why is conditioning useful in a GAN?
4. What does a projection discriminator add?
5. Why use spectral normalization?
6. Why keep an EMA generator?
7. What does lower FID generally indicate?
8. What are the three main components of a CVAE?
9. Why is the reparameterization trick necessary?
10. What does the KL term encourage?
11. Why can CVAE outputs be smoother than GAN outputs?
12. What is the difference between cross-class and within-class latent traversal?
13. Why does Pix2Pix need aligned pairs?
14. What does CycleGAN's cycle-consistency loss enforce?
15. What do StyleGAN's early versus later synthesis layers tend to control?
16. What is GAN inversion?
17. Why can StyleGANEX edit real images after inversion?
18. What prior does GFPGAN exploit?
19. Why should generative restoration not be treated as exact historical recovery?
20. What happens during forward diffusion?
21. What does the reverse model predict?
22. Why can standard diffusion sampling be slow?
23. Why is latent diffusion cheaper?
24. What role does the VAE play in Stable Diffusion?
25. What role does the text encoder play?
26. What role does the scheduler play?
27. How does InstructPix2Pix differ from pure text-to-image?
28. What problem does ControlNet solve?
29. What kind of information does a Canny control image preserve?
30. Why can SDXL-style image-to-image refinement preserve composition?
31. Why is diffusion-based super-resolution not equivalent to bicubic interpolation?
32. What information does an inpainting mask provide?
33. What does IP-Adapter contribute?
34. What does OpenPose/ControlNet contribute?
35. Why is combining reference and pose controls useful?
36. What criteria can be used to compare hosted image generators?
37. Why should API-specific code from a book be version-checked?
38. What is the difference between image understanding and image generation?
39. How can OpenCV/Canny improve control in a generative editing workflow?
40. What is the difference between explicit-mask editing and prompt-only local editing?
41. Why can object removal hallucinate unseen background?
42. What is multi-image composition?
43. How can a vision model support an industrial inspection workflow?
44. Why is structured JSON useful for inspection/change reports?
45. How can two satellite images be compared with a multimodal model?
46. Why should remote-sensing qualitative interpretation be separated from exact geospatial measurement?
47. Why should medical-image multimodal analysis remain non-diagnostic without expert review?
48. What is an image→reasoning→image workflow?
49. Which chapter method would you use for paired translation?
50. Which method would you choose for unpaired translation?
51. Which method would you choose when explicit pose control is required?
52. Which method would you choose for large-scale text-conditioned latent generation?
53. What is the broad trade-off between control and generative freedom?
54. Why is verification increasingly important as a generative model is allowed to invent more content?

---

## Retain this idea

**Generative computer vision is fundamentally about learning a visual distribution and then controlling how we sample or transform it. GANs introduced adversarial realism, VAEs introduced structured probabilistic latent spaces, diffusion introduced iterative denoising, latent diffusion made high-resolution synthesis practical, and modern multimodal systems combine text, images, geometry, and reference signals into increasingly controllable visual workflows.**
        """,

        "estimated_minutes": 480,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "generative-mental-model", "title": "From Understanding Images to Generating Them", "order": 1},
            {"id": "cgan", "title": "Conditional GANs: Generation Through Competition", "order": 2},
            {"id": "cvae", "title": "Conditional VAE: A Probabilistic Latent Space", "order": 3},
            {"id": "latent-traversal", "title": "Latent Interpolation and Semantic Manifolds", "order": 4},
            {"id": "pix2pix-cyclegan", "title": "Pix2Pix and CycleGAN: Translating Visual Domains", "order": 5},
            {"id": "stylegan", "title": "StyleGAN: High-Fidelity Synthesis and Semantic Control", "order": 6},
            {"id": "gfpgan", "title": "GFPGAN: Generative Priors for Face Restoration", "order": 7},
            {"id": "ddpm", "title": "DDPMs: Generation by Learning to Remove Noise", "order": 8},
            {"id": "latent-diffusion", "title": "Latent Diffusion: Denoise a Compressed Image Representation", "order": 9},
            {"id": "stable-diffusion", "title": "Stable Diffusion: Text-Conditioned Latent Denoising", "order": 10},
            {"id": "instructpix2pix", "title": "InstructPix2Pix: Edit an Existing Image with Language", "order": 11},
            {"id": "controlnet", "title": "ControlNet: Separate Semantic Intent from Geometry", "order": 12},
            {"id": "sdxl-applications", "title": "Practical Stable Diffusion and SDXL Workflows", "order": 13},
            {"id": "ipadapter-controlnet", "title": "IP-Adapter + ControlNet: Appearance and Pose as Separate Controls", "order": 14},
            {"id": "dalle-source-comparison", "title": "DALL·E 2 and DALL·E 3 in the Source Chapter", "order": 15},
            {"id": "multimodal-image-apis", "title": "Unified Multimodal Workflows: Understanding and Editing", "order": 16},
            {"id": "hybrid-editing", "title": "Hybrid Classical Computer Vision + Generative Editing", "order": 17},
            {"id": "gpt-image-applications", "title": "Generative Editing Applications in the Source", "order": 18},
            {"id": "vision-applications", "title": "Vision-Language Analysis: VQA, Inspection, Remote Sensing, and Medical Education", "order": 19},
            {"id": "chemistry-capstone", "title": "Scientific Visual Generation and the Chapter Capstone", "order": 20},
        ],
    },

    "exercises": [
        {
            "id": "M13.L01.EX01",

            "title": "Compare Conditional and Latent Generative Models",

            "lesson_code": "M13.L01",

            "section_id": "latent-diffusion",

            "placement": "after_section",

            "description": (
                "Build conceptual and practical intuition for conditioning, latent structure, "
                "translation, and diffusion by comparing several generative paradigms."
            ),

            "instructions": (
                "1. Choose a small dataset such as Fashion-MNIST or another simple labeled image set.\n"
                "2. For a cGAN or conceptual cGAN implementation, identify exactly where the "
                "class condition enters the generator and discriminator.\n"
                "3. For a CVAE, plot or inspect the latent mean vectors and explain the role of "
                "reconstruction and KL terms.\n"
                "4. Perform at least one latent interpolation and describe whether the transition "
                "appears smooth and semantically meaningful.\n"
                "5. Compare paired and unpaired image translation using Pix2Pix/CycleGAN examples "
                "from the source or pretrained models.\n"
                "6. Visualize several steps from a DDPM forward or reverse diffusion process.\n"
                "7. Compare pixel-space diffusion with latent diffusion conceptually in terms of "
                "representation size and computational cost.\n"
                "8. Build a comparison table for cGAN, CVAE, CycleGAN, DDPM, and latent diffusion "
                "covering training objective, conditioning, strengths, and failure modes.\n"
                "9. Explain which method you would select for class-controlled generation, smooth "
                "latent exploration, unpaired translation, and high-resolution text-conditioned generation."
            ),

            "expected_output": (
                "A notebook/report containing latent/conditional diagrams, at least one interpolation, "
                "a diffusion trajectory visualization, and a comparison table explaining how the "
                "learning objective changes the behavior of each model family."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "conditional-generation",
                "cgan",
                "cvae",
                "latent-interpolation",
                "cyclegan",
                "ddpm",
                "latent-diffusion",
                "model-comparison",
            ],
        },

        {
            "id": "M13.L01.EX02",

            "title": "Design a Controlled Multimodal Image Workflow",

            "lesson_code": "M13.L01",

            "section_id": "chemistry-capstone",

            "placement": "after_section",

            "description": (
                "Design a complete image-generation/editing system that clearly separates semantic, "
                "structural, reference, region, and reasoning controls."
            ),

            "instructions": (
                "1. Choose one application: product visualization, photo restoration, scientific "
                "illustration, fashion/avatar generation, industrial inspection, or remote sensing.\n"
                "2. Define the input sources: text prompt, input image, mask, edge/depth/pose map, "
                "reference image, or multiple images.\n"
                "3. Select a source-aligned model family for each requirement: Stable Diffusion/SDXL, "
                "InstructPix2Pix, ControlNet, IP-Adapter, multimodal vision, or image editing.\n"
                "4. Draw the full information flow from inputs to output.\n"
                "5. Include at least one explicit structural control if geometry must be preserved.\n"
                "6. Include an explicit mask when only one region should be regenerated, where appropriate.\n"
                "7. If a vision-language component is used, require a structured intermediate output "
                "such as a checklist or JSON schema before generation/editing.\n"
                "8. Add one verification stage comparing the output with source constraints such as "
                "identity, geometry, text content, region preservation, or scientific correctness.\n"
                "9. List at least three failure modes, including one hallucination/fidelity failure.\n"
                "10. State which parts are deterministic classical CV, learned understanding, "
                "generative synthesis, and human/expert validation."
            ),

            "expected_output": (
                "A system diagram and short report specifying conditioning signals, model stages, "
                "verification checks, failure modes, and the boundary between generated plausibility "
                "and trusted/verified information."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "stable-diffusion",
                "controlnet",
                "ip-adapter",
                "inpainting",
                "multimodal-vision",
                "hybrid-computer-vision",
                "verification",
                "system-design",
            ],
        },
    ],

    "quiz": {
        "id": "M13.L01.QZ01",

        "title": "Generative AI in Image Processing and Computer Vision — Knowledge Check",

        "lesson_code": "M13.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M13.L01.Q01",
                "section_id": "cgan",
                "question": "What makes a GAN conditional?",
                "options": [
                    "Generation and/or discrimination receive an additional condition such as a label",
                    "The generator receives no input",
                    "The discriminator is removed",
                    "Only PCA is used",
                ],
                "correct": 0,
                "explanation": (
                    "Conditioning lets the model control which type of image is generated."
                ),
            },

            {
                "id": "M13.L01.Q02",
                "section_id": "cgan",
                "question": "What is the purpose of a projection term in the source's discriminator?",
                "options": [
                    "Measure compatibility between image features and the supplied condition",
                    "Perform image upscaling",
                    "Create a diffusion schedule",
                    "Compute OCR text",
                ],
                "correct": 0,
                "explanation": (
                    "The projection term lets the discriminator judge both realism and condition agreement."
                ),
            },

            {
                "id": "M13.L01.Q03",
                "section_id": "cvae",
                "question": "Why does a VAE use the reparameterization trick?",
                "options": [
                    "To make stochastic latent sampling compatible with gradient-based learning",
                    "To remove the decoder",
                    "To make every image sharper than a GAN",
                    "To compute FID",
                ],
                "correct": 0,
                "explanation": (
                    "It rewrites sampling using differentiable distribution parameters plus external noise."
                ),
            },

            {
                "id": "M13.L01.Q04",
                "section_id": "pix2pix-cyclegan",
                "question": "What training data does CycleGAN remove the need for?",
                "options": [
                    "Aligned source-target image pairs",
                    "Any images at all",
                    "Two visual domains",
                    "A discriminator",
                ],
                "correct": 0,
                "explanation": (
                    "CycleGAN learns from separate unpaired collections and uses cycle consistency."
                ),
            },

            {
                "id": "M13.L01.Q05",
                "section_id": "stylegan",
                "question": "What is GAN inversion?",
                "options": [
                    "Finding a latent representation that reconstructs a real input image",
                    "Running the discriminator backward to classify text",
                    "Adding Gaussian noise to an image",
                    "Converting RGB to grayscale",
                ],
                "correct": 0,
                "explanation": (
                    "Inversion maps a real image into a generator-compatible latent representation for reconstruction/editing."
                ),
            },

            {
                "id": "M13.L01.Q06",
                "section_id": "gfpgan",
                "question": "What additional knowledge does GFPGAN use beyond degraded pixels?",
                "options": [
                    "A learned generative prior for realistic facial structure",
                    "Only a Canny edge map",
                    "Only an OCR language model",
                    "Only a histogram",
                ],
                "correct": 0,
                "explanation": (
                    "GFPGAN constrains restoration with a pretrained facial generative manifold."
                ),
            },

            {
                "id": "M13.L01.Q07",
                "section_id": "ddpm",
                "question": "What does a DDPM learn during reverse diffusion?",
                "options": [
                    "How to predict/remove noise from a noisy sample",
                    "A single direct latent-to-image mapping only",
                    "Only class labels",
                    "Only a JPEG decoder",
                ],
                "correct": 0,
                "explanation": (
                    "The denoiser estimates noise so the scheduler can move toward a cleaner sample."
                ),
            },

            {
                "id": "M13.L01.Q08",
                "section_id": "latent-diffusion",
                "question": "Why is latent diffusion computationally cheaper than pixel-space diffusion?",
                "options": [
                    "The denoising process operates on a much smaller compressed representation",
                    "It removes all neural networks",
                    "It requires no sampling",
                    "It stores only text",
                ],
                "correct": 0,
                "explanation": (
                    "The VAE compresses images before iterative denoising."
                ),
            },

            {
                "id": "M13.L01.Q09",
                "section_id": "stable-diffusion",
                "question": "Which component converts the text prompt into conditioning information in the source's Stable Diffusion explanation?",
                "options": [
                    "Text encoder",
                    "VAE decoder",
                    "FID metric",
                    "Projection discriminator",
                ],
                "correct": 0,
                "explanation": (
                    "The text encoder creates the semantic embedding used to condition denoising."
                ),
            },

            {
                "id": "M13.L01.Q10",
                "section_id": "instructpix2pix",
                "question": "What distinguishes InstructPix2Pix from ordinary text-to-image generation?",
                "options": [
                    "It edits an existing image using a natural-language instruction",
                    "It cannot use text",
                    "It uses only a discriminator",
                    "It always requires paired Fashion-MNIST data",
                ],
                "correct": 0,
                "explanation": (
                    "The source image is part of the conditioning, so the task is transformation rather than generation from scratch."
                ),
            },

            {
                "id": "M13.L01.Q11",
                "section_id": "controlnet",
                "question": "What problem does ControlNet primarily address?",
                "options": [
                    "Precise structural control of diffusion generation",
                    "GAN mode collapse",
                    "Face recognition",
                    "Federated averaging",
                ],
                "correct": 0,
                "explanation": (
                    "It injects edges, poses, depth, masks, or other geometry into the denoising process."
                ),
            },

            {
                "id": "M13.L01.Q12",
                "section_id": "sdxl-applications",
                "question": "How does diffusion-based super-resolution differ from fixed bicubic interpolation?",
                "options": [
                    "It can synthesize plausible high-frequency detail using a learned generative prior",
                    "It simply copies every fourth pixel",
                    "It cannot change image dimensions",
                    "It requires only a histogram",
                ],
                "correct": 0,
                "explanation": (
                    "The source describes learned generative upscaling rather than a fixed interpolation kernel."
                ),
            },

            {
                "id": "M13.L01.Q13",
                "section_id": "ipadapter-controlnet",
                "question": "What is the division of responsibility in the source's IP-Adapter + ControlNet example?",
                "options": [
                    "IP-Adapter supplies reference appearance while ControlNet supplies pose/structure",
                    "Both only compute FID",
                    "ControlNet supplies identity while IP-Adapter computes OCR",
                    "Neither uses an input image",
                ],
                "correct": 0,
                "explanation": (
                    "The combination separates visual identity/appearance guidance from geometric guidance."
                ),
            },

            {
                "id": "M13.L01.Q14",
                "section_id": "dalle-source-comparison",
                "question": "What is a robust way to compare two hosted image generators according to the source experiment?",
                "options": [
                    "Use the same prompt set and compare prompt fidelity, composition, coherence, typography, and diversity",
                    "Compare only file size",
                    "Use a different prompt for each model",
                    "Evaluate only one generated image",
                ],
                "correct": 0,
                "explanation": (
                    "Controlled prompts make qualitative model differences easier to interpret."
                ),
            },

            {
                "id": "M13.L01.Q15",
                "section_id": "multimodal-image-apis",
                "question": "What is the conceptual difference between image understanding and image generation?",
                "options": [
                    "Understanding maps visual input to analysis/text; generation creates or modifies visual output",
                    "They are always the same network operation",
                    "Understanding requires no image",
                    "Generation only classifies images",
                ],
                "correct": 0,
                "explanation": (
                    "The source treats reasoning/description and image synthesis/editing as complementary capabilities."
                ),
            },

            {
                "id": "M13.L01.Q16",
                "section_id": "hybrid-editing",
                "question": "Why combine Canny edges with a generative editor?",
                "options": [
                    "Classical CV supplies precise structure while the generative model supplies rich appearance synthesis",
                    "To eliminate all image conditioning",
                    "To compute a class label only",
                    "To perform PCA",
                ],
                "correct": 0,
                "explanation": (
                    "Hybrid workflows combine deterministic geometric information with generative flexibility."
                ),
            },

            {
                "id": "M13.L01.Q17",
                "section_id": "gpt-image-applications",
                "question": "Why should object removal be treated as generative rather than factual recovery?",
                "options": [
                    "The model must synthesize plausible pixels for content hidden behind the removed object",
                    "It always retrieves the exact background from a database",
                    "The hidden pixels are stored in the mask",
                    "No pixels are changed",
                ],
                "correct": 0,
                "explanation": (
                    "The model infers a plausible completion from context and learned priors."
                ),
            },

            {
                "id": "M13.L01.Q18",
                "section_id": "vision-applications",
                "question": "Why can structured JSON be useful for industrial or remote-sensing visual analysis?",
                "options": [
                    "It converts free-form visual reasoning into fields that downstream software can parse and validate",
                    "It guarantees every visual claim is correct",
                    "It removes the need for images",
                    "It replaces model inference",
                ],
                "correct": 0,
                "explanation": (
                    "Structured output makes reports easier to integrate into applications, while still requiring validation."
                ),
            },

            {
                "id": "M13.L01.Q19",
                "section_id": "chemistry-capstone",
                "question": "What is an image→reasoning→image workflow?",
                "options": [
                    "Analyze a visual input, form a textual/structured interpretation, then generate a new visual output",
                    "Only resize an image twice",
                    "Train a classifier from scratch",
                    "Apply one convolution kernel",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter's scientific examples combine multimodal analysis with generative visualization."
                ),
            },

            {
                "id": "M13.L01.Q20",
                "section_id": "chemistry-capstone",
                "type": "open",
                "question": (
                    "Design a controlled generative workflow for one of these tasks: restore "
                    "an old photo, create a pose-guided product/fashion image, generate a "
                    "scientific educational illustration, or edit one object inside a scene. "
                    "Identify every conditioning signal, explain which model family handles "
                    "each stage, state what information must be preserved, and describe how "
                    "you would verify that generated content is plausible without treating "
                    "it as automatically factual."
                ),
            },
        ],

        "passing_score": 70,
    },
}
