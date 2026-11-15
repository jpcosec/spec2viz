"""Diagrams as projections of the graph (IR11), over the blog of IR06 (tests/models/blog.py) and
over a store with spec2viz's specs synced by sldb (D1).

- The component and state projections of the blog's ViewDocs show the entity Post, and the store
  still has one document for it: projecting writes nothing.
- The authored spec of the publish components (fixtures/blog/) and the projection of
  ViewDoc:publish-components compile to structurally equivalent IRs; so does a composed ViewDoc
  (with sections, run by `run_view`) and the same selection as a projection.
- A SpecDoc with its SpecNodeDoc, resolved by `resolve_view`, gives the IR its YAML compiles to,
  except in what the store does not keep (`SPEC_DOC_GAPS`)."""

from __future__ import annotations

import dataclasses
import shutil
import sys
from pathlib import Path

import pytest
import sldb.api as api
from sldb.api.notations import load_spec, validate_spec

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "models"))  # blog.py, for conftest's blog fixtures

from blog import apply  # noqa: E402
from conftest import sldb, tree_digest  # noqa: E402
from specir.visual import ANY_STATE, compile_ir, component_from_view, differences, from_spec_doc, state_from_view  # noqa: E402
from specir.visual.projections import SPEC_DOC_GAPS  # noqa: E402

HERE = Path(__file__).resolve().parent
AUTHORED = HERE / "fixtures" / "blog" / "component.publish-components.yml"
SPEC2VIZ = HERE / "fixtures" / "spec2viz"
SYNCED = [
    "tests/fixtures/component.quotation.yml", "tests/fixtures/component.kinds.yml", "tests/fixtures/component.styled.yml",
    "tests/fixtures/state.quotation.yml", "examples/state/example.yml",
]
POST = "DomainEntityDoc:post"
COMPOSED = "post-persistence"


def documents_named_post(root: Path) -> list[str]:
    """Every document of the store that is, or draws, the entity Post."""
    found = []
    for document in api.load_runtime_documents(root / ".sldb", None, include_linked=False):
        payload = document.payload or {}
        if payload.get("title") == "Post" or POST in (payload.get("refs") or []):
            found.append(f"{document.model_name}:{document.name}")
    return found


@pytest.fixture(scope="module")
def blog_store(blog, blog_root: Path) -> Path:
    """The blog's store, written by the MCP (conftest's `blog`), and checked to have one Post."""
    assert documents_named_post(blog_root) == [POST]
    return blog_root / ".sldb"


def test_component_projection_shows_post_and_writes_nothing(blog_store: Path, blog_root: Path) -> None:
    before = tree_digest(blog_root)
    ir = component_from_view(blog_store, "ViewDoc:publish-components")
    post = next(n for n in ir.nodes if n.label == "Post")
    assert (post.id, post.kind) == ("document_DomainEntityDoc_post", "DomainEntityDoc")
    assert ("persisted_in", "document_TableDoc_posts") in {(e.relation, e.to) for e in ir.edges if e.from_ == post.id}
    assert len(ir.nodes) == 7 and len(ir.edges) == 6
    assert tree_digest(blog_root) == before
    assert documents_named_post(blog_root) == [POST]


def test_state_projection_shows_post_and_writes_nothing(blog_store: Path, blog_root: Path) -> None:
    before = tree_digest(blog_root)
    ir = state_from_view(blog_store, "ViewDoc:post-states")
    assert ir.entity == "Post"
    assert [(s.id, s.label) for s in ir.states] == [("post-draft", "Draft"), ("post-published", "Published")]
    assert ir.initial == "post-draft"
    assert [(t.from_, t.to, t.on) for t in ir.transitions] == [(ANY_STATE, "post-published", "PublishPost")]
    assert tree_digest(blog_root) == before
    assert documents_named_post(blog_root) == [POST]


def test_authored_spec_and_projection_compile_to_equivalent_irs(blog_store: Path) -> None:
    authored = load_spec(AUTHORED)
    validate_spec(authored)
    projected = component_from_view(blog_store, "ViewDoc:publish-components")
    assert differences(compile_ir(authored), projected) == []


def test_a_composed_view_projects_like_a_projection_view(blog, blog_store: Path, blog_root: Path) -> None:
    """A ViewDoc with sections (run by `run_view`) and a projection ViewDoc of the same documents
    and relation give the same ComponentIR but for the title."""
    composed = {"action": "create", "model": "ViewDoc", "name": COMPOSED, "path": f"blog/views/{COMPOSED}.md", "payload": {
        "id": COMPOSED, "name": COMPOSED, "title": "Persistencia de Post",
        "sections": [
            {"key": "entities", "select": {"model": "DomainEntityDoc"}, "edges": [{"relation": "persisted_in", "direction": "out"}]},
            {"key": "tables", "select": {"model": "TableDoc"}},
        ],
        "description": "Where the entities of the blog are persisted.",
    }}
    plain = {"action": "create", "model": "ViewDoc", "name": f"{COMPOSED}-projection", "path": f"blog/views/{COMPOSED}-projection.md", "payload": {
        "id": f"{COMPOSED}-projection", "name": f"{COMPOSED}-projection", "title": "Persistencia de Post",
        "nodes": [{"model": "DomainEntityDoc"}, {"model": "TableDoc"}], "relations": ["persisted_in"],
        "description": "Where the entities of the blog are persisted.",
    }}
    written = apply(blog, [composed, plain])
    assert written["applied"] is True, written
    try:
        from_sections = component_from_view(blog_store, f"ViewDoc:{COMPOSED}")
        from_projection = component_from_view(blog_store, f"ViewDoc:{COMPOSED}-projection")
        assert {n.label for n in from_sections.nodes} == {"Post", "posts"}
        assert [(e.from_, e.to, e.relation) for e in from_sections.edges] == [("document_DomainEntityDoc_post", "document_TableDoc_posts", "persisted_in")]
        assert differences(from_sections, from_projection) == []
    finally:
        removed = apply(blog, [{"action": "delete", "model": "ViewDoc", "name": name} for name in (COMPOSED, f"{COMPOSED}-projection")])
        assert removed["applied"] is True, removed
    assert documents_named_post(blog_root) == [POST]


@pytest.fixture(scope="module")
def spec_store(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A new store with spec2viz's component and state specs synced by `sldb notations sync --spec`."""
    root = tmp_path_factory.mktemp("specir-specdoc") / "project"
    (root / "specs").mkdir(parents=True)
    sldb("stores", "init", "--path", str(root), cwd=root)
    synced = []
    for rel in SYNCED:
        target = root / "specs" / rel.replace("/", "__")
        shutil.copy2(SPEC2VIZ / rel, target)
        synced += ["--spec", str(target.relative_to(root))]
    sldb("notations", "sync", *synced, "--store", ".sldb", cwd=root)
    return root


@pytest.mark.parametrize("rel", SYNCED)
def test_a_spec_doc_gives_the_ir_of_its_yaml(spec_store: Path, rel: str) -> None:
    diagram = load_spec(SPEC2VIZ / rel)
    expected = compile_ir(diagram)
    found = from_spec_doc(spec_store / ".sldb", f"SpecDoc:{diagram.id}")
    gaps = SPEC_DOC_GAPS[type(expected).__name__]
    assert all(not getattr(found, gap) for gap in gaps)
    assert differences(found, dataclasses.replace(expected, **{gap: getattr(found, gap) for gap in gaps})) == []
