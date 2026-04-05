# notes

## Purpose

A helper library designed for interacting with the [notes workshop](https://avrae.io/dashboard/workshop/6342ac449fb55be1a501367c).

It stores named notebooks per character: a registry maps notebook names to cvar keys, and each notebook is a JSON list of strings. Use `push` when you only need to append a line.

## Import

```drac2
using(notes = "b0a504fa-568a-44ca-a899-807660980ee5")
```

## Public API

### `get_notebooks_dict(char=char)`

Returns the notebook name → id map loaded from the `notes` cvar (JSON object).

### `set_notebooks_dict(contents, char=char) -> None`

Replaces the entire map and saves it to the `notes` cvar.

### `get_notebook_id(notebook, char=char) -> str`

Returns the cvar key for `notebook`, defaulting to `"note_" + notebook` when unmapped.

### `set_notebook_id(notebook, notebook_id, char=char) -> None`

Registers `notebook_id` as the storage key for `notebook`.

### `get_notebook(notebook, char=char) -> list`

Returns the notebook contents as a list (default empty list JSON when unset).

### `set_notebook(notebook, contents, char=char) -> None`

Replaces the notebook contents entirely.

### `create_notebook(notebook, contents=[], char=char) -> None`

Ensures the notebook id is registered, then sets contents.

### `push(notebook: str, note: str, char=char) -> list[str]`

Appends `note`, persists, and returns the updated notebook.
