"""JSON Schema export of specs and catalogs (SV-A15, SV-A16), migrated from `spec2viz.schema`.

The models are sldb's (D3); specIR only exports their schema. The export equals spec2viz's for all
types, each type and the diagram store envelope: against the saved goldens and spec2viz's checked-in
schemas (`examples/schema/`) always, against spec2viz live when it is installed. Ported from spec2viz
(revision 2de1056): `test_json_schema_for_all_types`, `test_json_schema_for_specific_type` and
`test_write_json_schema` of `tests/test_api.py`; `test_schema_stdout`, `test_schema_outfile`,
`test_schema_diagram_store_stdout`, `test_schema_invalid_type_fails` and `test_catalog_schema_stdout`
of `tests/test_cli.py` (on `diagram schema`, the command the top-level alias of IR13d calls); and
`test_schema_examples_match_generated_output` and `test_every_model_field_has_a_description` of
`tests/test_packaging.py` (the second over the exported schema, since the model classes are sldb's)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import render_parity  # noqa: E402

from specir.cli import main  # noqa: E402
from specir.visual.schema import json_schema, write_json_schema  # noqa: E402

SCHEMAS = HERE / "fixtures" / "spec2viz" / "examples" / "schema"
runner = CliRunner()


def test_schema_goldens_cover_every_type():
    assert set(render_parity.schema_goldens()) == {str(t or "all") for t in render_parity.SCHEMA_TYPES}


def test_specir_exports_what_the_goldens_say():
    assert render_parity.schemas(json_schema) == render_parity.schema_goldens()


@pytest.mark.parity
def test_specir_exports_what_spec2viz_exports():
    pytest.importorskip("spec2viz")
    assert render_parity.schemas(json_schema) == render_parity.schemas(render_parity.spec2viz_json_schema())


# ── tests/test_api.py ───────────────────────────────────────────────────────────────────────────


def test_json_schema_for_all_types():
    schema = json_schema()

    assert "$defs" in schema
    assert "SequenceDiagram" in schema["$defs"]


def test_json_schema_for_specific_type():
    schema = json_schema("sequence")

    assert schema["title"] == "SequenceDiagram"
    assert schema["properties"]["data"]["description"] == "Sequence-specific participants and messages."


def test_write_json_schema(tmp_path):
    path = write_json_schema(tmp_path / "sequence.schema.json", diagram_type="sequence")

    assert path.exists()
    assert json.loads(path.read_text())["title"] == "SequenceDiagram"


# ── tests/test_cli.py ───────────────────────────────────────────────────────────────────────────


def test_schema_stdout():
    r = runner.invoke(main, ["diagram", "schema", "--type", "sequence"])
    assert r.exit_code == 0
    assert '"title": "SequenceDiagram"' in r.output


def test_schema_outfile(tmp_path):
    out = tmp_path / "schema.json"
    r = runner.invoke(main, ["diagram", "schema", "--type", "state", "--out", str(out)])
    assert r.exit_code == 0
    assert out.exists()


def test_schema_diagram_store_stdout():
    r = runner.invoke(main, ["diagram", "schema", "--type", "diagram-store"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output
    assert '"diagram_store"' in r.output


def test_schema_invalid_type_fails():
    r = runner.invoke(main, ["diagram", "schema", "--type", "unknown"])
    assert r.exit_code != 0


def test_catalog_schema_stdout():
    r = runner.invoke(main, ["catalog", "schema"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output
    assert json.loads(r.output) == json_schema("diagram-store")


# ── tests/test_packaging.py ─────────────────────────────────────────────────────────────────────


def test_schema_examples_match_generated_output():
    assert json.loads((SCHEMAS / "spec2viz.schema.json").read_text()) == json_schema()
    assert json.loads((SCHEMAS / "sequence.schema.json").read_text()) == json_schema("sequence")


#: The models spec2viz's test checked, by the name of their schema definition. `BaseDiagram` has no
#: definition of its own: its fields are in each `*Diagram`.
DESCRIBED_MODELS = (
    "Metadata", "Style", "ParticipantModel", "MessageModel", "SequenceData", "SequenceDiagram",
    "StateModel", "TransitionModel", "StateData", "StateDiagram", "NodeModel", "EdgeModel", "ComponentData",
    "ComponentDiagram", "StepModel", "ActivityData", "ActivityDiagram", "DeploymentNodeModel", "ArtifactModel",
    "ConnectionModel", "DeploymentData", "DeploymentDiagram", "MatrixStageModel", "MatrixViewModel",
    "MatrixComponentModel", "MatrixData", "MatrixDiagram",
)


def test_every_model_field_has_a_description():
    """Every field of the models spec2viz checked has a description in the exported schema."""
    definitions = json_schema()["$defs"]
    missing = [
        f"{name}.{field}"
        for name in DESCRIBED_MODELS
        for field, prop in definitions[name]["properties"].items()
        if not prop.get("description")
    ]
    assert not missing, missing
