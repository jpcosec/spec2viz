"""Spec synchronization to the store and component spec generation (IR13a): specIR uses sldb's.

specIR defines no SpecSync and no spec generator: syncing a spec is `sldb.api.notations.SpecSync`
(or `sync_spec`, or `sldb notations sync --spec`, D1) and generating a component spec is
`component_spec_from_graph` / `component_spec_from_python` / `write_component_spec` (or
`sldb notations from-graph`, D2), called directly. sldb carries its own ported tests for both; these
are the checks it does not have:

- on a real sldb store (always): resyncing after removing an element deletes its SpecNodeDoc and
  RelationDoc; a non-builtin relation creates its RelationTypeDoc and the edge index validates;
  a component spec compiled from a store's edge index and one generated from specIR's own package
  validate with the spec models of D3.
- parity with spec2viz as the oracle (`parity` marker; what spec2viz answered at revision 2de1056 is
  frozen in `goldens/spec2viz-2de1056-oracle.json`, see `oracle.py`):
  the same SpecDoc, SpecNodeDoc, RelationDoc, RelationTypeDoc and notation documents and the same
  sync reports over spec2viz's sync fixtures (its `tests/fixtures/*.yml`, copied in IR11's corpus,
  and the ARQ/FLOW specs of its `tests/test_sldb_sync.py`); the same component spec from its
  graph-import snapshots (`tests/test_graph_import.py`) and from a store's edge index; and from the
  Python AST of specIR's package, the same spec up to the differences the coverage matrix declares
  for SV-F02.

Declared differences (docs/spec2viz/matriz-de-cobertura.md, SV-E01 and SV-F02):
- SV-E01: the description of a RelationTypeDoc created by the sync no longer ends in " de spec2viz".
- SV-F02: sldb reads imports from `sldb.code.scan_tree`, so `imports` edges count plain `import x`
  statements, resolve relative imports against the module's package and are not repeated per
  statement; `from x import y` statements nested below the module's top level (inside functions,
  `if`, `try`) are not read (asked to sldb's desk). Modules, classes and `defines` are identical."""

from __future__ import annotations

import ast
import json
import shutil
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml
import sldb.api as sldb_api
from sldb.api.notations import (
    SpecSync,
    component_spec_from_graph,
    component_spec_from_python,
    index_graph,
    load_node_link,
    load_node_link_graph,
    load_spec,
    validate_spec,
    write_component_spec,
)

from parity import CORPUS, FIXTURES, goldens

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oracle  # noqa: E402

PACKAGE = Path(__file__).resolve().parents[2] / "src" / "specir"
#: spec2viz's sync fixtures: its `tests/fixtures/*.yml` that validate (IR11's corpus keeps them).
SYNC_FIXTURES = [rel for rel in CORPUS if rel.startswith("tests/fixtures/") and goldens()[rel]["error"] is None]
#: The documents a spec sync writes (the spec, its elements and edges, relation types, notation).
MODELS = ("SpecDoc", "SpecNodeDoc", "RelationDoc", "RelationTypeDoc", "NotationDoc", "GlyphDoc", "LinkDoc")
REPORT_FIELDS = ("spec_id", "created", "updated", "deleted", "relation_types_added", "unresolved", "edge_errors")
#: SV-E01's declared difference: spec2viz signs the RelationTypeDoc descriptions it writes.
SPEC2VIZ_SIGNATURE = " de spec2viz."
KINDS = "tests/fixtures/component.kinds.yml"


# --- helpers ------------------------------------------------------------------------------------

def _project(root: Path, rels: list[str]) -> Path:
    """A real sldb store at `root` with the given corpus specs copied under `specs/`."""
    root.mkdir(parents=True)
    sldb_api.init_store(root)
    for rel in rels:
        target = root / "specs" / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURES / rel, target)
    return root


def _documents(root: Path) -> dict[str, tuple[str, dict[str, Any]]]:
    """Every synced document of the store, by export id: its path and its payload (no provenance)."""
    store = root / ".sldb"
    found: dict[str, tuple[str, dict[str, Any]]] = {}
    for model in MODELS:
        for row in sldb_api.select_documents(store, {"model": model}):
            found[row["export_id"]] = (row["path"], sldb_api.extract_document_payload(store, None, f"{model}/{row['name']}"))
    return found


def _report(report: Any) -> dict[str, Any]:
    return {field: getattr(report, field) if isinstance(getattr(report, field), str) else sorted(getattr(report, field)) for field in REPORT_FIELDS}


