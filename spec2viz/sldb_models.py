"""Modelos sldb con los que spec2viz materializa un spec de diagrama como documentos del store.

Un spec es un namespace sobre la documentacion: sus elementos pasan a ser documentos
(`SpecNodeDoc`), sus aristas `RelationDoc` del store, y el spec mismo un `SpecDoc` que
contiene a sus nodos. Con eso cualquier documento del store (un atomo, un simbolo de
codigo, una tarea) puede colgarse de un nodo del diagrama, y el grafo de sldb une las
dos direcciones: `refs:`/`atoms:` del spec salen como aristas `references` (el indice las
deriva de `__references__`), y `contains:` como aristas `contains` (`__containment__`).

sldb importa estos modelos por su referencia `spec2viz.sldb_models:SpecNodeDoc`, asi que
spec2viz tiene que estar instalado donde viva el store.
"""

from __future__ import annotations

from pydantic import Field
from sldb.models.structured_doc import StructuredNLDoc


class SpecDoc(StructuredNLDoc):
    """Un spec de diagrama spec2viz, como documento del store que contiene a sus nodos."""

    __semantics__ = {
        "type": ["architecture", "spec"],
        "layer": ["topology"],
        "system": ["spec2viz"],
    }
    # `references`, no `contains`: la relacion builtin `contains` es one_to_many y un nodo
    # anidado en otro ya tiene a ese otro como contenedor.
    __references__ = ["nodes"]
    __template__ = """---
id: ⸢rev•id⸥
diagram_type: ⸢rev•diagram_type⸥
version: ⸢rev•version⸥
spec_path: ⸢rev•spec_path⸥
sha256: ⸢rev•sha256⸥
nodes: ⸢rev,list•nodes⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="Id del spec (`id:` del YAML); nombre del documento.")
    title: str = Field(description="Titulo del spec, mostrado como H1.")
    diagram_type: str = Field(description="Tipo de diagrama del spec (component, sequence, state...).")
    version: str = Field(description="Version declarada en el spec.")
    spec_path: str = Field(description="Ruta del YAML relativa a la raiz del proyecto del store.")
    sha256: str = Field(description="SHA-256 del YAML en el momento de la sincronizacion.")
    nodes: list[str] = Field(
        default_factory=list,
        description="Ids `SpecNodeDoc:<spec>.<elemento>` de los nodos del spec; el indice los convierte en aristas `references`.",
    )
    description: str = Field(default="", description="Descripcion del spec (`metadata.description` del YAML).")


class SpecNodeDoc(StructuredNLDoc):
    """Un elemento de un spec de diagrama (nodo, estado, paso, clase, participante) como documento."""

    __semantics__ = {
        "type": ["architecture", "spec", "node"],
        "layer": ["topology"],
        "system": ["spec2viz"],
    }
    __references__ = ["spec", "refs", "atom_refs"]
    __containment__ = {"contains": ["SpecNodeDoc"]}
    __template__ = """---
id: ⸢rev•id⸥
spec: ⸢rev•spec⸥
element: ⸢rev•element⸥
kind: ⸢rev•kind⸥
refs: ⸢rev,list•refs⸥
atom_refs: ⸢rev,list•atom_refs⸥
contains: ⸢rev,list•contains⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="`<spec id>.<element id>`; nombre del documento.")
    title: str = Field(description="Etiqueta del elemento en el diagrama (o su id si no tiene).")
    spec: str = Field(description="Id `SpecDoc:<spec id>` del spec al que pertenece el elemento.")
    element: str = Field(description="Id del elemento dentro del spec.")
    kind: str = Field(default="", description="`kind` del elemento en el spec, si lo declara.")
    refs: list[str] = Field(
        default_factory=list,
        description="`refs:` del elemento: ids `Model:name` (o `store:Model:name`) de documentos que el nodo apunta.",
    )
    atom_refs: list[str] = Field(
        default_factory=list,
        description="`atoms:` del elemento, como ids `AtomDoc:<atom id>`.",
    )
    contains: list[str] = Field(
        default_factory=list,
        description="Ids `SpecNodeDoc:<spec>.<elemento>` de los elementos anidados (`contains:` del spec).",
    )
    description: str = Field(default="", description="Texto libre del elemento, si el spec lo trae.")


__all__ = ["SpecDoc", "SpecNodeDoc"]
