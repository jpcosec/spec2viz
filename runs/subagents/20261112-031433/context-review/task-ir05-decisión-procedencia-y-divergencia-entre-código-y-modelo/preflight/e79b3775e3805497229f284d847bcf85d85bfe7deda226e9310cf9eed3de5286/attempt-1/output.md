REFORMULACION
Propósito: fijar una taxonomía única de procedencia para specIR y una regla para la divergencia entre modelo y código. Resultado: el documento `docs/decisiones/procedencia-y-divergencia.md` y tres atoms: taxonomía canónica con equivalencias; representación de lo desconocido y paso de inferencia a validada; y divergencia cuando cambia la fuente. Repo: `SLDB_1/IR`, con lecturas en `sldb`. Límites: no implementar extractores; es una tarea de decisión documental, no un agregado ni un paquete ejecutable.

AMBIGUEDADES
1. “fundamentos_modelado_semantico_mcp.md, sección 7” y “Plan_IR.md, fase 5” no indican ruta ni repositorio, frente a “Lectura de sldb/docs/architecture/provenance.md y anchoring.md”. Obliga a inventar ubicación y versión vigente de las dos primeras fuentes.
2. “definir las equivalencias” no fija granularidad. Obliga a inventar si el mapeo es uno-a-uno, uno-a-varios o con pérdida, y si cada valor necesita fila propia.
3. “Cada decisión se registra como atom” frente a “Los tres atoms existen”. Obliga a inventar el agrupamiento: por ejemplo, si anclas y prevalencia van dentro del atom de divergencia.
4. “la fila correspondiente de la matriz de auditoría” no da ruta, esquema ni identificador. Obliga a inventar dónde vive la matriz y cómo se referencia una fila.
5. “por acción de quién” no nombra actores. Obliga a inventar roles o autoridades para validar una inferencia.

DRY-RUN
Lecturas: task doc, pill de guardrail, salida de IR01, `fundamentos_modelado_semantico_mcp.md`, `Plan_IR.md`, `sldb/src/sldb/models/provenance.py`, `sldb/docs/architecture/provenance.md` y `anchoring.md`. Cambios previstos: redactar el documento de decisión y crear tres atoms con taxonomía, equivalencias, desconocido/transición y divergencia. Dependencias: matriz de auditoría de IR01 y documentación/código de procedencia de SLDB. Validaciones futuras: existencia y contenido de los tres atoms; tabla de equivalencias; regla de transición y responsable; regla de divergencia; carencias mapeadas a la matriz; que tareas de dominio y extractores puedan citar una sola taxonomía. Sin ejecutar.

FUTURO
IR01 aporta la matriz de auditoría. Un humano o nodo decisor elige la taxonomía, el tratamiento de anclas, la prevalencia y la representación de lo desconocido. Las tareas de tipos de dominio y de extractores consumen y citan la decisión.
