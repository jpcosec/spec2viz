REFORMULACION

Propósito: auditar la API pública de SLDB frente a las capacidades que necesitará la futura superficie MCP de specIR, antes de diseñarla. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con una matriz de exactamente once capacidades (capacidad, necesidad con actor/entrada/resultado, estado, evidencia, brecha, acción, referencia de handoff). Repo: specIR en `/home/jp/proyectos/SLDB_1/IR`; solo se escribe ahí. Límites: se leen `../sldb` (API pública y docs) y `../pron/source/spec/14-superficie-mcp.md` sección 4; no se abren módulos internos de SLDB, no se importa/ejecuta pron, no se editan otros repos; cambios en SLDB se piden con `deskops message send --to sldb`.

AMBIGUEDADES

1. "El informe contiene exactamente once capacidades" — solo se nombran "fila 7", "fila 8", "fila 10", "fila 11"; las filas 1-6 y 9 y el orden no aparecen. Obliga a derivarlas de la sección 4 de la spec pron (fuente declarada) o a inventarlas.
2. "dirty incluye tracked y untracked dentro del corpus" — "corpus" no se define; obliga a decidir si es solo `../sldb` o el conjunto de fuentes.
3. "Registrar SHA-256 de cada archivo inspeccionado modificado/untracked" — no aclara si incluye el documento pron (fuera del repo sldb). Obliga a inventar la cobertura de hashes.
4. "la raíz StoreFingerprint.store_hash se acepta y compara dentro de la misma operación de escritura" — no se indica qué método concreto la materializa; el auditor debe inferirlo del docstring, con riesgo de invención.
5. "Si el mensaje falla o no retorna ID" — no se define qué salida de `deskops message send` cuenta como ID. Obliga a inventar el criterio de éxito del envío.

DRY-RUN

1. Capturar snapshot git de `../sldb` (HEAD, branch, status --short --untracked-files=all); si falla, registrar y hashear lo inspeccionado.
2. Leer recursivamente `../sldb/src/sldb/api/*.py`, `../sldb/docs/README.md`, `addressability_model.md`, los `.md` de `docs/architecture/` listados y la sección 4 de la spec pron.
3. Verificar por fila símbolos exactos (7: create_model/add_model/validate_model_draft/promote_model_draft; 8: check_store/check_edges; 10: StoreFingerprint.store_hash; 11: contrato kb_undo) y docstrings para composición.
4. Calcular SHA-256 de modificados/untracked inspeccionados.
5. Crear `docs/auditoria/` y escribir la matriz: disponibles → usar/componer con handoff `—`; no disponibles → requiere-extensión/faltante con handoff `sldb:<id>`.
6. Si hay no disponibles, enviar un único mensaje a sldb y capturar ID; si falla/no ID, handoff `ERROR` y Resumen "Nota no enviada; tarea abierta…".
7. Si todas disponibles, no enviar y Resumen "No se envió nota: todas las capacidades están disponibles".

Validaciones futuras: once filas completas, estados/acciones cerrados, evidencia con rutas reales bajo `src/sldb/api/`, snapshot y hashes, mensaje único si aplica, sin lectura de internos ni import/ejecución de pron.

FUTURO

El desk de SLDB decide y agenda las extensiones pedidas. Otro nodo (diseño de la superficie MCP de specIR) consume la matriz como entrada. Un humano verifica el mensaje/ID y cierra la tarea; si el envío falló, decide si reintentar (el plan lo prohíbe). La suficiencia de una "composición" puede requerir revisión humana de docstrings.
