"""The parity corpus of IR11 and its oracle.

The corpus is every diagram spec of spec2viz at revision `REVISION` (its `tests/fixtures/`, including
`invalid/`, `examples/` and `docs/architecture/spec2viz/`), copied to `fixtures/spec2viz/` with the
same relative paths. For each spec the outcome is what loading and validating it gives (`ok`, or
the error's class name and message) and, when it is valid, its compiled IR in normalized form
(`specir.visual.normalize`).

The oracle is `GOLDENS`: the outcomes spec2viz gave at `REVISION`, recorded by the script of the run
`exec-deskops-e-5ccf277d5e67` (`runs/subagents/`), which is the only place that runs spec2viz."""

from __future__ import annotations

import json
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


def goldens() -> dict[str, Any]:
    return json.loads(GOLDENS.read_text(encoding="utf-8"))
