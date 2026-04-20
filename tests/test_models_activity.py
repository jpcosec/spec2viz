import yaml
from pathlib import Path
from yaml_charts.models.activity import ActivityDiagram

FIXTURE = Path("tests/fixtures/activity.validation.yml")

def test_activity_loads():
    data = yaml.safe_load(FIXTURE.read_text())
    d = ActivityDiagram.model_validate(data)
    assert d.id == "activity.validation"
    assert d.data.start == "load_basket"
    assert d.data.end == "end"

def test_activity_steps():
    data = yaml.safe_load(FIXTURE.read_text())
    d = ActivityDiagram.model_validate(data)
    assert "load_basket" in d.data.steps
    assert d.data.steps["load_basket"].label == "Load basket"
    assert d.data.steps["load_basket"].next == "calculate_price"

def test_activity_decision_step():
    data = yaml.safe_load(FIXTURE.read_text())
    d = ActivityDiagram.model_validate(data)
    step = d.data.steps["check_validity"]
    assert step.kind == "decision"
    assert step.branches["yes"] == "export_summary"
    assert step.branches["no"] == "show_errors"
