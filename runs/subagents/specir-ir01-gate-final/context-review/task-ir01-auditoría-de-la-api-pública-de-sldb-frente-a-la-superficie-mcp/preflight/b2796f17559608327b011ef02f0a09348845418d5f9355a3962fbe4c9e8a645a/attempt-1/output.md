REFORMULACION

Nodo ejecutable `task.docs`, no agregado. Propósito: auditar la API pública de SLDB frente a 11 capacidades de la futura superficie MCP de specIR. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con snapshot, matriz de siete columnas, resumen y fuentes; si hay filas no disponibles, enviar una única nota al desk SLDB. Repo: `/home/jp/proyectos/SLDB_1/IR`; se lee `../sldb` y la spec `../pron/source/spec/14-superficie-mcp.md` (§1 y §4). Límites: no leer módulos internos de SLDB para evidencia, no escribir código, no tocar otros repos, no importar/ejecutar pron, no diseñar tools ni decidir política de escritura; solo escribir el informe y, si procede, enviar el mensaje.

AMBIGUEDADES

1. Evidencia documental vs ruta API. “La disponibilidad requiere evidencia directa o composición explícita en docstring sldb.api o doc SLDB listado” frente a “Cada fila disponible cita rutas existentes bajo sldb/src/sldb/api/”. Si una capacidad solo está demostrada en un doc permitido, exigir ruta API obliga a inventar un símbolo o a clasificar mal.
2. Éxito de envío. “path presente y no vacío significa envío exitoso” frente a “código distinto de cero se trata como fallo”. Si hay path y código no cero, hay que inventar precedencia.
3. Niveles de escritura. “escritura confirmada” significa una operación nivel 1 o 2” no define niveles; si pron §4 no los define, obliga a inventar la clasificación de la fila 11.
4. Formato de la nota. “después líneas Necesidad, Rutas/símbolos revisados...” no aclara si “Necesidad” repite el formato `Actor/Entrada/Resultado`; obliga a inventar el cuerpo.

DRY-RUN

Lecturas: comandos git sobre `../sldb` limitados al corpus; todos los `.py` de `../sldb/src/sldb/api/`; los docs listados; spec pron §1 y §4. Cambios previstos: crear el informe; si hay brechas, invocar una vez `deskops message send` y leer `path`. Dependencias: rutas y git disponibles, docstrings/docs públicos, `deskops`, definiciones de pron §4. Validaciones futuras: 11 filas y columnas exactas; estados/acciones; fila 4 separada; snapshot/hashes; fuentes; estructura; nota/ID o resumen sin nota; fallo registrado. Nada ejecutado.

FUTURO

IR02 decide la política y mutabilidad de escritura. El desk SLDB recibe la nota y decide si expone/documenta las brechas. Un humano revisa el informe y resuelve fuentes ausentes. Otro ejecutor corre git, escribe el informe y envía la nota.
