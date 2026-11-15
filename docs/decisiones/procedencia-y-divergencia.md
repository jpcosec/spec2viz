# Procedencia y divergencia entre código y modelo en specIR

> **Estado: DECIDIDO — JP aceptó las recomendaciones el 2026-11-15 (chat con el supervisor).**
> Tarea: `task-ir05-decisión-procedencia-y-divergencia-entre-código-y-modelo`.
> Redactado: 2026-11-14 por el ejecutor (agente) con alternativas y recomendación; elección de
> JP registrada el 2026-11-15 en cada sección. Los atoms están en la última sección.

## Insumos

- `fundamentos_modelado_semantico_mcp.md` §7 (observado, inferido, validado) y §8 («el sistema
  debe conservar lo que desconoce»).
- `Plan_IR.md` fase 5 (elementos observados, relaciones derivadas estáticamente, inferencias
  propuestas por LLM, relaciones verificadas), riesgos (§6: «divergencia entre código y
  modelo») y principio final («sin exigir que todos los artefactos sean generados
  exclusivamente desde [los modelos]»).
- SLDB `sldb@6aeba3eb`:
  - `src/sldb/models/provenance.py`: `Authority = Literal["source_raw", "authored", "theorem",
    "generated", "cache"]`; `Provenance` con `by`, `at`, `via`, `authority`, `from`; lo sella
    `src/sldb/api/documents/provenance_stamp.py` en cada escritura. Sin bloque se lee
    `agent / 0 / generated`.
  - `docs/architecture/provenance.md` §2 (qué es cada nivel y qué significa que cambie) y §5
    (la política lee la autoridad).
  - `docs/architecture/anchoring.md` §§1-6 y `code-anchoring.md`: anclar es «fundamentar una
    afirmación en su fuente y guardar lo que vio»; estados `intact`, `changed`, `reconnected`,
    `lost` (alertas, nunca error); `code:<ruta>::<qualified_name>`.
  - API: `sldb.api.anchors.record_anchor`, `sldb.api.anchors.check_anchors` (anclas a código,
    exportadas en `sldb.api.anchors.__all__`, no en `sldb.api.__all__`) y
    `sldb.api.check_doc_anchors` (anclas a documentos). El escáner de código
    (`src/sldb/code/scan.py`) recorre solo archivos `.py` con tree-sitter-python.
  - `src/sldb/models/relation_doc.py`: una relación es un `RelationDoc`, documento con su propio
    bloque `sldb` y un campo libre `attributes`.
- Matriz IR01: [docs/auditoria/sldb-api-frente-a-mcp.md](../auditoria/sldb-api-frente-a-mcp.md).
- Decisión hermana: [contrato-de-escritura-mcp.md](contrato-de-escritura-mcp.md) (IR02), D3.

## Diagnóstico de las tres listas

Las tres listas no compiten por lo mismo; mezclan tres ejes distintos:

| eje | pregunta | (1) fundamentos | (2) Plan_IR f5 | (3) SLDB `authority` |
|---|---|---|---|---|
| **origen** | ¿cómo se obtuvo la afirmación? | observado, inferido | observado, derivado estáticamente, inferencia de LLM | — |
| **verificación** | ¿alguien la confirmó? | validado | verificado | — |
| **autoridad** | ¿quién puede cambiar el documento y qué significa que cambie? | — | — | source_raw, authored, theorem, generated, cache |

(1) y (2) usan un solo enum para dos ejes: «verificado» borra cómo se obtuvo. (3) es la
política de mutación de SLDB, no un estado epistémico: un nodo extraído y una inferencia de
LLM pueden ser ambos `generated` o ambos `authored` según quién los regenere.

---

## D1. Taxonomía canónica y equivalencias

| | alternativa | consecuencias |
|---|---|---|
| D1-A | **Un enum de cuatro** (lista 2): `observado`, `derivado`, `inferido`, `verificado`. | Simple; pero al verificar se pierde el origen y no se puede preguntar «qué inferencias se verificaron». |
| D1-B | **Dos ejes en specIR + autoridad de SLDB como tercer eje por mapeo.** `origen ∈ {observado, derivado, inferido, declarado}` y `verificacion ∈ {sin_verificar, verificado, refutado}` (+ `verificado_por`, `evidencia`), en los modelos de dominio de specIR (nodos y `RelationDoc.attributes`). La `authority` de SLDB se fija por tabla y no se reinventa. | Cada pregunta tiene su campo; la autoridad la sigue manejando SLDB. Exige los dos campos en los tipos de dominio (IR06). |
| D1-C | **Solo la autoridad de SLDB + `by`**: observado/derivado = `generated` con `from: code:…`; inferido = `authored` por `agent:<id>`; validado = `authored` por `human:<id>`. | Cero campos nuevos. Pero la verificación queda implícita en `by`: un humano que edita una inferencia por otro motivo la «valida» sin querer, justo lo que fundamentos §7 prohíbe. |

