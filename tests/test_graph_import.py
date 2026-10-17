"""`diagram from-graph`: grafo sldb (node-link JSON o edge index) -> spec component."""
import json
from types import SimpleNamespace

import yaml
from click.testing import CliRunner

from spec2viz import validate
from spec2viz.cli import main
from spec2viz.graph_import import (
    DEFAULT_EXCLUDED_RELATIONS,
    component_spec_from_graph,
    document_ref,
    load_node_link,
    load_store_index,
    node_kind,
    sanitize_id,
)
from spec2viz.loader import _adapter

runner = CliRunner()

# Grafo minimo: dos atoms, una task, un modelo, un tag y una seccion.
NODES = {
    "sldb://store": "sldb_store",
    "sldb://model/AtomDoc": "sldb_model",
    "sldb://document/AtomDoc:atom-x": "sldb_document",
    "sldb://document/AtomDoc:atom-y": "AtomDoc",
    "sldb://document/TaskDoc:task-z": "sldb_document",
    "sldb://section/AtomDoc:atom-x#intro": "sldb_section",
    "sldb://semantic_tag/system:spec2viz": "semantic_tag",
}
EDGES = [
    ("sldb://store", "sldb://model/AtomDoc", "has_model"),
    ("sldb://model/AtomDoc", "sldb://document/AtomDoc:atom-x", "has_document"),
    ("sldb://document/AtomDoc:atom-x", "sldb://section/AtomDoc:atom-x#intro", "has_section"),
    ("sldb://document/AtomDoc:atom-x", "sldb://semantic_tag/system:spec2viz", "tagged_as"),
    ("sldb://document/AtomDoc:atom-x", "sldb://document/AtomDoc:atom-y", "contains"),
    ("sldb://document/AtomDoc:atom-y", "sldb://document/TaskDoc:task-z", "explains"),
    ("sldb://document/AtomDoc:atom-y", "sldb://document/TaskDoc:task-z", "explains"),
]


def _validated(spec: dict):
    diagram = _adapter.validate_python(spec)
    validate(diagram)
    return diagram


# --- helpers de ids -------------------------------------------------------------

def test_node_kind_prefers_uri_segment_over_source_type():
    assert node_kind("sldb://document/AtomDoc:atom-x", "AtomDoc") == "document"
    assert node_kind("sldb://document/AtomDoc:atom-x", "sldb_document") == "document"
    assert node_kind("sldb://semantic_tag/a:b", "semantic_tag") == "semantic_tag"
    assert node_kind("sldb://store", "sldb_store") == "store"
    assert node_kind("plain-id", "sldb_model") == "model"


def test_document_ref_parses_model_name_and_linked_store():
    assert document_ref("sldb://document/AtomDoc:atom-x") == ("AtomDoc", "atom-x")
    assert document_ref("sldb://document/desk:TaskDoc:task-z") == ("TaskDoc", "task-z")
    assert document_ref("sldb://document/atom-x", "AtomDoc") == ("AtomDoc", "atom-x")
    assert document_ref("sldb://model/AtomDoc", "sldb_model") == (None, None)


def test_sanitize_id_is_safe_identifier():
    assert sanitize_id("sldb://document/AtomDoc:atom-x") == "document_AtomDoc_atom_x"
    assert sanitize_id("sldb://section/AtomDoc:atom-x#intro") == "section_AtomDoc_atom_x_intro"
    assert sanitize_id("sldb://store") == "store"
    assert sanitize_id("123abc") == "n_123abc"
    assert sanitize_id("end") == "n_end"
    assert sanitize_id("///") == "node"


# --- compilacion ----------------------------------------------------------------

def test_default_keeps_documents_and_models_without_structural_edges():
    spec = component_spec_from_graph(NODES, EDGES, source="test")
    _validated(spec)
    nodes = spec["data"]["nodes"]
    assert set(nodes) == {"model_AtomDoc", "document_AtomDoc_atom_x", "document_AtomDoc_atom_y", "document_TaskDoc_task_z"}
    assert nodes["model_AtomDoc"] == {"label": "AtomDoc", "kind": "model"}
    assert nodes["document_AtomDoc_atom_y"]["label"] == "atom-y"
    assert nodes["document_AtomDoc_atom_y"]["kind"] == "AtomDoc"
    assert nodes["document_TaskDoc_task_z"]["kind"] == "TaskDoc"
    # has_model / has_document / has_section / tagged_as se descartan por defecto
    assert spec["data"]["edges"] == [{"from": "document_AtomDoc_atom_y", "to": "document_TaskDoc_task_z", "relation": "explains"}]
    assert spec["type"] == "component" and spec["version"] == "1.0"
    assert "test" in spec["metadata"]["description"]
    assert "exclude_relations=" + ",".join(DEFAULT_EXCLUDED_RELATIONS) in spec["metadata"]["description"]


