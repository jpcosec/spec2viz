## REFORMULACION
El nodo debe auditar, en solo lectura, la API pública de SLDB frente a 11 capacidades necesarias para la superficie MCP de specIR y dejar una matriz decisoria. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con Snapshot, Matriz de siete columnas, Resumen y Fuentes revisadas; si hay filas no disponibles, enviar una única nota al desk SLDB y registrar su ID o el error. Repo: IR/specIR; solo se escribe ese archivo. Fuentes: `../sldb/src/sldb/api/`, los docs SLDB enumerados y §§1 y 4 de `../pron/source/spec/14-superficie-mcp.md`. Límites: no código, no cambios en otros repos, no módulos internos de SLDB, no importar/ejecutar pron, no diseñar tools ni política de escritura. Es una tarea documental no ejecutable, sin hijos.

## AMBIGUEDADES
1. “(1) catálogo de modelos y tipos de relación con campos/tipos” frente a “el resultado como el resultado explícito en la misma frase de capacidad”. Esa capacidad es nominal y no enuncia resultado; obligaría a inventar el `Resultado esperado`.
2. “deshacer escritura confirmada de kb_undo/forma undo”. `kb_undo` no se define en el input; obligaría a inventar qué operación o semántica designa si pron §4 no la nombra.
3. “disponible usa usar/componer” no fija si la celda Acción debe contener literalmente `usar/componer` o elegir `usar` o `componer`; obligaría a inventar el criterio de elección.

## DRY-RUN
**Lecturas:** TaskDoc, pills/átomos, todos los `.py` bajo `../sldb/src/sldb/api/`, los docs SLDB listados y §§1 y 4 de la spec pron.
**Cambios previstos:** crear solo `docs/auditoria/sldb-api-frente-a-mcp.md`; no tocar SLDB ni pron.
**Dependencias:** existencia del corpus, Git para snapshot y `deskops` para la nota si hay brechas.
**Validaciones futuras:** 11 filas y columnas exactas; estados/acciones cerrados; fila 4 separada y con estado más severo; evidencia sin símbolos inventados; snapshot y hashes; fuentes revisadas; nota única con ID o error registrado.

## FUTURO
IR02 decide la política final de escritura y mutabilidad. El desk SLDB decide e integra o documenta las extensiones solicitadas. Un humano o nodo de cierre confirma si la respuesta del desk satisface la brecha y si el cambio puede commitearse.
