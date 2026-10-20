"""Activity: particiones (swimlanes), merge y notas UML, opcionales y retrocompatibles."""
from pathlib import Path

import pytest

from spec2viz.compilers import compile_ir
from spec2viz.exceptions import StructureError, UnknownReferenceError, ValidationError
from spec2viz.loader import load
from spec2viz.renderers.d2 import D2Renderer
from spec2viz.renderers.mermaid import MermaidRenderer
from spec2viz.renderers.plantuml import PlantUMLRenderer
from spec2viz.validator import validate

FIXTURES = Path(__file__).parent / "fixtures"
LANES = FIXTURES / "activity.lanes.yml"


def _ir(path=LANES):
    diagram = load(path)
    validate(diagram)
    return compile_ir(diagram)


def test_fields_reach_the_ir():
    steps = {s.id: s for s in _ir().steps}
    assert steps["open_pr"].partition == "Dev" and steps["review"].notes == "Two approvals for production"
    assert steps["joined"].kind == "merge" and steps["joined"].notes is None


def test_mermaid_draws_one_lane_per_partition_merge_as_diamond_and_notes():
    out = MermaidRenderer().render(_ir())
    lanes = [l.strip() for l in out.splitlines() if l.strip().startswith("subgraph")]
    assert lanes == ['subgraph __lane0 ["Dev"]', 'subgraph __lane1 ["Approver"]', 'subgraph __lane2 ["Script"]', 'subgraph __lane3 ["AWS"]']
    assert 'joined{" "}' in out and 'review{"Approve?"}' in out
    assert 'review__note["Two approvals for production"]:::note' in out and "review -.- review__note" in out
    assert "classDef note" in out


def test_mermaid_without_the_new_fields_is_unchanged():
    out = MermaidRenderer().render(_ir(FIXTURES / "activity.validation.yml"))
    assert "subgraph" not in out and "note" not in out
    assert out.splitlines()[:8] == ["---", "config:", "  layout: elk", "  flowchart:", "    curve: linear", "---", "flowchart TD", "    __start([Start])"]


def test_plantuml_swimlanes_and_note():
    out = PlantUMLRenderer().render(_ir())
    lines = out.splitlines()
    assert lines[:3] == ["@startuml", "|Dev|", "start"]
    assert "|Approver|" in lines and "note right: Two approvals for production" not in lines  # la nota es de una decision
    assert "|Script|" in lines


def test_plantuml_note_on_an_action():
    diagram = load(LANES)
    diagram.data.steps["deploy"].notes = "Blue/green"
    out = PlantUMLRenderer().render(compile_ir(diagram))
    assert ":Deploy;\nnote right: Blue/green" in out


def test_d2_lanes_are_containers_and_edges_use_qualified_ids():
    out = D2Renderer().render(_ir())
    assert '__lane0: "Dev"' in out and '__lane0.open_pr: "Open pull request"' in out
    assert "__lane2.joined.shape: diamond" in out and "__lane0.open_pr -> __lane1.review" in out
    assert "__lane1.review__note.shape: page" in out


def test_merge_with_branches_is_a_structure_error():
    diagram = load(LANES)
    diagram.data.steps["joined"].branches = {"a": "verify"}
    with pytest.raises(StructureError, match="merge"):
        validate(diagram)


def test_unknown_target_is_typed_and_still_a_validation_error():
    diagram = load(LANES)
    diagram.data.steps["deploy"].next = "nowhere"
    with pytest.raises(UnknownReferenceError) as info:
        validate(diagram)
    assert isinstance(info.value, ValidationError)


def test_empty_partition_is_rejected():
    diagram = load(LANES)
    diagram.data.steps["deploy"].partition = "  "
    with pytest.raises(StructureError, match="empty partition"):
        validate(diagram)


sldb_api = pytest.importorskip("sldb.api")


def test_sync_keeps_partition_and_notes_and_merge_has_its_glyph(tmp_path):
    import shutil

    from spec2viz.notation_view import resolve_view
    from spec2viz.sldb_sync import SpecSync

    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    spec = shutil.copy(LANES, tmp_path / "docs" / "lanes.yml")
    report = SpecSync(tmp_path / ".sldb").sync(Path(spec))
    assert report.problems == []
    view = resolve_view(tmp_path / ".sldb", "activity.lanes")
    nodes = {n["element"]: n for n in view["nodes"]}
    assert nodes["joined"]["glyph"] == "GlyphDoc:activity.merge" and nodes["review"]["glyph"] == "GlyphDoc:activity.decision"
    docs = {d.name: d.payload for d in sldb_api.load_runtime_documents(tmp_path / ".sldb", None, include_linked=False) if str(d.model_name) == "SpecNodeDoc"}
    assert docs["activity.lanes.open_pr"]["data"]["partition"] == "Dev"
    assert docs["activity.lanes.review"]["data"]["notes"] == "Two approvals for production"
