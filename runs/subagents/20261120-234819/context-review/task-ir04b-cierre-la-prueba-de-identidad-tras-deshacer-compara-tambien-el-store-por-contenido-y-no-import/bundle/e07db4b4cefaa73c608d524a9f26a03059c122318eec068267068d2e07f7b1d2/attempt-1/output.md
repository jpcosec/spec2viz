## REFORMULACION
Propósito: cerrar IR04b corrigiendo la prueba de identidad tras deshacer. Resultado: en `tests/test_mcp_undo.py`, comparar antes/después tanto cada `.md` como el store por contenido, y calcular digests usando solo API pública de `sldb`, sin imports internos. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`. Límites: dentro, `tests/test_mcp_undo.py` y su helper de digest; fuera, el código de deshacer de `src/specir/mcp_extension.py`, salvo fallo real revelado por la comparación. Deben pasar cuatro archivos de tests y commit con trailer `Task-Id`. El nodo es una tarea ejecutable `task.code`, no un agregado.

## AMBIGUEDADES
1. “su payload o el content hash que exponga sldb.api”: no se fija la API pública exacta ni si payload y hash son equivalentes; obliga a inventar nombre, forma de enumerar documentos trackeados y criterio de comparación.
2. “la función de sldb/api/documents/content_hash.py si se exporta, o el payload por sldb.api”: no consta que esté exportada; obliga a decidir su disponibilidad y alternativa sin verificar.
3. “salvo que la comparación del store revele un fallo real; en ese caso el ejecutor lo informa y lo arregla”: “fallo real” y el destinatario del informe no están definidos; obliga a inventar umbral y canal.
4. El Rationale menciona “pill-guardrail-specir-solo-usa-la-api-pública-de-sldb”, pero el frontmatter declara `pills: []`; obliga a decidir si debe ligarse y con qué contenido.
5. La Validación lista solo `tests/test_mcp_undo.py`, mientras “Done When” exige “Los cuatro archivos de tests pasan”; obliga a decidir el conjunto de cierre, aunque p4 ya nombra los cuatro.

## DRY-RUN
Lecturas previstas: TaskDoc, `tests/test_mcp_undo.py`, exports públicos de `sldb.api`, `src/specir/mcp_extension.py` solo si falla la comparación. Cambios previstos: snapshot del `.md` sin bloque sldb y del store por documento trackeado; comparación antes/después; sustitución de `strip_block` de `sldb.models.provenance_block` por API pública. Dependencias: API pública para enumerar/hashear contenido y comportamiento estable de undo MCP. Validaciones futuras: ejecutar el comando pytest indicado y los cuatro tests de p4 de a uno; comprobar ausencia de imports internos; commit con `Task-Id`. No se ejecuta nada.

## FUTURO
Un ejecutor implementará, probará y commiteará. Un tester/revisor validará. Un humano o coordinador decidirá si la API pública no basta, si hay que ampliar alcance por un fallo real o cómo aplicar la pill no incluida.
