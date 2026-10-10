"""M06.L01 — Frequency Domain Filtering.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 6. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M06.L01"

MODULE_ORDER = 6

MODULE_TITLE = "Frequency Domain Filtering"

MODULE_DESCRIPTION = (
    "Learn how to design and apply low-pass, high-pass, band-pass, and band-stop "
    "filters in Fourier space; compare Ideal, Butterworth, and Gaussian responses; "
    "remove periodic noise; reason about cutoff frequency and reconstruction quality; "
    "and understand how Fourier feature mappings help neural networks represent "
    "high-frequency image detail."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Frequency Domain Filtering",

    "slug": "image-processing-m06-l01",

    "description": (
        "A practical lesson on filtering images in Fourier space with low-pass, "
        "high-pass, band-pass, and band-stop filters, including Ideal, Butterworth, "
        "and Gaussian designs, denoising and periodic-noise removal, cutoff-frequency "
        "trade-offs, and an introduction to Fourier Feature Networks for image reconstruction."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 5.0,

    "skill_tags": [
        "image-processing",
        "frequency-domain-filtering",
        "fft",
        "low-pass-filter",
        "high-pass-filter",
        "band-pass-filter",
        "band-stop-filter",
        "notch-filter",
        "butterworth",
        "gaussian-filter",
        "periodic-noise",
        "psnr",
        "fourier-features",
        "neural-fields",
        "jax",
        "image-reconstruction",
    ],

    "prerequisite_ids": ["M05.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Frequency Domain Filtering",

        "content": r"""
# Frequency Domain Filtering

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M06.L01  
> **Module:** Frequency Domain Filtering  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 6. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what an image filter does in both the spatial and frequency domains.
- Build the standard FFT → filter mask → IFFT frequency-domain filtering pipeline.
- Distinguish low-pass, high-pass, band-pass, and band-stop/notch filters.
- Compare Ideal, Butterworth, and Gaussian frequency responses.
- Explain how cutoff frequency changes smoothness, edge emphasis, and reconstruction quality.
- Use PSNR to compare filtered output with a reference image.
- Apply low-pass filtering for denoising and high-pass filtering for detail/edge emphasis.
- Explain why periodic noise creates localized peaks or lines in a Fourier spectrum.
- Design a notch or band-stop strategy to suppress periodic interference.
- Understand Difference of Gaussians as a band-selective operation.
- Use Fourier-domain filtering functions from NumPy/SciPy/scikit-image.
- Explain the motivation for Fourier Feature Networks.
- Describe sinusoidal positional encoding as a mapping from image coordinates to frequency-rich features.
- Explain why the frequency scale of Fourier features affects image reconstruction.
- Interpret training/test PSNR curves and recognize overfitting in coordinate-based neural networks.

---

## 1. What is a frequency-domain filter?

Filtering means transforming an image so that some characteristics become more useful.

Typical goals include:

- smoothing,
- noise reduction,
- contrast/detail enhancement,
- edge emphasis,
- suppression of unwanted periodic structure,
- isolation of a particular frequency range.

In the spatial domain, we manipulate pixels or local neighborhoods directly.

In the frequency domain, we manipulate the image's Fourier coefficients.

The basic idea is:

```text
spatial image
    ↓ FFT
frequency representation
    ↓ multiply by filter mask
filtered frequency representation
    ↓ IFFT
filtered image
```

This works because Fourier coefficients describe how strongly different spatial-frequency patterns occur in the image.

### Frequency interpretation

A useful mental model is:

```text
low spatial frequencies
    -> slow intensity changes
    -> broad illumination and coarse shape

high spatial frequencies
    -> rapid intensity changes
    -> edges, fine texture, some forms of noise
```

This is not a perfect one-to-one classification. Real edges contain many frequencies, and noise can occupy different parts of the spectrum. But it is a strong starting point.

[[IMAGE_NEEDED: Frequency filtering pipeline | Show one grayscale image, its centered Fourier magnitude spectrum, a circular filter mask, the masked spectrum, and the reconstructed output | Learner should understand that frequency filtering is coefficient selection/attenuation followed by inverse transformation]]

---

## 2. Four main filter types

From the frequency-domain perspective, this chapter focuses on four families.

### Low-pass filter (LPF)

An LPF preserves lower frequencies and attenuates higher frequencies.

Typical effects:

- smoothing,
- blur,
- high-frequency noise reduction,
- removal of fine texture.

### High-pass filter (HPF)

An HPF suppresses low frequencies and preserves higher frequencies.

Typical effects:

- edge emphasis,
- detail extraction,
- sharpening-like behavior,
- removal of broad smooth variations.

### Band-pass filter (BPF)

A BPF preserves only a selected interval of frequencies.

Typical uses:

- isolate a scale of detail,
- feature extraction,
- emphasize mid-frequency structure.

### Band-stop / band-reject / notch filter

A band-stop filter suppresses selected frequency ranges while retaining frequencies outside them.

A narrow band-stop filter is often called a **notch filter**.

Typical use:

- periodic interference removal.

[[IMAGE_NEEDED: LPF HPF BPF and BSF masks | Show four centered radial frequency masks: low-pass bright center, high-pass dark center, band-pass bright ring, and band-stop dark ring/notches | Learner should visually associate each filter name with which frequency region is preserved]]

