"""M02.L01 — Image Manipulation.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 2. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M02.L01"

MODULE_ORDER = 2

MODULE_TITLE = "Practical Image Manipulation"

MODULE_DESCRIPTION = (
    "Learn to modify image appearance and geometry safely with NumPy, scikit-image, "
    "and Pillow; build intuition for masks, intensity transforms, inverse warping, "
    "resampling, noise, channels, transparency, compositing, and blend modes."
)

SOURCE_CHAPTER = 2

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Image Manipulation",

    "slug": "image-processing-m02-l01",

    "description": (
        "A hands-on lesson on manipulating images with NumPy, scikit-image, and "
        "Pillow, covering selective color, distortion correction, intensity and "
        "geometric transforms, resizing, cropping, noise, channels, drawing, "
        "transparency, compositing, and blending."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.5,

    "skill_tags": [
        "image-processing",
        "image-manipulation",
        "numpy",
        "scikit-image",
        "pillow",
        "masking",
        "geometric-transformations",
        "inverse-warping",
        "resampling",
        "noise",
        "image-channels",
        "alpha-compositing",
        "blending",
    ],

    "prerequisite_ids": ["M01.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Image Manipulation",

        "content": r"""
# Image Manipulation

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M02.L01  
> **Module:** Practical Image Manipulation  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 2. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Treat image manipulation as controlled transformations of pixel values, coordinates, or channels.
- Build masks for selective-color effects with NumPy and HSV representations.
- Explain the idea behind fish-eye correction and distinguish demonstration code from calibrated lens correction.
- Apply inversion, gamma adjustment, contrast stretching, and common noise models.
- Explain why geometric transformations normally use inverse mapping and interpolation.
- Distinguish translation, rotation, similarity, affine, projective, swirl, and piecewise-affine transforms.
- Resize and crop images while reasoning about interpolation, anti-aliasing, aspect ratio, and regions of interest.
- Apply point transformations such as log, power-law, thresholding, inversion, solarization, and posterization.
- Draw annotations, inspect image statistics, and split or merge color channels.
- Work safely with alpha transparency, image blending, masks, compositing, watermarks, and blend modes.
- Combine several manipulation techniques into a small practical image-processing workflow.

---

## 1. What does it mean to manipulate an image?

An image in Python is ultimately a grid of numerical values. Therefore, most image-manipulation operations can be understood as changing one of three things:

1. **Pixel values** — for example brightness, inversion, thresholding, or contrast.
2. **Pixel locations** — for example translation, rotation, scaling, or perspective correction.
3. **How channels or images are combined** — for example color-channel swapping, alpha compositing, or blending.

This mental model is more useful than memorizing individual functions.

### Three families of operations

| Family | What changes? | Examples |
|---|---|---|
| Intensity / point operation | Pixel value | inversion, gamma, log transform |
| Geometric operation | Pixel coordinate | rotate, translate, affine warp |
| Compositing operation | Contribution of multiple images/channels | masks, alpha blend, overlay |

A fourth practical family is **sampling/resolution change**, which appears in resizing, downsampling, pixelation, and resampling after geometric transformations.

### Why several libraries?

This chapter uses three main tools:

- **NumPy** for direct array manipulation, Boolean masks, and numerical operations.
- **scikit-image** for higher-level image-processing functions, transformations, exposure operations, and noise models.
- **Pillow (PIL)** for convenient image editing, resizing, point transforms, drawing, transparency, and compositing.

The goal is not to decide that one library is universally best. The useful skill is recognizing the numerical operation and then choosing a convenient tool.

[[IMAGE_NEEDED: Image manipulation mental model | A diagram with one input image branching into pixel-value transforms, geometric-coordinate transforms, and channel/compositing transforms, with 2–3 examples under each branch | Learner should see that many different APIs reduce to a few reusable mathematical ideas]]

---

## 2. Selective color and distortion correction

### Selective color with a mask

A **color-pop** or **selective-color** effect preserves one chosen color region while desaturating the rest.

The useful idea is not the photographic effect itself. The useful idea is the pipeline:

1. Convert the image into a representation where the property of interest is easier to isolate.
2. Build a Boolean mask.
3. Create a baseline output.
4. Copy original pixels back wherever the mask is `True`.

HSV is convenient because **Hue** represents color type more directly than raw RGB values.

A simplified implementation is:

```python
import numpy as np
from skimage import color
from skimage.color import rgb2gray

def apply_color_pop(im):
    gray = rgb2gray(im)
    gray_rgb = np.stack((gray,) * 3, axis=-1)

    hsv = color.rgb2hsv(im)
    hue = hsv[..., 0]

    # Example interval for red-like hues in normalized HSV.
    red_mask = (hue <= 5 / 180) | (hue >= 175 / 180)

    gray_rgb[red_mask] = im[red_mask]
    return gray_rgb
```

