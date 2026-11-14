# REFORMULACION

**Propósito.** Demostrar con un caso mínimo que el grafo tipado de specIR conecta interfaz, API, operación y datos sin duplicar identidades, antes de construir extractores o análisis.

**Resultado.** (1) Clases Python de modelo en el paquete specIR, subclases del documento base de SLDB, para nueve tipos (interfaz, acción, operación de API, handler, operación de dominio, política, estado, entidad de dominio, tabla); (2) RelationTypeDoc distribuidas e instaladas en un store: triggers, invokes, handled_by, executes, governed_by, transitions, writes, persisted_in; (3) RuleDoc distribuidas, p. ej. toda acción de interfaz invoca una operación de API existente; (4) un store de prueba poblado por MCP con la cadena de publicar un post (React/DRF/PostgreSQL).

**Repo.** Paquete specIR sobre `sldb.api` exclusivamente; datos de tipos y reglas viven en el store, no en clases.

**Límites.** Fuera: extractores, análisis de impacto, síntesis. Sin mocks; MCP escribe datos, no clases.

# AMBIGUEDADES

1. «Cada nodo y relación lleva la procedencia de la taxonomía canónica decidida»: no se cita cuál taxonomía ni el campo/forma de la procedencia. Obligaría a inventar el esquema de procedencia y su fuente.
2. «el mecanismo de registro de modelos de SLDB, como hace deskops»: no se incluye referencia al mecanismo ni a deskops. Obligaría a inventar la API de registro.
3. «un store de prueba poblado por MCP»: no se dice ubicación, nombre ni ciclo de vida del store. Obligaría a inventar configuración.
4. «endpoint, handler»: no se nombran los nodos concretos de la cadena. Obligaría a inventar identificadores.
5. «la evaluación de reglas reporte el RuleDoc incumplido»: no se especifica motor ni formato de reporte. Obligaría a inventar el evaluador (posiblemente fuera de alcance).
6. «Dos vistas distintas (una de estados y una de componentes)»: no se define cómo se materializan las vistas vía MCP. Obligaría a inventar la proyección.

# DRY-RUN

Lecturas: TaskDoc, rituales phase/execution/testing/closeout, ambas pills, cuatro átomos, y los ocho archivos listados (`models/domain.py`, `relation_types.yaml`, `rules.yaml`, `install.py`, tests y fixture). Cambios previstos: clases de modelo, YAML de tipos y reglas, comando de instalación, fixture `blog_chain.yaml`, dos tests. Dependencias: IR04 (escritura MCP) e IR05 (procedencia) cerradas; `sldb.api` con registro de modelos y escritura. Validaciones futuras: recorrido bidireccional por MCP, rechazo de relación no permitida, regla incumplida al borrar operación, identidad única de Post, procedencia presente, import-lint de `sldb.api`. Sin ejecutar.

# FUTURO

IR04 e IR05 deben entregar escritura MCP y criterio de procedencia; un humano decide la taxonomía canónica y aprueba el cierre; el store de prueba queda para tareas posteriores.
