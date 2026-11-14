## REFORMULACION
IR13D es una entrega de código, no un agregado. Propósito: que specIR sustituya las entradas públicas de spec2viz mediante un comando propio, una API Python pública y una habilidad de agente, más una tabla de correspondencia. Resultado: paquete instalable en entorno limpio, CLI operativa sin spec2viz instalado, pruebas de CLI/API/empaquetado y filas de CLI, API y habilidad de la matriz con condición de retiro cumplida. Repo: `specIR`. Límites: no implementa capacidades —dependen de IR13A, IR13B, IR13C e IR12—; no instala la habilidad en otros repos; no migra consumidores.

## AMBIGUEDADES
1. “cada entrada pública de spec2viz”: no se define el universo exacto ni versión de referencia. Obligaría a inventar el inventario de entradas públicas.
2. “API Python pública equivalente a la que exporta el paquete spec2viz”: no se enumeran símbolos, módulos ni firma esperada. Obligaría a inventar la superficie de API.
3. “Las pruebas anteriores pasan”: no hay pruebas previas identificadas en el nodo. Obligaría a inventar cuáles son.
4. “tabla de correspondencia comando por comando”: no se fija formato, columnas ni criterio de equivalencia. Obligaría a inventar el esquema documental.
5. “habilidad de agente que reemplaza a la de uso de spec2viz”: no se indica ruta, nombre ni contenido mínimo de la habilidad origen. Obligaría a inventar su contrato.
6. “entorno limpio”: no se define gestor, versión de Python ni método de instalación. Obligaría a inventar el escenario de empaquetado.

## DRY-RUN
Un ejecutor futuro leería IR13D, las salidas de IR13A/B/C e IR12 y la superficie pública observable de spec2viz para inventariar comandos, subgrupos y API. Crearía o ajustaría `src/specir/cli.py`, `src/specir/visual/__init__.py`, `skills/use-specir/SKILL.md`, `docs/spec2viz/correspondencia-cli.md` y las pruebas `test_cli.py`, `test_api.py`, `test_packaging.py`. Dependencias: capacidades ya provistas por IR13A/B/C e IR12. Validaciones futuras: invocar cada equivalente, portar pruebas de API, extraer e invocar comandos citados por la habilidad, instalar en entorno limpio y arrancar sin spec2viz. Sin ejecutar nada.

## FUTURO
IR13 consumirá la tabla y la evidencia para el gate de retiro y el acta. Los repos consumidores deberán migrar mediante sus desks. El dueño de spec2viz decidirá archivarlo o borrarlo cuando el gate lo permita.
