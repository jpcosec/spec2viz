import json
from pathlib import Path
from yaml_charts.loader import load
from yaml_charts.compilers import compile_ir
from yaml_charts.renderers import render
from yaml_charts.renderers.plantuml import PlantUMLRenderer
from yaml_charts.renderers.vega import VegaRenderer
from yaml_charts.renderers.mermaid import MermaidRenderer

FIXTURES = Path("tests/fixtures")


def _ir(name): return compile_ir(load(FIXTURES / name))


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

def test_activity_puml():
    out = PlantUMLRenderer().render(_ir("activity.validation.yml"))
    assert "start" in out and "stop" in out
    assert "Load basket" in out
    assert "if (" in out

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
    assert [s["id"] for s in stages] == ["browse", "client", "basket", "validation", "completed"]

def test_vega_spans():
    spec = VegaRenderer().render(_ir("matrix.quotation-view.yml"))
    spans = next(d for d in spec["data"] if d["name"] == "spans")["values"]
    qf = next(s for s in spans if s["component"] == "QuotationFlow")
    assert qf["start"] == 0 and qf["end"] == 5


# ── Mermaid ───────────────────────────────────────────────────────────────────

def test_mermaid_sequence():
    out = MermaidRenderer().render(_ir("sequence.create-quotation.yml"))
    assert "sequenceDiagram" in out
    assert "User" in out


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
