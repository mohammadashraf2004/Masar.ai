"""M01.L06 — Real-Time Communication with Generative Models.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 6, pages not provided in the supplied chapter extract.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L06"

MODULE_ORDER = 1

MODULE_TITLE = "Generative AI Service Foundations"

MODULE_DESCRIPTION = (
    "Design real-time GenAI experiences by choosing among request-response, polling, "
    "server-sent events, and WebSocket; stream model output safely; handle disconnects, "
    "retries, backpressure, CORS, and connection lifecycle; and simplify streaming APIs."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Not provided in supplied source"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Real-Time Communication with Generative Models",

    "slug": "generative-ai-services-m01-l06",

    "description": (
        "Learn when real-time communication is worth the added complexity, compare "
        "HTTP request-response, short polling, long polling, SSE, and WebSocket, then "
        "build streaming LLM endpoints with FastAPI while managing retries, errors, "
        "connection state, CORS, backpressure, and streaming API design."
    ),

    "order": 6,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 3.5,

    "skill_tags": [
        "real-time",
        "streaming",
        "fastapi",
        "sse",
        "server-sent-events",
        "websocket",
        "polling",
        "eventsource",
        "async-generators",
        "cors",
        "backpressure",
        "connection-management",
        "llm-streaming",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L05",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Real-Time Communication with Generative Models",

        "content": """
# Real-Time Communication with Generative Models

> **Course:** Building Generative AI Services  
> **Lesson:** M01.L06  
> **Module:** Generative AI Service Foundations  
> **Source alignment:** Chapter 6 from the supplied source. This lesson is an instructor-authored curriculum adaptation rather than a reproduction of the source text.

---

## Learning outcomes

By the end of this lesson, you should be able to:

- Explain why real-time delivery can improve user experience for slow AI generation.
- Recognize when streaming is unnecessary and may add avoidable complexity.
- Compare normal HTTP request-response, short polling, long polling, SSE, and WebSocket.
- Select a communication mechanism based on directionality, latency, browser support, scalability, and implementation complexity.
- Explain the SSE connection model and the browser `EventSource` interface.
- Format a simple SSE stream correctly.
- Stream LLM output through FastAPI with `StreamingResponse`.
- Explain why GET-based SSE is simple but limited for large request payloads.
- Implement the mental model for POST-based streaming using `fetch` and a streamed response body.
- Explain retries, reconnection, backpressure, connection cleanup, and state drift risks.
- Explain the WebSocket handshake and connection lifecycle.
- Build a WebSocket connection manager conceptually.
- Stream LLM output bidirectionally through a WebSocket endpoint.
- Distinguish WebSocket from webhooks.
- Handle WebSocket disconnects and close codes gracefully.
- Explain why one generalized streaming endpoint can be simpler than many specialized streaming endpoints.

---

## 1. Why real-time communication matters for GenAI

Concurrency helps a server handle multiple users.

But concurrency does not automatically improve the experience of **one user waiting for a slow generation**.

Suppose an LLM takes 20 seconds to produce a long answer.

With a traditional request-response flow:

```text
User sends request
      ↓
server generates full answer
      ↓
20 seconds pass
      ↓
entire answer arrives at once
```

The user sees nothing until generation is finished.

A real-time stream changes the experience:

```text
User sends request
      ↓
model begins generating
      ↓
chunk 1
      ↓
chunk 2
      ↓
chunk 3
      ↓
...
```

The total generation time may be similar, but the user starts receiving useful output much earlier.

### Streaming improves perceived responsiveness

For slow generation, partial delivery can:

- reduce the feeling of waiting,
- make long outputs easier to consume,
- show that the system is actively working,
- keep the user engaged.

This is particularly relevant for:

- chatbots,
- live transcription,
- speech interfaces,
- long text generation,
- progress updates.

### But real-time is not automatically better

The source warns that streaming adds complexity.

You may need to handle:

- persistent connections,
- dropped connections,
- reconnection,
- exception handling,
- state synchronization,
- many concurrent open streams,
- memory/resource usage,
- client compatibility.

Some models or providers may not support streaming at all.

So the first engineering question is:

> **Does this feature actually need real-time updates?**

If a task finishes in one or two seconds, normal HTTP may be simpler and entirely sufficient.

[[IMAGE_NEEDED: Traditional response versus streaming AI response | Side-by-side timeline showing a normal HTTP request where nothing appears until full completion, versus a streaming request where partial text chunks arrive throughout model generation | Learner should notice that streaming improves time-to-first-visible-output without necessarily reducing total generation time]]

---

## 2. Five web communication patterns

The chapter compares five mechanisms:

1. HTTP request-response
2. short/regular polling
3. long polling
4. server-sent events (SSE)
5. WebSocket (WS)

Each solves a slightly different problem.

### Quick comparison

| Mechanism | Connection style | Direction | Good fit |
|---|---|---|---|
| HTTP request-response | Short-lived | Request then response | Normal APIs |
| Short polling | Repeated short requests | Client asks repeatedly | Job/status checks |
| Long polling | Request stays open until update | Server responds once per request | Near-real-time updates |
| SSE | Persistent HTTP stream | Server → client | LLM output, feeds, dashboards |
| WebSocket | Persistent upgraded connection | Both directions | Voice, collaboration, interactive streams |

The source stresses that the choice depends on:

- user experience,
- latency needs,
- scalability,
- development cost,
- maintainability,
- browser/client support.

There is no universally correct mechanism.

{{exercise:M01.L06.EX01}}

---

## 3. Traditional HTTP request-response

The normal web API flow is simple:

```text
Client
  ↓ request
Server
  ↓ response
Client
```

HTTP is **stateless**.

Each request is handled independently unless your application explicitly stores state elsewhere.

For example, a chatbot without server-side conversation memory may send the entire conversation history with each request.

### Strengths

HTTP request-response is:

- simple,
- widely supported,
- easy to test,
- familiar,
- well suited to REST-style APIs.