`declarado` cubre lo que un humano o agente escribe a propósito en el modelo (diseño, regla,
decisión) y no se extrajo de código: el Plan dice que no todo se genera desde el código.

**Recomendación: D1-B**, con esta tabla de equivalencias:

| specIR `origen` | lista (1) | lista (2) | `authority` SLDB | `from` |
|---|---|---|---|---|
| `observado` (lo leyó un extractor tal cual: un símbolo, una ruta, una tabla) | observado | observado | `generated` | `code:<ruta>::<símbolo>` |
| `derivado` (regla estática enunciada sobre lo observado) | observado | derivado estáticamente | `theorem` | las fuentes de la regla |
| `inferido` (propuesto por un LLM) | inferido | inferencia de LLM | `authored` (`by: agent:<id>`) | lo que el LLM leyó, si lo declara |
| `declarado` (escrito con intención) | — | — | `authored` | — |

| specIR `verificacion` | lista (1) | lista (2) |
|---|---|---|
| `sin_verificar` | (observado/inferido) | (las tres primeras) |
| `verificado` | validado | verificado |
| `refutado` | — | — |

- Alternativa elegida: **D1-B (dos ejes `origen` y `verificacion` en specIR; autoridad SLDB por la tabla de equivalencias)**
- Motivo: se acepta la recomendación de esta sección.
- Fecha: 2026-11-15
- Decidió: JP (chat con el supervisor)

## D2. Cómo se representa lo desconocido y cómo una inferencia pasa a verificada

**Lo desconocido.**

| | alternativa | consecuencias |
|---|---|---|
| D2-A | Campo ausente o `null`. | Ambiguo: no distingue «no aplica» de «no se sabe». |
| D2-B | `null` más una lista `desconocidos` en el nodo (campo y motivo: «el extractor no ve permisos dinámicos»). | Lo desconocido queda nombrado y consultable (`find --where`), sin nodos falsos. |
| D2-C | Nodos de hueco (`GapDoc`) enlazados al nodo. | Visible en el grafo; multiplica documentos y se confunde con los hallazgos de inconsistencia de IR10. |

**La promoción a verificado.**

| | alternativa | consecuencias |
|---|---|---|
| D2-D | Cualquier actor con escritura de nivel 1 puede marcar `verificado`. | El agente se valida a sí mismo; viola fundamentos §7. |
| D2-E | Solo una de dos vías, y siempre con escritura explícita de `verificacion`, `verificado_por` y `evidencia`: (i) un humano por una superficie que no es el MCP (CLI de sldb/deskops con `--actor human:<id>`, graph_ui); (ii) un chequeo determinista (extractor estático que observa la misma relación, test) con `verificado_por: check:<id>` y su evidencia anclada. El servidor MCP rechaza que un agente escriba `verificado`. | Ninguna inferencia pasa a hecho en silencio. Como el actor de SLDB no está autenticado (IR02, D3-C), la frontera es la superficie, no el nombre declarado. |

**Recomendación: D2-B + D2-E.**

- Alternativa elegida: **D2-B + D2-E (`null` + lista `desconocidos`; verifica solo un humano fuera del MCP o un chequeo determinista)**
- Motivo: se acepta la recomendación de esta sección.
- Fecha: 2026-11-15
- Decidió: JP (chat con el supervisor)

## D3. Relación nodo extraído ↔ fuente: ¿anclas de código de SLDB?

