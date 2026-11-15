## REFORMULACION
Encargo ejecutable (`task.code`, no agregado): completar IR13a de la migración de spec2viz. Propósito: que el paquete specIR actúe como adaptador de dominio delgado sobre la API pública de sldb para (D1) sincronizar specs al store y (D2) generar specs de componentes desde grafo, snapshot y AST de Python, verificando paridad con spec2viz y actualizando la matriz de cobertura. Resultado: pruebas de paridad/sincronización/generación en verde, sin SpecSync ni generador propios en specIR, sin importar spec2viz, y filas de matriz con condición de retiro cumplida. Repo: paquete specIR en `SLDB_1/IR` (según ruta del input). Límites: fuera SpecSync/generador en specIR, catálogos, notaciones/paletas, CLI, consumidores y retiro de spec2viz; depende de las tareas espejo D1/D2.

## AMBIGUEDADES
1. “un store de prueba” (Validation): no define backend, configuración ni aislamiento; obliga a inventar el store y su limpieza.
2. “un paquete Python de fixture” (Validation): no indica ruta ni contenido; obliga a inventar el fixture AST.
3. “capa delgada en el paquete specIR (specir.visual)” (Implementation Path): no fija funciones, firmas ni errores; obliga a inventar la API adaptadora.
4. “las filas de sincronización, importación de grafo y generación de la matriz” (Done When): no indica archivo, esquema ni valores; obliga a inventar la matriz.
5. “D1”, “D2, que cubre B4” (Goal): no define esos identificadores; obliga a inferir su alcance desde tareas externas.

## DRY-RUN
Lecturas: este TaskDoc, pills, documentos de dependencias D1/D2, API pública de sldb, pruebas/fixtures de spec2viz y matriz de cobertura. Cambios previstos: módulo delgado en `specir.visual` que reexporta/llama a D1 y D2; pruebas de paridad y sincronización; filas de matriz actualizadas. Dependencias: D1/D2 ya migrados a sldb, API pública estable, store de prueba, spec2viz opcional como oráculo. Validaciones futuras: las seis de Validation (SpecDoc/SpecNodeDoc/RelationDoc, borrado, RelationTypeDoc/índice, grafo/snapshot, AST, no importar spec2viz). No se ejecuta nada.

## FUTURO
Los nodos D1/D2 producen SpecSync y el generador en sldb; un humano o nodo de planificación fija fixtures, store y esquema de matriz, y aprueba diferencias de paridad o su declaración en la matriz.
