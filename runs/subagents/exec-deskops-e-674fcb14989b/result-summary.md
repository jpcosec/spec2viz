# result-summary: task-ir04b (executor exec-deskops-e-674fcb14989b)

run_id: exec-deskops-e-674fcb14989b
session: n/a (Claude Code executor; no child session file)
session_sha256: n/a

Started from the WIP patch the user pointed to (runs/subagents/20261120-ir04b-wip/wip.patch), applied in the worktree, reviewed against Goal/Validation, completed and run.

## Commit (branch deskops/deskops-e-674fcb14989b)
- src/specir/mcp_extension.py: no longer creates a WriteTools nor replaces propose_changes/apply_changes; registers IR05 D2-E with `context.add_batch_validator` (error finding `specir_agent_verifies`), recognising typed Change (propose) and BatchChange (apply).
- tests/test_mcp_extension.py: D2-E tests adjusted to sldb's `domain` rejection.
- tests/test_mcp_undo.py (new): real sldb mcp + specIR extension over mount_copy; undo of create+edit+edge, stale refusal (applied false, rejected stale, document, written false; batch stays on the stack and is undone after reverting the foreign change), steps=2 and nothing_to_undo, level 0 (no write tools/undo), level 1 refuses RuleDoc, level 2 undoes a RuleDoc batch, rules/edges checks after undo, domain validators after undo, no own undo in src/specir.

## Validation (validation.log)
18 passed, 1 xfailed; grep -nE "undo_changes|inverse" src/specir finds only vendored bpmn-js; deskops graph missing rc 0.

## For the supervisor
- FINDING FOR SLDB (Validation 1 only partly met): after undo_changes the content of every .md is restored, but sldb re-stamps provenance `sldb.at` and `sldb.via` (create_document -> save_document_payload) on the edited document, and the derived hashes in .sldb/ (source_hash, model_hash, roster_hash, store_hash) change. So sha256 of .md/store is NOT byte-identical. Content tests normalise `at`/`via`; the byte-identity test is `xfail(strict=True)` and will flip when sldb stops re-stamping.
- undo_changes applies the inverse batch with api.apply_batch directly: specIR's batch validator does not run on it. After undo, sldb rules check and edges check pass (rc 0) and the validator over the stored documents finds no error (no finding for sldb here).
- Test env note: tests/conftest.py WORKSPACE=REPO.parent fails inside a worktree (deskops store not a sibling); I used a temporary symlink .worktrees/deskops (removed) and PYTHONPATH=<worktree>/src. Not changed in conftest.
