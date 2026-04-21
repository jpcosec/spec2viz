from pathlib import Path
from click.testing import CliRunner
from yaml_charts.cli import main

FIXTURES = Path("tests/fixtures")
runner   = CliRunner()


def test_validate_valid():
    r = runner.invoke(main, ["validate", str(FIXTURES / "sequence.create-quotation.yml")])
    assert r.exit_code == 0
    assert "OK" in r.output

def test_validate_invalid():
    r = runner.invoke(main, ["validate", str(FIXTURES / "invalid" / "unknown_node.yml")])
    assert r.exit_code != 0

def test_render_sequence(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path)])
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()

def test_render_matrix(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "matrix.quotation-view.yml"), "--out", str(tmp_path)])
    assert r.exit_code == 0
    assert (tmp_path / "matrix.quotation-view.vega.json").exists()

def test_render_override(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "sequence.create-quotation.yml"),
                             "--out", str(tmp_path), "--renderer", "mermaid"])
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.mmd").exists()
