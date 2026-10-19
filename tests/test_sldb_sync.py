"""`spec2viz diagram sync`: el spec como namespace sobre el store sldb (SpecDoc, SpecNodeDoc, RelationDoc)."""
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from spec2viz.cli import main
from spec2viz.deskops import SldbAtomResolver
from spec2viz.sldb_sync import SpecSync, catalog_entries, edge_name, find_store, relation_token, spec_edges, spec_elements, to_slash_ref

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
        {"from": "cli", "to": "core", "relation": "uses", "label": "", "condition": "", "attributes": {}},
        {"from": "core", "to": "renderers", "relation": "loads_path", "label": "x", "condition": "", "attributes": {}},
    ]
    assert spec_edges(FLOW) == [{"from": "a", "to": "b", "relation": "transitions_to", "label": "go", "condition": "", "attributes": {"on": "go"}}]
    assert edge_name("arq", 1, 2, spec_edges(ARQ)[0]) == "arq.01-cli__uses__core" and edge_name("x", 7, 123, {"from": "a", "relation": "r", "to": "b"}) == "x.007-a__r__b"
    assert relation_token(" Depends-On ", "x") == "depends_on" and relation_token("", "uses") == "uses"
    assert to_slash_ref("AtomDoc:atom-a") == "AtomDoc/atom-a" and to_slash_ref("desk:TaskDoc:t") == "desk:TaskDoc/t"


# --- contra un store real -----------------------------------------------------------

def test_sync_writes_spec_nodes_and_edges(project):
    store = project / ".sldb"
    report = SpecSync(store).sync(project / "docs" / "arq.yml")

    assert sorted(report.created) == sorted([
        "SpecDoc:arq", "SpecNodeDoc:arq.cli", "SpecNodeDoc:arq.core", "SpecNodeDoc:arq.renderers",
        "RelationDoc:arq.01-cli__uses__core", "RelationDoc:arq.02-core__loads_path__renderers",
        "NotationDoc:component", "GlyphDoc:component.boundary", "GlyphDoc:component.entry", "GlyphDoc:component.component",
        "LinkDoc:component.contains", "LinkDoc:component.relation",
    ])
    assert report.relation_types_added == ["loads_path", "uses"]
    assert report.unresolved == ["arq.renderers: 'AtomDoc:atom-nope' no existe en el store"]
    assert report.edge_errors == []

    out = project / "docs" / "sldb" / "arq"
    assert (out / "arq.md").exists() and (out / "nodes" / "arq.cli.md").exists() and (out / "edges" / "arq.01-cli__uses__core.md").exists()
    assert (project / "sldb" / "relation_types" / "loads_path.md").exists()
    assert sldb_api.doc_exists(store, "SpecNodeDoc/arq.renderers") and sldb_api.doc_exists(store, "RelationTypeDoc/reltype-uses")

    node = yaml.safe_load((out / "nodes" / "arq.cli.md").read_text(encoding="utf-8").split("---")[1])
    assert node == {"id": "arq.cli", "spec": "SpecDoc:arq", "element": "cli", "kind": "entry", "collection": "nodes", "refs": [], "atom_refs": [], "contains": ["SpecNodeDoc:arq.core"], "data": {}}
    spec_doc = yaml.safe_load((out / "arq.md").read_text(encoding="utf-8").split("---")[1])
    assert spec_doc["spec_path"] == "docs/arq.yml" and len(spec_doc["sha256"]) == 64
    assert spec_doc["notation"] == "NotationDoc:component" and spec_doc["category"] == ""
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
    transition = (project / "docs" / "sldb" / "flow" / "edges" / "flow.01-a__transitions_to__b.md").read_text(encoding="utf-8")
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
    assert again.created == [] and len(again.updated) == 12 and again.deleted == [] and again.relation_types_added == []

    smaller = yaml.safe_load(yaml.safe_dump(ARQ))
    smaller["data"]["nodes"].pop("renderers")
    smaller["data"]["edges"].pop()
    (project / "docs" / "arq.yml").write_text(yaml.safe_dump(smaller), encoding="utf-8")
    report = SpecSync(store).sync(project / "docs" / "arq.yml")
    assert sorted(report.deleted) == ["RelationDoc:arq.02-core__loads_path__renderers", "SpecNodeDoc:arq.renderers"]
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


