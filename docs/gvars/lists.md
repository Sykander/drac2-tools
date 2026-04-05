# lists

## Purpose

A helper library for list utilities: indexing lists of objects by key, sampling random distinct elements, type checks, and search helpers.

It uses the `random` gvar for `get_random_from_list`.

## Import

```drac2
using(lists = "be56beeb-512b-4cc3-93e3-e3b9a8d2b70c")
```

## Public API

### `to_dict(items: list, key: string) -> dict`

Builds `{ item[key]: item, … }`. Raises if an item lacks `key`. Duplicate keys keep the last item.

### `get_random_from_list(items: list, count=1) -> list`

Returns up to `count` distinct elements chosen at random without replacement. Returns `[]` when `count == 0`. Raises when `count` is negative, greater than `len(items)`, or when `items` is empty and `count` is positive.

### `is_list(maybe_list) -> bool`

Returns `True` if `maybe_list == list(maybe_list)`, otherwise `False`.

### `search_list(items: list, search: str) -> list`

Exact matches win; otherwise returns items whose string form contains `search` as a case-insensitive substring.

### `search_list_by_key(items: list[dict], key: str, search: str) -> list[dict]`

Same matching rules as `search_list`, but compares `item[key]`. Raises if an item lacks `key`.
