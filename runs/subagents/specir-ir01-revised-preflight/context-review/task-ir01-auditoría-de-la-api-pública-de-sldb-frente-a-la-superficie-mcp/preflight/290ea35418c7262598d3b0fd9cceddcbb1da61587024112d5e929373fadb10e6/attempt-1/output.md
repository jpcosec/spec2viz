## REFORMULACION
**Propósito:** auditar la API pública de SLDB frente a las capacidades que necesitará la superficie MCP de specIR, antes de diseñarla, para evitar reimplementar lo general y no depender de módulos internos ni de pron.  
**Resultado:** `docs/auditoria/sldb-api-frente-a-mcp.md`, con una matriz capacidad por capacidad y campos capacidad, necesidad, estado, evidencia, brecha y acción; estados cerrados: disponible, requiere-extensión-en-SLDB o faltante. Si hay faltante real, enviar una nota al desk de SLDB y registrar su ID.  
**Repo:** specIR, solo documentación. Se leen `sldb/src/sldb/api/`, documentación de arquitectura de SLDB y, como referencia contractual, `pron/source/spec/14-superficie-mcp.md`.  
**Límites:** no código, no cambios en SLDB, no diseño de tools, no uso directo de pron; no inventar funciones públicas. La ausencia se prueba con inventario de fuentes revisadas.

## AMBIGUEDADES
1. “Cada fila incluye capacidad, necesidad, estado, evidencia, brecha y acción.” No se define el formato ni granularidad de “necesidad” y “acción”; obligaría a inventar criterios de redacción.
2. “resolver vistas” y “búsqueda por predicados”: no se especifica qué contrato exacto debe cubrir cada capacidad; obligaría a inventar semántica funcional.
3. “hay API pública relacionada pero no compone el contrato requerido”: el “contrato requerido” no está detallado; obligaría a decidir qué composición cuenta como suficiente.
4. “Si hay faltante real, enviar una sola nota al desk de SLDB y registrar su ID en la fila correspondiente”: no aclara qué hacer si hay varios faltantes; obligaría a inventar si una nota cubre todos o si se registra el mismo ID en varias filas.

## DRY-RUN
Un ejecutor futuro leería esta TaskDoc, sus pills, el inventario de `sldb/src/sldb/api/`, la documentación de arquitectura de SLDB y la spec MCP de pron como referencia. Extraería las capacidades del scope, las mapearía a símbolos públicos o composiciones y anotaría rutas y símbolos. Para extensión/faltante, listaría fuentes inspeccionadas y la brecha. Si hallara un faltante real, redactaría y enviaría una nota al desk de SLDB con `deskops message send`, registraría su ID y escribiría el informe. Cambio previsto: solo el informe y, si procede, la nota. Dependencias: acceso a ambos repos y a deskops. Validaciones futuras: cobertura completa, estados exactos, rutas existentes, composiciones declaradas, ausencia de dependencia de `sldb.store`, `sldb.core` o pron, y constancia de nota o de no envío.

## FUTURO
Un humano o nodo validador aceptará la matriz y decidirá si las extensiones o faltantes justifican trabajo en SLDB. El diseño posterior de la superficie MCP consumirá esta auditoría; otro nodo podrá verificar citas y estados.
