"""vistas.yml: notation por vista; diagram sync conserva el catalogo (categoria, nav, resumen)."""
import shutil
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from spec2viz.cli import main
from spec2viz.exceptions import NotationMismatchError, UnknownNotationError

sldb_api = pytest.importorskip("sldb.api")

REPO = Path(__file__).parent.parent
SPEC = REPO / "tests" / "fixtures" / "activity.lanes.yml"
OWN_NOTATION = {
    "name": "flow-own", "title": "Own flow", "diagram_type": "activity", "layout": {"kind": "graph"},
    "glyphs": [{"id": "step", "model": "SpecNodeDoc", "shape": "box"}],
    "links": [{"id": "next", "relation": "next"}],
}


def _project(tmp_path, view_notation=None):
    sldb_api.init_store(tmp_path)
    docs = tmp_path / "docs"
    (docs / "notations").mkdir(parents=True)
    shutil.copy(SPEC, docs / "lanes.yml")
    (docs / "notations" / "flow-own.yml").write_text(yaml.safe_dump(OWN_NOTATION), encoding="utf-8")
    vista = {"id": "lanes", "category": "Flujos", "nav": "Carriles", "desc": "Aprobacion", "specs": ["lanes.yml"]}
    if view_notation is not None:
        vista["notation"] = view_notation
    (docs / "vistas.yml").write_text(yaml.safe_dump({"vistas": [vista]}), encoding="utf-8")
    return docs / "vistas.yml"


def _spec_doc(tmp_path):
    return next(d.payload for d in sldb_api.load_runtime_documents(tmp_path / ".sldb", None, include_linked=False)
                if str(d.model_name) == "SpecDoc" and d.name == "activity.lanes")


def test_diagram_sync_with_notation_keeps_the_catalog_metadata(tmp_path):
    config = _project(tmp_path)
    runner = CliRunner()
    assert runner.invoke(main, ["catalog", "sync", "--config", str(config), "--store", str(tmp_path / ".sldb")]).exit_code == 0
    result = runner.invoke(main, ["diagram", "sync", str(config.parent / "lanes.yml"), "--store", str(tmp_path / ".sldb"),
                                  "--notation", str(config.parent / "notations" / "flow-own.yml")])
    assert result.exit_code == 0, result.output
    doc = _spec_doc(tmp_path)
    assert (doc["category"], doc["nav"], doc["summary"]) == ("Flujos", "Carriles", "Aprobacion")
    assert doc["notation"] == "NotationDoc:flow-own"


def test_view_notation_path_is_relative_to_the_vistas_yml(tmp_path):
    config = _project(tmp_path, "notations/flow-own.yml")
    result = CliRunner().invoke(main, ["catalog", "sync", "--config", str(config), "--store", str(tmp_path / ".sldb")])
    assert result.exit_code == 0, result.output
    doc = _spec_doc(tmp_path)
    assert doc["notation"] == "NotationDoc:flow-own" and doc["category"] == "Flujos"


def test_view_notation_name_resolves_against_the_store(tmp_path):
    config = _project(tmp_path, "flow-own")
    runner = CliRunner()
    # sin la notacion en el store, el nombre no resuelve: error tipado y nada se escribe
    result = runner.invoke(main, ["catalog", "sync", "--config", str(config), "--store", str(tmp_path / ".sldb")])
    assert result.exit_code == 1 and "UnknownNotationError" in result.output
    assert not any(str(d.model_name) == "SpecDoc" for d in sldb_api.load_runtime_documents(tmp_path / ".sldb", None, include_linked=False))
    # una vez en el store, resuelve por nombre
    assert runner.invoke(main, ["notation", "sync", str(config.parent / "notations" / "flow-own.yml"), "--store", str(tmp_path / ".sldb")]).exit_code == 0
    result = runner.invoke(main, ["catalog", "sync", "--config", str(config), "--store", str(tmp_path / ".sldb")])
    assert result.exit_code == 0, result.output
    assert _spec_doc(tmp_path)["notation"] == "NotationDoc:flow-own"


def test_view_notation_builtin_name_and_absent_field(tmp_path):
    config = _project(tmp_path, "activity")
    assert CliRunner().invoke(main, ["catalog", "sync", "--config", str(config), "--store", str(tmp_path / ".sldb")]).exit_code == 0
    assert _spec_doc(tmp_path)["notation"] == "NotationDoc:activity"


@pytest.mark.parametrize("value, error", [
    ("notations/missing.yml", "UnknownNotationError"),
    ("no-such-notation", "UnknownNotationError"),
    ("deployment", "NotationMismatchError"),
])
def test_catalog_validate_and_sync_give_typed_errors(tmp_path, value, error):
    config = _project(tmp_path, value)
    runner = CliRunner()
    for command in (["catalog", "validate"], ["catalog", "sync"]):
        result = runner.invoke(main, [*command, "--config", str(config), "--store", str(tmp_path / ".sldb")])
        assert result.exit_code == 1 and error in result.output, (command, result.output)


def test_catalog_validate_passes_and_resolver_raises_typed_errors(tmp_path):
    from spec2viz.sldb_sync import resolve_spec_notation

    config = _project(tmp_path, "notations/flow-own.yml")
    result = CliRunner().invoke(main, ["catalog", "validate", "--config", str(config), "--store", str(tmp_path / ".sldb")])
    assert result.exit_code == 0 and "Valid: lanes" in result.output
    with pytest.raises(NotationMismatchError):
        resolve_spec_notation("statechart", "activity", "activity.x")
    with pytest.raises(UnknownNotationError):
        resolve_spec_notation("nope", "activity", "activity.x", tmp_path / ".sldb")
