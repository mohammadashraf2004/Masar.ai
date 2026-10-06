"""M01.L03 — AI Integration and Model Serving.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 3, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L03"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Understand how major generative model families process text, audio, images, "
    "video, and 3D data; expose them through FastAPI; prototype multimodal clients; "
    "choose an appropriate model-serving strategy; and monitor serving behavior."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "AI Integration and Model Serving",

    "slug": "generative-ai-services-m01-l03",

    "description": (
        "Learn the mechanics behind language, audio, image, video, and 3D generative "
        "models, then connect those models to FastAPI endpoints. Build a practical "
        "mental model for local versus external serving, model preloading, streaming "
        "binary outputs, prototyping with Streamlit, and monitoring model endpoints."
    ),

    "order": 3,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "generative-ai",
        "fastapi",
        "model-serving",
        "transformers",
        "tokenization",
        "embeddings",
        "stable-diffusion",
        "audio-generation",
        "video-generation",
        "3d-generation",
        "streaming-response",
        "streamlit",
        "lifespan",
        "bentoml",
        "middleware",
        "monitoring",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L02",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "AI Integration and Model Serving",

        "content": """
# AI Integration and Model Serving

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L03  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 3 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain how transformers differ from recurrent neural networks at a high level.
- Describe tokenization, embeddings, positional encoding, self-attention, autoregressive prediction, and context windows.
- Explain how model size and available RAM/VRAM influence model-selection and deployment decisions.
- Integrate a local language-model pipeline with a FastAPI endpoint.
- Interpret important generation parameters such as `max_new_tokens`, `do_sample`, `temperature`, `top_k`, and `top_p`.
- Explain the differences among encoder-decoder, encoder-only, and decoder-only transformers.
- Describe the main generation pipelines behind audio, image, video, and 3D models introduced in the chapter.
- Return text, image bytes, audio streams, video streams, and 3D model files from FastAPI.
- Use Streamlit as a lightweight prototyping client for multimodal endpoints.
- Distinguish model swapping, application-lifespan preloading, and external model serving.
- Explain why BentoML or a hosted provider can complement FastAPI for demanding inference workloads.
- Use middleware to collect model-service monitoring information while recognizing logging privacy concerns.

---

## 1. From a web API to a multimodal GenAI service

In the previous lesson, FastAPI acted as the application layer around a model.

This chapter expands that idea across several data modalities.

The source builds examples for models that work with:

- text,
- audio,
- images,
- video,
- 3D geometry.

Each model family produces a different output representation, so each FastAPI endpoint must return a response appropriate for that modality.

A useful overview is:

| Modality | Example input | Model output before HTTP formatting | Typical HTTP response |
|---|---|---|---|
| Text | Text prompt | String/tokens | Text or JSON |
| Audio | Text prompt | Audio waveform array | Streamed WAV bytes |
| Image | Text prompt | Image object | PNG/JPEG bytes |
| Video | Image or prompt | Sequence of frames | Streamed MP4 bytes |
| 3D | Text prompt | Mesh representation | Streamed OBJ or other 3D file |

This gives us our first major model-serving principle:

> **The model output and the API response are not the same thing.**

A model may return tensors, arrays, frames, or a mesh. Your application often has to transform that internal representation into something a browser or client can understand.

The chapter uses Hugging Face model libraries for several local models and Streamlit for lightweight UI prototyping.

The full pattern is:

```text
User
  ↓
Streamlit / other client
  ↓
FastAPI endpoint
  ↓
Input preparation
  ↓
Generative model
  ↓
Model-native output
  ↓
Conversion / encoding
  ↓
HTTP response
  ↓
Client renderer
```

---

## 2. Transformers versus recurrent neural networks

Before exposing a language model through FastAPI, it helps to understand why transformer models became so important.

### The older sequential idea: RNNs

A recurrent neural network processes a sequence step by step.

For text, the rough process is:

```text
token 1 → state
           ↓
token 2 → updated state
           ↓
token 3 → updated state
           ↓
...
```

The **state vector** carries information forward from earlier tokens.

This creates a problem for long sequences.

Information from very early in a document has to survive many sequential updates before influencing a much later prediction.

As the chapter explains, this makes it difficult for RNNs to capture long-range relationships reliably.

### The transformer idea

Transformers use **self-attention** rather than relying on one recurrent hidden state moving through the sequence.

Self-attention lets tokens directly represent relationships with other tokens in the input.

Instead of thinking only in terms of neighboring positions:

```text
word 1 → word 2 → word 3 → word 4
```

the transformer can model pairwise relationships across the sequence.

That means a word near the end can strongly relate to an earlier word if the context demands it.

[[IMAGE_NEEDED: RNN versus transformer sequence processing | Side-by-side diagram: an RNN processing tokens sequentially through a carried state vector, and a transformer processing the whole sequence with attention connections between distant tokens | Learner should notice that RNN information flows step-by-step while transformer attention can directly represent long-range token relationships]]

### Attention heads

A transformer contains **attention heads**.

Each head learns its own attention pattern.

One head may emphasize one type of relationship while another learns another pattern.

Together, multiple attention heads allow the model to inspect the same sequence from several learned perspectives.

Conceptually:

```text
Input sequence
   ├── attention head 1 → relationship pattern A
   ├── attention head 2 → relationship pattern B
   ├── attention head 3 → relationship pattern C
   └── ...
```

The separate results contribute to the model's representation of context.

[[IMAGE_NEEDED: Multi-head attention map | A sentence with several words connected by weighted lines in multiple small attention-head panels; line thickness should represent stronger or weaker learned relationships | Learner should notice that different heads can focus on different contextual relationships within the same sequence]]

### Why transformers scale better

RNN computation is fundamentally sequential: later steps depend on earlier hidden-state computations.

Transformers can process much of a sequence in parallel during training.

That makes them more suitable for modern accelerator hardware and large-scale training.

This scalability helped make very large language models possible.

{{exercise:M01.L03.EX01}}

---

## 3. Tokens, embeddings, and positional information

Neural networks operate on numbers, not words.

So text must move through several representation stages before the transformer can process it.

### Step 1: tokenization

**Tokenization** divides text into pieces.

Tokens might represent:

- whole words,
- parts of words,
- punctuation,
- symbols.

Then each token is associated with an integer identifier.

Conceptually:

```text
"FastAPI is useful."
        ↓
tokenizer
        ↓
["Fast", "API", " is", " useful", "."]
        ↓
[421, 918, 27, 6302, 13]
```

The exact tokenization depends on the tokenizer used by the model.

### Step 2: embeddings

Token IDs are still only identifiers.

The model needs a representation in which relationships can be learned.

An **embedding layer** maps each token to a dense vector of floating-point values.

For example:

```text
token id 421
     ↓
embedding layer
     ↓
[0.12, -0.84, 0.07, ..., 0.31]
```

The vector has many dimensions.

During training, the model adjusts parameters so these numerical representations become useful for modeling language.

The chapter uses a geometric intuition: tokens used in related contexts can end up with vectors that are closer in the learned space.

One common way to compare vector directions is **cosine similarity**.

At this stage, remember the conceptual relationship:

> **Tokenization gives symbols IDs; embeddings give those tokens learned continuous representations.**

