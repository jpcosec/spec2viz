"""`atoms: [id]` por elemento del spec -> vinculacion explicita en el catalogo."""
import json
import re
from pathlib import Path

import pytest
import yaml
from click.testing import CliRunner

from spec2viz.cli import main
from spec2viz.models.state import StateData
from spec2viz.models.activity import StepModel
from spec2viz.models.class_diagram import ClassDefinition
from spec2viz.models.component import NodeModel
from spec2viz.models.deployment import ArtifactModel, DeploymentNodeModel
from spec2viz.models.sequence import ParticipantModel
from spec2viz.schema import json_schema


@pytest.mark.parametrize("model", [NodeModel, DeploymentNodeModel, ArtifactModel, StepModel, ClassDefinition, ParticipantModel])
def test_models_accept_atoms(model):
    assert model.model_fields["atoms"].default_factory() == []
    kwargs = {"id": "p"} if model is ParticipantModel else {"label": "L"} if model is StepModel else {}
    assert model(**kwargs, atoms=["a1", "a2"]).atoms == ["a1", "a2"]


def test_state_model_and_schema_expose_atoms():
    data = StateData(entity="E", initial="a", states=[{"id": "a", "label": "A", "atoms": ["x"]}], transitions=[])
    assert data.states[0].atoms == ["x"]
    assert "atoms" in json.dumps(json_schema("state"))


def _atom(d: Path, atom_id: str, title: str, q="what"):
    (d / f"{atom_id}.md").write_text(
        f"---\ntitle: {title}\nfive_wh_one_plus: {q}\nid: {atom_id}\n---\nCuerpo de {atom_id}.\n", encoding="utf-8"
    )


def _project(tmp_path, state_atoms_a, state_atoms_b):
    atoms = tmp_path / "atoms"
    atoms.mkdir()
    _atom(atoms, "atom-uno", "Uno")
    _atom(atoms, "atom-dos", "Dos", "why")
    _atom(atoms, "atom-ruido", "Otro tema")
    spec = {
        "id": "ciclo", "title": "Ciclo", "type": "state", "version": "1.0",
        "data": {
            "entity": "OC", "initial": "nueva",
            "states": [
                {"id": "nueva", "label": "4 Nueva", **({"atoms": state_atoms_a} if state_atoms_a is not None else {})},
                {"id": "cerrada", "label": "Cerrada", **({"atoms": state_atoms_b} if state_atoms_b is not None else {})},
            ],
            "transitions": [{"from": "nueva", "to": "cerrada", "on": "cierra"}],
        },
    }
    (tmp_path / "ciclo.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
    (tmp_path / "f.mmd").write_text("stateDiagram-v2\n  nueva --> cerrada\n", encoding="utf-8")
    (tmp_path / "vistas.yml").write_text(
        "vistas:\n  - id: v1\n    title: V1\n    src: f.mmd\n    type: state\n    specs: [ciclo.yml]\n", encoding="utf-8"
    )
    return atoms


def _build(tmp_path, atoms, *extra):
    out = tmp_path / "o.html"
    res = CliRunner().invoke(
        main, ["catalog", "build", "--config", str(tmp_path / "vistas.yml"), "--out", str(out), "--atoms-dir", str(atoms), *extra]
    )
    return res, (out.read_text(encoding="utf-8") if out.exists() else "")


def _explicit(html):
    data = json.loads(re.search(r"window\.ATOMS_EXPLICIT = (\{.*?\}); window\.COVERAGE", html, re.S).group(1))
    assert len(data) == 1
    return {"v1": next(iter(data.values()))}


def test_spec_with_atoms_validates(tmp_path):
    _project(tmp_path, ["atom-uno"], None)
    res = CliRunner().invoke(main, ["diagram", "validate", str(tmp_path / "ciclo.yml")])
    assert res.exit_code == 0, res.output


def test_build_exposes_explicit_map_by_label_and_id(tmp_path):
    atoms = _project(tmp_path, ["atom-uno", "atom-dos"], None)
    res, html = _build(tmp_path, atoms)
    assert res.exit_code == 0, res.output
    view = _explicit(html)["v1"]
    assert [a["id"] for a in view["4 nueva"]["list"]] == ["atom-uno", "atom-dos"]
    assert [a["id"] for a in view["nueva"]["list"]] == ["atom-uno", "atom-dos"]
    assert "cerrada" not in view


def test_unknown_atom_is_warning_unless_strict(tmp_path):
    atoms = _project(tmp_path, ["atom-uno", "no-existe"], None)
    res, html = _build(tmp_path, atoms)
    assert res.exit_code == 0
    assert "no-existe" in res.output + json.dumps(re.findall(r"SPEC2VIZ_ATOM_WARNINGS = (\[.*?\]);", html))
    assert [a["id"] for a in _explicit(html)["v1"]["4 nueva"]["list"]] == ["atom-uno"]
    res, _ = _build(tmp_path, atoms, "--strict-atoms")
    assert res.exit_code != 0
    assert "no-existe" in res.output


def test_fully_explicit_view_embeds_no_fuzzy_payload(tmp_path):
    atoms = _project(tmp_path, ["atom-uno"], ["atom-dos"])
    res, html = _build(tmp_path, atoms)
    assert res.exit_code == 0, res.output
    # el cuerpo de un atomo no referenciado ya no viaja en el HTML; los referenciados si (via ATOMS_EXPLICIT)
    assert "Cuerpo de atom-ruido." not in html
    assert "Cuerpo de atom-uno." in html and "Cuerpo de atom-dos." in html


def test_partially_explicit_view_keeps_fuzzy_payload(tmp_path):
    atoms = _project(tmp_path, ["atom-uno"], None)
    res, html = _build(tmp_path, atoms)
    assert "Cuerpo de atom-ruido." in html
