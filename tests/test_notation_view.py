"""`resolve_view`: el unico interprete del contrato de notacion, contra un store real."""
import json

import pytest
import yaml
from click.testing import CliRunner

from spec2viz.cli import main
from spec2viz.notation_view import ViewError, flatten, lookup, render_template, resolve_view

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
            {"from": "Circle", "to": "Shape", "relation": "composition", "label": "parts"},
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
    assert view["skipped"] == []


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
    assert lines == {("closed", "open"): "push [unlocked]", ("open", "closed"): "pull"}


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
