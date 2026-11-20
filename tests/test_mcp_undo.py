"""IR04b: the `undo_changes` of `sldb mcp` over a mounted copy of this repo's store, with specIR's
extension mounted, driven by the real MCP client (tests/conftest.py `served`). Nothing is mocked and
specIR implements no undo: the tool, the stack of inverse batches and the guards are sldb's."""

from __future__ import annotations

import hashlib
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterator

import pytest

from conftest import REPO, copy_digest, mount_copy, served, tree_digest

ACTOR = "agent:specir-ir04b"
EDGE = {"origen": "declarado", "verificacion": "sin_verificar"}
OP = "undo-seed-op"


def node(model: str, description: str, **extra: Any) -> dict[str, Any]:
    return {"title": description, "origen": "declarado", "description": description, "symbol": None, "desconocidos": {"symbol": "no code yet"}, **extra}


def seed() -> list[dict[str, Any]]:
    """What the copy holds before the cases: one domain operation, written through the server."""
    return [{"action": "create", "model": "DomainOperationDoc", "name": OP, "path": "undo/domain/seed-op.md", "payload": node("DomainOperationDoc", "A seed operation.")}]


def content_batch(tag: str) -> list[dict[str, Any]]:
    """Level 1: create a DomainEntityDoc, edit the existing DomainOperationDoc, assert `writes` between them."""
    entity = f"undo-entity-{tag}"
    return [
        {"action": "create", "model": "DomainEntityDoc", "name": entity, "path": f"undo/domain/{entity}.md", "payload": node("DomainEntityDoc", f"Entity {tag}.")},
        {"action": "update", "model": "DomainOperationDoc", "name": OP, "fields": {"description": f"Edited by the batch {tag}."}},
        {"action": "assert_edge", "name": f"undo-op-writes-{tag}", "path": f"undo/edges/op-writes-{tag}.md", "source": f"DomainOperationDoc:{OP}", "target": f"DomainEntityDoc:{entity}", "relation_type": "writes", "attributes": EDGE},
    ]


def rule_change(tag: str) -> dict[str, Any]:
    return {"action": "create", "model": "RuleDoc", "name": f"rule-undo-{tag}", "path": f"undo/rules/rule-undo-{tag}.md",
            "payload": {"title": f"Undo rule {tag}", "subject": "model <= DomainEntityDoc", "where": "", "condition": "any(rel:writes: model <= DomainOperationDoc)", "severity": "alert", "moment": "on_check", "message": "No operation writes this entity."}}


def propose_apply(session: Any, changes: list[dict[str, Any]]) -> dict[str, Any]:
    proposal = session.call("propose_changes", changes=changes)["proposal"]
    return session.call("apply_changes", proposal=proposal)


def install(root: Path) -> None:
    """`python -m specir.install --store <root>/.sldb`, specIR's own command."""
    done = subprocess.run([sys.executable, "-m", "specir.install", "--store", str(root / ".sldb")], cwd=root, capture_output=True, text=True)
    assert done.returncode == 0, done.stdout + done.stderr


