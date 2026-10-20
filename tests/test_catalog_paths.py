"""Una sola regla para las rutas de vistas.yml (src, specs, notation): junto al vistas.yml y, si
no existe, desde la raiz del repo; ambigua si existen las dos; el error lista lo que probo."""
import shutil
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from spec2viz.catalog_paths import candidates, repo_root, resolve_catalog_path
from spec2viz.cli import main
from spec2viz.exceptions import AmbiguousPathError, UnknownNotationError, UnknownReferenceError

FIXTURES = Path(__file__).parent / "fixtures"
NOTATION = {"name": "flow-own", "diagram_type": "activity", "glyphs": [{"id": "step", "model": "SpecNodeDoc", "shape": "box"}],
            "links": [{"id": "next", "relation": "next"}]}


def _repo(tmp_path):
    """repo/ con .git; el registro en repo/docs/architecture/vistas.yml."""
    root = tmp_path / "repo"
    arch = root / "docs" / "architecture"
    (root / ".git").mkdir(parents=True)
    (arch / "flows").mkdir(parents=True)
    (arch / "notations").mkdir()
    shutil.copy(FIXTURES / "activity.lanes.yml", arch / "flows" / "lanes.yml")
    (arch / "notations" / "flow-own.yml").write_text(yaml.safe_dump(NOTATION), encoding="utf-8")
    (arch / "flows" / "lanes.mmd").write_text("flowchart TD\n  a --> b\n", encoding="utf-8")
    return root, arch


def _vistas(arch, **view):
    vista = {"id": "lanes", "category": "Flujos", "nav": "Carriles", **view}
    (arch / "vistas.yml").write_text(yaml.safe_dump({"vistas": [vista]}), encoding="utf-8")
    return arch / "vistas.yml"


def _cli(*args):
    return CliRunner().invoke(main, [str(a) for a in args])


def test_repo_root_and_candidates(tmp_path):
    root, arch = _repo(tmp_path)
    assert repo_root(arch) == root.resolve()
    assert candidates("x/y.yml", arch) == [(arch / "x/y.yml").resolve(), (root / "x/y.yml").resolve()]
    # un registro en la raiz no prueba dos veces la misma ruta
    assert candidates("x/y.yml", root) == [(root / "x/y.yml").resolve()]


@pytest.mark.parametrize("specs, notation, src", [
    ("flows/lanes.yml", "notations/flow-own.yml", "flows/lanes.mmd"),                                   # junto al vistas.yml
    ("docs/architecture/flows/lanes.yml", "docs/architecture/notations/flow-own.yml", "docs/architecture/flows/lanes.mmd"),  # desde la raiz
])
def test_the_three_fields_resolve_both_ways(tmp_path, specs, notation, src):
    root, arch = _repo(tmp_path)
    config = _vistas(arch, specs=[specs], notation=notation, src=src)
    result = _cli("catalog", "validate", "--config", config)
    assert result.exit_code == 0, result.output
    from spec2viz.sldb_sync import catalog_entries

    entry = catalog_entries(config)[0]
    assert entry["spec"] == (arch / "flows" / "lanes.yml").resolve()
    assert entry["notation"] == (arch / "notations" / "flow-own.yml").resolve()
    assert entry["src"] == (arch / "flows" / "lanes.mmd").resolve() and entry["errors"] == []


def test_reported_case_root_relative_notation_is_not_doubled(tmp_path):
    root, arch = _repo(tmp_path)
    config = _vistas(arch, specs=["docs/architecture/flows/lanes.yml"], notation="docs/architecture/notations/flow-own.yml")
    result = _cli("catalog", "validate", "--config", config)
    assert result.exit_code == 0 and "docs/architecture/docs/architecture" not in result.output


@pytest.mark.parametrize("field", ["specs", "notation", "src"])
def test_two_different_files_are_ambiguous_in_validate_and_sync(tmp_path, field):
    sldb_api = pytest.importorskip("sldb.api")
    root, arch = _repo(tmp_path)
    sldb_api.init_store(root)
    rel = {"specs": "flows/lanes.yml", "notation": "notations/flow-own.yml", "src": "flows/lanes.mmd"}[field]
    # el mismo camino relativo existe tambien desde la raiz, con otro contenido
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text((arch / rel).read_text(encoding="utf-8") + "\n# otra copia\n", encoding="utf-8")
    view = {"specs": ["flows/lanes.yml"], "notation": "notations/flow-own.yml", "src": "flows/lanes.mmd"}
    config = _vistas(arch, **view)
    for command in ("validate", "sync"):
        result = _cli("catalog", command, "--config", config, "--store", root / ".sldb")
        assert result.exit_code == 1 and "AmbiguousPathError" in result.output, (command, result.output)
        assert str((arch / rel).resolve()) in result.output and str((root / rel).resolve()) in result.output
    assert not any(str(d.model_name) == "SpecDoc" for d in sldb_api.load_runtime_documents(root / ".sldb", None, include_linked=False))


def test_same_file_both_ways_is_not_ambiguous(tmp_path):
    root, arch = _repo(tmp_path)
    (root / "flows").symlink_to(arch / "flows", target_is_directory=True)
    assert resolve_catalog_path("flows/lanes.yml", arch, "spec") == (arch / "flows" / "lanes.yml").resolve()


@pytest.mark.parametrize("field, value, error", [
    ("specs", "flows/missing.yml", "UnknownReferenceError"),
    ("notation", "notations/missing.yml", "UnknownNotationError"),
    ("src", "flows/missing.mmd", "UnknownReferenceError"),
])
def test_not_found_lists_the_paths_tried(tmp_path, field, value, error):
    root, arch = _repo(tmp_path)
    view = {"specs": ["flows/lanes.yml"], field: [value] if field == "specs" else value}
    config = _vistas(arch, **view)
    result = _cli("catalog", "validate", "--config", config)
    assert result.exit_code == 1 and error in result.output and "tried:" in result.output
    assert str((arch / value).resolve()) in result.output and str((root / value).resolve()) in result.output


def test_missing_src_does_not_block_sync_but_ambiguity_does(tmp_path):
    sldb_api = pytest.importorskip("sldb.api")
    root, arch = _repo(tmp_path)
    sldb_api.init_store(root)
    config = _vistas(arch, specs=["flows/lanes.yml"], src="flows/missing.mmd")
    result = _cli("catalog", "sync", "--config", config, "--store", root / ".sldb")
    assert result.exit_code == 0, result.output


def test_resolver_types(tmp_path):
    root, arch = _repo(tmp_path)
    with pytest.raises(UnknownNotationError, match="tried:"):
        resolve_catalog_path("nope.yml", arch, "notation", UnknownNotationError)
    with pytest.raises(UnknownReferenceError):
        resolve_catalog_path("nope.yml", arch, "spec")
    (root / "flows").mkdir()
    (root / "flows" / "lanes.yml").write_text("id: other\n", encoding="utf-8")
    with pytest.raises(AmbiguousPathError):
        resolve_catalog_path("flows/lanes.yml", arch, "spec")


def test_catalog_build_reads_src_with_the_same_rule(tmp_path):
    from spec2viz.orchestrator import resolve_item_path

    root, arch = _repo(tmp_path)
    assert resolve_item_path("docs/architecture/flows/lanes.mmd", arch, "src") == (arch / "flows" / "lanes.mmd").resolve()
    (root / "flows").mkdir()
    (root / "flows" / "lanes.mmd").write_text("flowchart LR\n", encoding="utf-8")
    with pytest.raises(AmbiguousPathError):
        resolve_item_path("flows/lanes.mmd", arch, "src")
