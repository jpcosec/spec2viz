REFORMULACION
Propósito: cerrar la migración de spec2viz a specIR demostrando cobertura total y ausencia de consumidores. Resultado: comprobador del gate de retiro, acta con evidencia y matriz actualizada. Repo: specIR (`src/specir/visual/retirement.py`, `src/specir/cli.py`, `tests/visual/test_retirement_gate.py`, `docs/spec2viz/...`). Límites: solo gate y acta; no implementar capacidades ni editar otros repos; auditar exactamente el inventario de `docs/spec2viz/matriz-de-cobertura.md` más specIR; no archivar spec2viz. No es un agregado no ejecutable: tiene entregable propio; las dependencias son precondiciones.

AMBIGUEDADES
1. Dependencias: el frontmatter lista IR13a, IR13b, IR13d e IR07, pero el texto exige “después de cerradas IR13a, IR13b, IR13c e IR13d”. Obliga a decidir si IR13c bloquea.
2. Contrato del comprobador: “expuesto como subcomando del comando de specIR; lee del inventario de la matriz de cobertura... y recibe por argumento solo la ruta local de cada uno”. No define nombre del subcomando, sintaxis ni formato del inventario; obliga a inventar CLI y parser.
3. Detección: “importaciones de spec2viz en código (import spec2viz o from spec2viz)” y “llamadas al comando spec2viz en código, scripts o configuración ejecutable”. No fija alcance para submódulos, imports dinámicos ni patrones; obliga a inventar heurísticas.
4. Matriz: “cada fila tiene su condición cumplida con una prueba citada” no define esquema de fila, condición o cita; obliga a inventar formato.
5. Paridad: “La suite de spec2viz pasa contra specIR, o cada prueba no portada tiene su equivalente declarado”. No indica cómo ejecutarla ni qué cuenta como equivalente; obliga a inventar criterio.

DRY-RUN
Lecturas: task doc, matriz/inventario, `cli.py`, tests e índices de stores. Cambios previstos: crear `retirement.py` y tests; añadir solo el subcomando en `cli.py`; actualizar la matriz; redactar el acta; pedir migraciones por deskops sin editar repos ajenos. Dependencias: IR13a, IR13b, IR13d e IR07, más la decisión sobre IR13c. Validaciones futuras: matrices sintéticas, repos sintéticos con las cuatro clases de dependencia, repo solo-docs sin hallazgos, inventario exacto, auditoría real read-only con salida 0, paridad de suite y acta completa.

FUTURO
Cierre de tareas dependientes; los desks migran y devuelven referencias; el dueño de spec2viz decide archivarlo; un humano acepta el acta y declara el retiro.
