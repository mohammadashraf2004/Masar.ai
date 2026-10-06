"""M01.L02 — Architecting Real-Time AI Interaction.

One source chapter -> one complete learner-facing Lesson + inline Images
+ inline Exercises + lesson Quiz.

Source alignment:
- Chapter 3: Architecting for Real-Time AI Interaction
- Early Release draft; page numbers were not provided in the supplied source.

Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L02"

MODULE_ORDER = 1

MODULE_TITLE = "Agent Foundations & Real-Time Interaction"

MODULE_DESCRIPTION = (
    "Move from static, turn-based AI interactions to live conversational systems "
    "by combining contextual language models, persistent WebSocket communication, "
    "browser audio processing, voice activity detection, session management, "
    "secure backend proxying, streaming playback, and interruption handling."
)

SOURCE_CHAPTER = 3

SOURCE_PAGES = "Early Release draft; page numbers not provided"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Architecting Real-Time AI Interaction",

    "slug": "agent-foundations-m01-l02",

    "description": (
        "Learn how to architect a browser-based, real-time voice AI application "
        "from first principles: why older intent-and-slot assistants felt rigid, "
        "why context and WebSockets change the interaction model, and how audio "
        "capture, proxying, streaming playback, VAD, and interruption fit together."
    ),

    "order": 2,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "real-time-ai",
        "voice-ai",
        "websockets",
        "streaming",
        "audio-processing",
        "audio-worklet",
        "vad",
        "session-management",
        "gemini-live",
        "backend-proxy",
        "echo-cancellation",
        "browser-audio",
    ],

    "prerequisite_ids": ["M01.L01"],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Architecting Real-Time AI Interaction",

        "content": r"""
# Architecting Real-Time AI Interaction

> **Lesson:** M01.L02  
> **Module:** Agent Foundations & Real-Time Interaction  
> **Source alignment:** Chapter 3 of the supplied Early Release material.  
> This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why early voice assistants often felt like command systems rather than genuine conversations.
- Describe the intent-and-slot architecture and where it breaks down.
- Explain how Transformer-based context handling enables follow-up questions and reference resolution.
- Explain why long-lived, bidirectional communication is important for real-time voice systems.
- Compare REST request-response communication with persistent WebSocket streaming.
- Identify the core ingredients of a modern live voice assistant: a capable model, streaming, VAD, session management, and multimodality.
- Explain why a secure backend proxy is useful in browser-based AI applications.
- Describe why browsers are attractive for voice applications, especially because of built-in audio capabilities such as echo cancellation.
- Explain how browser microphone audio can be captured, converted, chunked, and streamed.
- Explain why AudioWorklet is preferable to heavy processing on the browser's main UI thread.
- Describe the two concurrent forwarding paths needed in a bidirectional proxy.
- Explain how streamed audio responses are decoded, queued, and played smoothly.
- Explain how interruption handling creates a more natural "hot mic" conversational experience.
- Trace the full end-to-end data flow from microphone to model and back to speakers.
- Identify source-specific implementation details that should be re-verified before production use.

---

## 1. Why early voice assistants felt rigid

For many users, first-generation voice assistants looked conversational on the surface.

You could say something aloud and hear a spoken response.

But the architecture underneath was usually much more rigid than ordinary human conversation.

A simplified interaction might look like:

```text
User: Find me some Italian restaurants.
Assistant: Any part of town?
User: Near my office.
Assistant: I found web results for "near my office."
```

Why can the second request fail?

Because the system may not maintain the same flexible conversational context a modern language model can use.

The user assumes:

```text
"near my office"
```

means:

```text
"Find Italian restaurants near my office."
```

A rigid command architecture may instead treat the latest utterance as a fresh command.

### Intent-and-slot systems

A common design pattern for older assistants was:

```text
User utterance
     ↓
Intent classification
     ↓
Slot extraction
     ↓
Predefined backend action
```

For example:

```text
"Play Bohemian Rhapsody by Queen"
```

could be mapped to:

```text
Intent:
    PlayMusic

Slots:
    song_title = "Bohemian Rhapsody"
    artist_name = "Queen"
```

This works well when the user request fits a known form.

You can think of it as an intelligent form-filling system.

```text
Intent form: PlayMusic
--------------------------------
song_title: [Bohemian Rhapsody]
artist:     [Queen]
```

The system succeeds if:

1. it recognizes the intent,
2. it knows which slots that intent requires,
3. it extracts values for those slots,
4. and it has backend logic for that form.

### Why this breaks

Suppose a user says:

```text
"I'm in the mood for some 70s rock."
```

That is not necessarily a direct command matching one predefined form.

A human can infer:

- music is wanted,
- the style is rock,
- the decade is the 1970s,
- and the user probably wants recommendations or playback.

A rigid intent system may fail if there is no predefined intent covering that phrasing.

The deeper problem is:

> The user must learn how the software expects requests to be phrased.

That is the opposite of natural conversation.

[[IMAGE_NEEDED: Intent-and-slot voice assistant | A diagram showing several example utterances flowing into one Intent block, with extracted slots such as song_title and artist_name feeding a predefined backend action | Learner should notice that the system behaves like a structured form-filling pipeline rather than open-ended contextual reasoning]]

### What a natural conversation requires

A useful conversational system needs to handle:

- follow-up questions,
- pronouns and references,
- incomplete utterances,
- conversational repair,
- changing direction,
- interruptions,
- and context that spans multiple turns.

This requires more than speech recognition.

It requires a reasoning system that can interpret language **in context**.

---

## 2. Context: the first pillar of real-time conversation

The source connects the rise of modern conversational AI to Transformer-based language models.

A central idea is **self-attention**.

### Self-attention and relationships

Consider:

```text
He dropped the glass on the floor, and it shattered.
```

What does **it** refer to?

A human understands that the glass shattered.

The word "floor" is closer to "it" in the sentence, but semantic context makes "glass" the sensible referent.

A Transformer does not have to treat each word independently.

Its attention mechanism can model relationships across the sequence.

The practical result is that modern language models are much better at tasks such as:

