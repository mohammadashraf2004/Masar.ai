"""M14.L01 — Using Segmentation to Find Suspected Nodules.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 15.
Instructor-authored curriculum adaptation.

Quality standard:
- balanced quiz-answer positions
- explicit train/eval/no_grad/device best practices
- realistic study-time estimate
- learning checkpoints after dense sections
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M14.L01"
MODULE_ORDER = 14
MODULE_TITLE = "Segmentation & Fine-Tuning for Nodule Detection"
MODULE_DESCRIPTION = (
    "Move from candidate classification to automatic localization by learning semantic segmentation, "
    "using Segment Anything for promptable mask generation, adapting 3D CT data into 2D slices, "
    "building a CT-image/mask fine-tuning dataset, and fine-tuning SegFormer for prompt-free nodule segmentation."
)

SOURCE_CHAPTER = 15
SOURCE_PAGES = "Chapter 15 (page range not provided in source excerpt)"


TOPIC = {
    "title": "Using Segmentation to Find Suspected Nodules",
    "slug": "applied-deep-learning-m14-l01",
    "description": (
        "A complete learner-facing lesson on semantic segmentation for CT data, including SAM, prompt encoders, "
        "mask decoders, point prompting, 3D-to-2D adaptation, pseudo-label mask generation, SegFormer fine-tuning, "
        "AdamW, training/validation loops, state_dict persistence, and inference."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 6.5,
    "skill_tags": [
        "semantic-segmentation",
        "instance-segmentation",
        "object-detection",
        "segment-anything",
        "sam",
        "vision-transformer",
        "prompt-encoder",
        "mask-decoder",
        "zero-shot-segmentation",
        "medical-imaging",
        "ct-slices",
        "segformer",
        "fine-tuning",
        "adamw",
        "image-processor",
        "state-dict",
        "inference",
        "module-14",
    ],
    "prerequisite_ids": ["M13.L01"],

    "lesson": {
        "title": "Using Segmentation to Find Suspected Nodules",
        "content": (
            "# Using Segmentation to Find Suspected Nodules\n\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M14.L01  \n"
            "> **Source:** *Deep Learning with PyTorch, Second Edition*, Chapter 15.  \n"
            "> **Study expectation:** about **6.5 hours** including code tracing, checkpoints, exercises, and mask inspection.\n\n"
            "The previous lessons built a candidate classifier. But that classifier still depends on candidate locations supplied by annotations.\n\n"
            "This chapter solves the missing step:\n\n"
            "> **Given a raw CT slice, automatically identify image regions that might contain a nodule.**\n\n"
            "That is a segmentation problem.\n\n"
            "---\n\n"

            "## Learning outcomes\n\n"
            "By the end of this lesson, you should be able to:\n\n"
            "- Explain why segmentation is needed before candidate classification.\n"
            "- Distinguish semantic segmentation, instance segmentation, and object detection.\n"
            "- Explain segmentation as per-pixel classification.\n"
            "- Explain how segmentation output differs structurally from classification output.\n"
            "- Describe Segment Anything (SAM) as a promptable segmentation model.\n"
            "- Identify SAM's image encoder, prompt encoder, and mask decoder.\n"
            "- Explain point, box, and mask prompts.\n"
            "- Use an off-the-shelf pretrained segmentation model for automatic mask generation.\n"
            "- Explain the meaning of SAM's multiple candidate masks and confidence output.\n"
            "- Explain the domain gap between natural-image pretraining and medical imaging.\n"
            "- Convert a 3D CT volume into 2D slices for a 2D segmentation model.\n"
            "- Extract the correct CT slice from candidate XYZ/IRC coordinates.\n"
            "- Build an image/mask dataset for segmentation fine-tuning.\n"
            "- Explain how SAM-generated masks are used as training targets in this chapter.\n"
            "- Explain why SegFormer is used for prompt-free automatic segmentation.\n"
            "- Explain fine-tuning as adapting pretrained features to a new domain/task.\n"
            "- Configure `SegformerForSemanticSegmentation` for background/nodule labels.\n"
            "- Use `SegformerImageProcessor` to prepare images and masks.\n"
            "- Train with AdamW and validate using `eval()` and `torch.no_grad()`.\n"
            "- Save and restore model parameters with `state_dict()`.\n"
            "- Run semantic-segmentation inference and post-process model output back to the desired image size.\n"
            "- Explain how segmentation and classification can work together in a multi-stage detection pipeline.\n\n"
            "---\n\n"

            "## 1. Why classification alone is not enough\n\n"
            "The classifier from earlier chapters answers:\n\n"
            "> **Given this candidate crop, is it a nodule?**\n\n"
            "But it does not answer:\n\n"
            "> **Where should we look in the CT in the first place?**\n\n"
            "So the end-to-end project needs another model before classification:\n\n"
            "```text\n"
            "raw CT scan\n"
            "   ↓\n"
            "segmentation / candidate localization\n"
            "   ↓\n"
            "candidate regions\n"
            "   ↓\n"
            "classification\n"
            "   ↓\n"
            "nodule / non-nodule decision\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Multi-stage CT pipeline with segmentation before classification | Raw CT slice enters a segmentation model, "
            "candidate regions are extracted, then passed into the existing classifier | Learner should notice that segmentation answers "
            "where while classification answers what]]\n\n"
            "The chapter explicitly returns to step 2 of the project pipeline after finishing step 3 first.\n\n"
            "---\n\n"

            "## 2. Why this chapter uses 2D CT slices\n\n"
            "The raw CT data is volumetric, but this chapter intentionally works with 2D slices.\n\n"
            "Reasons include:\n\n"
            "- easier visualization,\n"
            "- easier demonstration,\n"
            "- compatibility with the 2D models used in the chapter,\n"
            "- simpler fine-tuning workflow.\n\n"
            "This choice has tradeoffs because a 2D slice does not contain the full 3D context available in the original scan.\n\n"
            "The chapter accepts that limitation for educational simplicity.\n\n"
            "---\n\n"

            "## 3. Semantic segmentation, instance segmentation, and object detection\n\n"
            "These tasks answer related but different questions.\n\n"
            "### Semantic segmentation\n\n"
            "Assign a class to every pixel.\n\n"
            "For this project:\n\n"
            "```text\n"
            "pixel = nodule candidate\n"
            "or\n"
            "pixel = background / healthy tissue\n"
            "```\n\n"
            "### Instance segmentation\n\n"
            "Separates individual objects of the same class.\n\n"
            "For example, two tumors could be labeled as two separate instances.\n\n"
            "### Object detection\n\n"
            "Finds objects and usually surrounds them with bounding boxes.\n\n"
            "[[IMAGE_NEEDED: Semantic segmentation vs instance segmentation vs object detection | One medical-style image shown three times: "
            "semantic mask labels all tumor pixels as one class, instance segmentation gives separate IDs to separate tumors, and object detection "
            "uses bounding boxes | Learner should distinguish pixel-level categories, object identities, and bounding boxes]]\n\n"
            "The chapter chooses **semantic segmentation** because the immediate need is a pixel-level mask of potentially interesting regions.\n\n"
            "---\n\n"

            "## 4. Segmentation is per-pixel classification\n\n"
            "Image classification compresses a whole image into one or a few class predictions.\n\n"
            "Segmentation preserves spatial structure and predicts a class for each image position.\n\n"
            "Conceptually:\n\n"
            "```text\n"
            "classification:\n"
            "H × W image -> class logits\n\n"
            "segmentation:\n"
            "H × W image -> H × W class map\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Classification versus segmentation output | Same input image feeds two models; classifier returns one class vector, "
            "segmenter returns an image-sized mask | Learner should notice that segmentation must preserve location information throughout the network]]\n\n"
            "This requirement strongly influences model architecture: the final result cannot be reduced to one global class vector.\n\n"

            "### Learning checkpoint 1 — Choose the right vision task\n\n"
            "For each requirement, choose classification, object detection, semantic segmentation, or instance segmentation:\n\n"
            "1. determine whether any nodule exists in a crop,\n"
            "2. draw one box around each suspicious object,\n"
            "3. label every suspicious pixel,\n"
            "4. distinguish tumor A from tumor B at the pixel level.\n\n"
            "{{exercise:M14.L01.EX01}}\n\n"
            "---\n\n"

            "## 5. Segment Anything: a general-purpose segmentation model\n\n"
            "The chapter introduces the **Segment Anything model (SAM)**, released by Meta AI.\n\n"
            "SAM is a promptable segmentation system based on transformer ideas.\n\n"
            "It can:\n\n"
            "- generate masks for objects in an image,\n"
            "- accept point prompts,\n"
            "- accept box prompts,\n"
            "- accept mask prompts,\n"
            "- generalize to unfamiliar objects without task-specific retraining in many settings.\n\n"
            "The chapter frames this as **zero-shot segmentation**.\n\n"
            "SAM's broad capability makes it useful as an off-the-shelf starting point even though the project domain—CT medical imaging—is quite different from ordinary photographs.\n\n"
            "---\n\n"

            "## 6. SAM architecture: image encoder, prompt encoder, mask decoder\n\n"
            "SAM is divided into three main components.\n\n"
            "### 1. Image encoder\n\n"
            "Uses a Vision Transformer to convert image patches into rich image features.\n\n"
            "### 2. Prompt encoder\n\n"
            "Turns prompts—points, boxes, or masks—into embeddings.\n\n"
            "### 3. Mask decoder\n\n"
            "Combines image features and prompt information to produce segmentation masks.\n\n"
            "[[IMAGE_NEEDED: SAM architecture | Input image enters a ViT image encoder; point/box/mask prompts enter a prompt encoder; both "
            "streams meet in a mask decoder that outputs masks and confidence | Learner should understand the three-component division of SAM]]\n\n"
            "This architecture reuses ideas from Chapter 9: token representations, transformer-style attention, and cross-information mixing.\n\n"
            "---\n\n"

            "## 7. Why SAM can return multiple masks\n\n"
            "A prompt can be ambiguous.\n\n"
            "For one point on an object, the intended region might be:\n\n"
            "- the whole object,\n"
            "- one meaningful part,\n"
            "- or a smaller subpart.\n\n"
            "SAM can therefore return several candidate masks and confidence-related values.\n\n"
            "The chapter describes them as often nested at different scales.\n\n"
            "That is an important lesson in segmentation systems: one prompt does not always uniquely define one correct region.\n\n"
            "---\n\n"

            "## 8. Open-source models also bring licensing responsibilities\n\n"
            "The chapter uses SAM from its public implementation and explicitly discusses licensing.\n\n"
            "Important lessons:\n\n"
            "- public code is still copyrighted,\n"
            "- no license does **not** mean public domain,\n"
            "- model code and pretrained weights can have different license terms,\n"
            "- redistribution may require attribution or including license text.\n\n"
            "This is part of production engineering, not an optional legal afterthought.\n\n"
            "Before integrating any pretrained model into a real product, inspect both the implementation license and the weight/data terms.\n\n"
            "---\n\n"

            "## 9. Try SAM off the shelf with automatic mask generation\n\n"
            "The chapter first uses the convenience abstraction:\n\n"
            "```python\n"
            "from segment_anything import (\n"
            "    SamAutomaticMaskGenerator,\n"
            "    sam_model_registry,\n"
            ")\n\n"
            "sam = sam_model_registry[model_config](\n"
            "    checkpoint=model_weights_path\n"
            ")\n"
            "sam.to(device)\n\n"
            "mask_generator = SamAutomaticMaskGenerator(sam)\n"
            "masks = mask_generator.generate(image_array)\n"
            "```\n\n"
            "The automatic generator handles much of the preprocessing and postprocessing.\n\n"
            "In the source example, it produces many image-sized Boolean masks over an ordinary photograph.\n\n"
            "This is useful for understanding the model before manually controlling its prompts.\n\n"
            "---\n\n"

            "## 10. A segmentation mask is an image-sized prediction\n\n"
            "A binary segmentation mask is a 2D array where each location means:\n\n"
            "```text\n"
            "True  -> pixel belongs to the selected object/region\n"
            "False -> pixel does not\n"
            "```\n\n"
            "The mask has the same spatial dimensions as the image after appropriate postprocessing.\n\n"
            "[[IMAGE_NEEDED: Binary segmentation mask | Original image beside a black-and-white mask where the target object is white and "
            "background is black | Learner should see that every output pixel corresponds spatially to the input]]\n\n"
            "The chapter also surfaces a predicted mask-quality/confidence value. This value is a model prediction, not a directly measured ground-truth IoU.\n\n"
            "---\n\n"

            "## 11. Use a point prompt to tell SAM where to look\n\n"
            "For the lung project, generating every possible mask is unnecessary.\n\n"
            "The chapter next uses `SamPredictor` and a point prompt:\n\n"
            "```python\n"
            "predictor = SamPredictor(sam)\n"
            "predictor.set_image(np.array(image))\n\n"
            "input_points = np.array([(320, 260)])\n"
            "masks, _, _ = predictor.predict(\n"
            "    input_points,\n"
            "    point_labels=np.array([1]),\n"
            ")\n"
            "```\n\n"
            "The point is encoded by SAM's prompt encoder and combined with encoded image information.\n\n"
            "[[IMAGE_NEEDED: Point-prompt segmentation | Image with one marked point inside an object and three candidate masks produced around "
            "that region | Learner should notice that the prompt guides which part of the image SAM should segment]]\n\n"
            "This prompt-driven behavior will later help generate masks around known CT nodule locations.\n\n"

            "### Learning checkpoint 2 — SAM mental model\n\n"
            "Explain the data flow:\n\n"
            "```text\n"
            "image -> image encoder ------\\\n"
            "                              -> mask decoder -> mask\n"
            "prompt -> prompt encoder ----/\n"
            "```\n\n"
            "Then answer: why is a point prompt useful for generating training masks from known candidate centers?\n\n"
            "{{exercise:M14.L01.EX02}}\n\n"
            "---\n\n"

            "## 12. General-purpose vision models have a domain gap\n\n"
            "SAM was designed for broad natural-image segmentation.\n\n"
            "CT imagery is very different:\n\n"
            "- grayscale intensity structure,\n"
            "- medical anatomy,\n"
            "- unusual textures,\n"
            "- imaging artifacts,\n"
            "- very small targets.\n\n"
            "The chapter explicitly notes that good performance on natural images does not guarantee equal performance on medical images.\n\n"
            "Researchers have created medical adaptations of SAM for exactly this reason.\n\n"
            "For this educational project, the source chooses a simple workable approach rather than pursuing the most specialized possible medical architecture.\n\n"
            "---\n\n"

            "## 13. Adapt 3D CT data to a 2D segmentation model\n\n"
            "SAM expects 2D images, while CT is a 3D volume.\n\n"
            "The chapter handles this by selecting one 2D slice containing the candidate center.\n\n"
            "Conceptually:\n\n"
            "```text\n"
            "3D CT volume D × H × W\n"
            "         ↓ choose one index\n"
            "2D CT slice H × W\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Extracting one 2D CT slice from a 3D volume | CT volume shown as stacked slices with one highlighted slice at the "
            "candidate depth; highlighted slice is pulled out as a 2D image | Learner should see the adaptation required for a 2D model]]\n\n"
            "This loses some 3D information, but it greatly simplifies the segmentation demonstration.\n\n"
            "---\n\n"

            "## 14. Extract the candidate-centered CT slice\n\n"
            "The source first converts the known physical candidate center into IRC coordinates:\n\n"
            "```python\n"
            "center_irc = xyz2irc(\n"
            "    center_xyz,\n"
            "    self.origin_xyz,\n"
            "    self.vxSize_xyz,\n"
            "    self.direction_a,\n"
            ")\n"
            "```\n\n"
            "Then it selects one index along an axis:\n\n"
            "```python\n"
            "center_val = int(round(center_irc[axis]))\n\n"
            "if axis == 0:\n"
            "    ct_slice = self.hu_a[center_val, :, :]\n"
            "elif axis == 1:\n"
            "    ct_slice = self.hu_a[:, center_val, :]\n"
            "elif axis == 2:\n"
            "    ct_slice = self.hu_a[:, :, center_val]\n"
            "```\n\n"
            "The expected example shape is:\n\n"
            "```text\n"
            "512 × 512\n"
            "```\n\n"
            "The geometry utilities built in earlier chapters are being reused rather than reinvented.\n\n"
            "---\n\n"

            "## 15. Cache deterministic slice extraction\n\n"
            "CT slice loading can be expensive, so the chapter uses the same caching principle as earlier:\n\n"
            "```python\n"
            "@raw_cache.memoize(typed=True)\n"
            "def getCtSlice(series_uid, center_xyz):\n"
            "    ct = getCt(series_uid)\n"
            "    ct_slice, center_irc = ct.getSingleSlice(center_xyz)\n"
            "    return ct_slice, center_irc\n"
            "```\n\n"
            "The deterministic source slice is worth caching because it can be reused repeatedly during later dataset generation.\n\n"
            "---\n\n"

            "## 16. We have point labels—but segmentation needs masks\n\n"
            "The original LUNA metadata gives the project a candidate center point.\n\n"
            "But semantic segmentation requires a dense target:\n\n"
            "```text\n"
            "one label for every pixel\n"
            "```\n\n"
            "Manually drawing masks for hundreds of CT slices would be expensive.\n\n"
            "The chapter therefore uses the pretrained SAM model to transform known candidate points into segmentation masks.\n\n"
            "This creates an image/mask dataset suitable for fine-tuning another segmentation model.\n\n"
            "In the chapter's pipeline, SAM is effectively used as a mask-generation teacher/tool for constructing training targets.\n\n"
            "---\n\n"

            "## 17. Build the fine-tuning dataset: image-mask pairs\n\n"
            "The final fine-tuning data consists of aligned pairs:\n\n"
            "```text\n"
            "CT slice image <-> nodule mask\n"
            "```\n\n"
            "The source stores them in separate directories:\n\n"
            "```text\n"
            "fine-tuning/\n"
            "  dataset/\n"
            "    ct/\n"
            "    mask/\n"
            "    metadata.jsonl\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Fine-tuning dataset layout | Folder tree with CT images, mask images, and metadata.jsonl; one metadata record links "
            "series UID and center IRC to matching image and mask paths | Learner should understand the pairing and traceability structure]]\n\n"
            "The exact folder structure is less important than maintaining an unambiguous relationship between each image and its target mask.\n\n"
            "---\n\n"

            "## 18. Convert CT slices into image files\n\n"
            "The source converts the CT tensor into a format suitable for PIL image handling.\n\n"
            "A channel-first tensor needs to become height-width-channel for PIL:\n\n"
            "```python\n"
            "ct_image_array = np.transpose(\n"
            "    scaled_ct_slice.numpy(),\n"
            "    (1, 2, 0),\n"
            ")\n"
            "ct_image = Image.fromarray(\n"
            "    ct_image_array,\n"
            "    mode='RGB',\n"
            ")\n"
            "```\n\n"
            "This is another example of boundary conversion between library conventions: PyTorch and PIL commonly expect different axis orders.\n\n"
            "---\n\n"

            "## 19. Generate target masks with SAM point prompts\n\n"
            "The source converts the candidate center to the point coordinate expected by the image:\n\n"
            "```python\n"
            "x, y = center_irc[2], center_irc[1]\n"
            "input_points = [[x, y]]\n"
            "```\n\n"
            "Then SAM generates a binary mask:\n\n"
            "```python\n"
            "predictor.set_image(ct_image_array)\n"
            "masks, _, _ = predictor.predict(\n"
            "    point_coords=np.array(input_points),\n"
            "    point_labels=np.array([1]),\n"
            "    multimask_output=False,\n"
            ")\n"
            "```\n\n"
            "The resulting mask is saved as the target paired with the CT slice.\n\n"
            "The source emphasizes that pixel-perfect clinical masks are not the primary goal here; the project needs useful candidate regions for the downstream classifier.\n\n"
            "{{exercise:M14.L01.EX03}}\n\n"
            "---\n\n"

            "## 20. Keep metadata linking images, masks, and original CT context\n\n"
            "The dataset metadata retains information such as:\n\n"
            "- series UID,\n"
            "- center IRC,\n"
            "- CT image path,\n"
            "- mask image path.\n\n"
            "This preserves traceability back to the original CT source.\n\n"
            "A `FineTuning` dataset can then return file paths and metadata cleanly without regenerating masks every epoch.\n\n"
            "This is a good data-engineering separation:\n\n"
            "```text\n"
            "expensive dataset construction\n"
            "        ↓\n"
            "stable image/mask artifact set\n"
            "        ↓\n"
            "lightweight training Dataset\n"
            "```\n\n"

            "### Learning checkpoint 3 — From CT annotations to segmentation targets\n\n"
            "Explain this chain:\n\n"
            "```text\n"
            "3D CT + candidate XYZ\n"
            " -> IRC conversion\n"
            " -> 2D CT slice\n"
            " -> point prompt\n"
            " -> SAM mask\n"
            " -> image/mask pair\n"
            " -> metadata.jsonl\n"
            "```\n\n"
            "If you understand every arrow, the fine-tuning stage becomes straightforward.\n\n"
            "---\n\n"

            "## 21. Why fine-tune SegFormer instead of prompting SAM forever?\n\n"
            "SAM requires a prompt telling it where to segment.\n\n"
            "But the end goal is **automatic nodule segmentation on unseen CT slices without a manually supplied point**.\n\n"
            "The chapter therefore uses the SAM-generated image/mask dataset to fine-tune **SegFormer**.\n\n"
            "SegFormer is a transformer-based semantic-segmentation model designed to produce dense segmentation output efficiently.\n\n"
            "The pipeline becomes:\n\n"
            "```text\n"
            "SAM + known point prompts\n"
            "    ↓\n"
            "generate training masks\n"
            "    ↓\n"
            "fine-tune SegFormer\n"
            "    ↓\n"
            "prompt-free automatic segmentation\n"
            "```\n\n"
            "[[IMAGE_NEEDED: SAM as mask teacher and SegFormer as deployable segmenter | Known point prompts plus CT slices go through SAM to create "
            "training masks; those image-mask pairs train SegFormer; trained SegFormer later receives only a CT image | Learner should see why the "
            "second model removes the prompt requirement]]\n\n"
            "---\n\n"

            "## 22. Fine-tuning adapts pretrained knowledge to a new domain\n\n"
            "Fine-tuning means starting from a pretrained model and continuing training on a more specific dataset/task.\n\n"
            "Benefits:\n\n"
            "- pretrained features provide a useful starting point,\n"
            "- less task-specific data may be needed,\n"
            "- training can be faster than learning everything from random initialization.\n\n"
            "The chapter uses a pretrained SegFormer checkpoint and adapts it to two labels:\n\n"
            "```python\n"
            "id2label = {\n"
            "    '0': 'background',\n"
            "    '1': 'nodule',\n"
            "}\n"
            "label2id = {v: k for k, v in id2label.items()}\n"
            "```\n\n"
            "---\n\n"

            "## 23. Configure SegFormer for two-class semantic segmentation\n\n"
            "The source uses:\n\n"
            "```python\n"
            "from transformers import SegformerForSemanticSegmentation\n\n"
            "model = SegformerForSemanticSegmentation.from_pretrained(\n"
            "    'nvidia/mit-b0',\n"
            "    num_labels=2,\n"
            "    id2label=id2label,\n"
            "    label2id=label2id,\n"
            ")\n"
            "model.to(device)\n"
            "```\n\n"
            "Some segmentation-head weights are newly initialized because the generic pretrained checkpoint is being adapted to the new downstream label setup.\n\n"
            "The source treats this warning as expected: those task-specific weights must be learned during fine-tuning.\n\n"
            "[[IMAGE_NEEDED: SegFormer encoder-decoder overview | CT image passes through transformer-style encoder stages at multiple scales, "
            "then a lightweight decoder fuses features and outputs a two-class pixel mask | Learner should understand that segmentation retains "
            "multi-scale spatial information rather than collapsing to one class vector]]\n\n"
            "---\n\n"

            "## 24. Use AdamW for fine-tuning\n\n"
            "The source uses:\n\n"
            "```python\n"
            "optimizer = torch.optim.AdamW(\n"
            "    model.parameters(),\n"
            "    lr=0.00006,\n"
            ")\n"
            "```\n\n"
            "Adam maintains adaptive parameter-wise update statistics.\n\n"
            "AdamW adds decoupled weight decay behavior and is widely used for transformer training/fine-tuning.\n\n"
            "The chapter follows the SegFormer paper's optimizer choice and learning-rate scale rather than trying to exhaustively search optimizers.\n\n"
            "The practical lesson is that optimizer choice matters, but experimental discipline matters more than chasing every optimizer variant.\n\n"
            "---\n\n"

            "## 25. Let the model's image processor enforce input conventions\n\n"
            "SegFormer expects images and masks in a specific format.\n\n"
            "The source uses:\n\n"
            "```python\n"
            "image_processor = SegformerImageProcessor()\n\n"
            "def encode_inputs_for_model(image_paths, masks_paths=[]):\n"
            "    images = [Image.open(path) for path in image_paths]\n"
            "    masks = [Image.open(path) for path in masks_paths] or None\n\n"
            "    encoded = image_processor(\n"
            "        images,\n"
            "        masks,\n"
            "        return_tensors='pt',\n"
            "    )\n\n"
            "    return (\n"
            "        encoded['pixel_values'].to(device),\n"
            "        encoded['labels'].to(device),\n"
            "    )\n"
            "```\n\n"
            "The processor handles transformations such as resizing, normalization, and conversion into model-ready tensors.\n\n"
            "Using the processor associated with a pretrained model reduces the risk of silently violating the model's expected preprocessing conventions.\n\n"
            "---\n\n"

            "## 26. Fine-tuning loop\n\n"
            "The training loop follows the familiar PyTorch pattern:\n\n"
            "```python\n"
            "for epoch in range(num_epochs):\n"
            "    model.train()\n\n"
            "    total_train_loss = 0.0\n"
            "    num_train_batches = 0\n\n"
            "    for batch in train_dataloader:\n"
            "        pixel_values, labels = encode_inputs_for_model(\n"
            "            batch['ct_image_path'],\n"
            "            batch['mask_image_path'],\n"
            "        )\n\n"
            "        optimizer.zero_grad(set_to_none=True)\n"
            "        outputs = model(\n"
            "            pixel_values=pixel_values,\n"
            "            labels=labels,\n"
            "        )\n"
            "        loss = outputs.loss\n"
            "        loss.backward()\n"
            "        optimizer.step()\n\n"
            "        total_train_loss += loss.item()\n"
            "        num_train_batches += 1\n"
            "```\n\n"
            "The chapter uses 20 epochs in its demonstration.\n\n"
            "Our Masar version makes `zero_grad(set_to_none=True)` explicit as the preferred clean gradient-reset pattern.\n\n"
            "---\n\n"

            "## 27. Validation loop: `eval()` + `no_grad()`\n\n"
            "Validation uses the same image/mask preprocessing but no optimization:\n\n"
            "```python\n"
            "model.eval()\n"
            "total_val_loss = 0.0\n\n"
            "with torch.no_grad():\n"
            "    for batch in val_dataloader:\n"
            "        pixel_values, labels = encode_inputs_for_model(\n"
            "            batch['ct_image_path'],\n"
            "            batch['mask_image_path'],\n"
            "        )\n\n"
            "        outputs = model(\n"
            "            pixel_values=pixel_values,\n"
            "            labels=labels,\n"
            "        )\n"
            "        total_val_loss += outputs.loss.item()\n"
            "```\n\n"
            "The source observes decreasing training and validation loss during fine-tuning, suggesting that the model is learning useful behavior rather than merely memorizing the training examples in the shown run.\n\n"
            "[[IMAGE_NEEDED: Fine-tuning train and validation loss curves | Two TensorBoard-style curves for SegFormer training and validation loss "
            "both trending downward | Learner should inspect whether validation follows training rather than diverging upward]]\n\n"
            "{{exercise:M14.L01.EX04}}\n\n"
            "---\n\n"

            "## 28. Save model parameters, not the entire Python object\n\n"
            "The source recommends:\n\n"
            "```python\n"
            "torch.save(\n"
            "    model.state_dict(),\n"
            "    'segformer_epoch_20.pt',\n"
            ")\n"
            "```\n\n"
            "`state_dict()` maps parameter names to tensors.\n\n"
            "Saving parameters rather than pickling the entire model object gives more flexibility and reduces coupling to the exact Python object representation.\n\n"
            "The chapter also notes that checkpoints can include more than model weights—for example optimizer state, timestamp, and training step—to support resuming interrupted training.\n\n"
            "---\n\n"

            "## 29. Restore the same model configuration and load its state\n\n"
            "To reload:\n\n"
            "```python\n"
            "model = SegformerForSemanticSegmentation.from_pretrained(\n"
            "    'nvidia/mit-b0',\n"
            "    num_labels=2,\n"
            "    id2label=id2label,\n"
            "    label2id=label2id,\n"
            ")\n\n"
            "state_dict = torch.load(\n"
            "    'segformer_epoch_20.pt',\n"
            "    map_location=device,\n"
            ")\n"
            "model.load_state_dict(state_dict)\n"
            "model.to(device)\n"
            "```\n\n"
            "The architecture and parameter names/shapes must remain compatible with the saved state.\n\n"
            "---\n\n"

            "## 30. Run segmentation inference on unseen slices\n\n"
            "Inference follows the same best practices:\n\n"
            "```python\n"
            "model.eval()\n\n"
            "pixel_values = image_processor(\n"
            "    images=image,\n"
            "    return_tensors='pt',\n"
            ").pixel_values.to(device)\n\n"
            "with torch.no_grad():\n"
            "    outputs = model(pixel_values=pixel_values)\n"
            "```\n\n"
            "Then the source uses the processor's post-processing function to resize the semantic map back to the target image size:\n\n"
            "```python\n"
            "predicted_map = image_processor.post_process_semantic_segmentation(\n"
            "    outputs,\n"
            "    target_sizes=[(512, 512)],\n"
            ")[0]\n"
            "```\n\n"
            "[[IMAGE_NEEDED: SegFormer inference comparison | Three panels: CT slice, target mask, predicted segmentation map | Learner should "
            "visually compare whether the predicted region overlaps the target nodule area]]\n\n"
            "The model now produces segmentation without requiring the SAM point prompt.\n\n"

            "### Learning checkpoint 4 — Fine-tuning lifecycle\n\n"
            "Explain this complete lifecycle:\n\n"
            "```text\n"
            "pretrained SegFormer\n"
            " -> configure 2 labels\n"
            " -> preprocess image/mask pairs\n"
            " -> train with AdamW\n"
            " -> validate read-only\n"
            " -> save state_dict\n"
            " -> reconstruct model\n"
            " -> load state_dict\n"
            " -> inference\n"
            "```\n\n"
            "{{exercise:M14.L01.EX05}}\n\n"
            "---\n\n"

            "## 31. Segmentation and classification are complementary\n\n"
            "The project deliberately uses two models because the tasks are different:\n\n"
            "```text\n"
            "SEGMENTATION\n"
            "Where might a candidate be?\n"
            "       ↓\n"
            "candidate regions\n"
            "       ↓\n"
            "CLASSIFICATION\n"
            "Is this candidate actually a nodule?\n"
            "```\n\n"
            "The segmentation stage is allowed to be generous and flag many possible regions because the classifier can reject false candidates later.\n\n"
            "This is a practical multi-stage design strategy: one model prioritizes localization, the other prioritizes discrimination.\n\n"
            "---\n\n"

            "## 32. Complete segmentation engineering blueprint\n\n"
            "```text\n"
            "RAW 3D CT + known annotations\n"
            "       ↓\n"
            "extract 2D slice\n"
            "       ↓\n"
            "use candidate center as SAM point prompt\n"
            "       ↓\n"
            "generate binary segmentation mask\n"
            "       ↓\n"
            "save CT image + mask + metadata\n"
            "       ↓\n"
            "load FineTuningDataset\n"
            "       ↓\n"
            "SegformerImageProcessor\n"
            "       ↓\n"
            "fine-tune pretrained SegFormer with AdamW\n"
            "       ↓\n"
            "monitor train/validation loss\n"
            "       ↓\n"
            "save state_dict\n"
            "       ↓\n"
            "prompt-free segmentation inference\n"
            "       ↓\n"
            "candidate regions for classifier\n"
            "```\n\n"
            "This chapter's deeper lesson is reusable far beyond medical imaging:\n\n"
            "> **A strong pretrained model can be used not only directly, but also as a tool for creating labels that help adapt a lighter task-specific model.**\n\n"
            "---\n\n"

            "## Important misconceptions\n\n"
            "### Misconception 1: Segmentation is just classification with more classes\n\n"
            "Segmentation differs structurally because the output must preserve spatial correspondence with the input image.\n\n"
            "### Misconception 2: Object detection and semantic segmentation are interchangeable\n\n"
            "Detection usually produces boxes, while semantic segmentation predicts labels at pixel level.\n\n"
            "### Misconception 3: SAM will automatically be perfect on CT images because it is a foundation model\n\n"
            "The chapter explicitly discusses the domain gap between natural-image pretraining and medical imaging.\n\n"
            "### Misconception 4: A point prompt and a segmentation mask are the same target representation\n\n"
            "A point is sparse guidance. A mask is a dense per-pixel target.\n\n"
            "### Misconception 5: Fine-tuning always means training every parameter from scratch\n\n"
            "Fine-tuning begins from pretrained weights and adapts them to the target task/domain.\n\n"
            "### Misconception 6: The model's image processor is optional boilerplate\n\n"
            "The processor enforces preprocessing conventions such as resizing, normalization, and label formatting expected by the pretrained model.\n\n"
            "### Misconception 7: Validation should perform optimizer updates if loss is bad\n\n"
            "Validation is read-only. It uses `eval()` and `no_grad()` and never updates weights.\n\n"
            "### Misconception 8: Saving the entire model object is always preferable\n\n"
            "The source recommends saving model parameters through `state_dict()` for flexibility.\n\n"
            "### Misconception 9: Segmentation replaces classification in this project\n\n"
            "Segmentation proposes locations; classification still rejects many false candidate regions.\n\n"
            "---\n\n"

            "## Key terminology\n\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Semantic segmentation | Assigning a class label to every pixel without distinguishing separate instances. |\n"
            "| Instance segmentation | Pixel-level segmentation that distinguishes individual object instances. |\n"
            "| Object detection | Locating objects, typically with bounding boxes. |\n"
            "| Segmentation mask | Image-sized map identifying pixels belonging to a class/region. |\n"
            "| Segment Anything (SAM) | Promptable transformer-based segmentation foundation model. |\n"
            "| Image encoder | SAM component extracting image features. |\n"
            "| Prompt encoder | SAM component converting points, boxes, or masks into embeddings. |\n"
            "| Mask decoder | SAM component combining image and prompt representations to generate masks. |\n"
            "| Zero-shot segmentation | Segmenting new objects/domains without task-specific fine-tuning. |\n"
            "| Point prompt | Coordinate supplied to guide segmentation toward a region of interest. |\n"
            "| Domain gap | Difference between source/pretraining data and target-domain data. |\n"
            "| Fine-tuning | Continuing training from pretrained weights on a task/domain-specific dataset. |\n"
            "| SegFormer | Transformer-based semantic segmentation model used for prompt-free CT segmentation. |\n"
            "| AdamW | Adam-family optimizer with decoupled weight decay. |\n"
            "| Image processor | Model-specific preprocessing/postprocessing utility. |\n"
            "| `state_dict` | Mapping of registered model state such as learned parameter tensors. |\n"
            "| Post-processing | Converting raw model outputs back into task-meaningful image-sized predictions. |\n\n"
            "---\n\n"

            "## Self-check\n\n"
            "1. Why does the project need segmentation in addition to classification?\n"
            "2. What question does semantic segmentation answer that classification does not?\n"
            "3. What is the difference between semantic and instance segmentation?\n"
            "4. What is the difference between segmentation and object detection?\n"
            "5. Why does segmentation output preserve spatial dimensions?\n"
            "6. What is SAM designed to do?\n"
            "7. What are SAM's three main architectural components?\n"
            "8. What does the image encoder process?\n"
            "9. What does the prompt encoder process?\n"
            "10. What does the mask decoder output?\n"
            "11. Why can SAM return multiple masks for one prompt?\n"
            "12. What is zero-shot segmentation?\n"
            "13. Why should open-source model licenses be reviewed separately from model functionality?\n"
            "14. What is the purpose of `SamAutomaticMaskGenerator`?\n"
            "15. What does a binary mask's `True` value represent?\n"
            "16. Why is a point prompt useful in this CT workflow?\n"
            "17. Why is natural-image pretraining not guaranteed to transfer perfectly to CT images?\n"
            "18. Why does this chapter use 2D slices instead of full 3D volumes?\n"
            "19. How is the candidate's CT slice selected from the 3D scan?\n"
            "20. Why is deterministic slice extraction cached?\n"
            "21. What supervision does the original dataset provide, and what supervision does segmentation require?\n"
            "22. How does SAM help bridge that supervision gap in the chapter?\n"
            "23. What files make up the generated fine-tuning dataset?\n"
            "24. Why preserve series UID and center metadata?\n"
            "25. Why is SegFormer fine-tuned after SAM has already generated masks?\n"
            "26. What is fine-tuning?\n"
            "27. What two output labels are configured for SegFormer?\n"
            "28. Why are some SegFormer weights newly initialized in the source setup?\n"
            "29. Why does the chapter choose AdamW?\n"
            "30. What does `SegformerImageProcessor` handle?\n"
            "31. What is the standard train-step order in this lesson?\n"
            "32. Why must validation use `model.eval()`?\n"
            "33. Why use `torch.no_grad()` during validation and inference?\n"
            "34. Why save `state_dict()` rather than only pickle the entire model?\n"
            "35. What must be compatible when loading a saved state dictionary?\n"
            "36. Why is segmentation output post-processed back to `(512,512)`?\n"
            "37. How do the segmentation and classification stages complement one another?\n"
            "38. What broader transfer-learning pattern does the chapter demonstrate by using SAM-generated masks to train SegFormer?\n\n"
            "---\n\n"

            "## Retain this idea\n\n"
            "**Segmentation changes the problem from 'what is in this image?' to 'where is it?'. In this chapter, a powerful promptable model "
            "is first used to turn sparse candidate points into dense masks; those masks become supervision for a lighter task-specific SegFormer "
            "that can later segment new CT slices automatically. The result is a reusable pattern: use pretrained models, domain-aware data engineering, "
            "fine-tuning, and careful inference to build one stage of a larger ML system.**\n"
        ),

        "estimated_minutes": 390,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-segmentation", "title": "Why segmentation is needed", "order": 1},
            {"id": "why-2d", "title": "Why use 2D CT slices", "order": 2},
            {"id": "segmentation-types", "title": "Types of segmentation and detection", "order": 3},
            {"id": "pixel-classification", "title": "Per-pixel classification", "order": 4},
            {"id": "sam-intro", "title": "Introducing Segment Anything", "order": 5},
            {"id": "sam-architecture", "title": "SAM architecture", "order": 6},
            {"id": "sam-multiple-masks", "title": "Multiple mask outputs", "order": 7},
            {"id": "licenses", "title": "Open-source licensing", "order": 8},
            {"id": "automatic-mask-generator", "title": "Automatic mask generation", "order": 9},
            {"id": "mask-output", "title": "Understanding mask output", "order": 10},
            {"id": "point-prompt", "title": "Point-prompt segmentation", "order": 11},
            {"id": "domain-gap", "title": "General-purpose models and medical imaging", "order": 12},
            {"id": "ct-3d-to-2d", "title": "Adapting 3D CT to 2D", "order": 13},
            {"id": "single-slice", "title": "Extracting a CT slice", "order": 14},
            {"id": "slice-cache", "title": "Caching CT slices", "order": 15},
            {"id": "mask-label-problem", "title": "From point labels to dense masks", "order": 16},
            {"id": "fine-tune-dataset", "title": "Building the fine-tuning dataset", "order": 17},
            {"id": "prepare-ct-image", "title": "Preparing CT images", "order": 18},
            {"id": "generate-masks", "title": "Generating masks with SAM", "order": 19},
            {"id": "metadata-jsonl", "title": "Fine-tuning metadata", "order": 20},
            {"id": "why-segformer", "title": "Why SegFormer", "order": 21},
            {"id": "fine-tuning", "title": "Fine-tuning fundamentals", "order": 22},
            {"id": "segformer-model", "title": "Configuring SegFormer", "order": 23},
            {"id": "adamw", "title": "Using AdamW", "order": 24},
            {"id": "image-processor", "title": "SegFormer image processor", "order": 25},
            {"id": "seg-training", "title": "Fine-tuning loop", "order": 26},
            {"id": "seg-validation", "title": "Validation loop", "order": 27},
            {"id": "save-state", "title": "Saving model state", "order": 28},
            {"id": "load-state", "title": "Loading model state", "order": 29},
            {"id": "seg-inference", "title": "Segmentation inference", "order": 30},
            {"id": "seg-plus-classification", "title": "Segmentation plus classification", "order": 31},
            {"id": "chapter-blueprint", "title": "Complete segmentation blueprint", "order": 32},
        ],
    },

    "exercises": [
        {
            "id": "M14.L01.EX01",
            "title": "Choose the Right Vision Task",
            "lesson_code": "M14.L01",
            "section_id": "pixel-classification",
            "placement": "after_section",
            "description": "Distinguish classification, detection, semantic segmentation, and instance segmentation.",
            "instructions": (
                "For eight short scenarios—four from medical imaging and four from everyday vision—choose one of: "
                "image classification, object detection, semantic segmentation, or instance segmentation. "
                "For each choice, specify the desired output shape/structure and explain why another task type would be insufficient."
            ),
            "expected_output": "An eight-row comparison table with task, output, and justification.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["semantic-segmentation", "instance-segmentation", "object-detection", "classification"],
        },
        {
            "id": "M14.L01.EX02",
            "title": "Trace SAM's Prompted Segmentation Flow",
            "lesson_code": "M14.L01",
            "section_id": "point-prompt",
            "placement": "after_section",
            "description": "Build a precise mental model of SAM's three components.",
            "instructions": (
                "Draw or describe the tensor/data flow for a single point-prompt segmentation request. "
                "Start with the RGB image and point coordinates. Identify which information goes to the image encoder, "
                "which goes to the prompt encoder, what the mask decoder receives, and what outputs are produced. "
                "Then explain why one prompt can produce several plausible masks."
            ),
            "expected_output": "A clear architecture trace and explanation of ambiguous/multiple masks.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["sam", "vision-transformer", "prompt-encoder", "mask-decoder"],
        },
        {
            "id": "M14.L01.EX03",
            "title": "Build a Minimal CT Slice-to-Mask Dataset",
            "lesson_code": "M14.L01",
            "section_id": "generate-masks",
            "placement": "after_section",
            "description": "Recreate the chapter's data-engineering path on a tiny synthetic subset.",
            "instructions": (
                "Using three synthetic or available CT-like 2D arrays with known center points, create an output directory with `ct/`, `mask/`, "
                "and `metadata.jsonl`. Save each image and a corresponding binary mask. If SAM is available, generate the masks from point prompts; "
                "otherwise create synthetic masks only to validate the dataset mechanics. Each metadata record must include series UID, center IRC, "
                "CT filename, and mask filename. Load the metadata back and verify every pair exists and has matching spatial dimensions."
            ),
            "expected_output": "A valid tiny paired dataset, metadata file, and integrity-check output.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["dataset-generation", "mask-pairs", "metadata", "data-integrity"],
        },
        {
            "id": "M14.L01.EX04",
            "title": "Write a Correct SegFormer Fine-Tuning Epoch",
            "lesson_code": "M14.L01",
            "section_id": "seg-validation",
            "placement": "after_section",
            "description": "Practice the complete training/validation mode transition.",
            "instructions": (
                "Write one function that performs a training epoch and another that performs a validation epoch. "
                "The training function must call `model.train()`, preprocess image/mask pairs, use `zero_grad(set_to_none=True)`, "
                "backpropagate `outputs.loss`, and step AdamW. The validation function must call `model.eval()`, use `torch.no_grad()`, "
                "never call the optimizer, and return average validation loss. Explain why these mode differences matter."
            ),
            "expected_output": "Two correct epoch functions and a concise explanation of train/eval/no_grad behavior.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["fine-tuning", "adamw", "train-mode", "eval-mode", "no-grad"],
        },
        {
            "id": "M14.L01.EX05",
            "title": "Design the Segmentation-to-Classification Interface",
            "lesson_code": "M14.L01",
            "section_id": "chapter-blueprint",
            "placement": "after_section",
            "description": "Connect the new segmentation model to the existing candidate classifier.",
            "instructions": (
                "Design a pipeline that takes an unseen CT scan, runs 2D segmentation, converts predicted mask regions into candidate centers/crops, "
                "and sends those candidates to the existing 3D classifier. Specify the data passed at each boundary, where coordinate conversion is needed, "
                "how duplicate regions across adjacent slices might be handled conceptually, and what failure modes segmentation can introduce downstream. "
                "Do not invent an exact merging algorithm not supplied by the chapter; mark unresolved design choices explicitly."
            ),
            "expected_output": "A system-interface diagram/table with known transformations, risks, and explicitly unresolved design decisions.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": ["system-design", "segmentation", "classification", "interfaces", "failure-analysis"],
        },
    ],

    "quiz": {
        "id": "M14.L01.QZ01",
        "title": "Segmentation & Fine-Tuning — Knowledge Check",
        "lesson_code": "M14.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M14.L01.Q01",
                "section_id": "segmentation-types",
                "question": "What does semantic segmentation predict?",
                "options": [
                    "One global class for the entire image",
                    "A class label for each pixel",
                    "Only object-center coordinates",
                    "Only one bounding box",
                ],
                "correct": 1,
                "explanation": "Semantic segmentation produces dense per-pixel class predictions.",
            },
            {
                "id": "M14.L01.Q02",
                "section_id": "why-segmentation",
                "question": "Why is segmentation needed before the existing candidate classifier?",
                "options": [
                    "It finds where suspicious regions are so the classifier knows what to inspect.",
                    "It replaces all CT metadata with RGB labels.",
                    "It computes the optimizer learning rate.",
                    "It removes the need for classification.",
                ],
                "correct": 0,
                "explanation": "The classifier evaluates candidates; segmentation is used to locate candidate regions automatically.",
            },
            {
                "id": "M14.L01.Q03",
                "section_id": "sam-architecture",
                "question": "Which SAM component converts point/box/mask prompts into embeddings?",
                "options": [
                    "Image encoder",
                    "Mask decoder",
                    "Prompt encoder",
                    "Optimizer",
                ],
                "correct": 2,
                "explanation": "The prompt encoder transforms sparse or dense guidance into representations used by the mask decoder.",
            },
            {
                "id": "M14.L01.Q04",
                "section_id": "sam-architecture",
                "question": "What is the mask decoder responsible for?",
                "options": [
                    "Reading CT files from disk",
                    "Updating AdamW statistics",
                    "Choosing train/validation splits",
                    "Combining encoded image and prompt information to produce segmentation masks",
                ],
                "correct": 3,
                "explanation": "The mask decoder turns encoded image/prompt information into output masks.",
            },
            {
                "id": "M14.L01.Q05",
                "section_id": "automatic-mask-generator",
                "question": "What is `SamAutomaticMaskGenerator` mainly used for in the chapter?",
                "options": [
                    "Conveniently generating many segmentation masks from an image with SAM.",
                    "Fine-tuning SegFormer.",
                    "Converting XYZ coordinates to IRC.",
                    "Saving optimizer checkpoints.",
                ],
                "correct": 0,
                "explanation": "It wraps preprocessing and mask-generation behavior for off-the-shelf SAM use.",
            },
            {
                "id": "M14.L01.Q06",
                "section_id": "point-prompt",
                "question": "What does a positive point prompt tell SAM?",
                "options": [
                    "Which optimizer to use",
                    "A location belonging to the region/object to segment",
                    "The final mask dimensions only",
                    "The train/validation split index",
                ],
                "correct": 1,
                "explanation": "The point provides spatial guidance about the target region.",
            },
            {
                "id": "M14.L01.Q07",
                "section_id": "domain-gap",
                "question": "Why can SAM's natural-image pretraining be imperfect for CT segmentation?",
                "options": [
                    "SAM cannot process arrays.",
                    "CT images contain no spatial information.",
                    "Medical CT imagery differs substantially from ordinary natural-image data.",
                    "The prompt encoder only supports text.",
                ],
                "correct": 2,
                "explanation": "Different visual statistics and semantics create a domain gap.",
            },
            {
                "id": "M14.L01.Q08",
                "section_id": "ct-3d-to-2d",
                "question": "How does the chapter adapt volumetric CT data for SAM?",
                "options": [
                    "By flattening the full CT into one vector",
                    "By converting every voxel into text tokens",
                    "By discarding all candidate coordinates",
                    "By extracting 2D slices from the 3D volume",
                ],
                "correct": 3,
                "explanation": "The chapter treats individual CT slices as 2D images.",
            },
            {
                "id": "M14.L01.Q09",
                "section_id": "mask-label-problem",
                "question": "What supervision mismatch must the chapter solve?",
                "options": [
                    "The source data gives candidate points, but semantic segmentation needs dense masks.",
                    "SegFormer requires 3D labels only.",
                    "The classifier gives masks while SAM needs class IDs.",
                    "The CT scans have no candidate positions.",
                ],
                "correct": 0,
                "explanation": "SAM is used to turn sparse point information into dense segmentation targets.",
            },
            {
                "id": "M14.L01.Q10",
                "section_id": "fine-tune-dataset",
                "question": "What does each fine-tuning example fundamentally contain?",
                "options": [
                    "Only a class scalar",
                    "A CT image paired with its segmentation mask",
                    "Only a series UID",
                    "A complete 3D CT and no label",
                ],
                "correct": 1,
                "explanation": "Semantic segmentation training needs aligned input images and dense target masks.",
            },
            {
                "id": "M14.L01.Q11",
                "section_id": "why-segformer",
                "question": "Why is SegFormer introduced after SAM?",
                "options": [
                    "To replace CT images with natural photographs",
                    "To create candidate point prompts manually",
                    "To learn prompt-free automatic segmentation from the generated image-mask dataset",
                    "To remove all transformer components",
                ],
                "correct": 2,
                "explanation": "SegFormer is fine-tuned to segment CT slices automatically without an external point prompt.",
            },
            {
                "id": "M14.L01.Q12",
                "section_id": "fine-tuning",
                "question": "What best describes fine-tuning?",
                "options": [
                    "Training only on validation data",
                    "Randomly reinitializing every layer before use",
                    "Saving a model without training",
                    "Continuing training from pretrained weights on a more specific task/domain",
                ],
                "correct": 3,
                "explanation": "Fine-tuning adapts a pretrained representation to the target problem.",
            },
            {
                "id": "M14.L01.Q13",
                "section_id": "adamw",
                "question": "Which optimizer does the chapter use for SegFormer fine-tuning?",
                "options": [
                    "AdamW",
                    "Plain gradient ascent",
                    "RMSProp only",
                    "No optimizer is needed",
                ],
                "correct": 0,
                "explanation": "The source uses AdamW with a small learning rate.",
            },
            {
                "id": "M14.L01.Q14",
                "section_id": "image-processor",
                "question": "What is the role of `SegformerImageProcessor`?",
                "options": [
                    "It downloads LUNA annotations.",
                    "It preprocesses images/masks into the format expected by SegFormer and post-processes outputs.",
                    "It replaces the model's decoder.",
                    "It stores optimizer momentum.",
                ],
                "correct": 1,
                "explanation": "The processor handles model-specific image/mask formatting such as resizing and normalization.",
            },
            {
                "id": "M14.L01.Q15",
                "section_id": "seg-validation",
                "question": "Which validation pattern is correct?",
                "options": [
                    "`model.train()` plus optimizer updates",
                    "Backpropagation without loss",
                    "`model.eval()` with `torch.no_grad()` and no optimizer step",
                    "Randomly reinitialize the segmentation head",
                ],
                "correct": 2,
                "explanation": "Validation measures model behavior without updating parameters or building unnecessary gradient graphs.",
            },
            {
                "id": "M14.L01.Q16",
                "section_id": "save-state",
                "question": "Why does the source save `model.state_dict()`?",
                "options": [
                    "To store the CT images inside the model",
                    "To serialize only TensorBoard charts",
                    "To eliminate the need to recreate model architecture",
                    "To persist model parameters in a flexible form that can later be loaded into a compatible model",
                ],
                "correct": 3,
                "explanation": "A state dictionary stores named learned state and avoids coupling to a pickled whole-model object.",
            },
            {
                "id": "M14.L01.Q17",
                "section_id": "chapter-blueprint",
                "type": "open",
                "question": (
                    "Trace the complete chapter pipeline from an annotated 3D CT candidate to prompt-free SegFormer inference. "
                    "Include slice extraction, SAM point prompting, mask generation, image/mask dataset construction, fine-tuning, "
                    "AdamW, validation, state_dict saving/loading, and final segmentation output."
                ),
            },
        ],
        "passing_score": 70,
    },
}
