## REFORMULACION

Tarea documental ejecutable —no agregado— del repo specIR, en la raíz `/home/jp/proyectos/SLDB_1/IR`. Propósito: auditar once capacidades necesarias para la futura superficie MCP de specIR frente a la API pública de SLDB. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md`, con una matriz de once filas; cada fila declara capacidad, necesidad con actor/entrada/resultado, estado cerrado, evidencia, brecha, acción y referencia de handoff. Límites: solo se lee `../sldb/src/sldb/api/` y los documentos listados; `../pron/source/spec/14-superficie-mcp.md` se lee solo como documento; no se abren módulos internos de SLDB, no se importa/ejecuta pron, no se editan otros repos ni se diseña la superficie MCP. Si hay filas no disponibles, se envía un único mensaje al desk de SLDB y se registra su ID; si no las hay, se usa `—`.

## AMBIGUEDADES

1. «crear/editar modelos según el nivel 3 de pron §4»: no identifica documento ni contenido del nivel 3; obliga a inventar qué permite ese nivel.
2. «la regla de §1 de que escrituras por forma dejan MoveDoc»: no nombra el documento cuyo §1 se cita; obliga a inventar la regla normativa.
3. «directamente o por composición documentada»: no fija qué cuenta como composición documentada; obliga a decidir si encadenar llamadas públicas basta.
4. «referidas a una única nota»: no aclara si todas las filas no disponibles comparten una nota o si basta una nota por brecha; obliga a elegir el agrupamiento.
5. «La ausencia se justifica contra ese corpus exacto»: «ese corpus» puede referir a los Python de `sldb.api`, a los documentos del Implementation Path o a ambos; obliga a fijar la base de evidencia.

## DRY-RUN

Lecturas previstas: metadatos git de `../sldb` (commit, branch, `git status --short`), fecha UTC; todos los `.py` bajo `../sldb/src/sldb/api/`; `README.md`, `addressability_model.md` y los documentos de arquitectura enumerados; la spec pron 14 solo como referencia. Cambios previstos: crear `docs/auditoria/` si falta y escribir únicamente `sldb-api-frente-a-mcp.md`. Dependencias: `deskops message send --to sldb` solo si alguna fila resulta no disponible. Validaciones futuras: once filas exactas, estados/acciones coherentes, citas a rutas y símbolos existentes, snapshot y hashes si hay modificaciones, mensaje único e ID en Resumen, ausencia de imports internos o ejecución de pron.

## FUTURO

Otro nodo o un humano deberá resolver las ambigüedades de contrato pron §4/§1, decidir si la composición documentada satisface una fila y interpretar la respuesta del desk de SLDB. La extensión o aceptación de brechas queda del lado de SLDB; el cierre de IR01 depende de esa evidencia y de la validación del informe.
