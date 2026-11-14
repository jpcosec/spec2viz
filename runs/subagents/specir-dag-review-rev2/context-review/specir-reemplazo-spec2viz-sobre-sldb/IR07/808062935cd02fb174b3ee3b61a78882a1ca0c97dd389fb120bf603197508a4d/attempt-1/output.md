REFORMULACION
Propósito: IR07 produce, en el repo specIR, la planificación documental del reemplazo de spec2viz por specIR. Resultado: una matriz de cobertura con una fila por capacidad, modo y condición verificable de retiro; un inventario de consumidores con archivo de dependencia; la decisión sobre el YAML de spec frente al grafo; y un gate comprobable de migración y retiro. Límites: no migra ni implementa filas, no hace extractores de otras tecnologías ni análisis de impacto. Es un nodo `docs` no ejecutable, sin hijos: se cumple entregando documentos, no ejecutando código.

AMBIGUEDADES
1. “todas las capacidades de spec2viz” y “Todos los comandos y subgrupos que lista la ayuda del CLI de spec2viz”: no fija versión, commit ni ruta de spec2viz; obligaría a inventar la línea base inventariada.
2. “los stores cuyo índice registra modelos spec2viz.sldb_models”: no define ubicaciones ni método de descubrimiento; obligaría a inventar el universo de stores auditado.
3. “la suite de spec2viz pasa contra specIR”: no delimita qué pruebas componen la suite ni qué cuenta como “prueba equivalente”; obligaría a inventar el criterio de evidencia.
4. “qué pasa con los specs YAML existentes en los repos que usan spec2viz”: no enumera repos/specs afectados ni criterio de compatibilidad o migración; obligaría a inventar el alcance y la política.

DRY-RUN
Lecturas: ayuda del CLI y módulos del paquete spec2viz; `graph_ui/frontends/mindmap/sldb_adapter.py` y su `pyproject.toml`; reglas de rutas en `deskops`; documentación y habilidad `use-spec2viz`; índices de stores; specs YAML existentes; API pública de SLDB para filas “exponer”. Cambios previstos: solo `docs/spec2viz/matriz-de-cobertura.md`, `docs/spec2viz/gate-de-retiro.md` y `docs/decisiones/fuente-de-verdad-del-diagrama.md`. Dependencias: IR03 aporta lectura MCP; IR06 aporta tipos de dominio y store de prueba. Validaciones futuras: cubrir CLI y módulos; citar prueba en cada fila; nombrar sustituto y equivalencia; citar API SLDB; citar archivo por consumidor; documentar decisión y gate como lista comprobable. Sin ejecutar nada.

FUTURO
IR11 usará matriz y decisión para compiladores y proyecciones; IR13a/IR13c y IR13 usarán matriz y gate; el dueño de spec2viz decide archivar o borrar tras el gate. IR03/IR06 entregan insumos, no decisiones de IR07.
