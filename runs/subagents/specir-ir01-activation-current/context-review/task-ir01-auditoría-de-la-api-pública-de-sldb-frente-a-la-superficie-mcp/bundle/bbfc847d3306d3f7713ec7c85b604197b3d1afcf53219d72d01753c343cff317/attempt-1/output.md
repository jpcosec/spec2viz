## REFORMULACION

Encargo ejecutable (no agregado): auditar la API pública de SLDB frente a la superficie MCP de specIR y producir un único informe en `docs/auditoria/sldb-api-frente-a-mcp.md`, con exactamente 11 filas —capacidad, necesidad (actor/entrada/resultado), estado cerrado, evidencia, brecha, acción y handoff—. Repo: IR, leyendo el corpus fijado de `../sldb` y solo §1/§4 de `../pron/source/spec/14-superficie-mcp.md`. Límites: escribir solo ese archivo; no abrir módulos internos de SLDB ni importar/ejecutar pron; si hay no disponibles, enviar un único `deskops message send` a sldb y registrar el ID; si falla, dejar celdas `ERROR` y resumen de fallo sin reintentar.

## AMBIGUEDADES

1. «Hay exactamente 11 filas, una por el listado numerado anterior.» — No hay listado numerado en el input. Obligaría a inventar las 11 capacidades y su orden.
2. «las capacidades 6, 10 y 11 permanecen en esta auditoría» / «Para fila 7» / «Fila 8» / «Fila 10» / «Fila 4» — Se referencian filas concretas sin lista; habría que inventar qué capacidad es cada número.
3. «El contrato final de escritura queda fuera solo como decisión de producto de IR02» — IR02 no se define en el input; obligaría a inventar su alcance o asumir que es un nodo futuro.

## DRY-RUN

Lecturas: TaskDoc, rituales, pills, átomos; todos los `.py` bajo `../sldb/src/sldb/api/`; `README.md`, `addressability_model.md` y los diez documentos de `architecture/` enumerados; spec pron §1/§4. Ejecutaría `git -C ../sldb rev-parse HEAD`, `branch --show-current` y `status --short --untracked-files=all` con esos pathspecs; si git falla, hashearía todo el corpus con SHA-256; si hay modificados/untracked, hashearía solo esos. Cambios previstos: crear/editar únicamente el informe y, si hay brechas, un mensaje deskops. Dependencias: corpus existente, git, deskops y la lista de 11 capacidades (ausente). Validaciones futuras: 11 filas con estados y acciones coherentes, citas reales bajo `sldb/src/sldb/api/`, snapshot con commit/branch/estado/hashes, mensaje único con ID exacto o resumen de fallo, y ausencia de apertura de módulos internos o ejecución de pron.

## FUTURO

IR02 decide el contrato final de escritura; el desk de SLDB atiende las extensiones solicitadas; el Board o un humano debe aportar el listado numerado de capacidades antes de ejecutar; la validación de cierre confirma informe y notificación.
