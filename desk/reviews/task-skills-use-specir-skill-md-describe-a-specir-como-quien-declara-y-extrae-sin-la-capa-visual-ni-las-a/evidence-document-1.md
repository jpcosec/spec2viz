---
sldb:
  by: agent
  at: '2026-11-25T21:23:11Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a-evidence-document-1
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: document
# kind evidence only: what the producer verified, one item per line
value: skills/use-specir/SKILL.md
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskDocsDoc:task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a@sha256:46fd1a49af4630053dd116562326c7c49123ba01dd182c667af02323ff267de1
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 08cfafd4e3433c3f2728d5a957a1e50d99f9188e70b43e142cae3aea8ce98614
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: document skills/use-specir/SKILL.md'
# ISO 8601 timestamp
created_at: '2026-11-25T21:22:59.776352+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-25T21:22:59.776352+00:00'
disposed_by: IR
# e.g. system:deskops
tags: []
---

# Closeout evidence document of task-skills-use-specir-skill-md-describe-a-specir-como-quien-declara-y-extrae-sin-la-capa-visual-ni-las-a

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked document: skills/use-specir/SKILL.md

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: document skills/use-specir/SKILL.md
