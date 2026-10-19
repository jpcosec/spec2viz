"""Deployment: nodos anidados, communication paths entre nodos y «deploy»/«manifest»."""
from pathlib import Path

import pytest

from spec2viz.compilers import compile_ir
from spec2viz.exceptions import EndpointKindError, StructureError, UnknownReferenceError
from spec2viz.loader import load
from spec2viz.renderers.d2 import D2Renderer
from spec2viz.renderers.mermaid import MermaidRenderer
from spec2viz.renderers.plantuml import PlantUMLRenderer
from spec2viz.validator import validate

NESTED = Path(__file__).parent / "fixtures" / "deployment.nested.yml"


def _diagram():
    return load(NESTED)


def _ir():
    diagram = _diagram()
    validate(diagram)
    return compile_ir(diagram)


def test_mermaid_nests_subgraphs_and_marks_deploy_and_manifest():
    out = MermaidRenderer().render(_ir())
    lines = out.splitlines()
    order = [l.strip() for l in lines if l.strip().startswith("subgraph")]
    assert order == ['subgraph vpc ["VPC"]', 'subgraph subnet ["Private subnet"]', 'subgraph cluster ["ECS cluster"]', 'subgraph db ["Postgres"]', 'subgraph edge ["CDN"]']
    assert '            subgraph cluster ["ECS cluster"]' in lines and '                api_service["api service"]' in lines
    assert '    cluster -->|"queries · :5432"| db' in lines and '    edge -->|"HTTPS"| cluster' in lines
    assert '    api_image -.->|"«deploy»"| cluster' in lines and '    api_image -.->|"«manifest»"| api_service' in lines


def test_plantuml_and_d2_nest_and_d2_edges_use_container_paths():
    puml = PlantUMLRenderer().render(_ir())
    assert 'node "VPC" as vpc {\n  node "Private subnet" as subnet {\n    node "ECS cluster" as cluster {' in puml
    assert "api_image ..> cluster : «deploy»" in puml
    d2 = D2Renderer().render(_ir())
    assert 'vpc.subnet.cluster.api_service: "api service"' in d2
    assert 'edge -> vpc.subnet.cluster: "HTTPS"' in d2 and "api_image -> vpc.subnet.cluster: \"«deploy»\" {style.stroke-dash: 3}" in d2


@pytest.mark.parametrize("mutate, error, message", [
    (lambda d: d.data.nodes["cluster"].contains.append("vpc"), StructureError, "cycle"),
    (lambda d: d.data.nodes["edge"].contains.append("subnet"), StructureError, "contained by both"),
    (lambda d: d.data.nodes["vpc"].contains.append("vpc"), StructureError, "contains itself"),
    (lambda d: d.data.artifacts.update({"db": d.data.artifacts["api_image"]}), StructureError, "both a node and an artifact"),
    (lambda d: d.data.nodes["vpc"].contains.append("ghost"), UnknownReferenceError, "unknown node or artifact 'ghost'"),
    (lambda d: setattr(d.data.connections[0], "to", "ghost"), UnknownReferenceError, "unknown node or artifact 'ghost'"),
    (lambda d: setattr(d.data.connections[2], "to", "api_service"), EndpointKindError, "deploy connection goes artifact -> node"),
    (lambda d: setattr(d.data.connections[2], "from_", "edge"), EndpointKindError, "goes node -> node"),
    (lambda d: setattr(d.data.connections[0], "to", "api_service"), EndpointKindError, "communication"),
])
def test_typed_errors_tell_unknown_ids_from_disallowed_ends(mutate, error, message):
    diagram = _diagram()
    mutate(diagram)
    with pytest.raises(error, match=message):
        validate(diagram)


def test_artifact_to_artifact_communication_still_valid():
    validate(load(Path(__file__).parent / "fixtures" / "deployment.runtime.yml"))


sldb_api = pytest.importorskip("sldb.api")


def test_sync_nests_nodes_and_draws_deploy_and_manifest(tmp_path):
    import shutil

    from spec2viz.notation_view import resolve_view
    from spec2viz.sldb_sync import SpecSync

    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    spec = shutil.copy(NESTED, tmp_path / "docs" / "nested.yml")
    report = SpecSync(tmp_path / ".sldb").sync(Path(spec))
    assert report.problems == [] and set(report.relation_types_added) >= {"connects", "deploy", "manifest"}
    view = resolve_view(tmp_path / ".sldb", "deployment.nested")
    assert view["skipped"] == []
    links = {(l["relation"], l["label"]) for l in view["links"]}
    assert ("connects", "queries :5432") in links and ("connects", "HTTPS") in links
    assert ("deploy", "«deploy»") in links and ("manifest", "«manifest»") in links
    nest = {(l["source"].rsplit(".", 1)[-1], l["target"].rsplit(".", 1)[-1]) for l in view["links"] if l["relation"] == "contains"}
    assert {("vpc", "subnet"), ("subnet", "cluster"), ("cluster", "api_service")} <= nest
