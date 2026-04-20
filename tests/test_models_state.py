import yaml
from pathlib import Path
from yaml_charts.models.state import StateDiagram

FIXTURE = Path("tests/fixtures/state.quotation.yml")

def test_state_loads():
    data = yaml.safe_load(FIXTURE.read_text())
    d = StateDiagram.model_validate(data)
    assert d.id == "state.quotation"
    assert d.data.entity == "Quotation"
    assert d.data.initial == "browsing"

def test_state_states():
    data = yaml.safe_load(FIXTURE.read_text())
    d = StateDiagram.model_validate(data)
    assert len(d.data.states) == 3
    assert d.data.states[0].id == "browsing"

def test_state_transitions():
    data = yaml.safe_load(FIXTURE.read_text())
    d = StateDiagram.model_validate(data)
    assert len(d.data.transitions) == 2
    t = d.data.transitions[1]
    assert t.from_ == "client_selected"
    assert t.on == "complete"
    assert t.guard == "all validations passed"
