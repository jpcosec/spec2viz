from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

from spec2viz.exceptions import RenderError
from spec2viz.ir import ActivityIR
from spec2viz.renderers.bpmn_palette import (
    END_TONE,
    GATEWAY_TONE,
    START_TONE,
    TONE_PALETTE,
)
from spec2viz.renderers.bpmn_viewer import render_bpmn_html, with_xml_provenance

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
BPMNDI_NS = "http://www.omg.org/spec/BPMN/20100524/DI"
DC_NS = "http://www.omg.org/spec/DD/20100524/DC"
DI_NS = "http://www.omg.org/spec/DD/20100524/DI"
COLOR_NS = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"
NAMESPACES = {"bpmn": BPMN_NS, "bpmndi": BPMNDI_NS, "dc": DC_NS, "di": DI_NS, "color": COLOR_NS}

GATEWAY_KINDS = {"decision", "merge"}

# geometry (px); the viewer draws text at TEXT_FONT_SIZE in Arial, so a character's width
# depends on its class: uppercase, '_', 'm' and 'w' are wide, lowercase and digits medium,
# spaces and thin punctuation narrow
TEXT_FONT_SIZE = 14
CHAR_W_WIDE = 9.8
CHAR_W_LOWER = 7.7
CHAR_W_NARROW = 4.0
LINE_H = 17
TASK_MAX_W = 240
TASK_MIN_W = 120
TASK_PAD = 16      # text padding inside a task (bpmn-js wraps at width - 12)
TASK_MIN_H = 64
GATEWAY = 50
EVENT = 36
GATEWAY_LABEL_W = 190
EDGE_LABEL_W = 150
COL_GAP = 190
MIN_COL_GAP = 70
NODE_GAP = 44
DUMMY_GAP = 30
PARALLEL_STEP = 36
MARGIN = 60
LANE_STEP = 10
SUB_MIN_W = 150
SUB_MIN_H = 80
SHORT_LABEL = 42

# punctuation and separators that take almost no room in Arial 14
_NARROW_CHARS = set(" .,:;!?'\"`|()[]{}-–—/\\·&")
# lower-case letters that are as wide as an uppercase one
_WIDE_LOWER = set("mw")


def _q(ns: str, tag: str) -> str:
    return f"{{{NAMESPACES[ns]}}}{tag}"


def _ncname(raw: str) -> str:
    """An XML NCName from a step id: invalid characters become `_`."""
    s = re.sub(r"[^A-Za-z0-9_.-]", "_", raw)
    if not s or not re.match(r"[A-Za-z_]", s[0]):
        s = "_" + s
    return s


def _char_w(ch: str) -> float:
    """Estimated advance of `ch` in Arial 14px."""
    if ch in _NARROW_CHARS:
        return CHAR_W_NARROW
    if ch.isupper() or ch == "_" or ch in _WIDE_LOWER:
        return CHAR_W_WIDE
    return CHAR_W_LOWER


def _text_w(text: str) -> float:
    """Estimated rendered width of `text` in Arial 14px."""
    return sum(_char_w(ch) for ch in text)


def _task_box(label: str) -> tuple[int, int]:
    """A task box sized to its label: wrapped at most at TASK_MAX_W, at least TASK_MIN_W wide."""
    longest = max((_text_w(word) for word in label.split()), default=CHAR_W_LOWER)
    natural = longest + TASK_PAD
    w = int(min(TASK_MAX_W, max(TASK_MIN_W, natural)))
    lines = _wrap(label, w - TASK_PAD + 4)
    return w, max(TASK_MIN_H, lines * LINE_H + 24)


def _sub_box(label: str) -> tuple[int, int]:
    """A collapsed subprocess: compact by default, growing with its label."""
    natural = _text_w(label) + TASK_PAD
    w = int(min(TASK_MAX_W, max(SUB_MIN_W, natural)))
    lines = _wrap(label, w - TASK_PAD + 4)
    return w, max(SUB_MIN_H, lines * LINE_H + 24)


