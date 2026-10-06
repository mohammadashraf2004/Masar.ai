"""M05.L01 — Convolution and Spatial/Frequency Domain Filtering.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 5. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M05.L01"

MODULE_ORDER = 5

MODULE_TITLE = "Convolution and Image Filtering"

MODULE_DESCRIPTION = (
    "Build a practical understanding of convolution in spatial and frequency domains, "
    "kernel-based filtering, boundary handling, correlation and template matching, "
    "normalized cross-correlation, FFT convolution, and the relationship between "
    "2D, 3D, and transposed convolution."
)

SOURCE_CHAPTER = 5

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Convolution and Spatial/Frequency Domain Filtering",

    "slug": "image-processing-m05-l01",

    "description": (
        "Learn convolution as a sliding weighted-neighborhood operation, apply common "
        "filters in the spatial domain, understand convolution modes and boundary "
        "conditions, distinguish convolution from correlation, perform template matching "
        "with NCC, accelerate large-kernel filtering with FFT convolution, and connect "
        "classical image filtering to 2D, 3D, and transposed convolutions in PyTorch."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 5.0,

    "skill_tags": [
        "image-processing",
        "convolution",
        "spatial-filtering",
        "frequency-domain-filtering",
        "kernels",
        "boundary-conditions",
        "correlation",
        "template-matching",
        "normalized-cross-correlation",
        "fft-convolution",
        "gaussian-filter",
        "pytorch-convolution",
        "conv2d",
        "conv3d",
        "transposed-convolution",
        "module-05",
    ],

    "prerequisite_ids": ["M04.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Convolution and Spatial/Frequency Domain Filtering",

        "content": r"""
# Convolution and Spatial/Frequency Domain Filtering

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M05.L01  
> **Module:** Convolution and Image Filtering  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 5. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain 2D convolution as a sliding weighted-neighborhood operation.
- Predict how changing a kernel changes the visual behavior of a filter.
- Apply blur, sharpening, embossing, and edge-detection kernels.
- Distinguish `full`, `same`, and `valid` convolution modes.
- Explain how padding/boundary strategies affect image borders.
- Compare spatial-domain convolution with FFT-based frequency-domain convolution.
- Explain the convolution theorem and implement a simple frequency-domain blur.
- Distinguish convolution from correlation by the kernel-flipping rule.
- Use cross-correlation and normalized cross-correlation for template matching.
- Explain why NCC is more robust to brightness and contrast changes.
- Choose between `scipy.signal`, `scipy.ndimage`, and OpenCV filtering APIs.
- Explain the conceptual differences among 2D convolution, 3D convolution, fixed interpolation upsampling, and transposed convolution.
- Recognize checkerboard artifacts as a possible failure mode of transposed convolution.

---

## 1. Convolution: one operation, many image-processing tasks

Convolution is one of the most reusable operations in image processing.

The basic setup contains:

- an **input image**,
- a small matrix called a **kernel**, **filter**, or sometimes a **mask**,
- an **output image**.

At each location, the kernel is placed over a local neighborhood of pixels. Corresponding kernel and image values are multiplied, and the products are summed to produce a new output value.

A simplified 3×3 example looks like this:

```text
image neighborhood        kernel

[a b c]                  [k1 k2 k3]
[d e f]        ×         [k4 k5 k6]
[g h i]                  [k7 k8 k9]

output =
a*k1 + b*k2 + c*k3 +
d*k4 + e*k5 + f*k6 +
g*k7 + h*k8 + i*k9
```

Then the kernel moves to the next spatial location.

### Why convolution is powerful

The same operation can create very different effects simply by changing the kernel.

Examples:

- averaging neighbors → smoothing,
- emphasizing center relative to neighbors → sharpening,
- measuring directional changes → edge detection,
- asymmetric weights → embossing.

This is why convolution appears throughout:

- classical image processing,
- computer vision,
- signal processing,
- convolutional neural networks.

{{image:convolution-sliding-window}}

### A kernel changes what the filter responds to

A normalized box blur:

```python
import numpy as np

box = np.ones((3, 3)) / 9
```

sums to `1`, so it averages a local neighborhood without intentionally increasing global brightness.

A Laplacian-like edge kernel:

```python
laplace = np.array([
    [0,  1, 0],
    [1, -4, 1],
    [0,  1, 0],
])
```

responds strongly where the center differs from neighboring pixels.

A sharpening kernel:

```python
sharpen = np.array([
    [ 0, -1,  0],
    [-1,  5, -1],
    [ 0, -1,  0],
])
```

preserves the center while subtracting surrounding content, increasing local contrast around detail.

### Convolution changes spatial-frequency characteristics

A smoother suppresses rapid spatial variation.

An edge detector emphasizes rapid spatial variation.

So convolution can be understood both:

- locally, as weighted neighboring pixels,
- globally, as changing frequency content.

That connection becomes important later in this lesson.

---

## 2. Spatial-domain convolution

Spatial-domain convolution works directly on image pixels.

For each output location:

1. place the kernel over the relevant neighborhood,
2. multiply kernel weights by pixel values,
3. add the products,
4. write the result,
5. slide the kernel.

### Computational cost

For an image containing many pixels and a `K × K` kernel, each output location needs roughly `K²` multiply/add operations.

That is manageable for small kernels such as:

```text
3×3
5×5
```

but becomes expensive as the kernel becomes large.

This is why direct spatial convolution is often preferred for small local filters, while large filters may benefit from FFT-based methods.

### Using `scipy.signal.convolve2d`

A simple blur:

```python
from scipy import signal

blur_kernel = np.ones((3, 3)) / 9

blurred = signal.convolve2d(
    image,
    blur_kernel,
    mode="same",
    boundary="symm",
)
```

An edge response:

```python
laplace_kernel = np.array([
    [0,  1, 0],
    [1, -4, 1],
    [0,  1, 0],
])

edges = signal.convolve2d(
    image,
    laplace_kernel,
    mode="same",
    boundary="symm",
)
```

### Kernel normalization

For smoothing kernels, the weights often sum to `1`.

Why?

If all pixels in a constant region have value `c`, then:

```text
output = c * sum(kernel)
```

If the kernel sums to `1`:

```text
output = c
```

so constant brightness is preserved.

This is not a universal rule: edge, sharpen, and derivative kernels often intentionally have different sums.

### Color images

With a function such as `scipy.signal.convolve2d()`, a straightforward approach is to process each RGB channel independently:

```python
out = np.empty_like(image, dtype=float)

for c in range(3):
    out[..., c] = signal.convolve2d(
        image[..., c],
        kernel,
        mode="same",
        boundary="symm",
    )
```

The chapter also demonstrates a complex Scharr-like kernel whose real and imaginary components encode gradients in different directions.

Conceptually:

```text
real part      -> one directional response
imaginary part -> perpendicular directional response
magnitude      -> edge strength
phase          -> edge orientation
```

[[IMAGE_NEEDED: Common kernels and outputs | Show one source image with box blur, Laplacian edge, sharpen, and emboss kernels beside their corresponding outputs | Learner should see that changing only kernel weights changes the visual operation]]

---

## 3. Output modes and boundary handling

The kernel eventually reaches image borders.

At the border, part of the kernel can fall outside the available image.

A convolution implementation therefore needs two separate decisions:

1. **What output region do we keep?**
2. **What values do we assume beyond the image boundary?**

### Convolution modes

Suppose an input has size:

```text
M × N
```

and a kernel has size:

```text
K × L
```

#### `valid`

Only positions where the kernel fits entirely inside the original image are returned.

No boundary padding is needed.

Output becomes smaller.

#### `same`

Return an output centered so that it has the same spatial size as the input.

This is convenient when each input pixel should correspond to an output position.

#### `full`

Return every position where the image and kernel overlap at least partially.

The output becomes larger than the input.

[[IMAGE_NEEDED: Full same valid convolution modes | Use a simple 5×5 input grid and 3×3 kernel to show visually which output positions are retained for valid, same, and full modes and how their output dimensions differ | Learner should understand that mode controls output extent, not the kernel itself]]

### Boundary conditions

For modes that require information beyond the border, common choices include:

#### Constant / fill

Pretend pixels outside the image have a constant value, often `0`.

```text
... 0 0 | image | 0 0 ...
```

This can introduce artificial dark boundaries.

#### Wrap

Treat the image as periodic:

```text
right edge connects to left edge
bottom connects to top
```

This can be appropriate for cyclic or tileable data.

#### Symmetric / reflection

Reflect image values near the boundary.

This often provides smoother edge behavior for ordinary photographs.

### Why border strategy matters

Suppose an edge detector sees an ordinary bright image ending at the border.

If outside pixels are assumed to be `0`, the algorithm may interpret the border as a strong intensity transition.

That creates a **false edge**.

For many general image filters, reflected/symmetric padding reduces these artificial transitions.

---

## 4. Applying kernels with SciPy and OpenCV

Different libraries expose similar mathematical operations through different APIs.

### `scipy.signal`

Useful when you want explicit 2D convolution behavior and control over:

- `mode`,
- boundary strategy,
- fill values.

Example:

```python
filtered = signal.convolve2d(
    image,
    kernel,
    mode="same",
    boundary="symm",
)
```

### `scipy.ndimage`

Designed for N-dimensional array processing.

A kernel can be shaped to avoid mixing the color-channel dimension unintentionally.

For example:

```python
kernel_rgb = sharpen_kernel.reshape(3, 3, 1)

out = ndimage.convolve(
    image,
    kernel_rgb,
    mode="nearest",
)
```

The final axis size of `1` means the kernel acts spatially without sliding across RGB channels.

### OpenCV `filter2D`

OpenCV provides an optimized implementation:

```python
import cv2

filtered = cv2.filter2D(
    image,
    ddepth=-1,
    kernel=kernel,
)
```

`ddepth=-1` keeps the source depth.

OpenCV is often attractive for:

- performance-sensitive code,
- high-resolution images,
- real-time vision pipelines.

