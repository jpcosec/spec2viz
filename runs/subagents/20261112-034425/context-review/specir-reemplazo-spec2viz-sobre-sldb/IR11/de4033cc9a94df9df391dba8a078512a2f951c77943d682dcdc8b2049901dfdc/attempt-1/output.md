## REFORMULACION
IR11 es un nodo de entrega de código en el repo `specIR`. Propósito: implementar la capa visual que compila los ocho tipos de diagrama de spec2viz y materializa proyecciones desde un `ViewDoc` evaluado sobre el grafo y desde un `SpecDoc` con sus `SpecNodeDoc` hacia una representación intermedia común, usando los modelos de vocabulario visual de SLDB sin redefinirlos. Resultado: los módulos `src/specir/visual/*` y sus pruebas en `tests/visual/`. Límites: fuera renderizado, linter, recursos empaquetados, sincronización al store, catálogos, consumidores y retiro de spec2viz; depende de IR07 e IR06.

## AMBIGUEDADES
1. “según la normalización definida en el camino de implementación”: la normalización no está definida en el input; obligaría a inventar los criterios de equivalencia estructural.
2. “desde la proyección equivalente del grafo”: no se define qué proyección equivale a un spec autorado; obligaría a inventar el mapeo de equivalencia.
3. “muestran la entidad Post”: no aclara si se comprueba en la representación intermedia o en un diagrama renderizado; como el renderizado está fuera, obligaría a inventar el nivel de verificación.
4. “el store sigue teniendo un solo documento para ella”: no nombra el store; obligaría a asumir que es el store de prueba de IR06.

## DRY-RUN
Lecturas: matriz y decisión de IR07; modelos, tipos de relación, reglas y store del blog de IR06; API pública de SLDB para vocabulario visual; fixtures de spec2viz. Cambios previstos: crear los archivos de `output_scope` con modelos de spec, carga, validación, IR, compiladores, proyecciones y pruebas. Dependencias: modo migrar/reemplazar por fila de IR07, tipos de IR06 y contratos `ViewDoc`/`SpecDoc` de SLDB. Validaciones futuras: paridad por tipo de diagrama, prueba de normalización, validación de YAML, proyecciones del blog, no redefinición de modelos SLDB y prueba de imports. Sin ejecutar nada.

## FUTURO
IR07 debe entregar la matriz de cobertura, el contrato de modos y la decisión YAML/grafo. IR06 debe entregar los modelos de dominio y el store del blog. La ruta de implementación debe fijar la normalización. IR12 consumirá la representación intermedia de IR11. Nada de esto se decide en esta revisión.
