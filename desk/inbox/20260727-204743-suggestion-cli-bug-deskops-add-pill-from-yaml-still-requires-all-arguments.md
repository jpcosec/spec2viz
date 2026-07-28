---
kind: suggestion
sender_project: spec2viz
created_at: 2026-07-27T20:47:43
status: open
---

# CLI bug: deskops add pill --from-yaml still requires all arguments

When running `deskops add pill --from-yaml pill1.yml`, argparse still enforces the required positional/keyword arguments like --what, --why, etc., resulting in: `deskops add pill: error: the following arguments are required: --what, --why, --when, --where, --how, --how-not`. The --from-yaml flag should override or make these arguments optional during argparse parsing.
