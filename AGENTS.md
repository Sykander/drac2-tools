# Agent notes — drac2-tools

This repository holds **Avrae Drac2** artifacts: **`*.gvar`**, **`*.alias`**, **`*.alias-test`**, **`*.snippet`**, and **markdown under `docs/`**.

## What to do when changing behavior

1. Update the implementation (`.gvar`, `.alias`, `.snippet`, etc.).
2. Update **any `docs/` markdown** that describes that surface (and **`docs/README.md`** when you add something new that should be indexed).
3. Update **`.alias` / `.alias-test`** when CI exercises behavior via **`avrae-ls --run-tests src`**.

Project rules in **`.cursor/rules/`** spell this out: **`drac2-tools-maintainer.mdc`** (always on: docs, tests, **`unused_gvars.md`** / workshop UUID hygiene) and **`drac2-avrae-sources.mdc`** (Drac2 file roles, test vs production aliases, cached Avrae RST under **`.cursor/avrae-reference/`**).

## Tooling

- **Drac2 tests:** `avrae-ls --run-tests src` (see `.github/workflows/test.yaml`).
- **Sourcemaps** (`utils/sourcemap.*.json`) are the **source of truth** for workshop layout. **`src/gvars/env.*.gvar`** and **`.varfile.json`** are **generated** by `npm run generate-env` / `npm run generate-vars` — do not edit those outputs by hand; run **`make rebuild`** (see **`Makefile`**) after sourcemap changes. Optional **`ENVIRONMENT=Development`** or **`Production`** selects which map many scripts use.
- **Deploy:** `npm run deploy` (`utils/deploy.js`) also keys off **`ENVIRONMENT`** and the sourcemaps.

## Drac2 / Avrae semantics

Use **`.cursor/rules/drac2-avrae-sources.mdc`** and the **cached RST** under **`.cursor/avrae-reference/`** (see **`README.md`** there for live URLs and **`refresh-avrae-docs.sh`**). That material is Cursor-adjacent, not under `docs/`. Do not invent engine behavior—confirm against those files, then refresh if they lag Read the Docs.
