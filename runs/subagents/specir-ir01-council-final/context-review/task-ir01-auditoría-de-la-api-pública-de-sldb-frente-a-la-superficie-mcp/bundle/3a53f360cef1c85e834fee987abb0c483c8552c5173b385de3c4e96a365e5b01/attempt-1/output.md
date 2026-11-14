## REFORMULACION

El nodo es una tarea documental ejecutable (`task.docs`), no un agregado ni un paquete. Propósito: auditar la API pública de SLDB frente a 11 capacidades requeridas por la superficie MCP de specIR. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con exactamente 11 filas, snapshot, evidencia, estados/acciones, brechas y handoff; si hay filas no disponibles, una única nota al desk SLDB. Repo: IR. Límites: solo escribir ese informe; no código, no cambios en otros repos, no módulos internos de SLDB, no importar/ejecutar pron; leer pron solo como documento (§1 y §4) y el corpus SLDB enumerado.

## AMBIGUEDADES

1. “acciones: usar/componer para disponible y solicitar-extensión para no disponible”: no aclara si el campo debe contener literalmente `usar/componer` o elegir `usar` o `componer`. Obligaría a inventar la etiqueta exacta.
2. “Registrar la fecha/hora UTC del snapshot en ISO-8601 `YYYY-MM-DDTHH:MM:SSZ`”: no indica en qué sección o campo del informe. Obligaría a inventar su ubicación.
3. “El nombre canónico y capacidad de cada fila es la frase completa tras su número” junto con “excluir número, paréntesis y separador final”: aunque luego se aclara “quitar solo el marcador numérico inicial `(N)`”, la primera formulación podría hacer dudar si se conservan paréntesis internos. Obligaría a inventar el criterio de título si no se aplica la aclaración posterior.

## DRY-RUN

Lecturas: TaskDoc, rituales, pills, átomos, corpus Python bajo `../sldb/src/sldb/api/`, los docs SLDB listados y pron §1/§4. Cambios previstos: crear solo `docs/auditoria/sldb-api-frente-a-mcp.md`; no tocar otros archivos. Dependencias: comandos Git para snapshot; `deskops message send` solo si hay filas no disponibles. Validaciones futuras: 11 filas; estados/acciones cerrados; evidencia por fila; fila 4 con evidencia separada de `select_documents` y `search`; snapshot/hashes; envío único y ID o registro exacto de error. Sin ejecutar nada.

## FUTURO

Un ejecutor futuro hará las lecturas, el snapshot Git, escribirá el informe y, condicionalmente, enviará la nota. IR02 o un humano decidirá la política de escritura. El desk SLDB recibirá la nota y decidirá/integrará extensiones o documentación; su respuesta queda fuera de este nodo.
