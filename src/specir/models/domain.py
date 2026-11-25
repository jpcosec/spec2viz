"""The cross-layer domain types of specIR: one SLDB model per kind of element a software system is
described with, from the interface control down to the table.

They are `StructuredNLDoc` subclasses, code of specIR registered in a store by SLDB's model
registry (`sldb.api.add_model`, `specir.install`), as deskops registers its own. What connects
them is data of the store, not code: the relation types (`RelationTypeDoc`) and the cross-layer
invariants (`RuleDoc`) that `specir.install` seeds from `specir/data/`.

Every node carries the provenance decided in IR05 (docs/decisiones/procedencia-y-divergencia.md):
two axes in its own fields, `origen` and `verificacion` (with `verificado_por` and `evidencia`),
and what is not known is `null` and named in `desconocidos` with its reason. The `authority` of
the `sldb` block follows the decided table and is SLDB's: these models declare `authored`, the
authority of `declarado` and `inferido`, the two origins an MCP writer can claim (an extractor
writing `observado` or `derivado` sets its own; IR08 and later).

No visual vocabulary of SLDB (`sldb.models.notation_models`: views, notations, glyphs) is
redefined here: a view of these documents is an SLDB `ViewDoc`.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import Field, field_validator, model_validator

from sldb.api import StructuredNLDoc

Origen = Literal["observado", "derivado", "inferido", "declarado"]
Verificacion = Literal["sin_verificar", "verificado", "refutado"]

#: Who may verify (IR05 D2-E): a human outside the MCP or a deterministic check.
VERIFIERS = ("human:", "check:")

#: The provenance fields every node and every edge (in `RelationDoc.attributes`) carries.
PROVENANCE_FIELDS = ("origen", "verificacion", "verificado_por", "evidencia", "desconocidos")


def check_provenance(values: dict[str, Any], known: set[str] | None = None) -> None:
    """The decided taxonomy on one node or edge: `verificado` names who verified it and with
    what; each name in `desconocidos` is a field that is `null` (when `known` lists the fields)."""
    if values.get("verificacion") == "verificado":
        by = values.get("verificado_por") or ""
        if not by.startswith(VERIFIERS):
            raise ValueError(f"verificado needs verificado_por human:<id> or check:<id>, not {by!r}")
        if not values.get("evidencia"):
            raise ValueError("verificado needs its evidencia")
    for name in values.get("desconocidos") or {}:
        if known is not None and name not in known:
            raise ValueError(f"desconocidos names {name!r}, which is not a field of this document")
        if known is not None and values.get(name) not in (None, "", []):
            raise ValueError(f"desconocidos names {name!r}, but it has a value; an unknown field is null")


def _template(fields: list[tuple[str, str]]) -> str:
    """Front matter with the provenance and the type's own fields, the title and the description.
    A field that may be unknown uses SLDB's `optrev`: `null` leaves no line, and reads back `null`."""
    own = "\n".join(f"{name}: ⸢{marker}•{name}⸥" for name, marker in fields)
    return f"""---
origen: ⸢rev•origen⸥
verificacion: ⸢rev•verificacion⸥
verificado_por: ⸢rev•verificado_por⸥
evidencia: ⸢rev•evidencia⸥
desconocidos: ⸢rev,dict•desconocidos⸥
{own}
---
# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()


class SpecIRNodeDoc(StructuredNLDoc):
    """A node of a software system's model in specIR, with its provenance. A base: it is not
    registered in a store; its subclasses are."""

    __authority__ = "authored"
    __semantics__ = {"type": ["specir", "node"], "layer": ["system"]}

    title: str = Field(description="The element's name, shown as the H1 heading.")
    origen: Origen = Field(description="How the claim was obtained (IR05 D1-B): observado, derivado, inferido or declarado.")
    verificacion: Verificacion = Field(default="sin_verificar", description="Whether someone confirmed it (IR05 D1-B): sin_verificar, verificado or refutado.")
    verificado_por: str = Field(default="", description="Who verified or refuted it: human:<id> or check:<id>; empty while sin_verificar.")
    evidencia: str = Field(default="", description="What the verification rests on (a test, an anchored observation); empty while sin_verificar.")
    desconocidos: dict[str, str] = Field(default_factory=dict, description="Fields whose value is not known (null), each with the reason (IR05 D2-B).")
    description: str = Field(default="", description="Markdown section describing the element.")

    @model_validator(mode="after")
    def _provenance(self) -> "SpecIRNodeDoc":
        check_provenance(self.model_dump(), set(type(self).model_fields))
        return self


class InterfaceControlDoc(SpecIRNodeDoc):
    """A control of a user interface the user acts on: a button, a menu entry, a form."""

    __semantics__ = {"type": ["specir", "node", "interface_control"], "layer": ["interface"]}
    __template__ = _template([("kind", "optrev"), ("component", "optrev")])

    kind: str | None = Field(default=None, description="What kind of control it is: button, menu_item, form, link.")
    component: str | None = Field(default=None, description="The interface component that renders it (e.g. a React component name).")


class InterfaceActionDoc(SpecIRNodeDoc):
    """What the interface does when a control is used: the action, apart from the control that triggers it."""

    __semantics__ = {"type": ["specir", "node", "interface_action"], "layer": ["interface"]}
    __template__ = _template([("event", "optrev")])

    event: str | None = Field(default=None, description="The interface event the action answers (click, submit).")


class InterfaceFieldDoc(SpecIRNodeDoc):
    """A field the interface shows or sends: an input of a form, a column of a list."""

    __semantics__ = {"type": ["specir", "node", "interface_field"], "layer": ["interface"]}
    __template__ = _template([("component", "optrev")])

    component: str | None = Field(default=None, description="The interface component that shows or collects it.")


class ApiOperationDoc(SpecIRNodeDoc):
    """An operation the API exposes: an endpoint and its method."""

    __semantics__ = {"type": ["specir", "node", "api_operation"], "layer": ["api"]}
    __template__ = _template([("method", "optrev"), ("route", "optrev")])

    method: str | None = Field(default=None, description="The HTTP method (GET, POST, ...).")
    route: str | None = Field(default=None, description="The route template, e.g. /posts/{id}/publish.")


class ApiFieldDoc(SpecIRNodeDoc):
    """A field of what an API operation receives or returns: an attribute of its serializer."""

    __semantics__ = {"type": ["specir", "node", "api_field"], "layer": ["api"]}
    __template__ = _template([("serializer", "optrev")])

    serializer: str | None = Field(default=None, description="The serializer or schema that declares it.")


class HandlerDoc(SpecIRNodeDoc):
    """The backend code that receives an API operation: a view, a viewset action, a controller."""

    __semantics__ = {"type": ["specir", "node", "handler"], "layer": ["backend"]}
    __template__ = _template([("framework", "optrev"), ("symbol", "optrev")])

    framework: str | None = Field(default=None, description="The framework the handler is written in (e.g. django-rest-framework).")
    symbol: str | None = Field(default=None, description="The handler's qualified name in the code.")


class DomainOperationDoc(SpecIRNodeDoc):
    """A capability of the domain, independent of how it is invoked (UI, CLI, job, agent)."""

    __semantics__ = {"type": ["specir", "node", "domain_operation"], "layer": ["domain"]}
    __template__ = _template([("symbol", "optrev")])

    symbol: str | None = Field(default=None, description="The operation's qualified name in the code.")


class CapabilityDoc(DomainOperationDoc):
    """A capability of the domain that someone needs the system to have, and who for.

    It is a `DomainOperationDoc` (a capability of the domain, however it is invoked) that also
    names its `audience`. Whether it is met is not a field: its acceptance test is a
    `MaterializationContractDoc` (target_identity `<path>::<test name>`) linked by `accepted_by`,
    and `rule-specir-capability-has-an-acceptance-test` reports the capability with none. An
    operation an extractor reads out of code is a `DomainOperationDoc`, not a capability."""

    __semantics__ = {"type": ["specir", "node", "domain_operation", "capability"], "layer": ["domain"]}
    __template__ = _template([("symbol", "optrev"), ("audience", "rev,list")])

    audience: list[str] = Field(description="Who the capability is for, at least one: 'agente', 'JP', 'graph_ui'.")

    @field_validator("audience")
    @classmethod
    def _audience(cls, value: list[str]) -> list[str]:
        if not value or any(not a.strip() for a in value):
            raise ValueError("a capability says who it is for: audience has at least one non-blank entry")
        return value


class PolicyDoc(SpecIRNodeDoc):
    """A rule of the domain an operation is governed by: who may do it and when."""

    __semantics__ = {"type": ["specir", "node", "policy"], "layer": ["domain"]}
    __template__ = _template([("statement", "optrev")])

    statement: str | None = Field(default=None, description="The policy as one sentence.")


class StateDoc(SpecIRNodeDoc):
    """A state a domain entity can be in."""

    __semantics__ = {"type": ["specir", "node", "state"], "layer": ["domain"]}
    __references__ = ["entity"]
    __template__ = _template([("entity", "rev")])

    entity: str = Field(description="Export id of the DomainEntityDoc this is a state of (DomainEntityDoc:<name>).")


class DomainEntityDoc(SpecIRNodeDoc):
    """A thing of the domain, with one identity however many views or layers show it."""

    __semantics__ = {"type": ["specir", "node", "domain_entity"], "layer": ["domain"]}
    __template__ = _template([("symbol", "optrev")])

    symbol: str | None = Field(default=None, description="The class that models it in the code (e.g. a Django model).")


class TableDoc(SpecIRNodeDoc):
    """A table of the database, with the columns the model knows of."""

    __semantics__ = {"type": ["specir", "node", "table"], "layer": ["data"]}
    __template__ = _template([("schema_name", "optrev"), ("columns", "rev,list")])

    schema_name: str | None = Field(default=None, description="The database schema the table lives in.")
    columns: list[str] = Field(default_factory=list, description="The columns the model knows of.")


#: The domain types, registered in a store by `specir.install`. The base is not.
DOMAIN_MODELS: tuple[type[SpecIRNodeDoc], ...] = (
    InterfaceControlDoc,
    InterfaceActionDoc,
    InterfaceFieldDoc,
    ApiOperationDoc,
    ApiFieldDoc,
    HandlerDoc,
    DomainOperationDoc,
    CapabilityDoc,
    PolicyDoc,
    StateDoc,
    DomainEntityDoc,
    TableDoc,
)
