"""M12.L01 — Image Classification and Object Detection.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Hands-On Image Processing and Computer Vision with Python, Second Edition,
Chapter 12. Page range was not specified in the supplied chapter text.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M12.L01"

MODULE_ORDER = 12

MODULE_TITLE = "Image Classification and Object Detection"

MODULE_DESCRIPTION = (
    "Learn modern visual recognition from feature embeddings and transfer learning through "
    "attention, transformers, few-shot and self-supervised learning, Bayesian uncertainty, "
    "semi-supervised and federated learning, adversarial robustness, semantic image retrieval, "
    "object detection, instance segmentation, OCR, landmark-based interaction, motion transfer, "
    "and task-specific YOLO segmentation."
)

SOURCE_CHAPTER = 12

SOURCE_PAGES = "Page range not specified in the supplied chapter text"


TOPIC = {
    "title": "Image Classification and Object Detection",

    "slug": "image-processing-m12-l01",

    "description": (
        "A source-aligned lesson on how modern vision systems represent, classify, retrieve, "
        "localize, and interpret images using CNNs, transformers, embeddings, low-label learning, "
        "uncertainty estimation, distributed learning, adversarial analysis, object detectors, OCR, "
        "landmark systems, and practical detection/segmentation applications."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 8.0,

    "skill_tags": [
        "computer-vision",
        "image-classification",
        "object-detection",
        "feature-embeddings",
        "pca",
        "tsne",
        "transfer-learning",
        "attention",
        "vit",
        "swin-transformer",
        "clip",
        "dinov2",
        "few-shot-learning",
        "facenet",
        "bayesian-neural-networks",
        "mc-dropout",
        "fixmatch",
        "mae",
        "federated-learning",
        "fgsm",
        "image-retrieval",
        "efficientnet",
        "retinanet",
        "mask-rcnn",
        "ocr",
        "mediapipe",
        "fomm",
        "yolov8-segmentation",
    ],

    "prerequisite_ids": ["M11.L01"],

    "lesson": {
        "title": "Image Classification and Object Detection",

        "content": r"""
# Image Classification and Object Detection

> **Course:** Image Processing and Computer Vision with Python  
> **Lesson:** M12.L01  
> **Module:** Image Classification and Object Detection  
> **Source alignment:** *Hands-On Image Processing and Computer Vision with Python, Second Edition*, Chapter 12. The supplied chapter text did not include a reliable page range. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why modern vision systems rely on feature embeddings rather than raw pixels.
- Compare PCA and t-SNE for visualizing high-dimensional image representations.
- Explain hierarchical CNN features and activation-map visualization.
- Distinguish direct use of a pretrained classifier from transfer learning and fine-tuning.
- Explain channel attention, spatial attention, Grad-CAM, ViT attention, and Swin-style windowed attention.
- Explain zero-shot classification with CLIP and prototype-based few-shot learning with DINOv2.
- Explain embedding-based face recognition and why metric-learning objectives improve identity separation.
- Explain Bayesian neural-network uncertainty and Monte Carlo Dropout.
- Describe semi-supervised FixMatch-style pseudo-labeling and consistency regularization.
- Explain Masked Autoencoders as self-supervised reconstruction models.
- Explain federated learning and FedAvg at a conceptual level.
- Explain the mechanism of FGSM-style adversarial perturbations and common defense ideas.
- Build the mental model of semantic image retrieval using EfficientNet embeddings, PCA, and cosine similarity.
- Distinguish image classification from object detection and instance segmentation.
- Explain RetinaNet, FPN, and focal loss.
- Explain Mask R-CNN outputs and why per-instance masks add information beyond boxes.
- Compare Tesseract, PaddleOCR, EasyOCR, and TrOCR pipelines.
- Explain detection + recognition pipelines for automatic license-plate recognition.
- Explain face and hand landmark localization with MediaPipe.
- Describe FOMM motion transfer at a conceptual level.
- Explain task-specific YOLOv8 instance segmentation and simple severity estimation from predicted mask area.

---

## 1. Images become feature embeddings

A raw image is a large array of pixels.

Modern neural networks transform that array into a representation:

```text
image
  ↓
feature extractor
  ↓
embedding vector
```

An embedding may have hundreds or thousands of dimensions.

The important idea is:

> The geometry of the embedding space can encode semantic similarity.

Images from similar categories often produce nearby representations, while unrelated images tend to be farther apart.

This idea powers:

- classification,
- transfer learning,
- few-shot learning,
- face recognition,
- semantic search,
- clustering,
- retrieval.

[[IMAGE_NEEDED: Pixel space to semantic embedding space | Show several animal images passing through a CNN into high-dimensional vectors, then a 2D conceptual embedding where dogs cluster together, cats cluster together, and unrelated animals are farther apart | Learner should understand that representation geometry becomes semantically meaningful]]

---

## 2. PCA and t-SNE: seeing high-dimensional feature space

High-dimensional vectors cannot be directly plotted.

Dimensionality reduction maps them to two or three dimensions for visualization.

### PCA

Principal Component Analysis is linear.

It finds orthogonal directions that capture large amounts of variance.

Conceptually:

```text
high-dimensional vectors
        ↓
linear projection
        ↓
principal components
```

Strengths:

- efficient,
- deterministic under fixed setup,
- useful for compression and global variance structure.

Limitation:

- nonlinear manifolds can remain overlapped.

### t-SNE

t-SNE is nonlinear and focuses strongly on preserving local neighborhoods.

It constructs pairwise similarity distributions in:

- original high-dimensional space,
- low-dimensional visualization space,

then minimizes a divergence between them.

The source uses a Student's t-distribution for low-dimensional pair similarities and KL divergence as the optimization objective.

### MNIST intuition

Raw 28×28 MNIST images can be considered:

```text
784-dimensional vectors
```

PCA may show overlapping digit classes.

t-SNE often reveals clearer local clusters.

### Important interpretation caution

t-SNE is mainly a visualization tool.

Do not read:

- exact cluster-to-cluster distance,
- global geometry,
- cluster area,

as if the 2D plot were a faithful metric reconstruction of the full space.

[[IMAGE_NEEDED: PCA versus t-SNE on MNIST | Show the same digit samples projected with PCA and t-SNE, using class colors | Learner should see PCA preserving linear variance while t-SNE emphasizes local neighborhood separation]]

### Deep features are usually more useful than raw pixels

The source then extracts VGG16's penultimate `fc2` features.

Each image becomes a 4096-dimensional descriptor.

Applying t-SNE to these features can produce semantically meaningful clusters even when the visualization dataset differs from the network's original ImageNet task.

That demonstrates the transferability of learned visual representations.

---

## 3. Looking inside CNN features

CNNs learn a hierarchy.

The source summarizes it approximately as:

