"""M10.L01 — Image Segmentation: From Classical Methods to Deep Learning.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 10. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M10.L01"

MODULE_ORDER = 10

MODULE_TITLE = "Image Segmentation: From Classical Methods to Deep Learning"

MODULE_DESCRIPTION = (
    "Learn image segmentation from interpretable classical methods—thresholding, "
    "watershed, morphology, superpixels, variational models, graph/probabilistic "
    "methods, and pixel classifiers—to modern semantic, instance, and panoptic "
    "segmentation with CNNs, Mask R-CNN, YOLO, and transformer-based architectures "
    "including DPT, DETR, SegFormer, Mask2Former, and OneFormer."
)

SOURCE_CHAPTER = 10

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


TOPIC = {
    "title": "Image Segmentation: From Classical Methods to Deep Learning",

    "slug": "image-processing-m10-l01",

    "description": (
        "A unified learner-facing lesson on dividing images into meaningful regions, "
        "starting with thresholding and topographic/region methods, progressing through "
        "superpixels, variational and graphical models, and ending with CNN and "
        "transformer architectures for semantic, instance, and panoptic segmentation."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 7.0,

    "skill_tags": [
        "image-processing",
        "image-segmentation",
        "otsu",
        "multi-otsu",
        "watershed",
        "morphology",
        "distance-transform",
        "superpixels",
        "slic",
        "maskslic",
        "rag",
        "felzenszwalb",
        "quickshift",
        "chan-vese",
        "mumford-shah",
        "grabcut",
        "crf",
        "random-forest",
        "semantic-segmentation",
        "instance-segmentation",
        "panoptic-segmentation",
        "fcn",
        "deeplab",
        "mask-rcnn",
        "yolo-segmentation",
        "transformers",
        "dpt",
        "detr",
        "segformer",
        "mask2former",
        "oneformer",
        "module-10",
    ],

    "prerequisite_ids": ["M09.L01"],

    "lesson": {
        "title": "Image Segmentation: From Classical Methods to Deep Learning",

        "content": r"""
# Image Segmentation: From Classical Methods to Deep Learning

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M10.L01  
> **Module:** Image Segmentation: From Classical Methods to Deep Learning  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 10. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain segmentation as pixel-wise or region-wise partitioning of an image.
- Distinguish semantic, instance, and panoptic segmentation.
- Explain binary and Multi-Otsu thresholding using between-class variance.
- Explain marker-controlled watershed through the flooding/topographic analogy.
- Build an object-counting pipeline using thresholding, morphology, distance transforms, watershed, connected components, and region properties.
- Explain why superpixels are an intermediate representation rather than final semantic segmentation.
- Compare SLIC, MaskSLIC, RAG merging, Felzenszwalb segmentation, Quickshift, and watershed-style region formation.
- Explain Chan–Vese segmentation as region-based energy minimization.
- Explain the Mumford–Shah idea and its Ambrosio–Tortorelli approximation at a conceptual level.
- Explain GrabCut using foreground/background appearance models plus graph cuts.
- Explain CRF refinement using unary and pairwise terms and mean-field approximation.
- Build the mental model for trainable classical segmentation using handcrafted multiscale features and a Random Forest.
- Explain why ensemble segmentation can combine complementary predictions.
- Explain fully convolutional semantic segmentation and the role of skip/multi-scale features.
- Explain atrous convolution and ASPP in the DeepLab family.
- Distinguish semantic segmentation from instance segmentation with Mask R-CNN and YOLO-style models.
- Explain transformer patch embeddings, positional information, self-attention, Q/K/V, and multi-head attention.
- Compare SETR, DPT, DETR, SegFormer, Mask2Former, and OneFormer.
- Choose a segmentation family based on supervision, interaction, scene complexity, object-instance needs, computational constraints, and desired output granularity.

---

## 1. What segmentation means

Image classification produces one label for a whole image.

Object detection produces coarse object locations such as bounding boxes.

Image segmentation provides a denser interpretation:

```text
image
  ↓
label / region assignment
for individual pixels
```

Formally, segmentation partitions the image domain into regions:

```text
Omega = R1 ∪ R2 ∪ ... ∪ Rk
```

where each region should be meaningful according to the task.

"Meaningful" may mean:

- similar intensity,
- similar color/texture,
- connected object region,
- foreground versus background,
- one semantic class,
- one individual instance,
- a complete panoptic scene representation.

### The evolution in this chapter

The source chapter presents segmentation as an evolution:

```text
intensity rules
    ↓
edges / morphology / topography
    ↓
regions / graphs / energy minimization
    ↓
handcrafted features + machine learning
    ↓
CNN dense prediction
    ↓
transformer / query / universal segmentation
```

[[IMAGE_NEEDED: Segmentation evolution map | Show one image flowing through threshold-based regions, watershed regions, superpixels/graphs, CNN semantic map, instance masks, and panoptic output | Learner should see segmentation evolving from hand-crafted local rules to learned global/object-centric reasoning]]

### Three modern output paradigms

**Semantic segmentation**

Every pixel receives a class:

```text
road, sky, person, tree, ...
```

Two people can share the same "person" label without being distinguished.

**Instance segmentation**

Objects of the same class are separated:

```text
person #1
person #2
person #3
```

**Panoptic segmentation**

Combines:

- **things** — countable object instances,
- **stuff** — amorphous regions such as sky or road.

---

## 2. Threshold-based segmentation and Multi-Otsu

Thresholding groups pixels by intensity.

For binary segmentation:

```text
pixel < T  -> class 0
pixel >= T -> class 1
```

### Otsu's principle

Otsu chooses a threshold that maximizes separation between classes.

The source describes this with **between-class variance**.

The central idea is:

> Choose thresholds so class means are as separated from the global intensity mean as possible.

### Multi-Otsu

Real images may contain more than two intensity groups.

For `K` classes, Multi-Otsu chooses:

```text
K - 1 thresholds
```

For example, three classes require two thresholds:

```text
[0 ... t1]       -> class 0
(t1 ... t2]      -> class 1
(t2 ... max]     -> class 2
```

With scikit-image:

```python
import numpy as np
from skimage.filters import threshold_multiotsu

thresholds = threshold_multiotsu(
    image,
    classes=3,
)

regions = np.digitize(
    image,
    bins=thresholds,
)
```

