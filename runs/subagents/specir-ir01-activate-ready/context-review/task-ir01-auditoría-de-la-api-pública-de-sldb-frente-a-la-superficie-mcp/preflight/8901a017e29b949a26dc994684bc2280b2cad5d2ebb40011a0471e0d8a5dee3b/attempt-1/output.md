## REFORMULACION
**Propósito:** auditar la API pública de SLDB frente a las necesidades de la futura superficie MCP de specIR y documentar una matriz de once capacidades. **Resultado:** `docs/auditoria/sldb-api-frente-a-mcp.md`, con snapshot, evidencia, estados y handoff; si hay brechas, una única nota al desk de SLDB. **Repo:** ejecutar desde `/home/jp/proyectos/SLDB_1/IR`, inspeccionando el working tree de `../sldb`; no modificar otros repos. **Límites:** leer solo API pública y documentos declarados, más la sección 4 de la spec de pron; no leer módulos internos de SLDB ni importar/ejecutar pron; escribir solo el informe; no ejecutar checks; no reintentar el envío.

## AMBIGUEDADES
1. «exactamente once capacidades» no enumera las once ni identifica las filas 7, 8, 10 y 11; obligaría a inventar la lista y el tema de cada fila.
2. «Cada fila usa uno de los estados cerrados» no fija el vocabulario exacto; obligaría a inventar estados y el mapeo desde «ofrece/extender/falta».
3. «mandar un mensaje a sldb» y «deskops message send» no definen herramienta, destinatario ni formato de respuesta; obligaría a inventar la invocación y el parseo del ID.
4. «el ID exacto aparece en Resumen» no aclara si «Resumen» es una sección del informe o del mensaje; obligaría a inventar su ubicación.
5. «todas las rutas parten de esa raíz» junto a «../pron/source/spec/...» no fija si la ruta externa se resuelve desde IR o desde otro directorio; obligaría a asumir una resolución.

## DRY-RUN
**Lecturas previstas:** estado git de `../sldb`; archivos Python bajo `src/sldb/api/`; README y documentos de arquitectura enumerados; sección 4 de la spec de pron. **Cambios previstos:** crear la carpeta `docs/auditoria/` si falta y escribir únicamente el informe. **Dependencias:** git, sistema de archivos, documentación de SLDB y mecanismo de envío a deskops si hay brechas. **Validaciones futuras:** once filas con todos los campos; estados y acciones permitidos; citas verificables; snapshot/hashes; mensaje único con ID o resúmenes exactos de no-envío/error; fuentes listadas y ausencia de lectura interna/importación. No se ejecuta nada.

## FUTURO
El ejecutor producirá la matriz y el resultado del envío. Un humano o nodo planificador debe resolver antes las ambigüedades —lista de capacidades, vocabulario de estados y contrato de envío—. El desk de SLDB responde las brechas detectadas.
