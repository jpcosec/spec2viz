"""BPMN renderer: XML structure, DI coverage and the offline bpmn-js viewer page."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from spec2viz import compile_ir, load, render_to_file
from spec2viz.cli import main
from spec2viz.ir import ActivityGroup, ActivityIR, ActivityStep, ComponentIR
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
FLOW_NODE_TAGS = NODE_TAGS + (
    "userTask", "serviceTask", "manualTask", "sendTask", "receiveTask", "scriptTask",
    "intermediateCatchEvent", "subProcess",
)


def _parse(xml: str) -> ET.Element:
    return ET.fromstring(xml.encode("utf-8"))


def _check_structure(root: ET.Element) -> dict[str, int]:
    """Common invariants; returns the element counts."""
    assert root.tag == f"{{{NS['bpmn']}}}definitions"
    processes = root.findall("bpmn:process", NS)
    assert len(processes) == 1
    proc = processes[0]
    nodes = {el.get("id"): el for tag in FLOW_NODE_TAGS for el in proc.findall(f"bpmn:{tag}", NS)}
    flows = proc.findall("bpmn:sequenceFlow", NS)
    ids = [el.get("id") for el in root.iter() if el.get("id")]
    assert len(ids) == len(set(ids)), "ids must be unique"
    for f in flows:
        assert f.get("sourceRef") in nodes and f.get("targetRef") in nodes
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    collab = root.find("bpmn:collaboration", NS)
    assert plane.get("bpmnElement") == (collab.get("id") if collab is not None else proc.get("id"))
    shapes = {s.get("bpmnElement"): s for s in plane.findall("bpmndi:BPMNShape", NS)
              if s.get("bpmnElement") in nodes}
    flow_ids = {f.get("id") for f in flows}
    edges = {e.get("bpmnElement"): e for e in plane.findall("bpmndi:BPMNEdge", NS)
             if e.get("bpmnElement") in flow_ids}
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
    assert w_long <= 240 and w_long >= 120
    assert h_long > h_short, "a long label grows the box in height instead of overflowing"
    assert w_short <= w_long
    assert h_short >= 60


def _column_gaps(xml: str) -> list[int]:
    """Horizontal space between consecutive columns: shapes plus their gateway labels."""
    plane = _parse(xml).find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    spans: list[tuple[int, int]] = []
    for shape in plane.findall("bpmndi:BPMNShape", NS):
        for bounds in shape.iter(f"{{{NS['dc']}}}Bounds"):
            x, w = int(bounds.get("x")), int(bounds.get("width"))
            spans.append((x, x + w))
    spans.sort()
    merged: list[list[int]] = []
    for a, b in spans:
        if merged and a < merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    ends = [m[1] for m in merged]
    starts = [m[0] for m in merged[1:]]
    return [start - end for end, start in zip(ends, starts)]


def test_text_width_is_estimated_per_character_class():
    from spec2viz.renderers.bpmn import TASK_PAD, _task_box, _text_w, _wrap

    # uppercase, '_' and 'm'/'w' are wider than the old flat 7.7px, narrow signs are thinner
    assert _text_w("PARTIAL_STOCK") > len("PARTIAL_STOCK") * 7.7
    assert _text_w("mmmm") > _text_w("iiii")
    assert _text_w("...") < _text_w("MMM")
    # PARTIAL_STOCK (the label that used to break in two) fits on a single line
    w, _h = _task_box("PARTIAL_STOCK")
    assert w - TASK_PAD + 4 >= _text_w("PARTIAL_STOCK")
    assert _wrap("PARTIAL_STOCK", w - TASK_PAD + 4) == 1
    # even the widest label of the real specs stays whole inside its box
    w2, _h2 = _task_box("Revisar + RESERVA_INSTITUCIONAL · Customer Service")
    assert _wrap("RESERVA_INSTITUCIONAL", w2 - TASK_PAD + 4) == 1
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="Aceptar + PARTIAL_STOCK", next="end"),
    ], start="a"))
    bounds = _shapes(xml)["Task_a"].find("dc:Bounds", NS)
    assert int(bounds.get("width")) - TASK_PAD + 4 >= _text_w("PARTIAL_STOCK")


def test_column_gaps_shrink_without_labels_and_grow_with_the_longest_one():
    from spec2viz.renderers.bpmn import COL_GAP, MIN_COL_GAP, _text_w

    # a linear plan with no edge labels only pays the minimum gap at every column
    steps = [ActivityStep(id=f"s{i}", label=f"Paso {i}", next=f"s{i + 1}") for i in range(5)]
    steps.append(ActivityStep(id="s5", label="Fin del camino"))
    linear = _column_gaps(BpmnRenderer().render(_ir(steps, start="s0")))
    assert linear and all(gap == MIN_COL_GAP for gap in linear)

    # a labelled flow widens only the gap it crosses, up to the old COL_GAP ceiling
    label = "etiqueta de rama"
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", next="d"),
        ActivityStep(id="d", label="¿Sigue?", kind="decision", branches={label: "b", "no": "end"}),
        ActivityStep(id="b", label="B", next="end"),
    ], start="a"))
    gaps = _column_gaps(xml)
    assert int(min(COL_GAP, max(MIN_COL_GAP, _text_w(label) + 40))) in gaps
    assert MIN_COL_GAP in gaps and max(gaps) < COL_GAP
    long_label = "una etiqueta considerablemente mas larga que el hueco maximo permitido"
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", next="d"),
        ActivityStep(id="d", label="¿Sigue?", kind="decision", branches={long_label: "b", "no": "end"}),
        ActivityStep(id="b", label="B", next="end"),
    ], start="a"))
    assert max(_column_gaps(xml)) == COL_GAP


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
    from spec2viz.renderers.bpmn_viewer import TEXT_FONT_SIZE

    assert f"fontSize: {TEXT_FONT_SIZE}" in page
    assert "MIN_ZOOM = 0.5" in page and "canvas.zoom(MIN_ZOOM)" in page
    # Fit really fits, it does not re-apply the minimum-zoom initial view
    assert "function fitViewport()" in page
    assert "document.getElementById('fit').addEventListener('click', fitViewport)" in page
    assert ".zoom('fit-viewport', 'auto')" in page
    assert "getAbsoluteBBox(start)" in page  # the initial view is anchored on the start event
    # ...and vertically shows the whole height when it fits, the top edge when it does not
    assert "height + 2 * PAD <= outer.height" in page
    # entering a subprocess applies the same rule as the initial view
    assert "viewer.on('root.set', function () { try { initialView(); }" in page


def test_legend_shows_only_used_tones_with_generic_spanish_labels():
    xml = BpmnRenderer().render(_ir([
        ActivityStep(id="a", label="A", tone="success", next="bad"),
        ActivityStep(id="bad", label="Bad", tone="danger", next="d"),
        ActivityStep(id="d", label="Decide", kind="decision", branches={"x": "end"}),
    ], start="a"))
    page = render_bpmn_html(xml, "T", None)
    assert ">favorable</span>" in page and ">rechazo</span>" in page
    assert ">gateway por defecto</span>" in page
    # start/end events never take a legend colour
    assert ">inicio</span>" not in page and ">fin</span>" not in page
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


def test_cli_render_takes_legend_and_questions_from_the_metadata_model(tmp_path):
    spec = tmp_path / "leyenda.yml"
    raw = yaml.safe_load((FIXTURES / "activity.mepu-decision.yml").read_text(encoding="utf-8"))
    raw["metadata"]["preguntas_abiertas"] = "¿Una sola pregunta?"
    raw["metadata"]["legend"] = {"gateway": "Decisión de negocio"}
    spec.write_text(yaml.safe_dump(raw, allow_unicode=True, sort_keys=False), encoding="utf-8")
    result = CliRunner().invoke(main, ["diagram", "render", str(spec), "--out", str(tmp_path), "--renderer", "bpmn"])
    assert result.exit_code == 0, result.output
    page = (tmp_path / "leyenda.bpmn.html").read_text(encoding="utf-8")
    assert "<li>¿Una sola pregunta?</li>" in page and ">Decisión de negocio</span>" in page


def _group_ir() -> ActivityIR:
    return ActivityIR(
        title="Grupos", start="a", end="e",
        steps=[
            ActivityStep(id="a", label="Entrada", group="g1", detail="Texto largo de a.", next="b"),
            ActivityStep(id="b", label="¿Sigue?", kind="decision", group="g1",
                         branches={"ok": "c", "no": "x"}),
            ActivityStep(id="c", label="Cierre interno", group="g1", next="d"),
            ActivityStep(id="x", label="Afuera", next="d"),
            ActivityStep(id="d", label="Evaluar", group="g2", next="e"),
            ActivityStep(id="e", label="Fin del grupo", group="g2"),
        ],
        groups={
            "g1": ActivityGroup(id="g1", label="Grupo uno", tone="info", detail="Detalle del grupo uno."),
            "g2": ActivityGroup(id="g2", label="Grupo dos", tone="warning", detail="Detalle del grupo dos."),
        },
    )


def test_groups_are_collapsed_subprocesses_with_their_own_planes():
    from spec2viz.renderers.bpmn import TONE_PALETTE

    root = _parse(BpmnRenderer().render(_group_ir()))
    proc = root.find("bpmn:process", NS)
    subs = {el.get("id"): el for el in proc.findall("bpmn:subProcess", NS)}
    assert set(subs) == {"SubProcess_g1", "SubProcess_g2"}
    assert subs["SubProcess_g1"].get("name") == "Grupo uno"
    planes = {p.get("bpmnElement"): p for p in root.findall("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)}
    assert set(planes) == {"Process_1", "SubProcess_g1", "SubProcess_g2"}
    top_shapes = {s.get("bpmnElement"): s for s in planes["Process_1"].findall("bpmndi:BPMNShape", NS)}
    for sid in subs:
        assert top_shapes[sid].get("isExpanded") == "false"
        assert top_shapes[sid].get(f"{{{COLOR_NS}}}background-color") in {
            background for background, _ in TONE_PALETTE.values()
        }
    # ids are unique across every plane
    ids = [el.get("id") for el in root.iter() if el.get("id")]
    assert len(ids) == len(set(ids))
    # each subprocess plane has its own start, its steps and its external end events
    g1 = planes["SubProcess_g1"]
    g1_nodes = [el.get("bpmnElement") for el in g1.findall("bpmndi:BPMNShape", NS)]
    assert {"StartEvent_g1__in", "Task_a", "Gateway_b", "Task_c"} <= set(g1_nodes)
    g1_ends = {el.get("bpmnElement") for el in g1.findall("bpmndi:BPMNShape", NS)
               if el.get("bpmnElement", "").startswith("EndEvent_g1__")}
    assert len(g1_ends) == 2  # one per distinct external destination (step x, group g2)
    g1_flows = g1.findall("bpmndi:BPMNEdge", NS)
    assert len(g1_flows) == 5
    g2 = planes["SubProcess_g2"]
    g2_ends = [el.get("bpmnElement") for el in g2.findall("bpmndi:BPMNShape", NS)
               if el.get("bpmnElement", "").startswith("EndEvent_g2__")]
    assert len(g2_ends) == 1  # terminal step e exits to the process end
    # top level: flows enter the subprocess and leave it toward the real destinations
    top_flows = proc.findall("bpmn:sequenceFlow", NS)
    assert {(f.get("sourceRef"), f.get("targetRef")) for f in top_flows} == {
        ("StartEvent_a", "SubProcess_g1"),
        ("SubProcess_g1", "Task_x"),
        ("SubProcess_g1", "SubProcess_g2"),
        ("Task_x", "SubProcess_g2"),
        ("SubProcess_g2", "EndEvent_e"),
    }
    labels = {f.get("name") for f in top_flows if f.get("sourceRef") == "SubProcess_g1"}
    assert labels == {"Afuera", "Grupo dos"}
    # the inner flows reach those end events
    inner = {(f.get("sourceRef"), f.get("targetRef")) for f in subs["SubProcess_g1"].findall("bpmn:sequenceFlow", NS)}
    assert ("Gateway_b", "Task_c") in inner and ("Task_c", "EndEvent_g1__g2") in inner


def test_group_and_step_detail_reach_the_viewer_json():
    xml = BpmnRenderer().render(_group_ir())
    page = render_bpmn_html(xml, "T", None)
    literal = re.search(r"var info = (\{.*?\});\n", page, re.S).group(1)
    info = json.loads(literal)
    assert info["Task_a"]["detail"] == "Texto largo de a."
    assert info["SubProcess_g1"]["detail"] == "Detalle del grupo uno."
    assert info["SubProcess_g1"]["label"] == "Grupo uno"
    assert info["SubProcess_g1"]["subprocess"] is True
    assert info["Gateway_b"]["branches"] == [
        {"label": "ok", "target": "Cierre interno"},
        {"label": "no", "target": "Afuera"},
    ]
    assert "id=\"panel\"" in page and "320px" in page and "toggle-panel" in page


def test_spec_without_groups_produces_one_plane_and_no_subprocess():
    xml = render(compile_ir(load(FIXTURES / "activity.mepu-decision.yml")), "bpmn")
    root = _parse(xml)
    assert root.findall(".//bpmn:subProcess", NS) == []
    assert len(root.findall("bpmndi:BPMNDiagram", NS)) == 1
    _check_structure(root)


def test_other_renderers_accept_groups_and_detail():
    ir = compile_ir(load(FIXTURES / "activity.groups.yml"))
    for name in ("mermaid", "plantuml", "d2"):
        assert render(ir, name)


def test_model_validates_groups_and_detail():
    from pydantic import ValidationError
    from spec2viz.models.activity import ActivityData, GroupModel, StepModel

    step = StepModel(label="A", detail="D", group="g")
    assert step.detail == "D" and step.group == "g"
    groups = {"g": GroupModel(label="G", tone="info", detail="GD")}
    data = ActivityData(start="a", end="end", steps={"a": step}, groups=groups)
    assert data.groups["g"].label == "G"
    with pytest.raises(ValidationError, match="unknown group 'missing'"):
        ActivityData(start="a", end="end",
                     steps={"a": StepModel(label="A", next="end", group="missing")})


# ── lanes, notes, start/end kinds, task types (presentable output) ─────────────


def _bounds_of(el: ET.Element) -> tuple[int, int, int, int]:
    b = el.find("dc:Bounds", NS)
    return tuple(int(b.get(k)) for k in ("x", "y", "width", "height"))


def _flow_shapes(root: ET.Element) -> dict[str, tuple[int, int, int, int]]:
    proc = root.find("bpmn:process", NS)
    nodes = {el.get("id") for tag in FLOW_NODE_TAGS for el in proc.findall(f"bpmn:{tag}", NS)}
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    return {s.get("bpmnElement"): _bounds_of(s) for s in plane.findall("bpmndi:BPMNShape", NS)
            if s.get("bpmnElement") in nodes}


def _assert_flows_avoid_shapes(root: ET.Element) -> None:
    """No flow segment passes over a shape other than its own source and target."""
    proc = root.find("bpmn:process", NS)
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    boxes = _flow_shapes(root)
    for f in proc.findall("bpmn:sequenceFlow", NS):
        edge = plane.find(f"bpmndi:BPMNEdge[@bpmnElement='{f.get('id')}']", NS)
        pts = [(int(w.get("x")), int(w.get("y"))) for w in edge.findall("di:waypoint", NS)]
        for nid, (x, y, w, h) in boxes.items():
            if nid in (f.get("sourceRef"), f.get("targetRef")):
                continue
            for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
                sx0, sx1, sy0, sy1 = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)
                crosses = sx1 > x and sx0 < x + w and sy1 > y and sy0 < y + h
                assert not crosses, f"{f.get('id')} crosses {nid}"


def _swimlanes():
    return render(compile_ir(load(FIXTURES / "activity.swimlanes.yml")), "bpmn")


def test_partitions_become_a_pool_with_one_lane_each_in_spec_order():
    root = _parse(_swimlanes())
    _check_structure(root)
    collab = root.find("bpmn:collaboration", NS)
    participant = collab.find("bpmn:participant", NS)
    assert participant.get("processRef") == "Process_1"
    lanes = root.findall("bpmn:process/bpmn:laneSet/bpmn:lane", NS)
    assert [lane.get("name") for lane in lanes] == [
        "Cliente (VM del ERP)", "Nube", "Panel", "Agente", "Cliente final",
    ]
    refs = {lane.get("name"): {r.text for r in lane.findall("bpmn:flowNodeRef", NS)} for lane in lanes}
    assert refs["Panel"] == {"Task_revisa"}
    assert {"Task_guarda", "Gateway_color", "Task_anota"} <= refs["Nube"]
    # the start event follows its first step, the end event the step before it
    assert "StartEvent_lee" in refs["Cliente (VM del ERP)"] and "EndEvent_anota" in refs["Nube"]
    # every flow node is in exactly one lane
    shapes = _flow_shapes(root)
    listed = [r for names in refs.values() for r in names]
    assert sorted(listed) == sorted(shapes)


def test_lane_di_is_horizontal_stacked_and_holds_its_steps():
    root = _parse(_swimlanes())
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    di = {s.get("bpmnElement"): s for s in plane.findall("bpmndi:BPMNShape", NS)}
    pool = di["Participant_1"]
    assert pool.get("isHorizontal") == "true"
    px, py, pw, ph = _bounds_of(pool)
    lanes = root.findall("bpmn:process/bpmn:laneSet/bpmn:lane", NS)
    top = py
    shapes = _flow_shapes(root)
    for lane in lanes:
        shape = di[lane.get("id")]
        assert shape.get("isHorizontal") == "true"
        lx, ly, lw, lh = _bounds_of(shape)
        assert ly == top and lx == px + 30 and lx + lw == px + pw  # stacked bands, title band at the left
        top += lh
        for ref in lane.findall("bpmn:flowNodeRef", NS):
            x, y, w, h = shapes[ref.text]
            assert lx < x and x + w < lx + lw and ly < y and y + h < ly + lh, f"{ref.text} leaves its lane"
    assert top == py + ph


def test_lane_layout_has_no_overlaps_and_flows_never_cross_shapes():
    for xml in (_swimlanes(), render(compile_ir(load(FIXTURES / "activity.lanes.yml")), "bpmn")):
        root = _parse(xml)
        _check_structure(root)  # also: no two shapes overlap, every waypoint orthogonal
        _assert_flows_avoid_shapes(root)
        # annotations and labels do not sit on top of shapes either
        plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
        boxes = list(_flow_shapes(root).values())
        for s in plane.findall("bpmndi:BPMNShape", NS):
            if s.get("bpmnElement", "").startswith("TextAnnotation_"):
                x, y, w, h = _bounds_of(s)
                for (x2, y2, w2, h2) in boxes:
                    assert x + w <= x2 or x2 + w2 <= x or y + h <= y2 or y2 + h2 <= y


def test_lanes_advance_left_to_right_and_a_lane_change_may_drop_straight_down():
    root = _parse(_swimlanes())
    shapes = _flow_shapes(root)
    proc = root.find("bpmn:process", NS)
    for f in proc.findall("bpmn:sequenceFlow", NS):
        (sx, _, sw, _), (tx, _, tw, _) = shapes[f.get("sourceRef")], shapes[f.get("targetRef")]
        assert sx + sw / 2 <= tx + tw / 2, f"{f.get('id')} goes backwards"
    # `manda` (Agente) hands over to `recibe` (Cliente final) right below it, in the same column
    edges = _edges(_swimlanes())
    pts = [(int(w.get("x")), int(w.get("y"))) for w in edges["Flow_manda__recibe"].findall("di:waypoint", NS)]
    assert len(pts) == 2 and pts[0][0] == pts[1][0] and pts[1][1] > pts[0][1]


def test_flows_into_the_same_step_do_not_share_their_last_stretch():
    root = _parse(_swimlanes())
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    proc = root.find("bpmn:process", NS)
    last: dict[str, list[tuple[tuple[int, int], tuple[int, int]]]] = {}
    for f in proc.findall("bpmn:sequenceFlow", NS):
        edge = plane.find(f"bpmndi:BPMNEdge[@bpmnElement='{f.get('id')}']", NS)
        pts = [(int(w.get("x")), int(w.get("y"))) for w in edge.findall("di:waypoint", NS)]
        last.setdefault(f.get("targetRef"), []).append((pts[-2], pts[-1]))
    into_manda = last["Task_manda"]
    assert len(into_manda) == 2
    assert into_manda[0][1] != into_manda[1][1], "two arrows end at the same point"


def test_spec_without_partitions_has_no_pool():
    root = _parse(render(compile_ir(load(FIXTURES / "activity.mepu-decision.yml")), "bpmn"))
    assert root.find("bpmn:collaboration", NS) is None
    assert root.find("bpmn:process/bpmn:laneSet", NS) is None
    _assert_flows_avoid_shapes(root)


def test_detail_reaches_the_viewer_without_groups():
    xml = _swimlanes()
    proc = _parse(xml).find("bpmn:process", NS)
    doc = proc.find("bpmn:task[@id='Task_lee']/bpmn:documentation", NS)
    assert doc.text.startswith("Una tarea programada")
    page = render_bpmn_html(xml, "T", None)
    info = json.loads(re.search(r"var info = (\{.*?\});\n", page, re.S).group(1))
    assert info["Task_lee"]["detail"].startswith("Una tarea programada")
    assert info["Gateway_color"]["detail"].startswith("Se le escribe")
    assert info["Task_guarda"]["notes"] == ["TC del día anterior"]
    assert info["Task_lee"]["lane"] == "Cliente (VM del ERP)"


def test_notes_are_text_annotations_joined_to_their_step():
    root = _parse(_swimlanes())
    proc = root.find("bpmn:process", NS)
    ann = proc.find("bpmn:textAnnotation[@id='TextAnnotation_guarda']", NS)
    assert ann.find("bpmn:text", NS).text == "TC del día anterior"
    assoc = proc.find("bpmn:association[@id='Association_guarda']", NS)
    assert (assoc.get("sourceRef"), assoc.get("targetRef")) == ("Task_guarda", "TextAnnotation_guarda")
    # the note is not repeated as documentation (it is visible on the canvas)
    assert proc.find("bpmn:task[@id='Task_guarda']/bpmn:documentation", NS) is None
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    shape = plane.find("bpmndi:BPMNShape[@bpmnElement='TextAnnotation_guarda']", NS)
    edge = plane.find("bpmndi:BPMNEdge[@bpmnElement='Association_guarda']", NS)
    ax, ay, aw, ah = _bounds_of(shape)
    tx, ty, tw, th = _flow_shapes(root)["Task_guarda"]
    assert ay + ah < ty, "the annotation sits above its step"
    pts = [(int(w.get("x")), int(w.get("y"))) for w in edge.findall("di:waypoint", NS)]
    assert pts[0][1] == ay + ah and pts[-1][1] == ty


def test_start_and_end_kinds_are_only_the_event():
    steps = [
        ActivityStep(id="inicio", label="Primera hora del día", kind="start", next="trabaja"),
        ActivityStep(id="trabaja", label="Trabaja", next="fin"),
        ActivityStep(id="fin", label="Fin del día", kind="end"),
    ]
    root = _parse(BpmnRenderer().render(_ir(steps, start="inicio", end="fin")))
    counts = _check_structure(root)
    assert counts == {"startEvent": 1, "endEvent": 1, "task": 1, "exclusiveGateway": 0, "sequenceFlow": 2}
    proc = root.find("bpmn:process", NS)
    assert proc.find("bpmn:startEvent", NS).get("name") == "Primera hora del día"
    assert proc.find("bpmn:endEvent", NS).get("name") == "Fin del día"
    # the event's label is placed below the circle
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    start_di = plane.find("bpmndi:BPMNShape[@bpmnElement='StartEvent_inicio']", NS)
    _, sy, _, sh = _bounds_of(start_di)
    _, ly, _, _ = _bounds_of(start_di.find("bpmndi:BPMNLabel", NS))
    assert ly > sy + sh


def test_start_and_end_kinds_are_validated():
    from pydantic import ValidationError
    from spec2viz.models.activity import ActivityData, StepModel

    with pytest.raises(ValidationError, match="kind 'start' but the activity starts"):
        ActivityData(start="a", end="b", steps={
            "a": StepModel(label="A", next="b"), "b": StepModel(label="B", kind="start")})
    with pytest.raises(ValidationError, match="kind 'end' and cannot have next"):
        ActivityData(start="a", end="b", steps={"a": StepModel(label="A", kind="end", next="b"),
                                                 "b": StepModel(label="B")})
    with pytest.raises(ValidationError, match="points at 'a', which has kind 'start'"):
        ActivityData(start="a", end="end", steps={"a": StepModel(label="A", kind="start", next="b"),
                                                   "b": StepModel(label="B", next="a")})
    with pytest.raises(RenderError):
        BpmnRenderer().render(_ir([ActivityStep(id="a", label="A", kind="end", next="end")]))


def test_existing_specs_keep_a_generated_start_and_end_event():
    # without `kind: start`/`end` the start step is a task after an unnamed start event, as before
    root = _parse(render(compile_ir(load(FIXTURES / "activity.validation.yml")), "bpmn"))
    proc = root.find("bpmn:process", NS)
    assert proc.find("bpmn:startEvent", NS).get("name") is None
    assert proc.find("bpmn:endEvent", NS).get("name") is None


def test_task_and_event_kinds():
    steps = [
        ActivityStep(id="a", label="Revisa", kind="user", next="b"),
        ActivityStep(id="b", label="Calcula", kind="service", next="t"),
        ActivityStep(id="t", label="Espera al lunes", kind="timer", next="m"),
        ActivityStep(id="m", label="Llega el pago", kind="message", next="c"),
        ActivityStep(id="c", label="Archiva", kind="manual", next="end"),
    ]
    root = _parse(BpmnRenderer().render(_ir(steps)))
    _check_structure(root)
    proc = root.find("bpmn:process", NS)
    assert proc.find("bpmn:userTask[@id='Task_a']", NS) is not None
    assert proc.find("bpmn:serviceTask[@id='Task_b']", NS) is not None
    assert proc.find("bpmn:manualTask[@id='Task_c']", NS) is not None
    timer = proc.find("bpmn:intermediateCatchEvent[@id='Event_t']", NS)
    assert timer.get("name") == "Espera al lunes" and timer.find("bpmn:timerEventDefinition", NS) is not None
    message = proc.find("bpmn:intermediateCatchEvent[@id='Event_m']", NS)
    assert message.find("bpmn:messageEventDefinition", NS) is not None
    # an unknown kind stays a plain task, as before
    root = _parse(BpmnRenderer().render(_ir([ActivityStep(id="a", label="A", kind="whatever", next="end")])))
    assert root.find("bpmn:process/bpmn:task[@id='Task_a']", NS) is not None


def test_merge_without_label_has_no_visible_name():
    root = _parse(render(compile_ir(load(FIXTURES / "activity.lanes.yml")), "bpmn"))
    gw = root.find("bpmn:process/bpmn:exclusiveGateway[@id='Gateway_joined']", NS)
    assert gw.get("name") is None
    plane = root.find("bpmndi:BPMNDiagram/bpmndi:BPMNPlane", NS)
    assert plane.find("bpmndi:BPMNShape[@bpmnElement='Gateway_joined']/bpmndi:BPMNLabel", NS) is None


def test_a_box_never_breaks_a_word_wider_than_the_maximum():
    from spec2viz.renderers.bpmn import TASK_MAX_W, TASK_PAD, _task_box, _text_w, _wrap

    word = "RESERVA_INSTITUCIONAL_EXTENDIDA"
    w, _ = _task_box(f"Revisar {word}")
    assert w > TASK_MAX_W and _wrap(word, w - TASK_PAD + 4) == 1 and w - TASK_PAD + 4 >= _text_w(word)


def test_viewer_starts_with_the_panel_folded_and_fits_with_a_margin():
    page = render_bpmn_html(_swimlanes(), "T", None)
    assert '<body class="panel-collapsed">' in page
    assert "setPanel(true)" in page and "id=\"close-panel\"" in page
    assert "var PAD = 28" in page and "outer.width - 2 * PAD" in page
    assert "data-import-warnings" in page and "data-zoom" in page