### A radial coordinate

Many frequency-domain filters use distance from the centered frequency origin:

```text
D(u, v) = sqrt(u^2 + v^2)
```

where `(u, v)` is a frequency coordinate measured relative to the center after `fftshift()`.

A cutoff frequency `D0` defines where the filter begins to attenuate or reject frequencies.

---

## 3. Ideal, Butterworth, and Gaussian filter shapes

The same logical filter type can be implemented with different transition shapes.

### Ideal filter

An ideal low-pass filter uses a hard boundary:

```text
H(u, v) = 1  when D(u,v) < D0
H(u, v) = 0  otherwise
```

This is easy to understand:

```text
inside cutoff -> keep
outside cutoff -> remove
```

But the abrupt frequency cutoff can introduce ringing in the spatial-domain reconstruction.

### Gaussian filter

A Gaussian low-pass response changes smoothly with distance.

Conceptually:

```text
H(D) = exp(-D^2 / (2 * D0^2))
```

There is no sudden boundary.

This smooth transition helps reduce ringing compared with a hard ideal cutoff.

### Butterworth filter

The Butterworth response lies between the ideal and Gaussian styles.

A common low-pass form is:

```text
H(D) = 1 / (1 + (D / D0)^(2n))
```

where:

- `D0` is the cutoff,
- `n` is the order.

Increasing `n` makes the transition sharper.

### Comparison

| Filter | Transition | Main strength | Main caution |
|---|---|---|---|
| Ideal | abrupt | simple and selective | strong ringing risk |
| Butterworth | adjustable | controllable transition | higher order becomes increasingly abrupt |
| Gaussian | very smooth | minimal abrupt-cutoff ringing | less sharply selective |

[[IMAGE_NEEDED: Ideal Butterworth Gaussian responses | Show 1D radial response curves and corresponding 2D circular low-pass masks for Ideal, Butterworth at two orders, and Gaussian | Learner should see how transition smoothness differs and why abrupt filters can ring]]

### Generic filter-mask pattern

The source chapter builds radial masks from a centered grid.

A clean conceptual implementation is:

```python
import numpy as np

def frequency_grid(shape):
    h, w = shape

    u = np.arange(-w // 2, w - w // 2)
    v = np.arange(-h // 2, h - h // 2)

    U, V = np.meshgrid(u, v)
    D = np.sqrt(U**2 + V**2)

    return D


def gaussian_lpf(shape, cutoff):
    D = frequency_grid(shape)
    return np.exp(-(D**2) / (2 * cutoff**2))
```

The filter mask should match the shifted Fourier spectrum shape.

---

## 4. Applying a frequency-domain filter correctly

A typical grayscale pipeline is:

```python
import numpy as np

F = np.fft.fft2(image)
F_shift = np.fft.fftshift(F)

H = gaussian_lpf(
    image.shape,
    cutoff=20,
)

G_shift = H * F_shift

G = np.fft.ifftshift(G_shift)
filtered = np.fft.ifft2(G).real
```

The conceptual roles are:

```text
F_shift -> image spectrum
H       -> filter response
G_shift -> filtered spectrum
filtered -> reconstructed spatial image
```

### Why `fftshift()`?

Standard FFT output places zero frequency near the array origin.

A radial filter is easier to construct if the low-frequency origin is at the image center.

So:

```python
np.fft.fftshift()
```

centers the spectrum for mask construction.

Before inverse FFT:

```python
np.fft.ifftshift()
```

restores the standard arrangement.

### Why take `.real`?

A perfectly symmetric real-valued filtering operation should reconstruct a real-valued image.

Tiny imaginary parts can appear because of floating-point arithmetic.

Therefore:

```python
np.fft.ifft2(...).real
```

keeps the meaningful real component.

### Important alignment rule

The filter mask and Fourier coefficients must use the same frequency layout.

Do not multiply:

```text
centered mask
```

with:

```text
uncentered FFT
```

unless the mask was specifically designed for that layout.

---

## 5. Low-pass filtering: smoothing and denoising

An LPF keeps the central low-frequency region and suppresses frequencies farther from the center.

### What disappears?

As high-frequency content is reduced, the image loses:

- sharp edges,
- fine texture,
- tiny details,
- some forms of rapidly varying noise.

The output becomes smoother.

### Ideal LPF

A radial ideal filter can be:

```python
def ideal_lpf(shape, cutoff):
    D = frequency_grid(shape)
    return (D < cutoff).astype(float)
```

This creates a hard circular pass region.

### Butterworth LPF

```python
def butterworth_lpf(shape, cutoff, order=2):
    D = frequency_grid(shape)

    return 1.0 / (
        1.0 + (D / cutoff) ** (2 * order)
    )
```

### Gaussian LPF

```python
def gaussian_lpf(shape, cutoff):
    D = frequency_grid(shape)

    return np.exp(
        -(D**2) / (2 * cutoff**2)
    )
```

### Cutoff controls retained detail

A very small cutoff passes only a small low-frequency region.

Result:

- strong blur,
- only coarse structures retained.

As cutoff grows:

