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


def test_schema_diagram_store_stdout():
    r = runner.invoke(main, ["schema", "--type", "diagram-store"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output
    assert '"diagram_store"' in r.output


def test_schema_invalid_type_fails():
    r = runner.invoke(main, ["schema", "--type", "unknown"])
    assert r.exit_code != 0


def test_help_mentions_taxonomy_groups_and_renderers():
    r = runner.invoke(main, ["--help"])
    assert r.exit_code == 0
    assert "diagram" in r.output
    assert "catalog" in r.output
    assert "Legacy top-level commands remain available" in r.output

    r = runner.invoke(main, ["render", "--help"])
    assert r.exit_code == 0
    for name in ["plantuml", "mermaid", "vega", "d2", "antonia-html", "json"]:
        assert name in r.output

    r = runner.invoke(main, ["diagram", "--help"])
    assert r.exit_code == 0
    assert "render" in r.output
    assert "validate" in r.output
    assert "schema" in r.output

    r = runner.invoke(main, ["catalog", "--help"])
    assert r.exit_code == 0
    assert "build" in r.output
    assert "schema" in r.output


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


def test_catalog_schema_stdout():
    r = runner.invoke(main, ["catalog", "schema"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output


def test_catalog_build_alias_matches_legacy_build(tmp_path):
    (tmp_path / "template.html").write_text(
        "<html><body>{{NAV}}{{FILTERS}}{{SECTIONS}}</body></html>", encoding="utf-8"
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

    legacy = tmp_path / "legacy.html"
    grouped = tmp_path / "grouped.html"
    r1 = runner.invoke(main, ["build", "--config", str(config), "--out", str(legacy)])
    r2 = runner.invoke(main, ["catalog", "build", "--config", str(config), "--out", str(grouped)])
    assert r1.exit_code == 0, r1.output
    assert r2.exit_code == 0, r2.output
    assert legacy.read_text(encoding="utf-8") == grouped.read_text(encoding="utf-8")


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
    html = out.read_text(encoding="utf-8")
    assert "catalog-search" in html


def test_build_command_supports_store_of_stores(tmp_path):
    root = tmp_path
    child = root / "child"
    child.mkdir()

    (root / "template.html").write_text(
        "<html><head><title>{{CATALOG_TITLE}}</title></head><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>",
        encoding="utf-8",
    )
    (child / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (child / "spec-component.yml").write_text(
        "id: spec-component\ntitle: Example\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n",
        encoding="utf-8",
    )
    (child / "vistas.yml").write_text(
        """
template: unused.html
vistas:
  - id: sample
    category: Arquitectura
    title: Sample Diagram
    nav: Sample
    desc: Demo child vista
    src: view.mmd
    specs:
      - spec-component
""",
        encoding="utf-8",
    )
    (root / "catalog.yml").write_text(
        """
template: template.html
title: Repo Catalog
brand_name: Diagram Catalog
stores:
  - path: child/vistas.yml
    project: demo/project
    tags:
      - domain:crm
""",
        encoding="utf-8",
    )

    out = root / "out.html"
    r = runner.invoke(main, ["build", "--config", str(root / "catalog.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert "Repo Catalog" in html
    assert "Diagram Catalog" in html
    assert "catalog-search" in html
    assert "data-project=\"demo/project\"" in html
    assert "data-type=\"component\"" in html
    assert "domain:crm" in html
    assert "Sample Diagram" in html


def test_build_command_supports_project_yml_envelope(tmp_path):
    root = tmp_path
    child = root / "child"
    child.mkdir()

    (root / "template.html").write_text(
        "<html><head><title>{{CATALOG_TITLE}}</title></head><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>",
        encoding="utf-8",
    )
    (child / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (child / "spec-state.yml").write_text(
        "id: spec-state\ntitle: Example State\ntype: state\nversion: '1.0'\ndata:\n  entity: X\n  initial: a\n  states:\n    - id: a\n      label: A\n  transitions: []\n",
        encoding="utf-8",
    )
    (child / "vistas.yml").write_text(
        """
template: ../template.html
vistas:
  - id: sample-state
    category: Estados
    title: State Diagram
    nav: State
    desc: Demo leaf
    src: view.mmd
    specs:
      - spec-state.yml
""",
        encoding="utf-8",
    )
    (root / "project.yml").write_text(
        """
diagram_store:
  kind: diagram-store
  template: template.html
  title: Project Catalog
  brand_name: Project Brand
  project_name: project/demo
  stores:
    - path: child/vistas.yml
      project: project/demo
      tags:
        - domain:workflow
""",
        encoding="utf-8",
    )

    out = root / "out.html"
    r = runner.invoke(main, ["build", "--config", str(root / "project.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert "Project Catalog" in html
    assert "Project Brand" in html
    assert "project/demo" in html
    assert "domain:workflow" in html
    assert "data-type=\"state\"" in html


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