```text
early layers
-> edges and corners

intermediate layers
-> textures and patterns

deeper layers
-> object parts

late layers
-> semantic concepts
```

### Forward hooks

PyTorch forward hooks can capture intermediate tensors without modifying the model architecture.

Conceptually:

```python
activations = {}

def hook_fn(name):
    def hook(module, inputs, output):
        activations[name] = output.detach()
    return hook
```

A pretrained ResNet18 can be instrumented at:

- initial convolution,
- layer1,
- layer2,
- layer3,
- layer4.

### Activation map

If a captured tensor has shape:

```text
C × H × W
```

one simple visualization averages across channels:

```text
activation(x,y)
=
mean over channels
```

Then normalize and overlay it on the original image.

[[IMAGE_NEEDED: CNN feature hierarchy | Show one image with feature visualizations from an early, middle, and deep ResNet layer: edges → textures → object parts/semantic region | Learner should see how internal representations become increasingly abstract]]

### What this visualization does and does not prove

A bright activation region indicates strong activation under the chosen summarization method.

It does not prove a human-like causal explanation of the model's reasoning.

Treat activation maps as diagnostic visualizations, not perfect explanations.

---

## 4. Image classification and transfer learning

Image classification asks:

```text
What is in this image?
```

It returns a class for the whole image.

For logits `z_k`, softmax produces class probabilities:

```text
p_k =
exp(z_k) / sum_j exp(z_j)
```

The predicted class is the largest probability.

### Why transfer learning matters

Training a large CNN from scratch often needs:

- many labeled samples,
- significant compute,
- careful optimization.

A pretrained network already contains useful generic features.

The source compares two strategies.

### Strategy A: use the pretrained classifier directly

A VGG16 trained on ImageNet can classify ImageNet categories.

For cats versus dogs, breed-level ImageNet predictions can be mapped into supercategories.

This requires no new training, but the classifier was not optimized for the target task.

### Strategy B: replace the classification head

Keep the convolutional feature extractor:

```text
pretrained backbone
```

remove its original ImageNet head, and add a task-specific classifier.

For binary classification:

```text
backbone
→ global average pooling
→ dense layer
→ dropout
→ sigmoid
```

Initially, the backbone can be frozen.

Only the new classifier is trained.

[[IMAGE_NEEDED: Transfer learning workflow | Show pretrained ImageNet CNN, removal of original classifier, frozen backbone, new binary cat-vs-dog head, then optional fine-tuning of deepest layers | Learner should distinguish feature extraction from fine-tuning]]

### Fine-tuning

After training a new head, selected deeper backbone layers can be unfrozen.

This lets higher-level features adapt to the target domain.

### Data augmentation

The chapter recommends transformations such as:

- flips,
- rotation,
- zoom,
- brightness variation.

These reduce overfitting by increasing training diversity.

---

## 5. Attention for image classification

A CNN feature tensor contains many channels and spatial positions.

Attention asks:

```text
WHAT features matter?
WHERE do they matter?
```

### Channel attention

Channel attention assigns importance to feature maps.

The source combines:

- global average pooling,
- global max pooling,

to estimate channel importance.

Intuition:

```text
average pooling -> consistently present features
max pooling     -> strongly activated features
```

A sigmoid gate scales each channel.

### Spatial attention

Spatial attention asks which image locations are important.

The source aggregates channels using:

- average,
- maximum,

then uses a convolution to produce a spatial attention mask.

The common ordering in the source is:

```text
channel attention
then
spatial attention
```

[[IMAGE_NEEDED: Channel and spatial attention | Show CNN feature tensor, channel-attention weights amplifying selected channels, then spatial mask highlighting important image regions | Learner should remember channel attention = what, spatial attention = where]]

### Grad-CAM

Grad-CAM uses gradients from a chosen class score to weight convolutional feature maps.

The resulting heatmap can indicate which regions contribute strongly to that class prediction.

The chapter uses it to compare a baseline CNN with an attention-enhanced CNN.

---

## 6. Vision Transformers and Swin Transformers

### Vision Transformer

ViT divides an image into patches.

Each patch becomes a token.

Self-attention lets each token interact with other tokens.

This provides direct long-range relationships.

The source uses pretrained ViT models for:

- classification,
- attention visualization,
- flower recognition.

### Attention rollout

Attention maps from several transformer layers can be combined into a coarse explanation of which image patches contributed strongly to the prediction.

[[IMAGE_NEEDED: ViT classification and attention rollout | Show image split into patches, tokens entering transformer blocks, CLS/class output, and a patch-level attention heatmap over the source image | Learner should understand both patch tokenization and global self-attention]]

### Swin Transformer

Global ViT attention becomes costly as image resolution grows.

Swin limits attention to local windows and shifts those windows between layers.

This gives:

- local efficiency,
- hierarchical features,
- communication between neighboring windows.

The source frames Swin as combining some CNN-like locality with transformer attention.

It demonstrates gradient-based saliency for interpreting a Swin classification.

### Attention map versus saliency map

The source uses different explanation approaches:

```text
ViT -> attention rollout
Swin -> gradient-based saliency
```

Do not assume these visualizations have identical meaning.

---

## 7. Zero-shot and few-shot classification

### N-way K-shot learning

A few-shot task contains:

```text
N classes
K labeled support examples per class
```

The model must recognize new query samples using very little labeled data.

### CLIP zero-shot classification

CLIP compares an image embedding with text embeddings.

Instead of a fixed classifier head:

```text
image embedding
     ↘
 cosine / similarity
     ↗
text embeddings
```

Candidate prompts might be:

```text
"a photo of a dog"
"a photo of a horse"
"a photo of a parrot"
```

The highest image-text similarity becomes the prediction.

This is called zero-shot because no target-task training examples are required at inference time.

### DINOv2 prototype-based few-shot learning

DINOv2 provides self-supervised image embeddings.

For each class:

1. embed its support images,
2. average embeddings,
3. create a class prototype.

Then:

```text
query image
→ embedding
→ cosine similarity to prototypes
→ nearest prototype class
```

[[IMAGE_NEEDED: CLIP zero-shot vs DINOv2 few-shot | Show CLIP comparing one image embedding to several text embeddings; beside it show DINOv2 averaging two support embeddings per class into prototypes and classifying a query by cosine similarity | Learner should distinguish language-based zero-shot from visual-prototype few-shot learning]]

### What is being transferred?

Neither method learns the target concept from scratch.

Both rely on a powerful pretrained representation.

---

## 8. Face recognition as metric learning

Face recognition can be formulated as:

```text
face image
→ embedding vector
```

Then identity is determined through embedding similarity.

### Gallery prototypes

For each known person:

```text
prototype =
average of several face embeddings
```

A query face is compared with all prototypes.

