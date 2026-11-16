"""Style resolution and the error root of sldb's notations, taken from SLDB, never defined here.

The renderers color elements with the one precedence that sldb owns (glyph > `style.kinds` of the
spec > palette, `sldb.notations.resolve_style`) and write text in the ink of sldb's builtin
`default` palette (`sldb.notations.load_palette`). The commands report sldb's loading and
validation errors (`sldb.notations.NotationError`, the root of `ParseError` and `ValidationError`).
The catalog (IR13b) reports the typed errors of the catalog path rule (`AmbiguousPathError`,
`UnknownReferenceError`, `UnknownNotationError`) and picks a view's notation with
`DEFAULT_NOTATIONS` and `builtin_notations`.
The notation and palette tests ported from spec2viz (IR13e, tests/visual/test_notations_parity.py)
load, validate and compare sldb's notations and palettes with the rest of what this module
re-exports from `sldb.notations`: `load_notation`, `NotationSpec`, `SHAPES`, `DiagramType`,
`load_palette`, `PaletteSpec`, `check_palette`, `contrast`, `resolve_color` and the typed errors
(`ValidationError`, `InvalidColorError`, `UnknownIconError`, `UnknownKindError`,
`UnknownShapeError`). Nothing here is defined by specIR.
`sldb.api` does not export these yet (asked to sldb's desk), so this module is the only one of
specIR that reaches `sldb.notations` (tests/test_imports.py allows it here and nowhere else). When
sldb exports them from `sldb.api.notations`, only these imports change."""

from __future__ import annotations

from functools import lru_cache

from sldb.notations import (
    DEFAULT_NOTATIONS,
    SHAPES,
    AmbiguousPathError,
    DiagramType,
    InvalidColorError,
    NotationError,
    NotationSpec,
    PaletteSpec,
    UnknownIconError,
    UnknownKindError,
    UnknownNotationError,
    UnknownReferenceError,
    UnknownShapeError,
    ValidationError,
    builtin_notations,
    check_palette,
    contrast,
    load_notation,
    load_palette,
    resolve_color,
    resolve_style,
)


@lru_cache(maxsize=1)
def default_ink() -> dict[str, str]:
    """The text color (`{light, dark}`) of sldb's builtin `default` palette."""
    return load_palette().ink.model_dump()


__all__ = [
    "DEFAULT_NOTATIONS", "SHAPES", "AmbiguousPathError", "DiagramType", "InvalidColorError", "NotationError",
    "NotationSpec", "PaletteSpec", "UnknownIconError", "UnknownKindError", "UnknownNotationError",
    "UnknownReferenceError", "UnknownShapeError", "ValidationError", "builtin_notations", "check_palette",
    "contrast", "default_ink", "load_notation", "load_palette", "resolve_color", "resolve_style",
]
