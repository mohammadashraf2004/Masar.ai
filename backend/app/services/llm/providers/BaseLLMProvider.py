from abc import ABC, abstractmethod
from typing import List


class BaseLLMProvider(ABC):
    """
    Every LLM provider must implement this interface.
    Controllers and services only ever call this — never the concrete class directly.
    """

    @abstractmethod
    def chat(self, system: str, messages: List[dict], max_tokens: int) -> str:
        """
        Send a system prompt + message history to the model.
        Returns the assistant's reply as a plain string.
        """
        ...

    @abstractmethod
    def validate(self) -> bool:
        """Check that the provider is configured correctly (API key present, etc.)."""
        ...