def cli(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run([str(Path(sys.executable).with_name("sldb")), *args, "--store", ".sldb"], cwd=root, capture_output=True, text=True)


def checks(root: Path) -> dict[str, tuple[int, str]]:
    """`sldb rules check` and `sldb edges check` over the copy: (rc, output)."""
    return {name: (done.returncode, done.stdout + done.stderr) for name, done in (("rules", cli(root, "rules", "check")), ("edges", cli(root, "edges", "check")))}


@pytest.fixture(scope="module")
def copy_root(tmp_path_factory, spec_store, federated) -> Path:
    """A writable mounted copy with specIR installed and the seed operation written by a level-1 session."""
    root = mount_copy(tmp_path_factory, "specir-undo", spec_store, federated)
    install(root)
    with served(root, "--level", "1", "--actor", ACTOR) as session:
        assert propose_apply(session, seed())["applied"] is True
    return root


class Digest(dict):
    """The sha256 of every file of the copy and the linked stores; comparing two of them that
    differ prints, for each file of the copy that changed, what changed (a unified diff)."""

    files: dict[str, bytes]

    def __eq__(self, other: object) -> bool:
        same = dict.__eq__(self, other)
        if not same and isinstance(other, Digest):
            import difflib

            for path in sorted(p for p in set(self) | set(other) if self.get(p) != other.get(p)):
                old, new = other.files.get(path, b""), self.files.get(path, b"")
                print("CHANGED", path)
                print("".join(difflib.unified_diff(old.decode(errors="replace").splitlines(True), new.decode(errors="replace").splitlines(True), "before", "after", n=1))[:3000])
        return same

    __hash__ = None  # type: ignore[assignment]


@pytest.fixture
def digest(copy_root, spec_store, federated):
    def take() -> Digest:
        taken = Digest(copy_digest(copy_root, spec_store, federated))
        taken.files = {str(p): p.read_bytes() for p in sorted(copy_root.rglob("*")) if p.is_file() and ".sldb_cache" not in p.parts and p.suffix in (".yaml", ".md")}
        return taken

    return take


@pytest.fixture
def content(copy_root):
    """What the store holds as documents: the sha256 of every Markdown document of the copy."""
    def take() -> Digest:
        taken = Digest(md_digest(copy_root))
        taken.files = {str(p): p.read_bytes() for p in sorted(copy_root.rglob("*.md")) if ".sldb_cache" not in p.parts}
        return taken

    return take


STAMP = re.compile(r"^(\s+(?:at|via): ).*$", re.MULTILINE)


def md_digest(root: Path) -> dict[str, str]:
    """sha256 of every Markdown document of the copy, with the provenance stamp (`sldb.at` and
    `sldb.via`) left out: an undo restores the content of a document but sldb stamps it with the time and the way of the undo
    (finding for sldb, see test_the_store_files_are_byte_identical_after_the_undo)."""
    digest = {}
    for path in sorted(p for n in (".sldb", "sldb", "desk", "undo") if (root / n).exists() for p in (root / n).rglob("*.md")):
        if path.is_file() and ".sldb_cache" not in path.parts:
            digest[str(path)] = hashlib.sha256(STAMP.sub(r"\1<stamp>", path.read_text(encoding="utf-8")).encode()).hexdigest()
    return digest


def test_level_1_batch_of_create_edit_and_edge_is_undone_to_the_same_documents(copy_root, digest, content) -> None:
    before, mds, checked = digest(), content(), checks(copy_root)
    with served(copy_root, "--level", "1", "--actor", ACTOR) as session:
        assert "undo_changes" in {t.name for t in session.list_tools()}
        applied = propose_apply(session, content_batch("a"))
        assert applied["applied"] is True and applied["edge_findings"] == [], applied
        assert digest() != before
        undone = session.call("undo_changes", steps=1)
        print("UNDO", undone)
        assert undone["applied"] is True and undone["undone"] == 1 and undone["remaining"] == 0, undone
    assert content() == mds
    after = checks(copy_root)
    print("CHECKS before", checked, "after", after)
    assert after == checked and all(rc == 0 for rc, _ in after.values()), after


@pytest.mark.xfail(strict=True, reason="finding for sldb: undo_changes restores the content but re-stamps `sldb.at` and `sldb.via` of the edited document (and the hashes derived from it in .sldb/)")
def test_the_store_files_are_byte_identical_after_the_undo(copy_root, digest) -> None:
    """Validation 1 asks the sha256 of the .md and of the store to match. They match but for the
    provenance stamp (`sldb.at`, `sldb.via`) of the document the batch edited, and the hashes derived from it.
    Strict xfail: when sldb stops re-stamping, this passes and the xfail must go."""
    before = digest()
    with served(copy_root, "--level", "1", "--actor", ACTOR) as session:
        assert propose_apply(session, content_batch("h"))["applied"] is True
        assert session.call("undo_changes", steps=1)["applied"] is True
    assert digest() == before


def foreign_edit(root: Path, description: str) -> None:
    """Someone else writes over the operation, outside the MCP session: `sldb.api.apply_batch`."""
    from sldb import api

    payload = api.serialize_document(api.runtime_document(root / ".sldb", None, f"DomainOperationDoc/{OP}"))["payload"]
    api.apply_batch(root / ".sldb", [{"action": "update", "id": OP, "payload": {**payload, "description": description}}])


def test_a_stale_batch_is_refused_without_writing_and_undone_once_the_foreign_change_is_reverted(copy_root, digest, content) -> None:
    before, mds = digest(), content()
    with served(copy_root, "--level", "1", "--actor", ACTOR) as session:
        assert propose_apply(session, content_batch("b"))["applied"] is True
        foreign_edit(copy_root, "Edited by someone else.")
        foreign_state = digest()
        refused = session.call("undo_changes", steps=1)
        print("STALE", refused)
        assert refused["applied"] is False and refused["rejected"] == "stale" and refused["written"] is False, refused
        assert OP in str(refused["document"]), refused
        assert digest() == foreign_state, "a stale undo wrote something"
        # The foreign change is reverted by another batch, from another session (its own stack),
        # that returns the document to the content it had after the batch.
        with served(copy_root, "--level", "1", "--actor", ACTOR) as other:
            assert propose_apply(other, [{"action": "update", "model": "DomainOperationDoc", "name": OP, "fields": {"description": "Edited by the batch b."}}])["applied"] is True
        # The batch stayed on the stack: it is undone now.
        undone = session.call("undo_changes", steps=1)
        print("UNDO AFTER REVERT", undone)
        assert undone["applied"] is True and undone["undone"] == 1, undone
    assert content() == mds


def test_two_batches_are_undone_newest_first_with_steps_and_an_empty_stack_refuses(copy_root, digest, content) -> None:
    before = content()
    with served(copy_root, "--level", "1", "--actor", ACTOR) as session:
        first = propose_apply(session, content_batch("d1"))
        second = propose_apply(session, [{"action": "update", "model": "DomainEntityDoc", "name": "undo-entity-d1", "fields": {"description": "Edited again."}}])
        assert first["applied"] and second["applied"]
        undone = session.call("undo_changes", steps=2)
        print("UNDO 2", undone)
        assert undone["applied"] is True and undone["undone"] == 2 and undone["remaining"] == 0, undone
        assert content() == before
        nothing = session.call("undo_changes", steps=1)
        print("EMPTY", nothing)
        assert nothing["applied"] is False and nothing["rejected"] == "nothing_to_undo" and nothing["written"] is False, nothing
    assert content() == before


def test_level_0_serves_neither_write_tools_nor_undo_changes(copy_root, digest) -> None:
    before = digest()
    with served(copy_root) as session:
        names = {t.name for t in session.list_tools()}
        assert not names & {"propose_changes", "apply_changes", "undo_changes"}, names
        answer = session.portal.call(lambda: session.client.call_tool("undo_changes", {"steps": 1}))
        print("LEVEL 0", answer.is_error, answer.structured_content)
        assert answer.structured_content["signal"] == "unknown_tool", answer
    assert digest() == before


def test_level_1_refuses_a_batch_of_rules_so_none_is_on_its_stack_and_a_level_2_batch_is_not_undone_from_it(copy_root, digest, content) -> None:
    before = content()
    with served(copy_root, "--level", "1", "--actor", ACTOR) as session:
        refusal = session.error_of("propose_changes", changes=[*content_batch("e"), rule_change("e")])
        print("LEVEL 1 RULEDOC", refusal)
        assert "level" in refusal
        nothing = session.call("undo_changes", steps=1)
        assert nothing["applied"] is False and nothing["rejected"] == "nothing_to_undo", nothing
    assert content() == before
    with served(copy_root, "--level", "2", "--actor", ACTOR) as rules:
        assert propose_apply(rules, [*content_batch("f"), rule_change("f")])["applied"] is True
        applied_state = content()
        with served(copy_root, "--level", "1", "--actor", ACTOR) as level_1:
            nothing = level_1.call("undo_changes", steps=1)
            print("LEVEL 1 OVER A LEVEL 2 BATCH", nothing)
            assert nothing["applied"] is False and nothing["rejected"] == "nothing_to_undo", nothing
        assert content() == applied_state
        undone = rules.call("undo_changes", steps=1)
        print("LEVEL 2 UNDO", undone)
        assert undone["applied"] is True and undone["undone"] == 1, undone
    assert content() == before


def test_the_store_after_an_undo_passes_the_checks_and_the_registered_domain_validators(copy_root, digest, content) -> None:
    """sldb applies the inverse batch with `apply_batch` directly, so the batch validators specIR
    registered (`add_batch_validator`) do not run on it. After the undo the store must pass sldb's
    rules and edges checks, and the registered validators, run over the documents of the batch as
    they are stored, must find no error."""
    from sldb import api
    from sldb.mcp.changes import BatchChange
    from sldb.mcp.context import ServerContext
    from sldb.mcp.server import build_server

    import specir.mcp_extension as extension

    before, checked = content(), checks(copy_root)
    context = ServerContext(copy_root / ".sldb", 2, ACTOR)
    extension.register(build_server(copy_root / ".sldb", 2, ACTOR), context)
    assert len(context.batch_validators) == 1
    stored = lambda name: api.serialize_document(api.runtime_document(copy_root / ".sldb", None, f"DomainOperationDoc/{name}"))["payload"]
    with served(copy_root, "--level", "2", "--actor", ACTOR) as session:
        assert propose_apply(session, [*content_batch("g"), rule_change("g")])["applied"] is True
        assert session.call("undo_changes", steps=1)["applied"] is True
    after = checks(copy_root)
    print("RULES/EDGES", after)
    assert after == checked and after["rules"][0] == 0 and after["edges"][0] == 0
    assert content() == before
    documents = [BatchChange(id=OP, action="update", model="DomainOperationDoc", payload=stored(OP))]
    findings = [f for validator in context.batch_validators for f in validator(documents, context)]
    print("VALIDATORS over the documents of the batch after the undo", findings)
    assert [f for f in findings if f["level"] == "error"] == [], findings


def test_specir_defines_no_undo() -> None:
    """(f): an own implementation is a `def`, a registered tool or a structure keeping batches; docstring
    mentions and calls to sldb's tool do not count. Today the only hit is the vendored, minified bpmn-js."""
    done = subprocess.run(["grep", "-rnE", "undo_changes|inverse", "src/specir"], cwd=REPO, capture_output=True, text=True)
    print("GREP", [line[:120] for line in done.stdout.splitlines()])
    own_code = [line for line in done.stdout.splitlines() if "/vendor/" not in line.split(":", 1)[0]]
    assert own_code == [], own_code
    assert all(line.startswith("src/specir/visual/templates/vendor/bpmn-js/") for line in done.stdout.splitlines())
