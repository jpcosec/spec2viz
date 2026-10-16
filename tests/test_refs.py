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


def _fake_store(monkeypatch):
    monkeypatch.setattr(SldbAtomResolver, "_discover_store_for_item", lambda self, item: Path("/s/.sldb"))
    monkeypatch.setattr(SldbAtomResolver, "_load_store_documents", lambda self, store: list(FAKE_DOCS))


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
        "path": "/s/desk/tasks/task-x.md", "store": "/s/.sldb", "summary": "Resumen de X",
    }
    assert refs[1]["summary"] == "Respuesta Y"


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
