## REFORMULACION
Propósito: auditar la API pública de SLDB frente a las 11 capacidades de la superficie MCP de specIR, sin diseñar tools ni decidir el contrato final.
Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con 11 filas (necesidad, estado cerrado, evidencia, brecha, acción, handoff) y, si hay no disponibles, una única nota a SLDB.
Raíz: `/home/jp/proyectos/SLDB_1/IR`. Corpus de solo lectura: `../sldb/src/sldb/api/*.py` y docs listados; `../pron/source/spec/14-superficie-mcp.md` §1/§4.
Límites: no código; no editar otros repos; no módulos internos de SLDB; no importar/ejecutar pron; un solo archivo escrito; un solo envío sin reintento.

## AMBIGUEDADES
1. «Si ese texto no permite decidir equivalencia»: no define equivalencia (¿funcional con `kb_undo`? ¿suficiencia contractual?). Obligaría a inventar el criterio.
2. «con rechazo atómico»: no fija evidencia admisible sin ejecutar. Obligaría a inventar definición o umbral.
3. «una única nota»: no aclara si admite N filas ni tope; el formato dice «estas filas». Obligaría a inventar el máximo.
4. «El contrato final de escritura queda fuera solo como decisión de producto de IR02»: «solo como» no aclara qué parte entra en el informe. Obligaría a fijar alcance.
5. «## Capacidad N: <nombre>»: no indica de dónde sale `<nombre>`. Obligaría a inventar nomenclatura.

## DRY-RUN
Lecturas: `git rev-parse`/`branch`/`status` en `../sldb` con pathspecs del corpus; archivos del corpus; `addressability_model.md`; spec pron §1/§4; docstrings públicos.
Cambios: crear el informe; si hay brechas, componer `message_body` y ejecutar una vez `deskops message send`; si falla, celdas `ERROR` y resumen de fallo.
Dependencias: git, deskops, paths existentes; SHA-256 solo de modificados/untracked.
Validaciones futuras: 11 filas, coherencia estado/acción, citas reales, snapshot con commit/status/hashes, mismo ID, fallo sin cierre.

## FUTURO
IR02 consume el informe para el contrato de escritura. SLDB decide la extensión vía suggestion. Un humano decide si el envío falla o hay contradicción documental. Es tarea ejecutable, no agregado.
