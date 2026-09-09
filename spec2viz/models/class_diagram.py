"""Language-neutral class, protocol and record contracts.

Relationships are directed: child -> parent for inheritance/realization,
owner -> part for composition/aggregation, client -> supplier otherwise.
"""
from __future__ import annotations

from typing import Annotated, Literal
from pydantic import BaseModel, ConfigDict, Field, StringConstraints
from spec2viz.models.base import BaseDiagram, DiagramType

Identifier = Annotated[str, StringConstraints(pattern=r"^[A-Za-z_][A-Za-z0-9_]*$")]
MemberName = Annotated[str, StringConstraints(pattern=r"^[A-Za-z_][A-Za-z0-9_?!-]*$")]
# Type names are display expressions, not a language-specific type checker.
TypeName = Annotated[str, StringConstraints(pattern=r"^[A-Za-z_][A-Za-z0-9_.\[\], ?|<>-]*$")]
Label = Annotated[str, StringConstraints(min_length=1, pattern=r'^[^\r\n{}\\"]+$')]
Visibility = Literal["public", "private", "protected", "package"]
Multiplicity = Annotated[str, StringConstraints(pattern=r"^(?:\*|[0-9]+(?:\.\.(?:[0-9]+|\*))?)$")]


class ClassParameter(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: MemberName
    type: TypeName


class ClassAttribute(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: MemberName
    type: TypeName
    visibility: Visibility = "public"
    static: bool = False


class ClassMethod(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: MemberName
    parameters: list[ClassParameter] = Field(default_factory=list)
    returns: TypeName = "void"
    visibility: Visibility = "public"
    abstract: bool = False
    static: bool = False


class ClassDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: Label | None = None
    kind: Literal["class", "interface", "abstract", "record", "protocol", "enum"] = "class"
    attributes: list[ClassAttribute] = Field(default_factory=list)
    methods: list[ClassMethod] = Field(default_factory=list)


class ClassRelation(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    from_: Identifier = Field(alias="from")
    to: Identifier
    relation: Literal["inheritance", "realization", "composition", "aggregation", "association", "dependency"]
    label: Label | None = None
    from_multiplicity: Multiplicity | None = None
    to_multiplicity: Multiplicity | None = None


class ClassData(BaseModel):
    model_config = ConfigDict(extra="forbid")
    direction: Literal["TB", "LR"] = "TB"
    classes: dict[Identifier, ClassDefinition] = Field(min_length=1)
    relations: list[ClassRelation] = Field(default_factory=list)


class ClassDiagram(BaseDiagram):
    model_config = ConfigDict(extra="forbid")
    type: Literal[DiagramType.class_] = DiagramType.class_
    data: ClassData
