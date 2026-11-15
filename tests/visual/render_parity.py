"""The render parity corpus of IR12 and its oracle.

The corpus is every spec of IR11's parity corpus (`parity.CORPUS`) that loads and validates, drawn by
each of the nine renderers of spec2viz's selector. For each (spec, renderer) the outcome is the
rendered output (text, or the JSON-able value of `vega` and `json`) or the error's class name and
message; an activity spec also gets the SHA-256 of its offline BPMN viewer page (`bpmn.html`), which
inlines the vendored bpmn-js.

The oracle is spec2viz itself when it is installed (`spec2viz_renders`); `GOLDENS` keeps the outcomes
of its last run (`python tests/visual/render_parity.py` rewrites them), so the parity still holds
against them once spec2viz is retired. The same run saves spec2viz's lint findings on its lint fixtures
(`LINT_GOLDENS`) and the JSON Schema it exports for every type (`SCHEMA_GOLDENS`)."""

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


def spec2viz_renders(rel: str) -> dict[str, Any]:
    from spec2viz.compilers import compile_ir
    from spec2viz.loader import load
    from spec2viz.renderers import render
    from spec2viz.renderers.bpmn import render_bpmn_html

    return outcomes(rel, load, compile_ir, render, render_bpmn_html)


# ── the rest of the oracle: every other use of spec2viz by the tests of IR12 goes through here ──


def spec2viz_selector() -> tuple[list[str], dict[str, str], dict[str, str]]:
    """spec2viz's `--renderer` values, its extensions and its default renderer per IR class name."""
    from spec2viz.cli import DIAGRAM_RENDERERS
    from spec2viz.renderers import DEFAULT_RENDERER, EXT_MAP

    return list(DIAGRAM_RENDERERS), dict(EXT_MAP), {k.__name__: v for k, v in DEFAULT_RENDERER.items()}


def spec2viz_view_to_mermaid(view: dict[str, Any], theme: str) -> str:
    from spec2viz.renderers.view_mermaid import view_to_mermaid

    return view_to_mermaid(view, theme=theme)


def spec2viz_lint() -> Callable:
    from spec2viz.linters.mermaid import lint_mermaid

    return lint_mermaid


def spec2viz_json_schema() -> Callable:
    from spec2viz.schema import json_schema

    return json_schema


def spec2viz_render_to_file(spec: str | Path, out: Path, renderer: str) -> Path:
    from spec2viz import render_to_file

    return render_to_file(spec, out=out, renderer=renderer)


def spec2viz_package_dir() -> Path:
    """Where the installed spec2viz package lives (its templates and vendored bpmn-js)."""
    import spec2viz

    return Path(spec2viz.__file__).parent


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


def write_goldens() -> None:
    """The render outcomes of spec2viz over the valid corpus, and its lint findings, as the saved oracle."""
    import os

    from spec2viz.linters.mermaid import lint_mermaid
    from spec2viz.schema import json_schema

    data = {rel: spec2viz_renders(rel) for rel in VALID}
    GOLDENS.write_text(json.dumps(data, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    os.environ["SPEC2VIZ_MMDC"] = "0"
    LINT_GOLDENS.write_text(json.dumps(lint_findings(lint_mermaid), indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    SCHEMA_GOLDENS.write_text(json.dumps(schemas(json_schema), indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.path.insert(0, str(HERE.parents[1] / "src"))
    write_goldens()
    print(f"{len(VALID)} specs x {len(RENDERERS)} renderers -> {GOLDENS}")