| | alternativa | operación SLDB | consecuencias |
|---|---|---|---|
| D3-A | **Anclas de SLDB.** Cada nodo `observado`/`derivado` lleva `from: code:<ruta>::<símbolo>` en su bloque `sldb`, y un `CodeAnchorDoc` guarda lo que vio (firma, docstring, cuerpo). | `sldb.api.anchors.record_anchor`, `check_anchors` (con `record=True` solo para reconexiones). | Reusa la detección de cambio, la reconexión por renombre y la regla «alerta, no error». **Solo Python**: Django sí; SQL y React/TSX (IR08, IR09) no. |
| D3-B | Solo `from: code:…` sin `CodeAnchorDoc`. | El bloque `Provenance`. | Dice de dónde viene, pero no verifica nada: anchoring.md §1 dice que eso no es anclar. |
| D3-C | Referencia propia de specIR (ruta, rango de líneas, hash del archivo). | — | Reimplementa en specIR lo que SLDB ya tiene: viola `atom-specir-depende-solo-de-la-api-pública-de-sldb`. Las líneas se mueven sin que nada cambie. |

**Recomendación: D3-A**, y pedir a SLDB que extienda el escáner de anclas a TypeScript/TSX y
a SQL (gramáticas tree-sitter) antes de IR08/IR09. Mientras no exista, los nodos de esas
fuentes usan D3-B y quedan con `verificacion: sin_verificar` y la ancla en `desconocidos`.

**Carencia frente a la matriz IR01:** la matriz **no tiene fila** para anclar a código fuera
de Python; es una carencia nueva. Se agrega como fila a la matriz (o se cita esta sección) y se
notifica a SLDB con `deskops message send --to sldb` tras la elección de JP. Se relaciona con
la fila «consultar journal e historial» solo para la historia del nodo, que ya cubre
`document_history`.

- Alternativa elegida: **D3-A (anclas de código de SLDB; TSX y SQL pedidos a SLDB, mientras tanto D3-B con `sin_verificar`)**
- Motivo: se acepta la recomendación de esta sección.
- Fecha: 2026-11-15
- Decidió: JP (chat con el supervisor)

## D4. Divergencia: qué prevalece cuando modelo y código discrepan

| | alternativa | consecuencias |
|---|---|---|
| D4-A | **Manda el código siempre**: re-extraer sobrescribe y borra lo que ya no está. | Simple; destruye diseño declarado y verificaciones humanas; borra nodos que quizá solo se renombraron. |
| D4-B | **Manda el modelo siempre**: el código que difiere es un hallazgo. | Respeta la intención; pero el modelo extraído envejece y deja de describir el sistema real. |
| D4-C | **Según el origen, y la divergencia se calcula, no se escribe.** Para `observado`/`derivado` (`generated`) manda el código: la re-extracción los regenera. Para `declarado` y todo lo `verificado` manda el modelo: la diferencia es un hallazgo para el análisis de impacto (IR10), nunca una sobrescritura. Un nodo cuya ancla queda `changed` o `lost` no se borra: el estado de la ancla se lee al consultar (como `anchor_state` en SLDB) y una verificación sobre un ancla no `intact` se reporta como vencida hasta que alguien vuelva a verificar o reanclar. `reconnected` se acepta y queda en el historial de la ancla. | Sigue las reglas del dueño en anchoring.md §§3-4 (cambiar es alerta) y el principio final del Plan. Exige que IR10 consuma los estados de ancla. |

**Recomendación: D4-C.** Lo desconocido (D2) y lo divergente se conservan y se muestran; nada
se borra en silencio.

- Alternativa elegida: **D4-C (según el origen; la divergencia se calcula al leer y nada se borra en silencio)**
- Motivo: se acepta la recomendación de esta sección.
- Fecha: 2026-11-15
- Decidió: JP (chat con el supervisor)

---

## Atoms

Creados el 2026-11-15 con `deskops add atom --provenance docs/decisiones/procedencia-y-divergencia.md`:

1. Taxonomía canónica y tabla de equivalencias (D1):
   `atom-la-procedencia-en-specir-tiene-dos-ejes-y-la-autoridad-de-sldb-se-asigna-por-tabla`
2. Lo desconocido y la promoción a verificado, por acción de quién (D2):
   `atom-lo-desconocido-se-nombra-y-solo-un-humano-fuera-del-mcp-o-un-chequeo-determinista-verifica`
3. Divergencia: qué pasa con un nodo cuya fuente cambió (D3 + D4):
   `atom-un-nodo-extraído-se-ancla-con-sldb-y-la-divergencia-con-el-código-se-calcula-según-su-origen`

Actualizado con `deskops edit atom`: `atom-reglas-de-seguridad-de-la-superficie-mcp-de-specir`
(cita la taxonomía decidida y ya no la declara pendiente).
