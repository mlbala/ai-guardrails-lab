import os
from pathlib import Path

import pytest

import guardrails_lab
from guardrails_lab.config import (
    CONFIGS_DIR,
    DATA_DIR,
    REPO_ROOT,
    MissingEnvError,
    get_data_dir,
    load_env,
    set_root_dir,
    setup_notebook,
)

TEST_KEY = "GUARDRAILS_LAB_TEST_KEY"


@pytest.fixture
def env_file(tmp_path, monkeypatch):
    """A .env file holding TEST_KEY; the key is removed from os.environ afterwards."""
    path = tmp_path / ".env"
    path.write_text(f"{TEST_KEY}=from-dotenv\n")
    monkeypatch.delenv(TEST_KEY, raising=False)
    yield path
    os.environ.pop(TEST_KEY, None)


@pytest.fixture
def fake_repo(tmp_path, monkeypatch):
    """A minimal repo (pyproject.toml, src/guardrails_lab, .env) used as the working directory."""
    root = (tmp_path / "repo").resolve()
    (root / "src" / "guardrails_lab").mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\nname = 'fake-repo'\n")
    (root / ".env").write_text(f"{TEST_KEY}=from-fake-repo\n")
    # monkeypatch.chdir also restores the original working directory after the test
    monkeypatch.chdir(root)
    monkeypatch.delenv(TEST_KEY, raising=False)
    yield root
    os.environ.pop(TEST_KEY, None)


@pytest.fixture
def lesson_dir(fake_repo, monkeypatch):
    """A nested folder inside fake_repo, like a notebook's own folder."""
    folder = fake_repo / "modules" / "01_foundations" / "01_langchain_agents"
    folder.mkdir(parents=True)
    monkeypatch.chdir(folder)
    return folder


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


def test_set_root_dir_from_nested_folder_changes_to_root(fake_repo, lesson_dir):
    assert set_root_dir() == fake_repo
    assert Path.cwd() == fake_repo


def test_set_root_dir_without_chdir_keeps_working_directory(fake_repo, lesson_dir):
    assert set_root_dir(chdir=False) == fake_repo
    assert Path.cwd() == lesson_dir


def test_set_root_dir_outside_any_repo_falls_back_to_installed_repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert set_root_dir(chdir=False) == REPO_ROOT
    assert Path.cwd() == tmp_path.resolve()


def test_get_data_dir_creates_the_data_folder(fake_repo, lesson_dir):
    data_dir = get_data_dir()
    assert data_dir == fake_repo / "data"
    assert data_dir.is_dir()


def test_get_data_dir_without_create_does_not_make_the_folder(fake_repo):
    data_dir = get_data_dir(create=False)
    assert data_dir == fake_repo / "data"
    assert not data_dir.exists()


def test_setup_notebook_from_nested_folder(fake_repo, lesson_dir):
    root_dir, data_dir = setup_notebook(required_env=[TEST_KEY])

    assert root_dir == fake_repo
    assert data_dir == fake_repo / "data"
    assert data_dir.is_dir()
    assert Path.cwd() == fake_repo
    assert os.environ[TEST_KEY] == "from-fake-repo"


def test_setup_notebook_without_chdir_keeps_working_directory(fake_repo, lesson_dir):
    root_dir, _ = setup_notebook(required_env=[TEST_KEY], chdir=False)
    assert root_dir == fake_repo
    assert Path.cwd() == lesson_dir


def test_setup_notebook_raises_for_missing_keys(fake_repo, lesson_dir):
    with pytest.raises(MissingEnvError, match="GUARDRAILS_LAB_NOT_SET"):
        setup_notebook(required_env=[TEST_KEY, "GUARDRAILS_LAB_NOT_SET"])


def test_helpers_are_exported_from_the_package():
    assert guardrails_lab.set_root_dir is set_root_dir
    assert guardrails_lab.get_data_dir is get_data_dir
    assert guardrails_lab.setup_notebook is setup_notebook
