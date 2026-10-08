"""Per-account fairness for the shared code runner.

Project Lab Run/Check Step and Python code-exercise Run/Submit all execute on
the same runner, which runs ONE job at a time per replica. Rate limits are keyed
by IP and Project Lab's lease only covers Project Lab, so before this a single
account could keep a replica busy back to back (each job may take the full
runner timeout) or fill its queue from several tabs, and every other learner
got "runner busy".

Two rules, enforced across every API worker (Redis in production, a process
dict in development and tests):

  * one in-flight runner execution per account, whatever started it;
  * a rolling budget of runner seconds per account (RUNNER_USER_SECONDS per
    RUNNER_USER_WINDOW_SECONDS), so no account can hold more than that share of
    a replica however it paces its requests.

Refusals are 429 with Retry-After. Neither rule depends on the number of
runner replicas; adding replicas raises capacity, it does not replace fairness.
"""
from __future__ import annotations

import logging
import math
import secrets
import threading
import time
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import HTTPException, status

from app.core.config import settings

logger = logging.getLogger(__name__)

_BUCKET_SECONDS = 60


class _MemoryStore:
    """Development/test fallback. Not shared between processes."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._held: dict[str, tuple[str, float]] = {}
        self._used: dict[str, float] = {}

    def acquire(self, key: str, token: str, ttl: float) -> bool:
        now = time.monotonic()
        with self._lock:
            held = self._held.get(key)
            if held and held[1] > now:
                return False
            self._held[key] = (token, now + ttl)
            return True

    def release(self, key: str, token: str) -> None:
        with self._lock:
            if self._held.get(key, ("",))[0] == token:
                self._held.pop(key, None)

    def add(self, key: str, seconds: float, ttl: int) -> None:
        with self._lock:
            self._used[key] = self._used.get(key, 0.0) + seconds

    def total(self, keys: list[str]) -> float:
        with self._lock:
            return sum(self._used.get(k, 0.0) for k in keys)

    def reset(self) -> None:
        with self._lock:
            self._held.clear()
            self._used.clear()


class _RedisStore:
    _RELEASE = "if redis.call('get', KEYS[1]) == ARGV[1] then return redis.call('del', KEYS[1]) end return 0"

    def __init__(self, url: str) -> None:
        import redis  # only needed when REDIS_URL is configured

        self._redis = redis.Redis.from_url(url, socket_timeout=2, socket_connect_timeout=2)

    def acquire(self, key: str, token: str, ttl: float) -> bool:
        return bool(self._redis.set(key, token, nx=True, px=int(ttl * 1000)))

    def release(self, key: str, token: str) -> None:
        self._redis.eval(self._RELEASE, 1, key, token)

    def add(self, key: str, seconds: float, ttl: int) -> None:
        pipe = self._redis.pipeline()
        pipe.incrbyfloat(key, seconds)
        pipe.expire(key, ttl)
        pipe.execute()

    def total(self, keys: list[str]) -> float:
        return sum(float(v) for v in self._redis.mget(keys) if v is not None)


_store = None


def _get_store():
    global _store
    if _store is None:
        _store = _RedisStore(settings.REDIS_URL) if settings.REDIS_URL else _MemoryStore()
    return _store


def _bucket_keys(user_id: int, now: float) -> list[str]:
    current = int(now // _BUCKET_SECONDS)
    count = max(1, math.ceil(settings.RUNNER_USER_WINDOW_SECONDS / _BUCKET_SECONDS))
    return [f"runner:used:{user_id}:{current - i}" for i in range(count)]


def _refuse(code: str, retry_after: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail={"code": code, "retry_after": retry_after},
        headers={"Retry-After": str(retry_after)},
    )


@asynccontextmanager
async def runner_turn(user_id: int) -> AsyncIterator[None]:
    """Hold this account's single runner slot for the body and charge the
    runner time it took against the account's rolling budget."""
    store = _get_store()
    now = time.time()
    keys = _bucket_keys(user_id, now)
    if store.total(keys) >= settings.RUNNER_USER_SECONDS:
        raise _refuse("RUNNER_BUDGET_EXHAUSTED", _BUCKET_SECONDS)
    token = secrets.token_hex(12)
    lock_key = f"runner:inflight:{user_id}"
    # The slot outlives the longest possible job (a Check Step runs the
    # learner's file twice), so a crashed worker's slot still expires.
    if not store.acquire(lock_key, token, settings.PROJECT_LAB_EXECUTION_LEASE_SECONDS):
        raise _refuse("RUNNER_BUSY_FOR_ACCOUNT", 5)
    started = time.monotonic()
    try:
        yield
    finally:
        used = max(1.0, time.monotonic() - started)
        try:
            store.add(keys[0], used, settings.RUNNER_USER_WINDOW_SECONDS + _BUCKET_SECONDS)
            store.release(lock_key, token)
        except Exception:  # noqa: BLE001 - the slot still expires; never mask the job's result
            logger.exception("could not record runner usage for user %s", user_id)
