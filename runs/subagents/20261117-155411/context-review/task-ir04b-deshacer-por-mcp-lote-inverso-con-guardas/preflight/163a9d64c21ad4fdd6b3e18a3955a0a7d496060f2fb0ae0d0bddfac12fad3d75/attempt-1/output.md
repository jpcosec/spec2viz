## REFORMULACION

**Propósito:** verificar, desde specIR, que el `undo_changes` servido por `sldb mcp` deshace los últimos lotes de la sesión —incluidos los que pasan por los validadores de dominio de specIR— sin que specIR implemente el deshacer. **Resultado:** pruebas de integración con cliente MCP real sobre copia montada del store, y corrección de `src/specir/mcp_extension.py` para que deje de crear un segundo `WriteTools` y registre su validador IR05 D2-E mediante `add_batch_validator`; módulo nuevo `tests/test_mcp_undo` y ajuste de expectativas en `tests/test_mcp_extension.py`. **Repo:** specIR (`src/specir`, `tests/`); sldb se usa como dependencia pública por MCP, sin cambios propios allí. **Límites:** no registrar `undo_changes`, no guardar pila ni construir lotes inversos, no deshacer entre sesiones, no nivel 3, sin mocks ni datos fabricados. Nodo ejecutable (`task.code`), no agregado.

## AMBIGUEDADES

1. «los tres espejos de depends_on están cerrados» frente a `depends_on` con tareas espejo y `status: draft`: ¿basta esa afirmación para ejecutar o debe verificarse el cierre? Obliga a inventar el criterio de comprobación.
2. «Si sldb mcp no sirve undo_changes, la tarea no se ejecuta» frente a «(a) los tres espejos [...] están cerrados»: ¿condición vigente o ya resuelta? Obliga a decidir si se comprueba antes de escribir pruebas.
3. «La única lógica nueva en specIR, si hace falta» frente a «(e) [...] Se corrige en specIR: la extensión deja de crear WriteTools [...] y registra su regla»: ¿la corrección es obligatoria o condicional? Obliga a inventar el alcance real del cambio.
4. «se ajustan al rechazo domain de sldb, sin debilitar lo que comprueban»: no define qué aserciones exactas cambian ni qué constituye debilitarlas. Obliga a inventar el criterio de equivalencia.
5. «una vez revertido el cambio ajeno»: no indica cómo revertirlo ni con qué herramienta o nivel. Obliga a inventar el procedimiento.
6. «si el deshacer deja el store en un estado que esos validadores rechazarían, es un hallazgo»: no fija cómo detectarlo ni dónde registrarlo. Obliga a inventar mecanismo y destino.

## DRY-RUN

**Lecturas:** TaskDoc, nota de inbox referenciada, `sldb/src/sldb/mcp/mutability.py`, `tests/conftest.py`, `src/specir/mcp_extension.py`, `tests/test_mcp_extension.py`. **Cambios previstos:** retirar creación/reemplazo de `WriteTools` y registrar validador con `add_batch_validator`; crear `tests/test_mcp_undo`; ajustar pruebas existentes. **Dependencias:** espejos cerrados; `undo_changes` de sldb; fixtures `mount_copy` y sesión MCP de escritura. **Validaciones futuras:** identidad del store tras deshacer; rechazo `stale` sin escritura y persistencia en pila; niveles 0/1/2; `grep` sin implementación propia; `sldb rules check`, `sldb edges check`; `deskops graph missing --root .` con rc 0.

## FUTURO

Un nodo o humano confirma el cierre de los espejos y que `undo_changes` está servido; decide el destino de hallazgos para sldb y valida el ajuste de pruebas existentes sin pérdida de cobertura.
