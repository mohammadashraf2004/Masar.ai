"""M03.L01 — More Image Manipulation.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 3. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M03.L01"

MODULE_ORDER = 3

MODULE_TITLE = "Advanced Image Manipulation"

MODULE_DESCRIPTION = (
    "Extend practical image manipulation skills across Pillow, OpenCV, SciPy, "
    "Wand/ImageMagick, Matplotlib, and Pilgram while learning reusable concepts "
    "such as compression, lookup tables, interpolation, homography, distortion "
    "correction, color grading, and procedural visual effects."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "More Image Manipulation",

    "slug": "image-processing-m03-l01",

    "description": (
        "A practical continuation of image manipulation covering JPEG quality, "
        "LUT-based color grading, gamma correction, blur and vignette effects, "
        "OpenCV transformations and homography, fisheye correction, SciPy "
        "interpolation, Wand effects, Matplotlib annotations and contours, "
        "and Instagram-style filters."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 5.0,

    "skill_tags": [
        "image-processing",
        "image-manipulation",
        "pillow",
        "opencv",
        "scipy",
        "wand",
        "matplotlib",
        "pilgram",
        "jpeg-compression",
        "lut",
        "gamma-correction",
        "homography",
        "fisheye-correction",
        "interpolation",
        "color-grading",
        "image-effects",
    ],

    "prerequisite_ids": ["M02.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "More Image Manipulation",

        "content": r"""
# More Image Manipulation

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M03.L01  
> **Module:** Advanced Image Manipulation  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 3. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain the trade-off between JPEG compression, file size, and visible image quality.
- Distinguish image resolution from compression quality.
- Use lookup tables for color grading and efficient gamma correction.
- Explain how lens blur, vignetting, temperature adjustment, and palette remapping change an image.
- Use Pillow for deformation, colorization, procedural image generation, and photographic effects.
- Rotate and flip images with OpenCV while controlling cropping, interpolation, and border behavior.
- Explain homography as a projective mapping between planes and use corresponding points correctly.
- Distinguish simplified distortion effects from calibrated fisheye correction.
- Use SciPy `ndimage` for affine transformations, zooming, spline interpolation, and coordinate-based warping.
- Recognize when Wand/ImageMagick provides a convenient high-level image-effect pipeline.
- Annotate images and interpret contour plots with Matplotlib.
- Explain what Instagram-like filters fundamentally do instead of treating them as magic presets.
- Choose an appropriate Python image library based on the task.

---

## 1. The bigger picture: effects are combinations of a few ideas

This chapter introduces many libraries and visual effects. At first, it may look like a long list of unrelated functions:

- JPEG quality,
- LUTs,
- gamma correction,
- lens blur,
- color temperature,
- vignette,
- rotation,
- homography,
- fisheye correction,
- spline interpolation,
- wave distortion,
- sketch effects,
- contours,
- Instagram-style filters.

The important learning goal is to see the common ideas underneath them.

Most of these operations are combinations of:

1. **Value mapping** — change pixel intensities or colors.
2. **Spatial mapping** — move information from one coordinate to another.
3. **Resampling** — estimate values at new coordinates.
4. **Neighborhood filtering** — compute a pixel from nearby pixels.
5. **Masking/compositing** — apply an effect only in selected regions.
6. **Encoding/compression** — change how image information is stored.
7. **Visualization/annotation** — add information without changing the underlying scene interpretation.

### Library map

| Library | Strong use in this chapter |
|---|---|
| Pillow / PIL | file encoding, LUTs, color effects, blur, palette work, generated images |
| OpenCV | efficient geometric transforms, real-time processing, homography, remapping |
| SciPy `ndimage` | numerical geometric transforms, interpolation, coordinate mapping |
| Wand / ImageMagick | high-level artistic effects and distortion operations |
| Matplotlib | visualization, annotations, contour representation |
| Pilgram | ready-made Instagram-like and CSS-style filter pipelines |

You do not need to memorize every library function. Learn the **operation**, then learn one or two convenient implementations.

[[IMAGE_NEEDED: Advanced image manipulation concept map | A diagram connecting value mapping, spatial mapping, interpolation, filtering, masking/compositing, compression, and visualization to example effects such as gamma, homography, blur, vignette, JPEG, and contours | Learner should see that many APIs are implementations of a small number of reusable ideas]]

---

## 2. JPEG quality, compression, and visible artifacts

A common beginner mistake is to use the words **quality**, **resolution**, and **file size** as if they mean the same thing.

They do not.

### Resolution

Resolution usually refers to image dimensions:

```text
width × height
```

For example:

```text
1920 × 1080
```

Changing resolution changes the number of pixels.

### JPEG quality

The JPEG `quality` parameter controls how aggressively information is discarded during **lossy compression**.

It does not necessarily change width or height.

With Pillow:

```python
from PIL import Image

im = Image.open("images/parrot.jpg")

for quality in [95, 20, 5, 1]:
    im.save(
        f"images/parrot_{quality}.jpg",
        quality=quality,
    )
```

The images can all have identical dimensions while having very different file sizes and visual fidelity.

### Why JPEG can become smaller

At a high level, JPEG processing includes ideas such as:

1. transform color representation,
2. optionally reduce chroma detail,
3. divide the image into small blocks,
4. represent each block with frequency information using the Discrete Cosine Transform,
5. quantize frequency coefficients,
6. encode the remaining information efficiently.