def test_contains_relation_nests_instead_of_edge():
    spec = component_spec_from_graph(NODES, EDGES)
    assert spec["data"]["nodes"]["document_AtomDoc_atom_x"]["contains"] == ["document_AtomDoc_atom_y"]
    assert "contains" not in spec["data"]["nodes"]["document_AtomDoc_atom_y"]
    assert all(e["relation"] != "contains" for e in spec["data"]["edges"])


def test_duplicate_edges_collapse():
    spec = component_spec_from_graph(NODES, EDGES)
    assert len([e for e in spec["data"]["edges"] if e["relation"] == "explains"]) == 1


def test_model_filter_keeps_only_documents_of_that_model():
    spec = component_spec_from_graph(NODES, EDGES, models=["AtomDoc"])
    nodes = spec["data"]["nodes"]
    assert "document_TaskDoc_task_z" not in nodes
    assert "model_AtomDoc" in nodes  # el filtro de modelo no toca nodos que no son documentos
    assert spec["data"]["edges"] == []  # la arista hacia task-z pierde su destino


def test_node_type_filter_accepts_sldb_prefix():
    spec = component_spec_from_graph(NODES, EDGES, node_types=["sldb_document", "semantic_tag"], relations=["tagged_as"])
    nodes = spec["data"]["nodes"]
    assert "model_AtomDoc" not in nodes
    assert nodes["semantic_tag_system_spec2viz"] == {"label": "system:spec2viz", "kind": "semantic_tag"}
    assert spec["data"]["edges"] == [
        {"from": "document_AtomDoc_atom_x", "to": "semantic_tag_system_spec2viz", "relation": "tagged_as"}
    ]


def test_relation_include_overrides_default_exclusions():
    spec = component_spec_from_graph(NODES, EDGES, relations=["has_document"])
    assert spec["data"]["edges"] == [
        {"from": "model_AtomDoc", "to": "document_AtomDoc_atom_x", "relation": "has_document"}
    ]
    assert "relations=has_document" in spec["metadata"]["description"]


def test_exclude_relation_replaces_defaults():
    spec = component_spec_from_graph(NODES, EDGES, exclude_relations=["explains"])
    relations = {e["relation"] for e in spec["data"]["edges"]}
    assert "explains" not in relations
    assert "has_document" in relations  # ya no esta excluida


def test_drop_isolated_removes_nodes_without_edges_or_nesting():
    spec = component_spec_from_graph(NODES, EDGES, drop_isolated=True)
    assert set(spec["data"]["nodes"]) == {"document_AtomDoc_atom_x", "document_AtomDoc_atom_y", "document_TaskDoc_task_z"}
    spec = component_spec_from_graph(NODES, EDGES, models=["AtomDoc"], relations=["explains"], drop_isolated=True)
    assert spec["data"]["nodes"] == {}
    assert spec["data"]["edges"] == []


def test_sanitized_ids_stay_unique():
    nodes = {"sldb://document/AtomDoc:a-b": "sldb_document", "sldb://document/AtomDoc:a_b": "sldb_document",
             "sldb://document/AtomDoc:a.b": "sldb_document"}
    spec = component_spec_from_graph(nodes, [("sldb://document/AtomDoc:a-b", "sldb://document/AtomDoc:a.b", "uses")])
    assert set(spec["data"]["nodes"]) == {"document_AtomDoc_a_b", "document_AtomDoc_a_b_2", "document_AtomDoc_a_b_3"}
    assert spec["data"]["edges"] == [{"from": "document_AtomDoc_a_b", "to": "document_AtomDoc_a_b_3", "relation": "uses"}]
    _validated(spec)


def test_edges_to_unknown_nodes_are_dropped():
    edges = EDGES + [("sldb://document/AtomDoc:atom-x", "sldb://document/Ghost:g", "uses")]
    spec = component_spec_from_graph(NODES, edges)
    assert all(e["to"] != "document_Ghost_g" for e in spec["data"]["edges"])
    _validated(spec)


# --- loaders --------------------------------------------------------------------

