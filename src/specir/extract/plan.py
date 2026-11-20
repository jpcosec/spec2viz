"""What the rules of specIR plan to write: nodes and edges, each with the rule that made it and
the facts it stands on (the facts are anchored when the plan is written, `write.py`)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any

#: Where a planned document lands in the store's project, relative to its root.
DOCUMENT_DIR = "specir/extracted"
ANCHOR_DIR = "specir/anchors"

#: Name prefix by model: document names are unique in a store whatever their model.
PREFIXES = {
    "ApiOperationDoc": "api", "HandlerDoc": "handler", "DomainOperationDoc": "op", "PolicyDoc": "policy",
    "StateDoc": "state", "InterfaceControlDoc": "control", "InterfaceActionDoc": "action", "DomainEntityDoc": "entity", "TableDoc": "table", "RelationDoc": "edge",
}


def slug(text: str) -> str:
    """Lowercase letters and digits separated by single hyphens."""
    out, last = [], "-"
    for char in text.lower():
        keep = char if char.isascii() and char.isalnum() else "-"
        if keep != "-" or last != "-":
            out.append(keep)
        last = keep
    return "".join(out).strip("-")


@dataclass
class Planned:
    """One node or edge to write: `model` and `name` make its export id; `fields` are the model's
    own fields (nodes) or the RelationDoc's (edges); `facts` are the facts the rule read."""

    model: str
    name: str
    fields: dict[str, Any]
    origen: str
    rule: str
    facts: list[dict[str, Any]] = field(default_factory=list)

    @property
    def export_id(self) -> str:
        return f"{self.model}:{self.name}"

    @property
    def path(self) -> str:
        return f"{DOCUMENT_DIR}/{self.name}.md"

    def payload(self) -> dict[str, Any]:
        """The document's payload: the provenance decided in IR05 (never inferido, never declarado,
        always sin_verificar, evidencia empty) plus the model's own fields."""
        if self.model == "RelationDoc":
            attributes = {"origen": self.origen, "verificacion": "sin_verificar", "verificado_por": "", "evidencia": "", "anchors": anchor_refs(self.facts)}
            return {**self.fields, "attributes": attributes}
        return {"origen": self.origen, "verificacion": "sin_verificar", "verificado_por": "", "evidencia": "", **self.fields}


def node_name(model: str, text: str) -> str:
    return f"{PREFIXES[model]}-{slug(text)}"


def edge_name(source: Planned, relation: str, target: Planned) -> str:
    return f"{PREFIXES['RelationDoc']}-{slug(source.name)}--{relation}--{slug(target.name)}"


def where(fact: dict[str, Any]) -> str:
    """`path:line symbol [anchor]` of a fact, as the descriptions name it: the anchor is the name of
    the CodeAnchorDoc that holds the fact's fingerprints and source_hash."""
    return f"{fact['path']}:{fact['span']['start_line']} {symbol_of(fact)} [{anchor_name(ref_of(fact))}]"


def anchor_name(ref: str) -> str:
    return "anchor-" + hashlib.sha256(ref.encode()).hexdigest()[:16]


def symbol_of(fact: dict[str, Any]) -> str:
    return fact["qualified_name"]


def ref_of(fact: dict[str, Any]) -> str:
    """The `code:<path>::<name>` reference of a fact (code-anchoring.md §1): its id without the
    module's, which keeps the `~n` suffix of a repeated name."""
    module = fact["attrs"]["module"]
    name = "" if fact["id"] == module else fact["id"].removeprefix(module + ".")
    return f"code:{fact['path']}::{name}"


def anchor_refs(facts: list[dict[str, Any]]) -> list[str]:
    return sorted({ref_of(f) for f in facts})


def sentence(rule: str, facts: list[dict[str, Any]], derived: bool) -> str:
    """One sentence that names the rule and the facts it stands on (preflight-5, point 3)."""
    named = "; ".join(dict.fromkeys(where(f) for f in facts))
    how = "Derivado" if derived else "Observado"
    return f"{how} por la regla {rule} sobre los facts de código {named}."