def _unsigned(documents: dict[str, Any]) -> dict[str, Any]:
    """spec2viz's documents with SV-E01's declared difference taken out."""
    out = {}
    for ref, (path, payload) in documents.items():
        if ref.startswith("RelationTypeDoc:") and payload.get("description", "").endswith(SPEC2VIZ_SIGNATURE):
            payload = {**payload, "description": payload["description"].removesuffix(SPEC2VIZ_SIGNATURE) + "."}
        out[ref] = [path, payload]
    return out


def _sync_ours(tmp_path: Path, rels: list[str], write=None) -> tuple[list, Path]:
    """Sync `rels` in order with sldb into a fresh store: the reports and the repo."""
    root = _project(tmp_path / "sldb", [] if write else rels)
    if write:
        write(root)
    sync = SpecSync(root / ".sldb")
    return [_report(sync.sync(root / "specs" / rel)) for rel in rels], root


def _assert_same_store(ours: Path, oracle_documents: dict) -> None:
    """`ours`' documents are the ones spec2viz left (its answer, in the golden), SV-E01 aside."""
    found, expected = oracle.plain(_documents(ours)), _unsigned(oracle_documents)
    assert sorted(found) == sorted(expected)
    differing = {ref: (found[ref], expected[ref]) for ref in found if found[ref] != expected[ref]}
    assert not differing, differing


def _validated(spec: dict, path: Path) -> None:
    write_component_spec(spec, path)
    validate_spec(load_spec(path))


# --- on a real sldb store -----------------------------------------------------------------------

def test_resync_deletes_the_spec_node_and_relations_of_a_removed_element(tmp_path: Path) -> None:
    root = _project(tmp_path / "p", [KINDS])
    spec_path = root / "specs" / KINDS
    sync = SpecSync(root / ".sldb")
    sync.sync(spec_path)
    store = root / ".sldb"
    assert sldb_api.doc_exists(store, "SpecNodeDoc/component.kinds.db")
    assert sldb_api.doc_exists(store, "RelationDoc/component.kinds.02-api__reads__db")

    data = yaml.safe_load(spec_path.read_text(encoding="utf-8"))
    del data["data"]["nodes"]["db"]
    data["data"]["edges"] = [edge for edge in data["data"]["edges"] if "db" not in (edge["from"], edge["to"])]
    spec_path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    report = sync.sync(spec_path)

    assert sorted(report.deleted) == ["RelationDoc:component.kinds.02-api__reads__db", "SpecNodeDoc:component.kinds.db"]
    assert not sldb_api.doc_exists(store, "SpecNodeDoc/component.kinds.db")
    assert not sldb_api.doc_exists(store, "RelationDoc/component.kinds.02-api__reads__db")
    assert sldb_api.doc_exists(store, "RelationDoc/component.kinds.01-web__calls__api")


def test_a_non_builtin_relation_creates_its_type_and_the_edge_index_validates(tmp_path: Path) -> None:
    root = _project(tmp_path / "p", [KINDS])
    report = SpecSync(root / ".sldb").sync(root / "specs" / KINDS)
    assert report.relation_types_added == ["calls", "reads"]
    assert sldb_api.doc_exists(root / ".sldb", "RelationTypeDoc/reltype-calls")
    check = sldb_api.check_edges(root / ".sldb")
    assert (check.errors, check.stale) == ([], []), check
    relations = {(r.source.rsplit(":", 1)[-1], r.relation, r.target.rsplit(":", 1)[-1]) for r in sldb_api.load_edge_index(root / ".sldb").edges}
    assert ("component.kinds.web", "calls", "component.kinds.api") in relations


def test_a_component_spec_from_a_store_graph_validates(tmp_path: Path) -> None:
    root = _project(tmp_path / "p", [KINDS])
    SpecSync(root / ".sldb").sync(root / "specs" / KINDS)
    nodes, edges = index_graph(sldb_api.load_edge_index(root / ".sldb"))
    spec = component_spec_from_graph(nodes, edges, node_types=("document",), models=("SpecNodeDoc",), relations=("calls", "reads"), source="store")
    labels = {key: node["label"].removeprefix("component.kinds.") for key, node in spec["data"]["nodes"].items()}
    assert sorted(labels.values()) == ["api", "db", "web"]
    assert [(labels[e["from"]], e["relation"], labels[e["to"]]) for e in spec["data"]["edges"]] == [("web", "calls", "api"), ("api", "reads", "db")]
    _validated(spec, tmp_path / "graph.yml")


