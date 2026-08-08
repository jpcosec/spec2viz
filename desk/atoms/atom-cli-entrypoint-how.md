---
id: atom-cli-entrypoint-how
title: CLI Entrypoint
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:cli
provenance: spec2viz/cli.py
---

# CLI Entrypoint - HOW

## Answer

Lee los argumentos con Click (`render`, `validate`, `schema`, `build`), despacha la carga del archivo YAML a `spec2viz.loader` y canaliza la IR resultante hacia el renderizador solicitado.
