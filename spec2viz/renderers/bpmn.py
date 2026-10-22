"""BPMN renderer: an activity spec as BPMN 2.0 XML with DI, plus an offline bpmn-js viewer page.

`BpmnRenderer().render(ir)` returns the XML of one process (startEvent, a task per step, an
exclusiveGateway per decision/merge step, a sequenceFlow per `next`/branch, one endEvent) and its
BPMN DI computed by a deterministic layered layout:

- ranks: longest path from the sources, left to right, over the graph without its back edges
  (found by a DFS from the start event in spec order);
- an edge that spans several ranks gets one dummy slot per intermediate rank, so it runs in its
  own horizontal lane instead of crossing the nodes in between;
- order inside a rank: discovery order refined by a few barycenter sweeps;
- y: slots stacked per rank and the rank centered on the tallest one; x: one column per rank;
- waypoints: orthogonal, leaving a node on its right, changing height only in the gaps between
  columns, entering the target on its left; back edges go around below the diagram.

`render_bpmn_html(xml, title, metadata)` wraps that XML in a self-contained page that inlines
the vendored bpmn-js NavigatedViewer (spec2viz/templates/vendor/bpmn-js), so it works from file://.
"""

from __future__ import annotations

import html
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from spec2viz.exceptions import RenderError
from spec2viz.ir import ActivityIR

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
BPMNDI_NS = "http://www.omg.org/spec/BPMN/20100524/DI"
DC_NS = "http://www.omg.org/spec/DD/20100524/DC"
DI_NS = "http://www.omg.org/spec/DD/20100524/DI"
COLOR_NS = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"
NAMESPACES = {"bpmn": BPMN_NS, "bpmndi": BPMNDI_NS, "dc": DC_NS, "di": DI_NS, "color": COLOR_NS}

VENDOR_DIR = Path(__file__).resolve().parent.parent / "templates" / "vendor" / "bpmn-js"

GATEWAY_KINDS = {"decision", "merge"}

# BPMN in Color (non-normative color namespace): (background, border) per tone. Soft fills with
# dark borders, chosen to keep the 12px dark text and the 2px outline readable.
TONE_PALETTE: dict[str, tuple[str, str]] = {
    "success": ("#E3F4E6", "#2E7D32"),
    "warning": ("#FFEFC7", "#B26A00"),
    "danger": ("#FBE3E3", "#B42318"),
    "info": ("#E1EEFB", "#1D4ED8"),
    "neutral": ("#EEF0F3", "#6B7280"),
    "rule1": ("#EDE9FE", "#6D4AFF"),
    "rule2": ("#FDE7D9", "#C2410C"),
    "rule3": ("#DCF5EE", "#0F766E"),
    "rule4": ("#FDE7F1", "#BE185D"),
    "rule5": ("#EAF0D8", "#4D7C0F"),
}
GATEWAY_TONE = ("#F4F0FB", "#7E57C2")
START_TONE = ("#E3F4E6", "#2E7D32")
END_TONE = ("#FBE3E3", "#8B1A1A")
TONE_LABELS = {
    "success": "success · resultado favorable",
    "warning": "warning · atención",
    "danger": "danger · rechazo",
    "info": "info · informativo",
    "neutral": "neutral · sin marca",
    "rule1": "rule1 · regla 1",
    "rule2": "rule2 · regla 2",
    "rule3": "rule3 · regla 3",
    "rule4": "rule4 · regla 4",
    "rule5": "rule5 · regla 5",
}

# geometry (px); bpmn-js draws text in 12px Arial, ~6.5px per character on average
CHAR_W = 6.6
LINE_H = 15
TASK_MAX_W = 220
TASK_MIN_W = 120
TASK_PAD = 16      # text padding inside a task (bpmn-js wraps at width - 12)
TASK_MIN_H = 60
GATEWAY = 50
EVENT = 36
GATEWAY_LABEL_W = 190
EDGE_LABEL_W = 150
COL_GAP = 190
NODE_GAP = 44
DUMMY_GAP = 30
PARALLEL_STEP = 36
MARGIN = 60
LANE_STEP = 10


def _q(ns: str, tag: str) -> str:
    return f"{{{NAMESPACES[ns]}}}{tag}"


