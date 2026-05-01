from __future__ import annotations
import hashlib
import json
from spec2viz.models.reflection import ReflectionDiagram, EnforcementArtifact, EnforcementFact

class ReflectionCompiler:
    """
    Compiles a ReflectionDiagram into an EnforcementArtifact.
    Processes the core IR into a list of atomic facts for consumption by linters and auditors.
    """

    def compile(self, diagram: ReflectionDiagram) -> EnforcementArtifact:
        facts = []
        
        # 1. Extract facts from edges
        for edge in diagram.data.edges:
            facts.append(
                EnforcementFact(
                    source=edge.from_,
                    target=edge.to,
                    relation=edge.relation,
                    context=edge.metadata.model_dump() if edge.metadata else {}
                )
            )
            
        # 2. Extract facts from nodes (e.g. kind/label facts)
        for node_id, node in diagram.data.nodes.items():
            facts.append(
                EnforcementFact(
                    source=node_id,
                    target=node.kind,
                    relation="is_kind",
                    context=node.metadata.model_dump() if node.metadata else {}
                )
            )
            
        # 3. Generate fingerprint
        facts_data = [f.model_dump() for f in facts]
        fingerprint = hashlib.sha256(
            json.dumps(facts_data, sort_keys=True).encode("utf-8")
        ).hexdigest()
        
        return EnforcementArtifact(
            fingerprint=fingerprint,
            facts=facts
        )
