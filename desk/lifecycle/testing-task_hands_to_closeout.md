---
sldb:
  by: agent
  at: '2026-11-17T23:28:47Z'
  authority: generated
  via: save_document_payload
source_id: RitualDoc:ritual-testing
target_id: RitualDoc:ritual-closeout
relation_type: task_hands_to_closeout
condition: nonempty(validation)
attributes:
  sets:
    status: ready_for_testing
  terminal: false
  hooks:
  - name: evento-para-el-coordinador
    run:
    - sh
    - -c
    - mkdir -p runs/hooks && printf '%s %s %s %s->%s\n' "$(date -u +%FT%TZ)" "$DESKOPS_TASK_ID"
      "$DESKOPS_TRANSITION" "$DESKOPS_FROM_NODE" "$DESKOPS_TO_NODE" >> runs/hooks/events.log
    timeout: 30
---

# Task hands to closeout

## Notes

The task has validation to prove and moves to the closeout ritual.
