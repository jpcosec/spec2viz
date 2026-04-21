from __future__ import annotations
from yaml_charts.ir import SequenceIR
from yaml_charts.exceptions import RenderError


class MermaidRenderer:
    def render(self, ir) -> str:
        if not isinstance(ir, SequenceIR):
            raise RenderError(f"MermaidRenderer only supports SequenceIR, got {type(ir).__name__}")
        lines = ["sequenceDiagram"]
        for msg in ir.messages:
            lines.append(f"    {msg.from_}->>{msg.to}: {msg.message}")
        return "\n".join(lines)
