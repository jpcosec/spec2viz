# Result
- src/specir/cli.py: new `specir mcp --store [--level] [--actor]` calling sldb.mcp.server.serve(..., extensions=('specir.mcp_extension:register',)).
- tests/test_cli_mcp.py (new): four tools, --help, args reaching serve. 3 passed.
- skills/use-specir/SKILL.md: MCP line added.
- Review: tests/test_mcp_extension.py errors in session fixtures (store integrity alerts anchors/doc_lost from other tasks' ReviewDocs in the desk copy), not caused by this change. Needed `uv pip install mcp pytest` in the venv.
- Code commit in worktree branch deskops/deskops-e-3d0893847263.
- BLOCKED: `deskops advance task` refused: gate ritual-execution needs an accepted, intact bundle receipt; preflight review anchor_state is "changed". Not advanced.
