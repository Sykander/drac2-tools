# strings

## Purpose

A helper library for reusable string formatting: readable lists, ordinals, replace helpers, and a string type check.

## Import

```drac2
using(strings = "58d3892c-170c-4f7a-95a2-8a5d4fb50b0d")
```

## Public API

### `get_readable_list(items: list[str], delim: str = ", ", final_delim: str = " and ") -> str`

Formats empty, single-item, and multi-item lists for natural language (for example `a, b and c`).

### `get_ordinal_index(index: int) -> str`

Returns ordinal text (`1st`, `2nd`, `3rd`, with `11th`–`13th` handled as exceptions).

### `replace_all(given_string: str, search: str, replace: str) -> str`

Replaces every occurrence of `search` with `replace` via split and join.

### `replace(given_string: str, search: str, replace: str) -> str`

Replaces the first occurrence of `search` with `replace`; if `search` appears more than once, behavior follows the implementation in `strings.gvar`.

### `is_str(maybe_str) -> bool`

Returns `True` if `maybe_str == str(maybe_str)`, otherwise `False`.
