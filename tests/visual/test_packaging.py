"""Packaging of the `specir` command (IR13d, SV-J07).

- spec2viz's `tests/test_packaging.py::test_primary_cli_still_exposes_commands`, ported (its other three
  cases are IR12's, in `test_render_cases.py` and `test_schema.py`).
- The script `specir` is declared in `pyproject.toml` and points at `specir.cli:main`.
- The package installs in a clean environment (a new venv with sldb and the wheel of specIR, without
  spec2viz) and the command starts there: `specir --help`, `specir about` and `specir diagram render`
  run, and `import spec2viz` fails."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest
from click.testing import CliRunner

from specir.cli import main as specir_main

PROJECT = Path(__file__).resolve().parents[2]
SLDB_SOURCE = PROJECT.parent / "sldb"
SPEC = PROJECT / "tests" / "visual" / "fixtures" / "spec2viz" / "tests" / "fixtures" / "state.quotation.yml"


def test_primary_cli_still_exposes_commands():
    runner = CliRunner()
    result = runner.invoke(specir_main, ["--help"])

    assert result.exit_code == 0
    assert "render" in result.output
    assert "validate" not in result.output


def test_the_script_is_the_command_of_specir_cli():
    scripts = tomllib.loads((PROJECT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["scripts"]
    assert scripts["specir"] == "specir.cli:main"
    installed = Path(sys.executable).with_name("specir")
    if installed.exists():
        result = subprocess.run(["timeout", "120", str(installed), "--help"], capture_output=True, text=True)
        assert result.returncode == 0 and "Taxonomy:" in result.stdout, result.stderr
    result = subprocess.run(["timeout", "120", sys.executable, "-m", "specir.cli", "--help"], capture_output=True, text=True)
    assert result.returncode == 0 and "Taxonomy:" in result.stdout, result.stderr


def _run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(["timeout", "600", *command], capture_output=True, text=True, **kwargs)


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv is not installed: no backend to build the wheel and the venv")
@pytest.mark.skipif(not (SLDB_SOURCE / "pyproject.toml").is_file(), reason=f"sldb sources not found at {SLDB_SOURCE}")
def test_the_package_installs_in_a_clean_environment_and_starts_without_spec2viz(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    shutil.copy(PROJECT / "pyproject.toml", project / "pyproject.toml")
    shutil.copytree(PROJECT / "src" / "specir", project / "src" / "specir", ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
    built = _run(["uv", "build", "--wheel", "--offline", "--out-dir", str(tmp_path / "dist"), str(project)])
    assert built.returncode == 0, built.stderr[-800:]
    wheel = next((tmp_path / "dist").glob("specir-*.whl"))

    venv = tmp_path / "venv"
    created = _run(["uv", "venv", "--offline", "--python", sys.executable, str(venv)])
    assert created.returncode == 0, created.stderr[-800:]
    python = venv / "bin" / "python"
    install = ["uv", "pip", "install", "--python", str(python), str(SLDB_SOURCE), str(wheel)]
    installed = _run([*install, "--offline"])  # from uv's cache when it holds every dependency
    if installed.returncode != 0:
        installed = _run(install)
        if installed.returncode != 0 and "network" in installed.stderr.lower():
            pytest.skip(f"the dependencies are neither in uv's cache nor reachable: {installed.stderr[-300:]}")
    assert installed.returncode == 0, installed.stderr[-1500:]

    listed = _run(["uv", "pip", "list", "--python", str(python)])
    assert "spec2viz" not in listed.stdout.lower(), listed.stdout
    no_spec2viz = _run([str(python), "-c", "import spec2viz"], cwd=tmp_path)
    assert no_spec2viz.returncode != 0 and "ModuleNotFoundError" in no_spec2viz.stderr

    specir = venv / "bin" / "specir"
    for args in (["--help"], ["about"], ["diagram", "--help"], ["catalog", "build", "--help"]):
        result = _run([str(specir), *args], cwd=tmp_path)
        assert result.returncode == 0, (args, result.stderr[-800:])
    assert "Taxonomy:" in _run([str(specir), "--help"], cwd=tmp_path).stdout

    out = tmp_path / "out"
    rendered = _run([str(specir), "render", str(SPEC), "--out", str(out), "--renderer", "mermaid"], cwd=tmp_path)
    assert rendered.returncode == 0, rendered.stderr[-800:]
    assert (out / "state.quotation.mmd").read_text(encoding="utf-8")
    # the package that runs is the installed wheel, not the source tree
    where = _run([str(python), "-c", "import specir, sys; print(specir.__file__)"], cwd=tmp_path)
    assert str(venv) in where.stdout, where.stdout