The chapter revisits the DCT later, so you do not need its full mathematics yet.

The key intuition is:

> Fine visual detail is associated with higher-frequency information. Stronger quantization can remove more of that information, producing a smaller file but more visible artifacts.

Common low-quality JPEG artifacts include:

- blocking,
- blur,
- ringing around edges,
- loss of fine texture.

[[IMAGE_NEEDED: JPEG quality comparison with zoomed crop | Show the same photograph saved at high, medium, low, and extremely low JPEG quality, with a magnified crop from each version | Learner should notice that dimensions can stay identical while fine detail, blocking, ringing, and file size change]]

### Measuring the trade-off

You can compare file sizes:

```python
import os

original_size = os.path.getsize("images/parrot.jpg")

for quality in [95, 20, 5, 1]:
    compressed_size = os.path.getsize(
        f"images/parrot_{quality}.jpg"
    )
    ratio = original_size / compressed_size
    print(quality, ratio)
```

A larger compression ratio means less storage relative to the original reference file.

However, a re-saved JPEG at quality `95` can sometimes be **larger** than the original. The original file may already have been compressed efficiently at a lower effective quality.

### JPEG versus PNG

JPEG is lossy.

PNG is lossless.

Therefore, Pillow's JPEG-style `quality` setting is not the correct control for PNG. PNG compression uses parameters such as `compress_level`.

The important distinction is:

```text
JPEG quality -> controls lossy fidelity/compression trade-off
PNG compression level -> attempts to store the same pixel information more compactly
```

---

## 3. Pillow: deformation, color grading, LUTs, and photographic effects

### Wave deformation

A wave deformation changes coordinates according to a periodic function.

Conceptually:

```text
x' = x
y' = y + A * sin(x / f)
```

where:

- `A` controls wave amplitude,
- `f` controls how rapidly the wave changes.

Pillow can apply a mesh-based deformation by dividing an image into patches and specifying how each patch maps back to the source.

The important concept is not the specific class definition. It is:

> A complex-looking distortion can be approximated by mapping many small regions from destination coordinates to source coordinates.

### Colorizing a grayscale image

Grayscale contains intensity but no chromatic color.

`ImageOps.colorize()` maps dark and bright intensities to chosen colors and interpolates the intermediate tones.

```python
from PIL import Image, ImageOps

im = Image.open("images/sculpture.png").convert("L")

colorized = ImageOps.colorize(
    im,
    black=(255, 0, 0),
    white=(255, 255, 127),
)
```

This is a form of **false-color mapping**.

If the grayscale image uses only a narrow intensity range, the result may look flat. Stretching contrast first can provide a richer mapping.

### Lookup tables for color grading

A **Lookup Table (LUT)** is a precomputed mapping:

```text
input value/color -> output value/color
```

LUTs are widely used for:

- color grading,
- cinematic looks,
- display transforms,
- fast repeated corrections.

A `.cube` LUT can encode RGB-to-RGB color transformations.

The useful mental model is:

```text
Original RGB
    ↓
predefined LUT mapping
    ↓
new RGB appearance
```

The image's geometry stays unchanged; its colors are remapped.

[[IMAGE_NEEDED: LUT color grading workflow | Show one original photograph, a simple conceptual RGB color cube/LUT mapping, and two different graded outputs from different LUTs | Learner should understand that a LUT changes color mapping rather than moving image geometry]]

### Gamma correction using a LUT

Suppose an 8-bit image can contain values from `0` to `255`.

Instead of recomputing the gamma formula for every pixel, we can precompute 256 results:

```python
import numpy as np
import cv2

def gamma_correct(img, gamma):
    table = np.array(
        [
            ((i / 255.0) ** gamma) * 255
            for i in range(256)
        ],
        dtype=np.uint8,
    )
    return cv2.LUT(img, table)
```

This reveals an important optimization principle:

> If the same deterministic point transform is applied repeatedly to a small finite set of possible input values, precompute the answers.

Pillow also supports 3D color LUTs for mappings that depend jointly on RGB values.

### Lens blur / depth-of-field simulation

A simple depth-of-field effect can be built from:

1. an original image,
2. a blurred copy,
3. a mask describing which regions should remain sharp,
4. compositing.

```text
sharp image -----\
                  > spatial mask -> output
blurred image ---/
```

A Gaussian blur can approximate defocus:

```python
from PIL import ImageFilter

blurred = image.filter(
    ImageFilter.GaussianBlur(radius=5)
)
```

Then:

```python
final = Image.composite(
    image,
    blurred,
    mask,
)
```

The mask creates **spatially varying blur**.

This is more important than memorizing the exact effect code: depth-of-field simulation is fundamentally a blur + mask + composite pipeline.

### Palette remapping

Palette-mode images store an index at each pixel rather than full RGB triples.

For example:

```text
pixel value 7
     ↓
palette[7]
     ↓
actual RGB color
```

If the palette changes while the pixel indices remain the same, the spatial structure remains but the colors can change dramatically.

That is why swapping palettes can produce surprising visual effects.

### Color temperature

The chapter demonstrates temperature changes by scaling RGB channels.

A warm appearance generally increases the relative contribution of red/yellow tones, while a cool appearance increases the relative contribution of blue.

A simple linear color transformation can be written as:

```text
[R']   [a 0 0] [R]
[G'] = [0 b 0] [G]
[B']   [0 0 c] [B]
```

