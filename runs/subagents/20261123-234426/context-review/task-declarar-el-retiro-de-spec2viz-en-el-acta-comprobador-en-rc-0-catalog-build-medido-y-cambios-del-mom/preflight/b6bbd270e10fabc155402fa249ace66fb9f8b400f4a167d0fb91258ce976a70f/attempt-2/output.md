## REFORMULACION

**Propósito:** declarar formalmente el retiro de spec2viz en el acta, a partir de la decisión de JP del 2026-11-23 y de las condiciones ya cumplidas (cierre de `attach_atom_edges`, `specir catalog build` en 55,8 s con rc 0, comprobador rc 0 y cambios del momento del retiro hechos).

**Resultado:** `docs/spec2viz/acta-de-retiro.md` con estado de cabecera «declarado», medición nueva de catalog build, salida rc 0 del comprobador, pendientes marcados como hechos con su commit, punto 9 como último paso y constancia sobre los oráculos de paridad (punto 6).

**Repo:** el workspace actual (`SLDB_1/IR`), según las rutas del input.

**Límites:** solo el acta y, si hace falta, `matriz-de-cobertura.md`. Fuera: código y el archivado del repo en GitHub. No es un nodo agregado: es una tarea documental ejecutable.

## AMBIGUEDADES

1. «Correr specir retirement check con el universo declarado»: no se da comando exacto ni configuración; obligaría a inventar la invocación.
2. «los oraculos de paridad (punto 6) se retiran al declarar, o el motivo si no»: no hay criterio para decidir; obligaría a inventar la decisión o el motivo.
3. «y, si hace falta, matriz-de-cobertura.md»: no se define cuándo hace falta; obligaría a inventar la condición.
4. «los items de 'Lo que falta para declarar el retiro' quedan marcados hechos con su commit»: los commits aparecen en el rationale, pero no el mapeo ítem→commit; obligaría a inventarlo.
5. «la seccion de medicion de catalog build trae la medicion nueva»: no se fija formato ni ubicación exacta; obligaría a inventar la presentación.

## DRY-RUN

**Lecturas previstas:** `docs/spec2viz/acta-de-retiro.md`, `matriz-de-cobertura.md` si existe, y salida de `specir retirement check`.

**Cambios previstos:** cabecera a «declarado» con fecha 2026-11-23; sección de medición con 55,8 s, rc 0 y 1,7 GB RSS; salida del comprobador con rc 0; pendientes marcados con commits; punto 6; punto 9 como último paso.

**Dependencias:** ejecutable `specir`, acta existente, commits `c377aff6`, `e6e369d`, `109684f`.

**Validaciones futuras:** rc 0 del comprobador; `grep -n 'no declarado'` solo en historia fechada.

## FUTURO

El coordinador archiva el repo spec2viz en GitHub (punto 9). La aceptación final corresponde a quien revise el acta.
