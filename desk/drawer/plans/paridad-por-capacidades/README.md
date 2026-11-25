# Plan: paridad de specIR por capacidades

Reescrito el 2026-11-25. Las decisiones y su porqué están en
`docs/decisiones/paridad-por-capacidades.md`; aquí va solo el trabajo. El borrador de notación
está en `specir-layers.yml`.

Planes hermanos: `sldb/desk/drawer/plans/superficie-como-contrato-de-editores/` (interfaces),
`sldb/desk/drawer/plans/pedidos-de-specir-y-graph-ui/` (lo pedido a sldb) y
`UIs/graph_ui/desk/drawer/plans/fierros-hacia-afuera/` (editor de grafo).

## Trabajo de IR

| Trabajo | Estado al 2026-11-25 |
|---|---|
| Borrar los goldens de spec2viz y las pruebas que los leen | hecho (`1fd427c`) |
| `specir mcp` delega en `mcp_extension` | hecho (`207c578`) |
| Las pruebas encuentran el workspace por `SPECIR_WORKSPACE` | hecho (`aa7045a`) |
| Dejar sin efecto las tareas U2, U3, U4, U5 y U9 de la app `IR/ui/` | sin hacer |
| Recibir de sldb las notaciones builtin y las clases de spec por tipo de diagrama | sin tarea |
| Sembrar la notación de los tipos de specIR desde `specir.install` | sin tarea; el borrador está validado |
| Notación BPMN | sin tarea |
| Notaciones de ORCA e IFML, y los huecos del modelo de dominio que destapan | sin tarea |
| Capacidades como datos del store, con su regla y su vista | **reemplazado** por la tarea `task-una-capacidad-del-dominio-declara-para-quien-es-y-cual-es-su-prueba-de-aceptacion-y-las-ocho-capacid` (`CapabilityDoc` con `audience`, `accepted_by` hacia una materialización, regla y vista) |
| Reescribir el guardrail de paridad | sin verificar si la tarea de goldens lo hizo |
| Retirar `CatalogAnnotationsDoc` y la página HTML del catálogo | espera las capacidades 1 a 4 y 6 |

## La notación de los tipos de specIR

`specir-layers.yml`: 11 glifos (uno por tipo de dominio) y 11 links (los 10 tipos de relación de
specIR más `references`). `sldb notations validate` lo acepta. Probado en el servidor de graph_ui:
con el blog de ejemplo extraído a un store, `POST /api/views/evaluate` devuelve los nodos con su
glifo y las aristas, sin error de notación.

Límites conocidos:

- No se puede ver todavía: la vista de notación de graph_ui solo lista `SpecDoc` (su tarea G-C).
- No hay carriles por capa: el layout `lanes` de graph_ui es el de secuencia. El borrador usa
  grafo de izquierda a derecha.

## Capacidades como datos

**Reemplazado** por la tarea `task-una-capacidad-del-dominio-declara-para-quien-es-y-cual-es-su-prueba-de-aceptacion-y-las-ocho-capacid`: una capacidad es un
`CapabilityDoc` (un `DomainOperationDoc` con `audience`), no un `AtomDoc`; su prueba es un
`MaterializationContractDoc` enlazado por `accepted_by`, y una regla y una vista la exigen y la
listan. Lo que decía este apartado se conserva abajo.

Antes: sin modelos nuevos: un `AtomDoc` por capacidad, un `MaterializationContractDoc` hacia su prueba de
aceptación, una `RuleDoc` que exige esa evidencia y una `ViewDoc` que las lista.

## Pendientes sueltos

| Pendiente | Dueño |
|---|---|
| Una prueba MCP falla si el despacho escribe en el store de IR mientras corre (`tests/test_mcp_extension.py:141`) | despacho de robocop2 |
| Las sesiones de Claude de robocop2 pierden el login; falta un token de larga duración (`claude setup-token`) | JP |
| Las decisiones D3 a D10 quedaron firmadas como `disposed_by: IR`, no a nombre de JP | deskops |