A similarity threshold can reject unknown identities.

### Generic encoder versus face-specific encoder

The chapter first demonstrates a ResNet-based feature extractor.

It explicitly notes that this is not the same as a classically trained Siamese face-recognition model.

Then it introduces FaceNet, which was trained specifically for identity embedding quality.

### Metric learning

Contrastive/triplet-style training encourages:

```text
same identity -> embeddings closer
different identities -> embeddings farther apart
```

This creates a more useful geometry for recognition.

[[IMAGE_NEEDED: Face embedding recognition | Show several gallery identities mapped to compact clusters/prototypes in embedding space, a query face mapped nearby, cosine similarity scores, and an Unknown threshold | Learner should understand recognition as nearest-prototype metric matching rather than fixed closed-set classification]]

---

## 9. Bayesian neural networks and MC Dropout

A deterministic network has one learned value for each parameter.

A Bayesian neural network models uncertainty over parameters.

Conceptually:

```text
weight
~ probability distribution
```

A forward pass samples weights, so repeated predictions can vary.

### Variational learning

The source combines:

- classification loss,
- KL-divergence regularization.

The KL term controls how far the learned posterior moves from the prior.

### Monte Carlo prediction

Run several stochastic forward passes:

```text
prediction mean
=
average probability

uncertainty
=
variation across predictions
```

High variation means the sampled models disagree.

That can signal lower confidence.

### MC Dropout

Full Bayesian networks can be expensive.

MC Dropout keeps dropout active during inference.

Each forward pass uses a different dropout mask:

```text
same input
→ slightly different network sample
```

Average predictions and measure variation.

[[IMAGE_NEEDED: Deterministic vs Bayesian vs MC Dropout | Show deterministic model producing one prediction; Bayesian model sampling several weight sets; MC Dropout sampling several dropout masks; both stochastic methods producing mean probability + uncertainty | Learner should understand uncertainty as disagreement across plausible model realizations]]

### Accuracy is not the whole objective

The source notes that a Bayesian model may trade some raw accuracy for uncertainty estimation.

In safety-critical applications, knowing that a model is unsure can be valuable.

---

## 10. Semi-supervised learning with FixMatch-style pseudo-labeling

Labeled images are expensive.

Unlabeled images are often abundant.

Semi-supervised learning uses both.

The chapter gives a simplified FixMatch-style demonstration.

### Step 1: supervised learning

Train normally on a small labeled subset:

```text
labeled image
→ model
→ true label loss
```

### Step 2: pseudo-label unlabeled data

Run the model on an unlabeled sample.

If the model is sufficiently confident:

```text
max probability >= threshold
```

treat the predicted class as a temporary pseudo-label.

### Step 3: consistency

Apply a stronger perturbation/augmentation.

Require the model to predict the same pseudo-label.

```text
weak version
→ confident pseudo-label

strong version
→ train toward that pseudo-label
```

### Combined objective

```text
total loss =
supervised loss
+
lambda_u * unsupervised consistency loss
```

[[IMAGE_NEEDED: FixMatch-style learning loop | Show small labeled set and large unlabeled set, weak augmentation creating high-confidence pseudo-labels, strong augmentation, consistency loss, and combined model update | Learner should understand how the model turns reliable guesses into temporary supervision]]

### Failure mode

Wrong high-confidence pseudo-labels can reinforce mistakes.

Confidence thresholds and augmentation design therefore matter.

---

## 11. Masked Autoencoders: self-supervision through reconstruction

Self-supervised learning creates supervision from the data itself.

Masked Autoencoders (MAE) use a simple task:

1. divide an image into patches,
2. hide a large fraction,
3. encode only visible patches,
4. reconstruct the missing patches.

The source notes that a large mask fraction such as around 75% is common.

### Architecture

An MAE contains:

- patch embedding,
- masking module,
- ViT encoder,
- lightweight decoder,
- reconstruction loss.

[[IMAGE_NEEDED: Masked Autoencoder pipeline | Show image split into patches, ~75% patches hidden, visible patches entering ViT encoder, mask tokens/decoder reconstructing the missing regions, and reconstructed image | Learner should understand how unlabeled images supervise themselves]]

### Why this can learn useful features

To reconstruct missing content, the model must infer:

- object structure,
- texture,
- shape,
- context.

The encoder can then be reused as a feature extractor.

The source visualizes MAE embeddings using:

- PCA,
- t-SNE.

Semantically related categories can cluster despite the pretraining objective not using class labels.

### Reconstruction is the pretext task

The final goal is often not perfect pixel reconstruction.

The reconstruction task is a way to learn transferable features.

{{exercise:M12.L01.EX01}}

---

## 12. Federated learning for distributed classification

Traditional training assumes data can be collected centrally.

Federated learning keeps raw client data local.

Conceptually:

```text
central server sends global model
           ↓
clients train on private local data
           ↓
clients send model updates
           ↓
server aggregates
           ↓
new global model
```

### Federated averaging

If clients have local model weights:

```text
w_1, w_2, ..., w_K
```

the server computes a weighted average, often weighted by each client's sample count.

This is the core idea behind FedAvg.

### Why federated learning matters

The source highlights benefits such as:

- raw images stay on local devices,
- distributed computation,
- continued learning from decentralized data.

### Challenges

The chapter also emphasizes:

- non-IID client data,
- communication cost,
- client drift,
- malicious/poisoned updates.

[[IMAGE_NEEDED: Federated averaging | Show central server distributing one model to several clients with different private image distributions, local training, model updates returning, weighted aggregation, and next global round | Learner should understand that models move while raw data stays local]]

### Privacy nuance

Federated learning reduces the need to centralize raw data.

That does not automatically make the system perfectly private or secure.

The source explicitly mentions security risks from malicious clients.

---

## 13. Adversarial examples and FGSM

An adversarial example is a deliberately perturbed input designed to change a model prediction.

The perturbation can be visually small but strategically aligned with the model's gradient.

### White-box versus black-box

**White-box**

The attacker has access to model parameters or gradients.

**Black-box**

The attacker has limited or indirect access and must infer or transfer an attack.

### FGSM intuition

The Fast Gradient Sign Method computes the gradient of the loss with respect to the input image.

Then it takes only the sign:

```text
perturbation =
epsilon * sign(gradient)
```

The adversarial image becomes:

```text
x_adv =
clip(
    x + epsilon * sign(∇x loss)
)
```

The source uses clipping to keep pixels in the valid input range.

[[IMAGE_NEEDED: FGSM adversarial perturbation | Show clean image, loss gradient sign pattern, tiny scaled perturbation, adversarial image that looks visually similar, and changed classifier prediction | Learner should understand that the perturbation follows the direction that increases model loss]]

### Defense ideas in the source

The chapter mentions approaches such as:

