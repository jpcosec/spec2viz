## REFORMULACION

**Propósito:** portar a IR, contra la API pública de sldb, las pruebas de notaciones, paletas y vistas de spec2viz, como evidencia para el gate de retiro (IR13). **Resultado:** `tests/visual/test_notations_parity.py` con 40 casos portados y 9 comparaciones «valida igual», fixtures copiados de spec2viz, 16 filas de la matriz actualizadas y el acta con la nueva salida de `specir retirement check`. **Repo:** solo IR/specIR; spec2viz y sldb son referencias de solo lectura y sus cambios se piden por desk. **Límites:** no implementar capacidades, no modificar sldb/spec2viz, no tocar filas fuera de alcance, no declarar el retiro. Es una tarea ejecutable (`task.code`), no un agregado.

## AMBIGUEDADES

1. «reporta las 40 pruebas portadas más las 9 comparaciones «valida igual»» frente a «Son 40 pruebas portadas». No queda claro si las 9 comparaciones ya están incluidas en las 40 o son adicionales (total 49). Obliga a inventar el recuento real que debe reportar pytest.
2. «su contenido modelado es igual al de la builtin de sldb del mismo nombre». «Contenido modelado» no define campos, normalización ni tolerancias; obliga a inventar el criterio de igualdad.
3. «las dos de mermaid se portan contra el renderer de specIR, specir.visual». No se nombra módulo ni función concreta del renderer; obliga a inventar el punto de importación.

## DRY-RUN

**Lecturas:** TaskDoc, pills y átomos; `src/specir/visual/notation_style.py`; `docs/spec2viz/matriz-de-cobertura.md` y `acta-de-retiro.md`; en spec2viz, solo lectura de `tests/test_view_doc.py`, `test_notation.py`, `test_notation_view.py`, `test_view_contract_resolved.py`, `test_style_palette.py`, notaciones y paleta en la revisión indicada. **Cambios previstos:** crear el archivo de pruebas y `tests/visual/fixtures/spec2viz-notations/` con README; ampliar reexportaciones y `__all__` en `notation_style.py`; actualizar matriz y acta. **Dependencias:** que `sldb.api` exporte lo necesario y `ViewDoc`; builtins de sldb; renderer de `specir.visual`; disponibilidad de la revisión de spec2viz. **Validaciones futuras:** pytest focalizado, tests de importación/matriz/gate, comprobador de retiro, suite completa bajo `flock` y `deskops graph missing`. Nada se ejecuta ahora.

## FUTURO

El desk de sldb debe exportar `ViewDoc` y las APIs faltantes y responder a las notas; el desk de spec2viz provee la revisión; un humano decide el retiro/archivo; el ritual de fase integra la capa y closeout actualiza board y commit.
