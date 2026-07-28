# UC-05: Reflection and enforcement

El usuario quiere usar el diagram type `reflection` para documentar decisiones arquitectónicas y generar artifacts de enforcement que validen que la implementación cumple con la arquitectura definida.

## Pasos

1. Validar un spec de tipo reflection
2. Renderizar el reflection a JSON (enforcement artifact)
3. Inspeccionar el enforcement artifact generado

## Preguntas de estrés

- ¿El tipo `reflection` aparece en `--help`? (es relativamente nuevo)
- ¿El enforcement artifact se puede consumir por otras herramientas?
- ¿El formato del enforcement artifact está documentado?
- ¿Qué validaciones semánticas aplican a reflection (vs otros tipos)?
- ¿El renderizador default para reflection es JSON?
