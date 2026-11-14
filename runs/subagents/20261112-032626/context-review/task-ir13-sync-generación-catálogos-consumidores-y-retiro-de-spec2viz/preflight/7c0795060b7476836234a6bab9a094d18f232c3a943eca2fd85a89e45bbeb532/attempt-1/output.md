## REFORMULACION

Propósito: cerrar la migración de spec2viz a specIR demostrando que toda capacidad está cubierta y que ningún consumidor depende de spec2viz. Resultado: comprobador del gate de retiro, acta con evidencia, matriz de cobertura actualizada y solicitudes a los desks afectados. Repo: specIR (`src/specir`, `tests`, `docs/spec2viz`), con lectura de solo lectura sobre repos/stores del inventario. Límites: no implementar capacidades de IR13a–IR13d ni de compiladores/renderers; no editar otros repos; no archivar spec2viz; añadir solo el subcomando del gate tras IR13d y evidencias a la matriz tras IR07, sin alterar sus condiciones. Es un `task.code` ejecutable, no un agregado formal; sus dependencias actúan como agregación.

## AMBIGUEDADES

1. “expuesto como subcomando del comando de specIR”: no se fija nombre, flags, forma de pasar rutas ni formato de salida; obligaría a inventar la interfaz CLI.
2. “el inventario de consumidores de docs/spec2viz/matriz-de-cobertura.md”: no se define esquema, formato ni correspondencia entre nombres de repos/stores y rutas locales; obligaría a inventar parser y convención.
3. “no se cambian los modos ni las condiciones de retiro que fijó IR07”: “modos” no está definido; obligaría a inventar qué campos de la matriz son intocables.
4. “la referencia del cambio que lo resolvió”: no se especifica formato de referencia; obligaría a inventar criterio (commit, mensaje, id u otro).

## DRY-RUN

Lecturas: TaskDoc, matriz, acta, `cli.py`, `retirement.py`, tests, configuración/CI/scripts y stores del inventario, más specIR. Cambios previstos: crear `src/specir/visual/retirement.py`; añadir subcomando en `cli.py`; crear `tests/visual/test_retirement_gate.py`; redactar acta; añadir evidencia por fila a la matriz. Si hay dependencias, registrar repo/ruta/línea/clase y no declarar retiro. Dependencias: IR13a–IR13d e IR07 cerradas; rutas locales disponibles; mensajes vía deskops. Validaciones futuras: fixtures de matriz incompleta y repo con cuatro clases de dependencia; repo con solo menciones documentales; inventario estricto; auditoría real con salida cero; suite de spec2viz; acta y matriz completas.

## FUTURO

IR13a–IR13d producen capacidades y base CLI; IR07 fija matriz y condiciones. Los dueños de graph_ui, deskops y stores migran y responden. El dueño de spec2viz decide archivarlo. CI o un humano ejecuta la auditoría real.
