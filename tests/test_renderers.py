import json
import pytest
from pathlib import Path
from spec2viz.loader import load
from spec2viz.compilers import compile_ir
from spec2viz.renderers import render
from spec2viz.renderers.plantuml import PlantUMLRenderer
from spec2viz.renderers.vega import VegaRenderer
from spec2viz.renderers.mermaid import MermaidRenderer
from spec2viz.exceptions import RenderError
from spec2viz.ir import SequenceIR, MatrixIR

FIXTURES = Path("tests/fixtures")


def _ir(name):
    return compile_ir(load(FIXTURES / name))


# ── PlantUML ──────────────────────────────────────────────────────────────────


def test_sequence_puml():
    out = PlantUMLRenderer().render(_ir("sequence.create-quotation.yml"))
    assert "@startuml" in out and "@enduml" in out
    assert "actor User" in out
    assert "User -> QuotationFlow" in out


def test_state_puml():
    out = PlantUMLRenderer().render(_ir("state.quotation.yml"))
    assert "[*] --> browsing" in out
    assert "select_client" in out
    assert "all validations passed" in out


def test_component_puml():
    out = PlantUMLRenderer().render(_ir("component.quotation.yml"))
    assert "@startuml" in out
    assert "QuotationFlow" in out
    assert "skinparam component<<core>> BackgroundColor" in out
    assert 'rectangle "Store" as Store <<boundary>>' in out


def test_component_puml_uses_yaml_style_overrides():
    out = PlantUMLRenderer().render(_ir("component.styled.yml"))
    assert "skinparam component<<core>> BackgroundColor #112233" in out
    assert "skinparam component<<core>> BorderColor #445566" in out
    assert "skinparam component<<core>> FontColor #778899" in out


def test_component_puml_nests_children_without_redefining_them():
    out = PlantUMLRenderer().render(_ir("component.quotation.yml"))
    assert out.count('rectangle "Store" as Store <<boundary>>') == 1
    assert out.count('package "QuotationFlow" as QuotationFlow <<core>> {') == 1


def test_activity_puml():
    out = PlantUMLRenderer().render(_ir("activity.validation.yml"))
    assert "start" in out and "stop" in out
    assert "Load basket" in out
    assert "if (" in out


def test_activity_complex_puml():
    out = PlantUMLRenderer().render(_ir("activity.complex.yml"))
    assert out.count("if (") == 2
    assert "Load data" in out
    assert "Save result" in out
    assert "Show auth error" in out
    assert "Show data error" in out


def test_activity_complex_mermaid():
    out = MermaidRenderer().render(_ir("activity.complex.yml"))
    assert out.count("{") == 2
    assert "Load data" in out
    assert "Save result" in out
    assert "Show auth error" in out
    assert "Show data error" in out


def test_deployment_puml():
    out = PlantUMLRenderer().render(_ir("deployment.runtime.yml"))
    assert "Browser" in out
    assert "HTTPS" in out


# ── Vega ──────────────────────────────────────────────────────────────────────


def test_vega_schema():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    assert spec["$schema"].startswith("https://vega.github.io/schema/vega/")


def test_vega_data_sections():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    names = {d["name"] for d in spec["data"]}
    assert {"stages", "rows", "spans", "stageBoundaries"} <= names


def test_vega_stages():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    stages = next(d for d in spec["data"] if d["name"] == "stages")["values"]
    assert [s["id"] for s in stages] == [
        "browse",
        "client",
        "basket",
        "validation",
        "completed",
    ]


def test_vega_spans():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    spans = next(d for d in spec["data"] if d["name"] == "spans")["values"]
    qf = next(s for s in spans if s["component"] == "QuotationFlow")
    assert qf["start"] == 0 and qf["end"] == 5


def test_vega_rows():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    rows = next(d for d in spec["data"] if d["name"] == "rows")["values"]
    ids = [r["id"] for r in rows]
    assert "QuotationFlow" in ids
    depths = {r["id"]: r["depth"] for r in rows}
    assert depths["QuotationFlow"] == 0
    assert depths["BasketItem"] > depths["Basket"]


def test_vega_signals():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    names = {s["name"] for s in spec["signals"]}
    assert {"left", "top", "cellWidth", "rowHeight", "barPadding"} <= names


def test_vega_scales():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    assert any(s["name"] == "kindColor" for s in spec["scales"])


def test_vega_marks_types():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    types = {m["type"] for m in spec["marks"]}
    assert {"text", "rect", "rule"} <= types


def test_vega_rejects_wrong_ir():
    ir = _ir("sequence.create-quotation.yml")
    with pytest.raises(RenderError):
        VegaRenderer().render(ir)


def test_plantuml_rejects_matrix():
    ir = _ir("matrix.quotation-view.yml")
    with pytest.raises(RenderError):
        PlantUMLRenderer().render(ir)


def test_mermaid_rejects_matrix():
    ir = _ir("matrix.quotation-view.yml")
    with pytest.raises(RenderError):
        MermaidRenderer().render(ir)


# ── Mermaid ───────────────────────────────────────────────────────────────────


def test_mermaid_sequence():
    out = MermaidRenderer().render(_ir("sequence.create-quotation.yml"))
    assert "sequenceDiagram" in out
    assert "User" in out


def test_mermaid_state():
    out = MermaidRenderer().render(_ir("state.quotation.yml"))
    assert "stateDiagram-v2" in out
    assert "[*] --> browsing" in out


def test_mermaid_component():
    out = MermaidRenderer().render(_ir("component.quotation.yml"))
    assert "graph TD" in out
    assert "QuotationFlow" in out


def test_mermaid_activity():
    out = MermaidRenderer().render(_ir("activity.validation.yml"))
    assert "flowchart TD" in out
    assert "Load basket" in out


def test_mermaid_deployment():
    out = MermaidRenderer().render(_ir("deployment.runtime.yml"))
    assert "graph TD" in out
    assert "Browser" in out
    assert "HTTPS" in out


# ── Dispatch ──────────────────────────────────────────────────────────────────


def test_render_dispatch_plantuml():
    out = render(_ir("sequence.create-quotation.yml"))
    assert isinstance(out, str) and "@startuml" in out


def test_render_dispatch_vega():
    out = render(_ir("matrix.quotation-view.yml"))
    assert isinstance(out, dict) and "$schema" in out


def test_render_dispatch_override():
    out = render(_ir("sequence.create-quotation.yml"), renderer="mermaid")
    assert "sequenceDiagram" in out
