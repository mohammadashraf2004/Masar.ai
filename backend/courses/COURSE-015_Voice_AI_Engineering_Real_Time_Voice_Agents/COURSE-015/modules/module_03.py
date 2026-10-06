"""M01.L03 — Advanced Live Interactions: Vision, Tools, and Deployment.

One source chapter -> one complete learner-facing Lesson + inline Images
+ inline Exercises + lesson Quiz.

Source alignment:
- Chapter 4: Advanced Live Interactions: Video, Tools, and System Instructions
- Early Release draft; page numbers were not provided in the supplied source.

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L03"

MODULE_ORDER = 1

MODULE_TITLE = "Agent Foundations & Advanced Live Interaction"

MODULE_DESCRIPTION = (
    "Extend a real-time voice assistant into a multimodal, tool-using, mobile-ready "
    "assistant by adding system instructions, voice configuration, live visual input, "
    "periodic frame capture, function calling, external APIs, mobile-first interface "
    "design, containerization, and cloud deployment."
)

SOURCE_CHAPTER = 4

SOURCE_PAGES = "Early Release draft; page numbers not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Advanced Live Interactions: Vision, Tools, and Deployment",

    "slug": "agent-foundations-m01-l03",

    "description": (
        "Build on a real-time voice application by adding a configurable persona, "
        "camera and screen perception, efficient frame sampling, external tools with "
        "function calling, a mobile-first interface, and a cloud deployment path."
    ),

    "order": 3,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.0,

    "skill_tags": [
        "system-instructions",
        "voice-configuration",
        "multimodal-ai",
        "computer-vision",
        "frame-sampling",
        "screen-sharing",
        "function-calling",
        "tool-use",
        "weather-api",
        "mobile-ui",
        "docker",
        "cloud-run",
        "cloud-deployment",
    ],

    "prerequisite_ids": ["M01.L01", "M01.L02"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Advanced Live Interactions: Vision, Tools, and Deployment",

        "content": r"""
# Advanced Live Interactions: Vision, Tools, and Deployment

> **Lesson:** M01.L03  
> **Module:** Agent Foundations & Advanced Live Interaction  
> **Source alignment:** Chapter 4 of the supplied Early Release material.  
> This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain how system instructions and voice configuration influence the behavior and presentation of a live assistant.
- Separate persona design from task logic and tool behavior.
- Explain the "show, don't tell" value of adding camera or screen input to an assistant.
- Describe how webcam and screen-sharing streams are acquired in a browser.
- Explain why a live multimodal application often samples periodic frames instead of sending full-rate video.
- Trace a captured image from browser video to canvas, Base64 encoding, WebSocket transport, backend decoding, and model input.
- Explain the complete function-calling lifecycle from user intent to final response.
- Design a local tool handler and a clear function declaration.
- Explain why external APIs extend a model beyond static learned knowledge.
- Describe how system instructions can guide tool-use policy.
- Explain the difference between a developer test UI and a mobile-first product interface.
- Identify the purpose of responsive controls, contextual UI, camera switching, and touch-friendly design.
- Explain how Docker containers package an application and its dependencies.
- Explain the role of Cloud Build and Cloud Run in the source deployment flow.
- Trace the deployment of backend and frontend services and explain why the browser must use a secure `wss://` backend endpoint in production.
- Distinguish durable architectural concepts from provider-specific model names, API schemas, quotas, SDK objects, and deployment commands that should be re-verified before production use.

---

## 1. From fluent conversation to a capable assistant

In the previous lesson, we built the architecture for a real-time voice experience:

```text
Microphone
   ↓
Browser audio pipeline
   ↓
WebSocket
   ↓
Secure proxy
   ↓
Live model session
   ↓
Streaming audio response
   ↓
Speaker
```

That gives us a conversational system.

But conversation alone is not enough for a capable assistant.

A more useful system needs to:

```text
speak with a consistent character
+
perceive visual context
+
use tools to access live data or take actions
+
work well on a mobile device
+
run outside localhost
```

This lesson therefore expands the application in four directions:

```text
1. Character  -> system instructions + voice
2. Eyes       -> camera + screen input
3. Hands      -> tools + function calling
4. Mobility   -> mobile UI + cloud deployment
```

These additions are not isolated features.

Together they move the application from:

```text
real-time chatbot
```

toward:

```text
multimodal assistant
```

The source is careful to treat this as a foundation for a more complete agent, not the final form of a fully autonomous system with advanced memory and multi-step task execution.

---

## 2. Giving the assistant a personality

A live assistant can be technically correct and still feel generic.

The source separates "character" into two configuration layers:

1. **System instructions**
2. **Voice configuration**

### 2.1 System instructions

A system instruction is high-level guidance applied at the beginning of the interaction.

It can influence:

- tone,
- style,
- rules,
- priorities,
- boundaries,
- and task behavior.

Think of it as persistent guidance for the session.

For example:

```text
You are a friendly and helpful assistant.
Begin every response with a specified greeting.
```

The source uses an intentionally obvious greeting rule as a test.

Why?

Because a visible behavior makes it easy to verify whether the configuration is actually reaching the model.

This is a useful engineering technique:

> When testing a configuration path, choose a behavior whose success or failure is immediately observable.

### 2.2 Voice configuration

System instructions affect **what and how the assistant communicates conceptually**.

Voice configuration affects **how the generated speech sounds acoustically**.

The source chooses a named voice profile.

The exact voice name is provider-specific and may change.

The durable idea is:

```text
behavior/persona configuration
        +
speech voice configuration
        =
a more coherent user-facing character
```

### Persona is not just decoration

Persona can influence user experience in important ways.

For example, the same technical assistant can be configured as:

- formal,
- concise,
- friendly,
- teacher-like,
- supportive,
- highly technical,
- or task-focused.

However, persona should not override core product requirements such as:

- safety,
- accuracy,
- tool rules,
- or user control.

### Keep persona separate from business logic

A useful design is:

```text
System instructions:
    behavior, tone, high-level rules

Tools:
    executable capabilities

Application code:
    validation, permissions, side effects

UI:
    presentation and controls
```

This separation makes the system easier to maintain.

