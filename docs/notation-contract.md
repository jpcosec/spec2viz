# Contrato de lectura de la notación

spec2viz completo se muestra sobre graph_ui: cada tipo de diagrama tiene una notación builtin, cada
spec del catálogo se sincroniza al store con ella y con sus metadatos de catálogo, y graph_ui lista
y dibuja desde el store. El bundle HTML (`catalog build`) es un export estático de lo mismo.

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
| `SpecDoc:<spec>` | `id:` del YAML | `diagram sync` / `catalog sync` | el spec: `diagram_type`, `notation`, `nodes`, `spec_path`, `sha256`, y del catálogo `category`, `nav`, `summary` |
| `SpecNodeDoc:<spec>.<elemento>` | id del elemento | `diagram sync` | un elemento: `title`, `kind`, `collection`, `refs`, `atom_refs`, `contains`, `data`, `description` |
| `RelationDoc:<spec>.<nn>-<from>__<rel>__<to>` | | `diagram sync` | una arista del spec, con su posición `nn`: `source_id`, `target_id`, `relation_type` (nombre), `condition`, `notes` |
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

## 2b. El catálogo

`spec2viz catalog sync --config vistas.yml --store .sldb` sincroniza cada spec del registro con la
notación de su tipo y escribe en el `SpecDoc` la `category`, el `nav` y el `desc` del registro
(`summary`). El catálogo en graph_ui es la lista de `SpecDoc` agrupada por `category`, con `nav`
como rótulo corto y `summary` como descripción; abrir uno es resolver su vista. No hay otro
documento de catálogo.

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
RelationDoc.relation_type`; si no lo hay, el link comodín (`relation: "*"`), que dibuja cualquier
relación y suele rotularla con `{relation_type}`; su campo `relation_type` va vacío, porque no nombra
ningún tipo de relación. Una relación sin link ni comodín no se dibuja y
el resolver la lista en `skipped`. Los links salen en el orden del spec (`order`, de la posición
`nn` del nombre del `RelationDoc`; 0 para las contenciones); en una secuencia ese orden es el
tiempo.
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
- Lo que viaja en `RelationDoc.attributes` (§8d) y lo que no: los roles de una asociación de clases
  no existen en el spec de spec2viz; cuando hagan falta, la salida es una relación reificada, no un
  parseo de `notes`.

## 8b. Las notaciones builtin, por tipo de diagrama

| Tipo | Notación | Layout | Glifos (por `where`) | Links |
|---|---|---|---|---|
| class | `uml-class` | graph TB | interface, protocol, abstract, enum, record por `kind`; class por defecto; compartimentos `data.attributes`, `data.methods` | inheritance, realization, composition, aggregation, association, dependency (line) |
| state | `statechart` | graph LR | composite si `nonempty(contains)`; state; marca initial `has(initial)` | contains (nest), transitions_to (line, `{notes}` = evento [guarda]) |
| component | `component` | graph TB | boundary, entry por `kind`; component | contains (nest), `*` (line, `{relation_type} {notes}`) |
| deployment | `deployment` | graph LR | artifact si `collection = "artifacts"`; node; keyword `«{kind}»` | contains (nest), `*` (line sin puntas, `{relation_type}` = protocolo) |
| sequence | `uml-sequence` | lanes LR | actor, boundary por `kind`; participant | sends (filled-arrow), sends_async (open-arrow), returns (dashed); `order` es el tiempo; `condition` del mensaje |
| activity | `activity` | graph TB | start `has(initial)`, end `has(final)`, decision por `kind`; action | next (line), branch (line, `[{notes}]`) |
| component_view_matrix | `component-view-matrix` | grid | stage si `collection = "stages"` (columna, `data.view`, `data.order`); boundary; component (fila) | contains (nest = jerarquía de filas), occupies (cell, `{notes}` = vista) |
| reflection | `reflection` | graph LR | boundary por `kind`; node con keyword `«{kind}»` | `*` (line, `{relation_type} {notes}`) |

Cada nodo de la vista trae además `collection` y `data` (el resto del elemento), para lo que un
glifo no cubre (el `view` y `order` de una etapa, los `branches` de una decisión).

## 8c. Carriles y grilla: cómo se ordenan

Acordado con graph_ui el 2026-10-18.

**Carriles** (`layout.kind: lanes`, `uml-sequence`): un carril por nodo de la vista, en el orden de
`nodes` (el de `participants` del spec); todos son `collection = "participants"`. Cada mensaje es un
link `draw: line` con `order` 1..n, y ese `order` es su fila en el tiempo. Un retorno es `relation:
returns` con `line: dashed`; una autollamada tiene `source == target` y se dibuja como bucle sobre
su carril, ocupando su fila. `fragments` (§11) son los marcos: rachas de mensajes
consecutivos con el mismo `group` del spec. `kind` sale de la primera palabra del `group` si es un
operador UML (`alt`, `loop`, `opt`, `par`, `break`, `critical`, `neg`, `ref`, `seq`, `strict`) y
`label` es el resto (`"loop for each spec"` → kind `loop`, label `for each spec`); sin operador, kind
`group` y label el grupo entero. El marco va de la primera a la última fila de `orders` y de la
línea de vida más a la izquierda a la más a la derecha entre los mensajes que contiene, con la
pestaña del operador arriba a la izquierda y `label` junto a ella. Dos rachas del mismo `group`
separadas por otro mensaje son dos marcos. `draw: lane` no lo usa ninguna notación builtin: queda para
"el destino se coloca en el carril del origen" (calles), no para secuencias.

**Grilla** (`layout.kind: grid`, `component-view-matrix`): columnas = nodos `collection = "stages"`,
con `data.view` (id de la vista), `data.view_label` y `data.order` 1..n dentro de la vista; una
grilla por vista. Filas = nodos `collection = "components"` en el orden de `nodes`, jerarquía por los
links `draw: nest` (el hijo indentado bajo el padre). Cada `draw: cell` es source = fila, target =
columna, y `label` es el contenido de la celda. Una fila sin celdas en una vista queda vacía, no se
omite.

## 8d. Atributos de arista

`RelationDoc.attributes` (sldb >= 0.1.11, la dependencia declarada; `diagram sync` lo escribe siempre) guarda lo que un `RelationDoc` no tiene dónde poner: en clases `from_multiplicity`,
`to_multiplicity`, `label`; en statecharts `on`, `guard`, `action`; en secuencias `kind`, `group`,
`message`; en despliegue `protocol`; en actividad `branch`; en matrices `view`, `stage`. La vista lo
expone como `data` de cada link. Las plantillas de un `LinkDoc` (`label`, `source_label`,
`target_label`) leen el `RelationDoc` con sus `attributes` encima, igual que un glifo lee `data`:
`uml-class` rotula los extremos de composición, agregación y asociación con `{from_multiplicity}` y
`{to_multiplicity}`. La acción de una transición va además en `notes` como `evento [guarda] / acción`.

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
     "draw": "line", "line": "solid", "source_end": "none", "target_end": "hollow-triangle", "label": "",
     "order": 1, "condition": "", "data": {}, "source_label": "", "target_label": ""}
  ],
  "fragments": [{"label": "for each spec", "kind": "loop", "group": "loop for each spec", "orders": [3, 4]}],
  "skipped": []
}
```

