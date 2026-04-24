# notes

## Purpose

A helper library designed for interacting with the [notes workshop](https://avrae.io/dashboard/workshop/6342ac449fb55be1a501367c).

It stores named notebooks per character: a registry maps notebook names to cvar keys, and each notebook is a JSON list of strings. Use `push` when you only need to append a line.

Every function accepts optional **`char`**. Pass **`None`** (the default) to use the **active** Avrae character; pass an explicit sheet to read or write another character’s cvars. If neither is available, functions **`err`** with a clear message.

## Import

```drac2
using(notes = "b0a504fa-568a-44ca-a899-807660980ee5")
```

## Public API

### `get_notebooks_dict(char=None)`

Returns the notebook name → id map loaded from the `notes` cvar (JSON object).

### `set_notebooks_dict(contents, char=None) -> None`

Replaces the entire map and saves it to the `notes` cvar.

### `get_notebook_id(notebook, char=None) -> str`

Returns the cvar key for `notebook`, defaulting to `"note_" + notebook` when unmapped.

### `set_notebook_id(notebook, notebook_id, char=None) -> None`

Registers `notebook_id` as the storage key for `notebook`.

### `get_notebook(notebook, char=None) -> list`

Returns the notebook contents as a list (default empty list JSON when unset).

### `set_notebook(notebook, contents, char=None) -> None`

Replaces the notebook contents entirely.

### `create_notebook(notebook, contents=[], char=None) -> None`

Ensures the notebook id is registered, then sets contents.

### `push(notebook: str, note: str, char=None) -> list[str]`

Appends `note`, persists, and returns the updated notebook.
