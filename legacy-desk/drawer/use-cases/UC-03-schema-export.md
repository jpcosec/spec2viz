# UC-03: Export JSON Schema

El usuario quiere integrar spec2viz con su editor (VS Code, Neovim) para tener autocompletado y validación en línea de los YAML de diagramas.

## Pasos

1. Exportar schema completo: `spec2viz schema > spec2viz.schema.json`
2. Exportar schema de un tipo específico: `spec2viz schema --type sequence`
3. Exportar schema a archivo: `spec2viz schema --out schema.json`

## Preguntas de estrés

- ¿El schema completo es un discriminated union válido?
- ¿El schema de tipo específico es correcto (solo ese tipo)?
- ¿El schema se puede usar inmediatamente en una config de VS Code (`yaml.schemas`)?
- ¿Qué pasa si el tipo no existe?
- ¿El schema incluye descriptions? (útiles para autocompletado)
- ¿Hay flag `--pretty` o es siempre pretty-printed?
