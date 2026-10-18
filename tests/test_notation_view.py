"""`resolve_view`: el unico interprete del contrato de notacion, contra un store real."""
import json
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from spec2viz.cli import main
from spec2viz.notation_view import ViewError, flatten, fragments_of, lookup, render_template, resolve_view

sldb_api = pytest.importorskip("sldb.api")

CLASSES = {
    "id": "shapes", "title": "Shapes", "type": "class", "version": "1",
    "data": {
        "classes": {
            "Shape": {"kind": "interface", "methods": [{"name": "area", "returns": "float"}]},
            "Base": {"kind": "abstract", "attributes": [{"name": "name", "type": "str"}]},
            "Circle": {"label": "Circle", "attributes": [{"name": "r", "type": "float"}], "methods": [{"name": "area", "returns": "float"}]},
        },
        "relations": [
            {"from": "Circle", "to": "Base", "relation": "inheritance"},
            {"from": "Base", "to": "Shape", "relation": "realization"},
            {"from": "Circle", "to": "Shape", "relation": "composition", "label": "parts", "from_multiplicity": "1", "to_multiplicity": "1..*"},
        ],
    },
}
MACHINE = {
    "id": "door", "title": "Door", "type": "state", "version": "1",
    "data": {
        "entity": "Door", "initial": "closed",
        "states": [
            {"id": "closed", "label": "Closed"},
            {"id": "open", "label": "Open", "contains": ["ajar", "wide"]},
            {"id": "ajar", "label": "Ajar"},
            {"id": "wide", "label": "Wide open"},
        ],
        "transitions": [
            {"from": "closed", "to": "open", "on": "push", "guard": "unlocked"},
            {"from": "open", "to": "closed", "on": "pull"},
            {"from": "wide", "to": "closed", "on": "slam"},  # cruza el borde del compuesto
        ],
    },
}


@pytest.fixture
def project(tmp_path):
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "shapes.yml").write_text(yaml.safe_dump(CLASSES), encoding="utf-8")
    (tmp_path / "docs" / "door.yml").write_text(yaml.safe_dump(MACHINE), encoding="utf-8")
    return tmp_path


def test_pure_helpers():
    payload = {"title": "A", "kind": "", "data": {"initial": True, "attributes": [1], "title": "shadow"}}
    assert flatten(payload)["initial"] is True and flatten(payload)["title"] == "A"
    assert lookup(payload, "data.attributes") == [1] and lookup(payload, "data.nope.x") is None
    assert render_template("{title} <{kind}> {missing} {data.initial}", payload) == "A <> True"


def test_class_view_picks_glyphs_by_where_and_links_by_relation(project):
    from spec2viz.sldb_sync import SpecSync

    store = project / ".sldb"
    SpecSync(store).sync(project / "docs" / "shapes.yml")
    view = resolve_view(store, "shapes")
    assert view["notation"] == "NotationDoc:uml-class" and view["layout"] == {"kind": "graph", "direction": "TB"}
    nodes = {n["doc"].split(".")[-1]: n for n in view["nodes"]}
    assert nodes["Shape"]["glyph"] == "GlyphDoc:uml-class.interface" and nodes["Shape"]["keyword"] == "«interface»"
    assert nodes["Base"]["glyph"] == "GlyphDoc:uml-class.abstract" and nodes["Base"]["label_style"] == "italic"
    assert nodes["Circle"]["glyph"] == "GlyphDoc:uml-class.class" and nodes["Circle"]["label"] == "Circle"
    assert [c["path"] for c in nodes["Circle"]["compartments"]] == ["data.attributes", "data.methods"]
    assert nodes["Circle"]["compartments"][0]["items"] == [{"name": "r", "type": "float"}]
    assert [c["path"] for c in nodes["Shape"]["compartments"]] == ["data.methods"]  # sin atributos no hay compartimento
    links = {(l["source"].split(".")[-1], l["target"].split(".")[-1]): l for l in view["links"]}
    assert links[("Circle", "Base")]["target_end"] == "hollow-triangle" and links[("Circle", "Base")]["line"] == "solid"
    assert links[("Base", "Shape")]["line"] == "dashed"
    assert links[("Circle", "Shape")]["source_end"] == "filled-diamond" and links[("Circle", "Shape")]["label"] == "parts"
    assert all(l["draw"] == "line" and l["doc"].startswith("RelationDoc:shapes.") for l in view["links"])
    assert view["skipped"] == [] and view["fragments"] == []
    from spec2viz.sldb_sync import relation_doc_has_attributes
    composition = links[("Circle", "Shape")]
    if relation_doc_has_attributes():  # sldb >= 0.1.11
        assert composition["data"] == {"from_multiplicity": "1", "to_multiplicity": "1..*", "label": "parts"}
        assert (composition["source_label"], composition["target_label"]) == ("1", "1..*")
    else:
        assert composition["data"] == {} and composition["source_label"] == "" and composition["target_label"] == ""


