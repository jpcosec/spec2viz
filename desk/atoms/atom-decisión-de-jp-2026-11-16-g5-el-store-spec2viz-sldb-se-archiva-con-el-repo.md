---
sldb:
  by: agent
  at: '2026-11-16T05:13:39Z'
  authority: generated
  via: create_document
id: atom-decisión-de-jp-2026-11-16-g5-el-store-spec2viz-sldb-se-archiva-con-el-repo
title: 'Decisión de JP 2026-11-16 (G5): el store spec2viz/.sldb se archiva con el
  repo'
five_wh_one_plus: why
tags:
- system:spec2viz
- topic:retiro
provenance: runs/decisions/g5-store-spec2viz.md
---

# Decisión de JP 2026-11-16 (G5): el store spec2viz/.sldb se archiva con el repo

## Answer

Decisión de JP del 2026-11-16, transmitida por el supervisor: el store spec2viz/.sldb se archiva junto con el repo spec2viz cuando specir retirement check dé 0. No se reapuntan sus 7 modelos spec2viz.sldb_models a sldb.models.notation (se descartó la opción B). Motivo: sin motivo declarado por JP; el coordinador recomendó A porque fuera de las pruebas de IR nadie lee este store y la decisión 6 del acta ya archiva el repo. Consecuencia: IR quita spec2viz/.sldb del universo del comprobador y cambia la federación del store en sus pruebas (IR/tests/conftest.py, IR/tests/test_mcp_extension.py) por un fixture. Origen: G5 del acta IR/docs/spec2viz/acta-de-retiro.md.
