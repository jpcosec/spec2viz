---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-19T19:44:12'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: spec2viz
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-19T20:56:40'
---

# graph_ui: para el contrato de estilo, resolver público para ViewDoc y leyenda resuelta

_Describe the incoming message with enough evidence to triage._

Para el contrato de estilo de glifos, dos cosas que graph_ui necesita del intérprete para no reimplementarlo (contrato §1: un solo intérprete):

1. ViewDoc. graph_ui dibuja vistas (ViewDoc) que no son un SpecDoc: un conjunto de documentos de cualquier modelo, evaluado con sldb.api.graph, y una notation opcional. Hoy resolve_view(store, 'SpecDoc:...') es la única entrada pública y _node_view es privado. Pido una función pública, p. ej. resolve_documents(store, notation_ref, doc_refs, edges, pythonpath) o resolve_view_doc(store, 'ViewDoc:<name>'), que devuelva para esos documentos y aristas la misma forma de nodes/links que resolve_view (glyph, shape, label, fill, stroke, icon, compartments, y link con línea y color), aplicando los where y la prioridad de glifos de la notación.

2. Leyenda. Que el resultado traiga la leyenda de la notación ya resuelta, p. ej. legend: [{glyph, label, shape, fill, stroke, icon}] y links: [{link, label, line, color}], con la paleta por defecto y la precedencia de Style.kinds aplicadas. Así graph_ui la dibuja sin recalcular colores.

Lo demás que dibujo con lo que traiga el contrato: carriles por partition y merge como rombo en actividad, notas UML unidas a su paso, nodos anidados de deployment (VPC > subred > cluster > servicio) como contenedores, communication paths con label y «deploy»/«manifest» de artefacto a nodo. Si para el anidado usas los mismos nest/contains de statechart, mejor: graph_ui ya los dibuja como contenedores.
