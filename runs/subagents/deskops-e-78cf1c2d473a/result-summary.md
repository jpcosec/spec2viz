# IR13i — ejecutor deskops-e-78cf1c2d473a (intento 1)

Contrato `task-ir13i-corregir-en-el-acta-el-estado-de-g5-y-la-fila-de-ir-tras-cerrar-la-federación-de-las-pruebas-m`
(sha256 `cc20a013…25f7`). Disposiciones aplicadas: preflight-1 y bundle-1 (aceptadas). Único archivo tocado:
`docs/spec2viz/acta-de-retiro.md` (`diff.patch`). Sin commit, sin `git add`.

## Qué cambié

- **Fila G5 del gate**: se quitó «(b) … hoy bloqueada: las pruebas MCP todavía leen `../spec2viz/.sldb` …».
  Ahora dice: «Resuelta en IR: las pruebas ya no federan ese store (`task-las-pruebas-de-mcp-dejan-de-federar-…-g5-opción-a`,
  código `b16aab7`, closeout `4f1e108`), después de que deskops quitara su enlace (`421d6a27`, closeout `74ffdb63`;
  pedido en la nota de inbox 20261116-122447). Pendiente: quitar `spec2viz/.sldb` del universo de `specir retirement check`
  al declarar el retiro (IR13) y archivar el store con el repo spec2viz.» El estado de la columna se mantiene
  («decidido; pendiente de ejecución en IR»), porque lo que queda de G5 sigue siendo de IR. Se conservan el id de la tarea
  y la nota 20261116-122447 como historia.
- **Lo que falta, punto 2 (G5)**: el mismo cambio. La tarea de federación «quedó resuelta» (`b16aab7`, `4f1e108`, tras
  `421d6a27`/`74ffdb63`); queda quitar el store del universo del comprobador al declarar y archivarlo con el repo.
- **Fila de IR en Consumidores**: se retiraron las dos menciones de la federación (`tests/conftest.py:24` y `:80` y
  `tests/test_mcp_extension.py:24`), según bundle-1 (1). Se conservan los oráculos de paridad y la lectura del CLI de
  `tests/test_matriz_cobertura_spec2viz.py:31`. En la columna «Mensaje enviado» se quitó también «y cambiar la federación
  por un fixture» del plan propio, porque ya está hecho. La columna «Cambio que lo resolvió» sigue en «pendiente» (oráculos).
- **Lo que falta, punto 6** (fuera de la lista literal del Scope, dentro del Goal): decía que IR tenía que quitar «la
  federación del store de spec2viz en las pruebas». Ahora solo pide quitar o congelar los oráculos de paridad y anota que
  la federación salió con `b16aab7`. Si el tester o el coordinador lo consideran fuera de alcance, se revierte esa línea
  sin afectar al resto.
- No se tocaron la matriz, las corridas del comprobador ni el recuento (63/9). No se añadió ningún bloque de corrida.

## Verificaciones (salida y rc en `validation.log`)

- `git merge-base --is-ancestor 4f1e108 HEAD` → rc 0; también `b16aab7` → rc 0.
- Grep de la ruta al store real (`WORKSPACE / "spec2viz"` o `../spec2viz`) en la versión commiteada
  (`git show HEAD:tests/conftest.py` y `HEAD:tests/test_mcp_extension.py`) → rc 1 en los dos: no hay coincidencias.
  `grep -nE spec2viz` en ambos solo muestra el nombre del enlace `spec2viz` del store temporal de specs, las rutas
  de fixtures de IR y el nombre de una prueba. No hay ninguna ruta al store real.
- `git diff --stat` fuera de desk/, .sldb/ y runs/: `docs/spec2viz/acta-de-retiro.md` más `tests/conftest.py` y
  `tests/test_mcp_extension.py`. Esos dos son cambios ajenos sin commitear de la tarea de la copia del store de deskops
  y no son míos (el brief los documenta). `tests/fixtures/blog_app/` (IR08) no aparece en el stat porque no tiene
  seguimiento. **Literalmente, este criterio de la Validation no se cumple** mientras esos cambios ajenos sigan en el árbol.
  Mi diff toca solo el acta.
- `grep -n 'bloqueada' docs/spec2viz/acta-de-retiro.md` → rc 1, sin coincidencias.
- `TMPDIR=/dev/shm .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_matriz_cobertura_spec2viz.py tests/visual/test_retirement_gate.py`
  → 11 passed, 1 xfailed, rc 0 (antes y después de corregir el punto 6). Es una validación, no una corrida nueva del acta.
- `deskops graph missing --root .` → «No missing graph references found.», rc 0.
- `.venv/bin/deskops` no existe; usé el `deskops` del PATH (`~/.local/bin/deskops`).

## Pendiente

- El criterio `git diff --stat` solo se cumple cuando se integren o retiren los cambios ajenos en `tests/conftest.py` y
  `tests/test_mcp_extension.py`. Lo decide el coordinador.
- Decidir si se acepta la corrección del punto 6.
- Commit y closeout de IR13i: los hace el coordinador.