`nodes` sigue el orden de `SpecDoc.nodes` y cada uno trae `element`, `collection` y `data`; `links`
lista primero las contenciones (`order` 0) y después los `RelationDoc` por `order`, con `condition`,
`data` (los `attributes` del RelationDoc) y los rótulos de extremo. `fragments` son las rachas de
links consecutivos con el mismo `data.group` (vacío si no hay grupos). `skipped` son relaciones del spec sin link en la notación. Un spec sin notación, una
notación de otro tipo de diagrama o un nodo sin glifo son errores (`ViewError`), no vistas a medias.

## 12. Vistas de la gramática de proyección: `ViewDoc`

Decisión del coordinador SLDB_1 (2026-10-19): las vistas son documentos del store y su modelo vive en
spec2viz junto a `NotationDoc` (`spec2viz.sldb_models.ViewDoc`). Campos: `id`/`name`, `title`, `nodes`
(unión de `{model, where}`; `where` en la gramática de `sldb find --where`; vacío = todos los documentos),
`relations` (tipos de relación; vacío = todos), `direction` (`both`, `outgoing`, `incoming`, como
`sldb.api.graph.RelationFilter`), `notation` (opcional, `NotationDoc:<name>`; su `layout` da el estilo),
`layout` (override de la misma forma) y `description`. Una vista es portable: nunca nombra ids de nodo ni
rutas de store. graph_ui la evalúa y la crea y guarda por sldb; spec2viz solo define y valida el modelo.

`layout` de `kind: graph` reconoce `direction` (TB, LR, BT, RL), `style` (`layered` o `rings`) y
`ring_field` (el campo del payload que asigna el anillo cuando `style: rings`).

## 13. Estilo: formas, paleta, colores e íconos (2026-10-19)

Todo es opcional: una notación que no usa estilo se escribe y se resuelve igual que antes (sin
`palette` en el NotationDoc, `style: {}` en cada nodo, `color: null` en cada link). Lo que spec2viz
resuelve llega aplicado en `resolve_view`; la superficie no recalcula precedencias ni contrastes.

