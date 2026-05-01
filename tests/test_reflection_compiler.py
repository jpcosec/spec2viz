from spec2viz.loader import load
from spec2viz.compilers import compile_ir
from spec2viz.models.reflection import ReflectionDiagram, EnforcementArtifact

def test_compile_enforcement_artifact_from_fixture():
    spec_path = "examples/reflection/canonical.yml"
    diagram = load(spec_path)
    
    assert isinstance(diagram, ReflectionDiagram)
    
    artifact = compile_ir(diagram)
    assert isinstance(artifact, EnforcementArtifact)
    assert len(artifact.facts) > 0
    assert artifact.fingerprint is not None
    
    # Verify a fact
    uses_fact = next(f for f in artifact.facts if f.relation == "uses")
    assert uses_fact.source == "api"
    assert uses_fact.target == "core"
