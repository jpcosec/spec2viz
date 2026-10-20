---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: sldb
# e.g., target_repo
target_project: spec2viz
# ISO 8601 timestamp
created_at: '2026-10-20T11:30:34'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# sldb cambia la salida: las alertas dejan de hacer fallar y nunca son silenciosas

_Describe the incoming message with enough evidence to triage._

Desde sldb, 2026-10-20. Aviso de un cambio de salida que va a main en los próximos commits (etapa (a) del anclaje, decisión del dueño). Si parseas alguna de estas salidas, revisa esto. Sin deploys ni release.

Regla: un ERROR es algo roto o que viola un contrato y hace fallar el comando. Una ALERTA es que la fuente se movió respecto de lo registrado: exit 0, pero nunca silenciosa. El exit code pasa a depender solo de los errores.

1. sldb stores check
   - Pasan a alerta (exit 0, PASS con conteo de alertas): hash raíz o roster atrasado, contrato movido, data_mutation, contract_mutation, legacy_contract, rewrite_loss, modelos sombreados y política de .gitignore.
   - Pasan a error (exit 1): documento trackeado ausente (missing), modelo que no importa, enlace a un store roto, ruido estructural (headings que el modelo no declara) y store declarado (.sldb/store.yaml) sin construir.
   - --format json: las claves de hoy siguen igual, y el note de cada documento no cambia. `valid` pasa a significar "sin errores", y llegan dos claves nuevas: `errors` y `alerts`, listas de {code, subject, what, fix}.
   - Texto: una línea "alert: ..." por alerta. --quiet también las imprime.
2. sldb stores build --check: que la copia trackee algo que el store local no tiene pasa a alerta. Todo lo demás sigue siendo error. El JSON trae `alerts`.
3. sldb selfdoc check y python-check: los campos, documentos o hashes viejos y la pista de renombre pasan a alerta. Metadata mal formada, ids repetidos y un grafo ausente o ilegible siguen siendo error.
4. sldb edges check: un shard construido desde otro hash_c pasa a alerta. Aristas inválidas y ciclos siguen siendo error.
5. sldb lint: una ruta citada que no existe pasa a ser la alerta lost (exit 0). Cada entrada del JSON trae `level`: error o alert.
6. sldb serve: en /lint, raíz o roster atrasados y data_mutation pasan a severity warning, y missing pasa a error. /health da status ok si no hay errores, y siempre lista los hallazgos, alertas incluidas.
7. sldb --envelope: `warnings` trae las alertas, que antes venían en [] fijo.
8. En GitHub Actions, cada alerta sale además como ::warning por stderr.

Si algo de esto te rompe, respóndeme por inbox antes de que lo suba.
