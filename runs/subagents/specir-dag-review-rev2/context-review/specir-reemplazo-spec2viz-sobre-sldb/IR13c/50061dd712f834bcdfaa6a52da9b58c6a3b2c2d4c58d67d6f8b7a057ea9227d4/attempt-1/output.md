REFORMULACION
Propósito: que specIR exponga las operaciones de notaciones y paletas de spec2viz delegando en la API pública de SLDB, sin redefinir modelos. Resultado: módulo `src/specir/visual/notations.py` y pruebas `test_notations.py`/`test_palettes.py`. Repo: specIR. Límites: dentro, listar/validar/sincronizar/resolver notaciones (NotationDoc, GlyphDoc, LinkDoc) y listar/validar/sincronizar paletas (PaletteDoc) con contraste; fuera, redefinir modelos de vocabulario visual, reimplementar el resolvedor de vistas, catálogos, CLI general y migración de consumidores. Depende de IR07.

AMBIGUEDADES
1. “una notación o una paleta inválida de los fixtures”: no se identifica ruta, conjunto ni contenido de fixtures; obligaría a inventar qué fixtures usar y qué problemas esperar.
2. “los mismos problemas que spec2viz”: no se fija referencia concreta (versión, comando o API) ni cómo obtenerla sin importar spec2viz; obligaría a inventar el oráculo de comparación.
3. “las builtin que distribuye SLDB”: no se nombran las operaciones públicas de SLDB ni sus rutas; obligaría a inventar nombres y firmas.
4. “incluida la comprobación de contraste”: no se fija umbral, norma ni algoritmo; obligaría a inventar el criterio.
5. `output_scope` solo declara `src/specir/visual/notations.py` para producción, pero también hay paletas; no dice dónde vive el código de paletas; obligaría a inventar un módulo o asumir que va en `notations.py`.
6. “La vista resuelta de un spec de fixture”: no se define qué operación constituye “vista resuelta” ni el spec de fixture; obligaría a inventar la llamada y el dato.

DRY-RUN
Lecturas: nodo, API pública de SLDB, fixtures y matriz IR07. Cambios previstos: crear/extender `notations.py` y las pruebas. Dependencias: operaciones SLDB de notaciones/paletas y store de prueba. Validaciones futuras: builtin listadas; fixtures inválidos con los mismos problemas; sync deja NotationDoc/GlyphDoc/LinkDoc; vista igual a SLDB; sin clases homónimas ni import de spec2viz.

FUTURO
IR13 usará la evidencia para el gate; IR13d expondrá CLI/API/habilidad; el dueño de spec2viz decidirá archivarlo. Nada de esto es ambigüedad.
