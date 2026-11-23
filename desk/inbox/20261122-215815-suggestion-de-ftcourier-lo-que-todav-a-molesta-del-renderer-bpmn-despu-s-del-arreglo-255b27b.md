---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: ftcourier
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-11-22T21:58:15'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
---

# De ftcourier: lo que todavía molesta del renderer bpmn después del arreglo (255b27b)

_Describe the incoming message with enough evidence to triage._

Reenviada desde el desk de ftcourier (nota 20261120-014152, triaje del 2026-11-22). Visto al regenerar los diagramas de ftcourier (FTC-33) con spec2viz 255b27b. (1) El ícono de las tareas con kind user, service o send se dibuja encima de la primera letra del rótulo: por eso ftcourier no usa esos tipos. (2) Varias flechas que entran al mismo evento de fin comparten el punto de entrada y se cruzan antes de llegar (specs/negocio/reglas-del-semaforo.yml de ftcourier: seis flechas a «Queda en la cola del día»). (3) Un evento de fin que no es data.end queda siempre en la última columna y su flecha atraviesa el diagrama. (4) El rótulo de una rama puede quedar montado sobre una línea paralela. (5) Una cadena larga en un solo carril baja la letra a unos 9 px a 1600 de ancho (specs/negocio/flujo-cobranza-actual.yml). (6) El almacén de datos no existe como elemento. La salida antonia-html sigue sin servir para un cliente: tema oscuro, carriles en cualquier orden y flechas sobre los títulos. No se comprobó cuáles siguen vigentes en master (ca2d22a y 2f7bfa5).
