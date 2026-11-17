---
sldb:
  by: agent
  at: '2026-11-17T00:06:10Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-espejo-sldb-readers-y-facts-tsx-ts-y-sql-b2-evidence-external-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: external
# kind evidence only: what the producer verified, one item per line
value: 'https://github.com/jpcosec/sldb/commit/34b26a505f81094d3859daea04289ac14c185b19

  https://github.com/jpcosec/sldb/commit/50e4aaabcc6150c6f148c29149347d76bad92934

  https://github.com/jpcosec/sldb/commit/600b51a9c2431c1fdaaa335f6a726138b290961f

  https://github.com/jpcosec/sldb/commit/b60b02b75a7bc9569267242b79225511930b5b0a'
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskExternalDoc:task-espejo-sldb-readers-y-facts-tsx-ts-y-sql-b2@sha256:7e5cc51e54567c8e4f560e39b31134606626c5ef46fc602159c1bdbba0717053
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 0e2638f1b257d7a738448ed3618d10ec2e37f094de05d69755bad42102d85531
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: external https://github.com/jpcosec/sldb/commit/34b26a505f81094d3859daea04289ac14c185b19

  https://github.com/jpcosec/sldb/commit/50e4aaabcc6150c6f148c29149347d76bad92934

  https://github.com/jpcosec/sldb/commit/600b51a9c2431c1fdaaa335f6a726138b290961f

  https://github.com/jpcosec/sldb/commit/b60b02b75a7bc9569267242b79225511930b5b0a'
# ISO 8601 timestamp
created_at: '2026-11-17T00:06:06.586055+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T00:06:06.586055+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence external of task-espejo-sldb-readers-y-facts-tsx-ts-y-sql-b2

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked external: https://github.com/jpcosec/sldb/commit/34b26a505f81094d3859daea04289ac14c185b19, https://github.com/jpcosec/sldb/commit/50e4aaabcc6150c6f148c29149347d76bad92934, https://github.com/jpcosec/sldb/commit/600b51a9c2431c1fdaaa335f6a726138b290961f, https://github.com/jpcosec/sldb/commit/b60b02b75a7bc9569267242b79225511930b5b0a

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: external https://github.com/jpcosec/sldb/commit/34b26a505f81094d3859daea04289ac14c185b19
https://github.com/jpcosec/sldb/commit/50e4aaabcc6150c6f148c29149347d76bad92934
https://github.com/jpcosec/sldb/commit/600b51a9c2431c1fdaaa335f6a726138b290961f
https://github.com/jpcosec/sldb/commit/b60b02b75a7bc9569267242b79225511930b5b0a
