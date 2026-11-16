## REFORMULACION

Propósito: cerrar la migración de spec2viz demostrando que specIR cubre todas sus capacidades y que ningún consumidor depende de ella. Resultado: el comprobador `specir retirement check` (`src/specir/visual/retirement.py`, montado en `src/specir/cli.py`), el acta `docs/spec2viz/acta-de-retiro.md` y la matriz actualizada con la prueba que acredita cada fila. Repo: solo specIR; el resto se audita en solo lectura y se corrige pidiéndolo a su desk. Límites: no implementa capacidades ni archiva spec2viz; el universo auditado es exactamente el inventario de la matriz más IR.

No es un paquete puro: es tarea de cierre con dependencias. IR13a entrega sincronización y generación con sus pruebas; IR13b, catálogos y emparejamiento de átomos; IR13d, CLI/API y el esqueleto de `cli.py`; IR07 fija modos y condiciones. Cada hijo transfiere a IR13 filas acreditadas y subcomandos; IR13 agrega citándolas en la matriz y validando el conjunto con el gate: rc 0, acta completa y suite de paridad.

## AMBIGUEDADES

1. «La suite de spec2viz pasa contra specIR, o cada prueba no portada tiene su equivalente declarado en la matriz»: «equivalente declarado» no fija formato ni quién lo declara si no hay prueba portada; obligaría a inventar el criterio de aceptación.
2. «Ninguna tarea lo tiene desde que se retiró IR13c»: reconoce filas «usar sldb directamente» sin dueño, pero el Scope excluye implementar capacidades; obligaría a inventar si IR13 debe portarlas.
3. «El acta de retiro lista... la salida del comprobador»: no dice si vale la salida con rc 1 (hoy 122 dependencias) o exige rc 0 para considerarla completa; obligaría a inventar el estado de cierre.

## DRY-RUN

Lecturas: matriz (inventario y acreditación), acta, `gate-de-retiro.md`, y en solo lectura los repos/stores del inventario. Cambios previstos: ninguno de código (ya hecho); al pasar el gate, quitar el xfail de `test_the_real_universe_has_no_dependency_and_every_row_is_accredited`, actualizar matriz y acta, y retirar oráculos de paridad y la federación del store de spec2viz. Dependencias: respuestas de graph_ui, deskops, pron, sldb y del store `spec2viz/.sldb`; comandos de validación en sldb; decisión G7 de JP; mmdc instalado. Validaciones futuras: `pytest tests/visual/test_retirement_gate.py`, `tests/test_imports.py`, `specir retirement check` real con rc 0, y suite de spec2viz contra specIR.

## FUTURO

Deciden o producen otros: JP, G7 y el archivo del repo; los desks de graph_ui, deskops, pron, sldb y spec2viz, sus commits; sldb, los comandos de validación y el arreglo de `attach_atom_edges`. El ejecutor de IR solo consume esa evidencia.
