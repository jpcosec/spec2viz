## REFORMULACION
Nodo ejecutable `task.code` (no agregado). Propósito: retirar el servidor MCP propio de specIR y montar sus tools de dominio como extensión de `sldb mcp`, una vez cerrada la tarea espejo A. Resultado: `src/specir/mcp_extension.py` con `register(server, context)` que registra `claims_verified` ante `propose_changes` y las tools `specir_types`/`specir_nodes`; borrar entero `src/specir/mcp`; borrar tests migrados y añadir pruebas con cliente MCP stdio real sobre copia aislada del store. Repo: solo specIR. Límites: no editar sldb ni otros repos; no reescribir servidor/log genéricos; fuera undo (IR04b) e impacto (IR10); sin mocks; el resto de specIR solo usa `sldb.api`.

## AMBIGUEDADES
1. “las tools de dominio que hoy viven en el paquete specir.mcp y no son genéricas (por ejemplo las de IR10 cuando existan)” — no fija inventario ni si las de IR10 se crean ya; obligaría a inventar tools y firmas.
2. “specir_types (tipos de dominio, capa, campos propios, si el store los registra y cuántos documentos tiene)” — “si el store los registra” no define fuente ni forma de respuesta; obligaría a inventar el esquema.
3. “un tipo desconocido es señal unknown_model” — no dice dónde ni cómo se emite; obligaría a inventar canal y formato.
4. “tests/mcp/... se borran porque sldb/tests/mcp tiene su equivalente” — no consta que la equivalencia exista ya en el commit citado; obligaría a asumirla o a editar sldb.

## DRY-RUN
Lecturas: TaskDoc, pills, átomos, rituales, contrato `sldb.mcp.extension`, estado de la tarea espejo A, árbol `src/specir/mcp`, tests actuales y `test_imports`. Cambios: crear extensión; mover `claims_verified` y añadir tools; ajustar `conftest`/`models/blog`; `git rm` de `src/specir/mcp`; borrar tests migrados; añadir `test_mcp_extension` y comprobaciones de imports/scripts. Dependencias: espejo A cerrado, API de extensión estable, cliente MCP stdio y store real aislado. Validaciones futuras: imports sin servidor propio ni `mcp` salvo la extensión; listado de tools por stdio; nivel 0 sin escritura y árbol igual; suite restante verde.

## FUTURO
La tarea espejo A en sldb debe cerrar y publicar el punto de extensión; el desk de sldb responde por cambios allí. IR10 aportará tools de impacto e IR04b las de deshacer. Un humano valida cierre y evidencia de no-escritura; el ejecutor no resuelve ambigüedades.
