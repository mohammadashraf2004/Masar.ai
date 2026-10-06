"""M08.L01 — Image Enhancements Using Derivatives.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 8. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M08.L01"

MODULE_ORDER = 8

MODULE_TITLE = "Image Enhancements Using Derivatives"

MODULE_DESCRIPTION = (
    "Learn how first- and second-order image derivatives support sharpening, edge "
    "detection, blur assessment, scale-space analysis, ridge detection, structured "
    "and learned edge detection, edge-preserving diffusion, and multiscale enhancement "
    "with Gaussian and Laplacian pyramids."
)

SOURCE_CHAPTER = 8

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


TOPIC = {
    "title": "Image Enhancements Using Derivatives",

    "slug": "image-processing-m08-l01",

    "description": (
        "A practical lesson on gradients, Laplacians, unsharp masking, entropy-based "
        "enhancement, Sobel/Prewitt/Scharr/Roberts/Kirsch/Canny detectors, LoG/DoG and "
        "zero crossings, scale-space blob detection, Hessian ridge filters, structured "
        "edges, guided filtering, anisotropic diffusion, HED/PiDiNet, and Gaussian/"
        "Laplacian pyramids for multiscale enhancement and blending."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 6.0,

    "skill_tags": [
        "image-processing",
        "image-derivatives",
        "gradient",
        "laplacian",
        "blur-detection",
        "unsharp-masking",
        "entropy-enhancement",
        "sobel",
        "prewitt",
        "scharr",
        "roberts",
        "kirsch",
        "canny",
        "log",
        "dog",
        "zero-crossing",
        "blob-detection",
        "hessian",
        "ridge-detection",
        "structured-edges",
        "guided-filter",
        "anisotropic-diffusion",
        "hed",
        "pidinet",
        "gaussian-pyramid",
        "laplacian-pyramid",
        "module-08",
    ],

    "prerequisite_ids": ["M07.L01"],

    "lesson": {
        "title": "Image Enhancements Using Derivatives",

        "content": r"""
# Image Enhancements Using Derivatives

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M08.L01  
> **Module:** Image Enhancements Using Derivatives  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 8. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain first-order partial derivatives, gradient magnitude, and gradient direction.
- Explain why strong derivative responses often indicate edges.
- Distinguish the vector gradient from the scalar Laplacian.
- Explain why second-order derivatives are especially sensitive to noise.
- Use Laplacian variance as a simple no-reference blur indicator.
- Explain and implement unsharp masking.
- Describe entropy-based gamma optimization for contrast enhancement.
- Compare Sobel, Prewitt, Scharr, Roberts, Laplacian, and Kirsch edge operators.
- Explain percentile-gradient edge detection and why rank statistics can improve robustness.
- Describe every stage of the Canny edge detector.
- Explain LoG, DoG, zero-crossing edge detection, and scale-space.
- Compare LoG, DoG, and DoH blob detection.
- Explain ridge detection from Hessian eigenvalues and compare Meijering, Sato, Frangi, and Hessian filters.
- Explain structured edge detection and the purpose of orientation-aware non-maximum suppression.
- Explain guided filtering and Perona–Malik anisotropic diffusion as edge-preserving operations.
- Compare HED and PiDiNet as learned edge detectors.
- Explain Gaussian and Laplacian pyramids, multiscale detail enhancement, reconstruction, and pyramid blending.
- Choose an edge detector according to noise, geometry, scale, semantic requirements, and computational constraints.

---

## 1. From intensity change to image derivatives

An image can be modeled as an intensity function:

```text
I(x, y)
```

An edge is often associated with a rapid change in this function.

Digital images are discrete, so derivatives are approximated with **finite differences**.

A simple forward difference along `x` is:

```text
dI/dx ≈ I(x+1, y) - I(x, y)
```

and similarly along `y`.

These differences can be implemented as convolution kernels.

For example:

```python
ker_x = [[-1, 1]]

ker_y = [
    [-1],
    [ 1],
]
```

### Gradient vector

The first-order partial derivatives form a gradient:

```text
∇I = [Ix, Iy]
```

The gradient has both:

- magnitude,
- direction.

Magnitude:

```text
|∇I| = sqrt(Ix^2 + Iy^2)
```

Direction:

```text
theta = atan(Iy / Ix)
```

The source uses a small epsilon in the denominator to avoid division by zero.

A more numerically convenient implementation in general is to use an angle function designed for two components, but the key source concept is the same: the gradient direction describes how intensity changes spatially.

{{image:image-gradient-geometry}}

### Why gradients reveal edges

In a smooth region:

```text
neighboring intensities ≈ similar
-> derivative ≈ small
```

At a sharp transition:

```text
neighboring intensities differ strongly
-> derivative magnitude becomes large
```

Therefore, peaks in gradient magnitude are strong candidates for edges.

[[IMAGE_NEEDED: Image profile and first derivative | Show a 1D row through alternating dark/bright image regions, the corresponding intensity profile, and derivative spikes at transitions | Learner should see why edges appear as peaks in first-order derivatives]]

### Gradient orientation

The gradient points in the direction of strongest intensity increase.

Its direction is perpendicular to the local edge orientation.

That distinction matters later for:

- non-maximum suppression,
- directional filters,
- edge thinning.

---

## 2. The Laplacian, blur detection, and noise sensitivity

The Laplacian combines second-order derivatives:

```text
∇²I = Ixx + Iyy
```

A common discrete kernel is:

```python
laplacian_kernel = [
    [ 0, -1,  0],
    [-1,  4, -1],
    [ 0, -1,  0],
]
```

