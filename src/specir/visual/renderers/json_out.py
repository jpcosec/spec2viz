"""JSON output (`json` renderer, `.artifact.json`), migrated from `spec2viz.renderers.JsonRenderer`."""

from __future__ import annotations


class JsonRenderer:
    def render(self, ir):
        if hasattr(ir, "model_dump"):
            return ir.model_dump()
        return ir


__all__ = ["JsonRenderer"]
