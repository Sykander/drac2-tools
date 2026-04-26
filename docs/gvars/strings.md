# strings

## Purpose

A helper library for reusable string formatting: readable lists, numeric ordinals (digits and words), replace helpers, and a string type check.

## Import

```drac2
using(strings = "58d3892c-170c-4f7a-95a2-8a5d4fb50b0d")
```

## Public API

### `get_readable_list(items: list[str], delim: str = ", ", final_delim: str = " and ") -> str`

Formats empty, single-item, and multi-item lists for natural language (for example `a, b and c`).

### `get_ordinal_index(index: int) -> str`

Returns ordinal text (`1st`, `2nd`, `3rd`, with `11th`–`13th` handled as exceptions).

### `get_cardinal_text(n: int) -> str`

Spells a non-negative integer in words as a cardinal (for example `193` → `One Hundred and Ninety Three`). `0` is `Zero`. Values must be `n >= 0` and below `10^15` (trillion scale); otherwise `err()` is raised.

### `get_ordinal_text(n: int) -> str`

Spells a non-negative integer in words as an ordinal (for example `193` → `One Hundred and Ninety Third`). `0` is `Zeroth`. Uses the same “hundred and …” style as `get_cardinal_text` for the sub-thousand part. For larger numbers, higher thousand-chunks are cardinal and the lowest non-zero chunk carries the ordinal (for example `1000001` → `One Million First`, `1000` → `One Thousandth`). Out of range values raise `err()` like `get_cardinal_text`.

### `replace_all(given_string: str, search: str, replace: str) -> str`

Replaces every occurrence of `search` with `replace` via split and join.

### `replace(given_string: str, search: str, replace: str) -> str`

Replaces the first occurrence of `search` with `replace`; if `search` appears more than once, behavior follows the implementation in `strings.gvar`.

### `is_str(maybe_str) -> bool`

Returns `True` if `maybe_str == str(maybe_str)`, otherwise `False`.
