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

from pydantic import Field, field_validator
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
    __references__ = ["nodes", "notation"]
    __template__ = """---
id: ⸢rev•id⸥
diagram_type: ⸢rev•diagram_type⸥
version: ⸢rev•version⸥
spec_path: ⸢rev•spec_path⸥
sha256: ⸢rev•sha256⸥
notation: ⸢optrev•notation⸥
category: ⸢optrev•category⸥
nav: ⸢optrev•nav⸥
summary: ⸢optrev•summary⸥
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
    notation: str = Field(
        default="",
        description="Id `NotationDoc:<name>` de la notacion con la que se dibuja el spec; vacio si no se asigno ninguna.",
    )
    category: str = Field(default="", description="Categoria del catalogo (`category` de vistas.yml); graph_ui agrupa los specs por ella.")
    nav: str = Field(default="", description="Rotulo corto de navegacion del catalogo (`nav` de vistas.yml).")
    summary: str = Field(default="", description="Resumen del catalogo (`desc` de vistas.yml).")
    description: str = Field(default="", description="Descripcion del spec (`metadata.description` del YAML).")

    @field_validator("notation", "category", "nav", "summary", mode="before")
    @classmethod
    def _absent_text(cls, value):
        # un documento escrito antes de que el campo existiera se extrae como None
        return "" if value is None else value


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
collection: ⸢optrev•collection⸥
refs: ⸢rev,list•refs⸥
atom_refs: ⸢rev,list•atom_refs⸥
contains: ⸢rev,list•contains⸥
data: ⸢optrev•data⸥
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
    collection: str = Field(default="", description="Coleccion del spec de la que sale el elemento (nodes, artifacts, states, steps, participants, classes, components, stages).")
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
    data: dict = Field(
        default_factory=dict,
        description="El resto del elemento tal como esta en el spec (attributes, methods, guard, initial...); los compartimentos de un GlyphDoc leen de aqui.",
    )
    description: str = Field(default="", description="Texto libre del elemento, si el spec lo trae.")

    @field_validator("data", mode="before")
    @classmethod
    def _absent_data(cls, value):
        return {} if value is None else value

    @field_validator("collection", mode="before")
    @classmethod
    def _absent_collection(cls, value):
        return "" if value is None else value


# --- vocabulario visual -------------------------------------------------------------------
#
# Una notacion dice como se dibuja un spec: un GlyphDoc por clase de elemento (un modelo del
# store mas un predicado `where`) y un LinkDoc por relacion. Son datos del store, no tablas
# en los renderers: graph_ui los lee para dibujar en vivo y spec2viz los valida y escribe.
# Los campos `ref` son planos (`model`, `where`, `relation`); `form` guarda la forma pron
# equivalente para quien la interprete, spec2viz no lo hace.


class NotationDoc(StructuredNLDoc):
    """Una notacion: nivel, tipo de diagrama, layout y los glifos y links que la componen."""

    __semantics__ = {
        "type": ["notation", "vocabulary"],
        "layer": ["presentation"],
        "system": ["spec2viz"],
    }
    __references__ = ["glyphs", "links"]
    __template__ = """---
id: ⸢rev•id⸥
name: ⸢rev•name⸥
diagram_type: ⸢rev•diagram_type⸥
level: ⸢rev•level⸥
projection: ⸢rev•projection⸥
layout: ⸢rev•layout⸥
markers: ⸢rev•markers⸥
glyphs: ⸢rev,list•glyphs⸥
links: ⸢rev,list•links⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="Nombre de la notacion; nombre del documento (`NotationDoc:<name>`).")
    title: str = Field(description="Titulo legible de la notacion.")
    name: str = Field(description="Nombre de la notacion, igual al id.")
    diagram_type: str = Field(description="Tipo de diagrama spec2viz al que aplica (class, state, component...).")
    level: str = Field(default="types", description="Nivel que dibuja: `types`, `instances` o `both`.")
    projection: str = Field(default="all", description="Proyeccion del store sobre la que se dibuja; `all` sin filtro.")
    layout: dict = Field(default_factory=dict, description="Layout de la vista: `kind` (graph, tree, lanes, grid, axis) y sus parametros (direction...).")
    markers: list[dict] = Field(
        default_factory=list,
        description="Marcas que apuntan a un elemento sin ser su glifo (el pseudoestado inicial): `id`, `shape`, `model`, `where`.",
    )
    glyphs: list[str] = Field(default_factory=list, description="Ids `GlyphDoc:<notation>.<glyph>` en orden de prioridad: el primero que casa gana.")
    links: list[str] = Field(default_factory=list, description="Ids `LinkDoc:<notation>.<link>`.")
    description: str = Field(default="", description="Que dibuja la notacion y sobre que mundo.")