- resolving references,
- maintaining topic continuity,
- interpreting ambiguous phrases,
- and using previous context.

### Models and conversation history

The chapter describes the model as stateless between separate calls.

A common application pattern is therefore:

```text
Turn 1 history:
User: What is the capital of France?
Assistant: Paris.

Turn 2 request sent to model:
User: What is the capital of France?
Assistant: Paris.
User: What is its population?
```

The application resends the relevant conversation history.

The model can then infer:

```text
"its" -> Paris
```

This is one way a chat application creates the experience of memory.

### Context is not free

As a conversation grows, the history becomes larger.

That means more data may need to be:

- retained,
- transmitted,
- processed,
- and managed within a context limit.

For ordinary text chat, that overhead can still be manageable.

For live voice, the system must additionally deal with continuous audio and low-latency turn-taking.

That introduces the second pillar: **real-time transport**.

---

## 3. REST vs WebSockets: letters versus a phone line

Traditional web APIs often use a request-response model.

### REST mental model

A simplified interaction is:

```text
Client creates complete request
            ↓
        Send request
            ↓
       Server works
            ↓
      Send response
            ↓
Client receives complete response
```

This resembles sending a letter.

You send one message and wait for a reply.

For many tasks, this is excellent.

REST is widely useful for:

- CRUD operations,
- ordinary web APIs,
- database-backed services,
- request-response inference,
- and operations that do not require a continuously open channel.

### Why real-time voice is different

A live conversation is not simply:

```text
request -> response -> request -> response
```

During a natural conversation:

- the user may start speaking before playback ends,
- the assistant may stream partial output,
- audio arrives continuously,
- session events can arrive at any time,
- turn boundaries are dynamic,
- and both sides need to send data independently.

That makes the transport problem different.

### WebSocket mental model

A WebSocket establishes a persistent, bidirectional connection.

```text
Client  <====================>  Server
          connection stays open
```

Both sides can send messages while the connection remains alive.

The source uses a useful analogy:

```text
REST       = postal service
WebSocket  = open phone line
```

This does not mean WebSockets replace REST everywhere.

It means WebSockets are a better match when the application needs **continuous two-way streaming**.

[[IMAGE_NEEDED: REST versus WebSocket communication | Side-by-side diagram: REST shows separate Request -> Response cycles that repeatedly open logical exchanges, while WebSocket shows one persistent bidirectional connection with audio/events flowing in both directions | Learner should notice that live conversation benefits from a continuously open two-way channel]]

{{exercise:M01.L02.EX01}}

---

## 4. The anatomy of a modern voice assistant

A strong model alone is not enough.

A WebSocket connection alone is not enough either.

A live conversational system needs several pieces working together.

### 4.1 A capable language model

The model must understand messy, natural language and conversation context.

It provides the reasoning layer.

### 4.2 Real-time streaming

The application needs a persistent communication path for continuous media and events.

This is where WebSockets fit.

### 4.3 Voice Activity Detection (VAD)

The system must recognize when:

- the user begins speaking,
- the user stops speaking,
- background sound should be ignored,
- and a new user turn may interrupt model playback.

VAD is part of natural turn-taking.

### 4.4 Session management

The application needs to track:

- the current live session,
- relevant conversation context,
- connection state,
- and context-window usage.

### 4.5 Multimodality

The interaction may include:

- audio input,
- audio output,
- text,
- and later visual streams.

The source focuses this chapter on a conversational voice assistant rather than the complete tool-using agent architecture from the previous lesson.

A useful distinction is:

```text
Voice assistant:
    conversation + streaming + turn-taking

Agent:
    conversation + reasoning + memory/state + tools/actions + goals
```

The boundaries can overlap in real systems, but this distinction helps separate concerns while learning.

### The blueprint

```text
User
 ↓
Microphone
 ↓
Browser audio pipeline
 ↓
Persistent WebSocket
 ↓
Secure backend proxy
 ↓
Live model session
 ↓
Streaming response
 ↓
Browser playback
```

Around that pipeline, the system also needs:

```text
VAD
session state
interruption handling
authentication
error handling
```

---

## 5. Why build the client in a web browser?

The chapter chooses a browser-based architecture deliberately.

One major reason is **acoustic echo**.

### The echo problem

Suppose:

1. the assistant speaks through the laptop speakers,
2. the laptop microphone is still listening,
3. the microphone captures the assistant's own voice,
4. the VAD sees speech,
5. the system may think the user interrupted.

This can create a feedback loop.

```text
AI speaker output
      ↓
room acoustics
      ↓
microphone
      ↓
VAD thinks user is speaking
      ↓
AI playback stops
```

The result can be a stuttering, unusable experience.

### Acoustic Echo Cancellation (AEC)

AEC attempts to remove the system's own speaker output from the microphone signal.

This is a signal-processing problem.

Doing it well can be difficult.

The source argues for browser-based capture because modern browsers already contain sophisticated real-time communication features built for applications such as video calls.

The architectural trade-off is:

```text
More web-application structure
        in exchange for
using mature browser media capabilities
```

### Why that is valuable

A browser can provide:

- microphone permission handling,
- Web Audio APIs,
- media-stream processing,
- built-in echo-related processing depending on the environment,
- and a portable UI layer.

The lesson to retain is broader than one API:

> A good architecture reuses mature platform capabilities instead of rebuilding difficult low-level infrastructure unnecessarily.

[[IMAGE_NEEDED: Acoustic echo feedback loop | A diagram showing AI audio leaving the speakers, being picked up by the microphone, entering VAD, and accidentally triggering interruption; beside it, show browser audio processing/AEC reducing that feedback path | Learner should understand why full-duplex voice systems must control self-captured playback]]

---

## 6. Secure two-server architecture

The chapter's implementation separates the system into a frontend and a backend proxy.

### Client application

The browser is responsible for:

- rendering the UI,
- asking for microphone permission,
- capturing audio,
- processing audio,
- sending audio chunks,
- receiving model events,
- and playing returned audio.

### Backend WebSocket proxy

The backend is responsible for:

- server-side authentication,
- establishing the upstream live-model session,
- forwarding audio from browser to model,
- forwarding model responses back to browser,
- and later supporting additional server-side logic.

