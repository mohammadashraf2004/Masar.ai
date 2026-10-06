"""M02.L01 — Pretrained Networks: From Image Recognition to Multimodal Models.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapter 2.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M02.L01"
MODULE_ORDER = 2
MODULE_TITLE = "Pretrained Networks"
MODULE_DESCRIPTION = (
    "Learn how to use pretrained deep learning models without training from scratch, "
    "including image classification, diffusion-based image editing, Hugging Face model "
    "pipelines, and multimodal image captioning."
)

SOURCE_CHAPTER = 2
SOURCE_PAGES = "Chapter 2 (page range not provided in source excerpt)"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Pretrained Networks: From Image Recognition to Multimodal Models",
    "slug": "applied-deep-learning-m02-l01",
    "description": (
        "A practical introduction to pretrained models: how learned weights encode useful "
        "capabilities, how inference pipelines prepare inputs and interpret outputs, and how "
        "pretrained vision, diffusion, language, and multimodal models can be reused."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.beginner,
    "estimated_hours": 2.0,
    "skill_tags": [
        "deep-learning",
        "pytorch",
        "pretrained-models",
        "torchvision",
        "inference",
        "image-classification",
        "vision-transformer",
        "diffusion",
        "inpainting",
        "hugging-face",
        "transformers",
        "multimodal",
        "blip",
        "module-02",
    ],
    "prerequisite_ids": ["M01.L01"],

    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Pretrained Networks: From Image Recognition to Multimodal Models",
        "content": (
            "# Pretrained Networks: From Image Recognition to Multimodal Models\n"
            "\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M02.L01  \n"
            "> **Module:** Pretrained Networks  \n"
            "> **Source alignment:** *Deep Learning with PyTorch, Second Edition*, "
            "Chapter 2. This lesson is an instructor-authored curriculum adaptation "
            "rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain what a pretrained model is and why pretrained weights are valuable.\n"
            "- Distinguish a neural-network architecture from the learned weights stored in it.\n"
            "- Describe the complete inference pipeline for an image classifier.\n"
            "- Prepare an image using resize, crop, tensor conversion, normalization, and batching.\n"
            "- Explain why inference usually requires evaluation mode.\n"
            "- Interpret model scores, class labels, softmax values, and top-k predictions.\n"
            "- Explain why a confident prediction can still be wrong.\n"
            "- Describe the basic idea behind diffusion-based image generation and inpainting.\n"
            "- Explain what a Hugging Face model zoo and pipeline provide.\n"
            "- Describe how a multimodal image-captioning model connects vision and language.\n"
            "- Recognize why pretrained models are often a strong starting point for new projects.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. What is a pretrained model?\n"
            "\n"
            "Training a deep neural network from scratch can require large datasets, significant "
            "computation, careful engineering, and a lot of experimentation. Fortunately, we do not "
            "always need to repeat that work ourselves.\n"
            "\n"
            "A **pretrained model** is a model whose parameters have already been learned from a "
            "previous training process. We can load those learned parameters and immediately use "
            "the model for inference on new data, provided our input is prepared in the form the "
            "model expects.\n"
            "\n"
            "A useful analogy is to think of a pretrained model as a program whose behavior was "
            "shaped by examples rather than being completely hardcoded by a programmer.\n"
            "\n"
            "### Architecture and weights are different things\n"
            "\n"
            "This distinction is essential:\n"
            "\n"
            "- **Architecture** describes the structure of the neural network: which operations and "
            "layers exist and how they connect.\n"
            "- **Weights** are the learned numerical parameters that determine how that architecture "
            "actually behaves after training.\n"
            "\n"
            "Two models can share the same architecture but behave very differently if their weights "
            "were learned from different data or objectives.\n"
            "\n"
            "Consider an untrained network:\n"
            "\n"
            "```python\n"
            "from torchvision import models\n"
            "\n"
            "model = models.AlexNet()\n"
            "```\n"
            "\n"
            "The object has the AlexNet structure, but its randomly initialized weights do not yet "
            "contain useful visual knowledge. Passing an image through it would produce numbers, but "
            "those numbers would not represent a meaningful trained classifier.\n"
            "\n"
            "Now compare that with loading pretrained weights into a defined architecture. The model "
            "can immediately perform the task it was trained to solve.\n"
            "\n"
            "> **Mental model:** the architecture is the scaffold; much of the learned task behavior "
            "lives in the weights.\n"
            "\n"
            "This is why pretrained models can accelerate a project: you inherit both the model design "
            "and the computation already spent learning useful parameters.\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Running a pretrained image classifier\n"
            "\n"
            "The chapter begins with image classification using models trained on ImageNet. The "
            "important lesson is not only the name of a particular architecture. It is the reusable "
            "**inference workflow**.\n"
            "\n"
            "ImageNet is a large labeled image dataset. A widely used ImageNet classification setup "
            "contains 1,000 output classes. In this context, **class** and **label** refer to the "
            "category associated with an image.\n"
            "\n"
            "For a classifier trained on those classes, the high-level inference pipeline is:\n"
            "\n"
            "```text\n"
            "raw image\n"
            "   |\n"
            "   v\n"
            "preprocessing\n"
            "   |\n"
            "   v\n"
            "input tensor / batch\n"
            "   |\n"
            "   v\n"
            "pretrained model\n"
            "   |\n"
            "   v\n"
            "1,000 output scores\n"
            "   |\n"
            "   v\n"
            "class indices -> human-readable labels\n"
            "```\n"
            "\n"
            '{{image:pretrained-inference-pipeline}}'
            '\n'
            "\n"
            "### Why preprocessing matters\n"
            "\n"
            "A pretrained model does not understand an arbitrary image file directly. It expects "
            "numerical input with the same basic conventions used during training.\n"
            "\n"
            "Typical steps include:\n"
            "\n"
            "1. resize the image,\n"
            "2. crop to the required spatial size,\n"
            "3. convert the image to a tensor,\n"
            "4. normalize color channels using expected statistics,\n"
            "5. add a batch dimension.\n"
            "\n"
            "A pipeline similar to the chapter's example is:\n"
            "\n"
            "```python\n"
            "from torchvision import transforms\n"
            "\n"
            "preprocess = transforms.Compose([\n"
            "    transforms.Resize(256),\n"
            "    transforms.CenterCrop(224),\n"
            "    transforms.ToTensor(),\n"
            "    transforms.Normalize(\n"
            "        mean=[0.485, 0.456, 0.406],\n"
            "        std=[0.229, 0.224, 0.225],\n"
            "    ),\n"
            "])\n"
            "```\n"
            "\n"
            "The exact values matter because the model learned from inputs prepared according to "
            "specific numerical conventions. If inference data is transformed very differently, "
            "the model may receive values outside the distribution it learned to process.\n"
            "\n"
            "### Adding the batch dimension\n"
            "\n"
            "One RGB image is often represented by a tensor shaped approximately like:\n"
            "\n"
            "```text\n"
            "[channels, height, width]\n"
            "```\n"
            "\n"
            "Neural-network code commonly expects a batch:\n"
            "\n"
            "```text\n"
            "[batch, channels, height, width]\n"
            "```\n"
            "\n"
            "For one image, we therefore add a batch dimension:\n"
            "\n"
            "```python\n"
            "import torch\n"
            "\n"
            "img_t = preprocess(img)\n"
            "batch_t = torch.unsqueeze(img_t, 0)\n"
            "```\n"
            "\n"
            "The batch size is now `1`.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Architecture, forward pass, and pretrained weights\n"
            "\n"
            "A neural-network architecture is a sequence or hierarchy of mathematical operations. "
            "When an input travels from the beginning of the model to the final outputs, that "
            "calculation is called a **forward pass**.\n"
            "\n"
            "For a callable PyTorch model, the idea is simply:\n"
            "\n"
            "```python\n"
            "output = model(input_tensor)\n"
            "```\n"
            "\n"
            "Internally, however, that single call can involve millions of parameters and many layers.\n"
            "\n"
            "### AlexNet as a historical example\n"
            "\n"
            "AlexNet became a major milestone in image recognition because of its strong ImageNet "
            "competition performance in 2012. Its historical importance is that it helped demonstrate "
            "how effective deep neural networks could be on large-scale computer-vision tasks.\n"
            "\n"
            "The chapter uses AlexNet as an approachable example of a model that transforms an image "
            "through a sequence of learned operations into scores for 1,000 classes.\n"
            "\n"
            "### Vision Transformers as a modern example\n"
            "\n"
            "The chapter then introduces a Vision Transformer (ViT). The specific internals are not "
            "required yet, but printing a ViT model reveals an important PyTorch concept: neural "
            "networks are assembled from **modules**.\n"
            "\n"
            "Modules can be nested. A large component can contain smaller submodules, producing a "
            "hierarchy that is visible when the model is printed.\n"
            "\n"
            "A pretrained ViT can be loaded with weights learned from ImageNet data:\n"
            "\n"
            "```python\n"
            "from torchvision import models\n"
            "\n"
            "vit = models.vit_b_16(\n"
            "    weights=models.ViT_B_16_Weights.IMAGENET1K_V1\n"
            ")\n"
            "```\n"
            "\n"
            "The educational point is more important than memorizing the model name:\n"
            "\n"
            "> **A useful pretrained model requires a compatible architecture, trained weights, and "
            "the correct preprocessing.**\n"
            "\n"
            "[[IMAGE_NEEDED: Neural-network architecture and forward pass | "
            "A simplified left-to-right model diagram inspired by an image classifier, showing an "
            "input image passing through several learned processing blocks into a final vector of "
            "class scores; optionally annotate intermediate representations without reproducing "
            "source artwork | Learner should notice that the input is progressively transformed and "
            "that the learned weights inside the blocks determine the transformations]]\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Inference: evaluation mode, scores, softmax, and top-k predictions\n"
            "\n"
            "**Inference** means using a trained model on new data to obtain predictions or generated "
            "outputs. During inference, we are not trying to learn new weights; we are using the "
            "knowledge already stored in the model.\n"
            "\n"
            "### Put the model in evaluation mode\n"
            "\n"
            "For the chapter's classifier, the model is switched to evaluation mode before inference:\n"
            "\n"
            "```python\n"
            "vit.eval()\n"
            "```\n"
            "\n"
            "This matters because some neural-network components behave differently during training "
            "and evaluation. The chapter specifically points to mechanisms such as dropout and batch "
            "normalization. Evaluation mode tells those components to use inference behavior.\n"
            "\n"
            "### Run the forward pass\n"
            "\n"
            "```python\n"
            "out = vit(batch_t)\n"
            "```\n"
            "\n"
            "For an ImageNet classifier, the output can contain 1,000 scores—one score for each class.\n"
            "\n"
            "These raw scores are not automatically meaningful English labels. We need to map output "
            "indices back to the class-label ordering used during training.\n"
            "\n"
            "### Find the highest-scoring class\n"
            "\n"
            "```python\n"
            "_, index = torch.max(out, 1)\n"
            "```\n"
            "\n"
            "The index tells us which class received the largest score.\n"
            "\n"
            "### Convert scores with softmax\n"
            "\n"
            "Softmax converts a vector of scores into nonnegative values that sum to 1:\n"
            "\n"
            "```python\n"
            "probabilities = torch.nn.functional.softmax(out, dim=1)\n"
            "```\n"
            "\n"
            "These values are often presented as confidence-like percentages. For learning purposes, "
            "treat them as the model's relative distribution across its available classes—not as a "
            "guarantee that the prediction is objectively correct.\n"
            "\n"
            "### Look at top-k predictions\n"
            "\n"
            "The top prediction is useful, but the ranked alternatives can reveal more about what "
            "the model is seeing:\n"
            "\n"
            "```python\n"
            "_, indices = torch.sort(out, descending=True)\n"
            "top5 = indices[0][:5]\n"
            "```\n"
            "\n"
            "A top-5 list can expose plausible alternatives as well as surprising associations learned "
            "from the training data.\n"
            "\n"
            "### A confident model can still be wrong\n"
            "\n"
            "This is one of the most important practical lessons in the chapter. Model behavior depends "
            "on the data it learned from and the classes it is capable of predicting.\n"
            "\n"
            "If an input is poorly represented in the training distribution—or represents something "
            "outside the available class set—the model can still produce a high score for one of the "
            "classes it knows.\n"
            "\n"
            "So remember:\n"
            "\n"
            "> **Confidence is a property of the model's output, not proof that the model understands "
            "the world correctly.**\n"
            "\n"
            "Unexpected top predictions can also expose correlations or biases present in the training "
            "data. The chapter's dog-classification example shows how seemingly unrelated objects can "
            "appear among the alternatives because of patterns that occurred in the data.\n"
            "\n"
            "{{exercise:M02.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Pretrained diffusion models and image inpainting\n"
            "\n"
            "Pretrained models are not limited to assigning labels. They can also generate and edit "
            "content. The chapter introduces this through **diffusion models** and **inpainting**.\n"
            "\n"
            "### The core diffusion idea\n"
            "\n"
            "At a high level, a diffusion model learns to reverse a gradual corruption process.\n"
            "\n"
            "During training, clean images are progressively disturbed with noise. The model learns how "
            "to reverse that process—removing noise step by step until meaningful structure appears.\n"
            "\n"
            "At inference time, that learned denoising process can be guided by a text prompt.\n"
            "\n"
            "A simplified picture is:\n"
            "\n"
            "```text\n"
            "noise / noisy representation\n"
            "          |\n"
            "          v\n"
            "guided denoising step\n"
            "          |\n"
            "          v\n"
            "less noisy representation\n"
            "          |\n"
            "       repeat\n"
            "          |\n"
            "          v\n"
            "coherent generated image\n"
            "```\n"
            "\n"
            "### Inpainting adds location control\n"
            "\n"
            "Inpainting edits only a selected region of an existing image. The chapter uses a mask "
            "with two conceptual regions:\n"
            "\n"
            "- protected pixels that should remain unchanged,\n"
            "- editable pixels where the model may generate new content.\n"
            "\n"
            "Three inputs therefore play different roles:\n"
            "\n"
            "| Input | Role |\n"
            "|---|---|\n"
            "| Text prompt | Describes what the generated result should contain |\n"
            "| Input image | Anchors the original scene and geometry |\n"
            "| Mask | Defines where edits are allowed |\n"
            "\n"
            "[[IMAGE_NEEDED: Inputs to diffusion inpainting | "
            "A conceptual three-input diagram showing a text prompt, an original image, and a black/"
            "white edit mask entering an inpainting pipeline and producing an edited image | Learner "
            "should notice that the prompt controls what to generate, the image defines the starting "
            "scene, and the mask constrains where changes may occur]]\n"
            "\n"
            "The source example changes a horse into a zebra while attempting to preserve the "
            "surrounding scene. The point is not the animal itself—it is that a pretrained generative "
            "model can perform a complex localized transformation without being retrained for that "
            "single edit.\n"
            "\n"
            "[[IMAGE_NEEDED: Iterative diffusion inpainting process | "
            "A sequence of 4–6 stages showing the masked region beginning noisy and becoming gradually "
            "more structured while the unmasked background remains fixed, ending with a coherent "
            "localized edit | Learner should notice that generation happens through repeated refinement "
            "rather than a single deterministic drawing step]]\n"
            "\n"
            "### A high-level inpainting pipeline\n"
            "\n"
            "The chapter uses a pretrained diffusion pipeline that bundles the components needed for "
            "generation:\n"
            "\n"
            "- text processing,\n"
            "- a text encoder,\n"
            "- a denoising network,\n"
            "- a variational autoencoder (VAE),\n"
            "- a scheduler controlling the denoising procedure.\n"
            "\n"
            "A simplified invocation looks like this:\n"
            "\n"
            "```python\n"
            "from diffusers import StableDiffusionInpaintPipeline\n"
            "\n"
            "pipe = StableDiffusionInpaintPipeline.from_pretrained(model_id)\n"
            "\n"
            "result = pipe(\n"
            "    prompt=prompt,\n"
            "    image=image,\n"
            "    mask_image=mask,\n"
            ")\n"
            "```\n"
            "\n"
            "The lesson to retain is that a high-level pipeline can hide a very sophisticated trained "
            "system behind a small number of application-facing calls.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Model zoos and Hugging Face\n"
            "\n"
            "A **model zoo** is a collection or repository of pretrained models. Model zoos let "
            "practitioners reuse models built and trained by other teams instead of starting every "
            "project from zero.\n"
            "\n"
            "The chapter discusses several sources and libraries, including TorchVision, "
            "`transformers`, and `diffusers`, then highlights Hugging Face as a major repository and "
            "ecosystem for pretrained models.\n"
            "\n"
            "### Why a uniform interface matters\n"
            "\n"
            "Historically, pretrained models could be distributed in inconsistent ways. A repository "
            "with standardized loading APIs reduces friction by packaging model weights, configuration, "
            "preprocessing, and task-specific interfaces more consistently.\n"
            "\n"
            "### Hugging Face pipelines\n"
            "\n"
            "The `pipeline` abstraction provides a convenient high-level interface for common tasks. "
            "The chapter demonstrates text generation with GPT-2:\n"
            "\n"
            "```python\n"
            "from transformers import pipeline\n"
            "\n"
            "generator = pipeline('text-generation', model='gpt2')\n"
            "result = generator(\n"
            "    'Deep learning models can',\n"
            "    max_length=20,\n"
            ")\n"
            "```\n"
            "\n"
            "You do not yet need to understand transformer internals. The important lesson is that "
            "pretrained capabilities can be accessed through a task-oriented interface with only a "
            "small amount of code.\n"
            "\n"
            "However, convenience does not eliminate engineering responsibility. When selecting a "
            "pretrained model, you still need to understand at least:\n"
            "\n"
            "- what task the model was designed for,\n"
            "- what inputs it expects,\n"
            "- what outputs it produces,\n"
            "- what data or domain it was trained on,\n"
            "- what limitations its documentation describes.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Multimodal models: turning images into language\n"
            "\n"
            "The final major example in the chapter is **BLIP**, an image-captioning model. It is "
            "multimodal because it connects more than one kind of data—in this case, images and text.\n"
            "\n"
            "### The problem\n"
            "\n"
            "Given a new image, the model should produce a natural-language sentence describing what "
            "it sees.\n"
            "\n"
            "At a high level, the process contains two conceptual stages:\n"
            "\n"
            "1. an **image encoder** converts visual information into a numerical representation,\n"
            "2. a **text decoder** uses that representation to generate a caption.\n"
            "\n"
            "[[IMAGE_NEEDED: BLIP image-captioning mental model | "
            "A conceptual pipeline showing an input image entering an image encoder, producing an "
            "embedding or visual representation, then entering a text decoder that generates a natural-"
            "language caption | Learner should notice that the model bridges two modalities by turning "
            "visual information into a representation that can condition language generation]]\n"
            "\n"
            "During training, image-text pairs help the model learn relationships between visual "
            "content and language. The source explains this in terms of encoded numerical "
            "representations, or **embeddings**, and a decoder that generates text.\n"
            "\n"
            "### Loading a pretrained captioning model\n"
            "\n"
            "A simplified version of the chapter's workflow is:\n"
            "\n"
            "```python\n"
            "from transformers import BlipProcessor, BlipForConditionalGeneration\n"
            "\n"
            "processor = BlipProcessor.from_pretrained(\n"
            "    'Salesforce/blip-image-captioning-large'\n"
            ")\n"
            "model = BlipForConditionalGeneration.from_pretrained(\n"
            "    'Salesforce/blip-image-captioning-large'\n"
            ")\n"
            "```\n"
            "\n"
            "The processor prepares the image in the format expected by the model. The model then "
            "generates token IDs that the processor can decode into text.\n"
            "\n"
            "```python\n"
            "inputs = processor(image, return_tensors='pt')\n"
            "out = model.generate(**inputs)\n"
            "caption = processor.decode(out[0], skip_special_tokens=True)\n"
            "```\n"
            "\n"
            "This example reinforces a pattern that appears throughout the chapter:\n"
            "\n"
            "```text\n"
            "raw input\n"
            "   -> task-specific preprocessing\n"
            "   -> pretrained model\n"
            "   -> raw model output\n"
            "   -> task-specific decoding\n"
            "   -> human-usable result\n"
            "```\n"
            "\n"
            "{{exercise:M02.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Reuse, fine-tuning, and the boundaries of pretrained models\n"
            "\n"
            "The deeper message of this chapter is not merely that pretrained demos are impressive. "
            "It is that reusing learned models is a core practical strategy in deep learning.\n"
            "\n"
            "A pretrained model can provide:\n"
            "\n"
            "- a strong baseline,\n"
            "- useful learned representations,\n"
            "- faster project prototyping,\n"
            "- access to training effort that would be expensive to reproduce.\n"
            "\n"
            "Later, instead of always training from scratch, we can **fine-tune** a pretrained model "
            "on a new but related task or dataset. The chapter specifically points forward to this "
            "strategy as useful when the new task does not have a huge amount of labeled data.\n"
            "\n"
            "But pretrained models also come with boundaries. Their behavior is shaped by:\n"
            "\n"
            "- the training data they saw,\n"
            "- the objectives used during training,\n"
            "- the labels or output space they support,\n"
            "- the preprocessing conventions they expect.\n"
            "\n"
            "Using a pretrained model responsibly therefore requires more than simply calling "
            "`from_pretrained()`. You should understand what the model knows, what it does not know, "
            "and how your input differs from the conditions under which it learned.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: If I instantiate the right architecture, I automatically have the trained model\n"
            "\n"
            "> Creating an AlexNet or ViT object is the same as loading a pretrained network.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The architecture defines the computation structure. Useful pretrained behavior comes "
            "from learned weights. An untrained architecture can run a forward pass but will not "
            "perform meaningful pretrained classification.\n"
            "\n"
            "### Misconception 2: Preprocessing is just cosmetic image cleanup\n"
            "\n"
            "> The network should work equally well no matter how I scale or normalize the image.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The model was trained under particular input conventions. Correct size, tensor shape, "
            "normalization, and batching help make new inputs consistent with those conventions.\n"
            "\n"
            "### Misconception 3: The highest softmax value proves the prediction is correct\n"
            "\n"
            "> If the model is highly confident, the answer must be true.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "A model distributes scores among the outputs it knows. It can be confidently wrong, "
            "especially on unusual, poorly represented, or out-of-distribution inputs.\n"
            "\n"
            "### Misconception 4: A pretrained pipeline means I do not need to understand the task\n"
            "\n"
            "> If a library gives me a one-line pipeline, I can safely ignore the model's expected "
            "inputs, training domain, and limitations.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "High-level APIs reduce coding effort, not the need for sound engineering judgment.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Pretrained model | Model whose parameters have already been learned from previous training. |\n"
            "| Architecture | Structural arrangement of layers and operations in a neural network. |\n"
            "| Weights | Learned numerical parameters controlling model behavior. |\n"
            "| Class / label | Category associated with an input in a classification task. |\n"
            "| Inference | Running a trained model on new data. |\n"
            "| Forward pass | Computation that moves input through the model to produce output. |\n"
            "| Preprocessing | Transformations that convert raw input into the representation expected by a model. |\n"
            "| Batch | Group of samples processed together; even one sample may be wrapped in a batch dimension. |\n"
            "| Evaluation mode | Model state used for inference behavior in components such as dropout or batch normalization. |\n"
            "| Softmax | Transformation that converts a vector of scores into nonnegative values summing to 1. |\n"
            "| Top-k prediction | The k highest-ranked model outputs rather than only the single highest one. |\n"
            "| Diffusion model | Generative model that learns a process related to reversing gradual noising. |\n"
            "| Inpainting | Image editing where generation is restricted to a selected region. |\n"
            "| Mask | Spatial specification defining which image regions may or may not be edited. |\n"
            "| Model zoo | Repository or collection of pretrained models. |\n"
            "| Hugging Face | Ecosystem and model repository providing standardized access to many pretrained models. |\n"
            "| Pipeline | High-level task-oriented interface that bundles model loading and application logic. |\n"
            "| Multimodal model | Model that works across multiple data types or modalities, such as images and text. |\n"
            "| Embedding | Numerical representation capturing information about an input. |\n"
            "| Encoder | Component that converts input into an internal representation. |\n"
            "| Decoder | Component that converts an internal representation into an output such as text. |\n"
            "| Fine-tuning | Further training a pretrained model for a new or related task. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What is the difference between model architecture and pretrained weights?\n"
            "2. Why can an untrained neural network execute a forward pass but still be useless for classification?\n"
            "3. Why must a pretrained image model receive inputs processed in the way it expects?\n"
            "4. What does `model.eval()` change conceptually?\n"
            "5. What is the difference between raw output scores and human-readable class labels?\n"
            "6. Why should top-k predictions sometimes be inspected instead of only top-1?\n"
            "7. Why can a model be confident and still be wrong?\n"
            "8. In inpainting, what separate roles do the prompt, input image, and mask play?\n"
            "9. What problem does a model zoo solve for practitioners?\n"
            "10. How does an image encoder plus text decoder enable image captioning?\n"
            "11. Why can fine-tuning be attractive when you have limited data for a related task?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**A pretrained model is reusable learned capability: the architecture provides the "
            "computational structure, the weights contain knowledge learned from earlier data, and a "
            "correct inference pipeline turns new raw inputs into the representations the model expects "
            "and decodes its outputs into useful results.**\n"
        ),

        "estimated_minutes": 120,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "pretrained-model-mental-model",
                "title": "What is a pretrained model?",
                "order": 1,
            },
            {
                "id": "image-classification-pipeline",
                "title": "Running a pretrained image classifier",
                "order": 2,
            },
            {
                "id": "architecture-forward-pass-and-weights",
                "title": "Architecture, forward pass, and pretrained weights",
                "order": 3,
            },
            {
                "id": "inference-and-output-interpretation",
                "title": "Inference and output interpretation",
                "order": 4,
            },
            {
                "id": "diffusion-and-inpainting",
                "title": "Pretrained diffusion models and image inpainting",
                "order": 5,
            },
            {
                "id": "hugging-face-model-zoo",
                "title": "Model zoos and Hugging Face",
                "order": 6,
            },
            {
                "id": "multimodal-captioning",
                "title": "Multimodal models and image captioning",
                "order": 7,
            },
            {
                "id": "reuse-fine-tuning-and-boundaries",
                "title": "Reuse, fine-tuning, and model boundaries",
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
            "title": "Trace an Image Through the Inference Pipeline",
            "lesson_code": "M02.L01",
            "section_id": "inference-and-output-interpretation",
            "placement": "after_section",
            "description": (
                "Practice reasoning about preprocessing, batching, inference, class scores, "
                "and prediction interpretation."
            ),
            "instructions": (
                "Imagine you have a JPEG photograph and a pretrained 1,000-class image classifier.\n"
                "1. Write the major steps from opening the image to obtaining a human-readable label.\n"
                "2. Explain why resize/crop and normalization must match the model's expectations.\n"
                "3. Explain why a batch dimension is added even when you have only one image.\n"
                "4. State why evaluation mode should be enabled before inference.\n"
                "5. Explain the difference between the raw output scores, softmax values, and labels.\n"
                "6. Suppose the top prediction has a very high softmax value but the subject is not "
                "represented by any of the model's known classes. Explain why the prediction may still "
                "be wrong."
            ),
            "expected_output": (
                "An ordered inference pipeline plus short explanations covering preprocessing, "
                "batching, evaluation mode, score interpretation, and confident errors."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "preprocessing",
                "inference",
                "evaluation-mode",
                "softmax",
                "model-limitations",
            ],
        },
        {
            "id": "M02.L01.EX02",
            "title": "Compare Three Pretrained Model Workflows",
            "lesson_code": "M02.L01",
            "section_id": "multimodal-captioning",
            "placement": "after_section",
            "description": (
                "Compare classification, diffusion inpainting, and image captioning as different "
                "applications of pretrained models."
            ),
            "instructions": (
                "Create a table with three rows: image classification, diffusion inpainting, and "
                "image captioning.\n"
                "For each workflow, identify:\n"
                "1. the raw input or inputs,\n"
                "2. the preprocessing or preparation needed,\n"
                "3. the kind of pretrained model used,\n"
                "4. the raw or intermediate model output,\n"
                "5. the final human-usable result.\n"
                "Then answer: what common pattern exists across all three workflows despite their "
                "different tasks?"
            ),
            "expected_output": (
                "A three-row comparison table plus a short paragraph identifying the shared pattern: "
                "prepare input, run pretrained learned computation, decode/interpret output."
            ),
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                "pretrained-models",
                "classification",
                "diffusion",
                "multimodal",
                "workflow-reasoning",
            ],
        },
    ],

    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M02.L01.QZ01",
        "title": "Pretrained Networks — Knowledge Check",
        "lesson_code": "M02.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M02.L01.Q01",
                "section_id": "pretrained-model-mental-model",
                "question": "Which statement best distinguishes architecture from pretrained weights?",
                "options": [
                    "Architecture stores class names, while weights store image files.",
                    "Architecture defines the network structure, while weights are learned numerical parameters.",
                    "Architecture is used only for training, while weights are used only for preprocessing.",
                    "There is no practical difference between them.",
                ],
                "correct": 1,
                "explanation": (
                    "The architecture specifies the operations and connections. Training adjusts "
                    "the weights, which determine how that structure behaves on the learned task."
                ),
            },
            {
                "id": "M02.L01.Q02",
                "section_id": "image-classification-pipeline",
                "question": "Why is input normalization important for a pretrained image model?",
                "options": [
                    "It converts the neural network into a transformer.",
                    "It helps match the numerical input conventions used when the model was trained.",
                    "It automatically creates new class labels.",
                    "It removes the need to resize an image.",
                ],
                "correct": 1,
                "explanation": (
                    "Pretrained models expect inputs prepared consistently with their training setup. "
                    "Normalization helps place channel values into the expected numerical range."
                ),
            },
            {
                "id": "M02.L01.Q03",
                "section_id": "inference-and-output-interpretation",
                "question": "What is the purpose of calling `model.eval()` before inference?",
                "options": [
                    "It retrains the model on the current image.",
                    "It switches applicable components to inference behavior.",
                    "It converts scores directly into English labels.",
                    "It guarantees that every prediction is correct.",
                ],
                "correct": 1,
                "explanation": (
                    "Some model components behave differently in training and inference. Evaluation "
                    "mode activates the appropriate inference behavior."
                ),
            },
            {
                "id": "M02.L01.Q04",
                "section_id": "inference-and-output-interpretation",
                "question": (
                    "A classifier gives one class a very high softmax value. What can we safely conclude?"
                ),
                "options": [
                    "The prediction is guaranteed to match reality.",
                    "The class had the strongest relative model output among the available classes, "
                    "but the model can still be wrong.",
                    "The input definitely appeared in the training dataset.",
                    "The model has human-level understanding of the object.",
                ],
                "correct": 1,
                "explanation": (
                    "A large softmax value reflects the model's relative output distribution. It does "
                    "not guarantee correctness, especially for unusual or out-of-distribution inputs."
                ),
            },
            {
                "id": "M02.L01.Q05",
                "section_id": "diffusion-and-inpainting",
                "question": "What is the main purpose of a mask in diffusion-based inpainting?",
                "options": [
                    "Choose the model's optimizer.",
                    "Specify which image regions may be edited and which should be preserved.",
                    "Convert the output into class probabilities.",
                    "Replace the need for a text prompt in every case.",
                ],
                "correct": 1,
                "explanation": (
                    "The mask provides spatial control. It identifies the region the generative model "
                    "may modify while helping preserve protected areas."
                ),
            },
            {
                "id": "M02.L01.Q06",
                "section_id": "hugging-face-model-zoo",
                "question": "What is a major practical benefit of a model zoo such as Hugging Face?",
                "options": [
                    "It guarantees every available model is appropriate for every task.",
                    "It gives standardized access to pretrained models and related tooling.",
                    "It eliminates the need to inspect model documentation.",
                    "It prevents models from using learned weights.",
                ],
                "correct": 1,
                "explanation": (
                    "Model repositories reduce friction by making pretrained models easier to discover "
                    "and load through common interfaces, but users still need to understand model scope "
                    "and limitations."
                ),
            },
            {
                "id": "M02.L01.Q07",
                "section_id": "multimodal-captioning",
                "question": "What is the high-level role of the image encoder in an image-captioning model?",
                "options": [
                    "Generate a random English sentence before seeing the image.",
                    "Convert visual information into a numerical representation used by later components.",
                    "Replace the input image with a class label only.",
                    "Perform image inpainting with a mask.",
                ],
                "correct": 1,
                "explanation": (
                    "The encoder transforms visual content into an internal representation. A language "
                    "decoder can then use that representation to generate a caption."
                ),
            },
            {
                "id": "M02.L01.Q08",
                "section_id": "reuse-fine-tuning-and-boundaries",
                "type": "open",
                "question": (
                    "You have a small labeled dataset for a task related to one solved by an existing "
                    "pretrained model. Explain why starting from that pretrained model and later "
                    "fine-tuning it may be preferable to training an entirely new model from scratch."
                ),
            },
        ],
        "passing_score": 70,
    },
}
