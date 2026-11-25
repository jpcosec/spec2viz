run_id: exec-deskops-e-a347e2092180
session: n/a (claude executor, no child session file)
session_sha256: n/a

## Hecho
- `ExtractionReport.skipped: list[str]` (write.py); `extract_frontend` lo llena desde `code_facts()["skipped"]` (extract/__init__.py).
- Grupo `specir ux` con `extract ROOT [--store] [--path P ...] [--strict]` (cli.py): resumen en stdout, aviso en stderr con cuenta y primeros 10 (sldb solo da rutas, sin motivo), rc 0; con --strict y saltados rc 1.
- Test nuevo tests/extract/test_ux_extract_cli.py (a: .tsx extrae rc 0; b: skipped simulado -> aviso y --strict rc 1).

## Validacion
14 passed (ver validation.log). Nota: el venv necesito instalar a mano las gramaticas tree-sitter (sin ellas los .tsx se saltan y fallan tests existentes).

## Archivos
src/specir/cli.py, src/specir/extract/__init__.py, src/specir/extract/write.py, tests/extract/test_ux_extract_cli.py
