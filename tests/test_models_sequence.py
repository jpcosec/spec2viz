import yaml
from pathlib import Path
from yaml_charts.models.sequence import SequenceDiagram

FIXTURE = Path("tests/fixtures/sequence.create-quotation.yml")

def test_sequence_loads():
    data = yaml.safe_load(FIXTURE.read_text())
    d = SequenceDiagram.model_validate(data)
    assert d.id == "sequence.create-quotation"
    assert d.type.value == "sequence"

def test_sequence_participants():
    data = yaml.safe_load(FIXTURE.read_text())
    d = SequenceDiagram.model_validate(data)
    assert len(d.data.participants) == 3
    assert d.data.participants[0].id == "User"
    assert d.data.participants[0].kind == "actor"

def test_sequence_messages():
    data = yaml.safe_load(FIXTURE.read_text())
    d = SequenceDiagram.model_validate(data)
    assert len(d.data.messages) == 3
    assert d.data.messages[0].from_ == "User"
    assert d.data.messages[0].to == "QuotationFlow"
    assert d.data.messages[1].kind == "sync"