The expression:

```python
gray_rgb[red_mask] = im[red_mask]
```

is the key. The mask decides **where** the original color is restored.

### Why HSV helps

In RGB, the same perceptual color can be represented by many combinations of red, green, and blue values. In HSV, color type is more directly represented by the hue channel, so color-based filtering often becomes easier to reason about.

[[IMAGE_NEEDED: Selective-color mask workflow | Show the original image, its hue channel or hue wheel, the Boolean mask for a selected color, and the final color-pop output | Learner should notice that the mask—not a special photo effect function—controls which pixels keep their color]]

### Fish-eye distortion

Fish-eye or barrel distortion bends straight lines, especially near image edges. A correction algorithm attempts to map output pixels back to locations in the distorted source.

A simplified educational correction can compute a radial distance from the image center and apply a nonlinear mapping:

```text
output coordinate
       ↓
distance from center
       ↓
radial correction rule
       ↓
source coordinate
       ↓
sample source pixel
```

The chapter demonstrates this with a custom `undistort()` function and a zoom parameter.

The important practical boundary is:

> A simple radial mapping is useful for learning geometric correction, but accurate real-camera undistortion normally requires camera calibration parameters and a lens distortion model.

In calibrated workflows, camera intrinsics and distortion coefficients are estimated and used by dedicated functions such as those provided by OpenCV.

---

## 3. Intensity transforms, contrast, noise, and distributions

Many useful manipulations modify pixel values without changing their coordinates.

### Image inversion

For a normalized image in `[0, 1]`:

```text
output = 1 - input
```

For an 8-bit image in `[0, 255]`:

```text
output = 255 - input
```

With scikit-image:

```python
from skimage.util import invert

im_inv = invert(im)
```

This is a **point transformation**: every output value depends only on the corresponding input value.

### Gamma adjustment

Gamma correction is a nonlinear intensity transform. Conceptually:

```text
output = input ^ gamma
```

Its visual effect depends on the convention used by the library, so you should verify actual behavior rather than rely only on memorized verbal rules.

Example:

```python
from skimage import exposure

brightened = exposure.adjust_gamma(im, gamma=1.5)
```

The deeper lesson is that nonlinear transforms redistribute intensity values rather than simply adding a constant.

### Contrast stretching

A low-contrast image may use only a narrow part of the available intensity range. Contrast stretching remaps a selected input interval to a broader output interval.

```python
stretched = exposure.rescale_intensity(
    im,
    in_range=(0.2, 0.8)
)
```

Values around the selected low/high boundaries are spread over a wider range, making differences more visible.

### Cumulative distribution function

For a random variable `X`, the cumulative distribution function is:

```text
F(x) = P(X <= x)
```

For an image channel, it tells us what fraction of pixels have intensity less than or equal to a chosen value.

The CDF is important because it connects image intensities with probability and later becomes useful in operations such as histogram equalization.

For RGB images, each channel can have its own distribution:

```python
from skimage import exposure

cdf_r = exposure.cumulative_distribution(im[:, :, 0])
cdf_g = exposure.cumulative_distribution(im[:, :, 1])
cdf_b = exposure.cumulative_distribution(im[:, :, 2])
```

### Gaussian noise

Gaussian noise adds random values sampled from a normal distribution.

A useful model is:

```text
noisy_pixel = original_pixel + noise
noise ~ N(mean, variance)
```

The standard deviation `sigma` controls the typical magnitude of the noise, while variance is:

```text
variance = sigma^2
```

With scikit-image:

```python
from skimage.util import random_noise

noisy = random_noise(im, mode="gaussian", var=0.01)
```

Different noise models represent different physical or synthetic effects:

| Noise model | Basic idea |
|---|---|
| Gaussian | additive normally distributed noise |
| Poisson | count-dependent noise |
| salt & pepper | random pixels become minimum or maximum intensity |
| speckle | multiplicative noise related to image intensity |

[[IMAGE_NEEDED: Noise model comparison | Show the same clean grayscale image beside Gaussian, salt-and-pepper, Poisson, and speckle versions | Learner should compare the visual structure of each noise model rather than treating all noise as the same phenomenon]]

### A useful rule

Before applying intensity arithmetic, inspect:

```python
print(im.dtype)
print(im.min(), im.max())
```

A transform that makes sense for floating-point `[0, 1]` data may behave incorrectly on unsigned 8-bit data if you do not account for range, overflow, or clipping.

---

## 4. Geometric transformations and inverse warping

Geometric transformations change **where image information appears**.

Common examples include:

