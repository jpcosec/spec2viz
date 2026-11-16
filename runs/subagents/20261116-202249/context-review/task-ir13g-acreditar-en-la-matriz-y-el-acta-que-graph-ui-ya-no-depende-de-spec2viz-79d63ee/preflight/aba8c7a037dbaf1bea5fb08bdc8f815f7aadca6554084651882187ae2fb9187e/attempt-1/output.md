REFORMULACION

Encargo ejecutable (no agregado): actualizar dos documentos, `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md`, para acreditar que graph_ui ya no depende de spec2viz tras su master 79d63ee (closeout c9b09f7). Resultado: SV-H03 y SV-K22 cumplidas (o abiertas con motivo verificado distinto de G4), graph_ui resuelto en el acta citando 79d63ee/c9b09f7/nota, y bloque fechado nuevo de `specir retirement check` con filas abiertas, dependencias por repo, rc y HEADs. Repo: IR, comandos desde su raíz con `TMPDIR=/dev/shm` y `.venv`. Límites: no tocar código ni pruebas, no cambiar graph_ui, no declarar el retiro, no editar la tabla de inventario de consumidores, no quitar `spec2viz/.sldb`.

AMBIGUEDADES

1. "los estados G1 y G2 del gate, si cambian" — no define qué gate ni qué significan G1/G2; obligaría a inventar su semántica si no está en la matriz.
2. "las pruebas que la sección Acreditación (IR13) asigna a SV-H03" — no las enumera; obligaría a inventar el mapeo si la sección no lo detalla.
3. "pasa a resuelto en la columna Cambio que lo resolvió" — no fija el literal exacto de la celda; obligaría a inventar formato.
4. "con el mismo formato del bloque de IR13f" — no reproduce el formato; obligaría a inventar estructura si el acta no lo muestra.
5. "SV-K18 sigue abierta mientras dependa de SV-K21" — no declara el estado actual de SV-K21; obligaría a inventarlo.

DRY-RUN

Lecturas: nota de inbox, filas SV-H03/SV-K18/SV-K22 y sección Acreditación, acta completa y bloque IR13f, pills. Cambios previstos: solo esas filas, resumen de cumplidas/abiertas, G1/G2 si procede; fila graph_ui y G4 y punto Consumidores del acta; bloque fechado nuevo. Dependencias: task-ir13f cerrada, repo `../UIs/graph_ui`, `.venv`, `specir`. Validaciones futuras: `git diff --stat` acotado; `merge-base --is-ancestor 79d63ee HEAD` rc 0; `git grep` sin coincidencias; pytest de paridad y de matriz/gate; `specir retirement check` coherente con filas abiertas; `deskops graph missing` rc 0.

FUTURO

Otro nodo o humano decide el retiro efectivo, el `ci.yml` de graph_ui y cualquier corrección en repos ajenos vía su desk.