[[IMAGE_NEEDED: Persona configuration layers | A diagram showing System Instructions controlling tone/rules and Voice Configuration controlling speech sound, both feeding the same live assistant session | Learner should notice that character is produced by multiple configuration layers rather than one prompt alone]]

{{exercise:M01.L03.EX01}}

---

## 3. "Show, don't tell": why visual input matters

Text and voice require the user to describe the world.

Sometimes description is inefficient.

Imagine trying to explain:

- a complex error message,
- a damaged machine part,
- a handwritten equation,
- a chart,
- a phone screen,
- or an unfamiliar object.

A visual interface changes the interaction from:

```text
"Let me describe what I see."
```

to:

```text
"Look at this."
```

The source calls this the **"show, don't tell" paradigm**.

### Example: field technician

Without vision:

```text
"The valve is metallic, round, has two bolts..."
```

With vision:

```text
[show camera]
"Is this a standard or high-pressure valve?"
```

### Example: student

Without vision:

```text
"I wrote x squared minus 4x..."
```

With vision:

```text
[show handwritten equation]
"Where did I go wrong?"
```

### Example: tourist

Without vision:

```text
"I'm looking at a building with arches..."
```

With vision:

```text
[point camera]
"What can you tell me about this architecture?"
```

Visual input can reduce the translation burden on the user.

But it also introduces new engineering concerns:

- permissions,
- camera selection,
- frame capture,
- bandwidth,
- latency,
- cost,
- privacy,
- and visual quality.

---

## 4. Managing webcam and screen-sharing streams

The source adds a dedicated `MediaHandler` class.

This is an example of good separation of responsibilities.

Instead of putting all media logic into one large application file, the application creates one component responsible for visual media.

Conceptually:

```text
MediaHandler
├── initialize()
├── startWebcam()
├── startScreenShare()
├── stopAll()
├── switchCamera()
├── startFrameCapture()
└── stopFrameCapture()
```

### `initialize()`

Connects the media handler to the browser's preview element.

### `startWebcam()`

Uses the browser media API to request camera access.

Conceptually:

```javascript
navigator.mediaDevices.getUserMedia({
    video: true
})
```

### `startScreenShare()`

Uses screen-capture APIs to let the user choose:

- a screen,
- a window,
- or a browser tab.

Conceptually:

```javascript
navigator.mediaDevices.getDisplayMedia({
    video: true
})
```

### `stopAll()`

A correct cleanup method should:

1. stop every track in the current media stream,
2. end camera/screen capture,
3. hide or reset the preview,
4. stop any frame-capture timer.

This matters because simply hiding the `<video>` element does **not** necessarily stop the physical camera.

### `switchCamera()`

This is especially relevant on mobile devices where the user may want to switch between:

- front-facing camera,
- rear-facing camera.

The source prepares this capability for the mobile UI.

### Why use a dedicated class?

Because media state has its own complexity:

```text
permission state
active stream
current camera
screen share
preview element
capture timer
cleanup
```

Encapsulating this logic makes the application easier to reason about.

---

## 5. Why periodic frame capture beats full video for many assistant tasks

A camera may produce:

```text
30 FPS
60 FPS
or more
```

But a conversational assistant usually does not need every frame.

Suppose a user asks:

> What object am I holding?

If the scene changes slowly, sending 30 images every second may be wasteful.

The source therefore makes an architectural decision:

```text
show smooth video locally
but
send only periodic snapshots to the model
```

### Source strategy

The chapter uses:

```text
1 captured frame per second
```

That is a source-specific implementation choice.

The durable principle is **frame sampling**.

### Why sample?

Frame sampling can reduce:

- network bandwidth,
- token/media usage,
- provider cost,
- backend work,
- and model processing load.

It also gives the model a manageable stream of visual context.

### When sampling works well

Examples:

- identify an object,
- inspect a static chart,
- explain a screen,
- view a homework page,
- check a slowly changing environment.

### When sampling is weak

Examples:

- fast sports movement,
- gesture timing,
- frame-by-frame defects,
- rapid assembly-line events,
- precise motion tracking.

So the correct question is not:

> Should I always use 1 FPS?

The correct question is:

> What visual sampling rate preserves enough information for my task?

[[IMAGE_NEEDED: Local smooth video vs sampled AI frames | A live camera stream displayed smoothly to the user on the left, while only periodic snapshots (for example at t=0s, 1s, 2s) are sent to the AI on the right | Learner should notice that the user can see full-motion video while the model receives a much lower-rate visual stream]]

---

## 6. Capturing frames with a hidden canvas

How do we turn a live `<video>` stream into periodic images?

The source uses a hidden `<canvas>` element.

The flow is:

```text
video element
    ↓
draw current frame to canvas
    ↓
encode canvas as JPEG
    ↓
Base64 string
    ↓
send through WebSocket
```

### Step 1 — Set the cadence

A timer runs periodically.

Conceptually:

```javascript
setInterval(captureFrame, 1000);
```

In the source, this produces roughly one frame per second.

### Step 2 — Draw the frame

The current video image is drawn onto a canvas.

Conceptually:

```javascript
ctx.drawImage(video, 0, 0, width, height);
```

### Step 3 — Encode the image

The canvas becomes an encoded image:

```javascript
canvas.toDataURL("image/jpeg");
```

This produces a data URL containing Base64-encoded JPEG data.

### Step 4 — Hand the frame to the application

The media handler calls a callback.

The main application can then send a message such as:

```json
{
  "type": "image",
  "data": "..."
}
```

The exact client message schema is application-specific.

### Why canvas?

Canvas acts as a convenient conversion boundary:

```text
live browser media
       ↓
single still image
       ↓
portable encoded payload
```

It also gives the application a place to:

- resize,
- crop,
- reduce quality,
- annotate,
- or transform frames before transmission.

Those optimizations are not required by the source lesson, but the architecture makes them possible.

{{exercise:M01.L03.EX02}}

---

## 7. Extending the proxy from audio-only to multimodal

In the previous lesson, the proxy primarily handled audio.

Now it must distinguish multiple message types.

Conceptually:

```python
if message contains audio:
    decode audio
    send audio upstream

elif message contains image:
    decode image
    send image upstream
```

The proxy becomes a multimodal gateway.

### Audio path

```text
browser PCM
    ↓
Base64
    ↓
proxy decode
    ↓
audio blob
    ↓
live model
```

### Image path

```text
camera/screen frame
    ↓
JPEG
    ↓
Base64
    ↓
WebSocket
    ↓
proxy decode
    ↓
image/jpeg input
    ↓
live model
```

### Why keep the proxy simple?

The source treats it mostly as a transparent relay.

That is useful early in development because it keeps responsibilities clear:

```text
Browser:
    capture media

Proxy:
    authenticate + translate + relay

Model:
    reason over media
```

As the system grows, the proxy may also need:

- validation,
- logging,
- rate limiting,
- moderation,
- tool execution,
- authorization,
- or storage decisions.

But the basic multimodal transport path should remain understandable.

[[IMAGE_NEEDED: Multimodal proxy flow | Browser sends two labeled streams, Audio and JPEG Frames, into one backend proxy; proxy decodes each and forwards both into one live model session | Learner should see that one session can receive multiple input types through the same application architecture]]

---

## 8. Testing visual reasoning

The source uses a simple checkpoint:

1. Start the live audio session.
2. Activate the webcam.
3. Allow camera access.
4. Show an object.
5. Ask a visual question.
6. Stop the camera.

Example prompts include:

```text
"What do you see?"
"Describe the object in front of me."
"What color is the mug?"
```

### Why this checkpoint is useful

It validates multiple layers at once:

```text
UI button
-> browser permission
-> camera stream
-> preview
-> capture timer
-> JPEG encoding
-> WebSocket
-> proxy decoding
-> model input
-> audio response
```

If the assistant answers correctly about the visible object, the whole visual pipeline is likely working.

### Better debugging strategy

If it fails, isolate the pipeline.

Check:

```text
1. Does camera preview work?
2. Are frames being captured?
3. Is Base64 data being produced?
4. Is browser sending image messages?
5. Is proxy receiving them?
6. Is proxy decoding correctly?
7. Is upstream session accepting image input?
8. Is the model responding to the visual context?
```

Again, good debugging follows the data path.

---

## 9. Giving the assistant "hands": tools and function calling

Vision lets the assistant perceive more of the world.

But perception is still passive.

To interact with live systems or perform tasks, the assistant needs **tools**.

A tool can connect the model to:

- a weather service,
- a calendar,
- a database,
- a booking system,
- a shopping cart,
- a smart-home device,
- or custom application logic.

The chapter uses weather as the teaching example.

### Why weather is a good tool example

A model's training knowledge is not a reliable source for:

```text
current weather right now
```

That information must come from a live data source.

So weather clearly demonstrates the difference between:

```text
model knowledge
```

and:

```text
external real-time data
```

### Function calling mental model

A user asks:

```text
"What's the weather in London?"
```

The model recognizes:

```text
I need current external data.
```

Then:

```text
1. Identify tool
2. Extract city
3. Request function call
4. Host executes real function
5. Tool result returns
6. Model synthesizes response
```

This is the same core execution loop introduced in Lesson M01.L01, now integrated into a live multimodal assistant.

---

## 10. The complete function-calling lifecycle

Let's examine the lifecycle carefully.

### Step 1 — Intent recognition

The model interprets:

```text
"How is the weather in Tokyo today?"
```

and recognizes that the request depends on current weather data.

### Step 2 — Tool selection

The model inspects available tool declarations and identifies:

```text
get_weather
```

### Step 3 — Parameter extraction

The model extracts:

```json
{
  "city": "Tokyo"
}
```

### Step 4 — Function call emission

The model does **not** directly call the weather provider itself in the source architecture.

Instead, it produces a structured tool request.

Conceptually:

```json
{
  "name": "get_weather",
  "args": {
    "city": "Tokyo"
  }
}
```

### Step 5 — Host execution

The backend receives the request and runs application code.

That code calls the external weather API.

Example result:

```json
{
  "city": "Tokyo",
  "temperature": 22,
  "description": "clear sky"
}
```

### Step 6 — Tool result returned to model

The backend packages the result in the provider's expected tool-response message.

### Step 7 — Response synthesis

The model receives the result and produces a user-facing answer.

For example:

```text
"The current weather in Tokyo is 22°C with clear skies."
```

### The execution boundary

The most important concept remains:

> The model selects and requests a tool. The application controls actual execution.

This allows the host application to add:

- input validation,
- authorization,
- rate limits,
- logging,
- user confirmation,
- retries,
- and safety checks.

[[IMAGE_NEEDED: Live function-calling loop | User asks weather -> live model chooses get_weather(city) -> backend tool handler calls external weather API -> API result returns to backend -> tool response returns to model -> spoken answer goes back to user | Learner should notice that external execution happens in backend code, not inside the model]]

---

## 11. A local architecture for tool execution

The source creates:

```text
backend/tool_handler.py
```

Its purpose is simple:

```text
store real tool implementations
```

This keeps tool logic separate from the WebSocket proxy.

### Architecture

```text
proxy.py
   |
   | receives tool request
   v
tool_handler.py
   |
   | calls external service
   v
Weather API
```

This is a useful learning architecture because it is:

- simple,
- local,
- easy to debug,
- fast to modify,
- and free from separate service deployment complexity.

### Separation of responsibilities

A good structure is:

```text
proxy.py
    transport/session/tool routing

tool_handler.py
    actual tool implementations

system-instructions.txt
    high-level behavior rules

.env
    secrets/configuration
```

This is cleaner than placing every concern inside one file.

### Example tool shape

Conceptually:

```python
def get_weather(city: str) -> dict:
    # read API key
    # call weather API
    # parse provider response
    # return clean application data
    ...
```

The key is that the function returns a stable internal structure.

Do not force the model to understand a huge raw provider response if the application only needs:

```json
{
  "city": "...",
  "temperature": "...",
  "description": "..."
}
```

This is an important tool-design principle:

> Tool outputs should be as structured and task-relevant as practical.

---

## 12. Teaching the model about a tool

Writing a Python function is not enough.

