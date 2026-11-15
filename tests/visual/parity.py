"""The parity corpus of IR11 and its oracle.

The corpus is every diagram spec of spec2viz at revision `REVISION` (its `tests/fixtures/`, including
`invalid/`, `examples/` and `docs/architecture/spec2viz/`), copied to `fixtures/spec2viz/` with the
same relative paths. For each spec the outcome is what loading and validating it gives (`ok`, or
the error's class name and message) and, when it is valid, its compiled IR in normalized form
(`specir.visual.normalize`).

The oracle is spec2viz itself when it is installed (`spec2viz_outcome`); `GOLDENS` keeps the
outcomes of its last run (`python tests/visual/parity.py` rewrites them), so the parity still
holds against them once spec2viz is retired."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures" / "spec2viz"
REVISION = "2de1056"
GOLDENS = HERE / "goldens" / f"spec2viz-{REVISION}.json"
CORPUS = sorted(str(p.relative_to(FIXTURES)) for p in FIXTURES.rglob("*.yml"))


def _message(error: Exception) -> str:
    """The error's text, with the corpus' absolute root left out (a path is provenance)."""
    return str(error).replace(str(FIXTURES) + "/", "")


def outcome(rel: str, load: Callable, validate: Callable, compile_ir: Callable) -> dict[str, Any]:
    from specir.visual.normalize import normalize

    try:
        diagram = load(FIXTURES / rel)
        validate(diagram)
    except Exception as error:  # the class and the text are what is compared
        return {"error": [type(error).__name__, _message(error)], "ir": None}
    return {"error": None, "ir": normalize(compile_ir(diagram))}


def specir_outcome(rel: str) -> dict[str, Any]:
    from sldb.api.notations import load_spec, validate_spec

    from specir.visual import compile_ir

    return outcome(rel, load_spec, validate_spec, compile_ir)


def spec2viz_outcome(rel: str) -> dict[str, Any]:
    from spec2viz.compilers import compile_ir
    from spec2viz.loader import load
    from spec2viz.validator import validate

    return outcome(rel, load, validate, compile_ir)


def goldens() -> dict[str, Any]:
    return json.loads(GOLDENS.read_text(encoding="utf-8"))


def write_goldens() -> None:
    """The outcomes of spec2viz over the corpus, as the saved oracle."""
    data = {rel: spec2viz_outcome(rel) for rel in CORPUS}
    GOLDENS.write_text(json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.path.insert(0, str(HERE.parents[1] / "src"))
    write_goldens()
    print(f"{len(CORPUS)} specs -> {GOLDENS}")
