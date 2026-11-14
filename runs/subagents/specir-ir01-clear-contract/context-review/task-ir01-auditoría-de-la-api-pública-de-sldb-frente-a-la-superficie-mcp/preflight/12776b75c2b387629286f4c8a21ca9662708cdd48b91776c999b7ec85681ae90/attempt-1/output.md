## REFORMULACION

**Propósito:** auditar, capacidad por capacidad, la API pública de SLDB frente a la superficie MCP que necesita specIR, sin reimplementar lo general ni depender de módulos internos de SLDB o de pron.

**Resultado:** `docs/auditoria/sldb-api-frente-a-mcp.md`, con exactamente 11 filas nombradas según el encargo; cada una con necesidad, estado cerrado (`disponible`, `requiere-extensión-en-SLDB`, `faltante`), evidencia permitida, brecha, acción y handoff. Si hay filas no disponibles, una única nota `deskops message send` con formato exacto y su `sldb:<stem>`.

**Repo:** ejecutar desde `/home/jp/proyectos/SLDB_1/IR`; leer el corpus indicado de `../sldb` y, como único documento externo, `../pron/source/spec/14-superficie-mcp.md` §1/§4.

**Límites:** no diseñar tools MCP ni decidir la política de escritura; no escribir código ni modificar otros repos; no leer módulos internos de SLDB; no importar ni ejecutar pron; escribir solo el informe; enviar como máximo un mensaje, sin reintentos.

## AMBIGUEDADES

1. “fallo es el texto literal ERROR” frente a “celdas ERROR” y “Acciones: usar/componer para disponible; solicitar-extensión para no disponible”. Obliga a inventar qué celdas exactas pasan a `ERROR` y si se conserva el estado/acción original de cada fila cuando falla el envío.

2. “si la referencia pron no define suficiente semántica o SLDB no ofrece operación, clasificar no disponible” y “solicitar-extensión para no disponible”. Si SLDB sí ofrece una operación pero la semántica de pron es insuficiente, obliga a inventar si la brecha es de SLDB o de pron y qué pregunta concreta enviar.

3. “Si git falla, registrar el error y hashear todos los archivos del corpus.” No indica cómo representar commit/branch ausentes en el informe; obliga a inventar marcadores o formato.

## DRY-RUN

Sin ejecutar: leería el TaskDoc, los archivos Python bajo `sldb.api`, los documentos SLDB listados y las secciones §1/§4 de la spec pron. Capturaría commit, branch y `git status` limitado al corpus; si git falla, registraría el error y hashearía todo el corpus; si hay dirty, SHA-256 de modificados/untracked. Redactaría 11 filas con evidencia citable, estados y acciones; si hay no disponibles, compondría el cuerpo exacto y ejecutaría una sola vez el mensaje, registrando `path`/stem o el fallo. Dependencias: disponibilidad de archivos, git, `deskops` y pron. Validaciones futuras: 11 filas, estados/acciones correctos, evidencia existente, snapshot y hashes, nota única e ID, fuentes revisadas y ausencia de lecturas internas/imports.

## FUTURO

El desk de SLDB recibe y responde la sugerencia. IR02 decide la política final de escritura. Un humano valida el cierre, resuelve un fallo de envío no reintentado y aprueba el informe.
