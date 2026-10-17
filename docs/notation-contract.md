# Contrato de lectura de la notación

Cómo una superficie (graph_ui, o cualquier otra) dibuja un spec de spec2viz leyendo solo el store
sldb. spec2viz escribe estos documentos con `spec2viz diagram sync` y `spec2viz notation sync`;
nunca escribe posiciones ni estado de vista. Lo que diga este documento manda sobre lo que
infiera una superficie del payload.

**El contrato tiene un solo intérprete**: `spec2viz.notation_view.resolve_view(store, "SpecDoc:<id>")`
(CLI: `spec2viz notation view <id> --store .sldb`). Aplica §2 a §6 con `sldb.api.where_matches` y
devuelve JSON listo para dibujar (§10). Una superficie sirve ese resultado (por ejemplo como
`/api/notation/view?spec=`) y dibuja; no reimplementa `where`, las plantillas ni la prioridad de los
glifos. Las secciones §2 a §7 describen lo que hace el resolver, para leerlo y para discutirlo.

## 1. Qué hay en el store

| Documento | Nombre | Lo escribe | Dice |
|---|---|---|---|
| `SpecDoc:<spec>` | `id:` del YAML | `diagram sync` | el spec: `diagram_type`, `notation`, `nodes`, `spec_path`, `sha256` |
| `SpecNodeDoc:<spec>.<elemento>` | id del elemento | `diagram sync` | un elemento: `title`, `kind`, `refs`, `atom_refs`, `contains`, `data`, `description` |
| `RelationDoc:<spec>.<from>__<rel>__<to>` | | `diagram sync` | una arista del spec: `source_id`, `target_id`, `relation_type` (nombre), `notes` |
| `RelationTypeDoc:reltype-<rel>` | `reltype-<rel>` | ambos | el tipo de relación: `name`, `direction`, `cardinality` |
| `NotationDoc:<name>` | nombre de la notación | `notation sync` | nivel, tipo de diagrama, `layout`, `markers`, `glyphs`, `links` |
| `GlyphDoc:<name>.<glyph>` | | `notation sync` | cómo se ve un documento |
| `LinkDoc:<name>.<link>` | | `notation sync` | cómo se ve una relación |

Los ficheros están en `<raíz>/docs/.../sldb/<spec>/` (specs), `<raíz>/sldb/notations/<name>/`
(notaciones) y `<raíz>/sldb/relation_types/` (tipos). Los modelos Pydantic están en
`spec2viz.sldb_models`; el store los importa por esa referencia, así que spec2viz tiene que estar
instalado donde se lea el store.

## 2. Resolver la notación de un spec

1. Leer `SpecDoc.notation`. Es `NotationDoc:<name>` o vacío. Vacío significa que el tipo de diagrama
   no tiene notación builtin ni se le asignó una: la superficie dibuja como sabe (cajas y flechas) o
   no ofrece la vista.
2. Cargar ese `NotationDoc`. `diagram_type` tiene que coincidir con `SpecDoc.diagram_type`; si no,
   es un error de datos, no algo que la superficie deba arreglar.
3. Cargar sus `glyphs` y `links` en el orden en que los lista. El orden de `glyphs` es prioridad.

En el índice de aristas todo esto son aristas `references` (`SpecDoc -> NotationDoc`,
`NotationDoc -> GlyphDoc|LinkDoc`, `GlyphDoc|LinkDoc -> NotationDoc`, `LinkDoc ->
sldb://relation_type/<rel>`), así que `sldb graph neighborhood NotationDoc:uml-class` lo recorre.

## 3. Qué documentos entran en la vista

Los `SpecNodeDoc` listados en `SpecDoc.nodes`, y los `RelationDoc` cuyo `source_id` y `target_id`
están ambos en esa lista. Nada más: un documento que apunte a un nodo del spec (un átomo, una
tarea) es contexto del nodo, no un elemento del diagrama. `NotationDoc.projection` vale `all` hoy;
cuando valga otra cosa será el nombre de una proyección del store que recorta esa lista.

`NotationDoc.level` dice qué nivel representa la vista (`types`, `instances`, `both`). Los specs de
spec2viz son siempre de tipos; `both` en `statechart` deja sitio para marcar el estado actual de una
instancia, que spec2viz no escribe.

## 4. Casar un glifo con un documento

Para cada `SpecNodeDoc`, recorrer `NotationDoc.glyphs` en orden y quedarse con el primero tal que:

- `GlyphDoc.model` es el modelo del documento (`SpecNodeDoc`), y
- `GlyphDoc.where` está vacío o se cumple sobre el **payload aplanado** del documento.

El payload aplanado es el payload del `SpecNodeDoc` con las claves de `data` copiadas al nivel
superior (`data` no pisa `id`, `title`, `kind`, `refs`, `atom_refs`, `contains`, `description`:
`diagram sync` deja fuera de `data` exactamente esas claves). La gramática de `where` es la de
`sldb find --where`: `kind = "interface"`, `nonempty(contains)`, `has(initial)`, predicados unidos
por ` and `. La gramática no tiene rutas con punto; por eso `where` se evalúa sobre el aplanado.
`sldb.api.where_matches(expr, payload)` la evalúa.

Dos vistas del payload, según el campo:

| Campo | Se evalúa sobre | Ejemplo |
|---|---|---|
| `where` (glifos y marcas) | el payload aplanado | `has(initial)`, `kind = "enum"` |
| `compartments` | el payload crudo, rutas con punto | `data.attributes` |
| `label` | `{campo}` sobre el aplanado; `{a.b}` con punto sobre el crudo | `{title}`, `{data.entity}` |

El último glifo de cada modelo no tiene `where` y es el glifo por defecto; `notation validate` lo
exige, así que siempre hay un glifo. Qué significa cada campo del glifo:

| Campo | Significado |
|---|---|
| `shape` | primitiva de la superficie: `class-box`, `rounded-box`, `rounded-container`, `bullseye`, `filled-circle`... |
| `label` | plantilla; `{campo}` se sustituye por el valor del payload (ver tabla); un campo ausente, nulo, lista o dict queda vacío; no hay escape de llaves, una llave literal no cabe en un rótulo; el resultado se recorta de espacios |
| `label_style` | `italic`, `bold` o vacío |
| `keyword` | texto encima del rótulo (`«interface»`) |
| `compartments` | lista de rutas con punto sobre el payload crudo (`data.attributes`, `data.methods`), un compartimento cada una, en orden; una ruta ausente o vacía no aparece en la vista |
| `function` | papel semántico (`class`, `interface`, `state`, `terminal`); para agrupar o colorear, nunca para decidir la forma |
| `form` | la forma pron equivalente; informativa |

Cómo se dibuja el contenido de un compartimento lo decide la superficie a partir de lo que haya en
esa ruta: una lista de dicts con `name` y `type` (los `attributes` y `methods` de un spec de clases)
se lista línea a línea.

## 5. Casar un link con una relación

Para cada `RelationDoc` de la vista, el `LinkDoc` de la notación con `relation ==
RelationDoc.relation_type`. Una relación sin link no se dibuja y el resolver la lista en `skipped`.
Además, cada id de `SpecNodeDoc.contains` que esté en la vista casa con el link cuya `relation` es
`contains`. La fuente canónica de la contención es ese campo del payload; las aristas `contains`
del índice de sldb se derivan de él y dicen lo mismo. Un link de contención no tiene `RelationDoc`
(`doc: null` en la vista).

| `draw` | Qué hacer con la pareja origen → destino |
|---|---|
| `line` | una línea entre los dos glifos, con `line` (solid, dashed, dotted), `source_end` y `target_end` como terminales y `label` como rótulo |
| `nest` | el destino se dibuja dentro del origen; no hay línea. Es como `statechart` dibuja `contains` |
| `lane` | el destino se coloca en el carril del origen (diagramas con calles); sin línea |
| `cell` | la pareja es una celda de una matriz origen × destino |
| `axis` | la pareja fija la posición del destino sobre un eje del origen |

Terminales: `none`, `open-arrow`, `filled-arrow`, `hollow-triangle`, `filled-triangle`,
`hollow-diamond`, `filled-diamond`, `filled-circle`, `hollow-circle`, `bar`, `crowfoot`. `label` es una
plantilla sobre el payload del `RelationDoc` (`{notes}`). Un link con `model` y `ends` es una relación
reificada (un documento con extremos); spec2viz no emite ninguna hoy, el campo existe para
notaciones externas.

La dirección es siempre `source_id → target_id` del `RelationDoc`; `RelationTypeDoc.direction`
`undirected` dice que la superficie puede omitir la punta.

## 6. Marcas