This is an approximation of color-temperature appearance, not a complete physical model of illumination.

### Vignetting

A vignette darkens the image toward its edges.

A radial mask can depend on distance from the center:

```text
distance from center ↑
        ↓
mask intensity ↓
        ↓
edge brightness ↓
```

A Lomography-style effect can combine:

- vignette,
- increased saturation,
- increased contrast.

This demonstrates a major principle of photo effects:

> Many recognizable "filters" are pipelines made by combining several simple transformations.

### Procedural image generation

Pillow can also generate controlled synthetic images:

- Mandelbrot fractals,
- Gaussian noise,
- linear gradients,
- radial gradients.

These are not only artistic demos. They can support:

- procedural textures,
- synthetic data,
- controlled testing,
- masks,
- lighting simulations.

For example, a radial gradient is useful as a mask for spotlight or vignette effects.

{{exercise:M03.L01.EX01}}

---

## 4. OpenCV: fast geometric manipulation

OpenCV is especially useful when transformations must be efficient, repeated, or applied to video.

### BGR versus RGB

OpenCV normally loads color images in **BGR** order.

Matplotlib typically expects **RGB**.

Therefore:

```python
import cv2

image_bgr = cv2.imread("images/fruits.png")

image_rgb = cv2.cvtColor(
    image_bgr,
    cv2.COLOR_BGR2RGB,
)
```

If you forget this conversion, the image may still look plausible but the colors will be wrong.

### Rotation

OpenCV can construct a 2D rotation matrix:

```python
rows, cols = image_rgb.shape[:2]

M = cv2.getRotationMatrix2D(
    (cols / 2, rows / 2),
    45,
    1.0,
)

rotated = cv2.warpAffine(
    image_rgb,
    M,
    (cols, rows),
)
```

`getRotationMatrix2D()` creates the affine transform and `warpAffine()` resamples the image.

### Why rotated images get cropped

If a rectangle rotates while the canvas dimensions remain unchanged, its corners may fall outside the original bounds.

Therefore, avoiding crop requires:

1. compute the bounding dimensions of the rotated image,
2. enlarge the output canvas,
3. adjust translation in the transform matrix,
4. warp into the new canvas.

[[IMAGE_NEEDED: Rotation canvas and cropping | Show a rectangular image inside its original canvas, the same rectangle rotated so corners leave the canvas, and an enlarged output canvas containing the full rotation | Learner should understand that rotation clipping is a canvas-size problem, not a rotation failure]]

### Interpolation and border handling

`cv2.warpAffine()` and related functions need policies for:

- sampling non-integer coordinates,
- filling areas outside the original image.

Interpolation options include nearest-neighbor, linear, and cubic methods.

Border options can include:

- constant fill,
- replication,
- reflection.

This means a transformation is not defined only by its matrix. The sampling and boundary policies also affect the output.

### Flipping

`cv2.flip()` reverses coordinates:

```python
vertical = cv2.flip(image, 0)
horizontal = cv2.flip(image, 1)
both = cv2.flip(image, -1)
```

Flipping both axes is equivalent to a 180-degree rotation in spatial arrangement.

### Pillow versus OpenCV

A useful practical rule:

**Pillow**

- convenient API,
- photo/file manipulation,
- drawing,
- format conversion,
- rapid scripts.

**OpenCV**

- optimized image processing,
- real-time video,
- geometric warping,
- computer vision pipelines,
- large/high-frequency workloads.

This is not an absolute rule. Both libraries overlap heavily.

---

## 5. Convolution and homography with OpenCV

### A crosshatch kernel

Convolution applies a small kernel over neighborhoods in an image.

The chapter builds a cross-like diagonal kernel and applies it with:

```python
result = cv2.filter2D(
    image,
    -1,
    kernel,
)
```

The kernel emphasizes diagonal structures, producing a stylized crosshatch appearance.

The transferable idea is:

> A convolution kernel determines which local spatial patterns are amplified, suppressed, blurred, sharpened, or detected.

The artistic example is therefore also an introduction to the same local filtering principle used throughout image processing.

### Homography

A **homography** maps points between two planes using a 3×3 projective transformation matrix.

Conceptually:

```text
source plane
    ↓ H
destination plane
```

It is useful for:

- perspective correction,
- planar document rectification,
- aligning planar surfaces,
- panorama-related transformations.

### Corresponding points

A four-point OpenCV workflow can begin with:

```python
src = np.array(
    [
        [267, 364],
        [312, 683],
        [555, 598],
        [561, 284],
    ],
    dtype=np.float32,
)

dst = np.array(
    [
        [0, 0],
        [0, height - 1],
        [width - 1, height - 1],
        [width - 1, 0],
    ],
    dtype=np.float32,
)
```

Then:

```python
M = cv2.getPerspectiveTransform(src, dst)

rectified = cv2.warpPerspective(
    image,
    M,
    (width, height),
)
```

The most important requirement is **correspondence order**.

If:

```text
src[0] = top-left
```

then:

```text
dst[0]
```

must describe where that same physical point should go.

Incorrect pair ordering can produce a severely warped result even when every coordinate is individually valid.

[[IMAGE_NEEDED: Four-point homography | Show a photographed book/document as a quadrilateral with four labeled source corners, the four ordered destination rectangle corners, and the perspective-corrected output | Learner should notice that each source point must correspond to the correct destination point]]

