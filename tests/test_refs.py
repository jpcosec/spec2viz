"""`refs: [Model:name]` por elemento del spec -> referencias a documentos sldb en el catalogo."""
import json
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml
from click.testing import CliRunner

from spec2viz.cli import main
from spec2viz.deskops import SldbAtomResolver, build_explicit_refs, collect_explicit_refs, render_deskops
from spec2viz.models.activity import StepModel
from spec2viz.models.class_diagram import ClassDefinition
from spec2viz.models.component import NodeModel
from spec2viz.models.deployment import ArtifactModel, DeploymentNodeModel
from spec2viz.models.sequence import ParticipantModel
from spec2viz.models.state import StateData
from spec2viz.schema import json_schema


@pytest.mark.parametrize("model", [NodeModel, DeploymentNodeModel, ArtifactModel, StepModel, ClassDefinition, ParticipantModel])
def test_models_accept_refs(model):
    assert model.model_fields["refs"].default_factory() == []
    kwargs = {"id": "p"} if model is ParticipantModel else {"label": "L"} if model is StepModel else {}
    assert model(**kwargs, refs=["TaskDoc:task-x", "desk:AtomDoc:atom-y"]).refs == ["TaskDoc:task-x", "desk:AtomDoc:atom-y"]


@pytest.mark.parametrize("bad", ["sin-modelo", "Model:", ":name", "a b:c", "Model:na me"])
def test_refs_without_model_part_are_rejected(bad):
    with pytest.raises(Exception):
        NodeModel(refs=[bad])


def test_state_model_and_schema_expose_refs():
    data = StateData(entity="E", initial="a", states=[{"id": "a", "label": "A", "refs": ["TaskDoc:t"]}], transitions=[])
    assert data.states[0].refs == ["TaskDoc:t"]
    assert "refs" in json.dumps(json_schema("state"))


# --- build ---------------------------------------------------------------------

