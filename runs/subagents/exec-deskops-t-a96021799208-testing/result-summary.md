PASA

# Result summary — tester

- Task: `task-las-pruebas-de-paridad-de-ir-comparan-contra-goldens-congelados-de-spec2viz-y-dejan-de-importarlo-ac`
- Commit del ejecutor: `c47111de57c53e75a15a565ec945b73695de96c8`
- Comprobado el commit (no hay cambios sin commitear en `tests/`).

## Qué se probó

Se ejecutaron de a uno, en procesos separados, todos los módulos `tests/*.py` tocados por el commit:

`tests/visual/test_visual_names.py`, `test_schema.py`, `test_resources.py`, `test_render_cases.py`,
`test_lint_mermaid.py`, `test_render_commands.py`, `test_render_parity.py`, `test_visual_parity.py`,
`test_catalog_parity.py`, `test_sync_generation_parity.py`, `tests/visual/test_cli.py` y
`tests/test_matriz_cobertura_spec2viz.py`.

No se tocó ningún módulo de `src/`, así que no hay `tests/test_<modulo>.py` adicionales que correr.
Los helpers `tests/visual/oracle.py`, `parity.py` y `render_parity.py` se ejercitan desde esas pruebas.

Comando base: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider <archivo>`.

## Resultado

Con `spec2viz` instalado:

| archivo | resultado |
|---|---|
| test_visual_names.py | 4 passed |
| test_schema.py | 12 passed |
| test_resources.py | 6 passed, 1 skipped (uv ausente) |
| test_render_cases.py | 27 passed, 3 skipped (mmdc ausente) |
| test_lint_mermaid.py | 7 passed, 7 skipped (mmdc ausente) |
| test_render_commands.py | 33 passed |
| test_render_parity.py | 45 passed |
| test_visual_parity.py | 45 passed |
| test_catalog_parity.py | 29 passed |
| test_sync_generation_parity.py | 22 passed |
| test_cli.py | 40 passed |
| test_matriz_cobertura_spec2viz.py | 5 passed |

Total: **275 passed, 11 skipped, exit 0**. Los skips son de entorno (mmdc/uv no instalados), no del cambio.

## Sin spec2viz importable

Se repitieron los mismos 12 archivos bloqueando el import de `spec2viz` mediante un
`sitecustomize.py` temporal en `PYTHONPATH` cuyo `MetaPathFinder` lanza `ImportError` para
`spec2viz` y `spec2viz.*` (verificado: `import spec2viz` falla).

Resultado idéntico en cada archivo: **275 passed, 11 skipped, exit 0**, sin ninguna importación ni
dependencia de `spec2viz` en tiempo de ejecución. Los logs están en `logs/*.nospec2viz.log`.

## Comprobaciones adicionales

- `test_visual_names.py::test_spec2viz_is_imported_by_nobody` pasa: ningún `.py` de `src/specir` ni
  de `tests/` importa `spec2viz`.
- `tests/test_matriz_cobertura_spec2viz.py` pasa sin el checkout de spec2viz: usa las listas
  congeladas del golden (`cli_commands`, `package_modules`, `test_files`).
- `specir retirement check` sobre un checkout limpio del commit (`git worktree` temporal en
  `/tmp/ir-clean-verify`, sin artefactos untracked de `runs/`) da **0 dependencias de IR**; solo
  lista las 19 de `spec2viz/.sldb`, fuera del alcance. La fila abierta `SV-A17` no es de esta tarea.
  Salida: `retirement-check-clean.txt`.
- Observación: ejecutado desde este directorio de trabajo (que contiene los artefactos untracked
  `runs/subagents/exec-deskops-e-5ccf277d5e67/`), el check lista las importaciones del script de
  grabación `record_goldens.py` de ese run dir. Ese script no forma parte del commit y el checkout
  limpio del commit no lo contiene; la tarea lo sitúa deliberadamente en `runs/<run>/` fuera de
  `tests/`. Salida: `retirement-check.txt`. No afecta al veredicto de las pruebas.

## Veredicto

**PASA**: los mismos casos de paridad pasan con y sin `spec2viz` importable, y el commit no deja
dependencias de IR sobre spec2viz.
