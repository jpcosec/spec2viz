"""A capability of the domain is a node of specIR with its audience, and its acceptance test is a
materialization the rule `rule-specir-capability-has-an-acceptance-test` asks for.

The eight capabilities of docs/decisiones/paridad-por-capacidades.md are data of this repo's own
store (`specir/capabilities/`), read here through an isolated copy of it, served by the real
`sldb mcp` with specIR's extension. 7 and 8 are the ones the table marks as met, each with its
test; the other six have none, and the rule reports them (no test is invented for them)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
import yaml
from conftest import REPO, sldb
from pydantic import ValidationError
from specir.models import CapabilityDoc, DomainOperationDoc

RULE = "rule-specir-capability-has-an-acceptance-test"
DECISION = REPO / "docs" / "decisiones" / "paridad-por-capacidades.md"
#: The capabilities the table marks as met, and the test that accredits each.
WITH_TEST = {
    7: "tests/visual/test_api.py::test_validate_passes",
    8: "tests/visual/test_cli.py::test_render_each_type",
}


def table_rows() -> list[tuple[int, str]]:
    """(number, capability) of the table of the decision."""
    rows = []
    for line in DECISION.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 4 and cells[0].isdigit():
            rows.append((int(cells[0]), cells[1]))
    return rows


def every(mcp, tool: str, **arguments: Any) -> list[dict[str, Any]]:
    answer = mcp.call(tool, limit=200, **arguments)
    assert not answer["truncated"], answer
    return answer["items"]


def capabilities(mcp) -> dict[int, dict[str, Any]]:
    items = every(mcp, "select_documents", model="CapabilityDoc")
    return {int(i["name"].split("-")[1]): i for i in items}


def test_the_model_asks_for_an_audience() -> None:
    fields = {"title": "Validate", "origen": "declarado"}
    assert CapabilityDoc(**fields, audience=["agente", "JP"]).audience == ["agente", "JP"]
    for audience in ([], [" "]):
        with pytest.raises(ValidationError):
            CapabilityDoc(**fields, audience=audience)
    with pytest.raises(ValidationError):
        CapabilityDoc(**fields)
    # An operation read out of code is not a capability: it needs no audience.
    assert DomainOperationDoc(**fields).title == "Validate"
    assert issubclass(CapabilityDoc, DomainOperationDoc)


def test_the_eight_capabilities_of_the_table_are_in_the_store_each_with_its_audience(mcp) -> None:
    table = table_rows()
    assert [n for n, _ in table] == list(range(1, 9))
    stored = capabilities(mcp)
    assert sorted(stored) == list(range(1, 9))
    for number, _ in table:
        item = stored[number]
        document = mcp.call("read_document", ref=item["export_id"])
        audience = _field(document, "audience")
        assert audience and all(isinstance(a, str) and a.strip() for a in audience), (number, audience)
        assert _field(document, "origen") == "declarado"


def _field(document: dict[str, Any], name: str) -> Any:
    for holder in (document, document.get("fields") or {}, document.get("payload") or {}):
        if name in holder:
            return holder[name]
    raise AssertionError(f"{name} not in {sorted(document)}")


def test_the_rule_reports_the_six_capabilities_without_a_test_and_not_the_two_with_one(mcp) -> None:
    reported = [f for f in every(mcp, "specir_rules") if f["rule"] == RULE]
    stored = capabilities(mcp)
    assert {f["subject"] for f in reported} == {stored[n]["export_id"] for n in range(1, 7)}
    assert {f["severity"] for f in reported} == {"error"}
    assert all(f["what"] and f["path"] for f in reported)


@pytest.mark.parametrize("number", sorted(WITH_TEST))
def test_a_met_capability_links_its_test_by_a_materialization(mcp, number: int) -> None:
    capability = capabilities(mcp)[number]["export_id"]
    neighbours = mcp.call("neighbors", node=capability, relation="accepted_by", direction="outgoing")
    targets = [e["target"].removeprefix("sldb://document/") if "target" in e else e["target_id"] for e in _items(neighbours)]
    assert len(targets) == 1 and targets[0].startswith("MaterializationContractDoc:"), neighbours
    contract = mcp.call("read_document", ref=targets[0])
    assert _field(contract, "target_kind") == "test"
    assert _field(contract, "target_identity") == WITH_TEST[number]
    assert _field(contract, "source_atoms") == [capability]
    path, name = WITH_TEST[number].split("::")
    assert f"def {name}(" in (REPO / path).read_text(encoding="utf-8"), WITH_TEST[number]


def _items(answer: dict[str, Any]) -> list[dict[str, Any]]:
    for key in ("items", "neighbors", "edges", "nodes"):
        if key in answer:
            return answer[key]
    raise AssertionError(f"no neighbours in {sorted(answer)}")


def test_the_anchors_of_the_two_tests_are_intact() -> None:
    """`sldb anchors check` over this repo's store: the anchor of each test (`code:<path>::<name>`)
    is intact, and no anchor of a capability's test is reported."""
    done = sldb("anchors", "check", "--store", ".sldb", "--format", "json", cwd=REPO)
    report = json.loads(done.stdout)
    rows = report if isinstance(report, list) else next(v for v in report.values() if isinstance(v, list))
    ours = {r.get("ref"): r for r in rows if str(r.get("ref", "")).startswith("code:tests/visual/")}
    for target in WITH_TEST.values():
        row = ours.get(f"code:{target}")
        assert row is not None, (target, sorted(ours))
        assert row.get("state") == "intact", row


def test_the_view_lists_capability_audience_and_test(store_copy: Path) -> None:
    done = sldb("views", "run", "view-specir-capabilities", "--store", ".sldb", "--format", "json", cwd=store_copy)
    sections = json.loads(done.stdout)["sections"]
    rows = {r["name"]: r for r in sections["capabilities"]["rows"]}
    assert len(rows) == 8
    for name, row in rows.items():
        number = int(name.split("-")[1])
        assert row["fields"]["audience"], name
        assert bool(row["test"]) == (number in WITH_TEST), (name, row["test"])
    tests = {r["fields"]["target_identity"] for r in sections["tests"]["rows"]}
    assert tests == set(WITH_TEST.values())


def test_the_view_and_the_rule_are_seeded_by_install() -> None:
    data = REPO / "src" / "specir" / "data"
    view = next(v for v in yaml.safe_load((data / "views.yaml").read_text(encoding="utf-8")) if v["name"] == "view-specir-capabilities")
    assert [s["select"]["model"] for s in view["sections"]] == ["CapabilityDoc", "MaterializationContractDoc"]
    rule = next(r for r in yaml.safe_load((data / "rules.yaml").read_text(encoding="utf-8")) if r["name"] == RULE)
    assert rule["severity"] == "error" and rule["subject"] == "model <= CapabilityDoc"
