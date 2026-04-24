# tools

## Purpose

A helper library for resolving D&D 5e tool and instrument names against a built-in list and reading proficiency or expertise from character cvars (`pTools`, `eTools`).

It uses `lists.search_list` for fuzzy matching.

`get_has_proficiency` and `get_has_expertise` take optional **`char`**: pass **`None`** for the active character, or pass an explicit sheet.

## Import

```drac2
using(tools = "254cb78d-e9ae-4b03-afc5-d2cbc93bb27e")
```

## Public API

### `search_for_tool(toolname) -> list`

Returns matches from the canonical `tools_list` via `lists.search_list` (exact match preferred, then case-insensitive substring).

### `get_has_proficiency(toolname: str, char=None) -> bool`

`True` when `toolname` is a known tool and appears in either proficiency or expertise cvars.

### `get_has_expertise(toolname: str, char=None) -> bool`

`True` when `toolname` is a known tool and appears in the expertise cvar.