### Why not connect the browser directly?

A core concern is credential security.

Sensitive server credentials should not be embedded in browser JavaScript.

Anything shipped to the browser can potentially be inspected by the user.

A proxy creates a trust boundary:

```text
Browser
  |
  | no server secret
  v
Backend proxy
  |
  | authenticated server-side connection
  v
Model provider
```

### Two WebSocket connections

The source architecture has:

```text
Browser
   ⇅ WebSocket 1
Backend Proxy
   ⇅ WebSocket 2
Live Model API
```

So the proxy is not merely a normal HTTP endpoint.

It maintains a live connection on both sides.

[[IMAGE_NEEDED: Two-WebSocket real-time voice architecture | Browser on the left with UI, microphone, and speaker; Python proxy in the middle; Live model service on the right; show one bidirectional WebSocket between browser and proxy and another between proxy and model | Learner should notice that the proxy protects credentials while relaying a continuous two-way stream]]

---

## 7. Project setup and separation of responsibilities

The source uses a project layout similar to:

```text
gemini-live-agent/
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── audio-processor.js
│   └── audio-streamer.js
└── backend/
    ├── server.py
    └── proxy/
        ├── proxy.py
        ├── requirements.txt
        └── .env
```

The exact names are less important than the responsibilities.

### `index.html`

Defines the browser UI.

### `app.js`

Acts as the browser-side coordinator.

It manages:

- the microphone button,
- recorder state,
- WebSocket messages,
- session setup,
- mute/unmute behavior,
- and playback coordination.

### `audio-processor.js`

Handles high-frequency microphone sample processing away from the main UI logic.

### `audio-streamer.js`

Queues and plays streamed model audio.

It also needs to support immediate stop behavior when the user interrupts.

### `server.py`

Serves the frontend files over HTTP during development.

### `proxy.py`

Acts as the server-side live gateway.

### `.env`

Stores environment configuration.

Sensitive values belong on the server side.

### Source-specific authentication options

The chapter shows two authentication paths:

- Application Default Credentials with Vertex AI.
- A Gemini API key for simpler testing.

These are source-aligned implementation choices.

Because provider APIs, model names, authentication methods, SDK signatures, and environment-variable conventions can change, they should be re-verified against current provider documentation before production deployment.

---

## 8. Capturing microphone audio in the browser

Now we enter the real-time media path.

### 8.1 Request microphone access

The browser requests an audio stream:

```javascript
const stream = await navigator.mediaDevices.getUserMedia({
    audio: true
});
```

This returns a `MediaStream`.

### 8.2 Create an AudioContext

The source configures an audio context for the input path.

Conceptually:

```javascript
const audioContext = new AudioContext({
    sampleRate: 16000
});
```

The chapter's implementation path expects 16 kHz PCM input.

Treat that as an implementation-specific requirement for the source's chosen live API path.

### 8.3 Why not process everything in `app.js`?

Audio arrives frequently.

If expensive audio work runs on the main browser thread, it competes with:

- UI updates,
- click events,
- layout,
- rendering,
- and other JavaScript.

This can make the page lag.

The source therefore uses an **AudioWorklet**.

### AudioWorklet mental model

```text
Main browser/UI thread
        |
        | control messages
        v
High-priority audio worklet thread
        |
        | processed chunks
        v
Main application logic
```

This separation keeps audio processing responsive without freezing the user interface.

### 8.4 Float32 to Int16 conversion

Browser audio processing often exposes floating-point samples around:

```text
-1.0 to +1.0
```

The source converts them to signed 16-bit PCM samples:

```javascript
int16Sample = floatSample * 0x7FFF;
```

Conceptually:

```text
Float32 sample
   ↓ scaling
Int16 PCM sample
```

### 8.5 Chunking

Sending each individual sample over the network would be inefficient.

So the worklet accumulates samples into a buffer.

The source uses:

```javascript
new Int16Array(2048)
```

Once full:

1. copy the buffer,
2. send the chunk to the main thread,
3. reset the index,
4. continue processing.

This is a classic streaming pattern:

```text
continuous samples
      ↓
small fixed-size buffer
      ↓
network message
      ↓
repeat
```

[[IMAGE_NEEDED: Browser microphone processing pipeline | Microphone -> MediaStream -> AudioContext -> AudioWorklet -> Float32-to-Int16 conversion -> fixed-size PCM chunks -> main thread -> WebSocket | Learner should notice that high-frequency audio processing is separated from ordinary UI work]]

{{exercise:M01.L02.EX02}}

---

## 9. Streaming audio from browser to proxy

Once a PCM chunk reaches the main browser thread, the application needs to send it through the WebSocket.

The source encodes the binary data as Base64 and packages it in JSON.

A simplified representation is:

```javascript
const message = {
    realtimeInput: {
        mediaChunks: [{
            mime_type: "audio/pcm",
            data: base64Audio
        }]
    }
};
```

Then:

```javascript
ws.send(JSON.stringify(message));
```

### Why Base64?

JSON is text-oriented.

Base64 converts binary bytes into a text representation.

The trade-off is additional size.

In many real-time systems, binary WebSocket frames may also be considered depending on the API contract.

For this lesson, preserve the source architecture:

```text
PCM bytes
   ↓
Base64
   ↓
JSON message
   ↓
WebSocket
```

### One-way checkpoint

Before connecting the model, the source verifies:

```text
Browser microphone
        ↓
AudioWorklet
        ↓
WebSocket
        ↓
Proxy receives messages
```

This is an excellent engineering practice.

Do not build the entire system and debug everything at once.

Instead, verify the pipeline in stages.

A useful sequence is:

```text
1. servers start
2. browser connects
3. microphone captures
4. proxy receives audio
5. proxy connects upstream
6. upstream receives audio
7. responses return
8. playback works
9. interruption works
```

This reduces the search space when something fails.

---

## 10. The secure proxy and connection lifecycle

The backend proxy is the center of the architecture.

It has to manage:

- the browser connection,
- the upstream live session,
- setup/configuration,
- and two simultaneous data directions.

### 10.1 Initial setup message

