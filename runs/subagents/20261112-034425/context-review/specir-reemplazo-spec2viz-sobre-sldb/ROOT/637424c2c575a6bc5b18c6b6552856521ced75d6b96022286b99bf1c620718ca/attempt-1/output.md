## REFORMULACION
El encargo es crear en el repo `specIR` un paquete periférico sobre la API pública de SLDB: primero un MCP de lectura/escritura y análisis; después una capa visual que absorba gradualmente spec2viz. `pron` no debe ser dependencia de ejecución y sus contratos necesarios se incorporan como MCPs en SLDB. spec2viz solo se retira cuando la matriz completa y el gate lo demuestren. El resultado sustantivo es cerrar los 17 nodos de entrega con evidencia y que IR13 confirme cobertura total y consumidores migrados antes de proponer el retiro.

## AMBIGUEDADES
1. “la capa visual absorbe de forma gradual spec2viz” no define si “absorber” incluye CLI, API Python, habilidades de agente y recursos empaquetados, no solo renderizado. Obligaría a inventar el perímetro de absorción.
2. “sus contratos necesarios se incorporan como MCPs en SLDB” no dice qué contratos de `pron`, quién los implementa en SLDB ni cómo los consume specIR. Obligaría a inventar titularidad e interfaz.
3. “Los 17 nodos de entrega cierran con evidencia” no define un artefacto global de evidencia; cada hijo tiene su aceptación, pero no hay índice común. Obligaría a inventar el formato de cierre.

## DRY-RUN
No ejecutable como agregado: se cumple recorriendo hijos. IR01 produce matriz API→MCP; alimenta IR02, IR03, IR05. IR02 decide contrato de escritura y atoms; IR03 entrega MCP lectura; ambos alimentan IR04. IR05 fija procedencia/divergencia; IR04 e IR05 alimentan IR06, que crea tipos, reglas y store del blog. IR06 alimenta IR07–IR11. IR07 produce matriz/gate spec2viz; IR08 e IR09 extraen Django/SQL y React; IR10 consume IR06/IR08/IR09 para reglas e impacto. IR11 compila desde IR07/IR06; IR12 renderiza desde IR11; IR13A sincroniza/genera desde IR07/IR11; IR13B consume IR13A/IR12; IR13C consume IR07; IR13D consume IR13A/B/C/IR12. IR13 consume IR13A–D e IR07. Validación conjunta: aceptaciones de los 17, imports sin `pron`/spec2viz, matriz con pruebas citadas, gate IR13 con salida cero sobre el universo inventariado y acta de retiro.

## FUTURO
El dueño del proyecto decide IR02, IR05 y la decisión de IR07; SLDB recibe faltantes y decide/extiende su API; los desks de graph_ui, deskops y stores afectados ejecutan migraciones pedidas por IR13; el dueño de spec2viz decide archivarlo tras el gate.
