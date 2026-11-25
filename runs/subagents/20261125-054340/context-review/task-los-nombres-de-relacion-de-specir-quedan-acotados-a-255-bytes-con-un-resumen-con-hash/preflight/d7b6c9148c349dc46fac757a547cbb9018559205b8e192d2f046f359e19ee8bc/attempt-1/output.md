## REFORMULACION

Encargo ejecutable `task.code`: modificar `edge_name` en `src/specir/extract/plan.py` para que ningún nombre de relación generado por specIR supere 255 bytes, de forma determinista y estable. El propósito es evitar `OSError Errno 36 File name too long` al ejecutar `extract_frontend` sobre árboles con rutas profundas (caso `graph_ui`: 21/133 relaciones >250 bytes).

Resultado esperado: si el nombre completo cabe en 200 bytes UTF-8, se conserva; si no, se recorta a un prefijo legible más `-` y los 12 primeros hex de `sha256(nombre completo)`, con total ≤200 bytes. Se añade `tests/extract/test_edge_name_bounded.py` con los casos (a)-(e), incluyendo nombres de archivo de `Planned.path` (`.md` y `.yaml`) ≤255 bytes y validez UTF-8 del recorte. Debe pasar junto con `tests/extract/test_frontend_extraction.py`.

Repo: `/mnt/ssd/proyectos/SLDB_1/IR`. Límites: solo `edge_name` y el test indicado; fuera de alcance nombres de nodos, otros extractores y migración de stores existentes.

## AMBIGUEDADES

1. El título dice “acotados a 255 bytes”, pero el contrato técnico fija “cabe en 200 bytes UTF-8”. Obliga a decidir si 200 es el límite efectivo del nombre y 255 solo del archivo final.
2. “se recorta a un prefijo legible” no define cómo recortar: ¿bytes, caracteres, límite de slug, separadores? Obliga a inventar el algoritmo de truncado.
3. “llamando al recorte directamente si slug los quitaria” presupone una función de recorte invocable, pero no nombra su API ni si deberá extraerse. Obliga a inventar nombre, firma y visibilidad.
4. “Solo src/specir/extract/plan.py (edge_name) y un test” contrasta con “el test comprueba ademas len(Path(p.path).name.encode()) <= 255”. Obliga a interpretar si solo se prueba `Planned.path` o también se modifica.

## DRY-RUN

Lecturas previas: `plan.py` líneas 49 y 65, `tests/extract/test_frontend_extraction.py`, fixtures TSX y README del plan. Cambios previstos: implementar el truncado determinista en `edge_name`; crear el test con casos (a)-(e). Dependencias: pytest, tree-sitter-typescript en `.venv`, `TMPDIR=/mnt/ssd/tmp/sldb1`, `PYTHONPATH=src`. Validación futura: ejecutar el comando pytest indicado. Sin ejecutar nada.

## FUTURO

Otro nodo ejecutará la validación y aportará evidencia pytest. Un humano decidirá si acepta el algoritmo concreto de “prefijo legible” y el límite de 200 bytes.