[[IMAGE_NEEDED: Tokenization to embeddings | A pipeline showing a sentence split into tokens, tokens mapped to integer IDs, and each ID mapped to a multi-dimensional floating-point embedding vector; optionally show a small 2D embedding plot with semantically related tokens closer together | Learner should notice the transformation from human-readable language to numeric model representations]]

### Step 3: positional encoding

Transformers can process token representations in parallel.

That creates a new question:

> If all tokens are processed together, how does the model know their order?

The source introduces **positional encoding**.

A position representation is combined with the token embedding so the representation carries both:

- what the token means in the learned representation,
- where it appears in the sequence.

Conceptually:

```text
token embedding
      +
position embedding
      =
representation used by attention
```

This matters because:

```text
"dog bites man"
```

and:

```text
"man bites dog"
```

contain similar tokens but different ordering and meaning.

### From representations to attention

The resulting representations are passed through transformer attention and other network layers.

The high-level path is:

```text
Text
  ↓
Tokens
  ↓
Token IDs
  ↓
Token embeddings
  +
Position information
  ↓
Transformer layers / attention
  ↓
Token probabilities
```

---

## 4. Autoregressive generation and the context window

A decoder-style language model generates text **autoregressively**.

That means each new prediction depends on information already present in the sequence.

Suppose the model sees:

```text
FastAPI is a Python web
```

It computes probabilities for possible next tokens.

It chooses or samples one token.

The new sequence might become:

```text
FastAPI is a Python web framework
```

Then the model predicts the next token again.

This repeats until:

- an end-of-sequence condition is reached,
- a stop token appears,
- a generation limit is reached.

### Generation loop

```text
Input tokens
    ↓
predict next-token probabilities
    ↓
select/sample next token
    ↓
append token
    ↓
run next prediction
    ↓
repeat
```

### The context window

A language model can only consider a limited number of tokens at once.

The chapter calls this the **context window**.

The context window can include:

- system instructions,
- user messages,
- conversation history,
- retrieved documents,
- generated tokens.

If the usable context is exceeded, information must be removed, summarized, truncated, or otherwise managed by the application/model implementation.

The engineering trade-off is important.

A larger context window can preserve more information, but it can also require:

- more memory,
- more computation,
- more latency,
- higher serving cost.

So model selection should not be based on "largest context wins."

Instead ask:

> **How much context does this use case really need, and what latency/cost can the service tolerate?**

---

## 5. Model size, memory, and hardware

Open-source language models can differ dramatically in parameter count.

A larger model generally needs more memory just to load its weights.

The chapter highlights the practical difference between:

- lightweight models that can run on consumer hardware,
- larger models requiring substantial GPU VRAM,
- extremely large models that may require multiple data-center GPUs.

### Parameters consume memory

A rough mental model is:

```text
more parameters
        ↓
more weight storage
        ↓
higher RAM / VRAM requirements
```

Training or fine-tuning can require still more memory because the system must hold additional states and intermediate values.

### Quantization

The source introduces **quantization** as a way to compress a model representation so a model can fit into less memory.

The detailed process is deferred to a later chapter, but the important lesson now is:

> Quantization trades numerical precision and sometimes quality/performance characteristics for lower memory usage.

### Local model versus provider API

The hardware requirement creates an important architectural decision.

You can:

```text
A. Self-host model
   → more infrastructure control
   → more hardware/operations responsibility

B. Use provider API
   → less model infrastructure
   → external dependency and data-sharing considerations
```

Neither choice is automatically correct.

Your decision depends on:

- privacy,
- cost,
- latency,
- expected traffic,
- model quality,
- available hardware,
- operational expertise.

---

## 6. Load and serve a local language model

The chapter demonstrates a small local conversational model through the Hugging Face `transformers` library.

A simplified version of the pattern looks like:

```python
import torch
from transformers import pipeline

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)


def load_text_model():
    return pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        device=device,
    )
```

The important architecture is:

```text
model identifier
      ↓
library downloads/loads artifacts
      ↓
model pipeline in memory
      ↓
generation function
```

### System and user messages

Conversational models often use structured messages such as:

```python
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant.",
    },
    {
        "role": "user",
        "content": prompt,
    },
]
```

The system message describes the desired assistant behavior.

The user message carries the current request.

A model-specific tokenizer can convert this structured conversation into the exact input format the model expects.

### Generation parameters

The source introduces several important controls.

#### `max_new_tokens`

Maximum number of newly generated tokens.

It controls output length, not the number of input tokens.

#### `do_sample`

Controls whether generation samples from candidate probabilities or chooses deterministically from the highest-probability option according to the implementation.

#### `temperature`

Controls the sharpness/randomness of sampling.

A beginner mental model:

```text
lower temperature
→ more conservative distribution

higher temperature
→ more varied sampling
```

It is not a "creativity guarantee." It changes sampling behavior.

#### `top_k`

Restricts candidate selection to the `k` highest-ranked token options.

Example:

```text
top_k = 50
→ only the current top 50 candidate tokens remain eligible
```

#### `top_p`

Uses cumulative probability mass.

Example:

```text
top_p = 0.95
→ include the highest-probability tokens until their cumulative probability reaches about 95%
```

This is commonly called **nucleus sampling**.

### Expose the model through FastAPI

A teaching version:

```python
from fastapi import FastAPI

app = FastAPI()
text_model = load_text_model()


@app.get("/generate/text")
def generate_text_controller(prompt: str):
    result = generate_text(text_model, prompt)
    return {"text": result}
```

The request path is:

```text
GET /generate/text
      ↓
read prompt
      ↓
pass prompt to model
      ↓
generate
      ↓
return HTTP response
```

### Hallucination remains possible

The source's local TinyLlama demonstration produces an incorrect statement in one example.

That is a useful teaching point.

A successfully running endpoint does **not** imply that the model's content is correct.

Operational success:

```text
HTTP 200
```

and semantic correctness:

```text
factually accurate answer
```

are separate properties.

The chapter therefore emphasizes warning users that language-model output may require fact-checking.

{{exercise:M01.L03.EX02}}

---

## 7. Prototype the service with Streamlit

Swagger UI is useful for endpoint testing, but it is not a realistic conversational interface.

The chapter uses **Streamlit** to build a lightweight browser client.

The role of Streamlit here is prototyping:

```text
User types prompt
      ↓
Streamlit client
      ↓
HTTP request to FastAPI
      ↓
FastAPI calls model
      ↓
response
      ↓
Streamlit renders output
```

A basic client may keep temporary chat history in `st.session_state`.

Conceptually:

```python
import requests
import streamlit as st

st.title("FastAPI ChatBot")

if "messages" not in st.session_state:
    st.session_state.messages = []

if prompt := st.chat_input("Write your prompt"):
    response = requests.get(
        "http://localhost:8000/generate/text",
        params={"prompt": prompt},
    )
    response.raise_for_status()
    st.markdown(response.text)
```

This is useful because it lets you test the **experience** around your endpoint without building a full frontend application.

[[IMAGE_NEEDED: FastAPI plus Streamlit prototype architecture | A diagram showing browser user → Streamlit client → FastAPI `/generate/text` endpoint → local model → response back through FastAPI → Streamlit chat display | Learner should notice that Streamlit is the client/UI while FastAPI remains the backend service]]

### Important limitation of the first prototype

If the route loads the model during **every request**, the service will be slow and wasteful.

