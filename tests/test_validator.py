import pytest
from pathlib import Path
from yaml_charts.loader import load
from yaml_charts.validator import validate
from yaml_charts.exceptions import ValidationError

FIXTURES = Path("tests/fixtures")
INVALID  = FIXTURES / "invalid"

def test_valid_component_passes():  validate(load(FIXTURES / "component.quotation.yml"))
def test_valid_sequence_passes():   validate(load(FIXTURES / "sequence.create-quotation.yml"))
def test_valid_state_passes():      validate(load(FIXTURES / "state.quotation.yml"))
def test_valid_matrix_passes():     validate(load(FIXTURES / "matrix.quotation-view.yml"))

def test_unknown_node_raises():
    with pytest.raises(ValidationError, match="MissingNode"):
        validate(load(INVALID / "unknown_node.yml"))

def test_unknown_stage_raises():
    with pytest.raises(ValidationError, match="nonexistent_stage"):
        validate(load(INVALID / "unknown_stage.yml"))
