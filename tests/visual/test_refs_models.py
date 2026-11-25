"""The model and schema cases of spec2viz's `tests/test_refs.py` (SV-I03, IR13), ported against sldb's
spec models (D3) and specIR's schema export, without a wrapper.

The resolution cases of that file are in sldb (`tests/matching/test_matching_refs.py`, D4), the store
discovery and the import rule in `tests/test_imports.py`."""

from __future__ import annotations

import json

import pytest

from sldb.models.notation.diagram_specs.activity import StepModel
from sldb.models.notation.diagram_specs.class_diagram import ClassDefinition
from sldb.models.notation.diagram_specs.component import NodeModel
from sldb.models.notation.diagram_specs.deployment import ArtifactModel, DeploymentNodeModel
from sldb.models.notation.diagram_specs.sequence import ParticipantModel
from sldb.models.notation.diagram_specs.state import StateData
from specir.visual import json_schema


@pytest.mark.parametrize("model", [NodeModel, DeploymentNodeModel, ArtifactModel, StepModel, ClassDefinition, ParticipantModel])
def test_models_accept_refs(model):
    assert model.model_fields["refs"].default_factory() == []
    kwargs = {"id": "p"} if model is ParticipantModel else {"label": "L"} if model is StepModel else {}
    assert model(**kwargs, refs=["TaskDoc:task-x", "desk:AtomDoc:atom-y"]).refs == ["TaskDoc:task-x", "desk:AtomDoc:atom-y"]


@pytest.mark.parametrize("bad", ["sin-modelo", "Model:", ":name", "a b:c", "Model:na me"])
def test_refs_without_model_part_are_rejected(bad):
    with pytest.raises(Exception):
        NodeModel(refs=[bad])


def test_state_model_and_schema_expose_refs():
    data = StateData(entity="E", initial="a", states=[{"id": "a", "label": "A", "refs": ["TaskDoc:t"]}], transitions=[])
    assert data.states[0].refs == ["TaskDoc:t"]
    assert "refs" in json.dumps(json_schema("state"))
