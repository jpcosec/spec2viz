import pytest
from pathlib import Path
from spec2viz.loader import load
from spec2viz.models.sequence   import SequenceDiagram
from spec2viz.models.state      import StateDiagram
from spec2viz.models.component  import ComponentDiagram
from spec2viz.models.activity   import ActivityDiagram
from spec2viz.models.deployment import DeploymentDiagram
from spec2viz.models.matrix     import MatrixDiagram
from spec2viz.exceptions import ParseError

FIXTURES = Path("tests/fixtures")

def test_load_sequence():
    assert isinstance(load(FIXTURES / "sequence.create-quotation.yml"), SequenceDiagram)

def test_load_state():
    assert isinstance(load(FIXTURES / "state.quotation.yml"), StateDiagram)

def test_load_component():
    assert isinstance(load(FIXTURES / "component.quotation.yml"), ComponentDiagram)

def test_load_activity():
    assert isinstance(load(FIXTURES / "activity.validation.yml"), ActivityDiagram)

def test_load_deployment():
    assert isinstance(load(FIXTURES / "deployment.runtime.yml"), DeploymentDiagram)

def test_load_matrix():
    assert isinstance(load(FIXTURES / "matrix.quotation-view.yml"), MatrixDiagram)

def test_missing_file_raises():
    with pytest.raises(ParseError, match="not found"):
        load(FIXTURES / "nonexistent.yml")

def test_unsupported_type_raises(tmp_path):
    f = tmp_path / "bad.yml"
    f.write_text("id: x\ntitle: X\ntype: random_diagram\nversion: '0.1'\ndata: {}\n")
    with pytest.raises(ParseError, match="Unsupported diagram type"):
        load(f)

def test_malformed_yaml_raises():
    with pytest.raises(ParseError, match="YAML parse error"):
        load(Path("tests/fixtures/invalid/malformed.yml"))

def test_bad_schema_raises():
    with pytest.raises(ParseError, match="Invalid diagram schema"):
        load(Path("tests/fixtures/invalid/bad_schema.yml"))


# ── unknown keys are errors, with their path (reported from MEPU: `edges` in a deployment validated OK) ──

import copy

import yaml

NESTED_DEPLOYMENT = FIXTURES / "deployment.nested.yml"


def _with(tmp_path, mutate):
    raw = yaml.safe_load(NESTED_DEPLOYMENT.read_text(encoding="utf-8"))
    mutate(raw)
    f = tmp_path / "spec.yml"
    f.write_text(yaml.safe_dump(raw, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return f


@pytest.mark.parametrize("mutate,path", [
    # the MEPU case: `edges` is not part of deployment (its arrows are `connections`), and it was ignored
    (lambda r: r["data"].__setitem__("edges", copy.deepcopy(r["data"]["connections"])), "data.edges"),
    (lambda r: r.__setitem__("estado", "x"), "estado"),
    (lambda r: r.setdefault("metadata", {}).__setitem__("estado", {"hecho": ["a"]}), "metadata.estado"),
    (lambda r: next(iter(r["data"]["nodes"].values())).__setitem__("colour", "red"),
     "data.nodes.{node}.colour"),
    (lambda r: r["data"]["connections"][0].__setitem__("via", "vpn"), "data.connections.0.via"),
])
def test_an_unknown_key_at_any_level_is_an_error_with_its_path(tmp_path, mutate, path):
    raw = yaml.safe_load(NESTED_DEPLOYMENT.read_text(encoding="utf-8"))
    path = path.format(node=next(iter(raw["data"]["nodes"])))
    with pytest.raises(ParseError, match=rf"unknown key '{path}'"):
        load(_with(tmp_path, mutate))


def test_every_unknown_key_is_listed_and_known_keys_still_load(tmp_path):
    def two(r):
        r["data"]["edges"] = []
        r["extra_top"] = 1
    with pytest.raises(ParseError) as err:
        load(_with(tmp_path, two))
    assert "unknown key 'data.edges'" in str(err.value) and "unknown key 'extra_top'" in str(err.value)
    assert isinstance(load(_with(tmp_path, lambda r: None)), DeploymentDiagram)


def test_metadata_takes_project_annotations_only_as_x_keys(tmp_path):
    """`x-*` under metadata is the project's annotation space (kept under `extensions`); data has none."""
    def anotar(r):
        r.setdefault("metadata", {})["x-fuentes"] = ["specs/negocio/README.md §3"]
        r["metadata"]["x-estado"] = {"construido": ["vpc"], "por_construir": []}
    d = load(_with(tmp_path, anotar))
    assert d.metadata.extensions == {"x-fuentes": ["specs/negocio/README.md §3"],
                                     "x-estado": {"construido": ["vpc"], "por_construir": []}}
    with pytest.raises(ParseError, match=r"unknown key 'data.x-nota'"):
        load(_with(tmp_path, lambda r: r["data"].__setitem__("x-nota", 1)))
    with pytest.raises(ParseError, match=r"unknown key 'metadata.fuentes'"):
        load(_with(tmp_path, lambda r: r.setdefault("metadata", {}).__setitem__("fuentes", [])))


def test_every_example_and_fixture_has_only_known_keys():
    """Forbidding unknown keys must not break a spec the project ships."""
    from spec2viz.loader import _valid_types
    specs = [p for p in [*Path("examples").rglob("*.yml"), *FIXTURES.glob("*.yml")]
             if (yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("type") in _valid_types]
    assert specs
    for p in specs:
        try:
            load(p)
        except ParseError as e:
            assert "unknown key" not in str(e), f"{p}: {e}"
