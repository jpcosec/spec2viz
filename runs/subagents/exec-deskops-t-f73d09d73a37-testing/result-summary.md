PASA

# Resultado del tester — skill `use-specir` declara y extrae

- Tarea: `task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a`
- Rol: tester · Run: `run-deskops-t-f73d09d73a37` · `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-f73d09d73a37`
- Commit del ejecutor: `e0ae0115910bf7eb13f2cd9a30bd019cfbbb2deb` — *docs: use-specir skill describes specIR as declaring and extracting*. Es el único commit con ese `Task-Id`, y `git diff --stat e0ae011 HEAD -- skills/use-specir/SKILL.md` sale vacío.
- Evidencia completa: `validation.log`.

## Validación exigida

```
! grep -nE 'the visual layer|same catalog page' skills/use-specir/SKILL.md
```

`grep` rc **1**, sin coincidencias. Pasa.

## Comandos que la skill nombra

Comprobados con `--help` (rc 0 en todos; ver `validation.log`):

- specIR: `specir about`, `specir diagram render|lint|schema`, `specir catalog build|schema`, el alias `specir build`, `specir mcp`, `python -m specir.cli`.
- sldb: `sldb notations validate|sync|from-graph|list|view`, `sldb serve`, `sldb mcp`.
- deskops: `deskops message send`.

Además, los tests de la skill en `tests/visual/test_cli.py` (que invocan cada comando) pasan:
`2 passed, 38 deselected`. El archivo completo: **40 passed**, rc 0 (126,92 s).

## Done When

- **No afirma que specIR dibuja ni que tiene interfaz.** Abre con «specIR declares and extracts… It does not draw and it has no interface of its own», y tiene una sección «Where a diagram is seen or edited» que manda a la vista de notación de graph_ui (`UIs/graph_ui`, `specs/notation`; el directorio existe).
- **Cada comando nombrado existe** (`--help` rc 0 y test de anti-drift verde).
- **Lo decidido y sin ejecutar está marcado con la fecha.** Las capacidades 3–5 faltantes, el retiro de `CatalogAnnotationsDoc`/página del catálogo, `sldb serve` sobre fastmcp y el montaje de `mcp_extension` en el servidor de sldb llevan `(decided 2026-11-25, not executed)`. Coincide con `docs/decisiones/paridad-por-capacidades.md`, que se leyó.
- Las referencias internas del «Mandatory read route» existen todas.

## Salvedad (no bloqueante)

La aclaración pedía el literal `(decidido 2026-11-25, sin ejecutar)` en la línea. El ejecutor usó su traducción inglesa `(decided 2026-11-25, not executed)`, coherente con que la skill está escrita en inglés. El Done When pide «marcado como tal con la fecha», y eso se cumple en las seis líneas afectadas; no hay ninguna afirmación de trabajo hecho donde solo hay decisión. Si el coordinador exige el literal en español, es un cambio de una palabra por línea, sin efecto sobre lo validado.
