"""spec2viz's catalog tests, ported to specIR's catalog (IR13b) and to sldb's catalog operations.

Ported from spec2viz `2de1056` (`tests/test_catalog_paths.py`, `tests/test_catalog_notation.py`,
the catalog build cases of `tests/test_catalog_resolved_views.py`, `tests/test_deskops.py`,
`tests/test_atoms_matching.py`, the build cases of `tests/test_explicit_atoms.py` and the
`build`/`catalog build` cases of `tests/test_cli.py`). What changes, and why:

- `catalog validate` and `catalog sync` are sldb's now: `sldb notations sync --catalog [--check]`
  (D1), run as the real CLI. The path rule is `sldb.api.notations.catalog_paths`.
- `catalog build` is `specir.visual.catalog.render_catalog`/`build_catalog`; the command and its
  `build` alias are IR13d's, so the CLI cases run on the API: "Rendered catalog" and "Error building
  catalog" were the command's messages, the build's error is the exception it raises.
- The atoms are matched by `sldb.api.matching` (D4): warnings are sldb findings, strict mode raises
  sldb's `UnknownAtomError`. Where spec2viz faked a store with monkeypatch, a real sldb store is used.
- spec2viz monkeypatched its scratch store or its resolver to prove the project store is used or that
  the build falls back to `src`; here the project store is made unusable for the scratch path (a
  notation that only lives there) and a sequence spec (not a graph) shows the fallback."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import sldb.api as sldb_api
import yaml
from sldb.api.matching import UnknownAtomError, filter_atoms_payload, parse_atoms
from sldb.api.notations import SpecSync, catalog_entries, sync_catalog
from sldb.api.notations.catalog_paths import candidates, repo_root, resolve_catalog_path

from specir.visual.catalog import build_catalog, render_catalog, resolve_item_path, split_shared_atoms
from specir.visual.notation_style import AmbiguousPathError, UnknownNotationError, UnknownReferenceError

HERE = Path(__file__).resolve().parent
SPECS = HERE / "fixtures" / "spec2viz" / "tests" / "fixtures"
ARCH_SPECS = HERE / "fixtures" / "spec2viz" / "docs" / "architecture" / "spec2viz"
TEMPLATE = Path(__file__).resolve().parents[2] / "src" / "specir" / "visual" / "templates" / "default.html"
SLDB = str(Path(sys.executable).with_name("sldb"))
NOTATION = {"name": "flow-own", "diagram_type": "activity", "glyphs": [{"id": "step", "model": "SpecNodeDoc", "shape": "box"}],
            "links": [{"id": "next", "relation": "next"}]}
OWN_NOTATION = {**NOTATION, "title": "Own flow", "layout": {"kind": "graph"}}
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node runs the template's code")


def sldb_cli(*args, cwd: Path | None = None) -> tuple[int, str]:
    done = subprocess.run([SLDB, *map(str, args)], capture_output=True, text=True, cwd=cwd)
    return done.returncode, done.stdout + done.stderr


def check(config: Path, store: Path | None = None) -> tuple[int, str]:
    """`catalog validate` of spec2viz: `sldb notations sync --catalog <config> --check`."""
    return sldb_cli("notations", "sync", "--catalog", config, "--check", *(["--store", store] if store else []))


def sync(config: Path, store: Path) -> tuple[int, str]:
    """`catalog sync` of spec2viz: `sldb notations sync --catalog <config> --store <store>`."""
    return sldb_cli("notations", "sync", "--catalog", config, "--store", store)


def spec_docs(store: Path) -> list:
    return [d for d in sldb_api.load_runtime_documents(store, None, include_linked=False) if str(d.model_name) == "SpecDoc"]


# --- tests/test_catalog_paths.py ----------------------------------------------------------------

def _repo(tmp_path):
    """repo/ with .git; the registry in repo/docs/architecture/vistas.yml."""
    root = tmp_path / "repo"
    arch = root / "docs" / "architecture"
    (root / ".git").mkdir(parents=True)
    (arch / "flows").mkdir(parents=True)
    (arch / "notations").mkdir()
    shutil.copy(SPECS / "activity.lanes.yml", arch / "flows" / "lanes.yml")
    (arch / "notations" / "flow-own.yml").write_text(yaml.safe_dump(NOTATION), encoding="utf-8")
    (arch / "flows" / "lanes.mmd").write_text("flowchart TD\n  a --> b\n", encoding="utf-8")
    return root, arch


def _vistas(arch, **view):
    vista = {"id": "lanes", "category": "Flujos", "nav": "Carriles", **view}
    (arch / "vistas.yml").write_text(yaml.safe_dump({"vistas": [vista]}), encoding="utf-8")
    return arch / "vistas.yml"


def test_repo_root_and_candidates(tmp_path):
    root, arch = _repo(tmp_path)
    assert repo_root(arch) == root.resolve()
    assert candidates("x/y.yml", arch) == [(arch / "x/y.yml").resolve(), (root / "x/y.yml").resolve()]
    assert candidates("x/y.yml", root) == [(root / "x/y.yml").resolve()]


@pytest.mark.parametrize("specs, notation, src", [
    ("flows/lanes.yml", "notations/flow-own.yml", "flows/lanes.mmd"),
    ("docs/architecture/flows/lanes.yml", "docs/architecture/notations/flow-own.yml", "docs/architecture/flows/lanes.mmd"),
])
def test_the_three_fields_resolve_both_ways(tmp_path, specs, notation, src):
    root, arch = _repo(tmp_path)
    config = _vistas(arch, specs=[specs], notation=notation, src=src)
    rc, output = check(config)
    assert rc == 0, output
    entry = catalog_entries(config)[0]
    assert entry["spec"] == (arch / "flows" / "lanes.yml").resolve()
    assert entry["notation"] == (arch / "notations" / "flow-own.yml").resolve()
    assert entry["src"] == (arch / "flows" / "lanes.mmd").resolve() and entry["errors"] == []


def test_reported_case_root_relative_notation_is_not_doubled(tmp_path):
    root, arch = _repo(tmp_path)
    config = _vistas(arch, specs=["docs/architecture/flows/lanes.yml"], notation="docs/architecture/notations/flow-own.yml")
    rc, output = check(config)
    assert rc == 0 and "docs/architecture/docs/architecture" not in output


@pytest.mark.parametrize("field", ["specs", "notation", "src"])
def test_two_different_files_are_ambiguous_in_validate_and_sync(tmp_path, field):
    root, arch = _repo(tmp_path)
    sldb_api.init_store(root)
    rel = {"specs": "flows/lanes.yml", "notation": "notations/flow-own.yml", "src": "flows/lanes.mmd"}[field]
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text((arch / rel).read_text(encoding="utf-8") + "\n# otra copia\n", encoding="utf-8")
    config = _vistas(arch, specs=["flows/lanes.yml"], notation="notations/flow-own.yml", src="flows/lanes.mmd")
    for command in (check, sync):
        rc, output = command(config, root / ".sldb")
        assert rc == 1 and "AmbiguousPathError" in output, (command.__name__, output)
        assert str((arch / rel).resolve()) in output and str((root / rel).resolve()) in output
    assert not spec_docs(root / ".sldb")


def test_same_file_both_ways_is_not_ambiguous(tmp_path):
    root, arch = _repo(tmp_path)
    (root / "flows").symlink_to(arch / "flows", target_is_directory=True)
    assert resolve_catalog_path("flows/lanes.yml", arch, "spec") == (arch / "flows" / "lanes.yml").resolve()


@pytest.mark.parametrize("field, value, error", [
    ("specs", "flows/missing.yml", "UnknownReferenceError"),
    ("notation", "notations/missing.yml", "UnknownNotationError"),
    ("src", "flows/missing.mmd", "UnknownReferenceError"),
])
def test_not_found_lists_the_paths_tried(tmp_path, field, value, error):
    root, arch = _repo(tmp_path)
    config = _vistas(arch, **{"specs": ["flows/lanes.yml"], field: [value] if field == "specs" else value})
    rc, output = check(config)
    assert rc == 1 and error in output and "tried:" in output
    assert str((arch / value).resolve()) in output and str((root / value).resolve()) in output


def test_missing_src_does_not_block_sync_but_ambiguity_does(tmp_path):
    root, arch = _repo(tmp_path)
    sldb_api.init_store(root)
    rc, output = sync(_vistas(arch, specs=["flows/lanes.yml"], src="flows/missing.mmd"), root / ".sldb")
    assert rc == 0, output


def test_resolver_types(tmp_path):
    root, arch = _repo(tmp_path)
    with pytest.raises(UnknownNotationError, match="tried:"):
        resolve_catalog_path("nope.yml", arch, "notation", UnknownNotationError)
    with pytest.raises(UnknownReferenceError):
        resolve_catalog_path("nope.yml", arch, "spec")
    (root / "flows").mkdir()
    (root / "flows" / "lanes.yml").write_text("id: other\n", encoding="utf-8")
    with pytest.raises(AmbiguousPathError):
        resolve_catalog_path("flows/lanes.yml", arch, "spec")


def test_catalog_build_reads_src_with_the_same_rule(tmp_path):
    root, arch = _repo(tmp_path)
    assert resolve_item_path("docs/architecture/flows/lanes.mmd", arch, "src") == (arch / "flows" / "lanes.mmd").resolve()
    (root / "flows").mkdir()
    (root / "flows" / "lanes.mmd").write_text("flowchart LR\n", encoding="utf-8")
    with pytest.raises(AmbiguousPathError):
        resolve_item_path("flows/lanes.mmd", arch, "src")


# --- tests/test_catalog_notation.py -------------------------------------------------------------

def _notation_project(tmp_path, view_notation=None):
    sldb_api.init_store(tmp_path)
    docs = tmp_path / "docs"
    (docs / "notations").mkdir(parents=True)
    shutil.copy(SPECS / "activity.lanes.yml", docs / "lanes.yml")
    (docs / "notations" / "flow-own.yml").write_text(yaml.safe_dump(OWN_NOTATION), encoding="utf-8")
    vista = {"id": "lanes", "category": "Flujos", "nav": "Carriles", "desc": "Aprobacion", "specs": ["lanes.yml"]}
    if view_notation is not None:
        vista["notation"] = view_notation
    (docs / "vistas.yml").write_text(yaml.safe_dump({"vistas": [vista]}), encoding="utf-8")
    return docs / "vistas.yml"


def _spec_doc(tmp_path):
    return next(d.payload for d in spec_docs(tmp_path / ".sldb") if d.name == "activity.lanes")


def test_diagram_sync_with_notation_keeps_the_catalog_metadata(tmp_path):
    config = _notation_project(tmp_path)
    assert sync(config, tmp_path / ".sldb")[0] == 0
    rc, output = sldb_cli("notations", "sync", "--spec", config.parent / "lanes.yml", "--store", tmp_path / ".sldb",
                          "--notation", config.parent / "notations" / "flow-own.yml")
    assert rc == 0, output
    doc = _spec_doc(tmp_path)
    assert (doc["category"], doc["nav"], doc["summary"]) == ("Flujos", "Carriles", "Aprobacion")
    assert doc["notation"] == "NotationDoc:flow-own"


def test_view_notation_path_is_relative_to_the_vistas_yml(tmp_path):
    config = _notation_project(tmp_path, "notations/flow-own.yml")
    rc, output = sync(config, tmp_path / ".sldb")
    assert rc == 0, output
    doc = _spec_doc(tmp_path)
    assert doc["notation"] == "NotationDoc:flow-own" and doc["category"] == "Flujos"


def test_view_notation_name_resolves_against_the_store(tmp_path):
    config = _notation_project(tmp_path, "flow-own")
    rc, output = sync(config, tmp_path / ".sldb")
    assert rc == 1 and "UnknownNotationError" in output
    assert not spec_docs(tmp_path / ".sldb")  # nothing written
    assert sldb_cli("notations", "sync", "--notation", config.parent / "notations" / "flow-own.yml", "--store", tmp_path / ".sldb")[0] == 0
    rc, output = sync(config, tmp_path / ".sldb")
    assert rc == 0, output
    assert _spec_doc(tmp_path)["notation"] == "NotationDoc:flow-own"


def test_view_notation_builtin_name_and_absent_field(tmp_path):
    config = _notation_project(tmp_path, "activity")
    assert sync(config, tmp_path / ".sldb")[0] == 0
    assert _spec_doc(tmp_path)["notation"] == "NotationDoc:activity"


@pytest.mark.parametrize("value, error", [
    ("notations/missing.yml", "UnknownNotationError"),
    ("no-such-notation", "UnknownNotationError"),
    ("deployment", "NotationMismatchError"),
])
def test_catalog_validate_and_sync_give_typed_errors(tmp_path, value, error):
    config = _notation_project(tmp_path, value)
    for command in (check, sync):
        rc, output = command(config, tmp_path / ".sldb")
        assert rc == 1 and error in output, (command.__name__, output)
    assert not spec_docs(tmp_path / ".sldb")


def test_catalog_validate_passes(tmp_path):
    config = _notation_project(tmp_path, "notations/flow-own.yml")
    rc, output = check(config, tmp_path / ".sldb")
    assert rc == 0 and "Valid: lanes" in output


def test_a_failing_view_writes_nothing_even_after_valid_ones(tmp_path):
    """IR13b: with one invalid view among valid ones, the catalog sync writes nothing at all."""
    config = _notation_project(tmp_path)
    data = yaml.safe_load(config.read_text(encoding="utf-8"))
    shutil.copy(SPECS / "state.quotation.yml", config.parent / "state.yml")
    data["vistas"].append({"id": "estado", "specs": ["state.yml"], "notation": "activity"})  # wrong type: NotationMismatchError
    config.write_text(yaml.safe_dump(data), encoding="utf-8")
    rc, output = sync(config, tmp_path / ".sldb")
    assert rc == 1 and "NotationMismatchError" in output and "Invalid: estado" in output
    assert not spec_docs(tmp_path / ".sldb")


# --- catalog build cases of tests/test_catalog_resolved_views.py --------------------------------

RESOLVED_NOTATION = {
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


def _resolved_project(tmp_path, view_notation=None):
    root = tmp_path / "repo"
    arch = root / "docs" / "architecture"
    (root / ".git").mkdir(parents=True)
    arch.mkdir(parents=True)
    shutil.copy(SPECS / "deployment.nested.yml", arch / "nested.yml")
    shutil.copy(ARCH_SPECS / "sequence-sync-pipeline.yml", arch / "seq.yml")
    (arch / "seq.mmd").write_text("sequenceDiagram\n  A->>B: hi\n", encoding="utf-8")
    (arch / "nested.mmd").write_text("flowchart TD\n  legacy_src_marker --> x\n", encoding="utf-8")
    (arch / "infra-own.yml").write_text(yaml.safe_dump(RESOLVED_NOTATION, allow_unicode=True), encoding="utf-8")
    vista = {"id": "nested", "title": "Nested", "category": "Infra", "src": "nested.mmd", "specs": ["nested.yml"]}
    if view_notation:
        vista["notation"] = view_notation
    vistas = [vista, {"id": "seq", "title": "Seq", "category": "Flows", "src": "seq.mmd", "specs": ["seq.yml"]}]
    (arch / "vistas.yml").write_text(yaml.safe_dump({"vistas": vistas}), encoding="utf-8")
    return root, arch


def test_catalog_build_draws_graph_views_from_the_view_notation(tmp_path, monkeypatch):
    monkeypatch.setenv("TMPDIR", str(tmp_path / "scratch"))
    (tmp_path / "scratch").mkdir()
    import tempfile
    monkeypatch.setattr(tempfile, "tempdir", None)
    root, arch = _resolved_project(tmp_path, "infra-own.yml")
    page = render_catalog(arch / "vistas.yml")
    assert 'data-resolved-from="SpecDoc:deployment.nested"' in page and 'data-notation="NotationDoc:infra-own"' in page
    assert "legacy_src_marker" not in page and "«database»&lt;br/&gt;Postgres" in page
    # a sequence is not a graph: it keeps its src
    assert "A-&gt;&gt;B: hi" in page and 'data-resolved-from="SpecDoc:sequence' not in page
    assert not list((tmp_path / "scratch").glob("specir-catalog-*"))  # the scratch store is removed


def test_catalog_build_uses_the_builtin_notation_without_the_field(tmp_path):
    root, arch = _resolved_project(tmp_path)
    page = render_catalog(arch / "vistas.yml")
    assert 'data-notation="NotationDoc:deployment"' in page and "«database»" in page


def test_catalog_build_prefers_the_project_store_when_the_spec_is_synced(tmp_path, capsys):
    # a notation that only lives in the project store: the build can only draw it from there
    root, arch = _resolved_project(tmp_path, "infra-own")
    sldb_api.init_store(root)
    page = render_catalog(arch / "vistas.yml")
    assert "legacy_src_marker" in page and "lives only in the store" in capsys.readouterr().err
    assert sldb_cli("notations", "sync", "--notation", arch / "infra-own.yml", "--store", root / ".sldb")[0] == 0
    sync_catalog(SpecSync(root / ".sldb"), arch / "vistas.yml")
    page = render_catalog(arch / "vistas.yml")
    assert 'data-resolved-from="SpecDoc:deployment.nested"' in page and 'data-notation="NotationDoc:infra-own"' in page


def test_catalog_build_falls_back_to_src_when_the_view_does_not_resolve(tmp_path):
    root, arch = _resolved_project(tmp_path)
    data = yaml.safe_load((arch / "vistas.yml").read_text(encoding="utf-8"))
    data["vistas"][0]["specs"] = ["nested.yml", "seq.yml"]  # one spec that is not a graph: the whole view keeps its src
    (arch / "vistas.yml").write_text(yaml.safe_dump(data), encoding="utf-8")
    page = render_catalog(arch / "vistas.yml")
    assert "legacy_src_marker" in page and "data-resolved-from" not in page


# --- tests/test_deskops.py ----------------------------------------------------------------------

def test_parse_atoms_handles_missing_dir(tmp_path):
    assert parse_atoms(tmp_path / "missing") == "{}"


def test_parse_atoms_builds_index_and_skips_bad_files(tmp_path):
    atoms_dir = tmp_path / "atoms"
    atoms_dir.mkdir()
    (atoms_dir / "good.md").write_text("---\ntitle: Architecture\nfive_wh_one_plus: what\nid: atom-1\n---\nBody text.\n", encoding="utf-8")
    (atoms_dir / "bad.md").write_text("---\n: bad yaml\n---\nBroken.\n", encoding="utf-8")
    findings = []
    payload = json.loads(parse_atoms(atoms_dir, findings))
    assert payload["architecture"]["title"] == "Architecture" and "architecture" in payload["architecture"]["aliases"]
    assert payload["architecture"]["atoms"]["what"] == {**payload["architecture"]["atoms"]["what"], "id": "atom-1", "body": "Body text."}
    assert [f.code for f in findings] == ["matching/atom-parse-failed"]


def _sources(base):
    (base / "flow.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (base / "diagram.svg").write_text("<svg><text>Diagram</text></svg>", encoding="utf-8")
    (base / "snippet.html").write_text("plain html snippet", encoding="utf-8")
    (base / "matrix.vega.json").write_text('{"$schema": "https://vega.github.io/schema/vega/v5.json", "marks": []}', encoding="utf-8")
    (base / "deploy.puml").write_text("@startuml\nnode A\n@enduml\n", encoding="utf-8")


def test_render_catalog_renders_mermaid_svg_html_and_notes(tmp_path):
    base = tmp_path
    (base / "template.html").write_text(
        "<html><body><nav>{{NAV}}</nav><main>{{SECTIONS}}</main><script>window.ATOMS_DB = {{ATOMS_DB}};</script></body></html>", encoding="utf-8")
    _sources(base)
    atoms_dir = base / "atoms"
    atoms_dir.mkdir()
    (atoms_dir / "atom.md").write_text("---\ntitle: Runtime\nfive_wh_one_plus: why\n---\nBecause reasons.\n", encoding="utf-8")
    (base / "vistas.yml").write_text("""
