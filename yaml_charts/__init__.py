from __future__ import annotations
import json
from pathlib import Path

from yaml_charts.loader    import load as _load
from yaml_charts.validator import validate as _validate
from yaml_charts.compilers import compile_ir as _compile_ir
from yaml_charts.renderers import render as _render, EXT_MAP, DEFAULT_RENDERER
from yaml_charts.models.base import BaseDiagram


def load(path: str | Path) -> BaseDiagram:
    return _load(path)


def validate(diagram: BaseDiagram) -> None:
    _validate(diagram)


def compile_ir(diagram: BaseDiagram):
    return _compile_ir(diagram)


def render(ir, renderer: str | None = None) -> str | dict:
    return _render(ir, renderer)


def render_to_file(
    path: str | Path,
    out: str | Path = ".",
    renderer: str | None = None,
) -> Path:
    path    = Path(path)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    diagram      = load(path)
    validate(diagram)
    ir           = compile_ir(diagram)
    renderer_name = renderer or DEFAULT_RENDERER[type(ir)]
    ext          = EXT_MAP[renderer_name]
    output_path  = out_dir / (path.stem + ext)

    result = render(ir, renderer_name)
    if isinstance(result, dict):
        output_path.write_text(json.dumps(result, indent=2))
    else:
        output_path.write_text(result)

    return output_path
