"""Notaciones: gramatica del YAML, builtins y su sincronizacion al store."""
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from spec2viz.cli import main
from spec2viz.exceptions import ValidationError
from spec2viz.notation import DEFAULT_NOTATIONS, NotationSpec, builtin_notations, load_notation

MINIMAL = {
    "name": "mini",
    "diagram_type": "class",
    "glyphs": [{"id": "box", "model": "SpecNodeDoc", "shape": "class-box"}],
    "links": [{"id": "inh", "relation": "inheritance", "target_end": "hollow-triangle"}],
}


def _with(**changes) -> dict:
    raw = yaml.safe_load(yaml.safe_dump(MINIMAL))
    raw.update(changes)
    return raw


# --- gramatica ------------------------------------------------------------------------

def test_builtins_load_and_cover_every_diagram_type():
    from spec2viz.models.base import DiagramType

    names = set(builtin_notations())
    assert set(DEFAULT_NOTATIONS.values()) == names and set(DEFAULT_NOTATIONS) == {t.value for t in DiagramType}
    for name in names:
        spec = load_notation(name)
        assert spec.name == name and spec.glyphs and DEFAULT_NOTATIONS[spec.diagram_type] == name


def test_wildcard_link_and_free_relations():
    spec = NotationSpec.model_validate(_with(diagram_type="component", links=[{"id": "any", "relation": "*"}, {"id": "c", "relation": "contains", "draw": "nest"}]))
    assert spec.relations == ["contains"]
    with pytest.raises(Exception, match="never emits"):
        NotationSpec.model_validate(_with(links=[{"id": "l", "relation": "uses"}]))
    with pytest.raises(Exception, match="vocabulary token"):
        NotationSpec.model_validate(_with(links=[{"id": "l", "relation": "Uses It"}]))


def test_uml_class_notation_matches_the_class_spec_vocabulary():
    spec = load_notation("uml-class")
    # `contains` anida los paquetes UML (glifo `package`, coleccion `packages`)
    assert spec.relations == ["contains", "inheritance", "realization", "composition", "aggregation", "association", "dependency"]
    assert [g.id for g in spec.glyphs][-1] == "class" and spec.glyphs[-1].where == ""
    assert spec.glyphs[0].id == "package" and spec.glyphs[0].shape == "package" and spec.glyphs[0].where == 'collection = "packages"'
    assert spec.glyphs[1].where == 'kind = "interface"' and spec.glyphs[1].keyword == "«interface»"
    assert {l.id: l.draw for l in spec.links}["contains"] == "nest"
    assert {l.id: (l.draw, l.line, l.source_end, l.target_end) for l in spec.links}["composition"] == ("line", "solid", "filled-diamond", "none")


def test_statechart_nests_contains_and_marks_the_initial_state():
    spec = load_notation("statechart")
    links = {l.relation: l for l in spec.links}
    assert links["contains"].draw == "nest" and links["transitions_to"].draw == "line"
    assert spec.markers[0].model_dump() == {"id": "initial", "shape": "filled-circle", "model": "SpecNodeDoc", "where": "has(initial)"}
    assert spec.glyphs[0].where == "nonempty(contains)"


def test_minimal_notation_defaults():
    spec = NotationSpec.model_validate(MINIMAL)
    assert spec.level == "types" and spec.layout == {"kind": "graph"} and spec.projection == "all"
    assert spec.links[0].draw == "line" and spec.links[0].line == "solid" and spec.links[0].source_end == "none"
    assert spec.models == ["SpecNodeDoc"] and spec.relations == ["inheritance"]


@pytest.mark.parametrize(
    "changes, message",
    [
        ({"name": "Mini Notation"}, "notation name"),
        ({"diagram_type": "mindmap"}, "not a spec2viz diagram type"),
        ({"level": "all"}, "level"),
        ({"layout": {"kind": "force"}}, "layout.kind"),
        ({"layout": {"kind": "graph", "direction": "UP"}}, "layout.direction"),
        ({"glyphs": []}, "glyphs"),
        ({"glyphs": [{"id": "a", "model": "SpecNodeDoc", "shape": "x", "where": 'kind = "a"'}]}, "no default glyph"),
        ({"glyphs": [{"id": "a", "model": "SpecNodeDoc", "shape": "x"}, {"id": "a", "model": "SpecNodeDoc", "shape": "y"}]}, "more than once"),
        ({"glyphs": [{"id": "a", "model": "SpecNodeDoc", "shape": "x", "where": "kind = = 1"}]}, "does not parse"),
        ({"links": [{"id": "l", "relation": "uses"}]}, "never emits"),
        ({"links": [{"id": "l", "relation": "inheritance", "draw": "curve"}]}, "draw"),
        ({"links": [{"id": "l", "relation": "inheritance", "target_end": "spear"}]}, "terminal"),
        ({"links": [{"id": "l", "relation": "inheritance", "model": "AssocDoc"}]}, "declares no ends"),
        ({"links": [{"id": "l", "relation": "inheritance"}, {"id": "m", "relation": "inheritance"}]}, "more than one link"),
        ({"glyphs": [{"id": "a", "model": "SpecNodeDoc", "shape": "x", "colour": "red"}]}, "colour"),
    ],
)
def test_invalid_notations_are_rejected(changes, message):
    with pytest.raises(Exception) as excinfo:
        NotationSpec.model_validate(_with(**changes))
    assert message in str(excinfo.value)


def test_free_relation_diagram_types_accept_any_relation():
    spec = NotationSpec.model_validate(_with(diagram_type="component", links=[{"id": "l", "relation": "loads_path"}]))
    assert spec.relations == ["loads_path"]


