---
sldb:
  by: agent
  at: '2026-11-16T15:31:27Z'
  authority: generated
  via: create_document
id: materialization-ir-gitignore-materializa-la-regla-de-ignorar-artefactos-de-instalación-editable-y-bytecode
title: IR .gitignore materializa la regla de ignorar artefactos de instalación editable
  y bytecode
source_atoms:
- atom-ir-ignora-en-git-los-artefactos-de-instalación-editable-y-de-bytecode
target_kind: config_file
target_identity: .gitignore
validation:
- git check-ignore -q src/specir.egg-info
- git ls-files -ci --exclude-standard sale vacío
tags:
- system:ir
- topic:git
---

# IR .gitignore materializa la regla de ignorar artefactos de instalación editable y bytecode

## Intent

Las líneas *.egg-info/ y __pycache__/ de .gitignore hacen que git ignore los artefactos que crean la instalación editable del hook de scion y pytest.
