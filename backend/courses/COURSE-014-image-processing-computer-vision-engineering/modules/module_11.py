"""M11.L01 — More Deep Learning Methods for Image Segmentation.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 11. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M11.L01"

MODULE_ORDER = 11

MODULE_TITLE = "More Deep Learning Methods for Image Segmentation"

MODULE_DESCRIPTION = (
    "Extend segmentation from fixed-label models to promptable and text-guided systems, "
    "semantic 3D understanding, real-world deployment, custom U-Net training, medical "
    "and volumetric segmentation, remote-sensing segmentation, and rigorous evaluation "
    "with IoU, Dice, pixel accuracy, and mAP."
)

SOURCE_CHAPTER = 11

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


TOPIC = {
    "title": "More Deep Learning Methods for Image Segmentation",

    "slug": "image-processing-m11-l01",

    "description": (
        "A source-aligned lesson on promptable foundation models such as SAM, "
        "vision-language segmentation with MaskCLIP and CLIPSeg, monocular depth and "
        "semantic 3D reconstruction, production segmentation workflows, training U-Net "
        "models, medical and volumetric segmentation, remote-sensing MAnet pipelines, "
        "and segmentation evaluation metrics."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 7.0,

    "skill_tags": [
        "image-segmentation",
        "sam",
        "foundation-models",
        "maskclip",
        "clipseg",
        "vision-language",
        "open-vocabulary-segmentation",
        "monocular-depth",
        "point-clouds",
        "semantic-3d",
        "mediapipe",
        "detectron2",
        "unet",
        "transfer-learning",
        "medical-segmentation",
        "swin-unetr",
        "monai",
        "remote-sensing",
        "manet",
        "iou",
        "dice",
        "map",
        "module-11",
    ],

    "prerequisite_ids": ["M10.L01"],

    "lesson": {
        "title": "More Deep Learning Methods for Image Segmentation",

        "content": r"""
# More Deep Learning Methods for Image Segmentation

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M11.L01  
> **Module:** More Deep Learning Methods for Image Segmentation  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 11. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain how promptable segmentation differs from fixed-label segmentation.
- Describe SAM as an image encoder + prompt encoder + mask decoder system.
- Explain how language-aligned segmentation connects image and text embeddings.
- Use the mental model behind MaskCLIP and CLIPSeg for open-vocabulary/text-guided masks.
- Explain how monocular depth estimation converts RGB images into dense geometric cues.
- Explain how depth plus camera intrinsics creates a 3D point cloud.
- Explain semantic 3D fusion by combining depth and segmentation.
- Describe practical segmentation deployment with MediaPipe/TFLite and Detectron2.
- Explain the U-Net encoder-decoder architecture and the purpose of skip connections.
- Describe a custom segmentation training pipeline from data loading through evaluation.
- Explain transfer learning with pretrained encoders.
- Explain why Dice-based losses are useful for small or imbalanced foreground regions.
- Describe 3D medical segmentation with Swin-UNETR and sliding-window inference.
- Explain how volumetric masks become 3D meshes using marching cubes.
- Explain the remote-sensing challenges of huge imagery, class imbalance, and sensor variation.
- Describe patch-based training, mask encoding, class balancing, attention, and tiled inference for satellite images.
- Compute and interpret IoU, Dice, pixel accuracy, precision, recall, AP, and mAP.
- Select segmentation metrics according to semantic, medical, remote-sensing, or instance-segmentation tasks.

---

## 1. From fixed-label segmentation to promptable segmentation

A conventional semantic model is trained to map:

```text
image -> dense label map
```

for a fixed set of classes.

Promptable segmentation changes the problem:

```text
(image, prompt) -> mask
```

The prompt can be:

- a positive or negative point,
- a bounding box,
- a rough mask,
- a text description, depending on the model.

This changes segmentation from:

```text
"Which predefined class is each pixel?"
```

to:

```text
"Which region matches this user/model request?"
```

The source chapter emphasizes:

- interactivity,
- zero-shot behavior,
- generalization,
- reduced need to retrain for every individual object category.

[[IMAGE_NEEDED: Fixed-label versus promptable segmentation | Show left: image entering a fixed-class semantic model producing a predefined class map; right: the same image plus point/box/text prompts entering a prompt-conditioned model producing different masks | Learner should understand that the prompt changes the requested segmentation without retraining]]

---

## 2. Segment Anything Model (SAM)

SAM is presented as a prompt-driven segmentation foundation model.

Its conceptual architecture has three main parts:

```text
image
  ↓
image encoder
  ↓
image embedding
        \
prompt -> prompt encoder
          \
        mask decoder
             ↓
          masks
```

### Image encoder

The image is transformed into a reusable visual representation.

This is computationally expensive, but once the image embedding is computed, several prompts can be evaluated efficiently.

### Prompt encoder

The prompt is encoded into a representation describing what region the user wants.

Prompt examples include:

- points,
- boxes,
- masks.

### Mask decoder

The decoder combines:

```text
image features + prompt features
```

to predict a binary mask and quality/confidence-related outputs.

### Automatic mask generation

The source also demonstrates automatic segmentation by sampling many prompt points over the image.

A simplified workflow is:

```python
generator = SamAutomaticMaskGenerator(
    sam,
    points_per_side=16,
    pred_iou_thresh=0.88,
    stability_score_thresh=0.92,
)

masks = generator.generate(image_rgb)
```

Candidate masks can contain information such as:

- segmentation,
- area,
- confidence/quality estimates.

[[IMAGE_NEEDED: SAM architecture and prompt types | Show image encoder producing reusable embedding, prompt encoder receiving a point and box, mask decoder, and several candidate masks with quality scores | Learner should understand why the same image representation can answer different segmentation prompts]]

### Practical optimization

The source recommends ideas such as:

- resizing very large images,
- GPU inference,
- FP16/autocast,
- mask filtering.

These are engineering optimizations rather than changes to the segmentation concept.

### SAM plus vision-language understanding

