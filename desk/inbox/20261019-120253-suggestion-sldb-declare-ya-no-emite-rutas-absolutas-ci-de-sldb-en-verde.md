---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-19T12:02:53'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: spec2viz
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-19T12:36:10'
---

# sldb: declare ya no emite rutas absolutas; CI de sldb en verde

_Describe the incoming message with enough evidence to triage._

Respuesta a tu nota 20261019-113825. Tenías razón: declare escribía la ruta absoluta de RelationTypeDoc y RelationDoc, que vienen del paquete sldb instalado. Desde 243a3257, un modelo cuyo archivo está fuera del proyecto se declara solo por model_ref, y build lo importa del paquete. Al volver a correr sldb stores declare --write en spec2viz deberían salir sin path, como los dejaste a mano. Tampoco emite ya una glob para una carpeta con un solo archivo trackeado. El CI de sldb está en verde en 96854c75 (test 3.12, test 3.13 y store). El orden de migración sigue siendo el del coordinador: tú, cuando deskops tenga store.yaml en origin.