template: template.html
vistas:
  - {id: flow, category: Core, title: Flow, lbl: Flow label, desc: Flow desc, src: flow.mmd, specs: [spec-a, spec-b], puml: flow.puml, notes: [gap one, gap two]}
  - {id: picture, category: Core, title: Picture, src: diagram.svg}
  - {id: html-view, category: Extras, title: Html View, src: snippet.html}
  - {id: matrix, category: Extras, title: Matrix, src: matrix.vega.json}
  - {id: deploy, category: Extras, title: Deploy, src: deploy.puml}
""", encoding="utf-8")
    html = render_catalog(base / "vistas.yml", atoms_dir=atoms_dir)
    assert re.search(r'<a href="#flow-[a-f0-9]{8}">Flow label</a>', html)
    assert 'data-spec="spec-a"' in html and 'data-spec="spec-b"' in html and 'data-puml="flow.puml"' in html
    assert '<pre class="mermaid">' in html and '<div class="board puml-board">' in html and "plain html snippet" in html
    assert '<div class="board vega-board">' in html and 'class="vega-spec"' in html and "vega.github.io/schema/vega/v5.json" in html
    assert '<pre class="source-board">@startuml' in html
    assert "Gaps de implementación" in html
    assert "window.ATOMS_DB = {}" in html and "window.ATOMS_BY_VIEW" in html and "window.COVERAGE_BY_VIEW" in html
    assert "because reasons." in html.lower()


def test_render_catalog_injects_atoms_before_body_when_placeholder_missing(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "flow.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (tmp_path / "vistas.yml").write_text("template: template.html\nvistas:\n  - id: flow\n    src: flow.mmd\n", encoding="utf-8")
    html = render_catalog(tmp_path / "vistas.yml", atoms_dir=tmp_path / "missing")
    assert "window.ATOMS_DB = {}" in html and "window.ATOMS_BY_VIEW" in html and "window.COVERAGE_BY_VIEW" in html
    assert html.count("</body>") == 1


def test_coverage_by_view_is_projected_from_the_snapshot_of_the_views_project(tmp_path):
    """test_build_coverage_by_view_projects_snapshot_payload, through the catalog: the snapshot is
    found above the vistas.yml and the view is matched by its `src`."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "view.html").write_text('<section id="d1"><div class="board">x</div></section>', encoding="utf-8")
    (tmp_path / "vistas.yml").write_text("vistas:\n  - {id: view-1, title: View 1, src: docs/view.html#d1, type: component}\n", encoding="utf-8")
    snapshot = tmp_path / ".sldb/runtime/knowledge_graph.kg.json"
    snapshot.parent.mkdir(parents=True)
    element = "diagram_element:view-1:node:runtime"
    snapshot.write_text(json.dumps({"nodes": [
        {"identity": {"node_id": "view:view-1", "node_type": "view"},
         "semantics": {"view_id": "view-1", "diagram_type": "component", "title": "Projected View", "source_ref": "docs/view.html#d1"},
         "edges": [{"target_id": element, "relation_type": "contains", "metadata": {}}]},
        {"identity": {"node_id": element, "node_type": "diagram_element"},
         "semantics": {"view_id": "view-1", "diagram_type": "component", "element_id": "node:runtime", "element_kind": "node", "label": "Runtime"},
         "edges": [{"target_id": "facet:what", "relation_type": "expects_facet", "metadata": {"facet": "what", "source_field": "label"}},
                   {"target_id": "atom:runtime", "relation_type": "covers_facet", "metadata": {
                       "atom_id": "runtime", "facet": "what", "score": 1.0, "match_basis": "title", "evidence": 'label="Runtime" matched atom.title="Runtime"'}}]},
        {"identity": {"node_id": "facet:what", "node_type": "facet"}, "semantics": {"facet": "what"}, "edges": []},
    ]}), encoding="utf-8")
    html = render_catalog(tmp_path / "vistas.yml")
    coverage = json.loads(re.search(r"window\.COVERAGE_BY_VIEW = (\{.*?\}); window\.SPEC2VIZ_ATOM_WARNINGS", html, re.S).group(1))
    (payload,) = coverage.values()
    assert payload["summary"]["elements_fully_covered"] == 1
    assert payload["elements"][0]["covered_facets"][0]["atom_id"] == "runtime" and payload["elements"][0]["missing_facets"] == []
    assert "window.SPEC2VIZ_COVERAGE_WARNINGS = [];" in html