def _wrap(text: str, width_px: float) -> int:
    """Number of lines `text` takes when word-wrapped in `width_px`."""
    width = max(CHAR_W_NARROW, float(width_px))
    lines, current = 1, 0.0
    for word in text.split():
        w = _text_w(word)
        if current and current + CHAR_W_NARROW + w <= width:
            current += CHAR_W_NARROW + w
            continue
        if current:
            lines += 1
            current = 0.0
        while w > width:  # only a word wider than the whole line is broken
            w -= width
            lines += 1
        current = w
    return lines


@dataclass
class _Node:
    id: str            # BPMN id
    kind: str          # start | end | task | gateway | dummy
    name: str = ""
    step: str | None = None
    doc: str | None = None
    detail: str | None = None
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


class BpmnRenderer:
    """Renders an ActivityIR as BPMN 2.0 XML with diagram interchange (DI)."""

    def render(self, ir) -> str:
        if not isinstance(ir, ActivityIR):
            raise RenderError(f"BpmnRenderer cannot render {type(ir).__name__}")
        diagram = self._build(ir)
        self._layout(diagram.nodes, diagram.edges)
        for plane in diagram.planes:
            self._layout(plane.nodes, plane.edges)
        return self._xml(ir, diagram)

    def _build(self, ir: ActivityIR) -> _Diagram:
        if not ir.groups:
            nodes, edges = self._graph(ir)
            return _Diagram(nodes, edges)
        return self._grouped_graph(ir)

    @staticmethod
    def _step_node(uid, step) -> _Node:
        label = step.label or step.id
        if step.kind in GATEWAY_KINDS:
            return _Node(uid(f"Gateway_{_ncname(step.id)}"), "gateway", label, step.id, step.notes,
                         detail=step.detail, tone=step.tone, w=GATEWAY, h=GATEWAY,
                         label_h=_wrap(label, GATEWAY_LABEL_W) * LINE_H)
        w, h = _task_box(label)
        return _Node(uid(f"Task_{_ncname(step.id)}"), "task", label, step.id, step.notes,
                     detail=step.detail, tone=step.tone, w=w, h=h)

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

        top_start = _Node(uid(f"StartEvent_{_ncname(ir.start)}"), "start", w=EVENT, h=EVENT)
        top_nodes[top_start.id] = top_start
        for gid, group in ir.groups.items():
            if not any(step.group == gid for step in ir.steps):
                raise RenderError(f"Group '{gid}' has no steps")
            nid = uid(f"SubProcess_{_ncname(gid)}")
            group_node[gid] = nid
            sub_w, sub_h = _sub_box(group.label or gid)
            top_nodes[nid] = _Node(
                nid, "subprocess", group.label or gid, doc=group.detail, tone=group.tone,
                w=sub_w, h=sub_h,
            )
            level_nodes[gid] = {}
            level_edges[gid] = []
            planes[gid] = _Plane(uid(f"BPMNPlane_{_ncname(gid)}"), nid, level_nodes[gid], level_edges[gid])

        node_of: dict[str, str] = {}
        for step in ir.steps:
            node = self._step_node(uid, step)
            level = step.group
            level_nodes[level][node.id] = node
            node_of[step.id] = node.id
            step_level[step.id] = level

        top_end = _Node(uid(f"EndEvent_{_ncname(ir.end)}"), "end", w=EVENT, h=EVENT)
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
                        end_node = _Node(end_id, "end", self._short(name), w=EVENT, h=EVENT)
                        level_nodes[src_level][end_id] = end_node
                        external_out[src_level][key] = (tgt_level, tgt, end_id)
                    add_edge(src_level, node_of[step.id], external_out[src_level][key][2], label)

        # the internal start event feeds every step that received a flow from outside
        for gid, entries in external_in.items():
            unique = list(dict.fromkeys(entries))
            if not unique:
                continue
            start = _Node(uid(f"StartEvent_{_ncname(gid)}__in"), "start", w=EVENT, h=EVENT)
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
        ends = [n for n in real if nodes[n].kind == "end"]
        if ends:
            last = max(rank.values()) if len(real) > 1 else 0
            for end_id in ends:
                rank[end_id] = last
            if any(rank[n] == last for n in real if nodes[n].kind != "end"):
                for end_id in ends:
                    rank[end_id] = last + 1
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
        # the gap between two columns is only as wide as the longest edge label crossing it,
        # so a mostly linear plan stays compact instead of paying COL_GAP at every column
        gap_need = [0.0] * max(len(layers) - 1, 0)
        for e in edges:
            if e.back or not e.name:
                continue
            need = _text_w(e.name) + 40
            # the label is drawn on the flow's first segment, so only that gap needs room
            r = all_nodes[e.chain[0]].rank
            if r < len(gap_need):
                gap_need[r] = max(gap_need[r], need)
        col_gap = [int(min(COL_GAP, max(MIN_COL_GAP, need))) for need in gap_need]
        col_x, x = [], MARGIN
        for i, w in enumerate(col_w):
            col_x.append(x)
            x += w + (col_gap[i] if i < len(col_gap) else COL_GAP)
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

        self._route(all_nodes, edges, col_x, col_w, col_gap)

    def _route(self, nodes: dict[str, _Node], edges: list[_Edge], col_x: list[int],
               col_w: list[int], col_gap: list[int]) -> None:
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
            gap_w = col_gap[gap] if gap < len(col_gap) else COL_GAP
            right = left + gap_w
            outs = sorted((k for k in keys if k[0] == "out"), key=lambda k: keys[k])
            ins = sorted((k for k in keys if k[0] == "in"), key=lambda k: keys[k])
            # narrow gaps still split in two lanes (fan-out left, fan-in right), at a smaller step
            half = max(6, gap_w // 2 - 18)
            step = max(4, min(LANE_STEP, half // max(1, max(len(outs), len(ins)))))
            for i, k in enumerate(outs):
                lane_x[(gap, k)] = left + 18 + i * step
            for i, k in enumerate(ins):
                lane_x[(gap, k)] = right - 18 - i * step

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
                h = _wrap(e.name, w) * LINE_H
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
                h = _wrap(e.name, w) * LINE_H
                e.label = (min(src.x, tgt.x) + src.w // 2 + 6, yl + 3, w, h)

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
        proc = ET.SubElement(defs, _q("bpmn", "process"), {"id": pid, "name": ir.title, "isExecutable": "false"})
        tags = {
            "start": "startEvent", "end": "endEvent", "task": "task",
            "gateway": "exclusiveGateway", "subprocess": "subProcess",
        }
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

        def emit_element(parent: ET.Element, n: _Node, incoming, outgoing) -> None:
            attrs = {"id": n.id}
            if n.name:
                attrs["name"] = n.name
            el = ET.SubElement(parent, _q("bpmn", tags[n.kind]), attrs)
            if n.doc:
                ET.SubElement(el, _q("bpmn", "documentation")).text = n.doc
            if n.detail:
                ET.SubElement(el, _q("bpmn", "documentation")).text = n.detail
            for f in incoming[n.id]:
                ET.SubElement(el, _q("bpmn", "incoming")).text = f
            for f in outgoing[n.id]:
                ET.SubElement(el, _q("bpmn", "outgoing")).text = f
            if n.kind == "subprocess":
                plane = planes_by_element[n.id]
                inner_in, inner_out = indexes(plane.nodes, plane.edges)
                for child in plane.nodes.values():
                    emit_element(el, child, inner_in, inner_out)
                emit_flows(el, plane.edges)

        top_in, top_out = indexes(diagram.nodes, diagram.edges)
        for n in diagram.nodes.values():
            emit_element(proc, n, top_in, top_out)
        emit_flows(proc, diagram.edges)

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
                if n.kind == "gateway":
                    lw = GATEWAY_LABEL_W
                    label = ET.SubElement(shape, _q("bpmndi", "BPMNLabel"))
                    _bounds(label, n.x + n.w // 2 - lw // 2, n.y - n.label_h - 6, lw, n.label_h)
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

        top_diagram = ET.SubElement(defs, _q("bpmndi", "BPMNDiagram"), {"id": "BPMNDiagram_1"})
        top_plane = ET.SubElement(top_diagram, _q("bpmndi", "BPMNPlane"),
                                  {"id": "BPMNPlane_1", "bpmnElement": pid})
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
    if node.kind in ("task", "subprocess") and node.tone in TONE_PALETTE:
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
