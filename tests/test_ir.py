from yaml_charts.ir import (
    MatrixIR, Stage, Row, Span,
    SequenceIR, Participant, Message,
    StateIR, StateNode, Transition,
    ComponentIR, ComponentNode, ComponentEdge,
    ActivityIR, ActivityStep,
    DeploymentIR, DeploymentNode, DeploymentArtifact, DeploymentConnection,
)

def test_matrix_ir():
    ir = MatrixIR(
        title="T",
        stages=[Stage("s1", 0, "S1")],
        rows=[Row("C1", "C1", 0, 0)],
        spans=[Span("C1", 0, 0, 1, "core")],
    )
    assert ir.stages[0].index == 0
    assert ir.spans[0].end == 1

def test_sequence_ir():
    ir = SequenceIR(
        title="T",
        participants=[Participant("User", "actor")],
        messages=[Message(0, "User", "App", "hello")],
    )
    assert ir.messages[0].kind == "sync"

def test_state_ir():
    ir = StateIR("T", "Order", "new",
                 [StateNode("new", "New")],
                 [Transition("new", "done", "complete")])
    assert ir.transitions[0].guard is None
