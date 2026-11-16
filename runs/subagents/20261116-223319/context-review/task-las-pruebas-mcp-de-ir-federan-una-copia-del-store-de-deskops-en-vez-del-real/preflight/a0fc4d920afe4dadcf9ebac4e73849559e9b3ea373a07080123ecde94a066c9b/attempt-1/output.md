## REFORMULACION

Encargo ejecutable (`task.code`) sobre el repo IR (`/mnt/ssd/proyectos/SLDB_1/IR`). **Propósito:** que la suite MCP de IR no dependa del store real de deskops, hoy federado en `tests/conftest.py`, porque escrituras concurrentes de otros agentes la hacen fallar. **Resultado:** el fixture que enlaza deskops copia su store (y lo necesario para resolver enlaces) a un directorio temporal de sesión, y `test_reading_through_every_tool_leaves_every_store_untouched` digiere esa copia; la cobertura de lectura sobre store federado se conserva. **Límites:** solo `tests/conftest.py` y `tests/test_mcp_extension.py`; no se modifica deskops ni sldb; queda fuera la tarea de federación spec2viz, que va antes y toca los mismos archivos. **Cierre:** pruebas MCP sin leer el store real y suite completa en verde aun con escrituras en deskops.

## AMBIGUEDADES

1. «una copia del store de deskops tomada al inicio de la sesión» / «directorio temporal de sesión»: no define si “sesión” es el scope de fixture pytest ni cuándo se toma la copia. Obliga a inventar alcance y momento.
2. «y lo que haga falta para que sus enlaces resuelvan»: indeterminado qué rutas (sldb, pron, scion) copiar o reescribir. Obliga a inventar la estrategia de enlaces.
3. «Con una escritura simulada en una copia desechable del store de deskops durante la prueba»: no dice mecanismo, fixture ni ubicación. Obliga a inventar cómo simularla.
4. «la prueba de untouched»: el rationale nombra `test_reading_through_every_tool_leaves_every_store_untouched`, pero no confirma que sea esa. Obliga a asumir el identificador.
5. «se detiene y se reporta»: sin formato, canal ni destinatario. Obliga a inventar el protocolo de bloqueo.
6. «Empezar cuando esté integrada task-…»: no hay criterio verificable de integración en el input. Obliga a inventar cómo comprobarlo.
7. «deskops graph missing --root .»: no fija cwd ni entorno. Obliga a asumir el directorio.

## DRY-RUN

**Lecturas:** `tests/conftest.py`, `tests/test_mcp_extension.py`, la tarea predecesora g5 y la pill de guardrail. **Cambios previstos:** fixture de copia a tempdir de sesión; ajuste del test untouched. **Dependencias:** predecesora integrada; ruta del store deskops; destinos de enlaces sldb/pron/scion; `TMPDIR=/dev/shm`. **Validaciones futuras:** pytest del archivo con rc 0 sin skips; escritura simulada sin romper untouched; suite completa bajo `flock`; `deskops graph missing --root .`.

## FUTURO

Decide un humano si la estrategia de copia de enlaces es aceptable y qué hacer ante el reporte de bloqueo. Otro nodo entrega la predecesora integrada y el resultado de la suite completa; este nodo no los produce.
