"""M07.L01 — Image Enhancement.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 7. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M07.L01"

MODULE_ORDER = 7

MODULE_TITLE = "Image Enhancement"

MODULE_DESCRIPTION = (
    "Learn classical and modern image-enhancement techniques, including point-wise "
    "intensity transforms, thresholding and dithering, histogram processing, fuzzy "
    "contrast enhancement, white balance, linear and nonlinear denoising, bilateral "
    "and non-local means filtering, BM3D, wavelet fusion, an interactive Streamlit "
    "enhancement workflow, and pretrained models for low-light enhancement, denoising, "
    "dehazing, and super-resolution."
)

SOURCE_CHAPTER = 7

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Image Enhancement",

    "slug": "image-processing-m07-l01",

    "description": (
        "A practical, source-aligned lesson on improving image appearance and useful "
        "visual structure with point transforms, histogram methods, dithering, fuzzy "
        "logic, color correction, linear and nonlinear denoising, BM3D, wavelet fusion, "
        "interactive enhancement tools, and advanced pretrained enhancement models."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 6.0,

    "skill_tags": [
        "image-processing",
        "image-enhancement",
        "gamma-correction",
        "histogram-equalization",
        "dithering",
        "floyd-steinberg",
        "fuzzy-logic",
        "white-balance",
        "gaussian-filter",
        "median-filter",
        "bilateral-filter",
        "non-local-means",
        "bm3d",
        "wavelet-fusion",
        "streamlit",
        "zero-dce",
        "maxim",
        "dark-channel-prior",
        "edsr",
        "super-resolution",
    ],

    "prerequisite_ids": ["M06.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Image Enhancement",

        "content": r"""
# Image Enhancement

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M07.L01  
> **Module:** Image Enhancement  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 7. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what image enhancement aims to do and how the chapter distinguishes it from restoration.
- Apply log, power-law/gamma, brightness, and contrast transformations.
- Explain thresholding, random halftoning, and Floyd–Steinberg error-diffusion dithering.
- Distinguish histogram stretching, shrinking, sliding, equalization, adaptive equalization, and histogram matching.
- Describe a Mamdani fuzzy-inference workflow for contrast enhancement.
- Apply saturation changes and compare several white-balance strategies.
- Choose between linear and nonlinear smoothing according to the noise model.
- Explain box, Gaussian, median, mode, min/max, percentile, bilateral, and non-local means filters.
- Explain the BM3D denoising pipeline and the role of PSNR/SSIM.
- Explain how a 2D discrete wavelet transform supports image fusion.
- Describe the architecture of a simple interactive Streamlit image-enhancement app.
- Explain the intuition behind Zero-DCE low-light enhancement.
- Describe the MAXIM pretrained denoising workflow.
- Explain Dark Channel Prior dehazing from the atmospheric scattering model.
- Explain why EDSR can reconstruct richer high-resolution detail than fixed bicubic interpolation.

---

## 1. What image enhancement is trying to achieve

The source chapter defines enhancement as improving visual quality or emphasizing useful features without requiring an explicit degradation model.

Typical goals include:

- improve contrast,
- make dark or bright regions easier to inspect,
- suppress visible noise,
- emphasize details,
- correct color casts,
- combine useful information from multiple images,
- produce a more useful input for later computer-vision tasks.

The chapter contrasts this with **image restoration**, where the processing is tied more explicitly to a degradation process or model.

A useful map for this chapter is:

```text
single pixel
    -> point transformations

global intensity distribution
    -> histogram processing

local neighborhood
    -> linear/nonlinear filters

similar patches
    -> non-local means / BM3D

multiple scales
    -> wavelets

data-driven or learned mapping
    -> Zero-DCE / MAXIM / EDSR
```

[[IMAGE_NEEDED: Image enhancement strategy map | A diagram grouping enhancement methods by information used: single pixel, global histogram, local neighborhood, non-local patches, multi-scale wavelets, and learned models | Learner should understand that enhancement methods differ mainly in what context they use to decide a new pixel value]]

---

## 2. Point-wise intensity transformations

A point-wise transformation is memoryless:

```text
output pixel = T(input pixel)
```

Each output value depends only on the corresponding input value.

It does not look at neighboring pixels.

### Log transform

A log transform has the general form:

```text
s = c * log(1 + r)
```

The `+1` avoids `log(0)`.

Its purpose is to redistribute intensity ranges nonlinearly.

The chapter connects this to Fourier-spectrum visualization, where a few large coefficients can otherwise dominate the display.

With Pillow:

```python
from PIL import Image
import numpy as np

im = Image.open("images/example.png")

im_log = im.point(
    lambda i: 255 * np.log(1 + i / 255)
)
```

The exact visual result depends on the input range and scaling, so inspect both image and histogram.

### Power-law / gamma transform

For normalized values:

```text
s = c * r^gamma
```

The source emphasizes the effect of gamma clearly:

```text
gamma < 1 -> expands dark values -> brightens shadows
gamma = 1 -> no change
gamma > 1 -> compresses low values -> darkens image
```

Example:

```python
from skimage import img_as_float
from skimage.io import imread

im = img_as_float(
    imread("images/cheetah.png")
)

gamma = 2.5
im_transformed = im ** gamma
```

This is nonlinear: it changes how contrast is distributed across the intensity range.

[[IMAGE_NEEDED: Gamma transform curves and images | Show gamma curves for gamma < 1, gamma = 1, gamma > 1 plus the same image transformed with each case | Learner should remember that gamma below one brightens darker intensities while gamma above one darkens them in the source convention]]

### Brightness versus contrast

A common affine intensity model is:

```text
output = alpha * input + beta
```

where:

- `alpha` scales differences between values,
- `beta` shifts values.

