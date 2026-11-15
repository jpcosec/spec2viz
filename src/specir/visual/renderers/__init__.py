"""Render dispatch: the nine renderers of spec2viz, by name, with their extensions and the default
renderer per intermediate representation (migrated from `spec2viz.renderers`)."""
from __future__ import annotations
import json
from specir.visual.ir import SequenceIR, StateIR, ComponentIR, ActivityIR, DeploymentIR, MatrixIR
from specir.visual.spec_models import EnforcementArtifact
from specir.visual.renderers.plantuml import PlantUMLRenderer
from specir.visual.renderers.vega     import VegaRenderer
from specir.visual.renderers.mermaid  import MermaidRenderer
from specir.visual.renderers.d2       import D2Renderer
from specir.visual.renderers.antonia_html import AntoniaHtmlRenderer
from specir.visual.renderers.tree     import TreeRenderer
from specir.visual.renderers.graph_html import GraphRenderer
from specir.visual.renderers.bpmn import BpmnRenderer
from specir.visual.renderers.json_out import JsonRenderer
from specir.visual.exceptions import RenderError
from specir.visual.ir import ClassIR


RENDERER_MAP = {
    "plantuml": PlantUMLRenderer,
    "vega":     VegaRenderer,
    "mermaid":  MermaidRenderer,
    "d2":       D2Renderer,
    "antonia-html": AntoniaHtmlRenderer,
    "tree":     TreeRenderer,
    "graph":    GraphRenderer,
    "bpmn":     BpmnRenderer,
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
    "bpmn":     ".bpmn",
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


__all__ = ["DEFAULT_RENDERER", "EXT_MAP", "RENDERER_MAP", "JsonRenderer", "render"]
