"""M17.L01 — Image Generation: VAEs, Diffusion, and Text-to-Image Models.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 17, page range not provided in supplied source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M17.L01"

MODULE_ORDER = 17

MODULE_TITLE = "Image Generation"

MODULE_DESCRIPTION = (
    "Learn how generative image models represent visual data in latent spaces, "
    "how variational autoencoders learn continuous representations, how "
    "diffusion models generate images through iterative denoising, and how "
    "pretrained text-to-image models condition generation on natural-language "
    "prompts."
)

SOURCE_CHAPTER = 17

SOURCE_PAGES = "Chapter 17 — page range not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Image Generation with VAEs, Diffusion, and Text Conditioning",

    "slug": "deep-learning-foundations-m17-l01",

    "description": (
        "Understand modern image generation from latent representations and "
        "variational autoencoders through diffusion models, text-conditioned "
        "generation, pretrained Stable Diffusion, and interpolation through "
        "learned representation spaces."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.intermediate,

    "estimated_hours": 3.0,

    "skill_tags": [
        "deep-learning",
        "generative-ai",
        "image-generation",
        "latent-space",
        "autoencoders",
        "vae",
        "diffusion-models",
        "unet",
        "denoising",
        "text-to-image",
        "stable-diffusion",
        "latent-interpolation",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Image Generation with VAEs, Diffusion, and Text Conditioning",

        "content": (
            "# Image Generation with VAEs, Diffusion, and Text Conditioning\n"
            "\n"
            "> **Course:** Deep Learning Foundations  \n"
            "> **Lesson:** M17.L01  \n"
            "> **Module:** Image Generation  \n"
            "> **Source alignment:** BOOK-002, Chapter 17. "
            "The supplied source did not specify a page range. "
            "This lesson is an instructor-authored curriculum adaptation "
            "rather than a reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Learning outcomes
            # ----------------------------------------------------------------

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain image generation as sampling from a learned latent space.\n"
            "- Explain the roles of generators and decoders.\n"
            "- Distinguish classical autoencoders from variational autoencoders.\n"
            "- Explain why a VAE predicts a distribution rather than one fixed latent point.\n"
            "- Explain the roles of `z_mean`, `z_log_var`, and random sampling.\n"
            "- Distinguish VAE reconstruction loss from KL regularization.\n"
            "- Explain how a decoder turns latent vectors into generated images.\n"
            "- Explain diffusion as progressive noising and generation as reverse denoising.\n"
            "- Explain the role of a U-Net in diffusion models.\n"
            "- Explain diffusion time, noise rate, signal rate, and a diffusion schedule.\n"
            "- Describe how a diffusion model is trained to predict noise.\n"
            "- Describe how generation begins from pure random noise.\n"
            "- Explain how text embeddings condition diffusion models.\n"
            "- Use the mental model behind positive and negative prompts.\n"
            "- Explain how the number of diffusion steps affects generation.\n"
            "- Explain why text and image latent spaces support interpolation.\n"
            "- Explain the purpose of spherical interpolation in latent space.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 1
            # ----------------------------------------------------------------

            "## 1. Latent Image Spaces and Variational Autoencoders\n"
            "\n"
            "Generative image models attempt to learn the underlying statistical "
            "structure of a collection of images.\n"
            "\n"
            "Instead of memorizing only the training images, the goal is to learn "
            "a representation space from which new but plausible images can be "
            "generated.\n"
            "\n"
            "The central idea is a **latent space**.\n"
            "\n"
            "### What is a latent space?\n"
            "\n"
            "A latent space is a learned vector space in which complicated data "
            "such as images is represented using more compact numerical vectors.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "high-dimensional image\n"
            "        ↓ encode\n"
            "small latent vector\n"
            "        ↓ decode\n"
            "image\n"
            "```\n"
            "\n"
            "If the latent space is structured well, nearby latent vectors should "
            "decode into visually similar images.\n"
            "\n"
            "This allows generation:\n"
            "\n"
            "```text\n"
            "sample latent vector\n"
            "       ↓\n"
            "decoder / generator\n"
            "       ↓\n"
            "new image\n"
            "```\n"
            "\n"
            "The generated image does not need to correspond to an exact training "
            "example. It can represent an interpolation between patterns learned "
            "from many training images.\n"
            "\n"
            "### Generators and decoders\n"
            "\n"
            "The component that maps a latent representation back into image "
            "pixels is commonly called a **decoder** or **generator**.\n"
            "\n"
            "```text\n"
            "latent vector z\n"
            "      ↓\n"
            "generator\n"
            "      ↓\n"
            "pixel image\n"
            "```\n"
            "\n"
            "### Main families of image generators\n"
            "\n"
            "The chapter identifies three major families:\n"
            "\n"
            "```text\n"
            "Variational Autoencoders\n"
            "Diffusion Models\n"
            "Generative Adversarial Networks\n"
            "```\n"
            "\n"
            "This lesson focuses on VAEs and diffusion models.\n"
            "\n"
            "### Classical autoencoder\n"
            "\n"
            "An autoencoder contains two main components:\n"
            "\n"
            "```text\n"
            "input image\n"
            "    ↓\n"
            "encoder\n"
            "    ↓\n"
            "compressed code\n"
            "    ↓\n"
            "decoder\n"
            "    ↓\n"
            "reconstructed image\n"
            "```\n"
            "\n"
            "The model is trained using the same image as both input and target.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "input  = handwritten digit 7\n"
            "target = same handwritten digit 7\n"
            "```\n"
            "\n"
            "The encoder is forced to compress useful information into the "
            "latent representation, while the decoder learns to reconstruct "
            "the image from that representation.\n"
            "\n"
            "### Why ordinary autoencoders are not enough for generation\n"
            "\n"
            "A standard autoencoder does not necessarily produce a smooth, "
            "well-organized latent space.\n"
            "\n"
            "Some latent points may decode into reasonable images while nearby "
            "unused regions may decode into meaningless outputs.\n"
            "\n"
            "For generation, we want something stronger:\n"
            "\n"
            "> Nearby points throughout the useful latent space should decode "
            "into plausible and related images.\n"
            "\n"
            "This is where the **Variational Autoencoder**, or VAE, helps.\n"
            "\n"
            "### The main VAE idea\n"
            "\n"
            "A VAE does not encode an image into one exact latent vector.\n"
            "\n"
            "Instead, the encoder outputs parameters describing a probability "
            "distribution.\n"
            "\n"
            "The chapter uses:\n"
            "\n"
            "```text\n"
            "z_mean\n"
            "z_log_variance\n"
            "```\n"
            "\n"
            "Then a latent point is sampled from this distribution.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "image\n"
            "  ↓\n"
            "encoder\n"
            "  ↓\n"
            "mean + variance\n"
            "  ↓\n"
            "sample latent point z\n"
            "  ↓\n"
            "decoder\n"
            "  ↓\n"
            "reconstruction\n"
            "```\n"
            "\n"
            "### Sampling equation\n"
            "\n"
            "The chapter expresses sampling conceptually as:\n"
            "\n"
            "```python\n"
            "z = z_mean + exp(0.5 * z_log_var) * epsilon\n"
            "```\n"
            "\n"
            "where `epsilon` is sampled from a normal distribution.\n"
            "\n"
            "The exact formula is less important than the intuition:\n"
            "\n"
            "> Do not always decode one exact location. Decode nearby sampled "
            "points as well.\n"
            "\n"
            "This encourages the decoder to produce meaningful outputs around "
            "each encoded training sample, which helps make the latent space "
            "continuous.\n"
            "\n"
            "### Why stochastic sampling helps\n"
            "\n"
            "Suppose one image is encoded near:\n"
            "\n"
            "```text\n"
            "z = (0.5, 1.2)\n"
            "```\n"
            "\n"
            "Training may also sample points such as:\n"
            "\n"
            "```text\n"
            "(0.48, 1.19)\n"
            "(0.53, 1.25)\n"
            "(0.50, 1.17)\n"
            "```\n"
            "\n"
            "The decoder therefore learns that an entire local region should "
            "represent related images.\n"
            "\n"
            "This gives the latent space useful continuity.\n"
            "\n"
            "### VAE encoder\n"
            "\n"
            "For MNIST, the source uses a ConvNet encoder:\n"
            "\n"
            "```python\n"
            "latent_dim = 2\n"
            "\n"
            "image_inputs = keras.Input(shape=(28, 28, 1))\n"
            "\n"
            "x = layers.Conv2D(\n"
            "    32, 3,\n"
            "    activation=\"relu\",\n"
            "    strides=2,\n"
            "    padding=\"same\",\n"
            ")(image_inputs)\n"
            "\n"
            "x = layers.Conv2D(\n"
            "    64, 3,\n"
            "    activation=\"relu\",\n"
            "    strides=2,\n"
            "    padding=\"same\",\n"
            ")(x)\n"
            "\n"
            "x = layers.Flatten()(x)\n"
            "x = layers.Dense(16, activation=\"relu\")(x)\n"
            "\n"
            "z_mean = layers.Dense(latent_dim)(x)\n"
            "z_log_var = layers.Dense(latent_dim)(x)\n"
            "```\n"
            "\n"
            "A two-dimensional latent space is especially convenient for "
            "visualization.\n"
            "\n"
            "### Why use strided convolution?\n"
            "\n"
            "The source uses strided convolution rather than max pooling when "
            "downsampling.\n"
            "\n"
            "Reconstruction depends strongly on spatial information—where image "
            "structures occur—so the architecture is designed to preserve useful "
            "location information while compressing the image.\n"
            "\n"
            "### VAE decoder\n"
            "\n"
            "The decoder performs the reverse transformation.\n"
            "\n"
            "```text\n"
            "latent vector\n"
            "   ↓\n"
            "Dense\n"
            "   ↓\n"
            "Reshape\n"
            "   ↓\n"
            "Conv2DTranspose\n"
            "   ↓\n"
            "Conv2DTranspose\n"
            "   ↓\n"
            "reconstructed image\n"
            "```\n"
            "\n"
            "For example:\n"
            "\n"
            "```python\n"
            "latent_inputs = keras.Input(shape=(2,))\n"
            "\n"
            "x = layers.Dense(7 * 7 * 64, activation=\"relu\")(latent_inputs)\n"
            "x = layers.Reshape((7, 7, 64))(x)\n"
            "\n"
            "x = layers.Conv2DTranspose(\n"
            "    64, 3,\n"
            "    activation=\"relu\",\n"
            "    strides=2,\n"
            "    padding=\"same\",\n"
            ")(x)\n"
            "\n"
            "x = layers.Conv2DTranspose(\n"
            "    32, 3,\n"
            "    activation=\"relu\",\n"
            "    strides=2,\n"
            "    padding=\"same\",\n"
            ")(x)\n"
            "\n"
            "outputs = layers.Conv2D(\n"
            "    1, 3,\n"
            "    activation=\"sigmoid\",\n"
            "    padding=\"same\",\n"
            ")(x)\n"
            "```\n"
            "\n"
            "The final result returns to shape:\n"
            "\n"
            "```text\n"
            "(28, 28, 1)\n"
            "```\n"
            "\n"
            "### Two VAE loss components\n"
            "\n"
            "A VAE is trained with two competing goals.\n"
            "\n"
            "#### Reconstruction loss\n"
            "\n"
            "The reconstructed image should resemble the original image.\n"
            "\n"
            "```text\n"
            "original image\n"
            "      ≈\n"
            "decoded image\n"
            "```\n"
            "\n"
            "#### KL regularization\n"
            "\n"
            "The latent distributions should stay organized around a standard "
            "normal distribution rather than spreading into arbitrary isolated "
            "regions.\n"
            "\n"
            "The source uses Kullback-Leibler divergence for this regularization.\n"
            "\n"
            "So conceptually:\n"
            "\n"
            "```text\n"
            "total loss\n"
            "=\n"
            "reconstruction loss\n"
            "+\n"
            "latent-space regularization\n"
            "```\n"
            "\n"
            "There is an important balance:\n"
            "\n"
            "```text\n"
            "reconstruction objective\n"
            "→ preserve information about each image\n"
            "\n"
            "KL objective\n"
            "→ organize latent space smoothly\n"
            "```\n"
            "\n"
            "### Self-supervised learning\n"
            "\n"
            "No class label is required to train this VAE.\n"
            "\n"
            "The input itself supplies the reconstruction target.\n"
            "\n"
            "```text\n"
            "input image\n"
            "→ target is the same image\n"
            "```\n"
            "\n"
            "The source describes this as a self-supervised setup.\n"
            "\n"
            "### Sampling after training\n"
            "\n"
            "After training, the decoder can receive arbitrary latent points.\n"
            "\n"
            "For a two-dimensional latent space, imagine a grid:\n"
            "\n"
            "```text\n"
            "(-1, 1)        ...       (1, 1)\n"
            "   ↓                        ↓\n"
            " digit                    digit\n"
            "\n"
            "   ...                    ...\n"
            "\n"
            "(-1,-1)        ...       (1,-1)\n"
            "```\n"
            "\n"
            "Decoding neighboring coordinates produces digits that smoothly "
            "morph into one another.\n"
            "\n"
            "This visually demonstrates that the VAE has learned a continuous "
            "representation space.\n"
            "\n"
            "> **Recommended manual figure:** Add a diagram showing "
            "`image → encoder → z_mean/z_log_var → sample z → decoder → reconstructed image` "
            "immediately here.\n"
            "\n"

            # Exercise EX01 is rendered here by the frontend.
            "{{exercise:M17.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 2
            # ----------------------------------------------------------------

            "## 2. Diffusion Models: Creating Images by Removing Noise\n"
            "\n"
            "Diffusion models approach image generation very differently from "
            "VAEs.\n"
            "\n"
            "The central idea comes from **denoising**.\n"
            "\n"
            "Suppose an image contains a little random noise.\n"
            "\n"
            "A neural network can be trained to predict and remove that noise.\n"
            "\n"
            "Now imagine repeating this process many times.\n"
            "\n"
            "Eventually, the starting point can be pure random noise.\n"
            "\n"
            "```text\n"
            "pure noise\n"
            "    ↓ denoise\n"
            "slightly more structured\n"
            "    ↓ denoise\n"
            "more image-like\n"
            "    ↓ denoise\n"
            "...\n"
            "    ↓\n"
            "generated image\n"
            "```\n"
            "\n"
            "This iterative reverse process is the key idea behind diffusion "
            "image generation.\n"
            "\n"
            "### Forward diffusion versus reverse diffusion\n"
            "\n"
            "The conceptual **forward** process adds noise:\n"
            "\n"
            "```text\n"
            "clean image\n"
            "   ↓ add noise\n"
            "slightly noisy image\n"
            "   ↓ add noise\n"
            "very noisy image\n"
            "   ↓\n"
            "almost pure noise\n"
            "```\n"
            "\n"
            "Generation performs the opposite process:\n"
            "\n"
            "```text\n"
            "noise\n"
            "   ↓\n"
            "denoise\n"
            "   ↓\n"
            "denoise\n"
            "   ↓\n"
            "clean generated image\n"
            "```\n"
            "\n"
            "### The denoising model\n"
            "\n"
            "Rather than directly predicting the clean image, the source's "
            "network predicts the noise contained in the input.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "noisy image\n"
            "+\n"
            "current noise level\n"
            "      ↓\n"
            "denoising neural network\n"
            "      ↓\n"
            "predicted noise mask\n"
            "```\n"
            "\n"
            "The predicted noise can then be removed from the noisy input.\n"
            "\n"
            "### Why tell the network the noise level?\n"
            "\n"
            "Removing a tiny amount of noise is a very different problem from "
            "recovering an image from something close to pure random noise.\n"
            "\n"
            "Therefore the denoising model receives information describing how "
            "noisy the current input is.\n"
            "\n"
            "### U-Net architecture\n"
            "\n"
            "The denoising model used in the chapter is a **U-Net**.\n"
            "\n"
            "Its high-level structure is:\n"
            "\n"
            "```text\n"
            "128 × 128 image\n"
            "      ↓\n"
            "DOWNSAMPLING PATH\n"
            "      ↓\n"
            "smaller spatial representation\n"
            "      ↓\n"
            "MIDDLE\n"
            "      ↓\n"
            "UPSAMPLING PATH\n"
            "      ↓\n"
            "128 × 128 output\n"
            "```\n"
            "\n"
            "There are also skip connections:\n"
            "\n"
            "```text\n"
            "downsampling feature ─────────┐\n"
            "                              ↓\n"
            "                        matching upsampling stage\n"
            "```\n"
            "\n"
            "These shortcuts preserve spatial detail that could otherwise be "
            "lost during repeated downsampling.\n"
            "\n"
            "### Three U-Net stages\n"
            "\n"
            "#### 1. Downsampling\n"
            "\n"
            "Spatial resolution becomes smaller while feature depth increases.\n"
            "\n"
            "```text\n"
            "128 × 128\n"
            "→ 64 × 64\n"
            "→ 32 × 32\n"
            "→ 16 × 16\n"
            "```\n"
            "\n"
            "#### 2. Middle representation\n"
            "\n"
            "The deepest features are processed at a compact spatial resolution.\n"
            "\n"
            "#### 3. Upsampling\n"
            "\n"
            "Spatial detail is reconstructed:\n"
            "\n"
            "```text\n"
            "16 × 16\n"
            "→ 32 × 32\n"
            "→ 64 × 64\n"
            "→ 128 × 128\n"
            "```\n"
            "\n"
            "Skip connections inject information from matching encoder stages.\n"
            "\n"
            "### Diffusion time\n"
            "\n"
            "Generation happens over multiple steps.\n"
            "\n"
            "The chapter describes a continuous **diffusion time** between 1 "
            "and 0.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "time = 1\n"
            "→ mostly noise\n"
            "\n"
            "time = 0\n"
            "→ mostly signal / image\n"
            "```\n"
            "\n"
            "### Diffusion schedule\n"
            "\n"
            "The mapping between diffusion time and the proportions of signal "
            "and noise is called a **diffusion schedule**.\n"
            "\n"
            "At one point in the process we may have:\n"
            "\n"
            "```text\n"
            "noisy_image\n"
            "=\n"
            "signal_rate × clean_image\n"
            "+\n"
            "noise_rate × random_noise\n"
            "```\n"
            "\n"
            "The source uses a cosine schedule where signal and noise change "
            "smoothly across diffusion time.\n"
            "\n"
            "### Training the diffusion model\n"
            "\n"
            "For every training image:\n"
            "\n"
            "```text\n"
            "clean image\n"
            "   ↓\n"
            "sample random diffusion time\n"
            "   ↓\n"
            "calculate signal + noise rates\n"
            "   ↓\n"
            "sample random noise\n"
            "   ↓\n"
            "create noisy image\n"
            "   ↓\n"
            "U-Net predicts the added noise\n"
            "   ↓\n"
            "compare predicted noise with real noise\n"
            "```\n"
            "\n"
            "The chapter uses mean absolute error between:\n"
            "\n"
            "```text\n"
            "actual noise mask\n"
            "and\n"
            "predicted noise mask\n"
            "```\n"
            "\n"
            "The model therefore learns one reusable skill:\n"
            "\n"
            "> Given an image corrupted to a known degree, estimate the noise "
            "that should be removed.\n"
            "\n"
            "### Generation\n"
            "\n"
            "Training begins from real images plus artificial noise.\n"
            "\n"
            "Generation is different.\n"
            "\n"
            "It begins from:\n"
            "\n"
            "```text\n"
            "pure random noise\n"
            "```\n"
            "\n"
            "Then the trained denoiser is repeatedly applied.\n"
            "\n"
            "```text\n"
            "noise\n"
            " ↓ step 1\n"
            "slightly structured noise\n"
            " ↓ step 2\n"
            "more structure\n"
            " ↓ ...\n"
            "image\n"
            "```\n"
            "\n"
            "### Number of diffusion steps\n"
            "\n"
            "Generation quality depends partly on how many denoising iterations "
            "are performed.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "few steps\n"
            "→ faster generation\n"
            "→ less opportunity for refinement\n"
            "\n"
            "more steps\n"
            "→ slower generation\n"
            "→ more iterative refinement\n"
            "```\n"
            "\n"
            "The exact quality-versus-speed behavior depends on the model and "
            "sampling method.\n"
            "\n"
            "### Monitoring generated images\n"
            "\n"
            "Unlike classification, image generation does not always provide a "
            "simple metric such as accuracy that captures visual quality.\n"
            "\n"
            "The chapter therefore demonstrates generating sample images after "
            "training epochs so that progress can be visually inspected.\n"
            "\n"
            "### Training stability\n"
            "\n"
            "The chapter also uses optimization techniques such as:\n"
            "\n"
            "```text\n"
            "learning-rate decay\n"
            "exponential moving averages of weights\n"
            "```\n"
            "\n"
            "These techniques can help stabilize the noisy optimization process "
            "involved in generative modeling.\n"
            "\n"
            "> **Recommended manual figure:** Add a diagram showing "
            "`pure noise → repeated denoising steps → generated image` here.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 3
            # ----------------------------------------------------------------

            "## 3. Text-to-Image Generation with Pretrained Diffusion Models\n"
            "\n"
            "An unconditional diffusion model generates an image without being "
            "told exactly what the image should contain.\n"
            "\n"
            "Text-to-image generation adds a powerful condition:\n"
            "\n"
            "```text\n"
            "text prompt\n"
            "+\n"
            "random noise\n"
            "      ↓\n"
            "conditional diffusion model\n"
            "      ↓\n"
            "image matching the prompt\n"
            "```\n"
            "\n"
            "### Text conditioning\n"
            "\n"
            "A text encoder first converts the prompt into numerical embeddings.\n"
            "\n"
            "```text\n"
            "\"a red flower beside a lake\"\n"
            "        ↓\n"
            "tokenizer\n"
            "        ↓\n"
            "text encoder\n"
            "        ↓\n"
            "text embeddings\n"
            "```\n"
            "\n"
            "The diffusion denoiser receives these text representations in "
            "addition to the noisy image.\n"
            "\n"
            "So instead of learning only:\n"
            "\n"
            "```text\n"
            "noisy image\n"
            "→ predicted noise\n"
            "```\n"
            "\n"
            "it learns:\n"
            "\n"
            "```text\n"
            "noisy image\n"
            "+\n"
            "text description\n"
            "→ predicted noise that moves toward that description\n"
            "```\n"
            "\n"
            "### Training data\n"
            "\n"
            "A text-conditioned diffusion system can be trained on pairs:\n"
            "\n"
            "```text\n"
            "(image, caption)\n"
            "```\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "image: photo of a red sports car\n"
            "caption: \"a red sports car on a road\"\n"
            "```\n"
            "\n"
            "Across many such examples, the model learns associations between "
            "language representations and visual structure.\n"
            "\n"
            "### Using a pretrained text-to-image model\n"
            "\n"
            "Training a strong text-to-image model from scratch requires "
            "substantial data and computation.\n"
            "\n"
            "The source therefore demonstrates a pretrained Stable Diffusion 3 "
            "model through KerasHub.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```python\n"
            "import keras_hub\n"
            "\n"
            "task = keras_hub.models.TextToImage.from_preset(\n"
            "    \"stable_diffusion_3_medium\",\n"
            "    image_shape=(512, 512, 3),\n"
            "    dtype=\"float16\",\n"
            ")\n"
            "\n"
            "image = task.generate(\n"
            "    \"A NASA astronaut riding an origami elephant in New York City\"\n"
            ")\n"
            "```\n"
            "\n"
            "The high-level API handles much of the pipeline automatically:\n"
            "\n"
            "```text\n"
            "prompt\n"
            "→ tokenize\n"
            "→ encode\n"
            "→ initialize image latents\n"
            "→ diffusion denoising\n"
            "→ decode image\n"
            "```\n"
            "\n"
            "### Negative prompts\n"
            "\n"
            "Generation can also include instructions describing concepts the "
            "model should avoid.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "positive prompt:\n"
            "\"a futuristic city at sunset\"\n"
            "\n"
            "negative prompt:\n"
            "\"blue color\"\n"
            "```\n"
            "\n"
            "The conditioning process then encourages the generated image toward "
            "the positive representation and away from the negative representation.\n"
            "\n"
            "### Why generation can contain visual mistakes\n"
            "\n"
            "A generated image may contain:\n"
            "\n"
            "```text\n"
            "extra fingers\n"
            "duplicated objects\n"
            "incorrect geometry\n"
            "inconsistent lighting\n"
            "strange anatomy\n"
            "```\n"
            "\n"
            "The chapter stresses that these models are interpolation systems "
            "learned from statistical patterns in training data rather than "
            "human-like physical understanding.\n"
            "\n"
            "A visually convincing image does not imply that the model possesses "
            "an internal human-level understanding of anatomy or physics.\n"
            "\n"
            "### Model scale\n"
            "\n"
            "Larger generative models often have greater capacity to represent "
            "complex visual patterns, but they require substantially more memory "
            "and computation.\n"
            "\n"
            "The source deliberately uses the smaller Stable Diffusion 3 Medium "
            "variant to keep the demonstration accessible.\n"
            "\n"
            "### Controlling diffusion steps\n"
            "\n"
            "High-level generation functions can expose the number of diffusion "
            "steps.\n"
            "\n"
            "For example, you might compare:\n"
            "\n"
            "```text\n"
            "5 steps\n"
            "10 steps\n"
            "15 steps\n"
            "20 steps\n"
            "25 steps\n"
            "```\n"
            "\n"
            "This makes the progressive denoising process easier to observe.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Section 4
            # ----------------------------------------------------------------

            "## 4. Exploring and Interpolating Learned Latent Spaces\n"
            "\n"
            "One of the most important ideas in deep learning is that learned "
            "representations often form smooth spaces.\n"
            "\n"
            "Similar concepts are represented by nearby or geometrically related "
            "points.\n"
            "\n"
            "Text-to-image systems give us a striking way to visualize this.\n"
            "\n"
            "### Decomposing text-to-image generation\n"
            "\n"
            "The high-level `generate()` operation can be thought of as three "
            "major stages.\n"
            "\n"
            "#### Step 1 — Encode the prompt\n"
            "\n"
            "```text\n"
            "prompt\n"
            " ↓\n"
            "tokenizer\n"
            " ↓\n"
            "text encoder\n"
            " ↓\n"
            "text embeddings\n"
            "```\n"
            "\n"
            "#### Step 2 — Denoise image latents\n"
            "\n"
            "```text\n"
            "pure noise\n"
            "+\n"
            "text embeddings\n"
            "      ↓\n"
            "iterative denoising\n"
            "      ↓\n"
            "image latent representation\n"
            "```\n"
            "\n"
            "#### Step 3 — Decode the image\n"
            "\n"
            "```text\n"
            "image latent\n"
            "    ↓\n"
            "decoder\n"
            "    ↓\n"
            "pixels\n"
            "```\n"
            "\n"
            "### Interpolating between prompts\n"
            "\n"
            "Suppose we have two prompts:\n"
            "\n"
            "```text\n"
            "Prompt A:\n"
            "\"A friendly dog looking up in a field of flowers\"\n"
            "\n"
            "Prompt B:\n"
            "\"A horrifying tentacled creature hovering over a field of flowers\"\n"
            "```\n"
            "\n"
            "The text encoder produces representations:\n"
            "\n"
            "```text\n"
            "embedding_A\n"
            "embedding_B\n"
            "```\n"
            "\n"
            "Now choose intermediate points:\n"
            "\n"
            "```text\n"
            "A\n"
            "↓\n"
            "mostly A\n"
            "↓\n"
            "mixture\n"
            "↓\n"
            "mostly B\n"
            "↓\n"
            "B\n"
            "```\n"
            "\n"
            "Generate an image from each intermediate embedding.\n"
            "\n"
            "The resulting images can smoothly transform from one visual concept "
            "into the other.\n"
            "\n"
            "### Why interpolation works\n"
            "\n"
            "The representation space learned by the network is not just a "
            "collection of isolated labels.\n"
            "\n"
            "It behaves more like a smooth manifold of learned concepts.\n"
            "\n"
            "Nearby meaningful points tend to produce related semantic outputs.\n"
            "\n"
            "This is closely related to what we observed in VAEs:\n"
            "\n"
            "```text\n"
            "VAE latent point A\n"
            "    ↓ interpolate\n"
            "VAE latent point B\n"
            "    ↓\n"
            "smooth visual transformation\n"
            "```\n"
            "\n"
            "and similarly:\n"
            "\n"
            "```text\n"
            "text embedding A\n"
            "    ↓ interpolate\n"
            "text embedding B\n"
            "    ↓\n"
            "smooth change in generated images\n"
            "```\n"
            "\n"
            "### Linear interpolation versus spherical interpolation\n"
            "\n"
            "Simply averaging two large embedding vectors can move the "
            "intermediate representation into regions with unusual vector "
            "magnitudes.\n"
            "\n"
            "The source therefore demonstrates **spherical linear interpolation**, "
            "or SLERP.\n"
            "\n"
            "The intuition is easier than the formula.\n"
            "\n"
            "Imagine two points on the surface of a sphere.\n"
            "\n"
            "Ordinary linear interpolation takes a shortcut through the inside:\n"
            "\n"
            "```text\n"
            "A •──────────• B\n"
            "     through\n"
            "     interior\n"
            "```\n"
            "\n"
            "Spherical interpolation follows a curved path closer to the sphere's "
            "surface.\n"
            "\n"
            "```text\n"
            "      • • •\n"
            "   A •     • B\n"
            "```\n"
            "\n"
            "The actual learned manifold is not literally a sphere, but its "
            "vectors often have similar magnitudes, so spherical interpolation "
            "can provide a better approximation than a straight line through "
            "the representation space.\n"
            "\n"
            "### Deep networks as interpolation machines\n"
            "\n"
            "The chapter closes with a broad interpretation of deep learning:\n"
            "\n"
            "> Neural networks learn structured manifolds that capture patterns "
            "in complicated real-world probability distributions.\n"
            "\n"
            "Generation exploits those representations by sampling and "
            "interpolating through them.\n"
            "\n"
            "This perspective connects many ideas from the course:\n"
            "\n"
            "```text\n"
            "word embeddings\n"
            "image embeddings\n"
            "VAE latent spaces\n"
            "text encoder representations\n"
            "diffusion latents\n"
            "```\n"
            "\n"
            "All are examples of networks learning useful numerical spaces for "
            "complex real-world concepts.\n"
            "\n"
            "> **Recommended manual figure:** Add a visual sequence showing "
            "Prompt A → intermediate generated images → Prompt B after this explanation.\n"
            "\n"

            # Exercise EX02 is rendered here by the frontend.
            "{{exercise:M17.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Misconceptions
            # ----------------------------------------------------------------

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> A VAE maps every image to one exact deterministic latent vector.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The VAE encoder predicts parameters of a latent probability "
            "distribution. A latent vector is sampled from that distribution.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Reconstruction loss alone is enough to create a well-structured VAE latent space.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The VAE also uses a KL regularization term that encourages latent "
            "distributions to form a smooth, organized space.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> A diffusion model generates an image in one forward pass from random noise.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The chapter's diffusion process repeatedly denoises the current "
            "representation over multiple steps.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> The diffusion network must directly predict the final clean image.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "In the chapter implementation, the U-Net predicts the noise mask, "
            "which is then used to estimate the clean image.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> Text-to-image models literally understand anatomy and physics like humans do.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "The source characterizes these systems as statistical pattern "
            "recognition and interpolation models. They can generate visually "
            "convincing outputs while still producing physically inconsistent details.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> A negative prompt deletes objects from an already generated image.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Negative conditioning influences the denoising trajectory during "
            "generation, steering it away from representations associated with "
            "the negative text.\n"
            "\n"
            "### Misconception 7\n"
            "\n"
            "> Every arbitrary point between two embeddings will necessarily "
            "correspond to a perfect semantic concept.\n"
            "\n"
            "### Why this is wrong\n"
            "\n"
            "Interpolation works because useful representation regions tend to "
            "be smooth, but the learned manifold is approximate and does not "
            "guarantee perfect outputs everywhere.\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Key terminology
            # ----------------------------------------------------------------

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Generative model | Model designed to produce new samples resembling a learned data distribution |\n"
            "| Latent space | Learned numerical representation space containing compressed or abstract features |\n"
            "| Generator | Network that maps latent representations into generated samples |\n"
            "| Decoder | Network that converts latent vectors back into data such as images |\n"
            "| Autoencoder | Encoder-decoder model trained to reconstruct its own input |\n"
            "| VAE | Variational autoencoder that encodes inputs as latent probability distributions |\n"
            "| Encoder | Network mapping input data into latent representations |\n"
            "| `z_mean` | Mean parameter of a VAE latent distribution |\n"
            "| `z_log_var` | Log-variance parameter of a VAE latent distribution |\n"
            "| Reconstruction loss | Measures similarity between original input and reconstructed output |\n"
            "| KL divergence | Regularization term encouraging an organized VAE latent distribution |\n"
            "| Diffusion | Process of progressively adding noise to data |\n"
            "| Reverse diffusion | Iteratively removing noise to generate a sample |\n"
            "| Denoiser | Network trained to estimate or remove noise |\n"
            "| U-Net | Encoder-decoder-style architecture with skip connections commonly used for image denoising |\n"
            "| Diffusion time | Position within the diffusion or denoising process |\n"
            "| Diffusion schedule | Rule mapping diffusion time to signal and noise strengths |\n"
            "| Noise mask | Random noise added during diffusion training or predicted by the denoiser |\n"
            "| Text conditioning | Guiding image generation using numerical representations of a text prompt |\n"
            "| Text encoder | Model that converts text into continuous vector representations |\n"
            "| Positive prompt | Text describing concepts generation should move toward |\n"
            "| Negative prompt | Text describing concepts generation should move away from |\n"
            "| Stable Diffusion | Pretrained text-to-image diffusion model family used in the chapter example |\n"
            "| Interpolation | Computing intermediate points between learned representations |\n"
            "| SLERP | Spherical linear interpolation between vectors |\n"
            "| Manifold | Lower-dimensional structured region representing meaningful data variations |\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Self-check
            # ----------------------------------------------------------------

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What is a latent space?\n"
            "2. How can sampling latent points generate new images?\n"
            "3. What is the difference between an encoder and decoder?\n"
            "4. How does a VAE differ from a classical autoencoder?\n"
            "5. Why does a VAE predict `z_mean` and `z_log_var`?\n"
            "6. What role does random `epsilon` play during VAE sampling?\n"
            "7. Why does a VAE need both reconstruction loss and KL regularization?\n"
            "8. Why does the source use strided convolution in the VAE encoder?\n"
            "9. What is the basic idea behind diffusion image generation?\n"
            "10. What does the denoising U-Net predict in the chapter implementation?\n"
            "11. Why does the U-Net receive information about the current noise level?\n"
            "12. What is a diffusion schedule?\n"
            "13. How is training different from generation in a diffusion model?\n"
            "14. Why does generation begin from pure random noise?\n"
            "15. How does text conditioning change the denoising process?\n"
            "16. What is the purpose of a negative prompt?\n"
            "17. Why can text-to-image models still generate physical or anatomical mistakes?\n"
            "18. What are the three conceptual stages inside a text-to-image `generate()` call?\n"
            "19. What does it mean to interpolate between two text embeddings?\n"
            "20. Why might SLERP be preferable to ordinary linear interpolation for embeddings?\n"
            "\n"
            "---\n"
            "\n"

            # ----------------------------------------------------------------
            # Retention statement
            # ----------------------------------------------------------------

            "## Retain this idea\n"
            "\n"
            "**Image generation works by learning structured numerical spaces "
            "that represent visual data. VAEs create continuous latent spaces "
            "by encoding images as probability distributions, while diffusion "
            "models learn to turn noise into images through repeated denoising. "
            "Text-to-image systems add language embeddings to guide this "
            "denoising process toward specific concepts. Because these learned "
            "spaces are continuous, we can sample and interpolate through them "
            "to create entirely new visual outputs.**\n"
            "\n"
            "Keep this map in mind:\n"
            "\n"
            "```text\n"
            "VAE\n"
            "\n"
            "image\n"
            " ↓\n"
            "encoder\n"
            " ↓\n"
            "mean + variance\n"
            " ↓\n"
            "sample latent z\n"
            " ↓\n"
            "decoder\n"
            " ↓\n"
            "generated / reconstructed image\n"
            "\n"
            "\n"
            "DIFFUSION\n"
            "\n"
            "pure noise\n"
            " ↓\n"
            "predict noise\n"
            " ↓\n"
            "remove some noise\n"
            " ↓\n"
            "repeat\n"
            " ↓\n"
            "generated image\n"
            "\n"
            "\n"
            "TEXT-TO-IMAGE\n"
            "\n"
            "prompt\n"
            " ↓\n"
            "text encoder\n"
            " ↓\n"
            "text embedding\n"
            "      +\n"
            "random noise\n"
            "      ↓\n"
            "conditioned diffusion\n"
            "      ↓\n"
            "generated image\n"
            "```\n"
        ),

        "estimated_minutes": 180,

        "has_code_examples": True,

        "sections": [
            {
                "id": "latent-spaces-vaes",
                "title": "Latent Image Spaces and Variational Autoencoders",
                "order": 1,
            },
            {
                "id": "diffusion-models",
                "title": "Diffusion Models: Creating Images by Removing Noise",
                "order": 2,
            },
            {
                "id": "text-to-image",
                "title": "Text-to-Image Generation with Pretrained Diffusion Models",
                "order": 3,
            },
            {
                "id": "latent-interpolation",
                "title": "Exploring and Interpolating Learned Latent Spaces",
                "order": 4,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M17.L01.EX01",

            "title": "Trace a Variational Autoencoder",

            "lesson_code": "M17.L01",

            "section_id": "latent-spaces-vaes",

            "placement": "after_section",

            "description": (
                "Practice tracing information through a VAE and explaining why "
                "its probabilistic latent representation is useful for generation."
            ),

            "instructions": (
                "Imagine you are building a VAE for 64 × 64 grayscale images.\n\n"
                "1. Identify the three major components: encoder, sampling step, "
                "and decoder.\n"
                "2. Explain what the encoder should output instead of one fixed "
                "latent vector.\n"
                "3. Explain the roles of `z_mean`, `z_log_var`, and `epsilon`.\n"
                "4. Write the conceptual VAE sampling equation.\n"
                "5. Explain what reconstruction loss encourages the model to do.\n"
                "6. Explain what KL regularization encourages the latent space "
                "to do.\n"
                "7. Explain why sampling nearby latent points should ideally "
                "produce visually similar outputs.\n"
                "8. Explain how you would generate a brand-new image after the "
                "VAE has been trained."
            ),

            "expected_output": (
                "A complete description of the VAE pipeline from input image "
                "through probabilistic encoding, latent sampling, reconstruction "
                "loss, KL regularization, and latent-space generation."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "latent-space",
                "autoencoders",
                "vae",
                "sampling",
                "reconstruction-loss",
                "kl-divergence",
            ],
        },

        {
            "id": "M17.L01.EX02",

            "title": "Design a Text-Conditioned Diffusion Pipeline",

            "lesson_code": "M17.L01",

            "section_id": "latent-interpolation",

            "placement": "after_section",

            "description": (
                "Practice connecting diffusion training, generation, text "
                "conditioning, negative prompts, and latent interpolation."
            ),

            "instructions": (
                "Suppose you want to generate images from prompts such as "
                "`a red robot walking through a snowy forest`.\n\n"
                "1. Describe how an unconditional diffusion model would be trained.\n"
                "2. Explain what random diffusion time controls.\n"
                "3. Explain what the U-Net receives as input and what it predicts.\n"
                "4. Explain how generation begins after training.\n"
                "5. Add text conditioning to the pipeline and explain the role "
                "of the text encoder.\n"
                "6. Explain how a positive prompt influences the denoising trajectory.\n"
                "7. Explain conceptually how a negative prompt can steer generation.\n"
                "8. Explain the tradeoff involved in changing the number of "
                "diffusion steps.\n"
                "9. Suppose Prompt A describes a red robot and Prompt B describes "
                "a blue dragon. Explain how interpolating their text embeddings "
                "could create intermediate generated concepts.\n"
                "10. Explain why spherical interpolation may be preferred over "
                "simple linear interpolation for learned embedding vectors."
            ),

            "expected_output": (
                "A structured explanation of training and generation in a "
                "text-conditioned diffusion model, including denoising, prompts, "
                "diffusion steps, and latent-space interpolation."
            ),

            "difficulty": DifficultyLevel.intermediate,

            "skill_tested": [
                "diffusion",
                "unet",
                "denoising",
                "text-conditioning",
                "negative-prompts",
                "latent-interpolation",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M17.L01.QZ01",

        "title": "Image Generation — Knowledge Check",

        "lesson_code": "M17.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M17.L01.Q01",

                "section_id": "latent-spaces-vaes",

                "question": (
                    "What does a VAE encoder produce for each input image?"
                ),

                "options": [
                    "Only one deterministic class label",
                    "Parameters describing a latent probability distribution",
                    "A finished generated image",
                    "Only a random noise tensor",
                ],

                "correct": 1,

                "explanation": (
                    "A VAE encoder produces parameters such as the latent mean "
                    "and log variance. A latent vector is then sampled from the "
                    "resulting distribution before decoding."
                ),
            },

            {
                "id": "M17.L01.Q02",

                "section_id": "latent-spaces-vaes",

                "question": (
                    "Why is KL divergence included in the VAE training objective?"
                ),

                "options": [
                    "To convert grayscale images into RGB images",
                    "To encourage an organized, continuous latent distribution",
                    "To classify each latent point into a digit",
                    "To increase the image resolution",
                ],

                "correct": 1,

                "explanation": (
                    "The KL term regularizes the encoder distributions toward a "
                    "well-behaved latent distribution, helping the latent space "
                    "remain smooth and useful for sampling."
                ),
            },

            {
                "id": "M17.L01.Q03",

                "section_id": "diffusion-models",

                "question": (
                    "In the diffusion implementation described in the lesson, "
                    "what does the denoising U-Net primarily learn to predict?"
                ),

                "options": [
                    "The class label of the image",
                    "The text caption",
                    "The noise added to the image",
                    "The latent mean of a VAE",
                ],

                "correct": 2,

                "explanation": (
                    "Training corrupts images with known random noise. The "
                    "denoising network learns to predict that noise, allowing "
                    "the system to estimate a cleaner image."
                ),
            },

            {
                "id": "M17.L01.Q04",

                "section_id": "text-to-image",

                "question": (
                    "How does text conditioning help a diffusion model generate "
                    "an image matching a prompt?"
                ),

                "options": [
                    "The prompt is rendered directly on top of the image",
                    "A text encoder produces representations that guide the denoising process",
                    "The prompt replaces the random noise tensor",
                    "The prompt determines only the final image resolution",
                ],

                "correct": 1,

                "explanation": (
                    "The prompt is encoded into continuous representations. "
                    "These representations condition the denoising network, "
                    "guiding the image trajectory toward visual patterns "
                    "associated with the text."
                ),
            },

            {
                "id": "M17.L01.Q05",

                "section_id": "latent-interpolation",

                "type": "open",

                "question": (
                    "Compare VAEs and diffusion models as image-generation "
                    "approaches. Explain how each represents or generates images, "
                    "how generation is performed after training, how text "
                    "conditioning extends diffusion, and why interpolation "
                    "through learned latent representations can produce smooth "
                    "transitions between visual concepts."
                ),
            },
        ],

        "passing_score": 70,
    },
}
