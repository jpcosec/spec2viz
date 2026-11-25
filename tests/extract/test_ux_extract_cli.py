"""`specir ux extract`: the frontend extraction from the CLI, with the warning of skipped files."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

import specir.extract as extract_module
from conftest import REPO
from extraction import new_project

from specir.cli import main

FRONTEND = REPO / "tests" / "fixtures" / "blog_frontend"


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    root = new_project(tmp_path)
    shutil.copytree(FRONTEND, root / "frontend")
    return root


def runner() -> CliRunner:
    try:
        return CliRunner(mix_stderr=False)
    except TypeError:  # click >= 8.2 always separates stderr
        return CliRunner()


def test_extracts_a_tree_with_a_tsx(project: Path):
    result = runner().invoke(main, ["ux", "extract", str(project)])
    assert result.exit_code == 0, result.output
    assert "created:" in result.stdout
    assert "skipped" not in result.stderr


def test_warns_of_skipped_files_and_strict_fails(project: Path, monkeypatch: pytest.MonkeyPatch):
    real = extract_module.code_facts
    skipped = [f"frontend/gen/f{i}.tsx" for i in range(12)]

    def fake(root, paths=None):
        return {**real(root, paths), "skipped": skipped}

    monkeypatch.setattr(extract_module, "code_facts", fake)
    warn = runner().invoke(main, ["ux", "extract", str(project)])
    assert warn.exit_code == 0, warn.output
    assert "skipped 12 file(s)" in warn.stderr
    assert "frontend/gen/f9.tsx" in warn.stderr and "frontend/gen/f10.tsx" not in warn.stderr
    assert "+2 more" in warn.stderr
    strict = runner().invoke(main, ["ux", "extract", str(project), "--strict"])
    assert strict.exit_code == 1
    assert "skipped 12 file(s)" in strict.stderr
