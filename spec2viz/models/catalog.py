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


class DiagramStoreItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str | None = None
    desc: str | None = None
    category: str | None = None
    nav: str | None = None
    lbl: str | None = None
    src: str | None = None
    mmd: str | None = None
    specs: list[str] = Field(default_factory=list)
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
