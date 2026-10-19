from __future__ import annotations
from spec2viz.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR
from spec2viz.exceptions import RenderError
from spec2viz.ir import ClassIR
from spec2viz.renderers.class_diagram import render_plantuml_class

_PARTICIPANT_KW = {"actor": "actor", "boundary": "boundary", "database": "database"}
_ARROW = {"sync": "->", "async": "->>", "return": "<--"}
_NODE_KW = {"database": "database"}
_DEFAULT_COMPONENT_KIND_STYLES = {
    "core": {"background": "#D8ECFF", "border": "#4C78A8", "font": "#16324F"},
    "boundary": {"background": "#FCECC9", "border": "#D4A73C", "font": "#5E450B"},
    "database": {"background": "#DCEFD8", "border": "#5A9B5A", "font": "#1F4F1F"},
}


class PlantUMLRenderer:
    def render(self, ir) -> str:
        match ir:
            case ClassIR():
                return render_plantuml_class(ir)
            case SequenceIR():
                return self._sequence(ir)
            case StateIR():
                return self._state(ir)
            case ComponentIR():
                return self._component(ir)
            case ActivityIR():
                return self._activity(ir)
            case DeploymentIR():
                return self._deployment(ir)
            case _:
                raise RenderError(f"PlantUMLRenderer cannot render {type(ir).__name__}")

    def _sequence(self, ir: SequenceIR) -> str:
        lines = ["@startuml"]
        for p in ir.participants:
            lines.append(f"{_PARTICIPANT_KW.get(p.kind, 'participant')} {p.id}")
        lines.append("")
        # Consecutive messages sharing a group render as one group block.
        current = None
        for msg in ir.messages:
            if msg.group != current:
                if current is not None:
                    lines.append("end")
                if msg.group is not None:
                    lines.append(f"group {msg.group}")
                current = msg.group
            arrow = _ARROW.get(msg.kind, "->")
            line = f"{msg.from_} {arrow} {msg.to}: {msg.message}"
            if msg.condition:
                line += f"  [{msg.condition}]"
            lines.append(line)
        if current is not None:
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
        style_kinds = self._resolve_component_kind_styles(ir)
        if style_kinds:
            lines.extend(self._emit_component_kind_styles(style_kinds))
            lines.append("")
        node_map = {node.id: node for node in ir.nodes}
        contained = {
            child_id
            for node in ir.nodes
            for child_id in node.contains
            if child_id in node_map
        }
        for node in ir.nodes:
            if node.id in contained:
                continue
            self._emit_component_node(lines, node, node_map, indent="")
        lines.append("")
        for edge in ir.edges:
            lines.append(f"{edge.from_} --> {edge.to} : {edge.label or edge.relation}")
        lines.append("@enduml")
        return "\n".join(lines)

    def _emit_component_node(
        self,
        lines: list[str],
        node,
        node_map: dict[str, object],
        indent: str,
    ) -> None:
        if node.contains:
            lines.append(
                f'{indent}package "{node.label}" as {node.id} <<{node.kind}>> {{'
            )
            for child_id in node.contains:
                child = node_map.get(child_id)
                if child is None:
                    lines.append(f"{indent}  [{child_id}]")
                    continue
                self._emit_component_node(lines, child, node_map, indent=f"{indent}  ")
            lines.append(f"{indent}}}")
            return

        kw = self._component_keyword(node.kind)
        lines.append(f'{indent}{kw} "{node.label}" as {node.id} <<{node.kind}>>')

    def _component_keyword(self, kind: str) -> str:
        if kind == "boundary":
            return "rectangle"
        if kind == "database":
            return "database"
        return "component"

    def _resolve_component_kind_styles(
        self, ir: ComponentIR
    ) -> dict[str, dict[str, str]]:
        styles = {
            kind: dict(values)
            for kind, values in _DEFAULT_COMPONENT_KIND_STYLES.items()
        }
        for kind, config in ir.style_kinds.items():
            plantuml = config.get("plantuml") if isinstance(config, dict) else None
            if not isinstance(plantuml, dict):
                continue
            current = styles.get(kind, {})
            merged = dict(current)
            for key in ("background", "border", "font"):
                value = plantuml.get(key)
                if isinstance(value, str) and value:
                    merged[key] = value
            if merged:
                styles[kind] = merged
        used_kinds = {node.kind for node in ir.nodes}
        return {kind: styles[kind] for kind in used_kinds if kind in styles}

    def _emit_component_kind_styles(
        self, styles: dict[str, dict[str, str]]
    ) -> list[str]:
        lines: list[str] = []
        for kind, values in sorted(styles.items()):
            background = values.get("background")
            border = values.get("border")
            font = values.get("font")
            for shape in ("component", "rectangle", "database", "package"):
                if background:
                    lines.append(
                        f"skinparam {shape}<<{kind}>> BackgroundColor {background}"
                    )
                if border:
                    lines.append(f"skinparam {shape}<<{kind}>> BorderColor {border}")
                if font:
                    lines.append(f"skinparam {shape}<<{kind}>> FontColor {font}")
        return lines

    def _activity(self, ir: ActivityIR) -> str:
        lines = ["@startuml"]
        step_map = {s.id: s for s in ir.steps}
        # con particiones, PlantUML necesita el primer carril antes de `start`
        first = step_map.get(ir.start)
        lane = [first.partition if first is not None and any(s.partition for s in ir.steps) else None]
        if lane[0]:
            lines.append(f"|{lane[0]}|")
        lines.append("start")
        self._emit_steps(lines, step_map, ir.start, ir.end, set(), lane)
        lines.extend(["stop", "@enduml"])
        return "\n".join(lines)

    def _emit_steps(self, lines, step_map, current, end, visited, lane=None):
        lane = lane if lane is not None else [None]
        while current and current != end and current not in visited:
            visited.add(current)
            step = step_map.get(current)
            if step is None:
                break
            if step.partition and step.partition != lane[0]:
                lines.append(f"|{step.partition}|")
                lane[0] = step.partition
            if step.kind == "merge":
                # el `endif` de PlantUML ya une las ramas: el merge no dibuja nada propio
                current = step.next
                continue
            if step.kind == "decision":
                lines.append(f"if ({step.label}?) then (yes)")
                yes = step.branches.get("yes")
                self._emit_steps(lines, step_map, yes, end, set(visited), lane)
                lines.append("else (no)")
                no = step.branches.get("no")
                self._emit_steps(lines, step_map, no, end, set(visited), lane)
                lines.append("endif")
                return
            else:
                lines.append(f":{step.label};")
                if step.notes:
                    lines.append(f"note right: {step.notes}")
                current = step.next

    def _deployment(self, ir: DeploymentIR) -> str:
        art_map = {a.id: a for a in ir.artifacts}
        node_map = {n.id: n for n in ir.nodes}
        nested = {ref for n in ir.nodes for ref in n.contains if ref in node_map}
        lines = ["@startuml"]

        def emit(node, indent: str) -> None:
            kw = _NODE_KW.get(node.kind, "node")
            lines.append(f'{indent}{kw} "{node.label}" as {node.id} {{')
            for ref in node.contains:
                if ref in art_map:
                    lines.append(f'{indent}  artifact "{art_map[ref].label}" as {ref}')
                elif ref in node_map:
                    emit(node_map[ref], indent + "  ")
            lines.append(f"{indent}}}")

        for node in ir.nodes:
            if node.id not in nested:
                emit(node, "")
        lines.append("")
        for conn in ir.connections:
            arrow = "..>" if conn.kind in ("deploy", "manifest") else "-->"
            line = f"{conn.from_} {arrow} {conn.to}"
            if conn.text:
                line += f" : {conn.text}"
            lines.append(line)
        lines.append("@enduml")
        return "\n".join(lines)