**Formas builtin** (`spec2viz.notation.SHAPES`; `notation validate` rechaza cualquier otra con
`UnknownShapeError`): `artifact`, `boundary-box`, `boundary-lifeline`, `box`, `bullseye`,
`class-box`, `column-header`, `diamond`, `filled-circle`, `lifeline`, `node-box`, `rounded-box`,
`rounded-container`, `row-header`, `stick-figure` y las nuevas `cylinder` (bases y almacenamiento,
vertical), `queue` (cola: cilindro horizontal), `cloud` (servicio externo), `package` (la carpeta con
pestaña de UML) y `note` (nota UML con la esquina doblada).

**Campos opcionales.** `GlyphDoc`: `kind` (un kind de la paleta: aporta su ícono y sus colores),
`fill`, `stroke` e `icon` (nombre del set declarado). `LinkDoc`: `color`.

**Un color** (en `fill`, `stroke`, `color` y en `style.kinds` del spec) es una de tres formas:

- un token de la paleta (`database-fill`): ya trae un valor por tema;
- un hex `#rrggbb`: **el mismo valor en los dos temas** (útil para trazos que contrastan con ambos
  fondos; un relleno claro así queda ilegible en el tema oscuro);
- un par `{light: ..., dark: ...}`, cuyos lados son un hex o un token (del token se toma el valor
  de ese tema). Es la forma de dar un color propio que se lea en los dos temas.

El GlyphDoc y el LinkDoc guardan el valor tal como se escribió (texto o par); el resolver siempre
entrega `{light, dark}`. Un par con otras claves, o con un lado que no es hex ni token, es
`InvalidColorError`. `NotationDoc`: `palette` (`PaletteDoc:<name>`), presente solo si la
notación usa estilo; si usa estilo sin nombrar paleta, es `default`. `SpecDoc`: `style`, el
`style.kinds` neutral del spec (kind -> `fill`, `stroke`, `icon`).