- translation,
- rotation,
- scaling,
- shearing,
- similarity transforms,
- affine transforms,
- projective transforms,
- nonlinear warps such as swirl.

### Why inverse mapping is used

Suppose we move input pixels forward into a new image.

A forward transform answers:

```text
Where does this input pixel go?
```

The problem is that some output pixels may receive no value, while multiple input pixels may land near the same output position.

Inverse mapping asks the more useful reconstruction question:

```text
For this output pixel, where should I sample from in the input image?
```

This ensures that every output location has a source coordinate to sample.

{{image:forward-vs-inverse-warping}}

### Interpolation

Inverse mapping often returns non-integer coordinates such as:

```text
(125.4, 88.7)
```

There is no physical pixel exactly at that coordinate, so the library estimates a value from nearby pixels.

Common interpolation approaches include:

- nearest-neighbor,
- bilinear,
- bicubic.

Interpolation is therefore part of geometric transformation—not an unrelated visualization detail.

### Translation

Translation shifts every coordinate by a constant displacement:

```text
x' = x + tx
y' = y + ty
```

In homogeneous coordinates:

```text
[1  0  tx]
[0  1  ty]
[0  0   1]
```

### Rotation

A 2D rotation is represented by:

```text
[ cos(theta)  -sin(theta) ]
[ sin(theta)   cos(theta) ]
```

A subtle but important issue is the **center of rotation**.

Rotating about `(0, 0)` means rotating around the image origin, commonly the top-left corner. To rotate around the image center, conceptually:

1. translate the center to the origin,
2. rotate,
3. translate back.

### Rigid, similarity, affine, and projective transforms

These transforms form a useful progression.

| Transform | Can translate? | Rotate? | Scale? | Shear? | Key preservation |
|---|---:|---:|---:|---:|---|
| Rigid | yes | yes | no | no | distances and angles |
| Similarity | yes | yes | uniform | no | shape / angles |
| Affine | yes | yes | non-uniform | yes | parallel lines |
| Projective | yes | yes | yes | yes | straight lines |

A **similarity transform** combines uniform scaling, rotation, and translation.

An **affine transform** is more general and can include non-uniform scaling and shear.

A **projective transform** or homography can model perspective-like changes between planes. It preserves straight lines but does not represent arbitrary 3D camera geometry.

### scikit-image `warp()`

A high-level example:

```python
from skimage.transform import SimilarityTransform, warp
import numpy as np

tform = SimilarityTransform(
    scale=0.9,
    rotation=np.deg2rad(45),
    translation=(80, -40),
)

out = warp(im, tform.inverse)
```

Notice the use of:

```python
tform.inverse
```

That reflects the inverse-mapping idea.

### Nonlinear transformations

Not every transform can be represented by one global matrix.

**Swirl** rotates pixels by an amount that depends on distance from a chosen center.

```python
from skimage.transform import swirl

im_swirled = swirl(
    im,
    rotation=0,
    strength=5,
    radius=300,
)
```

**Piecewise affine transformation** divides the image into local regions and fits affine transforms between source and destination control points.

This gives much more flexible local deformation, but boundaries between locally fitted regions may introduce artifacts.

### Validation matters

When estimating a transformation from control points:

- source and destination arrays must correspond,
- enough non-collinear points must be provided,
- an estimation routine may return failure instead of raising an exception,
- you should check the returned status before warping.

{{exercise:M02.L01.EX01}}

---

## 5. Resizing, cropping, downsampling, and pixelation

These operations look simple, but they teach important sampling concepts.

### Resize versus rescale

A **resize** specifies the target dimensions directly.

```python
from skimage.transform import resize

small = resize(
    image,
    (image.shape[0] // 4, image.shape[1] // 4),
    anti_aliasing=True,
)
```

A **rescale** specifies a factor:

```python
from skimage.transform import rescale

quarter = rescale(image, 0.25, anti_aliasing=True)
```

### Upsampling

When enlarging an image, new pixel positions must be estimated.

Without suitable interpolation, enlargement can appear blocky.

In Pillow:

```python
large = im.resize(
    (im.width * 5, im.height * 5),
    Image.Resampling.BILINEAR,
)
```

### Downsampling and aliasing

When shrinking an image, multiple original pixels must be represented by fewer output pixels.

High-frequency patterns can become:

- jagged,
- falsely patterned,
- moiré-like,
- unstable.

These are forms of **aliasing**.

Anti-aliasing filters smooth high-frequency content before or during downsampling to reduce those artifacts.

```python
small = im.resize(
    (im.width // 5, im.height // 5),
    Image.Resampling.LANCZOS,
)
```

