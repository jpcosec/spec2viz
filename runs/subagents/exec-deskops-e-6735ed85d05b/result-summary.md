# Result
- Changed: pyproject.toml line 43 (parity marker text) -> "compares specIR with the frozen spec2viz outputs (revision 2de1056) in tests/visual/goldens/; spec2viz is not needed". No tests touched.
- Validation: parity tests in tests/visual: 63 passed, 0 skipped (see validation.log). One initial failure was only the missing tree-sitter extra in my venv; passed after installing it.
- Commit made in worktree branch deskops/deskops-e-6735ed85d05b (file: pyproject.toml).
