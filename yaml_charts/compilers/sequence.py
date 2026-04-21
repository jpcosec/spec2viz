from __future__ import annotations
from yaml_charts.models.sequence import SequenceDiagram
from yaml_charts.ir import SequenceIR, Participant, Message


class SequenceCompiler:
    def compile(self, diagram: SequenceDiagram) -> SequenceIR:
        participants = [Participant(id=p.id, kind=p.kind) for p in diagram.data.participants]
        messages = [
            Message(index=i, from_=m.from_, to=m.to, message=m.message,
                    kind=m.kind, condition=m.condition, group=m.group)
            for i, m in enumerate(diagram.data.messages)
        ]
        return SequenceIR(title=diagram.title, participants=participants, messages=messages)
