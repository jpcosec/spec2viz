"""Style resolution and the error root of sldb's notations, taken from SLDB, never defined here.

The renderers color elements with the one precedence that sldb owns (glyph > `style.kinds` of the
spec > palette, `sldb.notations.resolve_style`) and write text in the ink of sldb's builtin
`default` palette (`sldb.notations.load_palette`). The commands report sldb's loading and
validation errors (`sldb.notations.NotationError`, the root of `ParseError` and `ValidationError`).
`sldb.api` does not export these three yet (asked to sldb's desk), so this module is the only one of
specIR that reaches `sldb.notations` (tests/test_imports.py allows it here and nowhere else). When
sldb exports them from `sldb.api.notations`, only these imports change."""

from __future__ import annotations

from functools import lru_cache

from sldb.notations import NotationError, load_palette, resolve_style


@lru_cache(maxsize=1)
def default_ink() -> dict[str, str]:
    """The text color (`{light, dark}`) of sldb's builtin `default` palette."""
    return load_palette().ink.model_dump()


__all__ = ["NotationError", "default_ink", "resolve_style"]
