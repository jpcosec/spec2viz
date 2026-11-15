## REFORMULACION
**Propósito:** dotar al MCP de specIR de escritura controlada sobre un store SLDB real: proponer, validar y aplicar cambios sin corromper el modelo ni perder procedencia. **Resultado:** tools MCP tipadas para crear/editar/borrar documentos registrados, afirmar/retirar `RelationDoc` y escribir `RelationTypeDoc`/`RuleDoc` como datos, con ejecución en seco y delegación en `sldb.api`. **Repo:** `src/specir/mcp/write_tools.py`, `changes.py`, `mutability.py` y pruebas en `tests/mcp/`. **Límites:** nada de clases Python de modelos, síntesis de código, CRUD propio, acceso a módulos internos de SLDB ni escritura directa a filesystem/índices; sin mocks; si falta API, se pide a SLDB y se detiene.

## AMBIGUEDADES
1. “Una arista que viola los tipos de origen o destino, la cardinalidad o la condición de su RelationTypeDoc es rechazada antes de escribir” frente a `PENDING["edge_validation_before_write"]`: “SLDB checks it only in check_edges, after the write”. Obliga a decidir si se acepta reporte posterior o se bloquea hasta que SLDB prevalide.
2. “Toda escritura admite ejecución en seco” y “Una ejecución en seco devuelve lo que se escribiría” frente a `PENDING["dry_run"]`: “the prevalidation ... runs only when apply_changes calls apply_batch”. Obliga a decidir si `propose_changes` basta como seco aunque no prevalide.
3. “Un cambio que incumple un RuleDoc vigente es rechazado o reportado según la severidad” frente a `PENDING["on_write_alerts"]`: las alertas de `RelationDoc` “are not reported”. Obliga a inventar cobertura o excluir ese caso.
4. “con el mecanismo decidido en la tarea de contrato de escritura” pero el bundle no incluye IR02/IR03 ni `docs/decisiones/...`; solo el átomo. Obliga a asumir el contrato.

## DRY-RUN
Lecturas: TaskDoc, rituales execution/testing/closeout, pills, átomos, archivos y tests citados. Comprobar dependencias IR02/IR03 y disponibilidad en `sldb.api` (`apply_batch`, `store_fingerprint`, `is_model_registered`, `rules_check`, `check_edges`). Cambios previstos: `write_tools.py`, `changes.py`, `mutability.py` y pruebas. Validaciones futuras: imports públicos, niveles 0/1/2, dry-run sin escritura, rechazo por guardas, reglas y aristas, procedencia y ausencia de tools Python. No ejecutar.

## FUTURO
SLDB debe decidir y proveer dry-run público, validación de aristas antes de escribir, `store_hash` atómico, guardas en transacción y alertas `on_write`; el desk SLDB o un humano prioriza esas extensiones. IR02/IR05 o el responsable del contrato decide si se acepta interinamente el reporte posterior.