[[IMAGE_NEEDED: Multi-Otsu histogram segmentation | Show grayscale image, multimodal histogram with two threshold lines, and three-color region label map | Learner should connect histogram peaks and valleys with threshold-based class separation]]

### When Multi-Otsu works well

The chapter says it works best when:

- the histogram has distinct modes,
- noise is low,
- meaningful classes have separable intensities.

### Limitations

It can struggle when:

- illumination varies across the image,
- class intensity distributions overlap,
- texture or semantics matter more than raw intensity.

The lesson:

> Thresholding is powerful when the data really are separable by intensity; it should not be forced onto problems where intensity is not the right representation.

---

## 3. Watershed, morphology, and object counting

Watershed treats an image as a topographic surface.

A common interpretation is:

```text
dark regions -> valleys / basins
bright regions -> mountains
gradient magnitude -> boundary terrain
```

### Flooding analogy

Imagine water rising from selected marker points.

1. Water begins inside marker basins.
2. Regions expand as the water level rises.
3. When two floods would meet, a watershed boundary is formed.

### Why markers matter

Naive watershed can over-segment noisy images.

Marker-controlled watershed uses selected seeds for:

- object regions,
- background regions.

This constrains flooding.

A source-aligned workflow:

```python
from scipy import ndimage as ndi
from skimage.filters import rank
from skimage.segmentation import watershed

denoised = rank.median(
    image,
    footprint=disk(2),
)

markers = (
    rank.gradient(
        denoised,
        disk(5),
    ) < 20
)

markers = ndi.label(markers)[0]

gradient = rank.gradient(
    denoised,
    disk(2),
)

labels = watershed(
    gradient,
    markers,
)
```

[[IMAGE_NEEDED: Marker-controlled watershed | Show grayscale image, gradient topography, marker seeds, flooding concept, and final labeled watershed regions | Learner should see markers controlling where basins begin and strong gradients stopping region growth]]

### Counting touching coins

The chapter turns segmentation into a complete vision pipeline.

#### Step 1: binary mask

Use thresholding to separate foreground from background.

#### Step 2: morphology

Operations such as:

- remove small objects,
- fill holes,
- opening,
- closing,

clean the mask.

#### Step 3: distance transform

For each foreground pixel:

```text
distance = distance to nearest background
```

The centers of thick objects create high values.

#### Step 4: local maxima as markers

Coin centers become marker seeds.

#### Step 5: watershed on negative distance

Using:

```text
-distance
```

turns distance peaks into watershed basins.

Touching coins can then be split.

#### Step 6: connected regions and properties

For each segmented region, compute properties such as:

- area,
- perimeter,
- eccentricity,
- solidity,
- centroid.

The chapter uses circularity:

```text
circularity =
4π * area / perimeter²
```

to reject irregular non-coin regions.

[[IMAGE_NEEDED: Coin counting pipeline | Show original coins, threshold mask, cleaned morphology mask, distance transform, local-max markers, watershed-separated coins, and final counted/centroid-labeled objects | Learner should understand segmentation as a multi-stage pipeline rather than a single function]]

{{exercise:M10.L01.EX01}}

---

## 4. Superpixels: SLIC, MaskSLIC, and RAG merging

Superpixels group neighboring pixels into small perceptually coherent regions.

They are usually an **over-segmentation**:

```text
pixels
  ↓
many small homogeneous regions
  ↓
later grouping / reasoning
```

They are not automatically semantic objects.

### SLIC

SLIC performs localized clustering in a combined space containing:

- spatial coordinates,
- color components, often in Lab space.

Its distance combines:

```text
color similarity
+
spatial proximity
```

A compactness parameter controls the trade-off.

### MaskSLIC

MaskSLIC constrains superpixel formation to a supplied region of interest.

This can:

- prevent irrelevant background superpixels,
- improve object-focused boundary adherence.

### Region Adjacency Graph (RAG)

Superpixels often fragment one object into many pieces.

A RAG represents:

```text
nodes -> regions
edges -> neighboring region relationships
```

Region features can include mean color.

Adjacent similar regions can be merged hierarchically.

The conceptual pipeline is:

```text
image
  ↓ SLIC
many superpixels
  ↓ build adjacency graph
region similarity weights
  ↓ hierarchical merging
larger meaningful regions
```

[[IMAGE_NEEDED: SLIC MaskSLIC and RAG | Show original image, SLIC superpixels, object mask, MaskSLIC constrained superpixels, adjacency graph over regions, and merged output | Learner should distinguish over-segmentation from later region merging]]

---

## 5. Felzenszwalb, Quickshift, Watershed, and the role of region grouping

The source compares several region/superpixel methods.

### Felzenszwalb graph segmentation

Model the image as a graph:

```text
node -> pixel
edge -> neighboring pixels
weight -> appearance difference
```

Initially:

```text
each pixel = its own component
```

Edges are considered in increasing order of dissimilarity.

Components merge when:

- the boundary difference is small enough,
- relative to their internal variation.

A scale parameter affects segmentation granularity.

### Quickshift

Quickshift treats pixels as samples in joint spatial-color space.

It estimates density and links pixels toward nearby higher-density points.

Segments emerge around density modes.

This is a mode-seeking idea rather than fixed-`K` clustering.

### Watershed

Watershed groups according to topographic flooding.

### SLIC

SLIC emphasizes regular, compact, color-homogeneous superpixels.

### The important comparison

These algorithms group regions for different reasons:

```text
Felzenszwalb -> graph/component evidence
Quickshift   -> density modes
Watershed    -> topographic basins
SLIC         -> localized clustering
```

The chapter then applies RAG merging to several methods to move from initial regionization toward larger segments.

---

## 6. Variational segmentation: Chan–Vese and Mumford–Shah

Variational methods define an **energy** and search for the segmentation that minimizes it.

A generic structure is:

```text
energy =
data fidelity
+
lambda * regularity
```

The data term rewards explaining the image.

The regularization term discourages implausible or overly complex boundaries.

### Chan–Vese active contours

Chan–Vese is region-based.

Unlike gradient-based contours, it can segment an object even when the visible boundary is weak.

Its energy encourages:

- pixels inside the contour to resemble an inside mean,
- pixels outside to resemble an outside mean,
- the contour to remain reasonably regular.

The contour is represented implicitly with a level-set function.

Using scikit-image:

```python
from skimage.segmentation import chan_vese

segmentation, level_set, energy = chan_vese(
    image,
    mu=0.25,
    lambda1=1,
    lambda2=1,
    init_level_set="checkerboard",
    extended_output=True,
)
```

[[IMAGE_NEEDED: Chan-Vese energy evolution | Show original weak-edge image, initial contour/level set, intermediate evolving contour, final binary region, and decreasing energy curve | Learner should see segmentation emerging from region statistics rather than explicit edge detection]]

### Mumford–Shah

Mumford–Shah jointly reasons about:

- a piecewise-smooth approximation,
- edges/discontinuities,
- boundary complexity.

Its energy conceptually balances:

```text
fit the observed image
+
keep each region smooth
+
avoid unnecessary boundaries
```

### Ambrosio–Tortorelli approximation

Direct Mumford–Shah minimization is difficult.

The chapter introduces an auxiliary edge variable so the problem can be optimized approximately.

The demonstration alternates:

```text
solve edge indicator
solve smooth image
repeat
```

This produces:

- a smoothed/segmented representation,
- an edge map.

---

## 7. GrabCut and conditional random fields

### GrabCut

GrabCut combines:

- Gaussian Mixture Models for foreground/background appearance,
- graph-cut optimization,
- user-provided initialization.

A user often draws a rectangle around the object.

Pixels receive one of several states:

```text
sure background
sure foreground
probable background
probable foreground
```

### Energy intuition

GrabCut balances:

```text
unary/data term
-> how well a pixel fits foreground/background appearance

pairwise/smoothness term
-> nearby similar pixels prefer consistent labels
```

A graph is built with:

- pixel nodes,
- source = foreground,
- sink = background.

Min-cut / max-flow produces a globally optimized binary labeling.

[[IMAGE_NEEDED: GrabCut graph model | Show image with bounding box/scribbles, foreground and background GMM appearance models, pixel graph connected to source/sink, min-cut boundary, and extracted object | Learner should understand the combination of user hints, appearance likelihood, and neighborhood smoothness]]

The chapter also demonstrates manual foreground/background scribbles to correct an imperfect rectangle initialization.

### Conditional Random Fields (CRFs)

CRFs refine label predictions probabilistically.

A CRF energy also combines:

- unary potential,
- pairwise potential.

The chapter's dense CRF uses two important pairwise kernels.

**Spatial Gaussian**

Encourages nearby pixels to have similar labels.

**Bilateral**

Encourages nearby pixels with similar colors to share labels while preserving color boundaries.

### Mean-field approximation

Exact dense CRF inference is expensive.

Mean-field inference approximates the distribution as a product of per-pixel label distributions and iteratively updates them.

One iteration conceptually performs:

```text
message passing
→ pairwise filtering
→ compatibility transform
→ add unary evidence
→ normalize
```

The result is a boundary-refined segmentation.

### GrabCut versus CRF

```text
GrabCut
-> interactive foreground/background segmentation
-> graph cut + appearance models

CRF
-> probabilistic segmentation refinement
-> context-aware, edge-aware label smoothing
```

---

## 8. Trainable classical segmentation and ensembles

Classical segmentation does not have to be rule-only.

The chapter builds a bridge toward deep learning by training a classifier on engineered pixel features.

### Pixel as a feature vector

For each pixel:

```text
features =
[
    intensity,
    multiscale texture,
    derivative/Hessian-type information,
    ...
]
```

The chapter uses multiscale features computed across several Gaussian scales.

Small scales capture:

- fine texture,
- small structures.

Large scales capture:

- broader shape/regions.

### Random Forest segmentation

Sparse training labels are provided manually.

Then:

```text
labeled pixels + handcrafted features
        ↓
Random Forest training
        ↓
predict class for every pixel
        ↓
segmentation map
```

With scikit-image utilities, the classifier is trained only on labeled locations.

[[IMAGE_NEEDED: Random-Forest pixel segmentation | Show image, sparse hand-labeled training regions, multiscale feature stack, Random Forest, and dense predicted segmentation map | Learner should see the bridge from handcrafted features to supervised pixel classification]]

### Ensemble segmentation

Different methods make different mistakes.

The source combines region outputs such as:

- watershed,
- SLIC/graph segmentation,

using segmentation joining or model voting.

For neural models, the chapter later demonstrates:

**Soft voting**

```text
average class probabilities
-> argmax
```

**Majority voting**

```text
collect hard class predictions
-> mode per pixel
```

Ensembling can improve robustness when component models are complementary.

---

## 9. Deep segmentation and fully convolutional networks

Deep learning learns:

```text
features + decision rule
```

jointly from data.

Instead of engineering intensity, texture, and edge features manually, the model learns hierarchical representations end to end.

### Training objective

The chapter describes a loss comparing:

```text
predicted segmentation
vs.
ground-truth mask
```

with examples such as:

- cross-entropy,
- Dice loss.

### Fully Convolutional Networks (FCNs)

A classification CNN normally compresses features and ends with fully connected layers.

FCNs remove fully connected layers and keep spatial feature maps.

Conceptually:

```text
image
  ↓ encoder
deep feature map
  ↓ class-score convolutions
coarse semantic map
  ↓ upsample
full-resolution segmentation
```

### Skip connections

Deep features contain semantics but lose spatial precision.

Shallower features retain more detail.

FCN-style fusion combines:

```text
deep semantics
+
shallow localization
```

to improve dense prediction.

[[IMAGE_NEEDED: FCN semantic segmentation | Show encoder feature hierarchy, 1×1 class-score maps, skip fusion from shallow/deep layers, upsampling, and final pixel-wise semantic map | Learner should understand why dense prediction differs from image classification]]

### Pretrained inference

The chapter uses pretrained segmentation models from Torchvision, including:

- FCN-ResNet50,
- DeepLabV3-ResNet50,
- DeepLabV3-MobileNet,
- LR-ASPP-MobileNet.

The practical inference pattern is:

```python
model.eval()

with torch.no_grad():
    logits = model(input_tensor)["out"]

probabilities = logits.softmax(dim=1)
mask = probabilities.argmax(dim=1)
```

---

## 10. DeepLab: atrous convolution, ASPP, and CNN ensembles

Repeated downsampling gives CNNs large receptive fields but harms output resolution.

DeepLab addresses this with **atrous/dilated convolution**.

### Atrous convolution

A dilation rate inserts spacing between kernel sample locations.

This increases receptive field without necessarily reducing feature-map resolution.