The model needs a declaration describing the function.

A declaration should communicate:

- name,
- purpose,
- parameters,
- types,
- required fields.

Conceptually:

```json
{
  "name": "get_weather",
  "description": "Get current weather information for a city.",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "City to retrieve weather for."
      }
    },
    "required": ["city"]
  }
}
```

### Why descriptions matter

The model uses the description to infer:

```text
when should I use this capability?
```

Poor declaration:

```text
name: thing
description: does stuff
```

Better declaration:

```text
name: get_weather
description: Returns current weather conditions for a requested city.
```

Clear declarations improve tool selection.

### System instructions can add policy

The source also adds a rule similar to:

```text
When asked about weather, use the get_weather tool.
```

This demonstrates two layers:

```text
Tool declaration:
    what the tool can do

System instruction:
    behavioral rule about when/how to use it
```

These should not be confused.

The declaration defines the interface.

The system instruction defines policy or behavior.

---

## 13. Handling a tool request inside the live proxy

The model can now request a tool.

The proxy must detect that event.

Conceptually:

```python
if response.tool_call:
    ...
```

Then:

```text
1. inspect requested function
2. read arguments
3. call local implementation
4. get result
5. wrap result in tool-response format
6. send result back to live session
```

The source uses provider-specific response objects.

Those exact class names should be re-verified for the current SDK.

The durable control flow is:

```python
tool_request = model_response.tool_call

result = execute_tool(
    tool_request.name,
    tool_request.args
)

send_tool_result_to_model(result)
```

### Add validation in real systems

A production implementation should not blindly trust model-generated arguments.

For weather:

```text
city must be a string
city must not be empty
API key must exist
external request must have timeout
response should be checked
```

For higher-risk tools, add stronger controls.

Examples:

```text
send_email(...)
delete_file(...)
transfer_money(...)
unlock_door(...)
```

Such tools may require:

- permissions,
- policy checks,
- explicit confirmation,
- or human review.

{{exercise:M01.L03.EX03}}

---

## 14. External APIs: extending the assistant beyond static knowledge

The source integrates a weather provider.

The important lesson is not the brand of weather service.

The important lesson is:

```text
model reasoning
+
external live API
=
current task-specific capability
```

### Secure key storage

The source stores the API key in `.env`.

That is preferable to hard-coding it into source files.

Conceptually:

```text
OPENWEATHER_API_KEY=...
```

The durable rule:

> Secrets should be injected through secure configuration, not embedded in client-side code or committed into source control.

### Tool execution flow

```text
get_weather("Berlin")
    ↓
HTTP request to weather service
    ↓
provider JSON
    ↓
application extracts useful fields
    ↓
clean tool result
```

### About source-specific quotas

The chapter mentions specific free-tier limits.

Those are time-sensitive provider details.

They should be treated as source-aligned information, not permanent architecture.

Always re-check:

- current pricing,
- authentication rules,
- quotas,
- terms,
- and endpoint formats

before production use.

---

## 15. From prototype to product

A working prototype proves the architecture.

It does not automatically create a good product.

The source identifies two remaining limitations:

```text
1. developer-oriented interface
2. application only runs on localhost
```

So the next transformation is:

```text
prototype
   ↓
mobile-first interface
   ↓
cloud deployment
   ↓
portable product
```

This is a key engineering transition.

The challenge changes from:

> Can the feature work?

to:

> Can a real user use it comfortably and reliably?

---

## 16. Designing a mobile-first assistant

The source creates a new mobile-oriented page rather than keeping the developer test layout.

Why?

Because a phone imposes different interaction constraints.

### 16.1 Streamlined start

Instead of multiple setup controls, the user begins with one clear action.

Conceptually:

```text
[ Play ]
```

This can:

- establish the connection,
- start the session,
- activate microphone capture.

Fewer initial decisions reduce friction.

### 16.2 Touch-friendly controls

Phone users need:

- large hit targets,
- good spacing,
- clear icons,
- minimal precision requirements.

A tiny desktop button can be frustrating on touchscreens.

### 16.3 Contextual UI

Only show controls when they are useful.

For example:

```text
camera inactive:
    no switch-camera control

camera active on phone:
    show switch-camera control
```

This keeps the interface simpler.

### 16.4 Responsive layout

The page should adapt across:

```text
phone portrait
phone landscape
tablet
desktop
```

The most important interaction elements should remain visible and accessible.

### 16.5 Media-first design

In a multimodal assistant, the most important screen regions may be:

- camera preview,
- conversation state,
- microphone controls,
- stop control,
- and tool/activity feedback.

The UI should reflect the task, not the internal architecture.

[[IMAGE_NEEDED: Mobile-first assistant UI layout | A phone mockup with a large start/play button before session start, then large circular stop/mic/camera controls after connection, a prominent video preview area, and contextual switch-camera control | Learner should notice reduced clutter, large touch targets, and state-dependent controls]]

---

## 17. UI state should mirror application state

A polished interface is not just styling.

The UI must accurately represent the live system state.

Possible states include:

```text
Disconnected
Connecting
Listening
AI speaking
Microphone muted
Camera active
Screen share active
Tool executing
Error
Stopped
```

If the UI state and application state disagree, users lose trust.

Example:

```text
UI says "Listening"
but microphone track is stopped
```

That is a serious usability bug.

### Contextual controls

A strong design maps state to controls.

For example:

```text
Disconnected
    -> show Connect

Connected
    -> show Stop + Mic + Camera

Camera active
    -> show Stop Camera
    -> maybe show Switch Camera
```

This is essentially a state machine expressed through UI.

The same state-machine thinking from the hot-mic lesson applies here.

---

## 18. Why deploy the assistant?

Localhost is useful for development.

But it has obvious limitations:

- only the local machine can access it easily,
- mobile testing is harder,
- external users cannot use it,
- secure public WebSocket behavior is not represented,
- production infrastructure concerns remain untested.

Deployment changes the environment from:

```text
private development system
```

to:

```text
public networked application
```

That adds new concerns:

- HTTPS/WSS,
- scaling,
- container startup,
- cloud permissions,
- environment configuration,
- network timeouts,
- cost,
- observability,
- and security.

