## REFORMULACION

Propósito: corregir `docs/spec2viz/acta-de-retiro.md` para que no afirme estados ya falsos sobre G5 y las pruebas de IR tras cerrarse la federación del store `spec2viz/.sldb` en las pruebas MCP. Resultado: la fila G5 del gate y el punto 2 de «Lo que falta» presentan la federación como resuelta (código `b16aab7`, closeout `4f1e108`) y dejan pendiente solo retirar `spec2viz/.sldb` del universo del comprobador al declarar el retiro y archivar el store; la fila de IR en Consumidores deja de citar la federación en `tests/conftest.py`. Repo: IR (`/mnt/ssd/proyectos/SLDB_1/IR`). Límites: solo ese archivo; fuera la matriz, código, pruebas, declarar el retiro y una corrida nueva del comprobador. Es una tarea ejecutable de edición documental, no un agregado.

## AMBIGUEDADES

1. «la fila de IR en Consumidores deja de mencionar la federación de spec2viz/.sldb en tests/conftest.py y conserva el resto (los oráculos de paridad en pruebas)» frente a la fila actual, que también dice «tests/test_mcp_extension.py:24 federan el store». Obliga a inventar si esa mención se conserva o se elimina, y si la federación está cerrada del todo o solo en `conftest.py`.

2. «pasa a resuelta citando b16aab7 y 4f1e108» no fija el texto exacto. Obliga a inventar la etiqueta («resuelta», «cumplida»), si se conserva el id de la tarea y qué hacer con «pedido a deskops en la nota 20261116-122447».

3. «Fuera: … una corrida nueva del comprobador, porque el recuento no cambia» frente a la validación con `pytest tests/visual/test_retirement_gate.py`. Obliga a inventar si esa prueba, que ejerce el comprobador, cuenta como corrida prohibida.

4. «grep -n 'bloqueada' … no muestra la tarea de federación como bloqueada» es un criterio vago. Obliga a inventar el texto exacto que debe desaparecer y si basta con que `bloqueada` no aparezca asociada a esa tarea.

## DRY-RUN

Lecturas: acta completa; informes de IR13h `runs/subagents/deskops-e-5d20e77cfc47` y `deskops-t-fb41c88d0a4a/result-summary.md`; `git merge-base --is-ancestor 4f1e108 HEAD`; `grep -nE 'spec2viz' tests/conftest.py`. Cambios previstos: en la fila G5, sustituir el pendiente de federación por resuelta con `b16aab7`/`4f1e108` y mantener pendiente el retiro del store; igual en el punto 2; en la fila IR de Consumidores, quitar la mención a `tests/conftest.py` y conservar los oráculos de paridad. Dependencias: `task-ir13h` y que los commits citados sean ancestros. Validaciones futuras: `git diff --stat`, `grep 'bloqueada'`, pytest de matriz y retirement gate, y `deskops graph missing --root .`.

## FUTURO

Un nodo posterior de IR declarará el retiro y quitará `spec2viz/.sldb` del universo; JP decidirá y ejecutará el archivo de spec2viz; sldb resolverá su dependencia en `gen_golden.py`; deskops responderá la nota 20261116-122447. Nada de esto se decide aquí.
