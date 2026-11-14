## REFORMULACION
Propósito: dotar a specIR de los tipos de dominio transversales (clases Python) y de los datos que los acompañan (RelationTypeDoc y RuleDoc) para modelar la cadena de publicación de un post. Resultado: modelos en `src/specir/models`, `relation_types.yaml`, `rules.yaml`, `install.py` y pruebas con el fixture `blog_chain.yaml`. Repo: specIR. Límites: dentro, clases de modelo, tipos de relación, invariantes y store de prueba; fuera, extractores, análisis de impacto y síntesis. El MCP escribe datos, no clases.

## AMBIGUEDADES
1. "subclases del documento base de SLDB": no se nombra la clase ni su API; obligaría a inventar el import y el contrato de herencia.
2. "Las pruebas anteriores pasan": sin antecedente en el nodo; obligaría a inventar qué suite previa se exige.
3. "PublishButton, PublishAction, endpoint, handler, PublishPost y tabla": solo algunos son nombres; obligaría a inventar los identificadores de endpoint, handler y tabla.
4. "invariantes entre capas... por ejemplo": conjunto abierto; obligaría a inventar qué reglas además de la citada.
5. Los ocho RelationTypeDoc no traen tipo origen, destino ni cardinalidad; obligaría a inventar sus esquemas.
6. "store de prueba poblado por MCP" frente a `tests/fixtures/blog_chain.yaml`: no se dice si se puebla con tools de IR04 o desde el fixture; obligaría a elegir el mecanismo.
7. "tipos de dominio transversales": no se define el criterio de transversalidad; obligaría a inventar qué queda dentro de cada clase.

## DRY-RUN
Un ejecutor leería la API pública de SLDB (documento base), el atom de procedencia de IR05 y las tools de escritura de IR04. Crearía los archivos de `output_scope`, definiría las clases y cargaría `relation_types.yaml`, `rules.yaml` y el fixture. Dependencias: IR04 e IR05. Validaría: recorrido MCP bidireccional de la cadena; rechazo de una relación no permitida; reporte del RuleDoc al quitar la operación de API; un único documento Post entre dos vistas; procedencia por nodo y relación; ausencia de redefinición de vocabulario visual de SLDB.

## FUTURO
IR05 entrega la taxonomía canónica de procedencia; IR04, las tools MCP de escritura. IR07, IR08, IR09, IR10 e IR11 consumen estos tipos y el store de prueba. Un humano decide cualquier cambio de alcance.
