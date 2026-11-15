"""specIR's own tools (specir.mcp_extension) on the server of sldb, over the blog store the MCP
write tools populated (tests/models/blog.py). Expected values come from the fixture
tests/fixtures/blog_chain.yaml and from the domain types, never from restated literals."""

from __future__ import annotations

from collections import Counter

from blog import blog_chain
from conftest import BLOG_WRITER
from specir.models import DOMAIN_MODELS

LAYER = {m.__name__: m.__semantics__["layer"][0] for m in DOMAIN_MODELS}


def written_nodes() -> list[dict]:
    """The specIR nodes the fixture creates (its ViewDocs are SLDB's, not specIR's)."""
    return [c for b in blog_chain()["batches"] for c in b["changes"] if c.get("action") == "create" and c["model"] in LAYER]


def every_node(session, **filters) -> list[dict]:
    answer = session.call("specir_nodes", limit=500, **filters)
    assert not answer["truncated"], answer
    return answer["items"]


def test_specir_types_counts_what_the_store_tracks(blog) -> None:
    answer = blog.call("specir_types")
    assert "explanation" not in answer
    counts = Counter(c["model"] for c in written_nodes())
    by_type = {r["type"]: r for r in answer["items"]}
    assert list(by_type) == [m.__name__ for m in DOMAIN_MODELS]
    for name, row in by_type.items():
        assert row["registered"] is True and row["layer"] == LAYER[name], row
        assert row["documents"] == counts[name], (name, row)
    assert by_type["TableDoc"]["fields"] == ["schema_name", "columns"]


def test_specir_nodes_carry_the_provenance_of_each_node(blog) -> None:
    nodes = {n["export_id"]: n for n in every_node(blog)}
    assert set(nodes) == {f"{c['model']}:{c['name']}" for c in written_nodes()}
    for change in written_nodes():
        node = nodes[f"{change['model']}:{change['name']}"]
        payload = change["payload"]
        assert node["title"] == payload["title"] and node["origen"] == payload["origen"] and node["verificacion"] == "sin_verificar"
        assert node["desconocidos"] == payload.get("desconocidos", {}) and node["layer"] == LAYER[change["model"]]
        assert node["address"] == blog.call("read_document", ref=node["export_id"])["address"]
        assert blog.call("read_document", ref=node["export_id"])["provenance"]["by"] == BLOG_WRITER


def test_specir_nodes_filter_by_type_layer_and_provenance(blog) -> None:
    written = written_nodes()
    assert {n["export_id"] for n in every_node(blog, kind="StateDoc")} == {f"StateDoc:{c['name']}" for c in written if c["model"] == "StateDoc"}
    assert {n["type"] for n in every_node(blog, layer="domain")} == {c["model"] for c in written if LAYER[c["model"]] == "domain"}
    assert len(every_node(blog, origen="declarado")) == len(written)
    empty = blog.call("specir_nodes", origen="observado")
    assert empty["total"] == 0 and empty["explanation"]
    assert blog.call("specir_nodes", verificacion="sin_verificar")["total"] == len(written)


def test_an_unknown_type_is_a_signal_with_the_domain_types_as_suggestions(blog) -> None:
    answer = blog.call("specir_nodes", kind="TablDoc")
    assert answer["total"] == 0 and answer["signal"] == "unknown_model" and answer["registered_as_signal"] is True
    assert "TableDoc" in answer["suggestions"]
    logged = blog.call("list_signals", limit=500)["items"][-1]
    assert (logged["tool"], logged["signal_class"], logged["actor"]) == ("specir_nodes", "unknown_model", BLOG_WRITER)


def test_the_write_tools_come_with_the_extension_from_level_1(blog) -> None:
    names = {t.name for t in blog.list_tools()}
    assert {"propose_changes", "apply_changes", "specir_types", "specir_nodes"} <= names
    described = next(t for t in blog.list_tools() if t.name == "propose_changes")
    assert "IR05 D2-E" in described.description
