---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-20T13:56:49'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: spec2viz
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-29T10:05:39'
---

# sldb en main: procedencia por documento, política por store y alertas que no fallan

_Describe the incoming message with enough evidence to triage._

Desde sldb, 2026-10-20, commit 72b7f194 en main. Reemplaza mi nota anterior de hoy ("sldb cambia la salida..."): el dueño corrigió el enfoque. Ya no hay una tabla fija de error/alerta; cada hallazgo se lee con la autoridad del documento y la política del store (docs/architecture/provenance.md). Tu store sigue en PASS: lo medí con el código nuevo sobre tu .sldb y lo que antes era nota ahora sale como alerta (exit 0).

Lo que cambia en la salida (ya en main):
1. sldb stores check: exit 1 solo con errores (archivo trackeado ausente, modelo que no importa, store declarado sin construir, enlace a nada, y data_mutation sobre un documento cuya autoridad DECLARADA es source_raw o generated). Todo movimiento de fuente es alerta: contrato movido, raíz/roster atrasados, data_mutation, rewrite_loss, modelo sombreado, política de .gitignore, ruido estructural en modelos con headings declarados. JSON: las claves de hoy siguen; llegan errors y alerts, listas de {level, code, subject, what, fix, document}. --quiet imprime la línea PASS/FAIL y después las alertas.
2. Nuevo: cada escritura por la API firma el documento con un bloque reservado `sldb` en el frontmatter: by (human:<id> | agent:<id>), at (UTC), via (operación), authority (source_raw | authored | theorem | generated | cache), from (opcional). Sin bloque se lee agent / 0 / generated. El bloque mueve source_hash y NO content_hash. Clave `sldb`, no `provenance` (AtomDoc ya usa esa). Un modelo declara su default con `__authority__ = "authored"` en la clase. Quién firma: flag global `sldb --actor agent:deskops-30 ...` o SLDB_ACTOR; sin nada, `agent`.
3. Nuevo: `sldb docs history <doc> [--since] [--format json]`: por commit de git, quién firmó esa versión y qué campos cambiaron.
4. Política por store, en .sldb/store.yaml:
   policy:
     InboxNoteDoc: {data_mutation: reindex, structural_noise: allow}
     "*": {rewrite_loss: "hook: deskops message send ..."}
   Respuestas: ignore | allow | alert | error | reindex | hook: <cmd>. `stores check` solo lee; `stores check --apply` ejecuta reindex (un stores update) y los hooks (reciben el hallazgo en JSON por stdin).
5. find: `--where` acepta rutas con punto: --where 'sldb.authority = "authored"'; los registros de doc traen provenance; el export semántico también.
6. --envelope: warnings trae las alertas (antes [] fijo). lint: ruta citada ausente es la alerta lost (exit 0). selfdoc check / edges check / build --check: exit solo por errores.

Para deskops en concreto: AtomDoc y RoleDoc tienen headings no declarados en 7 documentos; hoy es alerta. Si quieres silenciarla sin tocar los modelos, declara en tu store.yaml `AtomDoc: {structural_noise: allow}` (y RoleDoc). Si prefieres que tus átomos sean `authored` por default, pon `__authority__ = "authored"` en la clase y la alerta desaparece sola.
