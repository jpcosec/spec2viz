"""specIR imports SLDB only through its public API (`sldb.api`), and never pron or spec2viz.

Until `sldb.api.notations` exports the diagram spec models of D3, `specir.visual.spec_models` is the
one module that imports them from `sldb.models.notation.diagram_specs` (and only from there).

The one exception is specIR's extension of the MCP server of sldb (`specir.mcp_extension`): it
is the only module that reaches `sldb.mcp` (the extension contract of `sldb mcp --extension`)
or `mcp`. specIR implements no MCP server of its own."""

from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1] / "src" / "specir"
FORBIDDEN = ("pron", "spec2viz")
#: The only module allowed to reach the MCP server of sldb and the MCP SDK.
EXTENSION = PACKAGE / "mcp_extension.py"
#: The only module allowed to reach sldb's diagram spec models (D3), which `sldb.api.notations`
#: does not export yet (asked to sldb's desk); it imports them and nothing else of sldb's internals.
SPEC_MODELS = PACKAGE / "visual" / "spec_models.py"
SPEC_MODELS_PACKAGE = "sldb.models.notation.diagram_specs"


def is_spec_models(module: str) -> bool:
    return module == SPEC_MODELS_PACKAGE or module.startswith(SPEC_MODELS_PACKAGE + ".")


def is_mcp(module: str) -> bool:
    return module.split(".")[0] == "mcp" or module == "sldb.mcp" or module.startswith("sldb.mcp.")


def imported_modules(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names += [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names.append(node.module)
        elif isinstance(node, ast.Call) and getattr(node.func, "id", getattr(node.func, "attr", None)) in ("__import__", "import_module"):
            names += [arg.value for arg in node.args if isinstance(arg, ast.Constant) and isinstance(arg.value, str)]
    return names


def test_package_imports_only_the_public_sldb_api() -> None:
    sources = sorted(PACKAGE.rglob("*.py"))
    assert sources, f"no source under {PACKAGE}"
    offending: list[str] = []
    for path in sources:
        for module in imported_modules(path):
            root = module.split(".")[0]
            if path == EXTENSION and is_mcp(module):
                continue
            if path == SPEC_MODELS and is_spec_models(module):
                continue
            if root in FORBIDDEN or (root == "sldb" and module != "sldb.api" and not module.startswith("sldb.api.")):
                offending.append(f"{path.relative_to(PACKAGE.parent)}: {module}")
    assert not offending, offending


def test_sldb_is_reached_only_through_sldb_api() -> None:
    for path in sorted(PACKAGE.rglob("*.py")):
        assert "sldb" not in {m for m in imported_modules(path)}, f"{path}: bare `import sldb`"


def test_only_the_extension_reaches_mcp() -> None:
    reaching = {str(path.relative_to(PACKAGE.parent)) for path in sorted(PACKAGE.rglob("*.py")) if any(is_mcp(m) for m in imported_modules(path))}
    assert reaching == {str(EXTENSION.relative_to(PACKAGE.parent))}, reaching


def test_specir_has_no_mcp_server_of_its_own() -> None:
    assert not (PACKAGE / "mcp").exists(), "src/specir/mcp was migrated to sldb (sldb.mcp)"
    for path in sorted(PACKAGE.rglob("*.py")):
        text = path.read_text(encoding="utf-8")
        for server in ("MCPServer", "FastMCP", "build_server", ".run(\"stdio\")"):
            assert server not in text, f"{path}: {server}"
    pyproject = (PACKAGE.parents[1] / "pyproject.toml").read_text(encoding="utf-8")
    assert "specir-mcp" not in pyproject and "specir.mcp." not in pyproject


def test_only_spec_models_reaches_the_diagram_spec_models() -> None:
    reaching = {str(path.relative_to(PACKAGE.parent)) for path in sorted(PACKAGE.rglob("*.py")) if any(is_spec_models(m) for m in imported_modules(path))}
    assert reaching == {str(SPEC_MODELS.relative_to(PACKAGE.parent))}, reaching
