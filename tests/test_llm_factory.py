import pytest
from langchain_openai import ChatOpenAI

from guardrails_lab.llm_factory import get_chat_model


@pytest.mark.parametrize("spec", ["gpt-5-mini", "openai:", ":gpt-5-mini", ""])
def test_get_chat_model_rejects_specs_without_provider_and_model(spec):
    with pytest.raises(ValueError, match="provider:model"):
        get_chat_model(spec)


def test_get_chat_model_builds_the_provider_class(monkeypatch):
    # Constructing the model makes no API call; the key only has to be present
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    model = get_chat_model("openai:gpt-5-mini", max_retries=1)

    assert isinstance(model, ChatOpenAI)
    assert model.model_name == "gpt-5-mini"
    assert model.max_retries == 1
