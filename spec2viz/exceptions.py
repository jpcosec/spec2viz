"""Exception hierarchy for the spec2viz pipeline.

One exception type per pipeline stage:
  ParseError      — YAML parsing
  ValidationError — semantic validation
  CompileError    — IR compilation
  RenderError     — renderer output
"""


class Spec2VizError(Exception):
    pass


class ParseError(Spec2VizError):
    pass


class ValidationError(Spec2VizError):
    pass


class CompileError(Spec2VizError):
    pass


class RenderError(Spec2VizError):
    pass


__all__ = [
    "Spec2VizError",
    "ParseError",
    "ValidationError",
    "CompileError",
    "RenderError",
]