### OpenCV versus scikit-image

The source chapter compares multiple ways to implement projective warping:

- OpenCV perspective transformation,
- scikit-image `warp()` with an inverse map,
- `ProjectiveTransform` with custom coordinate processing.

The broader engineering lesson is:

| Approach | Typical strength |
|---|---|
| OpenCV high-level functions | speed and concise implementation |
| scikit-image `warp()` | flexible inverse mapping and interpolation |
| custom mapping | maximum visibility/control over coordinate logic |

Do not overgeneralize one timing result from one machine. Performance depends on image size, hardware, library versions, and implementation.

### Coordinate-order caution

Mathematical points are commonly written:

```text
(x, y)
```

NumPy array access is:

```text
array[row, column]
array[y, x]
```

When moving between geometric APIs and array indexing, explicitly verify which convention the library expects.

---

## 6. Calibrated fisheye correction and remapping

In the previous lesson, you saw simplified geometric distortion.

This chapter introduces a more realistic computer-vision workflow.

### Camera calibration information

A calibrated correction uses parameters such as:

- camera intrinsic matrix `K`,
- distortion coefficients `D`.

The intrinsic matrix contains quantities related to:

- focal lengths,
- principal point.

Distortion coefficients model lens behavior.

OpenCV can generate remapping tables:

```python
map1, map2 = cv2.fisheye.initUndistortRectifyMap(
    K,
    D,
    np.eye(3),
    Knew,
    new_size,
    cv2.CV_32F,
)
```

Then apply them:

```python
corrected = cv2.remap(
    distorted,
    map1,
    map2,
    interpolation=cv2.INTER_LINEAR,
    borderMode=cv2.BORDER_CONSTANT,
)
```

This is a reusable architecture:

```text
calibration parameters
        ↓
coordinate maps
        ↓
remap + interpolation
        ↓
corrected image
```

### Field of view

Changing the new camera matrix can alter the trade-off between:

- wider field of view with more empty/black boundary regions,
- narrower field of view with more cropping.

Correction therefore involves a design choice about what output region should be preserved.

### Interpolation for remapping

Typical options include:

| Method | Trade-off |
|---|---|
| nearest | fast; useful for discrete labels/masks |
| linear | balanced general-purpose choice |
| cubic | slower but can provide smoother visual reconstruction |

For segmentation masks, nearest-neighbor is often preferable because interpolation should not invent class IDs.

For natural photographs, linear or cubic interpolation can be appropriate.

### High-level defisheye tools

The chapter also demonstrates a high-level `defisheye` package with projection models such as:

- linear,
- equal-area,
- stereographic.

These approaches can be useful for visual correction when explicit calibration parameters are unavailable, but they are not the same as a fully calibrated camera model.

[[IMAGE_NEEDED: Calibrated fisheye correction pipeline | Show a distorted checkerboard, a simplified camera intrinsic/distortion-parameter block, remapping arrows, and the corrected checkerboard with straighter lines | Learner should connect calibration parameters to coordinate remapping rather than thinking undistortion is just a cosmetic filter]]

---

## 7. SciPy ndimage: affine transforms, zoom, interpolation, and coordinate warping

`scipy.ndimage` sits close to NumPy and provides numerical image operations for N-dimensional arrays.

### Affine transformation

An affine transform can be applied numerically with:

```python
from scipy.ndimage import affine_transform

transformed = affine_transform(
    im,
    matrix,
    offset=offset,
    output_shape=im.shape,
)
```

The matrix controls the linear part of the transform, while `offset` controls displacement.

This reinforces an important lesson:

> Different libraries may expose different APIs, but they can represent the same underlying mathematics.

### Zooming

For an RGB image:

```python
import scipy.ndimage as ndimage

zoomed = ndimage.zoom(
    im,
    zoom=(2, 2, 1),
    mode="nearest",
    order=1,
)
```

Why `(2, 2, 1)`?

Because we want:

```text
height  ×2
width   ×2
channel ×1
```

The color-channel axis is not a spatial dimension and should not be duplicated as though it were width or height.

### Spline interpolation order

`ndimage.zoom()` can use spline interpolation of different orders.

A higher-order interpolator can produce smoother or sharper approximations in some cases, but "higher order" does not universally mean "better."

Trade-offs include:

- computational cost,
- ringing or overshoot,
- preservation of discrete data,
- visual smoothness.

Always choose interpolation based on the data and task.

### Wave distortion with coordinate maps

You can create a coordinate grid:

```python
x, y = np.meshgrid(
    np.arange(im.shape[1], dtype=np.float32),
    np.arange(im.shape[0], dtype=np.float32),
)
```

Then modify coordinates:

```python
y = y + 20 * np.sin(x / 15)
```

Finally sample the original image:

```python
distorted = ndimage.map_coordinates(
    im,
    [y.ravel(), x.ravel()],
)
```

This is one of the most important ideas in the chapter:

> Many geometric effects are simply "create output coordinates → modify the coordinates → sample the source."

Once you understand this, wave distortion, lens correction, warping, and many artistic effects become conceptually related.

{{exercise:M03.L01.EX02}}

---

## 8. Wand and ImageMagick: high-level effects and distortions

Wand is a Python interface to ImageMagick.

Its strength in this chapter is the large collection of built-in image effects.

Examples include:

