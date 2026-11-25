"""The render cases of spec2viz (revision 2de1056) that live outside `tests/test_renderers.py`, ported to
specIR over the same fixtures (`fixtures/spec2viz/`):

- `tests/test_class_diagram.py` and `tests/test_class_packages.py`: the cases that render (SV-B03,
  SV-C13). Their validation cases are D3's (sldb) and their sync case is D1's.
- `tests/test_activity_lanes.py` and `tests/test_deployment_nested.py`: the cases that render
  (SV-C02 to SV-C04, SV-C11). Their validation and sync cases are sldb's (D3, D1).
- `tests/test_catalog_resolved_views.py`: the four `view_to_mermaid` cases (SV-C14), over the view
  that sldb resolves (`sldb.api.notations.resolve_view`) from a spec synced with sldb's `SpecSync`
  into a fresh store. Its `catalog build` cases are IR13b's.
- `tests/test_exceptions.py`: the asserts on `Spec2VizError`, `CompileError` and `RenderError`
  (SV-A14). Those on `ParseError` and `ValidationError` are D3's.

The cases that need the real mermaid engine (mmdc) skip when it is not installed, as in spec2viz."""

from __future__ import annotations

import html as _html
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml
from sldb.api.notations import load_spec as load
from sldb.api.notations import validate_spec as validate

from specir.visual.compilers import compile_ir
from specir.visual.exceptions import CompileError, RenderError, Spec2VizError
from specir.visual.ir import ClassIR
from specir.visual.lint_mermaid import MermaidLintError, lint_mermaid, mmdc_path
from specir.visual.renderers import render
from specir.visual.renderers.antonia_html import AntoniaHtmlRenderer
from specir.visual.renderers.class_diagram import render_mermaid_class, render_plantuml_class
from specir.visual.renderers.d2 import D2Renderer
from specir.visual.renderers.mermaid import MermaidRenderer
from specir.visual.renderers.plantuml import PlantUMLRenderer
from specir.visual.renderers.view_mermaid import view_to_mermaid
from specir.visual.spec_models import ClassDiagram

sys.path.insert(0, str(Path(__file__).resolve().parent))

CORPUS = Path(__file__).resolve().parent / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLE = CORPUS / "examples" / "class" / "runtime.yml"
PACKAGES = FIXTURES / "class.packages.yml"
LANES = FIXTURES / "activity.lanes.yml"
NESTED = FIXTURES / "deployment.nested.yml"
requires_mmdc = pytest.mark.skipif(mmdc_path() is None, reason="mmdc (mermaid-cli) not installed")


def _valid_ir(path: Path):
    diagram = load(path)
    validate(diagram)
    return compile_ir(diagram)


# ── tests/test_class_diagram.py ─────────────────────────────────────────────────────────────────


def test_schema_and_compiler_preserve_structured_signatures():
    from specir.visual.schema import json_schema

    ir = _valid_ir(EXAMPLE)
    assert isinstance(ir, ClassIR)
    method = ir.classes[0].methods[0]
    assert method.name == "execute"
    assert [(p.name, p.type) for p in method.parameters] == [("context", "ExecutionContext"), ("input", "PortValues")]
    assert method.returns == "ExecutionResult"
    assert ir.classes[1].attributes[0].visibility == "private"
    assert ir.relations[1].to_multiplicity == "1"
    schema = json_schema("class")
    assert schema["properties"]["type"]["const"] == "class"
    assert schema["$defs"]["ClassMethod"]["additionalProperties"] is False
    assert "class" in json_schema()["discriminator"]["mapping"]


def test_backends_preserve_realization_direction_and_generic_types():
    ir = compile_ir(load(EXAMPLE))
    mermaid = render(ir)
    plantuml = render(ir, "plantuml")
    assert mermaid.startswith("classDiagram")
    assert "DataNode ..|> ExecutableNode" in mermaid
    assert "DataNode ..|> ExecutableNode" in plantuml
    assert "+List~InputPort~ inputs" in mermaid
    assert "+inputs: List<InputPort>" in plantuml
    assert "+execute(context: ExecutionContext, input: PortValues)* ExecutionResult" in mermaid
    assert "{abstract} +execute(context: ExecutionContext, input: PortValues): ExecutionResult" in plantuml


