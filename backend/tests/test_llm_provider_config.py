"""
The AI provider layer: configuration checks, timeouts, and empty answers.

Nothing here reaches a network. The SDK clients are replaced with recorders,
so these tests pin down what the app *asks* the SDK to do — which is where
the mentor's "spins for ten minutes, then 500s" behaviour came from.
"""
from types import SimpleNamespace

import anthropic
import openai
import pytest

from app.core.config import Settings, settings
from app.services import get_llm
from app.services.llm import LLMProviderFactory
from app.services.llm.providers.AnthropicProvider import AnthropicProvider
from app.services.llm.providers.OpenAIProvider import OpenAIProvider


# ─── Settings.llm_config_problems ─────────────────────────────────────────

def _cfg(**kw) -> Settings:
    base = dict(
        GENERATION_BACKEND="openai", GENERATION_MODEL_ID="gpt-4o-mini",
        OPENAI_API_KEY="sk-test-not-real", ANTHROPIC_API_KEY=None,
    )
    base.update(kw)
    return Settings(**base)


def test_a_complete_configuration_has_no_problems():
    assert _cfg().llm_config_problems() == []
    assert _cfg(
        GENERATION_BACKEND="anthropic", GENERATION_MODEL_ID="claude-sonnet-4-20250514",
        ANTHROPIC_API_KEY="sk-ant-test", OPENAI_API_KEY=None,
    ).llm_config_problems() == []


@pytest.mark.parametrize("overrides, names", [
    ({"OPENAI_API_KEY": None}, "OPENAI_API_KEY"),
    ({"OPENAI_API_KEY": ""}, "OPENAI_API_KEY"),
    ({"OPENAI_API_KEY": "   "}, "OPENAI_API_KEY"),
    ({"GENERATION_MODEL_ID": ""}, "GENERATION_MODEL_ID"),
    ({"GENERATION_MODEL_ID": "  "}, "GENERATION_MODEL_ID"),
    ({"GENERATION_BACKEND": "gemini"}, "GENERATION_BACKEND"),
    ({"GENERATION_BACKEND": ""}, "GENERATION_BACKEND"),
    # Right key for the wrong backend — the default backend is anthropic.
    ({"GENERATION_BACKEND": "anthropic"}, "ANTHROPIC_API_KEY"),
])
def test_each_misconfiguration_is_named(overrides, names):
    problems = _cfg(**overrides).llm_config_problems()
    assert problems and any(names in p for p in problems), problems


def test_problems_never_contain_a_secret_value():
    joined = " ".join(_cfg(OPENAI_API_KEY="sk-SECRET-VALUE-1", GENERATION_MODEL_ID="").llm_config_problems())
    assert "sk-SECRET-VALUE-1" not in joined


# ─── get_llm() ────────────────────────────────────────────────────────────

def test_get_llm_refuses_a_misconfiguration_with_a_message_naming_the_setting(monkeypatch):
    monkeypatch.setattr(settings, "GENERATION_BACKEND", "openai")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", None)
    monkeypatch.setattr(settings, "GENERATION_MODEL_ID", "gpt-4o-mini")
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        get_llm()


def test_get_llm_refuses_a_blank_model(monkeypatch):
    monkeypatch.setattr(settings, "GENERATION_BACKEND", "openai")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-test-not-real")
    monkeypatch.setattr(settings, "GENERATION_MODEL_ID", "")
    with pytest.raises(RuntimeError, match="GENERATION_MODEL_ID"):
        get_llm()


def test_get_llm_builds_the_configured_provider(monkeypatch):
    monkeypatch.setattr(settings, "GENERATION_BACKEND", "openai")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-test-not-real")
    monkeypatch.setattr(settings, "GENERATION_MODEL_ID", "gpt-4o-mini")
    provider = get_llm()
    assert isinstance(provider, OpenAIProvider)
    assert provider.model_id == "gpt-4o-mini"


# ─── timeouts reach the SDK ───────────────────────────────────────────────

class _RecordingOpenAI:
    instances: list = []

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        _RecordingOpenAI.instances.append(self)


