"""Install specIR's domain types in an SLDB store: a thin adapter over SLDB's own mechanisms.

- The model classes (`specir.models.domain`) are registered by SLDB's model registry,
  `sldb.api.add_model`, as deskops registers its own (`deskops.bootstrap`); a model the store
  already has is left as it is.
- SLDB's relation models (`init_relations`), `RuleDoc` and `ViewDoc` are registered when the
  store lacks them, as deskops does for `RuleDoc` (`deskops.lifecycle.ensure_rule_model`).
- The relation types and rules specIR distributes (`specir/data/*.yaml`) are SLDB document
  seeds, written and tracked by `sldb.api.scaffold_store` in `managed` mode, the mechanism
  deskops uses for its lifecycle graph: a store's copy that differs is restored and reported.

Nothing here validates, renders or tracks a document: SLDB does. Running it twice changes
nothing the second time.

    python -m specir.install --store PATH/.sldb
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, field
from importlib import resources
from pathlib import Path
from typing import Any

import sldb.api as api
import yaml

from specir.models.domain import DOMAIN_MODELS

#: Where the seeds land in the store's project, relative to its root.
RELATION_TYPES_DIR = "specir/relation-types"
RULES_DIR = "specir/rules"

#: SLDB's own models specIR's data needs, by name and model ref.
SLDB_MODELS = {
    "RuleDoc": "sldb.models.rule_doc:RuleDoc",
    "ViewDoc": "sldb.models.notation_models:ViewDoc",
}


def package_pythonpath() -> str:
    """The directory `specir` is imported from: what SLDB needs to import the model classes."""
    return str(Path(__file__).resolve().parents[1])


def model_ref(model: type) -> str:
    return f"{model.__module__}:{model.__name__}"


def _data(name: str) -> list[dict[str, Any]]:
    return yaml.safe_load(resources.files("specir").joinpath("data", name).read_text(encoding="utf-8"))


def relation_type_seeds() -> list[api.Seed]:
    """One managed document seed per relation type of `relation_types.yaml`."""
    seeds = []
    for spec in _data("relation_types.yaml"):
        payload = {"direction": "directed", "condition": "", **spec}
        name = f"type-{spec['name']}"
        seeds.append(api.Seed(path=f"{RELATION_TYPES_DIR}/{name}.md", mode="managed", document={"model": "RelationTypeDoc", "name": name, "payload": payload}, track=True))
    return seeds


def rule_seeds() -> list[api.Seed]:
    """One managed document seed per rule of `rules.yaml`."""
    seeds = []
    for spec in _data("rules.yaml"):
        name = spec["name"]
        payload = {"where": "", "message": "", **{k: v for k, v in spec.items() if k != "name"}}
        seeds.append(api.Seed(path=f"{RULES_DIR}/{name}.md", mode="managed", document={"model": "RuleDoc", "name": name, "payload": payload}, track=True))
    return seeds


@dataclass
class InstallReport:
    store: str
    registered: list[str] = field(default_factory=list)
    created: list[str] = field(default_factory=list)
    rewritten: list[str] = field(default_factory=list)
    present: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)


def install(store: str | Path) -> InstallReport:
    """Register specIR's models and SLDB's models it needs, and seed its relation types and rules."""
    location = api.open_store(Path(store))
    store_path, pythonpath = location.store_path, package_pythonpath()
    report = InstallReport(store=str(store_path))
    for model in DOMAIN_MODELS:
        if not api.is_model_registered(store_path, model.__name__):
            api.add_model(store_path, model_ref(model), pythonpath=pythonpath)
            report.registered.append(model.__name__)
    if not all(api.is_model_registered(store_path, name) for name in ("RelationDoc", "RelationTypeDoc")):
        api.init_relations(store_path, pythonpath=pythonpath)
        report.registered += ["RelationDoc", "RelationTypeDoc"]
    for name, ref in SLDB_MODELS.items():
        if not api.is_model_registered(store_path, name):
            api.add_model(store_path, ref, pythonpath=pythonpath)
            report.registered.append(name)
    declaration = api.StoreDeclaration(seeds=[*relation_type_seeds(), *rule_seeds()])
    scaffold = api.scaffold_store(store_path, declaration=declaration, apply=True)
    if scaffold.rewritten:
        # SLDB's scaffold writes a restored file without rehashing it (as deskops.workspace notes).
        api.update_store_indexes(store_path, pythonpath)
    report.created, report.rewritten, report.present, report.conflicts = (list(scaffold.created), list(scaffold.rewritten), list(scaffold.present), list(scaffold.conflicts))
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="specir-install", description="Install specIR's domain models, relation types and rules in an SLDB store.")
    parser.add_argument("--store", required=True, help="The store (its .sldb directory or its project).")
    args = parser.parse_args(argv)
    report = install(args.store)
    print(json.dumps(asdict(report), indent=2, ensure_ascii=False))
    return 1 if report.conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