### Weakness for long AI generation

The server typically returns the response only after processing is complete.

For expensive generation:

```text
request
→ wait
→ wait
→ wait
→ full result
```

That is where real-time mechanisms become valuable.

---

## 4. Short polling

Short polling means the client repeatedly asks:

> Is there anything new yet?

Example:

```text
POST /jobs
→ returns job_id=42

GET /jobs/42
→ pending

GET /jobs/42
→ pending

GET /jobs/42
→ completed
```

### Why it is useful

This is easy to understand and implement.

It works well for:

- batch image jobs,
- long asynchronous jobs,
- occasional status checks,
- systems where updates are infrequent.

### The trade-off

If the client polls every second:

```text
request
request
request
request
request
```

many requests may return no new information.

With many users, this wastes:

- network traffic,
- server capacity,
- request-processing resources.

### Polling interval trade-off

```text
short interval
→ fresher updates
→ more traffic

long interval
→ less traffic
→ slower updates
```

Caching and rate limiting can reduce unnecessary server work.

[[IMAGE_NEEDED: Short polling lifecycle | Timeline showing a client sending repeated GET status requests every few seconds, with several `pending` responses followed by one `completed` response | Learner should notice the repeated request overhead even when nothing has changed]]

---

## 5. Long polling

Long polling tries to reduce unnecessary repeated requests.

Instead of answering immediately with:

```text
"nothing new"
```

the server keeps the request open until data is available.

```text
client request
      ↓
server waits
      ↓
new data appears
      ↓
server responds
      ↓
connection closes
      ↓
client immediately opens another request
```

### Why it can be better than short polling

The client creates fewer empty requests.

That can reduce traffic and improve near-real-time behavior.

### Why it is still not ideal

The server must keep unfulfilled requests open.

That consumes resources.

Other complications include:

- timeout handling,
- multiple requests from one client,
- message ordering,
- repeated reconnections.

The chapter presents SSE as a more modern alternative when a persistent server-to-client stream is available.

---

## 6. Server-sent events (SSE)

**Server-sent events** create a persistent HTTP connection through which the server can repeatedly push events to the client.

The connection is **unidirectional**:

```text
Client → initial HTTP request
Server → event
Server → event
Server → event
Server → event
```

The client does not use the same stream to continuously send arbitrary messages back.

### SSE handshake

The client requests a stream and indicates:

```text
Accept: text/event-stream
```

The server responds with:

```text
200 OK
Content-Type: text/event-stream
```

Then the connection stays open.

### Event formatting

A simple SSE event looks like:

```text
data: hello

```

The blank line terminates the event.

For token streaming:

```text
data: Hello

data:  world

data: !

data: [DONE]

```

### Why SSE is attractive for LLM output

An LLM conversation often has this pattern:

```text
client sends one prompt
server sends many generated chunks
```

That direction fits SSE naturally.

### Built-in browser support

Browsers provide the `EventSource` API.

An important advantage from the source is automatic reconnection behavior.

### SSE advantages

- built on HTTP,
- straightforward,
- persistent,
- automatic reconnection with `EventSource`,
- event IDs/retry support,
- good fit for text streams.

### SSE limitation

It is one-way.

If both sides need continuous real-time messaging, WebSocket is more appropriate.

{{exercise:M01.L06.EX02}}

---

## 7. Prototype streaming with an async generator

Before connecting a real model, it is useful to understand streaming with a mocked generator.

A teaching example:

```python
import asyncio
from typing import AsyncGenerator


async def mock_stream() -> AsyncGenerator[str, None]:
    for token in ["Hello", " ", "from", " ", "FastAPI"]:
        yield f"data: {token}\n\n"
        await asyncio.sleep(0.3)

    yield "data: [DONE]\n\n"
```

The important idea is the **async generator**.

Instead of producing one final return value:

```python
return full_text
```

it produces pieces:

```python
yield chunk_1
yield chunk_2
yield chunk_3
```

### Why mock first?

It lets you test:

- response streaming,
- browser rendering,
- disconnect handling,
- throttling,
- formatting,

without paying model-inference cost or depending on an external API.

### Stream endpoint

```python
from fastapi.responses import StreamingResponse


@app.get("/mock/stream")
async def mock_stream_controller():
    return StreamingResponse(
        mock_stream(),
        media_type="text/event-stream",
    )
```

Now FastAPI forwards each yielded chunk as it becomes available.

---

## 8. Stream an LLM response with SSE

Many model providers expose a streaming option.

Conceptually:

```python
stream = await client.generate(
    prompt=prompt,
    stream=True,
)
```

Instead of receiving one completed answer, the client receives a stream-like object.

### Async generator wrapper

The chapter uses a pattern like:

```python
async def chat_stream(prompt: str):
    stream = await model_client.create(
        prompt=prompt,
        stream=True,
    )

    async for chunk in stream:
        content = extract_content(chunk)

        if content:
            yield f"data: {content}\n\n"

    yield "data: [DONE]\n\n"
```

### FastAPI endpoint

```python
@app.get("/generate/text/stream")
async def stream_text(prompt: str):
    return StreamingResponse(
        chat_stream(prompt),
        media_type="text/event-stream",
    )
```

The path is:

```text
browser
  ↓ GET + prompt
FastAPI
  ↓
async provider stream
  ↓
generated chunk
  ↓
SSE formatting
  ↓
StreamingResponse
  ↓
browser
```

### Backpressure

The source raises an important issue:

> What if the server produces data faster than the client can consume it?

This is called **backpressure**.

A slow client can become overwhelmed by a rapid stream.

The chapter demonstrates small delays between chunks as a simple way to reduce pressure during prototyping.

In production, backpressure handling should be designed deliberately rather than assuming every client consumes at the same rate.

{{exercise:M01.L06.EX03}}

---

## 9. Consume SSE with `EventSource`

A browser can connect with:

```javascript
const source = new EventSource(
    "/generate/text/stream?prompt=hello"
);
```

Then attach handlers.

