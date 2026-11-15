## REFORMULACION

**Propósito:** migrar a specIR los compiladores de spec2viz y la materialización de proyecciones, sin redefinir lo que ya vive en SLDB.
**Resultado:** los ocho tipos de diagrama (clase, secuencia, estado, componente, actividad, despliegue, matriz, reflexión) compilan a una representación intermedia propia, generada tanto desde un spec autorado como desde una proyección del grafo (ViewDoc vía `run_view`/`evaluate_projection_view`, SpecDoc vía `resolve_view`), con paridad demostrada contra spec2viz 2de1056.
**Repo:** specIR; `src/specir/visual/` y `tests/visual/`.
**Límites:** no definir modelos de spec ni vocabulario visual (vienen de sldb); no índice/backend, render, linter, sincronización, catálogos ni retiro de spec2viz; solo `sldb.api` (excepción acotada en `spec_models.py`); `src/` no importa spec2viz.

## AMBIGUEDADES

1. «representación intermedia visual propia de specIR» frente a «mismos tipos de elemento, mismos campos con los mismos valores»: no se fija si la IR se diseña libre o debe espejar campo a campo la salida de spec2viz; obliga a inventar el esquema y el criterio de comparación.
2. «el corpus son los 44 specs de spec2viz (tests/fixtures con invalid/, examples/, docs/architecture/spec2viz/)»: no dice qué subconjunto debe compilar y cuál solo producir error; obliga a inventar la partición válidos/inválidos.
3. «Compilar desde un spec autorado y desde la proyección equivalente del grafo da representaciones […] equivalentes»: solo el blog fija pares estados/componentes; para los otros seis tipos obliga a inventar qué proyección equivale a qué spec.
4. «files: []» frente a «esta tarea crea src/specir/visual/__init__.py»: obliga a decidir qué lista de archivos es la autoritativa.

## DRY-RUN

**Lecturas:** TaskDoc y rituales; pills y átomos; `docs/spec2viz/matriz-de-cobertura.md` (SV-B01–SV-B10, SV-A14); `docs/decisiones/fuente-de-verdad-del-diagrama.md`; fixtures y tests de spec2viz 2de1056; firmas de `sldb.api` (641ecdfa).
**Cambios previstos:** `spec_models.py`, compiladores por tipo, `projections.py`, `__init__.py`, `tests/visual/parity.py`, copia de fixtures, `goldens/spec2viz-2de1056.json`, excepción en `tests/test_imports.py`.
**Dependencias:** IR07 (contrato), IR06 (blog), exportación de clases por el desk de SLDB, spec2viz instalado editable.
**Validaciones futuras:** los ocho checks de la sección Validation del TaskDoc.

## FUTURO

JP firma `fuente-de-verdad-del-diagrama.md`; IR07 fija el contrato de filas; el desk de SLDB exporta las clases de modelos; IR13d amplía `__init__.py`; una decisión humana resuelve la permanencia del YAML; el retiro de spec2viz sustituye el oráculo por goldens.
