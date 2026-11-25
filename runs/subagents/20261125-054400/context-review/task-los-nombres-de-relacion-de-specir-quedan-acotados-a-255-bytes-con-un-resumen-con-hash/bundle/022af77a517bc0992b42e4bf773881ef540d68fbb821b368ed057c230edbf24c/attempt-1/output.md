## REFORMULACION

**Propósito:** eliminar el `OSError Errno 36 File name too long` que aborta `extract_frontend` sobre graph_ui, donde 21 de 133 relaciones superan 250 bytes (máx. 266).

**Resultado:** que `edge_name` sea determinista y acotado: si el nombre completo cabe en 200 bytes UTF-8 queda igual; si no, prefijo legible + `-` + 12 primeros hex del sha256 del nombre completo, total ≤200 bytes; entradas distintas largas dan nombres distintos; resultado UTF-8 válido. Test nuevo cubre (a)–(e), incluido `len(Path(p.path).name.encode()) <= 255` para `.md` y `.yaml`.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/IR`.

**Límites:** solo `src/specir/extract/plan.py` (`edge_name`) y `tests/extract/test_edge_name_bounded.py`; fuera nombres de nodos, otros extractores y migración de stores. Validación: pytest de ese test y `tests/extract/test_frontend_extraction.py`.

## AMBIGUEDADES

1. «se recorta a un prefijo legible»: no fija longitud ni criterio de corte (bytes, caracteres, segmentos); obliga a inventar el algoritmo del prefijo.
2. «llamando al recorte directamente si slug los quitaria»: no define si debe existir función auxiliar, su nombre, firma ni importación; obliga a inventar API interna.
3. «un componente TSX en una ruta profunda»: no fija profundidad ni contenido del fixture; obliga a inventar el árbol temporal y el TSX mínimo.
4. «los 12 primeros hex del sha256 del nombre completo»: no fija minúsculas/mayúsculas; obliga a decidir formato.
5. «dos entradas distintas largas dan nombres distintos»: con hash truncado no se garantiza ausencia de colisión; obliga a asumir si es garantía o solo el caso probado.

## DRY-RUN

**Lecturas:** `plan.py` (`edge_name` ~línea 65, `Planned.path` ~línea 49), `test_frontend_extraction.py`, fixtures TSX y venv. **Cambios previstos:** calcular nombre completo, medir bytes UTF-8, devolverlo intacto si ≤200 o recortar con sufijo hash seguro UTF-8; crear test (a)–(e) con comprobación de `Planned.path`. **Dependencias:** `hashlib.sha256`, tree-sitter-typescript en venv. **Validaciones futuras:** ejecutar el comando pytest indicado con `TMPDIR` y `PYTHONPATH`, verificar (a)–(e) y no regresión en frontend.

## FUTURO

Un ejecutor implementa el cambio y corre la validación; closeout/humano decide cierre y commit; nodos posteriores consumen el nombre acotado; la migración de stores existentes queda fuera y podría decidirse aparte.
