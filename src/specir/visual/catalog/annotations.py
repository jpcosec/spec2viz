"""The annotations of an HTML catalog, kept in an sldb store and saved through `sldb serve`
(replaces spec2viz's `catalog serve`, which wrote them to a JSON file next to the page).

specIR runs no server: the catalog page talks to `sldb serve --cors` with the two routes D4
checked, `GET /document?id=` to read the annotations and `POST /save` to write them, with the
payload read as the optimistic guard (`changes[].expected`; 409 when someone else changed it).
What stays here is visual: the model of the document that holds a catalog's annotations
(`CatalogAnnotationsDoc`, registered in the store with sldb's `add_model`) and the page's script
(`templates/annotations-sldb.js`), which the build embeds when an annotations target is given.
Without one, the page keeps its annotations in the browser (`localStorage`), as before."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

import sldb.api as api
from pydantic import Field
from sldb.api import StructuredNLDoc

SCRIPT = "annotations-sldb.js"
MODEL_NAME = "CatalogAnnotationsDoc"


class CatalogAnnotationsDoc(StructuredNLDoc):
    """The annotations of one HTML catalog: one comment per diagram element of a view."""

    __authority__ = "authored"
    __semantics__ = {"type": ["specir", "catalog", "annotations"], "layer": ["visual"]}
    __template__ = """---
catalog: ⸢rev•catalog⸥
annotations: ⸢rev,list•annotations⸥
---
# ⸢rev•title⸥
""".strip()

    title: str = Field(description="The catalog's title, shown as the H1 heading.")
    catalog: str = Field(default="", description="The catalog these annotations belong to (its project name).")
    annotations: list[dict] = Field(
        default_factory=list,
        description="One entry per comment, as the catalog page writes it: key (`<view anchor>::<label>`), vista, label, comentario and ts.",
    )


def model_ref() -> str:
    return f"{CatalogAnnotationsDoc.__module__}:{CatalogAnnotationsDoc.__name__}"


def package_pythonpath() -> str:
    """The directory `specir` is imported from: what sldb needs to import the model."""
    return str(Path(__file__).resolve().parents[3])


def register_annotations_model(store: Path) -> None:
    """Registers `CatalogAnnotationsDoc` in the store (sldb's model registry); twice changes nothing."""
    if not api.is_model_registered(store, MODEL_NAME):
        api.add_model(store, model_ref(), pythonpath=package_pythonpath())


def annotations_id(catalog_name: str) -> str:
    """The id of a catalog's annotations document: what `sldb serve` accepts as a new id."""
    token = re.sub(r"[^a-zA-Z0-9_-]+", "-", catalog_name).strip("-_") or "catalog"
    return f"catalog-annotations-{token}"[:160]


@dataclass(frozen=True)
class AnnotationsTarget:
    """Where a catalog page saves its annotations: the base URL of `sldb serve` and the document id.
    The page also reads both from its URL (`?sldb=<url>&annotations=<id>`), which win."""

    server: str = ""
    doc: str = ""


def annotations_script(target: AnnotationsTarget, title: str, catalog: str) -> str:
    """The `<script>` that makes the page read and save its annotations with `sldb serve`."""
    config = {"server": target.server, "doc": target.doc or annotations_id(catalog or title), "model": MODEL_NAME, "title": title, "catalog": catalog}
    code = resources.files("specir.visual").joinpath("templates", SCRIPT).read_text(encoding="utf-8")
    return f"\n<script>\nwindow.SPECIR_ANNOTATIONS = {json.dumps(config)};\n{code}\n</script>\n"


__all__ = [
    "AnnotationsTarget", "CatalogAnnotationsDoc", "annotations_id", "annotations_script", "model_ref", "package_pythonpath",
    "register_annotations_model",
]
