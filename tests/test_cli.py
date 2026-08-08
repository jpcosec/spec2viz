from pathlib import Path
from click.testing import CliRunner
from spec2viz.cli import main

FIXTURES = Path("tests/fixtures")
runner = CliRunner()


# ── validate ──────────────────────────────────────────────────────────────────


def test_validate_valid():
    r = runner.invoke(
        main, ["validate", str(FIXTURES / "sequence.create-quotation.yml")]
    )
    assert r.exit_code == 0
    assert "OK" in r.output


def test_validate_invalid():
    r = runner.invoke(
        main, ["validate", str(FIXTURES / "invalid" / "unknown_node.yml")]
    )
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
    r = runner.invoke(
        main,
        [
            "render",
            str(FIXTURES / "sequence.create-quotation.yml"),
            "--out",
            str(tmp_path),
        ],
    )
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()


def test_render_matrix(tmp_path):
    r = runner.invoke(
        main,
        ["render", str(FIXTURES / "matrix.quotation-view.yml"), "--out", str(tmp_path)],
    )
    assert r.exit_code == 0
    assert (tmp_path / "matrix.quotation-view.vega.json").exists()


def test_render_state(tmp_path):
    r = runner.invoke(
        main, ["render", str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path)]
    )
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.puml").exists()


def test_render_activity(tmp_path):
    r = runner.invoke(
        main,
        ["render", str(FIXTURES / "activity.validation.yml"), "--out", str(tmp_path)],
    )
    assert r.exit_code == 0
    assert (tmp_path / "activity.validation.puml").exists()


def test_render_deployment(tmp_path):
    r = runner.invoke(
        main,
        ["render", str(FIXTURES / "deployment.runtime.yml"), "--out", str(tmp_path)],
    )
    assert r.exit_code == 0
    assert (tmp_path / "deployment.runtime.puml").exists()


def test_render_component(tmp_path):
    r = runner.invoke(
        main,
        ["render", str(FIXTURES / "component.quotation.yml"), "--out", str(tmp_path)],
    )
    assert r.exit_code == 0
    assert (tmp_path / "component.quotation.puml").exists()


def test_render_override(tmp_path):
    r = runner.invoke(
        main,
        [
            "render",
            str(FIXTURES / "sequence.create-quotation.yml"),
            "--out",
            str(tmp_path),
            "--renderer",
            "mermaid",
        ],
    )
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.mmd").exists()


def test_render_backend_alias(tmp_path):
    r = runner.invoke(
        main,
        [
            "render",
            str(FIXTURES / "state.quotation.yml"),
            "--out",
            str(tmp_path),
            "--backend",
            "mermaid",
        ],
    )
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.mmd").exists()


def test_render_multiple(tmp_path):
    r = runner.invoke(
        main,
        [
            "render",
            str(FIXTURES / "sequence.create-quotation.yml"),
            str(FIXTURES / "state.quotation.yml"),
            "--out",
            str(tmp_path),
        ],
    )
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()
    assert (tmp_path / "state.quotation.puml").exists()


def test_render_invalid_fails(tmp_path):
    r = runner.invoke(
        main,
        [
            "render",
            str(FIXTURES / "invalid" / "unknown_node.yml"),
            "--out",
            str(tmp_path),
        ],
    )
    assert r.exit_code != 0


def test_schema_stdout():
    r = runner.invoke(main, ["schema", "--type", "sequence"])
    assert r.exit_code == 0
    assert '"title": "SequenceDiagram"' in r.output


def test_schema_outfile(tmp_path):
    out = tmp_path / "schema.json"
    r = runner.invoke(main, ["schema", "--type", "state", "--out", str(out)])
    assert r.exit_code == 0
    assert out.exists()


def test_schema_invalid_type_fails():
    r = runner.invoke(main, ["schema", "--type", "unknown"])
    assert r.exit_code != 0


def test_help_mentions_build_and_all_renderers():
    r = runner.invoke(main, ["--help"])
    assert r.exit_code == 0
    assert "build" in r.output

    r = runner.invoke(main, ["render", "--help"])
    assert r.exit_code == 0
    for name in ["plantuml", "mermaid", "vega", "d2", "antonia-html", "json"]:
        assert name in r.output


def test_render_d2(tmp_path):
    r = runner.invoke(
        main,
        [
            "render",
            str(FIXTURES / "component.quotation.yml"),
            "--out",
            str(tmp_path),
            "--renderer",
            "d2",
        ],
    )
    assert r.exit_code == 0
    assert (tmp_path / "component.quotation.d2").exists()


def test_render_antonia_html(tmp_path):
    r = runner.invoke(
        main,
        [
            "render",
            str(FIXTURES / "sequence.create-quotation.yml"),
            "--out",
            str(tmp_path),
            "--renderer",
            "antonia-html",
        ],
    )
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.html").exists()


def test_render_json_reflection_artifact(tmp_path):
    r = runner.invoke(
        main,
        [
            "render",
            "examples/reflection/canonical.yml",
            "--out",
            str(tmp_path),
            "--renderer",
            "json",
        ],
    )
    assert r.exit_code == 0
    assert (tmp_path / "canonical.artifact.json").exists()


def test_build_command(tmp_path):
    (tmp_path / "template.html").write_text(
        "<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8"
    )
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text(
        """
template: template.html
vistas:
  - id: sample
    src: view.mmd
""",
        encoding="utf-8",
    )

    out = tmp_path / "out.html"
    r = runner.invoke(main, ["build", "--config", str(config), "--out", str(out)])
    assert r.exit_code == 0
    assert out.exists()
    assert "Rendered deskops architecture" in r.output


def test_build_command_reports_errors(tmp_path):
    (tmp_path / "template.html").write_text(
        "<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8"
    )
    config = tmp_path / "vistas.yml"
    config.write_text("template: template.html\nvistas: [\n  {id: broken, src: missing.mmd}\n]\n", encoding="utf-8")

    out = tmp_path / "out.html"
    r = runner.invoke(main, ["build", "--config", str(config), "--out", str(out)])
    assert r.exit_code != 0
    assert "Error building deskops" in r.output
