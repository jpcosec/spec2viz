## REFORMULACION
**Propósito:** producir el plan de cobertura que permita retirar spec2viz, sin migrar nada. **Resultado:** `docs/spec2viz/matriz-de-cobertura.md` con una fila por capacidad, modo y condición de retiro; `docs/decisiones/fuente-de-verdad-del-diagrama.md` con la propuesta sobre el YAML; `docs/spec2viz/gate-de-retiro.md` con el procedimiento; el atom de la propuesta; y `tests/test_matriz_cobertura_spec2viz.py`. **Repo:** solo specIR. **Límites:** no implementa filas, no extrae otras tecnologías, no hace análisis de impacto, no acredita cobertura; los cambios en otros repos se piden por su desk. Es un nodo ejecutable documental, no un agregado.

## AMBIGUEDADES
1. **Decidir o proponer.** Cita: “la decisión sobre el papel del YAML de spec frente al grafo” y “Estado: propuesta, pendiente de decisión de JP”. Obligaría a inventar si el nodo debe cerrar la decisión como aceptada o solo dejar una recomendación; afecta a G7.
2. **Gate cumplido o solo redactado.** Cita: “El gate de retiro está escrito como lista comprobable: toda fila con su condición cumplida”. Obligaría a inventar si hay que marcar cumplimiento, pese a que la matriz “no acredita nada” y “no declara nada como ya migrado”.
3. **Creación y edición del atom.** Cita: “se crea con deskops add atom en desk/atoms de este repo… y se añade a atoms de esta tarea”. El atom ya figura en `atoms`; obligaría a inventar si debe recrearse, actualizarse o no tocarse.
4. **Alcance de `gate-de-retiro.md`.** Cita: “docs/spec2viz/gate-de-retiro.md fija el procedimiento”. El archivo ya existe; obligaría a inventar si se crea, se reescribe o solo se conserva.

## DRY-RUN
**Lecturas:** TaskDoc, rituales, pills, átomos, matriz/gate/decisión/test existentes, `spec2viz/cli.py` y módulos/pruebas de la revisión `2de1056`, plan de sldb, D1–D4, consumidores y stores inventariados. **Cambios previstos:** completar matriz, gate, decisión, test y atom; sin tocar otros repos. **Dependencias:** D1–D4, IR11/12/13a/b/d y decisión de JP. **Validaciones futuras:** ejecutar el test de completitud; comprobar ayuda CLI, módulos, modos, ausencia de descartes, consumidores citados, atom y checklist del gate.

## FUTURO
JP acepta o rechaza la propuesta del YAML. D1–D4 migran piezas a sldb; IR11/12/13a/b/d implementan la capa visual. IR13 añade evidencia por fila, evalúa G1–G7 y redacta el acta. Los desks de graph_ui, deskops, pron y sldb migran consumidores. El dueño de spec2viz decide archivar o borrar el repo.