- adversarial training,
- defensive distillation,
- input denoising.

No defense should be assumed universally sufficient.

Robustness depends on threat model and evaluation.

---

## 14. Semantic image search with EfficientNet features

A content-based image search engine does not have to compare raw pixels.

The source builds:

```text
database image
→ EfficientNet embedding
→ optional PCA
→ stored vector
```

At query time:

```text
query image
→ same embedding pipeline
→ cosine similarity
→ nearest database images
```

### Why embeddings help

Two images can differ in:

- exact pixels,
- background,
- pose,
- scale,

while still representing similar objects.

A deep representation can place them nearby semantically.

### PCA for retrieval

PCA can reduce feature dimensionality.

Benefits may include:

- lower storage,
- faster distance calculations,
- reduced redundancy.

### Cosine similarity

For vectors `a` and `b`:

```text
cosine similarity =
(a · b) / (||a|| ||b||)
```

It measures angular similarity.

[[IMAGE_NEEDED: Semantic image retrieval pipeline | Show image database → EfficientNet embeddings → PCA/vector index; query image → embedding → cosine similarity → ranked visually/semantically similar results | Learner should see retrieval as nearest-neighbor search in feature space]]

### Scaling search

The source notes that brute-force comparison becomes expensive for very large databases.

It suggests scalable alternatives such as:

- KD-trees or ball trees in suitable lower-dimensional settings,
- FAISS,
- Annoy,
- ScaNN,
- vector databases.

It also suggests stronger modern embeddings such as:

- DINOv2,
- CLIP.

---

## 15. From classification to object detection

Classification asks:

```text
What is in the image?
```

Object detection asks:

```text
What objects are present?
Where are they?
```

Each detection contains:

- bounding box,
- class,
- confidence score.

### IoU

Intersection over Union compares predicted and ground-truth boxes:

```text
IoU =
intersection area
/
union area
```

Higher IoU means stronger localization overlap.

An image can contain many detections simultaneously.

[[IMAGE_NEEDED: Classification vs detection | Show same street image: classification returning one global label; detection returning several boxes with class names/confidences | Learner should understand that detection combines recognition and spatial localization]]

---

## 16. RetinaNet, FPN, and focal loss

RetinaNet is a one-stage object detector.

The source highlights three important components:

1. ResNet50 backbone,
2. Feature Pyramid Network,
3. focal loss.

### Feature Pyramid Network

Objects occur at different sizes.

FPN combines features across scales so the detector can recognize:

- small objects,
- medium objects,
- large objects.

### The class-imbalance problem

One-stage detectors evaluate many candidate locations.

Most are easy background.

If all examples contribute equally, those easy negatives can dominate training.

### Focal loss

Focal loss reduces the contribution from already-easy examples and focuses more on hard cases.

Conceptually:

```text
easy, confident example
-> downweighted

hard/misclassified example
-> stronger contribution
```

[[IMAGE_NEEDED: RetinaNet and focal loss | Show image pyramid/FPN levels feeding one-stage classification and box heads, plus a small chart where focal loss downweights easy high-confidence background examples | Learner should connect FPN with scale and focal loss with foreground-background imbalance]]

### Pretrained inference

A pretrained detector returns:

```text
boxes
scores
labels
```

Then a confidence threshold removes low-confidence detections.

The threshold controls a precision/recall trade-off and should not be treated as one universal value.

---

## 17. Mask R-CNN: detection plus instance masks

RetinaNet gives boxes.

Mask R-CNN adds a pixel-level mask for each detected object.

Each instance can contain:

```text
class
confidence
bounding box
binary mask
```

### Two-stage architecture

Stage 1:

```text
Region Proposal Network
-> candidate object regions
```

Stage 2:

```text
classify region
refine box
predict mask
```

A ResNet-FPN backbone provides multi-scale features.

[[IMAGE_NEEDED: RetinaNet vs Mask R-CNN output | Show one scene with RetinaNet bounding boxes and beside it Mask R-CNN with boxes plus individual colored pixel masks and contours | Learner should understand what instance masks add beyond rectangular localization]]

### Why masks matter

A box includes background pixels around an object.

A segmentation mask describes the object's actual shape more precisely.

This becomes important for:

- measurement,
- editing,
- robotics,
- medical/industrial inspection.

---

## 18. OCR: from characters to detection-and-recognition pipelines

OCR converts visual text into machine-readable strings.

The chapter shows that real-world OCR often contains two separate problems:

```text
text detection
+
text recognition
```

### Tesseract

Tesseract is used as a classical/established OCR baseline.

It can work well for relatively clean text but may need:

- thresholding,
- denoising,
- deskewing,
- language configuration.

The chapter also discusses multilingual OCR.

### PaddleOCR

PaddleOCR uses a deep pipeline with stages such as:

- text detection,
- angle classification,
- text recognition.

This is more robust for:

- rotated text,
- curved text,
- natural scenes.

### EasyOCR

EasyOCR provides a lightweight deep-learning API that returns:

- bounding box,
- text,
- confidence.

The source emphasizes ease of use in uncontrolled scenes.

### TrOCR

TrOCR formulates OCR as vision-to-text sequence generation.

Conceptually:

```text
cropped text image
→ visual encoder
→ transformer text decoder
→ character sequence
```

[[IMAGE_NEEDED: OCR model evolution | Show document/scene image passing through Tesseract baseline, PaddleOCR detection+angle+recognition pipeline, EasyOCR detection/recognition, and TrOCR vision-encoder→text-decoder pipeline | Learner should distinguish preprocessing-heavy OCR from learned detection/recognition and end-to-end vision-to-text modeling]]

### ALPR: detection before recognition

License-plate recognition is a useful example.

Pipeline:

```text
vehicle image
→ detect plate with YOLO
→ crop plate ROI
→ OCR
→ cleaned plate string
```

The detector eliminates irrelevant background before recognition.

This modular pattern generalizes to many document and scene-text systems.

---

## 19. Face and hand landmarks with MediaPipe

Bounding boxes locate coarse objects.

Landmarks locate meaningful internal geometry.

### Face landmarks

The source uses MediaPipe Face Landmarker with a dense facial mesh.

Selected landmarks include regions around:

- eyes,
- nose,
- mouth,
- jaw.

For an AR overlay such as glasses, the distance between the eyes can control overlay scale.

Then alpha blending places a transparent PNG over the face.

[[IMAGE_NEEDED: Face landmarks and AR overlay | Show dense face mesh, selected eye/nose/mouth anchor points, inter-eye distance used for scaling, and final sunglasses/moustache overlay | Learner should see landmarks as geometric anchors for stable augmentation]]

### Hand landmarks

The source uses 21 hand keypoints.

Connections form a skeletal graph.

Important points include:

- wrist,
- finger joints,
- fingertips.

