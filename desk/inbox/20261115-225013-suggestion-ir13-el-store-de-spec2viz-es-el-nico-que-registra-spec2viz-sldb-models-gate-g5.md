---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-11-15T22:50:13'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# IR13: el store de spec2viz es el único que registra spec2viz.sldb_models (gate G5)

_Describe the incoming message with enough evidence to triage._

IR13 (gate de retiro de spec2viz, repo IR) informa el estado del ítem G5 (stores) del gate. El retiro no está declarado; archivar o borrar spec2viz lo decide JP cuando el gate se cumpla.

El único store del universo auditado que registra modelos `spec2viz.sldb_models` es el de este repo: `.sldb/store.yaml:44-57`, `.sldb/core/store_index.yaml:141-260` y `.sldb/core/models/{SpecDoc,SpecNodeDoc,NotationDoc,GlyphDoc,LinkDoc,PaletteDoc,ViewDoc}.yaml:2` (19 registros según `specir retirement check`). Sustituto: los modelos públicos de sldb `sldb.models.notation.{spec_doc.SpecDoc, spec_node_doc.SpecNodeDoc, notation_doc.NotationDoc, glyph_doc.GlyphDoc, link_doc.LinkDoc, palette_doc.PaletteDoc, view_doc.ViewDoc}` (fila SV-A17 de `IR/docs/spec2viz/matriz-de-cobertura.md`).

Pedido: si el store debe sobrevivir al retiro, reapuntar esos modelos a los de sldb con `sldb` (no a mano); si el store se archiva con el repo, decirlo para registrarlo en `IR/docs/spec2viz/acta-de-retiro.md`. Ojo: IR federa este store en sus pruebas (`IR/tests/conftest.py:24` y `:80`, `IR/tests/test_mcp_extension.py:24`); IR lo cambia por su lado antes del retiro.
