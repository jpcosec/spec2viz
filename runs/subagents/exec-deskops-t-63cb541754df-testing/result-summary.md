PASA

# Resultado del tester (matriz spec2viz: SV-K16/K21/K26/K29 a sldb notations validate)

- task: `task-matriz-de-spec2viz-sv-k16-k21-k26-y-k29-pasan-a-sldb-notations-validate-y-se-retiran-los-validate-pr`
- commit del ejecutor: `3d0a436c52e07e5eb40922ccd06e06c65c650cdb` — *spec2viz: SV-K16, K21, K26 y K29 pasan a sldb notations validate; se retiran diagram validate y validate de specIR*
- archivos del commit: `docs/spec2viz/matriz-de-cobertura.md`, `docs/spec2viz/correspondencia-cli.md`, `skills/use-specir/SKILL.md`, `src/specir/cli.py`, `src/specir/visual/commands.py`, `src/specir/visual/render_file.py`, `tests/visual/test_cli.py`, `tests/visual/test_packaging.py`, `tests/visual/test_render_cases.py`, `tests/visual/test_render_commands.py`.
- entorno: `/workspace/IR/.venv/bin/python` (3.13), `TMPDIR=/tmp`; el `sldb` que usan las pruebas es `.venv/bin/sldb` (0.1.13).

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| `pytest -q -p no:cacheprovider tests/visual/test_cli.py` | **40 passed**, rc 0 (56 s) |
| `pytest -q -p no:cacheprovider tests/test_matriz_cobertura_spec2viz.py` | **5 passed**, rc 0 |
| `pytest -q -p no:cacheprovider tests/visual/test_retirement_gate.py` | **6 passed, 1 xfailed**, rc 0 (5 s) |
| `pytest -q -p no:cacheprovider tests/visual/test_render_cases.py` | **27 passed, 3 skipped**, rc 0 (66 s) |
| `pytest -q -p no:cacheprovider tests/visual/test_render_commands.py` | **33 passed**, rc 0 |
| `pytest -q -p no:cacheprovider tests/visual/test_packaging.py` | **2 passed, 1 skipped**, rc 0 |
| `specir retirement check` con las rutas del inventario | rc 1 por las dependencias restantes (paridad/G5, fuera de alcance); **1 fila no acreditada: solo SV-A17** |

El xfail de `test_retirement_gate.py` es el estricto preexistente de la corrida real (`test_the_real_universe_has_no_dependency_and_every_row_is_accredited`), que sigue fallando porque quedan dependencias de paridad y el store G5; no hay filas abiertas además de SV-A17. Los skips de `test_render_cases.py` y `test_packaging.py` son los condicionales de entorno/mmdc y de instalación limpia ya existentes.

## Cumplimiento del encargo

1. **Filas SV-K16, K21, K26 y SV-K29.** En `docs/spec2viz/matriz-de-cobertura.md` quedan en modo «usar sldb directamente», con equivalente `sldb notations validate` y estado `cumplida`, citando pruebas de `tests/visual/test_cli.py` y `tests/visual/test_render_commands.py`. Lo mismo en la tabla de `docs/spec2viz/correspondencia-cli.md` (con `--json --store`, opciones que la ayuda de sldb sí acepta).
2. **Subgrupos SV-K09, K18 y K23.** Pasan a `cumplida` con sus hijas acreditadas (SV-K10 a K16, SV-K19 a K22 y SV-K24 a K26).
3. **Retiro de los validate provisionales.** `specir diagram validate` y el alias `specir validate` ya no existen en `src/specir`; la ayuda raíz, `about`, la skill y la cabecera de procedencia remiten a `sldb notations validate`. `test_specir_defines_no_validate_command` comprueba que specIR no los define y que el comando de sldb valida un spec válido (rc 0) y uno inválido (rc 1).
4. **Tabla de equivalentes.** `test_every_equivalent_of_the_table_answers_its_help` recorre las 30 filas e invoca `sldb notations validate ... --help`; pasa.
5. **Gate de retiro.** `specir retirement check` deja abierta únicamente SV-A17; la salida quedó en `retirement-check.txt`.

## Nota no bloqueante

El docstring de `src/specir/visual/render_file.py` (línea 6) aún dice «the specIR command that validates it» al describir la cabecera, aunque la cabecera ya nombra `sldb notations validate`. Es una mención en prosa, no afecta a la ayuda, las pruebas ni el gate.

## Veredicto

**PASA.** Las tres validaciones exigidas y los demás archivos de test del commit pasan de a uno; los comandos de validate de specIR se retiraron y el gate solo mantiene abierta SV-A17.