For a large model:

```text
Request
  ↓
load model
  ↓
generate
  ↓
unload/lose model instance

next request
  ↓
load model again
```

Later in this lesson, we will fix that with model-serving strategies.

### Transformer variants

The source distinguishes three transformer configurations.

#### Encoder-decoder

Useful when transforming one sequence into another.

Examples in the source include:

- translation,
- summarization,
- question-answering tasks.

#### Encoder-only

Strong for representing and understanding input.

Examples:

- sentiment analysis,
- entity extraction,
- classification.

#### Decoder-only

Strong for autoregressive generation.

Examples:

- text generation,
- chat,
- language modeling.

Memory aid:

| Variant | Main mental model |
|---|---|
| Encoder-decoder | Transform input sequence into output sequence |
| Encoder-only | Understand/represent input |
| Decoder-only | Continue/generate sequence |

Model architecture should match the task.

---

## 8. Audio generation and streaming responses

Audio generation introduces two new ideas:

1. the model pipeline can contain multiple stages;
2. the API often needs to stream binary media rather than return text.

### Bark pipeline

The source uses Bark as the teaching example.

It describes a multi-stage pipeline:

1. **Semantic text model**  
   Converts text into a semantic representation.

2. **Coarse acoustics model**  
   Generates broad audio features.

3. **Fine acoustics model**  
   Refines those features with additional detail.

4. **Audio codec model**  
   Decodes the generated codes into a playable waveform.

A mental model:

```text
Text
  ↓
semantic tokens
  ↓
coarse acoustic representation
  ↓
fine acoustic representation
  ↓
audio codec
  ↓
waveform
```

[[IMAGE_NEEDED: Text-to-audio synthesis pipeline | A four-stage diagram showing text entering a semantic model, then coarse acoustics, then fine acoustics, then an audio codec that produces a waveform | Learner should notice that audio generation is a pipeline of representations rather than a single direct text-to-file conversion]]

### What the model returns

An audio model can produce an array of floating-point values representing waveform amplitude over time.

That is not yet a WAV file.

The service needs:

- the waveform,
- the sample rate,
- an encoding step.

### Convert the waveform to an in-memory audio file

A simplified pattern:

```python
from io import BytesIO
import soundfile


def audio_array_to_buffer(audio_array, sample_rate):
    buffer = BytesIO()
    soundfile.write(
        buffer,
        audio_array,
        sample_rate,
        format="wav",
    )
    buffer.seek(0)
    return buffer
```

Now the bytes can be sent to the client.

### Why `StreamingResponse`?

For larger media, it is often useful to stream data.

```python
from fastapi.responses import StreamingResponse


@app.get("/generate/audio")
def generate_audio_controller(prompt: str):
    audio, sample_rate = generate_audio(...)
    buffer = audio_array_to_buffer(
        audio,
        sample_rate,
    )

    return StreamingResponse(
        buffer,
        media_type="audio/wav",
    )
```

The main concept is:

> The endpoint describes the content correctly and returns an iterable/streamable byte representation.

### Memory versus disk

The source also highlights a useful systems trade-off.

**In-memory buffer**

- lower disk overhead,
- often lower latency,
- consumes RAM.

**Write to file first**

- can reduce memory pressure,
- adds disk I/O and latency.

There is no universal winner.

It depends on output size and resource constraints.

### Streamlit rendering

A Streamlit client can display returned binary audio content with its audio component.

The same backend pattern remains:

```text
model output array
      ↓
encode WAV
      ↓
FastAPI stream
      ↓
client audio player
```

{{exercise:M01.L03.EX03}}

---

## 9. Stable Diffusion and image-serving endpoints

The chapter uses Stable Diffusion as the main image-generation architecture.

### Diffusion intuition

The important idea is the relationship between:

- noise,
- latent representations,
- denoising.

During the conceptual diffusion process, the system learns how noisy representations relate to meaningful images.

During generation, a noisy representation can be iteratively refined.

Text conditioning helps steer this process toward the requested concept.

A simplified inference view:

```text
Text prompt
    ↓
text representation
    ↓
condition denoising process
    ↓
noisy latent representation
    ↓
iterative denoising
    ↓
decoded image
```

[[IMAGE_NEEDED: Stable Diffusion training and inference | A two-part diagram: forward process gradually corrupting/encoding an image toward noise, and reverse inference process starting from noisy latent representation and iteratively denoising it while conditioned by a text prompt | Learner should notice that generation uses iterative denoising controlled by prompt information]]

### Inference steps

The source exposes an argument such as:

```python
num_inference_steps=10
```

More steps generally imply more computation and longer generation.

The exact quality relationship depends on the model and scheduler, so treat the parameter as a **quality/latency control**, not a guarantee.

### Image model output

A diffusion pipeline may return a Pillow image.

That Python object must be converted to bytes before normal HTTP clients can receive it.

```python
from io import BytesIO


def image_to_bytes(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()
```

Then the FastAPI route can return:

```python
from fastapi import Response


@app.get("/generate/image")
def generate_image_controller(prompt: str):
    image = generate_image(...)
    return Response(
        content=image_to_bytes(image),
        media_type="image/png",
    )
```

The media type matters.

Without the correct type, a client may not know how to interpret the bytes.

### Larger image models

The chapter notes that larger image models need substantially more memory and are much better suited to GPU inference.

It also lists limitations that image-generation systems can exhibit, including:

- imperfect coherence,
- constrained output sizes,
- limited composition control,
- imperfect photorealism,
- difficulty rendering legible text.

The important lesson is that **higher model size does not remove every failure mode**.

### LoRA

The chapter introduces **Low-Rank Adaptation (LoRA)** as a fine-tuning strategy.

Instead of training all original model parameters, LoRA adds a comparatively small number of trainable parameters while most base-model parameters remain fixed.

The practical attraction is:

```text
fewer trainable parameters
        ↓
lower training memory requirement
        ↓
more practical customization
```

You will study fine-tuning in more depth later; here, remember why LoRA is relevant to large generative models.

{{exercise:M01.L03.EX04}}

---

## 10. Video generation: frames, encoding, and GPU cost

Video generation is much more computationally demanding than creating a single image.

A video is a sequence of frames.

At 30 frames per second:

```text
1 second
→ about 30 images/frames
```

The model must maintain visual consistency across those frames.

The source uses an image-to-video diffusion pipeline as its practical example.

### Image-to-video flow

```text
Input image
    ↓
resize / preprocess
    ↓
video diffusion model
    ↓
generated frame sequence
    ↓
video encoder
    ↓
MP4 buffer
    ↓
StreamingResponse
```

The source uses a fixed random seed in the example to make generation reproducible.

That illustrates another useful model-engineering concept:

> A controlled random seed can make a stochastic generation experiment easier to reproduce.

### Frame generation parameters

Two useful controls introduced in the example are:

- number of frames to generate,
- chunk size used while decoding frames.

Both affect resource requirements.

### Convert frames into a video

Individual Pillow images are not yet a video file.

A video library can:

1. create an MP4 container,
2. configure a codec,
3. encode each frame,
4. write encoded packets into the container,
5. return the completed buffer.

### File upload endpoint

The source's image-to-video route accepts an uploaded image.

Conceptually:

