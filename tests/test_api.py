import json
from pathlib import Path
import pytest
from yaml_charts import load, validate, compile_ir, render, render_to_file
from yaml_charts.exceptions import ValidationError
from yaml_charts.models.sequence import SequenceDiagram
from yaml_charts.models.state import StateDiagram
from yaml_charts.models.component import ComponentDiagram
from yaml_charts.models.activity import ActivityDiagram
from yaml_charts.models.deployment import DeploymentDiagram
from yaml_charts.models.matrix import MatrixDiagram
from yaml_charts.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR, MatrixIR

FIXTURES = Path("tests/fixtures")


# ── load ──────────────────────────────────────────────────────────────────────

def test_load_sequence():   assert isinstance(load(FIXTURES / "sequence.create-quotation.yml"), SequenceDiagram)
def test_load_state():      assert isinstance(load(FIXTURES / "state.quotation.yml"), StateDiagram)
def test_load_component():  assert isinstance(load(FIXTURES / "component.quotation.yml"), ComponentDiagram)
def test_load_activity():   assert isinstance(load(FIXTURES / "activity.validation.yml"), ActivityDiagram)
def test_load_deployment(): assert isinstance(load(FIXTURES / "deployment.runtime.yml"), DeploymentDiagram)
def test_load_matrix():     assert isinstance(load(FIXTURES / "matrix.quotation-view.yml"), MatrixDiagram)


# ── validate ──────────────────────────────────────────────────────────────────

def test_validate_passes():
    validate(load(FIXTURES / "component.quotation.yml"))

def test_validate_fails():
    with pytest.raises(ValidationError):
        validate(load(FIXTURES / "invalid" / "unknown_node.yml"))


# ── compile_ir ────────────────────────────────────────────────────────────────

def test_compile_sequence():   assert isinstance(compile_ir(load(FIXTURES / "sequence.create-quotation.yml")), SequenceIR)
def test_compile_state():      assert isinstance(compile_ir(load(FIXTURES / "state.quotation.yml")), StateIR)
def test_compile_component():  assert isinstance(compile_ir(load(FIXTURES / "component.quotation.yml")), ComponentIR)
def test_compile_activity():   assert isinstance(compile_ir(load(FIXTURES / "activity.validation.yml")), ActivityIR)
def test_compile_deployment():  assert isinstance(compile_ir(load(FIXTURES / "deployment.runtime.yml")), DeploymentIR)
def test_compile_matrix():     assert isinstance(compile_ir(load(FIXTURES / "matrix.quotation-view.yml")), MatrixIR)


# ── render ────────────────────────────────────────────────────────────────────

def test_render_str():
    ir = compile_ir(load(FIXTURES / "sequence.create-quotation.yml"))
    assert "@startuml" in render(ir)

def test_render_dict():
    ir = compile_ir(load(FIXTURES / "matrix.quotation-view.yml"))
    assert isinstance(render(ir), dict)

def test_render_mermaid_override():
    ir = compile_ir(load(FIXTURES / "state.quotation.yml"))
    assert "stateDiagram-v2" in render(ir, renderer="mermaid")


# ── render_to_file ────────────────────────────────────────────────────────────

def test_render_to_file_puml(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "@startuml" in p.read_text()

def test_render_to_file_vega(tmp_path):
    p = render_to_file(FIXTURES / "matrix.quotation-view.yml", out=tmp_path)
    assert p.name.endswith(".vega.json")
    assert "$schema" in json.loads(p.read_text())

def test_render_to_file_state(tmp_path):
    p = render_to_file(FIXTURES / "state.quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "[*] -->" in p.read_text()

def test_render_to_file_activity(tmp_path):
    p = render_to_file(FIXTURES / "activity.validation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "start" in p.read_text()

def test_render_to_file_deployment(tmp_path):
    p = render_to_file(FIXTURES / "deployment.runtime.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "Browser" in p.read_text()

def test_render_to_file_component(tmp_path):
    p = render_to_file(FIXTURES / "component.quotation.yml", out=tmp_path)
    assert p.suffix == ".puml"
    assert "QuotationFlow" in p.read_text()

def test_render_to_file_override(tmp_path):
    p = render_to_file(FIXTURES / "sequence.create-quotation.yml", out=tmp_path, renderer="mermaid")
    assert p.suffix == ".mmd"
    assert "sequenceDiagram" in p.read_text()