- blue shift,
- charcoal,
- colorize,
- tint,
- vignette,
- sepia,
- implode,
- polaroid,
- swirl,
- wave,
- shading,
- white balance,
- spread.

A useful pattern is to clone the source image before applying effects:

```python
def apply_effect(img, effect_name, params):
    out = img.clone()
    func = getattr(out, effect_name)
    func(**params)
    return out
```

This preserves the original while allowing systematic comparisons.

### Sketch and solarization

Wand also provides effects such as:

- `sketch()`,
- `solarize()`.

These are high-level wrappers around transformations that can also be understood through lower-level concepts such as filtering and intensity mapping.

### FX expressions

The `fx()` mechanism allows pixel-oriented expressions.

For example, an expression can select pixels based on hue and return either the original color or a lightness-based value.

The important learning point is conditional pixel processing:

```text
if pixel satisfies condition:
    use transformation A
else:
    use transformation B
```

This is conceptually similar to Boolean masking in NumPy.

### Distortions

Wand can apply geometric distortion modes such as:

- barrel,
- polar,
- arc,
- Shepard's distortion.

These change coordinate geometry in different ways.

Shepard-style distortion uses control-point influence weighted by distance, enabling local spatial deformation.

### Undistortion by inverse model

If a distortion model and its parameters are known, applying an appropriate inverse model can approximately restore the image.

Conceptually:

```text
original
  ↓ distortion model
distorted
  ↓ inverse model
approximately reconstructed
```

Exact reconstruction is not always possible because:

- pixels may have been resampled,
- information may have moved outside the frame,
- interpolation may lose detail,
- model parameters may be imperfect.

[[IMAGE_NEEDED: Wand distortion comparison | Show one source image beside barrel, polar, arc, Shepard/w local warp, and inverse-barrel corrected examples | Learner should compare global radial distortion, coordinate-system remapping, arc bending, local control-point warping, and approximate inversion]]

---

## 9. Matplotlib: annotations and image contours

Matplotlib is primarily a visualization library, but visualization is a critical part of image processing.

### Annotation

You can place labels and arrows directly over an image:

```python
import matplotlib.pyplot as plt

plt.imshow(im)

plt.text(
    310,
    310,
    "Target",
    fontsize=20,
)

plt.arrow(
    300,
    225,
    25,
    25,
    width=2,
)
```

Annotations help with:

- explaining algorithm output,
- labeling detected regions,
- showing direction or movement,
- creating educational figures,
- debugging.

### Contour lines

A contour line connects image locations with the same scalar value.

If a grayscale image is treated as a function:

```text
I(x, y)
```

then a contour at level `c` contains locations satisfying:

```text
I(x, y) = c
```

Example:

```python
levels = np.linspace(0, 255, 15)

cs = plt.contour(
    image,
    levels=levels,
)

plt.clabel(cs)
```

Filled contours use bands between levels:

```python
plt.contourf(image)
```

[[IMAGE_NEEDED: Grayscale image and contour interpretation | Show a grayscale image as an intensity surface concept, the original image, contour lines at several intensity levels, and filled contours | Learner should see that contours connect equal-intensity locations rather than automatically representing object boundaries]]

### Contours are not all the same

The chapter compares contour-related operations in multiple libraries:

- Pillow contour filtering,
- OpenCV binary-region contour extraction,
- scikit-image iso-valued contour finding,
- Matplotlib contour plotting.

These functions do **not** necessarily mean the same thing.

For example:

- Matplotlib contours visualize equal-value levels.
- OpenCV `findContours()` commonly extracts boundaries from a binary image.
- Pillow's contour filter is an image effect.
- scikit-image can trace level sets at a specified intensity.

The word "contour" is shared, but the operation and interpretation differ.

---

## 10. Pilgram and Instagram-like filter pipelines

Pilgram provides ready-made photo filters inspired by Instagram-style effects.

The educational value is not memorizing filter names.

The useful question is:

> What lower-level operations are hidden inside a preset filter?

Typical filter components include:

- color transformation,
- brightness adjustment,
- contrast adjustment,
- saturation,
- hue rotation,
- gamma correction,
- blending,
- convolution,
- sepia/grayscale conversion.

A filter can be viewed abstractly as:

```text
output = F(input)
```

where `F` may itself be a pipeline of multiple transformations.

### Applying preset functions

A library can expose many ready-made functions that transform a Pillow image.

This is convenient for experimentation, but in an engineering system you should still understand:

- input mode,
- output mode,
- range,
- whether the filter mutates data,
- computational cost,
- whether it is appropriate for training-data augmentation.

### CSS-style transformations

Pilgram also exposes operations analogous to CSS filters, including:

- contrast,
- grayscale,
- hue rotation,
- saturation,
- sepia.

These show the connection between image processing and frontend visual styling: the same mathematical categories appear in different ecosystems.

### Filters and machine learning

Creative filters can sometimes act as data augmentation by changing visual appearance while keeping semantic content.

However, a transformation is only useful augmentation if it reflects variation the model should handle.

For example:

- mild brightness changes may improve robustness to lighting,
- extreme hue rotation may destroy label-relevant color information,
- heavy vignette may hide peripheral features,
- perspective warp may or may not be realistic for the task.

Do not apply artistic transformations blindly just because they are available.

---

## Choosing the right tool

The chapter demonstrates similar ideas across several libraries.

A useful decision table is:

