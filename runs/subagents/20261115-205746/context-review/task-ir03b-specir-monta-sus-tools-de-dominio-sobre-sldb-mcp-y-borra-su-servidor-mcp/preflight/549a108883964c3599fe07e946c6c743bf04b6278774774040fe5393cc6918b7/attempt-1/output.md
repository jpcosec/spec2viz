REFORMULACION
Propósito: retirar de specIR su servidor MCP propio y montar solo sus tools de dominio como extensión de sldb mcp, tras cerrar la tarea espejo A. Resultado: una función `fn(server, ctx)` en specIR que registra tools de dominio; pruebas de specIR que arrancan sldb mcp con `--extension` y usan cliente MCP real por stdio sobre copia aislada; código genérico migrado borrado de `src/specir/mcp`. Repos: specIR principal; sldb como dependencia espejo. Límites: no reescribir servidor/log de sldb; fuera undo (IR04b), impacto (IR10), copiar servidor/log, mocks o datos fabricados. Es `task.code` ejecutable, no agregado.

AMBIGUEDADES
1. “el nombre del módulo lo fija la tarea al implementarla”: no se da módulo ni función; obliga a inventar identificador público y ruta.
2. “todo lo que hay bajo src/specir/mcp salvo lo de dominio”: no enumera qué es dominio; obliga a inventar la frontera de borrado/conservación.
3. “los tests que se portaron a sldb”: no lista tests; obliga a inventar inventario y equivalencias.
4. “con el mismo contexto y los mismos niveles”: no define contexto ni niveles; obliga a inferirlos de una API no incluida.

DRY-RUN
Lecturas: TaskDoc, pills, cierre/API de tarea espejo A, árbol `src/specir/mcp` y tests, docs de `build_server`/`--extension` de sldb. Cambios previstos: añadir `register(server, ctx)`; adaptar tests para lanzar sldb mcp `--extension ... --store` con copia aislada y cliente stdio; `git rm` de módulos genéricos y tests migrados tras comprobar equivalente. Dependencias: tarea espejo A cerrada, punto de extensión disponible, copia aislada. Validaciones futuras: test de imports; listado real de tools; nivel 0 sin escrituras y store sin cambios antes/después; suite portada/borrada pasa. Sin ejecutar.

FUTURO
La tarea espejo A produce el punto de extensión y el código migrado; el implementador fija nombre y frontera si el humano no los precisa; revisión/CI valida el cierre.
