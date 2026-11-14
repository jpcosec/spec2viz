REFORMULACION
Encargo ejecutable (task.docs; no agregado): auditar la API pública de SLDB frente a 11 capacidades del cliente MCP de specIR, con el agente MCP como actor. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md`, matriz de exactamente 11 filas con capacidad, necesidad, estado (disponible, requiere-extensión-en-SLDB o faltante), evidencia, brecha, acción y handoff. Repo de trabajo: `/home/jp/proyectos/SLDB_1/IR`; fuentes en `../sldb` y única spec externa `../pron/source/spec/14-superficie-mcp.md` (§1 y §4). Límites: no diseñar tools, escribir código, editar otros repos, importar/ejecutar pron ni leer módulos internos de SLDB; solo escribir el informe. Si hay brechas, una única nota a `sldb` mediante deskops.

AMBIGUEDADES
1. "si se envía usa ID sldb:<id>" frente a "Resumen de éxito exacto: Nota enviada; ID: sldb:<id>". ¿Cuál es la cadena exacta del Resumen? Obliga a inventar el formato.
2. "Dirty incluye tracked y untracked dentro del corpus." No define "corpus": ¿todo `../sldb`, solo API/docs enumerados? Obliga a fijar alcance de status y hashes.
3. "crear modelos... y registrar clases Python existentes" frente a "Fila 7 busca símbolos Python exactos sldb.api.create_model, add_model, validate_model_draft y promote_model_draft": no hay símbolo para registro de clases. Obliga a decidir evidencia de esa suboperación.
4. "buscar documentos por filtros soportados por sldb.api.where/search": la barra no aclara si son dos APIs, una ruta o una función. Obliga a inventar la superficie exacta a inspeccionar.

DRY-RUN
Lecturas: TaskDoc, todos los Python de `../sldb/src/sldb/api/`, los docs SLDB enumerados y la spec pron §1/§4. Cambios previstos: solo el informe. Dependencias: git, árbol `../sldb`, spec pron y CLI deskops. Secuencia hipotética: capturar commit/branch/status; hashear archivos modificados/untracked que correspondan; inspeccionar fuentes; construir y clasificar las 11 filas; si hay no disponibles, componer `message_body` y ejecutar una sola vez `deskops message send ...`; registrar ID o ERROR; escribir informe. Validaciones futuras: 11 filas exactas, estados/acciones cerrados, evidencia con rutas/símbolos reales, snapshot/hashes, resumen exacto y uso de una única nota.

FUTURO
El desk SLDB decide si acepta o extiende la API y responde la nota; un humano valida el informe. El contrato final de escritura y el diseño posterior de tools MCP quedan fuera de este nodo y los consume otro nodo. Si deskops falla, la tarea permanece abierta para decisión humana.