```python
@app.post("/generate/video")
def generate_video_controller(image: bytes = File(...)):
    input_image = Image.open(BytesIO(image))
    frames = generate_video(model, input_image)
    video_buffer = export_to_video_buffer(frames)

    return StreamingResponse(
        video_buffer,
        media_type="video/mp4",
    )
```

This is different from the earlier text-query endpoints.

Now the request includes binary file content.

### Why GPU matters

Video generation involves:

- many frames,
- high-dimensional representations,
- repeated denoising/decoding,
- large memory footprints.

The chapter therefore treats a CUDA-capable GPU as necessary for the demonstrated video model.

---

## 11. Large vision models and temporal consistency

The source then discusses a large text/video generation architecture as a conceptual example of combining transformer and diffusion ideas.

The important educational point is not the product name.

It is the architecture pattern:

```text
Transformer-style sequence modeling
              +
Diffusion-style iterative refinement
              ↓
High-dimensional visual generation
```

### Why video is difficult

The chapter highlights several challenges.

#### Temporal consistency

Objects should remain consistent from one frame to another.

If a person, car, or object changes identity unexpectedly, the illusion of a coherent world breaks.

#### Spatial consistency

The scene must preserve geometry and relationships as the camera or objects move.

#### Training data

High-quality video training requires:

- large data volumes,
- useful descriptions/captions,
- temporal information,
- meaningful metadata.

### Visual patches

The source describes representing visual information as patches, analogous at a high level to how text models work with tokens.

Mental model:

```text
text model
→ sequence of text tokens

vision transformer
→ sequence of visual/spatiotemporal patches
```

### Emergent behaviors described by the source

The chapter discusses capabilities such as:

- 3D consistency,
- object permanence,
- long-range temporal coherence,
- interaction with the generated environment,
- simulation-like behavior.

For this lesson, treat these as capabilities discussed in the source, not as a guarantee that every video model or every generated video will exhibit them reliably.

### Licensing remains part of engineering

The source explicitly warns that some open-source models may not permit every commercial use.

Therefore:

> **Model selection is not only a technical decision; license terms also matter.**

Before commercial deployment, inspect the model's license/model card.

---

## 12. Generating 3D geometry

Three-dimensional generation introduces spatial geometry.

### Mesh basics

A mesh can be described using:

- **vertices** — points in 3D space,
- **edges** — connections between vertices,
- **faces** — surfaces formed by connected edges/vertices.

A vertex can have coordinates:

```text
(x, y, z)
```

Many connected faces form the surface of a 3D object.

[[IMAGE_NEEDED: Vertices, edges, and faces in a 3D mesh | A simple low-poly 3D object with individual vertices marked as points, selected edges highlighted as line segments, and one or two polygon faces filled or shaded | Learner should notice how points connect into edges and edges form surface polygons]]

### Why naïve token-by-token geometry is expensive

A detailed object may require many thousands of vertices and faces.

Generating every coordinate sequentially can become slow.

The chapter therefore introduces **implicit functions** as another way to represent 3D surfaces.

Instead of explicitly storing every surface point, an implicit representation defines the shape continuously through a learned function.

### NeRF intuition

The chapter describes **Neural Radiance Fields (NeRF)** as part of the rendering idea.

At a high level, the function maps information such as:

- position in 3D space,
- viewing direction

to values such as:

- density,
- color.

This allows novel views of a learned 3D scene to be synthesized.

### Signed distance functions

A **signed distance function (SDF)** indicates how far a point is from a surface.

A simple mental model:

```text
negative → inside object
zero     → on surface
positive → outside object
```

The zero-valued boundary represents the surface.

### Shap-E flow in the source

The source uses Shap-E as its practical text-to-3D example.

Conceptually:

```text
Text prompt
   ↓
3D generative pipeline
   ↓
mesh representation
   ↓
convert mesh tensors
   ↓
OBJ buffer
   ↓
FastAPI StreamingResponse
   ↓
3D modeling application
```

The generated mesh may contain:

- vertices,
- faces,
- color information.

### OBJ serving

A FastAPI endpoint can declare a 3D media type and mark the response as an attachment.

The client can then save the generated object and open it in software such as Blender.

### Point clouds

The chapter also contrasts meshes with **point clouds**.

A point cloud is a large collection of 3D coordinates representing sampled points in space.

The source notes that scanning technologies such as LiDAR can produce point clouds.

The high-level distinction:

```text
mesh
→ explicit connected surface structure

point cloud
→ collection of sampled 3D points
```

{{exercise:M01.L03.EX05}}

---

## 13. Three model-serving strategies

After building endpoints for several modalities, the chapter asks the most important production question:

> **Where and when should the model be loaded?**

It presents three strategies.

### Strategy A — model agnostic: load/swap per request

Pattern:

```text
request
  ↓
load requested model
  ↓
generate
  ↓
release/swap
  ↓
response
```

This gives flexibility.

It can be useful when:

- memory is limited,
- only a few users access the service,
- you want to experiment with different models,
- latency is not critical.

The disadvantage is model-load latency.

Large models may take significant time to load, so repeated loading can dominate the request time.

### Strategy B — compute efficient: preload with lifespan

Pattern:

```text
application startup
        ↓
load model once
        ↓
request 1 → reuse model
request 2 → reuse model
request 3 → reuse model
        ↓
application shutdown
        ↓
cleanup / release model
```

This trades memory for lower request latency.

### Strategy C — lean application: serve models externally

Pattern:

```text
Client
  ↓
FastAPI application
  ↓
external model server/provider
  ↓
model inference
  ↓
FastAPI
  ↓
Client
```

FastAPI remains responsible for application concerns such as:

- users,
- security,
- business logic,
- prompt enrichment,
- content filtering,
- coordination,
- monitoring.

The external model layer focuses on inference.

### Decision table

| Strategy | Main advantage | Main trade-off |
|---|---|---|
| Load/swap per request | Flexible and lower persistent memory use | High latency from repeated loading |
| Preload with lifespan | Fast repeated inference | Model occupies RAM/VRAM continuously |
| External model serving | Separates application and inference concerns | More infrastructure/network integration |

{{exercise:M01.L03.EX06}}

---

## 14. Preload models with FastAPI lifespan

The source uses the FastAPI application lifespan to load resources before serving requests.

A simplified version is:

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    models["text2image"] = load_image_model()

    yield

    models.clear()


app = FastAPI(lifespan=lifespan)
```

The key line is:

```python
yield
```

It separates the two phases.

```text
before yield
→ application startup

yield
→ requests are served

after yield
→ application shutdown cleanup
```

Then routes reuse the preloaded model:

```python
@app.get("/generate/image")
def generate_image_controller(prompt: str):
    image = generate_image(
        models["text2image"],
        prompt,
    )
    ...
```

### Why this improves latency

Without preloading:

```text
every request
→ disk/model load
→ inference
```

With preloading:

```text
startup once
→ model load

