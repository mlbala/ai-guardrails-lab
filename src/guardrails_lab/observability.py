"""Tracing helpers (LangSmith)."""

import os

from guardrails_lab.config import load_env


def enable_langsmith(project: str | None = None) -> bool:
    """Turn on LangSmith tracing for this process if LANGSMITH_API_KEY is set.

    Args:
        project: LangSmith project to log runs to. Defaults to LANGSMITH_PROJECT from .env.

    Returns:
        True if tracing is on, False if no LANGSMITH_API_KEY was found.
    """
    load_env()
    if not os.getenv("LANGSMITH_API_KEY"):
        return False

    os.environ["LANGSMITH_TRACING"] = "true"
    if project:
        os.environ["LANGSMITH_PROJECT"] = project
    return True
