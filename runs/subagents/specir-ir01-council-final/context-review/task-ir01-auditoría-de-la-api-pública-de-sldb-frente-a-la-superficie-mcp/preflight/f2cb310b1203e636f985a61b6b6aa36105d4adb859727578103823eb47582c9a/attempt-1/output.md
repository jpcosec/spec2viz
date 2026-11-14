REFORMULACION
Propósito: auditar la API pública de SLDB frente a 11 capacidades que necesita la superficie MCP de specIR y dejar una matriz de decisión. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con 11 filas —capacidad, necesidad, estado, evidencia, brecha, acción y handoff—, snapshot del corpus SLDB y, si hay filas no disponibles, una nota al desk SLDB con ID o error. Raíz: `/home/jp/proyectos/SLDB_1/IR`; corpus `../sldb/src/sldb/api/*.py` y docs SLDB listados; único doc externo `../pron/source/spec/14-superficie-mcp.md` §§1,4. Límites: escribir solo ese informe; no tocar código ni otros repos; no leer módulos internos SLDB; no importar/ejecutar pron; no diseñar tools ni decidir política de escritura —eso es de IR02—.

AMBIGUEDADES
1. «leer ../pron/source/spec/14-superficie-mcp.md §§1,4»: no se adjunta ni aclara si son secciones 1 y 4 o 1–4; obligaría a inventar el alcance.
2. «Tras envío, repetir el mismo sldb:<stem> en filas no disponibles»: no dice en qué campo —¿handoff?— ni si también en el mensaje; obligaría a inventar la ubicación.
3. «excluir número, paréntesis y separador final»: los únicos paréntesis visibles son los marcadores «(1)»; no queda claro si excluye paréntesis internos; obligaría a decidir el nombre canónico.
4. «deshacer escritura confirmada de kb_undo/forma undo»: no define «kb_undo/forma undo» ni su fuente; obligaría a inventar la operación objetivo de la fila 11.
5. «inventarían (es decir, registrarían) las APIs existentes»: verbo opaco; obligaría a decidir si es inventariar o crear.
6. «La decisión final de política de escritura queda fuera solo como decisión de producto de IR02»: no precisa si la matriz puede recomendar; obligaría a inventar el límite.
7. «doc SLDB listado»: remite a una lista no incluida en el TaskDoc; obligaría a inventar qué docs cuentan.

DRY-RUN
Lecturas: los `.py` de `sldb/api` y los docs SLDB del corpus; pron §1 y §4. Cambios: crear/editar solo `docs/auditoria/sldb-api-frente-a-mcp.md`. Dependencias: `git -C ../sldb` (`rev-parse`, `branch`, `status`), SHA-256 de modificados/untracked, `deskops message send`. Validaciones futuras: 11 filas exactas; estados/acciones cerrados; fila 4 con doble evidencia y estado más severo; snapshot con commit/branch/fecha/status/hashes; nota única solo con no disponibles e ID exacto; error registra código, stderr, stdout y fecha. Sin ejecutar.

FUTURO
IR02 decide la política de escritura. El desk SLDB recibe la nota y decide extensiones. Un ejecutor futuro corre git/deskops y escribe el informe. Un humano revisa la matriz y cierra o reabre.
