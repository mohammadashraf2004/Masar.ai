"""M01.L01 — Getting Started with Digital Image Processing.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 1. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L01"

MODULE_ORDER = 1

MODULE_TITLE = "Digital Image Processing Foundations"

MODULE_DESCRIPTION = (
    "Build a practical mental model of digital images as numerical arrays, learn the "
    "standard image-processing workflow, use major Python imaging libraries, reason "
    "about formats and data types, work with color spaces, and perform foundational "
    "image manipulations safely."
)

SOURCE_CHAPTER = 1

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Getting Started with Digital Image Processing",

    "slug": "digital-image-processing-m01-l01",

    "description": (
        "A practical introduction to digital images, pixels, arrays, image-processing "
        "pipelines, Python image I/O, formats, data types, color spaces, and basic "
        "manipulation techniques."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.0,

    "skill_tags": [
        "digital-image-processing",
        "computer-vision",
        "numpy",
        "pillow",
        "matplotlib",
        "scikit-image",
        "opencv",
        "imageio",
        "color-spaces",
        "image-io",
        "image-manipulation",
        "module-01",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Getting Started with Digital Image Processing",

        "content": r"""
# Getting Started with Digital Image Processing

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M01.L01  
> **Module:** Digital Image Processing Foundations  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 1. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain what digital image processing is and how it differs from computer vision.
- Represent grayscale and color images as numerical arrays.
- Describe sampling, quantization, pixels, channels, shapes, and common image data types.
- Explain the main stages of an image-processing pipeline.
- Read, display, convert, and save images with common Python libraries.
- Compare important file formats and image modes.
- Avoid common mistakes involving value ranges, data types, overflow, and channel order.
- Explain why different color spaces exist and choose a useful representation for a task.
- Perform foundational manipulations such as cropping, masking, brightness/contrast adjustment, flipping, blending, and color filtering.
- Build a small end-to-end image-processing workflow and interpret its output.

---

## 1. A digital image is data

The most important idea in this lesson is simple:

> **A digital image is not only a picture. It is a numerical data structure.**

When you look at a photograph, you see objects, colors, textures, and shapes. A computer does not begin with those meanings. It begins with numbers arranged on a discrete grid.

A single image location is called a **pixel** (picture element). Each pixel stores one or more numerical values.

### Grayscale image

A grayscale image stores one intensity value at each location.

Conceptually:

```text
[
  [  0,  40, 120, 255],
  [ 10,  80, 160, 240],
  [ 20, 100, 180, 220]
]
```

If the image has height `H` and width `W`, a grayscale image is commonly represented as:

```text
(H, W)
```

For example:

```text
(340, 453)
```

means 340 rows and 453 columns.

### Color image

An RGB image stores three values per pixel:

```text
(R, G, B)
```

So its array normally has shape:

```text
(H, W, 3)
```

The three channels represent red, green, and blue components.

An RGBA image adds an alpha channel for transparency:

```text
(H, W, 4)
```

[[IMAGE_NEEDED: Image as matrix and tensor | Show one grayscale image beside a 2D intensity matrix and one RGB image beside a 3D H x W x 3 tensor with R, G, and B channels | Learner should connect visible pixels to numerical array elements and understand why grayscale is 2D while RGB is 3D]]

### Sampling and quantization

Turning a continuous visual scene into a digital image requires two major ideas:

1. **Spatial sampling** divides continuous space into a grid of pixel locations.
2. **Amplitude quantization** maps continuous intensity or color measurements into a finite set of numerical values.

This gives us a finite numerical array that software can process.

For a common 8-bit image, one channel often uses values from:

```text
0 to 255
```

For normalized floating-point processing, values are often represented approximately as:

```text
0.0 to 1.0
```

### File versus in-memory image

A PNG or JPEG file is not the same thing as the array you manipulate in Python.

A file may contain:

- compressed pixel data,
- metadata,
- color information,
- format-specific structure.

When an imaging library loads the file, it **decodes** the stored representation into an in-memory object such as:

- a `PIL.Image.Image`, or
- a NumPy `ndarray`.

That array is what most image-processing algorithms actually operate on.

### Why this mental model matters

Once you understand an image as an array, many operations become ordinary numerical operations:

- cropping becomes array slicing,
- thresholding becomes comparison,
- masking becomes Boolean indexing,
- brightness changes become arithmetic,
- color conversion becomes transformation between channel representations,
- filtering becomes local computation over neighborhoods.

This is the bridge between "pictures" and "algorithms."

---

## 2. Image processing, computer vision, and the processing pipeline

### What is digital image processing?

Digital image processing is the computational manipulation, transformation, analysis, and interpretation of images represented in digital form.

Typical goals include:

- improving visual quality,
- removing noise,
- correcting defects,
- changing color or contrast,
- segmenting regions,
- extracting features,
- preparing visual data for later analysis.

### Image processing versus computer vision

These areas overlap, but their goals are useful to distinguish.

**Image processing** often focuses on transforming or analyzing image data.

Examples:

- denoising,
- sharpening,
- contrast enhancement,
- color conversion,
- segmentation,
- edge detection.

**Computer vision** focuses more on enabling a machine to interpret visual content.

Examples:

- image classification,
- object recognition,
- object detection,
- tracking,
- scene understanding.

A useful mental model is:

