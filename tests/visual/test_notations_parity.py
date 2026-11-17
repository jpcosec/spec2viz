"""spec2viz's notation, palette and view tests, ported to run against sldb (IR13e).

The notations, palettes, the view contract (`resolve_view`) and its sync to the store are sldb's
(D1, D3): this file runs, against sldb and never against spec2viz, the cases of spec2viz's
`tests/test_view_doc.py` (3), `test_notation.py` (12 of 14), `test_notation_view.py` (10 of 11),
`test_view_contract_resolved.py` (2) and `test_style_palette.py` (15 of 16), revision b624b75:
42 ported tests, plus the 9 «valida igual» comparisons, 51 test functions.
The 6 tests that invoke spec2viz's CLI (`test_cli_list_and_validate`, `test_cli_notation_sync`,
`test_cli_view`, `test_notation_validate_gives_typed_errors`, `test_palette_validation_is_typed`,
`test_palette_cli_sync_writes_the_store_document`) are not ported whole: their CLI half is rows
SV-K of the coverage matrix, credited by `tests/visual/test_cli.py`. The typed validation that two
of them also check without the CLI is ported (`test_notation_load_gives_typed_errors`, 7 cases, and
`test_palette_check_is_typed`, 6 cases).

Each ported test names, in its docstring, the spec2viz test it comes from. Only the imports
change: the store, the sync and the view resolver come from `sldb.api` (`sldb.api.notations`);
what `sldb.api` does not export yet (`load_notation`, `NotationSpec`, `load_palette`, `PaletteSpec`,
`check_palette`, `contrast`, `resolve_color`, `resolve_style`, `SHAPES`, `DiagramType`,
`DEFAULT_NOTATIONS`, `builtin_notations` and the typed errors) is taken from
`specir.visual.notation_style`, the one module of specIR allowed to reach `sldb.notations`; the
mermaid and PlantUML renderers are specIR's (`specir.visual.renderers`), over sldb's spec loader.

The fixtures are spec2viz's, copied: its 8 builtin notations and its `default` palette in
`fixtures/spec2viz-notations/` (revision b624b75), its specs in `fixtures/spec2viz/` and its
catalog (`docs/architecture/vistas.yml` with its specs) in `fixtures/catalog/`.

The 9 «valida igual» comparisons check that each notation and the palette copied from spec2viz
load and validate with sldb, and that their `model_dump()` equals that of sldb's builtin of the
same name."""

from __future__ import annotations

import copy
import re
import shutil
from pathlib import Path

import pytest
import sldb.api as sldb_api
import yaml
from sldb.api import ViewDoc
from sldb.api.notations import (
    NotationSync,
    SpecSync,
    ViewError,
    flatten,
    fragments_of,
    lookup,
    render_keyword,
    render_template,
    resolve_documents,
    resolve_view,
)
from sldb.api.notations import load_spec as load
from sldb.api.notations import validate_spec as validate

from specir.visual.compilers import compile_ir
from specir.visual.notation_style import (
    DEFAULT_NOTATIONS,
    SHAPES,
    DiagramType,
    InvalidColorError,
    NotationSpec,
    PaletteSpec,
    UnknownIconError,
    UnknownKindError,
    UnknownShapeError,
    ValidationError,
    builtin_notations,
    check_palette,
    contrast,
    load_notation,
    load_palette,
    resolve_color,
    resolve_style,
)
from specir.visual.renderers.mermaid import MermaidRenderer
from specir.visual.renderers.plantuml import PlantUMLRenderer

HERE = Path(__file__).parent
NOTATION_COPIES = HERE / "fixtures" / "spec2viz-notations"
#: spec2viz's repository as copied into IR: its `tests/fixtures/` and `docs/architecture/spec2viz/`.
SPEC2VIZ = HERE / "fixtures" / "spec2viz"
#: spec2viz's catalog (`docs/architecture/vistas.yml` and the specs it lists), as copied into IR.
CATALOG = HERE / "fixtures" / "catalog"
FIXTURES = SPEC2VIZ / "tests" / "fixtures"
SPEC2VIZ_NOTATIONS = ("activity", "component", "component-view-matrix", "deployment", "reflection", "statechart", "uml-class", "uml-sequence")


