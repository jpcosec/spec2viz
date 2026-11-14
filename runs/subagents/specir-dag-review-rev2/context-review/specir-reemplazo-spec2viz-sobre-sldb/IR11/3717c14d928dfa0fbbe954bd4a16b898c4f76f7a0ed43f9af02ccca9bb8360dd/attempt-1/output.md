REFORMULACION
Propósito: implementar en specIR los modelos, carga/validación, representación intermedia, compiladores y proyecciones de los ocho tipos de diagrama de spec2viz, desde spec autorado y desde grafo. Resultado: código y pruebas en `src/specir/visual/` y `tests/visual/` listados en `output_scope`. Repo: specIR. Límites: fuera renderizado, linter, recursos, sincronización al store, catálogos, consumidores y retiro de spec2viz; depende de IR07 e IR06.

AMBIGUEDADES
1. “según el contrato decidido en la tarea de cobertura” y “modo que le asigne la matriz”: no se incluye la matriz ni el contrato; obligaría a inventar qué piezas se migran, reemplazan o exponen.
2. “representación intermedia”: no se define su esquema; obligaría a inventar campos, nodos y aristas.
3. “normalización definida en el camino de implementación”: no se especifica; obligaría a inventar reglas de equivalencia estructural.
4. “ViewDoc evaluado sobre el grafo” y “proyección equivalente”: faltan API y semántica; obligaría a inventar cómo evaluar y materializar.
5. “mismos errores tipados que en spec2viz”: no hay taxonomía citada; obligaría a inventar tipos y mensajes.
6. “modelos de vocabulario visual se usan desde SLDB”: no se indica módulo/API; obligaría a inventar rutas de importación.

DRY-RUN
Lecturas hipotéticas: contratos IR07/IR06, matriz de cobertura, fuentes/fixtures de spec2viz, API de vocabulario visual SLDB y archivos de `output_scope`. Cambios previstos: crear modelos, loader, validator, IR, compiladores, proyecciones y pruebas de paridad/normalización/imports. Dependencias: decisiones de IR07, modelos y store del blog de IR06, fixtures spec2viz, API pública SLDB. Validaciones futuras: ocho tipos compilan; normalización distingue orden/metadata de diferencias reales; YAML valida con errores equivalentes; proyecciones del blog muestran `Post` con un solo documento; spec autorado y proyección equivalentes; no se redefine vocabulario visual; `src/specir/` no importa spec2viz. Sin ejecutar nada.

FUTURO
IR07 debe entregar matriz, modos, condición de retiro y decisión YAML/grafo. IR06 debe aportar modelos transversales y store del blog. Un humano decide si falta precisar normalización o contrato. IR12 consumirá la IR; IR13a la sincronización/importación; IR13 validará el gate conjunto.
