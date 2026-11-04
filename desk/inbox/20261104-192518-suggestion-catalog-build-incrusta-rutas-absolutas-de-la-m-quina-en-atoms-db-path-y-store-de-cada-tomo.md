---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-11-04T19:25:18'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# catalog build incrusta rutas absolutas de la máquina en ATOMS_DB (path y store de cada átomo)

_Describe the incoming message with enough evidence to triage._

Visto en MEPU el 04-11-2026: rendered/catalogo.html (salida de 'spec2viz catalog build') trae en window.ATOMS_DB el 'path' y el 'store' absolutos de cada átomo (p. ej. /home/jp/proyectos/SLDB_1/deskops/desk/atoms/... y .../.sldb). Eso amarra un archivo commiteado a la máquina y al lugar donde está cada repo, y cambia el catálogo si se mueve un repo. Propuesta: emitir rutas relativas a la raíz del repo del átomo (o un id de repo + ruta relativa) y no incluir la ruta del store; generado en spec2viz/deskops.py y cli.py.
