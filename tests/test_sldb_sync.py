"""`spec2viz diagram sync`: el spec como namespace sobre el store sldb (SpecDoc, SpecNodeDoc, RelationDoc)."""
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from spec2viz.cli import main
from spec2viz.deskops import SldbAtomResolver
from spec2viz.sldb_sync import SpecSync, find_store, relation_token, spec_edges, spec_elements, to_slash_ref

sldb_api = pytest.importorskip("sldb.api")

ARQ = {
    "id": "arq", "title": "Arq", "type": "component", "version": "1.0", "metadata": {"description": "demo"},
    "data": {
        "nodes": {
            "cli": {"label": "CLI", "kind": "entry", "contains": ["core"]},
            "core": {"label": "Core"},
            "renderers": {"label": "Renderer Dispatch", "atoms": ["atom-nope"]},
        },
        "edges": [
            {"from": "cli", "to": "core", "relation": "uses"},
            {"from": "core", "to": "renderers", "relation": "loads(path)", "label": "x"},
        ],
    },
}
FLOW = {
    "id": "flow", "title": "Flow", "type": "state", "version": "1.0",
    "data": {
        "entity": "Job", "initial": "a",
        "states": [{"id": "a", "label": "A", "refs": ["SpecNodeDoc:arq.core"]}, {"id": "b", "label": "B"}],
        "transitions": [{"from": "a", "to": "b", "on": "go"}],
    },
}


@pytest.fixture
def project(tmp_path):
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "arq.yml").write_text(yaml.safe_dump(ARQ), encoding="utf-8")
    (tmp_path / "docs" / "flow.yml").write_text(yaml.safe_dump(FLOW), encoding="utf-8")
    return tmp_path


def _rels(records, attr):
    return sorted((r.relation, getattr(r, attr).removeprefix("sldb://document/")) for r in records
                  if r.relation in ("uses", "loads_path", "transitions_to", "references", "contains"))


# --- puro ---------------------------------------------------------------------------

def test_pure_extraction_and_tokens():
    assert [e["id"] for e in spec_elements(ARQ)] == ["cli", "core", "renderers"]
    assert spec_elements(ARQ)[0]["contains"] == ["core"] and spec_elements(ARQ)[2]["atoms"] == ["atom-nope"]
    assert spec_edges(ARQ) == [
        {"from": "cli", "to": "core", "relation": "uses", "label": ""},
        {"from": "core", "to": "renderers", "relation": "loads_path", "label": "x"},
    ]
    assert spec_edges(FLOW) == [{"from": "a", "to": "b", "relation": "transitions_to", "label": "go"}]
    assert relation_token(" Depends-On ", "x") == "depends_on" and relation_token("", "uses") == "uses"
    assert to_slash_ref("AtomDoc:atom-a") == "AtomDoc/atom-a" and to_slash_ref("desk:TaskDoc:t") == "desk:TaskDoc/t"


# --- contra un store real -----------------------------------------------------------

def test_sync_writes_spec_nodes_and_edges(project):
    store = project / ".sldb"
    report = SpecSync(store).sync(project / "docs" / "arq.yml")

    assert sorted(report.created) == sorted([
        "SpecDoc:arq", "SpecNodeDoc:arq.cli", "SpecNodeDoc:arq.core", "SpecNodeDoc:arq.renderers",
        "RelationDoc:arq.cli__uses__core", "RelationDoc:arq.core__loads_path__renderers",
    ])
    assert report.relation_types_added == ["loads_path", "uses"]
    assert report.unresolved == ["arq.renderers: 'AtomDoc:atom-nope' no existe en el store"]
    assert report.edge_errors == []

    out = project / "docs" / "sldb" / "arq"
    assert (out / "arq.md").exists() and (out / "nodes" / "arq.cli.md").exists() and (out / "edges" / "arq.cli__uses__core.md").exists()
    assert (project / "sldb" / "relation_types" / "loads_path.md").exists()
    assert sldb_api.doc_exists(store, "SpecNodeDoc/arq.renderers") and sldb_api.doc_exists(store, "RelationTypeDoc/reltype-uses")

    node = yaml.safe_load((out / "nodes" / "arq.cli.md").read_text(encoding="utf-8").split("---")[1])
    assert node == {"id": "arq.cli", "spec": "SpecDoc:arq", "element": "cli", "kind": "entry", "refs": [], "atom_refs": [], "contains": ["SpecNodeDoc:arq.core"], "data": {}}
    spec_doc = yaml.safe_load((out / "arq.md").read_text(encoding="utf-8").split("---")[1])
    assert spec_doc["spec_path"] == "docs/arq.yml" and len(spec_doc["sha256"]) == 64
    assert spec_doc["notation"] == ""  # component no tiene notacion builtin
    assert spec_doc["nodes"] == ["SpecNodeDoc:arq.cli", "SpecNodeDoc:arq.core", "SpecNodeDoc:arq.renderers"]

    assert _rels(sldb_api.edges_from(store, "SpecNodeDoc:arq.cli"), "target") == [
        ("contains", "SpecNodeDoc:arq.core"), ("references", "SpecDoc:arq"), ("uses", "SpecNodeDoc:arq.core"),
    ]
    assert ("loads_path", "SpecNodeDoc:arq.renderers") in _rels(sldb_api.edges_from(store, "SpecNodeDoc:arq.core"), "target")


