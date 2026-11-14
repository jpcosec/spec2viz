REFORMULACION  
Propósito: auditar la API pública de SLDB frente a 11 capacidades de la superficie MCP de specIR. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con matriz de columnas exactas, snapshot y, si hay brechas, una nota única al desk SLDB. Repo: solo IR; se lee el corpus permitido de `../sldb` y las secciones 1 y 4 de `../pron/source/spec/14-superficie-mcp.md`. Límites: no código, no tocar otros repos, no módulos internos SLDB, no importar/ejecutar pron, no diseñar tools ni decidir política de escritura. No es agregado ni paquete: es una tarea de documentación ejecutable.

AMBIGUEDADES  
1. “después líneas Necesidad, Rutas/símbolos revisados, Brecha, Pregunta al desk, TaskDoc” no fija formato literal ni contenido de la pregunta; obliga a inventar sintaxis, separadores y redacción de “Pregunta al desk”.  
2. “Registrar la fecha/hora UTC del snapshot” no dice si se toma antes o después de las lecturas ni con qué comando; obliga a inventar el instante y el método.  
3. “excluir número, paréntesis y separador final” frente a “quita solo el marcador numérico inicial `(N)` … cualquier paréntesis dentro de la frase se conserva”; obliga a decidir si se eliminan paréntesis internos del nombre de capacidad.  
4. “matriz que diga … si la API pública … ya lo ofrece, hay que extenderlo en SLDB, o falta” no fija por sí sola las etiquetas; aunque luego se cierran los estados, obliga a mapear la formulación narrativa a los tres estados.

DRY-RUN  
Lecturas: TaskDoc, rituales enrutados, pills, átomos, corpus exacto de `../sldb` y secciones 1 y 4 de pron. Cambios previstos: solo crear/editar `docs/auditoria/sldb-api-frente-a-mcp.md`; no código ni otros repos. Dependencias: git en `../sldb`, SHA-256 y `deskops message send`. Validaciones futuras: 11 filas, columnas y estados/acciones, evidencia por fila y fila 4 separada, snapshot/hashes, nota única si hay brechas, handoff/ID o error. Sin ejecutar nada.

FUTURO  
Otro nodo ejecutor hará lecturas, matriz, snapshot y envío. El desk SLDB decide e integra extensiones o documentación; IR02 decide la política de escritura.
