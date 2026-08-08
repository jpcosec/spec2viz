import pytest
from pathlib import Path
from spec2viz.loader import load
from spec2viz.validator import validate
from spec2viz.exceptions import ValidationError
from spec2viz.models.activity import ActivityData, ActivityDiagram, StepModel
from spec2viz.models.component import ComponentData, ComponentDiagram, EdgeModel, NodeModel
from spec2viz.models.deployment import ArtifactModel, ConnectionModel, DeploymentData, DeploymentDiagram, DeploymentNodeModel
from spec2viz.models.matrix import MatrixComponentModel, MatrixData, MatrixDiagram, MatrixStageModel, MatrixViewModel
from spec2viz.models.sequence import MessageModel, ParticipantModel, SequenceData, SequenceDiagram
from spec2viz.models.state import StateData, StateDiagram, StateModel, TransitionModel

FIXTURES = Path("tests/fixtures")
INVALID  = FIXTURES / "invalid"

def test_valid_component_passes():   validate(load(FIXTURES / "component.quotation.yml"))
def test_valid_sequence_passes():    validate(load(FIXTURES / "sequence.create-quotation.yml"))
def test_valid_state_passes():       validate(load(FIXTURES / "state.quotation.yml"))
def test_valid_activity_passes():    validate(load(FIXTURES / "activity.validation.yml"))
def test_valid_deployment_passes():  validate(load(FIXTURES / "deployment.runtime.yml"))
def test_valid_matrix_passes():      validate(load(FIXTURES / "matrix.quotation-view.yml"))

def test_unknown_node_raises():
    with pytest.raises(ValidationError, match="MissingNode"):
        validate(load(INVALID / "unknown_node.yml"))

def test_unknown_stage_raises():
    with pytest.raises(ValidationError, match="nonexistent_stage"):
        validate(load(INVALID / "unknown_stage.yml"))

def test_bad_activity_step_raises():
    with pytest.raises(ValidationError, match="nonexistent_step"):
        validate(load(INVALID / "bad_activity.yml"))

def test_bad_deployment_artifact_raises():
    with pytest.raises(ValidationError, match="missing_artifact"):
        validate(load(INVALID / "bad_deployment.yml"))

def test_bad_sequence_participant_raises():
    with pytest.raises(ValidationError, match="GhostComponent"):
        validate(load(INVALID / "bad_sequence.yml"))

def test_bad_state_transition_raises():
    with pytest.raises(ValidationError, match="nonexistent_state"):
        validate(load(INVALID / "bad_state.yml"))


def test_component_unknown_target_raises():
    diagram = ComponentDiagram(
        id="c",
        title="c",
        type="component",
        version="1",
        data=ComponentData(
            nodes={"A": NodeModel(label="A")},
            edges=[EdgeModel(**{"from": "A", "to": "B"})],
        ),
    )
    with pytest.raises(ValidationError, match="unknown node 'B'"):
        validate(diagram)



def test_component_unknown_source_raises():
    diagram = ComponentDiagram(
        id="c2",
        title="c2",
        type="component",
        version="1",
        data=ComponentData(
            nodes={"A": NodeModel(label="A")},
            edges=[EdgeModel(**{"from": "Ghost", "to": "A"})],
        ),
    )
    with pytest.raises(ValidationError, match="unknown node 'Ghost'"):
        validate(diagram)


def test_sequence_unknown_sender_raises():
    diagram = SequenceDiagram(
        id="s",
        title="s",
        type="sequence",
        version="1",
        data=SequenceData(
            participants=[ParticipantModel(id="A")],
            messages=[MessageModel(**{"from": "Ghost", "to": "A", "message": "hi"})],
        ),
    )
    with pytest.raises(ValidationError, match="unknown participant 'Ghost'"):
        validate(diagram)


def test_state_initial_and_target_errors_raise():
    bad_initial = StateDiagram(
        id="st1",
        title="st1",
        type="state",
        version="1",
        data=StateData(
            entity="Order",
            initial="missing",
            states=[StateModel(id="open", label="Open")],
            transitions=[],
        ),
    )
    with pytest.raises(ValidationError, match="Initial state 'missing'"):
        validate(bad_initial)

    bad_target = StateDiagram(
        id="st2",
        title="st2",
        type="state",
        version="1",
        data=StateData(
            entity="Order",
            initial="open",
            states=[StateModel(id="open", label="Open")],
            transitions=[TransitionModel(**{"from": "open", "to": "closed", "on": "finish"})],
        ),
    )
    with pytest.raises(ValidationError, match="unknown state 'closed'"):
        validate(bad_target)

    bad_source = StateDiagram(
        id="st3",
        title="st3",
        type="state",
        version="1",
        data=StateData(
            entity="Order",
            initial="open",
            states=[StateModel(id="open", label="Open")],
            transitions=[TransitionModel(**{"from": "ghost", "to": "open", "on": "rewind"})],
        ),
    )
    with pytest.raises(ValidationError, match="unknown state 'ghost'"):
        validate(bad_source)


def test_activity_missing_start_raises():
    diagram = ActivityDiagram(
        id="a1",
        title="a1",
        type="activity",
        version="1",
        data=ActivityData(
            start="missing",
            end="end",
            steps={"step1": StepModel(label="Step 1", next="end")},
        ),
    )
    with pytest.raises(ValidationError, match="Start step 'missing'"):
        validate(diagram)

    bad_branch = ActivityDiagram(
        id="a2",
        title="a2",
        type="activity",
        version="1",
        data=ActivityData(
            start="step1",
            end="end",
            steps={"step1": StepModel(label="Decide", kind="decision", branches={"yes": "ghost"})},
        ),
    )
    with pytest.raises(ValidationError, match="target 'ghost' unknown"):
        validate(bad_branch)


def test_deployment_unknown_connection_target_raises():
    diagram = DeploymentDiagram(
        id="d1",
        title="d1",
        type="deployment",
        version="1",
        data=DeploymentData(
            nodes={"server": DeploymentNodeModel(label="Server", contains=["api"])},
            artifacts={"api": ArtifactModel(label="API")},
            connections=[ConnectionModel(**{"from": "api", "to": "ghost"})],
        ),
    )
    with pytest.raises(ValidationError, match="unknown artifact 'ghost'"):
        validate(diagram)

    bad_source = DeploymentDiagram(
        id="d2",
        title="d2",
        type="deployment",
        version="1",
        data=DeploymentData(
            nodes={"server": DeploymentNodeModel(label="Server", contains=["api"])},
            artifacts={"api": ArtifactModel(label="API")},
            connections=[ConnectionModel(**{"from": "ghost", "to": "api"})],
        ),
    )
    with pytest.raises(ValidationError, match="unknown artifact 'ghost'"):
        validate(bad_source)


def test_matrix_nested_child_unknown_stage_raises():
    diagram = MatrixDiagram(
        id="m1",
        title="m1",
        type="component_view_matrix",
        version="1",
        data=MatrixData(
            views=[
                MatrixViewModel(
                    id="view1",
                    label="View 1",
                    stages=[MatrixStageModel(id="stage1", label="Stage 1")],
                )
            ],
            components=[
                MatrixComponentModel(
                    name="Parent",
                    children=[
                        MatrixComponentModel(
                            name="Child",
                            stages={"view1": ["ghost"]},
                        )
                    ],
                )
            ],
        ),
    )
    with pytest.raises(ValidationError, match="unknown stage 'ghost'"):
        validate(diagram)