- more detail returns,
- reconstruction becomes closer to the source.

[[IMAGE_NEEDED: LPF cutoff comparison | Show the same image filtered with small, medium, and large low-pass cutoffs, plus their circular masks | Learner should notice that increasing cutoff preserves progressively more image detail]]

### Denoising with an LPF

If noise is concentrated primarily in high-frequency components, reducing those frequencies can produce a cleaner image.

But remember:

> High frequencies are not only noise.

They also contain legitimate:

- edges,
- fine texture,
- small structures.

So stronger low-pass filtering can denoise while also blurring useful detail.

### Library support

SciPy can apply a Gaussian operation directly in the Fourier domain:

```python
from scipy import ndimage

F = np.fft.fft2(image)

F_filtered = ndimage.fourier_gaussian(
    F,
    sigma=4,
)

output = np.fft.ifft2(
    F_filtered
).real
```

This avoids manually constructing the Gaussian Fourier response.

---

## 6. Cutoff frequency and reconstruction quality

The chapter evaluates how cutoff frequency changes output quality.

One metric is PSNR.

### PSNR idea

PSNR measures reconstruction fidelity relative to a reference.

Higher PSNR usually means the reconstructed image is numerically closer to the reference under this metric.

For an LPF applied to a clean reference image:

```text
very low cutoff
    -> strong information removal
    -> lower reconstruction fidelity

larger cutoff
    -> more original frequencies retained
    -> usually higher reconstruction fidelity
```

This is why LPF reconstruction PSNR tends to improve as the cutoff expands toward retaining more of the original spectrum.

### But denoising changes the question

If the observed image is noisy and the clean reference is available, an optimal cutoff may occur before "keep everything."

Why?

Because keeping too many frequencies can reintroduce noise.

So the right cutoff depends on the task:

```text
faithful reconstruction of original observed image
!=
best denoising against clean ground truth
```

### PSNR is useful but incomplete

PSNR gives a numerical comparison, but it does not fully describe:

- perceptual sharpness,
- edge quality,
- texture realism,
- task performance.

Use it as one tool, not the only judgment.

---

## 7. High-pass filtering: details and edges

A high-pass filter is conceptually the complement of a low-pass filter.

For a Gaussian-style design:

```python
def gaussian_hpf(shape, cutoff):
    return 1.0 - gaussian_lpf(
        shape,
        cutoff,
    )
```

The center of the frequency spectrum is suppressed, while higher frequencies are preserved.

### What remains?

High-pass outputs often emphasize:

- edges,
- fine textures,
- noise,
- small intensity changes.

Broad smooth illumination is reduced.

[[IMAGE_NEEDED: LPF versus HPF | Show one source image, its low-pass result, high-pass result, and their corresponding centered masks | Learner should see coarse structure in LPF and edge/detail structure in HPF]]

### Cutoff interpretation

For an HPF, increasing the rejected low-frequency radius suppresses more coarse information.

The output can become increasingly dominated by:

- edges,
- fine texture,
- noise.

This typically makes the result less similar to the original image under metrics such as PSNR.

### Gaussian versus Ideal HPF

The same transition argument applies:

- Ideal HPF: hard boundary, greater ringing risk.
- Butterworth HPF: adjustable transition.
- Gaussian HPF: smooth transition.

### scikit-image Butterworth filtering

The chapter also uses `skimage.filters.butterworth()` for both low-pass and high-pass filtering.

Conceptually:

```python
from skimage import filters

low = filters.butterworth(
    image,
    cutoff_frequency_ratio=0.05,
    order=2,
    high_pass=False,
    channel_axis=-1,
)

high = filters.butterworth(
    image,
    cutoff_frequency_ratio=0.05,
    order=2,
    high_pass=True,
    channel_axis=-1,
)
```

The key is not memorizing arguments. It is recognizing that one transfer-function family can be configured to keep either the low or high side of the spectrum.

---

## 8. Band-pass filtering and Difference of Gaussians

Sometimes neither "keep low" nor "keep high" is enough.

You may want:

```text
reject very low
keep middle
reject very high
```

That is a band-pass response.

### Why preserve a middle band?

Different structures often dominate at different spatial scales.

A band-pass filter can emphasize a selected scale of detail while reducing:

- broad illumination trends,
- very fine high-frequency noise.

### Difference of Gaussians

A Difference of Gaussians (DoG) subtracts two Gaussian-smoothed versions with different scales.

Conceptually:

```text
DoG = Gaussian(scale_1) - Gaussian(scale_2)
```

One Gaussian suppresses frequencies at one scale, while the second suppresses them differently.

Subtracting their responses emphasizes frequencies between the two effective scales.

This makes DoG behave as a band-selective filter.

A conceptual kernel construction:

```python
from scipy import signal

g1 = make_gaussian_kernel(
    sigma=wide_sigma,
)

g2 = make_gaussian_kernel(
    sigma=narrow_sigma,
)

dog = g1 - g2

output = signal.fftconvolve(
    image,
    dog,
    mode="same",
)
```

[[IMAGE_NEEDED: Difference of Gaussians band-pass intuition | Show two Gaussian low-pass response curves with different widths, their subtraction producing a band-shaped response, and an image output emphasizing mid-scale structure | Learner should understand why subtracting two smoothing scales isolates a frequency band]]

