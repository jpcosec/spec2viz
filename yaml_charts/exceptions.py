"""Exception hierarchy for the yaml_charts pipeline.

One exception type per pipeline stage:
  ParseError      — YAML parsing
  ValidationError — semantic validation
  CompileError    — IR compilation
  RenderError     — renderer output
"""


class YamlChartsError(Exception):
    pass


class ParseError(YamlChartsError):
    pass


class ValidationError(YamlChartsError):
    pass


class CompileError(YamlChartsError):
    pass


class RenderError(YamlChartsError):
    pass


__all__ = [
    "YamlChartsError",
    "ParseError",
    "ValidationError",
    "CompileError",
    "RenderError",
]
