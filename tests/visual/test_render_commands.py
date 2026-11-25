"""Rendering through the API and the commands (SV-C01, SV-C04, SV-C05, SV-C10 to SV-C12, SV-C15).

Ported from spec2viz (revision 2de1056), over the same fixtures (`fixtures/spec2viz/`):

- `tests/test_api.py`: `test_render_str`, `test_render_dict`, `test_render_mermaid_override` and the
  seven `test_render_to_file_*` (on `specir.visual.render_file.render_to_file`).
- `tests/test_cli.py`: every `test_render_*` (on `diagram render`, the command the top-level alias of
  IR13d calls) and `test_rendered_text_projections_carry_a_provenance_header`, whose header now names
  sldb's command (`sldb notations validate`).
- `tests/test_rendering_bug.py`: `test_direct_render_to_file`."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner
from sldb.api.notations import load_spec as load

from specir.cli import main
from specir.visual.compilers import compile_ir
from specir.visual.render_file import provenance_header, render_to_file
from specir.visual.renderers import render

sys.path.insert(0, str(Path(__file__).resolve().parent))

CORPUS = Path(__file__).resolve().parent / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLES = CORPUS / "examples"
runner = CliRunner()


# ── tests/test_api.py ───────────────────────────────────────────────────────────────────────────


def test_render_str():
    ir = compile_ir(load(FIXTURES / "sequence.create-quotation.yml"))
    assert "@startuml" in render(ir)


def test_render_dict():
    ir = compile_ir(load(FIXTURES / "matrix.quotation-view.yml"))
    assert isinstance(render(ir), dict)


def test_render_mermaid_override():
    ir = compile_ir(load(FIXTURES / "state.quotation.yml"))
    assert "stateDiagram-v2" in render(ir, renderer="mermaid")


def test_render_to_file_puml(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "@startuml" in p.read_text()


def test_render_to_file_vega(tmp_path):
    p = render_to_file(FIXTURES / "matrix.quotation-view.yml", out=tmp_path)
    assert p.name.endswith(".vega.json")
    assert "$schema" in json.loads(p.read_text())


def test_render_to_file_state(tmp_path):
    p = render_to_file(FIXTURES / "state.quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "[*] --> browsing" in p.read_text()


def test_render_to_file_activity(tmp_path):
    p = render_to_file(FIXTURES / "activity.validation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "start" in p.read_text()


def test_render_to_file_deployment(tmp_path):
    p = render_to_file(FIXTURES / "deployment.runtime.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "Browser" in p.read_text()


def test_render_to_file_component(tmp_path):
    p = render_to_file(FIXTURES / "component.quotation.yml", out=tmp_path)
    assert p.name.endswith(".graph.html")
    assert "QuotationFlow" in p.read_text()


def test_render_to_file_override(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path, renderer="mermaid")
    assert p.suffix == ".mmd"
    assert "sequenceDiagram" in p.read_text()


# ── tests/test_cli.py ───────────────────────────────────────────────────────────────────────────


def _render(*args: str):
    return runner.invoke(main, ["diagram", "render", *args])


def test_render_sequence(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()


def test_render_matrix(tmp_path):
    r = _render(str(FIXTURES / "matrix.quotation-view.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "matrix.quotation-view.vega.json").exists()


def test_render_state(tmp_path):
    r = _render(str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.puml").exists()


def test_render_activity(tmp_path):
    r = _render(str(FIXTURES / "activity.validation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "activity.validation.puml").exists()


def test_render_deployment(tmp_path):
    r = _render(str(FIXTURES / "deployment.runtime.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "deployment.runtime.puml").exists()


def test_render_component(tmp_path):
    r = _render(str(FIXTURES / "component.quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "component.quotation.graph.html").exists()


def test_render_override(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path), "--renderer", "mermaid")
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.mmd").exists()


def test_render_backend_alias(tmp_path):
    r = _render(str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path), "--backend", "mermaid")
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.mmd").exists()


def test_render_multiple(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()
    assert (tmp_path / "state.quotation.puml").exists()


def test_render_invalid_fails(tmp_path):
    r = _render(str(FIXTURES / "invalid" / "unknown_node.yml"), "--out", str(tmp_path))
    assert r.exit_code != 0
    assert r.output.startswith("Error: ")


def test_render_help_lists_the_renderers():
    """The renderer part of `test_help_mentions_taxonomy_groups_and_renderers` (the rest is IR13d's)."""
    r = runner.invoke(main, ["diagram", "render", "--help"])
    assert r.exit_code == 0
    for name in ["plantuml", "mermaid", "vega", "d2", "antonia-html", "json"]:
        assert name in r.output
    r = runner.invoke(main, ["diagram", "--help"])
    assert r.exit_code == 0
    assert "render" in r.output and "validate" not in r.output and "schema" in r.output and "lint" in r.output


def test_render_d2(tmp_path):
    r = _render(str(FIXTURES / "component.quotation.yml"), "--out", str(tmp_path), "--renderer", "d2")
    assert r.exit_code == 0
    assert (tmp_path / "component.quotation.d2").exists()


def test_render_antonia_html(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path), "--renderer", "antonia-html")
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.html").exists()