The chapter uses OpenCV:

```python
import cv2

high_contrast = cv2.convertScaleAbs(
    image,
    alpha=2,
    beta=0,
)

brighter = cv2.convertScaleAbs(
    image,
    alpha=1.0,
    beta=50,
)
```

A useful distinction is:

```text
brightness -> shifts histogram location
contrast   -> stretches/compresses intensity differences
```

Values must remain inside the valid digital range.

---

## 3. Thresholding, halftoning, and dithering

### Thresholding

Thresholding converts a gray-level image into discrete classes, often binary:

```text
if intensity < T -> 0
else             -> 1
```

Applications mentioned in the chapter include:

- foreground/background separation,
- black-and-white printing,
- preprocessing for later morphology.

A hard threshold can destroy smooth shading.

This can create:

- posterization,
- false contours,
- abrupt artificial transitions.

### Random halftoning

One way to break up large artificial bands is to add random noise before binary quantization.

Conceptually:

```text
image
 + random perturbation
        ↓
threshold
        ↓
spatial pattern of black/white pixels
```

At normal viewing distance, the eye can perceive these patterns as intermediate gray levels.

The trade-off is that the output looks noisier at close range.

### Dithering

Dithering is the broader idea of deliberately redistributing quantization error in space instead of allowing the error to form large visible contour bands.

Methods can include:

- random dithering,
- ordered dithering,
- error diffusion.

### Floyd–Steinberg error diffusion

Floyd–Steinberg dithering processes pixels in a causal scan order.

After quantizing the current pixel:

```text
error = old_value - quantized_value
```

the error is distributed only to pixels that have not yet been processed.

The standard neighborhood weights used in the chapter are:

```text
        current   7/16
3/16     5/16     1/16
```

Their sum is `1`, so the quantization error is redistributed rather than simply discarded.

{{image:floyd-steinberg-error-diffusion}}

A simplified implementation pattern:

```python
def closest_level(value, num_levels):
    step = 255 / (num_levels - 1)
    return np.round(value / step) * step
```

Then each future neighbor receives a weighted fraction of the current quantization error.

[[IMAGE_NEEDED: Threshold vs random dithering vs Floyd-Steinberg | Show the same grayscale photograph converted by hard thresholding, random dithering, and Floyd–Steinberg dithering | Learner should compare false contours, noise-like halftone structure, and structured error diffusion]]

### Why error diffusion can look better

If several earlier pixels were rounded downward, the propagated positive error makes later pixels more likely to round upward.

The local average therefore tracks the original tone better than independent hard thresholding.

The chapter extends the method beyond binary output to:

```text
k discrete gray levels
```

using an equally spaced palette.

---

## 4. Histogram modification and equalization

A histogram describes how often intensity values occur.

Changing the histogram changes the distribution of brightness and contrast.

### Histogram stretching

Stretching expands a limited input range to a wider output range.

Conceptually:

```text
narrow intensity interval
        ↓ linear mapping
wide interval
```

This increases contrast.

The chapter also discusses clipping a small number of extreme pixels so that outliers do not dominate the stretch.

### Histogram shrinking

Shrinking maps the image into a smaller intensity interval.

Effect:

- reduced contrast,
- more washed-out appearance.

### Histogram sliding

Sliding adds or subtracts a constant:

```text
output = input + shift
```

It changes brightness while preserving the relative intensity differences until clipping occurs.

### Global histogram equalization

Histogram equalization applies a monotonic nonlinear mapping based on the cumulative distribution of intensities.

Its goal is to redistribute intensities across the available range and improve contrast.

With scikit-image:

```python
from skimage import exposure

equalized = exposure.equalize_hist(image)
```

### Adaptive histogram equalization

Instead of processing the entire image with one mapping, adaptive histogram equalization works locally in blocks/regions.

The chapter uses:

```python
adaptive = exposure.equalize_adapthist(
    image,
    clip_limit=0.03,
)
```

The source example finds the adaptive result better at revealing local details than global equalization for the shown input.

[[IMAGE_NEEDED: Histogram processing comparison | Show original low-contrast image and histogram beside contrast stretching, global histogram equalization, and adaptive histogram equalization with their histograms/CDFs | Learner should see the difference between global range expansion and local contrast redistribution]]

### Do not confuse these operations

```text
stretching
-> mostly range expansion

equalization
-> distribution-driven nonlinear remapping

adaptive equalization
-> local distribution-driven remapping

sliding
-> brightness shift
```

---

## 5. Fuzzy contrast enhancement and histogram matching

### Why fuzzy logic?

Terms such as:

- dark,
- medium,
- bright,

do not always have crisp boundaries.

Fuzzy logic allows one pixel to belong partially to several categories.

For example:

```text
intensity 110
might be:
0.2 dark
0.8 medium
0.0 bright
```

### Mamdani fuzzy enhancement

The chapter builds a Mamdani fuzzy-inference system with four stages.

#### 1. Fuzzification

Convert intensity into membership degrees for sets such as:

- dark,
- medium,
- bright.

#### 2. Rule evaluation

Example rules from the source:

```text
IF intensity is dark
THEN output is darker

IF intensity is medium
THEN output is enhanced

IF intensity is bright
THEN output is brighter
```

The rule firing strength is evaluated with minimum operations.

#### 3. Aggregation

Combine rule outputs using maximum operations.

#### 4. Defuzzification

Convert the aggregated fuzzy output into one numerical intensity, using centroid defuzzification in the chapter.

[[IMAGE_NEEDED: Mamdani fuzzy enhancement | Show input intensity axis with dark/medium/bright membership curves, three IF-THEN rules, aggregated output membership functions, and one defuzzified output intensity | Learner should understand the four-step fuzzy inference pipeline]]

