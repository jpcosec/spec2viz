# Resultado
Rama deskops/deskops-e-c2af90ecb869 (un commit, Task-Id). Archivos:
- src/specir/visual/renderers/bpmn.py: exporter="specir", targetNamespace="http://specir/bpmn".
- src/specir/visual/templates/default.html: clave specir.catalog.annotations.v1; annoMigrateLegacy (una vez: sin clave nueva y vieja JSON valido -> copia y borra la vieja; ambas -> gana la nueva y se borra la vieja; vieja invalida -> intacta con console.warn). La clave vieja solo queda en la migracion.
- tests/visual/test_catalog_annotations.py: harness con la clave nueva + 3 tests de migracion.
- goldens spec2viz-2de1056-renders.json y -oracle.json: no se pueden regrabar con spec2viz (retirado); se parchearon: cadenas exporter/targetNamespace, digests de pagina del catalogo (8, verificado que revertir la plantilla da el digest viejo), hash de templates/default.html y 6 digests de bpmn.html (recalculados con specir). El snapshot de fuente de bpmn.py en el oracle (linea 370) no se toco (congelado).
- docs/spec2viz/acta-de-retiro.md: punto 8 marcado hecho (2026-11-23; el commit se ve con git log --grep Task-Id).
# Validacion
Ver validation.log. A revisar: test_catalog_parity falla bajo xdist -n 4 pero pasa en serie.
