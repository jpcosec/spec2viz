"""The workspace the fixtures look for sibling repos in: SPECIR_WORKSPACE, else the repo's parent."""

from __future__ import annotations

from pathlib import Path

from conftest import REPO, workspace_root


def test_workspace_root_uses_env_when_set(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("SPECIR_WORKSPACE", str(tmp_path))
    assert workspace_root() == tmp_path


def test_workspace_root_defaults_to_repo_parent(monkeypatch) -> None:
    monkeypatch.delenv("SPECIR_WORKSPACE", raising=False)
    assert workspace_root() == REPO.parent


def test_workspace_root_ignores_empty_env(monkeypatch) -> None:
    monkeypatch.setenv("SPECIR_WORKSPACE", "")
    assert workspace_root() == REPO.parent
