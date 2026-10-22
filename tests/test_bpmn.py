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
