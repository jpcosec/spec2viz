REFORMULACION

Encargo ejecutable `task.code` en el repo IR: modificar `tests/visual/test_notations_parity.py` para que el caso `mindmap` de `test_invalid_notations_are_rejected` espere el mensaje de sldb «diagram_type 'mindmap' is not a valid diagram type», sin xfail estricto y con docstring que cite la nota 20261116-232335. Actualizar `docs/spec2viz/matriz-de-cobertura.md` para acreditar SV-H01 si ese xfail era su único faltante, ajustando resumen, G1 y filas dependientes como SV-K21. Actualizar `docs/spec2viz/acta-de-retiro.md` con G1, «Lo que falta» y una corrida nueva de `specir retirement check` con las 5 rutas, en el formato del bloque de IR13h. Límites: solo esos tres archivos; no tocar sldb, no cambiar otras expectativas de la prueba y no declarar el retiro. No es un agregado ni un paquete no ejecutable.

AMBIGUEDADES

1. «SV-H01 queda acreditada si ese era su único faltante»: no afirma que lo sea; obligaría a inventar si SV-H01 tiene otro bloqueo, en vez de verificarlo en la matriz y la corrida.
2. «las filas que dependen de SV-H01, como SV-K21, se revisan pero siguen abiertas mientras les falte otra cosa»: no enumera las filas dependientes ni sus faltantes; obligaría a inventar el conjunto y su estado.
3. «se actualizan el resumen y G1»: no fija el texto nuevo; obligaría a inventar redacción si no se copia el estilo existente y los datos de la corrida.
4. «Las filas no acreditadas de specir retirement check coinciden con las abiertas de la matriz»: no da el número esperado; obligaría a inventarlo si no se deriva de la ejecución.

DRY-RUN

Lecturas: nota de inbox, caso y línea 230 del test, filas SV-H01/SV-K21 y «Acreditación (IR13)», acta IR13h, pills. Cambios previstos: sustituir el `pytest.param` xfail por el mensaje real de sldb y citar la nota; actualizar matriz y acta; añadir la corrida con las 5 rutas. Dependencias: mensaje real vía `load_notation`, comprobador de retiro y suites. Validaciones futuras: pytest del archivo sin xfail/xpass; comparación de filas; pytest de matriz y gate; `git diff --stat`; `deskops graph missing --root .`.

FUTURO

Un nodo ejecutor implementará y correrá las validaciones. JP decidirá archivar spec2viz y declarar el retiro; sldb mantiene su mensaje como contrato.
