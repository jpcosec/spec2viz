from __future__ import annotations
import json
from spec2viz.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR, MatrixIR
from spec2viz.models.reflection import EnforcementArtifact
from spec2viz.renderers.plantuml import PlantUMLRenderer
from spec2viz.renderers.vega     import VegaRenderer
from spec2viz.renderers.mermaid  import MermaidRenderer
from spec2viz.exceptions import RenderError

class JsonRenderer:
    def render(self, ir):
        if hasattr(ir, "model_dump"):
            return ir.model_dump()
        return ir

RENDERER_MAP = {
    "plantuml": PlantUMLRenderer,
    "vega":     VegaRenderer,
    "mermaid":  MermaidRenderer,
    "json":     JsonRenderer,
}

EXT_MAP = {
    "plantuml": ".puml",
    "vega":     ".vega.json",
    "mermaid":  ".mmd",
    "json":     ".artifact.json",
}

DEFAULT_RENDERER = {
    SequenceIR:   "plantuml",
    StateIR:      "plantuml",
    ComponentIR:  "plantuml",
    ActivityIR:   "plantuml",
    DeploymentIR: "plantuml",
    MatrixIR:     "vega",
    EnforcementArtifact: "json",
}


def render(ir, renderer: str | None = None) -> str | dict:
    name = renderer or DEFAULT_RENDERER.get(type(ir))
    if name is None:
        raise RenderError(f"No default renderer for {type(ir).__name__}")
    cls = RENDERER_MAP.get(name)
    if cls is None:
        raise RenderError(f"Unknown renderer: {name}")
    return cls().render(ir)
