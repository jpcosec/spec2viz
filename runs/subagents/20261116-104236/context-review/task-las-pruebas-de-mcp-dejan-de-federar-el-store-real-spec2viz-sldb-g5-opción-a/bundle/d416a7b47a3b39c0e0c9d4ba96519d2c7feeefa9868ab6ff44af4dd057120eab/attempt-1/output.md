## REFORMULACION
Encargo ejecutable (`task.code`, no agregado): en el repo IR, modificar solo `tests/conftest.py` y `tests/test_mcp_extension.py` para que las pruebas MCP dejen de leer/enlazar `../spec2viz/.sldb`. Resultado: un store de specs temporal, construido desde la fixture `tests/visual/fixtures/spec2viz/docs/architecture/spec2viz/class-sldb-models.yml` con `sldb.api`, enlazado con alias `spec2viz`; `FEDERATED` solo conserva deskops; la lectura MCP y el chequeo de “untouched” siguen cubiertos. Límites: no tocar spec2viz, sldb, acta/matriz, retiro IR13 ni `tests/visual/test_api.py`.

## AMBIGUEDADES
1. «agregar un fixture de sesión que construya el store de specs» y «en mount_copy, enlazar ese store en vez del real»: `mount_copy` es una función normal, no un fixture; no se dice cómo recibe el store temporal. Obliga a inventar el mecanismo de paso (parámetro, fixture auxiliar o refactor).
2. «de modo que SPEC_STORE y los nombres de las pruebas no cambian» junto con «se ajusta la prueba para leer los datos del store temporal»: al quitar spec2viz de `FEDERATED`, la prueba ya no puede hacer `FEDERATED[SPEC_STORE]`; no se indica cómo obtiene la ruta temporal. Obliga a inventar la exposición del fixture a la prueba.
3. «que las pruebas de «untouched» (federated_digest y las que comparan digests antes y después) cubran también el store de specs temporal»: `federated_digest()` usa `FEDERATED` y `git ls-files`; el directorio temporal no es repo git ni está en `FEDERATED`. Obliga a inventar qué archivos temporales se digieren y con qué mecanismo.
4. «En un directorio de tmp_path_factory» y «sldb stores add <dir>/.sldb --name spec2viz --store .sldb, cwd=root»: no se precisa si `<dir>` queda dentro de `root` o fuera. Obliga a decidir ubicación y su efecto en digests/limpieza.

## DRY-RUN
Lecturas: `tests/conftest.py`, `tests/test_mcp_extension.py`, `tests/visual/test_notations_parity.py`, el YAML fixture y la API `sldb.api`. Cambios previstos: reducir `FEDERATED` a deskops; crear fixture de sesión que copie el YAML, ejecute `init_store` y `SpecSync`; enlazar `<dir>/.sldb` como `spec2viz`; adaptar la prueba para leer del store temporal sin relajar aserciones; extender el digest de “untouched”; actualizar docstrings. Dependencias: API pública de sldb, existencia del YAML, `git ls-files` para deskops. Validaciones futuras: grep, pytest focalizado, `git diff --stat`, suite completa bajo `flock` y `deskops graph missing`; ninguna se ejecuta aquí.

## FUTURO
Un humano/JP decide el retiro IR13 y la actualización del universo de `specir retirement check`; otro nodo ejecuta implementación, commit y cierre de fase. Si falta `sldb.api` o `SpecSync` no construye el store fuera de git, el ejecutor debe detenerse y reportar el bloqueo.
