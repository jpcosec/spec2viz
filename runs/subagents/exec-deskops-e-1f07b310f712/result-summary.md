# Result
Files (committed in worktree branch deskops/deskops-e-1f07b310f712):
- src/specir/extract/plan.py: `bounded_name` + `MAX_NAME_BYTES=200`; `edge_name` uses it (short names unchanged; long: UTF-8-safe prefix + '-' + sha256[:12]).
- tests/extract/test_edge_name_bounded.py: cases (a)-(e), incl. Planned.path and .yaml file-name length, and extract_frontend on a deep path.
Validation: 17 passed (see validation.log).
Note: node names are out of scope; the extract_frontend test uses a path deep enough for edge names >200 bytes but node names <255.
run_id: exec-deskops-e-1f07b310f712; session/session_sha256: n/a (not available to the executor)
