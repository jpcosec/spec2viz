"""Estilo de un elemento: una sola fuente con precedencia explicita.

Por cada propiedad (`fill`, `stroke`, `icon`) gana la primera capa que la define:

1. el glifo de la notacion: sus `fill`/`stroke`/`icon` explicitos y, detras, el kind de la paleta
   que nombra con `kind`;
2. `style.kinds` del spec para el kind del elemento (claves neutrales `fill`, `stroke`, `icon`);
3. la paleta de la notacion para el kind del elemento (solo si la notacion usa paleta).

Un color es un token de la paleta o un hex `#rrggbb` y se resuelve a `{light, dark}`; un token
del spec sin paleta en la notacion resuelve contra la paleta builtin `default`. `resolve_view`
devuelve el resultado ya aplicado (y el renderer de mermaid usa la misma funcion), asi que una
superficie no recalcula nada.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

PROPERTIES = ("fill", "stroke", "icon")


@lru_cache(maxsize=1)
def _builtin_default() -> dict[str, Any]:
    from spec2viz.palette import load_palette

    palette = load_palette()
    return {
        "name": palette.name,
        "colors": {k: v.model_dump() for k, v in palette.colors.items()},
        "kinds": {k: v.model_dump() for k, v in palette.kinds.items()},
        "icon_set": palette.icon_set.model_dump(),
        "ink": palette.ink.model_dump(),
    }


def _value(prop: str, raw: str, tokens: dict[str, Any], where: str) -> Any:
    from spec2viz.palette import resolve_color

    if prop == "icon":
        return raw
    return resolve_color(raw, tokens, where)


def resolve_style(glyph: dict[str, Any] | None, kind: str, spec_kinds: dict[str, dict] | None,
                  palette: dict[str, Any] | None) -> dict[str, Any]:
    """`{fill, stroke, icon, source}` de un elemento; `fill`/`stroke` son `{light, dark}`.

    `glyph` es el payload del GlyphDoc (o None), `kind` el del elemento, `spec_kinds` el
    `style.kinds` neutral del spec y `palette` el payload del PaletteDoc de la notacion (o None si
    la notacion no usa paleta). Solo aparecen las propiedades que alguna capa define; `source`
    dice de que capa salio cada una (`glyph`, `spec` o `palette`).
    """
    glyph = glyph or {}
    tokens = dict((palette or _builtin_default()).get("colors") or {})
    kinds = dict((palette or {}).get("kinds") or {})
    layers: list[tuple[str, dict[str, Any]]] = [("glyph", {p: glyph.get(p) for p in PROPERTIES})]
    if glyph.get("kind"):
        layers.append(("glyph", dict(kinds.get(glyph["kind"]) or _builtin_default()["kinds"].get(glyph["kind"]) or {})))
    if spec_kinds and kind in spec_kinds:
        layers.append(("spec", dict(spec_kinds[kind])))
    if palette is not None and kind in kinds:
        layers.append(("palette", dict(kinds[kind])))
    out: dict[str, Any] = {}
    source: dict[str, str] = {}
    for prop in PROPERTIES:
        for layer, values in layers:
            if values.get(prop):
                raw = values[prop] if isinstance(values[prop], dict) else str(values[prop])
                out[prop] = _value(prop, raw, tokens, f"{layer} {prop}")
                source[prop] = layer
                break
    if out:
        out["source"] = source
    return out


def resolve_line_color(link: dict[str, Any] | None, palette: dict[str, Any] | None) -> dict[str, str] | None:
    """El color de la linea de un link (`{light, dark}`) o None si no lo define."""
    from spec2viz.palette import resolve_color

    color = (link or {}).get("color")
    if not color:
        return None
    return resolve_color(color if isinstance(color, dict) else str(color), dict((palette or _builtin_default()).get("colors") or {}), "link color")


__all__ = ["PROPERTIES", "resolve_style", "resolve_line_color"]
