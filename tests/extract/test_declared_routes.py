"""extract_routes: the API operations of a non-DRF backend from a declared YAML table of routes."""

from __future__ import annotations

from pathlib import Path

import pytest

from extraction import documents, new_project

from specir.extract import extract, extract_frontend, extract_routes

TWO = "routes:\n  - {method: GET, route: /api/items}\n  - {method: POST, route: /api/x, title: Guardar x}\n"


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    return new_project(tmp_path)


def table(root: Path, text: str) -> Path:
    path = root / "routes.yaml"
    path.write_text(text, encoding="utf-8")
    return path


def operations(root: Path) -> dict:
    return {k: d for k, d in documents(root).items() if d.model_name == "ApiOperationDoc"}


def test_two_routes_write_two_declared_operations(project: Path) -> None:
    report = extract_routes(table(project, TWO), project / ".sldb")
    assert len(report.created) == 2 and report.stale_declared == []
    found = operations(project)
    assert {(d.payload["origen"], d.payload["method"], d.payload["route"]) for d in found.values()} == {("declarado", "GET", "/api/items"), ("declarado", "POST", "/api/x")}
    assert {d.payload["title"] for d in found.values()} == {"GET /api/items", "Guardar x"}


def test_running_twice_does_not_duplicate(project: Path) -> None:
    path = table(project, TWO)
    extract_routes(path, project / ".sldb")
    again = extract_routes(path, project / ".sldb")
    assert again.created == [] and len(again.unchanged) == 2
    assert len(operations(project)) == 2


@pytest.mark.parametrize("entry, named", [
    ("{method: post, route: /api/a}", r"routes\[1\]"),
    ("{method: FETCH, route: /api/a}", "FETCH"),
    ("{method: GET, route: api/a}", "api/a"),
])
def test_an_invalid_entry_is_a_value_error_that_names_it(project: Path, entry: str, named: str) -> None:
    path = table(project, f"routes:\n  - {entry}\n")
    with pytest.raises(ValueError, match=named):
        extract_routes(path, project / ".sldb")
    assert operations(project) == {}


def test_declared_route_links_the_invoke_of_the_frontend_and_fetch_stays_not_derived(project: Path) -> None:
    extract_routes(table(project, TWO), project / ".sldb")
    src = project / "frontend" / "src"
    src.mkdir(parents=True)
    (src / "SaveButton.tsx").write_text('import axios from "axios";\nexport function SaveButton() {\n  const save = () => { axios.post("/api/x"); };\n  return <button onClick={save}>Guardar</button>;\n}\n')
    (src / "FetchButton.tsx").write_text('export function FetchButton() {\n  const send = () => { fetch("/api/x", { method: "POST" }); };\n  return <button onClick={send}>Enviar</button>;\n}\n')
    report = extract_frontend(project)
    edges = {(d.payload["relation_type"], d.payload["target_id"]) for d in documents(project).values() if d.model_name == "RelationDoc"}
    assert ("invokes", "ApiOperationDoc:api-guardar-x") in edges
    assert len([e for e in edges if e[0] == "invokes"]) == 1
    # fetch gives no method in the facts: the call is reported as not derived, never linked
    assert any("fetch" in line and "FetchButton" in line for line in report.not_derived)


def test_a_name_held_by_a_derived_operation_is_refused_without_writing(project: Path) -> None:
    extract(project)
    derived = {k: d for k, d in operations(project).items() if d.payload["origen"] == "derivado"}
    assert derived
    one = next(iter(derived.values())).payload
    before = set(documents(project))
    path = table(project, f"routes:\n  - {{method: GET, route: /api/new}}\n  - {{method: {one['method']}, route: '{one['route']}'}}\n")
    with pytest.raises(ValueError, match=r"derivado") as error:
        extract_routes(path, project / ".sldb")
    assert one["title"] in str(error.value)
    assert set(documents(project)) == before


def test_declared_operations_that_left_the_table_are_reported_not_deleted(project: Path) -> None:
    extract_routes(table(project, TWO), project / ".sldb")
    report = extract_routes(table(project, "routes:\n  - {method: GET, route: /api/items}\n"), project / ".sldb")
    assert report.stale_declared == ["ApiOperationDoc:api-guardar-x"]
    assert "ApiOperationDoc:api-guardar-x" in operations(project)
