import json
from pathlib import Path
import pytest
from yaml_charts import load, validate, compile_ir, render, render_to_file
from yaml_charts.exceptions import ValidationError
from yaml_charts.models.sequence import SequenceDiagram
from yaml_charts.ir import SequenceIR, MatrixIR

FIXTURES = Path("tests/fixtures")


def test_load():
    assert isinstance(load(FIXTURES / "sequence.create-quotation.yml"), SequenceDiagram)

def test_validate_passes():
    validate(load(FIXTURES / "component.quotation.yml"))

def test_validate_fails():
    with pytest.raises(ValidationError):
        validate(load(FIXTURES / "invalid" / "unknown_node.yml"))

def test_compile_ir():
    assert isinstance(compile_ir(load(FIXTURES / "sequence.create-quotation.yml")), SequenceIR)

def test_render_str():
    ir = compile_ir(load(FIXTURES / "sequence.create-quotation.yml"))
    assert "@startuml" in render(ir)

def test_render_dict():
    ir = compile_ir(load(FIXTURES / "matrix.quotation-view.yml"))
    assert isinstance(render(ir), dict)

def test_render_to_file_puml(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "@startuml" in p.read_text()

def test_render_to_file_vega(tmp_path):
    p = render_to_file(FIXTURES / "matrix.quotation-view.yml", out=tmp_path)
    assert p.name.endswith(".vega.json")
    assert "$schema" in json.loads(p.read_text())

def test_render_to_file_override(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path, renderer="mermaid")
    assert p.suffix == ".mmd"
    assert "sequenceDiagram" in p.read_text()
