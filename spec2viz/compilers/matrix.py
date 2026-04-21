from __future__ import annotations
from spec2viz.models.matrix import MatrixDiagram, MatrixComponentModel
from spec2viz.ir import MatrixIR, Stage, Row, Span


class MatrixCompiler:
    def compile(self, diagram: MatrixDiagram) -> MatrixIR:
        stages = self._build_stages(diagram)
        stage_index = {s.id: s.index for s in stages}
        rows: list[Row] = []
        spans: list[Span] = []
        self._walk(diagram.data.components, 0, rows, spans, stage_index, diagram)
        return MatrixIR(title=diagram.title, stages=stages, rows=rows, spans=spans)

    def _build_stages(self, diagram: MatrixDiagram) -> list[Stage]:
        stages, idx = [], 0
        for view in diagram.data.views:
            for s in view.stages:
                stages.append(Stage(id=s.id, index=idx, label=s.label, view=view.label))
                idx += 1
        return stages

    def _walk(self, components, depth, rows, spans, stage_index, diagram):
        for comp in components:
            row_idx = len(rows)
            rows.append(Row(id=comp.name, label=comp.label or comp.name, row=row_idx, depth=depth))
            for view in diagram.data.views:
                indices = [stage_index[sid] for sid in comp.stages.get(view.id, []) if sid in stage_index]
                for start, end in _contiguous(indices):
                    spans.append(Span(component=comp.name, row=row_idx, start=start, end=end, kind=comp.kind))
            self._walk(comp.children, depth + 1, rows, spans, stage_index, diagram)


def _contiguous(indices: list[int]) -> list[tuple[int, int]]:
    if not indices:
        return []
    s = sorted(indices)
    result, start, prev = [], s[0], s[0]
    for i in s[1:]:
        if i != prev + 1:
            result.append((start, prev + 1))
            start = i
        prev = i
    result.append((start, prev + 1))
    return result