{{image:first-second-derivatives-zero-crossing}}

### Gradient versus Laplacian

| Property | Gradient | Laplacian |
|---|---|---|
| Derivative order | first | second |
| Output type | vector | scalar |
| Direction | available | lost |
| Typical edge cue | magnitude peaks | zero crossings / strong second-order response |
| Noise sensitivity | high | even higher |

The source emphasizes that the Laplacian is isotropic/rotation-invariant in its basic form.

### Zero crossings

A sharp transition can create:

```text
first derivative -> peak/valley
second derivative -> sign change
```

The location where the second derivative changes sign is a **zero crossing**.

Later, LoG edge detection uses this directly.

### Blur detection with variance of Laplacian

Blur suppresses high-frequency detail.

The Laplacian responds strongly to sharp structure.

So a simple sharpness score is:

```python
import cv2

def variance_of_laplacian(gray):
    lap = cv2.Laplacian(
        gray,
        cv2.CV_64F,
    )
    return lap.var()
```

Interpretation:

```text
high variance -> more sharp variation
low variance  -> smoother / potentially blurrier
```

The chapter gives heuristic threshold examples, but also states that the correct threshold depends on:

- content,
- image size,
- application.

So it should not be treated as a universal sharp/blurry boundary.

[[IMAGE_NEEDED: Laplacian variance blur comparison | Show the same image as original, box-blurred, and Gaussian-blurred, with the Laplacian response and variance score beneath each | Learner should understand why blur reduces derivative energy]]

### Why derivatives amplify noise

Noise can create rapid pixel-to-pixel intensity changes.

A derivative cannot inherently know whether the change comes from:

- a real edge,
- noise.

As noise increases, derivative responses become crowded with false peaks.

This motivates:

```text
smooth first
then differentiate
```

which leads naturally to LoG and Canny.

---

## 3. Classical derivative-based enhancement

### Unsharp masking

Despite its name, unsharp masking is used for sharpening.

The logic is:

```text
detail = original - blurred

sharpened =
original + amount * detail
```

Equivalently:

```text
sharpened =
(1 + amount) * original
- amount * blurred
```

With OpenCV:

```python
blurred = cv2.GaussianBlur(
    image,
    (0, 0),
    sigmaX=2,
)

alpha = 1.5

sharpened = cv2.addWeighted(
    image,
    1 + alpha,
    blurred,
    -alpha,
    0,
)
```

Pillow also provides an `UnsharpMask` with parameters for:

- blur radius,
- sharpening percentage,
- threshold.

The threshold helps avoid amplifying tiny changes in nearly flat regions.

[[IMAGE_NEEDED: Unsharp masking pipeline | Show original image, blurred image, extracted high-frequency detail layer (original minus blur), and sharpened result | Learner should see sharpening as adding back amplified detail]]

### Entropy-based gamma enhancement

The chapter also optimizes gamma by maximizing image entropy.

Gamma mapping:

```text
output = input^gamma
```

for normalized pixels.

The entropy of an intensity distribution is:

```text
H = -sum(p_i * log2(p_i))
```

The procedure is:

1. normalize the image,
2. choose a candidate gamma,
3. transform the image,
4. compute histogram entropy,
5. optimize gamma to maximize entropy.

With `scipy.optimize.minimize_scalar`, the implementation minimizes **negative entropy**.

The source notes that dark/low-contrast inputs often yield an optimal gamma below `1`, which brightens darker values.

### Important caution

Higher entropy can indicate a richer intensity distribution, but it is not automatically equivalent to "better" visual quality in every application.

The chapter uses it as a principled optimization target for this enhancement example.

---

## 4. Sobel, Prewitt, Roberts, Scharr, and Laplacian

Several classical edge detectors approximate image derivatives.

### Sobel

Sobel uses directional kernels to estimate horizontal and vertical change.

With scikit-image:

```python
from skimage import filters

edges_h = filters.sobel_h(image)
edges_v = filters.sobel_v(image)
edges = filters.sobel(image)
```

The combined Sobel response represents gradient magnitude.

### Prewitt

Prewitt is another first-order gradient approximation.

It is simple and efficient.

### Roberts

Roberts uses small diagonal difference kernels.

It responds to rapid local transitions with a very compact neighborhood.

### Scharr

The source highlights Scharr as having lower rotational variance than Sobel for gradient estimation.

### Laplacian

Laplacian is a second-order detector rather than a first-order directional gradient operator.

The chapter compares all of these on the same image.

[[IMAGE_NEEDED: Classical edge detector comparison | Show one grayscale scene beside Roberts, Prewitt, Sobel, Scharr, and Laplacian edge responses | Learner should compare edge thickness, directional sensitivity, and noise response rather than memorizing kernel names]]

### No single operator is always best

The practical choice depends on:

- noise,
- desired edge localization,
- orientation sensitivity,
- computation budget,
- downstream use.

---

## 5. Directional and percentile-gradient edge detection

### Kirsch compass operator

Real edges may appear at arbitrary orientations.

Kirsch addresses this by using eight directional kernels:

```text
N, NE, E, SE, S, SW, W, NW
```

Each kernel produces one response map.

Then:

```text
final response at pixel
=
maximum response across directions
```

This allows the detector to emphasize the strongest local orientation.

[[IMAGE_NEEDED: Kirsch compass edge detector | Show the eight compass directions around a central pixel, representative Kirsch masks, and a final map formed by taking the maximum directional response | Learner should understand multi-orientation edge detection]]

### Percentile gradient

