## REFORMULACION
Encargo: implementar en specIR, dentro del repo SLDB_1/IR (`src/specir/visual/`), la capa de compilación visual de spec2viz. Propósito: sustituir la compilación de spec2viz cubriendo sus ocho tipos de diagrama y producir una representación intermedia común desde specs autorados y desde proyecciones del grafo. Resultado: modelos de spec, carga/validación, IR, un compilador por tipo, proyecciones desde ViewDoc y SpecDoc/SpecNodeDoc, con exportaciones iniciales en `__init__.py`. Límites: no renderizar salidas, linter, recursos, sincronización al store, catálogos, consumidores ni retirar spec2viz; no redefinir vocabulario visual de SLDB ni importar spec2viz en el paquete. Validación: paridad con fixtures/pruebas de compiladores de spec2viz, errores tipados equivalentes, proyecciones del blog con Post y un solo documento, equivalencia spec/proyección, ausencia de colisión de nombres y de import de spec2viz.

## AMBIGUEDADES
1. “según el contrato decidido en la tarea de cobertura” y “según el modo que le asigne la matriz de cobertura”: no se adjuntan contrato ni matriz; obliga a inventar qué piezas se migran/reemplazan y si se compila YAML, grafo o ambos.
2. “produce diagramas tanto desde un spec autorado como desde una proyección del grafo”, frente a “Fuera: renderizado a formatos de salida”: obliga a decidir si “diagrama” es solo IR o un artefacto renderizado.
3. “la misma representación intermedia”: no define igualdad; obliga a inventar criterio de comparación y tolerancias.
4. “los mismos errores tipados que en spec2viz”: no hay catálogo; obliga a inventar equivalencia exacta y excepciones.
5. “proyección equivalente del grafo”: no define equivalencia spec/proyección; obliga a inventar la correspondencia.
6. “depende de ella por la cadena IR13a e IR12”, pero `depends_on` solo lista IR06/IR07: obliga a inventar orden y dependencias reales.
7. “El paquete no importa spec2viz”, frente a paridad con “fixtures y pruebas de compiladores de spec2viz”: obliga a decidir si las pruebas pueden importar spec2viz/fixtures.

## DRY-RUN
Lecturas: TaskDoc, pills, IR06/IR07, contrato/matriz de cobertura, fixtures y pruebas de spec2viz, API pública de SLDB y módulos existentes. Cambios previstos: crear/extender los archivos listados; modelos de spec, loader/validator, IR, ocho compiladores, proyecciones y pruebas. Dependencias: decisiones de cobertura, API SLDB, fixtures de spec2viz y secuencia IR13a/IR12/IR13d. Validaciones futuras: pruebas de paridad, errores YAML, proyecciones Post/un documento, equivalencia autorado/proyección, colisiones de nombres e import de spec2viz. Sin ejecutar nada.

## FUTURO
La tarea de cobertura produce contrato y matriz; IR13d extiende la API pública tras esta tarea; IR13a/IR12 habilitan el orden declarado. Un humano confirma alcance de “diagrama”, criterio de equivalencia y aislamiento de pruebas si no quedan fijados en la matriz.
