PASA

# Resultado del tester — marcador parity sin dependencia de spec2viz

- Tarea: `task-sin-marcador-parity-ni-dependencia-de-spec2viz-en-las-pruebas-de-ir`.
- Commit del ejecutor: `3de8d97e58fc7b1ce9d0d37391f11bfa6b73b462` — *Describe parity marker as golden-based, no spec2viz needed*.
- Archivos del commit: solo `pyproject.toml` (1 línea cambiada). No toca `src/` ni `tests/`, así que no hay `tests/test_<modulo>.py` adicionales que correr.
- Entorno: `/mnt/ssd/proyectos/SLDB_1/IR`; el `.venv` del repo no arranca en este contenedor (fue creado para Python 3.12 pero `/usr/bin/python3` es 3.11). Usé Python 3.12.16 de `/dev/shm/uvpy` con `PYTHONPATH` al `src` del repo, `sldb/src` y los `site-packages` 3.12 del `.venv`, más envoltorios `sldb`/`specir` que replican los console scripts (`sys.exit(main())`). `TMPDIR=/tmp` y `--basetemp=/tmp/pytest-deskops-t-cad81b085b87`.

## Comprobaciones

| Comprobación | Resultado |
|---|---|
| `git show 3de8d97 -- pyproject.toml` | Solo cambia el texto del marcador `parity`; el texto nuevo es exactamente `parity: compares specIR with the frozen spec2viz outputs (revision 2de1056) in tests/visual/goldens/; spec2viz is not needed`. |
| `pytest --markers` | Publica el nuevo texto del marcador `parity`, con goldens 2de1056 y `spec2viz is not needed`. |
| Los goldens existen | `tests/visual/goldens/spec2viz-2de1056{,-lint,-oracle,-renders,-schema}.json` presentes y versionados. |
| `PYTHONPATH=src TMPDIR=/tmp python -m pytest -q -m parity -rs -p no:cacheprovider tests/visual` | **63 passed, 563 deselected, 0 skipped**, rc 0 (296,59 s). Sin líneas de skip en `-rs`. |

## Veredicto

**PASA**: el marcador describe la comparación contra los goldens congelados de spec2viz y que spec2viz no hace falta; la suite de paridad pasa completa sin ningún test saltado por falta de spec2viz.
