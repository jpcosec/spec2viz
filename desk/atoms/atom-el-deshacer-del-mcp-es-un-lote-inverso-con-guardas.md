---
sldb:
  by: agent
  at: '2026-11-17T14:09:44Z'
  authority: generated
  via: save_document_payload
id: atom-el-deshacer-del-mcp-es-un-lote-inverso-con-guardas
title: El deshacer del MCP es un lote inverso con guardas
five_wh_one_plus: how
tags:
- system:specir
- topic:mcp
- layer:superficie
provenance: docs/decisiones/contrato-de-escritura-mcp.md
---

# El deshacer del MCP es un lote inverso con guardas

## Answer

El deshacer del MCP lo sirve sldb mcp con su tool undo_changes (sldb d0ee07a3, closeout 02ea724e). Cada apply_changes que se aplica apila su lote inverso, el que devuelve sldb.api.apply_batch, en una pila de la sesión del servidor, en memoria. undo_changes(steps) reaplica esos inversos del más reciente al más antiguo con las guardas expected_source_hash del estado que dejó la aplicación. Si alguien escribió después, responde rejected stale con el documento, no escribe nada y el lote queda en la pila; si no hay nada que deshacer, responde nothing_to_undo. Cubre los últimos lotes de la sesión en niveles 1 y 2; el nivel 3 no se sirve, y la historia durable es git. specIR no registra la tool, no guarda la pila ni construye inversos: con su extensión montada, solo verifica que el deshacer funciona (IR04b). Enmiendas: 2026-11-15 (JP), construir el lote inverso es de sldb; 2026-11-16 (nota de sldb 232335), la pila y la tool también son de sldb mcp.