### Performance measurements are contextual

The chapter reports benchmark comparisons in which OpenCV performs strongly.

But benchmark results depend on:

- image size,
- kernel size,
- CPU/GPU,
- library version,
- threading,
- memory layout.

Therefore, treat a benchmark as evidence for a specific environment, not a timeless universal ranking.

---

## 5. Correlation versus convolution

Correlation and convolution both slide a kernel/template over an image and compute weighted sums.

The defining difference is:

> **Convolution flips the kernel before applying it. Correlation does not.**

For a 2D kernel, convolution flips it:

- horizontally,
- vertically.

### Why they can look identical

If the kernel is symmetric, flipping it changes nothing.

For example, a symmetric Gaussian kernel looks the same after a 180-degree flip.

So:

```text
correlation result = convolution result
```

for that symmetric kernel.

With an asymmetric kernel, outputs can differ.

{{image:convolution-vs-correlation}}

### SciPy comparison

```python
from scipy.signal import convolve2d, correlate2d

conv = convolve2d(
    image,
    kernel,
    mode="valid",
)

corr = correlate2d(
    image,
    kernel,
    mode="valid",
)
```

For an asymmetric kernel:

```python
kernel_flipped = kernel[::-1, ::-1]
```

Correlation with the flipped kernel corresponds to convolution with the original kernel.

### Why correlation is useful

When a small image patch represents a pattern we want to find, we usually do **not** want to flip the pattern.

We want to compare it directly against regions in the larger image.

That naturally leads to template matching.

---

## 6. Template matching with cross-correlation

Template matching asks:

> Where does this small image patch most closely appear inside a larger image?

Let:

- `I` be a large image,
- `T` be a smaller template.

At each candidate location, correlation computes similarity between:

```text
template T
```

and the corresponding local patch of:

```text
image I
```

The result is a **correlation map**.

High values indicate stronger similarity.

### Cross-correlation workflow

```text
large image + template
         ↓
slide template
         ↓
similarity score at each position
         ↓
correlation map
         ↓
location of maximum
```

Using SciPy:

```python
cc = signal.correlate2d(
    image,
    template,
    boundary="symm",
    mode="same",
)

y, x = np.unravel_index(
    np.argmax(cc),
    cc.shape,
)
```

### Zero-mean correlation

Subtracting the mean helps reduce sensitivity to global offsets:

```python
template_zm = template - template.mean()
image_zm = image - image.mean()
```

This focuses matching more on relative structure than absolute brightness.

[[IMAGE_NEEDED: Template matching correlation map | Show a larger face/object image, a cropped template, the resulting correlation heatmap, and the detected best-match location marked on the source | Learner should understand that template matching searches for the maximum similarity response]]

### Limitations of ordinary correlation

Raw cross-correlation can be affected by:

- brightness,
- contrast,
- scale,
- rotation,
- viewpoint change,
- occlusion.

The next step—normalized cross-correlation—addresses brightness/contrast sensitivity better.

---

## 7. Normalized cross-correlation (NCC)

Normalized cross-correlation compares patterns after accounting for mean and scale.

The core idea is:

1. subtract local/template means,
2. measure aligned variation,
3. divide by standard deviations.

A conceptual form is:

```text
NCC =
zero-mean similarity
------------------------------
local contrast * template contrast
```

Scores are typically bounded around:

```text
[-1, 1]
```

where:

```text
+1 -> strong positive similarity
 0 -> weak linear similarity
-1 -> strong inverse similarity
```

### Why normalization helps

Imagine the same pattern under different lighting:

```text
patch A = dark version
patch B = bright version
```

Raw values differ.

But their normalized structure may be similar.

Therefore, NCC is more robust to:

- additive brightness changes,
- multiplicative contrast changes.

It is not invariant to every transformation, such as arbitrary rotation or large scale differences.

### A custom NCC structure

The source chapter constructs NCC from:

- a zero-mean template,
- a correlation numerator,
- local image mean,
- local image standard deviation,
- template standard deviation.

A simplified conceptual implementation is:

```python
def ncc(image, template):
    template_zero = template - template.mean()

    numerator = signal.correlate2d(
        image,
        template_zero,
        mode="valid",
    )

    # Additional local mean/std terms form denominator.
    # Return normalized similarity map.
```

A real implementation must avoid division by zero in flat regions.

### OpenCV

OpenCV provides normalized template matching directly:

```python
result = cv2.matchTemplate(
    image,
    template,
    cv2.TM_CCOEFF_NORMED,
)
```

Then:

```python
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
```

For this mode, `max_loc` is the best match.

{{exercise:M05.L01.EX01}}

---

## 8. The convolution theorem and frequency-domain filtering

The previous lesson introduced the DFT/FFT.

Now we use it to compute convolution.

### Convolution theorem

The central result is:

```text
spatial convolution
        ↕ Fourier transform
frequency multiplication
```

If:

```text
F = FFT(image)
H = FFT(kernel)
```

then:

```text
FFT(image *convolved_with* kernel)
=
F * H
```

where the multiplication on the right is element-wise.