The chapter isolates a segmented object and passes it to a vision-language model.

Conceptually:

```text
SAM
-> segment object

crop / masked object
-> vision-language model

vision + language
-> description
```

This creates a:

```text
Segment -> Understand -> Describe
```

pipeline.

The important lesson is that segmentation can become one tool inside a larger multimodal system.

---

## 3. MaskCLIP, CLIP alignment, and open-vocabulary segmentation

CLIP-style systems learn a shared embedding space for:

- images,
- text.

Matching image-text pairs are encouraged to have similar embeddings.

This enables zero-shot semantic matching.

### Dense language alignment

MaskCLIP-style segmentation extends this idea from one global image embedding toward:

- pixel embeddings,
- region embeddings,
- mask embeddings.

Then segmentation can be driven by similarity to text.

Conceptually:

```text
image region embedding
          ↘
        similarity -> semantic match
          ↗
text embedding
```

Instead of requiring one learned output neuron for every possible class, the model can reason about a text concept.

### Open-vocabulary segmentation

The central benefit is:

> Labels do not have to be limited to a small fixed class list defined during one segmentation training run.

A user can request concepts through language.

[[IMAGE_NEEDED: Language-aligned segmentation | Show image regions encoded into visual embeddings, text prompts such as "car", "person", "water" encoded into text embeddings, cosine-similarity matching, and resulting masks | Learner should see how text replaces a fixed output-class list]]

### Source implementation note

The source discusses MaskCLIP conceptually and demonstrates related universal segmentation with Mask2Former components.

The transferable idea is the **vision-language alignment**, not one specific wrapper API.

---

## 4. CLIPSeg and interactive text-to-mask segmentation

CLIPSeg turns a text prompt directly into a dense relevance mask.

The task is:

```text
(image, text prompt)
    ↓
pixel-wise relevance logits
    ↓ sigmoid
probability mask
```

Example prompt:

```text
"car"
```

The model predicts how strongly each pixel belongs to that concept.

A source-aligned workflow is:

```python
inputs = processor(
    text=prompt,
    images=image,
    return_tensors="pt",
)

with torch.no_grad():
    outputs = model(**inputs)

mask = torch.sigmoid(
    outputs.logits
)
```

The mask is then resized to the original image resolution.

### Thresholding probability

A probability map becomes a binary mask using a threshold:

```text
p > 0.5 -> foreground
p <= 0.5 -> background
```

Changing the threshold changes precision/recall behavior.

### Interactive Gradio app

The source wraps the model in a Gradio UI:

```text
upload image
+
enter prompt
    ↓
CLIPSeg
    ↓
mask + overlay
```

This is a useful product pattern because it exposes semantic segmentation through natural language.

[[IMAGE_NEEDED: CLIPSeg interactive pipeline | Show image + text prompt entering a shared vision-language encoder/decoder, a soft probability heatmap, thresholded binary mask, and colored overlay | Learner should distinguish logits/probabilities from the final thresholded mask]]

{{exercise:M11.L01.EX01}}

---

## 5. Monocular depth estimation with DPT

The chapter then extends segmentation toward 3D scene understanding.

A single RGB image contains no explicit depth measurement.

Monocular depth estimation predicts:

```text
image -> dense depth map
```

where each pixel receives an estimated depth-like value.

### Why this is difficult

The problem is ill-posed.

Different 3D scenes can project to similar 2D images.

Modern models learn geometric cues such as:

- perspective,
- texture gradients,
- relative object size,
- occlusion,
- shadows,
- semantic context.

### DPT

The source uses a pretrained Dense Prediction Transformer.

Conceptually:

```text
RGB image
  ↓ transformer feature extraction
global + multiscale reasoning
  ↓ dense decoder
depth map
```

The predicted low-resolution depth is upsampled to the original image size for visualization.

### Relative versus metric meaning

The source visualization normalizes values for display.

Therefore, a bright/dark map can represent relative depth ordering without automatically providing calibrated metric distance in meters.

[[IMAGE_NEEDED: Monocular depth with DPT | Show RGB scene, transformer/DPT block, dense depth prediction, and normalized heatmap with nearby and distant regions labeled | Learner should understand depth as a dense geometric prediction derived from monocular visual cues]]

---

## 6. From depth to point clouds and semantic 3D

Once depth is available, each image pixel can be projected into 3D.

For pixel `(x, y)` with depth `z` and camera intrinsics:

```text
X = (x - cx) * z / fx
Y = (y - cy) * z / fy
Z = z
```

where:

- `fx`, `fy` are focal lengths,
- `cx`, `cy` are principal-point coordinates.

This produces:

```text
pixel + depth -> 3D point
```

### Point cloud

A point cloud is a set:

```text
{(X, Y, Z, color)}
```

for many image pixels.

The source uses Open3D structures and demonstrates:

- point-cloud creation,
- multi-view fusion,
- voxel downsampling,
- normal estimation,
- interactive 3D visualization.

[[IMAGE_NEEDED: Depth to point-cloud projection | Show image pixel (x,y), camera intrinsic model, depth z, back-projection ray, resulting XYZ point, and a colored point cloud reconstructed from all pixels | Learner should connect the depth map with actual 3D geometry]]

### Semantic 3D fusion

Depth gives geometry.

Semantic segmentation gives meaning.

Combining them gives:

```text
(X, Y, Z, class)
```

The chapter uses SegFormer to obtain a semantic label map and projects those labels into the point cloud.

Result:

```text
RGB image
   ├─> depth
   └─> semantic segmentation
          ↓
3D projection
          ↓
semantic point cloud
```

This supports applications such as:

- robotics,
- autonomous navigation,
- AR/VR,
- scene mapping,
- digital twins.

### Important calibration note

The source example uses approximate intrinsics in its demonstration.

Accurate metric reconstruction requires correctly calibrated camera parameters and consistent depth scale.

---

## 7. Practical segmentation applications: MediaPipe and Detectron2

