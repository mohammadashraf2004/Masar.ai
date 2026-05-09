from enum import Enum


class LLMEnum(str, Enum):
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
