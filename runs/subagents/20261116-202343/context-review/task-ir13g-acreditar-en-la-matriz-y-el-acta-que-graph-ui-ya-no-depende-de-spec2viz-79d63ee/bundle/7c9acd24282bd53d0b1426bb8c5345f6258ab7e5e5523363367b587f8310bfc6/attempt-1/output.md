## REFORMULACION
Propósito: acreditar en la documentación de IR que graph_ui ya no depende de spec2viz tras su master `79d63ee`. Resultado: `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md` actualizados, con SV-H03 y SV-K22 cumplidas —si se verifican—, graph_ui resuelto en el acta y una corrida nueva de `specir retirement check` anotada con filas abiertas, dependencias por repo, rc y HEAD. Repo: IR. Límites: solo esos dos documentos; no tocar código, pruebas ni graph_ui; no declarar el retiro ni quitar `spec2viz/.sldb` del universo. Es una tarea única de documentación/evidencia, no un agregado.

## AMBIGUEDADES
1. «la fila de graph_ui pasa a resuelto en la columna Cambio que lo resolvió»: no dice si la columna Dependencias conserva el «34» histórico o pasa a 0; obligaría a inventar la política de la tabla.
2. «el resumen de cumplidas y abiertas y los estados G1 y G2 del gate, si cambian»: no fija cifras objetivo; obligaría a inventar el total o el nuevo conteo.
3. «Las filas no acreditadas que liste deben coincidir con las abiertas de la matriz»: no fija el conjunto esperado tras cerrar SV-H03 y SV-K22 ni qué hacer si no coincide; obligaría a inventar el criterio de bloqueo.
4. «SV-H03 pasa a cumplida si su único faltante era G4 de graph_ui y sus pruebas en tests/visual/test_notations_parity.py pasan»: no enumera cuáles pruebas; obligaría a inventar su correspondencia si no se lee la sección Acreditación.

## DRY-RUN
Lecturas: nota de inbox, filas SV-H03/SV-K18/SV-K22, sección Acreditación (IR13), acta completa y bloque de IR13f como formato. Verificación: `git -C ../UIs/graph_ui merge-base --is-ancestor 79d63ee HEAD` y `git grep` de imports/empaquetado; pytest de paridad; `specir retirement check` con las rutas indicadas. Cambios previstos: editar únicamente los dos documentos, congelando la tabla de inventario de consumidores de la matriz y anotando el `--src` sin uso en la fila de graph_ui del acta. Dependencias: HEAD de graph_ui con `79d63ee`, entorno `.venv`, `TMPDIR=/dev/shm` y timeout. Validaciones futuras: diff acotado, checker sin graph_ui, coincidencia de filas abiertas, pytest de matriz/gate y `deskops graph missing`. Sin ejecutar nada.

## FUTURO
JP decide el archivo de spec2viz; deskops y sldb resuelven sus pedidos; IR13 quita `spec2viz/.sldb` del universo al declarar el retiro; el coordinador decide si una verificación fallida bloquea o se reporta.