Segmentation becomes valuable when embedded into real workflows.

### Background blur with MediaPipe + DeepLabV3 TFLite

The chapter demonstrates a portrait-style pipeline:

```text
image
  ↓ lightweight segmentation
foreground/background mask
  ↓
blur original image
  ↓
combine:
foreground from original
background from blurred version
```

A simple formula is:

```text
output =
mask * original
+
(1 - mask) * blurred
```

This resembles:

- video-call background blur,
- AR effects,
- mobile portrait processing.

### Why TFLite/MediaPipe?

The source emphasizes:

- real-time behavior,
- edge/mobile deployment,
- lightweight execution.

[[IMAGE_NEEDED: Real-time background blur | Show original portrait, semantic foreground mask, strongly blurred full image, and final composite with sharp foreground + blurred background | Learner should see segmentation as an enabling component inside an application]]

### Detectron2

Detectron2 provides a production/research framework for:

- instance segmentation,
- semantic segmentation,
- panoptic segmentation.

The source demonstrates:

- Mask R-CNN for instances,
- Panoptic FPN,
- semantic labels derived from panoptic outputs,
- standard visualizers and model-zoo checkpoints.

The key engineering lesson is:

> A framework integrates preprocessing, model configuration, inference, and postprocessing so the developer can focus on task-specific system behavior.

---

## 8. Training a custom U-Net

Pretrained generic segmentation models are not always enough.

Custom training becomes important when the domain differs from common datasets.

Examples from the chapter include:

- autonomous driving,
- medical imaging,
- satellite imagery.

### U-Net architecture

U-Net has:

```text
encoder
   ↓
bottleneck
   ↓
decoder
```

with skip connections linking matching resolutions.

### Encoder

The encoder repeatedly applies:

- convolutions,
- nonlinear activation,
- downsampling.

As depth increases:

```text
spatial resolution decreases
semantic abstraction increases
```

### Decoder

The decoder upsamples features back toward the original resolution.

### Skip connections

Skip connections send fine spatial information from encoder stages directly to corresponding decoder stages.

This solves an important dense-prediction problem:

```text
deep layers know WHAT
shallow layers know WHERE
```

[[IMAGE_NEEDED: U-Net architecture | Show contracting encoder, bottleneck, expanding decoder, skip connections at matching scales, and final 1×1 pixel-classification layer | Learner should understand how U-Net combines semantic context and boundary detail]]

### Final classifier

A `1×1` convolution converts decoder features into:

```text
C class logits per pixel
```

Then:

```text
argmax(logits) -> predicted class
```

for multiclass segmentation.

---

## 9. Data pipelines, loss, training, and transfer learning

A complete segmentation project involves much more than defining a network.

### Dataset pipeline

The chapter's driving-scene example includes:

- image paths,
- mask paths,
- image/mask resizing,
- normalization,
- batching,
- caching,
- prefetching.

A critical detail:

> Masks should be resized with nearest-neighbor interpolation when they contain class IDs.

Ordinary bilinear interpolation can invent invalid intermediate label values.

### Training loop

For every batch:

```text
image
  ↓ model
logits
  ↓ loss versus mask
gradient
  ↓ optimizer update
```

The custom Keras U-Net uses categorical-style pixel loss and tracks Mean IoU.

### Transfer learning

The chapter then uses a U-Net with a ResNet encoder.

A pretrained encoder provides features learned from a large dataset.

Benefits can include:

- faster convergence,
- stronger low-level feature extraction,
- improved performance with limited labeled data.

### SMP-style production pipeline

The source demonstrates `segmentation_models_pytorch` with:

- PyTorch Dataset,
- DataLoader,
- augmentation,
- U-Net,
- CrossEntropyLoss,
- optimizer,
- IoU/Dice-style metrics,
- model saving.

[[IMAGE_NEEDED: Segmentation training pipeline | Show image/mask dataset → augmentation → batching → encoder-decoder network → logits → segmentation loss → backpropagation → validation metrics → saved model | Learner should see segmentation training as an end-to-end data/model/evaluation system]]

### Reported metric caution

The source gives example training/test metric values for its specific setup.

Treat those as results for that experiment, not universal expected performance for U-Net.

---

## 10. Brain-tumor MRI segmentation

Medical segmentation is especially sensitive to boundary quality.

A small geometric error can matter more than it would in a casual photographic task.

The source trains a U-Net with:

- ResNet34 encoder,
- binary tumor mask,
- sigmoid output,
- pretrained ImageNet encoder weights.

### Binary segmentation

For one foreground class:

```text
output probability p(x,y)
```

Then:

```text
p > threshold -> tumor
else          -> background
```

### Class imbalance

Tumor pixels can occupy a small fraction of the image.

Pixel accuracy alone can therefore be misleading.

The chapter combines:

```text
Binary Cross-Entropy
+
Dice loss
```

to balance:

- per-pixel classification,
- region overlap.

[[IMAGE_NEEDED: Brain tumor MRI segmentation | Show MRI slice, ground-truth tumor mask, predicted probability heatmap, thresholded binary prediction, and colored overlay | Learner should see why overlap-based loss/metrics matter for small medical regions]]

### Training controls

The source also uses training practices such as:

- ModelCheckpoint,
- validation metrics,
- learning-rate reduction,
- early stopping.

These are important because medical datasets can be small and overfitting is a serious risk.

---

## 11. 3D CT segmentation with Swin-UNETR

2D medical segmentation processes slices.

3D segmentation processes entire volumetric structure.

A CT scan can be represented as:

```text
H × W × D
```

where `D` is depth across slices.

### Why 3D context matters

An organ is not a collection of unrelated 2D slices.

Its shape extends across the volume.

A 3D model can reason about:

- continuity,
- anatomical shape,
- neighboring slices,
- long-range volumetric context.

### Swin-UNETR

The chapter uses Swin-UNETR.

It combines:

- hierarchical Swin Transformer encoder,
- shifted-window self-attention,
- U-Net-style decoder,
- multiscale skip connections.