```javascript
source.addEventListener("open", handleOpen);
source.addEventListener("message", handleMessage);
source.addEventListener("error", handleError);
```

### Message handler

```javascript
function handleMessage(event) {
    if (event.data === "[DONE]") {
        source.close();
        return;
    }

    container.textContent += event.data;
}
```

### Why `[DONE]`?

The source's examples use a sentinel message to signal that generation has finished.

Then the client closes the stream.

### Connection lifecycle

A useful mental model:

```text
create EventSource
    ↓
OPEN
    ↓
receive event
    ↓
receive event
    ↓
[DONE]
    ↓
close
```

If an error occurs, the client should also close or retry according to the desired behavior.

---

## 10. CORS and browser streaming

If the frontend and API are served from different origins, browsers may enforce **Cross-Origin Resource Sharing (CORS)** restrictions.

Example:

```text
frontend:
https://app.example.com

API:
https://api.example.com
```

The browser may reject the request unless the API explicitly allows the frontend origin.

### Development workaround

The source shows broad CORS settings for demonstration.

Conceptually:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Production warning

Do not assume permissive wildcard settings are appropriate for production.

A production service should normally allow only the origins, methods, and headers that are actually required.

### Same-origin alternative

The chapter also mounts static files through FastAPI so the browser page and API share the same origin.

This avoids cross-origin requests in the prototype.

---

## 11. SSE with GET versus POST

The browser's native `EventSource` interface is designed around GET requests.

That is convenient, but GET has limitations.

### GET limitations in this context

The prompt may need to be placed in the URL:

```text
/generate/text/stream?prompt=...
```

Potential problems:

- URL-length limits,
- awkward encoding,
- unsuitable place for large payloads,
- conversation history cannot be conveniently placed in the request body.

### One solution: keep state on the server

The server can store conversation history and identify it using:

- session,
- cookie,
- conversation ID.

Then the GET request only needs a small identifier.

### Another solution: POST stream

The chapter demonstrates a POST streaming endpoint:

```python
@app.post("/generate/text/stream")
async def stream_text(prompt: str = Body(...)):
    return StreamingResponse(
        chat_stream(prompt),
        media_type="text/event-stream",
    )
```

But `EventSource` does not directly handle POST.

The browser must use `fetch` and manually consume the response body.

### Manual browser stream

Conceptually:

```javascript
const response = await fetch(
    "/generate/text/stream",
    {
        method: "POST",
        body: JSON.stringify({
            prompt: message,
        }),
    }
);

const reader = response.body.getReader();
const decoder = new TextDecoder();

while (true) {
    const { value, done } = await reader.read();

    if (done) break;

    container.textContent +=
        decoder.decode(value);
}
```

### Trade-off

```text
GET + EventSource
→ simpler client
→ built-in reconnection
→ limited request payload

POST + fetch stream
→ flexible request body
→ more client-side stream management
```

{{exercise:M01.L06.EX04}}

---

## 12. Retries and reconnection

Persistent connections can fail because of:

- network interruptions,
- server restarts,
- proxy issues,
- client connectivity changes.

A production client should define how reconnection works.

### EventSource

One SSE advantage is built-in reconnection behavior.

The server can also communicate retry timing.

### Manual POST stream

When consuming a stream manually with `fetch`, retry logic is your responsibility.

The chapter demonstrates **exponential backoff**.

```text
attempt 1 → wait 1 second
attempt 2 → wait 2 seconds
attempt 3 → wait 4 seconds
...
```

This avoids immediately hammering a failing server.

### State drift risk

A reconnection raises an important question:

> Where should the stream resume?

If the client received half an answer before disconnecting, blindly restarting could produce:

- duplicated content,
- missing content,
- a different stochastic continuation.

Reliable resume behavior may require:

- event IDs,
- persisted generation state,
- message IDs,
- client-side deduplication.

Streaming is therefore not just "send chunks."

It is also a state-management problem.

---

## 13. WebSocket: persistent two-way communication

SSE is server → client.

WebSocket is **bidirectional**.

```text
Client ⇄ Server
```

Both sides can send messages while the connection remains open.

This makes WebSocket useful for:

- interactive chat,
- speech-to-text,
- text-to-speech,
- speech-to-speech,
- multiplayer applications,
- collaboration,
- real-time transcription.

### WebSocket is not a webhook

A **webhook** is typically server-to-server event delivery.

```text
Server A
  ↓ HTTP callback
Server B webhook endpoint
```

There is no persistent two-way socket.

A **WebSocket** is:

```text
Client ⇄ persistent connection ⇄ Server
```

Do not confuse them.

### Protocol difference

A WebSocket starts with an HTTP upgrade handshake.

After the upgrade, communication uses the WebSocket protocol over the underlying TCP connection rather than ordinary HTTP request-response messages.

### Secure WebSocket

For production, the source recommends:

```text
wss://
```

rather than:

```text
ws://
```

`wss://` provides TLS encryption analogous to HTTPS.

[[IMAGE_NEEDED: SSE versus WebSocket | Side-by-side persistent connections: SSE with only server-to-client event arrows and WebSocket with arrows in both directions | Learner should notice that directionality is the central architectural difference]]

---

## 14. WebSocket handshake and lifecycle

A WebSocket begins with an HTTP **upgrade request**.

A simplified handshake includes headers indicating:

```text
Connection: Upgrade
Upgrade: websocket
```

The server accepts or rejects the upgrade.

### Lifecycle states

The chapter describes the connection through states such as:

```text
CONNECTING
    ↓
OPEN
    ↓
CLOSING
    ↓
CLOSED
```

### Message frames

Once open, the connection sends WebSocket frames.

The source discusses:

- text frames,
- binary frames,
- fragmented messages,
- control frames.

### Control frames

Important control behavior includes:

- ping/pong for connection health,
- close frames for graceful termination.

### Why state matters

A WebSocket server must manage:

- active connections,
- disconnects,
- cleanup,
- authentication,
- resource limits.

