---
sldb:
  by: agent
  at: '2026-11-18T16:35:17Z'
  authority: generated
  via: save_document_payload
source_id: RitualDoc:ritual-execution
target_id: RitualDoc:ritual-testing
relation_type: task_activates
condition: ''
attributes:
  sets:
    status: active
  terminal: false
  hooks:
  - name: encola-reap-del-ejecutor
    run:
    - deskops
    - queue
    - add
    - dispatch-reap
    - --root
    - .
    timeout: 60
  - name: encola-tester
    run:
    - deskops
    - queue
    - add
    - dispatch-tester
    - --root
    - .
    timeout: 60
---

# Task activates

## Notes

The task passes its execution gate and enters active work, under the testing ritual.
