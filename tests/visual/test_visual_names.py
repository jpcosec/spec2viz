"""specIR's visual layer takes from sldb what is sldb's and does not redefine it.

- No class of specIR has the name of a visual vocabulary model of SLDB (the notation documents
  `sldb.api` exports and the notation and palette specs of `sldb.notations`).
- No class of specIR has the name of a diagram spec model: the eight models (and every model they
  are made of) are sldb's (D3) and `compile_ir` dispatches sldb's classes.
- spec2viz is imported, under tests/, only by the parity oracles (tests/visual/parity.py of IR11
  and tests/visual/render_parity.py of IR12); under src/specir/ never (tests/test_imports.py)."""

from __future__ import annotations

import ast
import inspect
import typing
from pathlib import Path

import sldb.api as api
import sldb.notations as notations
from pydantic import BaseModel
from sldb.api.notations import load_spec

from specir.visual import compile_ir
from specir.visual.spec_models import SPEC_MODELS, BaseDiagram, EnforcementArtifact, EnforcementFact

REPO = Path(__file__).resolve().parents[2]
PACKAGE = REPO / "src" / "specir"
TESTS = REPO / "tests"
#: The modules that reach spec2viz: none. Its answers are goldens (`tests/visual/goldens/`, `oracle.py`).
ORACLES: set[Path] = set()
EIGHT = {"ClassDiagram", "SequenceDiagram", "StateDiagram", "ComponentDiagram", "ActivityDiagram",
         "DeploymentDiagram", "MatrixDiagram", "ReflectionDiagram"}


def specir_classes() -> dict[str, str]:
    found = {}
    for path in sorted(PACKAGE.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.ClassDef):
                found[node.name] = str(path.relative_to(REPO))
    return found


def vocabulary() -> set[str]:
    docs = {n for n in dir(api) if inspect.isclass(getattr(api, n)) and getattr(api, n).__module__.startswith("sldb.models.notation")}
    specs = {n for n in notations.__all__ if inspect.isclass(getattr(notations, n)) and not issubclass(getattr(notations, n), Exception)}
    return docs | specs


def models_of(model: type, seen: set[type]) -> None:
    """`model` and every pydantic model its fields are made of."""
    if model in seen:
        return
    seen.add(model)
    for field in model.model_fields.values():
        for part in _types(field.annotation):
            if inspect.isclass(part) and issubclass(part, BaseModel):
                models_of(part, seen)


def _types(annotation) -> list:
    args = typing.get_args(annotation)
    return [annotation] if not args else [t for a in args for t in _types(a)]


def spec_model_names() -> set[str]:
    seen: set[type] = set()
    for model in (*SPEC_MODELS, BaseDiagram, EnforcementArtifact, EnforcementFact):
        models_of(model, seen)
    return {m.__name__ for m in seen}


def test_no_class_has_the_name_of_a_visual_vocabulary_model_of_sldb() -> None:
    names = vocabulary()
    assert {"SpecDoc", "SpecNodeDoc", "NotationDoc", "GlyphDoc", "LinkDoc", "PaletteDoc", "ViewDoc", "NotationSpec", "PaletteSpec"} <= names
    clashes = {name: where for name, where in specir_classes().items() if name in names}
    assert not clashes, clashes


def test_no_class_has_the_name_of_a_diagram_spec_model() -> None:
    names = spec_model_names()
    assert EIGHT <= names and {"NodeModel", "EdgeModel", "EnforcementArtifact"} <= names
    clashes = {name: where for name, where in specir_classes().items() if name in names}
    assert not clashes, clashes


def test_the_eight_spec_models_are_sldb_classes_and_compile() -> None:
    assert {m.__name__ for m in SPEC_MODELS} == EIGHT
    assert all(m.__module__.startswith("sldb.") for m in (*SPEC_MODELS, BaseDiagram, EnforcementArtifact, EnforcementFact))
    examples = REPO / "tests" / "visual" / "fixtures" / "spec2viz" / "examples"
    diagrams = [load_spec(path) for path in sorted(examples.rglob("*.yml"))]
    assert {type(d) for d in diagrams} == set(SPEC_MODELS)
    for diagram in diagrams:
        assert compile_ir(diagram) is not None, diagram.id


def test_spec2viz_is_imported_by_nobody() -> None:
    importing = set()
    for path in sorted([*TESTS.rglob("*.py"), *PACKAGE.rglob("*.py")]):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            names = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module or ""] if isinstance(node, ast.ImportFrom) else []
            if any(n.split(".")[0] == "spec2viz" for n in names):
                importing.add(path)
    assert importing == ORACLES, importing
