from __future__ import annotations
from spec2viz.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR
from spec2viz.exceptions import RenderError
from spec2viz.ir import ClassIR
from spec2viz.renderers.class_diagram import render_mermaid_class

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
    ';' ends a statement in mermaid, so it must be escaped as an entity too.
    """
    s = "" if text is None else str(text)
    return (
        s.replace(";", "#59;")
        .replace("&", "#amp;")
        .replace("<", "#lt;")
        .replace(">", "#gt;")
    )


def _kind_classes(style_kinds: dict[str, dict], kind_of: dict[str, str]) -> list[str]:
    """`classDef` y `class` de mermaid desde `style.kinds` del spec (claves neutrales fill,
    stroke), resueltas con la misma precedencia que `resolve_view` (tema claro). Solo los kinds que
    algun elemento usa; sin `style.kinds` neutral no emite nada."""
    from spec2viz.styling import _builtin_default, resolve_style

    neutral = {k: {p: (v[p] if isinstance(v[p], dict) else str(v[p])) for p in ("fill", "stroke") if isinstance(v, dict) and v.get(p)}
               for k, v in style_kinds.items()}
    lines: list[str] = []
    for index, (kind, values) in enumerate((k, v) for k, v in neutral.items() if v):
        members = [eid for eid, ekind in kind_of.items() if ekind == kind]
        if not members:
            continue
        style = resolve_style(None, kind, {kind: values}, None)
        parts = [f"{prop}:{style[prop]['light']}" for prop in ("fill", "stroke") if prop in style]
        parts.append(f"color:{_builtin_default()['ink']['light']}")
        name = f"kind{index}"
        lines.append(f"    classDef {name} {','.join(parts)}")
        lines.append(f"    class {','.join(members)} {name}")
    return lines


# flowcharts con el layout ELK y aristas ortogonales (curva linear sobre los codos que calcula ELK):
# con nodos anidados o un nodo central, dagre cruza y curva las flechas largas y pisa los rotulos
FLOWCHART_CONFIG = "---\nconfig:\n  layout: elk\n  flowchart:\n    curve: linear\n---"


def _flowchart(direction: str = "TD") -> list[str]:
    """Cabecera de un flowchart: frontmatter de config (ELK, curva linear) y `flowchart <dir>`."""
    return [*FLOWCHART_CONFIG.split("\n"), f"flowchart {direction}"]


class MermaidRenderer:
    def render(self, ir) -> str:
        match ir:
            case ClassIR():      return render_mermaid_class(ir)
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
        # Consecutive messages sharing a group render as one labeled block.
        current = None
        for msg in ir.messages:
            if msg.group != current:
                if current is not None:
                    lines.append("    end")
                if msg.group is not None:
                    lines.append("    rect rgba(127, 127, 127, 0.1)")
                    lines.append(f"    Note over {msg.from_},{msg.to}: {_esc_message(msg.group)}")
                current = msg.group
            arrow = _SEQ_ARROW.get(msg.kind, "->>")
            text = msg.message if not msg.condition else f"{msg.message} [{msg.condition}]"
            lines.append(f"    {msg.from_}{arrow}{msg.to}: {_esc_message(text)}")
        if current is not None:
            lines.append("    end")
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
        lines = _flowchart("TD")
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
        lines.extend(_kind_classes(ir.style_kinds, {n.id: n.kind for n in ir.nodes}))
        return "\n".join(lines)

    def _activity(self, ir: ActivityIR) -> str:
        lines = [*_flowchart("TD"), "    __start([Start])"]

        def node_lines(step, indent: str) -> list[str]:
            # decision y merge son rombos; una nota es un nodo aparte unido por una linea punteada
            if step.kind in ("decision", "merge"):
                # mermaid no acepta un rombo con rotulo vacio (el merge UML no lleva rotulo)
                out = [f"{indent}{step.id}{{\"{_esc_label(step.label) or ' '}\"}}"]
            else:
                out = [f"{indent}{step.id}[\"{_esc_label(step.label)}\"]"]
            if step.notes:
                out.append(f"{indent}{step.id}__note[\"{_esc_label(step.notes)}\"]:::note")
            return out

        # particiones (swimlanes): un subgraph por particion, en orden de aparicion
        lanes: dict[str, list] = {}
        for step in ir.steps:
            if step.partition:
                lanes.setdefault(step.partition, []).append(step)
        for step in ir.steps:
            if not step.partition:
                lines.extend(node_lines(step, "    "))
        for index, (lane, steps) in enumerate(lanes.items()):
            lines.append(f'    subgraph __lane{index} ["{_esc_label(lane)}"]')
            for step in steps:
                lines.extend(node_lines(step, "        "))
            lines.append("    end")
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
        for step in ir.steps:
            if step.notes:
                lines.append(f"    {step.id} -.- {step.id}__note")
        if any(step.notes for step in ir.steps):
            lines.append("    classDef note fill:#fff8c5,stroke:#9a6700,color:#1f2328")
        lines.extend(_kind_classes(ir.style_kinds, {st.id: st.kind for st in ir.steps}))
        return "\n".join(lines)

    def _deployment(self, ir: DeploymentIR) -> str:
        art_map = {a.id: a for a in ir.artifacts}
        node_map = {n.id: n for n in ir.nodes}
        nested = {ref for n in ir.nodes for ref in n.contains if ref in node_map}
        lines = _flowchart("TD")

        def emit(node, indent: str) -> None:
            # un nodo es un subgraph; dentro, sus artefactos y sus nodos hijos (anidados)
            lines.append(f'{indent}subgraph {node.id} ["{_esc_label(node.label)}"]')
            for ref in node.contains:
                if ref in art_map:
                    lines.append(f'{indent}    {ref}["{_esc_label(art_map[ref].label)}"]')
                elif ref in node_map:
                    emit(node_map[ref], indent + "    ")
            lines.append(f"{indent}end")

        for node in ir.nodes:
            if node.id not in nested:
                emit(node, "    ")
        for conn in ir.connections:
            label = conn.text
            arrow = "-.->" if conn.kind in ("deploy", "manifest") else "-->"
            if label:
                lines.append(f'    {conn.from_} {arrow}|"{_esc_label(label)}"| {conn.to}')
            else:
                lines.append(f"    {conn.from_} {arrow} {conn.to}")
        lines.extend(_kind_classes(ir.style_kinds, {**{a.id: a.kind for a in ir.artifacts}, **{n.id: n.kind for n in ir.nodes}}))
        return "\n".join(lines)