every request
→ inference only
```

This can dramatically improve user-perceived response time.

### Memory constraint

Preloading multiple large models can exhaust RAM or VRAM.

If each model requires a large amount of accelerator memory, it may be better to:

- deploy models separately,
- allocate different GPUs,
- call separate model servers.

### Legacy startup/shutdown handlers

The source also shows the older `startup` and `shutdown` event-handler style.

You should recognize it because existing code may use it, even though the lesson's preferred mental model is the lifespan context.

---

## 15. External serving: BentoML, providers, and abstraction layers

### Why move inference outside FastAPI?

FastAPI is excellent for application logic, but high-throughput model serving may need capabilities such as:

- process-based parallelism,
- inference batching,
- model resource management,
- specialized deployment logic.

The source introduces several external-serving options.

### Cloud model infrastructure

Cloud platforms can provide managed model endpoints.

The application then calls a network endpoint instead of owning the model process directly.

This reduces some infrastructure burden but introduces:

- provider/platform learning curves,
- deployment dependencies,
- networking,
- cost considerations.

### BentoML

The chapter uses BentoML as an example of a framework purpose-built for ML serving.

The source highlights abilities such as:

- running requests across worker processes,
- handling CPU-bound inference more appropriately,
- batching inference requests,
- managing model-serving concerns separately from FastAPI.

The architecture becomes:

```text
Client
  ↓
FastAPI :8000
  ↓ HTTP
BentoML model server :5000
  ↓
model
```

FastAPI can call the model service asynchronously with an HTTP client.

Conceptually:

```python
import httpx


async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://model-server/generate",
        json={"prompt": prompt},
    )
```

### External model providers

A different option is a hosted model API.

Then FastAPI becomes a wrapper:

```text
User
  ↓
your FastAPI API
  ↓
provider SDK/API
  ↓
hosted model
  ↓
your FastAPI API
  ↓
User
```

This can reduce self-hosting burden.

But the source reminds you to consider data privacy because input may be sent to an external service.

### Self-hosting versus hosted providers

| Self-hosting | Hosted provider |
|---|---|
| More infrastructure responsibility | Less inference infrastructure to manage |
| Greater deployment/control responsibility | External dependency |
| Potentially stronger direct control over data path | Data handling must match provider terms and architecture |
| Hardware/operations cost | Usage/service cost |

### Provider abstraction with orchestration libraries

The source also introduces an abstraction library that can help switch between model providers.

The deeper architectural idea is more general than one library:

> **Do not tightly couple all business logic to one model-provider SDK if you expect providers to change.**

A provider abstraction can isolate:

- prompt formatting,
- model invocation,
- provider-specific configuration.

That makes swapping integrations easier.

---

## 16. Monitor model-serving endpoints with middleware

Once several model endpoints exist, you need to understand how they behave in real use.

Examples of useful monitoring data include:

- request ID,
- request time,
- endpoint,
- client information,
- response duration,
- status code,
- success/failure.

### Why middleware?

Without middleware, every route might repeat logging code.

```text
text endpoint → logging logic
audio endpoint → same logging logic
image endpoint → same logging logic
video endpoint → same logging logic
```

Middleware centralizes the concern.

```text
request
  ↓
monitoring middleware starts timer / assigns ID
  ↓
route handler
  ↓
middleware records response data
  ↓
response
```

### Teaching version

```python
import time
from uuid import uuid4
from fastapi import Request


@app.middleware("http")
async def monitor_service(request: Request, call_next):
    request_id = uuid4().hex
    started = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - started

    response.headers["X-Response-Time"] = str(duration)
    response.headers["X-API-Request-ID"] = request_id

    return response
```

This demonstrates the middleware lifecycle:

1. inspect or annotate the request,
2. call the downstream route,
3. inspect or annotate the response,
4. return it.

[[IMAGE_NEEDED: Monitoring middleware request lifecycle | Diagram showing client request entering monitoring middleware, passing to a model-serving route, returning through the same middleware where duration/status/request ID are captured, then going back to the client | Learner should notice that one middleware layer can monitor many endpoints consistently]]

### Persistent logging matters

The source warns against relying on a local CSV file as a production monitoring store.

Why?

A container or host may restart or be deleted.

If logs live only inside ephemeral local storage, the records can disappear.

Production monitoring should use appropriate persistent logging/observability infrastructure.

### Privacy matters too

Logging request and response bodies may capture:

- personal data,
- proprietary prompts,
- confidential documents,
- generated sensitive content.

So a monitoring system must balance observability with:

- data minimization,
- privacy,
- retention rules,
- security,
- performance.

### Monitoring is not only about errors

For AI services, you may eventually want to monitor both system and model behavior.

This chapter focuses mainly on service usage and timing.

A useful foundation is:

```text
Can I identify the request?
Can I measure its latency?
Can I see whether it succeeded?
Can I identify which endpoint handled it?
```

You can build richer AI-specific observability on top of those basics later.

{{exercise:M01.L03.EX07}}

---

## 17. Putting the entire chapter together

The chapter begins with individual models but ends with system design.

That progression matters.

A production GenAI service is not:

```text
FastAPI + one model call
```

A more accurate mental model is:

```text
                           ┌─────────────────┐
                           │      User       │
                           └────────┬────────┘
                                    │
                                    ▼
                           ┌─────────────────┐
                           │ Client / UI     │
                           │ e.g. Streamlit  │
                           └────────┬────────┘
                                    │
                                    ▼
                     ┌─────────────────────────┐
                     │       FastAPI API       │
                     ├─────────────────────────┤
                     │ validation              │
                     │ routing                 │
                     │ authentication          │
                     │ business logic          │
                     │ content conversion      │
                     │ streaming responses     │
                     │ middleware monitoring   │
                     └──────────┬──────────────┘
                                │
           ┌────────────────────┼────────────────────┐
           │                    │                    │
           ▼                    ▼                    ▼
    Preloaded local       External model       Provider API
        model                 server
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                                ▼
                 text / audio / image / video / 3D
