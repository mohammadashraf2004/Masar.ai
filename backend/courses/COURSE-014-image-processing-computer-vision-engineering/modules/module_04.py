"""M04.L01 — Sampling and Fourier Transform.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 4. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M04.L01"

MODULE_ORDER = 4

MODULE_TITLE = "Sampling, Quantization, and Frequency-Domain Foundations"

MODULE_DESCRIPTION = (
    "Understand how continuous visual information becomes a digital image through "
    "sampling and quantization, then learn how the DFT/FFT represents images in the "
    "frequency domain and why magnitude, phase, transform bases, windowing, and DFT "
    "properties matter in practical image processing."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Sampling and Fourier Transform",

    "slug": "image-processing-m04-l01",

    "description": (
        "A learner-facing introduction to image sampling, interpolation, inpainting, "
        "downsampling, aliasing, anti-aliasing, quantization, the 2D DFT and FFT, "
        "magnitude and phase spectra, DCT and Walsh-Hadamard transforms, windowing, "
        "ringing, and fundamental Fourier properties."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 5.5,

    "skill_tags": [
        "image-processing",
        "sampling",
        "quantization",
        "interpolation",
        "inpainting",
        "anti-aliasing",
        "nyquist",
        "fourier-transform",
        "dft",
        "fft",
        "frequency-domain",
        "dct",
        "walsh-hadamard",
        "windowing",
        "gibbs-phenomenon",
        "parseval",
    ],

    "prerequisite_ids": ["M03.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Sampling and Fourier Transform",

        "content": r"""
# Sampling and Fourier Transform

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M04.L01  
> **Module:** Sampling, Quantization, and Frequency-Domain Foundations  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 4. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the difference between spatial sampling and intensity quantization.
- Compare nearest-neighbor, bilinear, bicubic, spline, and Lanczos interpolation.
- Explain why sparse interpolation and inpainting are related reconstruction problems.
- Describe the Nyquist–Shannon sampling criterion in image-processing terms.
- Recognize aliasing and explain why low-pass filtering reduces it before downsampling.
- Implement uniform intensity or color quantization and reason about quantization error.
- Explain the 2D discrete Fourier transform as a change from spatial representation to frequency representation.
- Compute a 2D FFT and inverse FFT and interpret magnitude, phase, and shifted spectra.
- Explain why phase contains crucial spatial-structure information.
- Describe DFT, DCT, and Walsh-Hadamard transforms as projections onto different basis functions.
- Explain separability, implicit periodicity, windowing, Gibbs/ringing artifacts, linearity, rotation, scaling, translation, and Parseval energy conservation.
- Connect these ideas to later tasks such as filtering, compression, restoration, and feature analysis.

---

## 1. How a visual signal becomes a digital image

A digital image can be thought of as a sampled and quantized version of a continuous visual signal.

There are two distinct steps:

### Sampling

Sampling answers:

> **Where do we measure the image?**

A continuous scene can conceptually be described by a function:

```text
f(x, y)
```

where `x` and `y` are continuous spatial coordinates.

A digital image only stores values on a discrete grid:

```text
f[m, n]
```

The spacing and number of grid points determine spatial resolution.

### Quantization

Quantization answers:

> **Which numerical values are allowed at each sampled position?**

Even after deciding where pixels exist, intensity or color could theoretically vary continuously. A computer stores one of a finite set of representable levels.

For example, an 8-bit grayscale image allows:

```text
0, 1, 2, ..., 255
```

### The distinction

```text
Sampling      -> discretizes spatial coordinates
Quantization  -> discretizes intensity/color values
```

This distinction is fundamental.

Changing width and height is primarily a **sampling/resampling** problem.

Reducing the number of gray levels or colors is a **quantization** problem.

[[IMAGE_NEEDED: Sampling versus quantization | Show a smooth continuous grayscale surface on the left, a spatial sampling grid in the middle, and the same samples restricted to a small number of intensity levels on the right | Learner should clearly distinguish discretizing position from discretizing pixel value]]

---

## 2. Upsampling and interpolation

Upsampling increases the number of spatial samples.

Suppose a small image is enlarged. The new grid contains pixel locations that did not exist in the original image.

Those values must be **estimated**.

That estimation process is interpolation.

### Nearest-neighbor interpolation

Nearest-neighbor interpolation chooses the closest original sample.

Conceptually:

```text
new_pixel = nearest_existing_pixel
```

Its strengths:

- very fast,
- preserves exact discrete values,
- useful for segmentation masks and label maps.

Its weaknesses:

- blocky appearance,
- jagged boundaries,
- no genuinely new intermediate intensity values.

[[IMAGE_NEEDED: Nearest-neighbor upsampling | Show a tiny 4×4 pixel grid enlarged several times with visible square blocks and duplicated values | Learner should notice that nearest-neighbor copies existing samples rather than estimating smooth transitions]]

### Bilinear interpolation

Bilinear interpolation uses the four neighboring pixels surrounding a target coordinate.

It computes a weighted average according to distance.

Conceptually:

```text
top-left ---- top-right
    \          /
     target point
    /          \
bottom-left -- bottom-right
```