The source expects the browser to send configuration when a session starts.

Conceptually:

```json
{
  "setup": {
    "model": "...",
    "generation_config": {
      "response_modalities": ["audio"]
    }
  }
}
```

The proxy validates that required setup information exists before establishing the upstream session.

This is a good general pattern:

> Validate the protocol handshake before allocating expensive upstream resources.

### 10.2 Connect to the live model

After setup, the proxy creates the upstream live session.

The exact SDK syntax is source-specific.

The architecture is:

```text
client setup
    ↓
proxy validates
    ↓
proxy authenticates
    ↓
proxy opens upstream live session
```

### 10.3 Two simultaneous forwarding loops

Now the system has two independent streams:

```text
Browser -> Model
Model   -> Browser
```

Both must run concurrently.

The source uses `asyncio.gather()` to run two coroutines together.

Conceptually:

```python
await asyncio.gather(
    forward_browser_to_model(),
    forward_model_to_browser(),
)
```

This is essential.

If you only listen in one direction at a time, you do not have a true bidirectional live path.

[[IMAGE_NEEDED: Concurrent proxy forwarding | The proxy in the center with two independent async loops: one arrow Browser -> Proxy -> Model and another arrow Model -> Proxy -> Browser, both running simultaneously | Learner should notice that full-duplex communication requires independent concurrent receive/send paths]]

---

## 11. Forwarding browser audio to the model

The upstream-forwarding function conceptually performs four steps.

### Step 1 — Receive browser message

```python
async for message in client_ws:
    ...
```

This continuously listens while the connection is alive.

### Step 2 — Parse the JSON

```python
data = json.loads(message)
```

### Step 3 — Decode Base64

```python
audio_bytes = base64.b64decode(chunk_data)
```

The browser converted bytes to Base64.

The proxy reverses that operation.

### Step 4 — Wrap the bytes in the provider's expected media object

The source creates a blob with an audio MIME type indicating raw PCM and a sample rate.

Then it sends the audio into the live session.

So the translation layer is:

```text
Browser JSON
    ↓
Base64 text
    ↓
raw PCM bytes
    ↓
provider SDK media object
    ↓
live model session
```

This is a common proxy responsibility:

> Translate the client protocol into the provider protocol.

---

## 12. Forwarding model events back to the browser

The second coroutine listens to the live model session.

The source emphasizes an important detail:

```text
outer loop:
    wait for another conversational turn

inner loop:
    consume messages for the current turn
```

Why?

Because one conversational turn does not necessarily end the entire live session.

The session must remain open for future turns.

### Serializing SDK responses

Provider SDK objects are not always directly JSON serializable.

The source converts response objects into dictionaries and adds special handling for byte data.

Conceptually:

```text
SDK response
    ↓
plain dictionary
    ↓
encode bytes if necessary
    ↓
JSON
    ↓
browser WebSocket
```

At this stage, the complete round trip exists:

```text
Browser microphone
    ↓
Proxy
    ↓
Model
    ↓
Proxy
    ↓
Browser console
```

But there is still one major missing piece:

> The browser must turn returned audio chunks into continuous sound.

---

## 13. Playing streamed audio smoothly

Streaming audio arrives in pieces.

A naive implementation might play each piece immediately and independently.

That can create:

- gaps,
- clicks,
- pops,
- or overlapping playback.

The source uses an `AudioStreamer` class with a queue.

### Queue mental model

```text
incoming audio chunks
      ↓
[chunk1, chunk2, chunk3, ...]
      ↓
play chunk1
      ↓
onended
      ↓
play chunk2
      ↓
...
```

### Decoding

The source path performs:

```text
Base64 text
   ↓
bytes
   ↓
Int16 PCM samples
   ↓
Float32 samples
   ↓
AudioBuffer
   ↓
audio output
```

The playback path uses a 24 kHz audio context in the supplied implementation.

Again, that sample rate is tied to the source's chosen model/API path and should be verified before reusing the code elsewhere.

### Why convert Int16 back to Float32?

The Web Audio API works naturally with floating-point audio buffers.

The conversion is conceptually:

```javascript
floatSample = int16Sample / 32768.0;
```

### Continuous playback

Each completed `AudioBufferSourceNode` triggers the next queued chunk.

This turns many network packets into the perception of one continuous voice.

[[IMAGE_NEEDED: Streaming audio playback queue | Incoming Base64 audio chunks enter a queue, each is decoded into PCM/Float32 AudioBuffer, then Buffer 1 -> Buffer 2 -> Buffer 3 plays sequentially through the speaker | Learner should notice that queueing hides network chunk boundaries and prevents audible gaps]]

---

## 14. The "hot mic" interaction model

A traditional push-to-talk system requires explicit turn control.

For example:

```text
Press button
Speak
Release button
Wait
```

The source aims for a more natural model.

### First press

Starts the session and activates continuous microphone streaming.

### Second press

Mutes the microphone without destroying the live session.

### Third press

Unmutes and resumes audio streaming.

The connection remains alive.

This separates two concepts:

```text
session active?
microphone currently sending?
```

Those are not the same thing.

### VAD determines turn boundaries

Without a "stop speaking" button, something must detect that the user has paused.

VAD provides that signal.

Conceptually:

```text
audio stream
    ↓
speech detected
    ↓
speech continues
    ↓
pause detected
    ↓
user turn considered complete
    ↓
model responds
```

### Fluid interruption

Natural conversation is not always polite turn-taking.

Users interrupt.

A live assistant should handle:

```text
AI speaking
    ↓
user starts talking
    ↓
system detects new user speech
    ↓
AI playback stops
    ↓
listen to user
```

The source listens for an interruption event and calls the audio streamer's `stop()` method.

### Why clear the entire queue?

Suppose the system only stops the currently playing chunk.

Older queued audio would still play afterward.

So `stop()` must:

1. stop the active source,
2. clear queued chunks,
3. prevent the playback callback from continuing the old chain.

That is what makes interruption immediate from the user's perspective.

