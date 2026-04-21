from __future__ import annotations
from yaml_charts.models.activity import ActivityDiagram
from yaml_charts.ir import ActivityIR, ActivityStep


class ActivityCompiler:
    def compile(self, diagram: ActivityDiagram) -> ActivityIR:
        steps = [
            ActivityStep(id=sid, label=s.label, kind=s.kind, next=s.next, branches=dict(s.branches))
            for sid, s in diagram.data.steps.items()
        ]
        return ActivityIR(title=diagram.title, start=diagram.data.start, steps=steps, end=diagram.data.end)