[[IMAGE_NEEDED: Resampling and aliasing | Show an original patterned image, a poor downsample with jagged/moiré artifacts, an anti-aliased downsample, and a nearest-neighbor enlarged version | Learner should distinguish resolution change from interpolation quality and recognize aliasing]]

### Preserve aspect ratio

If width and height are changed by unrelated factors, the scene becomes stretched.

A simple helper is:

```python
def resize_preserve_aspect_ratio(im, target_width, resample):
    ratio = im.height / im.width
    target_height = int(target_width * ratio)
    return im.resize((target_width, target_height), resample)
```

### Cropping

Cropping extracts a region of interest (ROI).

With Pillow:

```python
cropped = im.crop((left, top, right, bottom))
```

With NumPy, a rectangular region is often:

```python
roi = array[y1:y2, x1:x2]
```

Pay attention to coordinate conventions:

```text
Pillow geometric coordinates: (x, y)
NumPy indexing: array[row, column] -> array[y, x]
```

Mixing these conventions is a common source of ROI bugs.

### Pixelation

Pixelation can be built from two resize operations:

1. shrink the image,
2. enlarge it back with nearest-neighbor interpolation.

```python
def pixelate(im, factor):
    small = im.resize(
        (im.width // factor, im.height // factor),
        Image.Resampling.BILINEAR,
    )
    return small.resize(im.size, Image.Resampling.NEAREST)
```

This deliberately exposes large blocks instead of smoothing them.

### Region-specific pixelation

A processed version does not need to replace the whole image.

You can:

1. build a pixelated copy,
2. define a face or sensitive ROI,
3. copy only that region into the original.

This is a useful example of combining **geometric selection** with **pixel transformation**.

---

## 6. Point transformations and pixel-level effects with Pillow

A point transformation changes each pixel independently:

```text
output = T(input)
```

The transform does not need information from neighboring pixels.

### Log transformation

A logarithmic transform compresses a wide intensity range and can reveal detail in darker regions.

Conceptually:

```text
s = c * log(1 + r)
```

A Pillow-style implementation may normalize, apply the transform, and rescale:

```python
im_log = im_gray.point(
    lambda x: 255 * np.log(1 + x / 255)
)
```

### Power-law transformation

A power-law transform is:

```text
s = c * r^gamma
```

For normalized values, changing `gamma` changes how intensities are redistributed.

Example:

```python
im_gamma = im_gray.point(
    lambda x: 255 * (x / 255) ** 0.6
)
```

### Thresholding

A binary threshold converts a continuous range into discrete levels:

```python
poster = im.point(
    lambda x: 255 if x > 128 else 0
)
```

Applied independently to RGB channels, this can produce highly posterized colors.

### Lookup tables

A point operation does not need to be expressed as a formula. A lookup table can map every possible input value to a new output value.

For an 8-bit channel, a LUT has one mapping for each input value from `0` to `255`.

This is often faster and easier to reason about when the mapping is known in advance.

### Inversion

For 8-bit data:

```python
negative = im.point(lambda x: 255 - x)
```

### Solarization

Solarization reverses some intensity values while leaving others unchanged according to a threshold. The result mixes positive and negative-like tonal behavior.

Pillow provides:

```python
from PIL import ImageOps

solarized = ImageOps.solarize(im)
```

### Posterization

Posterization reduces the number of representable levels by reducing effective bit depth.

```python
posterized = ImageOps.posterize(im, 2)
```

Fewer levels mean flatter color regions and sharper tonal transitions.

[[IMAGE_NEEDED: Point transformation comparison | Show the same grayscale or RGB image as original, inverted, log transformed, gamma transformed, thresholded, solarized, and posterized | Learner should compare how different transfer functions redistribute intensities while leaving spatial coordinates unchanged]]

### Salt-and-pepper noise

Salt-and-pepper noise randomly replaces pixels with extreme values:

```text
salt   -> white / maximum intensity
pepper -> black / minimum intensity
```

A direct Pillow implementation may choose random coordinates and update them with `putpixel()`.

The broader lesson is that different noise models alter data differently. Gaussian noise perturbs values continuously; salt-and-pepper noise creates sparse impulses.

---

## 7. Drawing, image statistics, histograms, and channels

Image manipulation is not only about changing appearance. It also includes annotating and inspecting images.

### Drawing shapes and text