So frequency-domain filtering follows:

```text
image ----FFT----\
                  × ----IFFT---- filtered image
kernel ---FFT----/
```

[[IMAGE_NEEDED: Convolution theorem pipeline | Show spatial image and kernel entering separate FFT blocks, element-wise multiplication of their spectra, then IFFT to produce the filtered image; alongside show the equivalent sliding spatial convolution | Learner should understand that spatial convolution and frequency multiplication are two representations of the same linear filtering operation]]

### Why use the frequency domain?

Direct convolution gets more expensive as kernel size grows.

FFT-based convolution requires:

1. FFT of image,
2. FFT of kernel,
3. element-wise multiplication,
4. inverse FFT.

For sufficiently large kernels, this can be substantially faster.

For small kernels, FFT overhead can make direct spatial convolution faster.

So the engineering rule is:

```text
small kernel -> direct spatial convolution is often efficient
large kernel -> FFT convolution often becomes attractive
```

Memory use and padding also matter.

### Circular versus linear convolution

A direct FFT multiplication naturally corresponds to circular/periodic convolution unless arrays are padded appropriately.

This is important.

To reproduce a desired linear convolution, you must pay attention to:

- image/kernel padding,
- kernel alignment,
- output cropping.

High-level functions such as `fftconvolve()` handle much of this for you.

---

## 9. Gaussian blur in the frequency domain

A Gaussian kernel is a smoothing filter.

In the spatial domain, it averages nearby content with weights that decrease smoothly with distance.

In the frequency domain, a Gaussian behaves as a **low-pass filter**.

That means:

```text
low frequencies  -> preserved strongly
high frequencies -> attenuated
```

This explains why Gaussian blur reduces:

- fine texture,
- noise,
- sharp edge detail.

### Building a 2D Gaussian kernel

A separable Gaussian can be built from two 1D vectors:

```python
g_row = signal.windows.gaussian(height, std=5)
g_col = signal.windows.gaussian(width, std=5)

gaussian_2d = np.outer(g_row, g_col)
```

The outer product reflects Gaussian separability.

### Frequency response

```python
H = np.fft.fft2(
    np.fft.ifftshift(gaussian_2d)
)

H_view = np.fft.fftshift(H)
```

`ifftshift()` repositions a centered spatial kernel so that its origin aligns correctly for the FFT representation.

Then the centered magnitude:

```python
np.abs(H_view)
```

shows strong response near low frequencies and attenuation toward high frequencies.

[[IMAGE_NEEDED: Gaussian kernel spatial and frequency views | Show a 2D Gaussian kernel as an image/3D surface beside its centered Fourier magnitude response, with low-frequency center bright and high-frequency outer regions dark | Learner should see why Gaussian convolution behaves as low-pass filtering]]

### Manual FFT blur

```python
F = np.fft.fft2(image)

H = np.fft.fft2(
    np.fft.ifftshift(gaussian_kernel)
)

filtered_frequency = F * H

blurred = np.fft.ifft2(
    filtered_frequency
).real
```

The `.real` is used because tiny imaginary values can appear from floating-point numerical error.

### `fftconvolve`

SciPy provides a safer high-level tool:

```python
from scipy import signal

blurred = signal.fftconvolve(
    image,
    gaussian_kernel,
    mode="same",
)
```

This lets you focus on filtering instead of manually handling every FFT detail.

### Frequency content after blur

If you compare spectra before and after Gaussian blur, high-frequency magnitude is reduced.

This is a direct visual link between:

```text
spatial smoothing
```

and:

```text
frequency-domain attenuation
```

---

## 10. Choosing spatial or FFT convolution

The chapter compares spatial and FFT implementations.

The important conclusion is conditional rather than absolute.

### Spatial convolution tends to work well when

- kernels are small,
- operations are highly local,
- transform overhead would dominate,
- real-time operators use tiny fixed filters.

Examples:

- Sobel,
- Prewitt,
- small sharpening kernels.

### FFT convolution becomes attractive when

- kernels are large,
- images are large,
- many operations would otherwise require large sliding neighborhoods.

Examples can include large smoothing kernels and some restoration workflows.

### Memory considerations

FFT approaches require transformed arrays, often complex-valued.

For very large images, memory consumption can be significant.

Chunked methods such as:

- overlap-add,
- overlap-save,
- tiled FFT,

can process large signals in blocks.

### Benchmark correctly

A fair benchmark should hold constant:

- input image,
- kernel,
- output mode,
- data type,
- hardware,
- warm-up effects,
- repetition count.

Do not compare two functions performing different boundary rules or output sizes and call the result a fair speed comparison.

---

## 11. 2D and 3D convolution

The word "dimension" can become confusing when images also have channels.

### 2D convolution

A standard 2D convolution slides across:

```text
height × width
```

In deep-learning libraries, channels are often additional feature dimensions consumed by a kernel.

PyTorch expects 2D convolution input in:

```text
N × C × H × W
```

where:

- `N` = batch,
- `C` = channels,
- `H` = height,
- `W` = width.

