"""catalog build dibuja cada vista desde la vista resuelta (notation_view): la misma fuente de
glifos, keyword, forma y estilo que graph_ui, con la notacion de la vista."""
import shutil
from pathlib import Path

import pytest
import yaml

from spec2viz.renderers.view_mermaid import view_to_mermaid

FIXTURES = Path(__file__).parent / "fixtures"
NOTATION = {
    "name": "infra-own", "title": "Infra", "diagram_type": "deployment", "layout": {"kind": "graph", "direction": "LR"},
    "glyphs": [
        {"id": "db", "model": "SpecNodeDoc", "where": 'kind = "database"', "shape": "cylinder", "keyword": "«{kind}»", "fill": {"light": "#fff1c2", "dark": "#3d3200"}},
        {"id": "node", "model": "SpecNodeDoc", "where": 'collection = "nodes"', "shape": "node-box", "keyword": "«node»"},
        {"id": "any", "model": "SpecNodeDoc", "shape": "rounded-box"},
    ],
    "links": [
        {"id": "contains", "relation": "contains", "draw": "nest"},
        {"id": "deploy", "relation": "deploy", "line": "dashed", "label": "«deploy»"},
        {"id": "any", "relation": "*", "color": "#0072b2", "target_end": "none", "label": "{data.protocol}"},
    ],
}

sldb_api = pytest.importorskip("sldb.api")


def _view(tmp_path, spec=FIXTURES / "deployment.nested.yml", notation=None):
    from spec2viz.notation_view import resolve_view
    from spec2viz.sldb_sync import SpecSync

    root = tmp_path / "scratch"
    sldb_api.init_store(root)
    (root / "docs").mkdir()
    copy = Path(shutil.copy(spec, root / "docs" / spec.name))
    report = SpecSync(root / ".sldb").sync(copy, notation=notation)
    return resolve_view(root / ".sldb", report.spec_id)


def _notation(tmp_path):
    path = tmp_path / "infra-own.yml"
    path.write_text(yaml.safe_dump(NOTATION, allow_unicode=True), encoding="utf-8")
    return path


# --- view_to_mermaid -----------------------------------------------------------------------------

def test_view_to_mermaid_uses_glyph_shape_keyword_style_nesting_and_links(tmp_path):
    out = view_to_mermaid(_view(tmp_path, notation=_notation(tmp_path)), theme="dark")
    lines = [l.strip() for l in out.splitlines()]
    assert out.startswith("---\nconfig:\n  layout: elk\n") and "flowchart LR" in lines
    # nodos que contienen son subgraph con su keyword; la base de datos es un cilindro con su keyword
    assert any(l.startswith("subgraph ") and "«node»<br/>VPC" in l for l in lines)
    assert any('[("«database»<br/>Postgres")]' in l for l in lines)
    # estilo resuelto (lado oscuro) y color de link
    assert any(l.startswith("style ") and "fill:#3d3200" in l and "color:#e6edf3" in l for l in lines)
    assert any(l.startswith("linkStyle ") and "stroke:#0072b2" in l for l in lines)
    # deploy punteado con su rotulo; la conexion sin terminal, con el protocolo
    assert any("-.->|\"«deploy»\"|" in l for l in lines) and any("---|\"HTTPS\"|" in l for l in lines)


def test_view_to_mermaid_compartments_and_pseudonodes(tmp_path):
    klass = view_to_mermaid(_view(tmp_path, FIXTURES / "class.packages.yml"))
    assert "<hr/>id: int<br/>total: Decimal" in klass and "@{ shape: notch-rect" not in klass  # paquetes con hijos son subgraph
    act = view_to_mermaid(_view(tmp_path / "a", FIXTURES / "activity.lanes.yml"))
    assert "@{ shape: sm-circ }" in act and "@{ shape: fr-circ }" in act and '{" "}' in act  # inicial, final y merge sin rotulo


def test_view_to_mermaid_refuses_non_graph_layouts(tmp_path):
    view = _view(tmp_path, Path(__file__).parent.parent / "docs" / "architecture" / "spec2viz" / "sequence-sync-pipeline.yml")
    with pytest.raises(ValueError, match="not a graph"):
        view_to_mermaid(view)