A different strategy uses local rank statistics instead of fixed derivative weights.

Inside a neighborhood:

```text
gradient_percentile
=
upper_percentile
-
lower_percentile
```

For example:

```text
90th percentile - 10th percentile
```

This captures meaningful local intensity range while being less affected by minor fluctuations or isolated outliers.

A larger footprint:

- considers more context,
- smooths fine variation,
- detects broader local contrast.

A smaller footprint:

- reacts more strongly to fine detail.

### Interactive exploration

The supplied chapter text contains a Gradio interface for interactively changing:

- neighborhood radius,
- lower percentile,
- upper percentile,

and visualizing the resulting percentile-gradient edge map.

The chapter's opening/summary also describes interactive Canny experimentation; in the supplied code excerpt, the explicit Gradio implementation shown is for the percentile-gradient detector.

This is a useful engineering pattern:

```text
algorithm parameters
      ↓
interactive sliders
      ↓
immediate visual feedback
```

---

## 6. Canny edge detection

Canny combines several ideas into one carefully designed pipeline.

### Step 1: smoothing

Edge detection is noise-sensitive.

Canny starts with Gaussian smoothing.

### Step 2: gradient magnitude and orientation

Directional derivatives are computed, commonly with Sobel-like operators.

For each pixel we estimate:

- edge strength,
- gradient direction.

### Step 3: non-maximum suppression

Raw gradient responses are often thick.

A true edge should be locally strongest **across the edge direction**.

Non-maximum suppression keeps a pixel only when it is a local maximum along the gradient direction.

Result:

- thinner,
- better-localized candidate edges.

### Step 4: double threshold and hysteresis

Two thresholds are used:

```text
high threshold
low threshold
```

Pixels are categorized as:

- strong edges,
- weak candidates,
- non-edges.

A weak candidate is retained only if it is connected to a strong edge.

This helps reject isolated noise while preserving connected contours.

[[IMAGE_NEEDED: Canny four-stage pipeline | Show noisy/grayscale input, Gaussian-smoothed image, gradient magnitude/orientation, non-maximum-suppressed thin edges, and final hysteresis-linked edge map | Learner should understand that Canny is a pipeline, not just one convolution kernel]]

### Effect of smoothing scale

The source shows that a smaller Gaussian `sigma` preserves finer structures and therefore tends to produce more edges.

A larger `sigma` removes more small variation before edge extraction.

---

## 7. LoG, DoG, and zero-crossing edge detection

Second-order derivatives are extremely sensitive to noise.

So the chapter combines:

```text
Gaussian smoothing
+
Laplacian
```

to form the **Laplacian of Gaussian (LoG)**.

By associativity of convolution, the two stages can be represented as one LoG kernel.

### Difference of Gaussians (DoG)

DoG subtracts two Gaussian responses at different scales:

```text
DoG =
Gaussian(sigma_1)
-
Gaussian(sigma_2)
```

The chapter presents DoG as an efficient approximation to LoG.

Because the two Gaussian low-pass responses differ by scale, their subtraction emphasizes an intermediate frequency band.

### LoG as a scale-space operator

Using increasing `sigma`:

```text
small sigma -> small/fine structures
large sigma -> larger/coarser structures
```

So one detector can be applied across scales.

### Marr–Hildreth zero crossings

After LoG filtering, edges are detected by sign changes.

A simple local rule is:

```text
if current pixel and any neighbor have opposite signs:
    mark edge
```

This identifies zero-crossing contours.

[[IMAGE_NEEDED: LoG DoG and zero crossings | Show Gaussian smoothing, LoG kernel/response, DoG approximation, and binary zero-crossing edge contours | Learner should connect smoothing, second derivative, and sign changes]]

The source notes that zero-crossing boundaries form closed contours.

---

## 8. Scale-space blob detection with LoG, DoG, and DoH

An edge is not the only useful derivative structure.

A **blob** is a region that differs from its surroundings in intensity or texture.

Objects appear at different sizes, so a single detector scale is insufficient.

### Scale space

Create representations at multiple smoothing scales:

```text
small sigma -> fine features
large sigma -> larger structures
```

Then search for extrema across:

- position,
- scale.

### LoG blob detection

`blob_log()` uses Laplacian-of-Gaussian responses across scales.

The source describes it as accurate but computationally more expensive.

### DoG blob detection

`blob_dog()` uses Difference of Gaussians as a faster LoG approximation.

The chapter notes the connection to SIFT-style scale-space processing.

### Determinant of Hessian (DoH)

The Hessian matrix contains second-order derivatives:

```text
H = [
 Ixx  Ixy
 Ixy  Iyy
]
```

Its determinant is:

```text
det(H) = Ixx * Iyy - Ixy^2
```

Large responses can indicate strong blob-like curvature.

[[IMAGE_NEEDED: Multiscale blob detection | Show the same image with LoG, DoG, and DoH detected blobs drawn as circles of different radii | Learner should understand that detector scale becomes an estimate of feature size]]

The source comparison is roughly:

```text
LoG -> accurate, slower
DoG -> faster approximation
DoH -> Hessian/curvature-based blob response
```

---

## 9. Hessian-based ridge and vessel detection

A ridge is an elongated structure.

Examples from the chapter include:

- blood vessels,
- nerve fibers,
- neurites,
- roads,
- rivers,
- pipelines,
- microscopic filaments.

### Hessian eigenvalues

The Hessian describes local second-order curvature:

```text
H = [
 Ixx  Ixy
 Ixy  Iyy
]
```

Let its eigenvalues be:

```text
lambda_1, lambda_2
```

