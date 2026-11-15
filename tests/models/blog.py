"""The test store of the example blog: a new SLDB store with specIR installed, populated with the
chain of tests/fixtures/blog_chain.yaml through the MCP write tools.

Reusable by later tasks: `new_blog_project` makes the store, `populate` writes the chain with
any MCP session at write level 1 or more, and the `blog_root`/`blog` fixtures of conftest.py
serve it. Nothing is written to files directly: the store is made with SLDB's CLI, specIR is
installed with its own command, and every document comes from `apply_changes`."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

from conftest import REPO, sldb

FIXTURE = REPO / "tests" / "fixtures" / "blog_chain.yaml"


def blog_chain() -> dict[str, Any]:
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))


def changes_of(batch: str) -> list[dict[str, Any]]:
    """The changes of one batch of the fixture, by name."""
    return next(b["changes"] for b in blog_chain()["batches"] if b["name"] == batch)


def install(root: Path) -> subprocess.CompletedProcess:
    """`python -m specir.install --store <root>/.sldb`; fail the test with its output on error."""
    done = subprocess.run([sys.executable, "-m", "specir.install", "--store", str(root / ".sldb")], cwd=root, capture_output=True, text=True)
    if done.returncode != 0:
        pytest.fail(f"specir.install failed ({done.returncode}):\n{done.stdout}\n{done.stderr}")
    return done


def new_blog_project(root: Path) -> Path:
    """A new project at `root` with an SLDB store (`sldb stores init`) and specIR installed in it."""
    root.mkdir(parents=True)
    sldb("stores", "init", "--path", str(root), cwd=root)
    install(root)
    return root


def apply(session: Any, changes: list[dict[str, Any]]) -> dict[str, Any]:
    """Propose `changes` and apply the proposal as it came back; the answer of apply_changes."""
    proposal = session.call("propose_changes", changes=changes)["proposal"]
    return session.call("apply_changes", proposal=proposal)


def populate(session: Any) -> list[dict[str, Any]]:
    """Write the blog chain, batch by batch; the answer of each apply."""
    answers = []
    for batch in blog_chain()["batches"]:
        answer = apply(session, batch["changes"])
        assert answer["applied"] is True, (batch["name"], answer)
        answers.append(answer)
    return answers