`NotationDoc.markers` son símbolos que apuntan a un documento sin reemplazar su glifo:
`{id, shape, model, where}`. Se casan como un glifo (modelo + `where` sobre el payload aplanado)
y se dibujan junto al glifo del documento, con una línea corta hacia él. `statechart` lo usa para el
pseudoestado inicial: `has(initial)`, porque `diagram sync` pone `data.initial: true` solo en el
estado inicial.

## 7. Layout y vista

`NotationDoc.layout` es `{kind, ...}`: `graph` (dirigido, con `direction` TB|LR|BT|RL), `tree`,
`lanes`, `grid`, `axis`, `manual`. Es la sugerencia de la notación; la superficie elige el algoritmo.
Posiciones, plegado y selección son estado de la superficie y no se escriben en el store de spec2viz
ni en el YAML del spec.

## 8. Lo que cambia y lo que no

- Una superficie no debe leer `kind` para decidir una forma: eso lo dice el `GlyphDoc`. Si una
  notación necesita algo que no cabe en estos campos, se añade al modelo en spec2viz, no un `if` en
  la superficie.
- Añadir una notación es un YAML (`spec2viz notation validate` lo comprueba) y `notation sync`; no
  hace falta tocar código en ninguno de los dos lados.
- Lo que hoy no viaja: las multiplicidades y roles de una relación de clases (solo `notes` lleva la
  etiqueta), las acciones de una transición (solo evento y guarda en `notes`). Cuando haga falta, la
  salida es un `RelationDoc` con más campos o una relación reificada, no un parseo de `notes`.

## 9. Alcance de la primera vista de graph_ui

Acordado el 2026-10-17 con graph_ui: `layout.kind` `graph` (TB y LR) y `draw` `line` y `nest`. Una
notación que pida `lane`, `cell`, `axis`, `tree` o `grid` se dibuja como `line`/`graph` con aviso.
Lo caro del layout es un statechart con `nest` y transiciones que cruzan el contenedor. El shell de
graph_ui carga `/api/schema` al arrancar, así que el store tiene que ser legible por todos sus
modelos registrados (en spec2viz: migrar el desk con `deskops desk update --apply`).

## 10. Pilotos

`docs/architecture/spec2viz/class-sldb-models.yml` (notación `uml-class`),
`docs/architecture/spec2viz/state-diagram-type-lifecycle.yml` (notación `statechart`, sin compuestos) y
`docs/architecture/spec2viz/state-diagram-sync-lifecycle.yml` (`statechart` con un estado compuesto, tres
`nest` y una transición que cruza el borde del contenedor; `tests/test_notation_view.py` fija su vista), sincronizados
en el store del repo (`.sldb`). Con graph_ui:

```
SLDB_STORE=/home/jp/proyectos/SLDB_1/spec2viz/.sldb python3 frontends/mindmap/serve.py 8099
```

`/api/graph` lista los `SpecDoc`, `SpecNodeDoc`, `RelationDoc`, `NotationDoc`, `GlyphDoc` y
`LinkDoc`; la vista genérica que los interprete es trabajo de graph_ui.

## 11. Lo que devuelve el resolver

```json
{
  "spec": "SpecDoc:class.sldb-models", "title": "...", "diagram_type": "class",
  "notation": "NotationDoc:uml-class", "level": "types", "layout": {"kind": "graph", "direction": "TB"},
  "nodes": [
    {"doc": "SpecNodeDoc:class.sldb-models.SpecDoc", "title": "SpecDoc", "kind": "",
     "glyph": "GlyphDoc:uml-class.class", "shape": "class-box", "function": "class",
     "label": "SpecDoc", "label_style": "", "keyword": "",
     "compartments": [{"path": "data.attributes", "items": [{"name": "id", "type": "str"}]}],
     "markers": [], "refs": []}
  ],
  "links": [
    {"source": "SpecNodeDoc:...SpecDoc", "target": "SpecNodeDoc:...StructuredNLDoc",
     "relation": "inheritance", "link": "LinkDoc:uml-class.inheritance",
     "doc": "RelationDoc:class.sldb-models.SpecDoc__inheritance__StructuredNLDoc",
     "draw": "line", "line": "solid", "source_end": "none", "target_end": "hollow-triangle", "label": ""}
  ],
  "skipped": []
}
```

`nodes` sigue el orden de `SpecDoc.nodes`; `links` lista primero las contenciones y después los
`RelationDoc`. `skipped` son relaciones del spec sin link en la notación. Un spec sin notación, una
notación de otro tipo de diagrama o un nodo sin glifo son errores (`ViewError`), no vistas a medias.
