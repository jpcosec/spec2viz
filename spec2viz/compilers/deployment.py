from __future__ import annotations
from spec2viz.models.deployment import DeploymentDiagram
from spec2viz.ir import DeploymentIR, DeploymentNode, DeploymentArtifact, DeploymentConnection


class DeploymentCompiler:
    def compile(self, diagram: DeploymentDiagram) -> DeploymentIR:
        nodes = [
            DeploymentNode(id=nid, label=n.label or nid, kind=n.kind, contains=list(n.contains))
            for nid, n in diagram.data.nodes.items()
        ]
        artifacts = [
            DeploymentArtifact(id=aid, label=a.label or aid, kind=a.kind)
            for aid, a in diagram.data.artifacts.items()
        ]
        connections = [
            DeploymentConnection(from_=c.from_, to=c.to, protocol=c.protocol)
            for c in diagram.data.connections
        ]
        return DeploymentIR(title=diagram.title, nodes=nodes, artifacts=artifacts, connections=connections)