Unlike independent stateless HTTP requests, open sockets create state that remains associated with clients.

---

## 15. Manage WebSocket connections

The source creates a connection manager.

A teaching version:

```python
from fastapi import WebSocket


class WSConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(
        self,
        websocket: WebSocket,
    ) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(
        self,
        websocket: WebSocket,
    ) -> None:
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        await websocket.close()

    async def receive(
        self,
        websocket: WebSocket,
    ) -> str:
        return await websocket.receive_text()

    async def send(
        self,
        message: str,
        websocket: WebSocket,
    ) -> None:
        await websocket.send_text(message)
```

### Why centralize connection management?

Without a manager, every endpoint may duplicate:

- accept,
- send,
- receive,
- disconnect,
- tracking.

The manager becomes a reusable abstraction.

### Broadcast

If the application tracks every active connection:

```python
for connection in self.active_connections:
    await self.send(message, connection)
```

it can broadcast messages.

That is useful for:

- group chat,
- system notifications,
- collaborative editing.

### Scaling warning

An in-memory list only knows about connections in **that process**.

Once the application is distributed across several instances, connection coordination becomes a larger architectural problem.

The chapter's basic manager is useful for learning but should not be mistaken for a complete distributed WebSocket architecture.

{{exercise:M01.L06.EX05}}

---

## 16. Stream an LLM with WebSocket

The source reuses the model stream but changes the wire format.

For SSE:

```text
data: token\n\n
```

For WebSocket:

```text
token
```

because the WebSocket protocol already frames messages.

### WebSocket endpoint

Conceptually:

```python
@app.websocket("/generate/text/stream")
async def websocket_endpoint(
    websocket: WebSocket,
):
    await ws_manager.connect(websocket)

    try:
        while True:
            prompt = await ws_manager.receive(
                websocket
            )

            async for chunk in chat_stream(
                prompt,
                mode="ws",
            ):
                await ws_manager.send(
                    chunk,
                    websocket,
                )

    except WebSocketDisconnect:
        ...
    finally:
        await ws_manager.disconnect(websocket)
```

The loop allows multiple interactions over the same connection.

### Important difference from SSE

SSE pattern:

```text
client request
→ server streams one answer
```

WebSocket pattern:

```text
client message
↔ server stream
↔ client message
↔ server stream
```

The connection can support a longer interactive session.

### Client callbacks

A browser WebSocket typically has handlers for:

- `onopen`,
- `onmessage`,
- `onclose`,
- `onerror`.

This makes connection lifecycle explicit.

{{exercise:M01.L06.EX06}}

---

## 17. Graceful WebSocket error handling

HTTP APIs commonly communicate errors with status codes such as:

```text
400
404
500
```

Once a WebSocket connection is open, normal HTTP response handling no longer applies in the same way.

### During an open connection

If the server hits an error, it may:

1. send an error message,
2. initiate connection closure,
3. provide an appropriate WebSocket close code.

### Common close codes from the source

| Code | Meaning |
|---:|---|
| 1000 | Normal closure |
| 1001 | Client went away / server shutting down |
| 1002 | Protocol error |
| 1003 | Unsupported data |
| 1007 | Invalid/inconsistent encoding |
| 1008 | Policy violation |
| 1011 | Internal server error |

### Always clean up

A useful structure is:

```python
try:
    ...
except WebSocketDisconnect:
    ...
except Exception:
    ...
finally:
    cleanup_connection()
```

The `finally` block matters because stale connection references can create resource leaks.

### Authenticate before accepting sensitive connections

The chapter also warns that each new connection consumes server resources.

In production, connection establishment should include appropriate:

- authentication,
- authorization,
- limits,
- cleanup.

---

## 18. Choose SSE or WebSocket

For many GenAI applications, the most important choice is:

```text
SSE or WebSocket?
```

### Choose SSE when:

- the client sends a request and mainly receives a stream,
- text streaming is the main use case,
- you want simpler HTTP semantics,
- browser `EventSource` support is useful,
- built-in reconnection is attractive.

Example:

```text
User sends LLM prompt
→ model streams answer
```

### Choose WebSocket when:

- both sides need ongoing communication,
- the connection carries many messages,
- binary data matters,
- real-time interaction is highly dynamic.

Examples:

```text
live speech recognition
voice-to-voice assistant
collaborative AI editor
multi-user interactive chat
```

### Do not use WebSocket only because it sounds more advanced

The source explicitly frames WebSocket as potentially excessive for simple one-way model output.

The simpler protocol is often easier to:

- test,
- scale,
- observe,
- recover.

### Mechanism selection table

| Requirement | Prefer |
|---|---|
| No real-time updates needed | HTTP |
| Simple periodic job status | Short polling |
| Near-real-time update with held request | Long polling |
| One-way streaming output | SSE |
| Two-way persistent interaction | WebSocket |

{{exercise:M01.L06.EX07}}

---

## 19. Design streaming APIs for simplicity

The final architectural lesson is not protocol-specific.

The source warns against exposing too many specialized streaming endpoints.

Bad pattern:

```text
/stream/ask
/stream/search
/stream/summarize
/stream/tool
/stream/model-a
/stream/model-b
```

Now the client must understand and coordinate many backend workflows.

That pushes business logic into the frontend.

### Simpler pattern

Expose one main streaming entry point.

Use:

- request body,
- headers,
- query parameters,
- conversation state,

to tell the backend what behavior is needed.

Conceptually:

```text
Client
  ↓
/stream
  ↓
backend router/service
  ├── choose prompt
  ├── choose model
  ├── query database
  ├── call tool
  └── stream response
```

### Why this is easier

The backend already has access to:

- databases,
- services,
- prompts,
- model providers,
- authorization rules,
- application state.

Keeping switching logic there can reduce frontend complexity.

### Final architectural mental model

