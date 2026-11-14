REFORMULACION

Encargo: auditar la API pública de SLDB frente a las 11 capacidades que necesitará la superficie MCP de specIR, produciendo una matriz en `docs/auditoria/sldb-api-frente-a-mcp.md` con estado, evidencia, brecha, acción y handoff por fila. Repo de trabajo: `/home/jp/proyectos/SLDB_1/IR`; fuentes: `../sldb` y la spec `../pron` indicada. No es agregado ni paquete: es una tarea documental ejecutable. Límites: no escribir código, no cambiar otros repos, no leer módulos internos de SLDB, no importar/ejecutar pron, no diseñar tools ni decidir la política final de escritura. Solo se escribe el informe; si hay brechas, se envía un único mensaje por `deskops`.

AMBIGUEDADES

1. «las filas 6, 10 y 11 sí inventarían las APIs existentes frente a las necesidades declaradas.» Obliga a inventar si «inventarían» significa inventar APIs o auditarlas; choca con «no cita rutas o símbolos inventados».
2. «Disponibilidad requiere evidencia directa o composición explícita en docstring sldb.api o doc SLDB listado.» y «Fuentes de composición: solo docstrings públicos sldb.api y docs SLDB listados.» Obliga a decidir si una secuencia inferida de varios docstrings cuenta como composición explícita o si solo vale una mención literal.
3. «Para fila 11 no inferir detalles ausentes en pron §4» junto a «si SLDB ofrece función relacionada pero no documenta el comportamiento requerido, clasificar requiere-extensión-en-SLDB». Si pron §4 no detalla el comportamiento, obliga a inventar cuál es el requisito para clasificar.

DRY-RUN

Lecturas: metadatos git de `../sldb`; todos los `.py` bajo `../sldb/src/sldb/api/`; los docs SLDB listados; `../pron/source/spec/14-superficie-mcp.md` §§1 y 4. Cambios previstos: crear solo el informe; eventualmente `deskops message send` crea la nota. Dependencias: git, SHA-256, rutas relativas y `deskops`. Validaciones futuras: 11 filas exactas, estados/acciones cerrados, citas existentes, snapshot y hashes, formato del mensaje e ID, y ausencia de módulos internos o ejecución de pron.

FUTURO

`deskops message send` produce el `path`/ID o el error que se registrará; el desk de SLDB decide integrar o documentar las brechas; IR02 decide la política de escritura; el revisor valida la matriz y el cierre.
