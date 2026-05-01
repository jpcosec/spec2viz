# Packaging Instructions

Use this checklist whenever a repo should ship as a serious package rather than an ad-hoc code dump.

## Goal

The package should be:
- installable from source without surprises
- runnable through its intended CLI or import path
- documented well enough for both humans and LLMs
- validated locally before install, commit, or release
- consistent about naming across metadata, docs, and commands

## Packaging Standard

### 1. Package identity must be coherent

Keep the package name, import path, CLI name, and documentation aligned.

Verify at least:
- project name in `pyproject.toml`
- console script entry points
- import examples in `README.md`
- command examples in docs and examples
- any legacy names or migration shims

If a rename happened, update all user-facing references and provide a clear migration error for old imports or commands.

### 2. Metadata must be complete

Every package should define, at minimum:
- `name`
- `version`
- `description`
- supported Python version
- license metadata
- runtime dependencies
- optional dev dependencies when relevant
- package discovery/build configuration

The metadata should describe the real package, not a placeholder.

### 3. The install path must be proven

Do not assume packaging works because the code runs locally.

Validate the actual install flow by running:

```bash
python3 -m pip install --force-reinstall .
```

Then verify the primary interface:

```bash
sldb --help
```

For other projects, replace `sldb` with the real CLI or import smoke test.

If the package is library-only, verify importability with a minimal command such as:

```bash
python3 -c "import your_package"
```

### 4. Tests must cover packaged usage

Prefer tests that exercise the public surface area, not just internal helpers.

At minimum, cover:
- import from installed source layout
- CLI invocation or public API usage
- one realistic roundtrip or happy path
- any migration compatibility behavior

If a package creates example files, templates, or bundled assets, include tests that prove those artifacts are shipped and usable.

### 5. Documentation must match the shipped package

The README should show the real install command, real import path, and real CLI examples.

Also document:
- what the package does
- who it is for
- the main commands or entry points
- one minimal example
- how to run tests or validate behavior
- any safety constraints or special modes

If the package has a built-in example generator, the example must stay current with the shipped behavior.

### 6. Examples are part of the package contract

Examples should be treated as executable documentation.

They should:
- use the current package name
- reflect current APIs and conventions
- demonstrate recommended patterns
- be simple enough for a first run
- be validated by tests when practical

### 7. User guidance should be explicit

If the package expects a certain authoring discipline, encode it in the product and docs.

Examples:
- required field metadata
- naming conventions
- validation steps before completion
- safe versus unsafe execution modes

Prefer enforcement in code when the rule is important enough to prevent bad package usage.

### 8. Release hygiene matters

Before calling packaging work done, check:
- `README.md` is current
- changelog or release notes mention meaningful package-facing changes
- no stale references to old package names remain
- no untracked example or asset files are missing from package data
- local tests pass
- local install verification passes

## Recommended Workflow

When asked to package or re-package a project, follow this order:

1. Inspect current metadata, CLI entry points, docs, and examples.
2. Fix naming mismatches and missing metadata.
3. Update docs and examples to match the real package surface.
4. Add or update tests for packaged usage.
5. Run the test suite.
6. Reinstall from source with `python3 -m pip install --force-reinstall .`.
7. Verify the shipped CLI or import path.
8. Only then commit and push.

## Rigour Bar

A package is not "done" just because:
- `pytest` passes
- the source imports inside the repo
- the CLI works through `python -m ...`

It is done when the packaged artifact, docs, examples, and user-facing commands all agree and work together.