| Need | Good starting point |
|---|---|
| Simple photo/file edits | Pillow |
| Fast geometric transforms or live video | OpenCV |
| Numerical N-D interpolation and coordinate mapping | SciPy `ndimage` |
| Large catalog of high-level artistic effects | Wand/ImageMagick |
| Plotting, annotations, intensity contours | Matplotlib |
| Ready-made social-photo filters | Pilgram |

This is not a strict ranking. Choose based on:

- task requirements,
- performance,
- deployment constraints,
- dependency size,
- API clarity,
- compatibility with the rest of your pipeline.

---

## Important misconceptions

### Misconception 1

> Lower JPEG quality means lower image resolution.

### Why this is wrong

JPEG quality can reduce visual fidelity and file size while leaving width and height unchanged. Resolution and compression quality are separate properties.

### Misconception 2

> A LUT is only a cinematic visual preset.

### Why this is incomplete

A LUT is a general precomputed mapping. It can implement point transforms such as gamma correction efficiently as well as complex color grading.

### Misconception 3

> Homography can model any arbitrary 3D change.

### Why this is wrong

A homography is a projective mapping between planes. It is especially suitable when the relevant scene geometry is planar or when the imaging relationship can be represented by a planar projective transform.

### Misconception 4

> Any fisheye correction is equivalent to camera calibration.

### Why this is wrong

Aesthetic or approximate correction can be done with generic models, but calibrated correction uses camera intrinsics and lens-distortion parameters estimated from the camera system.

### Misconception 5

> A higher interpolation order is always better.

### Why this is wrong

Interpolation is a trade-off. High-order interpolation can cost more and may be inappropriate for labels, masks, or certain signals.

### Misconception 6

> Every function called "contour" finds object boundaries.

### Why this is wrong

A contour may mean an equal-intensity level, a binary boundary, or an artistic edge-like effect depending on the library and operation.

---

## Key terminology

| Term | Meaning |
|---|---|
| Lossy compression | Compression that discards some information to reduce storage |
| JPEG quality | Encoder setting controlling fidelity/compression trade-off |
| DCT | Transform that represents signal blocks in terms of frequency components |
| LUT | Precomputed mapping from input values/colors to output values/colors |
| Color grading | Deliberate remapping of colors to create or correct visual appearance |
| Gamma correction | Nonlinear intensity transformation |
| Lens blur | Blur designed to approximate out-of-focus camera behavior |
| Vignette | Gradual darkening toward image boundaries |
| Color temperature | Warm/cool color appearance related to illumination color |
| Affine warp | Spatial transform involving linear mapping plus translation |
| Homography | 3×3 projective transform mapping points between planes |
| Correspondence | Matched source and destination points describing the same locations |
| Remapping | Sampling an image according to coordinate maps |
| Camera intrinsic matrix | Matrix describing focal lengths and principal point in a camera model |
| Distortion coefficients | Parameters describing lens distortion behavior |
| Spline interpolation | Smooth interpolation based on piecewise polynomial functions |
| `map_coordinates` | SciPy mechanism for sampling an array at specified coordinates |
| Procedural image | Image generated algorithmically rather than captured |
| Contour line | Curve connecting locations with equal scalar value |
| Preset filter | Named pipeline combining multiple lower-level transformations |

---

## Self-check

Before continuing, make sure you can answer:

1. Why can two JPEG files have the same dimensions but very different file sizes?
2. What visual artifacts can aggressive JPEG compression introduce?
3. What is a LUT, and why can it make a point transformation efficient?
4. How can lens blur be modeled using an original image, blurred image, and mask?
5. Why can a palette swap change color without changing image structure?
6. What mathematical idea creates a vignette?
7. Why must BGR/RGB channel order be checked when using OpenCV and Matplotlib together?
8. Why can rotation crop an image even when the rotation matrix is correct?
9. What does a homography map?
10. Why must source and destination point orders correspond?
11. How does calibrated fisheye correction differ from a generic distortion effect?
12. Why is `(2, 2, 1)` a sensible zoom tuple for an RGB image?
13. What does changing spline interpolation order affect?
14. How is `map_coordinates()` related to geometric warping?
15. Why do "contour" functions from different libraries need to be interpreted carefully?
16. What lower-level operations might be hidden inside a social-media-style filter?

---

## Retain this idea

