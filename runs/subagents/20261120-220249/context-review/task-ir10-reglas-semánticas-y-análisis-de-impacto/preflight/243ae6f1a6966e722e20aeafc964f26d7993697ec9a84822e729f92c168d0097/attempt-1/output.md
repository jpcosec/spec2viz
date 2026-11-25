## REFORMULACION
Propósito: dotar a specIR de reglas semánticas de dominio y análisis de impacto para responder qué se rompe al cambiar un campo, endpoint o regla, con evidencia trazable. Resultado: documentos RuleDoc para detectar brechas entre interfaz, API, operación y datos; evaluación mediante el motor público de reglas de sldb; operación de impacto basada en `graph_path`/`graph_paths` de sldb; y una tool de solo lectura registrada como extensión de sldb mcp. Repo: specIR (`/mnt/ssd/proyectos/SLDB_1/IR`), consumiendo sldb como dependencia pública. Límites: no recorrer ni explicar grafos dentro de specIR, no proponer parches ni modificar el grafo, no ejecutar la aplicación, y resolver carencias del motor/recorrido en sldb.

## AMBIGUEDADES
1. “lenguaje de reglas de sldb” / “operaciones públicas de reglas”: no se define sintaxis, esquema RuleDoc, severidades ni API concreta; obligaría a inventar el contrato.
2. “tool ... registrada como extensión de sldb mcp”: faltan mecanismo de registro, nombre, esquema de entrada/salida y permisos; obligaría a inventar la interfaz.
3. “solo añade el mapeo de dominio (qué tipos cuentan como afectados y cómo se nombran)”: no se enumeran tipos ni nomenclatura; obligaría a decidir el modelo de impacto.
4. “store de prueba con la brecha sembrada”: no se especifica formato, ubicación ni cómo obtenerlo; obligaría a inventar fixtures.
5. “grafo completo del blog sin brechas sembradas”: no se indica fuente ni estado esperado; obligaría a asumir un grafo canónico.
6. “PublishButton” en la validación: no se define su relación con `posts.status`; obligaría a inventar el camino esperado.

## DRY-RUN
Lecturas: TaskDoc, pills, tareas IR06/IR08/IR09, tarea espejo B3 y documentación pública de reglas, `graph_path`, `graph_paths` y extensiones mcp de sldb. Cambios previstos: RuleDoc por brecha; mapeo de dominio y tool de impacto; registro mcp; stores y pruebas. Dependencias: extractores de IR08/IR09, tipos de IR06, caminos explicados de B3 y API pública de sldb. Validaciones futuras: brecha sembrada detectada con severidad/regla/evidencia; grafo del blog sin hallazgos; `posts.status` afecta `PublishButton` con camino; procedencia por tramo e inferencias señaladas; no escritura del store; ninguna respuesta con parches.

## FUTURO
B3 debe entregar caminos explicados y procedencia; sldb debe soportar las reglas y el recorrido requeridos; IR06/IR08/IR09 deben aportar el grafo y tipos; el responsable de sldb mcp debe aprobar/registrar la extensión; un humano valida el cierre.
