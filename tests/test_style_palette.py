"""Estilo: formas builtin, paleta accesible como documento del store, colores e iconos en glifos y
links, style.kinds del spec y una sola precedencia (glifo > spec > paleta)."""
import copy
import shutil
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from spec2viz.cli import main
from spec2viz.exceptions import InvalidColorError, UnknownIconError, UnknownKindError, UnknownShapeError, ValidationError
from spec2viz.notation import SHAPES, load_notation
from spec2viz.palette import check_palette, contrast, load_palette, PaletteSpec
from spec2viz.styling import resolve_style

FIXTURES = Path(__file__).parent / "fixtures"
STYLED = {
    "name": "infra", "title": "Infra", "diagram_type": "component", "layout": {"kind": "graph"},
    "glyphs": [
        {"id": "db", "model": "SpecNodeDoc", "where": 'kind = "database"', "shape": "cylinder", "kind": "database"},
        {"id": "api", "model": "SpecNodeDoc", "where": 'kind = "backend"', "shape": "box", "fill": "#fafafa"},
        {"id": "any", "model": "SpecNodeDoc", "shape": "rounded-box"},
    ],
    "links": [{"id": "any", "relation": "*", "color": "database-stroke", "label": "{relation_type}"}],
}


def _write(tmp_path, notation, name="infra.yml"):
    path = tmp_path / name
    path.write_text(yaml.safe_dump(notation), encoding="utf-8")
    return path


# --- formas y validacion tipada de notaciones --------------------------------------------------

def test_new_builtin_shapes_are_accepted(tmp_path):
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
def test_notation_validate_gives_typed_errors(tmp_path, mutate, error):
    notation = copy.deepcopy(STYLED)
    mutate(notation)
    path = _write(tmp_path, notation)
    with pytest.raises(error):
        load_notation(path)
    result = CliRunner().invoke(main, ["notation", "validate", str(path)])
    assert result.exit_code == 1 and error.__name__ in result.output


def test_builtin_notations_still_validate_and_are_unstyled():
    from spec2viz.notation import builtin_notations

    for name in builtin_notations():
        assert load_notation(name).styled is False


# --- paleta ------------------------------------------------------------------------------------

def test_default_palette_is_accessible_and_distinguishable_without_colour():
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
def test_palette_validation_is_typed(tmp_path, mutate, error, message):
    raw = yaml.safe_load((Path(__file__).parent.parent / "spec2viz" / "palettes" / "default.yml").read_text(encoding="utf-8"))
    mutate(raw)
    with pytest.raises(error, match=message):
        check_palette(PaletteSpec.model_validate(raw))
    path = _write(tmp_path, raw, "bad-palette.yml")
    result = CliRunner().invoke(main, ["palette", "validate", str(path)])
    assert result.exit_code == 1 and error.__name__ in result.output


# --- precedencia -------------------------------------------------------------------------------

def test_precedence_glyph_over_spec_over_palette():
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


# --- mermaid: style.kinds conectado --------------------------------------------------------------

def test_mermaid_class_defs_from_style_kinds_and_plantuml_block_untouched():
    from spec2viz.compilers import compile_ir
    from spec2viz.loader import load
    from spec2viz.renderers.mermaid import MermaidRenderer
    from spec2viz.renderers.plantuml import PlantUMLRenderer
    from spec2viz.validator import validate

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
    from spec2viz.loader import load
    from spec2viz.validator import validate

    diagram = load(FIXTURES / "component.kinds.yml")
    diagram.style.kinds["database"] = entry
    with pytest.raises(error):
        validate(diagram)


# --- store: PaletteDoc, campos de estilo, resolve_view y resolve_documents ------------------------

sldb_api = pytest.importorskip("sldb.api")


def _store(tmp_path):
    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    return tmp_path / ".sldb"


def test_styled_notation_syncs_its_palette_and_view_carries_resolved_style_and_legend(tmp_path):
    from spec2viz.notation_view import resolve_view
    from spec2viz.sldb_sync import SpecSync

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
    from spec2viz.notation_view import resolve_view
    from spec2viz.sldb_sync import SpecSync

    store = _store(tmp_path)
    spec = shutil.copy(FIXTURES / "deployment.runtime.yml", tmp_path / "docs" / "dep.yml")
    SpecSync(store).sync(Path(spec))
    assert not any(str(d.model_name) == "PaletteDoc" for d in sldb_api.load_runtime_documents(store, None, include_linked=False))
    text = (tmp_path / "sldb" / "notations" / "deployment" / "notation.md").read_text(encoding="utf-8")
    assert "palette:" not in text
    view = resolve_view(store, "deployment.runtime")
    assert all(n["style"] == {} for n in view["nodes"]) and all(l["color"] is None for l in view["links"])


def test_resolve_documents_is_public_and_filters_relations(tmp_path):
    from spec2viz.notation_view import resolve_documents, resolve_view
    from spec2viz.sldb_sync import SpecSync

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


def test_palette_cli_sync_writes_the_store_document(tmp_path):
    store = _store(tmp_path)
    result = CliRunner().invoke(main, ["palette", "sync", "default", "--store", str(store)])
    assert result.exit_code == 0 and "Synced palette default" in result.output
    doc = next(d.payload for d in sldb_api.load_runtime_documents(store, None, include_linked=False) if str(d.model_name) == "PaletteDoc")
    assert doc["kinds"]["queue"]["shape"] == "queue" and doc["icon_set"]["name"] == "lucide"


# --- un color propio para cada tema: el par {light, dark} --------------------------------------

PAIR = {"light": "#fff1c2", "dark": "#3d3200"}


@pytest.mark.parametrize("value, error", [
    ({"light": "#fff1c2"}, "exactly `light` and `dark`"),
    ({"light": "#fff1c2", "dark": "#3d3200", "hc": "#000000"}, "exactly `light` and `dark`"),
    ({"light": "#fff1c2", "dark": "dark-yellow"}, "dark"),
    ({"light": "fff1c2", "dark": "#3d3200"}, "light"),
])
def test_color_pair_is_validated_typed(tmp_path, value, error):
    notation = copy.deepcopy(STYLED)
    notation["glyphs"][1]["fill"] = value
    with pytest.raises(InvalidColorError, match=error):
        load_notation(_write(tmp_path, notation))


def test_single_hex_is_the_same_in_both_themes_and_a_pair_is_not():
    from spec2viz.palette import resolve_color

    assert resolve_color("#FFF1C2", {}) == {"light": "#fff1c2", "dark": "#fff1c2"}
    tokens = {k: v.model_dump() for k, v in load_palette().colors.items()}
    assert resolve_color(PAIR, tokens) == PAIR
    # cada lado puede ser un token: se toma el valor de ese tema
    assert resolve_color({"light": "#fff1c2", "dark": "queue-fill"}, tokens) == {"light": "#fff1c2", "dark": "#4a3911"}


def test_pair_reaches_the_view_per_theme_for_glyph_link_and_spec(tmp_path):
    from spec2viz.notation_view import resolve_view
    from spec2viz.sldb_sync import SpecSync

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
    from spec2viz.compilers import compile_ir
    from spec2viz.loader import load
    from spec2viz.renderers.mermaid import MermaidRenderer
    from spec2viz.validator import validate

    diagram = load(FIXTURES / "component.kinds.yml")
    diagram.style.kinds["database"] = {"fill": PAIR}
    validate(diagram)
    assert "classDef kind0 fill:#fff1c2,color:#1f2328" in MermaidRenderer().render(compile_ir(diagram))