The result is smoother than nearest-neighbor but can blur fine detail.

### Bicubic interpolation

Bicubic interpolation uses a larger neighborhood, usually 16 pixels, and cubic polynomials.

It often creates smoother and more visually natural results than bilinear interpolation, especially for larger enlargement factors.

Trade-offs include:

- more computation,
- possible ringing near sharp boundaries.

### Spline interpolation

Spline interpolation fits piecewise polynomials while enforcing smoothness across segment boundaries.

Cubic splines typically preserve continuity of:

- the function,
- the first derivative,
- the second derivative.

This makes splines valuable when smooth transitions matter, including scientific and medical reconstruction.

### Interpolation comparison

| Method | Neighborhood idea | Speed | Typical behavior |
|---|---|---:|---|
| Nearest | closest sample | fastest | blocky, discrete |
| Bilinear | 4 neighbors | fast | smooth but can blur |
| Bicubic | ~16 neighbors | moderate | smoother, possible ringing |
| Spline | piecewise polynomials | slower | very smooth reconstruction |
| Lanczos | windowed sinc neighborhood | moderate/slower | sharp resampling with good anti-aliasing behavior |

No interpolation method can recover information that was never captured. It only estimates a plausible value from available samples.

### Reconstructing from sparse samples

Interpolation also appears when only some pixels are known.

For example, SciPy can estimate an entire image from randomly sampled locations:

```python
from scipy import interpolate

reconstructed = interpolate.griddata(
    (sample_rows, sample_cols),
    sample_values,
    (Y, X),
    method="linear",
)
```

As the number of known samples increases, reconstruction generally becomes closer to the source image.

A practical caution:

> `griddata()` can return `NaN` outside the convex hull of the known sample coordinates.

### Inpainting as interpolation

Inpainting reconstructs missing or damaged regions.

If some pixels are unknown, the problem becomes:

```text
known coordinates + known values
            ↓
interpolation model
            ↓
estimated missing values
```

The chapter compares:

- nearest-neighbor interpolation,
- linear interpolation,
- radial basis function interpolation.

### Radial basis functions

An RBF depends primarily on distance from a center:

```text
phi(||x - c||)
```

The interpolated value is built as a weighted sum of basis functions centered at known samples, often with an additional low-degree polynomial term.

RBF interpolation can produce smooth results but can be computationally expensive for many known pixels.

Using a limited number of neighbors can reduce cost.

### Measuring reconstruction error

Mean squared error can quantify reconstruction:

```text
MSE = average((original - reconstruction)^2)
```

Lower MSE means the reconstruction is numerically closer to the reference.

The chapter also notes that perceptual metrics such as PSNR and SSIM can complement MSE.

### Spline filtering for denoising

Splines also appear as filters.

A spline filter can smooth noisy intensity variations:

```python
from scipy.ndimage import spline_filter

denoised = spline_filter(
    noisy,
    order=3,
    mode="nearest",
)
```

However, smoothing can reduce:

- noise,
- sharp edges,
- fine texture.

Denoising is therefore always a trade-off between noise suppression and detail preservation.

---

## 3. Downsampling, Nyquist, aliasing, and anti-aliasing

Downsampling reduces spatial resolution.

A simple approach could keep every `k`th sample:

```python
small = image[::k, ::k]
```

This is computationally simple but can produce serious artifacts.

### The Nyquist–Shannon idea

For a band-limited signal, perfect reconstruction requires a sampling frequency at least twice the highest frequency:

```text
fs >= 2 * fmax
```

For images, spatial frequency corresponds to how quickly intensities change across space.

Examples of high-frequency image content:

- narrow stripes,
- fine fabric,
- small repetitive patterns,
- sharp edges,
- dense text.

### What is aliasing?

If the sampling grid is too coarse to represent high-frequency structure, the sampled image may contain false lower-frequency patterns.

This is aliasing.

Common visual symptoms include:

- jagged lines,
- checkerboard-like artifacts,
- false stripes,
- Moiré patterns.

[[IMAGE_NEEDED: Nyquist and image aliasing | Show a fine stripe pattern at high resolution, a badly downsampled version with a Moiré pattern, and a properly low-pass-filtered/anti-aliased downsample | Learner should see high-frequency detail turning into false lower-frequency structure when undersampled]]

### Why anti-aliasing works

Before reducing resolution, high frequencies that cannot survive the new sampling rate should be attenuated.

This is commonly done with a low-pass filter.

A Gaussian low-pass filter is one practical option.

The processing idea is:

```text
high-resolution image
        ↓
low-pass filter
        ↓
remove frequencies new grid cannot represent
        ↓
downsample
```

### Lanczos resampling

Lanczos uses a windowed sinc kernel.

Its purpose is to approximate ideal band-limited reconstruction while keeping computation practical.

It often preserves more visual detail than nearest-neighbor while reducing aliasing during resizing.

With Pillow:

```python
from PIL import Image

small = image.resize(
    target_size,
    resample=Image.Resampling.LANCZOS,
)
```

### scikit-image anti-aliasing

With scikit-image:

```python
from skimage.transform import rescale

small = rescale(
    image,
    scale=0.3,
    channel_axis=-1,
    anti_aliasing=True,
)
```

The important concept is not the flag itself.

It is the ordering:

```text
filter first -> then sample more sparsely
```

{{exercise:M04.L01.EX01}}

---

## 4. Quantization and representation error

Quantization reduces the number of representable intensity or color values.

### Uniform quantization

Suppose a normalized grayscale image lies in:

```text
[0, 1]
```

If we want `L` output levels, divide the range into `L` intervals.

A simple implementation is:

```python
import numpy as np

def quantize_image(img, levels):
    img_min = img.min()
    img_max = img.max()

    step = (img_max - img_min) / levels

    quantized = (
        np.floor((img - img_min) / step) * step
        + step / 2
    )

    return np.clip(quantized, 0, 1)
```

Reducing the number of levels increases visible approximation.

For example:

```text
256 levels -> subtle quantization
16 levels  -> visible tonal simplification
4 levels   -> strong banding/posterization
```

[[IMAGE_NEEDED: Intensity quantization levels | Show one smooth grayscale photograph or gradient at high precision, 16 levels, 8 levels, and 4 levels | Learner should notice banding/contouring increasing as the number of allowed intensities decreases]]

### Quantization error

For an original value `f` and quantized value `q`:

```text
error = f - q
```

In uniform quantization, the maximum error is related to half the quantization step.

Reducing the number of levels increases:

- quantization error,
- contouring/banding,
- visible loss of subtle gradients.

### Non-uniform quantization

Not all value ranges are equally important.

Non-uniform quantization allocates more levels where additional precision is more valuable.

Possible criteria include:

- perceptual importance,
- image histogram density,
- optimized error.

Lloyd–Max quantization is one classical approach.

### Color quantization

For an RGB image, each color channel can be quantized, or the image can be mapped to a smaller optimized color palette.

Pillow supports adaptive palette quantization:

```python
quantized = image.quantize(colors=32)
```

As the number of colors decreases:

- storage may decrease,
- visual fidelity typically decreases,
- PSNR/SNR can decrease.

### Connection to JPEG

Quantization is central to lossy compression.

JPEG does not simply quantize raw pixels. It first transforms image blocks into a frequency-like DCT representation and then quantizes transform coefficients.

Higher-frequency coefficients often receive coarser quantization because they may be less visually important.

This is one reason DCT energy concentration matters.

---

## 5. From the spatial domain to the frequency domain

Until now, we have described an image directly by pixel intensities.

That is the **spatial domain**.

The discrete Fourier transform describes the same image using spatial-frequency components.

### Spatial intuition

Consider several patterns:

```text
slow brightness gradient -> low spatial frequency
wide stripes             -> lower frequency
narrow stripes           -> higher frequency
sharp edge               -> many frequencies
fine noise               -> strong high-frequency content
```

### The 2D DFT

For an image `f(x, y)`, the DFT produces complex-valued coefficients:

```text
F(u, v)
```

Each coefficient corresponds to a frequency basis pattern.

Instead of asking:

> What is the intensity at this pixel?

we can ask:

> How strongly is this frequency pattern present in the image?

### DFT and IDFT

The DFT moves from:

```text
spatial image -> frequency coefficients
```

The inverse DFT moves from:

```text
frequency coefficients -> spatial image
```

If all coefficients are preserved, the original image can be reconstructed to numerical precision.

### FFT

Directly evaluating the DFT formula is expensive.

The Fast Fourier Transform is an efficient algorithm for computing the same DFT.

In practice:

```python
import numpy as np

F = np.fft.fft2(image)
reconstructed = np.fft.ifft2(F).real
```

The FFT is not a different transform.

It is a faster algorithm for computing the DFT.

### Magnitude and phase

Fourier coefficients are complex:

```text
F = magnitude * exp(j * phase)
```

They contain two important components:

- **magnitude** — strength of the frequency component,
- **phase** — spatial alignment/structural information.

### Visualizing a spectrum

The zero-frequency component initially appears near a corner in standard FFT output.

For intuitive viewing:

```python
F_shifted = np.fft.fftshift(F)
```

This moves low frequencies toward the center.

Magnitude often has a huge dynamic range, so logarithmic scaling helps:

```python
spectrum = np.log1p(
    np.abs(F_shifted)
)
```

[[IMAGE_NEEDED: Spatial image, magnitude, and phase | Show one grayscale image beside its centered log-magnitude spectrum and phase spectrum; label center as low frequency and outer regions as higher frequency | Learner should connect the image to two complementary Fourier representations]]

### The DC component

The zero-frequency or **DC component** reflects the average intensity of the image.

Because it can be much larger than other coefficients, it often dominates an unscaled spectrum.

### Frequency direction

A useful property:

> Strong spatial edges tend to produce frequency energy in a direction perpendicular to the edge orientation.

Periodic structures can produce localized peaks in the frequency spectrum.

A rectangle or square generates a sinc-like spectral pattern due to its sharp spatial boundaries.

---

## 6. Why Fourier phase matters

The magnitude spectrum may look visually organized, while phase can appear noisy or random.