```text
Image processing: "How should I transform or analyze the pixels?"

Computer vision:  "What does the visual data tell the machine about the world?"
```

The chapter also connects these ideas to related fields:

- **Machine vision:** industrial inspection, measurement, defect detection, automation.
- **Computational photography:** HDR, image stitching, deblurring, computational enhancement.
- **Remote sensing:** analyzing images acquired by satellites, aircraft, and other sensors.

### Common applications

Digital image processing appears in:

- medical and biological imaging,
- satellite and space imaging,
- photography,
- OCR,
- fingerprint and face recognition,
- robotics,
- barcode scanning,
- industrial quality control,
- social-media image processing,
- video and broadcasting systems.

### The standard image-processing pipeline

A practical image-processing system often follows a sequence like this:

```text
Acquire
   ↓
Load / Represent
   ↓
Preprocess / Enhance / Restore
   ↓
Segment or isolate relevant regions
   ↓
Extract or learn features
   ↓
Recognize / Detect / Classify / Measure
   ↓
Visualize / Save / Transmit results
```

Not every project uses every stage, and the order can vary, but this pipeline is a powerful way to organize your thinking.

[[IMAGE_NEEDED: Digital image-processing pipeline | A left-to-right flow diagram showing acquisition, image I/O/representation, preprocessing, segmentation, feature extraction, recognition/detection/classification, and output visualization/storage | Learner should notice that low-level pixel operations prepare data for higher-level interpretation]]

### Handcrafted versus learned features

Before deep learning became dominant, many vision systems relied heavily on engineered features such as edges, corners, or descriptors such as HOG.

Modern systems may instead learn feature representations automatically using neural networks.

Both approaches still depend on the same foundation:

> Images must first be represented, loaded, transformed, and interpreted correctly.

---

## 3. The Python image-processing toolkit

The chapter introduces several libraries because no single library is ideal for every task.

### Core libraries and what they are good at

| Library | Main role in this chapter |
|---|---|
| Pillow (PIL) | Simple image loading, saving, resizing, cropping, mode conversion |
| NumPy | Array representation, arithmetic, slicing, masking, vectorized operations |
| Matplotlib | Displaying images, subplots, colormaps, visual comparison |
| scikit-image | High-level image-processing algorithms and color transformations |
| OpenCV-Python | Fast computer-vision and image-processing operations |
| Imageio | Simple image I/O, GIFs, frame sequences |
| SciPy | Numerical and scientific routines used by image-processing workflows |
| SimpleITK | Medical-image processing, registration, segmentation, volumetric work |
| scikit-learn | Classical machine learning on extracted image features |
| TensorFlow / Keras / PyTorch | Deep-learning-based image models |

The important lesson is not to memorize a list of libraries. It is to understand the layers:

```text
NumPy       -> numerical image representation
I/O library -> load/save
Processing  -> transform/analyze
Matplotlib  -> inspect and communicate results
ML/DL       -> learn patterns from visual data
```

### Reproducibility matters

Image-processing code depends on library versions, file paths, image assets, and execution environments.

The source chapter recommends practices such as:

- using a controlled Python environment,
- recording dependencies,
- installing compatible versions from a requirements file,
- isolating projects with tools such as `venv` or `conda`,
- using `pip freeze` when you need to record a working environment.

The underlying image-processing ideas may remain stable while Python APIs evolve.

That means debugging version differences is part of practical engineering, not a sign that the concept itself is invalid.

### Problem-oriented learning

A single visual problem can often be solved in several ways.

When comparing solutions, consider:

- correctness,
- clarity,
- execution time,
- memory usage,
- amount of code,
- robustness.

A good image-processing learner asks not only:

> "Does this code run?"

but also:

> "Why does this method work, what assumptions does it make, and what are its limitations?"

---

## 4. Reading, saving, and displaying images

Before you can process an image, you must load it into memory and understand what the library returned.

### 4.1 Pillow: simple object-oriented image I/O

```python
from PIL import Image

im = Image.open("images/parrot.png")

print(im.size)
print(im.mode)
print(im.format)

im_gray = im.convert("L")
im_gray.save("images/parrot_gray.png")
```

Important Pillow properties include:

- `size`
- `width`
- `height`
- `mode`
- `format`

Pillow stores image size as:

```text
(width, height)
```

After conversion to NumPy, the array shape follows:

```text
(height, width[, channels])
```

Example:

```python
import numpy as np

arr = np.array(im_gray)

print(im_gray.size)
print(arr.shape)
```

This difference is easy to forget.

### 4.2 Images from file-like objects

Pillow can also open binary file-like objects:

```python
from PIL import Image

with open("images/parrot.png", "rb") as f:
    im = Image.open(f)
    im.load()
```

The chapter also demonstrates loading downloaded binary image data through an in-memory `BytesIO` object.

The important idea is that an image does not have to come directly from a normal disk pathname. It can come from any compatible binary stream.

### 4.3 Matplotlib: arrays plus visualization

Matplotlib can read images directly into NumPy arrays:

```python
import matplotlib.image as mpimg

im = mpimg.imread("images/hill.png")

print(im.shape)
print(im.dtype)
print(im.min(), im.max())
```

A loaded image may use normalized floating-point values, depending on the format and loader.

To display:

```python
import matplotlib.pyplot as plt

plt.imshow(im)
plt.axis("off")
plt.show()
```

### Colormaps

A **colormap** maps scalar values to display colors.

This is especially useful for grayscale or single-channel data:

```python
plt.imshow(gray_image, cmap="gray")
plt.colorbar(label="Intensity")
plt.show()
```

Other colormaps can help reveal differences in scalar intensity distributions, but remember:

> A colormap changes how scalar data is visualized. It does not magically create new image information.

### Subplots

Subplots let you compare several representations in one figure:

```python
fig, axes = plt.subplots(1, 2, figsize=(8, 4))

axes[0].imshow(original)
axes[0].set_title("Original")
axes[0].axis("off")

axes[1].imshow(processed, cmap="gray")
axes[1].set_title("Processed")
axes[1].axis("off")

plt.tight_layout()
plt.show()
```

### Interpolation during display

When an image is resized for display, pixels may not map one-to-one to screen pixels.

Display interpolation methods estimate intermediate values. Examples mentioned in the chapter include:

- nearest,
- bilinear,
- bicubic,
- Gaussian,
- Lanczos.

For now, remember that interpolation can change how a displayed image *looks* even when the source array has not changed.

### 4.4 scikit-image: image processing around NumPy arrays

```python
from skimage.io import imread

im = imread("images/parrot.png")

print(im.shape)
print(im.dtype)
```

scikit-image integrates closely with NumPy and provides high-level image-processing operations.

It can also read a grayscale image directly:

```python
gray = imread("images/parrot.png", as_gray=True)
```

### Sample datasets

scikit-image includes sample images useful for experiments:

```python
from skimage import data

astronaut = data.astronaut()
camera = data.camera()
moon = data.moon()
```

These built-in images are useful when you want to test an operation without first finding external image files.

### Collections of images

The chapter also introduces loading multiple images that match a filename pattern.

This is useful when processing:

- folders of samples,
- frame sets,
- repeated experiments,
- small image datasets.

### 4.5 OpenCV: fast array-based computer vision

OpenCV reads images into NumPy arrays:

```python
import cv2

image = cv2.imread("images/model.png")

if image is None:
    raise FileNotFoundError("Image could not be loaded")
```

A crucial OpenCV convention is:

> OpenCV commonly loads a standard color image in **BGR** channel order.

Matplotlib normally expects RGB for conventional display.

So when displaying an OpenCV image with Matplotlib:

```python
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image_rgb)
plt.axis("off")
plt.show()
```

[[IMAGE_NEEDED: BGR versus RGB channel order | Show the same color image displayed once with OpenCV BGR values interpreted directly as RGB and once after BGR-to-RGB conversion | Learner should notice the color distortion caused by channel-order mismatch]]

OpenCV can read grayscale directly:

```python
gray = cv2.imread("images/model.png", cv2.IMREAD_GRAYSCALE)
```

To save:

```python
cv2.imwrite("images/output.png", image)
```

The file extension helps determine the output format.

### `cv2.imshow()` versus notebooks

The chapter notes that `cv2.imshow()` opens a GUI window and is better suited to normal Python scripts than notebook environments.

Inside notebooks, Matplotlib is often more convenient for inline display.

### 4.6 Imageio and animated images

Imageio offers a simple interface for image files and sequences.

Animated GIFs consist of multiple frames.

Conceptually:

```text
GIF
 ├─ frame 1
 ├─ frame 2
 ├─ frame 3
 └─ ...
```

A frame can be treated as an image array, processed, and written back into an animation.

This same idea generalizes to video processing:

> A video is essentially an ordered sequence of image frames plus timing and encoding information.

---

## 5. File formats, image modes, and data types

These three ideas are related but different.

### File format

A **file format** describes how an image is encoded and stored.

Common examples from the chapter:

| Format | Main characteristics |
|---|---|
| BMP | Simple raster representation, often large |
| PNG | Lossless compression, supports transparency |
| JPEG | Lossy compression, well suited to photographs |
| GIF | Palette-based, limited colors, supports animation |
| PPM/PNM | Simple formats, often large and mainly useful for basic interchange/education |
| TIFF | Flexible high-quality format with strong metadata/professional use |

### Image mode

An image **mode** describes how pixel values are interpreted.

Common Pillow modes include:

| Mode | Meaning |
|---|---|
| `1` | Binary / black-and-white |
| `L` | 8-bit grayscale |
| `P` | Palette/indexed color |
| `RGB` | Red, green, blue |
| `RGBA` | RGB plus alpha/transparency |
| `CMYK` | Cyan, magenta, yellow, black |
| `F` | Floating-point pixels |

### Bit depth

Bit depth determines how many values a pixel or channel can represent.

For 8 bits:

```text
2^8 = 256 levels
```

Commonly:

```text
0 ... 255
```

Higher bit depths can represent more levels and therefore finer numerical precision.

### Palette images

In a palette image, pixel values can be indices rather than direct RGB triplets.

Example:

```text
pixel array:
[[0, 1],
 [1, 2]]

palette:
0 -> red
1 -> green
2 -> blue
```

The visual color depends on the palette lookup table.

### Alpha channel

An alpha channel represents transparency.

For RGBA:

```text
(R, G, B, A)
```

The alpha value controls how opaque or transparent a pixel appears.