Pillow's `ImageDraw` lets you create annotations.

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(im)
draw.ellipse(
    (125, 125, 200, 250),
    outline="white",
    width=3,
)
```

For bounding boxes:

```python
bbox = im.getbbox()
draw.rectangle(bbox, outline="red", width=3)
```

And for text:

```python
draw.text((10, 5), "Detected object")
```

Annotations are useful in:

- debugging,
- dataset inspection,
- detection visualization,
- reports,
- human review workflows.

### Pasting images

`paste()` places one image inside another at a chosen coordinate.

This is a simple compositing operation and is useful for:

- creating collages,
- adding logos,
- inserting thumbnails,
- visual debugging.

### Basic statistics

Pixel statistics help you understand data before selecting transformations.

Pillow can compute quantities such as:

- extrema,
- mean,
- median,
- standard deviation,
- count.

These can answer questions like:

> Is this image globally dark?  
> Does one channel dominate?  
> Is the image using its available range?

### Histograms

An image histogram counts how often intensity values appear.

For an RGB image, you can inspect a histogram for each channel separately.

A histogram helps reveal:

- clipped blacks or whites,
- narrow contrast range,
- channel imbalance,
- multi-modal intensity structure.

[[IMAGE_NEEDED: RGB histograms and channel views | Show an RGB image, separate red/green/blue channel visualizations, and aligned histograms for the three channels | Learner should connect visible color structure with the numerical distribution of each channel]]

### Splitting channels

Pillow can separate an RGB image:

```python
r, g, b = im.split()
```

Each result is a single-channel image.

### Merging channels

Channels can be recombined:

```python
swapped = Image.merge("RGB", (b, g, r))
```

Swapping channels changes image colors dramatically while preserving spatial structure.

This is a practical reminder:

> Channel order is part of the image representation. Correct dimensions alone do not guarantee correct color interpretation.

---

## 8. Transparency, masks, compositing, and blend modes

### The alpha channel

RGBA images add an **alpha channel**:

```text
R, G, B, A
```

Alpha controls visibility:

```text
alpha = 0     -> fully transparent
alpha = 255   -> fully opaque
```

for standard 8-bit alpha.

PNG supports transparency. JPEG does not support an alpha channel.

### Creating transparency from a mask

A grayscale image can act as an alpha mask.

Conceptually:

```text
bright mask value -> more opaque
dark mask value   -> more transparent
```

Example:

```python
from PIL import Image, ImageChops

img = Image.open("subject.jpg").convert("RGBA")
mask = Image.open("mask.jpg").convert("L")
mask = ImageChops.invert(mask)

img.putalpha(mask)
img.save("subject_transparent.png")
```

You can also build the alpha mask from color rules. For example, Boolean conditions on R, G, and B channels can keep only pixels matching a chosen color.

### Constant alpha blending

`Image.blend()` combines two equally sized, same-mode images using one global value `alpha`.

Conceptually:

```text
output = (1 - alpha) * image1 + alpha * image2
```

Therefore:

```text
alpha = 0 -> image1
alpha = 1 -> image2
```

Example:

```python
im2 = im2.resize(im1.size)
mixed = Image.blend(im1, im2, alpha=0.5)
```

### Alpha compositing

Alpha compositing is different from constant blending.

Each pixel may have its own alpha value, so different parts of the foreground can contribute different amounts.

Use it when the foreground already contains transparency:

```python
foreground = foreground.convert("RGBA")
background = background.convert("RGBA")

result = Image.alpha_composite(
    background,
    foreground,
)
```

[[IMAGE_NEEDED: Alpha blending versus alpha compositing | Show two source images, a constant 50% blend, an RGBA foreground with a spatially varying alpha mask, and the alpha-composited result | Learner should understand the difference between one global mixing factor and per-pixel transparency]]

### Watermarking

A watermark is a common compositing workflow:

1. convert the base image to RGBA,
2. resize the watermark,
3. paste it onto a transparent layer,
4. reduce the watermark layer's alpha,
5. alpha-composite the layer with the base image.

The useful lesson is not the logo itself. It is the idea of building a separate transparent overlay layer.

### Mask-based compositing

A mask can vary continuously across an image.

For example, a horizontal gradient can transition smoothly from one image to another.

```python
grad = np.linspace(0, 1, width)
mask_array = np.tile(grad, (height, 1))
mask = Image.fromarray(
    (255 * mask_array).astype(np.uint8)
)