---

## 19. Serverless containers and Cloud Run

The source deploys the application using Google Cloud Run.

The chapter describes Cloud Run as a serverless container platform.

Let's unpack those terms.

### Serverless

"Serverless" does **not** mean no physical servers exist.

It means the application developer does not directly manage the underlying servers in the traditional way.

The platform handles much of the infrastructure.

The developer focuses more on:

```text
application
container
configuration
deployment
```

### Container

A container packages:

- application code,
- runtime,
- dependencies,
- configuration expectations,
- startup command.

This addresses the classic problem:

```text
"It works on my machine."
```

because the runtime environment becomes more reproducible.

### Source advantages

The chapter highlights:

- scaling to zero,
- automatic scaling,
- a secure public URL.

These are platform capabilities described by the source and should still be checked against the current service behavior and pricing before production planning.

---

## 20. Docker: packaging the application

A `Dockerfile` is a recipe for building a container image.

Conceptually:

```text
1. Choose base runtime
2. Copy application
3. Install dependencies
4. Configure environment
5. Define startup command
```

Example mental model:

```dockerfile
FROM python:...

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "server.py"]
```

The exact file depends on the application.

### Why containers matter here

We have a frontend service and a backend service.

Each may require:

- different code,
- different startup command,
- different environment variables,
- different network configuration.

Containers provide a standard deployment unit for both.

[[IMAGE_NEEDED: From source code to running cloud service | Source files + requirements + Dockerfile -> container image -> registry -> Cloud Run service -> public HTTPS/WSS endpoint | Learner should understand that Docker packages the app while Cloud Run runs the resulting container]]

---

## 21. Automating deployment with Cloud Build

The source includes `cloudbuild.yaml` files.

These act as build/deployment instructions.

The automated flow is:

```text
source code
    ↓
Cloud Build
    ↓
read Dockerfile
    ↓
build container image
    ↓
push image to registry
    ↓
deploy image to Cloud Run
```

This reduces a multi-step manual process into a repeatable command.

### Why repeatability matters

Manual deployment is error-prone.

Automation provides:

- consistent steps,
- reproducibility,
- less human variation,
- easier redeployment.

A good deployment pipeline should make the correct process the easy process.

---

## 22. Deploying the backend first

The source deploys the backend before the frontend.

Why?

Because the frontend needs to know the backend's public address.

So the dependency is:

```text
deploy backend
     ↓
receive backend URL
     ↓
configure frontend
     ↓
deploy frontend
```

### Backend deployment result

The backend gets a public service URL.

Conceptually:

```text
https://backend-service....run.app
```

The exact URL format is provider-generated.

### WebSocket protocol

The browser needs a WebSocket endpoint.

In secure production environments:

```text
https://
```

for ordinary HTTP becomes:

```text
wss://
```

for secure WebSockets.

This is an important distinction.

Development:

```text
ws://localhost:8081
```

Production:

```text
wss://public-backend.example
```

---

## 23. Deploying the frontend with backend configuration

Once the backend exists, the frontend build can receive the backend WebSocket URL.

The source uses a build substitution.

Conceptually:

```text
_BACKEND_URL = wss://...
```

The frontend is then built with the correct production endpoint.

This is better than manually editing code for each environment.

A more general configuration pattern is:

```text
Development:
    ws://localhost:8081

Production:
    wss://public-backend
```

### Environment-specific configuration

This is a broad software engineering lesson:

> Values that change across environments should be configuration, not hard-coded application logic.

Examples:

- API endpoints,
- feature flags,
- logging levels,
- model names,
- service URLs.

---

## 24. The complete product architecture

We can now connect the entire lesson.

### Input side

```text
Voice
Camera
Screen Share
Text
   ↓
Browser UI
   ↓
Audio processing + frame sampling
   ↓
Secure WebSocket
```

### Backend

```text
Cloud-hosted proxy
├── authentication
├── session forwarding
├── multimodal transport
├── tool routing
└── tool execution
```

### External systems

```text
Live model service
Weather API
Other future tools
```

### Output side

```text
streamed audio
visual UI state
tool status
text/status messages
```

### Deployment

```text
Frontend container -> public frontend service
Backend container  -> public backend service
```

### User experience

```text
mobile browser
   ↓
tap play
   ↓
speak naturally
   ↓
show camera or screen
   ↓
ask for live external information
   ↓
assistant sees, reasons, calls tools, and responds
```

[[IMAGE_NEEDED: End-to-end advanced assistant architecture | Mobile browser with microphone/camera on left -> secure frontend connection -> cloud backend proxy in center -> live multimodal model plus external weather/tool APIs on right; show tool-call loop and streamed response returning to phone | Learner should see how persona, vision, tools, UI, and deployment fit into one coherent system]]

{{exercise:M01.L03.EX04}}

---

## 25. Important production boundaries

The chapter is an Early Release tutorial.

Many implementation details are provider-specific and time-sensitive.

Before production use, verify the current documentation for:

- model names,
- available voice names,
- supported languages,
- live-session configuration,
- image input format,
- frame-rate guidance,
- SDK object names,
- function-calling schema,
- tool-response classes,
- authentication methods,
- weather API endpoint and pricing,
- Cloud Run pricing and scaling behavior,
- WebSocket timeout limits,
- container requirements,
- Cloud Build syntax,
- browser media compatibility,
- mobile permission behavior.

### Security boundaries

Do not expose:

- provider secrets,
- weather API keys,
- cloud service credentials

in frontend code.

Keep secrets in trusted server-side configuration.

### Tool security

Every tool should define:

```text
allowed inputs
validation rules
timeouts
error handling
authorization
side-effect policy
```

### Visual privacy

Camera and screen sharing can expose:

- faces,
- documents,
- passwords,
- notifications,
- personal spaces,
- company information.

The user should always have:

- explicit activation,
- visible active state,
- clear stop controls,
- understandable retention behavior.

### Deployment reliability

Add:

- health checks,
- structured logs,
- connection metrics,
- retry strategy,
- error UI,
- reconnect behavior,
- environment-specific configuration.

### Cost awareness

Real-time sessions can consume:

