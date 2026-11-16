## REFORMULACION

Encargo ejecutable (nodo `task.code`, no agregado). Propósito: aportar evidencia para el gate de retiro de spec2viz portando a IR las pruebas de notaciones, paletas y vistas de spec2viz, ejecutándolas contra sldb. Resultado: `tests/visual/test_notations_parity.py` con 40 pruebas portadas (docstring citando la prueba origen) más 9 comparaciones «valida igual» (8 notaciones + paleta default), fixtures copiados como datos en `tests/visual/fixtures/spec2viz-notations/` con README de una línea, reexportaciones en `src/specir/visual/notation_style.py`, y matriz/acta actualizadas (16 filas SV-* y resumen). Repo: IR, raíz actual, `.venv` propio, `TMPDIR=/dev/shm`. Límites: no tocar código de sldb ni spec2viz; no implementar notaciones/paletas/vistas; no cambiar IR07; no declarar retiro; filas SV-G08, SV-I02, SV-K09, SV-K16, SV-K21, SV-K26, SV-K29 y G5 de SV-A17 quedan fuera; un fallo real no se maquilla: xfail(strict=True) + fila abierta + nota a sldb.

## AMBIGUEDADES

1. «en la revisión b624b75 de spec2viz» — no indica cómo obtener/verificar esa revisión ni qué hacer si el checkout local difiere; obligaría a inventar el mecanismo de acceso y el criterio de conformidad.
2. «Las 10 no CLI de test_notation_view.py» — no enumera sus nombres; obligaría a inventar cuáles son (o a deducirlas por exclusión).
3. «su contenido modelado es igual al de la builtin» — no define igualdad (campos, orden, normalización); obligaría a inventar el criterio de comparación.
4. «ViewDoc se toma de sldb.api si sldb lo exporta» — no fija cómo determinarlo ni qué prueba concreta cubre SV-A17 si falta; obligaría a inventar la comprobación.
5. «anotar en docs/spec2viz/acta-de-retiro.md la nueva salida» — no dice sección ni formato; obligaría a inventar la disposición.

## DRY-RUN

Lecturas: pills de guardrail, matriz y acta, `notation_style.py`, `tests/test_imports.py`, `tests/visual/test_cli.py`, pruebas y fixtures de spec2viz en `../spec2viz` (revisión citada). Cambios previstos: crear test file y fixtures+README; añadir reexportaciones y `__all__`; editar matriz (16 filas + resumen) y acta. Dependencias: API pública de sldb instalada, `deskops`, `mmdc`, `flock`. Validaciones futuras: las cinco del apartado Validation (pytest del archivo nuevo, tests de imports/matriz/gate, greps de no-import, `specir retirement check`, suite completa con xdist, `deskops graph missing`). Nada se ejecuta ahora.

## FUTURO

Notas `deskops message send --to sldb` (exportaciones faltantes, diferencias xfail) y, si aplica, petición al desk de spec2viz por G5; decisión humana sobre acreditar filas abiertas y sobre el retiro efectivo (IR13/IR07); consumo del acta por el nodo de cierre.
