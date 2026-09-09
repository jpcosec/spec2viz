from __future__ import annotations
import json
from spec2viz.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR, MatrixIR
from spec2viz.models.reflection import EnforcementArtifact
from spec2viz.renderers.plantuml import PlantUMLRenderer
from spec2viz.renderers.vega     import VegaRenderer
from spec2viz.renderers.mermaid  import MermaidRenderer
from spec2viz.renderers.d2       import D2Renderer
from spec2viz.renderers.antonia  import AntoniaHtmlRenderer
from spec2viz.renderers.tree     import TreeRenderer
from spec2viz.renderers.graph_html import GraphRenderer
from spec2viz.exceptions import RenderError
from spec2viz.ir import ClassIR

class JsonRenderer:
    def render(self, ir):
        if hasattr(ir, "model_dump"):
            return ir.model_dump()
        return ir

RENDERER_MAP = {
    "plantuml": PlantUMLRenderer,
    "vega":     VegaRenderer,
    "mermaid":  MermaidRenderer,
    "d2":       D2Renderer,
    "antonia-html": AntoniaHtmlRenderer,
    "tree":     TreeRenderer,
    "graph":    GraphRenderer,
    "json":     JsonRenderer,
}

EXT_MAP = {
    "plantuml": ".puml",
    "vega":     ".vega.json",
    "mermaid":  ".mmd",
    "d2":       ".d2",
    "antonia-html": ".html",
    "tree":     ".tree.html",
    "graph":    ".graph.html",
    "json":     ".artifact.json",
}

DEFAULT_RENDERER = {
    ClassIR:      "mermaid",
    SequenceIR:   "plantuml",
    StateIR:      "plantuml",
    ComponentIR:  "graph",
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
