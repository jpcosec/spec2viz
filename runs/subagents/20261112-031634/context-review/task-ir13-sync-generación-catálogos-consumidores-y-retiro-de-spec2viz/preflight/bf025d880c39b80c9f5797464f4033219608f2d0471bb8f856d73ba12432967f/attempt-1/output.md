## REFORMULACION

Encargo: cerrar la migración de spec2viz a specIR produciendo (1) un comprobador de retiro en `src/specir/visual/retirement.py`, expuesto como subcomando en `src/specir/cli.py`; (2) pruebas en `tests/visual/test_retirement_gate.py`; (3) un acta en `docs/spec2viz/acta-de-retiro.md`; (4) la actualización de `docs/spec2viz/matriz-de-cobertura.md` con prueba y evidencia por fila. Repo: SLDB_1/IR (specIR). Límites: solo lectura sobre repos consumidores y stores; no editar otros repos (se piden por deskops); no implementar capacidades de spec2viz; no archivar/borrar spec2viz. Depende de IR13a–IR13d e IR07.

Es un **paquete no ejecutable** (agregado por dependencias, no por tipo). Lo cumplen sus hijos: IR13a transfiere specs sincronizadas al store y generadas; IR13b, catálogos, anotaciones y emparejamiento de átomos; IR13c, notaciones y paletas expuestas; IR13d, CLI/API y habilidad de agente; IR07, matriz y condiciones del gate. Esta tarea recibe todo ello, añade el subcomando y verifica el conjunto: cada fila con prueba citada, cero imports/invocaciones/modelos spec2viz en consumidores reales, acta completa y suite de spec2viz pasando o equivalentes declarados.

## AMBIGUEDADES

1. «los repos consumidores y los índices de store indicados» y «los stores inventariados en la matriz»: no se enumeran rutas ni índices; obligaría a inventar el universo a escanear.
2. «detecta una importación de spec2viz y una referencia a spec2viz.sldb_models»: no define qué cuenta como invocación (comando, URL, string, config); obligaría a inventar patrones.
3. «cada prueba no portada tiene su equivalente declarado»: no fija criterio de equivalencia ni formato; obligaría a inventar el criterio.
4. «sin que ningún repo del workspace falle»: no acota «workspace» ni define «fallar»; obligaría a inventar el alcance y el umbral.
5. «se registran en … con la referencia al cambio que los resolvió»: no define formato de referencia; obligaría a inventar el esquema del acta.

## DRY-RUN

Lecturas: TaskDoc, matriz, `cli.py`, `retirement.py` (si existe), tests, pills, estado de IR13a–d e IR07. Cambios previstos: crear `retirement.py`; añadir subcomando sin tocar los existentes; crear test; crear acta; actualizar filas de matriz. Dependencias: cierre de IR13a–d e IR07, API pública SLDB, respuestas de deskops. Validaciones futuras: fixture fila sin prueba (falla) y con prueba (pasa); fixture con import y modelo sembrados sin escritura; escaneo real de graph_ui/deskops/stores; suite spec2viz o equivalentes; acta por consumidor; matriz completa.

## FUTURO

Otros nodos producen IR13a–d e IR07 y sus evidencias; deskops ejecuta migraciones en otros repos; el dueño de spec2viz decide archivarlo tras el acta.