def test_cli_schema_validate_and_render(tmp_path, monkeypatch):
    """`test_cli_schema_validate_render_and_catalog` without its `catalog build` step (IR13b)."""
    from click.testing import CliRunner

    from specir.cli import main

    monkeypatch.setenv("SPECIR_MMDC", "0")
    runner = CliRunner()
    for args in [
        ["diagram", "schema", "--type", "class", "--out", str(tmp_path / "class.schema.json")],
        ["diagram", "render", str(EXAMPLE), "--out", str(tmp_path)],
        ["diagram", "render", str(EXAMPLE), "--backend", "plantuml", "--out", str(tmp_path)],
    ]:
        result = runner.invoke(main, args)
        assert result.exit_code == 0, result.output
    assert (tmp_path / "runtime.mmd").exists()
    assert (tmp_path / "runtime.puml").exists()


@requires_mmdc
def test_real_mermaid_engine_accepts_members_kinds_and_all_relations():
    data = yaml.safe_load(EXAMPLE.read_text())
    data["data"]["classes"]["DataNode"]["attributes"].append(
        {"name": "instances", "type": "Integer", "static": True, "visibility": "protected"})
    data["data"]["classes"]["DataNode"]["methods"].append(
        {"name": "create", "static": True, "returns": "DataNode", "visibility": "package"})
    for kind in ["class", "interface", "abstract", "record", "protocol", "enum"]:
        data["data"]["classes"][f"Kind_{kind}"] = {"kind": kind}
    for relation in ["inheritance", "composition", "aggregation", "association", "dependency"]:
        edge = {"from": "DataNode", "to": "NodeSpec", "relation": relation, "label": "contract & data"}
        if relation != "inheritance":
            edge.update(from_multiplicity="1", to_multiplicity="0..*")
        data["data"]["relations"].append(edge)
    diagram = ClassDiagram.model_validate(data)
    validate(diagram)
    assert lint_mermaid(render(compile_ir(diagram))) == []


# ── tests/test_class_packages.py ────────────────────────────────────────────────────────────────


def test_mermaid_namespaces_by_path_and_colors_classes_by_package_kind():
    out = render_mermaid_class(_valid_ir(PACKAGES))
    lines = [l.strip() for l in out.splitlines()]
    assert "namespace Core.Billing {" in lines and "namespace Core.Identity {" in lines and "namespace Shared {" in lines
    assert "namespace Core {" not in lines  # sin clases propias, el paquete raiz no abre namespace vacio
    assert "classDef pkg0 fill:#fff1c2,stroke:#7a5c00" in lines and 'cssClass "Invoice,Payment" pkg0' in lines
    assert "classDef pkg1 fill:#dbebf4,stroke:#0072b2" in lines and 'cssClass "User" pkg1' in lines
    assert not any("AuditLog" in l for l in lines if l.startswith("cssClass"))


def test_plantuml_nests_packages_with_their_fill():
    out = render_plantuml_class(_valid_ir(PACKAGES))
    assert 'package "Core" as core {\n    package "Billing" as billing #fff1c2 {\n        class "Invoice" as Invoice {' in out
    assert 'package "Shared" as shared {' in out


def test_without_packages_the_output_is_unchanged():
    diagram = load(PACKAGES)
    diagram.data.packages = {}
    diagram.style = None
    out = render_mermaid_class(compile_ir(diagram))
    assert "namespace" not in out and "classDef" not in out