def _front(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8").split("---")[1])


# ==================================================================================================
# «valida igual»: the notations and the palette copied from spec2viz against sldb's builtins
# ==================================================================================================

@pytest.mark.parametrize("name", SPEC2VIZ_NOTATIONS)
def test_spec2viz_notation_validates_the_same_as_the_sldb_builtin(name):
    """«valida igual»: the notation copied from spec2viz loads and validates with sldb, and its
    content equals that of sldb's builtin of the same name."""
    copied = load_notation(NOTATION_COPIES / "notations" / f"{name}.yml")
    assert name in builtin_notations()
    assert copied.model_dump() == load_notation(name).model_dump()


def test_spec2viz_default_palette_validates_the_same_as_the_sldb_builtin():
    """«valida igual»: the `default` palette copied from spec2viz loads and validates with sldb
    (`load_palette` runs `check_palette`), and its content equals that of sldb's builtin `default`."""
    copied = load_palette(NOTATION_COPIES / "palettes" / "default.yml")
    assert copied.model_dump() == load_palette("default").model_dump()


# ==================================================================================================
# spec2viz tests/test_view_doc.py
# ==================================================================================================

VIEW_BASE = {"id": "atoms-by-task", "name": "atoms-by-task", "title": "Atoms by task"}


def test_defaults_and_shape():
    """spec2viz tests/test_view_doc.py::test_defaults_and_shape."""
    v = ViewDoc.model_validate(VIEW_BASE)
    assert v.nodes == [] and v.relations == [] and v.direction == "both" and v.notation == "" and v.layout == {}
    v = ViewDoc.model_validate({**VIEW_BASE, "nodes": [{"model": "TaskDoc"}, {"model": "AtomDoc", "where": 'five_wh_one_plus = "why"'}],
                                "relations": ["references"], "direction": "outgoing", "notation": "NotationDoc:component",
                                "layout": {"kind": "graph", "style": "rings", "ring_field": "status"}})
    assert v.nodes == [{"model": "TaskDoc", "where": ""}, {"model": "AtomDoc", "where": 'five_wh_one_plus = "why"'}]
    assert v.layout["style"] == "rings"


@pytest.mark.parametrize("changes, message", [
    ({"direction": "up"}, "direction"),
    ({"nodes": [{"where": "x"}]}, "needs a model"),
    ({"nodes": [{"model": "A", "id": "SpecNodeDoc:x"}]}, "only take model and where"),
    ({"layout": {"style": "force"}}, "layout.style"),
])
def test_invalid(changes, message):
    """spec2viz tests/test_view_doc.py::test_invalid."""
    with pytest.raises(Exception, match=message):
        ViewDoc.model_validate({**VIEW_BASE, **changes})


def test_view_doc_in_a_store_references_its_notation(tmp_path):
    """spec2viz tests/test_view_doc.py::test_view_doc_in_a_store_references_its_notation."""
    sldb_api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    NotationSync(store).sync("component")
    payload = {**VIEW_BASE, "nodes": [{"model": "SpecNodeDoc", "where": 'kind = "entry"'}], "relations": ["uses"],
               "direction": "both", "notation": "NotationDoc:component", "layout": {"style": "layered"}, "description": "entry points"}
    sldb_api.create_document(store, "ViewDoc", tmp_path / "sldb" / "views" / "atoms-by-task.md", payload, name="atoms-by-task")
    sldb_api.rebuild_edges(store)
    front = _front(tmp_path / "sldb" / "views" / "atoms-by-task.md")
    assert front["nodes"] == [{"model": "SpecNodeDoc", "where": 'kind = "entry"'}] and front["notation"] == "NotationDoc:component"
    targets = {r.target for r in sldb_api.edges_from(store, "ViewDoc:atoms-by-task") if r.relation == "references"}
    assert targets == {"sldb://document/NotationDoc:component"}
    assert sldb_api.check_edges(store).errors == []


# ==================================================================================================
# spec2viz tests/test_notation.py
# ==================================================================================================

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


def test_builtins_load_and_cover_every_diagram_type():
    """spec2viz tests/test_notation.py::test_builtins_load_and_cover_every_diagram_type."""
    names = set(builtin_notations())
    assert set(DEFAULT_NOTATIONS.values()) == names and set(DEFAULT_NOTATIONS) == {t.value for t in DiagramType}
    for name in names:
        spec = load_notation(name)
        assert spec.name == name and spec.glyphs and DEFAULT_NOTATIONS[spec.diagram_type] == name


def test_wildcard_link_and_free_relations():
    """spec2viz tests/test_notation.py::test_wildcard_link_and_free_relations."""
    spec = NotationSpec.model_validate(_with(diagram_type="component", links=[{"id": "any", "relation": "*"}, {"id": "c", "relation": "contains", "draw": "nest"}]))
    assert spec.relations == ["contains"]
    with pytest.raises(Exception, match="never emits"):
        NotationSpec.model_validate(_with(links=[{"id": "l", "relation": "uses"}]))
    with pytest.raises(Exception, match="vocabulary token"):
        NotationSpec.model_validate(_with(links=[{"id": "l", "relation": "Uses It"}]))


def test_uml_class_notation_matches_the_class_spec_vocabulary():
    """spec2viz tests/test_notation.py::test_uml_class_notation_matches_the_class_spec_vocabulary."""
    spec = load_notation("uml-class")
    assert spec.relations == ["contains", "inheritance", "realization", "composition", "aggregation", "association", "dependency"]
    assert [g.id for g in spec.glyphs][-1] == "class" and spec.glyphs[-1].where == ""
    assert spec.glyphs[0].id == "package" and spec.glyphs[0].shape == "package" and spec.glyphs[0].where == 'collection = "packages"'
    assert spec.glyphs[1].where == 'kind = "interface"' and spec.glyphs[1].keyword == "«interface»"
    assert {l.id: l.draw for l in spec.links}["contains"] == "nest"
    assert {l.id: (l.draw, l.line, l.source_end, l.target_end) for l in spec.links}["composition"] == ("line", "solid", "filled-diamond", "none")


def test_statechart_nests_contains_and_marks_the_initial_state():
    """spec2viz tests/test_notation.py::test_statechart_nests_contains_and_marks_the_initial_state."""
    spec = load_notation("statechart")
    links = {l.relation: l for l in spec.links}
    assert links["contains"].draw == "nest" and links["transitions_to"].draw == "line"
    assert spec.markers[0].model_dump() == {"id": "initial", "shape": "filled-circle", "model": "SpecNodeDoc", "where": "has(initial)"}
    assert spec.glyphs[0].where == "nonempty(contains)"


def test_minimal_notation_defaults():
    """spec2viz tests/test_notation.py::test_minimal_notation_defaults."""
    spec = NotationSpec.model_validate(MINIMAL)
    assert spec.level == "types" and spec.layout == {"kind": "graph"} and spec.projection == "all"
    assert spec.links[0].draw == "line" and spec.links[0].line == "solid" and spec.links[0].source_end == "none"
    assert spec.models == ["SpecNodeDoc"] and spec.relations == ["inheritance"]


@pytest.mark.parametrize(
    "changes, message",
    [
        ({"name": "Mini Notation"}, "notation name"),
        ({"diagram_type": "mindmap"}, "diagram_type 'mindmap' is not a valid diagram type"),
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
    """spec2viz tests/test_notation.py::test_invalid_notations_are_rejected.

    The unknown diagram_type case (`mindmap`) expects sldb's message, "diagram_type 'mindmap' is not
    a valid diagram type", not spec2viz's "not a spec2viz diagram type": sldb keeps its message as the
    contract (sldb's answer in IR's inbox note 20261116-232335, to IR13e's note 20261116-022332)."""
    with pytest.raises(Exception) as excinfo:
        NotationSpec.model_validate(_with(**changes))
    assert message in str(excinfo.value)


def test_free_relation_diagram_types_accept_any_relation():
    """spec2viz tests/test_notation.py::test_free_relation_diagram_types_accept_any_relation."""
    spec = NotationSpec.model_validate(_with(diagram_type="component", links=[{"id": "l", "relation": "loads_path"}]))
    assert spec.relations == ["loads_path"]


def test_load_notation_from_path_and_unknown_name(tmp_path):
    """spec2viz tests/test_notation.py::test_load_notation_from_path_and_unknown_name."""
    path = tmp_path / "mine.yml"
    path.write_text(yaml.safe_dump(MINIMAL), encoding="utf-8")
    assert load_notation(path).name == "mini"
    with pytest.raises(ValidationError, match="unknown notation"):
        load_notation("nope")
    path.write_text("- not\n- a mapping\n", encoding="utf-8")
    with pytest.raises(ValidationError, match="a mapping"):
        load_notation(path)


@pytest.fixture
def store(tmp_path):
    sldb_api.init_store(tmp_path)
    return tmp_path / ".sldb"


def test_notation_sync_writes_docs_and_edges(store):
    """spec2viz tests/test_notation.py::test_notation_sync_writes_docs_and_edges."""
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

    notation = _front(root / "sldb" / "notations" / "statechart" / "notation.md")
    assert notation["layout"] == {"kind": "graph", "direction": "LR"} and notation["markers"][0]["where"] == "has(initial)"
    assert notation["glyphs"] == ["GlyphDoc:statechart.composite", "GlyphDoc:statechart.state"]

    rels = sorted((r.relation, r.target) for r in sldb_api.edges_from(store, "NotationDoc:statechart") if r.relation == "references")
    assert ("references", "sldb://document/GlyphDoc:statechart.state") in rels
    assert ("references", "sldb://document/LinkDoc:statechart.transition") in rels
    link_rels = {(r.relation, r.target) for r in sldb_api.edges_from(store, "LinkDoc:statechart.transition")}
    assert ("references", "sldb://relation_type/transitions_to") in link_rels
    assert ("references", "sldb://document/NotationDoc:statechart") in link_rels


def test_notation_sync_is_idempotent_and_prunes(store, tmp_path):
    """spec2viz tests/test_notation.py::test_notation_sync_is_idempotent_and_prunes."""
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
    """spec2viz tests/test_notation.py::test_notation_naming_an_unregistered_model_is_reported."""
    path = tmp_path / "other.yml"
    path.write_text(yaml.safe_dump(_with(name="other", glyphs=[{"id": "b", "model": "ClassDoc", "shape": "box"}])), encoding="utf-8")
    report = NotationSync(store).sync(path)
    assert report.unresolved == ["notation other: model 'ClassDoc' is not registered in the store"]


def test_wildcard_link_leaves_no_dangling_relation_type(store):
    """spec2viz tests/test_notation.py::test_wildcard_link_leaves_no_dangling_relation_type."""
    report = NotationSync(store).sync("component")
    assert report.unresolved == [] and report.edge_errors == []
    link = _front(store.parent / "sldb" / "notations" / "component" / "links" / "relation.md")
    assert link["relation"] == "*" and link["relation_type"] == ""
    targets = {r.target for r in sldb_api.edges_from(store, "LinkDoc:component.relation") if r.relation == "references"}
    assert targets == {"sldb://document/NotationDoc:component"}


# ==================================================================================================
# spec2viz tests/test_notation_view.py
# ==================================================================================================

def _in_project(tmp_path: Path, rel: str, source_root: Path = SPEC2VIZ) -> Path:
    """Copy of a spec of spec2viz's repo (or of vistas.yml with every spec it lists) inside the
    temporary project, at the same relative path (spec2viz's helper, over the copies in IR)."""
    source = source_root / rel
    if source.name == "vistas.yml":
        shutil.copytree(source.parent, tmp_path / rel.rsplit("/", 1)[0], dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("sldb", "*.md", "*.html", "*.svg", "*.puml", "*.mmd"))
    else:
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, tmp_path / rel)
    return tmp_path / rel


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
    """spec2viz tests/test_notation_view.py::test_pure_helpers."""
    payload = {"title": "A", "kind": "", "data": {"initial": True, "attributes": [1], "title": "shadow"}}
    assert flatten(payload)["initial"] is True and flatten(payload)["title"] == "A"
    assert lookup(payload, "data.attributes") == [1] and lookup(payload, "data.nope.x") is None
    assert render_template("{title} <{kind}> {missing} {data.initial}", payload) == "A <> True"


def test_class_view_picks_glyphs_by_where_and_links_by_relation(project):
    """spec2viz tests/test_notation_view.py::test_class_view_picks_glyphs_by_where_and_links_by_relation.

    spec2viz asserted the multiplicities of the composition only when the installed sldb stored
    relation attributes (`relation_doc_has_attributes()`, sldb >= 0.1.11); sldb stores them, so
    that branch is the one that runs here."""
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
    composition = links[("Circle", "Shape")]
    assert composition["data"] == {"from_multiplicity": "1", "to_multiplicity": "1..*", "label": "parts"}
    assert (composition["source_label"], composition["target_label"]) == ("1", "1..*")


def test_state_view_nests_contains_and_marks_initial(project):
    """spec2viz tests/test_notation_view.py::test_state_view_nests_contains_and_marks_initial."""
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
    """spec2viz tests/test_notation_view.py::test_repo_pilot_with_a_composite_state_resolves_nest_and_a_crossing_transition."""
    sldb_api.init_store(tmp_path)
    SpecSync(tmp_path / ".sldb").sync(_in_project(tmp_path, "docs/architecture/spec2viz/state-diagram-sync-lifecycle.yml"))
    view = resolve_view(tmp_path / ".sldb", "state.diagram-sync-lifecycle")
    nests = sorted((l["source"].split(".")[-1], l["target"].split(".")[-1]) for l in view["links"] if l["draw"] == "nest")
    assert nests == [("syncing", "indexing"), ("syncing", "validating"), ("syncing", "writing")]
    crossing = [l for l in view["links"] if l["draw"] == "line" and l["source"].endswith(".validating") and l["target"].endswith(".failed")]
    assert len(crossing) == 1 and crossing[0]["label"] == "load() raises [spec invalid]"
    nodes = {n["doc"].split(".")[-1]: n for n in view["nodes"]}
    assert nodes["syncing"]["glyph"] == "GlyphDoc:statechart.composite" and nodes["idle"]["markers"][0]["id"] == "initial"
    assert view["skipped"] == []


def test_fragments_group_consecutive_messages():
    """spec2viz tests/test_notation_view.py::test_fragments_group_consecutive_messages."""
    links = [
        {"order": 1, "data": {}}, {"order": 2, "data": {"group": "loop"}}, {"order": 3, "data": {"group": "loop"}},
        {"order": 4, "data": {"group": "alt"}}, {"order": 5, "data": {}}, {"order": 6, "data": {"group": "alt"}}, {"order": 0, "data": {"group": "x"}},
    ]
    assert fragments_of(links) == [
        {"label": "", "kind": "loop", "group": "loop", "orders": [2, 3]},
        {"label": "", "kind": "alt", "group": "alt", "orders": [4]},
        {"label": "", "kind": "alt", "group": "alt", "orders": [6]},
    ]
    assert fragments_of([{"order": 1, "data": {"group": "Loop for each spec"}}, {"order": 2, "data": {"group": "retries"}}]) == [
        {"label": "for each spec", "kind": "loop", "group": "Loop for each spec", "orders": [1]},
        {"label": "retries", "kind": "group", "group": "retries", "orders": [2]},
    ]


def test_repo_sequence_pilot_has_loop_and_alt_fragments(tmp_path):
    """spec2viz tests/test_notation_view.py::test_repo_sequence_pilot_has_loop_and_alt_fragments."""
    sldb_api.init_store(tmp_path)
    SpecSync(tmp_path / ".sldb").sync(_in_project(tmp_path, "docs/architecture/spec2viz/sequence-sync-pipeline.yml"))
    view = resolve_view(tmp_path / ".sldb", "sequence.sync-pipeline")
    kinds = [(f["kind"], f["label"]) for f in view["fragments"]]
    assert kinds == [("loop", "for each spec"), ("alt", "the diagram type has a notation"), ("loop", "for each spec")]
    loop = view["fragments"][0]
    by_order = {l["order"]: l for l in view["links"]}
    participants = {by_order[o][end].split(".")[-1] for o in loop["orders"] for end in ("source", "target")}
    assert len(participants) >= 3 and view["skipped"] == []


def test_view_errors(project):
    """spec2viz tests/test_notation_view.py::test_view_errors."""
    store = project / ".sldb"
    with pytest.raises(ViewError, match="not in the store"):
        resolve_view(store, "nope")
    SpecSync(store).sync(project / "docs" / "door.yml", notation="none")
    with pytest.raises(ViewError, match="has no notation"):
        resolve_view(store, "door")


def test_every_catalog_spec_resolves_under_its_builtin_notation(tmp_path):
    """spec2viz tests/test_notation_view.py::test_every_catalog_spec_resolves_under_its_builtin_notation.

    spec2viz's `docs/architecture/vistas.yml` and its specs, as copied into IR (`fixtures/catalog/`)."""
    from sldb.api.notations import sync_catalog

    sldb_api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    reports = sync_catalog(SpecSync(store), _in_project(tmp_path, "docs/architecture/vistas.yml", CATALOG))
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
    """spec2viz tests/test_notation_view.py::test_component_wildcard_link_and_sequence_order."""
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
    """spec2viz tests/test_notation_view.py::test_activity_and_matrix_views."""
    sldb_api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    sync = SpecSync(store)
    sync.sync(_in_project(tmp_path, "docs/architecture/spec2viz/activity-render-error-handling.yml"))
    sync.sync(_in_project(tmp_path, "tests/fixtures/matrix.quotation-view.yml"))

    act = resolve_view(store, "activity.render-error-handling")
    glyphs = {n["element"]: n["glyph"].split(".")[-1] for n in act["nodes"]}
    assert glyphs["__initial"] == "start" and glyphs["receive_paths"] == "action" and glyphs["iterate_path"] == "decision"
    assert glyphs["try_render"] == "action" and glyphs["__final"] == "end" and glyphs["done"] == "action"
    start = next(n for n in act["nodes"] if n["element"] == "__initial")
    assert start["label"] == ""  # label: "" explicito en el glifo: sin rotulo
    branch = next(l for l in act["links"] if l["relation"] == "branch" and l["source"].endswith(".iterate_path") and l["target"].endswith(".try_render"))
    assert branch["label"] == "[has_next]" and act["skipped"] == []

    mat = resolve_view(store, "matrix.quotation-view")
    assert mat["layout"] == {"kind": "grid"}
    stages = [n for n in mat["nodes"] if n["collection"] == "stages"]
    assert [s["data"]["order"] for s in stages] == [1, 2, 3, 4, 5] and stages[0]["glyph"] == "GlyphDoc:component-view-matrix.stage"
    cells = [l for l in mat["links"] if l["draw"] == "cell"]
    nests = [l for l in mat["links"] if l["draw"] == "nest"]
    assert cells and nests and all(c["label"] == "quotation" for c in cells) and mat["skipped"] == []


# ==================================================================================================
# spec2viz tests/test_view_contract_resolved.py
# ==================================================================================================

PLACEHOLDER = re.compile(r"\{[A-Za-z0-9_.]+\}")
CONTRACT_SPECS = [
    FIXTURES / "deployment.nested.yml", FIXTURES / "deployment.runtime.yml", FIXTURES / "activity.lanes.yml",
    FIXTURES / "component.styled.yml", SPEC2VIZ / "docs" / "architecture" / "spec2viz" / "state-diagram-sync-lifecycle.yml",
    SPEC2VIZ / "docs" / "architecture" / "spec2viz" / "sequence-sync-pipeline.yml", SPEC2VIZ / "docs" / "architecture" / "spec2viz" / "class-sldb-models.yml",
]


def _strings(value, path="view"):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from _strings(v, f"{path}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _strings(v, f"{path}[{i}]")


def _unresolved(view):
    # `data` es el payload del documento tal cual; las plantillas resueltas son el resto
    return [(p, s) for p, s in _strings({k: v for k, v in view.items()}) if ".data." not in p and PLACEHOLDER.search(s)]


@pytest.mark.parametrize("spec", CONTRACT_SPECS, ids=lambda p: p.stem)
def test_no_placeholder_reaches_the_render_contract(tmp_path, spec):
    """spec2viz tests/test_view_contract_resolved.py::test_no_placeholder_reaches_the_render_contract."""
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    copy_ = shutil.copy(spec, tmp_path / "docs" / spec.name)
    report = SpecSync(tmp_path / ".sldb").sync(Path(copy_))
    view = resolve_view(tmp_path / ".sldb", report.spec_id)
    assert _unresolved(view) == []


def test_deployment_keyword_interpolates_kind_and_drops_when_empty(tmp_path):
    """spec2viz tests/test_view_contract_resolved.py::test_deployment_keyword_interpolates_kind_and_drops_when_empty."""
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    copy_ = shutil.copy(FIXTURES / "deployment.nested.yml", tmp_path / "docs" / "nested.yml")
    SpecSync(tmp_path / ".sldb").sync(Path(copy_))
    nodes = {n["element"]: n for n in resolve_view(tmp_path / ".sldb", "deployment.nested")["nodes"]}
    assert nodes["db"]["keyword"] == "«database»" and nodes["api_image"]["keyword"] == "«image»"
    assert render_keyword("«{kind}»", {"kind": ""}) == "" and render_keyword("«{kind}»", {}) == ""
    assert render_keyword("«interface»", {}) == "«interface»" and render_keyword("", {"kind": "x"}) == ""


# ==================================================================================================
# spec2viz tests/test_style_palette.py
# ==================================================================================================

STYLED = {
    "name": "infra", "title": "Infra", "diagram_type": "component", "layout": {"kind": "graph"},
    "glyphs": [
        {"id": "db", "model": "SpecNodeDoc", "where": 'kind = "database"', "shape": "cylinder", "kind": "database"},
        {"id": "api", "model": "SpecNodeDoc", "where": 'kind = "backend"', "shape": "box", "fill": "#fafafa"},
        {"id": "any", "model": "SpecNodeDoc", "shape": "rounded-box"},
    ],
    "links": [{"id": "any", "relation": "*", "color": "database-stroke", "label": "{relation_type}"}],
}
PAIR = {"light": "#fff1c2", "dark": "#3d3200"}


def _write(tmp_path, notation, name="infra.yml"):
    path = tmp_path / name
    path.write_text(yaml.safe_dump(notation), encoding="utf-8")
    return path


def _store(tmp_path):
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    return tmp_path / ".sldb"


def test_new_builtin_shapes_are_accepted(tmp_path):
    """spec2viz tests/test_style_palette.py::test_new_builtin_shapes_are_accepted."""
    assert {"cylinder", "queue", "cloud", "package", "note"} <= set(SHAPES)
    notation = copy.deepcopy(STYLED)
    notation["glyphs"] = [{"id": s, "model": "SpecNodeDoc", "where": f'kind = "{s}"', "shape": s} for s in ("cylinder", "queue", "cloud", "package", "note")]
    notation["glyphs"].append({"id": "any", "model": "SpecNodeDoc", "shape": "box"})
    load_notation(_write(tmp_path, notation))


@pytest.mark.parametrize("mutate, error", [
    (lambda n: n["glyphs"][2].update(shape="hexagon"), UnknownShapeError),
    (lambda n: n["glyphs"][0].update(kind="mainframe"), UnknownKindError),
    (lambda n: n["glyphs"][1].update(fill="red"), InvalidColorError),
    (lambda n: n["glyphs"][1].update(stroke="#12345"), InvalidColorError),
    (lambda n: n["links"][0].update(color="url(#x)"), InvalidColorError),
    (lambda n: n["glyphs"][1].update(icon="https://example.com/x.svg"), UnknownIconError),
    (lambda n: n["glyphs"][1].update(icon="rocket"), UnknownIconError),
])
def test_notation_load_gives_typed_errors(tmp_path, mutate, error):
    """spec2viz tests/test_style_palette.py::test_notation_validate_gives_typed_errors, parte no CLI.

    The same 7 cases (mutation over STYLED, expected error class), with `load_notation` raising
    sldb's typed error; the `spec2viz notation validate` half is rows SV-K (tests/visual/test_cli.py)."""
    notation = copy.deepcopy(STYLED)
    mutate(notation)
    path = _write(tmp_path, notation)
    with pytest.raises(error):
        load_notation(path)


def test_builtin_notations_still_validate_and_are_unstyled():
    """spec2viz tests/test_style_palette.py::test_builtin_notations_still_validate_and_are_unstyled."""
    for name in builtin_notations():
        assert load_notation(name).styled is False


def test_default_palette_is_accessible_and_distinguishable_without_colour():
    """spec2viz tests/test_style_palette.py::test_default_palette_is_accessible_and_distinguishable_without_colour."""
    palette = load_palette()
    assert set(palette.kinds) == {"database", "queue", "storage", "gateway", "auth", "backend", "frontend", "client", "external"}
    pairs = {(k.shape, k.icon) for k in palette.kinds.values()}
    assert len(pairs) == len(palette.kinds)  # forma + icono distinguen sin el tono
    for kind in palette.kinds.values():
        for theme in ("light", "dark"):
            assert contrast(palette.color(kind.stroke)[theme], getattr(palette.backgrounds, theme)) >= 3.0
            assert contrast(getattr(palette.ink, theme), palette.color(kind.fill)[theme]) >= 4.5


@pytest.mark.parametrize("mutate, error, message", [
    (lambda p: p["colors"].update({"database-stroke": {"light": "#eeeeee", "dark": "#0072b2"}}), ValidationError, "WCAG 1.4.11"),
    (lambda p: p["colors"].update({"queue-fill": {"light": "#333333", "dark": "#4a3911"}}), ValidationError, "WCAG AA"),
    (lambda p: p["kinds"]["storage"].update(icon="database"), ValidationError, "only cue"),
    (lambda p: p["kinds"]["auth"].update(icon="rocket"), UnknownIconError, "icon set"),
    (lambda p: p["kinds"]["auth"].update(shape="hexagon"), UnknownShapeError, "shape"),
    (lambda p: p["kinds"]["auth"].update(fill="tomato"), InvalidColorError, "token"),
])
def test_palette_check_is_typed(mutate, error, message):
    """spec2viz tests/test_style_palette.py::test_palette_validation_is_typed, parte no CLI.

    The same 6 cases (mutation over spec2viz's `default` palette, copied in
    `fixtures/spec2viz-notations/palettes/default.yml`; error class and match pattern), with sldb's
    `check_palette(PaletteSpec.model_validate(raw))`; the `spec2viz palette validate` half is rows SV-K."""
    raw = yaml.safe_load((NOTATION_COPIES / "palettes" / "default.yml").read_text(encoding="utf-8"))
    mutate(raw)
    with pytest.raises(error, match=message):
        check_palette(PaletteSpec.model_validate(raw))


def test_precedence_glyph_over_spec_over_palette():
    """spec2viz tests/test_style_palette.py::test_precedence_glyph_over_spec_over_palette."""
    palette = {"colors": {k: v.model_dump() for k, v in load_palette().colors.items()},
               "kinds": {k: v.model_dump() for k, v in load_palette().kinds.items()}}
    # solo paleta
    style = resolve_style({}, "database", None, palette)
    assert style["fill"]["light"] == "#dbebf4" and style["icon"] == "database" and set(style["source"].values()) == {"palette"}
    # el spec gana a la paleta, propiedad por propiedad
    style = resolve_style({}, "database", {"database": {"fill": "#ffeecc"}}, palette)
    assert style["fill"] == {"light": "#ffeecc", "dark": "#ffeecc"} and style["source"]["fill"] == "spec" and style["source"]["stroke"] == "palette"
    # el glifo gana a todo: explicito, y detras el kind de la paleta que nombra
    style = resolve_style({"fill": "#000000", "kind": "queue"}, "database", {"database": {"fill": "#ffeecc", "icon": "cpu"}}, palette)
    assert style["fill"]["light"] == "#000000" and style["stroke"]["light"] == "#b37c00" and style["icon"] == "list-ordered"
    assert style["source"] == {"fill": "glyph", "stroke": "glyph", "icon": "glyph"}
    # sin paleta en la notacion, la paleta no aplica; el spec si (sus tokens resuelven contra default)
    assert resolve_style({}, "database", None, None) == {}
    assert resolve_style({}, "backend", {"backend": {"stroke": "backend-stroke"}}, None)["stroke"]["dark"] == "#56b4e9"


def test_mermaid_class_defs_from_style_kinds_and_plantuml_block_untouched():
    """spec2viz tests/test_style_palette.py::test_mermaid_class_defs_from_style_kinds_and_plantuml_block_untouched.

    Against specIR's renderers (`specir.visual.renderers`), which color with sldb's precedence."""
    diagram = load(FIXTURES / "component.kinds.yml")
    validate(diagram)
    out = MermaidRenderer().render(compile_ir(diagram))
    assert "classDef kind0 fill:#ffeecc,color:#1f2328" in out and "class db kind0" in out
    assert "classDef kind1 stroke:#1b8dce,color:#1f2328" in out and "class api kind1" in out
    assert "web" not in [l.split()[1] for l in out.splitlines() if l.strip().startswith("class ")]
    assert "classDef" not in MermaidRenderer().render(compile_ir(load(FIXTURES / "component.styled.yml")))
    assert "#112233" in PlantUMLRenderer().render(compile_ir(load(FIXTURES / "component.styled.yml")))


@pytest.mark.parametrize("entry, error", [({"fill": "blue"}, InvalidColorError), ({"icon": "rocket"}, UnknownIconError)])
def test_spec_style_kinds_are_validated_typed(entry, error):
    """spec2viz tests/test_style_palette.py::test_spec_style_kinds_are_validated_typed."""
    diagram = load(FIXTURES / "component.kinds.yml")
    diagram.style.kinds["database"] = entry
    with pytest.raises(error):
        validate(diagram)


def test_styled_notation_syncs_its_palette_and_view_carries_resolved_style_and_legend(tmp_path):
    """spec2viz tests/test_style_palette.py::test_styled_notation_syncs_its_palette_and_view_carries_resolved_style_and_legend."""
    store = _store(tmp_path)
    notation = _write(tmp_path / "docs", STYLED)
    spec = shutil.copy(FIXTURES / "component.kinds.yml", tmp_path / "docs" / "kinds.yml")
    report = SpecSync(store).sync(Path(spec), notation=notation)
    assert "PaletteDoc:default" in report.created
    docs = {f"{d.model_name}:{d.name}": d.payload for d in sldb_api.load_runtime_documents(store, None, include_linked=False)}
    assert docs["NotationDoc:infra"]["palette"] == "PaletteDoc:default"
    assert docs["GlyphDoc:infra.db"]["kind"] == "database" and docs["LinkDoc:infra.any"]["color"] == "database-stroke"
    assert docs["SpecDoc:component.kinds"]["style"] == {"database": {"fill": "#ffeecc"}, "backend": {"stroke": "backend-stroke", "icon": "cpu"}}

    view = resolve_view(store, "component.kinds")
    nodes = {n["element"]: n for n in view["nodes"]}
    # db: glifo con kind database (gana al spec), api: fill del glifo, stroke e icono del spec
    assert nodes["db"]["style"]["fill"]["light"] == "#dbebf4" and nodes["db"]["style"]["source"]["fill"] == "glyph"
    assert nodes["api"]["style"]["fill"]["light"] == "#fafafa" and nodes["api"]["style"]["icon"] == "cpu"
    assert nodes["api"]["style"]["source"] == {"fill": "glyph", "stroke": "spec", "icon": "spec"}
    # web: solo la paleta de la notacion
    assert nodes["web"]["style"]["icon"] == "app-window" and set(nodes["web"]["style"]["source"].values()) == {"palette"}
    assert all(l["color"] == {"light": "#0072b2", "dark": "#0072b2"} for l in view["links"])
    assert view["palette"] == "PaletteDoc:default"
    legend = view["legend"]
    assert [g["glyph"] for g in legend["glyphs"]] == ["GlyphDoc:infra.db", "GlyphDoc:infra.api", "GlyphDoc:infra.any"]
    assert legend["glyphs"][0]["shape"] == "cylinder" and legend["glyphs"][0]["style"]["icon"] == "database"
    assert legend["links"][0]["color"]["light"] == "#0072b2"
    assert {k["kind"] for k in legend["kinds"]} == {"backend", "frontend"} and next(k for k in legend["kinds"] if k["kind"] == "frontend")["shape"] == "box"


def test_unstyled_notation_writes_no_palette_and_no_style(tmp_path):
    """spec2viz tests/test_style_palette.py::test_unstyled_notation_writes_no_palette_and_no_style."""
    store = _store(tmp_path)
    spec = shutil.copy(FIXTURES / "deployment.runtime.yml", tmp_path / "docs" / "dep.yml")
    SpecSync(store).sync(Path(spec))
    assert not any(str(d.model_name) == "PaletteDoc" for d in sldb_api.load_runtime_documents(store, None, include_linked=False))
    text = (tmp_path / "sldb" / "notations" / "deployment" / "notation.md").read_text(encoding="utf-8")
    assert "palette:" not in text
    view = resolve_view(store, "deployment.runtime")
    assert all(n["style"] == {} for n in view["nodes"]) and all(l["color"] is None for l in view["links"])


def test_resolve_documents_is_public_and_filters_relations(tmp_path):
    """spec2viz tests/test_style_palette.py::test_resolve_documents_is_public_and_filters_relations."""
    store = _store(tmp_path)
    spec = shutil.copy(FIXTURES / "component.kinds.yml", tmp_path / "docs" / "kinds.yml")
    SpecSync(store).sync(Path(spec), notation=_write(tmp_path / "docs", STYLED))
    full = resolve_view(store, "component.kinds")
    refs = [n["doc"] for n in full["nodes"]]
    same = resolve_documents(store, "NotationDoc:infra", refs, spec_style={"database": {"fill": "#ffeecc"}, "backend": {"stroke": "backend-stroke", "icon": "cpu"}})
    assert [n["style"] for n in same["nodes"]] == [n["style"] for n in full["nodes"]] and same["links"] == full["links"]
    # api y db, y solo la arista api -> db aunque web -> api tambien exista
    keep = {r for r in refs if r.endswith((".api", ".db"))}
    edge = next(l["doc"] for l in full["links"] if l["source"] in keep and l["target"] in keep)
    one = resolve_documents(store, "infra", sorted(keep), relation_refs=[edge])
    assert len(one["nodes"]) == 2 and [l["doc"] for l in one["links"]] == [edge]
    assert resolve_documents(store, "infra", sorted(keep), relation_refs=[])["links"] == []


@pytest.mark.parametrize("value, error", [
    ({"light": "#fff1c2"}, "exactly `light` and `dark`"),
    ({"light": "#fff1c2", "dark": "#3d3200", "hc": "#000000"}, "exactly `light` and `dark`"),
    ({"light": "#fff1c2", "dark": "dark-yellow"}, "dark"),
    ({"light": "fff1c2", "dark": "#3d3200"}, "light"),
])
def test_color_pair_is_validated_typed(tmp_path, value, error):
    """spec2viz tests/test_style_palette.py::test_color_pair_is_validated_typed."""
    notation = copy.deepcopy(STYLED)
    notation["glyphs"][1]["fill"] = value
    with pytest.raises(InvalidColorError, match=error):
        load_notation(_write(tmp_path, notation))


def test_single_hex_is_the_same_in_both_themes_and_a_pair_is_not():
    """spec2viz tests/test_style_palette.py::test_single_hex_is_the_same_in_both_themes_and_a_pair_is_not."""
    assert resolve_color("#FFF1C2", {}) == {"light": "#fff1c2", "dark": "#fff1c2"}
    tokens = {k: v.model_dump() for k, v in load_palette().colors.items()}
    assert resolve_color(PAIR, tokens) == PAIR
    # cada lado puede ser un token: se toma el valor de ese tema
    assert resolve_color({"light": "#fff1c2", "dark": "queue-fill"}, tokens) == {"light": "#fff1c2", "dark": "#4a3911"}


def test_pair_reaches_the_view_per_theme_for_glyph_link_and_spec(tmp_path):
    """spec2viz tests/test_style_palette.py::test_pair_reaches_the_view_per_theme_for_glyph_link_and_spec."""
    store = _store(tmp_path)
    notation = copy.deepcopy(STYLED)
    notation["glyphs"][1]["fill"] = PAIR
    notation["glyphs"][1]["stroke"] = {"light": "#7a5c00", "dark": "#e6c34a"}
    notation["links"][0]["color"] = {"light": "#0072b2", "dark": "#56b4e9"}
    spec = yaml.safe_load((FIXTURES / "component.kinds.yml").read_text(encoding="utf-8"))
    spec["style"]["kinds"]["frontend"] = {"fill": {"light": "#eef6ff", "dark": "#10233a"}}
    (tmp_path / "docs" / "kinds.yml").write_text(yaml.safe_dump(spec, allow_unicode=True), encoding="utf-8")
    SpecSync(store).sync(tmp_path / "docs" / "kinds.yml", notation=_write(tmp_path / "docs", notation))

    glyph = next(d.payload for d in sldb_api.load_runtime_documents(store, None, include_linked=False) if d.name == "infra.api")
    assert glyph["fill"] == PAIR  # el GlyphDoc guarda el par tal cual
    nodes = {n["element"]: n for n in resolve_view(store, "component.kinds")["nodes"]}
    assert nodes["api"]["style"]["fill"] == PAIR and nodes["api"]["style"]["stroke"] == {"light": "#7a5c00", "dark": "#e6c34a"}
    assert nodes["web"]["style"]["fill"] == {"light": "#eef6ff", "dark": "#10233a"} and nodes["web"]["style"]["source"]["fill"] == "spec"
    view = resolve_view(store, "component.kinds")
    assert {l["color"]["dark"] for l in view["links"]} == {"#56b4e9"}


def test_mermaid_takes_the_light_side_of_a_spec_pair():
    """spec2viz tests/test_style_palette.py::test_mermaid_takes_the_light_side_of_a_spec_pair.

    Against specIR's mermaid renderer (`specir.visual.renderers.mermaid`)."""
    diagram = load(FIXTURES / "component.kinds.yml")
    diagram.style.kinds["database"] = {"fill": PAIR}
    validate(diagram)
    assert "classDef kind0 fill:#fff1c2,color:#1f2328" in MermaidRenderer().render(compile_ir(diagram))