For a ridge-like structure, the source describes the pattern:

```text
one eigenvalue -> near zero along the ridge
other eigenvalue -> large magnitude across the ridge
```

That asymmetry distinguishes a line/tube from a blob or flat region.

### Multiscale ridge detection

Ridges can have different widths.

Therefore, Hessian derivatives are evaluated across multiple Gaussian scales.

### Ridge filters

The chapter compares:

**Meijering**

- designed for neurites/filaments,
- emphasizes elongated structures,
- multiscale.

**Sato**

- targets tubular structures,
- described with a bright-ridge assumption.

**Frangi**

- vesselness-oriented,
- uses Hessian eigenvalue relationships,
- designed to suppress blob-like structures while emphasizing tubes.

**Hessian filter**

- more general second-order ridge response.

[[IMAGE_NEEDED: Hessian ridge detection | Show a retinal/vessel-like image, local Hessian ellipse/eigen-directions at one vessel point, and Meijering/Sato/Frangi/Hessian outputs | Learner should connect directional curvature with vessel-like structure]]

---

## 10. Structured edges, guided filtering, and anisotropic diffusion

### Structured edge detection

Classical detectors use manually designed local operators.

Structured Edge Detection instead learns a mapping from image patches to small structured edge maps using trained decision forests.

The chapter's OpenCV workflow uses:

```python
cv2.ximgproc.createStructuredEdgeDetection(
    model_path
)
```

The raw output is a probability-like edge response map.

### Orientation maps and NMS

The source then computes an edge-orientation map and applies non-maximum suppression.

Purpose:

```text
wide fuzzy edge response
      ↓ orientation
compare across edge width
      ↓
keep local maximum only
      ↓
thin localized edge
```

This is conceptually similar to Canny's thinning stage.

### Guided filtering

Guided filtering performs edge-aware smoothing by modeling the output locally as a linear transform of a **guidance image**.

Inputs:

- guide image,
- source to be filtered,
- radius,
- regularization `eps`.

The chapter applies guided filtering to a gradient-magnitude image, then subtracts the smoothed gradient to emphasize strong detail.

The key idea is:

> Use edge information in the guide to prevent smoothing across important boundaries.

### Anisotropic diffusion

Ordinary isotropic diffusion smooths in all directions.

Perona–Malik anisotropic diffusion changes the diffusion amount based on local gradient magnitude.

Conceptually:

```text
small gradient
-> likely homogeneous region
-> strong diffusion / smoothing

large gradient
-> likely boundary
-> weak diffusion
-> preserve edge
```

The source implementation exposes parameters:

- `niter` — iterations,
- `kappa` — edge/contrast sensitivity,
- `gamma` — time step,
- `option` — conductivity function.

It notes `gamma` should be at most about `0.25` for the implementation's stability.

[[IMAGE_NEEDED: Isotropic versus anisotropic diffusion | Show a noisy edge profile and two smoothing outcomes: isotropic blur crossing the edge, anisotropic diffusion smoothing inside regions while retaining the boundary | Learner should understand gradient-controlled diffusion]]

The chapter then applies Sobel to the diffused image and shows cleaner edge extraction.

---

## 11. Deep edge detection: HED and PiDiNet

The chapter treats edge detection as a learned pixel-wise problem.

For each pixel, the model predicts:

```text
probability of edge
```

### HED

Holistically-Nested Edge Detection uses a fully convolutional architecture with deep supervision.

The source describes it as VGG-16-based with side outputs from multiple depths.

Intuition:

```text
shallow features -> fine local edges
deeper features  -> coarser/semantic boundaries
learned fusion   -> final edge map
```

This gives HED a rich multiscale representation.

### PiDiNet

Pixel Difference Network is designed to be lighter and faster.

It incorporates trainable pixel-difference operations inspired by classical gradient filters.

The source frames it as:

```text
classical intensity differences
+
learned flexibility
```

### HED versus PiDiNet

| HED | PiDiNet |
|---|---|
| rich multiscale hierarchy | efficient local difference modeling |
| stronger semantic/contextual boundaries | crisp, lightweight responses |
| higher computational demand | better suited to constrained/real-time settings |

[[IMAGE_NEEDED: HED versus PiDiNet | Show one natural image beside PiDiNet and HED edge maps, labeling PiDiNet as sparse/crisp and HED as richer/hierarchical | Learner should understand the accuracy/context versus efficiency trade-off described in the source]]

The source demonstrates pretrained inference through `controlnet_aux` models.

The lesson goal is the architectural intuition, not memorizing model-loading syntax.

---

## 12. Gaussian and Laplacian pyramids

Derivative enhancement can be extended across multiple scales.

### Gaussian pyramid

A Gaussian pyramid repeatedly:

1. smooths,
2. downsamples.

Each deeper level contains:

- lower resolution,
- coarser structure,
- less high-frequency detail.

With scikit-image:

```python
from skimage.transform import pyramid_gaussian

levels = tuple(
    pyramid_gaussian(
        image,
        downscale=2,
        channel_axis=-1,
    )
)
```

[[IMAGE_NEEDED: Gaussian and Laplacian pyramids | Show the same image as a Gaussian pyramid of progressively smaller blurred levels and a Laplacian pyramid of corresponding detail/band-pass layers | Learner should distinguish coarse low-frequency representations from multiscale detail layers]]

### Laplacian pyramid

A Laplacian pyramid stores differences between scales.

Conceptually:

```text
L_k =
G_k
-
expanded(G_{k+1})
```

Each level captures a band of detail that was removed when moving to the next Gaussian scale.

