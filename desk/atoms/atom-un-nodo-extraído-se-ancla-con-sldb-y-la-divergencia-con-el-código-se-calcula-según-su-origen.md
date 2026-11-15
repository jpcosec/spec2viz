---
sldb:
  by: agent
  at: '2026-11-15T05:05:38Z'
  authority: generated
  via: create_document
id: atom-un-nodo-extraído-se-ancla-con-sldb-y-la-divergencia-con-el-código-se-calcula-según-su-origen
title: Un nodo extraído se ancla con SLDB y la divergencia con el código se calcula
  según su origen
five_wh_one_plus: how
tags:
- system:specir
- topic:procedencia
- layer:modelo
provenance: docs/decisiones/procedencia-y-divergencia.md
---

# Un nodo extraído se ancla con SLDB y la divergencia con el código se calcula según su origen

## Answer

Cada nodo observado o derivado lleva from code:<ruta>::<símbolo> en su bloque sldb y un CodeAnchorDoc registrado con sldb.api.anchors.record_anchor; check_anchors da su estado. Mientras SLDB no ancle TSX ni SQL, esos nodos llevan solo from, verificacion sin_verificar y la ancla en desconocidos. Cuando modelo y código discrepan: para observado y derivado manda el código y la re-extracción los regenera; para declarado y todo lo verificado manda el modelo y la diferencia es un hallazgo para el análisis de impacto, nunca una sobrescritura. Un nodo con ancla changed o lost no se borra; el estado de la ancla se lee al consultar y una verificación sobre un ancla no intact se reporta vencida hasta que alguien vuelva a verificar o reanclar; reconnected se acepta y queda en el historial de la ancla.