def test_view_to_mermaid_is_accepted_by_the_real_engine(tmp_path):
    import subprocess

    if shutil.which("mmdc") is None:
        pytest.skip("mmdc not installed")
    for name, spec in (("dep", FIXTURES / "deployment.nested.yml"), ("cls", FIXTURES / "class.packages.yml"), ("act", FIXTURES / "activity.lanes.yml")):
        source = tmp_path / f"{name}.mmd"
        source.write_text(view_to_mermaid(_view(tmp_path / name, spec, _notation(tmp_path) if name == "dep" else None)), encoding="utf-8")
        result = subprocess.run(["mmdc", "-i", str(source), "-o", str(tmp_path / f"{name}.svg"), "-q"], capture_output=True, text=True, timeout=120)
        assert result.returncode == 0, (name, result.stderr[-300:])


# --- catalog build ------------------------------------------------------------------------------

def _project(tmp_path, view_notation=None):
    root = tmp_path / "repo"
    arch = root / "docs" / "architecture"
    (root / ".git").mkdir(parents=True)
    arch.mkdir(parents=True)
    shutil.copy(FIXTURES / "deployment.nested.yml", arch / "nested.yml")
    shutil.copy(Path(__file__).parent.parent / "docs" / "architecture" / "spec2viz" / "sequence-sync-pipeline.yml", arch / "seq.yml")
    (arch / "seq.mmd").write_text("sequenceDiagram\n  A->>B: hi\n", encoding="utf-8")
    (arch / "nested.mmd").write_text("flowchart TD\n  legacy_src_marker --> x\n", encoding="utf-8")
    _notation(arch)
    vista = {"id": "nested", "title": "Nested", "category": "Infra", "src": "nested.mmd", "specs": ["nested.yml"]}
    if view_notation:
        vista["notation"] = view_notation
    vistas = [vista, {"id": "seq", "title": "Seq", "category": "Flows", "src": "seq.mmd", "specs": ["seq.yml"]}]
    (arch / "vistas.yml").write_text(yaml.safe_dump({"vistas": vistas}), encoding="utf-8")
    return root, arch


def _build(arch, tmp_path):
    from click.testing import CliRunner
    from spec2viz.cli import main

    out = tmp_path / "out" / "catalog.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    result = CliRunner().invoke(main, ["catalog", "build", "--config", str(arch / "vistas.yml"), "--out", str(out)])
    assert result.exit_code == 0, result.output
    return out.read_text(encoding="utf-8")


def test_catalog_build_draws_graph_views_from_the_view_notation(tmp_path):
    root, arch = _project(tmp_path, "infra-own.yml")
    page = _build(arch, tmp_path)
    assert 'data-resolved-from="SpecDoc:deployment.nested"' in page and 'data-notation="NotationDoc:infra-own"' in page
    assert "legacy_src_marker" not in page and "«database»&lt;br/&gt;Postgres" in page
    # una secuencia no es un grafo: sigue con su src
    assert "A-&gt;&gt;B: hi" in page and 'data-resolved-from="SpecDoc:sequence' not in page
    assert not list(Path("/tmp").glob("spec2viz-catalog-*"))  # el store temporal se borra


def test_catalog_build_uses_the_builtin_notation_without_the_field(tmp_path):
    root, arch = _project(tmp_path)
    page = _build(arch, tmp_path)
    assert 'data-notation="NotationDoc:deployment"' in page and "«database»" in page


def test_catalog_build_prefers_the_project_store_when_the_spec_is_synced(tmp_path, monkeypatch):
    from spec2viz import catalog_views
    from spec2viz.sldb_sync import sync_catalog, SpecSync

    root, arch = _project(tmp_path, "infra-own.yml")
    sldb_api.init_store(root)
    sync_catalog(SpecSync(root / ".sldb"), arch / "vistas.yml")
    monkeypatch.setattr(catalog_views, "_scratch_view", lambda *a, **k: (_ for _ in ()).throw(AssertionError("scratch store used")))
    page = _build(arch, tmp_path)
    assert 'data-resolved-from="SpecDoc:deployment.nested"' in page


def test_catalog_build_falls_back_to_src_without_sldb(tmp_path, monkeypatch):
    from spec2viz import catalog_views

    root, arch = _project(tmp_path)
    monkeypatch.setattr(catalog_views, "resolved_views", lambda *a, **k: None)
    page = _build(arch, tmp_path)
    assert "legacy_src_marker" in page and "data-resolved-from" not in page