### Data type controls arithmetic behavior

An image array may use data types such as:

| dtype | Typical role |
|---|---|
| `uint8` | Standard 8-bit image data |
| `float32` | Normalized or numerical processing |
| `float64` | Higher-precision numerical processing |
| `bool` | Binary masks |

Always inspect:

```python
print(image.dtype)
print(image.min(), image.max())
```

before performing arithmetic.

### Normalization

A common conversion is:

```python
image_float = image.astype("float32") / 255.0
```

which maps an 8-bit image approximately from:

```text
[0, 255]
```

to:

```text
[0.0, 1.0]
```

### Overflow is a real bug

Suppose a `uint8` pixel has value 250.

A naive arithmetic operation can exceed the allowed range.

Instead of relying on unsafe integer arithmetic, convert to a wider or floating type, perform the operation, and clip to the valid range.

Example:

```python
import numpy as np

bright = np.clip(
    image.astype(np.int16) + 100,
    0,
    255,
).astype(np.uint8)
```

A normalized floating-point workflow is often easier:

```python
image_float = image.astype(np.float32) / 255.0
bright_float = np.clip(image_float + 0.4, 0.0, 1.0)
```

### Boolean masks

A threshold can create a Boolean image:

```python
mask = gray > 0.5
```

Now each location is simply:

```text
True or False
```

This is extremely useful for segmentation, selective editing, and region-based processing.

### Safe library conversions

The chapter highlights scikit-image helpers such as:

```python
from skimage import img_as_float, img_as_ubyte

image_float = img_as_float(image)
image_uint8 = img_as_ubyte(image_float)
```

These utilities help make conversion intent explicit.

{{exercise:M01.L01.EX01}}

---

## 6. Color spaces: choosing the right representation

A color space is a coordinate system for representing color.

Different representations are useful because different tasks care about different aspects of color.

### RGB

RGB represents color using red, green, and blue components.

It is natural for:

- screens,
- cameras,
- general digital image representation.

Think of it as three intensity channels:

```text
R
G
B
```

### HSV

HSV separates color into:

- **Hue:** the type of color,
- **Saturation:** colorfulness,
- **Value:** brightness.

This is often useful for:

- color filtering,
- color segmentation,
- changing saturation,
- selecting a color while changing brightness separately.

{{image:rgb-vs-hsv-color-space}}

### CMYK

CMYK uses:

- cyan,
- magenta,
- yellow,
- black.

It is a subtractive color model associated strongly with printing.

RGB is based on emitted light; CMYK is based on inks subtracting parts of reflected light.

### Lab

Lab separates:

- `L*`: lightness,
- `a*`: opponent color dimension,
- `b*`: opponent color dimension.

The chapter uses Lab for operations where changing brightness separately from color is useful.

### YUV / YCbCr

These representations separate luminance/luma information from chrominance information.

They are important in:

- television,
- JPEG-related workflows,
- video compression,
- broadcasting.

### YIQ

YIQ is associated with NTSC television representation and also separates luminance-related information from chromatic components.

### Grayscale

Grayscale keeps only one intensity-like value per pixel.

It can reduce:

- memory,
- computational cost,
- complexity.

But it may also discard information that is important for a task.

For example, if an object is distinguishable primarily by color, grayscale conversion can make it much harder to separate.

### Color conversion

Libraries provide functions for converting between spaces.

Example with scikit-image:

```python
from skimage import color
from skimage.io import imread

image = imread("images/parrot.png")
hsv = color.rgb2hsv(image)
```

The three HSV channels can then be inspected independently.

### Grayscale conversion is not always "average the channels"

A simple grayscale approximation might average R, G, and B.

The chapter also presents a perceptually weighted luminance expression:

```python
gray = np.dot(image[..., :3], [0.299, 0.587, 0.114])
```

The larger green weight reflects the chapter's discussion of human brightness perception.

### Library conventions can differ

An important engineering lesson is that the same conceptual color space may use different numeric ranges in different libraries.

The chapter highlights HSV as an example:

- scikit-image uses normalized floating-point channel ranges,
- OpenCV uses its own integer scaling conventions.

Therefore:

> Never assume two libraries encode a color space identically. Inspect the documentation and actual value ranges.

### Color gamut

A **color gamut** is the range of colors a device or representation can reproduce.

The chapter introduces the CIE 1931 chromaticity diagram as a way to visualize chromaticity and compare color ranges.

[[IMAGE_NEEDED: CIE 1931 chromaticity diagram | A standard CIE 1931 xy chromaticity diagram with the visible-color boundary and an example device gamut triangle | Learner should notice that a device usually reproduces only a subset of the perceivable chromaticity region]]

---

## 7. Using color spaces for practical image manipulation

Color spaces become useful when they make an operation easier to express.

### 7.1 Changing saturation and value in HSV

A common workflow is:

```text
RGB image
   ↓
convert to HSV
   ↓
modify H, S, or V
   ↓
clip to valid range
   ↓
convert back to RGB
```

Example:

```python
from skimage import color
import numpy as np

def multiply_hsv_channel(image, channel, factor):
    hsv = color.rgb2hsv(image)
    hsv[..., channel] = np.minimum(
        factor * hsv[..., channel],
        1.0,
    )
    return color.hsv2rgb(hsv)
```

