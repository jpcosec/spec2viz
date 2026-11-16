REFORMULACION  
Nodo ejecutable `task.code` en el repo IR (`/mnt/ssd/proyectos/SLDB_1/IR`), no agregado. Propósito: dejar de federar el store real `../spec2viz/.sldb` en las pruebas MCP de IR sin perder la cobertura de lectura de una spec de un store enlazado vía servidor MCP. Resultado: `tests/conftest.py` y `tests/test_mcp_extension.py` usan un store temporal construido desde una fixture de IR; `FEDERATED` solo enlaza deskops; se conserva el alias `spec2viz`; los chequeos “untouched” cubren el store temporal; docstrings actualizados; validaciones en verde. Límites: no tocar acta/matriz, retiro IR13, `tests/visual/test_api.py:45`, spec2viz ni sldb; sin mocks ni documentos fabricados; detenerse ante bloqueo de API/SpecSync.

AMBIGUEDADES  
1. “Devuelve la ruta de su .sldb” frente a “sldb stores add <ruta>/.sldb”: ¿`spec_store` es el directorio `.sldb` o su padre? Obliga a inventar si el comando usa `spec_store` o `spec_store.parent`; de lo contrario duplica `.sldb`.  
2. “crear el store con sldb.api.init_store(<dir>) y sincronizar … SpecSync(<dir>/.sldb)” frente a “Devuelve la ruta de su .sldb”: ¿`<dir>` es la raíz temporal o el store? Obliga a decidir el argumento de `init_store` y la ruta de `SpecSync`.  
3. “tree_digest(spec_store) más el sha256 de cada archivo .md bajo su proyecto (spec_store.parent, recorrido con rglob)”: no dice qué `.md` existen ni si el YAML entra en el digest; obliga a inventar la lista o asumir que puede quedar vacía.  
4. “las mismas pruebas que hoy comparan federated_digest u original_digest”: no las nombra; obliga a inferir cuáles deben ampliarse.

DRY-RUN  
Lecturas: `tests/conftest.py` completo, `tests/test_mcp_extension.py`, fixture de paridad y API pública de sldb. Cambios previstos: quitar spec2viz de `FEDERATED`; `build_spec_store(tmp_path_factory)->Path` con `mktemp`, copia del YAML, `init_store`, `SpecSync`; fixture `spec_store`; `mount_copy(spec_store)` y llamadores; test lee del store temporal; digest temporal antes/después; docstrings. Dependencias: API pública sldb, SpecSync fuera de git, `tmp_path_factory`, deskops CLI y `flock`. Validaciones futuras: grep, pytest MCP, `git diff --stat`, suite completa y `deskops graph missing`. Sin ejecutar nada.

FUTURO  
Otro nodo ejecutor aplicará los cambios y correrá las validaciones; un humano/JP decide si el bloqueo de API o rutas exige detenerse. IR13, acta y matriz quedan fuera.
