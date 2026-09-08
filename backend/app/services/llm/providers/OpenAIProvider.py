from typing import List, Optional
import openai

from app.core.metrics import observe_llm_call
from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):

    def __init__(
        self,
        api_key: str,
        model_id: str,
        api_url: Optional[str] = None,
        default_max_tokens: int = 1000,
        default_temperature: float = 0.7,
        default_input_max_characters: int = 10000,
    ):
        self.api_key = api_key
        self.model_id = model_id
        self.api_url = api_url
        self.default_max_tokens = default_max_tokens
        self.default_temperature = default_temperature
        self.default_input_max_characters = default_input_max_characters
        self._client = None

    def _get_client(self) -> openai.OpenAI:
        if self._client is None:
            kwargs = {"api_key": self.api_key}
            if self.api_url:
                kwargs["base_url"] = self.api_url
            self._client = openai.OpenAI(**kwargs)
        return self._client

    def validate(self) -> bool:
        return bool(self.api_key)

    def chat(self, system: str, messages: List[dict], max_tokens: int = None) -> str:
        client = self._get_client()
        system, messages = self.clip_input(system, messages)
        full_messages = [{"role": "system", "content": system}] + messages
        # Token usage only exists on the provider's own response, so it is
        # reported from here rather than estimated anywhere else. This is
        # the number that answers "what is a mentor conversation costing".
        with observe_llm_call("openai", self.model_id) as call:
            response = client.chat.completions.create(
                model=self.model_id,
                max_tokens=max_tokens or self.default_max_tokens,
                messages=full_messages,
            )
            usage = getattr(response, "usage", None)
            call.record_usage(
                getattr(usage, "prompt_tokens", None),
                getattr(usage, "completion_tokens", None),
            )
            return response.choices[0].message.content