---

## 9. Band-stop and notch filtering for periodic noise

Periodic interference has a useful property:

> It often produces localized, structured peaks in the frequency spectrum.

For example, sinusoidal noise can create distinct symmetric frequency components.

This can make periodic noise easier to isolate in Fourier space than in the spatial image.

### Workflow

```text
noisy image
    ↓ FFT + shift
inspect magnitude spectrum
    ↓
identify suspicious periodic peaks/bands
    ↓
suppress those frequencies
    ↓ IFFT
reconstructed image
```

[[IMAGE_NEEDED: Periodic noise and notch filtering | Show a clean image, same image with sinusoidal stripes, centered spectrum with symmetric bright interference peaks marked, notch mask over those peaks, and restored image | Learner should see why periodic noise is especially suitable for frequency-domain removal]]

### Notch filtering

A narrow notch can zero or attenuate selected spectral components.

Conceptually:

```python
F = np.fft.fftshift(
    np.fft.fft2(noisy)
)

F_filtered = F.copy()

# Example only: suppress identified interference coordinates.
F_filtered[bad_region_1] = 0
F_filtered[bad_region_2] = 0

restored = np.fft.ifft2(
    np.fft.ifftshift(F_filtered)
).real
```

### The cost of aggressive rejection

The noise frequencies can overlap genuine image information.

Removing them may also remove real image structure.

Therefore:

```text
better noise suppression
can mean
greater loss of legitimate detail
```

The chapter explicitly shows a restored image becoming somewhat less sharp because useful frequencies were removed together with periodic noise.

### Band-stop versus band-pass

Remember:

```text
band-pass -> keep selected band
band-stop -> reject selected band
```

A narrow band-stop becomes a notch-style filter.

### Source implementation note

The supplied chapter text later discusses a "Gaussian band-stop filter" but the accompanying function is named `gaussian_bandpass_filter`, and the shown mask expression behaves like a band-selective product. When studying or implementing that example, inspect the actual transfer mask and verify whether it **passes** or **rejects** the intended band instead of relying only on the function label.

{{exercise:M06.L01.EX01}}

---

## 10. Practical frequency-filter design

A reliable workflow is more important than memorizing formulas.

### Step 1: inspect the image

Ask:

- Is the problem random noise?
- Periodic interference?
- Loss of sharpness?
- Unwanted smooth illumination?
- A specific texture scale?

### Step 2: inspect the spectrum

Use:

```python
F = np.fft.fft2(image)
F_shift = np.fft.fftshift(F)

spectrum = np.log1p(
    np.abs(F_shift)
)
```

Look for:

- central energy concentration,
- directional lines,
- isolated symmetric peaks,
- unusual high-frequency patterns.

### Step 3: choose filter topology

```text
remove high-frequency noise -> LPF
highlight fine detail       -> HPF
isolate a scale             -> BPF
remove periodic frequency   -> notch/BSF
```

### Step 4: choose transition shape

```text
Ideal       -> abrupt
Butterworth -> controllable
Gaussian    -> smooth
```

### Step 5: tune cutoff or band parameters

Do not choose a cutoff blindly.

Compare:

- visual result,
- spectrum,
- reconstruction metric,
- downstream task behavior.

### Step 6: check boundary and layout assumptions

Frequency-domain filtering assumes a finite image that behaves periodically.

Boundary discontinuities can create artifacts.

Windowing or padding may sometimes be useful, depending on the task.

### Step 7: preserve symmetry when necessary

For real spatial outputs, arbitrary edits to one side of a conjugate-symmetric spectrum can create complex reconstruction behavior.

When manually removing frequency peaks, symmetric counterpart frequencies should be considered.

---

## 11. From Fourier filtering to Fourier Feature Networks

The chapter then moves from classical signal processing to a neural representation.

The connection is frequency.

A standard multilayer perceptron can have a bias toward learning smoother, lower-frequency functions first or more easily.

When an MLP tries to represent an image as:

```text
(x, y) -> (R, G, B)
```

it may reconstruct broad smooth regions but struggle with:

- sharp edges,
- fine texture,
- high-frequency detail.

Fourier Feature Networks address this by transforming coordinates before giving them to the network.

### Coordinate-based image representation

Instead of storing an image as a fixed pixel matrix, imagine training a function:

```text
f(x, y) = RGB color
```

Each coordinate becomes an input.

The network predicts the pixel color.

This is a coordinate-based neural representation.

### Raw coordinates

A standard input is:

```text
x = [x_position, y_position]
```

### Fourier feature mapping

The coordinates are projected using a frequency matrix `B` and passed through sine/cosine functions.

Conceptually:

```text
x_proj = 2π x B^T

gamma(x) =
[
    sin(x_proj),
    cos(x_proj)
]
```

The neural network receives:

```text
gamma(x)
```

instead of only raw `x`.

[[IMAGE_NEEDED: Fourier Feature Network architecture | Show pixel coordinate (x,y), multiplication by frequency matrix B, parallel sin/cos encoding, concatenated Fourier features, MLP, and predicted RGB pixel | Learner should understand that Fourier features enrich the coordinate input before the network]]

