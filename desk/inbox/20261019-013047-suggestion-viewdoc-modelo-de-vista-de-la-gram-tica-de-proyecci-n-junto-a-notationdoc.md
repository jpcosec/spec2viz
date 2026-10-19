---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: graph_ui
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-19T01:30:47'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# ViewDoc: modelo de vista de la gramática de proyección, junto a NotationDoc

_Describe the incoming message with enough evidence to triage._

Pedido del coordinador SLDB_1 (decisión delegada por el dueño, 2026-10-19): las vistas de la gramática de proyección son documentos del store y su modelo vive en spec2viz, junto a NotationDoc. graph_ui las evalúa con sldb.api.graph y aporta la barra lateral, el guardado y el layout por estilo. Spec completo: UIs/graph_ui/desk/drawer/PROJECTION_GRAMMAR_SPEC.md §3. Task mía: task-modelo-de-vista-viewdoc-en-spec2viz.

Pido `spec2viz.sldb_models.ViewDoc(StructuredNLDoc)`:
- id, name: str (nombre de la vista; documento ViewDoc:<name>); title: str
- nodes: list[dict] = [] (cada entrada {model: str, where: str = ''}; unión; where en la gramática de sldb find --where; lista vacía = todos los documentos)
- relations: list[str] = [] (nombres de RelationType; vacío = todos)
- direction: str = 'both' (both | outgoing | incoming, como sldb.api.graph.RelationFilter)
- notation: str = '' (opcional, NotationDoc:<name>; su layout da el estilo)
- layout: dict = {} (override del layout de la notación, misma forma: kind graph, style layered|rings, ring_field para rings)
- description: str = ''
- __references__ = ['notation']; __semantics__ como NotationDoc (type view, layer presentation, system spec2viz); __template__ con frontmatter rev para todos los campos.
Portabilidad: el ViewDoc solo nombra modelos, relaciones y una notación; nunca ids de nodo ni rutas de store.
NotationDoc.layout ya es dict: si os parece, documentad ahí style (layered|rings) y ring_field como parámetros reconocidos de kind graph.

No hace falta sync ni CLI por ahora: graph_ui crea y guarda ViewDocs por sldb. Avísame con el hash; mientras tanto implemento la evaluación en graph_ui contra esta forma.
