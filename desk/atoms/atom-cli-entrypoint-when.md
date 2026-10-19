---
id: atom-cli-entrypoint-when
title: CLI Entrypoint
five_wh_one_plus: when
tags:
- system:spec2viz
- topic:cli
provenance: spec2viz/cli.py
---

# CLI Entrypoint

## Answer

Al validar o renderizar un spec YAML desde la terminal o un hook de git, al sincronizar specs y notaciones al store (diagram sync, notation sync, catalog sync) para que graph_ui los dibuje, y al exportar el bundle HTML (catalog build). La CI del repo (.github/workflows/tests.yml) ejercita la CLI por los tests.