def test_build_catalog_writes_output_file(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "flow.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("template: template.html\nvistas:\n  - id: flow\n    src: flow.mmd\n", encoding="utf-8")
    out = build_catalog(config, tmp_path / "architecture.html")
    assert out.exists() and "graph TD" in out.read_text(encoding="utf-8")


# --- tests/test_atoms_matching.py ---------------------------------------------------------------

HARNESS = """
const norm = (str) => str ? str.trim().toLowerCase().replace(/\\s+/g, ' ') : '';
const getViewAtomsDb = () => DB;
%s
const [db, text, explicit] = JSON.parse(process.argv[1]);
globalThis.DB = db;
globalThis.window = { ATOMS_EXPLICIT: explicit || {} };
const nodeEl = { closest: () => ({ id: 'v1' }) };
const hit = findAtomData(text, nodeEl);
console.log(JSON.stringify(hit ? (hit.explicit ? hit.list.map(a => a.id) : hit.title) : null));
"""


def _match(db: dict, text: str, explicit: dict | None = None):
    block = re.search(r"// <atom-match>.*?// </atom-match>", TEMPLATE.read_text(encoding="utf-8"), re.S)
    assert block, "the template lacks its <atom-match> block"
    out = subprocess.run(["node", "-e", HARNESS % block.group(0), json.dumps([db, text, explicit])], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def _entry(title, aliases=None):
    return {"title": title, "aliases": aliases or [], "atoms": {"what": {"id": "a", "body": "b"}}}


DB = {
    "evaluacion de ordenes": _entry("Evaluación de órdenes", ["evaluacion de ordenes", "evaluacion", "ordenes"]),
    "homologacion de producto": _entry("Homologación de producto", ["homologacion de producto", "homologacion", "producto"]),
}


@needs_node
class TestTemplateMatching:
    def test_one_shared_word_is_not_a_match(self):
        assert _match(DB, "Cerrar producto vencido") is None
        assert _match(DB, "Revisar ordenes") is None

    def test_unrelated_node_has_no_atom(self):
        assert _match(DB, "Enviar correo al cliente") is None

    def test_exact_title_matches_ignoring_accents_punctuation_case(self):
        assert _match(DB, "Evaluación de órdenes") == "Evaluación de órdenes"
        assert _match(DB, "HOMOLOGACION DE PRODUCTO (R1)") == "Homologación de producto"

    def test_phrase_contained_matches(self):
        assert _match(DB, "Paso: homologacion de producto nuevo") == "Homologación de producto"

    def test_two_shared_tokens_matching_most_of_the_alias(self):
        assert _match(DB, "Evaluacion ordenes") == "Evaluación de órdenes"

    def test_explicit_atoms_win_and_all_are_returned(self):
        explicit = {"v1": {"producto": {"title": "producto", "explicit": True, "list": [
            {"id": "a1", "title": "T", "question": "what", "body": "x"}, {"id": "a2", "title": "T", "question": "what", "body": "y"}]}}}
        assert _match(DB, "Producto", explicit) == ["a1", "a2"]

    def test_node_without_explicit_falls_back_to_fuzzy(self):
        explicit = {"v1": {"otro": {"title": "otro", "explicit": True, "list": [{"id": "a1", "title": "T", "question": "what", "body": "x"}]}}}
        assert _match(DB, "Evaluación de órdenes", explicit) == "Evaluación de órdenes"


def _norm_keys(texts: list[str]) -> list[str]:
    """The template's own `normKey` (with its `norm`) over `texts`, run by node."""
    src = TEMPLATE.read_text(encoding="utf-8")
    code = "".join(re.search(rf"    function {name}\(str\) \{{.*?\n    \}}\n", src, re.S).group(0) for name in ("norm", "normKey"))
    out = subprocess.run(["node", "-e", code + "console.log(JSON.stringify(JSON.parse(process.argv[1]).map(normKey)));", json.dumps(texts)],
                         capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


@needs_node
def test_label_key_of_sldb_is_the_template_s_norm_key():
    """sldb's `label_key` (D4) and the template's `normKey` give the same key (SV-G08)."""
    from sldb.api.matching import label_key

    texts = ["Evaluación de órdenes", "  HOMOLOGACION   DE producto (R1) ", "a-b.c/d", "4 Nueva", "Ñandú 2º", ""]
    assert _norm_keys(texts) == [label_key(t) for t in texts]


@needs_node
@pytest.mark.xfail(strict=True, reason="sldb's label_key keeps '_' (\\w) and normKey does not: asked to sldb's desk (matching/label-key-underscore)")
def test_label_key_of_sldb_splits_underscores_like_norm_key():
    """An element without a label is drawn with its id: `post_published` must key the same in both."""
    from sldb.api.matching import label_key

    assert _norm_keys(["post_published"]) == [label_key("post_published")]


def _two_atoms(tmp_path):
    d = tmp_path / "atoms"
    d.mkdir()
    for i, (title, tags) in enumerate([("Uno", ["dominio:oc"]), ("Dos", ["dominio:stock"])]):
        (d / f"a{i}.md").write_text(f"---\ntitle: {title}\nfive_wh_one_plus: what\nid: a{i}\ntags: {json.dumps(tags)}\n---\nCuerpo {i}.\n", encoding="utf-8")
    return d


def test_filter_atoms_payload_by_full_tag_or_value(tmp_path):
    payload = json.loads(parse_atoms(_two_atoms(tmp_path)))
    assert set(filter_atoms_payload(payload, ["dominio:oc"])) == {"uno"}
    assert set(filter_atoms_payload(payload, ["stock"])) == {"dos"}
    assert set(filter_atoms_payload(payload, None)) == {"uno", "dos"}
    assert filter_atoms_payload(payload, ["nada"]) == {}


def test_split_shared_atoms_emits_repeated_payload_once():
    p = {"x": {"title": "X", "atoms": {}}}
    shared, rest = split_shared_atoms({"v1": p, "v2": p, "v3": {}, "v4": {"y": {}}})
    assert shared == p and set(rest) == {"v3", "v4"}
    assert split_shared_atoms({"v1": p}) == ({}, {"v1": p})


def test_catalog_build_embeds_atoms_once_and_honors_atoms_tag(tmp_path):
    atoms = _two_atoms(tmp_path)
    (tmp_path / "f.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    cfg = tmp_path / "vistas.yml"
    cfg.write_text("vistas:\n" + "".join(f"  - id: v{i}\n    title: V{i}\n    src: f.mmd\n    type: mermaid\n" for i in range(3)), encoding="utf-8")
    html = render_catalog(cfg, atoms_dir=atoms)
    assert html.count("Cuerpo 0.") == 1 and html.count("Cuerpo 1.") == 1
    html = render_catalog(cfg, atoms_dir=atoms, atoms_tags=["dominio:oc"])
    assert "Cuerpo 0." in html and "Cuerpo 1." not in html


MD_HARNESS = """
const escapeHtmlUnused = null;
%s
const [body, known] = JSON.parse(process.argv[1]);
console.log(JSON.stringify(renderAtomBody(body, id => known[id] || null)));
"""


def _md(body: str, known: dict | None = None) -> str:
    block = re.search(r"// <atom-md>.*?// </atom-md>", TEMPLATE.read_text(encoding="utf-8"), re.S)
    assert block
    out = subprocess.run(["node", "-e", MD_HARNESS % block.group(0), json.dumps([body, known or {}])], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


@needs_node
class TestAtomMarkdown:
    def test_html_is_escaped(self):
        html = _md('<script>alert(1)</script> & "x"')
        assert "<script>" not in html and "&lt;script&gt;" in html and "&amp;" in html

    def test_inline_formatting(self):
        html = _md("**fuerte** y *suave* y `cod <b>`")
        assert "<strong>fuerte</strong>" in html and "<em>suave</em>" in html and "<code>cod &lt;b&gt;</code>" in html

    def test_paragraphs_breaks_and_lists(self):
        html = _md("uno\ndos\n\n- a\n- b")
        assert "<p>uno<br>dos</p>" in html and "<ul><li>a</li><li>b</li></ul>" in html

    def test_external_link_only_safe_schemes(self):
        assert 'href="https://x.cl/a"' in _md("[t](https://x.cl/a)")
        assert "<a " not in _md("[t](javascript:alert(1))")

    def test_atom_link_present_and_absent(self):
        known = {"a-1": {"id": "a-1", "title": "Plazo <48h>", "question": "what", "body": "x"}}
        html = _md("ver [[a-1]]", known)
        assert 'data-atom-id="a-1"' in html and "Plazo &lt;48h&gt;" in html
        html = _md("ver [[a-9]]", known)
        assert "atom-link-missing" in html and "data-atom-id" not in html and ">a-9<" in html

    def test_predicate_link(self):
        known = {"a-1": {"id": "a-1", "title": "Destino", "question": "what", "body": "x"}}
        html = _md("[depende de:: [[a-1]]]", known)
        assert "<em>depende de</em>: <a" in html and ">Destino</a>" in html


@needs_node
def test_tabs_follow_the_target_atom():
    src = TEMPLATE.read_text(encoding="utf-8")
    block = re.search(r"// <atom-md>.*?// </atom-md>", src, re.S).group(0)
    code = block + """
const target = { id: 't', title: 'Etapa', question: 'what' };
console.log(JSON.stringify([atomTabLabels([target], false), atomTabLabels([{question:'how_not',title:'T'}], true)]));
"""
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True)
    assert json.loads(out.stdout) == [["what"], ["how not · T"]]
    assert "showAtoms([target], false)" in src


# --- build cases of tests/test_explicit_atoms.py ------------------------------------------------

def _atom(d: Path, atom_id: str, title: str, q="what"):
    (d / f"{atom_id}.md").write_text(f"---\ntitle: {title}\nfive_wh_one_plus: {q}\nid: {atom_id}\n---\nCuerpo de {atom_id}.\n", encoding="utf-8")


def _explicit_project(tmp_path, state_atoms_a, state_atoms_b):
    atoms = tmp_path / "atoms"
    atoms.mkdir()
    _atom(atoms, "atom-uno", "Uno")
    _atom(atoms, "atom-dos", "Dos", "why")
    _atom(atoms, "atom-ruido", "Otro tema")
    spec = {
        "id": "ciclo", "title": "Ciclo", "type": "state", "version": "1.0",
        "data": {"entity": "OC", "initial": "nueva", "transitions": [{"from": "nueva", "to": "cerrada", "on": "cierra"}], "states": [
            {"id": "nueva", "label": "4 Nueva", **({"atoms": state_atoms_a} if state_atoms_a is not None else {})},
            {"id": "cerrada", "label": "Cerrada", **({"atoms": state_atoms_b} if state_atoms_b is not None else {})}]},
    }
    (tmp_path / "ciclo.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
    (tmp_path / "f.mmd").write_text("stateDiagram-v2\n  nueva --> cerrada\n", encoding="utf-8")
    (tmp_path / "vistas.yml").write_text("vistas:\n  - id: v1\n    title: V1\n    src: f.mmd\n    type: state\n    specs: [ciclo.yml]\n", encoding="utf-8")
    return atoms


def _explicit(html):
    data = json.loads(re.search(r"window\.ATOMS_EXPLICIT = (\{.*?\}); window\.ATOMS_LINKED", html, re.S).group(1))
    assert len(data) == 1
    return {"v1": next(iter(data.values()))}


def test_build_exposes_explicit_map_by_label_and_id(tmp_path):
    atoms = _explicit_project(tmp_path, ["atom-uno", "atom-dos"], None)
    view = _explicit(render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms))["v1"]
    assert [a["id"] for a in view["4 nueva"]["list"]] == ["atom-uno", "atom-dos"]
    assert [a["id"] for a in view["nueva"]["list"]] == ["atom-uno", "atom-dos"]
    assert "cerrada" not in view


def test_unknown_atom_is_warning_unless_strict(tmp_path, capsys):
    atoms = _explicit_project(tmp_path, ["atom-uno", "no-existe"], None)
    html = render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms)
    warnings = json.loads(re.search(r"SPEC2VIZ_ATOM_WARNINGS = (\[.*?\]);", html).group(1))
    # one per key of the element (its label and its id), as in spec2viz
    assert sorted((w["level"], w["code"], w["subject"].split("#")[1]) for w in warnings) == [
        ("warning", "matching/unknown-atom", "4 nueva"), ("warning", "matching/unknown-atom", "nueva")]
    assert all("no-existe" in w["what"] for w in warnings)
    assert "no-existe" in capsys.readouterr().err
    assert [a["id"] for a in _explicit(html)["v1"]["4 nueva"]["list"]] == ["atom-uno"]
    with pytest.raises(UnknownAtomError, match="no-existe"):
        render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms, strict_atoms=True)


def test_fully_explicit_view_embeds_no_fuzzy_payload(tmp_path):
    atoms = _explicit_project(tmp_path, ["atom-uno"], ["atom-dos"])
    html = render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms)
    assert "Cuerpo de atom-ruido." not in html
    assert "Cuerpo de atom-uno." in html and "Cuerpo de atom-dos." in html


def test_partially_explicit_view_keeps_fuzzy_payload(tmp_path):
    atoms = _explicit_project(tmp_path, ["atom-uno"], None)
    assert "Cuerpo de atom-ruido." in render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms)


