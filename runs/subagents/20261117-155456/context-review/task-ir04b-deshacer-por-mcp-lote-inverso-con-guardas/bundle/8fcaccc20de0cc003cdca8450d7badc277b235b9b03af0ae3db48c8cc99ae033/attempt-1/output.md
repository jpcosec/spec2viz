## REFORMULACION

Nodo ejecutable (`task.code`), no agregado. Propósito: comprobar con un cliente MCP real que el `undo_changes` de sldb mcp deshace los últimos lotes de la sesión sobre una copia montada, incluidos los que pasan por validadores de specIR, y corregir la extensión para que el deshacer no quede en una pila propia. Resultado: `tests/test_mcp_undo.py` nuevo; `mcp_extension.py` sin `WriteTools` propio y con IR05 D2-E vía `context.add_batch_validator`; `test_mcp_extension.py` ajustado al rechazo domain; evidencia escrita. Repo: solo specIR (`src/specir/`, `tests/`). Límites: no registrar `undo_changes`, pila, inversos, entre sesiones ni nivel 3; sin mocks; solo API pública de sldb; cambios ajenos por su desk; si sldb mcp no sirve `undo_changes`, no se ejecuta.

## AMBIGUEDADES

1. «Si hace falta algo en la extensión de specIR para que el deshacer pase por sus validadores, se agrega» frente a «Se corrige en specIR: la extensión deja de crear WriteTools…»: condicional o imperativo; obligaría a inventar si el refactor se exige aunque las pruebas pasen sin él.
2. «Esperar a que cierre el espejo task-espejo-sldb-sldb-mcp-sirve-undo-changes…» frente a «los tres espejos de depends_on están cerrados»: obligaría a inventar si la espera está cumplida o debe reverificarse.
3. «como hallazgo de nivel error» no define si es severidad del validador, clase de señal o mensaje al desk; obligaría a inventar su forma.
4. «grep -nE "undo_changes|inverse" src/specir no encuentra una implementación propia» frente a «las menciones en docstrings… no cuentan»: obligaría a inventar cómo distinguir mención de implementación.

## DRY-RUN

Lecturas: TaskDoc, rituales, pills, átomos, `mcp_extension.py`, `conftest.py`, `test_mcp_extension.py` y, solo lectura, `mutability.py`/`write.py` de sldb. Cambios: `register()` deja de crear `WriteTools` y de reemplazar `propose_changes`/`apply_changes`; registra el validador IR05 D2-E con `add_batch_validator`, reconociendo `Change` y `BatchChange`; ajusta `test_mcp_extension.py`; crea `tests/test_mcp_undo.py` con `mount_copy` y `served` por nivel. Dependencias: espejos cerrados, `undo_changes` y `add_batch_validator` de sldb mcp, fixtures `mount_copy`/`served`. Validaciones futuras: pytest nuevo y existente, `tree_digest` antes/después, stale sin escribir, niveles 0/1/2, grep, `deskops graph missing --root .` rc 0. Sin ejecutar.

## FUTURO

El cierre de los espejos y los hallazgos (nivel 1 deshaciendo `RelationTypeDoc`/`RuleDoc`; validadores de dominio tras undo) se deciden y corrigen en el desk de sldb; commit y closeout los ejecuta el ritual.