Changing channels produces different visual effects:

- hue changes the color family,
- saturation changes color vividness,
- value changes brightness.

[[IMAGE_NEEDED: HSV channel manipulation | Show one source image beside three outputs where hue, saturation, and value are changed independently | Learner should notice that each HSV component affects a different visual property]]

### 7.2 Tinting a grayscale image

A grayscale image can be converted to a 3-channel representation and assigned a hue.

This can create:

- artistic tinting,
- false-color displays,
- highlighted regions.

The chapter uses this idea to create a vintage-style look by controlling hue and saturation.

### 7.3 Color-pop effect

A color-pop effect preserves selected colors while desaturating others.

Conceptually:

```text
RGB
 ↓
HSV
 ↓
identify pixels by hue
 ↓
set saturation = 0 for unwanted colors
 ↓
HSV -> RGB
```

This is a good example of **choosing a representation that makes the task simple**.

Trying to perform the same operation directly in RGB can be less intuitive because color identity is distributed across three channels.

### 7.4 Manipulating lightness in Lab

The chapter also uses Lab when the goal is to alter lightness separately from chromatic information.

Conceptually:

```text
RGB
 ↓
Lab
 ↓
modify L* for brightness/lightness
or a*/b* for color shift
 ↓
Lab -> RGB
```

This demonstrates an important general principle:

> Choose the representation whose axes align with the property you want to manipulate.

### 7.5 Skin-color detection with HSV and YCbCr

The chapter demonstrates rule-based skin-color detection using more than one color space.

The workflow is:

1. convert the input into HSV,
2. threshold a predefined HSV range,
3. convert into YCbCr/YCrCb,
4. threshold another predefined range,
5. clean the masks with morphological operations,
6. combine the masks,
7. apply the resulting mask to the image.

Conceptually:

```text
Input image
   ├─> HSV threshold ----\
   |                      AND -> cleaned skin mask -> output
   └─> YCbCr threshold --/
```

This is educational because it shows that:

- color-space choice affects separability,
- thresholding creates masks,
- multiple weak cues can be combined,
- post-processing can reduce noise.

It also exposes an important limitation:

> Fixed color thresholds are rules, not universal understanding. Their usefulness depends on the data and imaging conditions.

---

## 8. Coordinates and foundational image manipulations

### Array coordinates

With NumPy-style image indexing, the usual pattern is:

```python
image[row, column]
```

which corresponds to:

```text
image[y, x]
```

The top-left array element is the natural starting point for image indexing.

This matters because image indexing and general plotting coordinates may use different conventions.

When combining:

- image arrays,
- `imshow`,
- scatter plots,
- annotations,
- boxes,

always make the coordinate convention explicit.

{{image:image-array-coordinates}}

### 8.1 Cropping with slicing

Cropping is simply selecting a rectangular region.

General pattern:

```python
crop = image[y1:y2, x1:x2]
```

This is one of the clearest examples of why image-as-array thinking is so useful.

### 8.2 Masking

A mask identifies which pixels should be affected.

Example:

```python
masked = image.copy()
masked[mask] = 0
```

The mask may come from:

- thresholding,
- geometric conditions,
- segmentation,
- color ranges,
- learned predictions.

### 8.3 Brightness

Brightness adjustment changes the overall intensity/lightness.

A safe numerical workflow usually involves:

1. converting to a suitable numeric representation,
2. changing values,
3. clipping to the valid range,
4. converting back if needed.

The chapter demonstrates brightness adjustment through the lightness channel in Lab.

### 8.4 Contrast

Contrast changes the separation between darker and brighter regions.

Increasing contrast makes differences stronger.

Decreasing contrast compresses those differences.

The chapter again uses the Lab lightness channel so the operation can focus on brightness structure.

### 8.5 Flipping

NumPy offers direct array operations:

```python
vertical = np.flipud(image)
horizontal = np.fliplr(image)
both = np.fliplr(vertical)
```

This is a geometric change implemented as array reordering.

### 8.6 Alpha blending and simple morphing

If two images have compatible dimensions, a simple linear blend can be computed as:

```text
output = (1 - alpha) * image1 + alpha * image2
```

When:

```text
alpha = 0
```

the output is entirely the first image.

When:

```text
alpha = 1
```

the output is entirely the second image.

Intermediate values blend them.

Example:

```python
alpha = 0.35
blend = (1 - alpha) * image1 + alpha * image2
```

The chapter uses a changing alpha value to demonstrate a simple cross-dissolve style of morphing.

This is not a full geometric face-morphing method; it is linear image blending.

### 8.7 Image division

Dividing one image by another can compensate for a known multiplicative pattern such as uneven illumination.

A safe implementation must avoid division by zero:

```python
epsilon = 1e-6
out = numerator.astype(float) / (
    denominator.astype(float) + epsilon
)
```

Then the result can be normalized for visualization.

This illustrates an important lesson:

> Image arithmetic can model real imaging effects, but numeric stability matters.

### 8.8 Sepia filter with matrix multiplication

A sepia effect can be implemented as a linear transformation of RGB values.

The chapter demonstrates a matrix like:

```python
sepia_matrix = np.array([
    [0.393, 0.769, 0.189],
    [0.349, 0.686, 0.168],
    [0.272, 0.534, 0.131],
])
```

Then each RGB pixel vector is transformed:

```python
sepia = np.dot(image, sepia_matrix.T)
sepia = np.clip(sepia, 0.0, 1.0)
```

This is a powerful pattern:

```text
pixel vector -> matrix transformation -> new pixel vector
```

The same mathematical idea appears in many color and geometric transformations.

[[IMAGE_NEEDED: Core image manipulations montage | Show one original image with outputs for crop, mask, brightness increase, contrast increase, horizontal flip, alpha blend, and sepia | Learner should connect each array/numerical operation to its visual effect]]

{{exercise:M01.L01.EX02}}

---

## 9. Useful engineering ideas from the chapter

The chapter includes several additional techniques that reinforce good image-processing practice.

### Converting between PIL and NumPy

Pillow object to NumPy:

```python
from PIL import Image
import numpy as np

pil_image = Image.open("images/flowers.jpg")
array_image = np.array(pil_image)
```

NumPy to Pillow:

```python
pil_again = Image.fromarray(array_image)
```

This lets you combine libraries instead of treating them as isolated ecosystems.

### Block views and local pooling

An image can be divided into non-overlapping blocks.

For each block, you might compute:

- mean,
- maximum,
- median.

This produces a lower-resolution representation.

Conceptually:

```text
8 x 8 pixel block
      ↓
one summary value
      ↓
downsampled image
```

This idea is related to local aggregation and pooling operations used throughout image processing and deep learning.

### Vectorization

When an operation can be expressed as NumPy array mathematics, vectorized code is often clearer and faster than manually looping over every pixel in Python.

For example:

```python
palette_array = np.array(palette, dtype=np.uint8)
modified = (palette_array + 19) % 256
```

rather than modifying every palette entry with a long Python-level loop.

### Decorators as reusable preprocessing

The chapter also demonstrates using a Python decorator to combine image loading with normalization.

The image-processing lesson is not "you must use decorators."

The useful engineering idea is:

> Repeated preprocessing steps can be wrapped into reusable abstractions.

### Quick demos with Gradio

The chapter finishes with a small Gradio interface around a sepia transformation.

The pattern is:

```text
Python function
   ↓
input component
   ↓
processing
   ↓
output component
   ↓
interactive browser demo
```

This is useful when you want to expose an image-processing function to someone who should not have to run notebook cells manually.

### A complete beginner workflow

At this point you can think of a basic image-processing project like this:

```text
1. Load
2. Inspect shape, dtype, range, and channel order
3. Convert to a representation suited to the task
4. Apply the operation
5. Clip/normalize safely
6. Visualize the result
7. Save if needed
8. Record assumptions and library/version details
```

This workflow is more important than memorizing a particular library function.

---

## Important misconceptions

### Misconception 1

> "An image is just a file such as JPEG or PNG."

### Why this is wrong

JPEG and PNG are storage formats. Once loaded, image-processing code usually works with an in-memory object or numerical array.

---

### Misconception 2

> "Every library uses the same shape, value range, and channel order."

### Why this is wrong

Library conventions can differ.

Examples from this chapter include:

- Pillow size uses `(width, height)`.
- NumPy image shape normally uses `(height, width[, channels])`.
- OpenCV commonly reads color images in BGR order.
- Matplotlib/scikit-image workflows may use different numeric representations.
- HSV scaling differs between libraries.

Always inspect the data you actually have.

---

### Misconception 3

> "If code works on `uint8`, arithmetic is automatically safe."

### Why this is wrong

The data type has a limited numerical range. Arithmetic can overflow or wrap if you do not convert, clip, or use an appropriate representation.

---

### Misconception 4

> "Grayscale is always a harmless simplification."

### Why this is wrong

Color can carry information that disappears in grayscale. Whether grayscale is appropriate depends on the task.

---

### Misconception 5

> "RGB is the best color space for every operation."

### Why this is wrong

Different tasks become easier in different representations.

HSV can make hue-based selection easier. Lab separates lightness from color-related dimensions. YUV/YCbCr separate brightness-related and chromatic information.

---

### Misconception 6

> "Computer vision and image processing are exactly the same thing."

### Why this is incomplete

They overlap heavily, but image processing often emphasizes transformation/analysis of image data, while computer vision emphasizes interpreting visual data for higher-level understanding.

---

## Key terminology

| Term | Meaning |
|---|---|
| Pixel | Smallest addressable image element storing one or more values |
| Channel | One component of a multi-component image representation |
| Sampling | Converting continuous spatial coordinates into discrete pixel locations |
| Quantization | Mapping continuous measurements to a finite set of intensity/color values |
| Grayscale | Single-channel intensity representation |
| RGB | Red-green-blue additive color representation |
| HSV | Hue-saturation-value representation |
| Lab | Color representation separating lightness from opponent color dimensions |
| YUV / YCbCr | Representations separating luminance/luma from chrominance |
| Alpha channel | Per-pixel transparency information |
| Color gamut | Range of colors a device or system can represent |
| NumPy ndarray | Multidimensional numerical array commonly used to store image data |
| Image mode | Interpretation of pixel components, such as `L`, `RGB`, or `RGBA` |
| File format | Encoded storage representation such as PNG or JPEG |
| Bit depth | Number of bits used to represent pixel/channel values |
| Normalization | Mapping values into a chosen numerical range |
| Mask | Array identifying pixels/regions to select or modify |
| Colormap | Mapping from scalar values to displayed colors |
| BGR | Blue-green-red channel ordering used commonly by OpenCV |
| Cropping | Extracting a rectangular subregion |
| Alpha blending | Weighted combination of two compatible images |
| Vectorization | Applying array-level operations rather than explicit Python loops |

