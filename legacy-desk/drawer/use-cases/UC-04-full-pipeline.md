# UC-04: Full pipeline (validate → render → verify)

El usuario tiene un conjunto de specs de diagrama (sequence, state, component, deployment, activity) y quiere procesarlos todos: validar primero, luego renderizar los que pasaron validación, y verificar los outputs.

## Pasos

1. Validar todos los specs: `spec2viz validate <file1> <file2> ...`
2. Renderizar todos los specs válidos: `spec2viz render <file1> <file2> ... --out diagrams/`
3. Inspeccionar los archivos generados en `diagrams/`
4. Verificar que cada renderizador produjo el formato correcto

## Preguntas de estrés

- ¿Se puede pipear validate a render? (¿o hay que re-listar archivos?)
- ¿Los nombres de output son consistentes entre todos los tipos?
- ¿Los archivos generados son válidos para el renderizador target?
- ¿Hay algún tipo de diagrama que no tenga un renderer por defecto?
- ¿El output de render incluye metadatos (timestamp, source file)?
- ¿Qué pasa si un render falla parcialmente en un batch?