def test_atoms_linked_from_explicit_are_embedded_one_level(tmp_path):
    atoms = _explicit_project(tmp_path, ["atom-uno"], ["atom-dos"])
    (atoms / "atom-uno.md").write_text("---\ntitle: Uno\nfive_wh_one_plus: what\nid: atom-uno\n---\nVer [depende:: [[atom-ruido]]] y [[atom-lejano]].\n", encoding="utf-8")
    _atom(atoms, "atom-lejano", "Lejano")
    (atoms / "atom-ruido.md").write_text("---\ntitle: Otro tema\nfive_wh_one_plus: what\nid: atom-ruido\n---\nSigue [[atom-lejano2]].\n", encoding="utf-8")
    _atom(atoms, "atom-lejano2", "Nivel dos")
    html = render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms)
    linked = json.loads(re.search(r"window\.ATOMS_LINKED = (\{.*?\}); window\.REFS_EXPLICIT", html, re.S).group(1))
    assert set(linked) == {"atom-ruido", "atom-lejano"}


# --- build cases of tests/test_cli.py -----------------------------------------------------------

def _simple(tmp_path, template="<html><body>{{NAV}}{{SECTIONS}}</body></html>"):
    (tmp_path / "template.html").write_text(template, encoding="utf-8")
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("template: template.html\nvistas:\n  - id: sample\n    src: view.mmd\n", encoding="utf-8")
    return config


