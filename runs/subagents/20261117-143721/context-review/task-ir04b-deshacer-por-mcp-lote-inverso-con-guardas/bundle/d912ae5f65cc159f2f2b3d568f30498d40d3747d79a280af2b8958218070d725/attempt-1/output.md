## REFORMULACION

Propósito: verificar desde specIR que el `undo_changes` de sldb mcp deshace los últimos lotes de la sesión con guardas, con la extensión de specIR montada, sin que specIR implemente el deshacer. Resultado: un módulo nuevo `tests/test_mcp_undo.py` con pruebas contra un cliente MCP real sobre copia montada; ajuste mínimo, solo si hace falta, en `src/specir/mcp_extension.py`; hallazgos escritos en `result-summary.md`. Repo: specIR (IR). Límites: fuera registrar `undo_changes`, guardar la pila, construir inversos, deshacer entre sesiones y nivel 3; lo que deba cambiar en sldb se pide por su desk.

## AMBIGUEDADES

1. "Si hace falta algo en la extensión de specIR para que el deshacer pase por sus validadores, se agrega en src/specir/mcp_extension.py" frente a "(e) Hoy src/specir/mcp_extension.py no registra validadores de lote (add_batch_validator)". No hay validador que el deshacer pueda atravesar y "si hace falta" no fija condición; obligaría a inventar un validador o a decidir que nunca procede.
2. "un undo_changes posterior, una vez revertido el cambio ajeno, lo deshace": no dice cómo se revierte ese cambio ajeno ni con qué tool o lote; obligaría a inventar el procedimiento.
3. "aplicar un lote de creación, edición y arista": no fija tipos ni documentos; en nivel 2 se exige tocar `RelationTypeDoc` o `RuleDoc`. Obligaría a inventar el contenido del lote.
4. Scope dice "que los niveles 0 y 1 se respetan" y (b) dice "Se prueban 0, 1 y 2". Contradicción que obliga a elegir; la precisión posterior parece resolverla.
5. "grep -nE \"undo_changes|inverse\" ... no encuentra una implementación propia" frente a (f), donde docstrings y llamadas no cuentan: el grep puede hallar menciones que (f) excluye; obligaría a inventar el filtro.

## DRY-RUN

Lecturas: TaskDoc, pills, átomos, `tests/conftest.py` (`mount_copy`, `served`, `tree_digest`), `src/specir/mcp_extension.py` y la fuente de sldb mcp (`undo_changes`, `mutability`). Cambios previstos: nuevo `tests/test_mcp_undo.py`; `mcp_extension.py` solo si un validador de lote resultara necesario; `result-summary.md`. Dependencias: sldb mcp con `undo_changes` y niveles; `mount_copy` escribible con `--level` por caso; cliente MCP real. Validaciones futuras: pytest del módulo; digest antes/después; caso stale (`applied: false`, `rejected: stale`, `written: false`, lote persistente); niveles 0/1/2; grep; `deskops graph missing` desde la raíz de IR. Sin ejecutar nada.

## FUTURO

sldb mcp ya sirve `undo_changes` y su pila; un humano decide los hallazgos si niveles o validadores fallan y autoriza el cierre y el commit; una carencia de sldb se traslada por mensaje a su desk.
