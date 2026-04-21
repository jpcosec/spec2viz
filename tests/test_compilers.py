from pathlib import Path
from spec2viz.loader import load
from spec2viz.compilers import compile_ir
from spec2viz.ir import (
    SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR, MatrixIR,
)

FIXTURES = Path("tests/fixtures")


# ── Dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_sequence():   assert isinstance(compile_ir(load(FIXTURES / "sequence.create-quotation.yml")), SequenceIR)
def test_dispatch_state():      assert isinstance(compile_ir(load(FIXTURES / "state.quotation.yml")), StateIR)
def test_dispatch_component():  assert isinstance(compile_ir(load(FIXTURES / "component.quotation.yml")), ComponentIR)
def test_dispatch_activity():   assert isinstance(compile_ir(load(FIXTURES / "activity.validation.yml")), ActivityIR)
def test_dispatch_deployment():  assert isinstance(compile_ir(load(FIXTURES / "deployment.runtime.yml")), DeploymentIR)
def test_dispatch_matrix():     assert isinstance(compile_ir(load(FIXTURES / "matrix.quotation-view.yml")), MatrixIR)


# ── Sequence ──────────────────────────────────────────────────────────────────

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


# ── State ─────────────────────────────────────────────────────────────────────

def test_state_ir():
    ir = compile_ir(load(FIXTURES / "state.quotation.yml"))
    assert ir.initial == "browsing"
    assert ir.entity == "Quotation"
    assert len(ir.states) == 3
    assert ir.transitions[1].guard == "all validations passed"


# ── Component ─────────────────────────────────────────────────────────────────

def test_component_ir():
    ir = compile_ir(load(FIXTURES / "component.quotation.yml"))
    ids = [n.id for n in ir.nodes]
    assert "QuotationFlow" in ids
    qf = next(n for n in ir.nodes if n.id == "QuotationFlow")
    assert "ClientSelection" in qf.contains
    assert ir.edges[0].relation == "reads_writes"


# ── Activity ──────────────────────────────────────────────────────────────────

def test_activity_ir():
    ir = compile_ir(load(FIXTURES / "activity.validation.yml"))
    assert ir.start == "load_basket"
    cv = next(s for s in ir.steps if s.id == "check_validity")
    assert cv.kind == "decision"
    assert cv.branches["yes"] == "export_summary"


# ── Deployment ────────────────────────────────────────────────────────────────

def test_deployment_ir():
    ir = compile_ir(load(FIXTURES / "deployment.runtime.yml"))
    assert any(n.id == "browser" for n in ir.nodes)
    assert any(a.id == "quotation_ui" for a in ir.artifacts)
    assert ir.connections[0].protocol == "HTTPS"


# ── Matrix ────────────────────────────────────────────────────────────────────

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