```text
                         ┌──────────────────┐
                         │      Client      │
                         └────────┬─────────┘
                                  │
                   request / connection
                                  │
                                  ▼
                    ┌────────────────────────┐
                    │   Streaming API Layer  │
                    ├────────────────────────┤
                    │ auth / state / routing │
                    │ model selection        │
                    │ error handling         │
                    │ connection management  │
                    └───────────┬────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │                 │                 │
              ▼                 ▼                 ▼
           Model API        Database           Tools
              │
              ▼
       generated chunks
              │
              ▼
     SSE or WebSocket stream
```

The protocol is only one part of the system.

A reliable streaming service also needs:

- good connection lifecycle management,
- clear ownership of state,
- safe retries,
- backpressure awareness,
- authentication,
- graceful errors.

---

## Important misconceptions

### Misconception 1

> Streaming makes the model compute the answer faster.

### Why this is wrong

Streaming mainly changes **delivery timing**. The user sees partial output earlier, but total model compute may be similar.

### Misconception 2

> Every AI endpoint should stream.

### Why this is wrong

Streaming adds connection, error, state, and scalability complexity. Short tasks may be simpler with ordinary HTTP.

### Misconception 3

> Short polling is real-time and efficient at any scale.

### Why this is wrong

Frequent polling can create many requests that return no new data.

### Misconception 4

> Long polling keeps one permanent connection forever.

### Why this is wrong

The server returns one message, closes that request, and the client opens another long-poll request.

### Misconception 5

> SSE and WebSocket are basically the same because both are persistent.

### Why this is wrong

SSE is primarily server-to-client over HTTP. WebSocket is bidirectional after an HTTP upgrade.

### Misconception 6

> `EventSource` can naturally send a large JSON POST body.

### Why this is wrong

The native EventSource interface uses GET, so large or structured request payloads require another pattern.

### Misconception 7

> POST streaming is always simpler than GET SSE.

### Why this is wrong

POST allows richer request bodies, but the client must manually consume and manage the response stream instead of relying on EventSource behavior.

### Misconception 8

> WebSocket is the same as a webhook.

### Why this is wrong

A webhook is an event-driven HTTP callback, usually server-to-server. A WebSocket is a persistent two-way connection.

### Misconception 9

> Once a WebSocket is accepted, normal HTTP 4xx/5xx responses are the standard error mechanism.

### Why this is wrong

After the upgrade, errors are typically communicated with messages and WebSocket close behavior/codes.

### Misconception 10

> An in-memory WebSocket connection list automatically scales across several server processes.

### Why this is wrong

Each process has separate memory. Distributed connection management requires additional architecture.

### Misconception 11

> If a client disconnects, nothing special is required.

### Why this is wrong

The server must clean up connection state and may also need to deal with incomplete streams or state drift.

### Misconception 12

> More streaming endpoints give the frontend more flexibility.

### Why this is often wrong

Too many specialized endpoints can push routing and conversation-state complexity into the client. A single streaming entry point can keep orchestration on the backend.

---

## Key terminology

| Term | Meaning |
|---|---|
| Real-time communication | Delivering updates with minimal delay while an interaction remains active |
| HTTP request-response | Client sends one request and receives one response |
| Stateless | Requests are independent unless application state is stored explicitly |
| Short polling | Client repeatedly checks for new data at fixed intervals |
| Long polling | Server holds a request until data is available, then client reconnects |
| SSE | Server-Sent Events; persistent HTTP-based server-to-client event stream |
| EventSource | Browser interface for consuming SSE streams |
| `text/event-stream` | Media type used for SSE |
| StreamingResponse | FastAPI response type that sends yielded/iterated content progressively |
| Async generator | Async function that yields values over time |
| Backpressure | Situation where the producer sends data faster than the consumer can process |
| Reconnection | Re-establishing a dropped streaming connection |
| Exponential backoff | Retry strategy that increases waiting time between repeated attempts |
| CORS | Browser security mechanism controlling cross-origin requests |
| WebSocket | Persistent full-duplex communication protocol established through an HTTP upgrade |
| Full-duplex | Both sides can send data independently over the same open connection |
| Webhook | Event-driven HTTP callback, usually from one server to another |
| Handshake | Initial negotiation used to establish a WebSocket connection |
| `ws://` | Unencrypted WebSocket scheme |
| `wss://` | TLS-protected WebSocket scheme |
| Message frame | Unit used to transmit WebSocket message data |
| Control frame | WebSocket frame used for ping/pong or closing the connection |
| Close code | WebSocket code explaining why a connection is closing |
| Connection manager | Application component tracking and operating active WebSocket connections |
| Broadcast | Sending a message to many currently connected clients |
| State drift | Client and server developing inconsistent views of stream/conversation state |
| Time to first output | Delay before the user receives the first visible generated chunk |

---

## Self-check

Before continuing, make sure you can answer:

1. Why can streaming improve the experience of a slow LLM even if total generation time is unchanged?
2. When is streaming unnecessary?
3. What is the normal HTTP request-response model?
4. Why can short polling become expensive?
5. How does polling frequency affect freshness and server traffic?
6. What makes long polling different from short polling?
7. Why does long polling still consume server resources?
8. What is SSE?
9. In which direction does data flow over an SSE stream?
10. Which content type is used for SSE?
11. Why is SSE a natural fit for LLM response streaming?
12. What does the `EventSource` browser API provide?
13. Why can an async generator model a stream naturally?
14. What role does `StreamingResponse` play?
15. What is backpressure?
16. Why might the server throttle generated chunks?
17. What does a `[DONE]` sentinel represent in the source's streaming examples?
18. When does CORS affect a streaming client?
19. Why is `allow_origins=["*"]` mainly a development convenience in the lesson?
20. Why is native EventSource GET-based SSE awkward for long conversation payloads?
21. How does POST streaming solve the request-body limitation?
22. What additional client responsibility appears when using `fetch` instead of `EventSource`?
23. What is exponential backoff?
24. Why can reconnection create duplicated or missing content?
25. What is the defining communication difference between SSE and WebSocket?
26. What is the difference between WebSocket and webhook?
27. What happens during the WebSocket HTTP upgrade?
28. Why should production WebSockets use `wss://`?
29. What are the main WebSocket lifecycle states?
30. What are text, binary, and control frames?
31. What do ping/pong frames help with?
32. Why should a WebSocket connection manager track active connections?
33. What does broadcasting mean?
34. Why does an in-memory connection manager not automatically work across several processes?
35. Why does a WebSocket LLM endpoint often use a `while True` loop?
36. How should `WebSocketDisconnect` be handled?
37. Why are WebSocket close codes useful?
38. What does close code 1000 represent?
39. What kind of applications strongly benefit from bidirectional streaming?
40. Why is SSE usually simpler for one-way LLM output?
41. When should short polling still be considered?
42. Why can one generalized streaming endpoint be easier than several specialized endpoints?
43. Which responsibilities should remain on the backend rather than the streaming client?
44. What risks must you consider when many users keep persistent connections open?

