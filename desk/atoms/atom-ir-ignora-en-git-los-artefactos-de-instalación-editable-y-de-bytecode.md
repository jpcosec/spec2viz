---
sldb:
  by: agent
  at: '2026-11-16T15:30:28Z'
  authority: generated
  via: create_document
id: atom-ir-ignora-en-git-los-artefactos-de-instalación-editable-y-de-bytecode
title: IR ignora en git los artefactos de instalación editable y de bytecode
five_wh_one_plus: why
tags:
- system:ir
- topic:git
- topic:scion
provenance: desk/inbox/20261116-021128-suggestion-ir-gitignore-no-ignora-egg-info-ni-pycache-el-hook-de-scion-instala-ir-editable.md
---

# IR ignora en git los artefactos de instalación editable y de bytecode

## Answer

IR/.gitignore incluye *.egg-info/ y __pycache__/ porque el hook pre-start de los ejecutores scion instala IR en modo editable (uv pip install -e IR[test]), y eso crea src/specir.egg-info/. Además, las corridas de pytest generan __pycache__/. Son artefactos de build locales, no fuente: no se versionan ni se borran, solo se ignoran, para que git status y la comprobación de alcance de los testers no los cuenten como cambios de una tarea.