[[IMAGE_NEEDED: Hot-mic conversational state machine | States: Session inactive -> Listening -> AI speaking -> user interruption -> Listening, plus Mic muted as a side state that preserves the session | Learner should notice that session lifetime, microphone state, VAD turn detection, and playback interruption are separate pieces of state]]

{{exercise:M01.L02.EX03}}

---

## 15. Trace the complete end-to-end pipeline

A strong engineer should be able to explain exactly where one audio sample travels.

Let's trace it.

### Input path

```text
1. User speaks
2. Browser microphone captures audio
3. MediaStream feeds AudioContext
4. AudioWorklet receives Float32 samples
5. Worklet converts to Int16 PCM
6. Samples are grouped into chunks
7. Chunk is sent to main thread
8. Browser encodes bytes as Base64
9. Browser wraps data in JSON
10. Browser sends JSON over WebSocket
11. Proxy receives JSON
12. Proxy decodes Base64 into PCM bytes
13. Proxy wraps bytes for provider SDK
14. Proxy sends audio into live session
```

### Model/session path

```text
15. Live session receives streaming audio
16. VAD/session logic determines conversational timing
17. Model produces response events/audio
```

### Output path

```text
18. Proxy receives model response event
19. Proxy serializes it for browser transport
20. Browser receives WebSocket message
21. Browser extracts audio payload
22. AudioStreamer decodes Base64
23. Int16 PCM becomes Float32 samples
24. AudioBuffer is queued
25. Browser plays audio through speaker
```

### Interruption path

```text
26. User begins speaking while AI is talking
27. Live session detects interruption
28. Browser receives interruption event
29. AudioStreamer stops active playback
30. Pending queue is cleared
31. System returns to listening
```

This is the complete real-time loop.

If any step is unclear, debugging becomes difficult.

If every step has a clear responsibility and checkpoint, the architecture becomes manageable.

---

## 16. Source-aligned implementation skeleton

The full source contains more code, but the most important architecture can be summarized without hiding the main pieces.

### Browser-side recorder

```javascript
class AudioRecorder {
    async start() {
        this.stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        this.audioContext = new AudioContext({
            sampleRate: 16000
        });

        await this.audioContext.audioWorklet.addModule(
            'audio-processor.js'
        );

        this.workletNode = new AudioWorkletNode(
            this.audioContext,
            'audio-processor'
        );

        const source =
            this.audioContext.createMediaStreamSource(this.stream);

        source.connect(this.workletNode);
    }
}
```

What matters:

- browser permission,
- media stream,
- configured audio context,
- worklet loading,
- and graph connection.

### Audio worklet

```javascript
class AudioProcessor extends AudioWorkletProcessor {
    buffer = new Int16Array(2048);
    bufferIndex = 0;

    process(inputs) {
        const channelData = inputs[0][0];

        if (!channelData) {
            return true;
        }

        for (let i = 0; i < channelData.length; i++) {
            this.buffer[this.bufferIndex++] =
                channelData[i] * 0x7FFF;

            if (this.bufferIndex === this.buffer.length) {
                this.port.postMessage(
                    this.buffer.buffer.slice(0)
                );

                this.bufferIndex = 0;
            }
        }

        return true;
    }
}

registerProcessor('audio-processor', AudioProcessor);
```

What matters:

- processing off the main thread,
- format conversion,
- chunk accumulation,
- and message passing.

### Browser-to-proxy WebSocket

```javascript
const ws = new WebSocket('ws://localhost:8081');
```

Each audio chunk is wrapped and sent through this connection.

### Proxy concurrency

```python
await asyncio.gather(
    forward_client_to_model(client_ws, model_session),
    forward_model_to_client(client_ws, model_session),
)
```

What matters:

- both directions stay active at the same time.

### Playback queue

```javascript
this.audioQueue.push(audioBuffer);

if (!this.isPlaying) {
    this.playNextChunk();
}
```

What matters:

- chunks are not treated as unrelated audio files,
- playback is serialized into one continuous stream.

### Interruption

```javascript
if (response.server_content?.interrupted) {
    streamer.stop();
}
```

What matters:

- user speech has the authority to immediately stop stale assistant audio.

---

## 17. Engineering principles hidden inside the project

The chapter teaches much more than one voice app.

### Principle 1 — Choose transport based on interaction pattern

Use request-response when the task is transactional.

Use persistent streaming when both sides need asynchronous, continuous communication.

### Principle 2 — Separate trust boundaries

Do not expose server-side credentials in browser code.

Keep sensitive authentication behind a server you control.

### Principle 3 — Move high-frequency processing off the UI thread

Real-time media should not freeze the interface.

Use specialized browser/media execution paths where appropriate.

### Principle 4 — Verify the pipeline incrementally

Test:

```text
connection
then capture
then transport
then upstream
then downstream
then playback
then interruption
```

Do not debug seven unknowns at once.

### Principle 5 — Separate session state from media state

A live session can remain active even while the microphone is muted.

Likewise, model playback and input capture are separate subsystems.

### Principle 6 — Design interruption explicitly

Stopping output is not the same as generating output.

You need clear logic for:

- current playback,
- queued playback,
- new user speech,
- and state transitions.

### Principle 7 — Reuse platform capabilities

Browsers already solve many hard media problems.

Architecture is partly about deciding what **not** to build yourself.

### Principle 8 — Provider-specific code is not the architecture

Model identifiers, SDK functions, authentication environment variables, sample rates, and response shapes can change.

The architecture remains:

```text
capture
-> stream
-> secure relay
-> live model session
-> stream back
-> playback
-> interrupt
```

That is the durable knowledge.

---

## 18. Important production boundaries

The source is an Early Release tutorial and its code is tied to the provider/API version it targets.

Before using similar code in production, verify:

- current model name,
- current Live API availability,
- current SDK method names,
- WebSocket/server library signatures,
- authentication environment variables,
- input audio format,
- output audio format,
- sample rates,
- session timeout behavior,
- reconnection requirements,
- rate limits,
- maximum session duration,
- tool/event schema,
- and production security recommendations.

### Add error handling

A robust application needs behavior for:

```text
microphone permission denied
WebSocket cannot connect
proxy disconnects
upstream model disconnects
invalid setup message
audio decode failure
session timeout
authentication failure
network interruption
```

