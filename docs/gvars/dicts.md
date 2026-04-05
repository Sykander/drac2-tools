# dicts

## Purpose

A small helper library for checking whether a value behaves like a plain dict.

It is useful for validation or branching before you treat something as a mapping.

## Import

```drac2
using(dicts = "9ce4d5ba-9dc2-45b0-938d-ab434f6f70ad")
```

## Public API

### `is_dict(maybe_dict) -> bool`

Returns `True` if `maybe_dict == dict(maybe_dict)`, otherwise `False`.
