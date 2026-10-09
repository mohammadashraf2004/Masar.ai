"""M10.L01 — From Diffusion Models to Real-World Deep Learning Projects.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Deep Learning with PyTorch, Second Edition, Chapters 10–11.
Instructor-authored curriculum adaptation.

Quality standard:
- balanced quiz-answer positions
- explicit training/evaluation best practices
- realistic study-time estimate
- learning checkpoints after dense sections
"""

from app.models.learning import DifficultyLevel


LESSON_CODE = "M10.L01"
MODULE_ORDER = 10
MODULE_TITLE = "Generative Models & Real-World Project Design"
MODULE_DESCRIPTION = (
    "Learn diffusion models from first principles, including forward noising, noise prediction, "
    "and iterative reverse sampling, then transition into the engineering mindset required for a "
    "large-scale real-world deep-learning project using 3D CT lung-cancer detection as the case study."
)

SOURCE_CHAPTER = "10–11"
SOURCE_PAGES = "Chapters 10–11 (page ranges not provided in source excerpts)"


TOPIC = {
    "title": "From Diffusion Models to Real-World Deep Learning Projects",
    "slug": "applied-deep-learning-m10-l01",
    "description": (
        "A combined lesson covering image-generation foundations with diffusion models and the "
        "engineering discipline needed to structure, scope, and prepare a complex deep-learning "
        "project involving 3D CT data."
    ),
    "order": 1,
    "difficulty": DifficultyLevel.intermediate,
    "estimated_hours": 7.5,
    "skill_tags": [
        "generative-ai",
        "diffusion-models",
        "vae",
        "gan",
        "noise-schedule",
        "forward-diffusion",
        "reverse-diffusion",
        "noise-prediction",
        "sinusoidal-embedding",
        "mse-loss",
        "sampling",
        "real-world-ml",
        "project-decomposition",
        "medical-imaging",
        "ct-scan",
        "voxel-data",
        "segmentation",
        "classification",
        "luna16",
        "data-readiness",
        "module-10",
    ],
    "prerequisite_ids": ["M09.L01"],

    "lesson": {
        "title": "From Diffusion Models to Real-World Deep Learning Projects",
        "content": (
            "# From Diffusion Models to Real-World Deep Learning Projects\n\n"
            "> **Course:** Applied Deep Learning with PyTorch  \n"
            "> **Lesson:** M10.L01  \n"
            "> **Sources:** *Deep Learning with PyTorch, Second Edition*, Chapters 10–11.  \n"
            "> **Structure:** Part A — Diffusion Models. Part B — Real-World Project Design with CT Data.  \n"
            "> **Study expectation:** approximately **7.5 hours** for a careful first pass including code tracing, "
            "checkpoints, and exercises.\n\n"
            "These two chapters cover very different subjects, but together they teach an important progression:\n\n"
            "1. understand a modern deep-learning architecture from first principles,\n"
            "2. then learn that solving a real project requires much more than choosing a model.\n\n"
            "---\n\n"

            "## Learning outcomes\n\n"
            "By the end of this lesson, you should be able to:\n\n"
            "### Diffusion-model skills\n"
            "- Compare the high-level ideas behind VAEs, GANs, and diffusion models.\n"
            "- Explain the shared generative goal of learning a data distribution and sampling new examples.\n"
            "- Explain the forward diffusion process as gradual corruption with scheduled Gaussian noise.\n"
            "- Describe the role of beta, alpha, and cumulative alpha products.\n"
            "- Explain why closed-form forward diffusion is useful during training.\n"
            "- Explain why a denoising model is trained to predict added noise.\n"
            "- Describe the role of timestep information and sinusoidal embeddings.\n"
            "- Implement the diffusion loss using mean squared error between real and predicted noise.\n"
            "- Explain iterative reverse diffusion and why sampling is slower than one-shot generation.\n"
            "- Use appropriate PyTorch training and inference practices for diffusion code.\n\n"
            "### Real-world project skills\n"
            "- Explain why serious deep-learning work often spends more effort on data and problem framing than on model code.\n"
            "- Break a complex project into smaller semi-independent tasks.\n"
            "- Explain CT scans as 3D arrays of single-channel voxel data.\n"
            "- Explain why voxel spacing and scanner settings matter.\n"
            "- Distinguish data loading, segmentation, candidate classification, and patient-level reasoning.\n"
            "- Explain why limiting model scope can make learning and debugging easier.\n"
            "- Describe the role of nodules in the lung-cancer project.\n"
            "- Explain why data imbalance and tiny targets make the full problem difficult.\n"
            "- Describe the role of the LUNA Grand Challenge dataset and annotations.\n"
            "- Perform a practical readiness check for compute, storage, data quality, and project structure.\n\n"
            "---\n\n"

            "# Part A — Diffusion Models for Image Generation\n\n"

            "## 1. The generative goal is the same across text and images\n\n"
            "Chapter 9 generated text by learning which tokens are likely to follow earlier tokens. "
            "Image generation looks different because images are spatial rather than purely sequential.\n\n"
            "But the deeper goal is the same:\n\n"
            "> **Learn enough of the training data's probability structure that we can sample new, plausible examples.**\n\n"
            "For text, a sample is a sequence of tokens. For images, a sample is a structured grid of pixel values. "
            "The representation and architecture change, but the generative-learning goal remains.\n\n"
            '{{image:text-vs-image-generation}}'
            '\n\n'
            "---\n\n"

            "## 2. Before diffusion: VAEs and GANs\n\n"
            "The chapter briefly places diffusion models in historical context.\n\n"
            "### Variational autoencoders (VAEs)\n\n"
            "A VAE uses two broad components:\n\n"
            "```text\n"
            "input -> encoder -> latent representation -> decoder -> reconstruction\n"
            "```\n\n"
            "For generation, new latent samples can be passed through the decoder to create new data.\n\n"
            "### Generative adversarial networks (GANs)\n\n"
            "A GAN uses two networks with competing roles:\n\n"
            "- **generator** — creates synthetic samples from random noise,\n"
            "- **discriminator** — tries to distinguish real samples from generated ones.\n\n"
            "Their adversarial interaction pushes the generator toward more realistic outputs.\n\n"
            "### Diffusion models\n\n"
            "Diffusion takes a different approach:\n\n"
            "```text\n"
            "real sample\n"
            " -> gradually add noise\n"
            " -> reach near-random noise\n"
            "\n"
            "train a model to learn how to reverse that corruption\n"
            "```\n\n"
            "[[IMAGE_NEEDED: VAE vs GAN vs diffusion | Three side-by-side simplified diagrams: encoder/decoder latent model, "
            "generator/discriminator adversarial model, and forward-noise/reverse-denoise diffusion process | Learner should "
            "notice that all generate new samples but learn through different mechanisms]]\n\n"
            "---\n\n"

            "## 3. Diffusion intuition: destroy structure slowly, then learn to restore it\n\n"
            "Imagine a structured image being corrupted little by little.\n\n"
            "At timestep 0, the sample is clear. After many timesteps, so much Gaussian noise has been added that the original "
            "structure becomes unrecognizable.\n\n"
            "The forward process is deliberately controlled. We know exactly how noise is injected.\n\n"
            "The model is then trained to learn information useful for reversing that corruption.\n\n"
            "A helpful mental picture is:\n\n"
            "```text\n"
            "structured data\n"
            "  -> slightly noisy\n"
            "  -> more noisy\n"
            "  -> heavily noisy\n"
            "  -> near-random noise\n"
            "\n"
            "reverse learned process:\n"
            "noise -> structure\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Forward and reverse diffusion | A sequence of the same simple shape progressing from clean to heavily "
            "noised left-to-right, with a reverse arrow from noise back to structure | Learner should notice that training relies "
            "on a known corruption process and generation relies on a learned denoising process]]\n\n"
            "---\n\n"

            "## 4. Learn diffusion first on 2D points\n\n"
            "Instead of beginning with full RGB images, the chapter uses a simpler visualization: an image outline represented "
            "as `(x, y)` coordinate points.\n\n"
            "For the PyTorch-logo example, the source constructs a tensor roughly shaped:\n\n"
            "```text\n"
            "[3177, 2]\n"
            "```\n\n"
            "Every row is one 2D point.\n\n"
            "This simplification is educationally valuable because we can directly watch the data cloud spread under forward diffusion "
            "and later contract into a recognizable structure during sampling.\n\n"
            "The equations used on `(x, y)` points are conceptually transferable to higher-dimensional image values.\n\n"
            "---\n\n"

            "## 5. The beta noise schedule\n\n"
            "Diffusion does not add the same amount of noise at every step. A **schedule** controls the process.\n\n"
            "The chapter uses a simple linear beta schedule:\n\n"
            "```python\n"
            "def linear_beta_schedule(timesteps, start=0.0001, end=0.02):\n"
            "    return torch.linspace(start, end, timesteps)\n\n"
            "T = 1000\n"
            "betas = linear_beta_schedule(T)\n"
            "```\n\n"
            "Each beta value controls how strongly the current sample is mixed with fresh random noise at that timestep.\n\n"
            "The schedule is therefore not a cosmetic implementation detail. It shapes how quickly information is destroyed and can affect training behavior.\n\n"
            "[[IMAGE_NEEDED: Linear beta noise schedule | A plot of beta against timestep increasing from a small starting value "
            "to a larger final value | Learner should notice that the amount of corruption is scheduled rather than arbitrary]]\n\n"
            "---\n\n"

            "## 6. One forward diffusion step\n\n"
            "A simplified forward step is:\n\n"
            "```python\n"
            "def diffuse_points(points, beta):\n"
            "    new_mean = torch.sqrt(1 - beta) * points\n"
            "    noise = torch.randn_like(points)\n"
            "    perturbation = torch.sqrt(beta) * noise\n"
            "    return new_mean + perturbation, noise\n"
            "```\n\n"
            "Two things happen simultaneously:\n\n"
            "1. the previous structure is scaled down,\n"
            "2. fresh Gaussian noise is added.\n\n"
            "As beta grows through the schedule, the original structure contributes less and randomness contributes more.\n\n"
            "Repeated across many timesteps, the original point pattern eventually becomes visually indistinguishable from noise.\n\n"
            "---\n\n"

            "## 7. Closed-form forward diffusion\n\n"
            "Repeatedly simulating every previous timestep would be inconvenient during training.\n\n"
            "Diffusion gives us a major shortcut: we can sample a noisy version of the original data directly at an arbitrary timestep.\n\n"
            "Define:\n\n"
            "```python\n"
            "alphas = 1.0 - betas\n"
            "alphas_cumprod = torch.cumprod(alphas, dim=0)\n"
            "sqrt_alphas_cumprod = torch.sqrt(alphas_cumprod)\n"
            "sqrt_one_minus_alphas_cumprod = torch.sqrt(1.0 - alphas_cumprod)\n"
            "```\n\n"
            "Then one conceptual implementation is:\n\n"
            "```python\n"
            "def forward_diffusion_sample(x0, t):\n"
            "    noise = torch.randn_like(x0)\n"
            "    signal_scale = reshape_for_x(sqrt_alphas_cumprod[t], x0)\n"
            "    noise_scale = reshape_for_x(sqrt_one_minus_alphas_cumprod[t], x0)\n"
            "    x_t = signal_scale * x0 + noise_scale * noise\n"
            "    return x_t, noise\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Closed-form diffusion at arbitrary timesteps | One clean point-cloud sample branches directly to several "
            "different noise levels t=0, 250, 500, 800, 999 without drawing every intermediate transition | Learner should notice "
            "that training can jump directly to a random timestep rather than simulating all earlier steps]]\n\n"
            "This is one of the most important practical ideas in the chapter: **training can choose random timesteps efficiently**.\n\n"

            "### Learning checkpoint 1 — Forward diffusion\n\n"
            "Before continuing, make sure you can explain:\n\n"
            "1. what beta controls,\n"
            "2. why `alpha = 1 - beta`,\n"
            "3. what the cumulative alpha product represents intuitively,\n"
            "4. why closed-form forward diffusion makes training easier.\n\n"
            "{{exercise:M10.L01.EX01}}\n\n"
            "---\n\n"

            "## 8. What the neural network actually learns\n\n"
            "The denoising model is not directly asked to output the clean final image in one step.\n\n"
            "Instead, it receives:\n\n"
            "- a noisy sample `x_t`,\n"
            "- its timestep `t`,\n\n"
            "and predicts the noise that was added.\n\n"
            "Conceptually:\n\n"
            "```text\n"
            "(x_t, t) -> neural network -> predicted_noise\n"
            "```\n\n"
            "Because the forward process gives us the exact random noise used to create `x_t`, training has a precise target.\n\n"
            "That target is self-generated by the corruption process.\n\n"
            "---\n\n"

            "## 9. The model needs to know the timestep\n\n"
            "A sample at timestep 10 needs different denoising behavior from a sample at timestep 900.\n\n"
            "So the model needs information about **where it is in the diffusion process**.\n\n"
            "The chapter uses sinusoidal embeddings for:\n\n"
            "- timestep,\n"
            "- the first point coordinate,\n"
            "- the second point coordinate.\n\n"
            "The implementation of the sinusoidal embedding helper is omitted in the source excerpt, but its role is explicit: transform scalar values "
            "into richer higher-dimensional representations before feeding them to an MLP.\n\n"
            "[[IMAGE_NEEDED: Denoising model input embeddings | Noisy x-coordinate, noisy y-coordinate, and timestep each pass through their "
            "own embedding transform; the three embeddings are concatenated and fed into an MLP that outputs two noise values | Learner should "
            "notice that the model conditions its prediction on both location and noise level]]\n\n"
            "---\n\n"

            "## 10. Denoising model architecture\n\n"
            "The source model follows this structure:\n\n"
            "```text\n"
            "x-coordinate -> embedding \\\n"
            "                           \\\n"
            "y-coordinate -> embedding ---> concatenate -> MLP -> predicted (noise_x, noise_y)\n"
            "                           /\n"
            "timestep     -> embedding /\n"
            "```\n\n"
            "Its final layer outputs two values because every training point has two coordinates and therefore two noise components to predict.\n\n"
            "The network is intentionally simple. The learning objective, not model sophistication, is the main focus of the chapter.\n\n"
            "---\n\n"

            "## 11. Diffusion loss: compare predicted noise with actual noise\n\n"
            "Training becomes surprisingly simple once the forward process exists:\n\n"
            "```python\n"
            "def get_loss(model, x0, t):\n"
            "    x_noisy, noise = forward_diffusion_sample(x0, t)\n"
            "    noise_pred = model(x_noisy, t)\n"
            "    return F.mse_loss(noise_pred, noise)\n"
            "```\n\n"
            "The target is the exact Gaussian noise used to corrupt the clean sample.\n\n"
            "Mean squared error asks:\n\n"
            "> **How close was the model's predicted noise to the real noise?**\n\n"
            "If the model learns this task across many examples and many timesteps, it gains the ability to perform the reverse process iteratively.\n\n"
            "---\n\n"

            "## 12. Train across random timesteps\n\n"
            "The source samples a random timestep for each point and optimizes with Adam.\n\n"
            "For a cleaner Masar implementation:\n\n"
            "```python\n"
            "def train_diffusion(model, optimizer, x0, timesteps, device, num_epochs):\n"
            "    model.train()\n"
            "    x0 = x0.to(device)\n\n"
            "    for epoch in range(num_epochs):\n"
            "        t = torch.randint(\n"
            "            0,\n"
            "            timesteps,\n"
            "            (x0.shape[0],),\n"
            "            device=device,\n"
            "        )\n\n"
            "        optimizer.zero_grad(set_to_none=True)\n"
            "        loss = get_loss(model, x0, t)\n"
            "        loss.backward()\n"
            "        optimizer.step()\n"
            "```\n\n"
            "Important best practices:\n\n"
            "- call `model.train()` explicitly,\n"
            "- keep model and data on the same device,\n"
            "- clear old gradients before backward,\n"
            "- log `loss.item()` rather than holding graph-connected loss tensors,\n"
            "- checkpoint model state during long training runs.\n\n"
            "The chapter trains for many iterations because learning denoising across all noise levels is not a trivial problem.\n\n"
            "{{exercise:M10.L01.EX02}}\n\n"
            "---\n\n"

            "## 13. Reverse diffusion: generation starts from noise\n\n"
            "Training began with clean data and added noise.\n\n"
            "Generation does the opposite:\n\n"
            "```text\n"
            "random noise at timestep T\n"
            " -> estimate/remove some noise\n"
            " -> timestep T-1\n"
            " -> estimate/remove more noise\n"
            " -> ...\n"
            " -> timestep 0\n"
            " -> structured sample\n"
            "```\n\n"
            "Unlike the closed-form forward process, the reverse process in this chapter is iterative.\n\n"
            "That repeated model evaluation is one reason diffusion sampling can be relatively slow.\n\n"
            "---\n\n"

            "## 14. One reverse sampling step\n\n"
            "The reverse equation combines:\n\n"
            "- the current noisy sample,\n"
            "- the model's predicted noise,\n"
            "- timestep-dependent coefficients,\n"
            "- controlled random noise except at the final step.\n\n"
            "The source wraps sampling in `@torch.no_grad()` because gradients are unnecessary during generation.\n\n"
            "A simplified structure is:\n\n"
            "```python\n"
            "@torch.no_grad()\n"
            "def sample_timestep(model, x, t):\n"
            "    # gather timestep-specific diffusion coefficients\n"
            "    # predict current noise with model(x, t)\n"
            "    # estimate the previous-step mean\n"
            "    # add controlled random noise unless t == 0\n"
            "    return x_previous\n"
            "```\n\n"
            "For generation, also switch the model into evaluation mode:\n\n"
            "```python\n"
            "model.eval()\n"
            "```\n\n"
            "`model.eval()` and `torch.no_grad()` solve different problems:\n\n"
            "- `eval()` switches modules with training/evaluation behavior,\n"
            "- `no_grad()` disables gradient graph construction.\n\n"
            "---\n\n"

            "## 15. The full sampling loop\n\n"
            "Sampling begins from random Gaussian points:\n\n"
            "```python\n"
            "sample = torch.randn(batch_size, 2, device=device)\n"
            "```\n\n"
            "Then move backward through timesteps:\n\n"
            "```python\n"
            "model.eval()\n\n"
            "with torch.no_grad():\n"
            "    for i in range(T - 1, -1, -1):\n"
            "        t = torch.full(\n"
            "            (batch_size,),\n"
            "            i,\n"
            "            dtype=torch.long,\n"
            "            device=device,\n"
            "        )\n"
            "        sample = sample_timestep(model, sample, t)\n"
            "```\n\n"
            "[[IMAGE_NEEDED: Reverse diffusion sampling progression | Random 2D points at a late timestep gradually reorganizing through "
            "several intermediate snapshots into the PyTorch-logo point-cloud structure | Learner should notice that generation is "
            "iterative rather than a single forward model call]]\n\n"
            "The chapter's point-cloud example eventually reconstructs a shape resembling the original training distribution.\n\n"

            "### Learning checkpoint 2 — Training versus generation\n\n"
            "Can you explain the difference between these two directions?\n\n"
            "```text\n"
            "TRAINING:\n"
            "clean x0 -> choose random t -> add known noise -> predict noise -> MSE\n\n"
            "GENERATION:\n"
            "random xT -> repeatedly predict/remove noise -> structured x0-like sample\n"
            "```\n\n"
            "If that distinction is clear, you understand the core diffusion workflow.\n\n"
            "{{exercise:M10.L01.EX03}}\n\n"
            "---\n\n"

            "## 16. What to retain from diffusion models\n\n"
            "The chapter deliberately uses a toy 2D dataset so the mechanics remain visible.\n\n"
            "The same high-level principles can extend to image tensors:\n\n"
            "- corrupt data according to a known schedule,\n"
            "- train a model to estimate the corruption/noise,\n"
            "- start generation from noise,\n"
            "- iteratively reverse the process.\n\n"
            "Modern diffusion systems contain much more sophisticated architectures and conditioning mechanisms, but this simple model exposes the foundational logic.\n\n"
            "---\n\n"

            "# Part B — Engineering a Large Real-World Deep-Learning Project\n\n"

            "## 17. A model is only one part of a real project\n\n"
            "Chapter 11 changes perspective dramatically.\n\n"
            "Instead of introducing a new layer type, it asks a more realistic engineering question:\n\n"
            "> **How do we approach a difficult problem when the data is messy, the targets are tiny, resources are limited, and no library hands us training samples in exactly the format we need?**\n\n"
            "The case study is lung-tumor detection from chest CT scans.\n\n"
            "The chapter explicitly treats this as a teaching project rather than a clinically deployable medical system. Its purpose is to develop the habits required for difficult deep-learning projects.\n\n"
            "---\n\n"

            "## 18. Understand the domain before writing the model\n\n"
            "One of the strongest lessons in Chapter 11 is that practitioners cannot apply deep learning blindly.\n\n"
            "Before designing the pipeline, we need to understand:\n\n"
            "- what the input physically represents,\n"
            "- how it was acquired,\n"
            "- which variations are meaningful,\n"
            "- what artifacts or scanner settings can change the data,\n"
            "- how the final task is actually judged.\n\n"
            "Domain knowledge narrows the space of possible approaches and helps us avoid preprocessing choices that destroy useful information.\n\n"
            "This principle generalizes far beyond medicine—to satellite imagery, autonomous-driving cameras, industrial sensors, audio, and many other domains.\n\n"
            "---\n\n"

            "## 19. CT scans are 3D single-channel voxel grids\n\n"
            "A CT scan can be understood as a stack of 2D slices forming a 3D volume.\n\n"
            "The 3D analogue of a pixel is a **voxel**.\n\n"
            "Conceptually:\n\n"
            "```text\n"
            "2D image  -> pixels     -> H × W\n"
            "3D CT     -> voxels     -> D × H × W\n"
            "```\n\n"
            "Each voxel stores a numeric intensity related to the radiodensity of the material inside that small volume.\n\n"
            "High-density material such as bone often appears bright, while air-filled lung regions appear dark in common visualizations.\n\n"
            "[[IMAGE_NEEDED: CT volume as stacked slices and voxels | Several grayscale CT slices stacked into a 3D volume, with one small "
            "rectangular voxel highlighted and labeled with depth/height/width spacing | Learner should notice that CT is volumetric data "
            "and that voxel dimensions do not have to be cubic]]\n\n"
            "---\n\n"

            "## 20. Array coordinates are not automatically physical coordinates\n\n"
            "A key subtlety is voxel spacing.\n\n"
            "CT scanners may sample differently along the head-to-foot axis than within each 2D slice. As a result, voxels can be rectangular prisms rather than cubes.\n\n"
            "This matters because:\n\n"
            "```text\n"
            "one array step in axis A\n"
            "```\n\n"
            "does not necessarily represent the same real-world distance as:\n\n"
            "```text\n"
            "one array step in axis B\n"
            "```\n\n"
            "Later data-processing code must therefore map between physical coordinates and voxel indexes carefully.\n\n"
            "This is exactly the type of domain-specific detail that can quietly break a project if preprocessing is designed without understanding the data source.\n\n"
            "---\n\n"

            "## 21. Break the cancer-detection problem into smaller tasks\n\n"
            "The source chooses a modular pipeline rather than one monolithic end-to-end network.\n\n"
            "The main stages are:\n\n"
            "```text\n"
            "1. Data loading\n"
            "2. Segmentation / candidate localization\n"
            "3. Candidate classification\n"
            "4. Combine candidate-level results into patient-level reasoning\n"
            "```\n\n"
            "The chapter's summary emphasizes three rough project steps: **data loading, segmentation, and classification**.\n\n"
            "[[IMAGE_NEEDED: Lung-cancer project pipeline | Raw CT volume flows into data loading, then segmentation/candidate localization, "
            "then cropped candidate volumes into a 3D classifier, then candidate results combined for patient-level output | Learner should "
            "notice that one hard problem has been decomposed into smaller interfaces]]\n\n"
            "The advantage is not that modularity is always mathematically optimal. The advantage is that each piece becomes easier to understand, train, debug, and improve independently.\n\n"
            "{{exercise:M10.L01.EX04}}\n\n"
            "---\n\n"

            "## 22. Why not throw the entire CT scan into one network?\n\n"
            "The target occupies an extremely small fraction of the scan.\n\n"
            "Most voxels are irrelevant to the question of whether a malignant lung nodule exists. The source emphasizes that even in a positive scan, essentially all voxels are still non-cancerous.\n\n"
            "This creates several difficulties:\n\n"
            "- extreme foreground/background imbalance,\n"
            "- very large input volumes,\n"
            "- limited labeled examples,\n"
            "- expensive training,\n"
            "- many normal anatomical structures that can look suspicious.\n\n"
            "Restricting later classification to **candidate nodules** reduces the scope dramatically.\n\n"
            "[[IMAGE_NEEDED: Whole CT versus candidate crop | Left side shows a large chest CT slice/volume with one tiny highlighted nodule; "
            "right side shows a zoomed candidate crop around the nodule | Learner should notice how little of the full scan is relevant to "
            "the focused classification problem]]\n\n"
            "Scope reduction is a general ML engineering technique: if the task can be broken into reliable stages, each model can specialize on a narrower problem.\n\n"
            "---\n\n"

            "## 23. What is a nodule in this project?\n\n"
            "The source uses **nodule** for small lump-like structures in the lung that may be benign or malignant.\n\n"
            "The important modeling point is not the exact medical taxonomy. It is this constraint:\n\n"
            "> the cancers of interest will appear as nodules, so later classification can focus on nodule candidates rather than arbitrary body tissue.\n\n"
            "A candidate nodule may still be:\n\n"
            "- benign,\n"
            "- malignant,\n"
            "- or a non-nodule structure that visually resembles one.\n\n"
            "That is why localization and classification are separate problems.\n\n"
            "---\n\n"

            "## 24. Segmentation and classification solve different questions\n\n"
            "### Segmentation / candidate localization\n\n"
            "Question:\n\n"
            "> **Where are suspicious voxels or structures?**\n\n"
            "This produces spatial information—similar to a heatmap or mask.\n\n"
            "### Candidate classification\n\n"
            "Question:\n\n"
            "> **Given a focused 3D crop, is this candidate actually a nodule, and later, is it malignant?**\n\n"
            "The candidate classifier can use 3D convolutions because the relevant spatial evidence is local to the candidate volume.\n\n"
            "This resembles the 2D convolution logic from Chapter 8, extended into volumetric data.\n\n"
            "---\n\n"

            "## 25. Implementation order does not have to match pipeline order\n\n"
            "The final system is conceptually:\n\n"
            "```text\n"
            "load -> segment -> classify\n"
            "```\n\n"
            "But the book does not implement everything strictly in that order.\n\n"
            "It first tackles the familiar classification side before returning to the more complicated segmentation problem.\n\n"
            "This is an excellent engineering lesson:\n\n"
            "> **Build the subsystem that gives you the best learning/debugging leverage first, not necessarily the subsystem that appears first in the final diagram.**\n\n"
            "Modular design makes this possible because interfaces let pieces be developed semi-independently.\n\n"
            "---\n\n"

            "## 26. The LUNA Grand Challenge dataset\n\n"
            "The project uses data from the LUNA lung-nodule challenge.\n\n"
            "The important characteristics emphasized by the source are:\n\n"
            "- real CT scan volumes,\n"
            "- human-annotated nodule-related labels/locations,\n"
            "- standardized challenge tasks,\n"
            "- enough structure to support both candidate detection and false-positive reduction work.\n\n"
            "High-quality annotations are a major asset. Real projects often succeed or fail based as much on label quality and data consistency as on model architecture.\n\n"
            "The source also warns that CT data outside a curated dataset can vary significantly across scanners and preprocessing pipelines, so assumptions learned from one dataset must be rechecked before combining new sources.\n\n"
            "---\n\n"

            "## 27. Resource planning is part of model engineering\n\n"
            "Chapter 11 explicitly discusses hardware and storage requirements.\n\n"
            "The complete project can require:\n\n"
            "- a GPU for practical training speed,\n"
            "- large amounts of raw-data storage,\n"
            "- additional cache space for processed subsets,\n"
            "- time for downloading and decompressing large archives.\n\n"
            "The source describes the full setup as requiring roughly hundreds of gigabytes of disk space once raw scans, caches, and model artifacts are included.\n\n"
            "If full resources are unavailable, the book notes that using only one or two data subsets is possible for learning, though model quality will suffer.\n\n"
            "This is a useful general rule:\n\n"
            "> **Before training, estimate compute, memory, storage, and iteration time. A theoretically good design that cannot be iterated on is often a poor practical design.**\n\n"
            "---\n\n"

            "## 28. Data organization and reproducibility matter\n\n"
            "The LUNA data is distributed across subsets such as:\n\n"
            "```text\n"
            "subset0\n"
            "subset1\n"
            "...\n"
            "subset9\n"
            "```\n\n"
            "Additional metadata files such as candidate and annotation CSV files provide the labels/locations needed by later stages.\n\n"
            "A production-minded project should keep clear separation between:\n\n"
            "- immutable raw downloads,\n"
            "- derived caches,\n"
            "- training splits,\n"
            "- model checkpoints,\n"
            "- generated reports/metrics.\n\n"
            "That organizational advice extends the source's project-preparation lesson and helps make debugging and reruns safer.\n\n"
            "---\n\n"

            "## 29. Learning checkpoint — before writing a model, can you answer these?\n\n"
            "For any difficult domain project, you should be able to answer:\n\n"
            "1. What exactly does one input tensor represent physically?\n"
            "2. What exactly is the target?\n"
            "3. Which parts of the input are irrelevant most of the time?\n"
            "4. How reliable are the labels?\n"
            "5. Can the task be decomposed?\n"
            "6. Which subproblem should be prototyped first?\n"
            "7. What compute and storage constraints apply?\n"
            "8. Which domain-specific transformations could silently invalidate the data?\n"
            "9. What does success mean at each subsystem boundary?\n\n"
            "If these questions do not have good answers, training a larger network is unlikely to fix the project.\n\n"
            "{{exercise:M10.L01.EX05}}\n\n"
            "---\n\n"

            "## 30. The combined lesson: model mechanics and project mechanics\n\n"
            "The two chapters fit together better than they first appear.\n\n"
            "Chapter 10 asks:\n\n"
            "> **How does a modern generative model work internally?**\n\n"
            "Chapter 11 asks:\n\n"
            "> **How do we turn deep-learning knowledge into a workable real-world project?**\n\n"
            "Together they reveal two levels of competence:\n\n"
            "### Level 1 — Model competence\n\n"
            "- understand the data representation,\n"
            "- define the learning objective,\n"
            "- train correctly,\n"
            "- sample/evaluate correctly.\n\n"
            "### Level 2 — System competence\n\n"
            "- understand the domain,\n"
            "- acquire and organize data,\n"
            "- reduce scope intelligently,\n"
            "- decompose the project,\n"
            "- budget compute/storage,\n"
            "- choose meaningful interfaces and metrics.\n\n"
            "Real machine-learning engineering requires both.\n\n"
            "---\n\n"

            "## Important misconceptions\n\n"
            "### Misconception 1: A diffusion model learns to reconstruct the clean sample directly in one pass\n\n"
            "In this chapter's formulation, the training target is the noise that was added at a selected timestep. Generation then uses repeated denoising steps.\n\n"
            "### Misconception 2: The forward diffusion loop must always be simulated from timestep 0 to timestep t\n\n"
            "The closed-form formulation allows training code to sample a noisy version directly at an arbitrary timestep.\n\n"
            "### Misconception 3: `model.eval()` and `torch.no_grad()` mean the same thing\n\n"
            "`eval()` changes behavior of modules with training/evaluation modes. `no_grad()` disables autograd graph construction. They are complementary, not interchangeable.\n\n"
            "### Misconception 4: A more complicated neural network automatically solves a harder domain problem\n\n"
            "Chapter 11 emphasizes that data quality, task framing, domain knowledge, resource limits, and project structure can dominate the difficulty.\n\n"
            "### Misconception 5: A CT scan is simply a normal 2D grayscale image\n\n"
            "A CT scan is volumetric. It contains a depth axis, voxel spacing, scanner-specific properties, and real-world coordinate relationships that matter for preprocessing.\n\n"
            "### Misconception 6: The final pipeline must be developed strictly from first stage to last stage\n\n"
            "Modular projects can be developed in an order chosen for learning and debugging leverage, as long as subsystem interfaces remain clear.\n\n"
            "### Misconception 7: Perfectly curated challenge data guarantees future production data will behave the same way\n\n"
            "The source warns that real CT data may vary across scanners and processing programs. Assumptions must be revalidated when data sources change.\n\n"
            "---\n\n"

            "## Key terminology\n\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Generative model | Model intended to learn a data distribution well enough to produce new samples. |\n"
            "| VAE | Encoder-decoder generative architecture using a learned latent representation. |\n"
            "| GAN | Generator-discriminator architecture trained adversarially. |\n"
            "| Diffusion model | Generative model trained around a controlled noise-addition process and learned reverse denoising. |\n"
            "| Beta schedule | Sequence controlling noise intensity over diffusion timesteps. |\n"
            "| Alpha | Usually `1 - beta`; controls retained signal in the forward process. |\n"
            "| Cumulative alpha product | Quantity used to jump directly from clean data to a chosen diffusion timestep. |\n"
            "| Gaussian noise | Random noise sampled from a normal distribution. |\n"
            "| Denoising model | Neural network predicting noise/corruption from a noisy sample and timestep. |\n"
            "| Sinusoidal embedding | Fixed periodic feature mapping used to represent scalar positions/timesteps. |\n"
            "| Reverse diffusion | Iterative process that transforms random noise into a structured sample. |\n"
            "| Voxel | 3D analogue of a pixel; one cell in a volumetric grid. |\n"
            "| CT scan | 3D medical imaging volume represented as single-channel radiodensity values. |\n"
            "| Voxel spacing | Real-world physical size represented by one step along each CT array axis. |\n"
            "| Nodule | Small lung lump/structure that may be benign or malignant. |\n"
            "| Segmentation | Spatial prediction identifying voxels/regions of interest. |\n"
            "| Candidate | Local region proposed for later classification. |\n"
            "| Classification | Assignment of a candidate to a discrete category such as nodule/non-nodule. |\n"
            "| Project decomposition | Breaking a complex system into smaller semi-independent problems. |\n"
            "| LUNA | Lung Nodule Analysis challenge/dataset used as the project's data source. |\n"
            "| Cache | Derived data stored for faster repeated access during training/experimentation. |\n\n"
            "---\n\n"

            "## Self-check\n\n"
            "### Diffusion\n"
            "1. What generative objective do text models and image models share?\n"
            "2. What are the high-level differences between VAE, GAN, and diffusion training?\n"
            "3. What happens during forward diffusion?\n"
            "4. What does beta control?\n"
            "5. Why does the retained contribution of the original sample shrink over time?\n"
            "6. Why is Gaussian noise convenient in the chapter's implementation?\n"
            "7. What problem does the closed-form forward equation solve?\n"
            "8. What are `alphas` and `alphas_cumprod` used for?\n"
            "9. Why is timestep information given to the denoising model?\n"
            "10. What exactly is the training target in the diffusion loss?\n"
            "11. Why does mean squared error fit that target?\n"
            "12. Why are random timesteps sampled during training?\n"
            "13. Why does reverse diffusion require repeated model calls?\n"
            "14. Why is `torch.no_grad()` appropriate during sampling?\n"
            "15. What is the difference between `model.train()` and `model.eval()`?\n\n"
            "### Real-world project design\n"
            "16. Why does Chapter 11 spend so much time before building a model?\n"
            "17. What is a voxel?\n"
            "18. Why might CT voxels not be cubic?\n"
            "19. Why is physical spacing important when converting coordinates to array indexes?\n"
            "20. What are the three rough project stages emphasized by the source?\n"
            "21. Why is candidate classification easier than classifying an entire CT volume directly?\n"
            "22. Why is the class/target imbalance in a full CT so extreme?\n"
            "23. What is the difference between segmentation and classification?\n"
            "24. Why can project implementation order differ from final inference order?\n"
            "25. Why are human annotations important in the LUNA project?\n"
            "26. What problems can appear when mixing CT scans from different scanners or processing pipelines?\n"
            "27. Why should disk/storage planning happen before model training begins?\n"
            "28. What can be gained by developing on only a subset of the full dataset when resources are constrained?\n"
            "29. Why is understanding the domain a deep-learning skill rather than an unrelated side task?\n"
            "30. What is the difference between model competence and system competence?\n\n"
            "---\n\n"

            "## Retain this idea\n\n"
            "**Deep-learning competence has two layers. At the model level, you must understand objectives, representations, training, "
            "and inference—for diffusion, that means learning to predict corruption and iteratively reverse it. At the project level, you "
            "must understand the domain, data, resources, decomposition, and interfaces. A sophisticated architecture cannot rescue a poorly "
            "framed project, and a well-framed project still needs technically correct models.**\n"
        ),

        "estimated_minutes": 450,
        "has_code_examples": True,
        "has_manual_image_requests": True,

        "sections": [
            {"id": "generative-goal", "title": "Shared generative objective", "order": 1},
            {"id": "vae-gan-diffusion", "title": "VAEs, GANs, and diffusion", "order": 2},
            {"id": "diffusion-intuition", "title": "Diffusion intuition", "order": 3},
            {"id": "point-dataset", "title": "2D point dataset", "order": 4},
            {"id": "noise-schedule", "title": "Beta noise schedule", "order": 5},
            {"id": "single-forward-step", "title": "One forward diffusion step", "order": 6},
            {"id": "closed-form-forward", "title": "Closed-form forward diffusion", "order": 7},
            {"id": "denoising-objective", "title": "Noise-prediction objective", "order": 8},
            {"id": "timestep-embedding", "title": "Timestep and coordinate embeddings", "order": 9},
            {"id": "denoiser-architecture", "title": "Denoising model architecture", "order": 10},
            {"id": "diffusion-loss", "title": "Diffusion loss", "order": 11},
            {"id": "diffusion-training-loop", "title": "Diffusion training loop", "order": 12},
            {"id": "reverse-diffusion", "title": "Reverse diffusion", "order": 13},
            {"id": "reverse-step", "title": "One reverse sampling step", "order": 14},
            {"id": "full-sampling-loop", "title": "Full sampling loop", "order": 15},
            {"id": "diffusion-takeaway", "title": "Diffusion takeaway", "order": 16},
            {"id": "model-is-not-project", "title": "A model is only part of a project", "order": 17},
            {"id": "domain-understanding", "title": "Understand the domain first", "order": 18},
            {"id": "ct-basics", "title": "CT scans and voxels", "order": 19},
            {"id": "voxel-spacing", "title": "Voxel spacing and coordinates", "order": 20},
            {"id": "project-decomposition", "title": "Project decomposition", "order": 21},
            {"id": "why-not-monolithic", "title": "Why not one monolithic network", "order": 22},
            {"id": "nodule", "title": "Understanding nodules", "order": 23},
            {"id": "segmentation-vs-classification", "title": "Segmentation versus classification", "order": 24},
            {"id": "project-order", "title": "Implementation order versus pipeline order", "order": 25},
            {"id": "data-source", "title": "LUNA data source", "order": 26},
            {"id": "resource-planning", "title": "Compute and storage planning", "order": 27},
            {"id": "data-layout", "title": "Data organization", "order": 28},
            {"id": "real-world-checkpoint", "title": "Real-world project readiness checkpoint", "order": 29},
            {"id": "combined-mental-model", "title": "Model competence and system competence", "order": 30},
        ],
    },

    "exercises": [
        {
            "id": "M10.L01.EX01",
            "title": "Visualize the Forward Diffusion Schedule",
            "lesson_code": "M10.L01",
            "section_id": "closed-form-forward",
            "placement": "after_section",
            "description": "Build intuition for beta, cumulative alpha, retained signal, and noise strength.",
            "instructions": (
                "Create a linear beta schedule with `T=1000`. Compute `alphas`, `alphas_cumprod`, "
                "`sqrt_alphas_cumprod`, and `sqrt_one_minus_alphas_cumprod`. Print values at timesteps "
                "0, 250, 500, 750, and 999. Use a small 2D point tensor and the closed-form equation to "
                "generate noisy versions at those timesteps. Explain how the retained-signal and noise "
                "coefficients change as t increases."
            ),
            "expected_output": (
                "PyTorch code, a table of selected schedule values, several noisy samples or plots, and an explanation."
            ),
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "beta-schedule",
                "alpha-cumprod",
                "forward-diffusion",
                "tensor-broadcasting",
            ],
        },
        {
            "id": "M10.L01.EX02",
            "title": "Implement One Clean Diffusion Training Step",
            "lesson_code": "M10.L01",
            "section_id": "diffusion-training-loop",
            "placement": "after_section",
            "description": "Connect the known corruption process to the model's noise-prediction objective.",
            "instructions": (
                "Using a simple denoising model that returns a tensor with the same shape as the input points:\n"
                "1. move the model and points to one device,\n"
                "2. call `model.train()`,\n"
                "3. sample one timestep per point,\n"
                "4. call the closed-form forward diffusion function,\n"
                "5. predict the noise,\n"
                "6. compute MSE against the real noise,\n"
                "7. clear gradients with `zero_grad(set_to_none=True)`,\n"
                "8. call backward and optimizer step,\n"
                "9. print the scalar loss.\n"
                "Explain why the model needs the timestep as an input."
            ),
            "expected_output": "One complete, best-practice training step plus a short explanation.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "diffusion-loss",
                "noise-prediction",
                "training-loop",
                "device-management",
            ],
        },
        {
            "id": "M10.L01.EX03",
            "title": "Trace Reverse Diffusion Without Hiding the Logic",
            "lesson_code": "M10.L01",
            "section_id": "full-sampling-loop",
            "placement": "after_section",
            "description": "Reason through the iterative nature of diffusion sampling.",
            "instructions": (
                "Write pseudocode for generating 1000 2D points starting from Gaussian noise. Your pseudocode "
                "must include `model.eval()`, `torch.no_grad()`, a reverse loop from `T-1` to `0`, construction "
                "of a timestep tensor, a call to `sample_timestep`, and optional snapshot collection at selected "
                "timesteps. Then explain why the reverse process cannot use the same single closed-form shortcut "
                "that forward training uses in the chapter."
            ),
            "expected_output": "Clear reverse-sampling pseudocode and an explanation of why generation is iterative.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "reverse-diffusion",
                "sampling",
                "eval-mode",
                "no-grad",
            ],
        },
        {
            "id": "M10.L01.EX04",
            "title": "Decompose a Difficult ML Problem",
            "lesson_code": "M10.L01",
            "section_id": "project-decomposition",
            "placement": "after_section",
            "description": "Practice turning one vague end goal into smaller trainable and debuggable tasks.",
            "instructions": (
                ('1. Start with the end goal: `given a chest CT, identify suspicious malignant lung tumors`.\n'
                 '2. Create a table with columns: stage, input, output, model/data operation, possible failure, and metric.\n'
                 '3. Include at least data loading, candidate localization/segmentation, candidate classification, and final result aggregation.\n'
                 '4. Then explain which stage you would prototype first if you wanted the fastest learning/debugging feedback and why.')
            ),
            "expected_output": "A system-decomposition table and a reasoned prototyping-order decision.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "project-decomposition",
                "system-design",
                "segmentation",
                "classification",
                "metrics",
            ],
        },
        {
            "id": "M10.L01.EX05",
            "title": "Real-World Data Readiness Audit",
            "lesson_code": "M10.L01",
            "section_id": "real-world-checkpoint",
            "placement": "after_section",
            "description": "Turn Chapter 11's project-preparation mindset into a reusable engineering checklist.",
            "instructions": (
                "Write a readiness report for the CT project covering:\n"
                "1. physical meaning and shape of one input,\n"
                "2. label sources,\n"
                "3. voxel spacing / coordinate concerns,\n"
                "4. scanner/source variability,\n"
                "5. class imbalance and target size,\n"
                "6. dataset split strategy you would need before training,\n"
                "7. storage and cache needs,\n"
                "8. compute requirements,\n"
                "9. subsystem boundaries,\n"
                "10. what assumptions must be validated before adding a new CT data source.\n"
                "Clearly distinguish facts provided by the chapter from decisions you would still need to make later."
            ),
            "expected_output": "A structured pre-training readiness report with known facts, risks, and unresolved decisions.",
            "difficulty": DifficultyLevel.intermediate,
            "skill_tested": [
                "data-readiness",
                "domain-analysis",
                "resource-planning",
                "risk-analysis",
                "medical-imaging",
            ],
        },
    ],

    "quiz": {
        "id": "M10.L01.QZ01",
        "title": "Diffusion Models & Real-World Project Design — Knowledge Check",
        "lesson_code": "M10.L01",
        "placement": "lesson_end",
        "questions": [
            {
                "id": "M10.L01.Q01",
                "section_id": "vae-gan-diffusion",
                "question": "Which description best matches diffusion-model training in this lesson?",
                "options": [
                    "A discriminator learns to separate real and fake samples.",
                    "Data is deliberately corrupted with noise and a model learns information needed to reverse that corruption.",
                    "An encoder maps every sample to one discrete class.",
                    "A model memorizes every possible image in a lookup table.",
                ],
                "correct": 1,
                "explanation": "Diffusion training is built around a known forward noising process and learned denoising.",
            },
            {
                "id": "M10.L01.Q02",
                "section_id": "noise-schedule",
                "question": "What is the role of beta in the forward diffusion process?",
                "options": [
                    "It controls the amount of corruption/noise introduced at a timestep.",
                    "It stores the final class label.",
                    "It sets the number of model layers.",
                    "It converts CT coordinates to voxel indexes.",
                ],
                "correct": 0,
                "explanation": "The beta schedule determines how strongly signal and fresh noise are mixed over time.",
            },
            {
                "id": "M10.L01.Q03",
                "section_id": "closed-form-forward",
                "question": "Why is the closed-form forward diffusion equation useful during training?",
                "options": [
                    "It eliminates the need for random noise.",
                    "It replaces the neural network with a lookup table.",
                    "It lets us generate x_t directly from x_0 for a chosen timestep without simulating every earlier step.",
                    "It makes reverse diffusion a one-step process.",
                ],
                "correct": 2,
                "explanation": "Training can jump directly to random timesteps efficiently.",
            },
            {
                "id": "M10.L01.Q04",
                "section_id": "diffusion-loss",
                "question": "What target does the denoising model learn to predict in the chapter's implementation?",
                "options": [
                    "The final class probability.",
                    "The next text token.",
                    "The clean sample in a single step.",
                    "The random noise used to corrupt the sample.",
                ],
                "correct": 3,
                "explanation": "The MSE compares predicted noise with the exact noise sampled during forward diffusion.",
            },
            {
                "id": "M10.L01.Q05",
                "section_id": "timestep-embedding",
                "question": "Why must the denoising model receive timestep information?",
                "options": [
                    "The amount and character of corruption depend on where the sample is in the diffusion process.",
                    "The timestep is the class label.",
                    "The timestep replaces the input data.",
                    "It is required only for plotting.",
                ],
                "correct": 0,
                "explanation": "Different noise levels require different denoising behavior.",
            },
            {
                "id": "M10.L01.Q06",
                "section_id": "reverse-diffusion",
                "question": "Why is diffusion sampling iterative in this lesson?",
                "options": [
                    "Because the model can only run on one coordinate at a time.",
                    "Because the reverse process repeatedly estimates a previous, slightly less noisy state across timesteps.",
                    "Because softmax must be applied 1000 times to class labels.",
                    "Because training data must be downloaded again at each timestep.",
                ],
                "correct": 1,
                "explanation": "Generation moves step by step from noise toward structure.",
            },
            {
                "id": "M10.L01.Q07",
                "section_id": "reverse-step",
                "question": "Which combination is appropriate for ordinary diffusion sampling/inference?",
                "options": [
                    "`model.train()` plus `loss.backward()`",
                    "`optimizer.step()` plus dropout augmentation",
                    "`model.eval()` plus no gradient tracking",
                    "`requires_grad=True` on every generated sample",
                ],
                "correct": 2,
                "explanation": "Sampling does not optimize the model and should not build gradient graphs.",
            },
            {
                "id": "M10.L01.Q08",
                "section_id": "ct-basics",
                "question": "What is a voxel?",
                "options": [
                    "A text token from a CT report.",
                    "A learned convolution filter.",
                    "A 2D grayscale pixel only.",
                    "A volumetric cell in a 3D data grid.",
                ],
                "correct": 3,
                "explanation": "A voxel is the 3D analogue of a pixel.",
            },
            {
                "id": "M10.L01.Q09",
                "section_id": "voxel-spacing",
                "question": "Why can CT array-index distance differ from physical distance across axes?",
                "options": [
                    "Voxel spacing can differ between axes, so voxels are not necessarily cubic.",
                    "Every CT is stored as RGB.",
                    "Segmentation removes physical units.",
                    "Class labels redefine the scan geometry.",
                ],
                "correct": 0,
                "explanation": "Scanner acquisition geometry can produce non-isotropic voxel spacing.",
            },
            {
                "id": "M10.L01.Q10",
                "section_id": "project-decomposition",
                "question": "What is a major benefit of breaking the cancer-detection project into smaller stages?",
                "options": [
                    "It guarantees the global optimum.",
                    "Each subproblem becomes easier to understand, train, debug, and improve independently.",
                    "It removes the need for labeled data.",
                    "It makes CT volumes two-dimensional.",
                ],
                "correct": 1,
                "explanation": "Modularity reduces the number of moving parts considered at once.",
            },
            {
                "id": "M10.L01.Q11",
                "section_id": "why-not-monolithic",
                "question": "Why is directly classifying an entire CT scan difficult in this project?",
                "options": [
                    "CT scans contain no numeric data.",
                    "The model cannot use convolution on medical data.",
                    "The relevant target occupies an extremely small portion of a very large volume and data/resources are limited.",
                    "Every voxel is equally likely to contain cancer.",
                ],
                "correct": 2,
                "explanation": "The tiny target, massive background, limited data, and compute cost make a naive monolithic approach difficult.",
            },
            {
                "id": "M10.L01.Q12",
                "section_id": "segmentation-vs-classification",
                "question": "What question does segmentation primarily answer in this project?",
                "options": [
                    "Which optimizer should be used?",
                    "How much disk space is available?",
                    "Which patient owns the scan?",
                    "Where are suspicious voxels or structures located?",
                ],
                "correct": 3,
                "explanation": "Segmentation provides spatial localization rather than only a global class.",
            },
            {
                "id": "M10.L01.Q13",
                "section_id": "project-order",
                "question": "Why can implementation order differ from the final inference-pipeline order?",
                "options": [
                    "Modular components can be developed in the order that provides better learning and debugging leverage.",
                    "The final system has no dependencies between stages.",
                    "Classification must always be implemented before loading data.",
                    "PyTorch executes project stages alphabetically.",
                ],
                "correct": 0,
                "explanation": "Clear subsystem boundaries allow teams to prototype pieces in a useful order.",
            },
            {
                "id": "M10.L01.Q14",
                "section_id": "data-source",
                "question": "Why are curated challenge annotations valuable?",
                "options": [
                    "They eliminate all scanner variation forever.",
                    "They provide high-quality reference information needed to train and evaluate the intended tasks.",
                    "They convert CT data into natural-language tokens.",
                    "They remove the need to understand the domain.",
                ],
                "correct": 1,
                "explanation": "Reliable annotations are central to supervised task development and evaluation.",
            },
            {
                "id": "M10.L01.Q15",
                "section_id": "resource-planning",
                "question": "What engineering lesson does the chapter's large storage/GPU requirement illustrate?",
                "options": [
                    "Resource constraints should be ignored until after model design.",
                    "Only cloud systems can use PyTorch.",
                    "Compute, storage, and iteration cost should be considered as part of project design.",
                    "A larger dataset always removes the need for caching.",
                ],
                "correct": 2,
                "explanation": "Practical constraints shape what can be trained and iterated on.",
            },
            {
                "id": "M10.L01.Q16",
                "section_id": "combined-mental-model",
                "type": "open",
                "question": (
                    "Explain the difference between model competence and system competence using both halves of this lesson. "
                    "Use diffusion training as an example of model competence and the CT/LUNA project as an example of system competence."
                ),
            },
        ],
        "passing_score": 70,
    },
}
