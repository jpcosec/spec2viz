---
sldb:
  by: agent
  at: '2026-11-15T05:05:36Z'
  authority: generated
  via: create_document
id: atom-lo-desconocido-se-nombra-y-solo-un-humano-fuera-del-mcp-o-un-chequeo-determinista-verifica
title: Lo desconocido se nombra y solo un humano fuera del MCP o un chequeo determinista
  verifica
five_wh_one_plus: how
tags:
- system:specir
- topic:procedencia
- layer:modelo
provenance: docs/decisiones/procedencia-y-divergencia.md
---

# Lo desconocido se nombra y solo un humano fuera del MCP o un chequeo determinista verifica

## Answer

En specIR un valor que no se sabe queda null y se nombra en la lista desconocidos del nodo, con el campo y el motivo (por ejemplo, el extractor no ve permisos dinámicos); no se inventan nodos ni valores. Una inferencia pasa a verificado solo por una escritura explícita de verificacion, verificado_por y evidencia, y solo por una de dos vías: un humano desde una superficie que no es el MCP (CLI de sldb o deskops con --actor human:<id>, graph_ui), o un chequeo determinista (extractor estático que observa la misma relación, un test) con verificado_por check:<id> y su evidencia anclada. El servidor MCP rechaza que un agente escriba verificado: el actor de SLDB no está autenticado, así que la frontera es la superficie.
