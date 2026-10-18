---
id: atom-empaquetado-y-ci-de-spec2viz
title: Empaquetado y CI de spec2viz
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:packaging
provenance: pyproject.toml
---

# Empaquetado y CI de spec2viz

## Answer

La version de pyproject.toml sigue a la ultima seccion versionada del CHANGELOG; structuredLanguageDB se declara una sola vez (>=0.1.11) y la instalacion editable se refresca con pip install -e . --no-deps tras cambiar metadata; mmdc (mermaid-cli) es un binario externo opcional solo para diagram lint; las notaciones viajan como package-data (notations/*.yml); .github/workflows/tests.yml corre pytest en 3.11-3.13 en push, tags v* y PRs. Sin tags ni releases hasta que la suite SLDB_1 este integrada (regla del dueño 2026-10-18).