def test_load_notation_from_path_and_unknown_name(tmp_path):
    path = tmp_path / "mine.yml"
    path.write_text(yaml.safe_dump(MINIMAL), encoding="utf-8")
    assert load_notation(path).name == "mini"
    with pytest.raises(ValidationError, match="unknown notation"):
        load_notation("nope")
    path.write_text("- not\n- a mapping\n", encoding="utf-8")
    with pytest.raises(ValidationError, match="a mapping"):
        load_notation(path)


# --- CLI sin store ----------------------------------------------------------------------

def test_cli_list_and_validate(tmp_path):
    runner = CliRunner()
    result = runner.invoke(main, ["notation", "list"])
    assert result.exit_code == 0 and "uml-class: class" in result.output and "statechart: state" in result.output
    result = runner.invoke(main, ["notation", "validate", "uml-class"])
    assert result.exit_code == 0 and "Valid: uml-class" in result.output
    bad = tmp_path / "bad.yml"
    bad.write_text(yaml.safe_dump(_with(level="all")), encoding="utf-8")
    result = runner.invoke(main, ["notation", "validate", str(bad)])
    assert result.exit_code == 1 and "Invalid" in result.output


# --- contra un store real ---------------------------------------------------------------

sldb_api = pytest.importorskip("sldb.api")


@pytest.fixture
def store(tmp_path):
    sldb_api.init_store(tmp_path)
    return tmp_path / ".sldb"


def test_notation_sync_writes_docs_and_edges(store):
    from spec2viz.sldb_sync import NotationSync

    report = NotationSync(store).sync("statechart")
    assert sorted(report.created) == [
        "GlyphDoc:statechart.composite", "GlyphDoc:statechart.state",
        "LinkDoc:statechart.substate", "LinkDoc:statechart.transition",
        "NotationDoc:statechart",
    ]
    assert report.relation_types_added == ["transitions_to"]  # `contains` es builtin
    assert report.unresolved == [] and report.edge_errors == []
    root = store.parent
    assert (root / "sldb" / "notations" / "statechart" / "notation.md").exists()
    assert (root / "sldb" / "notations" / "statechart" / "glyphs" / "composite.md").exists()
    assert (root / "sldb" / "notations" / "statechart" / "links" / "transition.md").exists()

    notation = yaml.safe_load((root / "sldb" / "notations" / "statechart" / "notation.md").read_text(encoding="utf-8").split("---")[1])
    assert notation["layout"] == {"kind": "graph", "direction": "LR"} and notation["markers"][0]["where"] == "has(initial)"
    assert notation["glyphs"] == ["GlyphDoc:statechart.composite", "GlyphDoc:statechart.state"]

    rels = sorted((r.relation, r.target) for r in sldb_api.edges_from(store, "NotationDoc:statechart") if r.relation == "references")
    assert ("references", "sldb://document/GlyphDoc:statechart.state") in rels
    assert ("references", "sldb://document/LinkDoc:statechart.transition") in rels
    link_rels = {(r.relation, r.target) for r in sldb_api.edges_from(store, "LinkDoc:statechart.transition")}
    assert ("references", "sldb://relation_type/transitions_to") in link_rels
    assert ("references", "sldb://document/NotationDoc:statechart") in link_rels


def test_notation_sync_is_idempotent_and_prunes(store, tmp_path):
    from spec2viz.sldb_sync import NotationSync

    sync = NotationSync(store)
    path = tmp_path / "mini.yml"
    path.write_text(yaml.safe_dump(MINIMAL), encoding="utf-8")
    first = sync.sync(path)
    again = sync.sync(path)
    assert first.created and again.created == [] and len(again.updated) == 3 and again.deleted == []

    smaller = yaml.safe_load(yaml.safe_dump(MINIMAL))
    smaller["links"] = []
    path.write_text(yaml.safe_dump(smaller), encoding="utf-8")
    pruned = sync.sync(path)
    assert pruned.deleted == ["LinkDoc:mini.inh"] and not sldb_api.doc_exists(store, "LinkDoc/mini.inh")


def test_notation_naming_an_unregistered_model_is_reported(store, tmp_path):
    from spec2viz.sldb_sync import NotationSync

    path = tmp_path / "other.yml"
    path.write_text(yaml.safe_dump(_with(name="other", glyphs=[{"id": "b", "model": "ClassDoc", "shape": "box"}])), encoding="utf-8")
    report = NotationSync(store).sync(path)
    assert report.unresolved == ["notation other: model 'ClassDoc' is not registered in the store"]


def test_cli_notation_sync(store):
    runner = CliRunner()
    result = runner.invoke(main, ["notation", "sync", "uml-class", "--store", str(store), "--strict"])
    assert result.exit_code == 0, result.output
    assert "Synced notation uml-class: 7 glyphs, 7 links (15 created" in result.output
    result = runner.invoke(main, ["notation", "sync", "nope", "--store", str(store)])
    assert result.exit_code == 1 and "unknown notation" in result.output


def test_wildcard_link_leaves_no_dangling_relation_type(store):
    from spec2viz.sldb_sync import NotationSync

    report = NotationSync(store).sync("component")
    assert report.unresolved == [] and report.edge_errors == []
    link = yaml.safe_load((store.parent / "sldb" / "notations" / "component" / "links" / "relation.md").read_text(encoding="utf-8").split("---")[1])
    assert link["relation"] == "*" and link["relation_type"] == ""
    targets = {r.target for r in sldb_api.edges_from(store, "LinkDoc:component.relation") if r.relation == "references"}
    assert targets == {"sldb://document/NotationDoc:component"}
