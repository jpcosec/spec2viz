"""The retirement gate of spec2viz (IR13): `specir.visual.retirement` and `specir retirement check`.

Synthetic repos and stores are built in tmp; the real run audits the inventory of
`docs/spec2viz/matriz-de-cobertura.md` in the workspace and is a strict xfail while a dependency or a
row not accredited remains (`docs/spec2viz/acta-de-retiro.md`); since 2026-11-23 the universe no longer
holds `spec2viz/.sldb` (G5, option A) and the real run must pass."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
from click.testing import CliRunner

from specir.cli import main
from specir.visual.retirement import (
    DECLARED,
    IMPORT,
    INVOCATION,
    MODEL,
    SKILL,
    InventoryError,
    check,
    inventory,
    open_rows,
)

REPO = Path(__file__).resolve().parents[2]
WORKSPACE = REPO.parent
MATRIX = REPO / "docs" / "spec2viz" / "matriz-de-cobertura.md"

ROWS = """## Matriz

| ID | Capacidad | Fuente | Modo | Destino | Condición |
|---|---|---|---|---|---|
| SV-A01 | a | `x.py` | migrar tal cual | IR | c |
| SV-A02 | b | `y.py` | reemplazar | IR | c |
"""

INVENTORY = """## Inventario de consumidores

| Consumidor | Archivo y línea | Clase | Sustituto previsto |
|---|---|---|---|
| app | `app/x.py:1` | importación | sldb |
| app | `app/pyproject.toml:3` | dependencia declarada | quitar |
| store `app/.sldb` | `store.yaml:4` | modelos | sldb |
"""


def accreditation(second: str) -> str:
    return f"""## Acreditación (IR13)

