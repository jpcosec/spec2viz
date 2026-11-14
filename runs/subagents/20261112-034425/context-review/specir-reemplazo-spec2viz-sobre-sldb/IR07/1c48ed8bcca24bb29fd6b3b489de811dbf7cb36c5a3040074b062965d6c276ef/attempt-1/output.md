REFORMULACION
Propósito: producir un plan de cobertura de todas las capacidades de spec2viz, la decisión sobre el papel del YAML de spec frente al grafo y un gate comprobable de migración y retiro. Resultado: `docs/spec2viz/matriz-de-cobertura.md`, `docs/spec2viz/gate-de-retiro.md` y `docs/decisiones/fuente-de-verdad-del-diagrama.md`. Repo: specIR. Límites: no migra ni implementa filas, no analiza impacto, no incluye extractores de otras tecnologías y no declara nada como ya migrado. Es un nodo documental no ejecutable y sin hijos; no hay recorrido de hijos que describir.

AMBIGUEDADES
1. Granularidad de “capacidad”. Cita: “una fila por cada capacidad de spec2viz”, con validación de “Todos los comandos y subgrupos” y “Todos los módulos”. Obligaría a inventar si una fila es comando, módulo, familia funcional o combinación, y cómo deduplicar.
2. Estados permitidos. Cita: los modos son “migrar tal cual; reemplazar…; exponer…”, pero también “Ninguna fila dice descartado, fuera de alcance o ya implementado sin una prueba citada”. Obligaría a inventar si “descartado” es modo válido, estado aparte o prohibido.
3. Evidencia de retiro. Cita: “condición verificable de retiro” y “con una prueba citada”. Obligaría a inventar el formato de prueba —ruta, comando, resultado, responsable— y el criterio de suficiencia.
4. Decisión sobre YAML. Cita: “decidir si el YAML de spec queda como formato de autoría e intercambio de forma permanente o solo durante la paridad”. Obligaría a inventar criterios, autoridad que decide y qué significa “solo durante la paridad”.
5. Inventario de deskops. Cita: “documentación de diagramas y la habilidad use-spec2viz”. Obligaría a inventar qué archivos concretos deben listarse.

DRY-RUN
Un ejecutor futuro leería la ayuda del CLI de spec2viz, el árbol de módulos y recursos, los specs YAML existentes, los archivos de consumidores citados, los índices de stores y la API pública de SLDB. Redactaría la matriz fila a fila con modo y condición; la decisión con alternativas, regla de diseño previo y destino de specs; y el gate como lista comprobable. Dependencias declaradas: IR03 e IR06. Validaciones futuras: cobertura de comandos y módulos, pruebas citadas, rutas de consumidores, atom de decisión y checklist del gate.

FUTURO
IR11 e IR13 consumirán la matriz y la decisión; un humano aprobará la decisión sobre el YAML y la autoridad de retiro; el dueño de spec2viz decidirá archivarlo tras el gate de IR13. Los nodos de migración implementarán las filas.
