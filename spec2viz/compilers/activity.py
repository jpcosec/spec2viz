from __future__ import annotations
from spec2viz.models.activity import ActivityDiagram
from spec2viz.ir import ActivityIR, ActivityStep


class ActivityCompiler:
    def compile(self, diagram: ActivityDiagram) -> ActivityIR:
        steps = [
            ActivityStep(id=sid, label=s.label, kind=s.kind, next=s.next, branches=dict(s.branches), partition=s.partition, notes=s.notes)
            for sid, s in diagram.data.steps.items()
        ]
        style_kinds = dict(diagram.style.kinds) if diagram.style else {}
        return ActivityIR(title=diagram.title, start=diagram.data.start, steps=steps, end=diagram.data.end, style_kinds=style_kinds)
