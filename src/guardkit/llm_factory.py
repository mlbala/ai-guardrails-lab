"""Create chat models from a single "provider:model" string."""

from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel


def get_chat_model(spec: str, **kwargs: Any) -> BaseChatModel:
    """Create a chat model from a "provider:model" string.

    Examples: "openai:gpt-5-mini", "groq:qwen/qwen3.8-27b", "google_genai:gemini-3.5-flash-lite".
    Extra keyword arguments (temperature, max_tokens, ...) go to the model class.

    Raises:
        ValueError: If spec is not in "provider:model" form.
    """
    provider, sep, model = spec.partition(":")
    if not sep or not provider or not model:
        raise ValueError(f'Expected "provider:model" (e.g. "openai:gpt-5-mini"), got {spec!r}')
    return init_chat_model(model, model_provider=provider, **kwargs)
