from __future__ import annotations
from spec2viz.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR
from spec2viz.exceptions import RenderError

class D2Renderer:
    def render(self, ir) -> str:
        match ir:
            case SequenceIR():   return self._sequence(ir)
            case StateIR():      return self._state(ir)
            case ComponentIR():  return self._component(ir)
            case ActivityIR():   return self._activity(ir)
            case DeploymentIR(): return self._deployment(ir)
            case _: raise RenderError(f"D2Renderer cannot render {type(ir).__name__}")

    def _sequence(self, ir: SequenceIR) -> str:
        lines = ["direction: right"]
        for p in ir.participants:
            lines.append(f"{p.id}: {p.id}")
        for msg in ir.messages:
            lines.append(f"{msg.from_} -> {msg.to}: {msg.message}")
        return "\n".join(lines)

    def _state(self, ir: StateIR) -> str:
        lines = ["direction: right"]
        for t in ir.transitions:
            label = t.on
            if t.guard:
                label += f" [{t.guard}]"
            lines.append(f"{t.from_} -> {t.to}: {label}")
        return "\n".join(lines)

    def _component(self, ir: ComponentIR) -> str:
        lines = ["direction: right"]
        for node in ir.nodes:
            label = node.label or node.id
            lines.append(f"{node.id}: \"{label}\"")
            for child in node.contains:
                lines.append(f"{node.id}.{child}: \"{child}\"")
        for edge in ir.edges:
            label = edge.label or edge.relation
            lines.append(f"{edge.from_} -> {edge.to}: \"{label}\"")
        return "\n".join(lines)

    def _activity(self, ir: ActivityIR) -> str:
        lines = ["direction: down", "__start: Start"]
        # con particiones, cada carril es un contenedor y los pasos se nombran `carril.paso`
        lanes = list(dict.fromkeys(s.partition for s in ir.steps if s.partition))
        lane_key = {lane: f"__lane{i}" for i, lane in enumerate(lanes)}
        path = {s.id: f"{lane_key[s.partition]}.{s.id}" if s.partition else s.id for s in ir.steps}
        for lane in lanes:
            lines.append(f'{lane_key[lane]}: "{lane}"')
        for step in ir.steps:
            ref = path[step.id]
            if step.kind in ("decision", "merge"):
                lines.append(f"{ref}: \"{step.label}\"")
                lines.append(f"{ref}.shape: diamond")
            else:
                lines.append(f"{ref}: \"{step.label}\"")
            if step.notes:
                lines.append(f'{ref}__note: "{step.notes}"')
                lines.append(f"{ref}__note.shape: page")
        lines.append(f"__end: End")
        lines.append(f"__start -> {path.get(ir.start, ir.start)}")
        for step in ir.steps:
            ref = path[step.id]
            if step.kind == "decision":
                for branch, target in step.branches.items():
                    dest = "__end" if target == ir.end else path.get(target, target)
                    lines.append(f"{ref} -> {dest}: \"{branch}\"")
            elif step.next:
                dest = "__end" if step.next == ir.end else path.get(step.next, step.next)
                lines.append(f"{ref} -> {dest}")
            if step.notes:
                lines.append(f"{ref} -- {ref}__note: {{style.stroke-dash: 3}}")
        return "\n".join(lines)

    def _deployment(self, ir: DeploymentIR) -> str:
        lines = ["direction: right"]
        art_map = {a.id: a for a in ir.artifacts}
        node_map = {n.id: n for n in ir.nodes}
        nested = {ref for n in ir.nodes for ref in n.contains if ref in node_map}
        # cada elemento se nombra por su ruta de contenedores (`vpc.subnet.cluster`): las aristas
        # tienen que usar esa ruta, si no d2 crea un elemento suelto con el mismo id
        path: dict[str, str] = {}

        def emit(node, prefix: str) -> None:
            ref_path = f"{prefix}{node.id}"
            path[node.id] = ref_path
            lines.append(f"{ref_path}: \"{node.label}\"")
            for ref in node.contains:
                if ref in art_map:
                    path.setdefault(ref, f"{ref_path}.{ref}")
                    lines.append(f"{ref_path}.{ref}: \"{art_map[ref].label}\"")
                elif ref in node_map:
                    emit(node_map[ref], f"{ref_path}.")

        for node in ir.nodes:
            if node.id not in nested:
                emit(node, "")
        for conn in ir.connections:
            src, dst = path.get(conn.from_, conn.from_), path.get(conn.to, conn.to)
            dashed = " {style.stroke-dash: 3}" if conn.kind in ("deploy", "manifest") else ""
            label = conn.text
            if label:
                lines.append(f"{src} -> {dst}: \"{label}\"{dashed}")
            elif dashed:
                lines.append(f"{src} -> {dst}:{dashed}")
            else:
                lines.append(f"{src} -> {dst}")
        return "\n".join(lines)