def _node_link(path):
    """Mezcla nodos con `id`/`type` y nodos que solo traen `schema.identity`."""
    nodes = []
    for i, (nid, ntype) in enumerate(NODES.items()):
        if i % 2:
            nodes.append({"id": nid, "type": ntype, "schema": {"identity": {"node_id": nid, "node_type": ntype}}})
        else:
            nodes.append({"schema": {"identity": {"node_id": nid, "node_type": ntype}}})
    links = [{"source": s, "target": t, "relation": r, "metadata": {}} for s, t, r in EDGES]
    path.write_text(json.dumps({"directed": True, "multigraph": False, "graph": {}, "nodes": nodes, "links": links}))
    return path


def test_load_node_link_reads_id_from_top_level_or_schema_identity(tmp_path):
    nodes, edges = load_node_link(_node_link(tmp_path / "g.json"))
    assert nodes == NODES
    assert edges == EDGES


def test_load_store_index_uses_public_sldb_api(monkeypatch, tmp_path):
    import sldb.api

    fake_index = SimpleNamespace(
        nodes={nid: SimpleNamespace(id=nid, node_type=ntype, semantics={}, facets={}) for nid, ntype in NODES.items()},
        edges=[SimpleNamespace(source=s, target=t, relation=r, metadata={}) for s, t, r in EDGES],
    )
    calls = []
    monkeypatch.setattr(sldb.api, "load_edge_index", lambda store: calls.append(store) or fake_index)

    nodes, edges = load_store_index(tmp_path / ".sldb")

    assert calls == [tmp_path / ".sldb"]
    assert nodes == NODES
    assert edges == EDGES


# --- CLI ------------------------------------------------------------------------

def test_cli_from_graph_writes_valid_spec(tmp_path):
    graph = _node_link(tmp_path / "snap.json")
    out = tmp_path / "graph.yml"
    r = runner.invoke(main, ["diagram", "from-graph", str(graph), "--model", "AtomDoc", "--out", str(out)])
    assert r.exit_code == 0, r.output
    assert "Generated" in r.output and "3 nodes" in r.output

    spec = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert spec["id"] == "snap" and spec["title"] == "snap graph"
    assert "snap.json" in spec["metadata"]["description"]
    _validated(spec)

    r = runner.invoke(main, ["diagram", "validate", str(out)])
    assert r.exit_code == 0, r.output
    r = runner.invoke(main, ["diagram", "render", str(out), "--out", str(tmp_path), "--renderer", "mermaid"])
    assert r.exit_code == 0, r.output
    mmd = (tmp_path / "graph.mmd").read_text(encoding="utf-8")
    assert 'subgraph document_AtomDoc_atom_x ["atom-x"]' in mmd
    assert 'document_AtomDoc_atom_y["atom-y"]' in mmd
    r = runner.invoke(main, ["diagram", "lint", str(out)])
    assert r.exit_code == 0, r.output


def test_cli_from_graph_prints_yaml_to_stdout_with_filters(tmp_path):
    graph = _node_link(tmp_path / "snap.json")
    r = runner.invoke(
        main,
        ["diagram", "from-graph", str(graph), "--id", "tags", "--title", "Tags", "--node-type", "document",
         "--node-type", "semantic_tag", "--relation", "tagged_as", "--drop-isolated"],
    )
    assert r.exit_code == 0, r.output
    spec = yaml.safe_load(r.output)
    assert spec["id"] == "tags" and spec["title"] == "Tags"
    assert set(spec["data"]["nodes"]) == {"document_AtomDoc_atom_x", "semantic_tag_system_spec2viz"}
    assert spec["data"]["edges"][0]["relation"] == "tagged_as"
    _validated(spec)


def test_cli_from_graph_requires_exactly_one_source(tmp_path):
    graph = _node_link(tmp_path / "snap.json")
    assert runner.invoke(main, ["diagram", "from-graph"]).exit_code == 2
    assert runner.invoke(main, ["diagram", "from-graph", str(graph), "--store", str(tmp_path)]).exit_code == 2


def test_cli_from_graph_store_goes_through_loader(monkeypatch, tmp_path):
    import spec2viz.graph_import as gi

    monkeypatch.setattr(gi, "load_store_index", lambda store: (dict(NODES), list(EDGES)))
    r = runner.invoke(main, ["diagram", "from-graph", "--store", str(tmp_path), "--relation", "has_document"])
    assert r.exit_code == 0, r.output
    spec = yaml.safe_load(r.output)
    assert spec["id"] == "sldb-graph"
    assert f"store {tmp_path}" in spec["metadata"]["description"]
    assert spec["data"]["edges"] == [{"from": "model_AtomDoc", "to": "document_AtomDoc_atom_x", "relation": "has_document"}]