def test_other_diagram_types_extract_their_own_edges():
    activity = {"type": "activity", "data": {"start": "a", "end": "z", "steps": {
        "a": {"label": "A", "next": "d"}, "d": {"label": "D?", "kind": "decision", "branches": {"yes": "z", "no": "a"}}, "z": {"label": "Z"}}}}
    els = {e["id"]: e for e in spec_elements(activity)}
    assert els["a"]["data"] == {"initial": True, "next": "d"} and els["z"]["data"] == {"final": True} and els["d"]["collection"] == "steps" and "branches" in els["d"]["data"]
    assert [(e["from"], e["to"], e["relation"], e["label"]) for e in spec_edges(activity)] == [("a", "d", "next", ""), ("d", "z", "branch", "yes"), ("d", "a", "branch", "no")]

    sequence = {"type": "sequence", "data": {"participants": [{"id": "u", "kind": "actor"}, {"id": "s"}], "messages": [
        {"from": "u", "to": "s", "message": "hi"}, {"from": "s", "to": "u", "message": "ok", "kind": "return", "condition": "if alive"}, {"from": "u", "to": "s", "message": "bye", "kind": "async"}]}}
    assert [(e["relation"], e["label"], e["condition"]) for e in spec_edges(sequence)] == [("sends", "hi", ""), ("returns", "ok", "if alive"), ("sends_async", "bye", "")]
    assert spec_edges(sequence)[1]["attributes"] == {"kind": "return", "message": "ok"}

    matrix = {"type": "component_view_matrix", "data": {
        "views": [{"id": "v", "label": "View", "stages": [{"id": "s1", "label": "One"}, {"id": "s2", "label": "Two"}]}],
        "components": [{"name": "Root", "kind": "core", "stages": {"v": ["s1", "s2"]}, "children": [{"name": "Kid", "kind": "boundary", "stages": {"v": ["s2"]}}]}]}}
    els = {e["id"]: e for e in spec_elements(matrix)}
    assert els["v__s1"]["collection"] == "stages" and els["v__s1"]["data"] == {"view": "v", "view_label": "View", "order": 1}
    assert els["Root"]["contains"] == ["Kid"] and els["Kid"]["kind"] == "boundary" and els["Root"]["data"]["stages"] == {"v": ["s1", "s2"]}
    assert [(e["from"], e["to"], e["relation"]) for e in spec_edges(matrix)] == [("Root", "v__s1", "occupies"), ("Root", "v__s2", "occupies"), ("Kid", "v__s2", "occupies")]

    reflection = {"type": "reflection", "data": {"nodes": {"a": {"label": "A", "kind": "internal"}}, "edges": [{"from": "a", "to": "a", "relation": "uses"}]}}
    assert spec_elements(reflection)[0]["collection"] == "nodes" and spec_edges(reflection)[0]["relation"] == "uses"


def test_catalog_entries_read_vistas(tmp_path):
    (tmp_path / "specs").mkdir()
    (tmp_path / "specs" / "a.yml").write_text("id: a\n", encoding="utf-8")
    (tmp_path / "vistas.yml").write_text(yaml.safe_dump({"vistas": [
        {"id": "va", "category": "Cat", "nav": "A", "desc": "About a", "specs": ["specs/a.yml"]},
        {"id": "vb", "category": "Cat", "title": "B", "specs": []},
    ]}), encoding="utf-8")
    entries = catalog_entries(tmp_path / "vistas.yml")
    assert entries == [{"spec": (tmp_path / "specs" / "a.yml").resolve(), "vista": "va", "catalog": {"category": "Cat", "nav": "A", "summary": "About a"}}]


