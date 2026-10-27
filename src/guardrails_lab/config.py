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


def _find_root_dir() -> Path:
    """Return the nearest folder at or above the working directory that holds pyproject.toml
    and src/guardrails_lab, or REPO_ROOT when working outside the repo."""
    cwd = Path.cwd().resolve()
    for folder in (cwd, *cwd.parents):
        if (folder / "pyproject.toml").is_file() and (folder / "src" / "guardrails_lab").is_dir():
            return folder
    if (REPO_ROOT / "pyproject.toml").is_file():
        return REPO_ROOT
    raise FileNotFoundError(f"No repo root (pyproject.toml + src/guardrails_lab) found at or above {cwd}")


def set_root_dir(chdir: bool = True) -> Path:
    """Find the repo root and, if chdir is True, make it the working directory.

    Notebooks start in their own folder; after this, relative paths resolve from the repo root.
    """
    root_dir = _find_root_dir()
    if chdir:
        os.chdir(root_dir)
    return root_dir


def get_data_dir(create: bool = True) -> Path:
    """Return <repo root>/data, creating it if create is True."""
    data_dir = _find_root_dir() / "data"
    if create:
        data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def setup_notebook(required_env: Iterable[str] = (), chdir: bool = True) -> tuple[Path, Path]:
    """One-line notebook setup: move to the repo root, load .env and check the required keys.

    Example:
        ROOT_DIR, DATA_DIR = setup_notebook(required_env=["OPENAI_API_KEY"])

    Returns:
        (ROOT_DIR, DATA_DIR)

    Raises:
        MissingEnvError: If any required key is missing or empty.
    """
    root_dir = set_root_dir(chdir=chdir)
    load_env(required=required_env, env_file=root_dir / ".env")
    return root_dir, get_data_dir()
