---
id: atom-vocabulario-visual-declarativo-donde-vive
title: 'Vocabulario visual declarativo: donde vive'
five_wh_one_plus: where
tags:
- system:spec2viz
- topic:notation
provenance: docs/notation-contract.md
---

# Vocabulario visual declarativo: donde vive

## Answer

Modelos en spec2viz/sldb_models.py (SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc); gramatica y builtins en spec2viz/notation.py y spec2viz/notations/*.yml; escritura al store en spec2viz/sldb_sync.py (diagram sync, notation sync, catalog sync); vista en spec2viz/notation_view.py; contrato en docs/notation-contract.md; en el store, sldb/notations/<name>/ y docs/.../sldb/<spec>/. Los atributos de arista viajan en RelationDoc.attributes (sldb >= 0.1.11).
