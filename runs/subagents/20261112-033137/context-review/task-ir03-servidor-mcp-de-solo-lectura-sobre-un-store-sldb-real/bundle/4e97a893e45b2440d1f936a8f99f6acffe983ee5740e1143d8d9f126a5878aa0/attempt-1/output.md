## REFORMULACION

**Propósito.** Entregar el primer producto de specIR: un servidor MCP de solo lectura que permita a un agente explorar un store SLDB real sin esperar decisiones de escritura.

**Resultado.** En el paquete Python specIR, un servidor MCP por stdio construido sobre `sldb.api`, con tools para listar/describir modelos y tipos de relación, leer documento o campo, vecinos y recorrido por relación, buscar por predicados, resolver vistas (ViewDoc/SpecDoc) a JSON y comprobar integridad. Cada tool devuelve JSON con dirección estable y paginación.

**Repo.** Este repositorio; superficies `pyproject.toml`, `src/specir/` (incluido `mcp/`) y `tests/` (incluido `mcp/` y `conftest.py`).

**Límites.** Sin escrituras, tipos de dominio nuevos, extractores ni renderizado. Solo API pública de SLDB; sin pron, spec2viz ni módulos internos. Sin mocks, stubs ni datos fabricados. Pruebas contra copia aislada del store real, con deskops y spec2viz federados en lectura.

## AMBIGUEDADES

1. «dependencia en structuredLanguageDB y el SDK de MCP como extra opcional»: no fija nombre de distribución, versión ni nombre del extra; obligaría a inventar entradas de `pyproject.toml`.
2. «cada tool devuelve JSON estructurado y, por cada documento, su dirección estable»: no define esquema de dirección ni sobre JSON; obligaría a inventar el contrato de salida.
3. «búsqueda por predicados» y «resolver una vista (ViewDoc o SpecDoc) a JSON»: no fija gramática de predicados ni forma JSON de la vista; obligaría a inventar ambos.
4. «Todo conjunto llega paginado, con su total y una marca cuando quedó cortado»: no nombra la marca ni el tamaño de página; obligaría a inventar campos y valores por defecto.
5. «se vuelve a enlazar en la copia con sldb stores add apuntando a su ruta real» (deskops): a diferencia de spec2viz, no define conducta si falta; obligaría a inventar si falla o se omite.
6. «un agente conectado al servidor recorre ese store sin escribir en él»: no define qué recorrido demuestra ello; obligaría a inventar un guion o umbral.

## DRY-RUN

**Lecturas:** TaskDoc, rituales, pills, átomos, archivos nombrados, store original (`.sldb/`, `sldb/`, `desk/`), stores deskops y spec2viz.

**Cambios previstos:** crear/ajustar `server.py`, `read_tools.py`, `addresses.py`, `paging.py`, `__init__.py`, tests y `pyproject.toml`; ningún cambio en stores.

**Dependencias:** matriz de auditoría de IR01; API pública y SDK MCP disponibles; stores federados presentes.

**Validaciones futuras:** ejecutar pruebas con cliente/servidor reales por stdio; comparar documentos y árboles antes/después; verificar paginación, federación, imports y ausencia de dobles.

## FUTURO

IR01 produce la matriz que determina qué tools existen. Un humano decide los contratos ante las ambigüedades 1–6 y aprueba el cierre; luego se actualiza el board y se prepara el commit.
