# UC-02: Render a diagram

El usuario validó su spec y quiere generar un diagrama visual en formato PlantUML, Mermaid, o Vega.

## Pasos

1. Renderizar un sequence diagram a PlantUML: `spec2viz render <file> --renderer plantuml --out out/`
2. Renderizar el mismo spec a Mermaid: `spec2viz render <file> --renderer mermaid --out out/`
3. Renderizar un matrix diagram a Vega: `spec2viz render <matrix.yml> --renderer vega --out out/`
4. Renderizar múltiples specs de una vez: `spec2viz render <file1> <file2> <file3>`

## Preguntas de estrés

- ¿El output se escribe en el directorio correcto?
- ¿El nombre del archivo output es predecible? (¿`<input>.puml`? ¿`<input>.mmd`?)
- ¿El contenido del output es sintácticamente válido para el renderizador?
- ¿`--renderer` y `--backend` son equivalentes? (¿hay preferencia?)
- ¿Qué pasa si el directorio de output no existe?
- ¿Qué pasa si el renderizador no soporta el tipo de diagrama? (ej: vega + sequence)
- ¿Hay feedback de progreso para múltiples archivos?
- ¿Overwrite silencioso o pregunta?