```

### Five questions before serving a model

When integrating a new model, ask:

1. **What input representation does it expect?**
2. **What native output does it produce?**
3. **How should that output be encoded for HTTP?**
4. **Where should the model live—per request, preloaded, or external?**
5. **How will I measure latency, failures, and usage safely?**

If you can answer those five questions, you have moved from simply "running a model" toward **serving a model as part of a real application**.

---

## Important misconceptions

### Misconception 1

> A language model directly reads human words.

### Why this is wrong

Text is tokenized and transformed into numerical representations before being processed by the neural network.

### Misconception 2

> Embeddings are just token IDs with more digits.

### Why this is wrong

Token IDs are identifiers. Embeddings are learned dense numerical vectors used by the model to represent useful properties and relationships.

### Misconception 3

> A larger context window is always better.

### Why this is wrong

Larger contexts can consume more memory, computation, latency, and cost. The useful context size depends on the application.

### Misconception 4

> If FastAPI returns HTTP 200, the model answer must be correct.

### Why this is wrong

HTTP success only means the request was processed successfully. A language model can still hallucinate or produce low-quality content.

### Misconception 5

> Audio, image, video, and 3D endpoints can all return ordinary JSON without extra conversion.

### Why this is wrong

These models often produce arrays, image objects, frame sequences, or meshes. The service must encode these into appropriate byte/file formats and media types.

### Misconception 6

> `StreamingResponse` makes model inference itself faster.

### Why this is wrong

Streaming changes how response data is delivered. It does not automatically reduce the computation required to generate the content.

### Misconception 7

> Loading a large model inside every request is a reasonable production default.

### Why this is wrong

Repeated model loading can dominate latency. Preloading or external serving is usually more appropriate for frequently used heavy models.

### Misconception 8

> Preloading every model is always best.

### Why this is wrong

Preloading improves repeated-request latency but consumes persistent RAM/VRAM. Multiple large models may not fit.

### Misconception 9

> FastAPI and BentoML are mutually exclusive choices.

### Why this is wrong

The source shows a complementary architecture: FastAPI handles application concerns while BentoML can specialize in inference serving.

### Misconception 10

> More logging is always better.

### Why this is wrong

Logging prompt and response content can create privacy, security, storage, and performance risks. Monitoring must be designed intentionally.

---

## Key terminology

| Term | Meaning |
|---|---|
| RNN | Recurrent neural network that processes sequences using recurrent state |
| Transformer | Neural architecture that uses attention mechanisms to model sequence relationships |
| Self-attention | Mechanism that represents relationships among elements in the same input sequence |
| Attention head | One learned attention mechanism within a multi-head attention block |
| Token | A model-specific piece of text such as a word, subword, symbol, or punctuation |
| Token ID | Integer identifier assigned to a token |
| Embedding | Dense numerical vector representation used by the model |
| Cosine similarity | Vector similarity measure based on the angle between vectors |
| Positional encoding | Representation added/combined with token representations to encode sequence position |
| Autoregressive generation | Generating each new element using previously available sequence elements |
| Context window | Maximum amount of token context a model can use at one time |
| Parameter | Learned model value such as a weight or bias |
| VRAM | GPU memory used to store model weights and inference data |
| Quantization | Reducing numerical precision/representation to lower model resource requirements |
| Temperature | Sampling control that changes the probability distribution used during generation |
| Top-k sampling | Sampling from only the highest-ranked `k` candidate tokens |
| Top-p sampling | Sampling from the smallest high-probability token set whose cumulative mass reaches a threshold |
| Encoder-only transformer | Transformer configuration mainly used for input representation/understanding tasks |
| Decoder-only transformer | Transformer configuration suited to autoregressive generation |
| Encoder-decoder transformer | Transformer configuration that maps an input sequence to an output sequence |
| Waveform | Numerical representation of audio amplitude over time |
| Sample rate | Number of audio samples represented per unit time |
| Stable Diffusion | Diffusion-based image-generation approach using latent representations and iterative denoising |
| Inference step | One iterative generation/refinement step in a diffusion-style process |
| LoRA | Fine-tuning approach that trains a small set of added low-rank parameters while keeping most base weights fixed |
| Frame | One still image in a video sequence |
| Temporal consistency | Maintaining coherent objects/events across successive video frames |
| Visual patch | Chunk of visual/spatiotemporal information used as a model representation |
| Vertex | Point in 3D space |
| Edge | Connection between vertices |
| Face | Polygon surface built from connected vertices/edges |
| Mesh | Connected geometric representation composed of vertices, edges, and faces |
| Point cloud | Collection of sampled 3D coordinates without necessarily defining connected faces |
| NeRF | Neural radiance field approach for representing/rendering views of 3D scenes |
| SDF | Signed distance function describing distance relative to a surface |
| Model swapping | Loading different models as needed instead of keeping all of them resident |
| Model preloading | Loading a model during application startup so requests can reuse it |
| Lifespan | FastAPI startup/shutdown context used to initialize and clean up shared resources |
| External model server | Separate service responsible primarily for model inference |
| Middleware | Code executed around request handling, useful for shared concerns such as monitoring |
| Request ID | Unique identifier used to trace one request through a service |

---

## Self-check

Before continuing, make sure you can answer:

1. Why do transformers handle long-range token relationships differently from RNNs?
2. What does an attention head learn?
3. What is the difference between a token ID and an embedding?
4. Why does a transformer need position information?
5. What does autoregressive generation mean?
6. What is a context window, and what trade-offs come with making it larger?
7. Why does model size affect RAM/VRAM requirements?
8. What problem does quantization try to address?
9. What do `temperature`, `top_k`, and `top_p` influence?
10. Why can a correctly functioning API still return an incorrect model answer?
11. What are encoder-only, decoder-only, and encoder-decoder transformers suited for?
12. What stages does the Bark pipeline use conceptually?
13. Why is an audio waveform not automatically a WAV file?
14. Why are streaming responses useful for larger media outputs?
15. How does a Stable Diffusion-style model conceptually generate an image from noise and text conditioning?
16. What trade-off does increasing inference steps introduce?
17. What problem does LoRA address?
18. Why is video generation more resource-intensive than still-image generation?
19. What are temporal and spatial consistency?
20. What are vertices, edges, faces, meshes, and point clouds?
21. What is the basic intuition behind an SDF?
22. When is model swapping useful?
23. What advantage does lifespan preloading provide?
24. Why might several large models need separate processes/GPUs?
25. Why might FastAPI call BentoML or another model server instead of performing inference directly?
26. What privacy concern appears when using external model providers?
27. Why is middleware a good place for shared service monitoring?
28. Why should production logs not rely solely on ephemeral local files?
29. What privacy risks arise from logging prompt and response bodies?
30. What five questions should you answer before exposing a new model through an API?

---

## Retain this idea

**Model serving is the bridge between machine learning and software engineering: understand the representation a model consumes and produces, convert its outputs into correct HTTP responses, choose where the model should live based on latency and memory constraints, and wrap inference with a reliable FastAPI application layer that can prototype, stream, monitor, secure, and scale the service.**
""",

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "serving-multimodal-models",
                "title": "From a web API to a multimodal GenAI service",
                "order": 1,
            },
            {
                "id": "transformers-vs-rnns",
                "title": "Transformers versus recurrent neural networks",
                "order": 2,
            },
            {
                "id": "tokens-embeddings-position",
                "title": "Tokens, embeddings, and positional information",
                "order": 3,
            },
            {
                "id": "autoregressive-context",
                "title": "Autoregressive generation and the context window",
                "order": 4,
            },
            {
                "id": "hardware-and-model-size",
                "title": "Model size, memory, and hardware",
                "order": 5,
            },
            {
                "id": "serving-a-language-model",
                "title": "Load and serve a local language model",
                "order": 6,
            },
            {
                "id": "streamlit-and-transformer-variants",
                "title": "Prototype the service with Streamlit",
                "order": 7,
            },
            {
                "id": "audio-models",
                "title": "Audio generation and streaming responses",
                "order": 8,
            },
            {
                "id": "vision-models",
                "title": "Stable Diffusion and image-serving endpoints",
                "order": 9,
            },
            {
                "id": "video-models",
                "title": "Video generation: frames, encoding, and GPU cost",
                "order": 10,
            },
            {
                "id": "large-vision-models",
                "title": "Large vision models and temporal consistency",
                "order": 11,
            },
            {
                "id": "three-dimensional-models",
                "title": "Generating 3D geometry",
                "order": 12,
            },
            {
                "id": "serving-strategies",
                "title": "Three model-serving strategies",
                "order": 13,
            },
            {
                "id": "lifespan-preloading",
                "title": "Preload models with FastAPI lifespan",
                "order": 14,
            },
            {
                "id": "external-serving",
                "title": "External serving: BentoML, providers, and abstraction layers",
                "order": 15,
            },
            {
                "id": "monitoring-middleware",
                "title": "Monitor model-serving endpoints with middleware",
                "order": 16,
            },
            {
                "id": "architecture-decision",
                "title": "Putting the entire chapter together",
                "order": 17,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L03.EX01",

            "title": "Trace RNN and Transformer Context",

            "lesson_code": "M01.L03",

            "section_id": "transformers-vs-rnns",

            "placement": "after_section",

            "description": (
                "Build an intuitive understanding of how sequence information flows "
                "through an RNN versus a transformer."
            ),

            "instructions": (
                "Consider the sentence: `The API that the engineering team deployed "
                "yesterday is failing.`\n\n"
                "1. Draw a simple RNN-style sequence in which information is carried "
                "token by token through a state.\n"
                "2. Draw a transformer-style representation with direct attention "
                "links between contextually related distant words.\n"
                "3. Explain in 3-5 sentences why long-range relationships are harder "
                "for a simple recurrent state to preserve.\n"
                "4. State one reason transformer training is more parallelizable."
            ),

            "expected_output": (
                "Two simple sequence diagrams and a short explanation comparing "
                "information flow and parallelism."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "transformer-intuition",
                "self-attention",
                "sequence-modeling",
            ],
        },

        {
            "id": "M01.L03.EX02",

            "title": "Tune a Text Generation Configuration",

            "lesson_code": "M01.L03",

            "section_id": "serving-a-language-model",

            "placement": "after_section",

            "description": (
                "Practice reasoning about common text-generation parameters without "
                "treating them as arbitrary numbers."
            ),

            "instructions": (
                "You have two use cases:\n\n"
                "A. A concise technical support assistant that should be relatively "
                "consistent.\n"
                "B. A brainstorming assistant where more variation is acceptable.\n\n"
                "For each use case, propose qualitative settings for:\n"
                "- `max_new_tokens`,\n"
                "- `do_sample`,\n"
                "- `temperature`,\n"
                "- `top_k`,\n"
                "- `top_p`.\n\n"
                "You do not need to find one perfect numeric configuration. Explain "
                "the direction of each choice and the expected behavior."
            ),

            "expected_output": (
                "Two generation configurations with reasoning for how the settings "
                "change output length, determinism, and sampling diversity."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "generation-parameters",
                "sampling-reasoning",
                "llm-inference",
            ],
        },

        {
            "id": "M01.L03.EX03",

            "title": "Design an Audio Response Pipeline",

            "lesson_code": "M01.L03",

            "section_id": "audio-models",

            "placement": "after_section",

            "description": (
                "Trace a text-to-audio result from user prompt to playable HTTP response."
            ),

            "instructions": (
                "Design the flow for a `/generate/audio` endpoint.\n\n"
                "Include these stages in the correct order:\n"
                "1. text prompt,\n"
                "2. audio generation pipeline,\n"
                "3. waveform array,\n"
                "4. sample rate,\n"
                "5. WAV encoding into a buffer,\n"
                "6. `StreamingResponse`,\n"
                "7. client audio player.\n\n"
                "Then explain why returning the raw Python/numpy waveform object directly "
                "would not be equivalent to returning a playable WAV response."
            ),

            "expected_output": (
                "An ordered pipeline diagram plus a short explanation of media encoding."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "audio-serving",
                "streaming-response",
                "media-encoding",
            ],
        },

        {
            "id": "M01.L03.EX04",

            "title": "Trace Text-to-Image Generation",

            "lesson_code": "M01.L03",

            "section_id": "vision-models",

            "placement": "after_section",

            "description": (
                "Connect the Stable Diffusion mental model to the API response pipeline."
            ),

            "instructions": (
                "Create a diagram for a text-to-image request with these ideas:\n"
                "1. text prompt,\n"
                "2. text conditioning,\n"
                "3. noisy latent representation,\n"
                "4. iterative denoising,\n"
                "5. decoded image,\n"
                "6. Pillow image object,\n"
                "7. PNG bytes,\n"
                "8. HTTP response with `image/png`.\n\n"
                "Then explain the latency trade-off of increasing the number of "
                "diffusion inference steps."
            ),

            "expected_output": (
                "A complete generation-and-serving pipeline plus an inference-step trade-off explanation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "diffusion-intuition",
                "image-serving",
                "http-media-types",
            ],
        },

        {
            "id": "M01.L03.EX05",

            "title": "From 3D Prompt to OBJ File",

            "lesson_code": "M01.L03",

            "section_id": "three-dimensional-models",

            "placement": "after_section",

            "description": (
                "Practice the geometric and API concepts needed for text-to-3D serving."
            ),

            "instructions": (
                "1. Define vertex, edge, face, mesh, and point cloud in your own words.\n"
                "2. Explain the sign convention of an SDF: inside, surface, outside.\n"
                "3. Draw a flow from text prompt → generative 3D pipeline → mesh → "
                "OBJ conversion → `StreamingResponse` → Blender or another 3D viewer.\n"
                "4. Explain why generating a detailed object by predicting every "
                "vertex sequentially can be expensive."
            ),

            "expected_output": (
                "Five definitions, an SDF explanation, and a text-to-3D serving diagram."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "3d-representation",
                "mesh-serving",
                "implicit-representation-intuition",
            ],
        },

        {
            "id": "M01.L03.EX06",

            "title": "Choose the Model-Serving Strategy",

            "lesson_code": "M01.L03",

            "section_id": "serving-strategies",

            "placement": "after_section",

            "description": (
                "Choose among model swapping, lifespan preloading, and external serving "
                "based on workload constraints."
            ),

            "instructions": (
                "Choose the most appropriate primary strategy for each scenario and justify it:\n\n"
                "1. A local experiment on a laptop with limited memory where you want "
                "to compare several small models and only one user will send requests.\n"
                "2. A frequently used image model that fits comfortably in available "
                "VRAM and must respond with low latency.\n"
                "3. A production API that handles users, permissions, billing, and "
                "business logic but relies on a very large model requiring specialized "
                "GPU serving infrastructure.\n\n"
                "For each scenario, discuss the main latency and memory consequence."
            ),

            "expected_output": (
                "Three serving-strategy choices with latency/memory reasoning."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "model-serving-strategy",
                "latency-memory-tradeoff",
                "architecture-decision",
            ],
        },

        {
            "id": "M01.L03.EX07",

            "title": "Design Safe Model-Service Monitoring",

            "lesson_code": "M01.L03",

            "section_id": "monitoring-middleware",

            "placement": "after_section",

            "description": (
                "Apply middleware monitoring while avoiding unnecessary collection of sensitive data."
            ),

            "instructions": (
                "Design a monitoring record for a production `/generate/text` endpoint.\n\n"
                "1. Include at least six useful fields such as request ID, endpoint, "
                "timestamp, latency, status code, and success flag.\n"
                "2. Identify which fields can be safely captured without reading the "
                "prompt body.\n"
                "3. Explain one risk of logging full prompts and model responses.\n"
                "4. Explain why an ephemeral local CSV file is insufficient as the "
                "only production log store.\n"
                "5. Draw where the middleware sits in the request/response path."
            ),

            "expected_output": (
                "A monitoring schema, privacy note, persistence explanation, and middleware-flow diagram."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "middleware",
                "observability",
                "privacy-aware-logging",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L03.QZ01",

        "title": "AI Integration and Model Serving — Knowledge Check",

        "lesson_code": "M01.L03",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L03.Q01",

                "section_id": "transformers-vs-rnns",

                "question": (
                    "What is the main sequence-modeling advantage of transformer "
                    "self-attention described in this lesson?"
                ),

                "options": [
                    "It eliminates the need for numerical representations",
                    "It can directly model relationships among tokens across the sequence",
                    "It forces all language generation to be deterministic",
                    "It stores the entire training dataset inside the prompt",
                ],

                "correct": 1,

                "explanation": (
                    "Self-attention lets the model represent relationships between "
                    "tokens across a sequence rather than relying only on a recurrent "
                    "state passed step-by-step."
                ),
            },

            {
                "id": "M01.L03.Q02",

                "section_id": "tokens-embeddings-position",

                "question": "What is the best description of a token embedding?",

                "options": [
                    "A dense numerical vector representation used by the model",
                    "The integer HTTP status code returned by FastAPI",
                    "A filename containing the original training text",
                    "A fixed position number with no learned information",
                ],

                "correct": 0,

                "explanation": (
                    "Embeddings are dense numerical vectors. Token IDs identify tokens, "
                    "while embeddings provide continuous representations the network can process."
                ),
            },

            {
                "id": "M01.L03.Q03",

                "section_id": "tokens-embeddings-position",

                "question": "Why is positional information needed in a transformer?",

                "options": [
                    "To tell the model which GPU brand is being used",
                    "To provide sequence-order information alongside token representations",
                    "To convert WAV files into MP4 files",
                    "To enforce API authorization",
                ],

                "correct": 1,

                "explanation": (
                    "Because transformer processing is not based on a recurrent token-by-token "
                    "state, position information helps preserve token order and sequence context."
                ),
            },

            {
                "id": "M01.L03.Q04",

                "section_id": "autoregressive-context",

                "question": "What does autoregressive text generation mean?",

                "options": [
                    "The model predicts a new token using the sequence available so far",
                    "The model generates every token independently with no context",
                    "The model can only classify text",
                    "The model always loads a new checkpoint after each token",
                ],

                "correct": 0,

                "explanation": (
                    "Autoregressive generation repeatedly predicts the next token based "
                    "on the existing sequence, appends it, and continues."
                ),
            },

            {
                "id": "M01.L03.Q05",

                "section_id": "serving-a-language-model",

                "question": (
                    "Which generation setting primarily limits how many new tokens "
                    "the model is allowed to produce?"
                ),

                "options": [
                    "top_p",
                    "temperature",
                    "max_new_tokens",
                    "device",
                ],

                "correct": 2,

                "explanation": (
                    "`max_new_tokens` places a cap on newly generated output tokens."
                ),
            },

            {
                "id": "M01.L03.Q06",

                "section_id": "streamlit-and-transformer-variants",

                "question": (
                    "Which transformer variant is most directly associated with "
                    "autoregressive conversational text generation in the lesson?"
                ),

                "options": [
                    "Encoder-only",
                    "Decoder-only",
                    "Image-only",
                    "Repository-only",
                ],

                "correct": 1,

                "explanation": (
                    "Decoder-only transformers predict subsequent tokens and are "
                    "well suited to text generation and conversational language modeling."
                ),
            },

            {
                "id": "M01.L03.Q07",

                "section_id": "audio-models",

                "question": (
                    "Why does the FastAPI audio example convert a generated waveform "
                    "into an encoded buffer before returning it?"
                ),

                "options": [
                    "Because a raw numerical waveform is not itself a standard playable HTTP audio file",
                    "Because FastAPI cannot return any binary data",
                    "Because audio models only produce text",
                    "Because WAV files cannot be held in memory",
                ],

                "correct": 0,

                "explanation": (
                    "The model output must be encoded into a media format such as WAV "
                    "and represented as bytes/buffer content a client can play."
                ),
            },

            {
                "id": "M01.L03.Q08",

                "section_id": "vision-models",

                "question": (
                    "What is the core generation intuition behind the Stable "
                    "Diffusion process described in the lesson?"
                ),

                "options": [
                    "Sort image pixels alphabetically",
                    "Iteratively refine a noisy latent representation under conditioning",
                    "Generate only deterministic vector graphics",
                    "Store one complete output image for every possible prompt",
                ],

                "correct": 1,

                "explanation": (
                    "The source's diffusion explanation centers on starting from a noisy "
                    "latent representation and iteratively denoising/refining it with conditioning."
                ),
            },

            {
                "id": "M01.L03.Q09",

                "section_id": "video-models",

                "question": "Why is video generation particularly resource intensive?",

                "options": [
                    "A video contains many frames that must be generated and kept coherent",
                    "Video never uses numeric tensors",
                    "FastAPI converts every frame into SQL",
                    "A video model cannot use a GPU",
                ],

                "correct": 0,

                "explanation": (
                    "Generating many high-dimensional frames while maintaining "
                    "temporal consistency requires substantial computation and memory."
                ),
            },

            {
                "id": "M01.L03.Q10",

                "section_id": "three-dimensional-models",

                "question": "What is a mesh?",

                "options": [
                    "A collection of connected vertices, edges, and faces describing a 3D surface",
                    "A list of HTTP response headers",
                    "A text tokenizer vocabulary",
                    "A type of middleware logger",
                ],

                "correct": 0,

                "explanation": (
                    "Meshes represent 3D geometry using vertices connected into edges "
                    "and polygonal faces."
                ),
            },

            {
                "id": "M01.L03.Q11",

                "section_id": "serving-strategies",

                "question": (
                    "Which serving strategy usually gives lower repeated-request latency "
                    "when one frequently used model fits comfortably in memory?"
                ),

                "options": [
                    "Reload the model from disk on every request",
                    "Preload the model during application lifespan",
                    "Delete the model before each generation",
                    "Convert the model into a CSV file",
                ],

                "correct": 1,

                "explanation": (
                    "Lifespan preloading pays the loading cost at startup and reuses "
                    "the resident model for subsequent requests."
                ),
            },

            {
                "id": "M01.L03.Q12",

                "section_id": "external-serving",

                "question": (
                    "What is one reason to place a specialized model server behind FastAPI?"
                ),

                "options": [
                    "To make route validation impossible",
                    "To separate high-resource inference concerns from application/business logic",
                    "To remove all network communication",
                    "To prevent the service from using GPUs",
                ],

                "correct": 1,

                "explanation": (
                    "A separate model server can specialize in inference while FastAPI "
                    "handles concerns such as users, validation, security, and coordination."
                ),
            },

            {
                "id": "M01.L03.Q13",

                "section_id": "monitoring-middleware",

                "question": "Why is middleware well suited to shared endpoint monitoring?",

                "options": [
                    "It can run around many request handlers without duplicating logging code in each route",
                    "It permanently increases model quality",
                    "It converts text models into image models",
                    "It replaces the need for persistent logs",
                ],

                "correct": 0,

                "explanation": (
                    "Middleware centralizes logic that should run before/after many "
                    "routes, such as assigning request IDs and measuring response time."
                ),
            },

            {
                "id": "M01.L03.Q14",

                "section_id": "architecture-decision",

                "type": "open",

                "question": (
                    "You must add a new generative model to a production FastAPI application. "
                    "Describe its expected input, native model output, HTTP encoding/response "
                    "format, serving strategy, and monitoring plan. Explain why each choice "
                    "fits the workload."
                ),
            },
        ],

        "passing_score": 70,
    },
}
