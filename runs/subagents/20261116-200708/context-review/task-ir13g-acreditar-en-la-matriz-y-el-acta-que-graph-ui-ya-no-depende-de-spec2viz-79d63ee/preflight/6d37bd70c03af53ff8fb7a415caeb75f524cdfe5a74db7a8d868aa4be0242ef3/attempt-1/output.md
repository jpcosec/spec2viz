## REFORMULACION
Tarea concreta, no agregado ni paquete no ejecutable. Propósito: acreditar en la documentación que `graph_ui` ya no depende de `spec2viz` en `79d63ee` (`c9b09f7`). Resultado: matriz y acta actualizadas, con una corrida nueva de `specir retirement check`. Repo/ámbito: workspace IR; solo `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md`. Límites: no tocar código/pruebas, no cambiar `graph_ui`, no declarar el retiro ni quitar `spec2viz/.sldb`; otros repos solo se leen o se piden por su desk.

## AMBIGUEDADES
1. “Las filas del inventario de consumidores de graph_ui se marcan resueltas citando 79d63ee”: no enumera filas ni campos exactos; obligaría a inventar cuáles son y qué texto poner.
2. “también se anota el pendiente sin efecto en specir que menciona la nota, el ci.yml de graph_ui”: no define redacción, ubicación ni criterio de “sin efecto”; obligaría a inventar la anotación.
3. “igual que las corridas anteriores”: no incluye el formato previo; obligaría a inventar estructura y nivel de detalle.
4. “si su único faltante era G4 de graph_ui y sus pruebas en tests/visual/test_notations_parity.py pasan”: no indica comando ni resultado; obligaría a inventar la verificación si no se inspecciona la matriz/pruebas.

## DRY-RUN
Lecturas: nota de inbox; matriz (SV-H03, SV-K18, SV-K22, Acreditación IR13); acta completa; pills citadas. Comprobaciones previstas, sin ejecutar: `git -C ../UIs/graph_ui merge-base --is-ancestor 79d63ee HEAD`; `git grep` de imports/dependencias; `specir retirement check` con los cinco `--path`. Cambios previstos: estados y resumen de matriz; consumidores, G4, “Lo que falta” y corrida nueva del acta. Dependencias: disponibilidad de repos y `79d63ee`; resultado de `task-ir13f`. Validaciones futuras: `git diff --stat`, rc de las comprobaciones, coincidencia de filas abiertas, pytest indicado y `deskops graph missing`.

## FUTURO
El nodo ejecutor aplicará ediciones y corridas. Un humano decide si una verificación falla, si hay inconsistencia matriz/comprobador o si procede cerrar. `task-ir13f` aporta la resolución previa del acta.
