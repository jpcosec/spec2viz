"""Render a spec file to an output file, with its provenance header (migrated from
`spec2viz.render_to_file` and its helpers).

The spec is loaded and validated by sldb (`sldb.api.notations.load_spec`/`validate_spec`, D3),
compiled by specIR's compilers (IR11) and drawn by specIR's renderers. A text output carries a header
that names its spec and the specIR command that validates it; a BPMN output is written twice, as
`<stem>.bpmn` (the XML) and `<stem>.bpmn.html` (the offline bpmn-js viewer)."""

from __future__ import annotations

import json
from pathlib import Path

from sldb.api.notations import load_spec, validate_spec

from specir.visual.compilers import compile_ir
from specir.visual.renderers import DEFAULT_RENDERER, EXT_MAP, render
from specir.visual.spec_models import BaseDiagram

#: The command that names the projections it writes (spec2viz wrote `spec2viz`).
COMMAND = "specir"


def render_to_file(
    path: str | Path,
    out: str | Path = ".",
    renderer: str | None = None,
) -> Path:
    path = Path(path)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    diagram = load_spec(path)
    validate_spec(diagram)
    ir = compile_ir(diagram)
    renderer_name = renderer or DEFAULT_RENDERER[type(ir)]
    ext = EXT_MAP[renderer_name]
    output_path = out_dir / (path.stem + ext)

    result = render(ir, renderer_name)
    if renderer_name == "bpmn":
        return _write_bpmn(path, output_path, result, diagram)
    if isinstance(result, dict):
        output_path.write_text(json.dumps(result, indent=2))
    else:
        result = with_provenance(renderer_name, path, result)
        if renderer_name == "mermaid":
            from specir.visual.lint_mermaid import assert_mermaid_ok

            assert_mermaid_ok(result, source=path.name)
        output_path.write_text(result)

    return output_path


def _write_bpmn(spec_path: Path, output_path: Path, xml: str, diagram: BaseDiagram) -> Path:
    """`<stem>.bpmn` (the XML) and `<stem>.bpmn.html` (the offline bpmn-js viewer)."""
    from specir.visual.renderers.bpmn import render_bpmn_html, with_xml_provenance

    output_path.write_text(with_xml_provenance(xml, provenance_text(spec_path)), encoding="utf-8")
    # description, preguntas_abiertas and legend are typed fields of the metadata model
    metadata = diagram.metadata.model_dump() if diagram.metadata else None
    page = render_bpmn_html(xml, diagram.title, metadata)
    output_path.with_name(output_path.name + ".html").write_text(page, encoding="utf-8")
    return output_path


# sintaxis de comentario de linea de cada salida de texto
_COMMENT_PREFIX = {"mermaid": "%%", "plantuml": "'", "d2": "#"}


def with_provenance(renderer_name: str, spec_path: str | Path, text: str) -> str:
    """El texto con su cabecera de trazabilidad. En mermaid, un frontmatter de config (`---`) tiene
    que ser la primera linea, asi que la cabecera va justo despues de el."""
    header = provenance_header(renderer_name, spec_path)
    if header and text.startswith("---\n"):
        end = text.find("\n---\n", 3)
        if end != -1:
            cut = end + len("\n---\n")
            return text[:cut] + header + text[cut:]
    return header + text


def provenance_header(renderer_name: str, spec_path: str | Path) -> str:
    """La cabecera de trazabilidad de una proyeccion de texto: de que spec sale y como se
    valida, para que nadie la edite a mano. Vacia para las salidas sin sintaxis de comentario."""
    prefix = _COMMENT_PREFIX.get(renderer_name)
    if prefix is None:
        return ""
    return f"{prefix} {provenance_text(spec_path)}\n"


def provenance_text(spec_path: str | Path) -> str:
    """El texto de la cabecera de trazabilidad, sin sintaxis de comentario."""
    spec = Path(spec_path)
    try:
        shown = spec.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        shown = spec
    return f"{COMMAND}: generated from {shown.as_posix()}; do not edit, run `sldb notations validate {shown.as_posix()}` and re-render"


__all__ = ["COMMAND", "provenance_header", "provenance_text", "render_to_file", "with_provenance"]