MediaPipe can also predict handedness.

These representations support:

- gesture recognition,
- sign-language analysis,
- virtual drawing,
- HCI,
- AR/VR.

[[IMAGE_NEEDED: Hand landmark graph | Show 21 labeled hand keypoints connected into finger chains, with fingertips emphasized and left/right handedness output | Learner should understand how a dense pose becomes a compact graph representation]]

---

## 20. Motion transfer with the First Order Motion Model

The First Order Motion Model (FOMM) animates a source image using motion from a driving video.

Conceptually:

```text
source image
+
driving frame sequence
    ↓
learned keypoints + motion estimation
    ↓
dense deformation of source features
    ↓
generated animation
```

Unlike manually specified facial landmarks, the source describes FOMM as learning motion-relevant keypoints automatically.

[[IMAGE_NEEDED: FOMM motion transfer | Show static source portrait, driving-video frame with learned motion keypoints, dense deformation field, and generated source-identity frame following the driving pose | Learner should understand appearance comes from the source while motion comes from the driver]]

### What the model preserves and transfers

The intended behavior is:

```text
source -> appearance/identity
driver -> pose/expression/motion
```

This family of techniques underlies:

- image animation,
- avatars,
- talking-head systems,
- synthetic video.

### Responsible-use note

Synthetic identity/media systems can be used legitimately for:

- animation,
- accessibility,
- education,
- entertainment,

but outputs should not be represented as authentic recordings of real people when they are synthetic.

---

## 21. Car-damage segmentation with YOLOv8

The final application turns instance segmentation into a domain-specific measurement system.

The source uses the CarDD dataset containing damages such as:

- dents,
- scratches,
- cracks,
- broken components.

### Why segmentation instead of only boxes?

A bounding box gives approximate location.

A mask gives:

```text
pixel-level damaged area
```

That enables measurement.

### Transfer learning

Start from a pretrained YOLOv8 segmentation model:

```text
COCO pretrained model
     ↓ fine-tune
vehicle damage masks
```

The source converts annotations from COCO segmentation format to YOLO polygon format.

Polygon coordinates are normalized to `[0,1]`.

### Inference

The model predicts instance masks.

Then damage area can be estimated by counting foreground pixels.

Conceptually:

```text
damage area =
sum(binary mask)
```

### Severity rule

The source demonstrates a simple hand-written mapping from total damaged mask area to:

- Minor,
- Moderate,
- Severe.

[[IMAGE_NEEDED: YOLOv8 car-damage assessment | Show damaged car, predicted damage instance masks, mask-area pixel count, and rule-based severity label | Learner should understand the separation between learned damage localization and hand-designed downstream severity logic]]

### Important limitation

Pixel area alone is a simplified severity estimate.

It does not automatically account for:

- physical scale,
- repair cost,
- component importance,
- depth of damage,
- safety significance.

The lesson is broader:

> A computer-vision model often produces measurements that a downstream business rule converts into a decision.

{{exercise:M12.L01.EX02}}

---

## Important misconceptions

### Misconception 1

> Deep classifiers compare raw pixels directly when deciding semantic similarity.

### Why this is wrong

The source emphasizes learned feature embeddings whose geometry captures higher-level visual structure.

### Misconception 2

> t-SNE preserves every global distance faithfully.

### Why this is wrong

t-SNE is optimized for local-neighborhood visualization, not exact preservation of global metric geometry.

### Misconception 3

> Transfer learning means the pretrained network must remain completely frozen forever.

### Why this is wrong

A common workflow trains a new head first, then optionally fine-tunes selected pretrained layers.

### Misconception 4

> Attention maps and Grad-CAM/saliency maps are identical explanations.

### Why this is wrong

They are generated through different mechanisms and should be interpreted as different diagnostic views.

### Misconception 5

> Few-shot learning means training a normal large classifier from scratch on only two images.

### Why this is wrong

The source relies on powerful pretrained embeddings and prototype similarity.

### Misconception 6

> High predictive probability always means the model truly knows the answer.

### Why this is wrong

Bayesian/MC-Dropout sections motivate uncertainty estimation because standard networks can be overconfident.

### Misconception 7

> Semi-supervised learning can safely trust every pseudo-label.

### Why this is wrong

FixMatch-style methods filter for confident predictions because unreliable pseudo-labels can reinforce errors.

### Misconception 8

> MAE reconstructs patches only because reconstruction is the final application.

### Why this is wrong

Reconstruction is a self-supervised pretraining task used to learn transferable representations.

### Misconception 9

> Federated learning automatically guarantees complete privacy and security.

### Why this is wrong

Raw data remain local, but the source still identifies communication, non-IID, drift, and malicious-client risks.

### Misconception 10

> Adversarial examples must look obviously corrupted.

### Why this is wrong

The point of attacks such as FGSM is that relatively small targeted perturbations can change model predictions.

### Misconception 11

> Image retrieval is classification followed by filename matching.

### Why this is wrong

The source implements retrieval as nearest-neighbor similarity in embedding space.

### Misconception 12

> Object detection and instance segmentation return the same spatial information.

### Why this is wrong

Object detection returns boxes, while instance segmentation additionally predicts pixel-level object shapes.

### Misconception 13

> OCR is only character classification.

### Why this is wrong

Real scene OCR frequently requires text detection, orientation handling, sequence recognition, and language modeling.

### Misconception 14

> A facial bounding box is sufficient for stable AR filters.

### Why this is wrong

The MediaPipe example uses precise landmarks to control position, scale, and alignment.

### Misconception 15

> A large predicted damage mask automatically means severe real-world damage.

### Why this is wrong

The source's severity mapping is a simplified rule based on mask pixel area rather than a complete physical or financial assessment.

---

## Key terminology

