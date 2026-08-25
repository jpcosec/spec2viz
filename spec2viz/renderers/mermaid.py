from __future__ import annotations
from spec2viz.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR
from spec2viz.exceptions import RenderError

# Mermaid sequence arrows. Return must be "-->>" (dashed). "<<--" is NOT
# valid mermaid and breaks the parser in the browser.
_SEQ_ARROW = {"sync": "->>", "async": "-->>", "return": "-->>"}
_PARTICIPANT_KW = {"actor": "actor", "database": "participant", "boundary": "participant"}


def _esc_label(text: object) -> str:
    """Escape text for a quoted mermaid label (node, subgraph, decision, edge).

    Mermaid treats '(', '{', '[' and bare '"' as syntax. Wrapping the label in
    double quotes handles brackets/parens; the inner '"' and angle brackets are
    replaced with mermaid HTML entities so they render literally instead of
    breaking the parser in the browser.
    """
    s = "" if text is None else str(text)
    return (
        s.replace("&", "#amp;")
        .replace('"', "#quot;")
        .replace("<", "#lt;")
        .replace(">", "#gt;")
    )


def _esc_message(text: object) -> str:
    """Escape text for an unquoted sequence message (after the ':').

    Sequence messages are not quoted, so only the HTML-significant angle
    brackets and ampersand must be neutralised; parentheses are safe here.
    """
    s = "" if text is None else str(text)
    return s.replace("&", "#amp;").replace("<", "#lt;").replace(">", "#gt;")


class MermaidRenderer:
    def render(self, ir) -> str:
        match ir:
            case SequenceIR():   return self._sequence(ir)
            case StateIR():      return self._state(ir)
            case ComponentIR():  return self._component(ir)
            case ActivityIR():   return self._activity(ir)
            case DeploymentIR(): return self._deployment(ir)
            case _: raise RenderError(f"MermaidRenderer cannot render {type(ir).__name__}")

    def _sequence(self, ir: SequenceIR) -> str:
        lines = ["sequenceDiagram"]
        for p in ir.participants:
            kw = _PARTICIPANT_KW.get(p.kind, "participant")
            lines.append(f"    {kw} {p.id}")
        for msg in ir.messages:
            arrow = _SEQ_ARROW.get(msg.kind, "->>")
            lines.append(f"    {msg.from_}{arrow}{msg.to}: {_esc_message(msg.message)}")
        return "\n".join(lines)

    def _state(self, ir: StateIR) -> str:
        lines = ["stateDiagram-v2"]
        
        state_map = {s.id: s for s in ir.states}
        children_ids = {child for s in ir.states if s.contains for child in s.contains}
        root_states = [s for s in ir.states if s.id not in children_ids]
        
        def render_state(s, indent="    "):
            lines.append(f'{indent}state "{_esc_label(s.label)}" as {s.id}' + (' {' if s.contains else ''))
            if s.contains:
                for child_id in s.contains:
                    if child_id in state_map:
                        render_state(state_map[child_id], indent + "    ")
                lines.append(f'{indent}}}')
                
        for s in root_states:
            render_state(s)
        
        lines.append(f"    [*] --> {ir.initial}")
        for t in ir.transitions:
            label = t.on or ""
            if t.guard:
                label += f" [{t.guard}]"
            lines.append(f"    {t.from_} --> {t.to} : {_esc_message(label)}")
        return "\n".join(lines)

    def _component(self, ir: ComponentIR) -> str:
        lines = ["graph TD"]
        child_ids = {child for node in ir.nodes for child in node.contains}

        def render_node(node_id, indent="    "):
            node = next((n for n in ir.nodes if n.id == node_id), None)
            if not node:
                lines.append(f"{indent}{node_id}")
                return
            label = _esc_label(node.label or node.id)
            if not node.contains:
                lines.append(f"{indent}{node.id}[\"{label}\"]")
            else:
                lines.append(f"{indent}subgraph {node.id} [\"{label}\"]")
                for child_id in node.contains:
                    render_node(child_id, indent + "    ")
                lines.append(f"{indent}end")

        for node in ir.nodes:
            if node.id not in child_ids:
                render_node(node.id)

        for edge in ir.edges:
            label = edge.label or edge.relation
            if label:
                lines.append(f'    {edge.from_} -->|"{_esc_label(label)}"| {edge.to}')
            else:
                lines.append(f"    {edge.from_} --> {edge.to}")
        return "\n".join(lines)

    def _activity(self, ir: ActivityIR) -> str:
        lines = ["flowchart TD", "    __start([Start])"]
        step_map = {s.id: s for s in ir.steps}
        for step in ir.steps:
            if step.kind == "decision":
                lines.append(f"    {step.id}{{\"{_esc_label(step.label)}\"}}")
            else:
                lines.append(f"    {step.id}[\"{_esc_label(step.label)}\"]")
        lines.append(f"    __end([End])")
        lines.append(f"    __start --> {ir.start}")
        for step in ir.steps:
            if step.kind == "decision":
                for branch, target in step.branches.items():
                    dest = "__end" if target == ir.end else target
                    lines.append(f'    {step.id} -->|"{_esc_label(branch)}"| {dest}')
            elif step.next:
                dest = "__end" if step.next == ir.end else step.next
                lines.append(f"    {step.id} --> {dest}")
        return "\n".join(lines)

    def _deployment(self, ir: DeploymentIR) -> str:
        art_map = {a.id: a for a in ir.artifacts}
        lines = ["graph TD"]
        for node in ir.nodes:
            lines.append(f'    subgraph {node.id} ["{_esc_label(node.label)}"]')
            for aid in node.contains:
                if aid in art_map:
                    lines.append(f'        {aid}["{_esc_label(art_map[aid].label)}"]')
            lines.append("    end")
        for conn in ir.connections:
            label = conn.protocol or ""
            if label:
                lines.append(f'    {conn.from_} -->|"{_esc_label(label)}"| {conn.to}')
            else:
                lines.append(f"    {conn.from_} --> {conn.to}")
        return "\n".join(lines)
