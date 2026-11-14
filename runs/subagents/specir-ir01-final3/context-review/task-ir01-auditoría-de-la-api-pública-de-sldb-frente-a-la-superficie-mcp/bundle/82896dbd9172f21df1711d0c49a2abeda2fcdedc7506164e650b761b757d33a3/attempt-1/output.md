## REFORMULACION
Propósito: auditar, capacidad por capacidad, si la API pública de SLDB cubre lo que necesita la futura superficie MCP de specIR, sin reimplementar ni tocar módulos internos. Resultado: un informe `docs/auditoria/sldb-api-frente-a-mcp.md` con exactamente once filas (capacidad, necesidad con actor/entrada/resultado, estado, evidencia, brecha, acción y handoff) y un Resumen con snapshot y nota a SLDB si hay faltantes. Repo: specIR (`/home/jp/proyectos/SLDB_1/IR`). Límites: solo lectura de `../sldb/src/sldb/api/` y docs listados; pron solo como documento; no editar otros repos, no diseñar tools, no escribir código, no decidir el contrato final de escritura.

## AMBIGUEDADES
1. “según lo que pron §4 define para kb_undo” frente a “Leer ../pron/source/spec/14-superficie-mcp.md como único documento de contrato externo”: no se afirma que §4 esté en ese archivo; obligaría a inventar su ubicación o asumir que sí.
2. “preguntar al desk SLDB” frente a “preguntar al propietario” para el caso de contrato indeterminado: son destinatarios distintos; obligaría a elegir uno sin criterio explícito.
3. “requiere-extensión-en-SLDB” y “faltante” comparten “solicitar-extensión”: no se define si una capacidad faltante se pide como extensión o solo se reporta; obligaría a inventar la acción.
4. “composición documentada” no indica qué documento la acredita; obligaría a decidir si vale una composición inferida del código público.

## DRY-RUN
Lecturas: snapshot `git -C ../sldb` (HEAD, branch, status); SHA-256 de archivos modificados/untracked; recursivamente `../sldb/src/sldb/api/*.py`; `../sldb/docs/README.md`, `addressability_model.md` y los diez documentos de `architecture/` nombrados; `../pron/source/spec/14-superficie-mcp.md` solo como documento. Cambios previstos: crear `docs/auditoria/` si falta y escribir únicamente `sldb-api-frente-a-mcp.md`. Dependencias: `deskops message send --to sldb` si hay filas no disponibles; registrar comando, resultado y fecha si falla. Validaciones futuras: once filas, estados/acciones cerrados, citas públicas existentes, snapshot, nota única con ID o declaración de no envío, lista de fuentes y ausencia de imports/ejecución de pron. Sin ejecutar nada.

## FUTURO
El desk SLDB recibe la nota y decide extensiones; el propietario aclara el contrato de undo si queda indeterminado; otro nodo o humano revisa el informe y autoriza el commit/cierre.
