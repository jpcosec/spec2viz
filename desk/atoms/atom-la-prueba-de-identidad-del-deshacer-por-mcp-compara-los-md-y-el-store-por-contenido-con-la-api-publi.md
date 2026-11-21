---
sldb:
  by: agent
  at: '2026-11-21T00:53:34Z'
  authority: generated
  via: create_document
id: atom-la-prueba-de-identidad-del-deshacer-por-mcp-compara-los-md-y-el-store-por-contenido-con-la-api-publi
title: La prueba de identidad del deshacer por MCP compara los .md y el store por
  contenido con la API pública de sldb
five_wh_one_plus: how
tags:
- system:ir
- topic:mcp
---

# La prueba de identidad del deshacer por MCP compara los .md y el store por contenido con la API pública de sldb

## Answer

En tests/test_mcp_undo.py, la identidad tras deshacer se verifica por contenido: cada .md por el sha256 de su texto sin el bloque sldb (helper local, sin sldb.models) y el store enumerado con sldb.api.select_documents y comparado por el mismo criterio. No se usa load_runtime_documents, que omite en silencio los modelos que no resuelven y hacía inestable el conjunto de documentos.
