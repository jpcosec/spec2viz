import importlib
import warnings
from pathlib import Path
import json

from click.testing import CliRunner

from spec2viz import json_schema, render_to_file
from spec2viz.cli import main as spec2viz_main
from spec2viz.models.activity import ActivityData, ActivityDiagram, StepModel
from spec2viz.models.base import BaseDiagram, Metadata, Style
from spec2viz.models.component import (
    ComponentData,
    ComponentDiagram,
    EdgeModel,
    NodeModel,
)
from spec2viz.models.deployment import (
    ArtifactModel,
    ConnectionModel,
    DeploymentData,
    DeploymentDiagram,
    DeploymentNodeModel,
)
from spec2viz.models.matrix import (
    MatrixComponentModel,
    MatrixData,
    MatrixDiagram,
    MatrixStageModel,
    MatrixViewModel,
)
from spec2viz.models.sequence import (
    MessageModel,
    ParticipantModel,
    SequenceData,
    SequenceDiagram,
)
from spec2viz.models.state import StateData, StateDiagram, StateModel, TransitionModel


def test_primary_cli_still_exposes_commands():
    runner = CliRunner()
    result = runner.invoke(spec2viz_main, ["--help"])

    assert result.exit_code == 0
    assert "render" in result.output
    assert "validate" in result.output


def test_every_model_field_has_a_description():
    model_classes = [
        Metadata,
        Style,
        BaseDiagram,
        ParticipantModel,
        MessageModel,
        SequenceData,
        SequenceDiagram,
        StateModel,
        TransitionModel,
        StateData,
        StateDiagram,
        NodeModel,
        EdgeModel,
        ComponentData,
        ComponentDiagram,
        StepModel,
        ActivityData,
        ActivityDiagram,
        DeploymentNodeModel,
        ArtifactModel,
        ConnectionModel,
        DeploymentData,
        DeploymentDiagram,
        MatrixStageModel,
        MatrixViewModel,
        MatrixComponentModel,
        MatrixData,
        MatrixDiagram,
    ]

    for model_class in model_classes:
        for field_name, field_info in model_class.model_fields.items():
            assert field_info.description, (
                f"{model_class.__name__}.{field_name} is missing a description"
            )


def test_examples_render_successfully(tmp_path):
    example_paths = sorted(Path("examples").glob("**/*.yml"))

    assert example_paths

    for example_path in example_paths:
        output_path = render_to_file(example_path, out=tmp_path)
        assert output_path.exists(), f"missing output for {example_path}"


def test_schema_examples_match_generated_output():
    checked_in_full_schema = Path("examples/schema/spec2viz.schema.json")
    checked_in_sequence_schema = Path("examples/schema/sequence.schema.json")

    assert json.loads(checked_in_full_schema.read_text()) == json_schema()
    assert json.loads(checked_in_sequence_schema.read_text()) == json_schema("sequence")