**Advanced image manipulation is not a collection of magic filters. Most effects reduce to value mappings, coordinate mappings, interpolation, neighborhood operations, masking, and compositing; the libraries mainly provide different interfaces and performance trade-offs for those same core ideas.**
        """,

        "estimated_minutes": 300,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "advanced-manipulation-map",
                "title": "The Bigger Picture: Effects Are Combinations of a Few Ideas",
                "order": 1,
            },
            {
                "id": "jpeg-quality-compression",
                "title": "JPEG Quality, Compression, and Visible Artifacts",
                "order": 2,
            },
            {
                "id": "pillow-color-effects",
                "title": "Pillow: Deformation, Color Grading, LUTs, and Photographic Effects",
                "order": 3,
            },
            {
                "id": "opencv-geometric",
                "title": "OpenCV: Fast Geometric Manipulation",
                "order": 4,
            },
            {
                "id": "convolution-homography",
                "title": "Convolution and Homography with OpenCV",
                "order": 5,
            },
            {
                "id": "fisheye-calibrated",
                "title": "Calibrated Fisheye Correction and Remapping",
                "order": 6,
            },
            {
                "id": "scipy-ndimage",
                "title": "SciPy ndimage: Affine Transforms, Zoom, Interpolation, and Warping",
                "order": 7,
            },
            {
                "id": "wand-effects",
                "title": "Wand and ImageMagick: High-Level Effects and Distortions",
                "order": 8,
            },
            {
                "id": "matplotlib-contours",
                "title": "Matplotlib: Annotations and Image Contours",
                "order": 9,
            },
            {
                "id": "pilgram-filters",
                "title": "Pilgram and Instagram-Like Filter Pipelines",
                "order": 10,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M03.L01.EX01",

            "title": "Build and Measure a Photo Enhancement Pipeline",

            "lesson_code": "M03.L01",

            "section_id": "pillow-color-effects",

            "placement": "after_section",

            "description": (
                "Combine several Pillow-based operations while separating compression, "
                "color transformation, masking, and image appearance."
            ),

            "instructions": (
                "1. Load one RGB photograph and record its dimensions, mode, and original "
                "file size.\n"
                "2. Save JPEG copies at three substantially different quality settings "
                "without changing the image dimensions.\n"
                "3. Record the resulting file sizes and inspect the same small crop from "
                "all versions for compression artifacts.\n"
                "4. On the original image, apply one gamma/LUT correction and one color "
                "temperature or color-grading transformation.\n"
                "5. Create a radial or manually supplied grayscale mask and use it for "
                "either a vignette or spatially varying blur.\n"
                "6. Display the original, corrected, and final-effect image side by side.\n"
                "7. Explain which operations changed pixel values, which used a mask, and "
                "which affected only encoded storage.\n"
                "8. State one reason an extreme version of the effect could be harmful "
                "if used as machine-learning augmentation."
            ),

            "expected_output": (
                "A runnable notebook or script with a small JPEG quality/file-size table, "
                "a zoomed artifact comparison, one LUT/gamma or color correction, one "
                "masked effect, and a short interpretation of the results."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "jpeg-compression",
                "lut",
                "gamma-correction",
                "color-grading",
                "masking",
                "vignette",
                "lens-blur",
                "visual-evaluation",
            ],
        },

        {
            "id": "M03.L01.EX02",

            "title": "Rectify and Warp an Image with Two Libraries",

            "lesson_code": "M03.L01",

            "section_id": "scipy-ndimage",

            "placement": "after_section",

            "description": (
                "Practice projective and coordinate-based transformations while reasoning "
                "about correspondence order, interpolation, canvas bounds, and library APIs."
            ),

            "instructions": (
                "1. Choose a photograph containing a roughly rectangular planar object "
                "such as a document, poster, screen, or book cover.\n"
                "2. Define four source corner points in a consistent order and four "
                "destination rectangle corners in the matching order.\n"
                "3. Use OpenCV to compute a perspective transform and rectify the region.\n"
                "4. Create a second geometric effect with SciPy `ndimage`, such as zoom, "
                "affine transformation, or sinusoidal coordinate warping.\n"
                "5. Compare at least two interpolation choices on one transformation.\n"
                "6. Record any cropping, empty borders, or artifacts and explain why they "
                "appear.\n"
                "7. Deliberately swap two destination correspondences once, observe the "
                "incorrect homography, then restore the correct order.\n"
                "8. Explain in your own words how both tasks reduce to coordinate mapping "
                "plus resampling."
            ),

            "expected_output": (
                "A notebook or script displaying the original image, correctly rectified "
                "homography, one intentionally wrong correspondence result, one SciPy "
                "warped result, and a concise explanation of coordinate mapping and "
                "interpolation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "homography",
                "point-correspondence",
                "opencv-warping",
                "scipy-ndimage",
                "coordinate-mapping",
                "interpolation",
                "debugging",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M03.L01.QZ01",

        "title": "More Image Manipulation — Knowledge Check",

        "lesson_code": "M03.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M03.L01.Q01",
                "section_id": "jpeg-quality-compression",
                "question": (
                    "What can happen when a JPEG is saved with a much lower quality setting "
                    "while keeping the same width and height?"
                ),
                "options": [
                    "Its resolution must increase",
                    "Its file size can decrease while compression artifacts become more visible",
                    "It automatically becomes lossless",
                    "Its RGB channels are replaced by an alpha channel",
                ],
                "correct": 1,
                "explanation": (
                    "JPEG quality controls a lossy compression trade-off; dimensions can "
                    "remain unchanged while file size and visual fidelity change."
                ),
            },

            {
                "id": "M03.L01.Q02",
                "section_id": "pillow-color-effects",
                "question": (
                    "Why can a lookup table make gamma correction efficient for an 8-bit image?"
                ),
                "options": [
                    "It moves every pixel to a new coordinate",
                    "It precomputes the output for each possible input intensity",
                    "It increases the image dimensions",
                    "It converts JPEG into PNG automatically",
                ],
                "correct": 1,
                "explanation": (
                    "An 8-bit channel has a finite set of possible input values, so the "
                    "transformation can be precomputed and looked up repeatedly."
                ),
            },

            {
                "id": "M03.L01.Q03",
                "section_id": "pillow-color-effects",
                "question": (
                    "Which pipeline best describes a simple spatially varying lens-blur effect?"
                ),
                "options": [
                    "JPEG encode → rename file → decode",
                    "Original image + blurred copy + spatial mask → composite",
                    "Swap width and height only",
                    "Convert every pixel to the same value",
                ],
                "correct": 1,
                "explanation": (
                    "A blur mask selects how much of the sharp versus blurred image should "
                    "appear at each position."
                ),
            },

            {
                "id": "M03.L01.Q04",
                "section_id": "opencv-geometric",
                "question": (
                    "Why can a correctly rotated image still be cropped?"
                ),
                "options": [
                    "Because rotation always deletes color channels",
                    "Because the rotated corners may extend beyond an unchanged output canvas",
                    "Because RGB cannot represent rotation",
                    "Because affine matrices cannot rotate images",
                ],
                "correct": 1,
                "explanation": (
                    "The transform may be mathematically correct while the chosen output "
                    "canvas is too small to contain the rotated bounding box."
                ),
            },

            {
                "id": "M03.L01.Q05",
                "section_id": "convolution-homography",
                "question": (
                    "What is the most important requirement when defining source and "
                    "destination corner points for a four-point homography?"
                ),
                "options": [
                    "All x coordinates must be equal",
                    "The point pairs must describe corresponding physical locations in the same order",
                    "The destination must always be square",
                    "Every coordinate must be an integer",
                ],
                "correct": 1,
                "explanation": (
                    "Homography estimation depends on correct source-to-destination point "
                    "correspondences. Misordered pairs describe the wrong mapping."
                ),
            },

            {
                "id": "M03.L01.Q06",
                "section_id": "fisheye-calibrated",
                "question": (
                    "What distinguishes calibrated fisheye correction from a generic "
                    "artistic distortion reversal?"
                ),
                "options": [
                    "It uses camera intrinsics and distortion parameters derived for the imaging system",
                    "It never performs interpolation",
                    "It can only process grayscale images",
                    "It does not map coordinates",
                ],
                "correct": 0,
                "explanation": (
                    "Calibrated correction uses a camera/lens model, including intrinsic "
                    "parameters and distortion coefficients, to construct remapping coordinates."
                ),
            },

            {
                "id": "M03.L01.Q07",
                "section_id": "scipy-ndimage",
                "question": (
                    "Why might an RGB zoom operation use a factor such as `(2, 2, 1)`?"
                ),
                "options": [
                    "To double height and width without treating the channel axis as spatial",
                    "To keep height fixed and double the number of channels",
                    "To convert RGB into grayscale",
                    "To rotate the image twice",
                ],
                "correct": 0,
                "explanation": (
                    "The first two axes are spatial dimensions; the last axis stores color "
                    "channels and normally should not be spatially zoomed."
                ),
            },

            {
                "id": "M03.L01.Q08",
                "section_id": "wand-effects",
                "question": (
                    "What common concept connects a Wand FX conditional expression with a "
                    "NumPy Boolean mask?"
                ),
                "options": [
                    "Both choose different processing based on a per-pixel condition",
                    "Both always resize the image",
                    "Both require camera calibration",
                    "Both only work on JPEG metadata",
                ],
                "correct": 0,
                "explanation": (
                    "Both can apply different behavior to pixels depending on whether a "
                    "condition is satisfied."
                ),
            },

            {
                "id": "M03.L01.Q09",
                "section_id": "matplotlib-contours",
                "question": (
                    "In a Matplotlib contour plot of a grayscale image, what does one "
                    "contour line represent?"
                ),
                "options": [
                    "All pixels that belong to the same RGB channel",
                    "Locations having the same selected intensity level",
                    "The physical edge of every object",
                    "All pixels changed by JPEG compression",
                ],
                "correct": 1,
                "explanation": (
                    "A scalar contour is a level set: it connects positions where the "
                    "underlying intensity has the same specified value."
                ),
            },

            {
                "id": "M03.L01.Q10",
                "section_id": "pilgram-filters",
                "question": (
                    "What is the best mental model for an Instagram-like preset filter?"
                ),
                "options": [
                    "A magical visual style unrelated to normal image processing",
                    "A pipeline composed of lower-level operations such as color mapping, contrast, gamma, and blending",
                    "A geometric homography only",
                    "A file-compression algorithm only",
                ],
                "correct": 1,
                "explanation": (
                    "Named photo filters generally combine familiar lower-level color, "
                    "intensity, filtering, and blending operations."
                ),
            },

            {
                "id": "M03.L01.Q11",
                "section_id": "advanced-manipulation-map",
                "question": (
                    "You need real-time perspective warping on video frames. Which library "
                    "from this lesson is the most natural starting point?"
                ),
                "options": [
                    "OpenCV",
                    "Pilgram only",
                    "Matplotlib only",
                    "A JPEG encoder only",
                ],
                "correct": 0,
                "explanation": (
                    "OpenCV is designed for efficient image processing and computer-vision "
                    "workflows, including geometric warping on image/video data."
                ),
            },

            {
                "id": "M03.L01.Q12",
                "section_id": "pilgram-filters",
                "type": "open",
                "question": (
                    "Design a small photo-processing pipeline that compresses an image for "
                    "delivery, applies a controlled color look, rectifies a photographed "
                    "planar object, and adds an annotation. Name the operation and library "
                    "you would use at each stage, and explain one important numerical or "
                    "geometric caution for each stage."
                ),
            },
        ],

        "passing_score": 70,
    },
}
