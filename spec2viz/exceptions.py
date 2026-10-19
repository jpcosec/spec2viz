"""Exception hierarchy for the spec2viz pipeline.

One exception type per pipeline stage:
  ParseError      — YAML parsing
  ValidationError — semantic validation (typed subclasses below, so callers can tell the
                    problems apart; catching ValidationError still catches them all)
  CompileError    — IR compilation
  RenderError     — renderer output
"""


class Spec2VizError(Exception):
    pass


class ParseError(Spec2VizError):
    pass


class ValidationError(Spec2VizError):
    pass


class UnknownReferenceError(ValidationError):
    """A spec names an id that does not exist (a step, a node, an artifact)."""


class EndpointKindError(ValidationError):
    """The id exists but its kind is not allowed at that end (a «deploy» whose target is an artifact)."""


class StructureError(ValidationError):
    """The shape of the spec is wrong: a containment cycle, a duplicated id, a merge with branches."""


class UnknownKindError(ValidationError):
    """A notation or a spec style names a kind the palette does not declare."""


class InvalidColorError(ValidationError):
    """A color that is neither a palette token nor a `#rrggbb` hex."""


class UnknownIconError(ValidationError):
    """An icon that is not in the declared icon set."""


class UnknownShapeError(ValidationError):
    """A glyph or marker shape that is not a builtin shape."""


class CompileError(Spec2VizError):
    pass


class RenderError(Spec2VizError):
    pass


__all__ = [
    "Spec2VizError",
    "ParseError",
    "ValidationError",
    "UnknownReferenceError",
    "EndpointKindError",
    "StructureError",
    "UnknownKindError",
    "InvalidColorError",
    "UnknownIconError",
    "UnknownShapeError",
    "CompileError",
    "RenderError",
]