A grayscale example:

```python
import torch
import torch.nn.functional as F

x = image_tensor.reshape(
    1, 1, H, W
)

kernel = torch.tensor([
    [1, 0, -1],
    [1, 0, -1],
    [1, 0, -1],
], dtype=torch.float32).view(
    1, 1, 3, 3
)

edges = F.conv2d(x, kernel)
```

### Multi-channel 2D convolution

For RGB input:

```text
N × 3 × H × W
```

a filter can have weights spanning all three input channels.

At one spatial location, values across:

```text
channel × kernel_height × kernel_width
```

are multiplied and summed.

The kernel still **slides over two spatial dimensions**.

This is the important definition of 2D convolution in CNNs.

### 3D convolution

3D convolution slides across three spatial/depth dimensions.

PyTorch expects:

```text
N × C × D × H × W
```

where `D` can represent:

- volume depth,
- time/frame depth,
- another genuine third spatial/sequential axis.

Typical applications include:

- CT/MRI volumes,
- video clips,
- volumetric scientific data.

[[IMAGE_NEEDED: 2D versus 3D convolution | Show a 2D kernel sliding across H×W while spanning input channels, then a 3D kernel sliding across D×H×W for a volume/video; label channel versus depth axes carefully | Learner should not confuse RGB channels with the third sliding spatial dimension of a true 3D convolution]]

### Important nuance

An RGB image having three channels does **not automatically mean** it should be processed with `Conv3d`.

A normal CNN commonly uses `Conv2d` with `in_channels=3`.

3D convolution is appropriate when a meaningful third sliding dimension exists.

---

## 12. Upsampling versus transposed convolution

Both operations can increase spatial resolution, but they are conceptually different.

### Fixed upsampling

Examples include:

- nearest-neighbor interpolation,
- bilinear interpolation.

These have no trainable parameters.

```python
upsample = torch.nn.Upsample(
    scale_factor=2,
    mode="bilinear",
)
```

### Upsample followed by convolution

A common architecture is:

```text
fixed resize
    ↓
learned Conv2d
```

The resize controls geometry while the convolution learns feature processing.

### Transposed convolution

`ConvTranspose2d` uses trainable kernels in an operation designed to produce a larger output feature map.

It is often used in:

- autoencoder decoders,
- segmentation decoders,
- generative models,
- learned super-resolution architectures.

It should not be thought of as simply "the mathematical inverse of convolution."

### Checkerboard artifacts

Transposed convolution can produce checkerboard patterns if kernel overlap is uneven.

A practical mitigation mentioned in the chapter is to:

- choose kernel/stride relationships carefully,
- or use explicit upsampling followed by ordinary convolution.

[[IMAGE_NEEDED: Upsampling versus transposed convolution | Show one low-resolution feature map passing through fixed interpolation + Conv2d versus ConvTranspose2d, with a small checkerboard artifact example on the transposed-convolution side | Learner should distinguish fixed geometric enlargement from learned upsampling and recognize uneven-overlap artifacts]]

