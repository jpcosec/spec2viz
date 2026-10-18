"""Notaciones: el vocabulario visual de un tipo de diagrama como datos.

Una notacion es un YAML con un `NotationDoc`, sus `GlyphDoc` (como se ve cada clase de
elemento) y sus `LinkDoc` (como se ve cada relacion). spec2viz trae notaciones builtin en
`spec2viz/notations/` y acepta otras por ruta. Aqui se cargan y validan; `sldb_sync` las
escribe al store y graph_ui las lee para dibujar.

Lo que se valida es la gramatica de la notacion, no el store: ids unicos, enumeraciones
(`draw`, `line`, terminales, `level`, `layout.kind`), que las relaciones nombradas existan
en el tipo de diagrama cuando ese tipo las fija, que haya un glifo por defecto (sin
`where`) y que cada `where` parsee en la gramatica de `sldb find --where`.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from spec2viz.exceptions import ValidationError
from spec2viz.models.base import DiagramType

NOTATIONS_DIR = Path(__file__).parent / "notations"

# notacion por defecto de cada tipo de diagrama; los tipos ausentes no llevan notacion
DEFAULT_NOTATIONS: dict[str, str] = {
    "class": "uml-class",
    "state": "statechart",
    "component": "component",
    "deployment": "deployment",
    "sequence": "uml-sequence",
    "activity": "activity",
    "component_view_matrix": "component-view-matrix",
    "reflection": "reflection",
}

# el link comodin: dibuja toda relacion que ningun otro link de la notacion nombre
ANY_RELATION = "*"

DRAW_KINDS = ("line", "nest", "lane", "cell", "axis")
LINE_KINDS = ("solid", "dashed", "dotted")
TERMINALS = (
    "none", "open-arrow", "filled-arrow", "hollow-triangle", "filled-triangle",
    "hollow-diamond", "filled-diamond", "filled-circle", "hollow-circle", "bar", "crowfoot",
)
LEVELS = ("types", "instances", "both")
LAYOUT_KINDS = ("graph", "tree", "lanes", "grid", "axis", "manual")

# relaciones que cada tipo de diagrama emite al sincronizar (`sldb_sync.spec_edges` mas
# `contains`); None = relaciones libres, no se comprueban
KNOWN_RELATIONS: dict[str, frozenset[str] | None] = {
    "class": frozenset({"inheritance", "realization", "composition", "aggregation", "association", "dependency", "contains"}),
    "state": frozenset({"transitions_to", "contains"}),
    "sequence": frozenset({"sends", "sends_async", "returns", "contains"}),
    "activity": frozenset({"next", "branch", "contains"}),
    "component_view_matrix": frozenset({"occupies", "contains"}),
    "component": None,
    "deployment": None,
    "reflection": None,
}

_NAME = re.compile(r"^[a-z0-9][a-z0-9-]*$")
_ID = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


class GlyphSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str = ""
    model: str
    where: str = ""
    shape: str
    label: str = "{title}"
    label_style: str = ""
    keyword: str = ""
    compartments: list[str] = Field(default_factory=list)
    function: str = ""
    form: str = ""
    description: str = ""

    @field_validator("id")
    @classmethod
    def _id(cls, v: str) -> str:
        if not _ID.match(v):
            raise ValueError(f"glyph id {v!r} must match {_ID.pattern}")
        return v

    @field_validator("where")
    @classmethod
    def _where(cls, v: str) -> str:
        _check_where(v)
        return v


class LinkEndSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    relation: str = ""
    label: str = ""
    terminal: str | dict = "none"


class LinkSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str = ""
    relation: str
    model: str = ""
    draw: Literal["line", "nest", "lane", "cell", "axis"] = "line"
    line: Literal["solid", "dashed", "dotted"] = "solid"
    source_end: str = "none"
    target_end: str = "open-arrow"
    label: str = ""
    source_label: str = ""
    target_label: str = ""
    ends: dict[str, LinkEndSpec] = Field(default_factory=dict)
    form: str = ""
    description: str = ""

    @field_validator("id")
    @classmethod
    def _id(cls, v: str) -> str:
        if not _ID.match(v):
            raise ValueError(f"link id {v!r} must match {_ID.pattern}")
        return v

    @field_validator("relation")
    @classmethod
    def _relation(cls, v: str) -> str:
        if v != ANY_RELATION and not _ID.match(v):
            raise ValueError(f"relation {v!r} must be a vocabulary token ({_ID.pattern}) or '*'")
        return v

    @field_validator("source_end", "target_end")
    @classmethod
    def _terminal(cls, v: str) -> str:
        if v not in TERMINALS:
            raise ValueError(f"terminal {v!r} is not one of {', '.join(TERMINALS)}")
        return v

    @model_validator(mode="after")
    def _reified_has_ends(self) -> "LinkSpec":
        if self.model and not self.ends:
            raise ValueError(f"link {self.id!r} names a reified model {self.model!r} but declares no ends")
        return self


class MarkerSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    shape: str
    model: str
    where: str = ""

    @field_validator("where")
    @classmethod
    def _where(cls, v: str) -> str:
        _check_where(v)
        return v


class NotationSpec(BaseModel):
    """Una notacion completa, tal como esta en su YAML."""

    model_config = ConfigDict(extra="forbid")

    name: str
    title: str = ""
    diagram_type: str
    level: Literal["types", "instances", "both"] = "types"
    projection: str = "all"
    layout: dict[str, Any] = Field(default_factory=lambda: {"kind": "graph"})
    markers: list[MarkerSpec] = Field(default_factory=list)
    glyphs: list[GlyphSpec] = Field(min_length=1)
    links: list[LinkSpec] = Field(default_factory=list)
    description: str = ""

    @field_validator("name")
    @classmethod
    def _name(cls, v: str) -> str:
        if not _NAME.match(v):
            raise ValueError(f"notation name {v!r} must match {_NAME.pattern}")
        return v

    @field_validator("diagram_type")
    @classmethod
    def _diagram_type(cls, v: str) -> str:
        if v not in {t.value for t in DiagramType}:
            raise ValueError(f"diagram_type {v!r} is not a spec2viz diagram type")
        return v

    @field_validator("layout")
    @classmethod
    def _layout(cls, v: dict) -> dict:
        kind = v.get("kind", "graph")
        if kind not in LAYOUT_KINDS:
            raise ValueError(f"layout.kind {kind!r} is not one of {', '.join(LAYOUT_KINDS)}")
        if "direction" in v and v["direction"] not in ("TB", "LR", "BT", "RL"):
            raise ValueError(f"layout.direction {v['direction']!r} must be TB, LR, BT or RL")
        return {"kind": kind, **{k: val for k, val in v.items() if k != "kind"}}

    @model_validator(mode="after")
    def _consistent(self) -> "NotationSpec":
        problems: list[str] = []
        for what, items in (("glyph", self.glyphs), ("link", self.links), ("marker", self.markers)):
            ids = [i.id for i in items]
            for dup in sorted({i for i in ids if ids.count(i) > 1}):
                problems.append(f"{what} id {dup!r} is declared more than once")
        models = {g.model for g in self.glyphs}
        for model in sorted(models):
            if not any(g.model == model and not g.where for g in self.glyphs):
                problems.append(f"model {model!r} has no default glyph (one without `where`)")
        known = KNOWN_RELATIONS.get(self.diagram_type)
        if known is not None:
            for link in self.links:
                if link.relation != ANY_RELATION and link.relation not in known:
                    problems.append(
                        f"link {link.id!r} draws relation {link.relation!r}, which a `{self.diagram_type}` spec never emits "
                        f"(known: {', '.join(sorted(known))})"
                    )
        relations = [l.relation for l in self.links if not l.model]
        for dup in sorted({r for r in relations if relations.count(r) > 1}):
            problems.append(f"relation {dup!r} is drawn by more than one link")
        if problems:
            raise ValueError("; ".join(problems))
        return self

    # --- vista util --------------------------------------------------------------------

    @property
    def relations(self) -> list[str]:
        """Relaciones que la notacion nombra, en orden de declaracion y sin repetir."""
        out: list[str] = []
        for link in self.links:
            for rel in [link.relation, *(e.relation for e in link.ends.values() if e.relation)]:
                if rel and rel != ANY_RELATION and rel not in out:
                    out.append(rel)
        return out

    @property
    def models(self) -> list[str]:
        """Modelos que la notacion nombra (glifos, marcas y relaciones reificadas)."""
        out: list[str] = []
        for m in [*(g.model for g in self.glyphs), *(m.model for m in self.markers), *(l.model for l in self.links if l.model)]:
            if m not in out:
                out.append(m)
        return out


def _check_where(expression: str) -> None:
    """Un `where` tiene que parsear en la gramatica de sldb; sin sldb instalado no se comprueba."""
    if not expression:
        return
    try:
        from sldb.api import where_matches
    except Exception:  # pragma: no cover - sldb opcional
        return
    try:
        where_matches(expression, {})
    except Exception as exc:  # WherePredicateError y afines
        raise ValueError(f"where {expression!r} does not parse: {exc}") from exc


# --- carga --------------------------------------------------------------------------


def builtin_notations() -> dict[str, Path]:
    """Las notaciones que spec2viz trae, por nombre."""
    return {p.stem: p for p in sorted(NOTATIONS_DIR.glob("*.yml"))}


def resolve_notation(name_or_path: str | Path) -> Path:
    """La ruta de una notacion: un nombre builtin o un YAML propio."""
    text = str(name_or_path)
    builtin = builtin_notations()
    if text in builtin:
        return builtin[text]
    path = Path(text)
    if path.is_file():
        return path.resolve()
    raise ValidationError(f"unknown notation {text!r}: not a builtin ({', '.join(builtin) or 'none'}) nor a file")


def load_notation(name_or_path: str | Path) -> NotationSpec:
    """Carga y valida una notacion; `ValidationError` si no es valida."""
    path = resolve_notation(name_or_path)
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ValidationError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValidationError(f"{path}: a notation is a mapping")
    try:
        return NotationSpec.model_validate(raw)
    except ValueError as exc:
        raise ValidationError(f"{path}: {exc}") from exc


def notation_ref(name: str) -> str:
    return f"NotationDoc:{name}"


def glyph_ref(notation: str, glyph_id: str) -> str:
    return f"GlyphDoc:{notation}.{glyph_id}"


def link_ref(notation: str, link_id: str) -> str:
    return f"LinkDoc:{notation}.{link_id}"


__all__ = [
    "DEFAULT_NOTATIONS", "KNOWN_RELATIONS", "ANY_RELATION", "TERMINALS", "DRAW_KINDS", "LINE_KINDS",
    "NotationSpec", "GlyphSpec", "LinkSpec", "MarkerSpec",
    "builtin_notations", "resolve_notation", "load_notation",
    "notation_ref", "glyph_ref", "link_ref",
]
