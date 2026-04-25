# avrae-ls upstream reference (cached)

This folder lives under **`.cursor/avrae-ls-reference/`** next to **`.cursor/rules/`**. It holds **copies of [avrae-ls](https://github.com/1drturtle/avrae-ls) documentation** from the **`main`** branch for Cursor agents and contributors—not part of the shipped Drac2 product docs under `docs/`.

Use it when you need authoritative detail on **`.alias-test`**, **`.avraels.json`**, **`avrae-ls --run-tests`**, workspace configuration, mock execution, and related LSP behavior—without guessing from an installed `avrae-ls` version alone.

| Cached file | Upstream (live) |
|-------------|-----------------|
| `upstream/README.md` | [github.com/1drturtle/avrae-ls/blob/main/README.md](https://github.com/1drturtle/avrae-ls/blob/main/README.md) |
| `upstream/docs/alias-tests.md` | [github.com/1drturtle/avrae-ls/blob/main/docs/alias-tests.md](https://github.com/1drturtle/avrae-ls/blob/main/docs/alias-tests.md) |
| `upstream/docs/configuration.md` | [github.com/1drturtle/avrae-ls/blob/main/docs/configuration.md](https://github.com/1drturtle/avrae-ls/blob/main/docs/configuration.md) |

**Releases / PyPI:** [pypi.org/project/avrae-ls](https://pypi.org/project/avrae-ls/) — when a new **avrae-ls** release ships, refresh this cache and update **Tracked avrae-ls version** below so agents know what the copy was aligned with.

## Tracked avrae-ls version

Record the **released** version you last validated against (run `avrae-ls --version` locally), not only the git `main` snapshot date.

**Tracked avrae-ls version:** 0.8.4

## Last upstream fetch

Update whenever you run **`refresh-avrae-ls-docs.sh`** (or otherwise replace files under **`upstream/`**).

**Last upstream fetch:** 2026-04-26

## Refreshing the cache

From the repository root:

```bash
./.cursor/avrae-ls-reference/refresh-avrae-ls-docs.sh
```

Or from this directory:

```bash
./refresh-avrae-ls-docs.sh
```

Requirements: `curl`, a shell. The script overwrites the files under **`upstream/`**.

After a refresh, bump **Last upstream fetch** and, if you verified against a new installer, **Tracked avrae-ls version**. If upstream adds more docs under **`docs/`**, extend **`refresh-avrae-ls-docs.sh`** and add rows to the table above.

## When behavior looks wrong

1. Search **`upstream/docs/`** and the root **`upstream/README.md`** for `.alias-test`, `.avraels.json`, profiles, `varFiles`, etc.
2. Compare with the **live** GitHub links in the table. If upstream changed, **refresh** and commit.
3. If the cache matches upstream but **`avrae-ls --run-tests`** still disagrees, compare your local **`avrae-ls --version`** to **Tracked avrae-ls version**—you may be on a different build than the repo expects.
