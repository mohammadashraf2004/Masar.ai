from app.services.llm.enums.LLMEnum import LLMEnum
from app.services.llm.providers.BaseLLMProvider import BaseLLMProvider
from app.services.llm.providers.AnthropicProvider import AnthropicProvider
from app.services.llm.providers.OpenAIProvider import OpenAIProvider


class LLMProviderFactory:

    def __init__(self, config):
        self.config = config

    def create(self, provider: str) -> BaseLLMProvider:
        if provider == LLMEnum.ANTHROPIC.value:
            return AnthropicProvider(
                api_key=self.config.ANTHROPIC_API_KEY,
                model_id=self.config.GENERATION_MODEL_ID,
                default_max_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
            )

        if provider == LLMEnum.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.OPENAI_API_KEY,
                model_id=self.config.GENERATION_MODEL_ID,
                api_url=self.config.OPENAI_API_URL,
                default_max_tokens=self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_temperature=self.config.GENERATION_DEFAULT_TEMPERATURE,
                default_input_max_characters=self.config.INPUT_DEFAULT_MAX_CHARACTERS,
            )

        raise ValueError(f"Unknown LLM provider: '{provider}'. Valid values: {[e.value for e in LLMEnum]}")
