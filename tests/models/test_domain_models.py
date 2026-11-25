"""The domain models are code of specIR, registered by SLDB's registry; the relation types and
rules are data of the store, seeded by `specir.install`; no visual model of SLDB is redefined."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import sldb.api as api
import yaml
from pydantic import ValidationError

import specir.models as models
from blog import install
from conftest import REPO
from specir.models import DOMAIN_MODELS, SpecIRNodeDoc

#: The visual vocabulary of SLDB (sldb.models.notation_models), served by sldb.api.
SLDB_VISUAL = (api.SpecDoc, api.SpecNodeDoc, api.NotationDoc, api.GlyphDoc, api.LinkDoc, api.PaletteDoc, api.ViewDoc)
DATA = REPO / "src" / "specir" / "data"
KINDS = {"InterfaceControlDoc", "InterfaceActionDoc", "InterfaceFieldDoc", "ApiOperationDoc", "ApiFieldDoc", "HandlerDoc", "DomainOperationDoc", "CapabilityDoc", "PolicyDoc", "StateDoc", "DomainEntityDoc", "TableDoc", "PieceDoc"}


def test_the_model_classes_live_in_the_specir_package() -> None:
    assert {m.__name__ for m in DOMAIN_MODELS} == KINDS
    for model in DOMAIN_MODELS:
        assert model.__module__ == "specir.models.domain", model
        assert issubclass(model, api.StructuredNLDoc) and issubclass(model, SpecIRNodeDoc), model
        assert Path(models.__file__).parent == REPO / "src" / "specir" / "models"


def test_no_visual_model_of_sldb_is_redefined() -> None:
    visual = {v.__name__ for v in SLDB_VISUAL}
    for model in (SpecIRNodeDoc, *DOMAIN_MODELS):
        assert model.__name__ not in visual and not issubclass(model, SLDB_VISUAL), model
    exported = {name for name in models.__all__ if isinstance(getattr(models, name), type)}
    assert not exported & visual


def test_install_registers_the_models_by_sldbs_registry_and_seeds_the_data(blog_root: Path, blog) -> None:
    by_name = {m["name"]: m for m in blog.call("list_models", limit=200)["items"]}
    for kind in KINDS:
        assert by_name[kind]["model_ref"] == f"specir.models.domain:{kind}", by_name[kind]
    # SLDB's own models are registered as SLDB's, not as copies.
    for name in ("RuleDoc", "ViewDoc", "RelationDoc", "RelationTypeDoc"):
        assert by_name[name]["model_ref"].startswith("sldb."), by_name[name]
    types = {d["name"] for d in yaml.safe_load((DATA / "relation_types.yaml").read_text(encoding="utf-8"))}
    assert types == {"triggers", "invokes", "handled_by", "executes", "governed_by", "transitions", "writes", "persisted_in", "bound_to", "field_of", "accepted_by", "depends_on"}
    declared = {t["name"] for t in blog.call("list_relation_types", limit=200)["items"]}
    assert types <= declared, types - declared
    rules = {d["name"] for d in yaml.safe_load((DATA / "rules.yaml").read_text(encoding="utf-8"))}
    stored = {r["name"] for r in blog.call("select_documents", model="RuleDoc", limit=200)["items"]}
    assert rules == stored


def test_install_is_idempotent(blog_root: Path, blog) -> None:
    again = json.loads(install(blog_root).stdout)
    assert again["registered"] == [] and again["created"] == [] and again["rewritten"] == [] and again["conflicts"] == [], again
    assert len(again["present"]) == 23


def node(**fields) -> dict:
    return {"title": "Post", "origen": "declarado", **fields}


def test_a_node_declares_its_origen_from_the_decided_taxonomy() -> None:
    assert models.DomainEntityDoc(**node()).verificacion == "sin_verificar"
    with pytest.raises(ValidationError):
        models.DomainEntityDoc(title="Post")
    with pytest.raises(ValidationError):
        models.DomainEntityDoc(**node(origen="validado"))


def test_verified_names_who_verified_and_with_what() -> None:
    assert models.DomainEntityDoc(**node(verificacion="verificado", verificado_por="human:jp", evidencia="tests/models/test_blog_chain.py")).verificado_por == "human:jp"
    assert models.DomainEntityDoc(**node(verificacion="verificado", verificado_por="check:django-extractor", evidencia="code:blog/models.py::Post"))
    for wrong in ({"verificado_por": "agent:x", "evidencia": "e"}, {"verificado_por": "human:jp"}, {"evidencia": "e"}):
        with pytest.raises(ValidationError, match="verificado"):
            models.DomainEntityDoc(**node(verificacion="verificado", **wrong))


def test_an_unknown_value_is_null_and_named() -> None:
    assert models.HandlerDoc(**node(symbol=None, desconocidos={"symbol": "the extractor does not see it"})).symbol is None
    with pytest.raises(ValidationError, match="has a value"):
        models.HandlerDoc(**node(symbol="blog.views.publish", desconocidos={"symbol": "x"}))
    with pytest.raises(ValidationError, match="not a field"):
        models.HandlerDoc(**node(desconocidos={"permissions": "x"}))