def _ncname(raw: str) -> str:
    """An XML NCName from a step id: invalid characters become `_`."""
    s = re.sub(r"[^A-Za-z0-9_.-]", "_", raw)
    if not s or not re.match(r"[A-Za-z_]", s[0]):
        s = "_" + s
    return s


def _task_box(label: str) -> tuple[int, int]:
    """A task box sized to its label: wrapped at most at TASK_MAX_W, at least TASK_MIN_W wide."""
    longest = max((len(word) for word in label.split()), default=1)
    natural = longest * CHAR_W + TASK_PAD
    w = int(min(TASK_MAX_W, max(TASK_MIN_W, natural)))
    lines = _wrap(label, w - TASK_PAD + 4)
    return w, max(TASK_MIN_H, lines * LINE_H + 24)


def _wrap(text: str, width_px: float) -> int:
    """Number of lines `text` takes when word-wrapped in `width_px`."""
    per_line = max(1, int(width_px / CHAR_W))
    lines, current = 1, 0
    for word in text.split():
        n = len(word)
        while n > per_line:  # a word longer than the line is broken
            if current:
                lines += 1
            current = 0
            n -= per_line
            lines += 1
        if current and current + 1 + n > per_line:
            lines += 1
            current = n
        else:
            current = current + (1 if current else 0) + n
    return lines


@dataclass
class _Node:
    id: str            # BPMN id
    kind: str          # start | end | task | gateway | dummy
    name: str = ""
    step: str | None = None
    doc: str | None = None
    tone: str | None = None
    w: int = 0
    h: int = 0
    label_h: int = 0   # external label above (gateways)
    rank: int = 0
    x: int = 0
    y: int = 0

    @property
    def slot_h(self) -> int:
        return self.h + (self.label_h + 6 if self.label_h else 0)

    @property
    def cy(self) -> int:
        return self.y + self.h // 2


@dataclass
class _Edge:
    id: str
    src: str
    tgt: str
    name: str = ""
    back: bool = False
    chain: list[str] = field(default_factory=list)  # src, dummies..., tgt
    entry_dy: int = 0
    points: list[tuple[int, int]] = field(default_factory=list)
    label: tuple[int, int, int, int] | None = None