- model usage,
- audio bandwidth,
- image/media processing,
- external API calls,
- cloud compute.

Measure usage rather than assuming the prototype cost model will remain valid at scale.

---

## Important misconceptions

### Misconception 1

> "System instructions and voice selection are the same thing."

### Why this is wrong

System instructions guide behavior and response style. Voice configuration changes the acoustic presentation of speech.

---

### Misconception 2

> "If I display live video, I must send every video frame to the model."

### Why this is wrong

For many assistant tasks, periodic frame sampling provides sufficient visual context with much lower bandwidth and processing cost.

---

### Misconception 3

> "The browser video preview and the model's visual input must use the same frame rate."

### Why this is wrong

The user can see smooth full-motion preview while the application sends only selected snapshots to the model.

---

### Misconception 4

> "Writing `get_weather()` automatically makes the model know the function exists."

### Why this is wrong

The model needs a tool/function declaration describing the capability and its parameters.

---

### Misconception 5

> "The model directly calls the external weather service."

### Why this is wrong

In the source architecture, the model requests the function. Backend application code executes the function and returns the result.

---

### Misconception 6

> "System instructions are enough to secure tool execution."

### Why this is wrong

Application-side validation and authorization are still required. Instructions influence model behavior but do not replace code-level safeguards.

---

### Misconception 7

> "A working developer page is already a product."

### Why this is wrong

A production interface requires usability, responsive layout, state clarity, error handling, and device-appropriate interaction design.

---

### Misconception 8

> "Serverless means there are no servers."

### Why this is wrong

Servers still exist; the cloud platform manages much of the underlying infrastructure on your behalf.

---

### Misconception 9

> "Docker and Cloud Run are the same thing."

### Why this is wrong

Docker defines/containerizes the application. Cloud Run is a platform that can run deployed containers.

---

### Misconception 10

> "Provider-specific names and quotas from a tutorial are permanent."

### Why this is wrong

Model IDs, voice names, quotas, pricing, API schemas, and SDK methods can change and should be re-verified.

---

## Key terminology

| Term | Meaning |
|---|---|
| System instruction | High-level session guidance that influences model behavior |
| Voice configuration | Settings that control the generated speech voice |
| Persona | Consistent behavioral and stylistic character of the assistant |
| Webcam stream | Live camera media acquired through browser media APIs |
| Screen sharing | Live capture of a display, application window, or browser tab |
| MediaHandler | Application component responsible for media acquisition and lifecycle |
| Frame sampling | Sending periodic still frames rather than full-rate video |
| Canvas | Browser drawing surface used here to capture a video frame as an image |
| Data URL | Text representation that can contain Base64-encoded image data |
| Multimodal proxy | Backend gateway that relays multiple media types such as audio and images |
| Tool | External capability available to the assistant |
| Function declaration | Structured description telling the model how a tool can be requested |
| Function calling | Mechanism where the model emits a structured request for an application function |
| Tool handler | Application module containing actual executable tool implementations |
| Tool response | Structured result sent back to the model after host-side execution |
| External API | Service outside the model used to obtain current data or perform actions |
| Mobile-first | Designing primarily for small-screen, touch-based interaction |
| Contextual UI | Interface controls that appear or change according to application state |
| Container | Packaged application and dependencies in a standardized runtime unit |
| Dockerfile | Recipe describing how to build a container image |
| Cloud Build | Build automation service used in the source deployment path |
| Cloud Run | Serverless container platform used by the source |
| `wss://` | Secure WebSocket protocol |
| Build substitution | Deployment-time value injected into a build configuration |

---

## Self-check

Before continuing, make sure you can answer:

1. What is the difference between system instructions and voice configuration?
2. Why does an obvious greeting rule make a useful configuration test?
3. What does the "show, don't tell" interaction model improve?
4. Why does the source use a dedicated `MediaHandler` class?
5. Why should stopping a video stream stop the underlying media tracks?
6. Why might 1 sampled frame per second be enough for some tasks but not others?
7. What role does a hidden canvas play in the visual pipeline?
8. Trace an image frame from webcam to model.
9. What changes are required in the proxy to support both audio and image messages?
10. Why is a live weather request a good demonstration of function calling?
11. What is the difference between the real Python tool implementation and the model's function declaration?
12. Who actually executes the weather function?
13. Why can a system instruction require the model to use a tool but still not replace backend validation?
14. Why is a clean internal tool result better than returning the raw external API payload?
15. What makes a mobile-first interface different from a developer test UI?
16. Why is contextual UI useful on a small screen?
17. What problem does containerization solve?
18. What role does Cloud Build play in the deployment flow?
19. Why is the backend deployed before the frontend in the source workflow?
20. Why does the production frontend need `wss://` rather than a localhost `ws://` URL?
21. Which parts of this lesson are durable architecture and which are provider-specific implementation details?
22. Which privacy controls should surround camera and screen-sharing features?

---

## Retain this idea

