---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-27T21:14:34'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Integrar el diagrama de anillos concéntricos de sldb (piezas del spec)

_Describe the incoming message with enough evidence to triage._

En sldb hay un diagrama hecho a mano en d3 que funcionó muy bien para ordenar el spec y hay que ver cómo integrarlo: `sldb/docs/spec/piezas.html` (commit 14b25805a), generado desde `sldb/docs/spec/piezas.md`.

Qué dibuja: 49 piezas de un sistema ubicadas en anillos concéntricos (cada anillo depende solo de los de adentro; el anillo central partido en dos mitades), con sus dependencias como líneas. Cada pieza lleva varios ejes independientes y el dibujo usa tres a la vez: el anillo da la posición, un eje da el color (quién pone la pieza: núcleo, declarado encima, puerta), otro da la forma (estructura, operación, mecanismo, lenguaje, adaptador), y un tercero un contorno punteado (abierto). Al pasar el cursor muestra los ejes de la pieza, de qué depende y quién la usa; se filtra por principio y por estado; tiene vista de tabla.

Por qué va a specIR: hoy es una página HTML suelta, y la regla del workspace es que un diagrama se declara y lo dibuja graph_ui; el HTML estático es solo para uso inline. Las piezas se van a cargar como grafo en el store (átomos con tags por eje y RelationDoc para las dependencias), así que el dibujo debería salir de ahí.

Lo que hay que ver: (1) si esto es una notación nueva o una vista con un layout nuevo: anillos concéntricos donde la posición radial la da un eje ordenado y el sector angular otro; (2) cómo declara una vista qué eje va a posición, cuál a color, cuál a forma y cuál a contorno, sin un if por diagrama; (3) si graph_ui tiene o necesita un layout radial por anillos; (4) si la regla 'una dependencia solo va hacia un anillo igual o más interno' se declara como RuleDoc junto a la vista.

No es urgente. Pedido por JP el 2026-11-27.
