# REFORMULACION

Encargo: reescribir `skills/use-specir/SKILL.md` (y sus referencias) para que describa specIR como capa que declara y extrae, sin presentarlo como capa visual ni con anotaciones de catálogo. Resultado: skill sin afirmaciones de que specIR dibuja o tiene interfaz, con un puntero a dónde ver/editar diagramas hoy, con cada comando verificado por `--help`, y con lo decidido-pero-no-ejecutado marcado como tal con fecha. Repo: SLDB_1. Límites: solo docs de la skill; fuera código y `deskops-workflow`.

# AMBIGUEDADES

1. "skills/use-specir/SKILL.md y sus referencias" — no se enumeran ni aparecen en `references: []`. Obliga a inventar qué ficheros son "sus referencias".
2. "a dónde se va para ver o editar un diagrama" — no se indica el destino sustituto. Obliga a inventar la ruta/herramienta real.
3. "lo decidido y sin ejecutar está marcado como tal con la fecha" — sin formato ni criterio de clasificación. Obliga a inventar marcador y a decidir qué afirmaciones son "decididas".
4. Rationale remite a `docs/decisiones/paridad-por-capacidades.md (JP, 2026-11-25)` pero no está en `references`/`depends_on`. Obliga a asumir su contenido (qué capacidades conserva specIR).
5. "Cada comando que nombra existe" vía `--help` no distingue "existe y funciona" de "existe y falla". Obliga a inventar criterio de aceptación.
6. Validación `! grep -nE ...` no indica si es negación de shell o notación. Obliga a inventar la forma ejecutable.

# DRY-RUN

Lecturas: `SKILL.md`, referencias detectadas, `docs/decisiones/paridad-por-capacidades.md`, `--help` de cada comando citado. Cambios previstos: reescribir apertura (quitar "the visual layer"/"same catalog page"), retirar sección de anotaciones de catálogo, añadir puntero a ver/editar diagramas, marcar con fecha lo decidido-no-ejecutado. Dependencias: doc de decisión accesible; CLIs instaladas. Validaciones futuras: `grep -nE 'the visual layer|same catalog page'` sin coincidencias; `--help` correcto por comando; revisión de que no se afirme interfaz.

# FUTURO

Un humano confirma el destino sustituto para ver/editar diagramas y el formato del marcador "decidido, sin ejecutar". Otro nodo aporta el contenido de `paridad-por-capacidades.md`; el commit/merge lo decide el flujo posterior.
