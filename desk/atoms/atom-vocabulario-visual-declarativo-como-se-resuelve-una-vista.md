---
id: atom-vocabulario-visual-declarativo-como-se-resuelve-una-vista
title: 'Vocabulario visual declarativo: como se resuelve una vista'
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:notation
provenance: spec2viz/notation_view.py
---

# Vocabulario visual declarativo: como se resuelve una vista

## Answer

Para dibujar un spec desde el store: resolver SpecDoc.notation, tomar sus glyphs en orden (el primero cuyo where casa sobre el payload aplanado con data encima gana; el ultimo no tiene where), casar cada RelationDoc con el link de su relation_type o con el comodin, tratar SpecNodeDoc.contains como el link contains (nest), y listar los links por order. El unico interprete es spec2viz.notation_view.resolve_view (CLI spec2viz notation view), que graph_ui sirve como /api/notation/view y dibuja; nadie reimplementa where.
