# spec2viz store

`.sldb/store.yaml` is the only versioned part of this store: it declares the models (spec2viz's own and
the ones inherited from deskops through the `deskops` link), the predicates and which tracked Markdown
files are documents of which model. Everything under `.sldb/core/` and `.sldb/runtime/` is derived and
stays out of git (sldb `docs/architecture/derived-store-boundary.md`).

In a fresh clone, with deskops checked out next to spec2viz (`../deskops`) and its store built:

```bash
sldb stores build --store .sldb     # rebuild .sldb/core from the declaration
sldb stores check --store .sldb     # PASS
```

`sldb stores build --check` rebuilds a scratch copy and fails if the sources and the declaration diverge;
CI runs it in the `store` job. After adding a model or a new kind of tracked document, refresh the
declaration with `sldb stores declare --write` and review the diff.
