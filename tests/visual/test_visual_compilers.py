"""spec2viz's compiler tests ported to specIR (SV-B02 to SV-B10, SV-A14): `tests/test_compilers.py`
(17), the `test_compile_*` of `tests/test_api.py` (6), `tests/test_reflection_compiler.py` (1), and
the compile-only cases of `tests/test_class_diagram.py`, `tests/test_class_packages.py`,
`tests/test_activity_lanes.py` and `tests/test_exceptions.py`. Specs load and validate with
sldb's `load_spec`/`validate_spec` (D3); fixtures are the spec2viz ones copied to fixtures/spec2viz."""

from pathlib import Path

import pytest
from sldb.api.notations import load_spec as load, validate_spec as validate

from specir.visual import BaseDiagram, ClassIR, EnforcementArtifact, ReflectionDiagram, compile_ir
from specir.visual.compilers.matrix import _contiguous
from specir.visual.exceptions import CompileError, Spec2VizError
from specir.visual.ir import ActivityIR, ComponentIR, DeploymentIR, MatrixIR, SequenceIR, StateIR

ROOT = Path(__file__).parent / "fixtures" / "spec2viz"
FIXTURES = ROOT / "tests" / "fixtures"


# ── Dispatch (tests/test_compilers.py) ───────────────────────────────────────

def test_dispatch_sequence():   assert isinstance(compile_ir(load(FIXTURES / "sequence.create-quotation.yml")), SequenceIR)
def test_dispatch_state():      assert isinstance(compile_ir(load(FIXTURES / "state.quotation.yml")), StateIR)
def test_dispatch_component():  assert isinstance(compile_ir(load(FIXTURES / "component.quotation.yml")), ComponentIR)
def test_dispatch_activity():   assert isinstance(compile_ir(load(FIXTURES / "activity.validation.yml")), ActivityIR)
def test_dispatch_deployment():  assert isinstance(compile_ir(load(FIXTURES / "deployment.runtime.yml")), DeploymentIR)
def test_dispatch_matrix():     assert isinstance(compile_ir(load(FIXTURES / "matrix.quotation-view.yml")), MatrixIR)


def test_sequence_participants():
    ir = compile_ir(load(FIXTURES / "sequence.create-quotation.yml"))
    assert len(ir.participants) == 3
    assert ir.participants[0].id == "User"
    assert ir.participants[0].kind == "actor"


def test_sequence_messages():
    ir = compile_ir(load(FIXTURES / "sequence.create-quotation.yml"))
    assert len(ir.messages) == 3
    assert ir.messages[0].index == 0
    assert ir.messages[0].from_ == "User"
    assert ir.messages[1].kind == "sync"


def test_state_ir():
    ir = compile_ir(load(FIXTURES / "state.quotation.yml"))
    assert ir.initial == "browsing"
    assert ir.entity == "Quotation"
    assert len(ir.states) == 3
    assert ir.transitions[1].guard == "all validations passed"


def test_component_ir():
    ir = compile_ir(load(FIXTURES / "component.quotation.yml"))
    ids = [n.id for n in ir.nodes]
    assert "QuotationFlow" in ids
    qf = next(n for n in ir.nodes if n.id == "QuotationFlow")
    assert "ClientSelection" in qf.contains
    assert ir.edges[0].relation == "reads_writes"


def test_activity_ir():
    ir = compile_ir(load(FIXTURES / "activity.validation.yml"))
    assert ir.start == "load_basket"
    cv = next(s for s in ir.steps if s.id == "check_validity")
    assert cv.kind == "decision"
    assert cv.branches["yes"] == "export_summary"


def test_deployment_ir():
    ir = compile_ir(load(FIXTURES / "deployment.runtime.yml"))
    assert any(n.id == "browser" for n in ir.nodes)
    assert any(a.id == "quotation_ui" for a in ir.artifacts)
    assert ir.connections[0].protocol == "HTTPS"


def test_matrix_stages():
    ir = compile_ir(load(FIXTURES / "matrix.quotation-view.yml"))
    assert len(ir.stages) == 5
    assert ir.stages[0].id == "browse"
    assert ir.stages[0].index == 0


def test_matrix_rows_depth():
    ir = compile_ir(load(FIXTURES / "matrix.quotation-view.yml"))
    qf = next(r for r in ir.rows if r.id == "QuotationFlow")
    store = next(r for r in ir.rows if r.id == "Store")
    assert qf.depth == 0
    assert store.depth == 1


