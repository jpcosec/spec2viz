## REFORMULACION
Propósito: auditar, capacidad por capacidad, qué ofrece ya la API pública de SLDB frente a las 11 necesidades del cliente MCP de specIR, sin reimplementar ni depender de módulos internos. Resultado: informe `docs/auditoria/sldb-api-frente-a-mcp.md` con matriz de 11 filas, snapshot de `../sldb` y, si hay brechas, una nota única a `sldb`. Repo: `/home/jp/proyectos/SLDB_1/IR`. Límites: solo lectura de `../sldb/src/sldb/api/`, los docs SLDB listados y `../pron/source/spec/14-superficie-mcp.md` §§1,4; único archivo escrito el informe; cero código, cero cambios en otros repos, cero imports/ejecución de pron; las carencias se piden con `deskops message send --to sldb`.

## AMBIGUEDADES
1. «registrar clase Python existente» frente a «add_model(model_ref) registra clase StructuredNLDoc por referencia module:ClassName»: obliga a decidir si la fila 7 cubre cualquier clase registrable o solo `StructuredNLDoc`.
2. «El campo path del JSON devuelve el archivo creado; el ID es basename sin .md»: no dice qué hacer si el comando sale 0 pero devuelve JSON sin `path` o con `path` no interpretable; el fallback solo cubre «falla/no hay path».
3. «los tres metadatos como desconocido/no disponible»: no enumera cuáles son; hay que asumir commit, branch y status.
4. «Hashear SHA-256 solo archivos del corpus modificados/untracked» frente a, en fallback, «hashear todos los archivos del corpus»: no aclara si en fallback se hashea todo o solo lo modificado.
5. «implement only the active task» (ritual) frente a una tarea solo-docs: no aclara si «implementar» incluye el envío del mensaje.

## DRY-RUN
Lecturas: docstrings de los `.py` públicos bajo `../sldb/src/sldb/api/`; `README.md`, `addressability_model.md` y los nueve docs de `architecture/`; pron §1 y §4. Comandos: `git -C ../sldb rev-parse HEAD`, `branch --show-current`, `status --short --untracked-files=all` acotado al corpus, y hashes de modificados. Cambios previstos: crear/sobrescribir el informe; condicionalmente un `deskops message send` con cuerpo de solo filas no disponibles. Dependencias: git, deskops, `../sldb` y `../pron` presentes. Validaciones futuras: 11 filas completas, estados/acciones cerrados, fila 4 con doble evidencia y severidad máxima, snapshot con hashes, mensaje único e ID en Resumen y handoffs, fallo registrado con código/stderr/stdout, sin módulos internos.

## FUTURO
El desk SLDB decide si integra/documenta las extensiones o provee las operaciones faltantes. IR02 define la política final de escritura. Si deskops o git no operan, un humano resuelve el entorno; la tarea queda abierta.