### Why sinusoidal features help

The encoded input explicitly exposes multiple frequency patterns.

This makes it easier for the MLP to represent rapidly changing functions.

For an image, rapidly changing functions correspond to:

- edges,
- small details,
- textures.

### Frequency scale matters

If the entries of `B` use different scales, the encoding exposes different frequency ranges.

The chapter compares:

- no mapping,
- a basic mapping,
- Gaussian random Fourier mappings at multiple scales.

The important principle is:

> Too little frequency diversity can miss fine detail; excessively high-frequency mappings can make optimization/generalization harder. The mapping scale is a model-design parameter.

### Applications

The source chapter connects Fourier features to areas such as:

- neural scene representations,
- NeRF-style models,
- image reconstruction,
- super-resolution,
- high-frequency function approximation.

---

## 12. Training a Fourier Feature Network in JAX

The chapter implements a coordinate-based network with JAX.

You do not need to memorize the full training code.

Understand the pipeline.

### Step 1: normalize the image

Image values are scaled to:

```text
[0, 1]
```

This keeps target RGB values compatible with the network's final Sigmoid output and makes metrics easier to interpret.

### Step 2: create coordinates

For an `H × W` image, build normalized coordinates:

```text
(x, y) in [0,1] × [0,1]
```

A simplified NumPy-style illustration:

```python
coords = np.linspace(
    0,
    1,
    image.shape[0],
    endpoint=False,
)

xy = np.stack(
    np.meshgrid(coords, coords),
    axis=-1,
)
```

The chapter trains on a downsampled subset and evaluates on full-resolution coordinates.

### Step 3: map coordinates

Without Fourier features:

```python
mapped = xy
```

With Fourier features:

```python
projection = (
    2 * np.pi * xy
) @ B.T

mapped = np.concatenate(
    [
        np.sin(projection),
        np.cos(projection),
    ],
    axis=-1,
)
```

### Step 4: MLP prediction

A multilayer perceptron maps features to:

```text
R, G, B
```

The output can use Sigmoid so predictions remain in:

```text
[0, 1]
```

### Step 5: loss

The chapter uses mean squared error:

```text
MSE(predicted RGB, target RGB)
```

### Step 6: optimize

The source implementation uses:

- JAX automatic differentiation,
- Adam optimization,
- repeated gradient updates.

### Step 7: monitor PSNR

Training and test PSNR are recorded periodically.

This allows comparison among frequency mappings.

[[IMAGE_NEEDED: Fourier mapping reconstruction comparison | Show ground-truth image beside reconstructions from raw coordinates, basic Fourier mapping, low-scale Gaussian mapping, medium-scale mapping, and high-scale mapping, plus small PSNR labels | Learner should compare how mapping frequency affects fine-detail reconstruction]]

### Training versus test behavior

A model can improve on training coordinates while becoming worse at generalizing.

If:

```text
training PSNR keeps increasing
test PSNR stops increasing or decreases
```

that is evidence of overfitting.

The chapter suggests strategies such as:

- early stopping,
- regularization,
- dropout where appropriate.

### Important implementation perspective

The JAX code is one implementation.

The transferable architecture is:

```text
coordinates
    ↓
optional Fourier mapping
    ↓
MLP
    ↓
RGB prediction
    ↓
MSE loss
    ↓
gradient-based optimization
```

The lesson goal is to understand this architecture and the role of Fourier features, not to memorize JAX syntax.