@requires_mmdc
def test_real_mermaid_engine_accepts_the_packages(tmp_path):
    source = tmp_path / "p.mmd"
    source.write_text(render_mermaid_class(_valid_ir(PACKAGES)), encoding="utf-8")
    result = subprocess.run([mmdc_path(), "-i", str(source), "-o", str(tmp_path / "p.svg"), "-q"], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr[-400:]


# ── tests/test_activity_lanes.py ────────────────────────────────────────────────────────────────


def test_mermaid_draws_one_lane_per_partition_merge_as_diamond_and_notes():
    out = MermaidRenderer().render(_valid_ir(LANES))
    lanes = [l.strip() for l in out.splitlines() if l.strip().startswith("subgraph")]
    assert lanes == ['subgraph __lane0 ["Dev"]', 'subgraph __lane1 ["Approver"]', 'subgraph __lane2 ["Script"]', 'subgraph __lane3 ["AWS"]']
    assert 'joined{" "}' in out and 'review{"Approve?"}' in out
    assert 'review__note["Two approvals for production"]:::note' in out and "review -.- review__note" in out
    assert "classDef note" in out


def test_mermaid_without_the_new_fields_is_unchanged():
    out = MermaidRenderer().render(_valid_ir(FIXTURES / "activity.validation.yml"))
    assert "subgraph" not in out and "note" not in out
    assert out.splitlines()[:8] == ["---", "config:", "  layout: elk", "  flowchart:", "    curve: linear", "---", "flowchart TD", "    __start([Start])"]


def test_plantuml_swimlanes_and_note():
    out = PlantUMLRenderer().render(_valid_ir(LANES))
    lines = out.splitlines()
    assert lines[:3] == ["@startuml", "|Dev|", "start"]
    assert "|Approver|" in lines and "note right: Two approvals for production" not in lines  # la nota es de una decision
    assert "|Script|" in lines


def test_plantuml_note_on_an_action():
    diagram = load(LANES)
    diagram.data.steps["deploy"].notes = "Blue/green"
    out = PlantUMLRenderer().render(compile_ir(diagram))
    assert ":Deploy;\nnote right: Blue/green" in out


def test_d2_lanes_are_containers_and_edges_use_qualified_ids():
    out = D2Renderer().render(_valid_ir(LANES))
    assert '__lane0: "Dev"' in out and '__lane0.open_pr: "Open pull request"' in out
    assert "__lane2.joined.shape: diamond" in out and "__lane0.open_pr -> __lane1.review" in out
    assert "__lane1.review__note.shape: page" in out


# ── tests/test_deployment_nested.py ─────────────────────────────────────────────────────────────


def test_mermaid_nests_subgraphs_and_marks_deploy_and_manifest():
    out = MermaidRenderer().render(_valid_ir(NESTED))
    lines = out.splitlines()
    order = [l.strip() for l in lines if l.strip().startswith("subgraph")]
    assert order == ['subgraph vpc ["VPC"]', 'subgraph subnet ["Private subnet"]', 'subgraph cluster ["ECS cluster"]', 'subgraph db ["Postgres"]', 'subgraph edge ["CDN"]']
    assert '            subgraph cluster ["ECS cluster"]' in lines and '                api_service["api service"]' in lines
    assert '    cluster -->|"queries · :5432"| db' in lines and '    edge -->|"HTTPS"| cluster' in lines
    assert '    api_image -.->|"«deploy»"| cluster' in lines and '    api_image -.->|"«manifest»"| api_service' in lines


def test_plantuml_and_d2_nest_and_d2_edges_use_container_paths():
    puml = PlantUMLRenderer().render(_valid_ir(NESTED))
    assert 'node "VPC" as vpc {\n  node "Private subnet" as subnet {\n    node "ECS cluster" as cluster {' in puml
    assert "api_image ..> cluster : «deploy»" in puml
    d2 = D2Renderer().render(_valid_ir(NESTED))
    assert 'vpc.subnet.cluster.api_service: "api service"' in d2
    assert 'edge -> vpc.subnet.cluster: "HTTPS"' in d2 and "api_image -> vpc.subnet.cluster: \"«deploy»\" {style.stroke-dash: 3}" in d2


def test_antonia_html_draws_every_connection_of_a_deployment():
    ir = _valid_ir(NESTED)
    page = AntoniaHtmlRenderer().render(ir)
    source = _html.unescape(re.search(r'<pre class="mermaid">(.*?)</pre>', page, re.S).group(1))
    expected = MermaidRenderer().render(ir)
    assert source.strip() == expected.strip()
    arrows = [l for l in source.splitlines() if re.search(r"\s(-->|-\.->)", l)]
    connections = yaml.safe_load(NESTED.read_text(encoding="utf-8"))["data"]["connections"]
    assert len(arrows) == len(connections) > 0


# ── tests/test_catalog_resolved_views.py (view_to_mermaid) ──────────────────────────────────────

NOTATION = {
    "name": "infra-own", "title": "Infra", "diagram_type": "deployment", "layout": {"kind": "graph", "direction": "LR"},
    "glyphs": [
        {"id": "db", "model": "SpecNodeDoc", "where": 'kind = "database"', "shape": "cylinder", "keyword": "«{kind}»", "fill": {"light": "#fff1c2", "dark": "#3d3200"}},
        {"id": "node", "model": "SpecNodeDoc", "where": 'collection = "nodes"', "shape": "node-box", "keyword": "«node»"},
        {"id": "any", "model": "SpecNodeDoc", "shape": "rounded-box"},
    ],
    "links": [
        {"id": "contains", "relation": "contains", "draw": "nest"},
        {"id": "deploy", "relation": "deploy", "line": "dashed", "label": "«deploy»"},
        {"id": "any", "relation": "*", "color": "#0072b2", "target_end": "none", "label": "{data.protocol}"},
    ],
}


def resolved_view(tmp_path: Path, spec: Path = NESTED, notation: Path | None = None) -> dict:
    """The view sldb resolves for `spec` once sldb's SpecSync wrote it into a fresh store."""
    import sldb.api as sldb_api
    from sldb.api.notations import SpecSync, resolve_view

    root = tmp_path / "scratch"
    sldb_api.init_store(root)
    (root / "docs").mkdir()
    copy = Path(shutil.copy(spec, root / "docs" / spec.name))
    report = SpecSync(root / ".sldb").sync(copy, notation=notation)
    return resolve_view(root / ".sldb", report.spec_id)


def _notation(tmp_path: Path) -> Path:
    path = tmp_path / "infra-own.yml"
    path.write_text(yaml.safe_dump(NOTATION, allow_unicode=True), encoding="utf-8")
    return path


def test_view_to_mermaid_uses_glyph_shape_keyword_style_nesting_and_links(tmp_path):
    out = view_to_mermaid(resolved_view(tmp_path, notation=_notation(tmp_path)), theme="dark")
    lines = [l.strip() for l in out.splitlines()]
    assert out.startswith("---\nconfig:\n  layout: elk\n") and "flowchart LR" in lines
    assert any(l.startswith("subgraph ") and "«node»<br/>VPC" in l for l in lines)
    assert any('[("«database»<br/>Postgres")]' in l for l in lines)
    assert any(l.startswith("style ") and "fill:#3d3200" in l and "color:#e6edf3" in l for l in lines)
    assert any(l.startswith("linkStyle ") and "stroke:#0072b2" in l for l in lines)
    assert any("-.->|\"«deploy»\"|" in l for l in lines) and any("---|\"HTTPS\"|" in l for l in lines)


def test_view_to_mermaid_compartments_and_pseudonodes(tmp_path):
    klass = view_to_mermaid(resolved_view(tmp_path, PACKAGES))
    assert "<hr/>id: int<br/>total: Decimal" in klass and "@{ shape: notch-rect" not in klass
    act = view_to_mermaid(resolved_view(tmp_path / "a", LANES))
    assert "@{ shape: sm-circ }" in act and "@{ shape: fr-circ }" in act and '{" "}' in act


def test_view_to_mermaid_refuses_non_graph_layouts(tmp_path):
    view = resolved_view(tmp_path, CORPUS / "docs" / "architecture" / "spec2viz" / "sequence-sync-pipeline.yml")
    with pytest.raises(ValueError, match="not a graph"):
        view_to_mermaid(view)


@requires_mmdc
def test_view_to_mermaid_is_accepted_by_the_real_engine(tmp_path):
    for name, spec in (("dep", NESTED), ("cls", PACKAGES), ("act", LANES)):
        source = tmp_path / f"{name}.mmd"
        source.write_text(view_to_mermaid(resolved_view(tmp_path / name, spec, _notation(tmp_path) if name == "dep" else None)), encoding="utf-8")
        result = subprocess.run([mmdc_path(), "-i", str(source), "-o", str(tmp_path / f"{name}.svg"), "-q"], capture_output=True, text=True, timeout=120)
        assert result.returncode == 0, (name, result.stderr[-300:])


# ── tests/test_exceptions.py (the visual layer's errors) ────────────────────────────────────────


def test_exception_hierarchy():
    assert issubclass(CompileError, Spec2VizError)
    assert issubclass(RenderError, Spec2VizError)
    assert issubclass(MermaidLintError, RenderError)


def test_exceptions_are_catchable_as_base():
    with pytest.raises(Spec2VizError):
        raise RenderError("cannot render")
