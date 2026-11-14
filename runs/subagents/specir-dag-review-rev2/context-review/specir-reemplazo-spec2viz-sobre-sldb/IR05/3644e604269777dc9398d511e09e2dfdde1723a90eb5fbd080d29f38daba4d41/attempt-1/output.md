REFORMULACION
Propósito: decidir una taxonomía canónica de procedencia para specIR y una regla de divergencia entre modelo y código fuente. Resultado: `docs/decisiones/procedencia-y-divergencia.md`, con taxonomía, equivalencias, representación de lo desconocido, promoción de inferencia a validada, divergencia y carencias de SLDB. Repo: `specIR`. Límites: no implementar extractores; el nodo es una decisión documental, no ejecutable. Depende de IR01 para la matriz de auditoría.

AMBIGUEDADES
1. “Los tres atoms existen”: no define qué es un atom ni su soporte. Obligaría a inventar si son secciones del `.md`, archivos separados o entradas de otro formato.
2. “cómo una inferencia pasa a validada, y por acción de quién”: no nombra al actor ni el mecanismo. Obligaría a inventar rol, permisos y evidencia exigida.
3. “qué prevalece cuando modelo y código discrepan”: no aclara si “modelo” es el store extraído, el modelo de dominio o la representación visual. Obligaría a inventar el criterio de precedencia y sus excepciones.
4. “un nodo cuya fuente cambió”: no define el efecto esperado —marcar, invalidar, conservar o bloquear— ni si afecta hechos validados. Obligaría a inventar la regla operativa.
5. “las anclas de código de SLDB”: no precisa si son rutas, líneas, hashes u otro identificador. Obligaría a inventar el formato de anclaje y su relación con la evidencia.

DRY-RUN
Nodo no ejecutable: un ejecutor futuro produciría solo el documento de decisión. Lecturas previstas: sección 7 de `fundamentos_modelado_semantico_mcp.md`, fase 5 de `Plan_IR.md`, `sldb/src/sldb/models/provenance.py` y la matriz de IR01. Cambio previsto: redactar la taxonomía, equivalencias, regla de desconocido, promoción, divergencia y fila de carencia si aplica. Dependencia: IR01. Validaciones posteriores: existencia de los tres atoms, tabla de equivalencias, regla de desconocido/promoción con actor, regla de fuente cambiada y carencia trazada a la matriz. Sin ejecución.

FUTURO
IR06 deberá citar esta taxonomía al crear tipos y datos; IR08 e IR09 deberán aplicarla a procedencia y divergencia. Un humano o nodo posterior deberá ratificar la decisión y, si no queda fijado aquí, designar al actor que valida inferencias.
