from typing import List, Optional
import anthropic

from app.core.metrics import observe_llm_call
from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider


class AnthropicProvider(BaseLLMProvider):

    def __init__(
        self,
        api_key: str,
        model_id: str,
        default_max_tokens: int = 1000,
        default_temperature: float = 0.7,
        default_input_max_characters: int = 10000,
        timeout: Optional[float] = None,
        max_retries: Optional[int] = None,
    ):
        self.api_key = api_key
        self.model_id = model_id
        self.default_max_tokens = default_max_tokens
        self.default_temperature = default_temperature
        self.default_input_max_characters = default_input_max_characters
        # None leaves the SDK default in place — see OpenAIProvider.
        self.timeout = timeout
        self.max_retries = max_retries
        self._client = None

    def _get_client(self) -> anthropic.Anthropic:
        if self._client is None:
            kwargs = {"api_key": self.api_key}
            if self.timeout is not None:
                kwargs["timeout"] = self.timeout
            if self.max_retries is not None:
                kwargs["max_retries"] = self.max_retries
            self._client = anthropic.Anthropic(**kwargs)
        return self._client

    def validate(self) -> bool:
        return bool(self.api_key)

    def chat(self, system: str, messages: List[dict], max_tokens: int = None) -> str:
        client = self._get_client()
        system, messages = self.clip_input(system, messages)
        # See OpenAIProvider.chat — usage comes from the provider response.
        with observe_llm_call("anthropic", self.model_id) as call:
            response = client.messages.create(
                model=self.model_id,
                max_tokens=max_tokens or self.default_max_tokens,
                system=system,
                messages=messages,
            )
            usage = getattr(response, "usage", None)
            call.record_usage(
                getattr(usage, "input_tokens", None),
                getattr(usage, "output_tokens", None),
            )
            # Every text block, not just the first: `content` can be empty
            # (a refusal) or lead with a non-text block, and indexing [0]
            # raised IndexError/AttributeError for both.
            return "".join(
                block.text for block in response.content if getattr(block, "type", None) == "text"
            )
