## REFORMULACION

**Propósito:** cerrar la migración de spec2viz a specIR demostrando, con evidencia, que ninguna capacidad queda sin cubrir y que ningún consumidor depende de spec2viz. **Resultado:** `specir retirement check` en solo lectura sobre el inventario de la matriz más el repo de specIR; informe con repo/store, ruta, línea y clase por dependencia; filas SV-* sin acreditar; código 0 solo si no hay ninguna; acta y matriz actualizadas; pedidos a otros desks. **Repo:** IR (specIR), con `src/specir/visual/retirement.py`, `src/specir/cli.py`, pruebas y `docs/spec2viz/`. **Límites:** no implementar capacidades, no editar otros repos, no archivar spec2viz; universo exacto del inventario más IR; prosa, documentación, comentarios y changelogs no cuentan. No es agregado puro: es `task.code` con entregable propio y papel de agregación; IR13a/b/d/e y IR07 aportan sincronización, catálogos, CLI, pruebas portadas y matriz, e IR13 integra esa evidencia en el gate.

## AMBIGUEDADES

1. «pedidos de migración a los desks de graph_ui, deskops y de cada repo con stores afectados» frente al inventario, que incluye también pron, sldb y spec2viz. Obligaría a inventar qué consumidores sin store deben recibir pedido; el estado ya menciona mensajes a deskops, graph_ui, pron, sldb y spec2viz.
2. «Qué no cuenta: menciones en texto, documentación, comentarios» frente a «habilidad de agente» y «habilidades (`SKILL.md`…) que nombran `spec2viz <subcomando>`». Obligaría a decidir si un `SKILL.md` es documentación exenta o dependencia operativa; la precisión 3 lo incluye, pero el alcance sigue en tensión.
3. «El acta de retiro lista, por cada consumidor del inventario, el mensaje enviado a su desk» frente a filas como IR (propio) y el store `spec2viz/.sldb`. Obligaría a inventar qué «mensaje enviado» corresponde a IR y a un store sin desk propio.

## DRY-RUN

**Lecturas:** matriz (inventario y acreditación), rutas locales de repos/stores, TaskDoc, pills y átomos. **Cambios previstos:** subcomando `retirement check` en `cli.py`; acta con salida y evidencia; matriz con prueba por fila; mensajes a desks. **Dependencias:** IR13a, IR13b, IR13d, IR13e e IR07 cerradas; respuestas de graph_ui, deskops, pron, sldb y spec2viz; comandos de validación de sldb. **Validaciones futuras:** pruebas sintéticas de fila sin prueba, cuatro clases de dependencia, ausencia de escritura, menciones inocuas, inventario estricto y ejecución real con rc 0.

## FUTURO

JP decide archivar spec2viz y su store; sldb entrega validación de spec/notación/paleta y resuelve `gen_golden.py`; los desks confirman commits; el supervisor/JP aprueba cualquier reescritura de filas.
