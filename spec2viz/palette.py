"""Paletas: colores, forma e icono por defecto de los kinds comunes, como datos.

Una paleta es un YAML con fondos e `ink` (texto) por tema, un set de iconos declarado, tokens de
color (`database-fill: {light, dark}`) y, por kind, su forma, icono, relleno y trazo. spec2viz trae
paletas builtin en `spec2viz/palettes/` (hoy `default`); `palette sync` (o `notation sync` de una
notacion que la usa) la escribe al store como `PaletteDoc`, y graph_ui la recibe ya aplicada en
`resolve_view`.

Un color es un token de la paleta o un hex `#rrggbb` (vale para los dos temas). Se valida la
gramatica y la accesibilidad: trazos >= 3:1 contra el fondo de cada tema (WCAG 1.4.11), texto
sobre cada relleno >= 4.5:1 (AA), y un par (forma, icono) distinto por kind para que el color no
sea la unica senal.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

from spec2viz.exceptions import InvalidColorError, UnknownIconError, UnknownKindError, UnknownShapeError, ValidationError

PALETTES_DIR = Path(__file__).parent / "palettes"
DEFAULT_PALETTE = "default"
THEMES = ("light", "dark")
HEX = re.compile(r"^#[0-9a-fA-F]{6}$")
ICON_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# contraste minimo (WCAG 2.2): objetos graficos y texto normal
MIN_GRAPHIC_CONTRAST = 3.0
MIN_TEXT_CONTRAST = 4.5


class ThemeColor(BaseModel):
    model_config = ConfigDict(extra="forbid")

    light: str
    dark: str


class IconSet(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    version: str = ""
    icons: list[str] = Field(min_length=1)


class KindStyle(BaseModel):
    model_config = ConfigDict(extra="forbid")

    shape: str
    icon: str
    fill: str
    stroke: str


class PaletteSpec(BaseModel):
    """Una paleta completa, tal como esta en su YAML."""

    model_config = ConfigDict(extra="forbid")

    name: str
    title: str = ""
    backgrounds: ThemeColor
    ink: ThemeColor
    icon_set: IconSet
    colors: dict[str, ThemeColor] = Field(default_factory=dict)
    kinds: dict[str, KindStyle] = Field(default_factory=dict)
    description: str = ""

    def color(self, value: str, where: str = "") -> dict[str, str]:
        """Un token o un hex -> `{light, dark}`; `InvalidColorError` si no es ninguno."""
        return resolve_color(value, self.colors, where)


# --- colores ------------------------------------------------------------------------


def resolve_color(value: str, tokens: dict[str, Any], where: str = "") -> dict[str, str]:
    """Un color (`#rrggbb` o un token de la paleta) como `{light, dark}`."""
    text = str(value or "").strip()
    if HEX.match(text):
        return {"light": text.lower(), "dark": text.lower()}
    if text in tokens:
        token = tokens[text]
        token = token.model_dump() if isinstance(token, BaseModel) else dict(token)
        return {"light": str(token["light"]).lower(), "dark": str(token["dark"]).lower()}
    at = f"{where}: " if where else ""
    raise InvalidColorError(f"{at}color {text!r} is neither a `#rrggbb` hex nor a palette token ({', '.join(sorted(tokens)) or 'none'})")


def _channel(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    r, g, b = (_channel(int(h[i:i + 2], 16) / 255) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    """Razon de contraste WCAG entre dos hex."""
    la, lb = luminance(a), luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# --- validacion ---------------------------------------------------------------------


def check_palette(palette: PaletteSpec) -> None:
    """Gramatica y accesibilidad de una paleta; errores tipados (`ValidationError` y subclases)."""
    from spec2viz.notation import SHAPES

    for theme in THEMES:
        for what, color in (("backgrounds", palette.backgrounds), ("ink", palette.ink)):
            value = getattr(color, theme)
            if not HEX.match(value):
                raise InvalidColorError(f"palette {palette.name}: {what}.{theme} {value!r} is not a `#rrggbb` hex")
    for token, color in palette.colors.items():
        for theme in THEMES:
            if not HEX.match(getattr(color, theme)):
                raise InvalidColorError(f"palette {palette.name}: token {token!r}.{theme} {getattr(color, theme)!r} is not a `#rrggbb` hex")
    for icon in palette.icon_set.icons:
        if not ICON_NAME.match(icon):
            raise UnknownIconError(f"palette {palette.name}: icon {icon!r} is not a {palette.icon_set.name} icon name (kebab-case, no URLs)")
    pairs: dict[tuple[str, str], str] = {}
    for kind, style in palette.kinds.items():
        where = f"palette {palette.name}, kind {kind}"
        if style.shape not in SHAPES:
            raise UnknownShapeError(f"{where}: shape {style.shape!r} is not one of {', '.join(SHAPES)}")
        if style.icon not in palette.icon_set.icons:
            raise UnknownIconError(f"{where}: icon {style.icon!r} is not in the {palette.icon_set.name} icon set")
        fill, stroke = palette.color(style.fill, where), palette.color(style.stroke, where)
        for theme in THEMES:
            background, ink = getattr(palette.backgrounds, theme), getattr(palette.ink, theme)
            if contrast(stroke[theme], background) < MIN_GRAPHIC_CONTRAST:
                raise ValidationError(f"{where}: stroke {stroke[theme]} contrasts {contrast(stroke[theme], background):.2f}:1 with the {theme} background {background}; WCAG 1.4.11 needs {MIN_GRAPHIC_CONTRAST}:1")
            if contrast(ink, fill[theme]) < MIN_TEXT_CONTRAST:
                raise ValidationError(f"{where}: text {ink} on fill {fill[theme]} ({theme}) contrasts {contrast(ink, fill[theme]):.2f}:1; WCAG AA needs {MIN_TEXT_CONTRAST}:1")
        pair = (style.shape, style.icon)
        if pair in pairs:
            raise ValidationError(f"{where}: shape and icon {pair} repeat kind {pairs[pair]!r}; colour must not be the only cue")
        pairs[pair] = kind


# --- carga --------------------------------------------------------------------------


def builtin_palettes() -> dict[str, Path]:
    return {p.stem: p for p in sorted(PALETTES_DIR.glob("*.yml"))}


def resolve_palette(name_or_path: str | Path, base: Path | None = None) -> Path:
    """La ruta de una paleta: un nombre builtin o un YAML propio (relativo a `base` si se da)."""
    text = str(name_or_path)
    builtin = builtin_palettes()
    if text in builtin:
        return builtin[text]
    path = Path(text)
    if not path.is_absolute() and base is not None:
        path = base / path
    if path.is_file():
        return path.resolve()
    raise ValidationError(f"unknown palette {text!r}: not a builtin ({', '.join(builtin) or 'none'}) nor a file")


def load_palette(name_or_path: str | Path = DEFAULT_PALETTE, base: Path | None = None) -> PaletteSpec:
    """Carga y valida una paleta; errores tipados si no es valida."""
    path = resolve_palette(name_or_path, base)
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ValidationError(f"{path}: invalid YAML: {exc}") from exc
    try:
        palette = PaletteSpec.model_validate(raw)
    except ValueError as exc:
        raise ValidationError(f"{path}: {exc}") from exc
    check_palette(palette)
    return palette


def palette_ref(name: str) -> str:
    return f"PaletteDoc:{name}"


__all__ = [
    "PaletteSpec", "KindStyle", "IconSet", "ThemeColor", "DEFAULT_PALETTE", "THEMES",
    "resolve_color", "contrast", "luminance", "check_palette",
    "builtin_palettes", "resolve_palette", "load_palette", "palette_ref",
]
