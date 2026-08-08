---
id: atom-spec-loader-how
title: Spec Loader
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:loader
provenance: spec2viz/loader.py
---

# Spec Loader - HOW

## Answer

Utiliza `yaml.safe_load()` para convertir YAML en diccionarios y luego invoca `TypeAdapter(AnyDiagram).validate_python()` usando el discriminador `type`.
