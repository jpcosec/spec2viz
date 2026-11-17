---
sldb:
  by: agent
  at: '2026-11-17T14:07:28Z'
  authority: generated
  via: create_document
# review-<task>-<kind>-<n>
id: review-task-ir08-extractor-estático-django-drf-y-sql-evidence-tests-2
# preflight | bundle | reproduction | goldens | owner | node | evidence
kind: evidence
# kind evidence only: tests | commit | atom | materialization | document | external
fact: tests
# kind evidence only: what the producer verified, one item per line
value: tests/extract/test_blog_extraction.py
# doc:<Model>:<id> or empty for reviews of plan nodes
subject: doc:TaskCodeDoc:task-ir08-extractor-estático-django-drf-y-sql@sha256:714ea9a93fbd78049b742685bc2c0d2cd16c5d16a6a6b3d42cfb03768b60526b
# <plan>/dag.yaml#node:<ID>; empty when subject names a document
subject_ref: ''
# RuntimeProfileDoc name or "human"
engine: deskops-closeout
actor: IR
# Run evidence directory under runs/, relative to the project root
run_dir: ''
input_sha256: 060284b70bfb4fb8fa96aafb4698399a39f5df759378be026a9ff3e80db87b7c
# preflight/bundle: SHA-256 of the input with the TaskDoc replaced by its __contract__ digest
contract_sha256: ''
output_sha256: ''
# pending | accepted | rejected | incomplete
verdict: accepted
reason: 'verified: tests tests/extract/test_blog_extraction.py'
# ISO 8601 timestamp
created_at: '2026-11-17T14:07:27.655920+00:00'
# ISO 8601 timestamp, empty while pending
disposed_at: '2026-11-17T14:07:27.655920+00:00'
disposed_by: IR
# e.g. workspace:desk
tags:
- workspace:desk
---

# Closeout evidence tests of task-ir08-extractor-estático-django-drf-y-sql

## Summary

_Summarize what was reviewed and the evidence this receipt records._

closeout verify checked tests: tests/extract/test_blog_extraction.py

## Disposition

_Record the verdict rationale and who disposed of the review._

Verdict accepted: verified: tests tests/extract/test_blog_extraction.py