def test_factory_bounds_the_openai_client(monkeypatch):
    _RecordingOpenAI.instances = []
    monkeypatch.setattr(openai, "OpenAI", _RecordingOpenAI)
    cfg = _cfg(GENERATION_TIMEOUT_SECONDS=12.5, GENERATION_MAX_RETRIES=0)

    LLMProviderFactory(cfg).create("openai")._get_client()

    kwargs = _RecordingOpenAI.instances[0].kwargs
    assert kwargs["timeout"] == 12.5
    assert kwargs["max_retries"] == 0
    assert kwargs["api_key"] == "sk-test-not-real"


def test_factory_bounds_the_anthropic_client(monkeypatch):
    seen = {}

    class _Recorder:
        def __init__(self, **kwargs):
            seen.update(kwargs)

    monkeypatch.setattr(anthropic, "Anthropic", _Recorder)
    cfg = _cfg(GENERATION_BACKEND="anthropic", ANTHROPIC_API_KEY="sk-ant-test",
               GENERATION_TIMEOUT_SECONDS=9, GENERATION_MAX_RETRIES=1)

    LLMProviderFactory(cfg).create("anthropic")._get_client()

    assert seen["timeout"] == 9 and seen["max_retries"] == 1


def test_default_budget_fits_inside_the_browser_and_gunicorn_limits():
    """The browser abandons an API call at 30 s and gunicorn kills a worker
    at 60 s. A provider allowed to outlive either is a request nobody is
    waiting for any more."""
    assert 0 < Settings().GENERATION_TIMEOUT_SECONDS * (Settings().GENERATION_MAX_RETRIES + 1) < 30


def test_a_provider_built_directly_keeps_the_sdk_defaults(monkeypatch):
    """Offline generation scripts construct providers themselves and may
    legitimately wait minutes; only the web app's factory bounds the call."""
    _RecordingOpenAI.instances = []
    monkeypatch.setattr(openai, "OpenAI", _RecordingOpenAI)

    OpenAIProvider(api_key="sk-test", model_id="gpt-4o-mini")._get_client()

    assert "timeout" not in _RecordingOpenAI.instances[0].kwargs
    assert "max_retries" not in _RecordingOpenAI.instances[0].kwargs


# ─── empty answers ────────────────────────────────────────────────────────

def _openai_returning(content):
    message = SimpleNamespace(content=content)
    response = SimpleNamespace(choices=[SimpleNamespace(message=message)], usage=None)
    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kw: response)))
    provider = OpenAIProvider(api_key="sk-test", model_id="gpt-4o-mini")
    provider._client = client
    return provider


def test_openai_none_content_becomes_empty_text_not_none():
    assert _openai_returning(None).chat("sys", [{"role": "user", "content": "hi"}]) == ""


def test_openai_text_content_is_returned_untouched():
    assert _openai_returning("hello").chat("sys", [{"role": "user", "content": "hi"}]) == "hello"


def _anthropic_returning(*blocks):
    response = SimpleNamespace(content=list(blocks), usage=None)
    client = SimpleNamespace(messages=SimpleNamespace(create=lambda **kw: response))
    provider = AnthropicProvider(api_key="sk-ant-test", model_id="claude-sonnet-4-20250514")
    provider._client = client
    return provider


def _text(value):
    return SimpleNamespace(type="text", text=value)


def test_anthropic_empty_content_is_empty_text_not_an_index_error():
    assert _anthropic_returning().chat("sys", [{"role": "user", "content": "hi"}]) == ""


def test_anthropic_joins_text_blocks_and_skips_the_others():
    provider = _anthropic_returning(SimpleNamespace(type="thinking", thinking="..."), _text("Hello, "), _text("world"))
    assert provider.chat("sys", [{"role": "user", "content": "hi"}]) == "Hello, world"


def test_anthropic_single_text_block_is_unchanged():
    assert _anthropic_returning(_text("hi there")).chat("sys", [{"role": "user", "content": "hi"}]) == "hi there"
