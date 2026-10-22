"""BPMN renderer: XML structure, DI coverage and the offline bpmn-js viewer page."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
from click.testing import CliRunner

from spec2viz import compile_ir, load, render_to_file
from spec2viz.cli import main
from spec2viz.ir import ActivityIR, ActivityStep, ComponentIR
from spec2viz.exceptions import RenderError
from spec2viz.renderers import render
from spec2viz.renderers.bpmn import BpmnRenderer, render_bpmn_html

FIXTURES = Path(__file__).parent / "fixtures"
NS = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
    "dc": "http://www.omg.org/spec/DD/20100524/DC",
    "di": "http://www.omg.org/spec/DD/20100524/DI",
}
NODE_TAGS = ("startEvent", "endEvent", "task", "exclusiveGateway")


def _parse(xml: str) -> ET.Element:
    return ET.fromstring(xml.encode("utf-8"))


def _check_structure(root: ET.Element) -> dict[str, int]:
    """Common invariants; returns the element counts."""
    assert root.tag == f"{{{NS['bpmn']}}}definitions"
    processes = root.findall("bpmn:process", NS)
    assert len(processes) == 1
    proc = processes[0]
    nodes = {el.get("id"): el for tag in NODE_TAGS for el in proc.findall(f"bpmn:{tag}", NS)}
    flows = proc.findall("bpmn:sequenceFlow", NS)
    ids = [el.get("id") for el in proc] + [proc.get("id")]
    assert len(ids) == len(set(ids)), "ids must be unique"
    for f in flows:
        assert f.get("sourceRef") in nodes and f.get("targetRef") in nodes
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    assert plane.get("bpmnElement") == proc.get("id")
    shapes = {s.get("bpmnElement"): s for s in plane.findall("bpmndi:BPMNShape", NS)}
    edges = {e.get("bpmnElement"): e for e in plane.findall("bpmndi:BPMNEdge", NS)}
    assert set(shapes) == set(nodes), "every node has exactly one DI shape"
    assert set(edges) == {f.get("id") for f in flows}, "every flow has exactly one DI edge"
    for s in shapes.values():
        b = s.find("dc:Bounds", NS)
        assert int(b.get("width")) > 0 and int(b.get("height")) > 0
    for e in edges.values():
        pts = [(int(w.get("x")), int(w.get("y"))) for w in e.findall("di:waypoint", NS)]
        assert len(pts) >= 2
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            assert x0 == x1 or y0 == y1, "waypoints are orthogonal"
    # no two shapes overlap
    boxes = [tuple(int(s.find("dc:Bounds", NS).get(k)) for k in ("x", "y", "width", "height")) for s in shapes.values()]
    for i, (x, y, w, h) in enumerate(boxes):
        for (x2, y2, w2, h2) in boxes[i + 1:]:
            assert x + w <= x2 or x2 + w2 <= x or y + h <= y2 or y2 + h2 <= y
    return {
        **{tag: len(proc.findall(f"bpmn:{tag}", NS)) for tag in NODE_TAGS},
        "sequenceFlow": len(flows),
    }


def test_small_activity_counts():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    root = _parse(xml)
    counts = _check_structure(root)
    assert counts == {"startEvent": 1, "endEvent": 1, "task": 4, "exclusiveGateway": 1, "sequenceFlow": 7}
    proc = root.find("bpmn:process", NS)
    gw = proc.find("bpmn:exclusiveGateway", NS)
    assert gw.get("id") == "Gateway_check_validity"
    assert gw.get("name") == "Is quotation valid?"
    names = {f.get("name") for f in proc.findall("bpmn:sequenceFlow", NS) if f.get("sourceRef") == gw.get("id")}
    assert names == {"yes", "no"}


def test_mepu_decision_example_counts():
    xml = render(compile_ir(load(FIXTURES / "activity.mepu-decision.yml")), "bpmn")
    root = _parse(xml)
    counts = _check_structure(root)
    assert counts == {"startEvent": 1, "endEvent": 1, "task": 12, "exclusiveGateway": 5, "sequenceFlow": 28}
    proc = root.find("bpmn:process", NS)
    # two branches of r5 go to the same step: two distinct flows with distinct paths
    to_peor = [f for f in proc.findall("bpmn:sequenceFlow", NS)
               if (f.get("sourceRef"), f.get("targetRef")) == ("Gateway_r5", "Task_peor")]
    assert len(to_peor) == 2
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    paths = [
        [(w.get("x"), w.get("y")) for w in plane.find(f"bpmndi:BPMNEdge[@bpmnElement='{f.get('id')}']", NS)
         .findall("di:waypoint", NS)]
        for f in to_peor
    ]
    assert paths[0] != paths[1]


def test_layout_is_deterministic_and_left_to_right():
    ir = compile_ir(load(FIXTURES / "activity.mepu-decision.yml"))
    a, b = render(ir, "bpmn"), render(ir, "bpmn")
    assert a == b
    root = _parse(a)
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    x = {s.get("bpmnElement"): int(s.find("dc:Bounds", NS).get("x")) for s in plane.findall("bpmndi:BPMNShape", NS)}
    for f in root.find("bpmn:process", NS).findall("bpmn:sequenceFlow", NS):
        assert x[f.get("sourceRef")] < x[f.get("targetRef")]


def _ir(steps, start="a", end="end"):
    return ActivityIR(title="T", start=start, steps=steps, end=end)


def test_cycles_terminal_steps_and_escaping():
    steps = [
        ActivityStep(id="a", label='Load <data> & "quote"', next="b?"),
        ActivityStep(id="b?", label="Valid?", kind="decision", branches={"retry <x>": "a", "ok": "done", "drop": "dead"}),
        ActivityStep(id="done", label="Done", next="end"),
        ActivityStep(id="dead", label="Dead end, no next"),  # terminal: flows to the end event
    ]
    xml = BpmnRenderer().render(_ir(steps))
    root = _parse(xml)
    counts = _check_structure(root)
    assert counts == {"startEvent": 1, "endEvent": 1, "task": 3, "exclusiveGateway": 1, "sequenceFlow": 7}
    proc = root.find("bpmn:process", NS)
    assert proc.find("bpmn:task[@id='Task_a']", NS).get("name") == 'Load <data> & "quote"'
    assert proc.find("bpmn:exclusiveGateway", NS).get("id") == "Gateway_b_"
    assert "&lt;data&gt; &amp;" in xml
    ends = [f for f in proc.findall("bpmn:sequenceFlow", NS) if f.get("targetRef").startswith("EndEvent_")]
    assert {f.get("sourceRef") for f in ends} == {"Task_done", "Task_dead"}


def test_end_that_is_also_a_step_and_id_collisions():
    steps = [
        ActivityStep(id="a b", label="A", next="a_b"),
        ActivityStep(id="a_b", label="A2", next="fin"),
        ActivityStep(id="fin", label="Finish"),
    ]
    root = _parse(BpmnRenderer().render(_ir(steps, start="a b", end="fin")))
    counts = _check_structure(root)
    assert counts["task"] == 3 and counts["endEvent"] == 1


def test_rejects_other_ir():
    with pytest.raises(RenderError):
        BpmnRenderer().render(ComponentIR(title="x", nodes=[], edges=[]))


def test_viewer_html_inlines_bpmn_js_and_the_xml():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    page = render_bpmn_html(xml, "T <1>", {"description": "Desc & more", "preguntas_abiertas": ["¿Q1 <b>?"]})
    assert "bpmn-js - bpmn-navigated-viewer v" in page
    assert ".djs-container" in page  # diagram-js.css
    assert "new BpmnJS(" in page and "fit-viewport" in page
    # nothing is loaded from outside the file
    assert "<script src=" not in page and "<link" not in page
    assert not re.search(r"url\(['\"]?https?:|@import", page)
    assert "T &lt;1&gt;" in page and "Desc &amp; more" in page and "¿Q1 &lt;b&gt;?" in page
    literal = re.search(r"var xml = (\".*?\");\n", page, re.S).group(1)
    assert json.loads(literal) == xml
    assert "</bpmn:" not in page  # the XML is inside a JSON string with `<` escaped


def test_cli_render_writes_bpmn_and_html(tmp_path):
    result = CliRunner().invoke(
        main,
        ["diagram", "render", str(FIXTURES / "activity.mepu-decision.yml"), "--out", str(tmp_path), "--renderer", "bpmn"],
    )
    assert result.exit_code == 0, result.output
    bpmn = tmp_path / "activity.mepu-decision.bpmn"
    page = tmp_path / "activity.mepu-decision.bpmn.html"
    assert bpmn.exists() and page.exists()
    text = bpmn.read_text(encoding="utf-8")
    assert text.startswith('<?xml version="1.0" encoding="UTF-8"?>\n<!-- spec2viz: generated from')
    _check_structure(_parse(text))
    html = page.read_text(encoding="utf-8")
    assert "Preguntas abiertas" in html and "R2 parcial" in html
    assert "MEPU · Cómo se decide una línea" in html
    assert str(page) in result.output


def test_render_to_file_returns_the_bpmn_path(tmp_path):
    out = render_to_file(FIXTURES / "activity.complex.yml", out=tmp_path, renderer="bpmn")
    assert out.name == "activity.complex.bpmn"
    assert (tmp_path / "activity.complex.bpmn.html").exists()


COLOR_NS = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"
COLOR = {"color": COLOR_NS}


def _shapes(xml: str) -> dict[str, ET.Element]:
    plane = _parse(xml).find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    return {s.get("bpmnElement"): s for s in plane.findall("bpmndi:BPMNShape", NS)}


def _edges(xml: str) -> dict[str, ET.Element]:
    plane = _parse(xml).find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    return {e.get("bpmnElement"): e for e in plane.findall("bpmndi:BPMNEdge", NS)}


def test_tones_emit_bpmn_in_color_attributes_and_namespace():
    steps = [
        ActivityStep(id="a", label="Prepare", tone="info", next="ok"),
        ActivityStep(id="ok", label="Accepted", tone="success", next="gate"),
        ActivityStep(id="gate", label="Decide", kind="decision", tone="rule2",
                     branches={"yes": "warn", "no": "bad"}),
        ActivityStep(id="warn", label="Review", tone="warning", next="end"),
        ActivityStep(id="bad", label="Rejected", tone="danger"),
        ActivityStep(id="plain", label="Neutral task", tone="neutral", next="end"),
    ]
    xml = BpmnRenderer().render(_ir(steps, start="a", end="end"))
    assert f'xmlns:color="{COLOR_NS}"' in xml
    shapes = _shapes(xml)
    assert shapes["Task_a"].get(f"{{{COLOR_NS}}}background-color") == "#E1EEFB"
    assert shapes["Task_a"].get(f"{{{COLOR_NS}}}border-color") == "#1D4ED8"
    assert shapes["Task_ok"].get(f"{{{COLOR_NS}}}background-color") == "#E3F4E6"
    assert shapes["Task_warn"].get(f"{{{COLOR_NS}}}border-color") == "#B26A00"
    assert shapes["Task_bad"].get(f"{{{COLOR_NS}}}border-color") == "#B42318"
    assert shapes["Task_plain"].get(f"{{{COLOR_NS}}}border-color") == "#6B7280"
    # the gateway carries its own tone; its outgoing flows take that border colour
    assert shapes["Gateway_gate"].get(f"{{{COLOR_NS}}}border-color") == "#C2410C"
    edges = _edges(xml)
    gw_flows = [e for name, e in edges.items() if name.startswith("Flow_gate__")]
    assert len(gw_flows) == 2
    assert all(e.get(f"{{{COLOR_NS}}}border-color") == "#C2410C" for e in gw_flows)
    # flows that do not leave a gateway stay unstyled
    assert edges["Flow_start__a"].get(f"{{{COLOR_NS}}}border-color") is None


def test_events_and_untinted_gateway_get_default_colors():
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", next="d"),
        ActivityStep(id="d", label="Decide", kind="decision", branches={"x": "end"}),
    ], start="a"))
    shapes = _shapes(xml)
    start = next(v for k, v in shapes.items() if k.startswith("StartEvent_"))
    end = next(v for k, v in shapes.items() if k.startswith("EndEvent_"))
    assert start.get(f"{{{COLOR_NS}}}background-color") == "#E3F4E6"
    assert end.get(f"{{{COLOR_NS}}}border-color") == "#8B1A1A"
    assert shapes["Gateway_d"].get(f"{{{COLOR_NS}}}background-color") == "#F4F0FB"
    # a task without tone stays at the default BPMN white, no colour attributes
    assert shapes["Task_a"].get(f"{{{COLOR_NS}}}background-color") is None


def test_rule_tones_are_five_distinct_soft_colors():
    from spec2viz.renderers.bpmn import TONE_PALETTE

    rules = [TONE_PALETTE[f"rule{i}"] for i in range(1, 6)]
    assert len(set(rules)) == 5
    assert len({bg for bg, _ in TONE_PALETTE.values()}) == len(TONE_PALETTE)


def test_tasks_are_wrapped_and_sized_to_their_text():
    long_label = "Una línea de una OC abierta de Laboratorio Chile con un texto bastante largo que debe envolverse"
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="short", label="Do it", next="long"),
        ActivityStep(id="long", label=long_label, next="end"),
    ], start="short"))
    shapes = _shapes(xml)

    def bounds(nid):
        b = shapes[nid].find("dc:Bounds", NS)
        return int(b.get("width")), int(b.get("height"))

    w_short, h_short = bounds("Task_short")
    w_long, h_long = bounds("Task_long")
    assert w_long <= 220 and w_long >= 120
    assert h_long > h_short, "a long label grows the box in height instead of overflowing"
    assert w_short <= w_long
    assert h_short >= 60


def test_tone_field_is_validated_by_the_model():
    from pydantic import ValidationError
    from spec2viz.models.activity import StepModel

    assert StepModel(label="x", tone="rule5").tone == "rule5"
    assert StepModel(label="x").tone is None
    with pytest.raises(ValidationError):
        StepModel(label="x", tone="chartreuse")


def test_viewer_has_a_compact_header_full_height_canvas_and_collapsed_meta():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    page = render_bpmn_html(xml, "T", {"description": "Desc", "preguntas_abiertas": ["¿Q?"]})
    # title, buttons and legend stay in the bar; description and questions are collapsed
    assert "<details class=\"meta\">" in page and "<summary>Descripción y preguntas abiertas</summary>" in page
    assert " open" not in page.split("<details")[1].split(">")[0]
    assert 'class="legend"' in page and "white-space: nowrap" in page
    # the canvas takes whatever the bar leaves, on a full-viewport flex column
    assert "height: 100vh" in page and "flex-direction: column" in page
    assert "#canvas { flex: 1 1 auto" in page
    assert "<header>" in page


def test_viewer_font_size_and_initial_zoom():
    xml = render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn")
    page = render_bpmn_html(xml, "T", None)
    assert "textRenderer" in page and "defaultStyle" in page and "externalStyle" in page
    assert "fontSize: 14" in page
    assert "MIN_ZOOM = 0.9" in page and "canvas.zoom(MIN_ZOOM)" in page
    # Fit really fits, it does not re-apply the minimum-zoom initial view
    assert "function fitViewport()" in page
    assert "document.getElementById('fit').addEventListener('click', fitViewport)" in page
    assert ".zoom('fit-viewport', 'auto')" in page
    assert "getAbsoluteBBox(start)" in page  # the initial view is anchored on the start event


def test_legend_shows_only_used_tones_with_generic_spanish_labels():
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", tone="success", next="bad"),
        ActivityStep(id="bad", label="Bad", tone="danger", next="d"),
        ActivityStep(id="d", label="Decide", kind="decision", branches={"x": "end"}),
    ], start="a"))
    page = render_bpmn_html(xml, "T", None)
    assert ">favorable</span>" in page and ">rechazo</span>" in page
    assert ">gateway por defecto</span>" in page and ">inicio</span>" in page and ">fin</span>" in page
    # unused tones are not in the legend
    for unused in ("atención", "informativo", "neutro", "regla 1", "regla 5"):
        assert f">{unused}</span>" not in page


def test_legend_reads_custom_labels_from_metadata():
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", tone="rule2", next="ok"),
        ActivityStep(id="ok", label="OK", tone="success", next="end"),
    ], start="a"))
    page = render_bpmn_html(xml, "T", {"legend": {"rule2": "R2 · Stock", "success": "Aceptar"}})
    assert ">R2 · Stock</span>" in page and ">Aceptar</span>" in page
    assert ">regla 2</span>" not in page
