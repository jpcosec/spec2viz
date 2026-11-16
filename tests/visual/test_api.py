"""The public Python API of specIR's visual layer (IR13d): spec2viz's `tests/test_api.py` ported.

spec2viz's package exported `load`, `validate`, `compile_ir`, `render`, `json_schema`,
`write_json_schema`, `render_to_file`, `with_provenance`, `provenance_header`, `provenance_text`,
`EXT_MAP`, `DEFAULT_RENDERER` and `BaseDiagram`. `load` and `validate` are sldb's (`load_spec` and
`validate_spec` of `sldb.api.notations`, D3) and are used directly, not re-exported by specIR (SV-J01);
the rest is `specir.visual` (SV-J02, SV-J03). Every case of spec2viz's file runs here over the same
fixtures (`fixtures/spec2viz/`), with only the imports changed: `load`/`validate` from sldb, the
models and the IR from `specir.visual`, `ValidationError` from sldb (D3)."""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest
import sldb.api.notations as sldb_notations
from sldb.api.notations import load_spec as load
from sldb.api.notations import validate_spec as validate

import specir.visual as visual
from specir.visual import (
    ActivityDiagram,
    ActivityIR,
    ComponentDiagram,
    ComponentIR,
    DeploymentDiagram,
    DeploymentIR,
    MatrixDiagram,
    MatrixIR,
    SequenceDiagram,
    SequenceIR,
    StateDiagram,
    StateIR,
    compile_ir,
    json_schema,
    render,
    render_to_file,
    write_json_schema,
)

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures" / "spec2viz" / "tests" / "fixtures"
SPEC2VIZ_INIT = HERE.parents[2] / "spec2viz" / "spec2viz" / "__init__.py"

#: What spec2viz's package exported that is sldb's, and the sldb name that replaces it.
FROM_SLDB = {"load": "load_spec", "validate": "validate_spec"}


def _validation_error() -> type[Exception]:
    from sldb.notations import ValidationError  # the error D3 raises (re-exported by sldb.notations)

    return ValidationError


# ── load ──────────────────────────────────────────────────────────────────────


def test_load_sequence():
    assert isinstance(load(FIXTURES / "sequence.create-quotation.yml"), SequenceDiagram)


def test_load_state():
    assert isinstance(load(FIXTURES / "state.quotation.yml"), StateDiagram)


def test_load_component():
    assert isinstance(load(FIXTURES / "component.quotation.yml"), ComponentDiagram)


def test_load_activity():
    assert isinstance(load(FIXTURES / "activity.validation.yml"), ActivityDiagram)


def test_load_deployment():
    assert isinstance(load(FIXTURES / "deployment.runtime.yml"), DeploymentDiagram)


def test_load_matrix():
    assert isinstance(load(FIXTURES / "matrix.quotation-view.yml"), MatrixDiagram)


# ── validate ──────────────────────────────────────────────────────────────────


def test_validate_passes():
    validate(load(FIXTURES / "component.quotation.yml"))


def test_validate_fails():
    with pytest.raises(_validation_error()):
        validate(load(FIXTURES / "invalid" / "unknown_node.yml"))


# ── compile_ir ────────────────────────────────────────────────────────────────


def test_compile_sequence():
    assert isinstance(compile_ir(load(FIXTURES / "sequence.create-quotation.yml")), SequenceIR)


def test_compile_state():
    assert isinstance(compile_ir(load(FIXTURES / "state.quotation.yml")), StateIR)


def test_compile_component():
    assert isinstance(compile_ir(load(FIXTURES / "component.quotation.yml")), ComponentIR)


def test_compile_activity():
    assert isinstance(compile_ir(load(FIXTURES / "activity.validation.yml")), ActivityIR)


def test_compile_deployment():
    assert isinstance(compile_ir(load(FIXTURES / "deployment.runtime.yml")), DeploymentIR)


def test_compile_matrix():
    assert isinstance(compile_ir(load(FIXTURES / "matrix.quotation-view.yml")), MatrixIR)


