---
sldb:
  by: agent
  at: '2026-11-21T09:26:53Z'
  authority: generated
  via: create_document
id: atom-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz
title: Las pruebas de paridad de IR comparan contra goldens congelados de spec2viz
five_wh_one_plus: how
tags:
- system:ir
- topic:retiro
---

# Las pruebas de paridad de IR comparan contra goldens congelados de spec2viz

## Answer

Los oráculos de paridad de tests/visual y tests/test_matriz_cobertura_spec2viz.py ya no importan spec2viz: comparan contra goldens versionados en tests/visual/goldens/spec2viz-2de1056-*.json, grabados desde spec2viz HEAD 91ba1d0 (código idéntico a 2de1056) (c47111d). El script de grabación quedó fuera del repo, en /mnt/ssd/proyectos/SLDB_1/reports/spec2viz-goldens/record_goldens.py. specir retirement check ya no lista dependencias de IR: quedan solo las 19 del store spec2viz/.sldb (G5) y la fila SV-A17.
