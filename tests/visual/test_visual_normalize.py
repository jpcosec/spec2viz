"""The normalization that decides structural equivalence (specir.visual.normalize)."""

from __future__ import annotations

import copy

from specir.visual.ir import ActivityIR, ActivityStep, ComponentEdge, ComponentIR, ComponentNode, SequenceIR, Participant, Message
from specir.visual.normalize import differences, equivalent, normalize


def component(nodes=None, edges=None) -> ComponentIR:
    return ComponentIR(
        title="T",
        nodes=nodes if nodes is not None else [ComponentNode("a", "A", "core", ["b", "c"]), ComponentNode("b", "B", "boundary")],
        edges=edges if edges is not None else [ComponentEdge("a", "b", "uses"), ComponentEdge("b", "a", "reads", "r")],
    )


def test_node_edge_and_contains_order_do_not_matter() -> None:
    left = component()
    right = component(
        nodes=[ComponentNode("b", "B", "boundary"), ComponentNode("a", "A", "core", ["c", "b"])],
        edges=[ComponentEdge("b", "a", "reads", "r"), ComponentEdge("a", "b", "uses")],
    )
    assert equivalent(left, right) and differences(left, right) == []


def test_provenance_metadata_does_not_matter() -> None:
    left = {"ir": normalize(component()), "metadata": {"origen": "declarado", "generated_at": "2026-11-15T00:00:00Z", "spec_path": "/abs/a.yml"}}
    right = {"ir": normalize(component()), "metadata": {"origen": "observado", "generated_at": "2026-11-16T10:00:00Z", "spec_path": "/other/b.yml"}}
    assert equivalent(left, right)
    assert normalize(left)["metadata"] == {}


def test_a_different_field_node_or_edge_is_not_equivalent() -> None:
    base = component()
    field = copy.deepcopy(base)
    field.nodes[1].kind = "core"
    node = copy.deepcopy(base)
    node.nodes.append(ComponentNode("c", "C", "core"))
    edge = copy.deepcopy(base)
    edge.edges[0] = ComponentEdge("a", "b", "writes")
    ends = copy.deepcopy(base)
    ends.edges[0] = ComponentEdge("b", "b", "uses")
    for changed in (field, node, edge, ends):
        assert not equivalent(base, changed)
        assert differences(base, changed)


def test_order_is_kept_where_it_means_something() -> None:
    steps = [ActivityStep("one", "One", next="two"), ActivityStep("two", "Two")]
    left = ActivityIR(title="T", start="one", steps=steps, end="two")
    right = ActivityIR(title="T", start="one", steps=list(reversed(steps)), end="two")
    assert not equivalent(left, right)
    messages = [Message(0, "a", "b", "x"), Message(1, "b", "a", "y")]
    participants = [Participant("a"), Participant("b")]
    assert not equivalent(SequenceIR("T", participants, messages), SequenceIR("T", participants, list(reversed(messages))))
    assert not equivalent(SequenceIR("T", participants, messages), SequenceIR("T", list(reversed(participants)), messages))


def test_the_type_name_is_compared() -> None:
    assert normalize(component())["__type__"] == "ComponentIR"
    assert not equivalent(component(), {"title": "T", "nodes": [], "edges": [], "style_kinds": {}})
