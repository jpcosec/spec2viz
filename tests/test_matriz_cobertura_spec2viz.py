"""The spec2viz coverage matrix (IR07) lists every capability that the retirement gate has to cover.

Completeness is checked against spec2viz itself: every command and subgroup of its CLI help, every
module of its compilers, renderers, linters and generators, and every file of its test suite has a
row in `docs/spec2viz/matriz-de-cobertura.md`, and every row has one of the four coverage modes.

The CLI tree comes from click when spec2viz is importable, and otherwise from the decorators in
`spec2viz/cli.py` (specIR never depends on spec2viz, so the source is the usual path)."""

from __future__ import annotations

import ast
import importlib
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MATRIX = REPO / "docs" / "spec2viz" / "matriz-de-cobertura.md"
SPEC2VIZ = REPO.parent / "spec2viz"
PACKAGE = SPEC2VIZ / "spec2viz"
SUBPACKAGES = ("compilers", "renderers", "linters", "generators")
MODES = ("migrar tal cual", "reemplazar", "usar sldb directamente", "migrado a sldb")

pytestmark = pytest.mark.skipif(not (PACKAGE / "cli.py").is_file(), reason=f"spec2viz sources not found at {SPEC2VIZ}")


def commands_from_click() -> set[str] | None:
    try:
        main = importlib.import_module("spec2viz.cli").main
    except ImportError:
        return None
    paths: set[str] = set()

    def walk(group, prefix: str) -> None:
        for name, command in group.commands.items():
            path = f"{prefix} {name}"
            paths.add(path)
            if hasattr(command, "commands"):
                walk(command, path)

    walk(main, "spec2viz")
    return paths


def commands_from_source() -> set[str]:
    """Each `@<parent>.command(...)`/`@<parent>.group(...)` of cli.py, with click's default name."""
    tree = ast.parse((PACKAGE / "cli.py").read_text(encoding="utf-8"))
    parents: dict[str, tuple[str, str]] = {}
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef):
            continue
        for decorator in node.decorator_list:
            if not (isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute)):
                continue
            if decorator.func.attr not in ("command", "group") or not isinstance(decorator.func.value, ast.Name):
                continue
            if decorator.func.value.id == "click":  # the root group (`main`)
                continue
            named = [arg.value for arg in decorator.args if isinstance(arg, ast.Constant)]
            named += [kw.value.value for kw in decorator.keywords if kw.arg == "name" and isinstance(kw.value, ast.Constant)]
            name = named[0] if named else node.name.replace("_", "-")
            parents[node.name] = (decorator.func.value.id, name)

    def path(function: str) -> str:
        parent, name = parents[function]
        return f"spec2viz {name}" if parent == "main" else f"{path(parent)} {name}"

    return {path(function) for function in parents}


def cli_commands() -> set[str]:
    return commands_from_click() or commands_from_source()


def package_modules() -> list[str]:
    return sorted(
        f"spec2viz/{sub}/{module.name}"
        for sub in SUBPACKAGES
        for module in (PACKAGE / sub).glob("*.py")
        if module.name != "__init__.py"
    )


def matrix_rows(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("| SV-")]


def test_cli_tree_is_read_from_spec2viz() -> None:
    commands = cli_commands()
    # the four subgroups of the help, so a parsing slip cannot pass the next test vacuously
    assert {"spec2viz diagram", "spec2viz catalog", "spec2viz notation", "spec2viz palette"} <= commands
    assert "spec2viz diagram from-graph" in commands


def test_every_cli_command_and_subgroup_has_a_row() -> None:
    rows = "\n".join(matrix_rows(MATRIX.read_text(encoding="utf-8")))
    missing = sorted(command for command in cli_commands() if f"`{command}`" not in rows)
    assert not missing, f"commands of the spec2viz help without a row in {MATRIX.name}: {missing}"


def test_every_compiler_renderer_linter_and_generator_module_has_a_row() -> None:
    modules = package_modules()
    assert modules, f"no modules under {PACKAGE}"
    rows = "\n".join(matrix_rows(MATRIX.read_text(encoding="utf-8")))
    missing = [module for module in modules if f"`{module}`" not in rows]
    assert not missing, f"spec2viz modules without a row in {MATRIX.name}: {missing}"


def test_every_spec2viz_test_file_maps_to_a_row() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    mapped = set(re.findall(r"^\| `(tests/test_[a-z0-9_]+\.py)` \| SV-", text, flags=re.MULTILINE))
    files = {f"tests/{path.name}" for path in (SPEC2VIZ / "tests").glob("test_*.py")}
    assert files, f"no tests under {SPEC2VIZ / 'tests'}"
    assert not sorted(files - mapped), f"spec2viz test files without a row: {sorted(files - mapped)}"


def test_every_row_has_exactly_one_mode_and_no_dismissal() -> None:
    rows = matrix_rows(MATRIX.read_text(encoding="utf-8"))
    assert rows
    for row in rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        assert sum(cell in MODES for cell in cells) == 1, f"row without exactly one mode: {cells[0]}"
        lowered = row.lower()
        assert "descartad" not in lowered and "fuera de alcance" not in lowered, f"dismissed row: {cells[0]}"
