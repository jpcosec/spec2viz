## REFORMULACION
Propósito: cerrar el caso de `diagram_type` desconocido en la prueba portada de notaciones, alineándolo con el mensaje que sldb conserva como contrato. Resultado: el caso de mindmap de `test_invalid_notations_are_rejected` deja de ser xfail, espera el mensaje de sldb y SV-H01 queda acreditada; se actualizan matriz y acta. Repo: `/mnt/ssd/proyectos/SLDB_1/IR`. Límites: solo `tests/visual/test_notations_parity.py`, `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md`; no tocar sldb, no cambiar otras expectativas, no declarar el retiro.

## AMBIGUEDADES
1. «SV-H01 queda acreditada si ese era su único faltante»: obligaría a inventar si el xfail era el único faltante o si existen otros, pues el input no lo afirma.
2. «se revisan pero siguen abiertas mientras les falte otra cosa»: obligaría a inventar qué cuenta como «otra cosa» para SV-K21 y filas dependientes.
3. «en el formato del bloque de IR13h»: obligaría a inventar la estructura exacta del bloque del acta, no incluida en el input.
4. «la notación del caso con diagram_type mindmap»: obligaría a inventar el fixture, parámetro `changes1` y ruta exacta usados por la prueba.
5. «esperando el mensaje de sldb»: obligaría a elegir entre igualdad exacta y coincidencia parcial; el rationale cita el texto, pero no fija el comparador.

## DRY-RUN
Lecturas: nota de inbox, `test_notations_parity.py` (caso y línea 230), filas SV-H01/SV-K21 y sección Acreditación de la matriz, bloque de IR13h del acta, módulo `specir.visual.notation_style`. Cambios previstos: quitar xfail y ajustar docstring/aserción del caso; actualizar SV-H01, resumen, G1 y filas dependientes; añadir corrida nueva con las 5 rutas al acta. Dependencias: mensaje real de `load_notation` vía API pública de sldb, helpers existentes de prueba y `specir retirement check`. Validaciones futuras: pytest del archivo sin xfail/xpass, coincidencia entre filas no acreditadas y matriz abierta, pytest de matriz/retirement gate, `git diff --stat` limitado a tres archivos y `deskops graph missing --root .`. Sin ejecutar nada.

## FUTURO
sldb mantiene el mensaje contractual; el resultado de `specir retirement check` y la matriz determinan si SV-H01 y dependientes quedan acreditadas; un humano confirma el cierre y la decisión sobre el retiro; IR13h aporta el formato del bloque del acta.