def _project(tmp_path, refs):
    spec = {
        "id": "arq", "title": "Arq", "type": "component", "version": "1.0",
        "data": {"nodes": {"cli": {"label": "CLI", "refs": refs}, "core": {"label": "Core"}}, "edges": []},
    }
    (tmp_path / "arq.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
    (tmp_path / "f.mmd").write_text("graph TD\n  cli --> core\n", encoding="utf-8")
    (tmp_path / "vistas.yml").write_text(
        "vistas:\n  - id: v1\n    title: V1\n    src: f.mmd\n    type: component\n    specs: [arq.yml]\n", encoding="utf-8"
    )
    (tmp_path / "template.html").write_text("<html><body>{{SECTIONS}}</body></html>", encoding="utf-8")
    return tmp_path / "vistas.yml"


FAKE_DOCS = [
    {"ref": "TaskDoc:task-x", "store": "/s/.sldb", "store_name": "local", "model": "TaskDoc", "name": "task-x",
     "title": "Tarea X", "path": "/s/desk/tasks/task-x.md", "payload": {"title": "Tarea X", "summary": "Resumen de X"}},
    {"ref": "AtomDoc:atom-y", "store": "/s/.sldb", "store_name": "local", "model": "AtomDoc", "name": "atom-y",
     "title": "Atomo Y", "path": "/s/desk/atoms/atom-y.md", "payload": {"title": "Atomo Y", "answer": "Respuesta Y"}},
]


FAKE_EDGES = {
    "AtomDoc:atom-y": [{"relation": "references", "direction": "in", "node": "sldb://document/SpecNodeDoc:arq.cli",
                        "ref": "SpecNodeDoc:arq.cli", "title": "CLI"}],
}


def _fake_store(monkeypatch):
    monkeypatch.setattr(SldbAtomResolver, "_discover_store_for_item", lambda self, item: Path("/s/.sldb"))
    monkeypatch.setattr(SldbAtomResolver, "_load_store_documents", lambda self, store: list(FAKE_DOCS))
    monkeypatch.setattr(SldbAtomResolver, "edges_of", lambda self, store, ref: list(FAKE_EDGES.get(ref, [])))


def test_collect_explicit_refs_indexes_by_label_and_id(tmp_path):
    from spec2viz.orchestrator import load_catalog

    item = load_catalog(_project(tmp_path, ["TaskDoc:task-x"])).items[0]
    assert collect_explicit_refs(item) == {"cli": ["TaskDoc:task-x"]}


def test_build_resolves_refs_with_title_path_and_summary(monkeypatch, tmp_path):
    _fake_store(monkeypatch)
    html = render_deskops(_project(tmp_path, ["TaskDoc:task-x", "AtomDoc:atom-y"]))
    payload = json.loads(html.split("window.REFS_EXPLICIT = ")[1].split("; window.")[0])
    refs = list(payload.values())[0]["cli"]
    assert [r["ref"] for r in refs] == ["TaskDoc:task-x", "AtomDoc:atom-y"]
    assert refs[0] == {
        "ref": "TaskDoc:task-x", "model": "TaskDoc", "name": "task-x", "title": "Tarea X",
        "path": "/s/desk/tasks/task-x.md", "store": "/s/.sldb", "summary": "Resumen de X", "edges": [],
    }
    assert refs[1]["summary"] == "Respuesta Y"
    assert refs[1]["edges"] == FAKE_EDGES["AtomDoc:atom-y"]


def test_unknown_ref_is_warning_unless_strict(monkeypatch, tmp_path, capsys):
    _fake_store(monkeypatch)
    config = _project(tmp_path, ["TaskDoc:no-existe"])
    html = render_deskops(config)
    assert "window.REFS_EXPLICIT = {}" in html
    assert "no-existe" in capsys.readouterr().err

    result = CliRunner().invoke(main, ["catalog", "build", "--config", str(config), "--out", str(tmp_path / "o.html"), "--strict-atoms"])
    assert result.exit_code == 1
    assert "no-existe" in result.output


def test_view_without_store_warns_per_ref(monkeypatch, tmp_path):
    monkeypatch.setattr(SldbAtomResolver, "_discover_store_for_item", lambda self, item: None)
    from spec2viz.orchestrator import load_catalog

    items = load_catalog(_project(tmp_path, ["TaskDoc:task-x"])).items
    result, warnings = build_explicit_refs(items)
    assert result == {}
    assert len(warnings) == 1 and "sin store" in warnings[0].message


# --- aristas sldb -----------------------------------------------------------------

def _edge(source, target, relation):
    return SimpleNamespace(source=source, target=target, relation=relation, metadata={"origin": "schema"})


def test_edges_of_keeps_declared_edges_both_ways_and_drops_structural(monkeypatch, tmp_path):
    import sldb.api

    store = tmp_path / ".sldb"
    me = "sldb://document/AtomDoc:atom-y"
    monkeypatch.setattr(SldbAtomResolver, "_load_store_documents", lambda self, s: list(FAKE_DOCS))
    monkeypatch.setattr(sldb.api, "edges_from", lambda s, ref: [
        _edge(me, "sldb://section/AtomDoc:atom-y#answer", "has_section"),
        _edge(me, "sldb://semantic_tag/system:x", "tagged_as"),
        _edge(me, "sldb://document/TaskDoc:task-x", "composes"),
    ])
    monkeypatch.setattr(sldb.api, "edges_to", lambda s, ref: [
        _edge("sldb://model/AtomDoc", me, "has_document"),
        _edge("sldb://document/SpecNodeDoc:arq.cli", me, "references"),
        _edge("sldb://relation_type/custom", me, "custom_rel"),
    ])

    resolver = SldbAtomResolver()
    edges = resolver.edges_of(store, "AtomDoc:atom-y")
    assert edges == [
        {"relation": "composes", "direction": "out", "node": "sldb://document/TaskDoc:task-x", "ref": "TaskDoc:task-x", "title": "Tarea X"},
        {"relation": "references", "direction": "in", "node": "sldb://document/SpecNodeDoc:arq.cli", "ref": "SpecNodeDoc:arq.cli", "title": "SpecNodeDoc:arq.cli"},
        {"relation": "custom_rel", "direction": "in", "node": "sldb://relation_type/custom", "ref": "", "title": "sldb://relation_type/custom"},
    ]
    assert resolver.edges_of(store, "AtomDoc:atom-y") is edges  # cache
    assert resolver.warnings == []


def test_edges_of_without_edge_index_warns_once_and_is_empty(monkeypatch, tmp_path, capsys):
    import sldb.api

    monkeypatch.setattr(SldbAtomResolver, "_load_store_documents", lambda self, s: [])

    def boom(store, ref):
        raise RuntimeError("no edge index")

    monkeypatch.setattr(sldb.api, "edges_from", boom)
    resolver = SldbAtomResolver()
    assert resolver.edges_of(tmp_path / ".sldb", "AtomDoc:a") == []
    assert resolver.edges_of(tmp_path / ".sldb", "AtomDoc:b") == []
    assert len(resolver.warnings) == 1 and "no edge index" in resolver.warnings[0].message


def test_edges_of_against_a_real_store(tmp_path):
    import sldb.api

    project = tmp_path / "proj"
    project.mkdir()
    sldb.api.init_store(project)
    sldb.api.init_relations(project / ".sldb")
    sldb.api.rebuild_edges(project / ".sldb")
    resolver = SldbAtomResolver()
    # la relacion builtin `references` existe como documento, sin aristas declaradas: lista vacia, sin warnings
    assert resolver.edges_of(project / ".sldb", "RelationTypeDoc:references") == []
    assert resolver.warnings == []


def test_build_attaches_edges_to_explicit_atoms(monkeypatch, tmp_path):
    spec = {
        "id": "arq", "title": "Arq", "type": "component", "version": "1.0",
        "data": {"nodes": {"cli": {"label": "CLI", "atoms": ["atom-y"]}}, "edges": []},
    }
    (tmp_path / "arq.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
    (tmp_path / "f.mmd").write_text("graph TD\n  cli\n", encoding="utf-8")
    (tmp_path / "vistas.yml").write_text(
        "vistas:\n  - id: v1\n    title: V1\n    src: f.mmd\n    type: component\n    specs: [arq.yml]\n", encoding="utf-8"
    )
    (tmp_path / "template.html").write_text("<html><body>{{SECTIONS}}</body></html>", encoding="utf-8")
    atom_docs = [{"ref": "AtomDoc:atom-y", "store": "/s/.sldb", "store_name": "local", "model": "AtomDoc", "name": "atom-y",
                  "title": "Atomo Y", "path": "/s/desk/atoms/atom-y.md",
                  "payload": {"id": "atom-y", "title": "Atomo Y", "five_wh_one_plus": "what", "answer": "Respuesta Y"}}]
    monkeypatch.setattr(SldbAtomResolver, "_discover_store_for_item", lambda self, item: Path("/s/.sldb"))
    monkeypatch.setattr(SldbAtomResolver, "_load_store_documents", lambda self, store: list(atom_docs))
    monkeypatch.setattr(SldbAtomResolver, "edges_of", lambda self, store, ref: list(FAKE_EDGES.get(ref, [])))

    html = render_deskops(tmp_path / "vistas.yml")
    explicit = json.loads(html.split("window.ATOMS_EXPLICIT = ")[1].split("; window.")[0])
    atom = list(explicit.values())[0]["cli"]["list"][0]
    assert atom["id"] == "atom-y" and atom["edges"] == FAKE_EDGES["AtomDoc:atom-y"]


# --- resolver over the public sldb API ------------------------------------------

def test_store_documents_come_from_sldb_api(monkeypatch, tmp_path):
    import sldb.api

    runtime_docs = [
        SimpleNamespace(model_name="AtomDoc", name="atom-a", path="desk/atoms/atom-a.md", store_name="local",
                        store_path=str(tmp_path / ".sldb"),
                        payload={"id": "atom-a", "title": "Alpha", "five_wh_one_plus": "what", "answer": "Cuerpo", "tags": ["x:y"]}),
        SimpleNamespace(model_name="TaskDoc", name="task-b", path="desk/tasks/task-b.md", store_name="desk",
                        store_path=str(tmp_path / "other" / ".sldb"), payload={"title": "Beta"}),
    ]
    calls = {}

    def fake_load(store_path, pythonpath=None, include_linked=False):
        calls["args"] = (store_path, pythonpath, include_linked)
        return runtime_docs

    monkeypatch.setattr(sldb.api, "load_runtime_documents", fake_load)
    monkeypatch.setattr(sldb.api, "open_store", lambda p: SimpleNamespace(store_path=Path(p), project_root=Path(p).parent))

    resolver = SldbAtomResolver(pythonpath="pp")
    docs = resolver._load_store_documents(tmp_path / ".sldb")

    assert calls["args"] == ((tmp_path / ".sldb").resolve(), "pp", True)
    assert [d["ref"] for d in docs] == ["AtomDoc:atom-a", "desk:TaskDoc:task-b"]
    assert docs[0]["path"] == str(tmp_path / "desk/atoms/atom-a.md")
    assert docs[1]["path"] == str(tmp_path / "other" / "desk/tasks/task-b.md")

    payload = resolver._load_store_payload(tmp_path / ".sldb")
    assert list(payload) == ["alpha"]
    assert payload["alpha"]["atoms"]["what"]["id"] == "atom-a"
    assert payload["alpha"]["atoms"]["what"]["tags"] == ["x:y"]
    assert resolver.resolve_ref(tmp_path / ".sldb", "desk:TaskDoc:task-b")["title"] == "Beta"
    assert resolver.resolve_ref(tmp_path / ".sldb", "TaskDoc:nope") is None


def test_store_discovery_uses_a_real_store(tmp_path, monkeypatch):
    import sldb.api

    project = tmp_path / "proj"
    (project / "docs").mkdir(parents=True)
    sldb.api.init_store(project)
    item = SimpleNamespace(anchor_id="v", source_base_dir=str(project / "docs"), src=None, project=None)

    assert SldbAtomResolver()._discover_store_for_item(item) == (project / ".sldb").resolve()
    assert SldbAtomResolver._store_exists(tmp_path) is False


def test_no_internal_sldb_imports():
    src = Path(__file__).resolve().parents[1] / "spec2viz" / "deskops.py"
    text = src.read_text(encoding="utf-8")
    assert "sldb.store" not in text and "sldb.cli" not in text and "sldb.runtime" not in text
