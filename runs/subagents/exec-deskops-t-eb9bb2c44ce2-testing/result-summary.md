PASA

# Resultado del tester — extractor de librerías Python con CLI

- Tarea: `task-specir-extract-describe-una-libreria-de-python-con-cli-con-los-tipos-que-ya-tiene-y-sobre-el-repo-de`
- Rol: tester · Run: `run-deskops-t-eb9bb2c44ce2` · `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-eb9bb2c44ce2-*`
- Commit del ejecutor: `4df694b5ceeb56fcab39658d32ef47faae48346e` — *feat: extractor de librerías Python con CLI (argparse, click) sobre los tipos existentes*. `git log --grep "Task-Id: ..."` no lo encuentra porque la tarea pidió no poner Task-Id en el commit de código; el commit se localizó por el log.
- `src/` y `tests/` son idénticos entre `4df694b` y `HEAD` (`git diff --stat 4df694b HEAD -- src tests` vacío; `git merge-base --is-ancestor` rc 0).
- Evidencia: `validation.log` (comandos, salidas y rc).

## Pruebas ejecutadas (de a una)

| Archivo | Módulo tocado | Resultado |
|---|---|---|
| `tests/test_extract_python_cli.py` | `extract/python_cli.py` | **9 passed**, rc 0 (30,59 s) |
| `tests/test_cli_mcp.py` | `specir/cli.py` | **3 passed**, rc 0 (2,56 s) |
| `tests/test_imports.py` | `extract/__init__.py` (API pública de sldb) | **9 passed**, rc 0 (1,81 s) |
| `tests/extract/test_ux_extract_cli.py` | `specir/cli.py` (`ux extract` convive con `extract`) | **2 passed**, rc 0 (43,02 s) |
| `tests/visual/test_cli.py` | `specir/cli.py` (superficie de comandos) | **40 passed**, rc 0 (94,92 s) |

No se corrió la suite completa: la integra el host, como indica el encargo del tester.

## Done When sobre una copia de deskops

Worktree `git worktree add --detach /tmp/deskops-accept origin/main` (`3abef17fd`), store nuevo con `specir.install`, y:

```
specir extract python-cli /tmp/deskops-accept --store /tmp/deskops-store/.sldb
created: 102, updated: 0, unchanged: 0, desconocidos: 1
```

- **102 `DomainEntityDoc`** (clases Pydantic/dataclass de deskops). Comprobados los 102: `origen=observado`, capa `layer.domain` (la de `__semantics__`, sin tipos nuevos) y descripción con `archivo.py:línea` y ancla `[anchor-...]`. Ninguno falla.
- **0 comandos, 0 handlers, 0 operaciones de API y 0 operaciones de dominio.** El parser de deskops (`cli/parser.py`) y su registro `Command(...)` (`cli/registry.py`) se arman dentro de cuerpos de función; `attrs.calls` de una función trae solo `{name, line}`, sin args/kwargs, así que sldb no entrega el nombre del subcomando ni su handler. El extractor lo reporta como **1 desconocido contado** con ese motivo, tal como anticipa el Implementation Path.
- **Reglas sembradas:** `sldb rules check` rc **0**. 102 hallazgos, todos `level=alert` (`rule-specir-entity-is-persisted`: entidad del árbol sin `TableDoc`), **ningún error**. (El rc 120 visto una vez fue por cerrar stdout con `| head`; el comando completo da rc 0.)
- **Notas de desconocido:** existen y están abiertas la de IR (`desk/inbox/20261125-194830-unclear-python-cli-...`) y la de sldb (`desk/inbox/20261125-194644-unclear-code-facts-argumentos-de-las-llamadas-dentro-del-cuerpo-de-una-funci-n.md`). Quedan sin seguimiento en sus repos.

## Veredicto y límite

**PASA** para el extractor y para la validación exigida: los tipos existentes se usan sin crear ninguno, las capas/procedencia/anclas son correctas y las reglas corren sin error. El test del commit cubre argparse (comando, handler, operación de dominio, API pública y modelo), click, idempotencia, desconocidos y capas.

El Done When literal («deja en el store los comandos de su CLI») **no se cumple sobre deskops**: 0 comandos. Lo acepto como cierre parcial permitido por la aclaración explícita del Implementation Path («a sldb solo si falta un hecho de código, sin bloquear la tarea»): el hecho que falta está pedido en el inbox de sldb y el ejecutor lo dejó dicho en su `result-summary.md`. Si el coordinador exige el Done When literal, el cierre debe esperar a que sldb entregue args/kwargs de las llamadas de cuerpo y se re-extraiga deskops; no es un defecto del extractor.

## Discrepancias con el ejecutor

Ninguna en el fondo: coinciden 102 entidades, 0 comandos, 1 desconocido, las dos notas y el rc 0 de las reglas. La única salvedad es que las dos notas están sin commitear en IR y sldb.