def test_state_view_nests_contains_and_marks_initial(project):
    from spec2viz.sldb_sync import SpecSync

    store = project / ".sldb"
    SpecSync(store).sync(project / "docs" / "door.yml")
    view = resolve_view(store, "SpecDoc:door")
    nodes = {n["doc"].split(".")[-1]: n for n in view["nodes"]}
    assert nodes["open"]["glyph"] == "GlyphDoc:statechart.composite" and nodes["ajar"]["glyph"] == "GlyphDoc:statechart.state"
    assert nodes["closed"]["markers"] == [{"id": "initial", "shape": "filled-circle"}] and nodes["open"]["markers"] == []
    nests = sorted((l["source"].split(".")[-1], l["target"].split(".")[-1]) for l in view["links"] if l["draw"] == "nest")
    assert nests == [("open", "ajar"), ("open", "wide")] and all(l["doc"] is None for l in view["links"] if l["draw"] == "nest")
    lines = {(l["source"].split(".")[-1], l["target"].split(".")[-1]): l["label"] for l in view["links"] if l["draw"] == "line"}
    assert lines == {("closed", "open"): "push [unlocked]", ("open", "closed"): "pull", ("wide", "closed"): "slam"}


def test_repo_pilot_with_a_composite_state_resolves_nest_and_a_crossing_transition(tmp_path):
    """El piloto del repo que graph_ui usa para dibujar `nest`: un compuesto y una transicion que sale de el."""
    from spec2viz.sldb_sync import SpecSync

    sldb_api.init_store(tmp_path)
    SpecSync(tmp_path / ".sldb").sync(Path(__file__).parent.parent / "docs" / "architecture" / "spec2viz" / "state-diagram-sync-lifecycle.yml")
    view = resolve_view(tmp_path / ".sldb", "state.diagram-sync-lifecycle")
    nests = sorted((l["source"].split(".")[-1], l["target"].split(".")[-1]) for l in view["links"] if l["draw"] == "nest")
    assert nests == [("syncing", "indexing"), ("syncing", "validating"), ("syncing", "writing")]
    crossing = [l for l in view["links"] if l["draw"] == "line" and l["source"].endswith(".validating") and l["target"].endswith(".failed")]
    assert len(crossing) == 1 and crossing[0]["label"] == "load() raises [spec invalid]"
    nodes = {n["doc"].split(".")[-1]: n for n in view["nodes"]}
    assert nodes["syncing"]["glyph"] == "GlyphDoc:statechart.composite" and nodes["idle"]["markers"][0]["id"] == "initial"
    assert view["skipped"] == []


def test_fragments_group_consecutive_messages():
    links = [
        {"order": 1, "data": {}}, {"order": 2, "data": {"group": "loop"}}, {"order": 3, "data": {"group": "loop"}},
        {"order": 4, "data": {"group": "alt"}}, {"order": 5, "data": {}}, {"order": 6, "data": {"group": "alt"}}, {"order": 0, "data": {"group": "x"}},
    ]
    assert fragments_of(links) == [
        {"label": "loop", "kind": "group", "orders": [2, 3]},
        {"label": "alt", "kind": "group", "orders": [4]},
        {"label": "alt", "kind": "group", "orders": [6]},
    ]


def test_view_errors(project):
    from spec2viz.sldb_sync import SpecSync

    store = project / ".sldb"
    with pytest.raises(ViewError, match="not in the store"):
        resolve_view(store, "nope")
    SpecSync(store).sync(project / "docs" / "door.yml", notation="none")
    with pytest.raises(ViewError, match="has no notation"):
        resolve_view(store, "door")


def test_cli_view(project):
    from spec2viz.sldb_sync import SpecSync

    store = project / ".sldb"
    SpecSync(store).sync(project / "docs" / "shapes.yml")
    result = CliRunner().invoke(main, ["notation", "view", "shapes", "--store", str(store)])
    assert result.exit_code == 0, result.output
    view = json.loads(result.output)
    assert view["spec"] == "SpecDoc:shapes" and len(view["nodes"]) == 3 and len(view["links"]) == 3
    result = CliRunner().invoke(main, ["notation", "view", "nope", "--store", str(store)])
    assert result.exit_code == 1 and "not in the store" in result.output



REPO = Path(__file__).parent.parent


