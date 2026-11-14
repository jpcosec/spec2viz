## REFORMULACION
Encargo: producir en el repo de specIR tres documentos —`docs/spec2viz/matriz-de-cobertura.md`, `docs/spec2viz/gate-de-retiro.md` y `docs/decisiones/fuente-de-verdad-del-diagrama.md`— que inventaríen todas las capacidades de spec2viz (CLI, modelos de spec, compiladores, renderizadores, linter, SpecSync, from-graph, generación desde AST, catálogos, NotationDoc/GlyphDoc/LinkDoc/PaletteDoc, emparejamiento de átomos, API pública y recursos, comando `about`, habilidad use-spec2viz) con modo por fila (migrar/reemplazar/exponer desde SLDB) y condición verificable de retiro; los consumidores conocidos; y la decisión sobre el papel del YAML de spec. No migra nada ni edita otros repos. Resultado: plan revisado del que se derivan tareas de migración. Tarea ejecutable de documentación, no agregado.

## AMBIGUEDADES
1. «spec2viz/tests/ como definición de paridad» y «la prueba que demostrará la equivalencia» no fijan versión/commit de spec2viz; obligaría a inventar el snapshot de referencia.
2. «Existe un atom con la decisión sobre el YAML de spec frente al grafo» choca con «Si el YAML se conserva como formato permanente es una decisión pendiente»: ¿átomo nuevo o edición del existente? `files:` no lo lista; inventaría su ruta.
3. «IR13 la actualiza después, añadiendo por fila la prueba que acredita la cobertura» frente a «nombra el sustituto y la prueba que demostrará»: no se dice qué citar en una fila `reemplazar` aún sin prueba; inventaría una convención de ruta futura.
4. «los stores cuyo índice registra modelos spec2viz.sldb_models» no indica raíz ni criterio de enumeración; inventaría dónde buscar.
5. «inventario de consumidores» enumera tres entradas sin declararlo cerrado; inventaría si hay barrido exhaustivo.
6. Formato y columnas de la matriz no se especifican; inventaría el esquema.
Ninguna otra.

## DRY-RUN
Lecturas: `spec2viz/spec2viz/cli.py` y módulos, `spec2viz/tests/` (solo lectura), plan `absorber-spec2viz-y-modelos-ui`, `sldb/src/sldb/api/notations/` y alias `model_reference.py`, `UIs/graph_ui/frontends/mindmap/sldb_adapter.py`, `deskops` graph.desk_graph, índices de stores. Cambios previstos: crear los tres documentos y el átomo de decisión. Dependencias: IR03, IR06. Validaciones futuras: los ocho checks de la sección de validación (cobertura de CLI y módulos, modos con sustituto y prueba, citas de API SLDB, consumidores con archivo, átomo de decisión, gate como lista).

## FUTURO
IR13 añade evidencias por fila; IR13a–d cierran las migraciones; los cambios en graph_ui/deskops/spec2viz se piden por desk; el dueño decide si el YAML permanece como formato permanente.
