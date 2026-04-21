from pathlib import Path
from click.testing import CliRunner
from yaml_charts.cli import main

FIXTURES = Path("tests/fixtures")
runner   = CliRunner()


# ── validate ──────────────────────────────────────────────────────────────────

def test_validate_valid():
    r = runner.invoke(main, ["validate", str(FIXTURES / "sequence.create-quotation.yml")])
    assert r.exit_code == 0
    assert "OK" in r.output

def test_validate_invalid():
    r = runner.invoke(main, ["validate", str(FIXTURES / "invalid" / "unknown_node.yml")])
    assert r.exit_code != 0

def test_validate_all_types():
    for name in [
        "sequence.create-quotation.yml",
        "state.quotation.yml",
        "activity.validation.yml",
        "deployment.runtime.yml",
        "component.quotation.yml",
        "matrix.quotation-view.yml",
    ]:
        r = runner.invoke(main, ["validate", str(FIXTURES / name)])
        assert r.exit_code == 0, f"{name}: {r.output}"


# ── render ────────────────────────────────────────────────────────────────────

def test_render_sequence(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path)])
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()

def test_render_matrix(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "matrix.quotation-view.yml"), "--out", str(tmp_path)])
    assert r.exit_code == 0
    assert (tmp_path / "matrix.quotation-view.vega.json").exists()

def test_render_state(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path)])
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.puml").exists()

def test_render_activity(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "activity.validation.yml"), "--out", str(tmp_path)])
    assert r.exit_code == 0
    assert (tmp_path / "activity.validation.puml").exists()

def test_render_deployment(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "deployment.runtime.yml"), "--out", str(tmp_path)])
    assert r.exit_code == 0
    assert (tmp_path / "deployment.runtime.puml").exists()

def test_render_component(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "component.quotation.yml"), "--out", str(tmp_path)])
    assert r.exit_code == 0
    assert (tmp_path / "component.quotation.puml").exists()

def test_render_override(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "sequence.create-quotation.yml"),
                             "--out", str(tmp_path), "--renderer", "mermaid"])
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.mmd").exists()

def test_render_backend_alias(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "state.quotation.yml"),
                             "--out", str(tmp_path), "--backend", "mermaid"])
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.mmd").exists()

def test_render_multiple(tmp_path):
    r = runner.invoke(main, [
        "render",
        str(FIXTURES / "sequence.create-quotation.yml"),
        str(FIXTURES / "state.quotation.yml"),
        "--out", str(tmp_path),
    ])
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()
    assert (tmp_path / "state.quotation.puml").exists()

def test_render_invalid_fails(tmp_path):
    r = runner.invoke(main, ["render", str(FIXTURES / "invalid" / "unknown_node.yml"),
                             "--out", str(tmp_path)])
    assert r.exit_code != 0