### Add reconnection strategy

A live session can fail.

Decide:

- whether the browser retries automatically,
- whether a new model session is created,
- what state is restored,
- and what the user sees.

### Add privacy controls

Voice capture should have:

- explicit user permission,
- visible recording/listening state,
- a reliable mute/stop mechanism,
- clear retention behavior,
- and safe logging practices.

### Add observability

Useful metrics include:

- time to first audio response,
- end-to-end latency,
- interruption latency,
- audio chunk rate,
- WebSocket disconnects,
- dropped messages,
- session duration,
- model errors,
- and playback underruns.

{{exercise:M01.L02.EX04}}

---

## Important misconceptions

### Misconception 1

> "A voice interface automatically means a conversational system."

### Why this is wrong

Speech input/output can be wrapped around a rigid intent-and-slot architecture. Natural conversation requires context handling, dynamic turn-taking, and a suitable interaction model.

---

### Misconception 2

> "A powerful model alone makes the experience real-time."

### Why this is wrong

Real-time conversation also depends on transport, audio capture, buffering, VAD, session state, playback, and interruption logic.

---

### Misconception 3

> "WebSockets are simply faster REST."

### Why this is wrong

The deeper difference is the communication model. REST is usually transactional request-response. WebSockets maintain a persistent bidirectional channel suitable for asynchronous streaming.

---

### Misconception 4

> "If the microphone is active, the user is always speaking."

### Why this is wrong

A hot microphone continuously supplies audio, but VAD is needed to identify speech activity and conversational turn boundaries.

---

### Misconception 5

> "Muting the microphone should terminate the whole session."

### Why this is wrong

Microphone transmission state and session lifetime are separate. A session may stay alive while input is temporarily muted.

---

### Misconception 6

> "If I stop the current audio chunk, an interruption is handled."

### Why this is wrong

Queued chunks may still play. A proper interruption handler must stop current playback and clear stale queued audio.

---

### Misconception 7

> "It is safe to put service credentials in frontend JavaScript if the code is minified."

### Why this is wrong

Client-side code is delivered to the user's device and can be inspected. Sensitive credentials belong behind a trusted backend.

---

### Misconception 8

> "The model and API details in a tutorial are permanent."

### Why this is wrong

Provider APIs change. Durable architecture should be separated from version-specific SDK syntax, model IDs, schemas, and media constraints.

---

## Key terminology

| Term | Meaning |
|---|---|
| Intent | A predefined category of user command in traditional assistant architectures |
| Slot | Structured value extracted from an utterance to fill an intent's parameters |
| Self-attention | Transformer mechanism for modeling relationships among elements in a sequence |
| Context | Information available to the model when interpreting the current input |
| Stateless model call | A call that does not inherently retain previous application turns unless state/history is supplied |
| REST | Common request-response web communication style |
| WebSocket | Persistent bidirectional connection supporting asynchronous messaging |
| Streaming | Processing or transmitting data incrementally rather than waiting for a complete payload |
| VAD | Voice Activity Detection; identifies when speech starts/stops |
| Session | Persistent interaction context spanning multiple live exchanges |
| AEC | Acoustic Echo Cancellation; reduces playback audio captured again by the microphone |
| MediaStream | Browser object representing live media tracks such as microphone audio |
| AudioContext | Web Audio API environment for audio processing and playback |
| AudioWorklet | Browser mechanism for custom low-latency audio processing off the main UI thread |
| PCM | Pulse-Code Modulation; raw digital audio sample representation |
| Int16 | Signed 16-bit integer sample format |
| Float32 audio | Floating-point audio representation commonly used by Web Audio APIs |
| Base64 | Text encoding commonly used to represent binary bytes inside JSON/text protocols |
| Backend proxy | Trusted server that relays data and protects provider credentials |
| Full-duplex | Both sides can send data independently over the connection |
| Playback queue | Ordered buffer of received audio chunks waiting to be played |
| Hot mic | Interaction model where microphone streaming remains active until explicitly muted/disabled |
| Interruption | User speech that causes current assistant playback/generation flow to be stopped or redirected |

---

## Self-check

Before continuing, make sure you can answer:

1. Why did intent-and-slot assistants struggle with flexible follow-up questions?
2. What role does conversation history play when model calls are otherwise stateless?
3. Why is a persistent bidirectional channel useful for live voice?
4. What does VAD contribute to the interaction?
5. Why is a capable LLM not sufficient by itself for a real-time voice application?
6. Why does the source place a backend proxy between the browser and model provider?
7. What problem can acoustic echo create in a hot-mic system?
8. Why is an AudioWorklet used instead of doing all sample processing on the main thread?
9. Why convert Float32 browser samples into Int16 PCM in the source implementation?
10. Why are audio samples grouped into chunks?
11. What are the two concurrent forwarding loops in the proxy?
12. Why must model response bytes be serialized carefully before sending them to the browser?
13. Why is a playback queue necessary for streamed audio?
14. Why must interruption handling clear queued audio as well as stop the current source?
15. What is the difference between microphone state and session state?
16. Which parts of this architecture are durable concepts, and which parts are provider/version-specific?
17. What would you measure to diagnose poor conversational latency?
18. Which failure cases should be handled before calling the application production-ready?

---

## Retain this idea