def test_refs_across_specs_show_up_as_edges_the_catalog_reads(project):
    store = project / ".sldb"
    sync = SpecSync(store)
    sync.sync(project / "docs" / "arq.yml")
    report = sync.sync(project / "docs" / "flow.yml")
    assert report.unresolved == [] and report.edge_errors == []
    assert report.notation == "NotationDoc:statechart" and "NotationDoc:statechart" in report.created
    assert "GlyphDoc:statechart.state" in report.created and "LinkDoc:statechart.transition" in report.created
    flow_doc = yaml.safe_load((project / "docs" / "sldb" / "flow" / "flow.md").read_text(encoding="utf-8").split("---")[1])
    assert flow_doc["notation"] == "NotationDoc:statechart"
    assert ("references", "NotationDoc:statechart") in _rels(sldb_api.edges_from(store, "SpecDoc:flow"), "target")
    state_a = yaml.safe_load((project / "docs" / "sldb" / "flow" / "nodes" / "flow.a.md").read_text(encoding="utf-8").split("---")[1])
    assert state_a["data"] == {"initial": True}
    transition = (project / "docs" / "sldb" / "flow" / "edges" / "flow.a__transitions_to__b.md").read_text(encoding="utf-8")
    assert "go" in transition  # el evento viaja en `notes` del RelationDoc

    assert ("references", "SpecNodeDoc:flow.a") in _rels(sldb_api.edges_to(store, "SpecNodeDoc:arq.core"), "source")
    edges = SldbAtomResolver().edges_of(store, "SpecNodeDoc:arq.core")
    assert {"relation": "references", "direction": "in", "node": "sldb://document/SpecNodeDoc:flow.a", "ref": "SpecNodeDoc:flow.a", "title": "A"} in edges
    assert all(e["relation"] not in ("has_section", "tagged_as", "has_document") for e in edges)


def test_resync_is_idempotent_and_deletes_what_left_the_spec(project):
    store = project / ".sldb"
    sync = SpecSync(store)
    sync.sync(project / "docs" / "arq.yml")
    again = sync.sync(project / "docs" / "arq.yml")
    assert again.created == [] and len(again.updated) == 6 and again.deleted == [] and again.relation_types_added == []

    smaller = yaml.safe_load(yaml.safe_dump(ARQ))
    smaller["data"]["nodes"].pop("renderers")
    smaller["data"]["edges"].pop()
    (project / "docs" / "arq.yml").write_text(yaml.safe_dump(smaller), encoding="utf-8")
    report = SpecSync(store).sync(project / "docs" / "arq.yml")
    assert sorted(report.deleted) == ["RelationDoc:arq.core__loads_path__renderers", "SpecNodeDoc:arq.renderers"]
    assert not sldb_api.doc_exists(store, "SpecNodeDoc/arq.renderers")
    assert not (project / "docs" / "sldb" / "arq" / "nodes" / "arq.renderers.md").exists()
    assert report.edge_errors == [] and report.unresolved == []


def test_invalid_spec_touches_nothing(project):
    (project / "docs" / "bad.yml").write_text("id: bad\ntitle: Bad\ntype: component\nversion: '1'\n", encoding="utf-8")
    with pytest.raises(Exception):
        SpecSync(project / ".sldb").sync(project / "docs" / "bad.yml")
    assert not (project / "docs" / "sldb").exists()


def test_find_store_walks_up(project):
    assert find_store(project / "docs") == (project / ".sldb").resolve()


def test_notation_override_and_mismatch(project):
    store = project / ".sldb"
    sync = SpecSync(store)
    report = sync.sync(project / "docs" / "flow.yml", notation="none")
    assert report.notation == "" and not any(d.startswith("NotationDoc") for d in report.created)
    with pytest.raises(ValueError, match="draws `class` specs"):
        sync.sync(project / "docs" / "flow.yml", notation="uml-class")


def test_spec_elements_keep_the_rest_of_the_element_in_data():
    spec = {"type": "class", "data": {"classes": {"a": {"label": "A", "kind": "interface", "attributes": [{"name": "x", "type": "int"}], "methods": []}}}}
    (el,) = spec_elements(spec)
    assert el["kind"] == "interface" and el["data"] == {"attributes": [{"name": "x", "type": "int"}], "methods": []}
    guarded = {"type": "state", "data": {"initial": "a", "states": [{"id": "a", "label": "A"}], "transitions": [{"from": "a", "to": "a", "on": "tick", "guard": "x > 1"}]}}
    assert spec_elements(guarded)[0]["data"] == {"initial": True}
    assert spec_edges(guarded)[0]["label"] == "tick [x > 1]"


# --- CLI ----------------------------------------------------------------------------

def test_cli_sync_discovers_store_and_strict_fails_on_unresolved(project):
    runner = CliRunner()
    result = runner.invoke(main, ["diagram", "sync", str(project / "docs" / "arq.yml")])
    assert result.exit_code == 0, result.output
    assert "Synced arq: 3 nodes, 2 edges (6 created" in result.output and "atom-nope" in result.output

    result = runner.invoke(main, ["diagram", "sync", str(project / "docs" / "arq.yml"), "--strict"])
    assert result.exit_code == 1

    result = runner.invoke(main, ["diagram", "sync", str(project / "docs" / "flow.yml"), "--store", str(project / ".sldb"), "--strict"])
    assert result.exit_code == 0, result.output


def test_cli_sync_without_store(tmp_path):
    (tmp_path / "arq.yml").write_text(yaml.safe_dump(ARQ), encoding="utf-8")
    result = CliRunner().invoke(main, ["diagram", "sync", str(tmp_path / "arq.yml")])
    assert result.exit_code == 1 and "no `.sldb` store" in result.output