{{exercise:M06.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Low-pass filtering removes only noise.

### Why this is wrong

It suppresses high frequencies, which may contain both noise and real edges/textures.

### Misconception 2

> High-pass filtering extracts only useful edges.

### Why this is wrong

High-frequency noise can also be strongly preserved or amplified.

### Misconception 3

> The ideal filter is always best because its cutoff is exact.

### Why this is wrong

The abrupt transition can create ringing in the spatial-domain output.

### Misconception 4

> A larger cutoff always means stronger filtering.

### Why this is incomplete

Its effect depends on filter type. A larger LPF cutoff keeps more frequencies, while a larger rejected low-frequency region in an HPF can remove more coarse content.

### Misconception 5

> Periodic noise should always be removed with a broad low-pass filter.

### Why this is wrong

Periodic interference can appear as localized spectral peaks. A targeted notch filter can remove it while preserving more unrelated frequencies.

### Misconception 6

> A Fourier Feature Network performs an FFT on the image and feeds the spectrum to an MLP.

### Why this is wrong

In this chapter, Fourier features are sinusoidal encodings of spatial coordinates. The model predicts RGB values from encoded coordinates.

### Misconception 7

> Higher Fourier-feature frequencies automatically improve reconstruction.

### Why this is wrong

Frequency scale affects optimization and generalization. Different image structures benefit from different representations.

---

## Key terminology

| Term | Meaning |
|---|---|
| Frequency-domain filtering | Modifying an image by weighting its Fourier coefficients |
| Transfer function / mask | Frequency-dependent multiplier applied to the image spectrum |
| Cutoff frequency | Boundary parameter controlling which frequencies are kept or attenuated |
| LPF | Low-pass filter; preserves lower frequencies |
| HPF | High-pass filter; preserves higher frequencies |
| BPF | Band-pass filter; preserves a selected frequency interval |
| BSF / BRF | Band-stop/reject filter; suppresses a selected interval |
| Notch filter | Narrow rejection filter aimed at specific interference frequencies |
| Ideal filter | Filter with abrupt pass/reject boundary |
| Butterworth filter | Smooth response with tunable order |
| Gaussian filter | Smooth Gaussian-shaped frequency response |
| Ringing | Oscillation near edges caused by abrupt spectral truncation |
| PSNR | Reconstruction-quality metric derived from MSE |
| DoG | Difference of Gaussians; can create band-selective behavior |
| Periodic noise | Repeating interference that often produces localized Fourier peaks |
| Fourier feature | Sinusoidal encoding derived from projected coordinates |
| Spectral bias | Tendency of standard neural networks to learn lower-frequency functions more readily |
| Coordinate MLP | Neural network mapping spatial coordinates to signal values such as RGB |
| Frequency matrix `B` | Projection matrix controlling Fourier-feature frequencies |
| JAX | Numerical/autodiff framework used by the source implementation |
| Overfitting | Improving training fit while generalization stops improving or worsens |

---

## Self-check

Before continuing, make sure you can answer:

1. What does a frequency-domain filter multiply?
2. Why is `fftshift()` convenient when designing radial masks?
3. What frequencies does an LPF preserve?
4. Why does LPF output look blurred?
5. What useful image structures may be lost during LPF denoising?
6. What is the difference between Ideal, Butterworth, and Gaussian transition shapes?
7. How does Butterworth order change its response?
8. Why can an Ideal filter produce ringing?
9. What does increasing LPF cutoff generally do to reconstruction detail?
10. What does an HPF remove from an image?
11. Why can HPF emphasize both edges and noise?
12. When would a band-pass filter be useful?
13. How does Difference of Gaussians create band-selective behavior?
14. Why is periodic noise often easy to identify in a Fourier magnitude spectrum?
15. What is a notch filter?
16. Why can notch filtering reduce legitimate image detail?
17. Why should manually removed Fourier peaks often be treated symmetrically?
18. What is the key difference between classical Fourier filtering and Fourier Feature Networks?
19. What does a Fourier feature mapping do to `(x, y)` coordinates?
20. Why do sine and cosine features help an MLP represent fine detail?
21. What role does the frequency matrix `B` play?
22. Why compare training PSNR with test PSNR?
23. What pattern suggests overfitting in the FFN experiment?

---

## Retain this idea

**Frequency-domain filtering is selective control over image scales: low frequencies represent broad structure, high frequencies represent rapid variation, and targeted bands can reveal or suppress specific patterns. Fourier Feature Networks reuse the same frequency intuition in a different way—not by filtering an FFT, but by giving a neural network sinusoidal coordinate features that make high-frequency image structure easier to learn.**
        """,

        "estimated_minutes": 300,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "filtering-mental-model",
                "title": "What Is a Frequency-Domain Filter?",
                "order": 1,
            },
            {
                "id": "filter-types",
                "title": "Four Main Filter Types",
                "order": 2,
            },
            {
                "id": "ideal-butterworth-gaussian",
                "title": "Ideal, Butterworth, and Gaussian Filter Shapes",
                "order": 3,
            },
            {
                "id": "frequency-filter-pipeline",
                "title": "Applying a Frequency-Domain Filter Correctly",
                "order": 4,
            },
            {
                "id": "low-pass-filtering",
                "title": "Low-Pass Filtering: Smoothing and Denoising",
                "order": 5,
            },
            {
                "id": "cutoff-quality",
                "title": "Cutoff Frequency and Reconstruction Quality",
                "order": 6,
            },
            {
                "id": "high-pass-filtering",
                "title": "High-Pass Filtering: Details and Edges",
                "order": 7,
            },
            {
                "id": "band-pass-filtering",
                "title": "Band-Pass Filtering and Difference of Gaussians",
                "order": 8,
            },
            {
                "id": "band-stop-periodic-noise",
                "title": "Band-Stop and Notch Filtering for Periodic Noise",
                "order": 9,
            },
            {
                "id": "practical-filter-design",
                "title": "Practical Frequency-Filter Design",
                "order": 10,
            },
            {
                "id": "fourier-feature-networks",
                "title": "From Fourier Filtering to Fourier Feature Networks",
                "order": 11,
            },
            {
                "id": "ffn-jax-training",
                "title": "Training a Fourier Feature Network in JAX",
                "order": 12,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M06.L01.EX01",

            "title": "Design and Diagnose Frequency-Domain Filters",

            "lesson_code": "M06.L01",

            "section_id": "band-stop-periodic-noise",

            "placement": "after_section",

            "description": (
                "Practice reading a spectrum, designing LPF/HPF/notch masks, tuning "
                "cutoff values, and explaining the trade-off between filtering and detail loss."
            ),

            "instructions": (
                "1. Load a grayscale image and compute its centered Fourier spectrum.\n"
                "2. Implement one Gaussian LPF and one Gaussian HPF using a radial distance grid.\n"
                "3. Apply both filters with at least three cutoff values and display the outputs.\n"
                "4. If you have a clean reference, compute PSNR for each output; otherwise, "
                "compare detail/noise visually and record your observations.\n"
                "5. Add synthetic sinusoidal periodic noise to the image and inspect how it "
                "appears in the centered magnitude spectrum.\n"
                "6. Design a narrow notch mask that suppresses the strongest interference "
                "frequencies while preserving the low-frequency center.\n"
                "7. Reconstruct the image and compare its sharpness with the noisy input.\n"
                "8. Explain why the notch positions should respect Fourier symmetry for a "
                "real-valued image.\n"
                "9. Compare an abrupt Ideal mask with a Gaussian or Butterworth mask and "
                "look for ringing near sharp edges.\n"
                "10. Summarize which filter you would use for random high-frequency noise, "
                "edge emphasis, mid-scale features, and periodic interference."
            ),

            "expected_output": (
                "A notebook or script showing LPF/HPF cutoff comparisons, spectra, PSNR or "
                "visual observations, a synthetic periodic-noise example, a notch-filter "
                "restoration, and a concise filter-selection summary."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "fft2",
                "frequency-mask-design",
                "low-pass-filter",
                "high-pass-filter",
                "notch-filter",
                "periodic-noise",
                "psnr",
                "spectral-analysis",
            ],
        },

        {
            "id": "M06.L01.EX02",

            "title": "Compare Raw Coordinates with Fourier Features",

            "lesson_code": "M06.L01",

            "section_id": "ffn-jax-training",

            "placement": "after_section",

            "description": (
                "Understand Fourier Feature Networks experimentally by comparing how "
                "coordinate mappings affect reconstruction of fine image detail."
            ),

            "instructions": (
                "1. Choose a small RGB image and normalize it to [0,1].\n"
                "2. Build normalized (x,y) coordinates for every pixel.\n"
                "3. Create two model inputs: raw coordinates and a sinusoidal Fourier "
                "mapping using sin(2πxBᵀ) and cos(2πxBᵀ).\n"
                "4. Train the same small coordinate MLP on both representations using the "
                "same optimizer, iteration budget, and training coordinate subset.\n"
                "5. Record training and test PSNR periodically.\n"
                "6. Compare reconstructed images, focusing on edges and textures.\n"
                "7. Repeat the Fourier mapping with at least two frequency scales.\n"
                "8. Explain which mapping represented high-frequency detail better and "
                "whether any mapping showed worse generalization.\n"
                "9. Identify evidence of overfitting from the PSNR curves.\n"
                "10. Write two sentences explaining why this experiment is different from "
                "applying an FFT filter to the image."
            ),

            "expected_output": (
                "A notebook or script comparing raw-coordinate and Fourier-feature MLP "
                "reconstructions, training/test PSNR curves, at least two feature scales, "
                "and a short interpretation of high-frequency representation and overfitting."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "fourier-features",
                "coordinate-mlp",
                "sinusoidal-encoding",
                "image-reconstruction",
                "psnr",
                "training-analysis",
                "overfitting",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M06.L01.QZ01",

        "title": "Frequency Domain Filtering — Knowledge Check",

        "lesson_code": "M06.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M06.L01.Q01",
                "section_id": "filter-types",
                "question": "Which filter primarily preserves broad smooth image structure?",
                "options": [
                    "Low-pass filter",
                    "High-pass filter",
                    "Notch filter only",
                    "Transposed convolution",
                ],
                "correct": 0,
                "explanation": (
                    "Low spatial frequencies represent broad, slowly varying structure, "
                    "which an LPF preserves."
                ),
            },

            {
                "id": "M06.L01.Q02",
                "section_id": "ideal-butterworth-gaussian",
                "question": (
                    "Which frequency filter has the most abrupt pass-to-reject transition?"
                ),
                "options": [
                    "Ideal",
                    "Gaussian",
                    "Low-order Butterworth",
                    "Fourier feature encoding",
                ],
                "correct": 0,
                "explanation": (
                    "The Ideal filter uses a hard cutoff, which is also why it is especially "
                    "susceptible to ringing."
                ),
            },

            {
                "id": "M06.L01.Q03",
                "section_id": "frequency-filter-pipeline",
                "question": (
                    "Why is ifftshift normally applied before the inverse FFT when the "
                    "filter mask was designed on an fftshift-centered spectrum?"
                ),
                "options": [
                    "To restore the frequency layout expected by the inverse transform",
                    "To increase image resolution",
                    "To calculate PSNR",
                    "To convert a high-pass filter to a low-pass filter",
                ],
                "correct": 0,
                "explanation": (
                    "fftshift is a rearrangement for centered frequency coordinates; "
                    "ifftshift undoes that rearrangement before reconstruction."
                ),
            },

            {
                "id": "M06.L01.Q04",
                "section_id": "low-pass-filtering",
                "question": (
                    "What is a major risk of using a very aggressive LPF for denoising?"
                ),
                "options": [
                    "It can remove legitimate edges and fine texture together with noise",
                    "It always creates more image channels",
                    "It preserves every high-frequency component",
                    "It can only operate on color images",
                ],
                "correct": 0,
                "explanation": (
                    "High frequencies contain real detail as well as some forms of noise."
                ),
            },

            {
                "id": "M06.L01.Q05",
                "section_id": "cutoff-quality",
                "question": (
                    "For LPF reconstruction of the original observed image, what generally "
                    "happens as the cutoff is increased?"
                ),
                "options": [
                    "More original frequencies are retained and the result becomes closer to the input",
                    "All high frequencies are removed more strongly",
                    "The image necessarily becomes more blurred",
                    "The Fourier transform stops being complex",
                ],
                "correct": 0,
                "explanation": (
                    "A larger LPF pass region preserves more of the original spectrum."
                ),
            },

            {
                "id": "M06.L01.Q06",
                "section_id": "high-pass-filtering",
                "question": (
                    "Which image components are typically emphasized by an HPF?"
                ),
                "options": [
                    "Fine details, edges, and potentially high-frequency noise",
                    "Only the DC component",
                    "Only smooth illumination gradients",
                    "File metadata",
                ],
                "correct": 0,
                "explanation": (
                    "High-pass filtering removes broad low-frequency variation and keeps "
                    "rapid spatial changes."
                ),
            },

            {
                "id": "M06.L01.Q07",
                "section_id": "band-pass-filtering",
                "question": (
                    "Why can Difference of Gaussians behave like a band-pass filter?"
                ),
                "options": [
                    "Subtracting two smoothing responses with different scales emphasizes frequencies between those scales",
                    "It always keeps only the DC component",
                    "It performs template matching",
                    "It converts RGB to HSV",
                ],
                "correct": 0,
                "explanation": (
                    "The two Gaussian low-pass responses attenuate frequencies differently; "
                    "their difference emphasizes an intermediate range."
                ),
            },

            {
                "id": "M06.L01.Q08",
                "section_id": "band-stop-periodic-noise",
                "question": (
                    "Why is periodic sinusoidal noise often suitable for notch filtering?"
                ),
                "options": [
                    "It can generate localized structured peaks in the Fourier spectrum",
                    "It is always confined to the DC component",
                    "It changes only image dimensions",
                    "It disappears after fftshift automatically",
                ],
                "correct": 0,
                "explanation": (
                    "Periodic interference has concentrated frequency structure that can "
                    "often be targeted more selectively than broad random noise."
                ),
            },

            {
                "id": "M06.L01.Q09",
                "section_id": "practical-filter-design",
                "question": (
                    "What is a sensible first frequency-domain strategy for removing "
                    "narrow periodic interference while preserving most other content?"
                ),
                "options": [
                    "Targeted notch or band-stop filtering around the interference peaks",
                    "Set the entire spectrum to zero",
                    "Use only an HPF with no spectrum inspection",
                    "Discard the phase spectrum",
                ],
                "correct": 0,
                "explanation": (
                    "A narrow rejection region is intended to suppress the interference "
                    "while disturbing less unrelated information."
                ),
            },

            {
                "id": "M06.L01.Q10",
                "section_id": "fourier-feature-networks",
                "question": (
                    "What is the input to the Fourier mapping in the chapter's coordinate-based FFN?"
                ),
                "options": [
                    "Spatial pixel coordinates such as (x,y)",
                    "Only the image JPEG header",
                    "The output of a notch filter only",
                    "A class label",
                ],
                "correct": 0,
                "explanation": (
                    "The model predicts color from spatial coordinates that are optionally "
                    "expanded with sinusoidal Fourier features."
                ),
            },

            {
                "id": "M06.L01.Q11",
                "section_id": "fourier-feature-networks",
                "question": (
                    "Why are sine and cosine Fourier features useful for coordinate MLPs?"
                ),
                "options": [
                    "They expose frequency-rich coordinate patterns that help represent rapid spatial variation",
                    "They remove the need for training",
                    "They guarantee no overfitting",
                    "They make every image grayscale",
                ],
                "correct": 0,
                "explanation": (
                    "Frequency-rich positional encodings help the network model fine detail "
                    "that raw-coordinate MLPs can struggle to represent."
                ),
            },

            {
                "id": "M06.L01.Q12",
                "section_id": "ffn-jax-training",
                "question": (
                    "What training pattern is evidence of overfitting in the FFN experiment?"
                ),
                "options": [
                    "Training PSNR rises while test PSNR plateaus or falls",
                    "Both training and test PSNR improve together",
                    "The image is normalized to [0,1]",
                    "The model uses Adam",
                ],
                "correct": 0,
                "explanation": (
                    "Improving training reconstruction while held-out/full-resolution "
                    "performance stagnates or declines indicates reduced generalization."
                ),
            },

            {
                "id": "M06.L01.Q13",
                "section_id": "ffn-jax-training",
                "type": "open",
                "question": (
                    "You are given an image containing fine texture plus periodic stripe "
                    "interference. Design a two-stage solution: first use frequency-domain "
                    "filtering to reduce the interference, then train a coordinate MLP to "
                    "reconstruct the cleaned image. Explain your notch-filter design, how "
                    "you would avoid removing useful frequencies, what Fourier features "
                    "would contribute to the MLP, and which training/test metric behavior "
                    "you would monitor."
                ),
            },
        ],

        "passing_score": 70,
    },
}