The chapter adapts input membership functions to the actual image intensity range.

This makes the rule system responsive to the input's dynamic range.

### Histogram matching

Histogram matching changes a source image so its intensity/color distribution resembles that of a reference image.

The central idea uses cumulative distribution functions:

```text
source intensity
 -> source CDF probability
 -> find reference intensity with similar CDF probability
 -> output intensity
```

With scikit-image:

```python
from skimage.exposure import match_histograms

matched = match_histograms(
    source,
    reference,
    channel_axis=-1,
)
```

The chapter lists uses such as:

- remote-sensing normalization,
- standardization of medical images,
- visual consistency across photographs.

---

## 6. Color enhancement and white balance

### Saturation enhancement

Pillow can increase or reduce color intensity:

```python
from PIL import ImageEnhance

enhancer = ImageEnhance.Color(image)

colorful = enhancer.enhance(1.8)
desaturated = enhancer.enhance(0.3)
```

This changes chromatic intensity rather than simply shifting overall brightness.

### White balance

White balancing aims to remove an unwanted color cast so neutral scene content appears neutral.

The chapter demonstrates several classical assumptions.

#### Gray World

Assume average scene reflectance is gray.

Compute mean R, G, and B values, then scale channels so their averages become more balanced.

#### Percentile clipping per channel

For each channel:

1. estimate lower and upper percentiles,
2. clip extreme values,
3. stretch the retained interval to the valid range.

This reduces sensitivity to extreme shadows/highlights.

#### White Patch

Assume the brightest value in each channel corresponds to white.

Scale each channel so its maximum reaches the output maximum.

#### Percentile White Patch

Use a high percentile such as the 95th percentile instead of the absolute maximum.

This is more robust to isolated bright outliers.

#### Shades of Gray

Use a Minkowski-norm estimate of channel illumination rather than only means or maxima.

[[IMAGE_NEEDED: White-balance methods | Show one color-cast input beside Gray World, White Patch, percentile White Patch, and Shades of Gray results | Learner should compare how different illuminant assumptions change RGB channel scaling]]

No single assumption is guaranteed to be correct for every scene.

The algorithm should be chosen based on image content and application.

---

## 7. Linear smoothing: box and Gaussian filters

Linear smoothing computes a weighted sum over a local neighborhood:

```text
output(i,j)
=
sum(kernel * neighborhood)
```

The chapter models a noisy observation as:

```text
observed = true signal + noise
```

and explains that averaging can reduce random variation.

### Box filter

A box filter gives all neighboring pixels equal weight.

For a `3×3` average:

```text
1/9 * [
1 1 1
1 1 1
1 1 1
]
```

It reduces noise through averaging, but it also blurs edges.

Increasing kernel size:

- increases smoothing,
- reduces more small variation,
- removes more detail.

### Gaussian filter

A Gaussian gives greater weight to closer pixels and smaller weight to more distant pixels.

Its kernel is:

- symmetric,
- separable,
- smoothly weighted.

Increasing Gaussian radius or standard deviation produces stronger blur.

[[IMAGE_NEEDED: Box versus Gaussian smoothing | Show a noisy image, box-filter outputs with two kernel sizes, and Gaussian outputs with two sigma/radius values | Learner should see stronger smoothing with larger neighborhoods and the different weighting behavior of box versus Gaussian filters]]

### Why linear smoothing struggles with impulse noise

Salt-and-pepper noise contains extreme outliers.

An average includes those extreme values, so the outlier can contaminate neighboring outputs.

This motivates nonlinear order-statistic filters.

---

## 8. Nonlinear order-statistic filters

Nonlinear filters do not compute a weighted sum.

Instead, they apply another function to neighborhood values.

### Median filter

Sort the neighborhood and take the middle value.

Why this helps with impulse noise:

- very dark/bright outliers move to the ends of the sorted list,
- the median is much less affected by extremes.

Properties from the chapter:

- good for salt-and-pepper noise,
- better edge preservation than averaging,
- large kernels can create patchy regions and remove small detail.

### Mode filter

Replace the center with the most common neighborhood value.

This encourages locally homogeneous regions.

### Maximum filter

Choose the largest neighborhood value.

The chapter connects this with removing dark/pepper impulses.

### Minimum filter

Choose the smallest neighborhood value.

The chapter connects this with removing bright/salt impulses.

### Percentile filter

The percentile filter generalizes these order-statistic choices.

Special cases include:

```text
0th percentile   -> minimum
50th percentile  -> median
100th percentile -> maximum
```

A percentile between the extremes can bias the output toward darker or brighter local values.

Example:

```python
from scipy import ndimage

filtered = ndimage.percentile_filter(
    image,
    percentile=50,
    size=(5, 5, 1),
)
```

[[IMAGE_NEEDED: Order-statistic filters | Show a salt-and-pepper corrupted image beside median, mode, minimum, maximum, and 25/50/75 percentile outputs | Learner should understand that these filters choose ranked neighborhood values rather than averages]]

{{exercise:M07.L01.EX01}}

---

## 9. Bilateral filtering and non-local means

### Bilateral filter

A Gaussian spatial smoother weights neighbors by distance.

A bilateral filter adds a second condition:

> Nearby pixels should also have similar intensity.

Its weight combines:

- spatial proximity,
- intensity similarity.

Conceptually:

```text
weight =
spatial_similarity
×
intensity_similarity
```

Therefore, pixels across a strong edge can receive very small weights even if they are spatially close.

This allows noise smoothing inside regions while reducing blur across boundaries.

Important parameters:

```text
sigma_spatial -> how far the filter looks
sigma_color   -> how different intensities may still be averaged
```

### Non-local means (NLM)

NLM moves beyond individual pixel similarity.

It compares **patches**.

For a target pixel:

