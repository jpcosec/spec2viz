## REFORMULACION

Encargo ejecutable (`task.code`): en el repo SLDB_1/IR, dentro de specIR, crear `src/specir/visual/notations.py` como envoltorio de las operaciones de notaciones, vistas y paletas de la API pública de SLDB, y portar pruebas a `tests/visual/test_notations.py` y `tests/visual/test_palettes.py`. Propósito: completar la migración que permite retirar spec2viz ofreciendo desde specIR el camino de notaciones y paletas. Resultado: listar, validar, sincronizar y resolver vistas de notaciones, y listar, validar y sincronizar paletas con comprobación de contraste, delegando en SLDB. Límites: no redefinir modelos de vocabulario visual ni reimplementar el resolvedor; fuera catálogos, CLI general y migración de consumidores.

## AMBIGUEDADES

1. “Paridad medida portando a tests/visual/ las pruebas de spec2viz”: no indica ruta, versión ni selección de esas pruebas; obligaría a inventar el corpus de origen.
2. “incluida la comprobación de contraste”: no fija umbral ni operación concreta; obligaría a inventar el criterio o asumir uno de SLDB.
3. “deja en un store de prueba”: no identifica backend, ubicación ni forma de provisión; obligaría a inventar infraestructura de pruebas.
4. “las builtin que distribuye SLDB”: no nombra la operación pública de listado; obligaría a inventar nombre y contrato.
5. “specIR expone las operaciones”: no define firmas, nombres ni si existe envoltorio CLI; obligaría a inventar la interfaz pública.
6. “las filas de notaciones y paletas de la matriz de cobertura”: no da ruta, formato ni condición exacta; obligaría a inventar la matriz y sus columnas.
7. “una notación o una paleta inválida de los fixtures”: no especifica qué fixtures ni su origen; obligaría a inventarlos.

## DRY-RUN

Lecturas hipotéticas: TaskDoc, pills, archivos listados, tarea dependiente IR07, API pública de SLDB y pruebas de spec2viz. Cambios previstos: crear el módulo de delegación y portar/adaptar las pruebas de notación, vista y paleta. Dependencias: API pública de SLDB, fixtures, store de prueba y corpus de pruebas de spec2viz. Validaciones futuras: listar builtins; comparar errores de validación, incluido contraste; comprobar NotationDoc, GlyphDoc y LinkDoc tras sincronizar; comparar vista resuelta con SLDB; verificar ausencia de clases modelo propias y de importaciones de spec2viz; ejecutar la suite.

## FUTURO

Otro nodo o el agregado IR13 aporta/actualiza la matriz de cobertura y verifica sus filas. Un humano o nodo de revisión debe confirmar la fuente exacta de pruebas de spec2viz y aprobar el cierre.
