from __future__ import annotations
from spec2viz.models.activity import ActivityDiagram
from spec2viz.ir import ActivityGroup, ActivityIR, ActivityStep


class ActivityCompiler:
    def compile(self, diagram: ActivityDiagram) -> ActivityIR:
        steps = [
            ActivityStep(
                id=sid, label=s.label, kind=s.kind, next=s.next, branches=dict(s.branches),
                partition=s.partition, notes=s.notes, tone=s.tone, detail=s.detail, group=s.group,
            )
            for sid, s in diagram.data.steps.items()
        ]
        groups = {
            gid: ActivityGroup(id=gid, label=g.label, tone=g.tone, detail=g.detail)
            for gid, g in diagram.data.groups.items()
        }
        style_kinds = dict(diagram.style.kinds) if diagram.style else {}
        return ActivityIR(
            title=diagram.title, start=diagram.data.start, steps=steps,
            end=diagram.data.end, style_kinds=style_kinds, groups=groups,
        )
