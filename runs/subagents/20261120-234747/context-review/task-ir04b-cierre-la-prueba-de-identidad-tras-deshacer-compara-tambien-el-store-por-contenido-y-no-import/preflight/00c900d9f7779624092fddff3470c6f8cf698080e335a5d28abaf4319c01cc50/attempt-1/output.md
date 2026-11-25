REFORMULACION
Propósito: cerrar IR04b corrigiendo la prueba de identidad tras deshacer por MCP. Resultado: en `tests/test_mcp_undo.py`, la prueba compara antes/después tanto cada `.md` como el store por contenido, sin `xfail`, y el digest usa solo la API pública de `sldb`. Repo: `SLDB_1/IR`. Límites: dentro `tests/test_mcp_undo.py` y su helper de digest; fuera `src/specir/mcp_extension.py`, salvo fallo real revelado por la comparación del store, que se informa y arregla dentro de IR04b. Nodo ejecutable `task.code`.

AMBIGUEDADES
1. “el payload o el content hash que exponga sldb.api”: no fija cuál usar ni su firma; obligaría a inventar el método público y el criterio exacto.
2. “para cada documento trackeado”: no indica cómo enumerarlos por API pública; obligaría a inventar la fuente de la lista.
3. “por el mismo criterio de contenido”: no define normalización del store frente al sha256 del texto sin bloque sldb; obligaría a inventar equivalencias.
4. “el ejecutor lo informa y lo arregla dentro del alcance de IR04b”: no dice a quién informa ni si requiere autorización; obligaría a inventar el canal y el permiso.
5. Validación solo lista `tests/test_mcp_undo.py`, pero “Los cuatro archivos de tests pasan”: obligaría a inventar si la validación mínima es uno o cuatro.
6. “el helper de digest que use”: no da ruta ni nombre; obligaría a inventar dónde ubicarlo.

DRY-RUN
Lecturas: `tests/test_mcp_undo.py`; exports de `sldb.api`; `sldb/api/documents/content_hash.py` si aplica; `mcp_extension.py` solo lectura; tests citados. Cambios: capturar store antes/después vía `sldb.api` y compararlo; sustituir `strip_block` por digest público; quitar `xfail` si existe. Dependencias: API pública para enumerar trackeados y obtener payload/hash; fixture de deshacer. Validaciones futuras: ejecutar de a uno los cuatro pytest y commit con `Task-Id`. Sin ejecutar.

FUTURO
El ejecutor futuro produce el diff, el commit y la evidencia de pruebas. El tester valida; el humano/coordinador decide aceptación y, si aparece fallo real del store, autoriza o confirma la ampliación a `src/specir/mcp_extension.py`.
