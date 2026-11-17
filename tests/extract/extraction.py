"""Helpers of the extractor tests: a project made of a copy of tests/fixtures/blog_app with an SLDB
store and specIR installed, the extraction of it, and what is read back from the store."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

import sldb.api as api
from conftest import REPO, sldb

from specir.install import package_pythonpath

FIXTURE = REPO / "tests" / "fixtures" / "blog_app"
BACKEND_AND_DATA = ("ApiOperationDoc", "HandlerDoc", "DomainOperationDoc", "PolicyDoc", "StateDoc", "DomainEntityDoc", "TableDoc")


def new_project(base: Path, name: str = "blog_app") -> Path:
    """`<base>/<name>`: a copy of the fixture with a new store, specIR installed in it."""
    root = base / name
    shutil.copytree(FIXTURE, root, ignore=shutil.ignore_patterns("__pycache__"))
    sldb("stores", "init", "--path", str(root), cwd=root)
    done = subprocess.run([sys.executable, "-m", "specir.install", "--store", str(root / ".sldb")], cwd=root, capture_output=True, text=True)
    if done.returncode != 0:
        pytest.fail(f"specir.install failed ({done.returncode}):\n{done.stdout}\n{done.stderr}")
    return root


def documents(root: Path) -> dict[str, Any]:
    """Every tracked document of the store by export id (`Model:name`)."""
    return {f"{d.model_name}:{d.name}": d for d in api.load_runtime_documents(root / ".sldb", package_pythonpath())}


def extracted(root: Path) -> dict[str, Any]:
    """The nodes and relations the extractor wrote (not the anchors nor the installed seeds)."""
    models = (*BACKEND_AND_DATA, "RelationDoc")
    return {k: d for k, d in documents(root).items() if d.model_name in models}


def triples(root: Path) -> set[tuple[str, str, str]]:
    """(source model, relation type, target model) of every extracted edge."""
    edges = [d for d in extracted(root).values() if d.model_name == "RelationDoc"]
    return {(d.payload["source_id"].split(":")[0], d.payload["relation_type"], d.payload["target_id"].split(":")[0]) for d in edges}


def rules_findings(root: Path) -> list[dict[str, Any]]:
    """`sldb rules check` over the store, whatever its exit code (it is 1 when a rule fails)."""
    command = [str(Path(sys.executable).with_name("sldb")), "rules", "check", "--store", ".sldb", "--format", "json"]
    done = subprocess.run(command, cwd=root, capture_output=True, text=True)
    assert done.stdout.strip(), done.stderr
    answer = json.loads(done.stdout)
    return answer["findings"] if isinstance(answer, dict) else answer
