import os

import pytest

from guardrails_lab.config import CONFIGS_DIR, DATA_DIR, REPO_ROOT, MissingEnvError, load_env

TEST_KEY = "GUARDRAILS_LAB_TEST_KEY"


@pytest.fixture
def env_file(tmp_path, monkeypatch):
    """A .env file holding TEST_KEY; the key is removed from os.environ afterwards."""
    path = tmp_path / ".env"
    path.write_text(f"{TEST_KEY}=from-dotenv\n")
    monkeypatch.delenv(TEST_KEY, raising=False)
    yield path
    os.environ.pop(TEST_KEY, None)


def test_repo_root_holds_the_project():
    assert (REPO_ROOT / "pyproject.toml").is_file()
    assert (REPO_ROOT / "src" / "guardrails_lab").is_dir()
    assert CONFIGS_DIR == REPO_ROOT / "configs"
    assert DATA_DIR == REPO_ROOT / "data"


def test_load_env_reads_the_env_file(env_file):
    assert load_env(required=[TEST_KEY], env_file=env_file) is True
    assert os.environ[TEST_KEY] == "from-dotenv"


def test_load_env_keeps_existing_values_unless_override(env_file, monkeypatch):
    monkeypatch.setenv(TEST_KEY, "already-set")
    load_env(env_file=env_file)
    assert os.environ[TEST_KEY] == "already-set"

    load_env(env_file=env_file, override=True)
    assert os.environ[TEST_KEY] == "from-dotenv"


def test_load_env_raises_for_missing_keys(env_file):
    with pytest.raises(MissingEnvError, match="GUARDRAILS_LAB_NOT_SET"):
        load_env(required=[TEST_KEY, "GUARDRAILS_LAB_NOT_SET"], env_file=env_file)


def test_load_env_without_env_file_returns_false(tmp_path):
    assert load_env(env_file=tmp_path / "missing.env") is False
