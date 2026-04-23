# Agent notes — drac2-tools

This repository holds **Avrae Drac2 gvars** (`*.gvar`), companion **aliases** (`*.alias`), **alias tests** (`*.alias-test`), and **markdown docs** under `docs/gvars/`.

## What to do when changing behavior

1. Update the **`.gvar`** implementation.
2. Update **`docs/gvars/*.md`** (and `docs/README.md` if you add a new documented module).
3. Update **`.alias` / `.alias-test`** for any new or changed behavior CI exercises via `avrae-ls --run-tests src`.

Project rules in **`.cursor/rules/`** expand on this (including **`drac2-avrae-sources.mdc`** for `.gvar`, `.alias`, `.snippet`, and `.alias-test` conventions).

## Tooling

- **Gvar tests:** `avrae-ls --run-tests src` (see `.github/workflows/test.yaml`).
- **Deploy / env generation:** `package.json` scripts and `utils/` Node helpers.

## Avrae / Drac2 depth

For engine-specific or workshop quirks not covered in-repo, prefer the **Drac2 Coder** Cursor agent or your usual Avrae references rather than inventing behavior.
