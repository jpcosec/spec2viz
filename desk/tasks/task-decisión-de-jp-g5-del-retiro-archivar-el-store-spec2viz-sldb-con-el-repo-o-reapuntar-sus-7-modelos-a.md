---
sldb:
  by: agent
  at: '2026-11-16T05:13:55Z'
  authority: generated
  via: save_document_payload
id: task-decisión-de-jp-g5-del-retiro-archivar-el-store-spec2viz-sldb-con-el-repo-o-reapuntar-sus-7-modelos-a
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-225013-suggestion-ir13-el-store-de-spec2viz-es-el-nico-que-registra-spec2viz-sldb-models-gate-g5.md
depends_on: []
pills: []
files:
- ../IR/docs/spec2viz/acta-de-retiro.md
- .sldb/core/models/SpecDoc.yaml
task_type: task.decision
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-decisión-de-jp-2026-11-16-g5-el-store-spec2viz-sldb-se-archiva-con-el-repo
---

# Decisión de JP (G5 del retiro): archivar el store spec2viz/.sldb con el repo o reapuntar sus 7 modelos a sldb

## Rationale

_Explain why this task exists or the business driver behind it._

El gate de retiro de spec2viz (IR13, acta IR/docs/spec2viz/acta-de-retiro.md, ítem G5 y paso 2 de «Lo que falta») sigue abierto porque spec2viz/.sldb es el único store del universo auditado que registra modelos spec2viz.sldb_models: 19 registros en .sldb/store.yaml:44-57, .sldb/core/store_index.yaml:141-260 y .sldb/core/models/{SpecDoc,SpecNodeDoc,NotationDoc,GlyphDoc,LinkDoc,PaletteDoc,ViewDoc}.yaml:2. El acta deja la elección como decisión del dueño. Corrida del 2026-11-16 de specir retirement check: rc 1, 122 dependencias.

## Goal

_Describe the concrete result this task must produce._

JP elige una de dos opciones y la decisión queda registrada en este desk y comunicada a IR: (A) archivar el store junto con el repo spec2viz cuando specir retirement check dé 0 (sin tocar el store ahora; IR quita el path spec2viz/.sldb del universo del comprobador y cambia la federación de sus pruebas por un fixture), o (B) mantener el store vivo después del retiro y reapuntar los 7 modelos a los públicos de sldb (sldb.models.notation.{spec_doc.SpecDoc, spec_node_doc.SpecNodeDoc, notation_doc.NotationDoc, glyph_doc.GlyphDoc, link_doc.LinkDoc, palette_doc.PaletteDoc, view_doc.ViewDoc}, fila SV-A17 de IR/docs/spec2viz/matriz-de-cobertura.md) con el CLI sldb, nunca a mano. Recomendación del coordinador: A, porque ningún consumidor fuera de las pruebas de IR lee este store y la decisión 6 del acta ya archiva el repo entero.

## Scope

_State what is in scope and what is out of scope._

Entra: (1) obtener la elección de JP, A o B, como recibo owner de esta tarea; (2) registrarla como atom de decisión en este desk; (3) avisar a IR con deskops message send --to IR; (4) solo si JP elige B, crear en este mismo cierre (sin ejecutarla) una task.code en este desk para el reapunte. No entra: ejecutar A o B. El reapunte de B (comandos sldb y criterio) lo define y ejecuta esa task.code aparte. El archivo de A lo hace la tarea de retiro cuando IR13 confirme que specir retirement check da 0; quien corre y verifica ese comando es el desk de IR, no esta tarea. Tampoco entra tocar IR/tests/conftest.py ni IR/tests/test_mcp_extension.py (los cambia IR), ni archivar el repo.

## Implementation Path

_Outline the expected implementation route or affected surface._

Lo ejecuta el coordinador del desk spec2viz; JP solo elige y dispone el recibo. 1) El coordinador presenta a JP las opciones A y B con la evidencia de ../IR/docs/spec2viz/acta-de-retiro.md (G5 y paso 2 de «Lo que falta») y la recomendación A. 2) El coordinador guarda la respuesta textual de JP en runs/decisions/g5-store-spec2viz.md y la registra como recibo owner: deskops review record task-decisión-de-jp-g5-del-retiro-archivar-el-store-spec2viz-sldb-con-el-repo-o-reapuntar-sus-7-modelos-a --kind owner --evidence runs/decisions/g5-store-spec2viz.md --reason "JP elige A" (o B) --root .; la disposición accepted de ese recibo la hace JP, no el coordinador. 3) Apenas JP responde, sin esperar a que specir retirement check dé 0, el coordinador crea el atom: deskops add atom --root . --five-wh-one-plus why --answer "Decisión de JP del <fecha ISO>: el store spec2viz/.sldb <se archiva con el repo cuando specir retirement check dé 0 | se mantiene y sus 7 modelos se reapuntan a sldb.models.notation>. Motivo: <motivo de JP>. Origen: G5 del acta IR/docs/spec2viz/acta-de-retiro.md." 4) Envía a IR: deskops message send --root . --to IR --kind suggestion --title "G5: decisión de JP sobre spec2viz/.sldb" "<opción elegida, id del atom y fecha>". 5) Solo si es B: deskops add task --root . --task-type task.code, con files .sldb/store.yaml más los 7 archivos de .sldb/core/models (SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc, PaletteDoc y ViewDoc .yaml) y el atom del paso 3 en --atom.

## Validation

_List the checks required before this task can close._

- deskops show task task-decisión-de-jp-g5-del-retiro-archivar-el-store-spec2viz-sldb-con-el-repo-o-reapuntar-sus-7-modelos-a --root . (muestra un recibo owner aceptado e intacto)
- grep -rl 'spec2viz/.sldb' desk/atoms (encuentra el atom de la decisión de JP)
- grep -l 'G5' ../IR/desk/inbox/*.md (encuentra la nota enviada a IR con la opción)

## Done When

_Name the observable condition that makes the task complete._

Existe en desk/atoms un atom de decisión con la opción elegida por JP (A o B) y la fecha; ../IR/desk/inbox tiene la nota «G5: decisión de JP sobre spec2viz/.sldb» con esa opción; si la opción es B, existe en desk/tasks la task.code del reapunte (creada, no ejecutada).
