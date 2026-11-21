"""The spec2viz coverage matrix (IR07) lists every capability that the retirement gate has to cover.

Completeness is checked against what spec2viz had (revision 2de1056, frozen in
`visual/goldens/spec2viz-2de1056-oracle.json`): every command and subgroup of its CLI help, every
module of its compilers, renderers, linters and generators, and every file of its test suite has a
row in `docs/spec2viz/matriz-de-cobertura.md`, and every row has one of the four coverage modes.

The lists are the golden's: specIR neither imports spec2viz nor reads its checkout."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tests" / "visual"))
import oracle  # noqa: E402

MATRIX = REPO / "docs" / "spec2viz" / "matriz-de-cobertura.md"
MODES = ("migrar tal cual", "reemplazar", "usar sldb directamente", "migrado a sldb")


def cli_commands() -> set[str]:
    return set(oracle.frozen("cli_commands"))


def package_modules() -> list[str]:
    return sorted(oracle.frozen("package_modules"))


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
    assert modules, "no modules in the golden"
    rows = "\n".join(matrix_rows(MATRIX.read_text(encoding="utf-8")))
    missing = [module for module in modules if f"`{module}`" not in rows]
    assert not missing, f"spec2viz modules without a row in {MATRIX.name}: {missing}"


def test_every_spec2viz_test_file_maps_to_a_row() -> None:
    text = MATRIX.read_text(encoding="utf-8")
    mapped = set(re.findall(r"^\| `(tests/test_[a-z0-9_]+\.py)` \| SV-", text, flags=re.MULTILINE))
    files = set(oracle.frozen("test_files"))
    assert files, "no test files in the golden"
    assert not sorted(files - mapped), f"spec2viz test files without a row: {sorted(files - mapped)}"


def test_every_row_has_exactly_one_mode_and_no_dismissal() -> None:
    rows = matrix_rows(MATRIX.read_text(encoding="utf-8"))
    assert rows
    for row in rows:
        cells = [cell.strip() for cell in row.strip("|").split("|")]
        assert sum(cell in MODES for cell in cells) == 1, f"row without exactly one mode: {cells[0]}"
        lowered = row.lower()
        assert "descartad" not in lowered and "fuera de alcance" not in lowered, f"dismissed row: {cells[0]}"
