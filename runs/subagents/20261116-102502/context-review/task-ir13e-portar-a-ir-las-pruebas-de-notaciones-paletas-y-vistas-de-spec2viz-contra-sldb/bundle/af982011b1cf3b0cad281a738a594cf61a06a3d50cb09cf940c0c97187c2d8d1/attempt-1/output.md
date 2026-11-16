REFORMULACION
El nodo debe portar a IR, contra sldb, las pruebas de notaciones, paletas y vistas de spec2viz: crear `tests/visual/test_notations_parity.py` con 42 pruebas portadas y 9 comparaciones «valida igual», copiar los fixtures de notaciones/paleta de spec2viz, completar reexportaciones en `src/specir/visual/notation_style.py` y actualizar `docs/spec2viz/matriz-de-cobertura.md` y `docs/spec2viz/acta-de-retiro.md`. Repo: specIR/IR. Límites: no tocar sldb ni spec2viz, no implementar capacidades visuales, no declarar el retiro, no ajustar expectativas para forzar verdes; las carencias se piden al desk de sldb.

AMBIGUEDADES
1. «ViewDoc se toma de sldb.api si sldb lo exporta; si no, la fila SV-A17 queda abierta» frente a `from sldb.api import ViewDoc` y «solo esa fila queda abierta». Un fallo de importación a nivel de módulo afectaría todo el archivo; obligaría a inventar importación condicional o aislamiento por fila.
2. Se autoriza «copiar… las 8 notaciones… y la paleta… a tests/visual/fixtures/spec2viz-notations/», pero el archivo previsto usa `FIXTURES = SPEC2VIZ / "tests" / "fixtures"` y `CATALOG = HERE / "fixtures" / "catalog"`. No se dice si esos árboles ya existen o si pueden copiarse; obligaría a inventar su procedencia.
3. «SV-G08 queda cumplida citando tests/visual/test_catalog.py… sin xfail» choca con el acta: «xfail estricto: `label_key` frente a `normKey` (`test_atoms_matching.py`)». Obligaría a decidir qué prueba es la evidencia y si el xfail desapareció.

DRY-RUN
No es un agregado ni un paquete no ejecutable: es una tarea de código/documentación. Un ejecutor leería el TaskDoc, el test existente, `notation_style.py`, la matriz, el acta y las pruebas/fixtures de spec2viz; comprobaría qué exporta `sldb.api`. Añadiría las dos pruebas de validación tipada, ajustaría docstrings, reexportaría lo que falte y copiaría o verificaría fixtures. Actualizaría filas, resumen y acta; si algo falla, aplicaría `xfail(strict=True)` y nota a sldb. Dependencias: sldb, fixtures de spec2viz, `pytest`, `specir`, `deskops`. Validaciones futuras: pytest del archivo nuevo, tests de imports/matriz/gate, `test_catalog.py` con `-rxX`, greps, `specir retirement check`, suite completa bajo `flock` y `deskops graph missing`.

FUTURO
El desk de sldb decide y corrige exportaciones, mensajes tipados y `label_key`; los consumidores resuelven G4; JP decide el archivo de spec2viz cuando el gate llegue a 0. Otro nodo ejecutor implementa, corre validaciones y deja evidencia; un humano revisa la matriz y el acta.
