from __future__ import annotations

import heapq
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from spec2viz.exceptions import RenderError
from spec2viz.ir import ActivityIR
from spec2viz.renderers.bpmn_palette import (
    END_TONE,
    GATEWAY_TONE,
    LANE_TINT,
    START_TONE,
    TONE_PALETTE,
)
from spec2viz.renderers.bpmn_viewer import TEXT_FONT_SIZE, render_bpmn_html, with_xml_provenance

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
BPMNDI_NS = "http://www.omg.org/spec/BPMN/20100524/DI"
DC_NS = "http://www.omg.org/spec/DD/20100524/DC"
DI_NS = "http://www.omg.org/spec/DD/20100524/DI"
COLOR_NS = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"
NAMESPACES = {"bpmn": BPMN_NS, "bpmndi": BPMNDI_NS, "dc": DC_NS, "di": DI_NS, "color": COLOR_NS}

GATEWAY_KINDS = {"decision", "merge"}
# step kinds drawn as a BPMN task of a given type
TASK_TAGS = {
    "user": "userTask", "service": "serviceTask", "manual": "manualTask",
    "send": "sendTask", "receive": "receiveTask", "script": "scriptTask",
}
# step kinds drawn as an intermediate catch event with an event definition
EVENT_DEFINITIONS = {"timer": "timerEventDefinition", "message": "messageEventDefinition"}

# geometry (px); the viewer draws text at TEXT_FONT_SIZE in Arial (Liberation Sans on Linux)
LINE_H = round(TEXT_FONT_SIZE * 1.2)
TASK_MAX_W = 200
TASK_MIN_W = 120
TASK_TWO_LINES_MAX_W = 170  # a label takes two lines when that fits in this width, else three
TASK_PAD = 16      # text padding inside a task (bpmn-js wraps at width - 12)
TASK_MIN_H = 64
GATEWAY = 50
EVENT = 36
GATEWAY_LABEL_W = 140
EVENT_LABEL_W = 120
NOTE_MAX_W = 190
NOTE_GAP = 16      # between a text annotation and the step it annotates
EDGE_LABEL_W = 150
COL_GAP = 170
MIN_COL_GAP = 60
NODE_GAP = 44
DUMMY_GAP = 30
ENTRY_STEP = 14    # vertical distance between flows entering the same side of a step
MARGIN = 60
LANE_STEP = 10
SUB_MIN_W = 150
SUB_MIN_H = 80
SHORT_LABEL = 42
# lanes: a pool with a vertical title band, one band per lane with its own vertical name
POOL_HEADER = 30
LANE_HEADER = 30
LANE_PAD = 30      # free space above and below the content of a lane
LANE_INNER = 34    # between the lane name band and the first column
LANE_RIGHT = 40
CORRIDOR_STEP = 16

# advance widths of Arial in 1/1000 em (Liberation Sans has the same metrics)
_AFM = {
    " ": 278, "!": 278, '"': 355, "#": 556, "$": 556, "%": 889, "&": 667, "'": 191, "(": 333, ")": 333,
    "*": 389, "+": 584, ",": 278, "-": 333, ".": 278, "/": 278, ":": 278, ";": 278, "<": 584, "=": 584,
    ">": 584, "?": 556, "@": 1015, "[": 278, "\\": 278, "]": 278, "^": 469, "_": 556, "`": 333, "{": 334,
    "|": 260, "}": 334, "~": 584, "«": 556, "»": 556, "¿": 611, "¡": 333, "·": 278, "–": 556, "—": 1000,
    "…": 1000, "“": 333, "”": 333, "‘": 222, "’": 222, "°": 400, "º": 365, "ª": 370,
    "A": 667, "B": 667, "C": 722, "D": 722, "E": 667, "F": 611, "G": 778, "H": 722, "I": 278, "J": 500,
    "K": 667, "L": 556, "M": 833, "N": 722, "O": 778, "P": 667, "Q": 778, "R": 722, "S": 667, "T": 611,
    "U": 722, "V": 667, "W": 944, "X": 667, "Y": 667, "Z": 611,
    "a": 556, "b": 556, "c": 500, "d": 556, "e": 556, "f": 278, "g": 556, "h": 556, "i": 222, "j": 222,
    "k": 500, "l": 222, "m": 833, "n": 556, "o": 556, "p": 556, "q": 556, "r": 333, "s": 500, "t": 278,
    "u": 556, "v": 500, "w": 722, "x": 500, "y": 500, "z": 500,
}
_SAFETY = 1.06  # the estimate errs on the wide side, so a label never overflows its box


def _q(ns: str, tag: str) -> str:
    return f"{{{NAMESPACES[ns]}}}{tag}"


def _ncname(raw: str) -> str:
    """An XML NCName from a step id: invalid characters become `_`."""
    s = re.sub(r"[^A-Za-z0-9_.-]", "_", raw)
    if not s or not re.match(r"[A-Za-z_]", s[0]):
        s = "_" + s
    return s


def _base_char(ch: str) -> str:
    """`á` -> `a`, `Ñ` -> `N`: accented letters take the width of their base letter."""
    import unicodedata

    base = unicodedata.normalize("NFD", ch)[0]
    return base if base in _AFM else ch


def _char_w(ch: str) -> float:
    """Estimated advance of `ch` at TEXT_FONT_SIZE."""
    units = _AFM.get(ch) or _AFM.get(_base_char(ch))
    if units is None:
        units = 556 if not ch.isupper() else 722
    return units * TEXT_FONT_SIZE / 1000 * _SAFETY


def _text_w(text: str) -> float:
    """Estimated rendered width of `text` at TEXT_FONT_SIZE."""
    return sum(_char_w(ch) for ch in text)


def _wrap(text: str, width_px: float) -> int:
    """Number of lines `text` takes when word-wrapped in `width_px`."""
    width = max(_char_w(" "), float(width_px))
    space = _char_w(" ")
    lines, current = 1, 0.0
    for word in text.split():
        w = _text_w(word)
        if current and current + space + w <= width:
            current += space + w
            continue
        if current:
            lines += 1
            current = 0.0
        while w > width:  # only a word wider than the whole line is broken
            w -= width
            lines += 1
        current = w
    return lines


def _task_box(label: str) -> tuple[int, int]:
    """A task box sized to its label: as narrow as two lines allow (three for long labels), never
    narrower than its longest word, between TASK_MIN_W and TASK_MAX_W."""
    longest = max((_text_w(word) for word in label.split()), default=_char_w("a"))
    floor = int(max(TASK_MIN_W, longest + TASK_PAD))  # a word wider than TASK_MAX_W widens the box
    w = max(floor, TASK_MAX_W)
    for max_lines, ceiling in ((2, TASK_TWO_LINES_MAX_W), (3, TASK_MAX_W)):
        cand = next((c for c in range(floor, max(floor, ceiling) + 1, 5)
                     if _wrap(label, c - TASK_PAD + 4) <= max_lines), None)
        if cand is not None:
            w = cand
            break
    lines = _wrap(label, w - TASK_PAD + 4)
    return w, max(TASK_MIN_H, lines * LINE_H + 24)


def _sub_box(label: str) -> tuple[int, int]:
    """A collapsed subprocess: compact by default, growing with its label."""
    natural = _text_w(label) + TASK_PAD
    w = int(min(TASK_MAX_W, max(SUB_MIN_W, natural)))
    lines = _wrap(label, w - TASK_PAD + 4)
    return w, max(SUB_MIN_H, lines * LINE_H + 24)


def _label_block(text: str, max_w: int) -> tuple[int, int]:
    """Width and height of an external label wrapped at `max_w`."""
    if not text:
        return 0, 0
    w = int(min(max_w, _text_w(text) + 8))
    w = max(w, int(min(max_w, max(_text_w(word) for word in text.split()) + 8)))
    return w, _wrap(text, w - 4) * LINE_H


