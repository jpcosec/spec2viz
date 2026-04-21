from __future__ import annotations
from yaml_charts.models.state import StateDiagram
from yaml_charts.ir import StateIR, StateNode, Transition


class StateCompiler:
    def compile(self, diagram: StateDiagram) -> StateIR:
        states = [StateNode(id=s.id, label=s.label) for s in diagram.data.states]
        transitions = [
            Transition(from_=t.from_, to=t.to, on=t.on, guard=t.guard, action=t.action)
            for t in diagram.data.transitions
        ]
        return StateIR(title=diagram.title, entity=diagram.data.entity,
                       initial=diagram.data.initial, states=states, transitions=transitions)
