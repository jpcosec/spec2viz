---
sldb:
  by: agent
  at: '2026-11-20T23:47:12Z'
  authority: generated
  via: create_document
id: atom-ir04b-specir-deshace-por-mcp-aplicando-el-lote-inverso-de-sldb-con-guard-de-contenido
title: 'IR04b: specIR deshace por MCP aplicando el lote inverso de sldb, con guard
  de contenido'
five_wh_one_plus: how
tags:
- system:ir
- topic:mcp
---

# IR04b: specIR deshace por MCP aplicando el lote inverso de sldb, con guard de contenido

## Answer

La extensión MCP de specIR (src/specir/mcp_extension.py) expone deshacer sobre el lote inverso que devuelve sldb (apply_batch y undo_changes de sldb efd5ebb8), con el guard expected_content_hash y el contrato 'mismo contenido salvo procedencia': tras deshacer, cada documento vuelve al mismo contenido sin el bloque sldb, porque sldb re-sella at y via. propose_changes sigue rechazando con un error de herramienta que nombra IR05 D2-E. Partió del trabajo sin commitear de otra sesión (runs/subagents/20261120-ir04b-wip/). Queda una tarea de cierre para que la prueba de identidad compare también el store y no use módulos internos de sldb.
