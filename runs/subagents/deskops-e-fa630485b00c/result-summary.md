# IR13f — resultado del ejecutor deskops-e-fa630485b00c

Único archivo tocado: `docs/spec2viz/acta-de-retiro.md` (`diff.patch`). Los cambios ajenos en
`tests/conftest.py`, `tests/test_mcp_extension.py` y `.sldb/` no son míos y no se tocaron.

## Scope
1. **Fila de pron (Consumidores)**: «pendiente» → «resuelto», con el commit
   `4224186527a894da6a7842ffa03c313292437425`, la nota `desk/inbox/20261116-040635-…`, lo que verificó el
   tester de pron (build.py rc 0 con specir y sin filas de pron en el comprobador) y la comprobación desde IR
   (grep líneas 22–24 con specir, merge-base rc 0 con HEAD `39ea972`, corrida de IR13f sin filas de pron).
2. **Fila G5 Stores**: estado «decidido; pendiente de ejecución en IR». Decisión de JP del 2026-11-16 (opción A:
   archivar `spec2viz/.sldb` con el repo cuando el comprobador dé 0, sin reapuntar los 7 modelos), con el atom
   `atom-decisión-de-jp-2026-11-16-g5-el-store-spec2viz-sldb-se-archiva-con-el-repo` y la task.decision
   `task-decisión-de-jp-g5-del-retiro-archivar-…-reapuntar-sus-7-modelos-a` (ambos existen con esos ids en
   ../spec2viz/desk; la task.decision está en status draft allí). Pendiente en IR: (a) quitar el store del
   universo al declarar el retiro; (b) `task-las-pruebas-de-mcp-dejan-de-federar-…-g5-opción-a`, bloqueada por
   la federación transitiva vía `deskops/.sldb`, pedido a deskops en la nota 20261116-122447.
3. **«Lo que falta»**: punto 1 (G4) sin pron (anotado como resuelto con 4224186); punto 2 (G5) con la decisión
   en lugar de la alternativa, más lo pendiente en IR.
4. **Corrida nueva** del comprobador (bloque fechado agregado tras las anteriores, sin reemplazarlas).

## Comprobador (`timeout 300 .venv/bin/specir retirement check …`)
rc 1; 85 dependencias (deskops 22, sldb 1, IR 43, spec2viz/.sldb 19, graph_ui 0 solo por 52 rutas sin
commitear, pron 0); 11 filas abiertas: SV-A17, H01, H03, K09, K16, K18, K21, K22, K23, K26, K29. Igual que la
corrida de IR13e. Salida completa: `retirement-check.out`.

## Validation (todo en `validation.log`)
- git diff --stat: fuera de desk/, .sldb/ y runs/ solo cambia el acta… más `tests/conftest.py` y
  `tests/test_mcp_extension.py`, que son cambios ajenos previos de la tarea bloqueada (el brief lo advierte).
- pron merge-base rc 0; sin filas de pron en el comprobador.
- pytest matriz + gate: 11 passed, 1 xfailed (el xfail estricto del universo real), rc 0.
- grep pron / G5: muestran la fila resuelta con 4224186 y G5 decidido (opción A) con lo pendiente.
- deskops graph missing --root .: rc 0.

## Pendiente
- G5 sigue sin ejecutar en IR (puntos a y b arriba); G4 sigue abierto por graph_ui, deskops y sldb.
- No se cerró la tarea, no se commiteó y no se tocó desk/.