**A capable live assistant is built by composing clear layers: system instructions shape behavior, media capture expands perception, frame sampling makes vision practical, function calling connects reasoning to external tools, a mobile-first UI turns a prototype into a usable product, and containerized cloud deployment makes the system portable. The durable architecture matters more than any one provider-specific model name, SDK object, voice, or deployment command.**
""".strip(),

        "estimated_minutes": 240,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "from-voice-to-assistant", "title": "From Fluent Conversation to a Capable Assistant", "order": 1},
            {"id": "persona", "title": "Giving the Assistant a Personality", "order": 2},
            {"id": "show-dont-tell", "title": "Show, Don't Tell: Why Visual Input Matters", "order": 3},
            {"id": "media-handler", "title": "Managing Webcam and Screen-Sharing Streams", "order": 4},
            {"id": "frame-sampling", "title": "Why Periodic Frame Capture Beats Full Video", "order": 5},
            {"id": "canvas-pipeline", "title": "Capturing Frames with a Hidden Canvas", "order": 6},
            {"id": "multimodal-proxy", "title": "Extending the Proxy from Audio-Only to Multimodal", "order": 7},
            {"id": "vision-checkpoint", "title": "Testing Visual Reasoning", "order": 8},
            {"id": "tools-introduction", "title": "Giving the Assistant Hands", "order": 9},
            {"id": "function-calling-loop", "title": "The Complete Function-Calling Lifecycle", "order": 10},
            {"id": "tool-handler", "title": "A Local Architecture for Tool Execution", "order": 11},
            {"id": "tool-declaration", "title": "Teaching the Model About a Tool", "order": 12},
            {"id": "tool-execution", "title": "Handling a Tool Request Inside the Live Proxy", "order": 13},
            {"id": "weather-tool", "title": "External APIs and Live Data", "order": 14},
            {"id": "prototype-to-product", "title": "From Prototype to Product", "order": 15},
            {"id": "mobile-first", "title": "Designing a Mobile-First Assistant", "order": 16},
            {"id": "mobile-state", "title": "UI State Should Mirror Application State", "order": 17},
            {"id": "deployment-intro", "title": "Why Deploy the Assistant?", "order": 18},
            {"id": "cloud-run", "title": "Serverless Containers and Cloud Run", "order": 19},
            {"id": "docker", "title": "Docker: Packaging the Application", "order": 20},
            {"id": "cloud-build", "title": "Automating Deployment with Cloud Build", "order": 21},
            {"id": "deploy-backend", "title": "Deploying the Backend First", "order": 22},
            {"id": "deploy-frontend", "title": "Deploying the Frontend with Backend Configuration", "order": 23},
            {"id": "full-product", "title": "The Complete Product Architecture", "order": 24},
            {"id": "production-boundaries", "title": "Important Production Boundaries", "order": 25},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L03.EX01",

            "title": "Design a Testable Assistant Persona",

            "lesson_code": "M01.L03",

            "section_id": "persona",

            "placement": "after_section",

            "description": (
                "Practice separating behavioral instructions from voice presentation."
            ),

            "instructions": (
                "1. Write a short system instruction for an AI study assistant.\n"
                "2. Include one obvious behavior that makes it easy to verify the instruction is active.\n"
                "3. Specify the desired tone in words without relying on a particular provider voice name.\n"
                "4. Explain which part belongs in system instructions and which part belongs in voice configuration.\n"
                "5. Add one rule that should remain enforced by application logic rather than persona text."
            ),

            "expected_output": (
                "A short persona specification containing system behavior, voice-style intent, "
                "a visible test behavior, and one application-level safeguard."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "system-instructions",
                "persona-design",
                "separation-of-concerns",
            ],
        },

        {
            "id": "M01.L03.EX02",

            "title": "Design a Frame-Sampling Strategy",

            "lesson_code": "M01.L03",

            "section_id": "canvas-pipeline",

            "placement": "after_section",

            "description": (
                "Choose an appropriate visual sampling strategy for different multimodal tasks."
            ),

            "instructions": (
                "For each scenario, choose a low, medium, or high visual sampling rate and explain why:\n"
                "1. Reading a static dashboard.\n"
                "2. Identifying an object held in front of a camera.\n"
                "3. Analyzing a fast tennis serve.\n"
                "4. Helping a user navigate a slowly changing settings screen.\n"
                "Then draw the browser pipeline Video -> Canvas -> JPEG -> Base64 -> WebSocket."
            ),

            "expected_output": (
                "A four-row decision table plus a diagram of the frame-capture pipeline."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "frame-sampling",
                "multimodal-design",
                "bandwidth-tradeoffs",
                "browser-media",
            ],
        },

        {
            "id": "M01.L03.EX03",

            "title": "Design a Safe Tool-Calling Loop",

            "lesson_code": "M01.L03",

            "section_id": "tool-execution",

            "placement": "after_section",

            "description": (
                "Apply the complete function-calling flow while adding application-side validation."
            ),

            "instructions": (
                "Design a `get_exchange_rate(base_currency, quote_currency)` tool.\n"
                "1. Write a concise function declaration.\n"
                "2. Define the real backend function signature.\n"
                "3. Add validation for currency codes.\n"
                "4. Add a timeout/error-handling rule for the external API.\n"
                "5. Show the model request -> backend execution -> tool result -> final answer flow.\n"
                "6. Explain why system instructions alone cannot replace validation."
            ),

            "expected_output": (
                "A tool declaration, backend function skeleton, validation rules, and "
                "a step-by-step execution flow."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "function-calling",
                "tool-design",
                "validation",
                "external-apis",
            ],
        },

        {
            "id": "M01.L03.EX04",

            "title": "Architect the Deployable Multimodal Assistant",

            "lesson_code": "M01.L03",

            "section_id": "full-product",

            "placement": "after_section",

            "description": (
                "Combine persona, vision, tools, mobile UI, and deployment into one complete architecture."
            ),

            "instructions": (
                "Design a mobile assistant that can answer spoken questions, inspect camera frames, "
                "and use two external tools.\n"
                "1. Define its system instructions.\n"
                "2. Define its browser media inputs.\n"
                "3. Choose a frame-sampling strategy.\n"
                "4. Define two tools and where they execute.\n"
                "5. Draw Browser -> Backend -> Model/Tools data flows.\n"
                "6. Define mobile UI states.\n"
                "7. Explain how frontend and backend are containerized/deployed.\n"
                "8. Add privacy, secret-management, and reconnect rules.\n"
                "9. Mark which configuration values must be environment-specific."
            ),

            "expected_output": (
                "A one- to two-page architecture specification with a system diagram, "
                "tool interfaces, UI states, deployment plan, and production safeguards."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "multimodal-architecture",
                "tool-use",
                "mobile-ui",
                "cloud-deployment",
                "security",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L03.QZ01",

        "title": "Advanced Live Interactions — Knowledge Check",

        "lesson_code": "M01.L03",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L03.Q01",
                "section_id": "persona",
                "question": (
                    "Which statement best describes the difference between system instructions and voice configuration?"
                ),
                "options": [
                    "System instructions influence behavior, while voice configuration affects speech presentation",
                    "They are two names for the same setting",
                    "Voice configuration defines tool permissions",
                    "System instructions only change microphone hardware",
                ],
                "correct": 0,
                "explanation": (
                    "System instructions guide model behavior and style; voice settings control how generated speech sounds."
                ),
            },

            {
                "id": "M01.L03.Q02",
                "section_id": "show-dont-tell",
                "question": (
                    "What is the main benefit of the 'show, don't tell' interaction model?"
                ),
                "options": [
                    "It removes the need for user permissions",
                    "It lets visual context replace lengthy verbal descriptions when appropriate",
                    "It guarantees perfect visual recognition",
                    "It eliminates network usage",
                ],
                "correct": 1,
                "explanation": (
                    "Visual input can communicate spatial and object information more directly than a long spoken description."
                ),
            },

            {
                "id": "M01.L03.Q03",
                "section_id": "frame-sampling",
                "question": (
                    "Why does the source send periodic visual frames instead of every camera frame?"
                ),
                "options": [
                    "To reduce bandwidth and processing while keeping enough visual context for many tasks",
                    "Because browsers cannot display full video",
                    "Because image models can only read one image per session",
                    "To disable screen sharing",
                ],
                "correct": 0,
                "explanation": (
                    "Frame sampling is an efficiency trade-off: it lowers bandwidth and model load for tasks that do not require high-speed motion analysis."
                ),
            },

            {
                "id": "M01.L03.Q04",
                "section_id": "canvas-pipeline",
                "question": (
                    "What role does the hidden canvas play in the source's video pipeline?"
                ),
                "options": [
                    "It stores API keys",
                    "It captures a still frame from the video and encodes it as an image",
                    "It runs the weather API",
                    "It replaces the WebSocket proxy",
                ],
                "correct": 1,
                "explanation": (
                    "The canvas provides a still-image conversion point from the live video element."
                ),
            },

            {
                "id": "M01.L03.Q05",
                "section_id": "function-calling-loop",
                "question": (
                    "When the model decides it needs current weather data, what happens first?"
                ),
                "options": [
                    "The model secretly executes the provider API itself",
                    "The model emits a structured request for the declared weather tool",
                    "The browser reloads the page",
                    "The camera turns off",
                ],
                "correct": 1,
                "explanation": (
                    "In the source architecture, the model requests a tool call and the backend executes the real function."
                ),
            },

            {
                "id": "M01.L03.Q06",
                "section_id": "tool-handler",
                "question": (
                    "Why is `tool_handler.py` useful?"
                ),
                "options": [
                    "It separates executable tool logic from session transport code",
                    "It replaces the model",
                    "It stores frontend CSS",
                    "It makes validation unnecessary",
                ],
                "correct": 0,
                "explanation": (
                    "Separating transport/session code from tool implementations keeps responsibilities clear and easier to maintain."
                ),
            },

            {
                "id": "M01.L03.Q07",
                "section_id": "tool-declaration",
                "question": (
                    "What information does a good function declaration provide to the model?"
                ),
                "options": [
                    "Only the source file path",
                    "Name, purpose, parameters, types, and required fields",
                    "The user's cloud password",
                    "The browser's entire JavaScript runtime",
                ],
                "correct": 1,
                "explanation": (
                    "The declaration acts as a structured interface description that helps the model decide when and how to request the tool."
                ),
            },

            {
                "id": "M01.L03.Q08",
                "section_id": "tool-execution",
                "question": (
                    "Why must backend validation remain even if the system instruction says when to use a tool?"
                ),
                "options": [
                    "Because instructions do not enforce application-level security or input correctness",
                    "Because tools cannot accept parameters",
                    "Because system instructions disable JSON",
                    "Because external APIs never fail",
                ],
                "correct": 0,
                "explanation": (
                    "Model instructions influence behavior, but the host application remains responsible for secure execution."
                ),
            },

            {
                "id": "M01.L03.Q09",
                "section_id": "mobile-first",
                "question": (
                    "Which design choice best reflects a mobile-first interface?"
                ),
                "options": [
                    "Small text-only controls packed closely together",
                    "Large touch-friendly controls and contextual actions",
                    "Showing every possible control at all times",
                    "Requiring a desktop mouse",
                ],
                "correct": 1,
                "explanation": (
                    "Mobile-first interfaces prioritize large touch targets, simple flows, and controls relevant to the current state."
                ),
            },

            {
                "id": "M01.L03.Q10",
                "section_id": "docker",
                "question": (
                    "What problem does containerization primarily address in this lesson?"
                ),
                "options": [
                    "It packages code and dependencies into a consistent deployable unit",
                    "It automatically writes system instructions",
                    "It replaces camera permissions",
                    "It acts as a weather API",
                ],
                "correct": 0,
                "explanation": (
                    "Containers make the runtime environment reproducible by packaging the application with its dependencies."
                ),
            },

            {
                "id": "M01.L03.Q11",
                "section_id": "deploy-frontend",
                "question": (
                    "Why does the production frontend need the deployed backend's WebSocket URL?"
                ),
                "options": [
                    "So browser clients know where to establish the live connection",
                    "So Docker can access the camera directly",
                    "So the weather API can edit CSS",
                    "So Cloud Run can remove authentication",
                ],
                "correct": 0,
                "explanation": (
                    "The frontend needs an environment-specific endpoint for its live backend connection."
                ),
            },

            {
                "id": "M01.L03.Q12",
                "section_id": "production-boundaries",
                "question": (
                    "Which detail should be treated as source-specific rather than a timeless architectural rule?"
                ),
                "options": [
                    "Separating secrets from frontend code",
                    "Using validation before executing tools",
                    "A specific provider model name, voice name, quota, or SDK class",
                    "Keeping application state visible in the UI",
                ],
                "correct": 2,
                "explanation": (
                    "Provider-specific identifiers and limits can change; the surrounding architecture and safety principles are more durable."
                ),
            },

            {
                "id": "M01.L03.Q13",
                "section_id": "full-product",
                "type": "open",
                "question": (
                    "Design a deployable multimodal assistant that can listen, view sampled camera frames, "
                    "call external tools, and run from a mobile browser. Explain the data flow, tool execution boundary, "
                    "mobile UI states, secret management, container deployment, and one privacy safeguard."
                ),
            },
        ],

        "passing_score": 70,
    },
}
