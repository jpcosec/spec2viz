# Task Completion Checklist

Before considering a task complete, ensure the following steps are performed:

1.  **Code Quality**:
    - [ ] Run `ruff check .` and resolve any new violations.
    - [ ] Ensure type hints are correct and complete.
2.  **Testing**:
    - [ ] Run `pytest` to ensure no regressions.
    - [ ] Add new tests in `tests/` for any new features or bug fixes.
    - [ ] If adding a new diagram type, include tests for Model, Compiler, and Renderer.
3.  **Documentation**:
    - [ ] Update `README.md` if CLI or API changes.
    - [ ] Update `DEVELOPER_GUIDE.md` if architectural patterns change.
4.  **Verification**:
    - [ ] Verify the change with a real example from `tests/fixtures/` or `examples/`.
    - [ ] If CLI changes, verify with `spec2viz --help`.