| Fila | Estado | Prueba que la acredita | Falta |
|---|---|---|---|
| `SV-A01` | cumplida | `tests/visual/test_api.py` (31 passed) | - |
{second}
"""


def specir_repo(tmp_path: Path, second: str = "| `SV-A02` | cumplida | `tests/visual/test_cli.py` | - |") -> Path:
    matrix = tmp_path / "IR" / "docs" / "spec2viz" / "matriz-de-cobertura.md"
    matrix.parent.mkdir(parents=True)
    matrix.write_text(f"# Matriz\n\n{ROWS}\n{INVENTORY}\n{accreditation(second)}", encoding="utf-8")
    return matrix


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def app_with_every_dependency(tmp_path: Path) -> tuple[Path, Path]:
    app = tmp_path / "app"
    write(app / "pkg" / "view.py", "import json\n\nfrom spec2viz.notation_view import resolve_view\n")
    write(app / "pyproject.toml", '[project]\nname = "app"\ndependencies = [\n  "spec2viz>=0.1.0",\n]\n')
    write(app / "scripts" / "build.sh", "#!/bin/sh\nset -e\nspec2viz diagram render specs/*.yml --out out\n")
    store = app / ".sldb"
    write(store / "store.yaml", "models:\n- name: SpecDoc\n  model_ref: spec2viz.sldb_models:SpecDoc\n")
    return app, store


def snapshot(root: Path) -> dict[str, str]:
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file()}


def test_the_inventory_names_the_repos_and_the_stores_of_the_matrix() -> None:
    assert inventory(INVENTORY) == (["app"], ["app/.sldb"])
    repos, stores = inventory(MATRIX.read_text(encoding="utf-8"))
    assert {"graph_ui", "deskops", "pron", "sldb", "IR"} <= set(repos)
    assert stores == []


def test_a_row_without_a_cited_test_fails_and_passes_once_every_row_has_one(tmp_path: Path) -> None:
    text = f"{ROWS}\n{accreditation('| `SV-A02` | cumplida | la ayuda lo muestra | - |')}"
    assert open_rows(text) == ["SV-A02: cumplida sin prueba citada"]
    assert open_rows(f"{ROWS}\n{accreditation('')}") == ["SV-A02: sin entrada en la acreditación"]
    assert open_rows(f"{ROWS}\n{accreditation('| `SV-A02` | abierta | - | falta el pedido |')}") == ["SV-A02: abierta"]
    assert open_rows(f"{ROWS}\n{accreditation('| `SV-A02` | cumplida | `tests/visual/test_cli.py` | - |')}") == []


def test_every_dependency_is_reported_with_repo_path_line_and_kind_and_nothing_is_written(tmp_path: Path) -> None:
    matrix = specir_repo(tmp_path)
    app, store = app_with_every_dependency(tmp_path)
    before = snapshot(tmp_path)
    report = check(matrix, {"app": app, "app/.sldb": store})
    found = {(d.owner, d.path, d.line, d.kind) for d in report.dependencies}
    assert found == {
        ("app", "pkg/view.py", 3, IMPORT),
        ("app", "pyproject.toml", 4, DECLARED),
        ("app", "scripts/build.sh", 3, INVOCATION),
        ("app/.sldb", "store.yaml", 3, MODEL),
    }
    assert not report.ok
    result = CliRunner().invoke(main, ["retirement", "check", "--matrix", str(matrix), "--path", f"app={app}", "--path", f"app/.sldb={store}"])
    assert result.exit_code == 1, result.output
    assert "app\tpkg/view.py:3\timportación" in result.output
    assert "gate: failed" in result.output
    assert snapshot(tmp_path) == before


def test_python_calls_dynamic_imports_ci_and_skills_count(tmp_path: Path) -> None:
    matrix = specir_repo(tmp_path)
    app = tmp_path / "app"
    write(app / "tests" / "test_x.py", (
        "import subprocess, pytest\n"
        "spec2viz = pytest.importorskip('spec2viz')\n"
        "subprocess.run(['spec2viz', 'diagram', 'sync', 'a.yml'], check=True)\n"
        "def run(*args): ...\n"
        "run('spec2viz', 'catalog', 'build')\n"
    ))
    write(app / ".github" / "requirements-suite.txt", "-e git+https://example.invalid/spec2viz@master#egg=spec2viz\n")
    write(app / ".github" / "workflows" / "ci.yml", "jobs:\n  b:\n    steps:\n      - run: spec2viz catalog build --config c.yml\n")
    write(app / ".claude" / "skills" / "use-it" / "SKILL.md", "# Use\n\nRun `spec2viz diagram render spec.yml`.\nA spec2viz diagram spec is YAML.\n")
    write(app / ".opencode" / "skills" / "use-spec2viz" / "SKILL.md", "---\nname: use-spec2viz\n---\n\nUse spec2viz.\n")
    store = tmp_path / "app" / ".sldb"
    store.mkdir()
    found = {(d.path, d.line, d.kind) for d in check(matrix, {"app": app, "app/.sldb": store}).dependencies}
    assert found == {
        ("tests/test_x.py", 2, IMPORT),
        ("tests/test_x.py", 3, INVOCATION),
        ("tests/test_x.py", 5, INVOCATION),
        (".github/requirements-suite.txt", 1, DECLARED),
        (".github/workflows/ci.yml", 4, INVOCATION),
        (".claude/skills/use-it/SKILL.md", 3, SKILL),
        (".opencode/skills/use-spec2viz/SKILL.md", 2, SKILL),
    }


def test_mentions_in_docs_comments_and_changelogs_are_not_dependencies(tmp_path: Path) -> None:
    matrix = specir_repo(tmp_path)
    app = tmp_path / "app"
    write(app / "README.md", "Diagrams were built with `spec2viz diagram render` before specIR.\n")
    write(app / "CHANGELOG.md", "- dropped spec2viz (import spec2viz no longer needed)\n")
    write(app / "docs" / "guide.md", "from spec2viz import render\n")
    write(app / "desk" / "tasks" / "task-x.md", "spec2viz catalog build --config c.yml\n")
    write(app / "pkg" / "mod.py", '"""Ported from spec2viz: `spec2viz diagram sync` became sldb\'s."""\n# import spec2viz\nlabel = "spec2viz render spec.yml"\n')
    write(app / "pyproject.toml", '[project]\nname = "app"\n# spec2viz was a dependency\ndescription = "after spec2viz"\n')
    write(app / "build.sh", "# spec2viz diagram render was here\necho done\n")
    write(app / "pkg" / "names.py", 'def f(n):\n    return n.startswith("spec2viz ") or n.split("spec2viz")\n')
    store = app / ".sldb"
    write(store / "store.yaml", "models:\n- name: SpecDoc\n  model_ref: sldb.models.notation.spec_doc:SpecDoc\n")
    report = check(matrix, {"app": app, "app/.sldb": store})
    assert report.dependencies == []
    assert report.ok


def test_the_universe_is_exactly_the_inventory_plus_specir(tmp_path: Path) -> None:
    matrix = specir_repo(tmp_path)
    app, store = app_with_every_dependency(tmp_path)
    with pytest.raises(InventoryError, match="not in the inventory.*other"):
        check(matrix, {"app": app, "app/.sldb": store, "other": tmp_path})
    with pytest.raises(InventoryError, match="no path given for: app/.sldb"):
        check(matrix, {"app": app})
    report = check(matrix, {"app": app, "app/.sldb": store})
    assert report.repos == ["app", "IR"] and report.stores == ["app/.sldb"]
    result = CliRunner().invoke(main, ["retirement", "check", "--matrix", str(matrix), "--path", f"other={tmp_path}"])
    assert result.exit_code == 2 and "not in the inventory" in result.output


def real_paths() -> dict[str, Path]:
    repos, stores = inventory(MATRIX.read_text(encoding="utf-8"))
    located = {"graph_ui": WORKSPACE / "UIs" / "graph_ui"}
    paths = {name: located.get(name, WORKSPACE / name) for name in [*repos, *stores] if name != "IR"}
    missing = [name for name, path in paths.items() if not path.is_dir()]
    if missing:
        pytest.skip(f"repos or stores of the inventory not in the workspace: {missing}")
    return paths


def test_the_real_universe_has_no_dependency_and_every_row_is_accredited() -> None:
    report = check(MATRIX, real_paths())
    assert report.ok, f"{len(report.dependencies)} dependencies, {len(report.open_rows)} rows not accredited"
