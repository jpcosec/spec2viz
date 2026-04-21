import pytest
from pathlib import Path
from yaml_charts.loader import load
from yaml_charts.models.sequence   import SequenceDiagram
from yaml_charts.models.state      import StateDiagram
from yaml_charts.models.component  import ComponentDiagram
from yaml_charts.models.activity   import ActivityDiagram
from yaml_charts.models.deployment import DeploymentDiagram
from yaml_charts.models.matrix     import MatrixDiagram
from yaml_charts.exceptions import ParseError

FIXTURES = Path("tests/fixtures")

def test_load_sequence():
    assert isinstance(load(FIXTURES / "sequence.create-quotation.yml"), SequenceDiagram)

def test_load_state():
    assert isinstance(load(FIXTURES / "state.quotation.yml"), StateDiagram)

def test_load_component():
    assert isinstance(load(FIXTURES / "component.quotation.yml"), ComponentDiagram)

def test_load_activity():
    assert isinstance(load(FIXTURES / "activity.validation.yml"), ActivityDiagram)

def test_load_deployment():
    assert isinstance(load(FIXTURES / "deployment.runtime.yml"), DeploymentDiagram)

def test_load_matrix():
    assert isinstance(load(FIXTURES / "matrix.quotation-view.yml"), MatrixDiagram)

def test_missing_file_raises():
    with pytest.raises(ParseError, match="not found"):
        load(FIXTURES / "nonexistent.yml")

def test_unsupported_type_raises(tmp_path):
    f = tmp_path / "bad.yml"
    f.write_text("id: x\ntitle: X\ntype: random_diagram\nversion: '0.1'\ndata: {}\n")
    with pytest.raises(ParseError, match="Unsupported diagram type"):
        load(f)
