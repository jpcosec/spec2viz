"""Stable addresses: the node ids SLDB gives documents, models and relation types.

The address of a document is `sldb://document/<export_id>` (`sldb.api.doc_node_id`), the one
the edge index and the semantic export use; `alias:Model:name` names a document of a linked
store. Nothing is minted here: every address comes from `sldb.api`."""

from __future__ import annotations

from typing import Any

import sldb.api as api

NODE_PREFIX = "sldb://"


def document_address(export_id: str) -> str:
    """The stable address of a document named by its export id (`[alias:]Model:name`)."""
    return api.doc_node_id(export_id)


def model_address(model: str) -> str:
    """The stable address of a registered model."""
    return api.model_node_id(model)


def relation_type_address(name: str) -> str:
    """The stable address of a relation type."""
    return api.relation_type_node_id(name)


def node_or_document(ref: str) -> str:
    """A node id as given (`sldb://...`), or the address of a document export id."""
    return ref if ref.startswith(NODE_PREFIX) else document_address(ref)


def addressed_row(row: dict[str, Any]) -> dict[str, Any]:
    """A `select_documents` row with its stable address."""
    return {"address": document_address(row["export_id"]), **row}


def row_alias(row: dict[str, Any]) -> str | None:
    """The linked-store alias of a `select_documents` row, or None for a local document."""
    local = f"{row['model']}:{row['name']}"
    export_id = row["export_id"]
    return None if export_id == local else export_id[: -len(local) - 1]