{{exercise:M05.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> A kernel determines only how large the local neighborhood is.

### Why this is wrong

Kernel **weights** determine what spatial pattern the filter emphasizes or suppresses. Two 3×3 kernels can produce completely different outputs.

### Misconception 2

> `same`, `valid`, and `full` describe different filter types.

### Why this is wrong

They describe the **output extent** of convolution. The kernel can be identical.

### Misconception 3

> Convolution and correlation are always interchangeable.

### Why this is wrong

Convolution flips the kernel; correlation does not. They match automatically only for kernels unchanged by the flip, such as symmetric kernels.

### Misconception 4

> FFT convolution is always faster.

### Why this is wrong

FFT setup has computational and memory overhead. Direct convolution is often faster for small kernels.

### Misconception 5

> Normalized cross-correlation can find a template under any visual transformation.

### Why this is wrong

NCC improves robustness to intensity offset/scale, but large changes in rotation, scale, viewpoint, deformation, or occlusion can still break matching.

### Misconception 6

> An RGB image requires 3D convolution because it has three channels.

### Why this is wrong

Standard CNNs process RGB images with 2D convolution whose filters span the three input channels while sliding over height and width.

### Misconception 7

> Transposed convolution is simply ordinary image interpolation.

### Why this is wrong

It uses learnable convolutional weights to produce expanded feature maps and can behave very differently from fixed interpolation.

---

## Key terminology

| Term | Meaning |
|---|---|
| Convolution | Sliding weighted aggregation with a flipped kernel |
| Kernel / filter | Small weight array applied over local neighborhoods |
| Spatial-domain filtering | Applying operations directly to image samples |
| Frequency-domain filtering | Modifying frequency coefficients, commonly using FFTs |
| Box blur | Averaging filter with equal local weights |
| Laplacian | Second-derivative-style operator emphasizing intensity changes |
| Sharpening | Increasing local contrast/detail response |
| Emboss | Directional filter creating relief-like appearance |
| `valid` mode | Output only where kernel fully overlaps the source |
| `same` mode | Output cropped/centered to input spatial dimensions |
| `full` mode | Full convolution including partial overlaps |
| Boundary condition | Rule for values beyond image borders |
| Correlation | Sliding similarity/weighted sum without flipping the kernel |
| Cross-correlation | Correlation used to compare a template across image positions |
| NCC | Normalized cross-correlation |
| Correlation map | Similarity score image produced by template matching |
| Convolution theorem | Spatial convolution corresponds to frequency multiplication |
| FFT convolution | Convolution computed through FFT → multiply → IFFT |
| Low-pass filter | Filter that preserves lower frequencies and attenuates higher ones |
| Gaussian filter | Smooth separable low-pass filter based on a Gaussian function |
| 2D convolution | Kernel slides across two spatial axes |
| 3D convolution | Kernel slides across three spatial/depth axes |
| NCHW | PyTorch layout: batch, channel, height, width |
| NCDHW | PyTorch 3D layout: batch, channel, depth, height, width |
| Upsampling | Fixed enlargement of spatial resolution |
| Transposed convolution | Learnable operation that can produce larger feature maps |
| Checkerboard artifact | Periodic pattern caused by uneven overlap in some transposed convolutions |

---

## Self-check

Before continuing, make sure you can answer:

1. What happens numerically at one output pixel during convolution?
2. Why is a normalized box filter good for averaging?
3. Why can a Laplacian-like kernel reveal edges?
4. Why does direct convolution get expensive as kernel size grows?
5. What is the difference between `valid`, `same`, and `full`?
6. Why can zero padding create false edge responses?
7. When might symmetric padding be more natural?
8. Why does an asymmetric kernel expose the difference between correlation and convolution?
9. What does the peak in a correlation map represent?
10. Why is NCC more robust than raw cross-correlation under brightness/contrast changes?
11. What are the three main computational steps of FFT-based convolution?
12. Why is Gaussian blur a low-pass filter?
13. Why can direct convolution beat FFT convolution for a 3×3 kernel?
14. Why do FFT approaches require attention to padding and periodic boundaries?
15. What dimensions does PyTorch `Conv2d` slide across?
16. Why can RGB still be handled by `Conv2d`?
17. When is `Conv3d` appropriate?
18. How does fixed upsampling differ from transposed convolution?
19. What causes checkerboard artifacts in some transposed convolutions?
20. Which library/API would you choose for a real-time 3×3 filter, and what factors would affect that choice?

---

## Retain this idea

**Convolution is a reusable local pattern operator. In the spatial domain it looks like a kernel sliding over neighborhoods; in the frequency domain the same linear filtering becomes multiplication. Correlation uses similar machinery for matching, and deep-learning convolutions extend the same core idea across channels, volumes, and learned filters.**
        """,

        "estimated_minutes": 300,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "convolution-mental-model",
                "title": "Convolution: One Operation, Many Image-Processing Tasks",
                "order": 1,
            },
            {
                "id": "spatial-convolution",
                "title": "Spatial-Domain Convolution",
                "order": 2,
            },
            {
                "id": "convolution-modes-boundaries",
                "title": "Output Modes and Boundary Handling",
                "order": 3,
            },
            {
                "id": "library-implementations",
                "title": "Applying Kernels with SciPy and OpenCV",
                "order": 4,
            },
            {
                "id": "correlation-vs-convolution",
                "title": "Correlation versus Convolution",
                "order": 5,
            },
            {
                "id": "template-matching",
                "title": "Template Matching with Cross-Correlation",
                "order": 6,
            },
            {
                "id": "normalized-cross-correlation",
                "title": "Normalized Cross-Correlation",
                "order": 7,
            },
            {
                "id": "frequency-domain-convolution",
                "title": "The Convolution Theorem and Frequency-Domain Filtering",
                "order": 8,
            },
            {
                "id": "gaussian-frequency-filter",
                "title": "Gaussian Blur in the Frequency Domain",
                "order": 9,
            },
            {
                "id": "runtime-tradeoffs",
                "title": "Choosing Spatial or FFT Convolution",
                "order": 10,
            },
            {
                "id": "two-vs-three-dimensional-convolution",
                "title": "2D and 3D Convolution",
                "order": 11,
            },
            {
                "id": "upsampling-transposed-convolution",
                "title": "Upsampling versus Transposed Convolution",
                "order": 12,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M05.L01.EX01",

            "title": "Filter an Image and Find a Template",

            "lesson_code": "M05.L01",

            "section_id": "normalized-cross-correlation",

            "placement": "after_section",

            "description": (
                "Practice convolution, boundary handling, correlation, and normalized "
                "template matching in one small image-processing workflow."
            ),

            "instructions": (
                "1. Load one grayscale image and normalize it to a known numerical range.\n"
                "2. Apply a normalized 3×3 box blur using spatial convolution with "
                "mode='same'.\n"
                "3. Apply a sharpening or Laplacian-like kernel to the original image.\n"
                "4. Repeat one filter with zero/fill padding and symmetric padding, then "
                "compare the image borders.\n"
                "5. Select a small distinctive template from the image.\n"
                "6. Compute ordinary cross-correlation and locate its maximum response.\n"
                "7. Compute normalized cross-correlation using either your own function or "
                "cv2.matchTemplate(..., TM_CCOEFF_NORMED).\n"
                "8. Modify the image brightness or contrast and compare how raw correlation "
                "and NCC respond.\n"
                "9. Mark the detected location on the source image.\n"
                "10. Explain why correlation—not convolution—is the natural operation for "
                "matching the template without reversing its appearance."
            ),

            "expected_output": (
                "A notebook or script showing blur/sharpen results, a border-condition "
                "comparison, the chosen template, raw correlation and NCC maps, detected "
                "locations, and a short explanation of robustness and kernel flipping."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "spatial-convolution",
                "boundary-handling",
                "correlation",
                "template-matching",
                "normalized-cross-correlation",
                "opencv",
                "scipy-signal",
            ],
        },

        {
            "id": "M05.L01.EX02",

            "title": "Compare Spatial, FFT, and Learned Convolution",

            "lesson_code": "M05.L01",

            "section_id": "upsampling-transposed-convolution",

            "placement": "after_section",

            "description": (
                "Connect classical spatial filtering, FFT convolution, and PyTorch "
                "convolutional operators through one set of experiments."
            ),

            "instructions": (
                "1. Load one grayscale image and construct a small Gaussian kernel.\n"
                "2. Blur the image once with direct spatial convolution and once with "
                "signal.fftconvolve(), using compatible output modes.\n"
                "3. Compute the maximum or mean absolute difference between the two "
                "outputs and explain any boundary-related discrepancy.\n"
                "4. Repeat the timing comparison with at least one substantially larger "
                "kernel and record the runtimes on your machine.\n"
                "5. Display the original and blurred Fourier magnitude spectra and explain "
                "what happened to high-frequency content.\n"
                "6. Convert an image to a PyTorch NCHW tensor and apply one Conv2d edge "
                "kernel.\n"
                "7. Explain why an RGB image can still be handled by Conv2d even though "
                "it has three channels.\n"
                "8. Demonstrate fixed 2× upsampling and one ConvTranspose2d example.\n"
                "9. Record output shapes and inspect the transposed-convolution result for "
                "uneven/checkerboard patterns.\n"
                "10. Summarize when you would choose direct convolution, FFT convolution, "
                "Conv2d, or ConvTranspose2d."
            ),

            "expected_output": (
                "A notebook or script with spatial-versus-FFT blur comparisons and timing, "
                "frequency spectra, one PyTorch Conv2d result, fixed upsampling and "
                "ConvTranspose2d outputs, shape checks, and a short method-selection summary."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "fftconvolve",
                "convolution-theorem",
                "runtime-benchmarking",
                "frequency-response",
                "pytorch-conv2d",
                "upsampling",
                "transposed-convolution",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M05.L01.QZ01",

        "title": "Convolution and Spatial/Frequency Domain Filtering — Knowledge Check",

        "lesson_code": "M05.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M05.L01.Q01",
                "section_id": "convolution-mental-model",
                "question": (
                    "What does a convolution kernel do at one spatial location?"
                ),
                "options": [
                    "It renames the image file",
                    "It computes a weighted sum of a local image neighborhood",
                    "It always converts RGB to grayscale",
                    "It sorts all image pixels globally",
                ],
                "correct": 1,
                "explanation": (
                    "The local kernel values are multiplied by overlapping image values "
                    "and the products are summed to form an output response."
                ),
            },

            {
                "id": "M05.L01.Q02",
                "section_id": "spatial-convolution",
                "question": (
                    "Why is a 3×3 box-blur kernel commonly divided by 9?"
                ),
                "options": [
                    "To make its weights sum to one so constant brightness is preserved",
                    "To flip the kernel",
                    "To perform normalized cross-correlation",
                    "To increase image dimensions",
                ],
                "correct": 0,
                "explanation": (
                    "Nine equal weights of 1/9 compute the neighborhood mean and preserve "
                    "a constant region."
                ),
            },

            {
                "id": "M05.L01.Q03",
                "section_id": "convolution-modes-boundaries",
                "question": (
                    "Which convolution mode returns only positions where the kernel fully "
                    "fits inside the source image without padding?"
                ),
                "options": [
                    "same",
                    "full",
                    "valid",
                    "wrap",
                ],
                "correct": 2,
                "explanation": (
                    "Valid convolution excludes boundary positions requiring values outside "
                    "the source."
                ),
            },

            {
                "id": "M05.L01.Q04",
                "section_id": "convolution-modes-boundaries",
                "question": (
                    "Why can zero padding create false responses near image boundaries?"
                ),
                "options": [
                    "It can introduce an artificial intensity jump between the image and zeros",
                    "It changes every kernel to a Gaussian",
                    "It disables multiplication",
                    "It forces the image to become periodic",
                ],
                "correct": 0,
                "explanation": (
                    "A filter—especially an edge detector—may respond to the artificial "
                    "transition created by zero-valued padding."
                ),
            },

            {
                "id": "M05.L01.Q05",
                "section_id": "correlation-vs-convolution",
                "question": (
                    "What is the defining operational difference between correlation and convolution?"
                ),
                "options": [
                    "Correlation is always in the frequency domain",
                    "Convolution flips the kernel while correlation applies it without that flip",
                    "Correlation works only with RGB images",
                    "Convolution cannot use small kernels",
                ],
                "correct": 1,
                "explanation": (
                    "Kernel reversal is the key mathematical distinction."
                ),
            },

            {
                "id": "M05.L01.Q06",
                "section_id": "template-matching",
                "question": (
                    "In ordinary correlation-based template matching, what does a strong peak "
                    "in the correlation map usually indicate?"
                ),
                "options": [
                    "A location whose image patch is highly similar to the template",
                    "A location where the image has zero intensity",
                    "The image file format",
                    "A Fourier DC component only",
                ],
                "correct": 0,
                "explanation": (
                    "The template produces a large correlation response where local structure "
                    "matches it strongly."
                ),
            },

            {
                "id": "M05.L01.Q07",
                "section_id": "normalized-cross-correlation",
                "question": (
                    "What is the main benefit of normalized cross-correlation over raw cross-correlation?"
                ),
                "options": [
                    "It eliminates all scale and rotation problems",
                    "It reduces sensitivity to local brightness and contrast differences",
                    "It always runs without a template",
                    "It converts correlation into convolution",
                ],
                "correct": 1,
                "explanation": (
                    "Mean subtraction and standard-deviation normalization make the score "
                    "less dependent on intensity offset and scale."
                ),
            },

            {
                "id": "M05.L01.Q08",
                "section_id": "frequency-domain-convolution",
                "question": (
                    "According to the convolution theorem, spatial-domain convolution "
                    "corresponds to what operation in the frequency domain?"
                ),
                "options": [
                    "Element-wise multiplication",
                    "Sorting",
                    "Image rotation",
                    "Matrix inversion only",
                ],
                "correct": 0,
                "explanation": (
                    "After transforming image and kernel, their Fourier representations are "
                    "multiplied element-wise, followed by inverse transformation."
                ),
            },

            {
                "id": "M05.L01.Q09",
                "section_id": "gaussian-frequency-filter",
                "question": "Why is a Gaussian blur considered a low-pass filter?",
                "options": [
                    "It preserves high frequencies and removes smooth regions",
                    "It preserves low-frequency variation while attenuating high-frequency detail",
                    "It changes only file metadata",
                    "It always detects edges",
                ],
                "correct": 1,
                "explanation": (
                    "Smoothing suppresses rapidly varying structures such as fine texture, "
                    "noise, and sharp detail."
                ),
            },

            {
                "id": "M05.L01.Q10",
                "section_id": "runtime-tradeoffs",
                "question": (
                    "When is direct spatial convolution often preferable to FFT convolution?"
                ),
                "options": [
                    "For small kernels where FFT setup overhead may dominate",
                    "Only for images larger than memory",
                    "Only when the image is already in the frequency domain",
                    "Never",
                ],
                "correct": 0,
                "explanation": (
                    "For small kernels, direct local computation is often efficient enough "
                    "that FFT overhead provides no advantage."
                ),
            },

            {
                "id": "M05.L01.Q11",
                "section_id": "two-vs-three-dimensional-convolution",
                "question": (
                    "Why can a normal RGB image be processed by Conv2d rather than Conv3d?"
                ),
                "options": [
                    "Conv2d can span all RGB input channels while sliding only over height and width",
                    "Conv2d ignores all but the red channel",
                    "RGB has no channel dimension",
                    "Conv3d cannot process numbers",
                ],
                "correct": 0,
                "explanation": (
                    "The convolution is called 2D because the kernel slides over two spatial "
                    "axes; channel depth is handled inside the filter weights."
                ),
            },

            {
                "id": "M05.L01.Q12",
                "section_id": "upsampling-transposed-convolution",
                "question": (
                    "Which statement best distinguishes fixed upsampling from transposed convolution?"
                ),
                "options": [
                    "Fixed upsampling uses a predetermined interpolation rule, while transposed convolution uses convolutional weights that can be learned",
                    "They are always numerically identical",
                    "Transposed convolution cannot increase spatial size",
                    "Fixed upsampling requires more trainable parameters",
                ],
                "correct": 0,
                "explanation": (
                    "Interpolation applies a fixed geometric rule, whereas transposed "
                    "convolution introduces trainable filter weights."
                ),
            },

            {
                "id": "M05.L01.Q13",
                "section_id": "upsampling-transposed-convolution",
                "type": "open",
                "question": (
                    "Design a pipeline that first smooths a noisy image, then locates a known "
                    "template, and finally produces a 2× learned-resolution feature map in "
                    "PyTorch. Explain which stages use convolution, correlation/NCC, FFT or "
                    "spatial filtering, and transposed convolution or upsampling, and justify "
                    "your choice for each stage."
                ),
            },
        ],

        "passing_score": 70,
    },
}