def test_matrix_spans():
    ir = compile_ir(load(FIXTURES / "matrix.quotation-view.yml"))
    qf_spans = [s for s in ir.spans if s.component == "QuotationFlow"]
    assert len(qf_spans) == 1
    assert qf_spans[0].start == 0 and qf_spans[0].end == 5


def test_matrix_contiguous_helper_handles_empty_and_gaps():
    assert _contiguous([]) == []
    assert _contiguous([0, 1, 3, 4, 7]) == [(0, 2), (3, 5), (7, 8)]


def test_compile_ir_rejects_unknown_diagram_type():
    class DummyDiagram(BaseDiagram):
        pass

    diagram = DummyDiagram(id="x", title="x", type="reflection", version="1")
    with pytest.raises(CompileError, match="No compiler"):
        compile_ir(diagram)


# ── compile_ir (the test_compile_* of tests/test_api.py) ──────────────────────

def test_compile_sequence():
    assert isinstance(compile_ir(load(FIXTURES / "sequence.create-quotation.yml")), SequenceIR)


def test_compile_state():
    assert isinstance(compile_ir(load(FIXTURES / "state.quotation.yml")), StateIR)


def test_compile_component():
    assert isinstance(compile_ir(load(FIXTURES / "component.quotation.yml")), ComponentIR)


def test_compile_activity():
    assert isinstance(compile_ir(load(FIXTURES / "activity.validation.yml")), ActivityIR)


def test_compile_deployment():
    assert isinstance(compile_ir(load(FIXTURES / "deployment.runtime.yml")), DeploymentIR)


def test_compile_matrix():
    assert isinstance(compile_ir(load(FIXTURES / "matrix.quotation-view.yml")), MatrixIR)


# ── Reflection (tests/test_reflection_compiler.py) ────────────────────────────

def test_compile_enforcement_artifact_from_fixture():
    diagram = load(ROOT / "examples" / "reflection" / "canonical.yml")

    assert isinstance(diagram, ReflectionDiagram)

    artifact = compile_ir(diagram)
    assert isinstance(artifact, EnforcementArtifact)
    assert len(artifact.facts) > 0
    assert artifact.fingerprint is not None

    uses_fact = next(f for f in artifact.facts if f.relation == "uses")
    assert uses_fact.source == "api"
    assert uses_fact.target == "core"


# ── Class (compile cases of tests/test_class_diagram.py and tests/test_class_packages.py) ──

def test_compiler_preserves_structured_signatures():
    """test_schema_and_compiler_preserve_structured_signatures without its json_schema asserts (IR12)."""
    diagram = load(ROOT / "examples" / "class" / "runtime.yml")
    validate(diagram)
    ir = compile_ir(diagram)
    assert isinstance(ir, ClassIR)
    method = ir.classes[0].methods[0]
    assert method.name == "execute"
    assert [(p.name, p.type) for p in method.parameters] == [
        ("context", "ExecutionContext"), ("input", "PortValues")]
    assert method.returns == "ExecutionResult"
    assert ir.classes[1].attributes[0].visibility == "private"
    assert ir.relations[1].to_multiplicity == "1"


def test_ir_knows_paths_and_owners():
    diagram = load(FIXTURES / "class.packages.yml")
    validate(diagram)
    ir = compile_ir(diagram)
    assert ir.package_path("billing") == ["core", "billing"] and ir.package_of("Invoice") == "billing"
    assert ir.package_of("AuditLog") == "shared"


# ── Activity (tests/test_activity_lanes.py) ───────────────────────────────────

def test_fields_reach_the_ir():
    diagram = load(FIXTURES / "activity.lanes.yml")
    validate(diagram)
    steps = {s.id: s for s in compile_ir(diagram).steps}
    assert steps["open_pr"].partition == "Dev" and steps["review"].notes == "Two approvals for production"
    assert steps["joined"].kind == "merge" and steps["joined"].notes is None


# ── Errors (the CompileError asserts of tests/test_exceptions.py) ─────────────

def test_compile_error_is_a_visual_layer_error():
    assert issubclass(CompileError, Spec2VizError)
    with pytest.raises(Spec2VizError):
        raise CompileError("no compiler")
