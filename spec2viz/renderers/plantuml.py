from __future__ import annotations
from spec2viz.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR
from spec2viz.exceptions import RenderError

_PARTICIPANT_KW = {"actor": "actor", "boundary": "boundary", "database": "database"}
_ARROW = {"sync": "->", "async": "->>", "return": "<--"}
_NODE_KW = {"database": "database"}


class PlantUMLRenderer:
    def render(self, ir) -> str:
        match ir:
            case SequenceIR():   return self._sequence(ir)
            case StateIR():      return self._state(ir)
            case ComponentIR():  return self._component(ir)
            case ActivityIR():   return self._activity(ir)
            case DeploymentIR(): return self._deployment(ir)
            case _: raise RenderError(f"PlantUMLRenderer cannot render {type(ir).__name__}")

    def _sequence(self, ir: SequenceIR) -> str:
        lines = ["@startuml"]
        for p in ir.participants:
            lines.append(f"{_PARTICIPANT_KW.get(p.kind, 'participant')} {p.id}")
        lines.append("")
        for msg in ir.messages:
            arrow = _ARROW.get(msg.kind, "->")
            line = f"{msg.from_} {arrow} {msg.to}: {msg.message}"
            if msg.condition:
                line += f"  [{msg.condition}]"
            if msg.group:
                lines.append(f"group {msg.group}")
            lines.append(line)
            if msg.group:
                lines.append("end")
        lines.append("@enduml")
        return "\n".join(lines)

    def _state(self, ir: StateIR) -> str:
        lines = ["@startuml", f"[*] --> {ir.initial}", ""]
        for t in ir.transitions:
            line = f"{t.from_} --> {t.to} : {t.on}"
            if t.guard:
                line += f" [{t.guard}]"
            if t.action:
                line += f" / {t.action}"
            lines.append(line)
        lines.append("@enduml")
        return "\n".join(lines)

    def _component(self, ir: ComponentIR) -> str:
        lines = ["@startuml"]
        for node in ir.nodes:
            if node.contains:
                lines.append(f'package "{node.label}" {{')
                for child in node.contains:
                    lines.append(f"  [{child}]")
                lines.append("}")
            else:
                kw = _PARTICIPANT_KW.get(node.kind, "component")
                lines.append(f"{kw} [{node.label}] as {node.id}")
        lines.append("")
        for edge in ir.edges:
            lines.append(f"{edge.from_} --> {edge.to} : {edge.label or edge.relation}")
        lines.append("@enduml")
        return "\n".join(lines)

    def _activity(self, ir: ActivityIR) -> str:
        lines = ["@startuml", "start"]
        step_map = {s.id: s for s in ir.steps}
        self._emit_steps(lines, step_map, ir.start, ir.end, set())
        lines.extend(["stop", "@enduml"])
        return "\n".join(lines)

    def _emit_steps(self, lines, step_map, current, end, visited):
        while current and current != end and current not in visited:
            visited.add(current)
            step = step_map.get(current)
            if step is None:
                break
            if step.kind == "decision":
                lines.append(f"if ({step.label}?) then (yes)")
                yes = step.branches.get("yes")
                self._emit_steps(lines, step_map, yes, end, set(visited))
                lines.append("else (no)")
                no = step.branches.get("no")
                self._emit_steps(lines, step_map, no, end, set(visited))
                lines.append("endif")
                return
            else:
                lines.append(f":{step.label};")
                current = step.next

    def _deployment(self, ir: DeploymentIR) -> str:
        art_map = {a.id: a for a in ir.artifacts}
        lines = ["@startuml"]
        for node in ir.nodes:
            kw = _NODE_KW.get(node.kind, "node")
            lines.append(f'{kw} "{node.label}" as {node.id} {{')
            for aid in node.contains:
                if aid in art_map:
                    lines.append(f'  artifact "{art_map[aid].label}" as {aid}')
            lines.append("}")
        lines.append("")
        for conn in ir.connections:
            line = f"{conn.from_} --> {conn.to}"
            if conn.protocol:
                line += f" : {conn.protocol}"
            lines.append(line)
        lines.append("@enduml")
        return "\n".join(lines)
