# Resultado (intento 2 de cierre)
Archivo cambiado: tests/test_mcp_undo.py (commit en la rama deskops/deskops-e-ac8d469581e4-a2).
- md_digest ya no usa load_runtime_documents (omitía en silencio los modelos heredados, de ahí 53 vs 506 documentos). Enumera el store con sldb.api.select_documents(store, {}) (filas export_id/model/name/path, sin importar modelos) y hashea el texto de cada archivo sin el bloque sldb (md_text_without_block local). Las claves quedan estables entre instantáneas.
- Sin imports de sldb.models.*. Quedan en test_the_store_after_an_undo_passes_the_checks... imports de sldb.mcp.changes/context/server (ya existían, son del test de validadores, no del digest): el supervisor decide si cuentan contra el pill.
- Validación: ver validation.log; los cuatro archivos pasan.
- Nota de entorno: en el worktree faltaba runs/subagents/exec-deskops-t-da81f2bd34e0-testing/run.md (sin commitear en el checkout principal) y el fixture de copia fallaba con "Skipped missing documents". Lo copié temporalmente para validar y lo borré; no está en el commit. Hace falta commitearlo en main o los tests fallarán en un worktree limpio.
- Venv: hubo que instalar además mcp y pytest-asyncio.
- run_id: exec-deskops-e-ac8d469581e4-a2; session / session_sha256: no disponibles para el ejecutor.
