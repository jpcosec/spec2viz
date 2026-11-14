REFORMULACION

Propósito: auditar qué ofrece la API pública de SLDB frente a las 11 capacidades que necesita la superficie MCP de specIR, clasificando cada fila como disponible, requiere-extensión-en-SLDB o faltante. Resultado: `docs/auditoria/sldb-api-frente-a-mcp.md` con tabla de 11 filas (Capacidad, Necesidad, Estado, Evidencia, Brecha, Acción, Handoff), snapshot git de sldb y, si hay brechas, una única nota al desk SLDB vía deskops. Repo: specIR, raíz IR. Límites: solo lectura de docstrings de `sldb.api`, docs SLDB listados y pron §1 y §4; no escribir código, no tocar otros repos, no leer módulos internos de SLDB, no importar/ejecutar pron, no diseñar tools ni decidir política de escritura (IR02).

AMBIGUEDADES

1. "excluir número, paréntesis y separador final" frente a "cualquier paréntesis dentro de la frase se conserva": si hubiera paréntesis interno, obliga a inventar qué regla prevalece.
2. El corpus se cita "bajo ../sldb/src/sldb/api/" pero la validación exige "bajo sldb/src/sldb/api/": obliga a inventar el prefijo con que citar en el informe.
3. "conservar estado y acción de cada fila ... cambiar solo handoff a ERROR literal" / "handoff ERROR": no aclara si ERROR sustituye también el — de las filas disponibles o solo el de las no disponibles.
4. "de kb_undo/forma undo": no define qué es kb_undo ni qué forma buscar; aunque se fija el mínimo (revertir escritura confirmada), obliga a inventar el nombre o criterio de operación.
5. "Resumen enviado exacto: Nota enviada; ID: sldb:<stem>" no indica dónde vive el Resumen (informe, TaskDoc o cierre); obliga a decidir su ubicación.

DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout, dos pills, dos átomos, Python de `../sldb/src/sldb/api/`, docs SLDB listados y pron §1 y §4. Cambios previstos: escribir `docs/auditoria/sldb-api-frente-a-mcp.md`; si hay filas no disponibles, componer `message_body` solo con esas filas y ejecutar `deskops message send` una vez; fijar Resumen y handoffs. Dependencias: git y deskops disponibles; corpus sldb y spec pron presentes. Validaciones futuras: las 12 de Validation (11 filas, estados/acciones, fila 4 separada, no disponibles con módulos, snapshot/hashes, mensaje único e ID, fallo de envío, fuentes, columnas, Brecha y Necesidad exactas, rutas). Nada ejecutado.

FUTURO

IR02 decide la política de escritura y mutabilidad. El desk SLDB decide si integra o documenta las brechas y responde a la nota; un humano puede resolver las ambigüedades 2–5 si el ejecutor no lo hace. No son ambigüedades.