def test_a_component_spec_from_specir_python_ast_validates(tmp_path: Path) -> None:
    spec, findings = component_spec_from_python(PACKAGE, project_id="specir", title="specIR")
    assert findings == [] and spec is not None
    modules = {node["label"] for node in spec["data"]["nodes"].values() if node["kind"] == "module"}
    assert {"install", "mcp_extension", "visual.commands", "visual.compilers.component"} <= modules
    _validated(spec, tmp_path / "specir.yml")


# --- parity with spec2viz -----------------------------------------------------------------------

@pytest.mark.parity
@pytest.mark.parametrize("rel", SYNC_FIXTURES)
def test_sync_of_a_spec2viz_fixture_matches_spec2viz(tmp_path: Path, rel: str) -> None:
    ours, our_root = _sync_ours(tmp_path, [rel])
    oracle_reports, oracle_documents = oracle.expect("sync", tmp_path / "spec2viz", [rel], roots=(tmp_path,))
    assert oracle.plain(ours) == oracle_reports
    _assert_same_store(our_root, oracle_documents)


@pytest.mark.parity
def test_sync_and_resync_of_the_spec2viz_sync_specs_match_spec2viz(tmp_path: Path) -> None:
    arq, flow = (oracle.frozen("sync_specs")[name] for name in ("ARQ", "FLOW"))  # spec2viz's tests/test_sldb_sync.py
    reduced = json.loads(json.dumps(arq))
    del reduced["data"]["nodes"]["renderers"]
    reduced["data"]["edges"] = [edge for edge in reduced["data"]["edges"] if edge["to"] != "renderers"]

    def write(root: Path) -> None:
        (root / "specs").mkdir()
        for spec in (arq, flow):
            (root / "specs" / f"{spec['id']}.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
        (root / "specs" / "arq-reduced.yml").write_text(yaml.safe_dump(reduced), encoding="utf-8")

    rels = ["arq.yml", "flow.yml", "arq-reduced.yml"]
    ours, our_root = _sync_ours(tmp_path, rels, write)
    oracle_reports, oracle_documents = oracle.expect("sync", tmp_path / "spec2viz", rels, write, roots=(tmp_path,))
    assert oracle.plain(ours) == oracle_reports
    assert sorted(ours[2]["deleted"]) == ["RelationDoc:arq.02-core__loads_path__renderers", "SpecNodeDoc:arq.renderers"]
    _assert_same_store(our_root, oracle_documents)


@pytest.mark.parity
def test_graph_import_of_the_spec2viz_snapshots_matches_spec2viz(tmp_path: Path) -> None:
    inputs = oracle.frozen("graph_import_inputs")  # spec2viz's tests/test_graph_import.py: _node_link and PY_GRAPH
    snapshot = tmp_path / "snap.json"
    snapshot.write_text(json.dumps(inputs["snapshot"]), encoding="utf-8")
    cases = [
        {"models": ("AtomDoc",)},
        {"node_types": ("document", "semantic_tag"), "relations": ("tagged_as",), "drop_isolated": True, "spec_id": "tags", "title": "Tags"},
        {"relations": ("has_document",)},
        {},
    ]
    expected = oracle.expect("graph_import", snapshot, f"snapshot {snapshot}", cases, roots=(tmp_path,))
    assert oracle.scrub(load_node_link(snapshot), tmp_path) == expected["loaded"]
    nodes, edges = load_node_link(snapshot)
    for index, options in enumerate(cases):
        spec = component_spec_from_graph(nodes, edges, source=f"snapshot {snapshot}", **options)
        assert oracle.scrub(spec, tmp_path) == expected["specs"][index], options
        _validated(spec, tmp_path / f"snap-{index}.yml")

    python_graph = tmp_path / "python-source.graph.json"
    python_graph.write_text(json.dumps(inputs["py_graph"]), encoding="utf-8")
    loaded = load_node_link_graph(python_graph)
    cases = [{"node_types": ("python_module", "python_symbol", "python_external"), "attrs": loaded[2], "module_prefixes": prefixes}
             for prefixes in (("sldb.selfdoc",), None)]
    expected = oracle.expect("graph_import_python", python_graph, cases, roots=(tmp_path,))
    assert oracle.scrub(loaded, tmp_path) == expected["loaded"]
    for index, options in enumerate(cases):
        spec = component_spec_from_graph(loaded[0], loaded[1], **options)
        assert oracle.scrub(spec, tmp_path) == expected["specs"][index], options["module_prefixes"]
        _validated(spec, tmp_path / f"python-{index}.yml")


@pytest.mark.parity
def test_graph_import_of_a_store_edge_index_matches_spec2viz(tmp_path: Path) -> None:
    root = _project(tmp_path / "p", SYNC_FIXTURES[:4])
    sync = SpecSync(root / ".sldb")
    for rel in SYNC_FIXTURES[:4]:
        sync.sync(root / "specs" / rel)
    nodes, edges = index_graph(sldb_api.load_edge_index(root / ".sldb"))
    cases = [{}, {"models": ("SpecNodeDoc",), "drop_isolated": True}, {"exclude_relations": ("contains",)}]
    expected = oracle.expect("graph_import_store", root, f"store {root}", cases, roots=(tmp_path,))
    assert oracle.scrub((nodes, edges), tmp_path) == expected["index"]
    for index, options in enumerate(cases):
        spec = component_spec_from_graph(nodes, edges, source=f"store {root}", **options)
        assert oracle.scrub(spec, tmp_path) == expected["specs"][index], options


def _imports_sldb_does_not_read(package: Path) -> tuple[set, set]:
    """The two sides of SV-F02's declared difference, read from the package's own source:
    (edges only sldb may add: plain imports and resolved relative imports;
     edges only spec2viz may add: nested `from` imports and unresolved relative ones)."""
    def node(module: str) -> str:
        return "module_" + module.replace(".", "_").replace("-", "_")

    sldb_only, spec2viz_only = set(), set()
    for path in sorted(package.rglob("*.py")):
        if path.name == "__init__.py":
            continue
        module = str(path.relative_to(package).with_suffix("")).replace("/", ".")
        tree = ast.parse(path.read_text(encoding="utf-8"))
        top = {id(statement) for statement in tree.body}
        for statement in ast.walk(tree):
            if isinstance(statement, ast.Import) and id(statement) in top:
                sldb_only |= {(node(module), node(alias.name)) for alias in statement.names}
            elif isinstance(statement, ast.ImportFrom) and statement.level:
                base = module.split(".")[: -statement.level] + ([statement.module] if statement.module else [])
                sldb_only.add((node(module), node(".".join(base))))
                if statement.module:
                    spec2viz_only.add((node(module), node(statement.module)))
            elif isinstance(statement, ast.ImportFrom) and id(statement) not in top:
                spec2viz_only.add((node(module), node(statement.module)))
    return sldb_only, spec2viz_only


@pytest.mark.parity
def test_python_ast_generation_of_specir_matches_spec2viz_up_to_the_declared_differences(tmp_path: Path) -> None:
    # spec2viz's answer is over a frozen copy of specIR's package (the golden holds its sources),
    # so the comparison does not move with `src/`.
    package = tmp_path / "specir"
    for rel, text in oracle.frozen("python_ast_package").items():
        (package / rel).parent.mkdir(parents=True, exist_ok=True)
        (package / rel).write_text(text, encoding="utf-8")
    expected = oracle.expect("python_ast", package, roots=(tmp_path,))

    ours, findings = component_spec_from_python(package, project_id="specir", title="specIR")
    ours = oracle.scrub(ours, tmp_path)
    assert findings == []
    assert {k: v for k, v in ours.items() if k != "data"} == {k: v for k, v in expected.items() if k != "data"}

    def internal(spec: dict) -> list:
        return [(key, node) for key, node in spec["data"]["nodes"].items() if node["kind"] != "external"]

    def edges(spec: dict, relation: str) -> list:
        return [(edge["from"], edge["to"]) for edge in spec["data"]["edges"] if edge["relation"] == relation]

    assert internal(ours) == internal(expected)
    assert edges(ours, "defines") == edges(expected, "defines")
    our_imports, expected_imports = edges(ours, "imports"), edges(expected, "imports")
    assert len(our_imports) == len(set(our_imports)), "sldb repeats an imports edge"
    sldb_only, spec2viz_only = _imports_sldb_does_not_read(package)
    assert set(our_imports) - set(expected_imports) <= sldb_only
    assert set(expected_imports) - set(our_imports) <= spec2viz_only