That can mislead beginners into assuming phase is unimportant.

It is not.

### Magnitude

Magnitude answers approximately:

> How much of this frequency is present?

### Phase

Phase answers approximately:

> How are these frequency components aligned in space?

Image structure depends strongly on those alignments.

Experiments in the chapter combine:

- magnitude from one image,
- phase from another,
- random magnitude,
- random phase,
- zero phase.

The central result is:

> Preserving phase often preserves much more recognizable spatial structure than preserving magnitude alone.

A useful mental model is:

```text
magnitude -> frequency strength
phase     -> spatial arrangement
```

Both are required for faithful reconstruction.

[[IMAGE_NEEDED: Magnitude versus phase reconstruction | Show two source images, reconstruction using magnitude from A + phase from B, and reconstruction using phase from A + unrelated magnitude; include a random-phase example | Learner should notice that phase strongly controls recognizable structure]]

### Random textures

The chapter uses a fractional Brownian field to generate a random texture and then substitutes its magnitude or phase into Fourier reconstructions.

You do not need to memorize that specific texture model.

Its educational role is to supply an unrelated frequency representation for testing the importance of phase.

---

## 7. DFT, DCT, and Walsh-Hadamard as basis transforms

A powerful way to understand transforms is:

> A transform expresses an image as a weighted combination of basis patterns.

### Matrix view of the DFT

For a square image matrix `X`, the DFT can be expressed using a Fourier basis matrix `W`.

Conceptually:

```text
F = W X W
```

with normalization choices depending on the convention.

The inverse uses the inverse or Hermitian-related transform matrix.

This matrix formulation is slower than FFT algorithms for large images, but it makes the mathematics visible.

### Orthonormal basis

With suitable normalization, basis vectors can be orthonormal.

That means they are:

- mutually perpendicular in vector-space terms,
- unit length.

An orthonormal basis lets us decompose and reconstruct signals cleanly.

### Discrete Cosine Transform

The DCT uses cosine basis functions.

It is important in compression because natural images often concentrate a large amount of energy into a relatively small set of low-frequency DCT coefficients.

Conceptually:

```text
image
  ↓ project onto cosine patterns
DCT coefficients
```

This energy concentration is a major reason DCT-like processing is useful in JPEG.

[[IMAGE_NEEDED: DCT basis and energy concentration | Show a small grid of low-order 2D DCT basis patterns plus a DCT spectrum whose strong coefficients cluster near the low-frequency origin | Learner should see that the image can be represented as weights on cosine patterns and that much energy often concentrates in a small region]]

### Walsh-Hadamard Transform

The Walsh-Hadamard transform uses basis patterns containing only:

```text
+1 and -1
```

This makes it computationally simple because the transform can rely heavily on additions and subtractions.

Hadamard basis vectors can be reordered by **sequency**, which is analogous to ordering by the number of sign changes.

Low-sequency patterns vary slowly.

High-sequency patterns change signs more frequently.

### Basis images

For 2D transforms, each pair of basis indices corresponds to a 2D basis image.

Examples:

- smooth low-frequency cosine basis,
- rapidly varying cosine basis,
- block-like Walsh patterns.

This provides a visual interpretation of coefficients:

```text
coefficient = how much of this basis image is present
```

### Comparing DFT, DCT, and WHT

| Transform | Basis type | Key characteristic |
|---|---|---|
| DFT | complex sinusoids | explicit magnitude + phase representation |
| DCT | real cosines | strong energy compaction in many natural images |
| WHT | ±1 Walsh/Hadamard patterns | efficient arithmetic and sequency structure |

---

## 8. DFT properties: separability, periodicity, and windowing

### Separability

A 2D DFT can be computed by:

1. applying 1D DFTs along one axis,
2. applying 1D DFTs along the other axis.

In NumPy:

```python
def fft2_separable(f):
    return np.fft.fft(
        np.fft.fft(f).T
    ).T
```

This should agree with:

```python
np.fft.fft2(f)
```

The conceptual lesson is that a 2D transform can be decomposed into successive 1D transforms.

### Why separability matters

It reduces computational complexity and makes implementation more efficient.

Fast separable algorithms are one reason Fourier methods are practical for real images.

### Implicit periodicity

The DFT behaves as if the finite image repeats periodically in both directions.

Imagine tiling the image:

```text
A A A
A A A
A A A
```

If the left and right boundaries or top and bottom boundaries do not match smoothly, tiling creates artificial discontinuities.

Sharp discontinuities introduce high-frequency energy.

Therefore, the spectrum can contain strong components caused by the **image boundary**, not only by meaningful internal structure.

{{image:dft-periodic-extension}}

### Windowing

Windowing multiplies the image by a smooth function that is large near the center and tapers toward the boundaries.

Conceptually:

```text
windowed_image = image * window
```

This reduces boundary discontinuities before the DFT.

Different windows create different trade-offs, but the shared purpose is to reduce spectral leakage caused by abrupt boundaries.

### Important trade-off

Windowing modifies the image.

It reduces edge discontinuities but also attenuates information near the borders.

So windowing is not "free cleanup"; it changes the signal to improve frequency analysis.

