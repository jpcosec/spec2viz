from __future__ import annotations
from spec2viz.ir import MatrixIR
from spec2viz.exceptions import RenderError

_KIND_COLORS = {
    "core": "#F59E0B", "boundary": "#60A5FA", "decision_engine": "#EC4899",
    "actor": "#A78BFA", "database": "#10B981",
}
_DEFAULT_COLOR = "#94A3B8"


class VegaRenderer:
    def render(self, ir) -> dict:
        if not isinstance(ir, MatrixIR):
            raise RenderError(f"VegaRenderer expects MatrixIR, got {type(ir).__name__}")
        kinds = list({s.kind for s in ir.spans})
        return {
            "$schema": "https://vega.github.io/schema/vega/v5.json",
            "description": ir.title,
            "width": 220 + len(ir.stages) * 140 + 20,
            "height": max(120, 70 + len(ir.rows) * 34 + 20),
            "padding": 5,
            "signals": [
                {"name": "left",       "value": 220},
                {"name": "top",        "value": 70},
                {"name": "cellWidth",  "value": 140},
                {"name": "rowHeight",  "value": 34},
                {"name": "barPadding", "value": 6},
            ],
            "data": [
                {"name": "stages",         "values": [{"id": s.id, "index": s.index, "label": s.label, "view": s.view} for s in ir.stages]},
                {"name": "views", "source": "stages", "transform": [
                    {"type": "aggregate", "groupby": ["view"], "fields": ["index", "index"], "ops": ["min", "max"], "as": ["minIdx", "maxIdx"]}
                ]},
                {"name": "viewBoundaries", "source": "views", "transform": [
                    {"type": "formula", "expr": "[datum.minIdx, datum.maxIdx + 1]", "as": "indices"},
                    {"type": "flatten", "fields": ["indices"]},
                    {"type": "aggregate", "groupby": ["indices"]}
                ]},
                {"name": "stageBoundaries","values": [{"index": i} for i in range(len(ir.stages) + 1)]},
                {"name": "rows",           "values": [{"id": r.id, "label": r.label, "row": r.row, "depth": r.depth} for r in ir.rows]},
                {"name": "spans",          "values": [{"component": s.component, "row": s.row, "start": s.start, "end": s.end, "kind": s.kind, "depth": ir.rows[s.row].depth} for s in ir.spans]},
            ],
            "scales": [{"name": "kindColor", "type": "ordinal", "domain": kinds,
                        "range": [_KIND_COLORS.get(k, _DEFAULT_COLOR) for k in kinds]}],
            "marks": self._marks(ir),
        }

    def _marks(self, ir: MatrixIR) -> list[dict]:
        n = len(ir.rows)
        return [
            # View Labels
            {"type": "text", "from": {"data": "views"}, 
             "encode": {"enter": {
                "x": {"signal": "left + (datum.minIdx + datum.maxIdx + 1) * cellWidth / 2"},
                "y": {"value": 15}, "text": {"field": "view"},
                "align": {"value": "center"}, "fontWeight": {"value": "bold"}, "fontSize": {"value": 15}, "fill": {"value": "#475569"}
            }}},
            # Stage Labels
            {"type": "text", "from": {"data": "stages"}, "encode": {"enter": {
                "x": {"signal": "left + datum.index * cellWidth + cellWidth / 2"},
                "y": {"value": 40}, "text": {"field": "label"},
                "align": {"value": "center"}, "fontWeight": {"value": "bold"}, "fontSize": {"value": 13},
                "fill": {"value": "#475569"}
            }}},
            # Stage boundaries (dotted)
            {"type": "rule", "from": {"data": "stageBoundaries"}, "encode": {"enter": {
                "x": {"signal": "left + datum.index * cellWidth"},
                "y": {"signal": "top - 20"}, "y2": {"signal": f"top + {n} * rowHeight + 10"},
                "stroke": {"value": "#CBD5E1"}, "strokeDash": {"value": [4, 4]},
            }}},
            # View boundaries (solid, thick)
            {"type": "rule", "from": {"data": "viewBoundaries"}, "encode": {"enter": {
                "x": {"signal": "left + datum.indices * cellWidth"},
                "y": {"signal": "top - 40"}, "y2": {"signal": f"top + {n} * rowHeight + 20"},
                "stroke": {"value": "#475569"}, "strokeWidth": {"value": 2.5},
                "strokeOpacity": {"value": 0.6}
            }}},
            # Row Backgrounds (Zebra + Depth cues)
            {"type": "rect", "from": {"data": "rows"}, "encode": {"enter": {
                "x": {"value": 0}, "x2": {"signal": "width"},
                "y": {"signal": "top + datum.row * rowHeight"}, "height": {"signal": "rowHeight"},
                "fill": {"signal": "datum.depth === 0 ? (datum.row % 2 === 0 ? '#475569' : '#94A3B8') : (datum.row % 2 === 0 ? '#CBD5E1' : '#E2E8F0')"},
                "fillOpacity": {"value": 0.15}
            }}},
            # Hierarchy Indentation Cue (Vertical line on the left)
            {"type": "rule", "from": {"data": "rows"}, "encode": {"enter": {
                "x": {"signal": "12 + datum.depth * 18"}, "x2": {"signal": "12 + datum.depth * 18"},
                "y": {"signal": "top + datum.row * rowHeight + 2"}, 
                "y2": {"signal": "top + datum.row * rowHeight + rowHeight - 2"},
                "stroke": {"signal": "datum.depth === 0 ? '#475569' : '#94A3B8'"}, 
                "strokeWidth": {"signal": "datum.depth === 0 ? 3 : 1.5"}
            }}},
            # Component Labels
            {"type": "text", "from": {"data": "rows"}, "encode": {"enter": {
                "x": {"signal": "20 + datum.depth * 18"},
                "y": {"signal": "top + datum.row * rowHeight + rowHeight / 2"},
                "text": {"field": "label"}, "align": {"value": "left"},
                "baseline": {"value": "middle"}, "fontSize": {"value": 13}, "fill": {"value": "#111827"},
            }}},
            {"type": "rect", "from": {"data": "spans"}, "encode": {"enter": {
                "x": {"signal": "left + datum.start * cellWidth + 4"},
                "x2": {"signal": "left + datum.end * cellWidth - 4"},
                "y": {"signal": "top + datum.row * rowHeight + barPadding"},
                "height": {"signal": "rowHeight - barPadding * 2"},
                "cornerRadius": {"value": 7}, 
                "fill": {"scale": "kindColor", "field": "kind"},
                "fillOpacity": {"signal": "max(0.3, 1 - (datum.depth * 0.25))"},
                "stroke": {"scale": "kindColor", "field": "kind"}, 
                "strokeOpacity": {"value": 0.7},
                "strokeWidth": {"value": 1.5}
            }}},
        ]