1. take the patch around it,
2. search a wider region,
3. find other patches with similar appearance,
4. average using patch-similarity weights.

This is powerful when textures repeat in different image locations.

[[IMAGE_NEEDED: Bilateral versus non-local means | Show a target pixel/patch, bilateral local neighborhood weighted by distance+intensity, and NLM searching for similar patches across a larger region | Learner should distinguish local pixel similarity from non-local patch similarity]]

The chapter compares the methods:

```text
Bilateral:
- local
- edge-preserving
- lower/moderate cost

NLM:
- non-local
- strong texture preservation
- higher computational cost
```

The NLM parameter `h` controls how selective the patch weighting is:

```text
small h -> only very similar patches matter
large h -> more patches contribute -> stronger smoothing
```

---

## 10. Interactive enhancement workflow and BM3D

### Streamlit enhancement app

The chapter turns enhancement algorithms into an interactive application.

The architecture separates:

```text
Streamlit UI
    ↓
image enhancement engine
    ↓
processed output
```

The UI allows a learner/user to:

- upload an image,
- select an enhancement method,
- adjust method-specific parameters,
- compare original and enhanced results side by side.

The source app includes histogram-related methods such as:

- GHE,
- BBHE,
- BPHEME,
- RLBHE,
- QBHE,
- AGCCPF.

A simplified UI pattern is:

```python
import streamlit as st

uploaded = st.file_uploader(
    "Upload an image",
    type=["png", "jpg", "jpeg"],
)

method = st.selectbox(
    "Enhancement method",
    [
        "Global HE",
        "Brightness Preserving HE",
    ],
)
```

The important software-design lesson is separation of concerns:

```text
UI code
!=
enhancement algorithm code
```

[[IMAGE_NEEDED: Streamlit enhancement app architecture | Show user/upload controls feeding app.py, then a separate enhancement-engine module, then original/enhanced preview panels | Learner should see the benefit of keeping UI and image-processing logic modular]]

### BM3D denoising

Block-Matching and 3D filtering (BM3D) uses repeated image patterns more aggressively than ordinary local filtering.

The chapter describes two main estimation stages:

1. **Basic estimate** using hard thresholding.
2. **Final estimate** using Wiener filtering.

Its recurring pipeline contains:

#### Block matching

Find similar 2D patches throughout the image.

#### 3D grouping

Stack similar patches into a 3D group.

#### Collaborative filtering

Transform the group, suppress noise through thresholding or Wiener filtering, then invert the transform.

#### Aggregation

Return filtered patches to their image positions and combine overlapping estimates.

[[IMAGE_NEEDED: BM3D pipeline | Show noisy image, extraction of one reference patch, matching similar patches across the image, stacking into a 3D group, collaborative transform-domain filtering, and aggregation back into a denoised image | Learner should understand why the method is called block-matching and 3D filtering]]

The chapter evaluates BM3D with:

- PSNR,
- SSIM.

It also emphasizes a practical limitation:

> BM3D is computationally heavier than simpler filters and depends on a reasonable noise-level estimate.

---

## 11. Wavelet-based image fusion

Image fusion combines complementary information from multiple images of the same scene.

The chapter uses the discrete wavelet transform (DWT) because it is localized in both:

- space,
- frequency/scale.

### One-level 2D DWT

A 2D wavelet decomposition produces four sub-bands:

```text
LL -> approximation / low-frequency structure
LH -> one directional detail component
HL -> another directional detail component
HH -> diagonal/high-frequency detail
```

Conceptually:

```text
input image
    ↓ low/high filtering across rows
    ↓ downsample
    ↓ low/high filtering across columns
    ↓ downsample
LL, LH, HL, HH
```

[[IMAGE_NEEDED: 2D wavelet decomposition | Show an input image splitting into the four standard wavelet sub-bands LL, LH, HL, HH with labels for approximation and directional details | Learner should see wavelet decomposition as a multi-scale separation of coarse structure and details]]

### Fusion

Given two images:

1. decompose both with the same wavelet,
2. combine corresponding coefficient arrays,
3. reconstruct with inverse DWT.

Fusion rules in the source include:

```text
mean -> average coefficients
max  -> keep stronger coefficient
min  -> keep weaker coefficient
```

Example library:

```python
import pywt

coeffs1 = pywt.wavedec2(
    image1,
    "db1",
)

coeffs2 = pywt.wavedec2(
    image2,
    "db1",
)
```

Then fuse approximation/detail coefficients and reconstruct with:

```python
pywt.waverec2(...)
```

The choice of fusion rule controls which structures are emphasized.

---

## 12. Advanced enhancement: Zero-DCE and MAXIM

The chapter's final section moves to data-driven enhancement using pretrained models.

### Zero-DCE for low-light enhancement

Zero-DCE learns a pixel-adaptive enhancement curve.

Instead of needing paired low-light and normal-light target images, the source describes a zero-reference training strategy with self-regularizing losses.

The network predicts per-pixel curve parameters, then applies the enhancement repeatedly.

A source-aligned forward step has the form:

```python
x = x + alpha * (x**2 - x)
```

where `alpha` is predicted by the network.

Repeated updates progressively modify the low-light image.

### Why the source says it works

Its loss design encourages:

- spatial consistency,
- target exposure,
- color constancy,
- smooth illumination behavior.

The DCE-Net described in the chapter is lightweight and convolutional, with skip connections and multiple predicted enhancement maps.

[[IMAGE_NEEDED: Zero-DCE iterative enhancement | Show low-light input, DCE-Net predicting per-pixel alpha maps, several iterative curve-adjustment stages, and final enhanced image | Learner should understand that the network predicts adaptive enhancement curves rather than directly outputting an unrelated image]]

### MAXIM denoising

