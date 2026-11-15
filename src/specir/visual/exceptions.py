"""Errors of specIR's visual layer, migrated from `spec2viz.exceptions` with their names.

`ParseError`, `ValidationError` and its typed subclasses are sldb's (D3, `sldb.notations.exceptions`)
and are not defined here. IR11 brought the root and `CompileError`; IR12 adds `RenderError`."""


class Spec2VizError(Exception):
    """Root of the errors of the visual layer (compilation and rendering)."""


class CompileError(Spec2VizError):
    """A spec that no compiler of specIR turns into an intermediate representation."""


class RenderError(Spec2VizError):
    """An intermediate representation that a renderer cannot draw, or rendered text that breaks
    its engine (`specir.visual.lint_mermaid.MermaidLintError`)."""


__all__ = ["Spec2VizError", "CompileError", "RenderError"]
