from __future__ import annotations
from spec2viz.models.activity import ActivityDiagram
from spec2viz.ir import ActivityIR, ActivityStep


class ActivityCompiler:
    def compile(self, diagram: ActivityDiagram) -> ActivityIR:
        steps = [
            ActivityStep(id=sid, label=s.label, kind=s.kind, next=s.next, branches=dict(s.branches))
            for sid, s in diagram.data.steps.items()
        ]
        return ActivityIR(title=diagram.title, start=diagram.data.start, steps=steps, end=diagram.data.end)
