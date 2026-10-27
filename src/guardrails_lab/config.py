"""Repo paths and .env loading shared by the modules, projects and tests."""

import os
from collections.abc import Iterable
from pathlib import Path

from dotenv import load_dotenv

# src/guardrails_lab/config.py -> repo root (the package is installed editable with `-e .`)
REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIGS_DIR = REPO_ROOT / "configs"
DATA_DIR = REPO_ROOT / "data"


class MissingEnvError(RuntimeError):
    """Raised when a required environment variable is not set."""


def load_env(
    required: Iterable[str] = (),
    env_file: str | Path | None = None,
    override: bool = False,
) -> bool:
    """Load the repo's .env file into os.environ and check that the required keys are set.

    Args:
        required: Keys that must be set (and non-empty) after loading, e.g. ["OPENAI_API_KEY"].
        env_file: The .env file to load. Defaults to <repo root>/.env.
        override: Replace variables that are already set in the environment.

    Returns:
        True if a .env file was found and loaded.

    Raises:
        MissingEnvError: If any required key is missing or empty.
    """
    env_file = Path(env_file) if env_file else REPO_ROOT / ".env"
    loaded = load_dotenv(env_file, override=override)

    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise MissingEnvError(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            f"Add them to {env_file} (see .env.example)."
        )
    return loaded