Conceptually:

```text
ordinary 3×3
x x x
x x x
x x x

dilated
x . x . x
. . . . .
x . x . x
. . . . .
x . x . x
```

### Atrous Spatial Pyramid Pooling (ASPP)

Objects occur at different scales.

ASPP applies several parallel atrous filters at different dilation rates.

Their outputs are combined to capture multiscale context.

[[IMAGE_NEEDED: DeepLab ASPP | Show feature map entering parallel atrous convolution branches with different dilation rates plus pooled/global context, then feature fusion and semantic prediction | Learner should see ASPP as multiscale context without aggressive spatial downsampling]]

### DeepLab family progression in the source

```text
DeepLabV1 -> CRF refinement
DeepLabV2 -> atrous convolution
DeepLabV3 -> ASPP
DeepLabV3+ -> encoder-decoder refinement
```

### Multiple frameworks

The chapter demonstrates or references DeepLab inference using:

- Torchvision,
- TensorFlow Model Garden,
- Torch Hub,
- KerasHub,
- KerasCV.

The important learner skill is recognizing the common pipeline:

```text
preprocess
→ forward pass
→ logits
→ resize to original image
→ class argmax
→ colorize/overlay
```

not memorizing each framework's syntax.

### CNN ensemble

The source combines models by averaging probability maps or majority voting hard masks.

Ensembling can improve stability but adds:

- runtime,
- memory,
- deployment complexity.

---

## 11. Instance segmentation: Mask R-CNN and YOLO-style segmentation

Semantic segmentation answers:

```text
which class does this pixel belong to?
```

Instance segmentation additionally asks:

```text
which individual object does this pixel belong to?
```

### Mask R-CNN

Mask R-CNN extends Faster R-CNN with a mask branch.

Its major components are:

1. backbone such as ResNet + FPN,
2. Region Proposal Network,
3. ROI heads for:
   - class prediction,
   - bounding-box refinement,
   - binary instance mask.

The total objective includes:

```text
classification loss
+
box regression loss
+
mask loss
```

### ROIAlign

Pixel-accurate masks require spatial alignment.

ROIAlign uses interpolation rather than coarse quantized ROI pooling.

This reduces alignment error between features and object masks.

[[IMAGE_NEEDED: Mask R-CNN architecture | Show image→backbone/FPN→RPN proposals→ROIAlign→parallel classification, box regression, and mask branches→separate instance masks | Learner should understand the two-stage instance-segmentation pipeline]]

### Strengths and limits

The source emphasizes:

- strong accuracy,
- separate same-class instances,
- good spatial precision.

Trade-offs:

- two-stage processing,
- more memory,
- slower than single-stage real-time designs.

### YOLO segmentation

The chapter also introduces YOLOv8/YOLOv11-style single-stage segmentation.

The model predicts object information in one forward pass and combines instance-specific coefficients with learned prototype masks.

Conceptually:

```text
shared image features
   ↓
boxes/classes/confidence
+
mask coefficients
   ↓
prototype masks
   ↓
individual instance masks
```

This is optimized for fast GPU inference.

---

## 12. Transformer foundations for segmentation

CNNs have a strong locality bias.

Transformers explicitly model long-range relationships through attention.

### From image to tokens

Divide an image into patches.

Each patch becomes a token:

```text
patch
  ↓ flatten / projection
embedding vector
```

Stack all token embeddings:

```text
image -> token sequence
```

The chapter notes that patch projection can also be viewed as a convolution with kernel size/stride equal to the patch size.

### Positional information

Plain self-attention does not inherently know spatial order.

Different architectures handle spatial information differently.

The source examples include:

- learnable positional embeddings in ViT/DPT,
- relative positional bias in Swin,
- no explicit positional encoding in SegFormer.

### Q, K, V

For every token:

```text
Query  -> what am I looking for?
Key    -> what do I contain?
Value  -> what information do I provide?
```

Scaled dot-product attention compares queries with keys and uses the resulting weights to combine values.

[[IMAGE_NEEDED: Q K V self-attention for image patches | Show image split into patches/tokens, one token producing Query, all tokens providing Keys/Values, attention weights to distant patches, and aggregated context | Learner should understand global interaction between image regions]]

### Multi-head attention

Several attention heads can model different relationships:

- geometry,
- texture,
- semantics.

### Transformer block

A transformer encoder layer includes:

- normalization,
- multi-head self-attention,
- residual connection,
- second normalization,
- feed-forward network,
- second residual connection.

### Computational challenge

Full attention grows rapidly with token count.

High-resolution segmentation therefore motivates:

- hierarchical representations,
- efficient decoders,
- query-based prediction.

---

## 13. SETR and DPT: from tokens back to dense maps

### SETR

SETR demonstrated pure ViT semantic segmentation.

The basic logic is:

```text
image patches
→ transformer encoder
→ token predictions
→ spatial reshape
→ 1×1 classification
→ upsample
```

The source highlights limitations:

- weak fine spatial detail,
- boundary localization difficulty,
- high computation.

### DPT

Dense Prediction Transformer improves localization by fusing features from multiple transformer depths.

Interpretation:

```text
earlier layers -> finer details
deeper layers  -> stronger semantics
multi-scale fusion -> better dense prediction
```

[[IMAGE_NEEDED: SETR versus DPT | Show SETR using one final ViT token grid and simple upsampling versus DPT taking features from several transformer depths and fusing them into a dense output | Learner should understand why multi-level fusion improves localization]]

The chapter demonstrates pretrained DPT semantic segmentation by:

1. preprocessing the image,
2. producing logits,
3. resizing logits to original resolution,
4. taking the class argmax,
5. colorizing and overlaying the result.

---

## 14. DETR and SegFormer: two different transformer philosophies

### DETR: query-based prediction

DETR uses learned **object queries**.

Instead of independently classifying every pixel, queries reason about objects/regions globally.

For panoptic segmentation, post-processing converts the query outputs into:

- segmentation map,
- segment metadata.

The source emphasizes:

- end-to-end object reasoning,
- no traditional non-maximum suppression requirement,
- unified detection + segmentation behavior.

[[IMAGE_NEEDED: DETR object queries | Show transformer image features plus several learned object-query tokens attending globally and producing class/mask predictions that combine into a panoptic segmentation map | Learner should understand object-centric query prediction versus per-pixel classification]]