**Real-time conversational AI is a system architecture, not just a model feature. A natural voice experience emerges when contextual reasoning, persistent bidirectional transport, browser audio capture, VAD, secure proxying, continuous playback, session state, and interruption handling all work together as one low-latency loop.**
""".strip(),

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "why-old-assistants-failed",
                "title": "Why Early Voice Assistants Felt Rigid",
                "order": 1,
            },
            {
                "id": "context-foundation",
                "title": "Context: the First Pillar of Real-Time Conversation",
                "order": 2,
            },
            {
                "id": "rest-vs-websockets",
                "title": "REST vs WebSockets",
                "order": 3,
            },
            {
                "id": "modern-voice-blueprint",
                "title": "The Anatomy of a Modern Voice Assistant",
                "order": 4,
            },
            {
                "id": "browser-architecture",
                "title": "Why Build the Client in a Web Browser?",
                "order": 5,
            },
            {
                "id": "two-server-architecture",
                "title": "Secure Two-Server Architecture",
                "order": 6,
            },
            {
                "id": "project-setup",
                "title": "Project Setup and Separation of Responsibilities",
                "order": 7,
            },
            {
                "id": "audio-capture",
                "title": "Capturing Microphone Audio in the Browser",
                "order": 8,
            },
            {
                "id": "browser-to-proxy",
                "title": "Streaming Audio from Browser to Proxy",
                "order": 9,
            },
            {
                "id": "proxy-lifecycle",
                "title": "The Secure Proxy and Connection Lifecycle",
                "order": 10,
            },
            {
                "id": "forwarding-upstream",
                "title": "Forwarding Browser Audio to the Model",
                "order": 11,
            },
            {
                "id": "forwarding-downstream",
                "title": "Forwarding Model Events Back to the Browser",
                "order": 12,
            },
            {
                "id": "streaming-playback",
                "title": "Playing Streamed Audio Smoothly",
                "order": 13,
            },
            {
                "id": "hot-mic",
                "title": "The Hot-Mic Interaction Model",
                "order": 14,
            },
            {
                "id": "end-to-end-flow",
                "title": "Trace the Complete End-to-End Pipeline",
                "order": 15,
            },
            {
                "id": "source-code-review",
                "title": "Source-Aligned Implementation Skeleton",
                "order": 16,
            },
            {
                "id": "engineering-principles",
                "title": "Engineering Principles Hidden Inside the Project",
                "order": 17,
            },
            {
                "id": "production-boundaries",
                "title": "Important Production Boundaries",
                "order": 18,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L02.EX01",

            "title": "Choose the Right Communication Model",

            "lesson_code": "M01.L02",

            "section_id": "rest-vs-websockets",

            "placement": "after_section",

            "description": (
                "Practice choosing between request-response and persistent streaming "
                "based on application behavior."
            ),

            "instructions": (
                "For each scenario, choose REST-style request-response, WebSocket-style "
                "persistent streaming, or a combination of both:\n"
                "1. Update a user's profile name.\n"
                "2. Stream microphone audio to a live assistant while receiving audio back.\n"
                "3. Fetch a static course catalog.\n"
                "4. Run a live dashboard where the server can push updates at any time.\n"
                "5. Explain the communication requirement that drove each decision."
            ),

            "expected_output": (
                "A five-row table containing the chosen communication model and a "
                "one- or two-sentence justification for each scenario."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "websockets",
                "rest",
                "architecture-selection",
                "real-time-systems",
            ],
        },

        {
            "id": "M01.L02.EX02",

            "title": "Trace One Audio Chunk",

            "lesson_code": "M01.L02",

            "section_id": "audio-capture",

            "placement": "after_section",

            "description": (
                "Reconstruct the transformation of one microphone chunk before it "
                "leaves the browser."
            ),

            "instructions": (
                "1. Start with microphone Float32 samples.\n"
                "2. Show how they are converted to Int16 PCM.\n"
                "3. Explain why samples are buffered instead of sent individually.\n"
                "4. Show how the chunk reaches the main application thread.\n"
                "5. Explain why AudioWorklet processing protects UI responsiveness.\n"
                "6. Draw the final flow using arrows."
            ),

            "expected_output": (
                "A short written walkthrough and one arrow diagram from microphone "
                "capture to a WebSocket-ready PCM chunk."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "audio-processing",
                "pcm",
                "audio-worklet",
                "streaming",
            ],
        },

        {
            "id": "M01.L02.EX03",

            "title": "Design the Hot-Mic State Machine",

            "lesson_code": "M01.L02",

            "section_id": "hot-mic",

            "placement": "after_section",

            "description": (
                "Model the state transitions required for listening, speaking, muting, "
                "and interruption."
            ),

            "instructions": (
                "Create states for Session Inactive, Listening, AI Speaking, and Mic Muted.\n"
                "1. Define the event that starts the session.\n"
                "2. Define the event that transitions Listening -> AI Speaking.\n"
                "3. Define what happens when the user interrupts the AI.\n"
                "4. Define mute and unmute transitions without destroying the session.\n"
                "5. State exactly what should happen to queued playback on interruption."
            ),

            "expected_output": (
                "A small text-based state diagram plus transition rules for each event."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "vad",
                "state-machines",
                "interruption",
                "session-management",
            ],
        },

        {
            "id": "M01.L02.EX04",

            "title": "Production-Harden the Prototype",

            "lesson_code": "M01.L02",

            "section_id": "production-boundaries",

            "placement": "after_section",

            "description": (
                "Turn the chapter's learning prototype into a more robust production design."
            ),

            "instructions": (
                "Review the architecture Browser <-> Proxy <-> Live Model.\n"
                "1. Add handling for microphone permission denial.\n"
                "2. Add WebSocket reconnect behavior.\n"
                "3. Add a visible recording/listening indicator.\n"
                "4. Add a policy for logs and audio retention.\n"
                "5. Add metrics for latency and disconnects.\n"
                "6. Explain which source-specific values (model name, sample rates, SDK "
                "calls, authentication settings) must be re-verified.\n"
                "7. Draw the hardened architecture."
            ),

            "expected_output": (
                "A production-readiness checklist and a revised architecture diagram "
                "covering reliability, privacy, observability, and provider-version verification."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "production-readiness",
                "security",
                "observability",
                "reliability",
                "voice-ai-architecture",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L02.QZ01",

        "title": "Architecting Real-Time AI Interaction — Knowledge Check",

        "lesson_code": "M01.L02",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L02.Q01",
                "section_id": "why-old-assistants-failed",
                "question": (
                    "What is the core limitation of a rigid intent-and-slot assistant "
                    "when a user makes an unexpected conversational request?"
                ),
                "options": [
                    "It cannot represent audio digitally",
                    "It depends heavily on predefined intents and required fields",
                    "It cannot use any server",
                    "It always needs a GPU in the browser",
                ],
                "correct": 1,
                "explanation": (
                    "Intent-and-slot systems work well when requests fit predefined "
                    "structures, but they are brittle when phrasing or goals fall outside them."
                ),
            },

            {
                "id": "M01.L02.Q02",
                "section_id": "context-foundation",
                "question": (
                    "Why does the application resend conversation history when using "
                    "a stateless model call?"
                ),
                "options": [
                    "To provide the context needed to interpret follow-up questions",
                    "To increase speaker volume",
                    "To enable browser echo cancellation",
                    "To convert WebSockets into REST",
                ],
                "correct": 0,
                "explanation": (
                    "The previous turns provide context for references such as 'it', "
                    "'that', or 'the previous result'."
                ),
            },

            {
                "id": "M01.L02.Q03",
                "section_id": "rest-vs-websockets",
                "question": (
                    "Which property of WebSockets is most important for a live voice system?"
                ),
                "options": [
                    "They only allow the client to send messages",
                    "They provide a persistent bidirectional communication channel",
                    "They automatically perform all audio decoding",
                    "They eliminate the need for a backend",
                ],
                "correct": 1,
                "explanation": (
                    "A persistent two-way channel allows continuous audio and asynchronous "
                    "events to move in both directions without separate request-response cycles."
                ),
            },

            {
                "id": "M01.L02.Q04",
                "section_id": "modern-voice-blueprint",
                "question": (
                    "What is the primary purpose of Voice Activity Detection in the lesson?"
                ),
                "options": [
                    "Store API credentials",
                    "Detect when speech starts and stops for turn-taking",
                    "Convert JSON to binary",
                    "Serve the HTML page",
                ],
                "correct": 1,
                "explanation": (
                    "VAD supports natural turn boundaries and interruption behavior by "
                    "identifying when the user is speaking."
                ),
            },

            {
                "id": "M01.L02.Q05",
                "section_id": "browser-architecture",
                "question": (
                    "Why is acoustic echo problematic in a hot-mic voice assistant?"
                ),
                "options": [
                    "The system's own speaker output can be captured by the microphone "
                    "and mistaken for new user speech",
                    "It prevents HTML from loading",
                    "It changes JSON into PCM",
                    "It deletes the WebSocket connection",
                ],
                "correct": 0,
                "explanation": (
                    "Playback captured by the microphone can trigger VAD or feedback, "
                    "making the assistant interrupt itself."
                ),
            },

            {
                "id": "M01.L02.Q06",
                "section_id": "two-server-architecture",
                "question": (
                    "Why does the chapter place a backend proxy between the browser and provider?"
                ),
                "options": [
                    "To hide the HTML from the user",
                    "To protect server-side credentials and relay the live connection",
                    "To prevent all network traffic",
                    "To replace microphone permission handling",
                ],
                "correct": 1,
                "explanation": (
                    "The proxy forms a trusted server-side boundary for authentication "
                    "and bidirectional message forwarding."
                ),
            },

            {
                "id": "M01.L02.Q07",
                "section_id": "audio-capture",
                "question": (
                    "What is the main reason for using an AudioWorklet?"
                ),
                "options": [
                    "To perform custom low-latency audio processing outside normal UI work",
                    "To store cloud credentials",
                    "To render CSS",
                    "To replace the WebSocket server",
                ],
                "correct": 0,
                "explanation": (
                    "High-frequency sample conversion and buffering can interfere with the "
                    "UI if done on the main thread; AudioWorklet provides a specialized path."
                ),
            },

            {
                "id": "M01.L02.Q08",
                "section_id": "proxy-lifecycle",
                "question": (
                    "Why does the proxy run browser-to-model and model-to-browser forwarders concurrently?"
                ),
                "options": [
                    "Because only one direction is needed at a time",
                    "Because full-duplex live interaction requires independent traffic in both directions",
                    "To avoid using asynchronous code",
                    "To disable interruptions",
                ],
                "correct": 1,
                "explanation": (
                    "The browser may be sending audio while the model is independently "
                    "sending responses or events, so both loops must stay active."
                ),
            },

            {
                "id": "M01.L02.Q09",
                "section_id": "streaming-playback",
                "question": (
                    "Why does the browser maintain an audio playback queue?"
                ),
                "options": [
                    "To convert WebSockets into HTTP",
                    "To play streamed chunks in order as one smooth response",
                    "To classify user intents",
                    "To authenticate with the provider",
                ],
                "correct": 1,
                "explanation": (
                    "Network audio arrives as chunks. Queueing and sequential playback "
                    "prevent overlapping or gapped audio."
                ),
            },

            {
                "id": "M01.L02.Q10",
                "section_id": "hot-mic",
                "question": (
                    "What should happen when the user interrupts while the assistant is speaking?"
                ),
                "options": [
                    "Only update the UI text",
                    "Stop current playback and clear queued stale audio",
                    "Close the entire browser immediately",
                    "Ignore the user until every queued chunk finishes",
                ],
                "correct": 1,
                "explanation": (
                    "Natural interruption requires ending current output immediately "
                    "and preventing already-buffered audio from continuing afterward."
                ),
            },

            {
                "id": "M01.L02.Q11",
                "section_id": "engineering-principles",
                "question": (
                    "Which statement best separates durable architecture from source-specific implementation?"
                ),
                "options": [
                    "A particular preview model name is the architecture",
                    "The durable design is capture -> stream -> secure relay -> live session "
                    "-> stream back -> playback -> interrupt",
                    "Environment variable names never change",
                    "All voice APIs use identical sample rates",
                ],
                "correct": 1,
                "explanation": (
                    "Provider identifiers, SDK calls, and media constraints may change, "
                    "while the system responsibilities and data flow remain useful concepts."
                ),
            },

            {
                "id": "M01.L02.Q12",
                "section_id": "production-boundaries",
                "type": "open",
                "question": (
                    "Design a production-ready real-time voice assistant architecture. "
                    "Explain the browser audio path, secure proxy, live transport, session "
                    "state, VAD, interruption logic, reconnect behavior, privacy controls, "
                    "and three metrics you would monitor."
                ),
            },
        ],

        "passing_score": 70,
    },
}