So:

```text
Gaussian pyramid  -> coarse representations
Laplacian pyramid -> multiscale detail/band-pass information
```

### Reconstruction

The original image can be reconstructed by starting from the coarsest representation, expanding it, and adding Laplacian detail levels back.

### Detail enhancement

If a Laplacian level is multiplied by a boost factor before reconstruction:

```text
enhanced reconstruction
=
coarse image
+
boosted detail bands
```

then structures at selected scales can be sharpened.

This is a multiscale extension of the detail-layer idea from unsharp masking.

---

## 13. Pyramid blending and choosing the right detector

### Multiscale blending

The chapter uses Gaussian and Laplacian pyramids to blend two images smoothly.

Given:

- image `A`,
- image `B`,
- mask `M`,

build:

- Laplacian pyramid of `A`,
- Laplacian pyramid of `B`,
- Gaussian pyramid of `M`.

At each scale:

```text
L_blend =
M * L_A
+
(1 - M) * L_B
```

Then reconstruct.

Why this works:

- coarse scales create broad transition,
- fine scales blend details,
- hard seams are reduced.

[[IMAGE_NEEDED: Pyramid image blending | Show two source images, a mask, Laplacian levels from both images, Gaussian mask levels, level-wise blending, and final seamless composite | Learner should understand why blending across scales is smoother than direct binary masking]]

### Detector selection guide

The source ends with a practical mapping.

| Scenario | Starting method(s) from the source |
|---|---|
| Quick low-noise baseline | Sobel / Prewitt |
| Noisy edge detection | Canny / LoG |
| Thin localized edges | Canny |
| Blob-like structures | DoH |
| Vessels / roads / ridges | Frangi |
| Multiscale edges | LoG / DoG |
| Directional emphasis | Kirsch |
| Real-time / low compute | Sobel / PiDiNet |
| Semantic natural-scene boundaries | HED |
| Edge-device deep detector | PiDiNet |

The deeper lesson is that different methods define "edge" differently:

```text
gradient methods
-> intensity discontinuity

second-order methods
-> curvature / zero crossing

Hessian ridge methods
-> directional anisotropy

learned methods
-> boundaries learned from data/context
```

