# bags

## Purpose

A helper library designed for interacting with the [bags workshop](https://avrae.io/dashboard/workshop/6296b723c964982e890e5315).

It allows you to check a characters bags as well as modify the contents

## Import

```drac2
using(bags = "38756442-20f6-4773-ab67-340895f79224")
```

## Public API

### `get_bags(char=None) -> list[Tuple[str, dict]]`

Returns the full bag list for the character (default: active character). Each entry is a pair of bag name and contents mapping.

### `set_bags(bags: list[Tuple[str, dict]], char=None) -> None`

Replaces the entire bag list and persists it to the character `bags` cvar.

### `get_bag(bag_name: str, char=None) -> dict`

Returns the contents dict for a named bag, or `{}` if the bag does not exist.

### `set_bag(bag_name: str, bag_contents: dict, char=None) -> None`

Creates or updates a single bag’s contents and persists.

### `modify_bag(item: str, count: int | None = None, bag: str | None = None, char=None) -> Tuple[bool, str]`

High-level add/remove for one item.

- `item`: item name.
- `count`: amount to add (positive) or remove (negative); defaults to `1`.
- `bag`: bag name; defaults to `"Equipment"`.
- `char`: defaults to active character.

Returns `(did_update, message)`. If the new count would be negative, returns `(False, explanation)` and does not write.