def test_spec_elements_keep_the_rest_of_the_element_in_data():
    spec = {"type": "class", "data": {"classes": {"a": {"label": "A", "kind": "interface", "attributes": [{"name": "x", "type": "int"}], "methods": []}}}}
    (el,) = spec_elements(spec)
    assert el["kind"] == "interface" and el["data"] == {"attributes": [{"name": "x", "type": "int"}], "methods": []}
    guarded = {"type": "state", "data": {"initial": "a", "states": [{"id": "a", "label": "A"}], "transitions": [{"from": "a", "to": "a", "on": "tick", "guard": "x > 1"}]}}
    assert spec_elements(guarded)[0]["data"] == {"initial": True}
    assert spec_edges(guarded)[0]["label"] == "tick [x > 1]"
    acted = {"type": "state", "data": {"initial": "a", "states": [{"id": "a", "label": "A"}], "transitions": [{"from": "a", "to": "a", "on": "tick", "action": "log()"}]}}
    assert spec_edges(acted)[0]["label"] == "tick / log()" and spec_edges(acted)[0]["attributes"] == {"on": "tick", "action": "log()"}
    classes = {"type": "class", "data": {"classes": {"A": {}, "B": {}}, "relations": [{"from": "A", "to": "B", "relation": "composition", "from_multiplicity": "1", "to_multiplicity": "0..*", "label": "parts"}]}}
    assert spec_edges(classes)[0]["attributes"] == {"from_multiplicity": "1", "to_multiplicity": "0..*", "label": "parts"}


# --- CLI ----------------------------------------------------------------------------

def test_cli_sync_discovers_store_and_strict_fails_on_unresolved(project):
    runner = CliRunner()
    result = runner.invoke(main, ["diagram", "sync", str(project / "docs" / "arq.yml")])
    assert result.exit_code == 0, result.output
    assert "Synced arq: 3 nodes, 2 edges (12 created" in result.output and "atom-nope" in result.output

    result = runner.invoke(main, ["diagram", "sync", str(project / "docs" / "arq.yml"), "--strict"])
    assert result.exit_code == 1

    result = runner.invoke(main, ["diagram", "sync", str(project / "docs" / "flow.yml"), "--store", str(project / ".sldb"), "--strict"])
    assert result.exit_code == 0, result.output


def test_cli_sync_without_store(tmp_path):
    (tmp_path / "arq.yml").write_text(yaml.safe_dump(ARQ), encoding="utf-8")
    result = CliRunner().invoke(main, ["diagram", "sync", str(tmp_path / "arq.yml")])
    assert result.exit_code == 1 and "no `.sldb` store" in result.output


def test_activity_terminal_end_that_is_not_a_step_is_materialized():
    """`end: end` (como en examples/activity) nombra un nodo terminal: las aristas `next: end` tienen destino."""
    spec = {"id": "activity.t", "type": "activity", "data": {"start": "a", "end": "end", "steps": {
        "a": {"label": "A", "next": "b"}, "b": {"label": "B", "next": "end"}}}}
    elements = {e["id"]: e for e in spec_elements(spec)}
    assert elements["end"]["kind"] == "end" and elements["end"]["data"]["final"] is True and elements["end"]["collection"] == "steps"
    assert elements["a"]["data"]["initial"] is True and "start" not in elements
    assert {e["to"] for e in spec_edges(spec)} <= set(elements)


def test_activity_end_that_is_a_step_is_not_duplicated():
    spec = {"id": "activity.t", "type": "activity", "data": {"start": "a", "end": "done", "steps": {"a": {"next": "done"}, "done": {"label": "Done"}}}}
    ids = [e["id"] for e in spec_elements(spec)]
    assert ids.count("done") == 1


def test_deployment_protocol_is_an_attribute_not_a_relation_type():
    """`:5432` y `Postgres :5432` son la misma relacion `connects`; el protocolo va en attributes y rotulo."""
    spec = {"id": "deployment.t", "type": "deployment", "data": {"connections": [
        {"from": "api", "to": "db", "protocol": ":5432"}, {"from": "ui", "to": "db", "protocol": "Postgres :5432"}, {"from": "ui", "to": "api"}]}}
    edges = spec_edges(spec)
    assert {e["relation"] for e in edges} == {"connects"}
    assert [e["attributes"].get("protocol") for e in edges] == [":5432", "Postgres :5432", None]
    assert [e["label"] for e in edges] == [":5432", "Postgres :5432", ""]
