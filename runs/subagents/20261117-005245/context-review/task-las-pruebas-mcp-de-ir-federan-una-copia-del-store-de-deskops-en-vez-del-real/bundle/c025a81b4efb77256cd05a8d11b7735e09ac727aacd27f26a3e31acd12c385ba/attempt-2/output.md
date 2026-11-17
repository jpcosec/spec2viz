REFORMULACION
Propósito: que las pruebas MCP de IR dejen de federar el store real de deskops y usen una copia de sesión, para que la suite no falle cuando otros desks escriben. Resultado: build_deskops_copy copia el .sldb de deskops (sin caché) y sus archivos git-tracked a <tmp>/deskops, sin symlinks a repos reales (quitar enlaces con sldb stores remove o copiar sldb/pron/scion a <tmp>/<nombre>); FEDERATED y federated_digest usan la copia; mount_copy la enlaza como deskops; la prueba untouched conserva sus aserciones. Repo: /mnt/ssd/proyectos/SLDB_1/IR. Límites: solo tests/conftest.py y tests/test_mcp_extension.py; no cambiar deskops ni sldb; exige integrada la tarea de federación de spec2viz; ante bloqueo, detenerse y reportar en result-summary.md.

AMBIGUEDADES
1. «Los symlinks a los repos reales quedan prohibidos» choca con el conftest.py del input, donde build_deskops_copy hace «(base / name).symlink_to(linked, target_is_directory=True)». Obliga a inventar si ese archivo es la base a corregir o un intento.
2. «pasada la ventana de la copia, ningún proceso ... abre archivos bajo SLDB_1/deskops/» no define la ventana; obliga a inventar su inicio/fin y cómo strace separa las lecturas legítimas de git/copytree.
3. «copiar ese store enlazado...» no cubre que sldb, pron o scion no sean repos git ni que sus enlaces apunten fuera de <tmp>; obliga a inventar el fallback.

DRY-RUN
Lecturas: conftest.py, test_mcp_extension.py, tarea spec2viz y su closeout 4f1e108, git ls-files de deskops y stores enlazados, ayuda de sldb stores remove/add. Cambios: reescribir build_deskops_copy sin symlinks: copiar .sldb sin .sldb_cache y los archivos git-tracked; intentar sldb stores remove --store sobre la copia para sldb/pron/scion; si se rechaza, copiar cada store a <tmp>/<nombre> con su .sldb y git ls-files, quitando enlaces salientes; si también se rechaza, detenerse y reportar. federated devuelve la copia; federated_digest lee TRACKED; mount_copy ya la enlaza como deskops. Dependencias: spec2viz integrada, CLI sldb, git, store deskops. Validaciones futuras: los seis checks de Validation.

FUTURO
La tarea spec2viz debe estar integrada antes (closeout 4f1e108). El tester/verificador ejecuta las validaciones y decide PASS/FAIL; el closeout vincula átomos y actualiza el Board. Un humano decide ante el bloqueo reportado en result-summary.md si la copia o los enlaces no resuelven.