Interpretation:

```text
Swin Transformer
-> long-range / hierarchical context

U-Net decoder
-> spatial reconstruction

skip connections
-> preserve localization
```

[[IMAGE_NEEDED: Swin-UNETR volumetric segmentation | Show 3D CT volume entering shifted-window Swin encoder stages, U-Net decoder with skips, and 3D multi-organ label volume | Learner should understand how transformer context and U-Net localization are combined in 3D]]

### Medical preprocessing

The source pipeline includes:

- NIfTI loading,
- channel setup,
- orientation normalization,
- voxel spacing/resampling,
- Hounsfield-unit intensity scaling,
- padding for architecture compatibility.

This matters because medical volumes must be geometrically standardized before inference.

### Sliding-window inference

A complete CT volume may not fit in GPU memory.

The chapter uses overlapping 3D windows:

```text
full volume
  ↓ split into overlapping cubes
model inference per cube
  ↓ merge predictions
full segmentation
```

This is a general strategy for large volumetric data.

---

## 12. From 3D masks to anatomical visualization

A voxel segmentation map is useful computationally, but 3D visualization makes structure easier to inspect.

### Marching cubes

Given a binary organ mask:

```text
voxels
  ↓ isosurface extraction
vertices + faces
  ↓
polygon mesh
```

The source uses `measure.marching_cubes()`.

### Vedo

The chapter constructs individual organ meshes and gives each:

- color,
- transparency,
- label.

It then displays:

- CT volume,
- segmentation meshes.

### VTK volume rendering

VTK provides volumetric rendering.

Important concepts include:

- volume data,
- opacity transfer function,
- color transfer function,
- interactive camera movement.

[[IMAGE_NEEDED: CT mask to 3D mesh | Show axial CT slices and voxel segmentation feeding marching cubes, resulting liver/organ mesh, then combined 3D volume + colored organ meshes | Learner should understand that segmentation can become patient-specific 3D geometry]]

### Applications

The source connects 3D segmentation to:

- organ volume estimation,
- surgical planning,
- radiotherapy,
- navigation,
- anatomical modeling,
- digital twins.

---

## 13. Remote sensing with Mixed-Attention U-Net

Satellite segmentation introduces a different set of challenges.

### Challenge 1: huge images

Satellite scenes can be thousands of pixels wide/high.

Training on the entire image can exceed memory limits.

### Challenge 2: severe class imbalance

Examples:

```text
vegetation/background -> huge area
road/river            -> very small area
```

Ordinary average cross-entropy can be dominated by frequent classes.

### Challenge 3: multi-source variability

The same land-cover class can look different because of:

- different satellites,
- sensors,
- altitude,
- season,
- weather,
- atmosphere,
- acquisition time.

[[IMAGE_NEEDED: Remote sensing segmentation challenges | Show large satellite image with tiled grid, class-frequency bar chart with rare roads/water, and same land-cover class under several sensor/season appearances | Learner should understand why patching, class weighting, augmentation, and attention are useful]]

### Patch-based training

Large images are divided into patches such as:

```text
512 × 512
```

Benefits:

- lower GPU memory,
- more training samples,
- easier batching,
- stochastic diversity.

### Color mask encoding

Some satellite datasets store labels as RGB colors.

Example:

```text
green -> vegetation
red   -> buildings
blue  -> water
```

Before training:

```text
RGB mask -> integer class map
```

### Class balancing

The source uses median-frequency balancing:

```text
class_weight
≈ median_frequency / class_frequency
```

Rare classes get larger weights.

### Data augmentation

The chapter uses transformations such as:

- horizontal flip,
- vertical flip,
- 90° rotation,
- brightness/contrast variation.

These fit remote-sensing imagery well because many land-cover classes are orientation invariant.

---

## 14. MAnet, attention, and tiled full-image inference

The source uses Mixed-Attention U-Net (MAnet) from `segmentation_models_pytorch`.

Its high-level structure contains:

- ResNet34 encoder,
- U-Net-like decoder,
- attention mechanisms.

### Why attention helps

Satellite scenes contain structures at very different scales.

Attention can adaptively emphasize:

- useful channels,
- useful spatial regions,
- context needed to separate visually similar classes.

### Loss design

The source combines:

```text
weighted Cross-Entropy
+
Dice-style objective
```

This addresses:

- pixel classification,
- overlap,
- imbalance.

### Full-image tiled inference

Training uses patches.

At inference time, the full large image is:

1. padded to a compatible size,
2. divided into tiles,
3. predicted tile by tile,
4. stitched back together,
5. cropped to original size.

Conceptually:

```text
large image
→ tiles
→ model each tile
→ stitch labels
→ full segmentation
```

[[IMAGE_NEEDED: Satellite tiled inference | Show very large satellite image split into patches, MAnet processing each patch, predicted tiles, stitching/reconstruction, and final full-resolution land-cover map | Learner should understand how models trained on patches can segment images too large for one GPU pass]]

### Qualitative inspection still matters

Even if a Dice score looks good, inspect:

- thin roads,
- coastline boundaries,
- small buildings,
- patch seams,
- rare classes.

Metrics and visual error analysis complement each other.

---

## 15. IoU and Dice: measuring mask overlap

Before choosing a metric, define:

- `TP` — correctly predicted foreground,
- `FP` — false foreground,
- `FN` — missed foreground,
- `TN` — correctly predicted background.

### Intersection over Union

IoU measures:

```text
intersection
------------
union
```

For binary segmentation:

```text
IoU =
TP / (TP + FP + FN)
```

Interpretation:

```text
1 -> perfect overlap
0 -> no overlap
```

For multiclass segmentation:

1. compute IoU per class,
2. average across classes.

This produces mean IoU (mIoU).

### Dice coefficient

Dice is:

```text
Dice =
2 * TP / (2*TP + FP + FN)
```

It also ranges from `0` to `1`.

Dice and IoU are closely related.

