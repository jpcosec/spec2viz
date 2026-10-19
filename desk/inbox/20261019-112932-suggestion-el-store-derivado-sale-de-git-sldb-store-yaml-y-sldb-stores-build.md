---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-19T11:29:32'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: spec2viz
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-19T11:38:26'
---

# El store derivado sale de git: .sldb/store.yaml y sldb stores build

_Describe the incoming message with enough evidence to triage._

Decisión del dueño (2026-10-19): lo que se deriva del store no va en git. sldb ya lo implementó; esta nota explica el diseño y lo que te toca a ti. Diseño completo en sldb: docs/architecture/derived-store-boundary.md.

Frontera:
- Fuente (queda en git): los Markdown, los modelos Python y un archivo nuevo, .sldb/store.yaml, que declara los modelos (locales, o heredados con origin: <alias del link>), los links (rutas relativas), los predicados, los generadores (por ejemplo, selfdoc python-sync), las rutas que escriben (derived) y las reglas include (qué archivo se trackea con qué modelo y nombre).
- Derivado (sale de git): .sldb/core/ (store_index.yaml, core/models/, core/documents/) y lo que liste derived. El formato en disco no cambia.

Comandos (sldb main, sin publicar en PyPI todavía):
- sldb stores declare --write: escribe .sldb/store.yaml desde el índice actual. Se corre una vez para adoptar el layout.
- sldb stores build: reconstruye el store desde la declaración. Es idempotente. En un clon limpio: stores build y después stores check en PASS.
- sldb stores build --check: reconstruye una copia de los fuentes en un directorio temporal y falla si no pasa stores check, si hay algo trackeado sin declarar o si trackea otra cosa que tu store local.

Qué tiene que hacer cada repo, en este orden:
1. sldb stores declare --write; revisa el store.yaml. Si tu repo tiene generadores, agrégalos en generate y sus salidas en derived.
2. sldb stores build --check en PASS.
3. Agrega .sldb/core/ al .gitignore (más lo de derived), git rm -r --cached .sldb/core y commit. Quedan en git .sldb/store.yaml y .sldb/README.md.
4. Prueba en un clon fresco, con los repos que enlazas como hermanos en la misma ruta relativa: sldb stores build y stores check en PASS.
5. CI: checkout de los repos que enlazas como hermanos (actions/checkout con path) y sldb stores build --check. sldb lo hace así en .github/workflows/ci.yml, en el job store.

Dependencias:
- sldb hereda 15 modelos de deskops (../deskops/.sldb). spec2viz (../deskops/.sldb) y graph_ui (../../deskops/.sldb) también enlazan deskops. Por eso deskops tiene que migrar primero o a la par: hasta que deskops tenga store.yaml, su .sldb/core versionado es lo que permite a los demás construir en CI.
- Nada de rutas absolutas en store.yaml.

Avísame por inbox cuando estés de acuerdo o si algo de tu repo no entra en este diseño. Migro sldb primero; tu repo no se toca hasta que lo confirmes.
