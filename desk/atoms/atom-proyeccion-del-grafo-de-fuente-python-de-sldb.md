---
id: atom-proyeccion-del-grafo-de-fuente-python-de-sldb
title: Proyeccion del grafo de fuente Python de sldb
five_wh_one_plus: how
tags:
- system:spec2viz
- topic:graph-import
provenance: spec2viz/graph_import.py
---

# Proyeccion del grafo de fuente Python de sldb

## Answer

spec2viz diagram from-graph lee el node-link que escribe sldb selfdoc python-sync (.sldb/runtime/graphs/python-source.graph.json) con load_node_link_graph, que ademas de id y tipo devuelve por nodo lo que declara: label desde ast.name (simbolo) o ast.module (modulo), kind desde semantics.kind si esta declarado y si no desde la clase AST (module, class, function, variable; external para python_external), y module para el alcance. --module-prefix (repetible) conserva un modulo y lo que cuelga de el; como las aristas y los contains solo se emiten entre nodos conservados, nada queda colgando. Las relaciones se copian con su nombre (contains anida; imports, references y las demas son aristas). La salida valida con spec2viz diagram validate.
