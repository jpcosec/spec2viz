# Resultado intento 2 (IR04b)
Commit en la rama deskops/deskops-e-674fcb14989b-a2 (trailer Task-Id). Archivos:
- src/specir/mcp_extension.py
- tests/test_mcp_undo.py
- tests/test_mcp_extension.py

1. Validación 1: el xfail estricto se reemplazó por test_the_documents_and_the_store_have_the_same_content_after_the_undo: sha256 del texto sin bloque sldb (strip_block, criterio de content_hash de sldb), documento por documento, y mismo conjunto de archivos. md_digest usa ese criterio. Pasa, sin xfail.
2. D2-E: el add_batch_validator lanza ValueError con "IR05 D2-E" ante cambios tipados (propose_changes: error de herramienta) y devuelve findings ante BatchChange (apply_changes: rechazo domain de sldb). La descripción de propose_changes se amplía en el sitio con la regla; no se crea WriteTools ni se registra/quita ninguna tool (la pila de undo es la de sldb). No se tocaron los asserts de test_blog_chain ni test_domain_tools.
3. tests/test_mcp_extension.py: la prueba de propose espera ahora error de herramienta con "IR05 D2-E" (renombrada), sin debilitar lo comprobado.

Validación: validation.log, todo verde, corrida de a un archivo.

Para el supervisor / limpieza: para correr las pruebas en el worktree hizo falta (a) copiar run.md de dos RunDocs (runs/subagents/exec-deskops-e-674fcb14989b y exec-deskops-t-ef3b25a2dd59-testing) al worktree, porque la fixture copia solo archivos de git y el store los referencia; (b) un symlink .worktrees/deskops -> ../deskops, porque WORKSPACE=REPO.parent. Ambos quedan SIN commitear en el worktree (untracked) y no están en el commit; el sistema me bloqueó el rm, así que hay que borrar a mano: .worktrees/deskops (symlink) y los dos directorios runs/subagents/exec-... del worktree.
