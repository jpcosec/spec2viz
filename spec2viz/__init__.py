from __future__ import annotations
import json
from pathlib import Path

from spec2viz.loader import load as _load
from spec2viz.schema import (
    json_schema as _json_schema,
    write_json_schema as _write_json_schema,
)
from spec2viz.validator import validate as _validate
from spec2viz.compilers import compile_ir as _compile_ir
from spec2viz.renderers import render as _render, EXT_MAP, DEFAULT_RENDERER
from spec2viz.models.base import BaseDiagram


def load(path: str | Path) -> BaseDiagram:
    return _load(path)


def validate(diagram: BaseDiagram) -> None:
    _validate(diagram)


def compile_ir(diagram: BaseDiagram):
    return _compile_ir(diagram)


def render(ir, renderer: str | None = None) -> str | dict:
    return _render(ir, renderer)


def json_schema(diagram_type: str | None = None) -> dict:
    return _json_schema(diagram_type)


def write_json_schema(path: str | Path, diagram_type: str | None = None) -> Path:
    return _write_json_schema(path, diagram_type)


def render_to_file(
    path: str | Path,
    out: str | Path = ".",
    renderer: str | None = None,
) -> Path:
    path = Path(path)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    diagram = load(path)
    validate(diagram)
    ir = compile_ir(diagram)
    renderer_name = renderer or DEFAULT_RENDERER[type(ir)]
    ext = EXT_MAP[renderer_name]
    output_path = out_dir / (path.stem + ext)

    result = render(ir, renderer_name)
    if isinstance(result, dict):
        output_path.write_text(json.dumps(result, indent=2))
    else:
        output_path.write_text(result)

    return output_path