---

## Retain this idea

**Choose the simplest communication mechanism that matches the interaction: normal HTTP for completed responses, polling for occasional job status, SSE for persistent one-way model output, and WebSocket when both client and server must communicate continuously. Reliable AI streaming requires more than yielding tokens—it requires connection lifecycle management, retries, backpressure control, state consistency, security, and a clean API design.**
""",

        "estimated_minutes": 210,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {
                "id": "why-real-time",
                "title": "Why real-time communication matters for GenAI",
                "order": 1,
            },
            {
                "id": "communication-options",
                "title": "Five web communication patterns",
                "order": 2,
            },
            {
                "id": "http-request-response",
                "title": "Traditional HTTP request-response",
                "order": 3,
            },
            {
                "id": "short-polling",
                "title": "Short polling",
                "order": 4,
            },
            {
                "id": "long-polling",
                "title": "Long polling",
                "order": 5,
            },
            {
                "id": "sse-basics",
                "title": "Server-sent events (SSE)",
                "order": 6,
            },
            {
                "id": "sse-mock-stream",
                "title": "Prototype streaming with an async generator",
                "order": 7,
            },
            {
                "id": "llm-sse-stream",
                "title": "Stream an LLM response with SSE",
                "order": 8,
            },
            {
                "id": "eventsource-client",
                "title": "Consume SSE with EventSource",
                "order": 9,
            },
            {
                "id": "cors",
                "title": "CORS and browser streaming",
                "order": 10,
            },
            {
                "id": "sse-get-vs-post",
                "title": "SSE with GET versus POST",
                "order": 11,
            },
            {
                "id": "sse-retry",
                "title": "Retries and reconnection",
                "order": 12,
            },
            {
                "id": "websocket-basics",
                "title": "WebSocket: persistent two-way communication",
                "order": 13,
            },
            {
                "id": "websocket-handshake",
                "title": "WebSocket handshake and lifecycle",
                "order": 14,
            },
            {
                "id": "websocket-manager",
                "title": "Manage WebSocket connections",
                "order": 15,
            },
            {
                "id": "websocket-streaming",
                "title": "Stream an LLM with WebSocket",
                "order": 16,
            },
            {
                "id": "websocket-errors",
                "title": "Graceful WebSocket error handling",
                "order": 17,
            },
            {
                "id": "choose-sse-or-ws",
                "title": "Choose SSE or WebSocket",
                "order": 18,
            },
            {
                "id": "streaming-api-design",
                "title": "Design streaming APIs for simplicity",
                "order": 19,
            },
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L06.EX01",

            "title": "Choose the Communication Mechanism",

            "lesson_code": "M01.L06",

            "section_id": "communication-options",

            "placement": "after_section",

            "description": (
                "Practice choosing among HTTP, short polling, long polling, SSE, and "
                "WebSocket from application requirements."
            ),

            "instructions": (
                "Choose the most appropriate primary mechanism for each scenario:\n\n"
                "1. A normal CRUD endpoint returning a saved user profile.\n"
                "2. A batch image job where the client checks progress every 20 seconds.\n"
                "3. A text chatbot that only needs to stream the assistant's response.\n"
                "4. A live speech-to-speech assistant where both sides continuously send data.\n"
                "5. A legacy client that needs near-real-time updates but cannot use SSE/WS.\n\n"
                "For each answer, explain the direction of communication and why the "
                "chosen mechanism is simpler than the alternatives."
            ),

            "expected_output": (
                "Five communication-mechanism choices with directionality and reasoning."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "protocol-selection",
                "real-time-architecture",
                "tradeoff-reasoning",
            ],
        },

        {
            "id": "M01.L06.EX02",

            "title": "Build a Mock SSE Stream",

            "lesson_code": "M01.L06",

            "section_id": "sse-basics",

            "placement": "after_section",

            "description": (
                "Learn SSE formatting and streaming behavior without depending on an AI provider."
            ),

            "instructions": (
                "1. Create an async generator that yields the words in `Hello from FastAPI` "
                "one at a time.\n"
                "2. Format each message using the SSE `data:` prefix and blank-line terminator.\n"
                "3. Add a short `asyncio.sleep` between messages.\n"
                "4. End with `[DONE]`.\n"
                "5. Expose the generator with FastAPI `StreamingResponse` and "
                "`media_type=\"text/event-stream\"`.\n"
                "6. Explain why `yield` is more appropriate than returning one final string."
            ),

            "expected_output": (
                "A mock SSE generator, streaming endpoint, and short explanation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "sse-format",
                "async-generators",
                "streaming-response",
            ],
        },

        {
            "id": "M01.L06.EX03",

            "title": "Wrap a Provider Stream for SSE",

            "lesson_code": "M01.L06",

            "section_id": "llm-sse-stream",

            "placement": "after_section",

            "description": (
                "Practice converting a provider's asynchronous token stream into a browser-compatible SSE stream."
            ),

            "instructions": (
                "Write pseudocode or Python for an async `chat_stream(prompt)` function.\n\n"
                "It must:\n"
                "1. request streaming output from an async model client,\n"
                "2. iterate asynchronously over provider chunks,\n"
                "3. ignore empty chunks,\n"
                "4. format content as SSE events,\n"
                "5. yield a final `[DONE]` event,\n"
                "6. include one simple backpressure/throttling control.\n\n"
                "Then state what happens if the provider returns the entire answer instead "
                "of a stream."
            ),

            "expected_output": (
                "An async streaming wrapper plus an explanation of provider streaming requirements."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "llm-streaming",
                "sse",
                "async-iteration",
            ],
        },

        {
            "id": "M01.L06.EX04",

            "title": "GET EventSource or POST Stream?",

            "lesson_code": "M01.L06",

            "section_id": "sse-get-vs-post",

            "placement": "after_section",

            "description": (
                "Reason about the trade-off between native EventSource simplicity and richer POST request bodies."
            ),

            "instructions": (
                "You are building a chatbot whose request contains:\n"
                "- the newest user message,\n"
                "- conversation ID,\n"
                "- several generation options,\n"
                "- optional retrieved context.\n\n"
                "Compare these designs:\n"
                "A. GET SSE with EventSource.\n"
                "B. POST endpoint whose streamed response is read through `fetch`.\n"
                "C. POST data first, store it server-side, then open GET SSE using an ID.\n\n"
                "For each design, list one strength and one weakness, then select one "
                "for this scenario and explain your reasoning."
            ),

            "expected_output": (
                "A three-option comparison and one justified design choice."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "sse-api-design",
                "eventsource",
                "streaming-http",
            ],
        },

        {
            "id": "M01.L06.EX05",

            "title": "Implement a WebSocket Connection Manager",

            "lesson_code": "M01.L06",

            "section_id": "websocket-manager",

            "placement": "after_section",

            "description": (
                "Centralize WebSocket connection lifecycle operations."
            ),

            "instructions": (
                "Create a `WSConnectionManager` with:\n"
                "1. an `active_connections` list,\n"
                "2. `connect`,\n"
                "3. `disconnect`,\n"
                "4. `receive`,\n"
                "5. `send`,\n"
                "6. `broadcast`.\n\n"
                "Then explain why the in-memory list works for a simple single-process "
                "demo but is insufficient by itself for a distributed deployment."
            ),

            "expected_output": (
                "A connection-manager implementation plus a scaling explanation."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "websocket",
                "connection-management",
                "broadcasting",
            ],
        },

        {
            "id": "M01.L06.EX06",

            "title": "Design a Bidirectional LLM Stream",

            "lesson_code": "M01.L06",

            "section_id": "websocket-streaming",

            "placement": "after_section",

            "description": (
                "Trace message flow through a persistent WebSocket LLM session."
            ),

            "instructions": (
                "Design a WebSocket endpoint that:\n"
                "1. accepts a connection,\n"
                "2. waits for a client prompt,\n"
                "3. forwards the prompt to a streaming LLM client,\n"
                "4. sends each generated chunk back to the same socket,\n"
                "5. waits for another prompt without reopening the connection,\n"
                "6. catches `WebSocketDisconnect`,\n"
                "7. always removes the connection during cleanup.\n\n"
                "Draw the message flow for two user prompts over the same connection."
            ),

            "expected_output": (
                "A WebSocket endpoint/pseudocode and a two-turn message-flow diagram."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "websocket-streaming",
                "connection-lifecycle",
                "llm-streaming",
            ],
        },

        {
            "id": "M01.L06.EX07",

            "title": "SSE or WebSocket for Three AI Products",

            "lesson_code": "M01.L06",

            "section_id": "choose-sse-or-ws",

            "placement": "after_section",

            "description": (
                "Choose the simplest real-time protocol that satisfies each AI product's interaction pattern."
            ),

            "instructions": (
                "Choose SSE or WebSocket for each product and justify the choice:\n\n"
                "1. A text assistant where the user submits one message and receives "
                "a streamed answer.\n"
                "2. A live transcription product where microphone audio continuously "
                "flows to the server while transcripts continuously return.\n"
                "3. A collaborative AI whiteboard where several users and the AI "
                "exchange updates throughout one session.\n\n"
                "For each, discuss directionality, implementation complexity, and "
                "connection-state requirements."
            ),

            "expected_output": (
                "Three protocol choices with directionality and architecture reasoning."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "sse-vs-websocket",
                "real-time-system-design",
                "protocol-tradeoffs",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L06.QZ01",

        "title": "Real-Time Communication with Generative Models — Knowledge Check",

        "lesson_code": "M01.L06",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L06.Q01",

                "section_id": "why-real-time",

                "question": (
                    "What is the main user-experience benefit of streaming a slow LLM response?"
                ),

                "options": [
                    "The user can receive partial output before full generation finishes",
                    "The model always uses less GPU memory",
                    "The response becomes factually correct",
                    "The service no longer needs concurrency",
                ],

                "correct": 0,

                "explanation": (
                    "Streaming improves time to first visible output by sending chunks as "
                    "they become available."
                ),
            },

            {
                "id": "M01.L06.Q02",

                "section_id": "short-polling",

                "question": "What is the main scalability drawback of short polling?",

                "options": [
                    "Clients may repeatedly send requests even when no new data exists",
                    "It requires a WebSocket handshake",
                    "It cannot use normal HTTP",
                    "It is always bidirectional",
                ],

                "correct": 0,

                "explanation": (
                    "Frequent status checks can create large request volumes with many "
                    "responses containing no new information."
                ),
            },

            {
                "id": "M01.L06.Q03",

                "section_id": "long-polling",

                "question": "How does long polling typically deliver multiple updates over time?",

                "options": [
                    "The server sends many messages on one permanent response forever",
                    "Each held request returns one update, then the client opens another request",
                    "The client uses UDP packets",
                    "The browser creates an EventSource automatically",
                ],

                "correct": 1,

                "explanation": (
                    "Long polling holds one request until data is available, responds, "
                    "closes that request, and the client reconnects."
                ),
            },

            {
                "id": "M01.L06.Q04",

                "section_id": "sse-basics",

                "question": "Which statement best describes SSE?",

                "options": [
                    "Persistent server-to-client events over HTTP",
                    "Persistent full-duplex binary protocol only",
                    "Repeated client polling with no open connection",
                    "A server-to-server webhook specification",
                ],

                "correct": 0,

                "explanation": (
                    "SSE keeps an HTTP connection open and lets the server push events "
                    "to the client."
                ),
            },

            {
                "id": "M01.L06.Q05",

                "section_id": "sse-basics",

                "question": "Which media type is used for an SSE response?",

                "options": [
                    "application/websocket",
                    "text/event-stream",
                    "application/pdf",
                    "multipart/form-data",
                ],

                "correct": 1,

                "explanation": (
                    "The SSE response uses `text/event-stream` so compatible clients can "
                    "interpret the event stream correctly."
                ),
            },

            {
                "id": "M01.L06.Q06",

                "section_id": "llm-sse-stream",

                "question": (
                    "Why is an async generator useful for streaming model output?"
                ),

                "options": [
                    "It can yield generated chunks over time rather than waiting to return one final value",
                    "It forces the model to run on multiple GPUs",
                    "It automatically validates CORS",
                    "It converts WebSocket into HTTP",
                ],

                "correct": 0,

                "explanation": (
                    "An async generator naturally represents data that becomes available "
                    "incrementally."
                ),
            },

            {
                "id": "M01.L06.Q07",

                "section_id": "eventsource-client",

                "question": "What is a useful built-in behavior of browser EventSource?",

                "options": [
                    "Automatic reconnection support",
                    "Bidirectional binary messaging",
                    "POST request bodies",
                    "GPU inference scheduling",
                ],

                "correct": 0,

                "explanation": (
                    "EventSource is designed for SSE and includes reconnection behavior."
                ),
            },

            {
                "id": "M01.L06.Q08",

                "section_id": "sse-get-vs-post",

                "question": (
                    "What is a major limitation of GET-based EventSource for rich chatbot requests?"
                ),

                "options": [
                    "It does not naturally provide a request body for large structured payloads",
                    "It cannot receive text",
                    "It always requires WebSocket",
                    "It cannot remain connected",
                ],

                "correct": 0,

                "explanation": (
                    "EventSource uses GET, so request data is generally carried through "
                    "the URL or existing server-side state."
                ),
            },

            {
                "id": "M01.L06.Q09",

                "section_id": "websocket-basics",

                "question": "What is the defining communication capability of WebSocket?",

                "options": [
                    "Full-duplex communication over one persistent connection",
                    "Server-to-client communication only",
                    "One response per request followed by immediate close",
                    "Only server-to-server callbacks",
                ],

                "correct": 0,

                "explanation": (
                    "WebSocket supports ongoing two-way messaging while one connection "
                    "remains open."
                ),
            },

            {
                "id": "M01.L06.Q10",

                "section_id": "websocket-basics",

                "question": "How is a webhook different from a WebSocket?",

                "options": [
                    "A webhook is typically an event-driven HTTP callback rather than a persistent bidirectional socket",
                    "A webhook is always faster because it bypasses TCP",
                    "A webhook is another name for an SSE stream",
                    "A webhook requires a WebSocket upgrade handshake",
                ],

                "correct": 0,

                "explanation": (
                    "Webhooks are usually one-way event callbacks, while WebSockets keep "
                    "a persistent two-way connection."
                ),
            },

            {
                "id": "M01.L06.Q11",

                "section_id": "websocket-handshake",

                "question": "What begins a WebSocket connection?",

                "options": [
                    "An HTTP upgrade handshake",
                    "A database transaction",
                    "An SSE retry event",
                    "A background task",
                ],

                "correct": 0,

                "explanation": (
                    "The client first sends an HTTP request asking the server to upgrade "
                    "the connection to the WebSocket protocol."
                ),
            },

            {
                "id": "M01.L06.Q12",

                "section_id": "websocket-errors",

                "question": "What does WebSocket close code 1000 represent?",

                "options": [
                    "Normal closure",
                    "Protocol error",
                    "Unsupported data",
                    "Internal server error",
                ],

                "correct": 0,

                "explanation": (
                    "Code 1000 indicates a normal WebSocket connection closure."
                ),
            },

            {
                "id": "M01.L06.Q13",

                "section_id": "choose-sse-or-ws",

                "question": (
                    "Which mechanism is usually simpler for one-way streamed LLM text output?"
                ),

                "options": [
                    "SSE",
                    "WebSocket",
                    "Webhook",
                    "Short polling every millisecond",
                ],

                "correct": 0,

                "explanation": (
                    "The source recommends SSE as the simpler fit when the main need is "
                    "server-to-client streaming."
                ),
            },

            {
                "id": "M01.L06.Q14",

                "section_id": "streaming-api-design",

                "question": (
                    "Why can one generalized streaming endpoint simplify a GenAI client?"
                ),

                "options": [
                    "The backend can own model/prompt/routing logic instead of forcing the client to switch among many streaming endpoints",
                    "It eliminates all backend state",
                    "It makes authentication unnecessary",
                    "It guarantees every model supports WebSocket",
                ],

                "correct": 0,

                "explanation": (
                    "Centralizing routing and business logic keeps the client simpler and "
                    "reduces duplicated state-management responsibilities."
                ),
            },

            {
                "id": "M01.L06.Q15",

                "section_id": "streaming-api-design",

                "type": "open",

                "question": (
                    "Design the real-time communication layer for two products: "
                    "(1) a text chatbot that streams one answer after each user message, "
                    "and (2) a live voice assistant where audio must continuously travel "
                    "in both directions. Choose a mechanism for each and explain how you "
                    "would handle reconnection, errors, and connection cleanup."
                ),
            },
        ],

        "passing_score": 70,
    },
}
