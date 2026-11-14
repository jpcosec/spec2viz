## REFORMULACION

Propósito: auditar la API pública de SLDB frente a las 11 capacidades que necesita la superficie MCP de specIR. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md`, con matriz de exactamente 11 filas (estado, evidencia, brecha, acción y handoff) y, si hay filas no disponibles, una única nota al desk de SLDB. Repo: IR; único archivo escrito. Límites: no se toca código ni otros repos, no se leen módulos internos de SLDB, no se importa ni ejecuta pron; de pron solo se lee `14-superficie-mcp.md` §§1 y 4.

Nodo ejecutable individual, no agregado.

## AMBIGUEDADES

1. «nombre de fila igual a la frase tras su número» frente a «cada fila incluye capacidad»: no queda claro si «capacidad» es la frase completa o una etiqueta breve. Obligaría a inventar el nombre canónico de cada fila.
2. «Handoff disponible: EM DASH literal —»: la redacción mezcla el nombre del carácter con el valor. Obligaría a decidir si el handoff debe ser exactamente `—` o el texto «EM DASH».
3. «Si cualquier comando git falla»: no especifica si un fallo parcial invalida solo ese campo o todo el bloque de snapshot. Obligaría a inventar la política de fallback.
4. «message_body contiene solo esas filas»: no aclara el orden de las secciones cuando hay varias filas no disponibles. Obligaría a inventar un criterio de orden.

## DRY-RUN

Lecturas: los `.py` bajo `../sldb/src/sldb/api/`, los diez docs SLDB listados, `../pron/source/spec/14-superficie-mcp.md` §§1,4, las dos pills y los dos átomos; `git -C ../sldb rev-parse HEAD`, `branch --show-current` y `status --short --untracked-files=all` acotado al corpus.

Cambios previstos: crear/sobrescribir `docs/auditoria/sldb-api-frente-a-mcp.md` con snapshot, fuentes, 11 filas y resumen. Dependencias: presencia de `../sldb`, `../pron`, git y `deskops` con `message send`. Validaciones futuras: once filas, estados y acciones cerrados, evidencia por símbolo público, fila 4 con doble evidencia, hashes SHA-256 si hay modificados, y nota única con ID repetido si hay brechas.

## FUTURO

El desk de SLDB decide e integra las extensiones solicitadas. IR02 decide la política final de escritura. Un humano revisa y cierra la tarea; el envío de la nota y su ID quedan como evidencia externa.
