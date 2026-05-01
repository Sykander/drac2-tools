# Agent notes — drac2-tools

This repository holds **Avrae Drac2** artifacts: **`*.gvar`**, **`*.alias`**, **`*.alias-test`**, **`*.snippet`**, and documentation: **`docs/`**, **`README.md`**, and **`DEVELOPMENT.md`**.

**Gvar rule:** **`using()`** only exposes names **without** a leading **`_`**. Do not put **`_`**-prefixed “API” in **`docs/`**—that is source-only. See **`.cursor/rules/drac2-tools-maintainer.mdc`**.

## What to do when changing behavior

1. Update the implementation (`.gvar`, `.alias`, `.snippet`, etc.).
2. Update **any `docs/` markdown** that describes that surface (and **`docs/README.md`** when you add something new that should be indexed). Update **`README.md`** / **`DEVELOPMENT.md`** when onboarding, discovery, or workflow text should change. **`docs/`** is for **consumers** (API and behavior): keep it current and forward-looking—no changelog-style “removed X” prose. Put **testing / CI / avrae-ls** notes in **`AGENTS.md`** or **`DEVELOPMENT.md`**, not in **`docs/gvars/`** module pages. For **Drac2** examples in that prose, use **` ```py `** fenced blocks (not **` ```drac2 `**) so common Markdown highlighters work—see **`.cursor/rules/drac2-avrae-sources.mdc`** → Docs.
3. Update **`.alias` / `.alias-test`** when CI exercises behavior via **`avrae-ls --run-tests src`**.

Project rules in **`.cursor/rules/`** spell this out: **`drac2-tools-maintainer.mdc`** (always on: docs, tests, **`unused_gvars.md`** / workshop UUID hygiene), **`drac2-avrae-sources.mdc`** (Drac2 file roles, test vs production aliases, cached Avrae RST under **`.cursor/avrae-reference/`**), **`gvar-perf-boundaries.mdc`** when tuning **`*-perf`** stress tests or **`.cursor/scripts/probe_perf_boundaries.py`**, and **`python-drac2-style.mdc`** when weighing Python-style idioms against **Drac2 statement-budget** tradeoffs (see **`performance_examples`** gvar + **`--preset performance_examples`** on the probe script).

## Tooling

- **Drac2 tests:** `avrae-ls --run-tests src` (see `.github/workflows/test.yaml`). The **`languages`** gvar intentionally exposes only **`get_character_languages`** and **`language_comprehension_score`** without a leading **`_`**; Avrae disallows calling **`_*`** on `using`-bound gvars from aliases, so **`languages.alias-test`** covers those two surfaces only.
- **Perf stress boundaries (any util):** Re-tune **`*-perf.alias-test`** with a **single-test probe file** + **cap / gallop / binary** search. Tool: **`python3 .cursor/scripts/probe_perf_boundaries.py`** (`--preset regex` / `--preset rolls` / **`--preset performance_examples`**, or **`--dimension`** / **`--dimensions-file`**; template **`.cursor/templates/probe-perf-dimensions.example.txt`**). To **re-validate** `performance_examples` from current CI **`-loops`**, use **`.cursor/templates/probe-performance_examples-from-committed.txt`** with **`--max-binary 20`** (omit **`--preset`** so that file is the dimension source). Workflow: **`.cursor/rules/gvar-perf-boundaries.mdc`**.
- **avrae-ls behavior (`.alias-test`, `.avraels.json`, `varFiles`, mock context):** cached upstream docs under **`.cursor/avrae-ls-reference/`** ([avrae-ls](https://github.com/1drturtle/avrae-ls) on GitHub). Refresh with **`.cursor/avrae-ls-reference/refresh-avrae-ls-docs.sh`** when releases or `main` docs change; bump the version/date in **`.cursor/avrae-ls-reference/README.md`**.
- **Sourcemaps** (`utils/sourcemap.*.json`) are the **source of truth** for workshop layout. **`src/gvars/env.*.gvar`** and **`.varfile.json`** are **generated** by `npm run generate-env` / `npm run generate-vars` — do not edit those outputs by hand; run **`make rebuild`** (see **`Makefile`**) after sourcemap changes. Optional **`ENVIRONMENT=Development`** or **`Production`** selects which map many scripts use.
- **Deploy:** `npm run deploy` (`utils/deploy.js`) also keys off **`ENVIRONMENT`** and the sourcemaps.

## Drac2 / Avrae semantics

Use **`.cursor/rules/drac2-avrae-sources.mdc`** and the **cached RST** under **`.cursor/avrae-reference/`** (see **`README.md`** there for live URLs and **`refresh-avrae-docs.sh`**). That material is Cursor-adjacent, not under `docs/`. Do not invent engine behavior—confirm against those files, then refresh if they lag Read the Docs.

**Discord `<drac2>` blocks:** On the live bot, block substitution follows the **return**-based rules in **`aliasing-api.rst.txt`**—see **`.cursor/rules/drac2-avrae-sources.mdc`** → **Live Avrae `<drac2>` blocks**. One-liner tests should **`return "…"`**, not rely on a trailing expression alone.
