"""The render parity corpus of IR12 and its oracle.

The corpus is every spec of IR11's parity corpus (`parity.CORPUS`) that loads and validates, drawn by
each of the nine renderers of spec2viz's selector. For each (spec, renderer) the outcome is the
rendered output (text, or the JSON-able value of `vega` and `json`) or the error's class name and
message; an activity spec also gets the SHA-256 of its offline BPMN viewer page (`bpmn.html`), which
inlines the vendored bpmn-js.

The oracle is `GOLDENS`: what spec2viz gave at `REVISION`, recorded by the script of the run
`exec-deskops-e-5ccf277d5e67` (`runs/subagents/`), which is the only place that runs spec2viz. The same run
saved spec2viz's lint findings on its lint fixtures (`LINT_GOLDENS`) and the JSON Schema it exports
for every type (`SCHEMA_GOLDENS`)."""

from __future__ import annotations

import dataclasses
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import parity  # noqa: E402

REVISION = parity.REVISION
GOLDENS = HERE / "goldens" / f"spec2viz-{REVISION}-renders.json"
LINT_GOLDENS = HERE / "goldens" / f"spec2viz-{REVISION}-lint.json"
SCHEMA_GOLDENS = HERE / "goldens" / f"spec2viz-{REVISION}-schema.json"
#: Every value of `json_schema(diagram_type)` and of the CLI's `--type`: all types (`None`), each of the
#: seven types spec2viz exported and its three names of the diagram store envelope.
SCHEMA_TYPES = (None, "class", "sequence", "state", "component", "activity", "deployment",
                "component_view_matrix", "diagram-store", "catalog", "project")
#: The values of spec2viz's `--renderer` selector (`spec2viz.cli.DIAGRAM_RENDERERS`, revision `REVISION`).
RENDERERS = ("plantuml", "mermaid", "vega", "d2", "antonia-html", "tree", "graph", "bpmn", "json")
#: The specs of the corpus that load and validate (IR11's goldens say which).
VALID = sorted(rel for rel, outcome in parity.goldens().items() if outcome["error"] is None)


def _jsonable(value: Any) -> Any:
    """A render result as JSON: the `json` renderer returns an IR dataclass as is."""
    return json.loads(json.dumps(value, default=lambda o: dataclasses.asdict(o) if dataclasses.is_dataclass(o) else str(o)))


def outcomes(rel: str, load: Callable, compile_ir: Callable, render: Callable, bpmn_html: Callable) -> dict[str, Any]:
    diagram = load(parity.FIXTURES / rel)
    ir = compile_ir(diagram)
    result: dict[str, Any] = {}
    for renderer in RENDERERS:
        try:
            result[renderer] = {"out": _jsonable(render(ir, renderer))}
        except Exception as error:  # the class and the text are what is compared
            result[renderer] = {"error": [type(error).__name__, str(error)]}
    if "out" in result["bpmn"]:
        metadata = diagram.metadata.model_dump() if diagram.metadata else None
        page = bpmn_html(result["bpmn"]["out"], diagram.title, metadata)
        result["bpmn.html"] = hashlib.sha256(page.encode("utf-8")).hexdigest()
    return result


def specir_renders(rel: str) -> dict[str, Any]:
    from sldb.api.notations import load_spec

    from specir.visual.compilers import compile_ir
    from specir.visual.renderers import render
    from specir.visual.renderers.bpmn import render_bpmn_html

    return outcomes(rel, load_spec, compile_ir, render, render_bpmn_html)


def comparable(outcome: dict[str, Any]) -> dict[str, Any]:
    """An outcome with the one order that spec2viz did not fix left out: its `vega` kind color scale
    listed the kinds of a set, so their order changed with `PYTHONHASHSEED`. The scale compares as
    the kind -> color mapping (specIR lists the kinds in order of first appearance)."""
    out = json.loads(json.dumps(outcome))
    vega = (out.get("vega") or {}).get("out")
    if isinstance(vega, dict):
        for scale in vega.get("scales", []):
            if scale.get("name") == "kindColor":
                scale["domain"], scale["range"] = sorted(zip(scale.pop("domain"), scale.pop("range"))), None
    return out


def goldens() -> dict[str, Any]:
    return json.loads(GOLDENS.read_text(encoding="utf-8"))


#: The lint fixtures of spec2viz: the texts of `tests/test_mermaid_mmdc.py` and the bad texts of
#: `tests/test_renderers.py`. `lint_cases` adds the mermaid that spec2viz rendered for the corpus.
LINT_TEXTS = {
    "paren-edge-label": "graph TD\n    a -->|ask (paso 2)| b\n",
    "brace-edge-label": "graph TD\n    a -->|fetch {id}| b\n",
    "nested-quotes": 'flowchart TD\n    e["mostrar "msg" fin"]\n',
    "html-entity-seq": "sequenceDiagram\n    A->>B: show &lt;name&gt;\n",
    "simple-graph": "graph TD\n    a --> b\n",
    "quoted-paren-edge": 'graph TD\n    a -->|"ask (paso 2)"| b\n',
    "sequence-ok": "sequenceDiagram\n    A->>B: hello\n",
    "invalid-return-arrow": "sequenceDiagram\n    A<<--B: reply",
    "raw-angle-brackets": "sequenceDiagram\n    A->>B: GET path?x=<id>",
    "bad-return-arrow": "sequenceDiagram\n    A<<--B: bad\n",
    "empty-decision": "flowchart TD\n    d{}\n",
}


def lint_cases() -> dict[str, str]:
    """Every lint fixture by name: `LINT_TEXTS` and the mermaid of each spec of the corpus that has one."""
    cases = dict(LINT_TEXTS)
    for rel, outcome in goldens().items():
        if "out" in outcome["mermaid"]:
            cases[f"mermaid:{rel}"] = outcome["mermaid"]["out"]
    return cases


def lint_findings(lint: Callable) -> dict[str, Any]:
    """The findings of `lint` on every lint fixture, with and without the raw-angle-bracket rule.
    The caller turns the mmdc pass off: the findings of the regex rules are what is compared."""
    return {name: {"check_html": lint(text, check_html=True), "no_html": lint(text, check_html=False)}
            for name, text in sorted(lint_cases().items())}


def lint_goldens() -> dict[str, Any]:
    return json.loads(LINT_GOLDENS.read_text(encoding="utf-8"))


def schemas(json_schema: Callable) -> dict[str, Any]:
    return {str(diagram_type or "all"): json_schema(diagram_type) for diagram_type in SCHEMA_TYPES}


def schema_goldens() -> dict[str, Any]:
    return json.loads(SCHEMA_GOLDENS.read_text(encoding="utf-8"))
