from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DiagramStoreRef(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str
    project: str | None = None
    category: str | None = None
    type: str | None = None
    tags: list[str] = Field(default_factory=list)


_PATH_RULE = (
    "Relative paths follow one rule for `src`, `mmd`, `specs` and `notation`: first next to the config file "
    "(the folder of the vistas.yml), then from the repo root (nearest ancestor with `.git`, else `.sldb`). "
    "If both exist and are different files the path is ambiguous (AmbiguousPathError); if neither exists the "
    "error lists the paths tried."
)


class DiagramStoreItem(BaseModel):
    """A catalog view: an item of a diagram store or an entry of a legacy `vistas.yml`."""

    model_config = ConfigDict(extra="forbid", json_schema_extra={"description": "A catalog view. " + _PATH_RULE})

    id: str
    title: str | None = None
    desc: str | None = None
    category: str | None = None
    nav: str | None = None
    lbl: str | None = None
    src: str | None = Field(default=None, description="Rendered source of the view (`.mmd`, `.svg`, `.html`, optionally `#fragment`). " + _PATH_RULE)
    mmd: str | None = Field(default=None, description="Legacy alias of `src`. " + _PATH_RULE)
    specs: list[str] = Field(default_factory=list, description="Spec YAML files of the view (a path with extension; an id without extension keeps the legacy lookup). " + _PATH_RULE)
    notation: str | None = Field(
        default=None,
        description="Notation the view is synced with: a path to a notation YAML, a builtin name or the name of a NotationDoc in the store; absent = the builtin of the spec's type. " + _PATH_RULE,
    )
    puml: str | None = None
    notes: list[str] = Field(default_factory=list)
    project: str | None = None
    type: str | None = None
    tags: list[str] = Field(default_factory=list)


class DiagramStore(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal["diagram-store"] = "diagram-store"
    template: str = "template.html"
    title: str | None = None
    catalog_title: str | None = None
    brand_name: str | None = None
    brand_subtitle: str | None = None
    project_name: str | None = None
    project: str | None = None
    category: str | None = None
    type: str | None = None
    html_artifact: str | None = None
    tags: list[str] = Field(default_factory=list)
    stores: list[str | DiagramStoreRef] = Field(default_factory=list)
    items: list[DiagramStoreItem] = Field(default_factory=list)


class DiagramStoreEnvelope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    diagram_store: DiagramStore
