---
sldb:
  by: agent
  at: '2026-11-27T18:05:55Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: IR
# ISO 8601 timestamp
created_at: '2026-11-27T15:02:16'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Desde mepu: el render de mermaid (mmdc con Chrome headless de puppeteer) se traba en la GPU; pasar --disable-gpu

_Describe the incoming message with enough evidence to triage._

Reenviada desde el inbox de mepu (triage del 27-11; nota original desk/inbox/20261124-035615-suggestion-el-guardi-n-de-mermaid-mmdc-chrome-headless-de-puppeteer-se-traba-en.md en heyantonia/mepu). # El guardián de mermaid (mmdc, Chrome headless de puppeteer) se traba en 


El guardián de mermaid (mmdc, Chrome headless de puppeteer) se traba en la GPU en johanes: los procesos gpu-process quedan en estado D en drm_open sobre /dev/dri/renderD128, no se pueden matar ni con SIGKILL y se acumulan (130 el 24-11, ~2 GB, swap lleno), lo que además sube la presión de IO para todas las sesiones. Hoy cada agente lo esquiva exportando VK_ICD_FILENAMES=/nonexistent LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=llvmpipe. Propuesta: que el target que llama a mmdc pase un puppeteer config con args --disable-gpu --use-angle=swiftshader (o esas variables) para que nadie dependa de acordarse. Los procesos ya trabados solo se liberan reiniciando el driver o la máquina.