| Term | Meaning |
|---|---|
| Embedding | High-dimensional learned representation of an image |
| PCA | Linear dimensionality reduction preserving major variance directions |
| t-SNE | Nonlinear visualization emphasizing local neighborhoods |
| Forward hook | Mechanism for capturing intermediate neural activations |
| Transfer learning | Reusing pretrained representations on a target task |
| Fine-tuning | Continuing training on selected pretrained parameters |
| Global average pooling | Spatial averaging that converts feature maps to compact descriptors |
| Channel attention | Learned importance over feature channels |
| Spatial attention | Learned importance over spatial locations |
| Grad-CAM | Gradient-weighted class activation visualization |
| ViT | Vision Transformer |
| Swin Transformer | Hierarchical shifted-window vision transformer |
| Zero-shot learning | Predicting target concepts without target-task labeled examples |
| Few-shot learning | Learning/recognizing classes from very few labeled support examples |
| Prototype | Representative embedding, often the mean of support embeddings |
| Metric learning | Learning embeddings where distance corresponds to semantic/identity similarity |
| FaceNet | Face-recognition embedding model |
| Bayesian neural network | Neural model representing uncertainty over parameters |
| MC Dropout | Stochastic inference with dropout active to approximate uncertainty |
| Pseudo-label | Model-generated temporary label for unlabeled data |
| FixMatch | Semi-supervised method using confidence filtering and consistency |
| MAE | Masked Autoencoder |
| Self-supervised learning | Learning representations from automatically generated supervision |
| Federated learning | Collaborative training without centralizing raw client data |
| FedAvg | Federated averaging of client model updates |
| Non-IID | Client data distributions that are not identically distributed |
| Adversarial example | Input intentionally perturbed to alter model prediction |
| FGSM | Fast Gradient Sign Method |
| Cosine similarity | Angular similarity between embedding vectors |
| ANN | Approximate nearest-neighbor search |
| Object detection | Classification plus spatial localization with boxes |
| FPN | Feature Pyramid Network |
| Focal loss | Loss that downweights easy examples in dense detection |
| RetinaNet | One-stage FPN detector using focal loss |
| Mask R-CNN | Two-stage detector with an instance-mask branch |
| OCR | Optical Character Recognition |
| ALPR | Automatic License Plate Recognition |
| TrOCR | Transformer-based vision-to-text OCR |
| Landmark | Semantically meaningful geometric keypoint |
| FOMM | First Order Motion Model for image animation |
| Instance segmentation | Per-object pixel mask prediction |
| YOLOv8 segmentation | YOLO-family instance-segmentation model |

---

## Self-check

Before continuing, make sure you can answer:

1. Why are learned image embeddings useful?
2. What does PCA preserve?
3. What does t-SNE prioritize?
4. Why should t-SNE global distances be interpreted cautiously?
5. Why can VGG16 features transfer to a new dataset?
6. What do early and deep CNN layers tend to represent?
7. What does a forward hook capture?
8. How does direct pretrained inference differ from transfer learning?
9. What is frozen during feature-extractor training?
10. Why use global average pooling in a new classification head?
11. What is fine-tuning?
12. What is the difference between channel and spatial attention?
13. How does Grad-CAM differ from raw activation averaging?
14. How does ViT represent an image?
15. Why does Swin use local shifted windows?
16. How does CLIP perform zero-shot classification?
17. How does DINOv2 support prototype-based few-shot classification?
18. What is an N-way K-shot task?
19. Why are embeddings useful for face recognition?
20. Why does FaceNet generally produce more task-appropriate identity embeddings than a generic ImageNet encoder?
21. What is uncertainty in a Bayesian classifier?
22. How does MC Dropout approximate model uncertainty?
23. What does disagreement across stochastic forward passes indicate?
24. What is a pseudo-label?
25. Why does FixMatch use a confidence threshold?
26. Why train on a strongly augmented version after creating a weak-view pseudo-label?
27. What is MAE's self-supervised objective?
28. Why mask a large fraction of image patches?
29. Why can MAE encoder features transfer to other tasks?
30. What data are exchanged in federated learning?
31. What does FedAvg aggregate?
32. What does non-IID client data mean?
33. Why is federated learning not automatically perfectly secure?
34. What gradient does FGSM use?
35. What does epsilon control in FGSM?
36. Why can semantic search succeed when images do not match pixel-for-pixel?
37. Why might PCA help an image-retrieval system?
38. What does cosine similarity compare?
39. Why do large retrieval systems use ANN indexes?
40. What additional output does object detection provide beyond classification?
41. What does IoU measure for boxes?
42. Why does RetinaNet need focal loss?
43. Why does FPN help detect multiple object sizes?
44. What information does Mask R-CNN add beyond a box?
45. Why is OCR often split into detection and recognition?
46. What makes TrOCR conceptually different from Tesseract?
47. Why does ALPR detect the plate before running OCR?
48. Why are landmarks better than a coarse face box for AR overlays?
49. How many hand-landmark concepts does MediaPipe provide in the source example?
50. What does FOMM transfer from the driving video?
51. What does the source retain from the static source image in motion transfer?
52. Why does car-damage estimation benefit from segmentation masks?
53. What is learned by YOLOv8 in the damage pipeline, and what is still hand-designed afterward?
54. Why should predicted mask area not be treated as a complete severity assessment?

---

## Retain this idea