---

## 9. Ringing artifacts and the Gibbs phenomenon

A sharp edge is a rapid spatial transition.

Representing a perfect discontinuity requires many frequency components.

If the frequency representation is truncated or strongly low-pass filtered, reconstruction near the edge can show oscillations.

These oscillations are called **ringing**.

The related mathematical behavior is the **Gibbs phenomenon**.

### A simple example

Consider a binary image:

```text
black background
white circle
very sharp boundary
```

The boundary contains strong high-frequency information.

Its spectrum contains oscillatory structure.

If high frequencies are removed or limited, reconstruction near the sharp transition can overshoot and oscillate.

### Smoothing before the transform

A Gaussian filter softens the edge:

```python
from skimage.filters import gaussian

smoothed = gaussian(
    binary_image,
    sigma=5,
)
```

This suppresses high-frequency content.

The resulting Fourier spectrum contains less extreme high-frequency structure.

[[IMAGE_NEEDED: Gibbs ringing and smoothing | Show a sharp binary circle, its Fourier spectrum with oscillatory structure, a Gaussian-smoothed circle, and its smoother spectrum/reconstruction | Learner should connect sharp discontinuities to high-frequency content and ringing behavior]]

### Important nuance

Low-pass filtering can reduce high-frequency noise and ringing, but it also blurs legitimate fine detail.

Again, image processing is a trade-off.

---

## 10. Transform laws: linearity, rotation, scaling, translation, and energy

Several DFT properties make frequency-domain reasoning powerful.

### Linearity

For images `f1` and `f2` and constants `a`, `b`:

```text
DFT(a f1 + b f2)
=
a DFT(f1) + b DFT(f2)
```

This means transforms distribute over linear combinations.

### Rotation

If the spatial image is rotated, its frequency structure rotates correspondingly.

This is useful for understanding directional texture and orientation.

### Scaling

Spatial scaling and frequency scaling have an inverse relationship.

Conceptually:

```text
stretch in space
       ↓
contract in frequency

compress in space
       ↓
expand in frequency
```

This reflects a broader uncertainty-like relationship between localization in one domain and spread in the other.

### Translation and phase

A spatial shift changes Fourier phase but does not change the magnitude spectrum.

That means two identical objects at different positions can have the same Fourier magnitude but different phase.

This reinforces why phase carries location and structural information.

[[IMAGE_NEEDED: Fourier transform property summary | A four-panel figure showing spatial rotation with rotated spectrum, spatial stretching with contracted spectrum, spatial translation with unchanged magnitude but changed phase, and linear addition in spatial/frequency domains | Learner should visually connect common spatial operations with their Fourier consequences]]

### Parseval / Rayleigh energy conservation

Parseval's theorem states that signal energy is conserved across the spatial and frequency representations, subject to the transform's normalization convention.

Conceptually:

```text
energy in pixels
≈
properly normalized energy in Fourier coefficients
```

This tells us the Fourier transform redistributes information into a new coordinate system rather than creating or destroying the underlying signal energy.

### Why these properties matter

They provide reasoning tools.

Instead of treating the Fourier spectrum as a mysterious image, you can predict how it should behave when the spatial image is:

- shifted,
- rotated,
- stretched,
- added to another image,
- windowed,
- smoothed.

