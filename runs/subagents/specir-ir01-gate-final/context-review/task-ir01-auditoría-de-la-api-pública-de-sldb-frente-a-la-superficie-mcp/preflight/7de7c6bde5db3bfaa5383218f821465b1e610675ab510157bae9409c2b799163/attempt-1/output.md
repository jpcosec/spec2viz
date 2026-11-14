REFORMULACION
El nodo es una tarea documental ejecutable, no un agregado. Debe auditar la API pública de SLDB frente a 11 capacidades MCP de specIR y producir `docs/auditoria/sldb-api-frente-a-mcp.md` desde `/home/jp/proyectos/SLDB_1/IR`. Resultado: matriz de siete columnas con snapshot, resumen y fuentes, usando estados/acciones cerrados y evidencia permitida. Límites: leer solo el corpus SLDB indicado y pron §1 y §4; no leer módulos internos, no importar/ejecutar pron, no tocar otros repos, no diseñar tools ni decidir política de escritura; escribir solo ese informe y, si hay brechas, enviar una única nota a sldb.

AMBIGUEDADES
1. «los tres metadatos como desconocido/no disponible y el error completo; hashear todos los archivos del corpus». No dice cuáles son los tres (¿commit, branch, status?) ni si la fecha UTC también queda desconocida, ni dónde/cómo registrar el error completo; obligaría a inventar.
2. «Fuentes revisadas enumera solo documentos efectivamente leídos» frente a «Cada fila disponible cita rutas existentes bajo sldb/src/sldb/api/». No aclara si los módulos Python cuentan como documentos y deben listarse; obligaría a inventar el criterio.
3. «leer únicamente las secciones 1 y 4 (no 1–4) de ../pron/source/spec/14-superficie-mcp.md como documento externo» frente a «Fuentes revisadas enumera solo documentos efectivamente leídos». No aclara si la spec pron debe aparecer en Fuentes revisadas o excluirse por externa; obligaría a inventar.

DRY-RUN
Un ejecutor futuro leería TaskDoc, pills, corpus exacto, metadatos Git y pron §1/§4; abriría solo API pública y docs listados; construiría 11 filas con nombre canónico, necesidad `Actor/Entrada/Resultado`, evidencia, brecha, acción y handoff; aplicaría severidad de fila 4 y reglas de no disponibilidad. Cambio previsto: crear el informe con estructura fijada. Dependencias: `../sldb` y `../pron` presentes, Git y `deskops` disponibles. Si hay filas no disponibles, generaría `message_body` exacto y enviaría una vez; si falta path/JSON/exit 0, registraría fallo y dejaría la tarea abierta. Validaría: 11 filas, columnas, estados/acciones, citas existentes, cadenas exactas, snapshot/hashes y ausencia de escrituras extra. No ejecutaría código SLDB ni importaría pron.

FUTURO
Otro nodo ejecutor producirá el informe y la posible nota; el desk SLDB decide/implementa extensiones o documentación; IR02 decide la política de escritura; un humano valida el cierre. La respuesta del desk no forma parte de este nodo.
