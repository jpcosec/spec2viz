## REFORMULACION

Propósito: auditar la API pública de SLDB frente a las 11 capacidades que necesita la superficie MCP de specIR, sin diseñar tools ni decidir política de escritura. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con snapshot fijado, tabla de columnas exactas Capacidad, Necesidad, Estado, Evidencia, Brecha, Acción, Handoff, y —si hay filas no disponibles— una única nota enviada a desk SLDB con `deskops message send`. Raíz de trabajo: `/home/jp/proyectos/SLDB_1/IR`; fuentes `../sldb` y lectura documental de `../pron`. Límites: solo docstrings públicos de `sldb.api` y docs SLDB enumerados; no leer módulos internos, no importar/ejecutar pron, no tocar otros repos, escribir un solo archivo.

## AMBIGUEDADES

1. «La celda Necesidad usa exactamente `Actor: ...; Entrada: ...; Resultado esperado: ...`»: las 11 capacidades solo dan nombre; obliga a inventar Entrada y Resultado esperado de cada fila.
2. «Resumen enviado exacto: Nota enviada; ID: sldb:<stem>.» y «El informe lista el snapshot»: no se define dónde ni con qué formato viven Resumen y snapshot fuera de la tabla; obliga a inventar la estructura del documento.
3. «pills:\n- desk/contexts/pill-guardrail-...»: las pills se referencian pero quedan fuera del corpus permitido; obliga a decidir si obligan o se ignoran, e inventar su contenido si se honran.
4. «Pregunta al desk, TaskDoc: task-ir01-...»: no hay plantilla para el texto de «Pregunta al desk»; obliga a redactar la pregunta por fila no disponible.
5. «La fila 4 informa por separado la evidencia y disponibilidad de select_documents y search; no combinar sus resultados en una sola afirmación»: no se especifica cómo representar dos suboperaciones en celdas únicas; obliga a inventar el formato interno.
6. «Si falla/no hay path»: no define qué salida JSON cuenta como ausencia de path; obliga a inventar el criterio de detección.

## DRY-RUN

Lecturas: `../sldb/src/sldb/api/*.py` (docstrings públicos), `../sldb/docs/README.md`, `addressability_model.md` y los `architecture/*.md` enumerados; `../pron/source/spec/14-superficie-mcp.md` secciones 1 y 4; `git -C ../sldb rev-parse HEAD`, `branch --show-current`, `status --short` limitado al corpus. Cambios previstos: crear el informe con snapshot, once filas y Resumen; si hay filas no disponibles, componer `message_body` y enviar una sola vez. Dependencias: estado real de `../sldb`, evidencia en docstrings, salida JSON de deskops. Validaciones futuras: once filas, estados/acciones cerrados, evidencia citada, fila 4 dual, hashes si hay dirty, mensaje único/ID, ausencia de imports o ejecución de pron.

## FUTURO

IR02 decide la política de escritura; el desk SLDB evalúa e integra extensiones; deskops produce path/ID o error de envío; `../sldb` produce commit, branch y status; un humano valida el informe final.
