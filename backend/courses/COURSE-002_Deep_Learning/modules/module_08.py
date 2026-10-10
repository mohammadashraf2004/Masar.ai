"""M10.L01 — Interpreting What ConvNets Learn.

One Topic -> one complete learner-facing Lesson + inline Exercises + lesson Quiz.
BOOK-002, Chapter 10, pages not provided in the supplied extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M10.L01"

MODULE_ORDER = 10

MODULE_TITLE = "Interpreting Convolutional Neural Networks"

MODULE_DESCRIPTION = (
    "Learn practical methods for interpreting convolutional neural networks using "
    "intermediate activations, learned filter visualizations, Grad-CAM heatmaps, "
    "and latent-space inspection."
)

SOURCE_CHAPTER = 10

SOURCE_PAGES = "Not provided in supplied chapter extract"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Interpreting What ConvNets Learn",

    "slug": "deep-learning-foundations-m10-l01",

    "description": (
        "Understand how ConvNets transform images, what individual filters detect, "
        "which image regions drive a prediction, and how learned latent spaces "
        "organize visual examples."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 2.25,

    "skill_tags": [
        "deep-learning",
        "computer-vision",
        "convnets",
        "interpretability",
        "grad-cam",
        "feature-visualization",
        "latent-space",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Interpreting What ConvNets Learn",

        "content": (
            '# Interpreting What ConvNets Learn\n'
            '\n'
            '> **Course:** Deep Learning Foundations  \n'
            '> **Lesson:** M10.L01  \n'
            '> **Module:** Interpreting Convolutional Neural Networks  \n'
            '> **Source alignment:** BOOK-002, Chapter 10. The supplied chapter extract does not include page numbers. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.\n'
            '\n'
            '---\n'
            '\n'
            '## Learning outcomes\n'
            '\n'
            'By the end of this lesson, you should be able to:\n'
            '\n'
            '- Explain why interpretability matters in computer vision.\n'
            '- Visualize intermediate ConvNet activations and interpret how representations change with depth.\n'
            '- Explain how individual convolutional filters can be visualized using gradient ascent in input space.\n'
            '- Distinguish when to use `model(x)` versus `model.predict(x)`.\n'
            '- Explain how Grad-CAM highlights image regions that influence a class prediction.\n'
            '- Describe how latent-space visualization reveals the semantic organization learned by a ConvNet.\n'
            '- Recognize the limitations of projecting high-dimensional learned representations into two dimensions.\n'
            '\n'
            '---\n'
            '\n'
            '## 1. Why ConvNet interpretability matters\n'
            '\n'
            'A classifier can make a prediction without explaining why it made that prediction.\n'
            '\n'
            'For example, suppose a model predicts:\n'
            '\n'
            '```text\n'
            '"fridge"\n'
            '```\n'
            '\n'
            'for an image that appears to contain a truck.\n'
            '\n'
            'The important engineering question is:\n'
            '\n'
            '> What visual evidence caused the network to make that decision?\n'
            '\n'
            'This question becomes especially important when deep learning supports human expertise, such as in medical imaging.\n'
            '\n'
            'Although deep-learning models are often described as "black boxes," convolutional neural networks are unusually suitable for visual inspection because their internal representations are themselves spatial and visual.\n'
            '\n'
            'The chapter focuses on four ways to inspect what a ConvNet has learned:\n'
            '\n'
            '```text\n'
            '1. Intermediate activations\n'
            '2. Learned filter patterns\n'
            '3. Class-activation heatmaps such as Grad-CAM\n'
            '4. Latent-space visualization\n'
            '```\n'
            '\n'
            'Each method answers a different question.\n'
            '\n'
            '| Technique | Main question |\n'
            '|---|---|\n'
            '| Intermediate activations | How does each layer transform this image? |\n'
            '| Filter visualization | What pattern makes this filter respond strongly? |\n'
            '| Grad-CAM | Which image regions influenced this class prediction? |\n'
            '| Latent-space visualization | Which images does the model consider semantically similar? |\n'
            '\n'
            'Together, these methods make ConvNet behavior more inspectable.\n'
            '\n'
            '---\n'
            '\n'
            '## 2. Visualizing intermediate activations\n'
            '\n'
            'The output of a layer is often called its **activation**.\n'
            '\n'
            'For a ConvNet, a convolutional activation usually has three spatial dimensions per sample:\n'
            '\n'
            '```text\n'
            'height × width × channels\n'
            '```\n'
            '\n'
            'For example:\n'
            '\n'
            '```text\n'
            '178 × 178 × 32\n'
            '```\n'
            '\n'
            'means:\n'
            '\n'
            '- height = 178,\n'
            '- width = 178,\n'
            '- channels = 32.\n'
            '\n'
            'Each channel acts like a feature map responding to a particular learned pattern.\n'
            '\n'
            '### Preparing a single image\n'
            '\n'
            'A model expects batches, even if you want to inspect only one image.\n'
            '\n'
            'A typical preprocessing flow is:\n'
            '\n'
            '```python\n'
            'import keras\n'
            'import numpy as np\n'
            '\n'
            'def get_img_array(img_path, target_size):\n'
            '    img = keras.utils.load_img(img_path, target_size=target_size)\n'
            '    array = keras.utils.img_to_array(img)\n'
            '    array = np.expand_dims(array, axis=0)\n'
            '    return array\n'
            '```\n'
            '\n'
            'If the resized image has shape:\n'
            '\n'
            '```text\n'
            '(180, 180, 3)\n'
            '```\n'
            '\n'
            'adding the batch dimension makes it:\n'
            '\n'
            '```text\n'
            '(1, 180, 180, 3)\n'
            '```\n'
            '\n'
            'The leading `1` means:\n'
            '\n'
            '```text\n'
            'one image in the batch\n'
            '```\n'
            '\n'
            '### Building an activation model\n'
            '\n'
            'A Keras Functional model can expose the outputs of internal layers.\n'
            '\n'
            'Suppose the original ConvNet contains convolution and pooling layers.\n'
            '\n'
            'You can collect their outputs:\n'
            '\n'
            '```python\n'
            'from keras import layers\n'
            '\n'
            'layer_outputs = []\n'
            'layer_names = []\n'
            '\n'
            'for layer in model.layers:\n'
            '    if isinstance(layer, (layers.Conv2D, layers.MaxPooling2D)):\n'
            '        layer_outputs.append(layer.output)\n'
            '        layer_names.append(layer.name)\n'
            '\n'
            'activation_model = keras.Model(\n'
            '    inputs=model.input,\n'
            '    outputs=layer_outputs,\n'
            ')\n'
            '```\n'
            '\n'
            'This creates a new model:\n'
            '\n'
            '```text\n'
            'input image\n'
            '   ↓\n'
            'same original ConvNet computation\n'
            '   ↓\n'
            'multiple intermediate layer outputs\n'
            '```\n'
            '\n'
            'Now:\n'
            '\n'
            '```python\n'
            'activations = activation_model.predict(img_tensor)\n'
            '```\n'
            '\n'
            'returns one activation tensor per selected layer.\n'
            '\n'
            '### Visualizing one channel\n'
            '\n'
            'Suppose the first convolutional layer produces:\n'
            '\n'
            '```text\n'
            '(1, 178, 178, 32)\n'
            '```\n'
            '\n'
            'Then one channel can be visualized as:\n'
            '\n'
            '```python\n'
            'first_layer_activation = activations[0]\n'
            '\n'
            'plt.matshow(\n'
            '    first_layer_activation[0, :, :, 5],\n'
            '    cmap="viridis",\n'
            ')\n'
            '```\n'
            '\n'
            'That 2D image shows where one learned filter responds strongly in the input.\n'
            '\n'
            '### What changes as we move deeper?\n'
            '\n'
            'One of the most important observations in the chapter is that representations become more abstract as depth increases.\n'
            '\n'
            'Early layers often respond to:\n'
            '\n'
            '```text\n'
            'edges\n'
            'directions\n'
            'simple colors\n'
            'basic textures\n'
            '```\n'
            '\n'
            'Later layers respond to combinations of these features.\n'
            '\n'
            'A useful progression is:\n'
            '\n'
            '```text\n'
            'raw pixels\n'
            '   ↓\n'
            'edges\n'
            '   ↓\n'
            'textures\n'
            '   ↓\n'
            'parts\n'
            '   ↓\n'
            'high-level class-related concepts\n'
            '```\n'
            '\n'
            'The exact features depend on the model and training process, but the overall pattern is consistent.\n'
            '\n'
            '### Information distillation\n'
            '\n'
            'As the representation moves deeper into the network:\n'
            '\n'
            '```text\n'
            'less information about exact appearance\n'
            'more information relevant to the task\n'
            '```\n'
            '\n'
            'This is an example of **information distillation**.\n'
            '\n'
            'The network gradually removes details that are not useful for the final classification and strengthens features that are useful.\n'
            '\n'
            '### Activation sparsity\n'
            '\n'
            'Deeper layers often contain more blank or inactive channels for a specific image.\n'
            '\n'
            'That means:\n'
            '\n'
            '> The visual concept represented by that filter was not strongly present in this input.\n'
            '\n'
            'So a deep ConvNet is not simply preserving the image.\n'
            '\n'
            'It is selectively transforming and filtering information.\n'
            '\n'
            '{{exercise:M10.L01.EX01}}\n'
            '\n'
            '---\n'
            '\n'
            '## 3. Visualizing what individual filters detect\n'
            '\n'
            'Intermediate activations answer:\n'
            '\n'
            '> Where did this filter respond in this specific image?\n'
            '\n'
            'Filter visualization asks a different question:\n'
            '\n'
            '> What input pattern would make this filter respond as strongly as possible?\n'
            '\n'
            'The chapter solves this using **gradient ascent in input space**.\n'
            '\n'
            '### The core idea\n'
            '\n'
            'Normally, gradient descent changes model parameters to reduce a loss.\n'
            '\n'
            'For filter visualization:\n'
            '\n'
            '- model weights stay fixed,\n'
            '- the input image is changed,\n'
            "- the objective is to increase one filter's activation.\n"
            '\n'
            'Conceptually:\n'
            '\n'
            '```text\n'
            'random image\n'
            '    ↓\n'
            'ConvNet filter activation\n'
            '    ↓\n'
            'compute gradient with respect to image pixels\n'
            '    ↓\n'
            'change image to increase activation\n'
            '    ↓\n'
            'repeat\n'
            '```\n'
            '\n'
            'The result becomes a synthetic image containing the visual pattern the filter prefers.\n'
            '\n'
            '### Building a feature extractor\n'
            '\n'
            'First choose a convolutional layer:\n'
            '\n'
            '```python\n'
            'layer_name = "block3_sepconv1"\n'
            'layer = model.get_layer(name=layer_name)\n'
            '\n'
            'feature_extractor = keras.Model(\n'
            '    inputs=model.input,\n'
            '    outputs=layer.output,\n'
            ')\n'
            '```\n'
            '\n'
            'This model returns the feature maps of one target layer.\n'
            '\n'
            '### Define the objective\n'
            '\n'
            "To visualize a particular filter, define a scalar score based on that filter's activation.\n"
            '\n'
            '```python\n'
            'from keras import ops\n'
            '\n'
            'def compute_loss(image, filter_index):\n'
            '    activation = feature_extractor(image)\n'
            '    filter_activation = activation[:, 2:-2, 2:-2, filter_index]\n'
            '    return ops.mean(filter_activation)\n'
            '```\n'
            '\n'
            'The score answers:\n'
            '\n'
            '```text\n'
            'How strongly does this image activate filter N?\n'
            '```\n'
            '\n'
            'The borders are ignored to reduce border artifacts.\n'
            '\n'
            '### Why `model(x)` instead of `model.predict(x)`?\n'
            '\n'
            'This distinction is important.\n'
            '\n'
            'Both approaches produce model outputs:\n'
            '\n'
            '```python\n'
            'model.predict(x)\n'
            'model(x)\n'
            '```\n'
            '\n'
            'but they are used differently.\n'
            '\n'
            '`predict()`:\n'
            '\n'
            '- processes inputs in batches,\n'
            '- is convenient for large datasets,\n'
            '- returns ordinary output values,\n'
            '- is not intended for differentiating through the model call.\n'
            '\n'
            '`model(x)`:\n'
            '\n'
            '- directly executes the differentiable model computation,\n'
            "- keeps the operation inside the backend's gradient system,\n"
            '- should be used when gradients are required.\n'
            '\n'
            'A useful rule is:\n'
            '\n'
            '> Use `predict()` when you only need predictions. Use `model(x)` inside low-level gradient-based code.\n'
            '\n'
            '### Gradient ascent\n'
            '\n'
            'Gradient ascent moves the input image in the direction that **increases** the filter activation.\n'
            '\n'
            'The only difference from gradient descent is the direction.\n'
            '\n'
            'Gradient descent:\n'
            '\n'
            '```text\n'
            'parameter = parameter - learning_rate × gradient\n'
            '```\n'
            '\n'
            'Gradient ascent:\n'
            '\n'
            '```text\n'
            'input = input + learning_rate × gradient\n'
            '```\n'
            '\n'
            '### TensorFlow version\n'
            '\n'
            '```python\n'
            'import tensorflow as tf\n'
            '\n'
            '@tf.function\n'
            'def gradient_ascent_step(image, filter_index, learning_rate):\n'
            '    with tf.GradientTape() as tape:\n'
            '        tape.watch(image)\n'
            '        loss = compute_loss(image, filter_index)\n'
            '\n'
            '    grads = tape.gradient(loss, image)\n'
            '    grads = ops.normalize(grads)\n'
            '\n'
            '    image += learning_rate * grads\n'
            '    return image\n'
            '```\n'
            '\n'
            '### PyTorch version\n'
            '\n'
            '```python\n'
            'def gradient_ascent_step(image, filter_index, learning_rate):\n'
            '    image = image.clone().detach().requires_grad_(True)\n'
            '\n'
            '    loss = compute_loss(image, filter_index)\n'
            '    loss.backward()\n'
            '\n'
            '    grads = ops.normalize(image.grad)\n'
            '\n'
            '    image = image + learning_rate * grads\n'
            '    return image\n'
            '```\n'
            '\n'
            '### JAX version\n'
            '\n'
            '```python\n'
            'import jax\n'
            '\n'
            'grad_fn = jax.grad(compute_loss)\n'
            '\n'
            '@jax.jit\n'
            'def gradient_ascent_step(image, filter_index, learning_rate):\n'
            '    grads = grad_fn(image, filter_index)\n'
            '    grads = ops.normalize(grads)\n'
            '\n'
            '    image += learning_rate * grads\n'
            '    return image\n'
            '```\n'
            '\n'
            'All three perform the same mathematics.\n'
            '\n'
            'The API changes, but the idea does not.\n'
            '\n'
            '### Why normalize gradients?\n'
            '\n'
            'Raw gradients can vary greatly in magnitude.\n'
            '\n'
            'Normalizing them makes the update size more stable:\n'
            '\n'
            '```text\n'
            'large gradient  ┐\n'
            'small gradient  ├─> similar update scale\n'
            'medium gradient ┘\n'
            '```\n'
            '\n'
            'This prevents one step from changing the image too aggressively simply because the gradient happens to have a large magnitude.\n'
            '\n'
            '### Generate the pattern\n'
            '\n'
            'Start with a mostly neutral random image:\n'
            '\n'
            '```python\n'
            'image = keras.random.uniform(\n'
            '    minval=0.4,\n'
            '    maxval=0.6,\n'
            '    shape=(1, 200, 200, 3),\n'
            ')\n'
            '```\n'
            '\n'
            'Then repeatedly apply gradient ascent:\n'
            '\n'
            '```python\n'
            'for _ in range(30):\n'
            '    image = gradient_ascent_step(\n'
            '        image,\n'
            '        filter_index,\n'
            '        learning_rate=10.0,\n'
            '    )\n'
            '```\n'
            '\n'
            'Finally, convert the optimized tensor into a displayable image.\n'
            '\n'
            '### What do filters learn?\n'
            '\n'
            'The chapter observes a hierarchy.\n'
            '\n'
            'Early layers learn patterns such as:\n'
            '\n'
            '```text\n'
            'directional edges\n'
            'color transitions\n'
            'simple color-edge combinations\n'
            '```\n'
            '\n'
            'Middle layers learn:\n'
            '\n'
            '```text\n'
            'textures\n'
            'repeated visual motifs\n'
            'combinations of edges\n'
            '```\n'
            '\n'
            'Higher layers may respond to structures resembling:\n'
            '\n'
            '```text\n'
            'feathers\n'
            'eyes\n'
            'leaves\n'
            'fur-like textures\n'
            'object parts\n'
            '```\n'
            '\n'
            'This reinforces the earlier idea that deeper layers represent increasingly complex visual concepts.\n'
            '\n'
            '---\n'
            '\n'
            '## 4. Grad-CAM: understanding a classification decision\n'
            '\n'
            'Filter visualization tells us what a filter prefers in general.\n'
            '\n'
            'Grad-CAM answers a more practical question:\n'
            '\n'
            '> Which parts of this particular image contributed to this particular prediction?\n'
            '\n'
            'This is a form of **class activation map** visualization.\n'
            '\n'
            'The result is a heatmap placed over the input image.\n'
            '\n'
            'Hot regions indicate places that were important for the selected class.\n'
            '\n'
            '### Example question\n'
            '\n'
            'Suppose a pretrained classifier predicts:\n'
            '\n'
            '```text\n'
            'African elephant\n'
            '```\n'
            '\n'
            'for an image containing elephants.\n'
            '\n'
            'Grad-CAM can help answer:\n'
            '\n'
            '```text\n'
            'Where in the image did the model find evidence for\n'
            '"African elephant"?\n'
            '```\n'
            '\n'
            '### Core intuition\n'
            '\n'
            'Take the feature maps from a late convolutional layer.\n'
            '\n'
            'Each channel represents some high-level visual feature.\n'
            '\n'
            'Then ask:\n'
            '\n'
            '> How important was each channel for the predicted class?\n'
            '\n'
            'Gradients provide this importance information.\n'
            '\n'
            'Conceptually:\n'
            '\n'
            '```text\n'
            'last convolutional feature maps\n'
            '           +\n'
            'gradient of class score\n'
            'with respect to those maps\n'
            '           ↓\n'
            'channel importance\n'
            '           ↓\n'
            'weighted spatial maps\n'
            '           ↓\n'
            'class activation heatmap\n'
            '```\n'
            '\n'
            '### Why use the last convolutional layer?\n'
            '\n'
            'Earlier layers retain fine visual detail but are less class-specific.\n'
            '\n'
            'Very late dense outputs are class-specific but have usually lost spatial structure.\n'
            '\n'
            'The last convolutional layer offers a useful balance:\n'
            '\n'
            '```text\n'
            'high-level semantic information\n'
            '+\n'
            'spatial layout\n'
            '```\n'
            '\n'
            '### Step 1 — Compute last convolutional activations\n'
            '\n'
            'Create a model:\n'
            '\n'
            '```text\n'
            'input image\n'
            '    ↓\n'
            'last convolutional output\n'
            '```\n'
            '\n'
            '### Step 2 — Map convolutional output to class scores\n'
            '\n'
            'Create another model:\n'
            '\n'
            '```text\n'
            'last convolutional output\n'
            '    ↓\n'
            'pooling / classifier head\n'
            '    ↓\n'
            'class predictions\n'
            '```\n'
            '\n'
            '### Step 3 — Compute class gradients\n'
            '\n'
            'For the top predicted class, compute:\n'
            '\n'
            '```text\n'
            '∂ class_score\n'
            '──────────────\n'
            '∂ feature_map\n'
            '```\n'
            '\n'
            'The chapter shows this with:\n'
            '\n'
            '```text\n'
            'TensorFlow -> GradientTape\n'
            'PyTorch    -> backward() and .grad\n'
            'JAX        -> jax.grad()\n'
            '```\n'
            '\n'
            'Again, the backend APIs differ while the mathematical objective stays the same.\n'
            '\n'
            '### Step 4 — Pool the gradients\n'
            '\n'
            'Average the gradient across spatial locations:\n'
            '\n'
            '```python\n'
            'pooled_grads = np.mean(grads, axis=(0, 1, 2))\n'
            '```\n'
            '\n'
            'Now each channel gets one importance score.\n'
            '\n'
            'Conceptually:\n'
            '\n'
            '```text\n'
            'channel 0 -> importance 0.05\n'
            'channel 1 -> importance 0.91\n'
            'channel 2 -> importance 0.12\n'
            '...\n'
            '```\n'
            '\n'
            '### Step 5 — Weight the channels\n'
            '\n'
            'Multiply each feature-map channel by its importance.\n'
            '\n'
            '```text\n'
            'important channel -> contributes strongly\n'
            'unimportant channel -> contributes weakly\n'
            '```\n'
            '\n'
            'Then average across channels to obtain a 2D heatmap.\n'
            '\n'
            '### Step 6 — Normalize and overlay\n'
            '\n'
            'The heatmap is normalized into a visible range and placed over the original image.\n'
            '\n'
            'The resulting visualization answers:\n'
            '\n'
            '```text\n'
            '"What image regions supported this class prediction?"\n'
            '```\n'
            '\n'
            'It can also provide approximate object localization, even though the model was trained only for image classification.\n'
            '\n'
            '### What Grad-CAM can and cannot tell you\n'
            '\n'
            'Grad-CAM is useful for:\n'
            '\n'
            '- debugging surprising predictions,\n'
            '- checking whether the model looks at the expected object,\n'
            '- identifying suspicious reliance on background regions,\n'
            '- explaining a prediction to a human reviewer,\n'
            '- approximate localization.\n'
            '\n'
            'But a heatmap should not automatically be treated as a perfect causal explanation.\n'
            '\n'
            "It shows regions associated with the class score under the method's gradient-based approximation.\n"
            '\n'
            'Interpretability tools should support investigation, not replace careful validation.\n'
            '\n'
            '{{exercise:M10.L01.EX02}}\n'
            '\n'
            '---\n'
            '\n'
            '## 5. Visualizing the ConvNet latent space\n'
            '\n'
            'Deep-learning models transform inputs into **latent representations**.\n'
            '\n'
            'A latent representation is an internal coordinate system learned by the network.\n'
            '\n'
            'Images that the model considers semantically similar tend to lie near each other in this learned space.\n'
            '\n'
            'Conceptually:\n'
            '\n'
            '```text\n'
            'input image\n'
            '    ↓\n'
            'ConvNet\n'
            '    ↓\n'
            'latent vector\n'
            '```\n'
            '\n'
            'For example:\n'
            '\n'
            '```text\n'
            'cat A -> [ ... hundreds of values ... ]\n'
            'cat B -> [ ... hundreds of values ... ]\n'
            'dog A -> [ ... hundreds of values ... ]\n'
            '```\n'
            '\n'
            'If the learned representation is useful:\n'
            '\n'
            '```text\n'
            'distance(cat A, cat B)\n'
            '<\n'
            'distance(cat A, unrelated object)\n'
            '```\n'
            '\n'
            '### Which layer should we inspect?\n'
            '\n'
            'You can inspect the representation of any layer.\n'
            '\n'
            'But late layers are often especially useful because they are more semantically organized.\n'
            '\n'
            'A layer near the classifier has already removed much of the low-level visual detail and retained information important to recognition.\n'
            '\n'
            '### Why dimensionality reduction is needed\n'
            '\n'
            'A latent vector may have:\n'
            '\n'
            '```text\n'
            '512 dimensions\n'
            '1024 dimensions\n'
            '2048 dimensions\n'
            '```\n'
            '\n'
            'Humans cannot directly visualize these spaces.\n'
            '\n'
            'So we project the high-dimensional representation into:\n'
            '\n'
            '```text\n'
            '2 dimensions\n'
            '```\n'
            '\n'
            'and plot the resulting points.\n'
            '\n'
            '### A map analogy\n'
            '\n'
            'The chapter compares this problem to drawing a world map.\n'
            '\n'
            'Earth exists in 3D.\n'
            '\n'
            'Its surface is a 2D manifold.\n'
            '\n'
            'We can project that surface onto a flat map.\n'
            '\n'
            'But every projection introduces distortion.\n'
            '\n'
            'The same principle applies to latent-space visualization.\n'
            '\n'
            'A 2D visualization may reveal:\n'
            '\n'
            '- clusters,\n'
            '- class separation,\n'
            '- outliers,\n'
            '- ambiguous samples,\n'
            '- suspicious labels.\n'
            '\n'
            'But it cannot preserve all information from the original high-dimensional space.\n'
            '\n'
            '### Why this is useful\n'
            '\n'
            'Latent-space inspection can help you find:\n'
            '\n'
            '```text\n'
            'mislabeled samples\n'
            'outliers\n'
            'ambiguous samples\n'
            'unexpected class overlap\n'
            'dataset problems\n'
            '```\n'
            '\n'
            'Suppose most dog images form one cluster, but one image labeled "dog" appears deep inside the cat cluster.\n'
            '\n'
            'That sample deserves inspection.\n'
            '\n'
            'Maybe:\n'
            '\n'
            '- the label is wrong,\n'
            '- the image is ambiguous,\n'
            '- the model has learned an unexpected feature,\n'
            '- the dataset contains a systematic issue.\n'
            '\n'
            'This makes latent-space visualization useful not only for explaining the model, but also for improving the dataset.\n'
            '\n'
            '---\n'
            '\n'
            '## 6. A practical ConvNet interpretation workflow\n'
            '\n'
            'When a ConvNet makes a surprising prediction, use the techniques in a sequence.\n'
            '\n'
            '### Step 1 — Confirm the prediction\n'
            '\n'
            'Record:\n'
            '\n'
            '```text\n'
            'predicted class\n'
            'prediction score\n'
            'expected class\n'
            '```\n'
            '\n'
            'Do not begin interpretation before confirming exactly what the model produced.\n'
            '\n'
            '### Step 2 — Inspect intermediate activations\n'
            '\n'
            'Ask:\n'
            '\n'
            '```text\n'
            'What information survives each layer?\n'
            'Which channels activate?\n'
            'At what depth does the representation become class-specific?\n'
            '```\n'
            '\n'
            'This gives a layer-by-layer view of information transformation.\n'
            '\n'
            '### Step 3 — Inspect representative filters\n'
            '\n'
            'Use filter visualization to ask:\n'
            '\n'
            '```text\n'
            'What kinds of visual patterns has this layer learned?\n'
            '```\n'
            '\n'
            'Compare early, middle, and deep layers.\n'
            '\n'
            'You should expect increasing abstraction.\n'
            '\n'
            '### Step 4 — Generate a class heatmap\n'
            '\n'
            'Use Grad-CAM to ask:\n'
            '\n'
            '```text\n'
            'Where did the model find evidence for this class?\n'
            '```\n'
            '\n'
            'Compare the heatmap with the actual object.\n'
            '\n'
            '### Step 5 — Inspect the latent neighborhood\n'
            '\n'
            'Ask:\n'
            '\n'
            '```text\n'
            'Which examples are close to this image in representation space?\n'
            '```\n'
            '\n'
            'This may reveal:\n'
            '\n'
            '- ambiguous samples,\n'
            '- mislabeled examples,\n'
            '- unusual clusters.\n'
            '\n'
            '### Step 6 — Turn interpretation into action\n'
            '\n'
            'Interpretability is most useful when it leads to engineering decisions.\n'
            '\n'
            'Possible actions include:\n'
            '\n'
            '```text\n'
            'clean incorrect labels\n'
            'collect missing examples\n'
            'reduce background bias\n'
            'change augmentation\n'
            'improve evaluation data\n'
            'investigate spurious correlations\n'
            'retrain the model\n'
            '```\n'
            '\n'
            'A useful interpretation tool should help you improve either:\n'
            '\n'
            '```text\n'
            'the model\n'
            'the data\n'
            'the evaluation process\n'
            '```\n'
            '\n'
            'not merely create attractive visualizations.\n'
            '\n'
            '---\n'
            '\n'
            '## Important misconception\n'
            '\n'
            '### Misconception\n'
            '\n'
            '> "A deep ConvNet is completely impossible to inspect because neural networks are black boxes."\n'
            '\n'
            '### Why this is wrong\n'
            '\n'
            'ConvNets learn spatial feature maps that can be visualized directly. Intermediate activations, filter-maximization patterns, Grad-CAM heatmaps, and latent-space projections provide several complementary views into what the network has learned.\n'
            '\n'
            'These methods do not make every internal decision perfectly transparent, but they make ConvNets far more inspectable than the phrase "black box" suggests.\n'
            '\n'
            '---\n'
            '\n'
            '## Key terminology\n'
            '\n'
            '| Term | Meaning |\n'
            '|---|---|\n'
            '| Interpretability | Techniques for understanding how a model represents inputs and produces decisions |\n'
            '| Activation | The output produced by a neural-network layer |\n'
            '| Feature map | A spatial activation channel produced by a convolutional layer |\n'
            '| Intermediate activation | The output of an internal network layer for a specific input |\n'
            '| Filter | A learned convolutional pattern detector |\n'
            '| Information distillation | Progressive transformation from raw input details toward task-relevant representations |\n'
            '| Gradient ascent | Updating a variable in the direction that increases an objective |\n'
            '| Feature extractor | A model that returns an intermediate representation rather than only the final prediction |\n'
            '| Class activation map | A spatial map showing which image locations support a class prediction |\n'
            '| Grad-CAM | A gradient-based method for producing class activation heatmaps |\n'
            '| Pooled gradient | A summarized gradient value used to estimate the importance of a feature-map channel |\n'
            '| Latent space | A learned internal representation space in which inputs are encoded |\n'
            '| Manifold | A structured lower-dimensional space embedded in a higher-dimensional representation |\n'
            '| Dimensionality reduction | Projecting high-dimensional data into fewer dimensions for visualization or analysis |\n'
            '\n'
            '---\n'
            '\n'
            '## Self-check\n'
            '\n'
            'Before continuing, make sure you can answer:\n'
            '\n'
            '1. Why are ConvNets particularly suitable for visual interpretation?\n'
            '2. What does one channel in a convolutional activation represent?\n'
            '3. How do early-layer and late-layer activations usually differ?\n'
            '4. What is being optimized during filter visualization?\n'
            '5. Why do we use `model(x)` instead of `predict(x)` inside a gradient-based visualization loop?\n'
            '6. What is the difference between gradient descent and gradient ascent?\n'
            '7. What question does Grad-CAM answer?\n'
            '8. Why is a late convolutional layer useful for class activation mapping?\n'
            '9. What do pooled gradients represent in Grad-CAM?\n'
            '10. What does distance in a learned latent space roughly represent?\n'
            '11. Why must a 2D latent-space projection lose some information?\n'
            '12. How can interpretability help improve the training dataset?\n'
            '\n'
            '---\n'
            '\n'
            '## Retain this idea\n'
            '\n'
            '**ConvNet interpretability is about connecting internal representations to human-understandable evidence: activations show how an image is transformed, filter visualization shows what patterns neurons prefer, Grad-CAM shows where a class decision came from, and latent-space visualization shows how the model organizes images semantically.**\n'
        ),

        "estimated_minutes": 135,

        "has_code_examples": True,

        "sections": [
            {
                "id": 'why-interpretability-matters',
                "title": 'Why ConvNet interpretability matters',
                "order": 1,
            },
            {
                "id": 'intermediate-activations',
                "title": 'Visualizing intermediate activations',
                "order": 2,
            },
            {
                "id": 'filter-visualization',
                "title": 'Visualizing what individual filters detect',
                "order": 3,
            },
            {
                "id": 'grad-cam',
                "title": 'Grad-CAM: understanding a classification decision',
                "order": 4,
            },
            {
                "id": 'latent-space-visualization',
                "title": 'Visualizing the ConvNet latent space',
                "order": 5,
            },
            {
                "id": 'interpretability-workflow',
                "title": 'A practical ConvNet interpretation workflow',
                "order": 6,
            }
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": 'M10.L01.EX01',
            "title": 'Read a ConvNet Activation Stack',
            "lesson_code": "M10.L01",
            "section_id": 'intermediate-activations',
            "placement": "after_section",
            "description": 'Practice interpreting how image representations change from early to deep convolutional layers.',
            "instructions": '1. Imagine you visualize activations from four convolutional layers for the same cat image.\n2. Layer 1 clearly shows edges and color boundaries, while Layer 4 contains sparse, hard-to-recognize patterns.\n3. Explain why this progression is expected.\n4. Explain what a completely blank channel in a deeper layer suggests about the current image.\n5. In one paragraph, connect the observation to the idea of information distillation.',
            "expected_output": 'A short interpretation explaining increasing abstraction, activation sparsity, and information distillation across ConvNet depth.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'convnet-activations',
                'feature-maps',
                'representation-depth',
            ],
        },

        {
            "id": 'M10.L01.EX02',
            "title": 'Debug a Suspicious Prediction with Grad-CAM',
            "lesson_code": "M10.L01",
            "section_id": 'grad-cam',
            "placement": "after_section",
            "description": 'Use Grad-CAM reasoning to investigate whether a classifier is focusing on the intended object or a spurious region.',
            "instructions": "1. Assume a dog classifier predicts 'dog' with high confidence for an image containing a dog on grass.\n2. A Grad-CAM heatmap highlights mostly the grass instead of the dog.\n3. Explain what this suggests about the model's learned decision rule.\n4. Propose two dataset or training changes that could reduce this behavior.\n5. Explain how you would verify whether the changes improved the model.",
            "expected_output": 'A diagnosis of possible background bias or spurious correlation, two corrective actions, and a plan using Grad-CAM plus held-out evaluation.',
            "difficulty": DifficultyLevel.beginner,
            "skill_tested": [
                'grad-cam',
                'spurious-correlations',
                'model-debugging',
            ],
        }
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M10.L01.QZ01",

        "title": "Interpreting What ConvNets Learn — Knowledge Check",

        "lesson_code": "M10.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": 'M10.L01.Q01',
                "section_id": 'why-interpretability-matters',
                "question": 'Which technique is most directly intended to show how successive ConvNet layers transform one particular input image?',
                "options": [
                    'Intermediate activation visualization',
                    'Random label shuffling',
                    'Learning-rate scheduling',
                    'Weight decay',
                ],
                "correct": 0,
                "explanation": 'Intermediate activation visualization exposes the feature maps produced at different depths for a specific input.',
            },

            {
                "id": 'M10.L01.Q02',
                "section_id": 'intermediate-activations',
                "question": 'What usually happens to ConvNet representations as layer depth increases?',
                "options": [
                    'They become increasingly abstract and more task-relevant',
                    'They always become identical to the original image',
                    'They stop using channels',
                    'They become raw RGB values again',
                ],
                "correct": 0,
                "explanation": 'Early layers preserve local visual details, while deeper layers typically encode more abstract and class-relevant concepts.',
            },

            {
                "id": 'M10.L01.Q03',
                "section_id": 'filter-visualization',
                "question": 'During filter visualization, what is changed by gradient ascent?',
                "options": [
                    "The model's class labels",
                    'The model weights',
                    'The input image values',
                    'The dataset split',
                ],
                "correct": 2,
                "explanation": 'The model remains fixed. The input image is iteratively changed to maximize activation of the selected filter.',
            },

            {
                "id": 'M10.L01.Q04',
                "section_id": 'filter-visualization',
                "question": 'Why is model(x) preferred over model.predict(x) inside a low-level gradient visualization loop?',
                "options": [
                    'Because predict() changes model weights',
                    'Because model(x) keeps the computation differentiable for gradient calculation',
                    'Because predict() cannot process images',
                    'Because model(x) automatically creates labels',
                ],
                "correct": 1,
                "explanation": "Gradient-based visualization requires the model call to remain inside the backend's automatic-differentiation computation.",
            },

            {
                "id": 'M10.L01.Q05',
                "section_id": 'grad-cam',
                "question": 'What does a Grad-CAM heatmap primarily indicate?',
                "options": [
                    'Which pixels were stored in the training dataset',
                    'Which image regions contributed strongly to a selected class score',
                    'The exact model weights',
                    'The batch size used during training',
                ],
                "correct": 1,
                "explanation": 'Grad-CAM combines convolutional activations with class gradients to estimate which spatial regions supported the class prediction.',
            },

            {
                "id": 'M10.L01.Q06',
                "section_id": 'grad-cam',
                "question": 'Why is the last convolutional layer often used for Grad-CAM?',
                "options": [
                    'It combines high-level semantic information with spatial structure',
                    'It contains the original file name',
                    'It is always one-dimensional',
                    'It has no relationship to the final prediction',
                ],
                "correct": 0,
                "explanation": 'Late convolutional layers preserve spatial layout while containing features that are much more semantically related to the prediction.',
            },

            {
                "id": 'M10.L01.Q07',
                "section_id": 'latent-space-visualization',
                "question": 'What does it usually mean when two images are close together in a useful learned latent space?',
                "options": [
                    'The files have similar names',
                    'The model represents them as semantically similar',
                    'Their raw pixels must be identical',
                    'They must belong to different classes',
                ],
                "correct": 1,
                "explanation": 'A useful latent representation places semantically similar inputs near each other according to features learned by the model.',
            },

            {
                "id": 'M10.L01.Q08',
                "section_id": 'latent-space-visualization',
                "question": 'Why should a 2D latent-space visualization be interpreted cautiously?',
                "options": [
                    'All dimensionality-reduction projections lose or distort some information',
                    'Latent vectors can never be numerical',
                    '2D plots cannot contain points',
                    'ConvNets do not learn representations',
                ],
                "correct": 0,
                "explanation": 'Projecting hundreds or thousands of dimensions into two dimensions necessarily destroys some information and can distort distances or structure.',
            },

            {
                "id": 'M10.L01.Q09',
                "section_id": 'interpretability-workflow',
                "question": 'Which observation would most strongly suggest a spurious background correlation?',
                "options": [
                    'Grad-CAM repeatedly highlights the background instead of the target object',
                    'Early layers detect edges',
                    'The network has convolutional layers',
                    'The input has a batch dimension',
                ],
                "correct": 0,
                "explanation": 'If class evidence consistently comes from background regions, the model may be relying on an unintended shortcut rather than the object itself.',
            },

            {
                "id": 'M10.L01.Q10',
                "section_id": 'interpretability-workflow',
                "type": "open",
                "question": 'A ConvNet misclassifies an image. Describe how you would use intermediate activations, filter visualization, Grad-CAM, and latent-space inspection together to investigate the error.',
            }
        ],

        "passing_score": 70,
    },
}