# ── render ────────────────────────────────────────────────────────────────────


def test_render_str():
    ir = compile_ir(load(FIXTURES / "sequence.create-quotation.yml"))
    assert "@startuml" in render(ir)


def test_render_dict():
    ir = compile_ir(load(FIXTURES / "matrix.quotation-view.yml"))
    assert isinstance(render(ir), dict)


def test_render_mermaid_override():
    ir = compile_ir(load(FIXTURES / "state.quotation.yml"))
    assert "stateDiagram-v2" in render(ir, renderer="mermaid")


# ── render_to_file ────────────────────────────────────────────────────────────


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
    assert "[*] -->" in p.read_text()


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


# ── json_schema ───────────────────────────────────────────────────────────────


def test_json_schema_for_all_types():
    schema = json_schema()

    assert "$defs" in schema
    assert "SequenceDiagram" in schema["$defs"]


def test_json_schema_for_specific_type():
    schema = json_schema("sequence")

    assert schema["title"] == "SequenceDiagram"
    assert schema["properties"]["data"]["description"] == "Sequence-specific participants and messages."


def test_write_json_schema(tmp_path):
    path = write_json_schema(tmp_path / "sequence.schema.json", diagram_type="sequence")

    assert path.exists()
    assert json.loads(path.read_text())["title"] == "SequenceDiagram"


# ── the API covers spec2viz's ─────────────────────────────────────────────────


def spec2viz_public_names() -> set[str]:
    """The public names spec2viz's `__init__` defines or imports (read from its source, not imported)."""
    tree = ast.parse(SPEC2VIZ_INIT.read_text(encoding="utf-8"))
    names = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("spec2viz"):
            names |= {alias.asname or alias.name for alias in node.names}
    return {name for name in names if not name.startswith("_")}


def test_every_public_name_of_spec2viz_has_its_equivalent():
    if not SPEC2VIZ_INIT.is_file():
        pytest.skip(f"spec2viz sources not found at {SPEC2VIZ_INIT}")
    names = spec2viz_public_names()
    assert {"load", "validate", "compile_ir", "render", "render_to_file", "json_schema", "write_json_schema"} <= names
    for name in sorted(names):
        if name in FROM_SLDB:
            assert callable(getattr(sldb_notations, FROM_SLDB[name])), name
            assert name not in visual.__all__ and FROM_SLDB[name] not in visual.__all__, f"specIR re-exports sldb's {name}"
        else:
            assert name in visual.__all__ and getattr(visual, name) is not None, name


def test_every_name_of_the_public_api_resolves():
    for name in visual.__all__:
        assert hasattr(visual, name), name
    assert visual.EXT_MAP.keys() == visual.RENDERER_MAP.keys()
    assert set(visual.DEFAULT_RENDERER.values()) <= set(visual.RENDERER_MAP)


def test_the_api_renders_a_catalog_and_lints_mermaid(tmp_path):
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("title: Demo\nvistas:\n  - id: sample\n    title: Sample\n    src: view.mmd\n", encoding="utf-8")
    out = visual.build_catalog(config, tmp_path / "catalog.html")
    assert out.read_text(encoding="utf-8") == visual.render_catalog(config)
    assert "window.SPECIR_ANNOTATIONS" in visual.render_catalog(config, annotations=visual.AnnotationsTarget(server="http://127.0.0.1:1"))
    text = visual.render(compile_ir(load(FIXTURES / "state.quotation.yml")), "mermaid")
    assert visual.lint_mermaid(text, check_html=True) == []
    with pytest.raises(visual.MermaidLintError):
        visual.assert_mermaid_ok("graph TD\nA[<b>x</b>]-->B\n", source="bad.mmd")


def test_the_provenance_helpers_name_specir(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "s.yml").write_text("x", encoding="utf-8")
    assert visual.provenance_text("s.yml").startswith("specir: generated from s.yml;")
    assert visual.provenance_header("plantuml", "s.yml").startswith("' specir:")
    assert visual.with_provenance("d2", "s.yml", "a -> b\n").startswith("# specir:")
