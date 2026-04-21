from __future__ import annotations
from yaml_charts.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR, MatrixIR
from yaml_charts.renderers.plantuml import PlantUMLRenderer
from yaml_charts.renderers.vega     import VegaRenderer
from yaml_charts.renderers.mermaid  import MermaidRenderer
from yaml_charts.exceptions import RenderError

RENDERER_MAP = {
    "plantuml": PlantUMLRenderer,
    "vega":     VegaRenderer,
    "mermaid":  MermaidRenderer,
}

EXT_MAP = {
    "plantuml": ".puml",
    "vega":     ".vega.json",
    "mermaid":  ".mmd",
}

DEFAULT_RENDERER = {
    SequenceIR:   "plantuml",
    StateIR:      "plantuml",
    ComponentIR:  "plantuml",
    ActivityIR:   "plantuml",
    DeploymentIR: "plantuml",
    MatrixIR:     "vega",
}


def render(ir, renderer: str | None = None) -> str | dict:
    name = renderer or DEFAULT_RENDERER.get(type(ir))
    if name is None:
        raise RenderError(f"No default renderer for {type(ir).__name__}")
    cls = RENDERER_MAP.get(name)
    if cls is None:
        raise RenderError(f"Unknown renderer: {name}")
    return cls().render(ir)