The chapter then demonstrates a pretrained MAXIM model for image denoising.

Key architectural ideas listed by the source include:

- multi-axis MLP processing,
- local and global operations,
- hierarchical encoder-decoder structure,
- skip connections,
- cross-gating,
- multi-scale outputs.

The practical workflow is:

```text
noisy image
    ↓ resize/preprocess
pretrained MAXIM-S3
    ↓
intermediate restoration outputs
    ↓
final denoised result
```

The source example loads a pretrained SIDD denoising model and uses the last restoration output as the final result.

---

## 13. Dehazing with Dark Channel Prior and super-resolution with EDSR

### Dark Channel Prior (DCP)

The chapter's advanced enhancement section also includes Dark Channel Prior dehazing.

The method is based on an atmospheric scattering model.

A hazy image contains contributions from:

- scene radiance,
- atmospheric light,
- transmission through the medium.

The algorithm uses the empirical observation that many haze-free outdoor patches contain very dark pixels in at least one color channel.

### DCP workflow

The source implementation follows these steps:

1. compute a dark channel using a local minimum operation,
2. estimate atmospheric light from bright dark-channel locations,
3. estimate a transmission map,
4. enforce a minimum transmission,
5. recover scene radiance from the haze model.

[[IMAGE_NEEDED: Dark Channel Prior dehazing | Show hazy input, dark-channel image, estimated atmospheric-light marker/vector, transmission map, and reconstructed dehazed result | Learner should understand the sequence from statistical prior to transmission estimation to scene recovery]]

The source notes that the approach works best for suitable outdoor haze and that transmission refinement can improve visual quality.

### EDSR super-resolution

Super-resolution estimates a high-resolution image from a low-resolution input.

The chapter compares:

```text
fixed bicubic interpolation
vs.
pretrained EDSR
```

EDSR is built from residual learning.

The architecture described includes:

- initial feature extraction,
- multiple residual blocks,
- short residual skip connections,
- a long skip connection,
- upsampling via sub-pixel convolution/pixel shuffle,
- final RGB reconstruction.

A residual block follows the pattern:

```text
input
  ↓
Conv -> ReLU -> Conv
  ↓
+ skip connection
  ↓
output
```

For ×4 scaling, the implementation can apply ×2 pixel-shuffle stages successively.

[[IMAGE_NEEDED: Bicubic versus EDSR super-resolution | Show the same low-resolution crop, bicubic ×4 enlargement, and EDSR ×4 output with a magnified edge/texture region | Learner should compare fixed interpolation with learned detail reconstruction]]

The source example reports that the EDSR result appears sharper and retains stronger texture than the bicubic baseline.

{{exercise:M07.L01.EX02}}

---

## Choosing an enhancement method

The chapter includes many techniques. A useful decision guide is:

| Problem | Reasonable starting point from this chapter |
|---|---|
| Dark image | Gamma/power-law, brightness adjustment, Zero-DCE |
| Low global contrast | Contrast stretching or histogram equalization |
| Uneven/local contrast | Adaptive histogram equalization |
| Need reference-image appearance | Histogram matching |
| Color cast | White-balance methods |
| Gaussian-like noise | Gaussian, bilateral, NLM, BM3D |
| Salt-and-pepper noise | Median / percentile-based filtering |
| Preserve edges while smoothing | Bilateral |
| Preserve repetitive texture | NLM / BM3D |
| Combine complementary images | Wavelet fusion |
| Outdoor haze | Dark Channel Prior |
| Low-resolution input | EDSR |
| Experiment with many methods | Streamlit enhancement app |

The choice depends on the **problem**, not on which function is most sophisticated.

---

## Important misconceptions

### Misconception 1

> Enhancement always recovers missing information.

### Why this is wrong

Many enhancement operations only redistribute or suppress existing pixel information. They may make structures easier to see without proving what the unavailable original signal was.

### Misconception 2

> Increasing gamma always brightens an image.

### Why this is wrong in the source convention

For normalized values with `s = r^gamma`, gamma below one brightens darker intensities, while gamma above one darkens them.

### Misconception 3

> Thresholding and dithering produce the same kind of binary image.

### Why this is wrong

Hard thresholding makes an independent binary decision per pixel. Error-diffusion dithering redistributes quantization error spatially to preserve local tone perceptually.

### Misconception 4

> Histogram equalization and histogram matching solve the same problem.

### Why this is wrong

Equalization redistributes an image's own intensities; matching tries to make its distribution resemble a chosen reference.

### Misconception 5

> A larger smoothing kernel is always better for denoising.

### Why this is wrong

Stronger smoothing can remove noise but also erase edges and fine texture.

### Misconception 6

> Median filtering is just another weighted average.

### Why this is wrong

Median filtering ranks neighborhood values and selects the middle value; it is nonlinear and robust to outliers.

### Misconception 7

> Bilateral filtering and NLM use the same similarity rule.

### Why this is wrong

Bilateral filtering compares nearby pixels using distance and intensity; NLM compares patches and can use similar structures much farther away.

### Misconception 8

> BM3D is simply a 3D convolution.

### Why this is wrong

The source describes block matching, stacking similar patches into groups, collaborative transform-domain filtering, and aggregation.

### Misconception 9

> Wavelet fusion simply averages the input images pixel by pixel.

### Why this is wrong

The images are first decomposed into approximation/detail coefficients, and fusion rules are applied in wavelet space before reconstruction.

### Misconception 10

> Super-resolution with EDSR is equivalent to bicubic enlargement.

### Why this is wrong

Bicubic interpolation uses a fixed resampling rule, whereas EDSR uses learned residual features and pixel-shuffle upsampling.

---

## Key terminology