---

## Self-check

Before continuing, make sure you can answer:

1. Why is an RGB image usually a 3D array while a grayscale image is usually 2D?
2. What is the difference between an image file format and an in-memory image array?
3. Where does preprocessing fit in a typical image-processing pipeline?
4. Why can an OpenCV image display with strange colors in Matplotlib?
5. What information do `shape`, `dtype`, `min()`, and `max()` tell you?
6. Why can `uint8` arithmetic produce unexpected results?
7. When might HSV be more useful than RGB?
8. What information is lost when an image is converted to grayscale?
9. How does a Boolean mask control which pixels are changed?
10. What does alpha control in alpha blending?
11. Why does image division require protection against division by zero?
12. Why is it useful to convert between PIL images and NumPy arrays?
13. What is the benefit of vectorized array operations?
14. What assumptions should you inspect before applying an image-processing function from another library?

---

## Retain this idea

**A digital image-processing workflow is fundamentally numerical: load an image into a known representation, inspect its shape/type/range/channel conventions, choose a representation suited to the task, transform the data safely, and interpret the result visually and numerically.**
""",

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "digital-image-model",
                "title": "A digital image is data",
                "order": 1,
            },
            {
                "id": "processing-and-vision",
                "title": "Image processing, computer vision, and the processing pipeline",
                "order": 2,
            },
            {
                "id": "python-toolkit",
                "title": "The Python image-processing toolkit",
                "order": 3,
            },
            {
                "id": "image-io",
                "title": "Reading, saving, and displaying images",
                "order": 4,
            },
            {
                "id": "formats-modes-dtypes",
                "title": "File formats, image modes, and data types",
                "order": 5,
            },
            {
                "id": "color-spaces",
                "title": "Color spaces: choosing the right representation",
                "order": 6,
            },
            {
                "id": "color-manipulation",
                "title": "Using color spaces for practical image manipulation",
                "order": 7,
            },
            {
                "id": "coordinates-manipulation",
                "title": "Coordinates and foundational image manipulations",
                "order": 8,
            },
            {
                "id": "engineering-extras",
                "title": "Useful engineering ideas from the chapter",
                "order": 9,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L01.EX01",

            "title": "Inspect, Convert, and Normalize an Image",

            "lesson_code": "M01.L01",

            "section_id": "formats-modes-dtypes",

            "placement": "after_section",

            "description": (
                "Practice reading an image as numerical data and reasoning about its "
                "shape, channel structure, mode, data type, and value range before "
                "performing arithmetic."
            ),

            "instructions": (
                "1. Load the same image with Pillow and convert the Pillow image to a "
                "NumPy array.\n"
                "2. Record the Pillow `size` and `mode`, then record the NumPy `shape`, "
                "`dtype`, minimum value, and maximum value.\n"
                "3. Explain why Pillow size and NumPy shape list spatial dimensions in "
                "a different order.\n"
                "4. Convert the array to floating point and normalize it to the range "
                "[0, 1]. Verify the new dtype and range.\n"
                "5. Create a grayscale or single-channel representation and build a "
                "Boolean mask using a threshold of your choice.\n"
                "6. Explain what `True` and `False` mean in that mask.\n"
                "7. Describe one arithmetic operation that could be unsafe on the "
                "original `uint8` array and explain how you would make it safe."
            ),

            "expected_output": (
                "A notebook or Python script containing the inspection code, printed "
                "metadata/ranges, the Boolean mask, and a short written explanation "
                "of dimension ordering, normalization, and overflow safety."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "image-io",
                "array-inspection",
                "data-types",
                "normalization",
                "boolean-masks",
                "numeric-safety",
            ],
        },

        {
            "id": "M01.L01.EX02",

            "title": "Build a Mini Image-Processing Pipeline",

            "lesson_code": "M01.L01",

            "section_id": "coordinates-manipulation",

            "placement": "after_section",

            "description": (
                "Combine the chapter's core ideas into a small, explainable processing "
                "pipeline rather than testing isolated functions."
            ),

            "instructions": (
                "1. Load one RGB image and inspect its shape, dtype, and value range.\n"
                "2. Crop a meaningful rectangular region using NumPy slicing.\n"
                "3. Create a second version of the image with either brightness or "
                "contrast changed using a numerically safe workflow.\n"
                "4. Convert the image into HSV or Lab and change one channel for a "
                "clear purpose; then convert back to RGB.\n"
                "5. Create one additional output using either horizontal flipping, "
                "alpha blending, masking, or a sepia matrix transformation.\n"
                "6. Display the original and processed outputs side-by-side with clear "
                "titles.\n"
                "7. For every step, write one sentence explaining why that operation "
                "was applied and what numerical representation it relied on.\n"
                "8. Identify one failure mode related to dtype, channel order, value "
                "range, shape, file path, or coordinate convention."
            ),

            "expected_output": (
                "A runnable notebook or Python script showing the original image and "
                "at least three processed results, plus a short explanation of the "
                "data representation and one identified failure mode."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "cropping",
                "brightness-contrast",
                "color-spaces",
                "image-manipulation",
                "visualization",
                "pipeline-reasoning",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L01.QZ01",

        "title": "Getting Started with Digital Image Processing — Knowledge Check",

        "lesson_code": "M01.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L01.Q01",
                "section_id": "digital-image-model",
                "question": (
                    "Which representation most naturally describes a standard RGB "
                    "image loaded as a NumPy array?"
                ),
                "options": [
                    "A one-dimensional array containing only color names",
                    "A two-dimensional array with no channel dimension",
                    "A three-dimensional array with height, width, and color channels",
                    "A text file containing one RGB tuple for the whole image",
                ],
                "correct": 2,
                "explanation": (
                    "An RGB image normally stores a three-component color vector at "
                    "each spatial location, so the array commonly has shape "
                    "(height, width, 3)."
                ),
            },

            {
                "id": "M01.L01.Q02",
                "section_id": "processing-and-vision",
                "question": (
                    "Which stage most directly prepares a noisy or low-contrast image "
                    "before later segmentation or recognition?"
                ),
                "options": [
                    "Preprocessing/enhancement",
                    "File naming",
                    "Final transmission only",
                    "Palette indexing only",
                ],
                "correct": 0,
                "explanation": (
                    "Preprocessing and enhancement improve or standardize the visual "
                    "data before higher-level analysis."
                ),
            },

            {
                "id": "M01.L01.Q03",
                "section_id": "image-io",
                "question": (
                    "Why might an image loaded with OpenCV show incorrect-looking "
                    "colors when passed directly to Matplotlib?"
                ),
                "options": [
                    "OpenCV cannot read color images",
                    "Matplotlib supports only grayscale",
                    "OpenCV commonly uses BGR ordering while Matplotlib expects RGB",
                    "NumPy automatically reverses image rows",
                ],
                "correct": 2,
                "explanation": (
                    "The array can contain valid color data but use a different channel "
                    "order. Converting BGR to RGB before Matplotlib display prevents "
                    "channel misinterpretation."
                ),
            },

            {
                "id": "M01.L01.Q04",
                "section_id": "formats-modes-dtypes",
                "question": (
                    "What should you inspect before applying arithmetic to an image "
                    "array?"
                ),
                "options": [
                    "Only the file name",
                    "Only the image's visual subject",
                    "Its dtype and numerical value range",
                    "Only whether it is JPEG",
                ],
                "correct": 2,
                "explanation": (
                    "The dtype and range determine how arithmetic behaves and whether "
                    "overflow, clipping, or normalization must be handled."
                ),
            },

            {
                "id": "M01.L01.Q05",
                "section_id": "color-spaces",
                "question": (
                    "Why can HSV be convenient for a task that selects pixels by color "
                    "while handling brightness separately?"
                ),
                "options": [
                    "HSV removes every color channel",
                    "HSV separates hue, saturation, and value into distinct components",
                    "HSV always uses fewer bytes than grayscale",
                    "HSV prevents all image noise",
                ],
                "correct": 1,
                "explanation": (
                    "HSV separates color identity, colorfulness, and brightness-related "
                    "information, which can make color-based operations easier to express."
                ),
            },

            {
                "id": "M01.L01.Q06",
                "section_id": "color-manipulation",
                "question": (
                    "What operation creates a color-pop effect in the lesson's HSV "
                    "workflow?"
                ),
                "options": [
                    "Increasing every hue to its maximum",
                    "Setting saturation to zero for pixels outside the colors to preserve",
                    "Deleting the value channel",
                    "Converting the image to a text file",
                ],
                "correct": 1,
                "explanation": (
                    "Desaturating unwanted regions makes them grayscale-like while "
                    "selected colors remain visible."
                ),
            },

            {
                "id": "M01.L01.Q07",
                "section_id": "coordinates-manipulation",
                "question": (
                    "What does `image[y1:y2, x1:x2]` most directly perform on a normal "
                    "image array?"
                ),
                "options": [
                    "Cropping",
                    "Color-space conversion",
                    "JPEG compression",
                    "Histogram equalization",
                ],
                "correct": 0,
                "explanation": (
                    "Array slicing selects a rectangular range of rows and columns, "
                    "which corresponds directly to cropping."
                ),
            },

            {
                "id": "M01.L01.Q08",
                "section_id": "coordinates-manipulation",
                "question": (
                    "In alpha blending `output = (1-alpha)*A + alpha*B`, what happens "
                    "when alpha equals 1?"
                ),
                "options": [
                    "The output is entirely image A",
                    "The output is entirely image B",
                    "Both images become grayscale",
                    "The arrays are divided by zero",
                ],
                "correct": 1,
                "explanation": (
                    "With alpha = 1, the coefficient of A becomes zero and the "
                    "coefficient of B becomes one."
                ),
            },

            {
                "id": "M01.L01.Q09",
                "section_id": "engineering-extras",
                "type": "open",
                "question": (
                    "You receive an unfamiliar image array from another Python library. "
                    "Before modifying it, describe the checks you would perform and "
                    "explain how those checks protect you from at least two common image-"
                    "processing mistakes."
                ),
            },
        ],

        "passing_score": 70,
    },
}
