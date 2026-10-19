---
id: atom-activity-pseudonodos-inicial-y-final-propios
title: 'Activity: pseudonodos inicial y final propios'
five_wh_one_plus: what
tags:
- system:spec2viz
- topic:notation
provenance: docs/notation-contract.md
---

# Activity: pseudonodos inicial y final propios

## Answer

Al sincronizar una actividad, el nodo inicial es un pseudonodo propio (__initial, glifo start) con next al paso de start, que conserva su glifo de accion o decision. El final es end mismo si no es un paso (end: end) o, si end nombra un paso, un pseudonodo __final al que ese paso fluye. Un glifo con label vacio explicito no lleva rotulo.