| Term | Meaning |
|---|---|
| Image enhancement | Processing intended to improve visual quality or emphasize useful features |
| Point transform | Pixel mapping where output depends only on the corresponding input pixel |
| Log transform | Nonlinear mapping used to redistribute intensity dynamic range |
| Gamma transform | Power-law intensity mapping |
| Brightness | Overall intensity level or offset-like visual attribute |
| Contrast | Degree of intensity separation between darker and brighter regions |
| Thresholding | Mapping intensities into discrete classes using a threshold |
| Halftoning | Simulating intermediate tones with spatial binary patterns |
| Dithering | Spatial redistribution of quantization error |
| Floyd–Steinberg | Error-diffusion dithering with weighted propagation to future pixels |
| Histogram stretching | Expanding occupied intensity range |
| Histogram equalization | CDF-based remapping to redistribute intensities |
| Adaptive histogram equalization | Local/block-wise histogram equalization |
| Histogram matching | Remapping source distribution toward a reference distribution |
| Fuzzification | Mapping a crisp value to fuzzy membership degrees |
| Defuzzification | Converting fuzzy output back to a crisp value |
| Gray World | White-balance assumption that average scene color should be neutral |
| Linear filter | Neighborhood operator based on weighted sums |
| Median filter | Rank filter selecting neighborhood median |
| Percentile filter | Rank filter selecting an arbitrary neighborhood percentile |
| Bilateral filter | Local smoother weighted by spatial and intensity similarity |
| Non-local means | Patch-similarity-based non-local denoising |
| BM3D | Block-matching collaborative transform-domain denoising |
| DWT | Discrete wavelet transform |
| LL/LH/HL/HH | Approximation and directional detail wavelet sub-bands |
| Zero-DCE | Zero-reference deep curve-estimation method for low-light enhancement |
| MAXIM | Multi-axis MLP restoration architecture |
| Dark Channel Prior | Statistical prior used for single-image haze removal |
| Transmission map | Estimated fraction of scene light reaching the camera through haze |
| EDSR | Enhanced Deep Residual Network for image super-resolution |
| Pixel shuffle | Sub-pixel rearrangement used for learned upsampling |

---

## Self-check

Before continuing, make sure you can answer:

1. How does enhancement differ from explicit model-based restoration in the chapter framing?
2. What makes a point transform "memoryless"?
3. Why is `+1` used inside a log transform?
4. What happens when gamma is below or above one?
5. How do brightness and contrast differ mathematically?
6. Why can hard thresholding create false contours?
7. How does random dithering reduce visible banding?
8. Why do Floyd–Steinberg weights sum to one?
9. How does histogram stretching differ from equalization?
10. Why might adaptive equalization reveal local details better than a single global mapping?
11. What are the four stages of the Mamdani fuzzy-inference system?
12. How does histogram matching use CDFs?
13. What assumption does Gray World make?
14. Why can Gaussian/box averaging perform poorly on impulse noise?
15. Why is the median robust to salt-and-pepper outliers?
16. What are the 0th, 50th, and 100th percentile filters?
17. What two similarities control a bilateral-filter weight?
18. How does NLM differ from bilateral smoothing?
19. What are the three recurring BM3D operations?
20. What information lives in LL versus LH/HL/HH wavelet bands?
21. How is a Streamlit UI separated from an enhancement engine?
22. What does Zero-DCE predict for each pixel?
23. What roles do spatial consistency, exposure, color, and illumination losses play?
24. What architectural idea distinguishes MAXIM in the chapter?
25. What observation motivates the Dark Channel Prior?
26. What is a transmission map?
27. Why is EDSR different from bicubic interpolation?
28. What role does pixel shuffle play in EDSR?

---

## Retain this idea

