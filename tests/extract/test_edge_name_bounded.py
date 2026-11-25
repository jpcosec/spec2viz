"""edge_name never yields a name over 255 bytes (file name included): short names are unchanged,
long ones are cut to a readable prefix plus a sha256 digest."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

from conftest import REPO
from extraction import new_project

from specir.extract import extract, extract_frontend
from specir.extract.plan import MAX_NAME_BYTES, Planned, bounded_name, edge_name

FRONTEND = REPO / "tests" / "fixtures" / "blog_frontend"


def node(name: str) -> Planned:
    return Planned("DomainEntityDoc", name, {}, "extraido", "rule")


def edge(source: str, target: str) -> Planned:
    return Planned("RelationDoc", edge_name(node(source), "invokes", node(target)), {}, "extraido", "rule")


def test_a_short_name_is_unchanged() -> None:
    assert edge_name(node("entity-a"), "invokes", node("entity-b")) == "edge-entity-a--invokes--entity-b"


def test_a_deep_source_gives_a_bounded_name_ending_in_the_hash() -> None:
    name = edge_name(node("control-" + "/".join(["deep"] * 80)), "invokes", node("entity-b"))
    assert len(name.encode()) <= MAX_NAME_BYTES
    assert re.search(r"-[0-9a-f]{12}$", name)
    assert name == edge_name(node("control-" + "/".join(["deep"] * 80)), "invokes", node("entity-b"))


def test_two_long_targets_differing_at_the_end_differ() -> None:
    common = "x" * 400
    a, b = edge(common + "-one", common + "-two"), edge(common + "-one", common + "-twp")
    assert a.name != b.name
    for planned in (a, b):
        assert len(Path(planned.path).name.encode()) <= 255
        assert len(f"{planned.name}.yaml".encode()) <= 255


def test_the_cut_is_on_a_utf8_boundary() -> None:
    for text in ("ñ" * 300, "€" * 300, "😀" * 300, "a" + "€" * 300):
        out = bounded_name(text)
        assert len(out.encode()) <= MAX_NAME_BYTES
        assert out.encode().decode("utf-8") == out
        assert re.search(r"-[0-9a-f]{12}$", out)
    assert bounded_name("ñ" * 50) == "ñ" * 50


def test_extract_frontend_writes_a_component_in_a_deep_path(tmp_path: Path) -> None:
    root = new_project(tmp_path)
    extract(root)
    deep = root / "frontend" / "/".join(["d" * 28] * 3)
    shutil.copytree(FRONTEND, deep)
    extract_frontend(root)
    names = [p.name for p in (root / ".sldb").rglob("*") if p.is_file()]
    assert names and all(len(n.encode()) <= 255 for n in names)
    assert any(re.search(r"-[0-9a-f]{12}\.yaml$", n) for n in names if n.startswith("edge-"))