Both measure region overlap, but Dice places somewhat more relative emphasis on overlap and is widely used for small medical structures.

[[IMAGE_NEEDED: IoU versus Dice geometry | Show ground-truth and predicted binary masks with intersection/union regions highlighted, plus formulas for IoU and Dice | Learner should understand both metrics from set overlap rather than memorizing equations only]]

### Dice loss

A differentiable soft Dice formulation can be optimized directly.

This is especially useful when:

- foreground is small,
- class imbalance is severe.

---

## 16. Pixel accuracy, precision/recall, AP, and mAP

### Pixel accuracy

Pixel accuracy is:

```text
correct pixels / all pixels
```

For binary segmentation:

```text
(TP + TN)
--------------------
TP + TN + FP + FN
```

### Why accuracy can fail

Suppose only 1% of pixels are tumor.

A model that predicts:

```text
background everywhere
```

may achieve approximately:

```text
99% pixel accuracy
```

while completely failing the task.

So pixel accuracy should not be used alone for heavily imbalanced segmentation.

### Precision and recall

For an object/instance prediction:

```text
precision =
TP / (TP + FP)

recall =
TP / (TP + FN)
```

Precision asks:

> Of what I predicted, how much was correct?

Recall asks:

> Of what truly exists, how much did I find?

### Average Precision

Across confidence thresholds, the model produces a precision-recall curve.

AP summarizes that curve for one class.

### Mean Average Precision

mAP averages AP across classes.

COCO-style evaluation also averages across multiple IoU thresholds, creating a stricter instance-segmentation evaluation.

[[IMAGE_NEEDED: Segmentation metric selection | Show four panels: IoU/Dice overlap for semantic masks, class-imbalance example exposing accuracy weakness, precision-recall curve and AP area, and instance masks evaluated across IoU thresholds for mAP | Learner should know which metric matches which segmentation problem]]

### Metric-to-domain mapping from the source

```text
medical imaging
-> Dice + IoU

autonomous driving semantic segmentation
-> mIoU

remote sensing
-> IoU + F1/Dice-style overlap

instance segmentation
-> mAP
```

### Use multiple metrics

No single number tells the whole story.

A strong evaluation often includes:

- class-wise scores,
- aggregate scores,
- visual inspection,
- boundary errors,
- rare-class performance,
- runtime/resource cost.