@dataclass
class _Node:
    id: str            # BPMN id
    kind: str          # start | end | task | gateway | subprocess | event | dummy
    name: str = ""
    step: str | None = None
    doc: str | None = None
    detail: str | None = None
    tone: str | None = None
    w: int = 0
    h: int = 0
    tag: str = ""      # BPMN element tag (task, userTask, intermediateCatchEvent, ...)
    event_def: str | None = None
    note: str | None = None
    label_w: int = 0   # external label: above a gateway, below an event
    label_h: int = 0
    note_w: int = 0
    note_h: int = 0
    lane: int = 0
    rank: int = 0
    x: int = 0
    y: int = 0

    @property
    def top_h(self) -> int:
        """Space taken above the shape: a gateway's label and the note's text annotation."""
        h = self.label_h + 6 if (self.label_h and self.kind == "gateway") else 0
        if self.note:
            h += self.note_h + NOTE_GAP
        return h

    @property
    def bottom_h(self) -> int:
        """Space taken below the shape: an event's label."""
        return self.label_h + 6 if (self.label_h and self.kind in ("start", "end", "event")) else 0

    @property
    def span_w(self) -> int:
        """Width of the shape with its label and annotation, centered on the shape."""
        return max(self.w, self.label_w, self.note_w)

    @property
    def cx(self) -> int:
        return self.x + self.w // 2

    @property
    def cy(self) -> int:
        return self.y + self.h // 2

    def label_box(self) -> tuple[int, int, int, int] | None:
        if not self.label_h:
            return None
        if self.kind == "gateway":
            return (self.cx - self.label_w // 2, self.y - self.label_h - 6, self.label_w, self.label_h)
        return (self.cx - self.label_w // 2, self.y + self.h + 6, self.label_w, self.label_h)

    def note_box(self) -> tuple[int, int, int, int] | None:
        if not self.note:
            return None
        above = self.label_h + 6 if (self.label_h and self.kind == "gateway") else 0
        return (self.cx - self.note_w // 2, self.y - above - NOTE_GAP - self.note_h, self.note_w, self.note_h)


@dataclass
class _Edge:
    id: str
    src: str
    tgt: str
    name: str = ""
    back: bool = False
    chain: list[str] = field(default_factory=list)  # src, dummies..., tgt
    route: str = "gap"  # gap | vertical | hv | vh | back
    entry_dy: int = 0
    bottom_entry: bool = False
    points: list[tuple[int, int]] = field(default_factory=list)
    label: tuple[int, int, int, int] | None = None


@dataclass
class _Lane:
    id: str
    name: str
    nodes: list[str] = field(default_factory=list)
    y: int = 0
    h: int = 0


@dataclass
class _Geometry:
    lanes: list[_Lane] = field(default_factory=list)
    pool: tuple[int, int, int, int] | None = None


@dataclass
class _Plane:
    """The BPMNDiagram of a collapsed subProcess: its own nodes, edges and layout."""
    id: str
    bpmn_element: str
    nodes: dict[str, _Node] = field(default_factory=dict)
    edges: list[_Edge] = field(default_factory=list)


@dataclass
class _Diagram:
    nodes: dict[str, _Node]
    edges: list[_Edge]
    planes: list[_Plane] = field(default_factory=list)
    lanes: list[str] = field(default_factory=list)
    geometry: _Geometry = field(default_factory=_Geometry)


class BpmnRenderer:
    """Renders an ActivityIR as BPMN 2.0 XML with diagram interchange (DI)."""

    def render(self, ir) -> str:
        if not isinstance(ir, ActivityIR):
            raise RenderError(f"BpmnRenderer cannot render {type(ir).__name__}")
        diagram = self._build(ir)
        diagram.geometry = self._layout(diagram.nodes, diagram.edges, diagram.lanes)
        for plane in diagram.planes:
            self._layout(plane.nodes, plane.edges)
        return self._xml(ir, diagram)

    def _build(self, ir: ActivityIR) -> _Diagram:
        if not ir.groups:
            return self._graph(ir)
        return self._grouped_graph(ir)

    @staticmethod
    def _step_node(uid, step, events: bool = True) -> _Node:
        label = step.label or step.id
        kind = step.kind
        if kind in GATEWAY_KINDS:
            text = step.label or ""
            lw, lh = _label_block(text, GATEWAY_LABEL_W)
            node = _Node(uid(f"Gateway_{_ncname(step.id)}"), "gateway", text, step.id,
                         detail=step.detail, tone=step.tone, w=GATEWAY, h=GATEWAY,
                         tag="exclusiveGateway", label_w=lw, label_h=lh)
        elif events and kind in ("start", "end", *EVENT_DEFINITIONS):
            prefix, nkind, tag = {
                "start": ("StartEvent", "start", "startEvent"),
                "end": ("EndEvent", "end", "endEvent"),
            }.get(kind, ("Event", "event", "intermediateCatchEvent"))
            lw, lh = _label_block(label, EVENT_LABEL_W)
            node = _Node(uid(f"{prefix}_{_ncname(step.id)}"), nkind, label, step.id,
                         detail=step.detail, tone=step.tone, w=EVENT, h=EVENT, tag=tag,
                         event_def=EVENT_DEFINITIONS.get(kind), label_w=lw, label_h=lh)
        else:
            w, h = _task_box(label)
            node = _Node(uid(f"Task_{_ncname(step.id)}"), "task", label, step.id,
                         detail=step.detail, tone=step.tone, w=w, h=h, tag=TASK_TAGS.get(kind, "task"))
        if step.notes:
            node.note = step.notes
            node.note_w, lines_h = _label_block(step.notes, NOTE_MAX_W)
            node.note_w += 14  # the annotation bracket and its 7px padding on each side
            node.note_h = lines_h + 14
        return node

    @staticmethod
    def _short(text: str) -> str:
        text = " ".join((text or "").split())
        return text if len(text) <= SHORT_LABEL else text[:SHORT_LABEL - 1].rstrip() + "…"

    def _grouped_graph(self, ir: ActivityIR) -> _Diagram:
        """Steps in a group become a collapsed subProcess with its own drill-down plane."""
        used: set[str] = set()

        def uid(base: str) -> str:
            cand, i = base, 2
            while cand in used:
                cand, i = f"{base}_{i}", i + 1
            used.add(cand)
            return cand

        by_step = {step.id: step for step in ir.steps}
        if ir.start not in by_step:
            raise RenderError(f"Start step '{ir.start}' not found")
        step_level: dict[str, str | None] = {}
        for step in ir.steps:
            if step.group is not None and step.group not in ir.groups:
                raise RenderError(f"Step '{step.id}' references unknown group '{step.group}'")

        top_nodes: dict[str, _Node] = {}
        level_nodes: dict[str | None, dict[str, _Node]] = {None: top_nodes}
        level_edges: dict[str | None, list[_Edge]] = {None: []}
        group_node: dict[str, str] = {}
        planes: dict[str, _Plane] = {}

        top_start = _Node(uid(f"StartEvent_{_ncname(ir.start)}"), "start", w=EVENT, h=EVENT, tag="startEvent")
        top_nodes[top_start.id] = top_start
        for gid, group in ir.groups.items():
            if not any(step.group == gid for step in ir.steps):
                raise RenderError(f"Group '{gid}' has no steps")
            nid = uid(f"SubProcess_{_ncname(gid)}")
            group_node[gid] = nid
            sub_w, sub_h = _sub_box(group.label or gid)
            top_nodes[nid] = _Node(
                nid, "subprocess", group.label or gid, detail=group.detail, tone=group.tone,
                w=sub_w, h=sub_h, tag="subProcess",
            )
            level_nodes[gid] = {}
            level_edges[gid] = []
            planes[gid] = _Plane(uid(f"BPMNPlane_{_ncname(gid)}"), nid, level_nodes[gid], level_edges[gid])

        node_of: dict[str, str] = {}
        for step in ir.steps:
            # inside groups the process start and end stay the generated events: a `kind: start`
            # or `kind: end` step is drawn as a task there
            node = self._step_node(uid, step, events=step.kind not in ("start", "end"))
            level = step.group
            level_nodes[level][node.id] = node
            node_of[step.id] = node.id
            step_level[step.id] = level

        top_end = _Node(uid(f"EndEvent_{_ncname(ir.end)}"), "end", w=EVENT, h=EVENT, tag="endEvent")
        top_nodes[top_end.id] = top_end

        def resolve(ref: str) -> tuple[str, str | None]:
            if ref in by_step:
                return node_of[ref], step_level[ref]
            if ref == ir.end:
                return top_end.id, None
            raise RenderError(f"Activity reference '{ref}' is neither a step nor the end")

        def add_edge(level: str | None, src: str, tgt: str, name: str = "") -> _Edge:
            nodes = level_nodes[level]
            s, t = nodes[src], nodes[tgt]
            base = f"Flow_{_ncname(s.step or s.id)}__{_ncname(t.step or t.id)}"
            edge = _Edge(uid(base), src, tgt, name)
            level_edges[level].append(edge)
            return edge

        def target_label(ref: str, level: str | None) -> str:
            if level is not None:
                return ir.groups[level].label or level
            if ref in by_step:
                return by_step[ref].label or ref
            return "fin"

        external_in: dict[str, list[str]] = {gid: [] for gid in ir.groups}
        external_out: dict[str, dict[str, tuple[str | None, str, str]]] = {
            gid: {} for gid in ir.groups
        }

        # the top-level start event enters the subProcess when the start step lives inside one
        start_level = step_level[ir.start]
        start_target = group_node[start_level] if start_level else node_of[ir.start]
        add_edge(None, top_start.id, start_target)
        if start_level:
            external_in[start_level].append(node_of[ir.start])

        for step in ir.steps:
            src_level = step_level[step.id]
            outs = list(step.branches.items())
            if step.next:
                outs.append(("", step.next))
            if not outs:  # terminal step: to the process end event, even when it is this step
                outs.append(("", None))
            for label, ref in outs:
                if ref is None:
                    tgt, tgt_level = top_end.id, None
                else:
                    tgt, tgt_level = resolve(ref)
                if src_level == tgt_level:
                    add_edge(src_level, node_of[step.id], tgt, label)
                elif src_level is None:
                    dest = group_node[tgt_level] if tgt_level else tgt
                    add_edge(None, node_of[step.id], dest, label)
                    if tgt_level:
                        external_in[tgt_level].append(tgt)
                else:
                    key = tgt_level if tgt_level is not None else tgt
                    if key not in external_out[src_level]:
                        suffix = tgt_level or (by_step[ref].id if ref in by_step else "fin")
                        end_id = uid(f"EndEvent_{_ncname(src_level)}__{_ncname(suffix)}")
                        name = target_label(ref, tgt_level) if ref is not None else "fin"
                        name = self._short(name)
                        lw, lh = _label_block(name, EVENT_LABEL_W)
                        end_node = _Node(end_id, "end", name, w=EVENT, h=EVENT, tag="endEvent",
                                         label_w=lw, label_h=lh)
                        level_nodes[src_level][end_id] = end_node
                        external_out[src_level][key] = (tgt_level, tgt, end_id)
                    add_edge(src_level, node_of[step.id], external_out[src_level][key][2], label)

        # the internal start event feeds every step that received a flow from outside
        for gid, entries in external_in.items():
            unique = list(dict.fromkeys(entries))
            if not unique:
                continue
            start = _Node(uid(f"StartEvent_{_ncname(gid)}__in"), "start", w=EVENT, h=EVENT, tag="startEvent")
            planes[gid].nodes = {start.id: start, **planes[gid].nodes}
            level_nodes[gid] = planes[gid].nodes
            first: list[_Edge] = []
            for entry in unique:
                base = f"Flow_{_ncname(gid)}__in_{_ncname(level_nodes[gid][entry].step or entry)}"
                first.append(_Edge(uid(base), start.id, entry))
            level_edges[gid][0:0] = first
            planes[gid].edges = level_edges[gid]

        # one top-level flow per distinct external destination; labelled when the group has several
        for gid, destinations in external_out.items():
            many = len(destinations) > 1
            for tgt_level, tgt, end_id in destinations.values():
                dest = group_node[tgt_level] if tgt_level else tgt
                name = ""
                if many:
                    end_node = level_nodes[gid][end_id]
                    name = end_node.name
                add_edge(None, group_node[gid], dest, name)

        return _Diagram(top_nodes, level_edges[None], list(planes.values()))

    # ── graph ────────────────────────────────────────────────────────────────

    def _graph(self, ir: ActivityIR) -> _Diagram:
        used: set[str] = set()

        def uid(base: str) -> str:
            cand, i = base, 2
            while cand in used:
                cand, i = f"{base}_{i}", i + 1
            used.add(cand)
            return cand

        steps = {step.id: step for step in ir.steps}
        if ir.start not in steps:
            raise RenderError(f"Start step '{ir.start}' not found")
        for step in ir.steps:
            if step.kind == "start" and step.id != ir.start:
                raise RenderError(f"Step '{step.id}' has kind 'start' but the activity starts at '{ir.start}'")
            if step.kind == "end" and (step.next or step.branches):
                raise RenderError(f"Step '{step.id}' has kind 'end' and cannot have next or branches")

        nodes: dict[str, _Node] = {}
        start_is_step = steps[ir.start].kind == "start"
        start: _Node | None = None
        if not start_is_step:
            start = _Node(uid(f"StartEvent_{_ncname(ir.start)}"), "start", w=EVENT, h=EVENT, tag="startEvent")
            nodes[start.id] = start
        by_step: dict[str, str] = {}
        for step in ir.steps:
            node = self._step_node(uid, step)
            nodes[node.id] = node
            by_step[step.id] = node.id
        end_step = steps.get(ir.end)
        end: _Node | None = None
        if end_step is not None and end_step.kind == "end":
            end_id = by_step[ir.end]
        else:
            end = _Node(uid(f"EndEvent_{_ncname(ir.end)}"), "end", w=EVENT, h=EVENT, tag="endEvent")
            nodes[end.id] = end
            end_id = end.id

        def target(ref: str) -> str:
            if ref in by_step:
                if steps[ref].kind == "start":
                    raise RenderError(f"Step '{ref}' has kind 'start' and cannot be the target of a flow")
                return by_step[ref]
            if ref == ir.end:
                return end_id
            raise RenderError(f"Activity reference '{ref}' is neither a step nor the end")

        pairs: list[tuple[str, str, str]] = []
        if start is not None:
            pairs.append((start.id, by_step[ir.start], ""))
        for step in ir.steps:
            if step.kind == "end":
                continue
            src = by_step[step.id]
            outs = [(label, target(t)) for label, t in step.branches.items()]
            if step.next:
                outs.append(("", target(step.next)))
            if not outs:  # a step without outgoing flow is terminal: it ends the process
                outs.append(("", end_id))
            for label, tgt in outs:
                pairs.append((src, tgt, label))

        key = {nid: _ncname(sid) for sid, nid in by_step.items()}
        if start is not None:
            key[start.id] = "start"
        if end is not None:
            key[end.id] = "end"
        edges: list[_Edge] = []
        for src, tgt, label in pairs:
            base = f"Flow_{key[src]}__{key[tgt]}"
            edges.append(_Edge(uid(base), src, tgt, label))

        lanes = list(dict.fromkeys(step.partition for step in ir.steps if step.partition))
        if lanes:
            index = {name: i for i, name in enumerate(lanes)}
            lane_of = {by_step[s.id]: (index[s.partition] if s.partition else None) for s in ir.steps}
            self._assign_lanes(nodes, edges, lane_of)
        return _Diagram(nodes, edges, lanes=lanes)

    @staticmethod
    def _assign_lanes(nodes: dict[str, _Node], edges: list[_Edge], lane_of: dict[str, int | None]) -> None:
        """Every node gets a lane: its step's partition, else the lane of the step before it (events
        and steps without partition), else the lane of the step after it."""
        lane = {nid: lane_of.get(nid) for nid in nodes}
        changed = True
        while changed:
            changed = False
            for e in edges:
                if lane[e.tgt] is None and lane[e.src] is not None:
                    lane[e.tgt] = lane[e.src]
                    changed = True
            if changed:
                continue
            for e in edges:
                if lane[e.src] is None and lane[e.tgt] is not None:
                    lane[e.src] = lane[e.tgt]
                    changed = True
                    break
        for nid, node in nodes.items():
            node.lane = lane[nid] if lane[nid] is not None else 0

    # ── layout ───────────────────────────────────────────────────────────────

    def _layout(self, nodes: dict[str, _Node], edges: list[_Edge], lane_names: list[str] | None = None) -> _Geometry:
        laned = bool(lane_names)
        if not laned:
            for node in nodes.values():
                node.lane = 0
        real = list(nodes)
        out: dict[str, list[_Edge]] = {n: [] for n in real}
        indegree = {n: 0 for n in real}
        for e in edges:
            out[e.src].append(e)
            indegree[e.tgt] += 1
        for nid, node in nodes.items():
            # a step that many flows enter grows so that each arrow keeps its own entry point
            if node.kind in ("task", "subprocess") and indegree[nid] > 3:
                node.h = max(node.h, (indegree[nid] - 1) * ENTRY_STEP + 36)

        # back edges: DFS from the start event, then from any unvisited node, in spec order
        state: dict[str, int] = {}
        order: list[str] = []

        def dfs(root: str) -> None:
            stack = [(root, iter(out[root]))]
            state[root] = 1
            order.append(root)
            while stack:
                n, it = stack[-1]
                e = next(it, None)
                if e is None:
                    state[n] = 2
                    stack.pop()
                    continue
                s = state.get(e.tgt, 0)
                if s == 1:
                    e.back = True
                elif s == 0:
                    state[e.tgt] = 1
                    order.append(e.tgt)
                    stack.append((e.tgt, iter(out[e.tgt])))

        for n in real:
            if n not in state:
                dfs(n)

        fwd = [e for e in edges if not e.back]
        rank, reserved = self._ranks(nodes, fwd, out, order, laned)
        ends = [n for n in real if nodes[n].kind == "end"]
        if ends:
            last = max(rank.values()) if len(real) > 1 else 0
            bump = any(rank[n] == last for n in real if nodes[n].kind != "end")
            for end_id in ends:
                r = last + 1 if bump else last
                while (r, nodes[end_id].lane) in reserved:
                    r += 1
                rank[end_id] = r
        for n in real:
            nodes[n].rank = rank[n]

        # dummies for long forward edges; in the lane of their source
        all_nodes: dict[str, _Node] = dict(nodes)
        for e in edges:
            e.chain = [e.src, e.tgt]
            if e.back:
                continue
            rs, rt = rank[e.src], rank[e.tgt]
            if rt - rs > 1:
                dummies = []
                for r in range(rs + 1, rt):
                    d = _Node(f"__dummy_{e.id}_{r}", "dummy", w=0, h=0, rank=r, lane=nodes[e.src].lane)
                    all_nodes[d.id] = d
                    dummies.append(d.id)
                e.chain = [e.src, *dummies, e.tgt]

        # order inside each rank: lane, then discovery order refined by barycenter sweeps
        disc = {n: i for i, n in enumerate(order)}
        pred: dict[str, list[str]] = {n: [] for n in all_nodes}
        succ: dict[str, list[str]] = {n: [] for n in all_nodes}
        for e in edges:
            if e.back:
                continue
            for a, b in zip(e.chain, e.chain[1:]):
                succ[a].append(b)
                pred[b].append(a)
        max_rank = max(n.rank for n in all_nodes.values())
        layers: list[list[str]] = [[] for _ in range(max_rank + 1)]
        dkey: dict[str, float] = {}
        for i, e in enumerate(edges):
            for d in e.chain[1:-1]:
                dkey[d] = disc[e.src] + 0.001 * (i + 1)
        for nid, n in all_nodes.items():
            layers[n.rank].append(nid)
        lane_key = {nid: all_nodes[nid].lane for nid in all_nodes}
        for layer in layers:
            layer.sort(key=lambda n: (lane_key[n], disc.get(n, dkey.get(n, 0.0))))

        def sweep(down: bool) -> None:
            rng = range(1, len(layers)) if down else range(len(layers) - 2, -1, -1)
            for r in rng:
                ref = layers[r - 1] if down else layers[r + 1]
                pos = {n: i for i, n in enumerate(ref)}
                cur = {n: i for i, n in enumerate(layers[r])}

                def bary(n: str) -> float:
                    nb = [pos[m] for m in (pred[n] if down else succ[n]) if m in pos]
                    return sum(nb) / len(nb) if nb else float(cur[n])

                layers[r].sort(key=lambda n: (lane_key[n], bary(n), cur[n]))

        for _ in range(4):
            sweep(True)
            sweep(False)
        sweep(True)

        # x per column; a column is as wide as its widest shape with label and annotation
        col_w = [max((all_nodes[n].span_w for n in layer), default=0) or EVENT for layer in layers]
        # the gap between two columns is only as wide as the longest edge label crossing it
        gap_need = [0.0] * max(len(layers) - 1, 0)
        for e in edges:
            if e.back or not e.name:
                continue
            need = min(_text_w(e.name), EDGE_LABEL_W) + 40
            r = all_nodes[e.chain[0]].rank
            if r < len(gap_need) and all_nodes[e.chain[1]].rank != r:
                gap_need[r] = max(gap_need[r], need)
        col_gap = [int(min(COL_GAP, max(MIN_COL_GAP, need))) for need in gap_need]
        left = MARGIN + (POOL_HEADER + LANE_HEADER + LANE_INNER if laned else 0)
        col_x, x = [], left
        for i, w in enumerate(col_w):
            col_x.append(x)
            x += w + (col_gap[i] if i < len(col_gap) else COL_GAP)
        right = col_x[-1] + col_w[-1] if col_x else left

        # y: inside each lane, every rank starts stacked, then each slot is pulled toward the median
        # of its neighbors (in the same lane) in the next/previous rank; order and gaps hold
        center: dict[str, float] = {}
        lane_ids = sorted({n.lane for n in all_nodes.values()})
        for lane in lane_ids:
            sub = [[n for n in layer if lane_key[n] == lane] for layer in layers]
            same = (lambda nbs: [m for m in nbs if lane_key[m] == lane]) if laned else (lambda nbs: nbs)
            self._place_lane(all_nodes, sub, {n: same(pred[n]) for n in pred}, {n: same(succ[n]) for n in succ},
                             center)

        def head(n: _Node) -> float:  # slot top -> center
            return n.top_h + n.h / 2

        def foot(n: _Node) -> float:  # center -> slot bottom
            return n.h / 2 + n.bottom_h

        back_edges = [e for e in edges if e.back]
        geometry = _Geometry()
        if not laned:
            shift = MARGIN - min(center[n] - head(all_nodes[n]) for n in all_nodes)
            for nid, node in all_nodes.items():
                node.y = int(round(center[nid] + shift - node.h / 2))
        else:
            corridors = {lane: 0 for lane in lane_ids}
            for e in back_edges:
                corridors[max(nodes[e.src].lane, nodes[e.tgt].lane)] += 1
            top = MARGIN
            for lane in range(len(lane_names)):
                members = [n for n in all_nodes if lane_key[n] == lane]
                name = lane_names[lane]
                min_h = max(120, int(_text_w(name)) + 40)
                if members:
                    lo = min(center[n] - head(all_nodes[n]) for n in members)
                    hi = max(center[n] + foot(all_nodes[n]) for n in members)
                else:
                    lo = hi = 0.0
                content = hi - lo
                extra = (CORRIDOR_STEP * corridors.get(lane, 0) + 8) if corridors.get(lane) else 0
                h = int(max(min_h, content + 2 * LANE_PAD + extra))
                offset = top + LANE_PAD + (h - extra - 2 * LANE_PAD - content) / 2 - lo
                for nid in members:
                    node = all_nodes[nid]
                    node.y = int(round(center[nid] + offset - node.h / 2))
                geometry.lanes.append(_Lane(f"Lane_{lane + 1}", name,
                                            [n for n in members if all_nodes[n].kind != "dummy"], top, h))
                top += h
            pool_x = MARGIN
            pool_w = right + LANE_RIGHT - pool_x
            geometry.pool = (pool_x, MARGIN, pool_w, top - MARGIN)
        for layer_index, layer in enumerate(layers):
            for nid in layer:
                node = all_nodes[nid]
                node.x = col_x[layer_index] + (col_w[layer_index] - node.w) // 2

        self._straighten(all_nodes, edges, layers, geometry)
        self._route(all_nodes, edges, col_x, col_w, col_gap, geometry)
        return geometry

    @staticmethod
    def _straighten(all_nodes: dict[str, _Node], edges: list[_Edge], layers: list[list[str]],
                    geometry: _Geometry) -> None:
        """A long flow runs at the height of its source (or of its target) when its whole corridor is
        free there, so it does not jog by a few pixels on the way."""
        layer_of = {nid: r for r, layer in enumerate(layers) for nid in layer}
        for e in edges:
            dummies = e.chain[1:-1]
            if e.back or not dummies:
                continue
            src, tgt = all_nodes[e.src], all_nodes[e.tgt]
            lane = all_nodes[dummies[0]].lane
            band = geometry.lanes[lane] if geometry.lanes else None
            candidates = [src.cy] + ([tgt.cy] if tgt.lane == lane else [])

            def free(y: int) -> bool:
                if band is not None and not (band.y + 12 <= y <= band.y + band.h - 12):
                    return False
                for d in dummies:
                    for m in layers[layer_of[d]]:
                        if m == d or all_nodes[m].lane != lane:
                            continue
                        n = all_nodes[m]
                        if n.kind == "dummy":
                            if abs(n.y - y) < 12:
                                return False
                        elif n.y - n.top_h - 14 <= y <= n.y + n.h + n.bottom_h + 14:
                            return False
                return True

            for y in candidates:
                if all(all_nodes[d].y == y for d in dummies):
                    break
                if free(y):
                    for d in dummies:
                        all_nodes[d].y = y
                    break

    @staticmethod
    def _ranks(nodes: dict[str, _Node], fwd: list[_Edge], out: dict[str, list[_Edge]], order: list[str],
               laned: bool) -> tuple[dict[str, int], set[tuple[int, int]]]:
        """Longest-path ranks. With lanes, a task whose only flow goes to a task in another lane can
        have it right below (or above) it, in the same column, when nothing sits in between."""
        disc = {n: i for i, n in enumerate(order)}
        indeg = {n: 0 for n in nodes}
        preds: dict[str, list[str]] = {n: [] for n in nodes}
        for e in fwd:
            indeg[e.tgt] += 1
            preds[e.tgt].append(e.src)
        heap = [(disc[n], n) for n in nodes if indeg[n] == 0]
        heapq.heapify(heap)
        rank: dict[str, int] = {}
        occupied: dict[tuple[int, int], list[str]] = {}
        reserved: set[tuple[int, int]] = set()

        def stacked(u: str, v: str) -> bool:
            a, b = nodes[u], nodes[v]
            if not laned or a.kind != "task" or b.kind != "task" or a.lane == b.lane or len(out[u]) != 1:
                return False
            upper, lower = (a, b) if a.lane < b.lane else (b, a)
            return not upper.bottom_h and not lower.top_h

        while heap:
            _, n = heapq.heappop(heap)
            node = nodes[n]
            r = 0
            for u in preds[n]:
                r = max(r, rank[u] + (0 if stacked(u, n) else 1))
            while True:
                same_col = [u for u in preds[n] if rank[u] == r]
                if len(same_col) > 1 or (r, node.lane) in reserved:
                    r += 1
                    continue
                if same_col:
                    u = same_col[0]
                    lo, hi = sorted((nodes[u].lane, node.lane))
                    cells = [(r, lane) for lane in range(lo, hi + 1)]
                    if any(c in reserved for c in cells) or any(set(occupied.get(c, [])) - {u} for c in cells):
                        r += 1
                        continue
                    reserved.update(cells)
                break
            rank[n] = r
            occupied.setdefault((r, node.lane), []).append(n)
            for e in out[n]:
                if e.back:
                    continue
                indeg[e.tgt] -= 1
                if indeg[e.tgt] == 0:
                    heapq.heappush(heap, (disc[e.tgt], e.tgt))
        for n in nodes:  # unreachable leftovers (cycles without entry) keep rank 0
            rank.setdefault(n, 0)
        return rank, reserved

    @staticmethod
    def _place_lane(all_nodes: dict[str, _Node], layers: list[list[str]], pred: dict[str, list[str]],
                    succ: dict[str, list[str]], center: dict[str, float]) -> None:
        def head(n: _Node) -> float:
            return n.top_h + n.h / 2

        def gap(a: _Node, b: _Node) -> int:
            return DUMMY_GAP if (a.kind == "dummy" and b.kind == "dummy") else NODE_GAP

        def offsets(layer: list[str]) -> list[float]:
            offs, acc = [], 0.0
            for i, nid in enumerate(layer):
                if i:
                    a, b = all_nodes[layer[i - 1]], all_nodes[nid]
                    acc += a.h / 2 + a.bottom_h + gap(a, b) + head(b)
                offs.append(acc)
            return offs

        for layer in layers:
            for nid, off in zip(layer, offsets(layer)):
                center[nid] = off

        def median(vals: list[float]) -> float:
            vals = sorted(vals)
            m = len(vals) // 2
            return vals[m] if len(vals) % 2 else (vals[m - 1] + vals[m]) / 2

        def place(layer: list[str], neighbors) -> None:
            if not layer:
                return
            offs = offsets(layer)
            z = []
            for nid, off in zip(layer, offs):
                nb = [center[m] for m in neighbors(nid) if m in center]
                z.append((median(nb) if nb else center[nid]) - off)
            blocks: list[list[float]] = []  # pool adjacent violators: non-decreasing fit of z
            for v in z:
                blocks.append([v, 1])
                while len(blocks) > 1 and blocks[-2][0] / blocks[-2][1] > blocks[-1][0] / blocks[-1][1]:
                    s_, c_ = blocks.pop()
                    blocks[-1][0] += s_
                    blocks[-1][1] += c_
            fit = [b[0] / b[1] for b in blocks for _ in range(int(b[1]))]
            for nid, f, off in zip(layer, fit, offs):
                center[nid] = f + off

        for _ in range(6):
            for layer in layers[1:]:
                place(layer, lambda n: pred[n])
            for layer in reversed(layers[:-1]):
                place(layer, lambda n: succ[n])

        def both(n: str) -> list[str]:
            # a long edge stays straight: its slots follow the neighbor slot of the same edge
            if all_nodes[n].kind == "dummy":
                for m in pred[n] + succ[n]:
                    if all_nodes[m].kind == "dummy":
                        return [m]
            return pred[n] + succ[n]

        for _ in range(2):
            for layer in layers:
                place(layer, both)

    # ── routing ──────────────────────────────────────────────────────────────

    def _route(self, nodes: dict[str, _Node], edges: list[_Edge], col_x: list[int],
               col_w: list[int], col_gap: list[int], geometry: _Geometry) -> None:
        real = {nid: n for nid, n in nodes.items() if n.kind != "dummy"}
        outs: dict[str, list[_Edge]] = {n: [] for n in nodes}
        for e in edges:
            outs[e.src].append(e)

        obstacles: list[tuple[str, bool, tuple[int, int, int, int]]] = []  # node, is body, (x0, y0, x1, y1)
        for nid, n in real.items():
            obstacles.append((nid, True, (n.x, n.y, n.x + n.w, n.y + n.h)))
            for box in (n.label_box(), n.note_box()):
                if box:
                    bx, by, bw, bh = box
                    obstacles.append((nid, False, (bx, by, bx + bw, by + bh)))

        def clear(points: list[tuple[int, int]], src: str, tgt: str) -> bool:
            for (x0, y0), (x1, y1) in zip(points, points[1:]):
                sx0, sx1, sy0, sy1 = min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)
                for nid, body, (bx0, by0, bx1, by1) in obstacles:
                    if body and nid in (src, tgt):
                        continue
                    if sx1 >= bx0 - 4 and sx0 <= bx1 + 4 and sy1 >= by0 - 4 and sy0 <= by1 + 4:
                        return False
            return True

        def gap_left(rank: int) -> int:
            return col_x[rank] + col_w[rank]

        # 1. how each forward flow is drawn
        for e in edges:
            if e.back:
                e.route = "back"
                continue
            src, tgt = nodes[e.src], nodes[e.tgt]
            e.route = "gap"
            if len(e.chain) != 2:
                continue
            if src.rank == tgt.rank:
                e.route = "vertical"
            elif src.kind == "gateway" and tgt.cy > src.y + src.h:
                pts = [(src.cx, src.y + src.h), (src.cx, tgt.cy), (tgt.x, tgt.cy)]
                if clear(pts, e.src, e.tgt):
                    e.route = "vh"
            elif (src.kind != "gateway" and len(outs[e.src]) == 1 and src.lane != tgt.lane
                  and abs(tgt.cy - src.cy) > src.h // 2):
                entry = (tgt.cx, tgt.y) if tgt.cy > src.cy else (tgt.cx, tgt.y + tgt.h)
                pts = [(src.x + src.w, src.cy), (tgt.cx, src.cy), entry]
                if clear(pts, e.src, e.tgt):
                    e.route = "hv"

        # several flows entering the top (or the bottom) of the same step get their own x, the one
        # coming from farther away entering farther right, so their vertical stretches never cross
        sides: dict[tuple[str, bool], list[_Edge]] = {}
        for e in edges:
            if e.route == "hv":
                sides.setdefault((e.tgt, nodes[e.tgt].cy > nodes[e.src].cy), []).append(e)
        for (tid, from_above), group in sides.items():
            tgt = nodes[tid]
            if len(group) == 1 or tgt.kind == "gateway":
                for e in group[1:]:
                    e.route = "gap"
                continue
            group.sort(key=lambda e: nodes[e.src].cy, reverse=not from_above)
            k = len(group)
            step = min(18, (tgt.w - 24) / (k - 1))
            for i, e in enumerate(group):
                e.entry_dy = int(round(((k - 1) / 2 - i) * step))  # x offset for hv flows
                src = nodes[e.src]
                x = tgt.cx + e.entry_dy
                entry = (x, tgt.y) if from_above else (x, tgt.y + tgt.h)
                if not clear([(src.x + src.w, src.cy), (x, src.cy), entry], e.src, e.tgt):
                    e.route, e.entry_dy = "gap", 0

        # 2. flows entering the left side of a step: spread so their last stretches never overlap;
        # into a gateway they meet at the left corner, except one coming from below (bottom corner)
        def approach_y(e: _Edge) -> float:
            if e.route == "back":
                return float("inf")
            return nodes[e.chain[-2]].cy if nodes[e.chain[-2]].kind != "dummy" else nodes[e.chain[-2]].y

        entering: dict[str, list[_Edge]] = {}
        for e in edges:
            if e.route in ("gap", "vh", "back"):
                entering.setdefault(e.tgt, []).append(e)
        for tid, group in entering.items():
            tgt = nodes[tid]
            group.sort(key=lambda e: (approach_y(e), edges.index(e)))
            if tgt.kind == "gateway" or tgt.kind in ("start", "end", "event"):
                for e in group:
                    e.entry_dy = 0
                if tgt.kind == "gateway" and len(group) > 1:
                    low = group[-1]
                    if low.route == "gap" and approach_y(low) > tgt.y + tgt.h + 4:
                        a = nodes[low.chain[-2]]
                        ya = int(approach_y(low))
                        start_x = gap_left(a.rank) if a.kind == "dummy" else a.x + a.w
                        if clear([(start_x, ya), (tgt.cx, ya), (tgt.cx, tgt.y + tgt.h)], low.src, low.tgt):
                            low.bottom_entry = True
                continue
            k = len(group)
            step = min(ENTRY_STEP, (tgt.h - 16) / max(1, k - 1))
            offsets = [(i - (k - 1) / 2) * step for i in range(k)]
            # a flow that arrives level with the step's center keeps entering there, straight
            level = [i for i, e in enumerate(group) if abs(approach_y(e) - tgt.cy) <= 1]
            if level and k > 1:
                room = tgt.h / 2 - 5
                shift = -offsets[level[0]]
                shift = max(-room - offsets[0], min(room - offsets[-1], shift))
                offsets = [o + shift for o in offsets]
            for e, off in zip(group, offsets):
                e.entry_dy = int(round(off))

        # 3. vertical tracks in each gap for hops that change height: fan-outs near the source
        # column, fan-ins near the target column
        def station_y(e: _Edge, i: int) -> int:
            n = nodes[e.chain[i]]
            if n.kind == "dummy":
                return n.y
            if i == len(e.chain) - 1:
                return n.cy + e.entry_dy
            return n.cy

        def hops(e: _Edge):
            last = len(e.chain) - 2
            for i in range(len(e.chain) - 1):
                if i == last and e.bottom_entry:
                    continue
                yield i

        tracks: dict[int, dict[tuple, int]] = {}
        for e in edges:
            if e.route != "gap":
                continue
            for i in hops(e):
                a = nodes[e.chain[i]]
                ya, yb = station_y(e, i), station_y(e, i + 1)
                if ya != yb:
                    key = ("out", a.id) if a.kind != "dummy" and i == 0 else ("in", e.id)
                    tracks.setdefault(a.rank, {}).setdefault(key, ya if key[0] == "out" else yb)
        track_x: dict[tuple[int, tuple], int] = {}
        for gap, keys in tracks.items():
            left = gap_left(gap)
            gap_w = col_gap[gap] if gap < len(col_gap) else COL_GAP
            right = left + gap_w
            fan_out = sorted((k for k in keys if k[0] == "out"), key=lambda k: keys[k])
            fan_in = sorted((k for k in keys if k[0] == "in"), key=lambda k: keys[k])
            half = max(6, gap_w // 2 - 18)
            step = max(4, min(LANE_STEP, half // max(1, max(len(fan_out), len(fan_in)))))
            for i, k in enumerate(fan_out):
                track_x[(gap, k)] = left + 18 + i * step
            for i, k in enumerate(fan_in):
                track_x[(gap, k)] = right - 18 - i * step

        # 4. points and labels
        for e in edges:
            src, tgt = nodes[e.src], nodes[e.tgt]
            if e.route == "back":
                continue
            if e.route == "vertical":
                if tgt.cy > src.cy:
                    e.points = [(src.cx, src.y + src.h), (src.cx, tgt.y)]
                else:
                    e.points = [(src.cx, src.y), (src.cx, tgt.y + tgt.h)]
                if e.name:
                    y0, y1 = sorted((e.points[0][1], e.points[1][1]))
                    w = EDGE_LABEL_W
                    h = _wrap(e.name, w) * LINE_H
                    e.label = (src.cx + 8, (y0 + y1) // 2 - h // 2, w, h)
                continue
            if e.route == "vh":
                y = tgt.cy + e.entry_dy
                e.points = _compress([(src.cx, src.y + src.h), (src.cx, y), (tgt.x, y)])
                if e.name:
                    w = max(40, min(EDGE_LABEL_W, tgt.x - src.cx - 14))
                    h = _wrap(e.name, w) * LINE_H
                    e.label = (src.cx + 8, y - h - 3, w, h)
                continue
            if e.route == "hv":
                x = tgt.cx + e.entry_dy
                entry = (x, tgt.y) if tgt.cy > src.cy else (x, tgt.y + tgt.h)
                e.points = _compress([(src.x + src.w, src.cy), (x, src.cy), entry])
                if e.name:
                    w = max(40, min(EDGE_LABEL_W, tgt.cx - src.x - src.w - 12))
                    h = _wrap(e.name, w) * LINE_H
                    e.label = (src.x + src.w + 6, src.cy - h - 3, w, h)
                continue
            pts = [(src.x + src.w, src.cy)]
            label_seg = None
            last = len(e.chain) - 2
            for i in range(len(e.chain) - 1):
                a, b = nodes[e.chain[i]], nodes[e.chain[i + 1]]
                ya = station_y(e, i)
                start_x = gap_left(a.rank)
                pts.append((start_x, ya))
                if i == last and e.bottom_entry:
                    pts += [(b.cx, ya), (b.cx, b.y + b.h)]
                    if label_seg is None:
                        label_seg = (start_x if i else src.x + src.w, b.cx, ya)
                    break
                yb = station_y(e, i + 1)
                if ya != yb:
                    key = ("out", a.id) if a.kind != "dummy" and i == 0 else ("in", e.id)
                    lx = track_x[(a.rank, key)]
                    pts += [(lx, ya), (lx, yb)]
                    seg = (lx, yb)
                else:
                    seg = (start_x if i else src.x + src.w, yb)
                if b.kind == "dummy":
                    pts += [(col_x[b.rank], yb), (col_x[b.rank] + col_w[b.rank], yb)]
                    end_x = col_x[b.rank] + col_w[b.rank]
                else:
                    pts.append((b.x, yb))
                    end_x = b.x
                if label_seg is None:
                    label_seg = (seg[0], end_x, seg[1])
            e.points = _compress(pts)
            if e.name and label_seg:
                x0, x1, y = label_seg
                w = max(40, min(EDGE_LABEL_W, x1 - x0 - 12))
                h = _wrap(e.name, w) * LINE_H
                e.label = (x0 + 6, y - h - 3, w, h)

        self._separate_labels(edges, obstacles)

        # 5. back edges (loops): out of the source's right side, down to a corridor under the lane
        # (or under the whole diagram), back to the target's column and into its left side
        back = [e for e in edges if e.route == "back"]
        if not back:
            return
        bottom_all = max(n.y + n.h + n.bottom_h for n in real.values())
        per_lane: dict[int, int] = {}
        for k, e in enumerate(back):
            src, tgt = nodes[e.src], nodes[e.tgt]
            if geometry.lanes:
                lane = max(src.lane, tgt.lane)
                slot = per_lane.get(lane, 0)
                per_lane[lane] = slot + 1
                band = geometry.lanes[lane]
                yc = band.y + band.h - 12 - slot * CORRIDOR_STEP
            else:
                yc = bottom_all + 40 + k * 20
            x_out = gap_left(src.rank) + 8 + (k % 4) * 4
            x_in = col_x[tgt.rank] - 8 - (k % 4) * 4
            y_in = tgt.cy + e.entry_dy
            e.points = _compress([
                (src.x + src.w, src.cy), (x_out, src.cy), (x_out, yc),
                (x_in, yc), (x_in, y_in), (tgt.x, y_in),
            ])
            if e.name:
                w = EDGE_LABEL_W
                h = _wrap(e.name, w) * LINE_H
                e.label = (min(x_in, x_out) + 6, yc + 3, w, h)

    @staticmethod
    def _separate_labels(edges: list[_Edge], obstacles) -> None:
        """A flow label that would sit on top of another label (or a shape) moves below its stretch,
        then further down, until it is free."""
        placed: list[tuple[int, int, int, int]] = []

        def hits(box, others) -> bool:
            x, y, w, h = box
            return any(x < ox + ow and ox < x + w and y < oy + oh and oy < y + h for ox, oy, ow, oh in others)

        shapes = [(x0, y0, x1 - x0, y1 - y0) for _, _, (x0, y0, x1, y1) in obstacles]
        for e in edges:
            if not e.label:
                continue
            x, y, w, h = e.label
            candidates = [(x, y), (x, y + h + 6)] + [(x, y + h + 6 + k * LINE_H) for k in range(1, 4)]
            for cx, cy in candidates:
                if not hits((cx, cy, w, h), placed) and not hits((cx, cy, w, h), shapes):
                    e.label = (cx, cy, w, h)
                    break
            placed.append(e.label)

    # ── xml ──────────────────────────────────────────────────────────────────

    def _xml(self, ir: ActivityIR, diagram: _Diagram) -> str:
        for prefix, uri in NAMESPACES.items():
            ET.register_namespace(prefix, uri)
        pid = "Process_1"
        defs = ET.Element(_q("bpmn", "definitions"), {
            "id": "Definitions_1",
            "targetNamespace": "http://spec2viz/bpmn",
            "exporter": "spec2viz",
        })
        geometry = diagram.geometry
        laned = bool(geometry.lanes)
        if laned:
            collab = ET.SubElement(defs, _q("bpmn", "collaboration"), {"id": "Collaboration_1"})
            participant = {"id": "Participant_1", "processRef": pid}
            pool_h = geometry.pool[3]
            if _text_w(ir.title) + 24 <= pool_h:
                participant["name"] = ir.title
            ET.SubElement(collab, _q("bpmn", "participant"), participant)
        proc = ET.SubElement(defs, _q("bpmn", "process"), {"id": pid, "name": ir.title, "isExecutable": "false"})
        if laned:
            lane_set = ET.SubElement(proc, _q("bpmn", "laneSet"), {"id": "LaneSet_1"})
            for lane in geometry.lanes:
                lane_el = ET.SubElement(lane_set, _q("bpmn", "lane"), {"id": lane.id, "name": lane.name})
                for nid in lane.nodes:
                    ET.SubElement(lane_el, _q("bpmn", "flowNodeRef")).text = nid
        planes_by_element = {plane.bpmn_element: plane for plane in diagram.planes}

        def indexes(nodes: dict[str, _Node], edges: list[_Edge]):
            incoming: dict[str, list[str]] = {n: [] for n in nodes}
            outgoing: dict[str, list[str]] = {n: [] for n in nodes}
            for e in edges:
                outgoing[e.src].append(e.id)
                incoming[e.tgt].append(e.id)
            return incoming, outgoing

        def emit_flows(parent: ET.Element, edges: list[_Edge]) -> None:
            for e in edges:
                attrs = {"id": e.id, "sourceRef": e.src, "targetRef": e.tgt}
                if e.name:
                    attrs["name"] = e.name
                ET.SubElement(parent, _q("bpmn", "sequenceFlow"), attrs)

        def annotation_ids(n: _Node) -> tuple[str, str]:
            base = _ncname(n.step or n.id)
            return f"TextAnnotation_{base}", f"Association_{base}"

        def emit_annotations(parent: ET.Element, nodes: dict[str, _Node]) -> None:
            for n in nodes.values():
                if not n.note:
                    continue
                ann_id, assoc_id = annotation_ids(n)
                ann = ET.SubElement(parent, _q("bpmn", "textAnnotation"), {"id": ann_id})
                ET.SubElement(ann, _q("bpmn", "text")).text = n.note
                ET.SubElement(parent, _q("bpmn", "association"),
                              {"id": assoc_id, "sourceRef": n.id, "targetRef": ann_id})

        def emit_element(parent: ET.Element, n: _Node, incoming, outgoing) -> None:
            attrs = {"id": n.id}
            if n.name:
                attrs["name"] = n.name
            el = ET.SubElement(parent, _q("bpmn", n.tag), attrs)
            text = n.detail or n.doc
            if text:
                ET.SubElement(el, _q("bpmn", "documentation")).text = text
            for f in incoming[n.id]:
                ET.SubElement(el, _q("bpmn", "incoming")).text = f
            for f in outgoing[n.id]:
                ET.SubElement(el, _q("bpmn", "outgoing")).text = f
            if n.event_def:
                ET.SubElement(el, _q("bpmn", n.event_def), {"id": f"{n.id}_definition"})
            if n.kind == "subprocess":
                plane = planes_by_element[n.id]
                inner_in, inner_out = indexes(plane.nodes, plane.edges)
                for child in plane.nodes.values():
                    emit_element(el, child, inner_in, inner_out)
                emit_flows(el, plane.edges)
                emit_annotations(el, plane.nodes)

        top_in, top_out = indexes(diagram.nodes, diagram.edges)
        for n in diagram.nodes.values():
            emit_element(proc, n, top_in, top_out)
        emit_flows(proc, diagram.edges)
        emit_annotations(proc, diagram.nodes)

        def emit_shapes(plane_el: ET.Element, nodes: dict[str, _Node], edges: list[_Edge]) -> None:
            gateway_border = {n.id: _tone_colors(n)[1] for n in nodes.values() if n.kind == "gateway"}
            for n in nodes.values():
                attrs = {"id": f"{n.id}_di", "bpmnElement": n.id}
                if n.kind == "gateway":
                    attrs["isMarkerVisible"] = "true"
                if n.kind == "subprocess":
                    attrs["isExpanded"] = "false"
                colors = _tone_colors(n)
                if colors[0]:
                    attrs[_q("color", "background-color")] = colors[0]
                if colors[1]:
                    attrs[_q("color", "border-color")] = colors[1]
                shape = ET.SubElement(plane_el, _q("bpmndi", "BPMNShape"), attrs)
                _bounds(shape, n.x, n.y, n.w, n.h)
                box = n.label_box()
                if box:
                    label = ET.SubElement(shape, _q("bpmndi", "BPMNLabel"))
                    _bounds(label, *box)
            for e in edges:
                attrs = {"id": f"{e.id}_di", "bpmnElement": e.id}
                border = gateway_border.get(e.src)
                if border:
                    attrs[_q("color", "border-color")] = border
                edge = ET.SubElement(plane_el, _q("bpmndi", "BPMNEdge"), attrs)
                for x, y in e.points:
                    ET.SubElement(edge, _q("di", "waypoint"), {"x": str(x), "y": str(y)})
                if e.label:
                    label = ET.SubElement(edge, _q("bpmndi", "BPMNLabel"))
                    _bounds(label, *e.label)
            for n in nodes.values():
                box = n.note_box()
                if not box:
                    continue
                ann_id, assoc_id = annotation_ids(n)
                shape = ET.SubElement(plane_el, _q("bpmndi", "BPMNShape"), {"id": f"{ann_id}_di", "bpmnElement": ann_id})
                _bounds(shape, *box)
                edge = ET.SubElement(plane_el, _q("bpmndi", "BPMNEdge"), {"id": f"{assoc_id}_di", "bpmnElement": assoc_id})
                bx, by, bw, bh = box
                top = n.y - (n.label_h + 6 if (n.label_h and n.kind == "gateway") else 0)
                for x, y in ((n.cx, by + bh), (n.cx, top)):
                    ET.SubElement(edge, _q("di", "waypoint"), {"x": str(x), "y": str(y)})

        top_diagram = ET.SubElement(defs, _q("bpmndi", "BPMNDiagram"), {"id": "BPMNDiagram_1"})
        top_plane = ET.SubElement(top_diagram, _q("bpmndi", "BPMNPlane"),
                                  {"id": "BPMNPlane_1", "bpmnElement": "Collaboration_1" if laned else pid})
        if laned:
            px, py, pw, ph = geometry.pool
            shape = ET.SubElement(top_plane, _q("bpmndi", "BPMNShape"),
                                  {"id": "Participant_1_di", "bpmnElement": "Participant_1", "isHorizontal": "true"})
            _bounds(shape, px, py, pw, ph)
            for i, lane in enumerate(geometry.lanes):
                attrs = {"id": f"{lane.id}_di", "bpmnElement": lane.id, "isHorizontal": "true"}
                if i % 2:
                    attrs[_q("color", "background-color")] = LANE_TINT
                shape = ET.SubElement(top_plane, _q("bpmndi", "BPMNShape"), attrs)
                _bounds(shape, px + POOL_HEADER, lane.y, pw - POOL_HEADER, lane.h)
        emit_shapes(top_plane, diagram.nodes, diagram.edges)

        for plane in diagram.planes:
            suffix = plane.id[len("BPMNPlane_"):]
            sub_diagram = ET.SubElement(defs, _q("bpmndi", "BPMNDiagram"),
                                        {"id": f"BPMNDiagram_{suffix}"})
            sub_plane = ET.SubElement(sub_diagram, _q("bpmndi", "BPMNPlane"),
                                      {"id": plane.id, "bpmnElement": plane.bpmn_element})
            emit_shapes(sub_plane, plane.nodes, plane.edges)

        ET.indent(defs, space="  ")
        body = ET.tostring(defs, encoding="unicode")
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + body + "\n"


def _tone_colors(node: "_Node") -> tuple[str | None, str | None]:
    """The BPMN in Color (background, border) of a node; plain tasks without tone stay default."""
    if node.kind == "start":
        return START_TONE
    if node.kind == "end":
        return END_TONE
    if node.kind == "gateway":
        return TONE_PALETTE.get(node.tone or "", GATEWAY_TONE)
    if node.kind in ("task", "subprocess", "event") and node.tone in TONE_PALETTE:
        return TONE_PALETTE[node.tone]
    return None, None


def _bounds(parent: ET.Element, x: int, y: int, w: int, h: int) -> None:
    ET.SubElement(parent, _q("dc", "Bounds"), {"x": str(int(x)), "y": str(int(y)), "width": str(int(w)), "height": str(int(h))})


def _compress(pts: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Drops repeated points and the middle point of collinear runs."""
    out: list[tuple[int, int]] = []
    for p in pts:
        p = (int(p[0]), int(p[1]))
        if out and out[-1] == p:
            continue
        if len(out) >= 2:
            (x0, y0), (x1, y1) = out[-2], out[-1]
            if (x0 == x1 == p[0]) or (y0 == y1 == p[1]):
                out[-1] = p
                continue
        out.append(p)
    return out


__all__ = ["BpmnRenderer", "render_bpmn_html", "with_xml_provenance", "NAMESPACES", "BPMN_NS"]