class BpmnRenderer:
    """Renders an ActivityIR as BPMN 2.0 XML with diagram interchange (DI)."""

    def render(self, ir) -> str:
        if not isinstance(ir, ActivityIR):
            raise RenderError(f"BpmnRenderer cannot render {type(ir).__name__}")
        nodes, edges = self._graph(ir)
        self._layout(nodes, edges)
        return self._xml(ir, nodes, edges)

    # ── graph ────────────────────────────────────────────────────────────────

    def _graph(self, ir: ActivityIR) -> tuple[dict[str, _Node], list[_Edge]]:
        used: set[str] = set()

        def uid(base: str) -> str:
            cand, i = base, 2
            while cand in used:
                cand, i = f"{base}_{i}", i + 1
            used.add(cand)
            return cand

        nodes: dict[str, _Node] = {}
        start = _Node(uid(f"StartEvent_{_ncname(ir.start)}"), "start", w=EVENT, h=EVENT)
        nodes[start.id] = start
        by_step: dict[str, str] = {}
        for step in ir.steps:
            label = step.label or step.id
            if step.kind in GATEWAY_KINDS:
                node = _Node(uid(f"Gateway_{_ncname(step.id)}"), "gateway", label, step.id, step.notes,
                             tone=step.tone, w=GATEWAY, h=GATEWAY,
                             label_h=_wrap(label, GATEWAY_LABEL_W) * LINE_H)
            else:
                w, h = _task_box(label)
                node = _Node(uid(f"Task_{_ncname(step.id)}"), "task", label, step.id, step.notes,
                             tone=step.tone, w=w, h=h)
            nodes[node.id] = node
            by_step[step.id] = node.id
        end = _Node(uid(f"EndEvent_{_ncname(ir.end)}"), "end", w=EVENT, h=EVENT)
        nodes[end.id] = end

        def target(ref: str) -> str:
            if ref in by_step:
                return by_step[ref]
            if ref == ir.end:
                return end.id
            raise RenderError(f"Activity reference '{ref}' is neither a step nor the end")

        pairs: list[tuple[str, str, str]] = []
        if ir.start not in by_step:
            raise RenderError(f"Start step '{ir.start}' not found")
        pairs.append((start.id, by_step[ir.start], ""))
        for step in ir.steps:
            src = by_step[step.id]
            outs = [(label, target(t)) for label, t in step.branches.items()]
            if step.next:
                outs.append(("", target(step.next)))
            if not outs:  # a step without outgoing flow is terminal: it ends the process
                outs.append(("", end.id))
            for label, tgt in outs:
                pairs.append((src, tgt, label))

        key = {start.id: "start", end.id: "end"}
        key.update({nid: _ncname(sid) for sid, nid in by_step.items()})
        edges: list[_Edge] = []
        for src, tgt, label in pairs:
            base = f"Flow_{key[src]}__{key[tgt]}"
            edges.append(_Edge(uid(base), src, tgt, label))
        return nodes, edges

    # ── layout ───────────────────────────────────────────────────────────────

    def _layout(self, nodes: dict[str, _Node], edges: list[_Edge]) -> None:
        real = list(nodes)
        out: dict[str, list[_Edge]] = {n: [] for n in real}
        for e in edges:
            out[e.src].append(e)

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

        # longest-path ranks on the DAG (Kahn's order)
        fwd = [e for e in edges if not e.back]
        indeg = {n: 0 for n in real}
        for e in fwd:
            indeg[e.tgt] += 1
        queue = [n for n in order if indeg[n] == 0]
        rank = {n: 0 for n in real}
        while queue:
            n = queue.pop(0)
            for e in out[n]:
                if e.back:
                    continue
                rank[e.tgt] = max(rank[e.tgt], rank[n] + 1)
                indeg[e.tgt] -= 1
                if indeg[e.tgt] == 0:
                    queue.append(e.tgt)
        end_id = next(n for n in real if nodes[n].kind == "end")
        rank[end_id] = max(rank.values()) if len(real) > 1 else 0
        if any(rank[n] == rank[end_id] and n != end_id for n in real):
            rank[end_id] += 1
        for n in real:
            nodes[n].rank = rank[n]

        # dummies for long forward edges
        all_nodes: dict[str, _Node] = dict(nodes)
        for e in edges:
            e.chain = [e.src, e.tgt]
            if e.back:
                continue
            rs, rt = rank[e.src], rank[e.tgt]
            if rt - rs > 1:
                dummies = []
                for r in range(rs + 1, rt):
                    d = _Node(f"__dummy_{e.id}_{r}", "dummy", w=0, h=0, rank=r)
                    all_nodes[d.id] = d
                    dummies.append(d.id)
                e.chain = [e.src, *dummies, e.tgt]

        # parallel flows between the same pair enter the target at different heights
        groups: dict[tuple[str, str], list[_Edge]] = {}
        for e in edges:
            if not e.back:
                groups.setdefault((e.src, e.tgt), []).append(e)
        for group in groups.values():
            k = len(group)
            for i, e in enumerate(group):
                e.entry_dy = int((i - (k - 1) / 2) * PARALLEL_STEP)

        # order inside each rank: discovery order, then barycenter sweeps
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
        # dummies are discovered right after their edge's source
        dkey: dict[str, float] = {}
        for e in edges:
            for j, d in enumerate(e.chain[1:-1]):
                dkey[d] = disc[e.src] + 0.001 * (edges.index(e) + 1)
        for nid, n in all_nodes.items():
            layers[n.rank].append(nid)
        for layer in layers:
            layer.sort(key=lambda n: disc.get(n, dkey.get(n, 0.0)))

        def sweep(down: bool) -> None:
            rng = range(1, len(layers)) if down else range(len(layers) - 2, -1, -1)
            for r in rng:
                ref = layers[r - 1] if down else layers[r + 1]
                pos = {n: i for i, n in enumerate(ref)}
                cur = {n: i for i, n in enumerate(layers[r])}

                def bary(n: str) -> float:
                    nb = [pos[m] for m in (pred[n] if down else succ[n]) if m in pos]
                    return sum(nb) / len(nb) if nb else float(cur[n])

                layers[r].sort(key=lambda n: (bary(n), cur[n]))

        for _ in range(4):
            sweep(True)
            sweep(False)
        sweep(True)

        # x per column, y per slot (each column centered on the tallest)
        # a gateway's column is as wide as its label, so the label never reaches into a gap
        col_w = [max((GATEWAY_LABEL_W if all_nodes[n].label_h else all_nodes[n].w for n in layer), default=0) or EVENT
                 for layer in layers]
        col_x, x = [], MARGIN
        for w in col_w:
            col_x.append(x)
            x += w + COL_GAP
        # y: each rank starts stacked, then every slot is pulled toward the median of its neighbors
        # in the next/previous rank; the order and minimum gaps hold (isotonic regression per rank)
        def head(n: _Node) -> float:  # slot top -> center
            return (n.label_h + 6 if n.label_h else 0) + n.h / 2

        def gap(a: _Node, b: _Node) -> int:
            return DUMMY_GAP if (a.kind == "dummy" and b.kind == "dummy") else NODE_GAP

        def offsets(layer: list[str]) -> list[float]:
            offs, acc = [], 0.0
            for i, nid in enumerate(layer):
                if i:
                    a, b = all_nodes[layer[i - 1]], all_nodes[nid]
                    acc += a.h / 2 + gap(a, b) + head(b)
                offs.append(acc)
            return offs

        center: dict[str, float] = {}
        for layer in layers:
            for nid, off in zip(layer, offsets(layer)):
                center[nid] = off

        def median(vals: list[float]) -> float:
            vals = sorted(vals)
            m = len(vals) // 2
            return vals[m] if len(vals) % 2 else (vals[m - 1] + vals[m]) / 2

        def place(layer: list[str], neighbors) -> None:
            offs = offsets(layer)
            z = []
            for nid, off in zip(layer, offs):
                nb = [center[m] for m in neighbors(nid)]
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

        shift = MARGIN - min(center[n] - head(all_nodes[n]) for n in all_nodes)
        for r, layer in enumerate(layers):
            for nid in layer:
                node = all_nodes[nid]
                node.x = col_x[r] + (col_w[r] - node.w) // 2
                node.y = int(round(center[nid] + shift - node.h / 2))

        self._route(all_nodes, edges, col_x, col_w)

    def _route(self, nodes: dict[str, _Node], edges: list[_Edge], col_x: list[int], col_w: list[int]) -> None:
        # hops in each gap that change height get a vertical lane: fan-outs near the source column,
        # fan-ins near the target column
        hops: list[tuple[_Edge, int, int, int, int]] = []  # edge, hop index, gap, y_from, y_to

        def station_y(e: _Edge, i: int) -> int:
            n = nodes[e.chain[i]]
            if n.kind == "dummy":
                return n.y
            if i == len(e.chain) - 1:
                return n.cy + max(-(n.h // 2) + 6, min(n.h // 2 - 6, e.entry_dy))
            return n.cy

        lanes: dict[int, dict[tuple, int]] = {}
        for e in edges:
            if e.back:
                continue
            for i in range(len(e.chain) - 1):
                a = nodes[e.chain[i]]
                ya, yb = station_y(e, i), station_y(e, i + 1)
                hops.append((e, i, a.rank, ya, yb))
                if ya != yb:
                    key = ("out", a.id) if a.kind != "dummy" else ("in", e.chain[i + 1], yb)
                    lanes.setdefault(a.rank, {}).setdefault(key, ya)
        lane_x: dict[tuple[int, tuple], int] = {}
        for gap, keys in lanes.items():
            left = col_x[gap] + col_w[gap]
            right = left + COL_GAP
            outs = sorted((k for k in keys if k[0] == "out"), key=lambda k: keys[k])
            ins = sorted((k for k in keys if k[0] == "in"), key=lambda k: keys[k])
            for i, k in enumerate(outs):
                lane_x[(gap, k)] = left + 18 + i * LANE_STEP
            for i, k in enumerate(ins):
                lane_x[(gap, k)] = right - 18 - i * LANE_STEP

        for e in edges:
            if e.back:
                continue
            src, tgt = nodes[e.src], nodes[e.tgt]
            pts = [(src.x + src.w, src.cy)]
            label_seg = None
            for i in range(len(e.chain) - 1):
                a, b = nodes[e.chain[i]], nodes[e.chain[i + 1]]
                ya, yb = station_y(e, i), station_y(e, i + 1)
                gap_left = col_x[a.rank] + col_w[a.rank]
                pts.append((gap_left, ya))
                if ya != yb:
                    key = ("out", a.id) if a.kind != "dummy" else ("in", b.id, yb)
                    lx = lane_x[(a.rank, key)]
                    pts += [(lx, ya), (lx, yb)]
                    seg = (lx, yb)
                else:
                    seg = (gap_left if i else src.x + src.w, yb)
                if b.kind == "dummy":
                    pts += [(col_x[b.rank], yb), (col_x[b.rank] + col_w[b.rank], yb)]
                    end_x = col_x[b.rank] + col_w[b.rank]
                else:
                    pts.append((tgt.x, yb))
                    end_x = tgt.x
                if label_seg is None:
                    label_seg = (seg[0], end_x, seg[1])
            e.points = _compress(pts)
            if e.name and label_seg:
                x0, x1, y = label_seg
                w = max(40, min(EDGE_LABEL_W, x1 - x0 - 12))
                h = _wrap(e.name, w) * 14
                e.label = (x0 + 6, y - h - 3, w, h)

        # back edges loop below everything
        bottom = max(n.y + n.h for n in nodes.values() if n.kind != "dummy")
        for k, e in enumerate(x for x in edges if x.back):
            src, tgt = nodes[e.src], nodes[e.tgt]
            yl = bottom + 40 + k * 20
            e.points = _compress([
                (src.x + src.w // 2, src.y + src.h), (src.x + src.w // 2, yl),
                (tgt.x + tgt.w // 2, yl), (tgt.x + tgt.w // 2, tgt.y + tgt.h),
            ])
            if e.name:
                w = EDGE_LABEL_W
                h = _wrap(e.name, w) * 14
                e.label = (min(src.x, tgt.x) + src.w // 2 + 6, yl + 3, w, h)

    # ── xml ──────────────────────────────────────────────────────────────────

    def _xml(self, ir: ActivityIR, nodes: dict[str, _Node], edges: list[_Edge]) -> str:
        for prefix, uri in NAMESPACES.items():
            ET.register_namespace(prefix, uri)
        pid = "Process_1"
        defs = ET.Element(_q("bpmn", "definitions"), {
            "id": "Definitions_1",
            "targetNamespace": "http://spec2viz/bpmn",
            "exporter": "spec2viz",
        })
        proc = ET.SubElement(defs, _q("bpmn", "process"), {"id": pid, "name": ir.title, "isExecutable": "false"})
        tags = {"start": "startEvent", "end": "endEvent", "task": "task", "gateway": "exclusiveGateway"}
        incoming: dict[str, list[str]] = {n: [] for n in nodes}
        outgoing: dict[str, list[str]] = {n: [] for n in nodes}
        for e in edges:
            outgoing[e.src].append(e.id)
            incoming[e.tgt].append(e.id)
        for n in nodes.values():
            attrs = {"id": n.id}
            if n.name:
                attrs["name"] = n.name
            el = ET.SubElement(proc, _q("bpmn", tags[n.kind]), attrs)
            if n.doc:
                ET.SubElement(el, _q("bpmn", "documentation")).text = n.doc
            for f in incoming[n.id]:
                ET.SubElement(el, _q("bpmn", "incoming")).text = f
            for f in outgoing[n.id]:
                ET.SubElement(el, _q("bpmn", "outgoing")).text = f
        for e in edges:
            attrs = {"id": e.id, "sourceRef": e.src, "targetRef": e.tgt}
            if e.name:
                attrs["name"] = e.name
            ET.SubElement(proc, _q("bpmn", "sequenceFlow"), attrs)

        diagram = ET.SubElement(defs, _q("bpmndi", "BPMNDiagram"), {"id": "BPMNDiagram_1"})
        plane = ET.SubElement(diagram, _q("bpmndi", "BPMNPlane"), {"id": "BPMNPlane_1", "bpmnElement": pid})
        gateway_border = {n.id: _tone_colors(n)[1] for n in nodes.values() if n.kind == "gateway"}
        for n in nodes.values():
            attrs = {"id": f"{n.id}_di", "bpmnElement": n.id}
            if n.kind == "gateway":
                attrs["isMarkerVisible"] = "true"
            colors = _tone_colors(n)
            if colors[0]:
                attrs[_q("color", "background-color")] = colors[0]
            if colors[1]:
                attrs[_q("color", "border-color")] = colors[1]
            shape = ET.SubElement(plane, _q("bpmndi", "BPMNShape"), attrs)
            _bounds(shape, n.x, n.y, n.w, n.h)
            if n.kind == "gateway":
                lw = GATEWAY_LABEL_W
                label = ET.SubElement(shape, _q("bpmndi", "BPMNLabel"))
                _bounds(label, n.x + n.w // 2 - lw // 2, n.y - n.label_h - 6, lw, n.label_h)
        for e in edges:
            attrs = {"id": f"{e.id}_di", "bpmnElement": e.id}
            border = gateway_border.get(e.src)
            if border:
                attrs[_q("color", "border-color")] = border
            edge = ET.SubElement(plane, _q("bpmndi", "BPMNEdge"), attrs)
            for x, y in e.points:
                ET.SubElement(edge, _q("di", "waypoint"), {"x": str(x), "y": str(y)})
            if e.label:
                label = ET.SubElement(edge, _q("bpmndi", "BPMNLabel"))
                _bounds(label, *e.label)

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
    if node.kind == "task" and node.tone in TONE_PALETTE:
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


# ── viewer page ──────────────────────────────────────────────────────────────

def _vendor(name: str) -> str:
    path = VENDOR_DIR / name
    if not path.exists():
        raise RenderError(f"Vendored bpmn-js asset missing: {path}")
    return path.read_text(encoding="utf-8")


def _script_safe(text: str) -> str:
    """Text that can sit inside an inline <script> or <style> element."""
    return re.sub(r"</(script|style)", r"<\\/\1", text, flags=re.IGNORECASE)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@@TITLE@@</title>
<style>
@@DIAGRAM_CSS@@
</style>
<style>
@@BPMN_CSS@@
</style>
<style>
  html, body { margin: 0; height: 100%; font-family: system-ui, -apple-system, "Segoe UI", Arial, sans-serif; color: #1f2328; background: #fff; }
  body { display: flex; flex-direction: column; }
  header { padding: 14px 22px 10px; border-bottom: 1px solid #d0d7de; flex: 0 0 auto; max-height: 38vh; overflow: auto; }
  header h1 { font-size: 20px; margin: 0 0 6px; }
  header p { margin: 4px 0; font-size: 14px; line-height: 1.45; max-width: 120ch; }
  header h2 { font-size: 14px; margin: 10px 0 4px; }
  header ul { margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.45; max-width: 120ch; }
  .legend { display: flex; flex-wrap: wrap; gap: 4px 16px; margin: 8px 0 2px; font-size: 13px; align-items: center; }
  .legend .item { display: inline-flex; align-items: center; gap: 6px; }
  .legend .swatch { width: 16px; height: 14px; border-radius: 3px; border: 2px solid #555; box-sizing: border-box; }
  .legend .title { font-weight: 600; margin-right: 2px; }
  .toolbar { display: flex; gap: 6px; margin-top: 8px; }
  .toolbar button { font: inherit; font-size: 13px; padding: 3px 10px; border: 1px solid #d0d7de; background: #f6f8fa; border-radius: 5px; cursor: pointer; }
  #canvas { flex: 1 1 auto; min-height: 360px; position: relative; }
  #error { color: #b42318; font-size: 13px; white-space: pre-wrap; }
</style>
</head>
<body>
<header>
  <h1>@@TITLE@@</h1>
@@META@@
@@LEGEND@@
  <div class="toolbar">
    <button type="button" id="fit">Fit</button>
    <button type="button" id="zoom-in">Zoom +</button>
    <button type="button" id="zoom-out">Zoom &minus;</button>
  </div>
  <div id="error"></div>
</header>
<div id="canvas"></div>
<script>
@@VIEWER_JS@@
</script>
<script>
(function () {
  var xml = @@XML_JSON@@;
  var viewer = new BpmnJS({ container: '#canvas' });
  window.bpmnViewer = viewer;
  var MIN_ZOOM = 0.6;  // fit, then never show the diagram smaller than this
  function fit() {
    var canvas = viewer.get('canvas');
    canvas.zoom('fit-viewport', 'auto');
    if (canvas.zoom() < MIN_ZOOM) {
      // too big to fit legibly: zoom in and start at the diagram's left edge,
      // with the start event in view, instead of in the middle of the flow
      canvas.zoom(MIN_ZOOM);
      var start = viewer.get('elementRegistry').filter(function (el) {
        return el.type === 'bpmn:StartEvent';
      })[0];
      if (start) {
        var box = canvas.getAbsoluteBBox(start);
        var outer = canvas.viewbox().outer;
        canvas.scroll({ dx: 40 - box.x, dy: Math.round(outer.height * 0.4) - box.y });
      }
    }
  }
  viewer.importXML(xml).then(function (result) {
    if (result.warnings && result.warnings.length) { console.warn('bpmn-js import warnings', result.warnings); }
    fit();
    window.bpmnReady = true;
  }).catch(function (err) {
    document.getElementById('error').textContent = 'Could not render the BPMN diagram: ' + err.message;
    console.error(err);
  });
  document.getElementById('fit').addEventListener('click', fit);
  document.getElementById('zoom-in').addEventListener('click', function () { viewer.get('zoomScroll').stepZoom(1); });
  document.getElementById('zoom-out').addEventListener('click', function () { viewer.get('zoomScroll').stepZoom(-1); });
  window.addEventListener('resize', function () { viewer.get('canvas').resized(); });
})();
</script>
</body>
</html>
"""


def _legend_html() -> str:
    items = []
    for tone, (background, border) in TONE_PALETTE.items():
        label = TONE_LABELS.get(tone, tone)
        items.append(
            f'    <span class="item"><i class="swatch" style="background:{background};border-color:{border}"></i>'
            f"{html.escape(label)}</span>"
        )
    for label, (background, border) in (
        ("Gateway por defecto", GATEWAY_TONE),
        ("Inicio", START_TONE),
        ("Fin", END_TONE),
    ):
        items.append(
            f'    <span class="item"><i class="swatch" style="background:{background};border-color:{border}"></i>'
            f"{html.escape(label)}</span>"
        )
    return '  <div class="legend" aria-label="Leyenda de colores">\n    <span class="title">Colores:</span>\n' + "\n".join(items) + "\n  </div>"


def _meta_html(metadata: dict | None) -> str:
    if not isinstance(metadata, dict):
        return ""
    parts = []
    desc = metadata.get("description")
    if desc:
        parts.append(f"  <p class=\"description\">{html.escape(str(desc).strip())}</p>")
    questions = metadata.get("preguntas_abiertas")
    if isinstance(questions, str):
        questions = [questions]
    if questions:
        items = "\n".join(f"    <li>{html.escape(str(q))}</li>" for q in questions)
        parts.append(f"  <h2>Preguntas abiertas</h2>\n  <ul class=\"preguntas-abiertas\">\n{items}\n  </ul>")
    return "\n".join(parts)


def render_bpmn_html(xml: str, title: str, metadata: dict | None = None) -> str:
    """A self-contained page that renders `xml` with the vendored bpmn-js NavigatedViewer."""
    # JSON with `<`, `>` and `&` escaped can never close the script element it lives in
    xml_json = json.dumps(xml).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    values = {
        "@@DIAGRAM_CSS@@": _script_safe(_vendor("diagram-js.css")),
        "@@BPMN_CSS@@": _script_safe(_vendor("bpmn-js.css")),
        "@@VIEWER_JS@@": _script_safe(_vendor("bpmn-navigated-viewer.production.min.js")),
        "@@XML_JSON@@": xml_json,
        "@@META@@": _meta_html(metadata),
        "@@LEGEND@@": _legend_html(),
        "@@TITLE@@": html.escape(title),
    }
    return re.sub("|".join(re.escape(k) for k in values), lambda m: values[m.group(0)], HTML_TEMPLATE)


def provenance_comment(text: str) -> str:
    """`text` as an XML comment (`--` is not allowed inside one)."""
    return "<!-- " + text.replace("--", "- -") + " -->\n"


def with_xml_provenance(xml: str, header: str) -> str:
    """The XML with a provenance comment right after its declaration."""
    decl, sep, rest = xml.partition("\n")
    if not decl.startswith("<?xml"):
        return provenance_comment(header) + xml
    return decl + sep + provenance_comment(header) + rest


__all__ = ["BpmnRenderer", "render_bpmn_html", "with_xml_provenance", "NAMESPACES", "BPMN_NS"]