{{exercise:M11.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Promptable segmentation means the model never needs image features.

### Why this is wrong

Promptable systems combine a visual representation with a prompt representation; the prompt tells the model what to extract.

### Misconception 2

> SAM automatically assigns semantic names to every mask.

### Why this is wrong

SAM primarily produces object/region masks from prompts or automatic mask generation. Semantic naming requires an additional classifier or vision-language step.

### Misconception 3

> Open-vocabulary segmentation means the model understands every possible text phrase perfectly.

### Why this is wrong

Language alignment expands flexibility, but quality still depends on training, visual ambiguity, prompt wording, and model capacity.

### Misconception 4

> A monocular depth map automatically gives exact metric 3D geometry.

### Why this is wrong

The source example normalizes predicted depth for visualization, and accurate metric reconstruction also depends on correct camera intrinsics and calibrated depth scale.

### Misconception 5

> U-Net skip connections simply make the network deeper.

### Why this is wrong

Their main purpose is to transfer spatial detail from encoder stages into decoder reconstruction.

### Misconception 6

> Bilinear resizing is always safe for segmentation masks.

### Why this is wrong

Interpolating categorical class IDs can create invalid intermediate labels; nearest-neighbor interpolation is appropriate for discrete masks.

### Misconception 7

> High pixel accuracy guarantees useful medical segmentation.

### Why this is wrong

A dominant background class can produce high accuracy even when the foreground object is never detected.

### Misconception 8

> A 3D segmentation model is equivalent to applying a 2D model independently to every slice.

### Why this is wrong

A volumetric model can exploit cross-slice and long-range 3D context.

### Misconception 9

> Patch-based satellite training means the final system can only predict small patches.

### Why this is wrong

The source reconstructs full-image output through tiled inference and stitching.

### Misconception 10

> IoU, Dice, and mAP measure exactly the same thing.

### Why this is wrong

IoU and Dice are overlap metrics for masks, while mAP additionally evaluates confidence-ranked instance localization/classification across IoU criteria.

---

## Key terminology

| Term | Meaning |
|---|---|
| Promptable segmentation | Segmentation conditioned on user/model prompts |
| Foundation model | Large pretrained model designed to generalize across many tasks/settings |
| SAM | Segment Anything Model |
| Prompt encoder | Component converting points/boxes/masks into prompt features |
| Mask decoder | Component combining image and prompt features to produce masks |
| Open-vocabulary segmentation | Segmentation driven by flexible language concepts rather than one fixed label set |
| CLIP | Contrastive image-text representation model |
| CLIPSeg | Text-conditioned pixel-level segmentation model |
| Monocular depth | Dense depth estimation from one RGB image |
| Point cloud | Set of 3D coordinates, optionally with color/semantic attributes |
| Camera intrinsics | Parameters mapping camera pixels to viewing rays |
| Semantic point cloud | 3D points augmented with semantic labels |
| TFLite | TensorFlow Lite deployment format/runtime |
| Detectron2 | Framework for detection and segmentation research/deployment |
| U-Net | Encoder-decoder segmentation architecture with skip connections |
| Transfer learning | Reusing pretrained features for a new domain/task |
| Logit | Unnormalized model score before softmax/sigmoid |
| Swin-UNETR | 3D segmentation model combining Swin Transformer and U-Net-style decoding |
| Sliding-window inference | Overlapping patch inference over a large 2D/3D input |
| Marching cubes | Surface extraction from volumetric masks |
| MAnet | Mixed-Attention U-Net-style segmentation model |
| Class weighting | Increasing/decreasing loss contribution by class frequency |
| Tiled inference | Patch-wise prediction followed by full-image reconstruction |
| IoU | Intersection over Union |
| mIoU | Mean IoU across classes |
| Dice coefficient | Overlap similarity measure |
| Pixel accuracy | Fraction of correctly classified pixels |
| Precision | Fraction of predicted positives that are correct |
| Recall | Fraction of true positives that are detected |
| AP | Area under a precision-recall curve for a class |
| mAP | Mean Average Precision across classes and/or IoU thresholds |

---

## Self-check

Before continuing, make sure you can answer:

1. How does promptable segmentation differ from fixed-class semantic segmentation?
2. What are SAM's three main architectural components?
3. Why can one SAM image embedding support several prompts?
4. Why does automatic mask generation need filtering?
5. What role can a vision-language model play after SAM?
6. What does it mean for image and text representations to share an embedding space?
7. Why is text-guided segmentation considered open-vocabulary?
8. What does sigmoid do to CLIPSeg logits?
9. How does the mask threshold affect output?
10. Why is monocular depth an ill-posed problem?
11. What cues can a learned model use to infer depth?
12. How does camera geometry convert `(x,y,z)` into `X,Y,Z`?
13. What extra information turns a point cloud into a semantic point cloud?
14. Why is calibration important for metric 3D reconstruction?
15. How does a segmentation mask create background blur?
16. Why is TFLite suitable for edge/mobile applications?
17. What problem does Detectron2 solve at the framework level?
18. What does the U-Net encoder learn?
19. What does the decoder reconstruct?
20. Why are skip connections important?
21. Why should class masks use nearest-neighbor resizing?
22. What is the advantage of a pretrained encoder?
23. Why can Dice loss help with small foreground objects?
24. What is the difference between binary sigmoid output and multiclass softmax output?
25. Why does 3D CT segmentation benefit from volumetric context?
26. What does shifted-window attention contribute to Swin-UNETR?
27. Why is sliding-window inference used for CT volumes?
28. What does marching cubes produce?
29. Why are satellite images often trained in patches?
30. Why does remote sensing suffer severe class imbalance?
31. What is median-frequency class balancing trying to achieve?
32. Why are flips/rotations especially natural augmentations for satellite images?
33. What does attention contribute in MAnet?
34. How are patch predictions reconstructed into a full satellite mask?
35. What do TP, FP, FN, and TN mean for segmentation?
36. What is IoU measuring?
37. What is Dice measuring?
38. Why can pixel accuracy hide complete foreground failure?
39. What is the difference between precision and recall?
40. What does AP summarize?
41. Why does COCO-style mAP average across several IoU thresholds?
42. Which metrics would you choose for tumor segmentation?
43. Which metric family would you choose for instance segmentation?
44. Why should visual inspection still accompany numerical metrics?

---

## Retain this idea

**Modern segmentation is no longer only about assigning one fixed class to every pixel. It can be promptable, language-guided, geometric, volumetric, domain-specific, and deployment-aware. The architecture matters, but so do the data pipeline, calibration, inference strategy, class imbalance, and evaluation metric chosen for the real problem.**
        """,

        "estimated_minutes": 420,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "promptable-segmentation", "title": "From Fixed-Label to Promptable Segmentation", "order": 1},
            {"id": "sam", "title": "Segment Anything Model (SAM)", "order": 2},
            {"id": "language-segmentation", "title": "MaskCLIP, CLIP Alignment, and Open-Vocabulary Segmentation", "order": 3},
            {"id": "clipseg", "title": "CLIPSeg and Interactive Text-to-Mask Segmentation", "order": 4},
            {"id": "monocular-depth", "title": "Monocular Depth Estimation with DPT", "order": 5},
            {"id": "pointcloud-semantic3d", "title": "From Depth to Point Clouds and Semantic 3D", "order": 6},
            {"id": "production-apps", "title": "Practical Segmentation Applications: MediaPipe and Detectron2", "order": 7},
            {"id": "unet-foundations", "title": "Training a Custom U-Net", "order": 8},
            {"id": "custom-training", "title": "Data Pipelines, Loss, Training, and Transfer Learning", "order": 9},
            {"id": "medical-mri", "title": "Brain-Tumor MRI Segmentation", "order": 10},
            {"id": "swin-unetr", "title": "3D CT Segmentation with Swin-UNETR", "order": 11},
            {"id": "volumetric-visualization", "title": "From 3D Masks to Anatomical Visualization", "order": 12},
            {"id": "remote-sensing", "title": "Remote Sensing with Mixed-Attention U-Net", "order": 13},
            {"id": "manet-tiled-inference", "title": "MAnet, Attention, and Tiled Full-Image Inference", "order": 14},
            {"id": "metrics-overlap", "title": "IoU and Dice: Measuring Mask Overlap", "order": 15},
            {"id": "metrics-accuracy-map", "title": "Pixel Accuracy, Precision/Recall, AP, and mAP", "order": 16},
        ],
    },

    "exercises": [
        {
            "id": "M11.L01.EX01",

            "title": "Build an Interactive Prompted Segmentation Demo",

            "lesson_code": "M11.L01",

            "section_id": "clipseg",

            "placement": "after_section",

            "description": (
                "Compare visual prompting and text prompting by building a small interactive "
                "segmentation workflow."
            ),

            "instructions": (
                "1. Choose one image containing at least three visually distinct objects.\n"
                "2. If SAM is available, segment at least one object using a point or bounding-box prompt.\n"
                "3. Run CLIPSeg with at least three text prompts referring to different image concepts.\n"
                "4. Keep the raw probability mask before thresholding for each CLIPSeg prompt.\n"
                "5. Compare threshold values such as 0.3, 0.5, and 0.7 and explain how the "
                "foreground region changes.\n"
                "6. Create an overlay for each final mask.\n"
                "7. Build a minimal Gradio or notebook UI that accepts an image and text prompt.\n"
                "8. If a vision-language model is available, pass one segmented crop to it and "
                "request a short description.\n"
                "9. Explain the difference between geometric prompting (point/box) and semantic "
                "prompting (text).\n"
                "10. Record one failure case caused by an ambiguous prompt or visually confusing object."
            ),

            "expected_output": (
                "A notebook or small app containing point/box or automatic SAM masks when "
                "available, several CLIPSeg text-conditioned probability/binary masks, "
                "threshold comparisons, overlays, and a short explanation of prompt behavior."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "sam",
                "clipseg",
                "promptable-segmentation",
                "vision-language",
                "mask-thresholding",
                "gradio",
                "interactive-vision",
            ],
        },

        {
            "id": "M11.L01.EX02",

            "title": "Design, Train, and Evaluate a Domain Segmentation Pipeline",

            "lesson_code": "M11.L01",

            "section_id": "metrics-accuracy-map",

            "placement": "after_section",

            "description": (
                "Connect architecture, data strategy, class imbalance, inference, and "
                "evaluation in one realistic segmentation-system design."
            ),

            "instructions": (
                "1. Choose one domain: road scenes, medical images, or remote sensing.\n"
                "2. Define the output as binary, multiclass semantic, instance, or 3D volumetric segmentation.\n"
                "3. Select an architecture from the chapter: U-Net, pretrained-encoder U-Net, "
                "Swin-UNETR, or MAnet, and justify the choice.\n"
                "4. Design the image/mask preprocessing pipeline, including interpolation rules for masks.\n"
                "5. Identify whether class imbalance is expected and select a loss strategy such as "
                "Cross-Entropy, weighted Cross-Entropy, BCE + Dice, or CE + Dice.\n"
                "6. If inputs are too large, specify patch/tile or sliding-window inference.\n"
                "7. Train or simulate the training loop and record at least one validation metric.\n"
                "8. Compute or explain IoU/mIoU, Dice/F1, pixel accuracy, and—if instance masks "
                "are involved—mAP.\n"
                "9. Construct an example where pixel accuracy looks good but foreground "
                "segmentation is poor.\n"
                "10. Finish with a deployment/evaluation checklist that includes visual error "
                "analysis, rare classes, boundary quality, memory, and runtime."
            ),

            "expected_output": (
                "A notebook/report specifying the full segmentation pipeline from data and "
                "architecture through training/inference and evaluation, including an "
                "imbalance strategy, metric table, and qualitative error analysis."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "unet",
                "transfer-learning",
                "medical-segmentation",
                "swin-unetr",
                "remote-sensing",
                "class-imbalance",
                "iou",
                "dice",
                "map",
                "system-design",
            ],
        },
    ],

    "quiz": {
        "id": "M11.L01.QZ01",

        "title": "More Deep Learning Methods for Image Segmentation — Knowledge Check",

        "lesson_code": "M11.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M11.L01.Q01",
                "section_id": "promptable-segmentation",
                "question": "What changes when segmentation becomes promptable?",
                "options": [
                    "The predicted mask is conditioned on both the image and an external prompt",
                    "The image is no longer used",
                    "All models become binary classifiers",
                    "No visual features are computed",
                ],
                "correct": 0,
                "explanation": (
                    "Promptable segmentation predicts a region conditioned jointly on image evidence and a prompt."
                ),
            },

            {
                "id": "M11.L01.Q02",
                "section_id": "sam",
                "question": "Which three components define the source's high-level SAM architecture?",
                "options": [
                    "Image encoder, prompt encoder, and mask decoder",
                    "RPN, ROIAlign, and box regressor",
                    "Depth encoder, point-cloud renderer, and CRF",
                    "Histogram, threshold, and watershed",
                ],
                "correct": 0,
                "explanation": (
                    "SAM combines encoded image features with encoded prompts in a mask decoder."
                ),
            },

            {
                "id": "M11.L01.Q03",
                "section_id": "language-segmentation",
                "question": "What enables open-vocabulary segmentation in CLIP-style systems?",
                "options": [
                    "Alignment between visual and text embeddings",
                    "A fixed list of three intensity thresholds",
                    "Only connected-component labeling",
                    "No training data at all",
                ],
                "correct": 0,
                "explanation": (
                    "Image/region features can be matched to flexible text embeddings through a shared representation."
                ),
            },

            {
                "id": "M11.L01.Q04",
                "section_id": "clipseg",
                "question": "What does sigmoid convert CLIPSeg logits into?",
                "options": [
                    "Pixel-wise relevance probabilities",
                    "3D points",
                    "Bounding boxes only",
                    "Class-frequency weights",
                ],
                "correct": 0,
                "explanation": (
                    "Sigmoid maps logits into values interpretable as per-pixel concept relevance probabilities."
                ),
            },

            {
                "id": "M11.L01.Q05",
                "section_id": "monocular-depth",
                "question": "Why is monocular depth estimation inherently ambiguous?",
                "options": [
                    "Multiple 3D scenes can produce similar 2D projections",
                    "RGB images contain no pixels",
                    "Depth networks cannot use transformers",
                    "Camera images always contain stereo pairs",
                ],
                "correct": 0,
                "explanation": (
                    "One 2D view does not uniquely determine scene geometry without learned or geometric priors."
                ),
            },

            {
                "id": "M11.L01.Q06",
                "section_id": "pointcloud-semantic3d",
                "question": "What additional information is required to back-project image pixels into 3D correctly?",
                "options": [
                    "Depth and camera intrinsic parameters",
                    "Only an image histogram",
                    "A text prompt only",
                    "One Dice score",
                ],
                "correct": 0,
                "explanation": (
                    "Depth gives distance along a ray, while intrinsics define how pixels correspond to camera rays."
                ),
            },

            {
                "id": "M11.L01.Q07",
                "section_id": "production-apps",
                "question": "How does the chapter create background blur using segmentation?",
                "options": [
                    "Keep foreground from the original and combine it with a blurred background using a mask",
                    "Blur only the foreground mask",
                    "Run object detection without a mask",
                    "Replace the image with its histogram",
                ],
                "correct": 0,
                "explanation": (
                    "The segmentation mask controls compositing between the sharp source foreground and blurred background."
                ),
            },

            {
                "id": "M11.L01.Q08",
                "section_id": "unet-foundations",
                "question": "What is the central role of U-Net skip connections?",
                "options": [
                    "Transfer fine spatial features from encoder stages to corresponding decoder stages",
                    "Remove the encoder",
                    "Convert multiclass masks into bounding boxes",
                    "Estimate camera intrinsics",
                ],
                "correct": 0,
                "explanation": (
                    "Skip connections restore localization detail that can be lost during downsampling."
                ),
            },

            {
                "id": "M11.L01.Q09",
                "section_id": "custom-training",
                "question": "Why should integer segmentation masks generally use nearest-neighbor resizing?",
                "options": [
                    "To avoid creating invalid interpolated class IDs",
                    "To make every boundary blurry",
                    "To convert classes into probabilities",
                    "To increase the number of classes",
                ],
                "correct": 0,
                "explanation": (
                    "Categorical labels must remain discrete during resizing."
                ),
            },

            {
                "id": "M11.L01.Q10",
                "section_id": "medical-mri",
                "question": "Why is Dice loss useful for tumor segmentation?",
                "options": [
                    "It directly emphasizes foreground-region overlap and helps when the tumor occupies few pixels",
                    "It measures only image brightness",
                    "It creates CT slices",
                    "It removes the need for masks",
                ],
                "correct": 0,
                "explanation": (
                    "Overlap-based objectives are valuable under severe foreground/background imbalance."
                ),
            },

            {
                "id": "M11.L01.Q11",
                "section_id": "swin-unetr",
                "question": "Why does the chapter use sliding-window inference for 3D CT?",
                "options": [
                    "A whole volumetric scan may exceed GPU memory",
                    "The model can process only RGB pixels",
                    "Sliding windows create ground-truth labels",
                    "It replaces the decoder",
                ],
                "correct": 0,
                "explanation": (
                    "Overlapping 3D subvolumes allow inference on inputs too large to process at once."
                ),
            },

            {
                "id": "M11.L01.Q12",
                "section_id": "volumetric-visualization",
                "question": "What does marching cubes produce from a volumetric segmentation mask?",
                "options": [
                    "A polygonal surface mesh",
                    "A text embedding",
                    "A class-frequency table",
                    "A bounding-box proposal network",
                ],
                "correct": 0,
                "explanation": (
                    "Marching cubes extracts an isosurface represented by vertices and polygon faces."
                ),
            },

            {
                "id": "M11.L01.Q13",
                "section_id": "remote-sensing",
                "question": "Why is patch-based training useful for large satellite imagery?",
                "options": [
                    "It reduces memory requirements and turns huge scenes into manageable training samples",
                    "It guarantees every class is balanced automatically",
                    "It removes the need for segmentation masks",
                    "It converts satellite images to depth maps",
                ],
                "correct": 0,
                "explanation": (
                    "Large full-resolution satellite images may not fit into GPU memory and are easier to train as patches."
                ),
            },

            {
                "id": "M11.L01.Q14",
                "section_id": "remote-sensing",
                "question": "What is the purpose of median-frequency class weighting?",
                "options": [
                    "Give rare classes stronger loss influence than dominant classes",
                    "Remove rare classes from training",
                    "Increase the image resolution",
                    "Convert RGB to grayscale",
                ],
                "correct": 0,
                "explanation": (
                    "Class weighting counteracts domination of the loss by frequent pixels."
                ),
            },

            {
                "id": "M11.L01.Q15",
                "section_id": "metrics-overlap",
                "question": "What does IoU measure?",
                "options": [
                    "Intersection of predicted and true regions divided by their union",
                    "Only the number of true negatives",
                    "The training learning rate",
                    "The model's parameter count",
                ],
                "correct": 0,
                "explanation": (
                    "IoU is a direct region-overlap metric."
                ),
            },

            {
                "id": "M11.L01.Q16",
                "section_id": "metrics-overlap",
                "question": "Which metric is especially common for small medical foreground structures?",
                "options": [
                    "Dice coefficient",
                    "JPEG compression ratio",
                    "Image entropy only",
                    "Bounding-box width",
                ],
                "correct": 0,
                "explanation": (
                    "The source emphasizes Dice for overlap-sensitive medical segmentation."
                ),
            },

            {
                "id": "M11.L01.Q17",
                "section_id": "metrics-accuracy-map",
                "question": "Why can pixel accuracy be misleading on an imbalanced dataset?",
                "options": [
                    "A model can predict the dominant background class everywhere and still obtain high accuracy",
                    "Accuracy always ignores true negatives",
                    "Accuracy can only be computed for instance masks",
                    "Accuracy equals mAP by definition",
                ],
                "correct": 0,
                "explanation": (
                    "Large background regions can dominate the fraction of correct pixels even if the target is missed."
                ),
            },

            {
                "id": "M11.L01.Q18",
                "section_id": "metrics-accuracy-map",
                "question": "What does mAP evaluate that a simple mask-overlap score does not fully capture?",
                "options": [
                    "Confidence-ranked instance localization and classification quality across detections",
                    "Only global brightness",
                    "Only true-negative pixels",
                    "Only camera calibration",
                ],
                "correct": 0,
                "explanation": (
                    "mAP is based on precision-recall behavior and IoU-qualified instance matches."
                ),
            },

            {
                "id": "M11.L01.Q19",
                "section_id": "metrics-accuracy-map",
                "type": "open",
                "question": (
                    "Design three segmentation systems: an interactive photo-selection tool, "
                    "a 3D abdominal CT organ segmenter, and a satellite land-cover model. "
                    "For each system, select one architecture/workflow from this lesson, "
                    "specify the input and output representation, identify the main data or "
                    "inference challenge, and choose the most appropriate evaluation metrics."
                ),
            },
        ],

        "passing_score": 70,
    },
}