class GlyphDoc(StructuredNLDoc):
    """Como se ve un documento: un modelo (y un predicado) -> forma, rotulo, compartimentos."""

    __semantics__ = {
        "type": ["notation", "glyph"],
        "layer": ["presentation"],
        "system": ["spec2viz"],
    }
    __references__ = ["notation"]
    __template__ = """---
id: ⸢rev•id⸥
notation: ⸢optrev•notation⸥
model: ⸢rev•model⸥
where: ⸢rev•where⸥
shape: ⸢rev•shape⸥
label: ⸢rev•label⸥
label_style: ⸢rev•label_style⸥
keyword: ⸢rev•keyword⸥
compartments: ⸢rev,list•compartments⸥
function: ⸢rev•function⸥
form: ⸢rev•form⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="`<notation>.<glyph>`; nombre del documento.")
    title: str = Field(description="Nombre legible del glifo.")
    notation: str = Field(description="Id `NotationDoc:<name>` de la notacion a la que pertenece.")
    model: str = Field(description="Modelo del store cuyos documentos dibuja (SpecNodeDoc, ClassDoc...).")
    where: str = Field(default="", description="Predicado sobre el payload, en la gramatica de `sldb find --where`; vacio casa con todo.")
    shape: str = Field(description="Forma primitiva de la superficie (class-box, rounded-box, rounded-container, bullseye...).")
    label: str = Field(default="{title}", description="Plantilla del rotulo; `{campo}` lee del payload del documento.")
    label_style: str = Field(default="", description="Estilo del rotulo (italic, bold) o vacio.")
    keyword: str = Field(default="", description="Estereotipo o palabra clave encima del rotulo (`«interface»`).")
    compartments: list[str] = Field(default_factory=list, description="Campos del payload que se muestran como compartimentos, en orden (`data.attributes`).")
    function: str = Field(default="", description="Papel semantico del glifo en la notacion (class, interface, state, terminal).")
    form: str = Field(default="", description="Forma pron equivalente al par model/where, si alguien la interpreta; spec2viz no.")
    description: str = Field(default="", description="Texto libre.")


class LinkDoc(StructuredNLDoc):
    """Como se ve una relacion: linea, anidamiento, carril, celda o eje, con trazo y terminales."""

    __semantics__ = {
        "type": ["notation", "link"],
        "layer": ["presentation"],
        "system": ["spec2viz"],
    }
    __references__ = ["notation", "relation_type"]
    __template__ = """---
id: ⸢rev•id⸥
notation: ⸢optrev•notation⸥
relation: ⸢rev•relation⸥
relation_type: ⸢rev•relation_type⸥
model: ⸢rev•model⸥
draw: ⸢rev•draw⸥
line: ⸢rev•line⸥
source_end: ⸢rev•source_end⸥
target_end: ⸢rev•target_end⸥
label: ⸢rev•label⸥
ends: ⸢rev•ends⸥
form: ⸢rev•form⸥
---

# ⸢rev•title⸥

## Description

⸢rev,markdown•description⸥
""".strip()

    id: str = Field(description="`<notation>.<link>`; nombre del documento.")
    title: str = Field(description="Nombre legible del link.")
    notation: str = Field(description="Id `NotationDoc:<name>` de la notacion a la que pertenece.")
    relation: str = Field(description="Nombre de la relacion del store que dibuja (`relation_type` de los RelationDoc).")
    relation_type: str = Field(description="Id `RelationTypeDoc:reltype-<relation>`; el indice lo convierte en arista hacia el tipo de relacion.")
    model: str = Field(default="", description="Modelo de la relacion reificada (un documento con extremos), si la hay; vacio si es una arista.")
    draw: str = Field(default="line", description="Como se dibuja: `line`, `nest`, `lane`, `cell` o `axis`.")
    line: str = Field(default="solid", description="Trazo de la linea: `solid`, `dashed`, `dotted`.")
    source_end: str = Field(default="none", description="Terminal en el origen (none, open-arrow, filled-arrow, hollow-triangle, hollow-diamond, filled-diamond, filled-circle, bar).")
    target_end: str = Field(default="open-arrow", description="Terminal en el destino.")
    label: str = Field(default="", description="Plantilla del rotulo sobre el payload del RelationDoc (`{notes}`).")
    ends: dict = Field(default_factory=dict, description="Extremos de una relacion reificada: nombre -> {relation, label, terminal}.")
    form: str = Field(default="", description="Forma pron equivalente (`(relation R)`), si alguien la interpreta; spec2viz no.")
    description: str = Field(default="", description="Texto libre.")


__all__ = ["SpecDoc", "SpecNodeDoc", "NotationDoc", "GlyphDoc", "LinkDoc"]
