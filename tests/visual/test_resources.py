"""Resources that specIR's visual layer packages (SV-C07, SV-C10, SV-J04, SV-J05, SV-G08 for the template).

- The catalog template (`templates/default.html`) and the vendored bpmn-js
  (`templates/vendor/bpmn-js/`) are package data of specIR: the installed package reads them, a wheel
  built from the project carries them, and they are spec2viz's own bytes (live, when installed).
- The pages that must open from `file://` with nothing from outside (the offline BPMN viewer and the
  graph HTML; the tree HTML too) reference no external script, stylesheet, font or import; the
  viewer inlines the vendored bpmn-js and its two stylesheets.
- `test_examples_render_successfully` of spec2viz's `tests/test_packaging.py`, over the same
  examples (`fixtures/spec2viz/examples/`)."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import zipfile
from importlib.resources import files
from pathlib import Path

import pytest

from specir.visual.render_file import render_to_file
from specir.visual.renderers.bpmn_viewer import VENDOR_DIR

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import render_parity  # noqa: E402

PROJECT = HERE.parents[1]
CORPUS = HERE / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLES = CORPUS / "examples"
VENDOR = ("LICENSE", "README.md", "bpmn-js.css", "bpmn-navigated-viewer.production.min.js", "diagram-js.css")
RESOURCES = ("templates/default.html", *(f"templates/vendor/bpmn-js/{name}" for name in VENDOR))
#: What would make a page fetch something to open: a script by URL, a stylesheet or font link, a CSS
#: import, a CSS url() to the network, or any `src` (image, frame) to the network. A link the reader
#: may follow (`<a href>`, like bpmn.io's watermark inside bpmn-js) fetches nothing.
EXTERNAL = re.compile(r"<script[^>]*\bsrc=|<link\b|@import|url\(\s*['\"]?(?:https?:)?//|\bsrc=['\"]?(?:https?:)?//", re.I)


def _resource(rel: str):
    return files("specir.visual").joinpath(*rel.split("/"))


def test_the_installed_package_reads_its_resources():
    for rel in RESOURCES:
        assert _resource(rel).is_file(), rel
        assert _resource(rel).read_bytes(), rel
    assert Path(str(_resource("templates/vendor/bpmn-js"))) == VENDOR_DIR
    readme = _resource("templates/vendor/bpmn-js/README.md").read_text(encoding="utf-8")
    js = _resource("templates/vendor/bpmn-js/bpmn-navigated-viewer.production.min.js").read_text(encoding="utf-8")
    version = re.search(r"`bpmn-js` (\d+\.\d+\.\d+)", readme).group(1)
    assert f"bpmn-navigated-viewer v{version}" in js


@pytest.mark.parity
def test_resources_are_spec2viz_bytes():
    pytest.importorskip("spec2viz")
    origin = render_parity.spec2viz_package_dir()
    for rel in RESOURCES:
        assert _resource(rel).read_bytes() == (origin / rel).read_bytes(), rel


@pytest.mark.skipif(shutil.which("uv") is None, reason="uv is not installed: no backend to build the wheel")
def test_a_wheel_of_the_project_carries_the_resources(tmp_path):
    """The package data is declared (pyproject.toml), not only present in the source tree."""
    project = tmp_path / "project"
    project.mkdir()
    shutil.copy(PROJECT / "pyproject.toml", project / "pyproject.toml")
    shutil.copytree(PROJECT / "src" / "specir", project / "src" / "specir", ignore=shutil.ignore_patterns("__pycache__", "*.egg-info"))
    result = subprocess.run(
        ["uv", "build", "--wheel", "--offline", "--out-dir", str(tmp_path / "dist"), str(project)],
        capture_output=True, text=True, timeout=300,
    )
    assert result.returncode == 0, result.stderr[-800:]
    wheel = next((tmp_path / "dist").glob("specir-*.whl"))
    names = set(zipfile.ZipFile(wheel).namelist())
    for rel in RESOURCES:
        assert f"specir/visual/{rel}" in names, rel


def test_bpmn_viewer_opens_without_external_resources(tmp_path):
    out = render_to_file(FIXTURES / "activity.mepu-decision.yml", out=tmp_path, renderer="bpmn")
    page = out.with_name(out.name + ".html").read_text(encoding="utf-8")
    assert not EXTERNAL.search(page), EXTERNAL.search(page)
    for name in ("bpmn-js.css", "diagram-js.css"):
        css = (VENDOR_DIR / name).read_text(encoding="utf-8")
        assert css.strip()[:200] in page, name
    js = (VENDOR_DIR / "bpmn-navigated-viewer.production.min.js").read_text(encoding="utf-8")
    assert js[:200] in page and len(page) > len(js)


@pytest.mark.parametrize("renderer, spec", [("graph", "component.quotation.yml"), ("tree", "component.quotation.yml")])
def test_component_html_opens_without_external_resources(tmp_path, renderer, spec):
    page = render_to_file(FIXTURES / spec, out=tmp_path, renderer=renderer).read_text(encoding="utf-8")
    assert page.lstrip().lower().startswith("<!doctype html")
    assert not EXTERNAL.search(page), EXTERNAL.search(page)
    assert "QuotationFlow" in page


# ── tests/test_packaging.py ─────────────────────────────────────────────────────────────────────


def test_examples_render_successfully(tmp_path):
    example_paths = [
        path
        for path in sorted(EXAMPLES.glob("**/*.yml"))
        if "/catalog/" not in path.as_posix() and path.name not in {"project.yml", "vistas.yml"}
    ]

    assert example_paths

    for example_path in example_paths:
        output_path = render_to_file(example_path, out=tmp_path)
        assert output_path.exists(), f"missing output for {example_path}"
