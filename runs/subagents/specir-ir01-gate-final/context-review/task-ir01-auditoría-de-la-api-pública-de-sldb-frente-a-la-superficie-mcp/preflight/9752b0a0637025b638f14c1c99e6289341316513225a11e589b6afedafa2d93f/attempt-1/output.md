## REFORMULACION

**Propósito:** auditar la API pública de SLDB frente a las 11 capacidades que necesita la superficie MCP de specIR, clasificando cada una como disponible, requiere-extensión-en-SLDB o faltante. Es una tarea documental única, no un paquete agregado.

**Resultado:** un solo archivo `docs/auditoria/sldb-api-frente-a-mcp.md` con `## Snapshot`, `## Matriz` (7 columnas, 11 filas), `## Resumen` y `## Fuentes revisadas`; si hay filas no disponibles, una única nota a desk SLDB con formato fijado.

**Repo:** trabajar desde `/home/jp/proyectos/SLDB_1/IR`, leyendo `../sldb/src/sldb/api/`, los docs SLDB enumerados y `../pron/source/spec/14-superficie-mcp.md` §1 y §4 como documento externo.

**Límites:** escribir solo ese informe; no tocar otros repos; no leer módulos internos de SLDB; no importar ni ejecutar pron; no ejecutar `check_store`/`check_edges`; no diseñar tools ni decidir política de escritura (IR02).

## AMBIGUEDADES

1. “anotando requisito de texto además de where” (fila 4): no aclara si esa cláusula forma parte del nombre canónico o es instrucción meta; obligaría a inventar el título y el mensaje.
2. “Fecha UTC: <ISO-8601>” en el Resumen de error: no distingue si es la del snapshot o la del intento de envío; obligaría a inventar el instante.
3. “escritura confirmada significa una operación nivel 1 o 2 cuya evaluación terminó con éxito”: los docs no definen cómo constatar ese éxito; obligaría a inventar el criterio de evidencia.
4. “status --short --untracked-files=all limitado a esas rutas”: no fija cómo volcar el estado ni su relación con los hashes; obligaría a inventar el formato del Snapshot.

## DRY-RUN

**Lecturas:** todos los `.py` de `../sldb/src/sldb/api/`; README, addressability_model y los diez docs de `architecture/` enumerados; §1 y §4 de pron.

**Cambios previstos:** crear únicamente el informe.

**Dependencias:** acceso a `../sldb`, git, `deskops message send` y el `path` del JSON.

**Validaciones futuras:** 11 filas y orden de columnas; estados/acciones cerrados; evidencia citada sin símbolos inventados; fila 4 desdoblada con estado global; formato exacto del mensaje y del Resumen; hashes y fuentes revisadas.

## FUTURO

El desk SLDB decide si integra o documenta las brechas; IR02 decide la política de escritura; el envío produce un ID y la revisión humana valida el informe.
