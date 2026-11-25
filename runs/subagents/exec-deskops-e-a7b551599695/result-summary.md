# result-summary: task-specir-extract-describe-una-libreria-de-python-con-cli-con-los-tipos-que-ya-tiene-y-sobre-el-repo-de
run_id: exec-deskops-e-a7b551599695
session: n/a (executor Claude en Scion; sin sesión de subagente pi)
session_sha256: n/a

## Qué hice
Extractor nuevo `src/specir/extract/python_cli.py` (lee hechos de sldb, no código), exportado como
`specir.extract.extract_python_cli` y expuesto como `specir extract python-cli ROOT`.
- Comando argparse (parser, add_subparsers, add_parser, set_defaults(func=) a nivel de módulo) o click (@x.command) -> InterfaceControlDoc + InterfaceActionDoc (triggers).
- Handler = la función de set_defaults / la decorada -> HandlerDoc. Lo que llama dentro del paquete -> DomainOperationDoc (executes).
- Función exportada por `__all__` (o sin guion bajo en `__init__`) que el handler llama -> ApiOperationDoc (method y route nulos, nombrados en `desconocidos`; invokes, y handled_by si la llama un solo handler, si no, desconocido).
- Clase Pydantic (BaseModel/StructuredNLDoc, o heredera en el paquete) o dataclass -> DomainEntityDoc.
- La capa es la de cada modelo (__semantics__), no se creó ningún tipo. Origen observado/derivado, anclas en cada hecho (archivo:línea en la descripción).
- No hizo falta tocar plan.py: sus PREFIXES ya cubren todos los tipos usados.
- Fixture tests/fixtures/cli_lib y test tests/test_extract_python_cli.py (9 tests).

## Resultado sobre deskops (copia origin/main, quitada)
102 modelos como DomainEntityDoc; 0 comandos; 1 desconocido contado. Razón: el parser de deskops (cli/parser.py) y su registro (cli/registry.py, Command(...)) viven en cuerpos de función, y `attrs.calls` de una función trae solo {name, line}, sin argumentos. Por eso la meta "comandos de deskops en el store" NO se cumple todavía; falta un hecho de sldb. Pedido enviado: sldb inbox 20261125-194644-unclear-code-facts-... ; nota en el inbox de IR 20261125-194830-unclear-python-cli-... (IR no está en el registro de repos, así que --to IR falló y se envió sin --to).
Las reglas sembradas corren rc 0 (alertas de entidad sin tabla, no errores).

## Revisar
- Si se acepta que el cierre quede parcial hasta que sldb entregue args de llamadas de cuerpo.
- write_plan tarda ~18 s por anclaje en deskops (30 min); no se tocó.
- Sin Task-Id en el commit de código (según aclaración).

## Archivos
src/specir/extract/python_cli.py, src/specir/extract/__init__.py, src/specir/cli.py, tests/test_extract_python_cli.py, tests/fixtures/cli_lib/mylib/{__init__,core,models,cli,dynamic,clicmd}.py

## Commit y advance
Commit de código en la rama deskops/deskops-e-a7b551599695 (sin Task-Id).
`deskops advance task` BLOQUEADO (no por el código): rules/rule-activation-task-code exige recibos preflight y bundle aceptados e intactos; el ReviewDoc ...-bundle-1 está en anchor_state "changed". Hace falta que el supervisor renueve el recibo.
