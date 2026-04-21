from __future__ import annotations

import importlib
import sys
import warnings


_MIGRATION_MESSAGE = (
    "`yaml_charts` was renamed to `spec2viz`. Update imports to `spec2viz` "
    "and prefer the `spec2viz` CLI."
)


def _warn() -> None:
    warnings.warn(_MIGRATION_MESSAGE, DeprecationWarning, stacklevel=2)


_warn()

_MODULE_ALIASES = [
    "cli",
    "compilers",
    "compilers.activity",
    "compilers.component",
    "compilers.deployment",
    "compilers.matrix",
    "compilers.sequence",
    "compilers.state",
    "exceptions",
    "ir",
    "loader",
    "models",
    "models.activity",
    "models.base",
    "models.component",
    "models.deployment",
    "models.matrix",
    "models.sequence",
    "models.state",
    "renderers",
    "renderers.mermaid",
    "renderers.plantuml",
    "renderers.vega",
    "schema",
    "validator",
]

for module_name in _MODULE_ALIASES:
    sys.modules[f"{__name__}.{module_name}"] = importlib.import_module(
        f"spec2viz.{module_name}"
    )

from spec2viz import (
    compile_ir,
    json_schema,
    load,
    render,
    render_to_file,
    validate,
    write_json_schema,
)

__all__ = [
    "load",
    "validate",
    "compile_ir",
    "render",
    "render_to_file",
    "json_schema",
    "write_json_schema",
    "legacy_main",
]


def legacy_main() -> None:
    warnings.warn(
        "`yaml-charts` was renamed to `spec2viz`. Please use `spec2viz` instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    from spec2viz.cli import main

    main(prog_name="yaml-charts")
