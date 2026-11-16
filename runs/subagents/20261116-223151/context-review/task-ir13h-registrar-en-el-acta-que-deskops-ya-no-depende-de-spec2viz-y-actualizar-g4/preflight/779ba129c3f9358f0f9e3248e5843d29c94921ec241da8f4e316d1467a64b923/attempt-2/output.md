## REFORMULACION
La tarea IR13h actualiza documentación en el repo IR (`/mnt/ssd/proyectos/SLDB_1/IR`) para registrar que deskops ya no depende de spec2viz. Debe editar solo `docs/spec2viz/acta-de-retiro.md` y `docs/spec2viz/matriz-de-cobertura.md`: marcar deskops como resuelto citando tres pares de commits en origin, actualizar G4 y “Lo que falta”, añadir una corrida fechada de `specir retirement check` con cinco rutas y corregir solo la línea de estado de G4 en la matriz. Fuera de alcance: código, pruebas, deskops, otras filas de matriz/resumen y declarar el retiro.

## AMBIGUEDADES
1. “su columna Dependencias sigue el precedente de pron y graph_ui”: no se define el valor exacto ni si debe quedar vacío, “0” o una nota. Obligaría a inventar el contenido/formato de esa celda.
2. “en un bloque fechado con el formato del bloque de IR13g”: no se indica la fecha/hora exacta de la nueva corrida. Obligaría a inventar el timestamp o asumir la fecha actual.
3. “que están en origin”: se citan tres pares de commits, pero la verificación propuesta usa los closeouts `2421ca29`, `74ffdb63` y `b716bf85`; no queda explícito si también deben verificarse los commits principales `421d6a27`, `42b752ea` y `ce66f69e`. Obligaría a decidir qué commits acreditan “origin”.

## DRY-RUN
Lecturas: acta completa, fila deskops, G4, “Lo que falta”, bloque de IR13g; línea G4 de la matriz; precedentes pron/graph_ui; `../deskops/.sldb/core/store_index.yaml`. Cambios previstos: fila deskops a resuelto con commits; G4 y consumidores pendientes sin deskops; bloque fechado con salida nueva del comprobador; línea G4 de matriz según esa salida. Dependencias: `.venv`, repos hermanos `../deskops`, `../UIs/graph_ui`, `../pron`, `../spec2viz/.sldb`, git y `TMPDIR=/dev/shm`. Validaciones futuras: `merge-base --is-ancestor` con rc 0; `grep` sin enlaces a spec2viz; `specir retirement check` sin deskops y con filas no acreditadas coincidentes con la matriz; pytest de `test_matriz_cobertura_spec2viz.py` y `test_retirement_gate.py`; `deskops graph missing --root .`; `git diff --stat` limitado a los dos documentos fuera de `desk/`, `.sldb/` y `runs/`. Sin ejecutar.

## FUTURO
Otro nodo o un humano ejecutará las comprobaciones, aportará la salida real del comprobador y validará el cierre. La decisión de declarar el retiro queda fuera de esta tarea.
