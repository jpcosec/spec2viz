"""The typed changes an agent proposes, and the proposal that carries them to `apply`.

A change is a typed argument, never text the server interprets: one of the actions below,
with the model and name of the document it touches. A proposal is the batch in the form of
`sldb.api.apply_batch` (IR02 D1-A: an ephemeral batch, nothing kept between steps) with the
`expected_source_hash` guard the server filled in for every document it touches (D2-A), and
a seal over that batch so `apply` runs exactly what was proposed.

The seal is an HMAC with a secret of the server process: it only proves the batch came from
`propose_changes` of this process unchanged. It is not a store precondition; the guards are,
and `apply_batch` checks them."""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
from typing import Annotated, Any, Literal, Union

from pydantic import BaseModel, ConfigDict, Field

from specir.mcp.mutability import model_level

#: The model of an authored edge (sldb.models.relation_doc).
EDGE_MODEL = "RelationDoc"


class _Change(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CreateDocument(_Change):
    """Create a document of a registered model."""

    action: Literal["create"]
    model: str = Field(description="A model the store registers.")
    name: str = Field(description="The new document's name, unique in the store.")
    payload: dict[str, Any] = Field(description="Every field of the document, as the model declares it.")
    path: str | None = Field(default=None, description="Markdown path relative to the project root; omitted, the model's default directory.")


class UpdateDocument(_Change):
    """Set fields of a tracked document; the rest of its payload stays as it is."""

    action: Literal["update"]
    model: str
    name: str
    fields: dict[str, Any] = Field(description="Dotted field path -> new value (sldb.api.deep_set).")


class DeleteDocument(_Change):
    """Delete a tracked document and its file."""

    action: Literal["delete"]
    model: str
    name: str


class AssertEdge(_Change):
    """Assert an authored edge: a `RelationDoc` source -[relation_type]-> target."""

    action: Literal["assert_edge"]
    name: str = Field(description="The RelationDoc's name, unique in the store.")
    source: str = Field(description="Export id of the source document (`Model:name`, `alias:Model:name` for a linked store).")
    target: str = Field(description="Export id of the target document.")
    relation_type: str = Field(description="The name of a tracked RelationTypeDoc.")
    title: str | None = Field(default=None, description="The RelationDoc's title; omitted, `<source> <relation_type> <target>`.")
    condition: str = Field(default="", description="A predicate for this edge only; empty inherits the type's condition.")
    attributes: dict[str, Any] = Field(default_factory=dict)
    notes: str = Field(default="")
    path: str | None = Field(default=None, description="Markdown path relative to the project root; omitted, RelationDoc's default directory.")


class RetractEdge(_Change):
    """Retract an authored edge: delete its `RelationDoc`."""

    action: Literal["retract_edge"]
    name: str = Field(description="The RelationDoc's name.")


Change = Annotated[Union[CreateDocument, UpdateDocument, DeleteDocument, AssertEdge, RetractEdge], Field(discriminator="action")]


def model_of(change: CreateDocument | UpdateDocument | DeleteDocument | AssertEdge | RetractEdge) -> str:
    """The model of the document a change touches."""
    return getattr(change, "model", EDGE_MODEL)


def level_of(changes: list[Any]) -> int:
    """The write level a list of changes needs: the highest of its documents' models."""
    return max((model_level(model_of(c)) for c in changes), default=0)


def edge_payload(change: AssertEdge) -> dict[str, Any]:
    """The `RelationDoc` payload of an asserted edge."""
    return {
        "title": change.title or f"{change.source} {change.relation_type} {change.target}",
        "source_id": change.source,
        "target_id": change.target,
        "relation_type": change.relation_type,
        "condition": change.condition,
        "attributes": change.attributes,
        "notes": change.notes,
    }


class BatchChange(BaseModel):
    """One change in the form `sldb.api.apply_batch` takes, plus the model it touches."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="The document name.")
    action: Literal["create", "update", "delete"]
    model: str
    payload: dict[str, Any] | None = None
    path: str | None = None
    expected_source_hash: str | None = Field(default=None, description="The document's source hash when the change was proposed (filled by the server).")

    def batch_form(self) -> dict[str, Any]:
        """The dict `apply_batch` reads (it names the model only on create)."""
        form = {"id": self.id, "action": self.action}
        if self.action == "create":
            form["model"] = self.model
        if self.payload is not None:
            form["payload"] = self.payload
        if self.path is not None:
            form["path"] = self.path
        if self.expected_source_hash is not None:
            form["expected_source_hash"] = self.expected_source_hash
        return form


class Proposal(BaseModel):
    """What `propose_changes` returns and `apply_changes` takes back, unchanged."""

    model_config = ConfigDict(extra="forbid")

    changes: list[BatchChange]
    level: int = Field(description="The write level the batch needs.")
    store_hash: str = Field(description="The store's fingerprint when proposed (informational: no SLDB write accepts it as a precondition yet).")
    seal: str = Field(description="The server's seal over the batch; any edit makes `apply_changes` refuse it.")


class Sealer:
    """Seals and checks proposals with a secret of this server process."""

    def __init__(self) -> None:
        self._key = secrets.token_bytes(32)

    def seal(self, changes: list[BatchChange], level: int, store_hash: str) -> str:
        body = json.dumps({"changes": [c.model_dump(mode="json") for c in changes], "level": level, "store_hash": store_hash}, sort_keys=True, separators=(",", ":"))
        return hmac.new(self._key, body.encode("utf-8"), hashlib.sha256).hexdigest()

    def check(self, proposal: Proposal) -> None:
        if not hmac.compare_digest(proposal.seal, self.seal(proposal.changes, proposal.level, proposal.store_hash)):
            raise ValueError("the proposal is not the one propose_changes returned (edited, or proposed by another server process); propose it again")
