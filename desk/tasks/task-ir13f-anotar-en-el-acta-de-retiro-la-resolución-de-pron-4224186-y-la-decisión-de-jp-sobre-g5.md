---
sldb:
  by: agent
  at: '2026-11-16T10:40:23Z'
  authority: generated
  via: save_document_payload
id: task-ir13f-anotar-en-el-acta-de-retiro-la-resolución-de-pron-4224186-y-la-decisión-de-jp-sobre-g5
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- system:specir
- system:spec2viz
- topic:migracion
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-021430-suggestion-g5-decisi-n-de-jp-sobre-spec2viz-sldb.md
- desk/inbox/20261116-040635-suggestion-pron-ir13-resuelto-4224186.md
- task-ir13-sync-generación-catálogos-consumidores-y-retiro-de-spec2viz
depends_on:
- task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb
pills:
- desk/contexts/pill-guardrail-sin-mocks-ni-datos-fabricados-detenerse-ante-un-bloqueo.md
- desk/contexts/pill-guardrail-los-cambios-en-otros-repos-se-piden-por-su-desk.md
files:
- docs/spec2viz/acta-de-retiro.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# IR13f Anotar en el acta de retiro la resolución de pron (4224186) y la decisión de JP sobre G5

## Rationale

_Explain why this task exists or the business driver behind it._

docs/spec2viz/acta-de-retiro.md es el registro del gate de retiro de spec2viz (IR13), y dos de sus entradas quedaron desactualizadas por mensajes recibidos. (1) pron resolvió su pedido: el commit 4224186527a894da6a7842ffa03c313292437425 de pron (master, pusheado) hace que el script build.py de la carpeta docs/spec2viz de pron use specir en las tres llamadas de las líneas 22 a 24. Su tester independiente verificó que build.py sale con rc 0 y que specir retirement check no muestra filas de pron (nota desk/inbox/20261116-040635-suggestion-pron-ir13-resuelto-4224186.md). La fila de pron del acta sigue en «pendiente». (2) JP decidió G5 el 2026-11-16 con la opción A: el store spec2viz/.sldb se archiva junto con el repo spec2viz cuando specir retirement check dé 0, y no se reapuntan sus 7 modelos (nota desk/inbox/20261116-021430-suggestion-g5-decisi-n-de-jp-sobre-spec2viz-sldb.md). La fila G5 sigue en «abierto», con las dos opciones planteadas.

## Goal

_Describe the concrete result this task must produce._

El acta registra a pron como resuelto, con su commit y la evidencia, y registra en G5 la decisión de JP (opción A) y lo que queda pendiente en IR por esa decisión.

## Scope

_State what is in scope and what is out of scope._

Dentro, solo en docs/spec2viz/acta-de-retiro.md: (1) la fila de pron de la tabla de consumidores (hoy con «pendiente»): pasa a «resuelto», citando el commit 4224186 de pron y lo que verificó su tester; (2) la fila «G5 Stores»: registra la decisión de JP del 2026-11-16 (opción A: archivar spec2viz/.sldb con el repo, sin reapuntar sus 7 modelos), cita el atom de spec2viz atom-decisión-de-jp-2026-11-16-g5-el-store-spec2viz-sldb-se-archiva-con-el-repo y la task.decision task-decisión-de-jp-g5-del-retiro-archivar-el-store-spec2viz-sldb-con-el-repo-o-reapuntar-sus-7-modelos-a, y lista lo pendiente en IR: quitar spec2viz/.sldb del universo de specir retirement check al declarar el retiro (IR13), y dejar de federar ese store en las pruebas (task-las-pruebas-de-mcp-dejan-de-federar-el-store-real-spec2viz-sldb-g5-opción-a). El estado de G5 queda «decidido; pendiente de ejecución en IR», no «cerrado»; (3) la lista de pasos que quedan al final del acta (los puntos «Consumidores (G4)» y «Store (G5)»): se quita pron de G4 y en G5 se reemplaza la alternativa por la decisión tomada; (4) se corre de nuevo specir retirement check y se anota su salida resumida (filas abiertas, número de dependencias y rc), igual que las corridas anteriores del acta. Fuera: la matriz de cobertura; declarar el retiro; quitar spec2viz/.sldb del universo; tocar las pruebas; cambiar pron o spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

Leer primero las dos notas de desk/inbox citadas en Why y el acta completa. Editar solo docs/spec2viz/acta-de-retiro.md, conservando el formato de sus tablas y de las corridas anteriores de specir retirement check. Para comprobar lo que dice la nota de pron: grep -n specir ../pron/docs/spec2viz/build.py muestra las llamadas de las líneas 22 a 24, y git -C ../pron merge-base --is-ancestor 4224186 HEAD sale con rc 0. Si alguna de las dos cosas falla, la fila de pron no se marca como resuelta: se anota lo que se encontró y se reporta. Para verificar el atom y la task.decision de spec2viz: ls ../spec2viz/desk/atoms/ | grep g5 y ls ../spec2viz/desk/tasks/ | grep g5. El comando del comprobador es el mismo de las corridas anteriores del acta: timeout 300 .venv/bin/specir retirement check --path graph_ui=../UIs/graph_ui --path deskops=../deskops --path pron=../pron --path sldb=../sldb --path spec2viz/.sldb=../spec2viz/.sldb. Comandos desde la raíz de IR, con TMPDIR=/dev/shm y el .venv del repo.

## Validation

_List the checks required before this task can close._

- git diff --stat muestra, fuera de desk/, .sldb/ y runs/, solo docs/spec2viz/acta-de-retiro.md.
- git -C ../pron merge-base --is-ancestor 4224186 HEAD sale con rc 0, y la salida de specir retirement check no tiene filas de pron.
- TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py sale con rc 0.
- grep -n 'pron' docs/spec2viz/acta-de-retiro.md muestra la fila de pron como resuelta, con 4224186, y grep -n 'G5' muestra la decisión de JP (opción A) y lo pendiente en IR.
- deskops graph missing --root . sale con rc 0.

## Done When

_Name the observable condition that makes the task complete._

El acta registra a pron como resuelto con su commit y su evidencia, y G5 como decidido (opción A) con lo pendiente en IR. La salida nueva de specir retirement check está anotada, y las pruebas de la matriz y del gate pasan.
