# Avrae upstream reference (cached)

This folder lives under **`.cursor/avrae-reference/`** next to **`.cursor/rules/`**. It holds **copies of official Avrae Read the Docs sources** for Cursor agents and contributors—not part of the shipped Drac2 product docs under `docs/`.

| File | Canonical URL (HTML) | RST source URL (what `refresh-avrae-docs.sh` downloads) |
|------|----------------------|-----------------------------------------------------------|
| `aliasing-api.rst.txt` | https://avrae.readthedocs.io/en/latest/aliasing/api.html | https://avrae.readthedocs.io/en/latest/_sources/aliasing/api.rst.txt |
| `automation-reference.rst.txt` | https://avrae.readthedocs.io/en/latest/automation_ref.html | https://avrae.readthedocs.io/en/latest/_sources/automation_ref.rst.txt |

## Last synced

Update the line below whenever you run **`refresh-avrae-docs.sh`** in this directory (or otherwise replace these files).

**Last RST fetch:** 2026-04-24

## Refreshing the cache

From the repository root:

```bash
./.cursor/avrae-reference/refresh-avrae-docs.sh
```

Or from this directory:

```bash
./refresh-avrae-docs.sh
```

Requirements: `curl`, a shell. The script overwrites the two `.rst.txt` files here.

After a refresh, **check the canonical HTML URLs** in a browser if Avrae reorganizes paths (404 or redirect chains). If Read the Docs moves `_sources/…` paths, update the URLs in **`refresh-avrae-docs.sh`** and in this table.

## When behavior looks wrong

1. Read the relevant section in **`aliasing-api.rst.txt`** (Drac2 / aliasing) or **`automation-reference.rst.txt`** (automation nodes).
2. Compare with the **live** HTML pages (links above). If live text differs from the cache, **refresh** and commit; the drift was stale cache, not necessarily a bug.
3. If live docs and Avrae **Discord** agree but **`avrae-ls`** or local Drac2 still misbehaves, suspect **avrae-ls** or the **local engine** version—file or ask in the appropriate project with a minimal repro.
4. If live Avrae (bot) disagrees with published docs, that may be an **Avrae** documentation or product bug upstream.