**Modern visual understanding is built around transferable representations. The same idea—map visual content into meaningful features—supports classification, few-shot recognition, uncertainty estimation, self-supervised learning, semantic search, detection, OCR, landmark reasoning, and instance segmentation. The downstream task changes, but strong representations and appropriate evaluation remain the foundation.**
        """,

        "estimated_minutes": 480,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "embedding-space", "title": "Images Become Feature Embeddings", "order": 1},
            {"id": "pca-tsne", "title": "PCA and t-SNE: Seeing High-Dimensional Feature Space", "order": 2},
            {"id": "cnn-feature-visualization", "title": "Looking Inside CNN Features", "order": 3},
            {"id": "classification-transfer", "title": "Image Classification and Transfer Learning", "order": 4},
            {"id": "attention-classification", "title": "Attention for Image Classification", "order": 5},
            {"id": "vit-swin", "title": "Vision Transformers and Swin Transformers", "order": 6},
            {"id": "few-shot-clip-dino", "title": "Zero-Shot and Few-Shot Classification", "order": 7},
            {"id": "face-embeddings", "title": "Face Recognition as Metric Learning", "order": 8},
            {"id": "bayesian-uncertainty", "title": "Bayesian Neural Networks and MC Dropout", "order": 9},
            {"id": "semi-supervised", "title": "Semi-Supervised Learning with FixMatch-Style Pseudo-Labeling", "order": 10},
            {"id": "mae-selfsupervised", "title": "Masked Autoencoders: Self-Supervision Through Reconstruction", "order": 11},
            {"id": "federated-learning", "title": "Federated Learning for Distributed Classification", "order": 12},
            {"id": "adversarial-robustness", "title": "Adversarial Examples and FGSM", "order": 13},
            {"id": "semantic-image-search", "title": "Semantic Image Search with EfficientNet Features", "order": 14},
            {"id": "object-detection", "title": "From Classification to Object Detection", "order": 15},
            {"id": "retinanet", "title": "RetinaNet, FPN, and Focal Loss", "order": 16},
            {"id": "mask-rcnn", "title": "Mask R-CNN: Detection Plus Instance Masks", "order": 17},
            {"id": "ocr", "title": "OCR: From Characters to Detection-and-Recognition Pipelines", "order": 18},
            {"id": "mediapipe-landmarks", "title": "Face and Hand Landmarks with MediaPipe", "order": 19},
            {"id": "fomm", "title": "Motion Transfer with the First Order Motion Model", "order": 20},
            {"id": "damage-yolov8", "title": "Car-Damage Segmentation with YOLOv8", "order": 21},
        ],
    },

    "exercises": [
        {
            "id": "M12.L01.EX01",

            "title": "Compare Visual Representations Across Learning Paradigms",

            "lesson_code": "M12.L01",

            "section_id": "mae-selfsupervised",

            "placement": "after_section",

            "description": (
                "Build intuition for representation quality by comparing supervised, "
                "zero/few-shot, uncertainty-aware, semi-supervised, and self-supervised features."
            ),

            "instructions": (
                "1. Choose a small image dataset with at least three classes.\n"
                "2. Extract pretrained CNN embeddings for a subset of images and visualize them with PCA and t-SNE.\n"
                "3. Compare the separation of raw-pixel t-SNE with deep-feature t-SNE.\n"
                "4. Run a CLIP zero-shot classification example using descriptive text prompts.\n"
                "5. Build class prototypes from two or three support images per class using "
                "a pretrained embedding model such as DINOv2 or another source-aligned encoder.\n"
                "6. Classify query images by cosine similarity to prototypes.\n"
                "7. If practical, run MC Dropout on a small classifier and compare uncertainty "
                "for an easy input and an ambiguous/noisy input.\n"
                "8. Create one pseudo-labeling experiment where low-confidence unlabeled "
                "predictions are rejected.\n"
                "9. Visualize a masked-patch reconstruction or pretrained MAE representation.\n"
                "10. Summarize which representation method is most useful for visualization, "
                "zero-shot classification, few-shot classification, uncertainty, and unlabeled-data learning."
            ),

            "expected_output": (
                "A notebook/report containing at least one embedding visualization, one "
                "zero/few-shot experiment, one uncertainty or pseudo-labeling experiment, "
                "one self-supervised representation example, and a comparison table."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "embeddings",
                "pca",
                "tsne",
                "clip",
                "few-shot-learning",
                "cosine-similarity",
                "mc-dropout",
                "pseudo-labeling",
                "mae",
            ],
        },

        {
            "id": "M12.L01.EX02",

            "title": "Build a Multi-Stage Visual Understanding Pipeline",

            "lesson_code": "M12.L01",

            "section_id": "damage-yolov8",

            "placement": "after_section",

            "description": (
                "Combine representation learning, localization, OCR or landmarks, and "
                "instance masks into one application-oriented computer-vision workflow."
            ),

            "instructions": (
                "1. Choose one application: vehicle inspection, visual search, document/plate "
                "understanding, or human-interaction analysis.\n"
                "2. Identify which stage requires classification, retrieval, detection, "
                "instance segmentation, OCR, or landmark localization.\n"
                "3. Use a pretrained feature extractor or detector from the chapter for the "
                "first stage.\n"
                "4. If your pipeline uses detection, retain class, confidence, and box outputs "
                "and apply a documented confidence threshold.\n"
                "5. If text is present, crop the detected text ROI and compare at least two "
                "OCR strategies conceptually or experimentally.\n"
                "6. If instance geometry is important, use a mask-based method and compute one "
                "measurement such as area or contour size.\n"
                "7. If human geometry is important, use face/hand landmarks rather than only boxes.\n"
                "8. Add one robustness check: ambiguous image, low confidence, adversarial/noisy "
                "perturbation, domain shift, or out-of-distribution input.\n"
                "9. Separate clearly what the neural model predicts from any downstream "
                "rule-based decision logic.\n"
                "10. Finish with an architecture diagram and failure-analysis table."
            ),

            "expected_output": (
                "A notebook/report with a complete multi-stage vision pipeline, intermediate "
                "outputs, at least one quantitative or confidence-based check, and a diagram "
                "showing learned predictions versus rule-based downstream logic."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "object-detection",
                "instance-segmentation",
                "ocr",
                "landmarks",
                "semantic-retrieval",
                "confidence-thresholding",
                "robustness",
                "pipeline-design",
            ],
        },
    ],

    "quiz": {
        "id": "M12.L01.QZ01",

        "title": "Image Classification and Object Detection — Knowledge Check",

        "lesson_code": "M12.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M12.L01.Q01",
                "section_id": "embedding-space",
                "question": "What is the main purpose of an image embedding?",
                "options": [
                    "Represent visual content as a numerical feature vector whose geometry can encode similarity",
                    "Store the JPEG filename",
                    "Replace every image with one pixel",
                    "Guarantee perfect classification",
                ],
                "correct": 0,
                "explanation": (
                    "Embeddings provide a reusable numerical representation for classification, retrieval, matching, and clustering."
                ),
            },

            {
                "id": "M12.L01.Q02",
                "section_id": "pca-tsne",
                "question": "What is a key difference between PCA and t-SNE?",
                "options": [
                    "PCA is linear and variance-oriented, while t-SNE is nonlinear and emphasizes local neighborhoods",
                    "t-SNE is a supervised classifier",
                    "PCA only works on images with labels",
                    "They are identical algorithms",
                ],
                "correct": 0,
                "explanation": (
                    "The source contrasts PCA's linear projection with t-SNE's nonlinear neighborhood-preserving visualization."
                ),
            },

            {
                "id": "M12.L01.Q03",
                "section_id": "classification-transfer",
                "question": "What is usually frozen first in simple transfer learning?",
                "options": [
                    "The pretrained feature-extraction backbone",
                    "The new task-specific head only",
                    "The dataset labels",
                    "The optimizer",
                ],
                "correct": 0,
                "explanation": (
                    "The pretrained backbone can be held fixed while the new target-task classifier is trained."
                ),
            },

            {
                "id": "M12.L01.Q04",
                "section_id": "attention-classification",
                "question": "What question does channel attention answer conceptually?",
                "options": [
                    "Which feature maps are most useful?",
                    "Where is every bounding box?",
                    "Which client owns the data?",
                    "Which OCR language is installed?",
                ],
                "correct": 0,
                "explanation": (
                    "Channel attention weights feature channels; spatial attention weights positions."
                ),
            },

            {
                "id": "M12.L01.Q05",
                "section_id": "vit-swin",
                "question": "Why does Swin Transformer use local shifted windows?",
                "options": [
                    "To reduce the cost of global attention while still exchanging information across windows",
                    "To remove patch embeddings",
                    "To perform OCR only",
                    "To replace all learned parameters with rules",
                ],
                "correct": 0,
                "explanation": (
                    "Windowed attention improves efficiency, while shifting supports cross-window interaction."
                ),
            },

            {
                "id": "M12.L01.Q06",
                "section_id": "few-shot-clip-dino",
                "question": "How does CLIP perform zero-shot classification?",
                "options": [
                    "It compares an image embedding with candidate text embeddings",
                    "It trains from scratch on one image",
                    "It uses only PCA",
                    "It predicts a bounding box first",
                ],
                "correct": 0,
                "explanation": (
                    "The class prompt with the strongest image-text similarity is selected."
                ),
            },

            {
                "id": "M12.L01.Q07",
                "section_id": "few-shot-clip-dino",
                "question": "What is a class prototype in the chapter's DINOv2 few-shot example?",
                "options": [
                    "The average embedding of a few support images from that class",
                    "A handwritten rule",
                    "A detection anchor",
                    "A dropout mask",
                ],
                "correct": 0,
                "explanation": (
                    "Support embeddings are averaged to create a representative vector."
                ),
            },

            {
                "id": "M12.L01.Q08",
                "section_id": "bayesian-uncertainty",
                "question": "What does MC Dropout do during inference?",
                "options": [
                    "Keeps dropout active and performs multiple stochastic forward passes",
                    "Disables all model randomness",
                    "Replaces weights with PCA components",
                    "Only calculates training accuracy",
                ],
                "correct": 0,
                "explanation": (
                    "Variation across stochastic passes can be used as an approximate uncertainty signal."
                ),
            },

            {
                "id": "M12.L01.Q09",
                "section_id": "semi-supervised",
                "question": "Why does FixMatch-style learning keep only high-confidence pseudo-labels?",
                "options": [
                    "To reduce the risk of training on unreliable model guesses",
                    "To ensure every unlabeled sample is used immediately",
                    "To remove data augmentation",
                    "To create adversarial examples",
                ],
                "correct": 0,
                "explanation": (
                    "Incorrect pseudo-labels can reinforce errors, so confidence filtering is important."
                ),
            },

            {
                "id": "M12.L01.Q10",
                "section_id": "mae-selfsupervised",
                "question": "What is the pretraining task of a Masked Autoencoder?",
                "options": [
                    "Reconstruct missing image patches from visible patches",
                    "Predict only ImageNet labels",
                    "Detect license plates",
                    "Average client models",
                ],
                "correct": 0,
                "explanation": (
                    "The image itself supplies the reconstruction target, so no human class label is required."
                ),
            },

            {
                "id": "M12.L01.Q11",
                "section_id": "federated-learning",
                "question": "What is exchanged in the chapter's federated-learning setup?",
                "options": [
                    "Model updates rather than raw client images",
                    "All private datasets",
                    "Only t-SNE coordinates",
                    "Only OCR strings",
                ],
                "correct": 0,
                "explanation": (
                    "Clients train locally and send model parameters/updates to the aggregation server."
                ),
            },

            {
                "id": "M12.L01.Q12",
                "section_id": "adversarial-robustness",
                "question": "What information does FGSM use to choose its perturbation direction?",
                "options": [
                    "The sign of the loss gradient with respect to the input image",
                    "The average image color only",
                    "A random t-SNE cluster",
                    "A face landmark graph",
                ],
                "correct": 0,
                "explanation": (
                    "FGSM perturbs the image in the sign direction that increases the loss."
                ),
            },

            {
                "id": "M12.L01.Q13",
                "section_id": "semantic-image-search",
                "question": "How does the source's image search engine rank database images?",
                "options": [
                    "By similarity between learned feature embeddings",
                    "By filename length",
                    "By exact pixel equality",
                    "By OCR confidence only",
                ],
                "correct": 0,
                "explanation": (
                    "The retrieval task becomes nearest-neighbor search in learned representation space."
                ),
            },

            {
                "id": "M12.L01.Q14",
                "section_id": "object-detection",
                "question": "What does object detection add beyond image classification?",
                "options": [
                    "Spatial localization of each detected object",
                    "Only lower-dimensional PCA",
                    "Only uncertainty",
                    "Only image reconstruction",
                ],
                "correct": 0,
                "explanation": (
                    "Detection predicts both object identity and bounding-box location."
                ),
            },

            {
                "id": "M12.L01.Q15",
                "section_id": "retinanet",
                "question": "Why is focal loss useful in RetinaNet?",
                "options": [
                    "It downweights easy examples so hard foreground/background cases matter more",
                    "It generates OCR strings",
                    "It computes hand landmarks",
                    "It performs federated averaging",
                ],
                "correct": 0,
                "explanation": (
                    "Dense one-stage detection creates many easy background examples that would otherwise dominate the loss."
                ),
            },

            {
                "id": "M12.L01.Q16",
                "section_id": "mask-rcnn",
                "question": "What additional prediction does Mask R-CNN provide beyond a detector's box/class output?",
                "options": [
                    "A pixel-level mask for each instance",
                    "A text caption only",
                    "A PCA embedding only",
                    "A client update",
                ],
                "correct": 0,
                "explanation": (
                    "The mask branch predicts the exact spatial extent of each detected instance."
                ),
            },

            {
                "id": "M12.L01.Q17",
                "section_id": "ocr",
                "question": "Why is license-plate OCR commonly implemented as detection followed by recognition?",
                "options": [
                    "Cropping the plate isolates the relevant text region before character decoding",
                    "OCR cannot process images",
                    "Detection automatically returns the final text",
                    "The plate must be converted to a point cloud first",
                ],
                "correct": 0,
                "explanation": (
                    "Detection localizes the text-bearing ROI and recognition decodes its characters."
                ),
            },

            {
                "id": "M12.L01.Q18",
                "section_id": "mediapipe-landmarks",
                "question": "Why are facial landmarks useful for AR filters?",
                "options": [
                    "They provide stable geometric anchors for position, scale, and alignment",
                    "They provide only an image-level class",
                    "They perform federated averaging",
                    "They eliminate the need for image coordinates",
                ],
                "correct": 0,
                "explanation": (
                    "Landmark coordinates allow virtual elements to follow detailed facial geometry."
                ),
            },

            {
                "id": "M12.L01.Q19",
                "section_id": "fomm",
                "question": "What does FOMM conceptually transfer from the driving video?",
                "options": [
                    "Motion, pose, and expression onto the appearance of the source image",
                    "Only OCR text",
                    "Only ImageNet class labels",
                    "Only PCA components",
                ],
                "correct": 0,
                "explanation": (
                    "The source provides appearance, while the driving sequence supplies motion."
                ),
            },

            {
                "id": "M12.L01.Q20",
                "section_id": "damage-yolov8",
                "type": "open",
                "question": (
                    "Design a vehicle-inspection pipeline that first detects or segments "
                    "damage, then estimates a severity indicator and optionally reads a "
                    "license plate. Separate the learned components from the rule-based "
                    "components, identify which confidence/quality checks you would record, "
                    "and explain why mask area alone should not be interpreted as a complete "
                    "physical or financial damage assessment."
                ),
            },
        ],

        "passing_score": 70,
    },
}
