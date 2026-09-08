from abc import ABC, abstractmethod
from typing import List


class BaseLLMProvider(ABC):
    """
    Every LLM provider must implement this interface.
    Controllers and services only ever call this — never the concrete class directly.
    """

    # Set by the concrete providers from settings.INPUT_DEFAULT_MAX_CHARACTERS.
    default_input_max_characters: int = 10_000

    def clip_input(self, system: str, messages: List[dict]) -> tuple[str, List[dict]]:
        """Last line of defence on prompt size.

        The request schemas already cap every user-supplied field, but
        content also reaches these prompts from the database (lesson
        bodies, rubrics, dataset samples, stored chat history) where no
        pydantic model is in the path. `default_input_max_characters` was
        being stored and never applied; this applies it, so no single call
        can send an unbounded prompt to a metered vendor API regardless of
        which route assembled it.
        """
        cap = self.default_input_max_characters
        clipped = [
            {**m, "content": str(m.get("content", ""))[:cap]}
            for m in messages
        ]
        return system[:cap], clipped

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