**Paleta** (`PaletteDoc:<name>`, builtin `default` en `spec2viz/palettes/default.yml`, escrita por
`spec2viz palette sync` o por `notation sync` de una notación con estilo): `backgrounds` e `ink` por
tema (`{light, dark}`), `icon_set` (`{name: lucide, version: "0.577.0", icons: [...]}`: nombres de
[Lucide](https://lucide.dev) en kebab-case tal como los exporta `lucide-react` 0.577.0; nunca una
URL), `colors` (token -> `{light, dark}`) y `kinds` (kind -> `{shape, icon, fill, stroke}`). La
`default` cubre `database`, `queue`, `storage`, `gateway`, `auth`, `backend`, `frontend`, `client` y
`external`; `palette validate` exige trazo >= 3:1 contra el fondo de cada tema (WCAG 1.4.11), texto
(`ink`) >= 4.5:1 sobre cada relleno (AA) y un par (forma, ícono) distinto por kind, para que el tono
nunca sea la única señal.

**Precedencia, una sola fuente** (`spec2viz.styling.resolve_style`, la usan `resolve_view` y el
renderer de mermaid). Por propiedad (`fill`, `stroke`, `icon`) gana la primera capa que la define:

1. el glifo de la notación: sus `fill`/`stroke`/`icon` y, detrás, el kind de la paleta que nombra;
2. `style.kinds` del spec para el `kind` del elemento;
3. la paleta de la notación para el `kind` del elemento (solo si la notación usa paleta).

Un token sin paleta en la notación resuelve contra `default`. La forma del nodo es siempre la del
glifo; la de la paleta es la forma de referencia del kind (la leyenda la muestra).

**En la salida del resolver**: cada nodo trae `style`: `{fill: {light, dark}, stroke: {light, dark},
icon, source: {fill: "glyph"|"spec"|"palette", ...}}` con solo las propiedades que alguna capa
define (`{}` si ninguna); cada link trae `color` (`{light, dark}` o `null`); la vista trae `palette`
y `legend`:

```json
"legend": {
  "glyphs": [{"glyph": "GlyphDoc:infra.db", "title": "db", "shape": "cylinder", "function": "",
              "style": {"fill": {"light": "#dbebf4", "dark": "#092c42"}, "stroke": {...}, "icon": "database", "source": {...}}}],
  "links":  [{"link": "LinkDoc:infra.any", "title": "any", "relation": "*", "draw": "line", "line": "solid",
              "source_end": "none", "target_end": "open-arrow", "color": {"light": "#0072b2", "dark": "#0072b2"}}],
  "kinds":  [{"kind": "frontend", "shape": "box", "icon": "app-window", "fill": {...}, "stroke": {...}, "source": {...}}]
}
```

`legend.kinds` lista los kinds de la vista que reciben estilo del spec o de la paleta. El texto sobre
un relleno usa el `ink` del tema de la paleta.

**Resolver público para documentos de cualquier modelo**:
`spec2viz.notation_view.resolve_documents(store, notation_ref, doc_refs, *, relation_refs=None,
spec_style=None)` devuelve lo mismo que `resolve_view` sin los campos del spec (`notation`,
`palette`, `level`, `layout`, `nodes`, `links`, `fragments`, `skipped`, `legend`). Cada documento se
dibuja con el primer glifo de su modelo cuyo `where` casa; los links son los `contains` entre ellos y
los `RelationDoc` con los dos extremos en la vista (solo `relation_refs`, si se da). Para una
`ViewDoc`, graph_ui elige documentos y aristas y esta función aplica la notación.

**Los specs.** `style.kinds` de un spec acepta claves neutrales `fill`, `stroke` (token de `default`
o `#rrggbb`) e `icon`; el validador las comprueba (`InvalidColorError`, `UnknownIconError`). Mermaid
las dibuja como `classDef` + `class` en component, activity y deployment; un bloque por renderer
(`plantuml: {background, border, font}`) sigue siendo solo de ese renderer.

## 14. Activity y deployment (2026-10-19)

**Activity.** Cada paso puede llevar `partition` (carril UML; viaja como `data.partition` del
SpecNodeDoc: la superficie dibuja un carril por partición, en orden de aparición) y `notes` (nota
UML, `data.notes`: una forma `note` unida a su paso por una línea punteada). `kind: merge` se dibuja
como rombo sin rótulo (glifo `activity.merge`). El paso de `start:` conserva su glifo (acción o
decisión): el nodo inicial es el pseudonodo propio `<spec>.__initial` (glifo `activity.start`) con un
`next` hacia él. El final es `end` mismo cuando no es un paso (`end: end`) o, si `end` nombra un
paso, el pseudonodo `<spec>.__final`, al que ese paso fluye. Un glifo con `label: ""` explícito no
lleva rótulo (antes caía a `{title}`).

**Deployment.** Un nodo `contains` nodos y artefactos a cualquier profundidad (un padre por nodo,
sin ciclos): la superficie anida con el link `contains` (`draw: nest`), así que un `contains` de nodo
a nodo es un subgrafo dentro de otro. Las conexiones son `connects` (communication path; nodo a nodo,
o artefacto a artefacto como antes), con `data.label` y `data.protocol`; `deploy` («deploy»,
artefacto -> nodo) y `manifest` («manifest», artefacto -> nodo o artefacto) son relaciones propias,
dibujadas punteadas con su estereotipo en el rótulo. El `keyword` de un glifo se interpola como un
rótulo (`«{kind}»` -> `«database»`) y se omite si queda vacío: ningún `{campo}` sin resolver llega a
la salida del resolver (lo comprueba un test).

**Catálogo.** Una vista de `vistas.yml` puede fijar `notation:` (ruta relativa al `vistas.yml`,
nombre builtin o `NotationDoc` del store); `catalog sync` la usa y `catalog validate` la comprueba
(`UnknownNotationError`, `NotationMismatchError`). `diagram sync` conserva `category`, `nav` y
`summary` del SpecDoc.

## 15. Paquetes UML en diagramas de clase (2026-10-20)

Un spec `type: class` puede declarar `data.packages`: id -> `{label, kind, contains, description}`.
`contains` lista clases y otros paquetes (anidado a cualquier profundidad). Si hay paquetes, cada
clase pertenece a exactamente uno; una clase huérfana, un id desconocido, un paquete que se contiene,
un elemento con dos padres, un ciclo o un id compartido entre clase y paquete son errores tipados
(`StructureError`, `UnknownReferenceError`).

**En el store y en la vista.** Cada paquete es un SpecNodeDoc de la colección `packages` (con su
`kind`); `contains` del paquete apunta a sus clases y subpaquetes. La notación `uml-class` lo dibuja
con el glifo `uml-class.package` (forma `package`) y anida con el link `uml-class.contains`
(`draw: nest`): la superficie dibuja cada paquete como contenedor de sus hijos, como los nodos
anidados de deployment. El estilo de un paquete sale de la misma precedencia (§13), por su `kind`:
`style.kinds.<kind>` del spec o la paleta; llega en `node.style` del paquete. Las clases no heredan
el color del paquete en la vista (el contenedor ya lo muestra); en mermaid sí, ver abajo.

**Renderers.** PlantUML anida `package` con el relleno (tema claro) de su kind. Mermaid no anida
`namespace`: cada paquete con clases propias es un `namespace` con el nombre de su ruta
(`Core.Billing`), y las clases toman, con `classDef` + `cssClass`, el estilo del paquete más interno
que lo tenga.

