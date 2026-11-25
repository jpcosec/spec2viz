# Result
- src/specir/mcp_extension.py: new `serve(store, level=None, actor=None)` (lazy-imports sldb.mcp.server/READ, calls server.serve with the specir extension).
- src/specir/cli.py: `mcp` imports specir.mcp_extension.serve lazily; no sldb.mcp import; --level help is free text.
- Validation: tests/test_imports.py + tests/test_cli_mcp.py: 12 passed (validation.log). Tests unchanged.
- Commit in worktree branch deskops/deskops-e-544521523f25 with the two files above.
- run_id: exec-deskops-e-544521523f25; session/session_sha256: not available in this environment.
