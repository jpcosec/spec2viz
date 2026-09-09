from spec2viz.models.class_diagram import ClassDiagram
from spec2viz.ir import (
    ClassIR, ClassNodeIR, ClassAttributeIR, ClassMethodIR, ClassParameterIR, ClassRelationIR,
)


class ClassCompiler:
    def compile(self, diagram: ClassDiagram) -> ClassIR:
        nodes = []
        for ident, definition in diagram.data.classes.items():
            nodes.append(ClassNodeIR(
                id=ident, label=definition.label or ident, kind=definition.kind,
                attributes=[ClassAttributeIR(**a.model_dump()) for a in definition.attributes],
                methods=[ClassMethodIR(
                    name=m.name, returns=m.returns, visibility=m.visibility,
                    abstract=m.abstract, static=m.static,
                    parameters=[ClassParameterIR(**p.model_dump()) for p in m.parameters],
                ) for m in definition.methods],
            ))
        return ClassIR(
            title=diagram.title, direction=diagram.data.direction, classes=nodes,
            relations=[ClassRelationIR(**r.model_dump()) for r in diagram.data.relations],
        )
