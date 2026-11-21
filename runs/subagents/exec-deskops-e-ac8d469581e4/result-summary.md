# Result
- Changed only tests/test_mcp_undo.py (commit in worktree branch deskops/deskops-e-ac8d469581e4, Task-Id trailer).
- md_digest no longer imports sldb.models; it strips the sldb frontmatter block locally (yaml) and ALSO hashes, for each tracked document, its payload via sldb.api.load_runtime_documents (store compared by content). Used by the identity test (content() before/after).
- No real undo failure revealed; src/specir untouched.
- Validation: see validation.log, all green.
- Note for reviewer: in the worktree the 4 untracked run.md of earlier runs are missing, so 'sldb stores update' in mount_copy fails; I copied them temporarily from the main checkout to run tests and removed them afterwards (not committed).