out = Image.composite(
    image_a,
    image_b,
    mask,
)
```

The mask answers:

```text
How much of image A versus image B should appear at this pixel?
```

### Hard Light, Soft Light, and Overlay

Blend modes combine two images pixel-by-pixel with nonlinear rules.

**Hard Light**

- darker blend values tend toward Multiply-like behavior,
- brighter blend values tend toward Screen-like behavior,
- effect is relatively strong.

**Soft Light**

- also darkens shadows and brightens highlights,
- transitions are gentler,
- useful for softer lighting effects.

**Overlay**

- also combines Multiply-like and Screen-like behavior,
- but the base image drives which behavior dominates.

The exact formulas matter in implementation, but the conceptual distinction is:

```text
hard light -> stronger contrast driven by blend image
soft light -> gentler contrast / lighting
overlay    -> contrast behavior driven by base image
```

### Lighter and darker combinations

Another type of composition simply compares pixels.

A "lighter" operation keeps the larger channel value at each position.

Conceptually:

```text
output = max(image1, image2)
```

A "darker" operation uses:

```text
output = min(image1, image2)
```

These are simple but powerful examples of image arithmetic.

### Choosing the right combination method

| Goal | Good mental model |
|---|---|
| mix two whole images uniformly | constant alpha blend |
| place transparent foreground over background | alpha composite |
| reveal images according to a spatial region | mask composite |
| add a semi-transparent logo | overlay layer + alpha composite |
| create lighting/contrast interaction | blend mode |
| keep brightest/darkest contribution | pixel-wise max/min |

{{exercise:M02.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Geometric transformation means moving input pixels directly into their new output positions.

### Why this is incomplete

That is the **forward-mapping** view, but image reconstruction commonly uses inverse mapping: for each output pixel, find where to sample from the source. This helps avoid unfilled holes and supports interpolation.

### Misconception 2

> Resizing an image only changes its width and height.

### Why this is incomplete

Resizing also requires a sampling strategy. Enlarging requires interpolation; shrinking can produce aliasing unless high-frequency information is handled appropriately.

### Misconception 3

> Alpha blending and alpha compositing are the same thing.

### Why this is wrong

A simple blend often uses one constant global `alpha`. Alpha compositing uses per-pixel alpha values, allowing spatially varying transparency.

### Misconception 4

> Any fish-eye correction function is suitable for accurate camera calibration.

### Why this is wrong

A simplified radial transform can demonstrate the concept, but precise lens correction requires a calibrated camera model and distortion parameters.

### Misconception 5

> If an image operation looks visually correct, its numerical representation must also be correct.

### Why this is dangerous

You still need to check data type, value range, channel order, coordinate convention, interpolation behavior, and clipping. A visually plausible result can hide numerical mistakes.

---

## Key terminology

| Term | Meaning |
|---|---|
| Point transformation | Pixel-value mapping where each output pixel depends on the corresponding input pixel |
| Boolean mask | True/False array used to select image regions |
| HSV | Color space separating hue, saturation, and value |
| Geometric transform | Operation that changes spatial pixel coordinates |
| Inverse mapping | For each output coordinate, find the corresponding input coordinate |
| Interpolation | Estimating a value at a non-integer coordinate from neighboring samples |
| Homogeneous coordinates | Matrix-friendly coordinate representation used for geometric transforms |
| Similarity transform | Uniform scaling + rotation + translation |
| Affine transform | Transform supporting translation, rotation, non-uniform scaling, shear, and reflection |
| Projective transform | Homography-based transform preserving straight lines |
| Aliasing | Distortion caused by insufficient sampling during resolution reduction |
| Anti-aliasing | Filtering used to reduce aliasing before/during downsampling |
| ROI | Region of interest selected from an image |
| Gamma / power-law transform | Nonlinear mapping of intensity values |
| Histogram | Frequency distribution of pixel intensity values |
| CDF | Cumulative probability distribution of intensities |
| Alpha channel | Per-pixel transparency/opacity channel |
| Alpha blending | Mixing images using a weighting factor |
| Alpha compositing | Combining transparent layers using per-pixel alpha |
| Blend mode | Pixel-wise formula for combining a base and blend image |

---

## Self-check

Before continuing, make sure you can answer:

1. Why can HSV make selective-color masking easier than RGB?
2. What is the difference between changing pixel values and changing pixel coordinates?
3. Why does inverse warping reduce holes in transformed images?
4. Why is interpolation needed during geometric transforms?
5. How does an affine transform differ from a similarity transform?
6. Why can downsampling create aliasing?
7. What is the difference between Gaussian and salt-and-pepper noise?
8. Why should aspect ratio usually be preserved while resizing?
9. What does an alpha value represent?
10. When would you choose `Image.blend()`, `Image.alpha_composite()`, or `Image.composite()`?
11. What information can an image histogram reveal?
12. Why is checking dtype and value range important before arithmetic?

---

## Retain this idea

**Image manipulation becomes much easier when you stop memorizing effects and instead ask three questions: what pixel values change, what coordinates change, and how are channels or images combined?**
        """,

        "estimated_minutes": 270,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "manipulation-mental-model",
                "title": "What Does It Mean to Manipulate an Image?",
                "order": 1,
            },
            {
                "id": "selective-color-distortion",
                "title": "Selective Color and Distortion Correction",
                "order": 2,
            },
            {
                "id": "intensity-exposure-noise",
                "title": "Intensity Transforms, Contrast, Noise, and Distributions",
                "order": 3,
            },
            {
                "id": "geometric-transformations",
                "title": "Geometric Transformations and Inverse Warping",
                "order": 4,
            },
            {
                "id": "resize-crop-pixelate",
                "title": "Resizing, Cropping, Downsampling, and Pixelation",
                "order": 5,
            },
            {
                "id": "pil-point-effects",
                "title": "Point Transformations and Pixel-Level Effects with Pillow",
                "order": 6,
            },
            {
                "id": "drawing-stats-channels",
                "title": "Drawing, Image Statistics, Histograms, and Channels",
                "order": 7,
            },
            {
                "id": "alpha-blending-compositing",
                "title": "Transparency, Masks, Compositing, and Blend Modes",
                "order": 8,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M02.L01.EX01",

            "title": "Build and Explain a Geometric Transformation Pipeline",

            "lesson_code": "M02.L01",

            "section_id": "geometric-transformations",

            "placement": "after_section",

            "description": (
                "Practice geometric transformation as coordinate mapping rather than "
                "treating rotation, translation, and affine warping as unrelated API calls."
            ),

            "instructions": (
                "1. Load one RGB image and record its shape.\n"
                "2. Apply a translation and display the result.\n"
                "3. Rotate the image once around the origin and once around its center; "
                "compare the outputs.\n"
                "4. Apply one SimilarityTransform or AffineTransform with at least two "
                "effects combined, such as rotation + translation or scale + shear.\n"
                "5. For one transformed output, explain why inverse mapping is useful.\n"
                "6. Repeat one transformation with two interpolation settings and note "
                "the visible difference.\n"
                "7. Identify any pixels or regions lost because they moved outside the "
                "output canvas.\n"
                "8. In two or three sentences, distinguish rigid, similarity, affine, "
                "and projective transformations."
            ),

            "expected_output": (
                "A runnable notebook or Python script showing the original plus at least "
                "four transformed outputs, accompanied by short explanations of inverse "
                "mapping, interpolation, center of rotation, and transformation type."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "translation",
                "rotation",
                "inverse-warping",
                "interpolation",
                "similarity-transform",
                "affine-transform",
                "geometric-reasoning",
            ],
        },

        {
            "id": "M02.L01.EX02",

            "title": "Create a Selective Edit and Composite",

            "lesson_code": "M02.L01",

            "section_id": "alpha-blending-compositing",

            "placement": "after_section",

            "description": (
                "Combine masks, resizing, channel reasoning, and compositing into one "
                "small practical image-editing workflow."
            ),

            "instructions": (
                "1. Load a color image and create a selective mask using either HSV hue "
                "thresholds, RGB channel conditions, or a grayscale intensity threshold.\n"
                "2. Use the mask to create one selective effect, such as preserving a "
                "color while desaturating the background.\n"
                "3. Create a second image or overlay layer and resize it while preserving "
                "aspect ratio.\n"
                "4. Add transparency and composite the overlay onto the first image.\n"
                "5. Create one comparison output using either constant alpha blending, a "
                "gradient mask, or a blend mode.\n"
                "6. Display the original, the mask, the selective edit, and both composite "
                "results with labels.\n"
                "7. Record the mode, size, dtype/value range where relevant, and explain "
                "why the images had to be compatible before combining them.\n"
                "8. Describe one failure mode involving channel order, alpha, mask range, "
                "coordinate order, interpolation, or aspect ratio."
            ),

            "expected_output": (
                "A notebook or script containing a visible mask, one selective edit, at "
                "least two image-combination results, and a short written explanation of "
                "the numerical and geometric choices."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "masking",
                "hsv",
                "resizing",
                "alpha-channel",
                "alpha-compositing",
                "blending",
                "image-debugging",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M02.L01.QZ01",

        "title": "Image Manipulation — Knowledge Check",

        "lesson_code": "M02.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M02.L01.Q01",
                "section_id": "selective-color-distortion",
                "question": (
                    "Why is HSV often convenient for building a selective-color mask?"
                ),
                "options": [
                    "Because HSV removes the need for any mask",
                    "Because hue represents color type more directly than raw RGB channel combinations",
                    "Because every HSV image is automatically grayscale",
                    "Because HSV always has fewer pixels than RGB",
                ],
                "correct": 1,
                "explanation": (
                    "Hue separates color type from saturation and brightness, making many "
                    "color-thresholding tasks easier to express."
                ),
            },

            {
                "id": "M02.L01.Q02",
                "section_id": "intensity-exposure-noise",
                "question": (
                    "Which description best matches salt-and-pepper noise?"
                ),
                "options": [
                    "Every pixel is multiplied by exactly the same constant",
                    "Random pixels are replaced by extreme dark or bright values",
                    "The image is translated by random coordinates",
                    "Only the alpha channel is modified",
                ],
                "correct": 1,
                "explanation": (
                    "Salt-and-pepper noise consists of sparse impulse-like pixels set near "
                    "the minimum or maximum intensity."
                ),
            },

            {
                "id": "M02.L01.Q03",
                "section_id": "geometric-transformations",
                "question": (
                    "What does inverse mapping ask during an image transformation?"
                ),
                "options": [
                    "Where should each output pixel sample from in the input image?",
                    "Which file extension should be used for the output?",
                    "Which input channel has the largest mean?",
                    "How many histogram bins should be plotted?",
                ],
                "correct": 0,
                "explanation": (
                    "Inverse mapping reconstructs the output by mapping every destination "
                    "coordinate back to a source coordinate."
                ),
            },

            {
                "id": "M02.L01.Q04",
                "section_id": "geometric-transformations",
                "question": (
                    "Which transformation supports non-uniform scaling and shearing while "
                    "preserving parallel lines?"
                ),
                "options": [
                    "Rigid transform",
                    "Similarity transform",
                    "Affine transform",
                    "Simple inversion",
                ],
                "correct": 2,
                "explanation": (
                    "Affine transformations support translation, rotation, non-uniform "
                    "scaling, shear, and reflection while preserving parallelism."
                ),
            },

            {
                "id": "M02.L01.Q05",
                "section_id": "resize-crop-pixelate",
                "question": (
                    "Why is anti-aliasing especially important when shrinking an image?"
                ),
                "options": [
                    "It adds an alpha channel",
                    "It reduces artifacts caused by undersampling high-frequency detail",
                    "It converts RGB into HSV",
                    "It guarantees the image becomes sharper",
                ],
                "correct": 1,
                "explanation": (
                    "Downsampling can misrepresent fine detail; anti-aliasing suppresses "
                    "high-frequency content that the smaller grid cannot represent reliably."
                ),
            },

            {
                "id": "M02.L01.Q06",
                "section_id": "pil-point-effects",
                "question": (
                    "What defines a point transformation?"
                ),
                "options": [
                    "Each output pixel depends only on the corresponding input pixel value",
                    "Every output pixel depends on the entire image",
                    "Only spatial coordinates are changed",
                    "The image must always become binary",
                ],
                "correct": 0,
                "explanation": (
                    "Point transforms apply a value-mapping function independently at each "
                    "pixel location."
                ),
            },

            {
                "id": "M02.L01.Q07",
                "section_id": "drawing-stats-channels",
                "question": (
                    "What happens if the red and blue channels of an RGB image are swapped "
                    "during merging?"
                ),
                "options": [
                    "The image geometry changes",
                    "The image is automatically cropped",
                    "Colors change while the spatial layout remains the same",
                    "The image becomes transparent",
                ],
                "correct": 2,
                "explanation": (
                    "Channel swapping changes how stored values are interpreted as colors "
                    "without moving the pixel coordinates."
                ),
            },

            {
                "id": "M02.L01.Q08",
                "section_id": "alpha-blending-compositing",
                "question": (
                    "What is the key difference between simple constant alpha blending and "
                    "alpha compositing?"
                ),
                "options": [
                    "Blending can only work on grayscale images",
                    "Alpha compositing can use spatially varying per-pixel transparency",
                    "Alpha compositing never uses RGB values",
                    "Constant blending always changes image geometry",
                ],
                "correct": 1,
                "explanation": (
                    "A simple blend commonly uses one global mixing factor, while alpha "
                    "compositing combines RGBA layers using per-pixel alpha."
                ),
            },

            {
                "id": "M02.L01.Q09",
                "section_id": "alpha-blending-compositing",
                "question": (
                    "You need one side of an image to gradually transition into a second "
                    "image. Which approach is most directly suited to this?"
                ),
                "options": [
                    "A spatial gradient mask used for compositing",
                    "A rigid transform",
                    "A histogram count only",
                    "A binary file rename",
                ],
                "correct": 0,
                "explanation": (
                    "A gradient mask provides a different mixing weight at each position, "
                    "creating a smooth spatial transition."
                ),
            },

            {
                "id": "M02.L01.Q10",
                "section_id": "alpha-blending-compositing",
                "type": "open",
                "question": (
                    "Design a small pipeline that anonymizes one region of an image, adds "
                    "a semi-transparent watermark, and creates a smaller preview. Explain "
                    "which operations you would use, in what order, and why interpolation, "
                    "masking, aspect ratio, and alpha handling matter."
                ),
            },
        ],

        "passing_score": 70,
    },
}
