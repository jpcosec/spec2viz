## REFORMULACION

Propósito: añadir al MCP de specIR escritura validada para que un agente proponga, valide y aplique cambios al store sin dejarlo inconsistente y con procedencia. Resultado: tools MCP de escritura con ejecución en seco, usando el mecanismo que decida IR02. Repo: `SLDB_1/IR`, paquete `src/specir`, pruebas en `tests/mcp`. Límites: dentro, crear/editar/borrar documentos de modelos registrados, aristas `RelationDoc`, `RelationTypeDoc` y `RuleDoc`; fuera, clases Python de modelos y síntesis de código. El nodo es una `task.code` ejecutable, no un agregado ni paquete, aunque depende de IR02 e IR03.

## AMBIGUEDADES

1. “con el mecanismo decidido en la tarea de contrato de escritura”: el input no trae ese mecanismo; obligaría a inventar la interfaz y el flujo proponer/validar/aplicar.
2. “según la severidad de la regla”: no enumera severidades ni si cada una rechaza, advierte o solo reporta.
3. “Una tool por encima del nivel de escritura permitido”: no define niveles ni cuál es el permitido; obligaría a inventar la matriz de mutabilidad.
4. “Cada documento escrito lleva en su procedencia quién y por qué operación”: no fija campos, formato ni identidad del agente.
5. “Aplicar un cambio validado sobre un store que cambió después de la validación”: no define versión, token ni criterio de detección.
6. “store de prueba”: no indica cómo se aprovisiona ni si debe ser SLDB real.
7. “lo que falte se resuelve en SLDB, no en specIR”: no delimita qué operaciones faltan ni su contrato.

## DRY-RUN

Lecturas: esta tarea, salidas de IR02/IR03, pills de guardrail, API pública de SLDB y pruebas existentes. Cambios previstos: `write_tools.py`, `changes.py`, `mutability.py` y pruebas `test_write_tools.py`, `test_dry_run.py`, `test_mutability.py`. Dependencias: contrato de IR02, servidor de IR03 y operaciones públicas de SLDB. Validaciones futuras: ejecutar `pytest tests/mcp`; comprobar que el dry-run no muta el store; rechazo por store cambiado, arista inválida y regla incumplida; argumentos solo tipados; procedencia; bloqueo por nivel; ausencia de tools sobre módulos Python; ciclo manual de un agente. Nada se ejecuta ahora.

## FUTURO

IR02 decide el contrato de escritura y el nivel de mutabilidad. IR03 entrega el servidor MCP de solo lectura como base. SLDB implementa las operaciones públicas faltantes. Un humano revisa y aprueba el cierre tras las validaciones.