### SegFormer: hierarchical dense prediction

SegFormer uses a different design.

It combines:

- overlapping patch embeddings,
- multi-stage hierarchical transformer encoder,
- multi-resolution feature maps,
- lightweight MLP decoder,
- no explicit positional encoding.

Interpretation:

```text
CNN-like spatial hierarchy
implemented with transformer blocks
+
simple multi-scale decoder
```

This aims to balance:

- global context,
- efficiency,
- spatial detail.

### Dataset-specific meaning

The chapter demonstrates SegFormer on datasets such as:

- ADE20K,
- Cityscapes,
- CamVid.

The architecture may be shared, but fine-tuning/training data defines:

- the label space,
- what scene concepts the model predicts.

---

## 15. Mask2Former and OneFormer: universal segmentation

### Mask2Former

Mask2Former reformulates segmentation as **mask classification**.

Instead of asking independently for every pixel:

```text
what class are you?
```

the model predicts a set:

```text
(mask_1, class_1)
(mask_2, class_2)
...
```

This is object/region-centric.

The source describes training with matching plus losses for:

- classification,
- pixel-wise mask accuracy,
- Dice overlap.

### Why mask classification is important

The same architecture can support:

- semantic segmentation,
- instance segmentation,
- panoptic segmentation.

The chapter demonstrates separate pretrained checkpoints and post-processing for these output types.

[[IMAGE_NEEDED: Pixel classification vs mask classification | Show left: independent per-pixel semantic labels; right: transformer queries predicting mask–class pairs that combine into semantic, instance, or panoptic outputs | Learner should understand the Mask2Former paradigm shift]]

### OneFormer

OneFormer extends universal segmentation with **task conditioning**.

A single architecture can be prompted/configured for a task such as:

```text
semantic
instance
panoptic
```

The chapter demonstrates semantic segmentation on:

- ADE20K,
- Cityscapes.

The central idea is:

```text
shared model
+
task condition
+
mask prediction
```

This reduces the need for completely separate models for each segmentation paradigm.

### Evolution of transformer segmentation in the chapter

```text
SETR
-> pure ViT dense prediction

DPT
-> multi-scale transformer fusion

DETR
-> object-query reasoning

SegFormer
-> hierarchical efficient dense prediction

Mask2Former
-> universal mask classification

OneFormer
-> task-conditioned universal segmentation
```

---

## 16. Choosing the right segmentation approach

The chapter spans very different methods because segmentation problems differ.

A practical decision guide is:

| Situation | Good starting point from this chapter |
|---|---|
| Clear intensity classes | Otsu / Multi-Otsu |
| Touching objects | Distance transform + watershed |
| Need compact low-level regions | SLIC / MaskSLIC |
| Need graph-aware region merging | RAG / Felzenszwalb |
| Weak edges but homogeneous regions | Chan–Vese |
| Interactive foreground extraction | GrabCut |
| Refine coarse labels along boundaries | Dense CRF |
| Small labeled set + engineered features | Random Forest pixel classification |
| Standard semantic segmentation | FCN / DeepLab |
| Need same-class objects separated | Mask R-CNN / YOLO segmentation |
| Need long-range global context | Transformer segmentation |
| Efficient transformer semantic segmentation | SegFormer |
| Unified semantic/instance/panoptic masks | Mask2Former |
| Task-conditioned universal model | OneFormer |

The deeper questions are:

```text
Do I need classes or only regions?
Do I need separate object instances?
Is supervision available?
Do I have user hints or masks?
Are boundaries weak?
Is the image histogram separable?
Is real-time performance required?
Do I need global semantic context?
```