{{exercise:M04.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Sampling and quantization are the same operation.

### Why this is wrong

Sampling discretizes **where** values are measured. Quantization discretizes **which values** can be represented.

### Misconception 2

> Upsampling creates new true detail.

### Why this is wrong

Interpolation estimates missing values from existing samples. It may create a visually smoother image, but it cannot recover genuinely uncaptured information.

### Misconception 3

> Downsampling can be done safely by simply deleting rows and columns.

### Why this is incomplete

If high-frequency structure is present, undersampling can create aliasing. Low-pass filtering or appropriate resampling is often necessary first.

### Misconception 4

> FFT and DFT are different frequency transforms.

### Why this is wrong

The DFT is the transform. FFT refers to efficient algorithms used to compute the DFT.

### Misconception 5

> The Fourier magnitude contains the whole important image structure.

### Why this is wrong

Phase carries crucial spatial alignment information. Replacing phase can severely destroy recognizable structure even if magnitude is preserved.

### Misconception 6

> The DFT spectrum only represents features inside the image.

### Why this is wrong

Because the DFT assumes periodic repetition, discontinuities at image boundaries can create artificial high-frequency components. Windowing is often used to reduce these effects.

### Misconception 7

> Anti-aliasing and smoothing are always beneficial.

### Why this is wrong

They suppress high-frequency content, which can include both unwanted alias-causing detail and legitimate edges/textures.

---

## Key terminology

| Term | Meaning |
|---|---|
| Sampling | Selecting discrete spatial positions from a continuous or higher-resolution signal |
| Quantization | Mapping values to a finite set of allowed levels |
| Upsampling | Increasing spatial sample count |
| Downsampling | Decreasing spatial sample count |
| Interpolation | Estimating values at unsampled coordinates |
| Nearest-neighbor | Interpolation using the closest known sample |
| Bilinear | Interpolation using four neighboring samples |
| Bicubic | Cubic interpolation using a larger neighborhood, typically 16 pixels |
| Spline | Piecewise-polynomial interpolation with smooth derivative constraints |
| Inpainting | Estimating missing or damaged image regions |
| RBF | Radial basis function depending on distance from a center |
| Nyquist frequency | Highest frequency representable without aliasing at a given sampling rate |
| Aliasing | False low-frequency structure created by undersampling high frequencies |
| Anti-aliasing | Suppressing high frequencies before/reducing sampling density |
| Low-pass filter | Filter that attenuates higher-frequency components |
| Lanczos | Windowed-sinc resampling kernel |
| Quantization error | Difference between original and quantized value |
| Spatial domain | Image representation directly by pixel coordinates and intensities |
| Frequency domain | Representation by spatial-frequency coefficients |
| DFT | Discrete Fourier transform |
| IDFT | Inverse discrete Fourier transform |
| FFT | Efficient family of algorithms for computing the DFT |
| Magnitude spectrum | Strength of Fourier frequency components |
| Phase spectrum | Angular component encoding spatial alignment/structure |
| DC component | Zero-frequency coefficient related to mean intensity |
| DCT | Discrete cosine transform |
| WHT | Walsh-Hadamard transform |
| Basis image | One spatial pattern used to represent a transform component |
| Separability | Ability to compute a 2D transform using successive 1D transforms |
| Windowing | Tapering image boundaries to reduce periodic-edge spectral artifacts |
| Gibbs phenomenon | Oscillatory overshoot near discontinuities in truncated spectral representations |
| Parseval theorem | Conservation of appropriately normalized signal energy across domains |

---

## Self-check

Before continuing, make sure you can answer:

1. What is the difference between sampling and quantization?
2. Why does upsampling require interpolation?
3. When is nearest-neighbor interpolation preferable to bilinear or bicubic interpolation?
4. Why can `griddata()` leave missing values outside the convex hull of known samples?
5. How is interpolation-based inpainting related to ordinary interpolation?
6. What does the Nyquist criterion mean for a striped image?
7. Why can fine fabric produce Moiré patterns after downsampling?
8. Why should low-pass filtering often happen before downsampling?
9. What visual effect occurs when the number of quantization levels becomes very small?
10. What is the difference between the DFT and FFT?
11. What does `fftshift()` change: the transform itself or only how coefficients are arranged for viewing?
12. What information does Fourier magnitude represent?
13. Why is Fourier phase essential for reconstruction?
14. Why is DCT useful for compression?
15. How is the Walsh-Hadamard basis different from the Fourier basis?
16. What does DFT separability mean?
17. Why can image boundaries introduce unwanted spectral components?
18. What trade-off does windowing introduce?
19. Why do sharp transitions create strong high-frequency content?
20. What happens to the magnitude spectrum when an image is translated?
21. How does spatial stretching affect frequency spread?
22. What does Parseval's theorem tell us?

---

## Retain this idea

**A digital image is created by discretizing space and value, and the Fourier transform gives us a second way to describe that same image—not by where pixels are, but by which spatial-frequency patterns combine to form it. Sampling determines what information can exist in the digital image; phase and frequency structure help explain how that information is organized.**
        """,

        "estimated_minutes": 330,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "sampling-quantization-model",
                "title": "How a Visual Signal Becomes a Digital Image",
                "order": 1,
            },
            {
                "id": "upsampling-interpolation",
                "title": "Upsampling and Interpolation",
                "order": 2,
            },
            {
                "id": "downsampling-aliasing",
                "title": "Downsampling, Nyquist, Aliasing, and Anti-Aliasing",
                "order": 3,
            },
            {
                "id": "quantization",
                "title": "Quantization and Representation Error",
                "order": 4,
            },
            {
                "id": "dft-fft-foundations",
                "title": "From the Spatial Domain to the Frequency Domain",
                "order": 5,
            },
            {
                "id": "magnitude-phase",
                "title": "Why Fourier Phase Matters",
                "order": 6,
            },
            {
                "id": "transform-bases",
                "title": "DFT, DCT, and Walsh-Hadamard as Basis Transforms",
                "order": 7,
            },
            {
                "id": "dft-properties",
                "title": "DFT Properties: Separability, Periodicity, and Windowing",
                "order": 8,
            },
            {
                "id": "ringing-gibbs",
                "title": "Ringing Artifacts and the Gibbs Phenomenon",
                "order": 9,
            },
            {
                "id": "fourier-transform-laws",
                "title": "Transform Laws: Linearity, Rotation, Scaling, Translation, and Energy",
                "order": 10,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M04.L01.EX01",

            "title": "Investigate Sampling, Aliasing, and Quantization",

            "lesson_code": "M04.L01",

            "section_id": "downsampling-aliasing",

            "placement": "after_section",

            "description": (
                "Build intuition for how interpolation, anti-aliasing, sampling density, "
                "and quantization affect image information."
            ),

            "instructions": (
                "1. Choose an image containing fine repeating detail such as fabric, text, "
                "roof tiles, fences, or narrow stripes.\n"
                "2. Enlarge a small crop using nearest-neighbor, bilinear, and bicubic "
                "interpolation and compare the visible differences.\n"
                "3. Downsample the same high-frequency crop strongly using nearest-neighbor "
                "or direct slicing and record any jagged or Moiré artifacts.\n"
                "4. Downsample again using an anti-aliased method such as Lanczos or "
                "skimage.transform.rescale(..., anti_aliasing=True).\n"
                "5. Explain which high-frequency structures were responsible for the "
                "largest aliasing artifacts.\n"
                "6. Convert one grayscale version to 16, 8, and 4 quantization levels.\n"
                "7. Compute MSE between the original normalized grayscale image and each "
                "quantized result.\n"
                "8. Explain separately what information was lost because of sampling and "
                "what was lost because of quantization."
            ),

            "expected_output": (
                "A notebook or script showing interpolation comparisons, aliased and "
                "anti-aliased downsampling, several quantized images, a small error table, "
                "and a written distinction between sampling loss and quantization loss."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "interpolation",
                "downsampling",
                "aliasing",
                "anti-aliasing",
                "nyquist-reasoning",
                "quantization",
                "mse",
            ],
        },

        {
            "id": "M04.L01.EX02",

            "title": "Read an Image Through Its Fourier Spectrum",

            "lesson_code": "M04.L01",

            "section_id": "fourier-transform-laws",

            "placement": "after_section",

            "description": (
                "Use FFT experiments to connect visible spatial structure with magnitude, "
                "phase, periodic boundaries, and transform properties."
            ),

            "instructions": (
                "1. Load a grayscale image and compute its 2D FFT.\n"
                "2. Display the centered log-magnitude spectrum and phase spectrum.\n"
                "3. Reconstruct the image with IFFT and verify numerical closeness to the "
                "original using np.allclose() or a reconstruction error.\n"
                "4. Translate the image spatially, recompute its FFT, and compare magnitude "
                "and phase with the original.\n"
                "5. Rotate the image and observe the corresponding rotation of dominant "
                "frequency directions.\n"
                "6. Create a simple binary shape with sharp boundaries, compute its "
                "spectrum, then smooth it with a Gaussian and recompute the spectrum.\n"
                "7. Apply a window to an image whose opposite boundaries differ strongly "
                "and compare the spectrum before and after windowing.\n"
                "8. Verify Parseval-style energy consistency using the normalization "
                "convention of your FFT implementation.\n"
                "9. Explain which observations were predicted by translation, rotation, "
                "windowing, and high-frequency suppression properties."
            ),

            "expected_output": (
                "A notebook or script with original/reconstructed images, magnitude and "
                "phase spectra, translation and rotation comparisons, sharp-versus-smoothed "
                "spectra, a windowing comparison, one energy calculation, and concise "
                "interpretations of each Fourier property."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "fft2",
                "ifft2",
                "magnitude-spectrum",
                "phase-spectrum",
                "fftshift",
                "windowing",
                "gibbs-phenomenon",
                "translation-property",
                "rotation-property",
                "parseval",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M04.L01.QZ01",

        "title": "Sampling and Fourier Transform — Knowledge Check",

        "lesson_code": "M04.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M04.L01.Q01",
                "section_id": "sampling-quantization-model",
                "question": "What is the main difference between sampling and quantization?",
                "options": [
                    "Sampling chooses spatial positions; quantization restricts representable values",
                    "Sampling restricts values; quantization chooses spatial positions",
                    "Sampling only applies to color images",
                    "They are two names for the same operation",
                ],
                "correct": 0,
                "explanation": (
                    "Sampling discretizes coordinates, while quantization discretizes "
                    "intensity or color values."
                ),
            },

            {
                "id": "M04.L01.Q02",
                "section_id": "upsampling-interpolation",
                "question": (
                    "Why does nearest-neighbor interpolation often produce a blocky result?"
                ),
                "options": [
                    "It invents too many intermediate intensities",
                    "It copies the closest existing sample instead of estimating smooth transitions",
                    "It always converts images to binary",
                    "It performs a Fourier transform before resizing",
                ],
                "correct": 1,
                "explanation": (
                    "Nearest-neighbor repeats existing samples, so enlarged pixels appear "
                    "as visible blocks."
                ),
            },

            {
                "id": "M04.L01.Q03",
                "section_id": "downsampling-aliasing",
                "question": (
                    "What is the main reason for low-pass filtering before strong downsampling?"
                ),
                "options": [
                    "To add more color channels",
                    "To suppress frequencies the lower sampling rate cannot represent reliably",
                    "To increase file metadata",
                    "To make the image periodic",
                ],
                "correct": 1,
                "explanation": (
                    "High frequencies above the new Nyquist limit would otherwise alias "
                    "into false lower-frequency structures."
                ),
            },

            {
                "id": "M04.L01.Q04",
                "section_id": "quantization",
                "question": (
                    "What usually happens as the number of intensity quantization levels decreases?"
                ),
                "options": [
                    "Quantization error decreases",
                    "Spatial resolution increases",
                    "Banding/contouring and approximation error become more visible",
                    "Fourier phase becomes zero",
                ],
                "correct": 2,
                "explanation": (
                    "Fewer allowed values force more original intensities onto the same "
                    "representative levels."
                ),
            },

            {
                "id": "M04.L01.Q05",
                "section_id": "dft-fft-foundations",
                "question": "Which statement correctly relates the FFT and DFT?",
                "options": [
                    "FFT is a completely different transform from DFT",
                    "FFT is an efficient family of algorithms for computing the DFT",
                    "DFT is only for continuous signals",
                    "FFT removes phase information",
                ],
                "correct": 1,
                "explanation": (
                    "The DFT defines the transform; FFT algorithms compute it efficiently."
                ),
            },

            {
                "id": "M04.L01.Q06",
                "section_id": "dft-fft-foundations",
                "question": (
                    "What does np.fft.fftshift() mainly do for a 2D spectrum?"
                ),
                "options": [
                    "Changes the underlying Fourier coefficients",
                    "Rearranges coefficients so the zero/low-frequency region is centered for viewing",
                    "Removes all high frequencies",
                    "Converts phase into magnitude",
                ],
                "correct": 1,
                "explanation": (
                    "fftshift rearranges coefficient positions for interpretation; it does "
                    "not compute a new transform."
                ),
            },

            {
                "id": "M04.L01.Q07",
                "section_id": "magnitude-phase",
                "question": (
                    "Why can an image reconstructed with incorrect Fourier phase become unrecognizable?"
                ),
                "options": [
                    "Phase strongly controls spatial alignment and structure",
                    "Phase only stores the image file name",
                    "Magnitude becomes zero automatically",
                    "Phase changes image dimensions",
                ],
                "correct": 0,
                "explanation": (
                    "Fourier phase contains crucial information about how frequency "
                    "components align spatially."
                ),
            },

            {
                "id": "M04.L01.Q08",
                "section_id": "transform-bases",
                "question": (
                    "Why is the DCT particularly useful in image compression?"
                ),
                "options": [
                    "It always turns images into binary masks",
                    "It often concentrates much of a natural image's energy into relatively few low-frequency coefficients",
                    "It eliminates the need for quantization",
                    "It preserves only phase",
                ],
                "correct": 1,
                "explanation": (
                    "Energy compaction allows many less-important coefficients to be "
                    "represented more coarsely or discarded in compression schemes."
                ),
            },

            {
                "id": "M04.L01.Q09",
                "section_id": "dft-properties",
                "question": (
                    "Why can a finite image produce unexpected horizontal or vertical spectral artifacts?"
                ),
                "options": [
                    "The DFT implicitly treats the image as periodically repeated, so boundary jumps create high frequencies",
                    "The DFT automatically adds grid lines",
                    "Every grayscale image contains vertical stripes",
                    "fftshift creates new edges",
                ],
                "correct": 0,
                "explanation": (
                    "Periodic repetition can create discontinuities where opposite image "
                    "boundaries meet."
                ),
            },

            {
                "id": "M04.L01.Q10",
                "section_id": "ringing-gibbs",
                "question": (
                    "What image feature most strongly promotes Gibbs/ringing behavior?"
                ),
                "options": [
                    "Very smooth constant regions only",
                    "Sharp intensity discontinuities",
                    "A single global mean value",
                    "An alpha channel",
                ],
                "correct": 1,
                "explanation": (
                    "Abrupt transitions require strong high-frequency content; limiting the "
                    "spectral representation produces oscillatory behavior near the edge."
                ),
            },

            {
                "id": "M04.L01.Q11",
                "section_id": "fourier-transform-laws",
                "question": (
                    "What happens to Fourier magnitude when an image is translated without otherwise changing it?"
                ),
                "options": [
                    "The magnitude spectrum is unchanged while phase changes",
                    "The magnitude becomes all zeros",
                    "The magnitude rotates by 90 degrees",
                    "The frequency domain disappears",
                ],
                "correct": 0,
                "explanation": (
                    "Spatial translation introduces a phase shift but preserves Fourier magnitude."
                ),
            },

            {
                "id": "M04.L01.Q12",
                "section_id": "fourier-transform-laws",
                "question": (
                    "What does Parseval's theorem express in this context?"
                ),
                "options": [
                    "Properly normalized signal energy is conserved between spatial and frequency domains",
                    "Every image must be square",
                    "All frequencies have equal magnitude",
                    "Quantization introduces no error",
                ],
                "correct": 0,
                "explanation": (
                    "The transform redistributes the signal into a different basis while "
                    "preserving total energy under the appropriate normalization."
                ),
            },

            {
                "id": "M04.L01.Q13",
                "section_id": "fourier-transform-laws",
                "type": "open",
                "question": (
                    "You must shrink a fine-striped image and then analyze its dominant "
                    "frequency directions. Describe a correct pipeline from anti-aliasing "
                    "through downsampling to FFT visualization. Explain what could go wrong "
                    "if you skip anti-aliasing, why fftshift/log magnitude are useful for "
                    "visualization, and what phase contributes beyond magnitude."
                ),
            },
        ],

        "passing_score": 70,
    },
}