def test_render_json_reflection_artifact(tmp_path):
    r = _render(str(EXAMPLES / "reflection" / "canonical.yml"), "--out", str(tmp_path), "--renderer", "json")
    assert r.exit_code == 0
    assert (tmp_path / "canonical.artifact.json").exists()


def test_rendered_text_projections_carry_a_provenance_header(tmp_path, monkeypatch):
    """Una proyeccion generada dice de que spec sale y como se valida; el JSON no lleva cabecera."""
    monkeypatch.chdir(CORPUS)
    spec = Path("examples/component/example.yml")
    for renderer, prefix in (("mermaid", "%%"), ("plantuml", "'"), ("d2", "#")):
        text = render_to_file(spec, out=tmp_path, renderer=renderer).read_text(encoding="utf-8")
        lines = text.splitlines()
        # en mermaid el frontmatter de config (ELK) va primero; la cabecera, justo despues
        first = lines[lines.index("---", 1) + 1] if renderer == "mermaid" else lines[0]
        assert first.startswith(f"{prefix} specir: generated from examples/component/example.yml;")
        assert "`sldb notations validate examples/component/example.yml`" in first
    assert provenance_header("vega", spec) == "" and provenance_header("json", spec) == ""
    matrix = render_to_file(Path("tests/fixtures/matrix.quotation-view.yml"), out=tmp_path, renderer="vega").read_text(encoding="utf-8")
    assert matrix.lstrip().startswith("{")


def test_the_header_names_a_command_that_validates(tmp_path, monkeypatch):
    """The command the provenance header names exists and validates the spec."""
    monkeypatch.chdir(CORPUS)
    sldb = str(Path(sys.executable).with_name("sldb"))
    ok = subprocess.run([sldb, "notations", "validate", "examples/component/example.yml"], capture_output=True, text=True)
    assert ok.returncode == 0, ok.stderr
    bad = subprocess.run([sldb, "notations", "validate", "tests/fixtures/invalid/unknown_node.yml"], capture_output=True, text=True)
    assert bad.returncode == 1, bad.stdout


# ── tests/test_rendering_bug.py ─────────────────────────────────────────────────────────────────


def test_direct_render_to_file(tmp_path):
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    fixture_path = fixture_dir / "canonical.yml"
    fixture_path.write_text("""
id: canonical-arch
title: Canonical Architecture
type: component
version: "1.0"
data:
  nodes:
    core: {label: Core, kind: internal}
    api: {label: API, kind: boundary}
  edges:
    - {from: api, to: core, relation: uses}
""")
    out_dir = tmp_path / "out"
    output_path = render_to_file(fixture_path, out=out_dir, renderer="mermaid")
    assert output_path.exists()
    assert "flowchart TD" in output_path.read_text()
    assert "core" in output_path.read_text()
    assert "api" in output_path.read_text()