{{exercise:M10.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Segmentation and classification are the same because both assign labels.

### Why this is wrong

Classification returns image-level labels; segmentation returns dense spatial labels or regions.

### Misconception 2

> Multi-Otsu discovers semantic classes.

### Why this is wrong

It separates intensity distributions. Semantic meaning is not guaranteed.

### Misconception 3

> Watershed automatically solves touching-object segmentation without setup.

### Why this is wrong

Noise and poor markers can cause severe over-segmentation or incorrect region splitting.

### Misconception 4

> Superpixels are final semantic objects.

### Why this is wrong

They are usually low-level homogeneous regions that can serve as an efficient intermediate representation.

### Misconception 5

> Chan–Vese requires strong visible edges.

### Why this is wrong

It is region-based and can work when boundaries are weak if inside/outside region statistics differ.

### Misconception 6

> CRF refinement is just ordinary image blurring.

### Why this is wrong

Its pairwise terms smooth labels probabilistically and can preserve boundaries using bilateral appearance information.

### Misconception 7

> A Random Forest segmentation pipeline has no learning because the features are handcrafted.

### Why this is wrong

The features are engineered, but the classifier still learns a decision boundary from labeled pixels.

### Misconception 8

> Semantic segmentation separates every person into a different mask.

### Why this is wrong

Semantic segmentation merges same-class pixels conceptually; instance segmentation separates objects.

### Misconception 9

> Atrous convolution increases receptive field only by downsampling feature maps.

### Why this is wrong

It expands sampling spacing inside the convolution kernel while preserving denser spatial output.

### Misconception 10

> An RGB image becomes a transformer input simply by treating every pixel as one token in all architectures.

### Why this is wrong

The source describes patch/token embeddings; architectures then vary in hierarchy and spatial representation.

### Misconception 11

> DETR, SegFormer, and Mask2Former solve segmentation in the same way.

### Why this is wrong

DETR is query/object-centric, SegFormer is hierarchical dense prediction, and Mask2Former uses mask classification.

### Misconception 12

> A universal segmentation architecture means training data no longer matters.

### Why this is wrong

The source examples show that datasets such as ADE20K and Cityscapes define different label spaces and scene knowledge.

---

## Key terminology

| Term | Meaning |
|---|---|
| Segmentation | Partitioning an image into meaningful labeled pixels or regions |
| Semantic segmentation | One semantic class per pixel without separate object identities |
| Instance segmentation | Separate mask for each individual object instance |
| Panoptic segmentation | Unified thing-instance and stuff-region segmentation |
| Thresholding | Region assignment based on intensity boundaries |
| Otsu | Threshold selection by maximizing between-class variance |
| Multi-Otsu | Generalization of Otsu to multiple intensity classes |
| Watershed | Topographic flooding-based segmentation |
| Marker | Seed that initializes a watershed region |
| Morphology | Shape-based binary/region operations such as opening and closing |
| Distance transform | Distance of each foreground pixel to nearest background |
| Connected component | Spatially connected labeled region |
| Superpixel | Small perceptually homogeneous image region |
| SLIC | Localized color-spatial clustering for superpixels |
| MaskSLIC | SLIC constrained by a region mask |
| RAG | Region Adjacency Graph |
| Felzenszwalb segmentation | Graph-based adaptive component merging |
| Quickshift | Mode-seeking clustering in spatial-color feature space |
| Chan–Vese | Region-based active-contour energy model |
| Mumford–Shah | Variational piecewise-smooth segmentation framework |
| GrabCut | Interactive GMM + graph-cut foreground segmentation |
| Unary potential | Per-pixel label evidence |
| Pairwise potential | Compatibility/smoothness relationship between labels |
| CRF | Conditional Random Field |
| Mean-field inference | Approximate iterative probabilistic inference |
| FCN | Fully Convolutional Network |
| Atrous convolution | Dilated convolution with spaced kernel sampling |
| ASPP | Atrous Spatial Pyramid Pooling |
| ROIAlign | Interpolated ROI feature extraction preserving spatial alignment |
| Object query | Learned token used to predict object/region outputs |
| Patch embedding | Projection of image patches into transformer tokens |
| Self-attention | Global token interaction based on Q/K/V similarity |
| SETR | Pure ViT dense segmentation framework |
| DPT | Dense Prediction Transformer with multi-scale fusion |
| DETR | Query-based end-to-end detection/segmentation transformer |
| SegFormer | Hierarchical transformer with lightweight MLP decoder |
| Mask2Former | Universal mask-classification transformer |
| OneFormer | Task-conditioned universal segmentation transformer |

---

## Self-check

Before continuing, make sure you can answer:

1. How does segmentation differ from classification and detection?
2. What is the difference between semantic, instance, and panoptic segmentation?
3. What objective does Otsu optimize?
4. Why does Multi-Otsu work best for multimodal histograms?
5. Why does watershed need markers?
6. Why does the distance transform help separate touching coins?
7. What do opening and hole filling contribute to object counting?
8. Why are region properties useful after segmentation?
9. Why are superpixels called over-segmentation?
10. What two types of distance does SLIC balance?
11. What does MaskSLIC add to SLIC?
12. Why is a RAG useful after superpixelization?
13. How does Felzenszwalb segmentation differ from SLIC?
14. What is mode seeking in Quickshift?
15. Why can Chan–Vese work with weak boundaries?
16. What three terms/ideas does Mumford–Shah balance?
17. What evidence does GrabCut model?
18. What is the role of min-cut/max-flow in GrabCut?
19. What is the difference between CRF unary and pairwise terms?
20. Why does a bilateral CRF term preserve edges?
21. Why is mean-field inference used for dense CRFs?
22. What makes Random-Forest segmentation "trainable classical" rather than deep learning?
23. Why are multiscale handcrafted features useful?
24. What is the difference between soft voting and majority voting?
25. What makes an FCN different from a classification CNN?
26. Why do skip connections help semantic segmentation?
27. What does atrous convolution change?
28. Why does DeepLab use ASPP?
29. Why does semantic segmentation not distinguish two people?
30. What three output branches does Mask R-CNN use?
31. Why is ROIAlign important for masks?
32. Why can YOLO segmentation be faster than a two-stage system?
33. How does an image become a token sequence?
34. What do Query, Key, and Value mean conceptually?
35. Why is positional information important for transformers?
36. Why is full self-attention expensive at high image resolution?
37. How does DPT improve on a simple pure-ViT dense prediction approach?
38. How does DETR differ from pixel-wise segmentation?
39. What makes SegFormer hierarchical?
40. What is mask classification in Mask2Former?
41. How can Mask2Former support semantic, instance, and panoptic tasks?
42. What extra idea does OneFormer add?
43. Why does dataset-specific training still matter for universal architectures?

---

## Retain this idea

**Segmentation has evolved from asking “which pixels look alike?” to asking “which regions belong together?”, then “which class is each pixel?”, and finally “which objects and scene regions exist, and what masks describe them?” Classical methods expose the rules explicitly; deep and transformer models learn increasingly global representations and object-level reasoning from data.**
        """,

        "estimated_minutes": 420,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "segmentation-mental-model", "title": "What Segmentation Means", "order": 1},
            {"id": "multi-otsu", "title": "Threshold-Based Segmentation and Multi-Otsu", "order": 2},
            {"id": "watershed-morphology", "title": "Watershed, Morphology, and Object Counting", "order": 3},
            {"id": "superpixels-rag", "title": "Superpixels: SLIC, MaskSLIC, and RAG Merging", "order": 4},
            {"id": "graph-region-algorithms", "title": "Felzenszwalb, Quickshift, Watershed, and Region Grouping", "order": 5},
            {"id": "variational-segmentation", "title": "Variational Segmentation: Chan–Vese and Mumford–Shah", "order": 6},
            {"id": "grabcut-crf", "title": "GrabCut and Conditional Random Fields", "order": 7},
            {"id": "classical-learning-ensemble", "title": "Trainable Classical Segmentation and Ensembles", "order": 8},
            {"id": "deep-segmentation-paradigms", "title": "Deep Segmentation and Fully Convolutional Networks", "order": 9},
            {"id": "deeplab-ensemble", "title": "DeepLab: Atrous Convolution, ASPP, and CNN Ensembles", "order": 10},
            {"id": "instance-maskrcnn-yolo", "title": "Instance Segmentation: Mask R-CNN and YOLO-Style Segmentation", "order": 11},
            {"id": "transformer-foundations", "title": "Transformer Foundations for Segmentation", "order": 12},
            {"id": "setr-dpt", "title": "SETR and DPT: From Tokens Back to Dense Maps", "order": 13},
            {"id": "detr-segformer", "title": "DETR and SegFormer: Two Transformer Philosophies", "order": 14},
            {"id": "mask2former-oneformer", "title": "Mask2Former and OneFormer: Universal Segmentation", "order": 15},
            {"id": "method-selection", "title": "Choosing the Right Segmentation Approach", "order": 16},
        ],
    },

    "exercises": [
        {
            "id": "M10.L01.EX01",

            "title": "Build a Classical Segmentation Pipeline",

            "lesson_code": "M10.L01",

            "section_id": "watershed-morphology",

            "placement": "after_section",

            "description": (
                "Use thresholding, morphology, distance transforms, watershed, and region "
                "properties to turn an image-processing problem into measurable objects."
            ),

            "instructions": (
                "1. Choose an image containing multiple objects, preferably with at least "
                "some objects touching.\n"
                "2. Convert to grayscale if needed and create an initial foreground mask "
                "using Otsu or Multi-Otsu thresholding.\n"
                "3. Remove small regions and fill internal holes using morphology.\n"
                "4. Compute the Euclidean distance transform of the foreground mask.\n"
                "5. Detect local maxima of the distance map and convert them into watershed markers.\n"
                "6. Apply watershed to the negative distance map while restricting it to "
                "the foreground mask.\n"
                "7. Compute region properties such as area, perimeter, centroid, "
                "eccentricity, or solidity.\n"
                "8. Define at least one geometric rule for rejecting non-target regions.\n"
                "9. Count the remaining labeled objects and overlay their centroids on the image.\n"
                "10. Explain one failure caused by thresholding and one failure caused by "
                "incorrect marker selection."
            ),

            "expected_output": (
                "A notebook or script showing the original image, threshold mask, cleaned "
                "mask, distance map, markers, watershed regions, final filtered objects, "
                "object count, and a short error analysis."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "otsu",
                "morphology",
                "distance-transform",
                "watershed",
                "connected-components",
                "region-properties",
                "object-counting",
            ],
        },

        {
            "id": "M10.L01.EX02",

            "title": "Compare Classical, CNN, and Transformer Segmentation",

            "lesson_code": "M10.L01",

            "section_id": "method-selection",

            "placement": "after_section",

            "description": (
                "Compare how segmentation changes when the representation evolves from "
                "handcrafted regions to learned dense prediction and object-centric masks."
            ),

            "instructions": (
                "1. Select one natural image with several semantic categories and multiple "
                "object instances.\n"
                "2. Run one classical method such as SLIC+RAG, watershed, GrabCut, or "
                "Random-Forest segmentation.\n"
                "3. Run one pretrained CNN semantic model such as FCN or DeepLab.\n"
                "4. Run one instance or panoptic model such as Mask R-CNN, YOLO segmentation, "
                "DETR, or Mask2Former if compute/resources allow.\n"
                "5. Optionally run one transformer semantic model such as SegFormer, DPT, "
                "or OneFormer.\n"
                "6. For each output, state whether it represents low-level regions, semantic "
                "classes, individual instances, or panoptic thing/stuff labels.\n"
                "7. Compare boundary precision, same-class instance separation, global "
                "context, runtime/compute needs, and the role of training data.\n"
                "8. Explain why a superpixel output should not be judged as though it were "
                "a semantic model.\n"
                "9. Explain why two pretrained semantic models may disagree even on the same image.\n"
                "10. Finish with a decision table selecting a method for: document regions, "
                "touching cells/coins, interactive foreground extraction, road-scene "
                "semantics, real-time instances, and unified panoptic scene understanding."
            ),

            "expected_output": (
                "A notebook/report with at least three segmentation paradigms, visual "
                "overlays, a comparison of output meaning and computational assumptions, "
                "and a problem-to-method decision table."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "classical-segmentation",
                "semantic-segmentation",
                "instance-segmentation",
                "panoptic-segmentation",
                "cnn-segmentation",
                "transformer-segmentation",
                "model-comparison",
                "method-selection",
            ],
        },
    ],

    "quiz": {
        "id": "M10.L01.QZ01",

        "title": "Image Segmentation: From Classical Methods to Deep Learning — Knowledge Check",

        "lesson_code": "M10.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M10.L01.Q01",
                "section_id": "segmentation-mental-model",
                "question": "What is the key output difference between classification and segmentation?",
                "options": [
                    "Segmentation provides dense spatial labels or regions rather than only an image-level label",
                    "Classification always produces more pixels",
                    "Segmentation cannot use neural networks",
                    "Classification requires a mask for every image",
                ],
                "correct": 0,
                "explanation": (
                    "Segmentation assigns labels spatially, while image classification summarizes "
                    "the whole image with one or more labels."
                ),
            },

            {
                "id": "M10.L01.Q02",
                "section_id": "multi-otsu",
                "question": "What does Multi-Otsu optimize conceptually?",
                "options": [
                    "Separation between intensity classes using between-class variance",
                    "Object-query matching",
                    "Transformer attention entropy",
                    "Bounding-box overlap only",
                ],
                "correct": 0,
                "explanation": (
                    "Multi-Otsu selects multiple thresholds that maximize separability among intensity classes."
                ),
            },

            {
                "id": "M10.L01.Q03",
                "section_id": "watershed-morphology",
                "question": "Why are marker seeds useful in watershed segmentation?",
                "options": [
                    "They control where flooding regions begin and reduce uncontrolled over-segmentation",
                    "They convert RGB to grayscale",
                    "They create transformer tokens",
                    "They remove the need for a gradient/topographic surface",
                ],
                "correct": 0,
                "explanation": (
                    "Marker-controlled watershed constrains basin growth using selected object/background seeds."
                ),
            },

            {
                "id": "M10.L01.Q04",
                "section_id": "watershed-morphology",
                "question": "Why is the distance transform useful for separating touching objects?",
                "options": [
                    "Interior peaks can provide approximate object-center markers for watershed",
                    "It directly predicts semantic classes",
                    "It performs graph-cut optimization",
                    "It replaces morphology with a CNN",
                ],
                "correct": 0,
                "explanation": (
                    "Thick object interiors are farther from the background, so distance maxima provide useful seeds."
                ),
            },

            {
                "id": "M10.L01.Q05",
                "section_id": "superpixels-rag",
                "question": "What is the main role of a Region Adjacency Graph after superpixelization?",
                "options": [
                    "Represent neighboring regions so similar adjacent superpixels can be merged",
                    "Convert masks into object queries",
                    "Perform image classification",
                    "Generate a Fourier transform",
                ],
                "correct": 0,
                "explanation": (
                    "RAG nodes represent regions and edges represent adjacency/dissimilarity relationships."
                ),
            },

            {
                "id": "M10.L01.Q06",
                "section_id": "variational-segmentation",
                "question": "Why can Chan–Vese work when object boundaries are weak?",
                "options": [
                    "It primarily models region statistics and contour regularity rather than requiring strong gradients",
                    "It ignores image intensities entirely",
                    "It requires pretrained transformer weights",
                    "It only works on binary images",
                ],
                "correct": 0,
                "explanation": (
                    "Chan–Vese is a region-based active-contour model."
                ),
            },

            {
                "id": "M10.L01.Q07",
                "section_id": "grabcut-crf",
                "question": "What two major ingredients does GrabCut combine?",
                "options": [
                    "Foreground/background appearance models and graph-cut energy minimization",
                    "Fourier filtering and histogram equalization",
                    "Object queries and self-attention",
                    "SLIC and DDIM inversion",
                ],
                "correct": 0,
                "explanation": (
                    "GrabCut uses GMM appearance modeling plus graph optimization."
                ),
            },

            {
                "id": "M10.L01.Q08",
                "section_id": "grabcut-crf",
                "question": "What does the bilateral pairwise term in a dense CRF encourage?",
                "options": [
                    "Nearby pixels with similar appearance should prefer consistent labels while respecting edges",
                    "Every pixel should have the same label",
                    "Only distant pixels should interact",
                    "All masks should become rectangular",
                ],
                "correct": 0,
                "explanation": (
                    "The bilateral term combines spatial proximity and appearance similarity."
                ),
            },

            {
                "id": "M10.L01.Q09",
                "section_id": "classical-learning-ensemble",
                "question": "What makes Random-Forest segmentation supervised?",
                "options": [
                    "The classifier learns pixel-label decisions from annotated feature vectors",
                    "SLIC automatically provides semantic ground truth",
                    "It contains a pretrained transformer",
                    "It does not use any labels",
                ],
                "correct": 0,
                "explanation": (
                    "Engineered features are fixed, but the Random Forest learns from labeled pixels."
                ),
            },

            {
                "id": "M10.L01.Q10",
                "section_id": "deep-segmentation-paradigms",
                "question": "What is the defining idea of a fully convolutional network for segmentation?",
                "options": [
                    "Preserve spatial feature maps and produce dense class-score maps without a fully connected image-level head",
                    "Replace every pixel with a graph node only",
                    "Use only thresholding",
                    "Predict one class for the whole image",
                ],
                "correct": 0,
                "explanation": (
                    "FCNs transform spatial features directly into pixel-wise score maps."
                ),
            },

            {
                "id": "M10.L01.Q11",
                "section_id": "deeplab-ensemble",
                "question": "What is the purpose of ASPP in DeepLab?",
                "options": [
                    "Capture context at multiple dilation scales",
                    "Separate individual instances with object IDs",
                    "Perform GrabCut initialization",
                    "Create a region adjacency graph",
                ],
                "correct": 0,
                "explanation": (
                    "ASPP combines atrous convolutions at several rates to model multiscale context."
                ),
            },

            {
                "id": "M10.L01.Q12",
                "section_id": "instance-maskrcnn-yolo",
                "question": "Why is ROIAlign important in Mask R-CNN?",
                "options": [
                    "It preserves spatial alignment for accurate instance-mask prediction",
                    "It turns instance segmentation into classification",
                    "It computes Multi-Otsu thresholds",
                    "It removes the Region Proposal Network",
                ],
                "correct": 0,
                "explanation": (
                    "ROIAlign avoids coarse quantization that would misalign mask features with the source object."
                ),
            },

            {
                "id": "M10.L01.Q13",
                "section_id": "instance-maskrcnn-yolo",
                "question": "What is a key reason YOLO-style segmentation can support real-time use?",
                "options": [
                    "It uses a single-stage prediction design optimized for one-pass inference",
                    "It uses no learned weights",
                    "It requires multiple graph-cut iterations",
                    "It is only a thresholding method",
                ],
                "correct": 0,
                "explanation": (
                    "The source contrasts YOLO's single-stage design with slower two-stage instance methods."
                ),
            },

            {
                "id": "M10.L01.Q14",
                "section_id": "transformer-foundations",
                "question": "In self-attention, what does a Query represent conceptually?",
                "options": [
                    "What a token is looking for in other tokens",
                    "The final segmentation mask",
                    "The image histogram",
                    "A connected-component ID",
                ],
                "correct": 0,
                "explanation": (
                    "The source uses the intuition: Query asks what information is relevant."
                ),
            },

            {
                "id": "M10.L01.Q15",
                "section_id": "setr-dpt",
                "question": "What key improvement does DPT add over a minimal pure-ViT dense predictor such as SETR?",
                "options": [
                    "Multi-scale feature fusion from different transformer depths",
                    "Otsu threshold optimization",
                    "Graph cuts",
                    "A point-spread function",
                ],
                "correct": 0,
                "explanation": (
                    "DPT fuses features at different depths to recover both detail and semantics."
                ),
            },

            {
                "id": "M10.L01.Q16",
                "section_id": "detr-segformer",
                "question": "What distinguishes SegFormer from DETR in the chapter's framing?",
                "options": [
                    "SegFormer is hierarchical dense prediction, while DETR is query/object-centric",
                    "SegFormer is a thresholding method",
                    "DETR is purely a Random Forest",
                    "They use exactly the same output representation",
                ],
                "correct": 0,
                "explanation": (
                    "The source presents two different transformer philosophies: dense hierarchy versus query-based set prediction."
                ),
            },

            {
                "id": "M10.L01.Q17",
                "section_id": "mask2former-oneformer",
                "question": "What does Mask2Former predict instead of only independent pixel classes?",
                "options": [
                    "Mask–class pairs",
                    "Only global image labels",
                    "Only bounding-box widths",
                    "Only histogram bins",
                ],
                "correct": 0,
                "explanation": (
                    "Mask2Former treats segmentation as mask classification/set prediction."
                ),
            },

            {
                "id": "M10.L01.Q18",
                "section_id": "method-selection",
                "type": "open",
                "question": (
                    "You need to solve six tasks: separate three intensity bands in a "
                    "microscopy image, split touching circular objects, interactively extract "
                    "one foreground object, label every road-scene pixel semantically, "
                    "separate individual people in real time, and produce a complete "
                    "thing/stuff scene representation. Choose one method or model family from "
                    "this lesson for each task and justify every choice using the assumptions "
                    "and output type of the selected method."
                ),
            },
        ],

        "passing_score": 70,
    },
}
