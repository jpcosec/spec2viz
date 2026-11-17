"""Writing a plan to a store: every anchor is checked before anything is written, anchors are
written with `sldb.api.anchors.write_anchor`, documents and relations by `apply_batch`."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import sldb.api as api
from sldb.api.anchors import check_anchors, record_anchor, write_anchor

from specir.extract.plan import ANCHOR_DIR, Planned, anchor_name, anchor_refs, ref_of

ANCHOR_MODEL = "CodeAnchorDoc"
ANCHOR_REF = "sldb.models.code_anchor_doc:CodeAnchorDoc"
#: What a verifier changed by hand and a re-extraction therefore never writes over (IR05 D4-C).
UNVERIFIED = "sin_verificar"
ANCHOR_NAME = re.compile(r"\[(anchor-[0-9a-f]{16})\]")


@dataclass
class ExtractionReport:
    """What one extraction did, as `specir.extract.extract` returns it: the export ids of the
    documents and relations created, left as they were, changed (an anchor of theirs is not
    `intact`, or their content differs), and what the facts did not let the rules derive."""

    created: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    not_derived: list[str] = field(default_factory=list)


def claim_of(fact: dict[str, Any]) -> str:
    span = fact["span"]
    return f"{ref_of(fact)}: {fact['kind']} en {fact['path']} líneas {span['start_line']}-{span['end_line']}, source_hash {fact['source_hash']}"


def checked_blocks(root: Path, facts: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """The anchor block of every fact, each checked against the fact it anchors: the same fingerprints
    and the same source_hash. `ValueError` naming the ref of the first that does not match."""
    blocks = {}
    for ref, fact in sorted(facts.items()):
        try:
            block = record_anchor(root, ref)
        except ValueError as error:
            raise ValueError(f"{ref}: {error}") from error
        if block["seen"] != fact["fingerprints"]:
            raise ValueError(f"{ref}: the anchor does not match the fact (fingerprints differ)")
        if "sha256:" + hashlib.sha256((root / fact["path"]).read_bytes()).hexdigest() != fact["source_hash"]:
            raise ValueError(f"{ref}: the anchor does not match the fact (source_hash differs)")
        blocks[ref] = block
    return blocks


def _same(existing: dict[str, Any], wanted: dict[str, Any]) -> bool:
    def blank(value: Any) -> Any:
        return None if value in ("", [], {}) else value
    return all(blank(existing.get(k)) == blank(v) for k, v in wanted.items())


def write_plan(store: Path, root: Path, pythonpath: str, nodes: list[Planned], edges: list[Planned], not_derived: list[str]) -> ExtractionReport:
    facts = {ref_of(f): f for p in (*nodes, *edges) for f in p.facts}
    blocks = checked_blocks(root, facts)
    if not api.is_model_registered(store, ANCHOR_MODEL):
        api.add_model(store, ANCHOR_REF, pythonpath=pythonpath)
    states = {r.ref: r.state.value for r in check_anchors(store, pythonpath)}
    held = {d.name: d for d in api.load_runtime_documents(store, pythonpath) if d.model_name == ANCHOR_MODEL}
    for ref, fact in facts.items():
        name = anchor_name(ref)
        if name in held and states.get(ref) == "intact" and held[name].payload.get("claim") == claim_of(fact):
            continue
        write_anchor(store, pythonpath, root / ANCHOR_DIR / f"{name}.md", blocks[ref], claim_of(fact), name)
    current = {(d.model_name, d.name): d for d in api.load_runtime_documents(store, pythonpath) if d.model_name != ANCHOR_MODEL}
    report, changes = ExtractionReport(not_derived=list(not_derived)), []
    for planned in (*nodes, *edges):
        moved = any(states.get(ref, "intact") != "intact" for ref in anchor_refs(planned.facts))
        old = current.get((planned.model, planned.name))
        wanted = planned.payload()
        if old is None:
            changes.append({"action": "create", "id": planned.name, "model": planned.model, "path": planned.path, "payload": wanted})
            report.created.append(planned.export_id)
        elif (old.payload.get("verificacion") or (old.payload.get("attributes") or {}).get("verificacion")) != UNVERIFIED:
            (report.changed if moved else report.unchanged).append(planned.export_id)
        elif moved or not _same(old.payload, wanted) or not _same(old.payload.get("attributes") or {}, wanted.get("attributes") or {}):
            changes.append({"action": "update", "id": planned.name, "payload": wanted})
            report.changed.append(planned.export_id)
        else:
            report.unchanged.append(planned.export_id)
    planned_ids = {p.export_id for p in (*nodes, *edges)}
    anchored = {d.name: d.payload.get("ref") for d in held.values()}
    for key, old in sorted(current.items()):
        export_id = f"{key[0]}:{key[1]}"
        fields = old.payload.get("attributes") or old.payload if key[0] == "RelationDoc" else old.payload
        if export_id in planned_ids or fields.get("origen") not in ("observado", "derivado"):
            continue
        text = old.payload.get("description") or old.payload.get("notes") or ""
        refs = [anchored[n] for n in ANCHOR_NAME.findall(text) if n in anchored]
        # Written by the extractor and anchored to code that moved, and the new plan no longer produces it:
        # flagged, never deleted nor modified.
        if refs and any(states.get(ref, "intact") != "intact" for ref in refs):
            report.changed.append(export_id)
    if changes:
        api.apply_batch(store, changes, pythonpath)
    return report