**Image enhancement is not one algorithm. It is a family of strategies that use different amounts of context—from a single pixel, to a neighborhood, to repeated patches, to multi-scale wavelet coefficients, to pretrained neural models. The best method depends on what is wrong with the image and what information must be preserved.**
        """,

        "estimated_minutes": 360,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "enhancement-mental-model",
                "title": "What Image Enhancement Is Trying to Achieve",
                "order": 1,
            },
            {
                "id": "point-transformations",
                "title": "Point-Wise Intensity Transformations",
                "order": 2,
            },
            {
                "id": "threshold-halftone-dither",
                "title": "Thresholding, Halftoning, and Dithering",
                "order": 3,
            },
            {
                "id": "histogram-processing",
                "title": "Histogram Modification and Equalization",
                "order": 4,
            },
            {
                "id": "fuzzy-histogram-matching",
                "title": "Fuzzy Contrast Enhancement and Histogram Matching",
                "order": 5,
            },
            {
                "id": "color-white-balance",
                "title": "Color Enhancement and White Balance",
                "order": 6,
            },
            {
                "id": "linear-smoothing",
                "title": "Linear Smoothing: Box and Gaussian Filters",
                "order": 7,
            },
            {
                "id": "nonlinear-order-filters",
                "title": "Nonlinear Order-Statistic Filters",
                "order": 8,
            },
            {
                "id": "edge-preserving-denoising",
                "title": "Bilateral Filtering and Non-Local Means",
                "order": 9,
            },
            {
                "id": "interactive-app-bm3d",
                "title": "Interactive Enhancement Workflow and BM3D",
                "order": 10,
            },
            {
                "id": "wavelet-fusion",
                "title": "Wavelet-Based Image Fusion",
                "order": 11,
            },
            {
                "id": "zero-dce-maxim",
                "title": "Advanced Enhancement: Zero-DCE and MAXIM",
                "order": 12,
            },
            {
                "id": "dehazing-superresolution",
                "title": "Dehazing with Dark Channel Prior and Super-Resolution with EDSR",
                "order": 13,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M07.L01.EX01",

            "title": "Build an Enhancement and Denoising Comparison",

            "lesson_code": "M07.L01",

            "section_id": "nonlinear-order-filters",

            "placement": "after_section",

            "description": (
                "Compare intensity enhancement and linear/nonlinear denoising methods while "
                "reasoning from the image problem rather than choosing filters blindly."
            ),

            "instructions": (
                "1. Choose one image with low contrast or poor brightness and create at "
                "least two point-transform versions using gamma, brightness, or contrast.\n"
                "2. Apply global histogram equalization and adaptive histogram equalization "
                "and compare local detail.\n"
                "3. Convert one clean image to grayscale and create two degraded versions: "
                "one with Gaussian-like noise and one with salt-and-pepper noise.\n"
                "4. Apply a Gaussian or box filter to both degraded images.\n"
                "5. Apply a median/50th-percentile filter to both degraded images.\n"
                "6. Compare which method is better suited to each noise type.\n"
                "7. On the Gaussian-noise example, also test bilateral filtering or "
                "non-local means.\n"
                "8. If the clean reference is available, compute PSNR for the noisy and "
                "denoised versions.\n"
                "9. Record one case where a stronger parameter removes more noise but also "
                "destroys image detail.\n"
                "10. Explain the final method choice using the assumed noise/image problem."
            ),

            "expected_output": (
                "A notebook or script showing point/histogram enhancement, Gaussian-noise "
                "and impulse-noise experiments, linear versus nonlinear denoising, optional "
                "bilateral/NLM results, PSNR where possible, and a short method-selection explanation."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "gamma-correction",
                "histogram-equalization",
                "gaussian-filter",
                "median-filter",
                "percentile-filter",
                "bilateral-filter",
                "non-local-means",
                "psnr",
                "method-selection",
            ],
        },

        {
            "id": "M07.L01.EX02",

            "title": "Create a Multi-Method Enhancement Demo",

            "lesson_code": "M07.L01",

            "section_id": "dehazing-superresolution",

            "placement": "after_section",

            "description": (
                "Connect the chapter's classical and advanced methods in a small enhancement "
                "demo that exposes the reason for choosing each technique."
            ),

            "instructions": (
                "1. Build a small Streamlit interface with image upload and an enhancement "
                "method selector.\n"
                "2. Include at least three classical methods from this lesson, such as "
                "gamma adjustment, histogram equalization, white balance, median denoising, "
                "or bilateral filtering.\n"
                "3. Keep UI code separate from the processing functions/module.\n"
                "4. Add original/enhanced side-by-side display and at least one parameter slider.\n"
                "5. Create one BM3D or NLM denoising comparison and report PSNR/SSIM if a "
                "clean reference is available.\n"
                "6. Perform one wavelet fusion experiment on two same-size grayscale images "
                "using mean or max coefficient fusion.\n"
                "7. Run or document inference for one advanced method from the chapter: "
                "Zero-DCE, pretrained MAXIM, Dark Channel Prior, or EDSR.\n"
                "8. For every method included, state the image problem it is intended to solve.\n"
                "9. Explain one artifact or failure mode that the user should inspect.\n"
                "10. Finish with a compact decision table mapping image problems to methods."
            ),

            "expected_output": (
                "A working or clearly structured Streamlit-based enhancement demo plus "
                "classical filtering results, one patch/multi-scale enhancement experiment, "
                "one advanced-method inference/result, and a concise problem-to-method guide."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "streamlit",
                "image-enhancement",
                "bm3d",
                "wavelet-fusion",
                "pretrained-model-inference",
                "software-modularity",
                "evaluation",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M07.L01.QZ01",

        "title": "Image Enhancement — Knowledge Check",

        "lesson_code": "M07.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M07.L01.Q01",
                "section_id": "point-transformations",
                "question": (
                    "For normalized intensities using the source chapter's power-law "
                    "mapping s = r^gamma, what is the typical effect of gamma < 1?"
                ),
                "options": [
                    "Dark regions become brighter",
                    "The image is converted to binary",
                    "Only edges remain",
                    "All RGB channels become identical",
                ],
                "correct": 0,
                "explanation": (
                    "The source explains that gamma below one expands lower intensities, "
                    "brightening darker regions."
                ),
            },

            {
                "id": "M07.L01.Q02",
                "section_id": "threshold-halftone-dither",
                "question": (
                    "Why does Floyd–Steinberg dithering distribute quantization error to "
                    "future pixels?"
                ),
                "options": [
                    "To preserve local average tone more effectively",
                    "To perform a Fourier transform",
                    "To create an RGB image from grayscale",
                    "To increase spatial resolution",
                ],
                "correct": 0,
                "explanation": (
                    "The residual error influences later decisions so local average "
                    "intensity better approximates the original image."
                ),
            },

            {
                "id": "M07.L01.Q03",
                "section_id": "histogram-processing",
                "question": (
                    "Which operation uses local image regions rather than one global "
                    "histogram mapping?"
                ),
                "options": [
                    "Adaptive histogram equalization",
                    "Histogram sliding only",
                    "Hard thresholding",
                    "White-patch balancing",
                ],
                "correct": 0,
                "explanation": (
                    "Adaptive histogram equalization performs localized contrast adjustment."
                ),
            },

            {
                "id": "M07.L01.Q04",
                "section_id": "fuzzy-histogram-matching",
                "question": (
                    "What does defuzzification do in the Mamdani enhancement system?"
                ),
                "options": [
                    "Converts the aggregated fuzzy output into a crisp numerical value",
                    "Splits RGB into channels",
                    "Computes an FFT",
                    "Creates random dithering noise",
                ],
                "correct": 0,
                "explanation": (
                    "After rule aggregation, centroid defuzzification produces one output intensity."
                ),
            },

            {
                "id": "M07.L01.Q05",
                "section_id": "color-white-balance",
                "question": "What assumption is used by the Gray World white-balance method?",
                "options": [
                    "Average scene color should be approximately neutral/gray",
                    "The darkest pixel must be pure black",
                    "Every image contains a white calibration card",
                    "The blue channel must always be strongest",
                ],
                "correct": 0,
                "explanation": (
                    "Gray World balances channels based on the assumption that their average "
                    "reflectance should be neutral."
                ),
            },

            {
                "id": "M07.L01.Q06",
                "section_id": "linear-smoothing",
                "question": (
                    "Why do box and Gaussian filters often perform poorly on strong "
                    "salt-and-pepper noise?"
                ),
                "options": [
                    "Averaging spreads extreme impulse values into nearby output pixels",
                    "They cannot process grayscale data",
                    "They always increase image resolution",
                    "They only work in the frequency domain",
                ],
                "correct": 0,
                "explanation": (
                    "Impulse noise contains outliers, and linear averaging allows those "
                    "outliers to influence neighboring results."
                ),
            },

            {
                "id": "M07.L01.Q07",
                "section_id": "nonlinear-order-filters",
                "question": (
                    "Which percentile filter is equivalent to a median filter?"
                ),
                "options": [
                    "50th percentile",
                    "0th percentile",
                    "100th percentile",
                    "25th percentile only",
                ],
                "correct": 0,
                "explanation": (
                    "The median is the middle ranked value, corresponding to the 50th percentile."
                ),
            },

            {
                "id": "M07.L01.Q08",
                "section_id": "edge-preserving-denoising",
                "question": (
                    "What extra criterion does a bilateral filter use in addition to spatial distance?"
                ),
                "options": [
                    "Intensity similarity",
                    "Filename similarity",
                    "Histogram size",
                    "Wavelet level",
                ],
                "correct": 0,
                "explanation": (
                    "Bilateral weights depend on both spatial proximity and range/intensity similarity."
                ),
            },

            {
                "id": "M07.L01.Q09",
                "section_id": "edge-preserving-denoising",
                "question": (
                    "What makes non-local means different from a local bilateral filter?"
                ),
                "options": [
                    "It compares patches and can use similar regions farther away",
                    "It always outputs a binary image",
                    "It ignores image structure",
                    "It requires a histogram reference image",
                ],
                "correct": 0,
                "explanation": (
                    "NLM uses patch similarity over a larger search region instead of only "
                    "local pixel similarity."
                ),
            },

            {
                "id": "M07.L01.Q10",
                "section_id": "interactive-app-bm3d",
                "question": "What are the three recurring operations in the BM3D pipeline?",
                "options": [
                    "Block matching, collaborative filtering, and aggregation",
                    "Thresholding, histogram matching, and gamma correction",
                    "FFT shift, notch masking, and inverse FFT",
                    "Cropping, rotation, and resizing",
                ],
                "correct": 0,
                "explanation": (
                    "Similar patches are found, grouped/filtered collaboratively, and then "
                    "aggregated back into the image."
                ),
            },

            {
                "id": "M07.L01.Q11",
                "section_id": "wavelet-fusion",
                "question": (
                    "Which wavelet sub-band contains the coarse low-frequency approximation?"
                ),
                "options": [
                    "LL",
                    "LH",
                    "HL",
                    "HH",
                ],
                "correct": 0,
                "explanation": (
                    "LL is the approximation sub-band; the other bands capture directional detail."
                ),
            },

            {
                "id": "M07.L01.Q12",
                "section_id": "zero-dce-maxim",
                "question": (
                    "What does Zero-DCE learn in the chapter's low-light enhancement formulation?"
                ),
                "options": [
                    "Per-pixel curve parameters applied iteratively",
                    "A single global threshold only",
                    "A fixed bicubic kernel",
                    "Only a histogram reference image",
                ],
                "correct": 0,
                "explanation": (
                    "The network predicts adaptive enhancement-curve parameters that are "
                    "applied iteratively to the image."
                ),
            },

            {
                "id": "M07.L01.Q13",
                "section_id": "dehazing-superresolution",
                "question": (
                    "What observation motivates the Dark Channel Prior used for dehazing?"
                ),
                "options": [
                    "Many haze-free outdoor patches contain a very low value in at least one color channel",
                    "All outdoor images have identical histograms",
                    "Haze only affects the red channel",
                    "Every hazy image has zero atmospheric light",
                ],
                "correct": 0,
                "explanation": (
                    "The dark-channel observation provides a cue for estimating haze and transmission."
                ),
            },

            {
                "id": "M07.L01.Q14",
                "section_id": "dehazing-superresolution",
                "question": (
                    "What distinguishes EDSR super-resolution from bicubic enlargement?"
                ),
                "options": [
                    "EDSR uses learned residual features and learned upsampling, while bicubic is a fixed interpolation rule",
                    "EDSR only changes the image file extension",
                    "Bicubic has trainable residual blocks",
                    "They are mathematically identical",
                ],
                "correct": 0,
                "explanation": (
                    "The chapter uses bicubic as a fixed baseline and EDSR as a learned "
                    "residual super-resolution model."
                ),
            },

            {
                "id": "M07.L01.Q15",
                "section_id": "dehazing-superresolution",
                "type": "open",
                "question": (
                    "A dataset contains underexposed images, some salt-and-pepper noise, "
                    "several hazy outdoor scenes, and low-resolution crops. Design an "
                    "enhancement workflow using methods from this lesson. For each problem, "
                    "name the technique you would try first, explain why it matches the "
                    "problem, and state one artifact or limitation you would inspect before "
                    "accepting the result."
                ),
            },
        ],

        "passing_score": 70,
    },
}