def test_every_catalog_spec_resolves_under_its_builtin_notation(tmp_path):
    """El catalogo entero sobre graph_ui: cada spec de vistas.yml se sincroniza y resuelve sin skipped."""
    from spec2viz.sldb_sync import SpecSync, sync_catalog

    sldb_api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    reports = sync_catalog(SpecSync(store), REPO / "docs" / "architecture" / "vistas.yml")
    assert len(reports) >= 9 and all(r.edge_errors == [] for r in reports)
    seen_types = set()
    for report in reports:
        view = resolve_view(store, report.spec_id)
        seen_types.add(view["diagram_type"])
        assert view["skipped"] == [], (report.spec_id, view["skipped"])
        assert view["nodes"] and all(n["glyph"] for n in view["nodes"])
    assert {"component", "sequence", "state", "activity", "class", "component_view_matrix"} <= seen_types
    spec_doc = next(d for d in sldb_api.load_runtime_documents(store, None, include_linked=False) if str(d.model_name) == "SpecDoc" and d.name == "component.spec2viz-architecture")
    assert spec_doc.payload["category"] == "Arquitectura de Módulos" and spec_doc.payload["nav"] == "Módulos"


def test_component_wildcard_link_and_sequence_order(tmp_path):
    from spec2viz.sldb_sync import SpecSync

    sldb_api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    (tmp_path / "arq.yml").write_text(yaml.safe_dump({
        "id": "arq", "title": "Arq", "type": "component", "version": "1",
        "data": {"nodes": {"cli": {"label": "CLI", "kind": "entry", "contains": ["core"]}, "core": {"label": "Core"}, "db": {"label": "DB", "kind": "boundary"}},
                 "edges": [{"from": "core", "to": "db", "relation": "reads(sql)", "label": "rows"}, {"from": "cli", "to": "core", "relation": "uses"}]}}), encoding="utf-8")
    (tmp_path / "seq.yml").write_text(yaml.safe_dump({
        "id": "seq", "title": "Seq", "type": "sequence", "version": "1",
        "data": {"participants": [{"id": "U", "kind": "actor"}, {"id": "S", "kind": "component"}],
                 "messages": [{"from": "U", "to": "S", "message": "first"}, {"from": "S", "to": "U", "message": "second", "kind": "return"}, {"from": "U", "to": "S", "message": "third", "kind": "async"}]}}), encoding="utf-8")
    sync = SpecSync(store)
    sync.sync(tmp_path / "arq.yml")
    sync.sync(tmp_path / "seq.yml")

    arq = resolve_view(store, "arq")
    nodes = {n["element"]: n for n in arq["nodes"]}
    assert nodes["cli"]["glyph"] == "GlyphDoc:component.entry" and nodes["db"]["glyph"] == "GlyphDoc:component.boundary" and nodes["core"]["collection"] == "nodes"
    links = [(l["source"].split(".")[-1], l["target"].split(".")[-1], l["relation"], l["draw"], l["label"], l["order"]) for l in arq["links"]]
    assert links == [("cli", "core", "contains", "nest", "", 0), ("core", "db", "reads_sql", "line", "reads_sql rows", 1), ("cli", "core", "uses", "line", "uses", 2)]
    assert all(l["link"] == "LinkDoc:component.relation" for l in arq["links"] if l["draw"] == "line")

    seq = resolve_view(store, "seq")
    assert seq["layout"] == {"kind": "lanes", "direction": "LR"}
    assert [(l["order"], l["relation"], l["line"], l["target_end"], l["label"]) for l in seq["links"]] == [
        (1, "sends", "solid", "filled-arrow", "first"), (2, "returns", "dashed", "open-arrow", "second"), (3, "sends_async", "solid", "open-arrow", "third")]
    assert {n["element"]: n["glyph"].split(".")[-1] for n in seq["nodes"]} == {"U": "actor", "S": "participant"}


def test_activity_and_matrix_views(tmp_path):
    from spec2viz.sldb_sync import SpecSync

    sldb_api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    sync = SpecSync(store)
    sync.sync(REPO / "docs" / "architecture" / "spec2viz" / "activity-render-error-handling.yml")
    sync.sync(REPO / "tests" / "fixtures" / "matrix.quotation-view.yml")

    act = resolve_view(store, "activity.render-error-handling")
    glyphs = {n["element"]: n["glyph"].split(".")[-1] for n in act["nodes"]}
    assert glyphs["receive_paths"] == "start" and glyphs["iterate_path"] == "decision" and glyphs["try_render"] == "action" and "end" in glyphs.values()
    branch = next(l for l in act["links"] if l["relation"] == "branch" and l["source"].endswith(".iterate_path") and l["target"].endswith(".try_render"))
    assert branch["label"] == "[has_next]" and act["skipped"] == []

    mat = resolve_view(store, "matrix.quotation-view")
    assert mat["layout"] == {"kind": "grid"}
    stages = [n for n in mat["nodes"] if n["collection"] == "stages"]
    assert [s["data"]["order"] for s in stages] == [1, 2, 3, 4, 5] and stages[0]["glyph"] == "GlyphDoc:component-view-matrix.stage"
    cells = [l for l in mat["links"] if l["draw"] == "cell"]
    nests = [l for l in mat["links"] if l["draw"] == "nest"]
    assert cells and nests and all(c["label"] == "quotation" for c in cells) and mat["skipped"] == []
