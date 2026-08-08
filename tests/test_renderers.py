import json
import pytest
from pathlib import Path
from spec2viz.loader import load
from spec2viz.compilers import compile_ir
from spec2viz.renderers import render
from spec2viz.renderers.plantuml import PlantUMLRenderer
from spec2viz.renderers.vega import VegaRenderer
from spec2viz.renderers.mermaid import MermaidRenderer
from spec2viz.renderers.d2 import D2Renderer
from spec2viz.renderers.antonia import AntoniaHtmlRenderer
from spec2viz.renderers import JsonRenderer
from spec2viz.exceptions import RenderError
from spec2viz.ir import DeploymentArtifact, DeploymentConnection, DeploymentIR, DeploymentNode, SequenceIR, MatrixIR

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


# ── D2 / HTML / JSON ──────────────────────────────────────────────────────────


def test_d2_sequence():
    out = D2Renderer().render(_ir("sequence.create-quotation.yml"))
    assert "direction: right" in out
    assert "User -> QuotationFlow: open quotation flow" in out


def test_d2_state():
    out = D2Renderer().render(_ir("state.quotation.yml"))
    assert "browsing -> client_selected: select_client" in out


def test_d2_component():
    out = D2Renderer().render(_ir("component.quotation.yml"))
    assert 'QuotationFlow: "QuotationFlow"' in out
    assert 'QuotationFlow.ClientSelection: "ClientSelection"' in out


def test_d2_activity():
    out = D2Renderer().render(_ir("activity.validation.yml"))
    assert "__start: Start" in out
    assert "check_validity.shape: diamond" in out
    assert "__end: End" in out


def test_d2_deployment():
    out = D2Renderer().render(_ir("deployment.runtime.yml"))
    assert 'browser.quotation_ui: "Quotation UI"' in out
    assert 'quotation_ui -> quotation_api: "HTTPS"' in out


def test_d2_and_mermaid_deployment_without_protocol():
    ir = DeploymentIR(
        title="runtime",
        nodes=[DeploymentNode(id="n1", label="N1", kind="server")],
        artifacts=[],
        connections=[DeploymentConnection(from_="a", to="b")],
    )
    assert "a -> b" in D2Renderer().render(ir)
    assert "a --> b" in MermaidRenderer().render(ir)


def test_d2_rejects_matrix():
    with pytest.raises(RenderError):
        D2Renderer().render(_ir("matrix.quotation-view.yml"))


def test_plantuml_sequence_message_condition_and_group():
    from spec2viz.ir import SequenceIR, Participant, Message
    ir = SequenceIR(
        title="Test",
        participants=[Participant(id="A"), Participant(id="B")],
        messages=[
            Message(from_="A", to="B", message="hello", condition="cond1", group="g1"),
            Message(from_="B", to="A", message="world", condition="cond2", group=None),
        ],
    )
    out = PlantUMLRenderer().render(ir)
    assert "[cond1]" in out
    assert "group g1" in out
    assert "end" in out  # group close
    assert "[cond2]" in out
    assert out.count("group g1") == 1  # group appears only once for first message


def test_plantuml_state_transition_with_action():
    from spec2viz.ir import StateIR, StateNode, Transition
    ir = StateIR(
        title="Test",
        entity="Order",
        initial="open",
        states=[StateNode(id="open", label="Open"), StateNode(id="closed", label="Closed")],
        transitions=[Transition(from_="open", to="closed", on="finish", action="doSomething")],
    )
    out = PlantUMLRenderer().render(ir)
    assert " / doSomething" in out


def test_plantuml_component_style_kinds_non_dict_plantuml():
    from spec2viz.ir import ComponentIR, ComponentNode, ComponentEdge
    ir = ComponentIR(
        title="Test",
        nodes=[ComponentNode(id="A", label="A", kind="core")],
        edges=[],
        style_kinds={"core": {"plantuml": "not a dict"}},
    )
    out = PlantUMLRenderer().render(ir)
    # Should not crash and should produce valid output
    assert "@startuml" in out


def test_plantuml_activity_broken_chain():
    from spec2viz.ir import ActivityIR, ActivityStep
    ir = ActivityIR(
        title="Test",
        start="step1",
        steps=[
            ActivityStep(id="step1", label="Step 1", kind="action", next="missing"),
        ],
        end="end",
    )
    out = PlantUMLRenderer().render(ir)
    assert "@startuml" in out
    assert "start" in out
    assert "stop" in out
    # Should not crash on missing step


def test_plantuml_activity_decision_branches():
    from spec2viz.ir import ActivityIR, ActivityStep
    ir = ActivityIR(
        title="Test",
        start="decide",
        steps=[
            ActivityStep(id="decide", label="Decide?", kind="decision", branches={"yes": "yes_step", "no": "no_step"}),
            ActivityStep(id="yes_step", label="Yes", next="end"),
            ActivityStep(id="no_step", label="No", next="end"),
        ],
        end="end",
    )
    out = PlantUMLRenderer().render(ir)
    assert "if (Decide??) then (yes)" in out or "if (Decide?) then (yes)" in out
    assert "else (no)" in out
    assert "endif" in out


def test_json_renderer_handles_model_and_plain_dict():
    model_payload = JsonRenderer().render(compile_ir(load("examples/reflection/canonical.yml")))
    plain_payload = JsonRenderer().render({"ok": True})
    assert isinstance(model_payload, dict)
    assert plain_payload == {"ok": True}


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


def test_render_dispatch_unknown_renderer():
    with pytest.raises(RenderError):
        render(_ir("sequence.create-quotation.yml"), renderer="nope")


def test_render_dispatch_without_default_renderer():
    class UnknownIR:
        pass

    with pytest.raises(RenderError):
        render(UnknownIR())
