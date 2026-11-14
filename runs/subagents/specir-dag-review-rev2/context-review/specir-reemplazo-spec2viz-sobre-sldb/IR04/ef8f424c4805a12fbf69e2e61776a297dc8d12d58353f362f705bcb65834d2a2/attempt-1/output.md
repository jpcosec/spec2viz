REFORMULACION

IR04 es un nodo de código, no un agregado, del repo specIR: entregar tools MCP de escritura para que un agente proponga, valide y aplique cambios al store SLDB, usando el mecanismo que fije IR02. Resultado: `write_tools.py`, `changes.py`, `mutability.py` y sus pruebas. Límites: dentro, mutar documentos de modelos ya registrados, aristas, RelationTypeDoc y RuleDoc, con ejecución en seco; fuera, editar clases Python de modelos por MCP y sintetizar código de aplicación.

AMBIGUEDADES

1. «Un cambio que incumple un RuleDoc vigente es rechazado o reportado según la severidad de la regla»: no se definen las severidades ni el criterio rechazar/reportar; obligaría a inventar el catálogo y su semántica.
2. «Cada documento escrito lleva en su procedencia quién y por qué operación se escribió»: no se indica de dónde sale «quién»; obligaría a inventar el modelo de actor o identidad.
3. «Una tool por encima del nivel de escritura permitido responde error sin evaluar nada»: el nodo no enumera los niveles ni cómo se resuelve el permitido; obligaría a inventar la escala y su consulta.
4. «Las pruebas anteriores pasan contra un store de prueba»: el antecedente es ambiguo; obligaría a inventar qué suite previa debe ejecutarse.

DRY-RUN

Lecturas: decisión y atoms de IR02, servidor y `read_tools` de IR03, API pública de SLDB y pruebas existentes. Cambios previstos: implementar los tres módulos MCP y tres suites de pruebas. Dependencias: IR02 (mecanismo, precondición, nivel de escritura, deshacer) e IR03 (servidor y tools de lectura). Validaciones futuras: pytest contra store de prueba; dry-run sin modificar archivos; rechazo por validación obsoleta; validación de tipos, cardinalidad y condición; reglas según severidad; argumentos tipados; procedencia; error por nivel; ausencia de tools que creen o modifiquen módulos Python.

FUTURO

IR02 entrega la decisión citable y sus atoms; IR06 consume estas tools para poblar la cadena del blog; un humano decide si la edición de clases de modelo se expone por MCP; la validación conjunta y el gate quedan fuera de este nodo.
