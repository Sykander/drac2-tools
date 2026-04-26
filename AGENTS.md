# Agent notes — drac2-tools

This repository holds **Avrae Drac2** artifacts: **`*.gvar`**, **`*.alias`**, **`*.alias-test`**, **`*.snippet`**, and **markdown under `docs/`**.

## What to do when changing behavior

1. Update the implementation (`.gvar`, `.alias`, `.snippet`, etc.).
2. Update **any `docs/` markdown** that describes that surface (and **`docs/README.md`** when you add something new that should be indexed). **`docs/`** is for **consumers** of the code (API and behavior); put **testing / CI / avrae-ls** notes here in **`AGENTS.md`** or **`DEVELOPMENT.md`**, not in **`docs/gvars/`** module pages.
3. Update **`.alias` / `.alias-test`** when CI exercises behavior via **`avrae-ls --run-tests src`**.

Project rules in **`.cursor/rules/`** spell this out: **`drac2-tools-maintainer.mdc`** (always on: docs, tests, **`unused_gvars.md`** / workshop UUID hygiene), **`drac2-avrae-sources.mdc`** (Drac2 file roles, test vs production aliases, cached Avrae RST under **`.cursor/avrae-reference/`**), and **`gvar-perf-boundaries.mdc`** when tuning **`*-perf`** stress tests or **`.cursor/scripts/probe_perf_boundaries.py`**.

## Tooling

- **Drac2 tests:** `avrae-ls --run-tests src` (see `.github/workflows/test.yaml`).
- **Perf stress boundaries (any util):** Re-tune **`*-perf.alias-test`** with a **single-test probe file** + **cap / gallop / binary** search. Tool: **`python3 .cursor/scripts/probe_perf_boundaries.py`** (`--preset regex` / `--preset rolls`, or **`--dimension`** / **`--dimensions-file`**; template **`.cursor/templates/probe-perf-dimensions.example.txt`**). Workflow: **`.cursor/rules/gvar-perf-boundaries.mdc`**.
- **avrae-ls behavior (`.alias-test`, `.avraels.json`, `varFiles`, mock context):** cached upstream docs under **`.cursor/avrae-ls-reference/`** ([avrae-ls](https://github.com/1drturtle/avrae-ls) on GitHub). Refresh with **`.cursor/avrae-ls-reference/refresh-avrae-ls-docs.sh`** when releases or `main` docs change; bump the version/date in **`.cursor/avrae-ls-reference/README.md`**.
- **Sourcemaps** (`utils/sourcemap.*.json`) are the **source of truth** for workshop layout. **`src/gvars/env.*.gvar`** and **`.varfile.json`** are **generated** by `npm run generate-env` / `npm run generate-vars` — do not edit those outputs by hand; run **`make rebuild`** (see **`Makefile`**) after sourcemap changes. Optional **`ENVIRONMENT=Development`** or **`Production`** selects which map many scripts use.
- **Deploy:** `npm run deploy` (`utils/deploy.js`) also keys off **`ENVIRONMENT`** and the sourcemaps.

## Drac2 / Avrae semantics

Use **`.cursor/rules/drac2-avrae-sources.mdc`** and the **cached RST** under **`.cursor/avrae-reference/`** (see **`README.md`** there for live URLs and **`refresh-avrae-docs.sh`**). That material is Cursor-adjacent, not under `docs/`. Do not invent engine behavior—confirm against those files, then refresh if they lag Read the Docs.
