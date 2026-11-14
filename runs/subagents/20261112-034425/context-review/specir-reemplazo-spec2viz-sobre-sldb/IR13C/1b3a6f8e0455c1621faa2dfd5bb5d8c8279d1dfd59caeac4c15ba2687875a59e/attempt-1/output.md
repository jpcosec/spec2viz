REFORMULACION
IR13C es un nodo de entrega de código, ejecutable, en el repo specIR. Propósito: exponer desde specIR las operaciones de notaciones (NotationDoc, GlyphDoc, LinkDoc) y paletas (PaletteDoc) delegando en la API pública de SLDB, sin redefinir modelos ni importar spec2viz. Resultado: código en src/specir/visual y pruebas que demuestren listar, validar, sincronizar al store y resolver la vista de notaciones, y listar, validar y sincronizar paletas con comprobación de contraste. Límites: fuera redefinir vocabulario visual, reimplementar el resolvedor, catálogos, CLI general y migración de consumidores.

AMBIGUEDADES
1. “listar, validar y sincronizar paletas (PaletteDoc)” frente a output_scope, que solo incluye src/specir/visual/notations.py y tests/visual/test_palettes.py. Obligaría a inventar dónde vive el código de paletas.
2. “Las pruebas anteriores pasan”: no se enumeran. Obligaría a inventar qué suite previa y qué casos cuentan.
3. “Sincronizar una notación desde specIR deja en un store de prueba…” no define la interfaz de store ni el fixture. Obligaría a inventar el protocolo y el store de prueba.
4. “reporta los mismos problemas que spec2viz”: no fija formato, mensajes ni oráculo de comparación. Obligaría a inventar el criterio de equivalencia.

DRY-RUN
Lecturas: API pública de SLDB para NotationDoc, GlyphDoc, LinkDoc y PaletteDoc; paquete visual existente en specIR; fixtures de notaciones y paletas; filas de la matriz de IR07. Cambios previstos: crear src/specir/visual/notations.py con envoltorios de listar, validar, sincronizar y resolver vista; crear tests/visual/test_notations.py y tests/visual/test_palettes.py. Dependencias: disponibilidad y firma de la API pública de SLDB; filas de IR07. Validaciones futuras: builtin listadas, errores equivalentes incluido contraste, sincronización en store de prueba, igualdad de vista con SLDB, ausencia de clases homónimas e import de spec2viz.

FUTURO
IR07 define las filas y condiciones de retiro; IR13D consume estas operaciones para CLI, API pública y habilidad; IR13 ejecuta el gate de retiro; el dueño de SLDB decide estabilidad de la API; un humano valida la equivalencia con spec2viz antes de declarar el retiro.