def test_catalog_build_alias_matches_legacy_build(tmp_path):
    """The `build` alias is IR13d's; on the API, building twice gives the same page."""
    config = _simple(tmp_path, "<html><body>{{NAV}}{{FILTERS}}{{SECTIONS}}</body></html>")
    legacy = build_catalog(config, tmp_path / "legacy.html")
    grouped = build_catalog(config, tmp_path / "grouped.html")
    assert legacy.read_text(encoding="utf-8") == grouped.read_text(encoding="utf-8")


def test_build_command(tmp_path):
    out = build_catalog(_simple(tmp_path), tmp_path / "out.html")
    assert out.exists() and "catalog-search" in out.read_text(encoding="utf-8")


COMPONENT_SPEC = "id: spec-component\ntitle: Example\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n"
LOCAL_TEMPLATE = "<html><head><title>{{CATALOG_TITLE}}</title></head><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>"


def test_build_command_supports_store_of_stores(tmp_path):
    child = tmp_path / "child"
    child.mkdir()
    (tmp_path / "template.html").write_text(LOCAL_TEMPLATE, encoding="utf-8")
    (child / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (child / "spec-component.yml").write_text(COMPONENT_SPEC, encoding="utf-8")
    (child / "vistas.yml").write_text("template: unused.html\nvistas:\n  - id: sample\n    category: Arquitectura\n    title: Sample Diagram\n"
                                      "    nav: Sample\n    desc: Demo child vista\n    src: view.mmd\n    specs:\n      - spec-component\n", encoding="utf-8")
    (tmp_path / "catalog.yml").write_text("template: template.html\ntitle: Repo Catalog\nbrand_name: Diagram Catalog\nstores:\n"
                                          "  - path: child/vistas.yml\n    project: demo/project\n    tags:\n      - domain:crm\n", encoding="utf-8")
    html = build_catalog(tmp_path / "catalog.yml", tmp_path / "out.html").read_text(encoding="utf-8")
    for text in ("Repo Catalog", "Diagram Catalog", "catalog-search", 'data-project="demo/project"', 'data-type="component"', "domain:crm", "Sample Diagram"):
        assert text in html, text


def test_build_command_supports_brand_subtitle_in_builtin_template(tmp_path):
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (tmp_path / "spec-component.yml").write_text(COMPONENT_SPEC, encoding="utf-8")
    (tmp_path / "catalog.yml").write_text(
        "template: missing-template.html\ntitle: Repo Catalog\nbrand_name: Diagram Catalog\nbrand_subtitle: Repo subtitle from config\nvistas:\n"
        "  - id: sample\n    category: Arquitectura\n    title: Sample Diagram\n    src: view.mmd\n    specs:\n      - spec-component.yml\n", encoding="utf-8")
    html = build_catalog(tmp_path / "catalog.yml", tmp_path / "out.html").read_text(encoding="utf-8")
    assert "Repo subtitle from config" in html and "Visor transversal de diagramas de spec2viz" not in html


def test_build_command_warns_on_local_template_override(tmp_path, capsys):
    (tmp_path / "template.html").write_text(LOCAL_TEMPLATE, encoding="utf-8")
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (tmp_path / "spec-component.yml").write_text(COMPONENT_SPEC, encoding="utf-8")
    (tmp_path / "catalog.yml").write_text("template: template.html\nvistas:\n  - id: sample\n    category: Arquitectura\n    title: Sample Diagram\n"
                                          "    src: view.mmd\n    specs:\n      - spec-component.yml\n", encoding="utf-8")
    build_catalog(tmp_path / "catalog.yml", tmp_path / "out.html")
    assert "using local catalog template override" in capsys.readouterr().err


def test_build_command_supports_project_yml_envelope(tmp_path):
    child = tmp_path / "child"
    child.mkdir()
    (tmp_path / "template.html").write_text(LOCAL_TEMPLATE, encoding="utf-8")
    (child / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (child / "spec-state.yml").write_text(
        "id: spec-state\ntitle: Example State\ntype: state\nversion: '1.0'\ndata:\n  entity: X\n  initial: a\n  states:\n    - id: a\n      label: A\n  transitions: []\n",
        encoding="utf-8")
    (child / "vistas.yml").write_text("template: ../template.html\nvistas:\n  - id: sample-state\n    category: Estados\n    title: State Diagram\n"
                                      "    nav: State\n    desc: Demo leaf\n    src: view.mmd\n    specs:\n      - spec-state.yml\n", encoding="utf-8")
    (tmp_path / "project.yml").write_text(
        "diagram_store:\n  kind: diagram-store\n  template: template.html\n  title: Project Catalog\n  brand_name: Project Brand\n"
        "  project_name: project/demo\n  stores:\n    - path: child/vistas.yml\n      project: project/demo\n      tags:\n        - domain:workflow\n",
        encoding="utf-8")
    html = build_catalog(tmp_path / "project.yml", tmp_path / "out.html").read_text(encoding="utf-8")
    for text in ("Project Catalog", "Project Brand", "project/demo", "domain:workflow", 'data-type="state"'):
        assert text in html, text


def test_build_command_extracts_types_from_specs_dir_and_makes_anchor_ids_unique(tmp_path):
    (tmp_path / "template.html").write_text("<html><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>", encoding="utf-8")
    for folder in [tmp_path / "alpha" / "docs" / "vistas", tmp_path / "beta" / "docs" / "vistas"]:
        folder.mkdir(parents=True)
        project = folder.parent.parent
        (project / "project.yaml").write_text("project_name: Demo\nclient: sample\n", encoding="utf-8")
        (project / "specs").mkdir(exist_ok=True)
        (project / "specs" / "same-view.yml").write_text(COMPONENT_SPEC.replace("spec-component", "same-view"), encoding="utf-8")
        (project / "rendered").mkdir(exist_ok=True)
        (project / "rendered" / "same-view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
        (folder / "vistas.yml").write_text("template: template.html\nvistas:\n  - id: vista01\n    title: Demo\n    category: Arquitectura\n"
                                           "    specs:\n      - same-view\n    mmd: ../../rendered/same-view.mmd\n", encoding="utf-8")
    (tmp_path / "catalog.yml").write_text("template: template.html\nstores:\n  - path: alpha/docs/vistas/vistas.yml\n  - path: beta/docs/vistas/vistas.yml\n", encoding="utf-8")
    html = build_catalog(tmp_path / "catalog.yml", tmp_path / "out.html").read_text(encoding="utf-8")
    assert html.count('data-type="component"') == 2
    assert len(set(re.findall(r'id="(sample-demo-vista01-[a-f0-9]{8})"', html))) == 2


def test_build_command_extracts_html_section_fragments(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{FILTERS}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "bundle.html").write_text(
        "<html><body><section id=\"d1\"><div class=\"board\"><pre class=\"mermaid\">graph TD\\nA-->B</pre></div></section></body></html>", encoding="utf-8")
    (tmp_path / "catalog.yml").write_text(
        "template: template.html\nitems:\n  - id: frag\n    title: Fragment\n    src: bundle.html#d1\n    type: component\n    category: Arquitectura\n", encoding="utf-8")
    html = build_catalog(tmp_path / "catalog.yml", tmp_path / "out.html").read_text(encoding="utf-8")
    assert "bundle.html#d1" not in html
    assert '<div class="board"><pre class="mermaid">graph TD\\nA-->B</pre></div>' in html


def test_build_command_reports_errors(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("template: template.html\nvistas: [\n  {id: broken, src: missing.mmd}\n]\n", encoding="utf-8")
    with pytest.raises(FileNotFoundError, match="missing.mmd"):
        build_catalog(config, tmp_path / "out.html")
    assert not (tmp_path / "out.html").exists()


# --- the built page opens without missing resources (IR13b) -------------------------------------

FIXTURE_TREE = HERE / "fixtures" / "catalog"


def fixture_repo(tmp_path: Path) -> Path:
    """spec2viz's catalog fixtures (its `docs/architecture/` and `examples/catalog/`) in a repo of their own."""
    root = tmp_path / "spec2viz-repo"
    shutil.copytree(FIXTURE_TREE, root)
    (root / ".git").mkdir()
    return root


@pytest.mark.parametrize("config", ["docs/architecture/vistas.yml", "examples/catalog/project.yml"])
def test_the_built_catalog_opens_without_missing_resources(tmp_path, config):
    root = fixture_repo(tmp_path)
    page = build_catalog(root / config, tmp_path / "catalog.html").read_text(encoding="utf-8")
    ids = set(re.findall(r'\sid="([^"]+)"', page))
    for kind, ref in re.findall(r'\s(src|href)="([^"$]*)"', page):
        if ref.startswith("https://") or ref == "#":
            continue
        assert ref.startswith("#") and ref[1:] in ids, (kind, ref)  # nothing next to the page is needed
    assert '<div class="nav-category">' in page and '<div class="catalog-toolbar">' in page and "window.ATOMS_BY_VIEW" in page
    sections = re.findall(r'<section id="([^"]+)"', page)
    assert sections and all(f'href="#{anchor}"' in page for anchor in sections)