{{exercise:M08.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> A large gradient response is always a real object boundary.

### Why this is wrong

Noise and texture can also cause rapid intensity changes and therefore large derivative responses.

### Misconception 2

> The Laplacian contains edge orientation.

### Why this is wrong

The Laplacian is scalar; the directional information available in the gradient vector is lost.

### Misconception 3

> A universal Laplacian-variance threshold can determine blur for every image.

### Why this is wrong

The source explicitly notes that useful thresholds depend on image content, dimensions, and application.

### Misconception 4

> Unsharp masking detects edges and discards the original image.

### Why this is wrong

It extracts a detail layer from the original-versus-blurred difference and adds amplified detail back to the original.

### Misconception 5

> Canny is just Sobel with a different kernel.

### Why this is wrong

Canny is a multi-stage pipeline including smoothing, gradient calculation, non-maximum suppression, and hysteresis thresholding.

### Misconception 6

> LoG should be applied before smoothing.

### Why this is wrong

Second-order derivatives amplify noise strongly. LoG deliberately combines Gaussian smoothing before the Laplacian response.

### Misconception 7

> DoG and LoG are unrelated.

### Why this is wrong

The chapter presents DoG as an efficient approximation to LoG using two Gaussian scales.

### Misconception 8

> Blob detection and ridge detection are the same task.

### Why this is wrong

Blob detectors seek compact scale-space structures, while ridge filters exploit directional Hessian eigenvalue patterns characteristic of elongated structures.

### Misconception 9

> An RGB image needs a deep model to produce semantic edges.

### Why this is incomplete

Classical derivative methods still work and may be preferable for simplicity, speed, or explicitly local intensity boundaries. Learned methods add data-driven context.

### Misconception 10

> Gaussian and Laplacian pyramids store the same information at each level.

### Why this is wrong

Gaussian levels are progressively smoothed/downsampled images; Laplacian levels encode detail differences between adjacent scales.

---

## Key terminology

| Term | Meaning |
|---|---|
| Partial derivative | Rate of intensity change along one spatial axis |
| Gradient | Vector of first-order image derivatives |
| Gradient magnitude | Strength of local intensity change |
| Gradient direction | Direction of strongest intensity increase |
| Laplacian | Scalar sum of second-order partial derivatives |
| Zero crossing | Position where a second-derivative response changes sign |
| Laplacian variance | Simple derivative-energy measure used for blur assessment |
| Unsharp masking | Sharpening by amplifying original-minus-blur detail |
| Entropy | Measure of intensity-distribution information/uncertainty |
| Sobel | First-order gradient edge operator |
| Prewitt | First-order gradient edge operator |
| Roberts | Compact diagonal difference edge operator |
| Scharr | Gradient operator designed for improved rotational behavior |
| Kirsch | Eight-direction compass edge detector |
| Percentile gradient | Local upper-percentile minus lower-percentile contrast |
| Canny | Multi-stage smoothed gradient edge detector with NMS and hysteresis |
| LoG | Laplacian of Gaussian |
| DoG | Difference of Gaussians |
| Scale space | Representation of structures over multiple smoothing scales |
| DoH | Determinant of Hessian blob response |
| Hessian | Matrix of second-order partial derivatives |
| Ridge | Elongated line/tube-like intensity structure |
| Frangi vesselness | Hessian-eigenvalue ridge measure |
| Structured edge detection | Learned patch-to-edge-map prediction with structured forests |
| NMS | Non-maximum suppression |
| Guided filter | Edge-aware local linear filtering controlled by a guidance image |
| Anisotropic diffusion | Gradient-dependent diffusion that reduces smoothing across edges |
| HED | Holistically-Nested Edge Detection |
| PiDiNet | Pixel Difference Network |
| Gaussian pyramid | Progressively smoothed and downsampled image levels |
| Laplacian pyramid | Multiscale detail/band-pass layers between Gaussian levels |
| Pyramid blending | Multiscale compositing using Laplacian images and Gaussian masks |

---

## Self-check

Before continuing, make sure you can answer:

1. Why does a sharp edge produce a strong first-derivative response?
2. What are `Ix` and `Iy`?
3. What does gradient magnitude represent?
4. How is gradient direction related to edge orientation?
5. How is the Laplacian different from the gradient?
6. Why are second-order derivatives especially sensitive to noise?
7. Why does Laplacian variance fall when an image is blurred?
8. Why is a blur threshold application-dependent?
9. What detail layer does unsharp masking add back?
10. What is optimized in entropy-based gamma enhancement?
11. How do Sobel, Prewitt, Roberts, and Scharr relate conceptually?
12. Why does Kirsch use several directional masks?
13. How does a percentile gradient reduce sensitivity to outliers?
14. What are Canny's four major stages?
15. Why is non-maximum suppression needed?
16. What is hysteresis thresholding?
17. Why does LoG smooth before taking the second derivative?
18. How does DoG approximate LoG?
19. What does a zero crossing represent?
20. Why does scale-space processing help detect differently sized structures?
21. How do LoG, DoG, and DoH differ as blob detectors?
22. What Hessian eigenvalue pattern suggests a ridge?
23. Why is Frangi useful for vessel-like structures?
24. What does structured edge detection predict for an image patch?
25. Why do structured-edge methods use orientation-aware NMS?
26. How does guided filtering preserve boundaries?
27. How does anisotropic diffusion change smoothing at strong gradients?
28. What is the main conceptual difference between HED and PiDiNet?
29. What does each level of a Gaussian pyramid contain?
30. What does each Laplacian-pyramid level contain?
31. How can boosting Laplacian levels sharpen selected spatial scales?
32. Why does pyramid blending create smoother seams than direct masking?
33. Which detector would you choose for vessels, blobs, noisy edges, semantic boundaries, and low-compute deployment?

---

## Retain this idea

**Image derivatives convert intensity change into measurable structure. First-order gradients reveal directional transitions, second-order operators reveal curvature and zero crossings, Hessians reveal local shape, and multiscale or learned methods extend those same ideas across size, context, and semantics.**
        """,

        "estimated_minutes": 360,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "derivative-foundations",
                "title": "From Intensity Change to Image Derivatives",
                "order": 1,
            },
            {
                "id": "laplacian-blur-noise",
                "title": "The Laplacian, Blur Detection, and Noise Sensitivity",
                "order": 2,
            },
            {
                "id": "classical-enhancement",
                "title": "Classical Derivative-Based Enhancement",
                "order": 3,
            },
            {
                "id": "classical-edge-operators",
                "title": "Sobel, Prewitt, Roberts, Scharr, and Laplacian",
                "order": 4,
            },
            {
                "id": "directional-percentile-edges",
                "title": "Directional and Percentile-Gradient Edge Detection",
                "order": 5,
            },
            {
                "id": "canny",
                "title": "Canny Edge Detection",
                "order": 6,
            },
            {
                "id": "log-dog-zero-crossing",
                "title": "LoG, DoG, and Zero-Crossing Edge Detection",
                "order": 7,
            },
            {
                "id": "scale-space-blobs",
                "title": "Scale-Space Blob Detection with LoG, DoG, and DoH",
                "order": 8,
            },
            {
                "id": "ridge-detection",
                "title": "Hessian-Based Ridge and Vessel Detection",
                "order": 9,
            },
            {
                "id": "structured-guided-diffusion",
                "title": "Structured Edges, Guided Filtering, and Anisotropic Diffusion",
                "order": 10,
            },
            {
                "id": "deep-edge-detection",
                "title": "Deep Edge Detection: HED and PiDiNet",
                "order": 11,
            },
            {
                "id": "multiscale-pyramids",
                "title": "Gaussian and Laplacian Pyramids",
                "order": 12,
            },
            {
                "id": "pyramid-blending-selection",
                "title": "Pyramid Blending and Choosing the Right Detector",
                "order": 13,
            },
        ],
    },

    "exercises": [
        {
            "id": "M08.L01.EX01",

            "title": "Compare Derivative-Based Edge Detectors",

            "lesson_code": "M08.L01",

            "section_id": "canny",

            "placement": "after_section",

            "description": (
                "Build intuition for derivative order, smoothing, orientation, "
                "non-maximum suppression, and noise sensitivity by comparing several "
                "classical edge detectors on the same images."
            ),

            "instructions": (
                "1. Choose one clean grayscale image with strong edges and one noisy "
                "version of the same image.\n"
                "2. Compute horizontal/vertical derivatives and gradient magnitude using "
                "finite-difference or Sobel kernels.\n"
                "3. Apply Sobel, Scharr, Laplacian, and Canny to both clean and noisy images.\n"
                "4. Compare how strongly each method responds to the added noise.\n"
                "5. Smooth the noisy image with a Gaussian filter and repeat the Laplacian "
                "or LoG response.\n"
                "6. Measure Laplacian variance for the original and at least two deliberately "
                "blurred versions.\n"
                "7. Run Canny with at least two smoothing/threshold configurations and "
                "compare edge thickness, missing edges, and false edges.\n"
                "8. If possible, run Kirsch or percentile-gradient detection and compare "
                "directional/rank-based behavior with ordinary gradients.\n"
                "9. Explain which method provides the best result for your chosen image and "
                "why; do not judge only by the number of detected pixels."
            ),

            "expected_output": (
                "A notebook or script containing derivative components, classical edge maps, "
                "noise/smoothing comparisons, Laplacian-variance blur scores, at least two "
                "Canny configurations, and a short evidence-based detector comparison."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "image-gradients",
                "laplacian",
                "blur-detection",
                "sobel",
                "scharr",
                "canny",
                "noise-analysis",
                "parameter-tuning",
            ],
        },

        {
            "id": "M08.L01.EX02",

            "title": "Build a Multiscale Edge and Detail Analysis",

            "lesson_code": "M08.L01",

            "section_id": "pyramid-blending-selection",

            "placement": "after_section",

            "description": (
                "Connect second-order derivatives, scale-space analysis, ridges, learned "
                "edge maps, and image pyramids in one multiscale workflow."
            ),

            "instructions": (
                "1. Choose an image containing structures of several sizes.\n"
                "2. Apply LoG at at least three sigma values and explain which feature "
                "sizes become more visible at each scale.\n"
                "3. Run one blob detector (LoG, DoG, or DoH) and visualize detected radii.\n"
                "4. If the image has line-like structures, apply Frangi or another ridge "
                "filter and compare it with a normal edge detector.\n"
                "5. Build a Gaussian pyramid and a Laplacian pyramid with downscale=2.\n"
                "6. Reconstruct the image from the Laplacian pyramid.\n"
                "7. Boost one or more Laplacian detail levels and observe which spatial "
                "scales become sharper.\n"
                "8. If resources permit, run pretrained PiDiNet or HED and compare the "
                "learned edge map with Canny.\n"
                "9. Create a small decision table choosing a detector for: noisy edges, "
                "blobs, vessels/ridges, semantic boundaries, and low-compute deployment.\n"
                "10. Explain how the meaning of 'edge' differs across gradient, Hessian, "
                "and learning-based methods."
            ),

            "expected_output": (
                "A notebook or script with multiscale LoG results, one blob/ridge experiment, "
                "Gaussian and Laplacian pyramids, successful reconstruction, detail-boosted "
                "output, optional learned-edge comparison, and a detector-selection table."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "log",
                "scale-space",
                "blob-detection",
                "ridge-detection",
                "gaussian-pyramid",
                "laplacian-pyramid",
                "multiscale-enhancement",
                "edge-detector-selection",
            ],
        },
    ],

    "quiz": {
        "id": "M08.L01.QZ01",

        "title": "Image Enhancements Using Derivatives — Knowledge Check",

        "lesson_code": "M08.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M08.L01.Q01",
                "section_id": "derivative-foundations",
                "question": "What does gradient magnitude primarily measure in an image?",
                "options": [
                    "Strength of local intensity change",
                    "Global file size",
                    "Image color mode",
                    "Number of pyramid levels",
                ],
                "correct": 0,
                "explanation": (
                    "Large first-order derivative magnitude indicates a strong local "
                    "intensity transition."
                ),
            },

            {
                "id": "M08.L01.Q02",
                "section_id": "laplacian-blur-noise",
                "question": (
                    "Why is the Laplacian generally more noise-sensitive than a first-order gradient?"
                ),
                "options": [
                    "It uses second-order derivatives, which amplify rapid local variation strongly",
                    "It always uses a larger image",
                    "It removes all high frequencies",
                    "It can only process binary images",
                ],
                "correct": 0,
                "explanation": (
                    "Higher derivative order magnifies rapid fluctuations, including noise."
                ),
            },

            {
                "id": "M08.L01.Q03",
                "section_id": "laplacian-blur-noise",
                "question": (
                    "What does a low variance of the Laplacian often suggest in the chapter's blur heuristic?"
                ),
                "options": [
                    "The image may be relatively blurred or low in sharp detail",
                    "The image is guaranteed to be correctly exposed",
                    "The image contains more edges",
                    "The image has more color channels",
                ],
                "correct": 0,
                "explanation": (
                    "Blur suppresses high-frequency structure and therefore reduces "
                    "variation in the Laplacian response."
                ),
            },

            {
                "id": "M08.L01.Q04",
                "section_id": "classical-enhancement",
                "question": "What is the core detail layer used in unsharp masking?",
                "options": [
                    "Original minus blurred image",
                    "Blurred image minus histogram",
                    "Only the Fourier phase",
                    "Thresholded binary image",
                ],
                "correct": 0,
                "explanation": (
                    "Subtracting a blurred image from the original isolates higher-frequency detail."
                ),
            },

            {
                "id": "M08.L01.Q05",
                "section_id": "classical-edge-operators",
                "question": (
                    "Which source statement distinguishes Scharr from Sobel in gradient estimation?"
                ),
                "options": [
                    "Scharr has less rotational variance",
                    "Scharr is a second-order Laplacian",
                    "Scharr requires eight compass kernels",
                    "Scharr performs hysteresis thresholding",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter describes Scharr as providing improved rotational behavior."
                ),
            },

            {
                "id": "M08.L01.Q06",
                "section_id": "directional-percentile-edges",
                "question": "How does Kirsch produce its final edge strength?",
                "options": [
                    "Take the strongest response across eight directional kernels",
                    "Average all image pixels globally",
                    "Run a single isotropic Laplacian only",
                    "Use histogram matching",
                ],
                "correct": 0,
                "explanation": (
                    "Kirsch evaluates eight compass directions and keeps the strongest response."
                ),
            },

            {
                "id": "M08.L01.Q07",
                "section_id": "canny",
                "question": (
                    "What is the purpose of non-maximum suppression in Canny?"
                ),
                "options": [
                    "Thin broad gradient responses by keeping local maxima across edge width",
                    "Add Gaussian noise",
                    "Increase image brightness",
                    "Perform color correction",
                ],
                "correct": 0,
                "explanation": (
                    "NMS improves edge localization by suppressing non-maximal responses."
                ),
            },

            {
                "id": "M08.L01.Q08",
                "section_id": "canny",
                "question": (
                    "What does hysteresis thresholding do with a weak edge candidate?"
                ),
                "options": [
                    "Keeps it when it is connected to a strong edge",
                    "Always discards it",
                    "Always converts it into a strong edge",
                    "Uses only its RGB value",
                ],
                "correct": 0,
                "explanation": (
                    "Connectivity to strong edges determines whether intermediate responses survive."
                ),
            },

            {
                "id": "M08.L01.Q09",
                "section_id": "log-dog-zero-crossing",
                "question": "Why does LoG include Gaussian smoothing?",
                "options": [
                    "Second-order derivatives are very noise-sensitive",
                    "Gaussian smoothing creates color channels",
                    "The Laplacian cannot operate on grayscale images",
                    "Smoothing is required to compute a histogram",
                ],
                "correct": 0,
                "explanation": (
                    "Smoothing suppresses noise before the sensitive second derivative is applied."
                ),
            },

            {
                "id": "M08.L01.Q10",
                "section_id": "scale-space-blobs",
                "question": (
                    "Why are several sigma values used in scale-space blob detection?"
                ),
                "options": [
                    "To detect structures appearing at different spatial sizes",
                    "To change JPEG quality",
                    "To rotate the image",
                    "To create an alpha channel",
                ],
                "correct": 0,
                "explanation": (
                    "Different Gaussian scales make the detector responsive to differently sized features."
                ),
            },

            {
                "id": "M08.L01.Q11",
                "section_id": "ridge-detection",
                "question": (
                    "What local Hessian pattern is characteristic of a ridge in the source discussion?"
                ),
                "options": [
                    "One eigenvalue near zero and another with large magnitude",
                    "Both eigenvalues always exactly zero",
                    "No second derivatives",
                    "Only the RGB mean matters",
                ],
                "correct": 0,
                "explanation": (
                    "A ridge is relatively flat along its direction but strongly curved across it."
                ),
            },

            {
                "id": "M08.L01.Q12",
                "section_id": "structured-guided-diffusion",
                "question": (
                    "How does anisotropic diffusion preserve edges?"
                ),
                "options": [
                    "It reduces diffusion where gradient magnitude is large",
                    "It applies equal smoothing everywhere",
                    "It deletes all low frequencies",
                    "It uses only a global histogram",
                ],
                "correct": 0,
                "explanation": (
                    "Perona–Malik diffusion uses a gradient-dependent conductivity that "
                    "suppresses smoothing across strong boundaries."
                ),
            },

            {
                "id": "M08.L01.Q13",
                "section_id": "deep-edge-detection",
                "question": (
                    "Which statement best reflects the source's HED versus PiDiNet comparison?"
                ),
                "options": [
                    "HED emphasizes rich multiscale/semantic boundaries, while PiDiNet emphasizes efficient learned pixel differences",
                    "PiDiNet is a histogram-equalization algorithm",
                    "HED is a fixed Sobel kernel",
                    "Both are identical architectures",
                ],
                "correct": 0,
                "explanation": (
                    "The source contrasts HED's representation richness with PiDiNet's "
                    "lightweight local-difference design."
                ),
            },

            {
                "id": "M08.L01.Q14",
                "section_id": "multiscale-pyramids",
                "question": (
                    "What is stored in a Laplacian-pyramid level?"
                ),
                "options": [
                    "Detail/band-pass information between adjacent Gaussian scales",
                    "Only the full-resolution original image at every level",
                    "A histogram reference",
                    "Only an edge probability from HED",
                ],
                "correct": 0,
                "explanation": (
                    "Each Laplacian level represents detail lost between adjacent smoothed scales."
                ),
            },

            {
                "id": "M08.L01.Q15",
                "section_id": "pyramid-blending-selection",
                "question": (
                    "Why does pyramid blending often create a smoother composite than a hard binary mask?"
                ),
                "options": [
                    "The transition is blended across multiple spatial scales",
                    "It removes all derivative information",
                    "It forces every pixel to the same value",
                    "It uses only a single global threshold",
                ],
                "correct": 0,
                "explanation": (
                    "Gaussian mask levels and Laplacian image levels distribute the blend "
                    "smoothly across coarse and fine structures."
                ),
            },

            {
                "id": "M08.L01.Q16",
                "section_id": "pyramid-blending-selection",
                "type": "open",
                "question": (
                    "You must process three datasets: noisy street scenes requiring thin "
                    "boundaries, retinal images requiring vessel extraction, and natural "
                    "scenes requiring semantic object boundaries on an edge device. Choose "
                    "a method from this lesson for each case, justify the choice using the "
                    "type of structure each method detects, and describe one failure mode or "
                    "trade-off you would inspect."
                ),
            },
        ],

        "passing_score": 70,
    },
}
