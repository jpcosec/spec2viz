## REFORMULACION

Nodo agregado no ejecutable por sí mismo: aunque `task_type: task.code`, su entregable depende de IR13a–IR13d e IR07. Propósito: cerrar la migración demostrando que specIR cubre spec2viz y que ningún consumidor depende de ella. Resultado: comprobador `src/specir/visual/retirement.py` expuesto como subcomando en `src/specir/cli.py`, acta `docs/spec2viz/acta-de-retiro.md` y matriz actualizada; gate con salida cero sobre el universo auditado. Repo: solo specIR. Límites: no implementa capacidades (hijos), no edita otros repos, no archiva spec2viz; cambios externos vía `deskops message send`.

## AMBIGUEDADES

1. "docs/spec2viz/acta-de-retiro.md" frente a "solo crea o modifica archivos dentro del repo de specIR": ¿la ruta vive en specIR o en spec2viz? Obliga a inventar la ubicación real.
2. "lee del inventario de la matriz de cobertura la lista de repos consumidores y de stores": no se define formato ni marcadores del inventario; obliga a inventar el parser.
3. "un índice de store con un modelo spec2viz.sldb_models": no se define qué archivo es índice ni cómo se registra; obliga a inventar el esquema.
4. "una llamada al comando spec2viz en un script": no se fija heurística (regex, AST, shell); obliga a inventar detección.
5. "termina con código de salida distinto de cero": valor concreto no fijado; obliga a elegir.
6. "pedidos de migración a los desks de graph_ui, deskops y de cada repo con stores afectados": lista exacta depende del inventario no transcrito; obliga a inferirla.
7. "La suite de spec2viz pasa contra specIR": no se especifica cómo se ejecuta esa suite contra otro repo; obliga a inventar el arnés.

## DRY-RUN

Lecturas: TaskDoc, pills, átomos, IR07 (matriz), IR13a–d (specs, catálogos, notaciones, CLI). Cambios previstos: crear `retirement.py` y `tests/visual/test_retirement_gate.py`; añadir subcomando en `cli.py` sin tocar los de IR13d; actualizar matriz y acta. Dependencias: IR13a aporta sincronización/store; IR13b catálogos y emparejamiento de átomos; IR13c notaciones y paletas; IR13d CLI/API/habilidad; IR07 matriz y condiciones de retiro. Validaciones futuras: matriz sin prueba falla; repo con cuatro clases de dependencia reporta ruta/línea y sale ≠0 sin escribir; solo-documentación no reporta; universo restringido al inventario; ejecución real sale 0; suite spec2viz o equivalentes declarados; acta completa por consumidor.

## FUTURO

Deciden otros: dueños de graph_ui, deskops y stores responden a los mensajes; IR07 valida condiciones de retiro; el dueño de spec2viz decide archivar; el ejecutor de IR13 integra y corre sobre repos reales.
