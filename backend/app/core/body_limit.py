"""Bound the size of every request body before anything buffers it.

FastAPI reads a JSON body into memory in full before validation (field
max_length checks run after), and uvicorn sets no limit of its own. One
unauthenticated 300 MB POST to /auth/login grew a worker by ~300 MB and held it
for over a minute (measured in the 2026-10 release audit). Caddy enforces the
same ceiling at the edge (deploy/Caddyfile); this is the in-process guard for
anything that reaches the API port another way.

A declared Content-Length over the limit is refused with 413 before a byte is
read. A body without one (chunked) is counted as it streams and cut off at the
limit, so memory stays bounded either way.
"""
from __future__ import annotations

import json


class _TooLarge(Exception):
    pass


class BodySizeLimitMiddleware:
    def __init__(self, app, max_bytes: int) -> None:
        self.app = app
        self.max_bytes = max_bytes

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        declared = next((v for k, v in scope.get("headers", []) if k == b"content-length"), None)
        if declared is not None:
            try:
                too_big = int(declared) > self.max_bytes
            except ValueError:
                too_big = True
            if too_big:
                await self._reject(send)
                return

        received = 0
        started = False

        async def limited_receive():
            nonlocal received
            message = await receive()
            if message["type"] == "http.request":
                received += len(message.get("body", b""))
                if received > self.max_bytes:
                    raise _TooLarge()
            return message

        async def tracking_send(message):
            nonlocal started
            if message["type"] == "http.response.start":
                started = True
            await send(message)

        try:
            await self.app(scope, limited_receive, tracking_send)
        except _TooLarge:
            if not started:
                await self._reject(send)

    async def _reject(self, send) -> None:
        body = json.dumps({"detail": "Request body too large"}).encode()
        await send({"type": "http.response.start", "status": 413, "headers": [
            (b"content-type", b"application/json"), (b"content-length", str(len(body)).encode()),
            (b"connection", b"close"),
        ]})
        await send({"type": "http.response.body", "body": body})
