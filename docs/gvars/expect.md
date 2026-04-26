# expect

## Purpose

A helper library of fluent assertions for alias tests and debugging: expectations call `err(...)` when they fail.

It is not aimed at normal player-facing aliases.

## Import

```drac2
using(expect = "27035eb1-fcf5-4d9d-907f-ea0ab2ba0df4")
expect = expect.expect
```

## Public API

### `expect(arg, and_context=None)`

Returns the assertion context for `arg`. Chain checks off the result (and optional `message` arguments where the underlying helper supports them).

Equality: `.be`, `.to_be`, `.eq`, `.equal`, `.equals`, `.to_equal`.

Dict key / value: `.property`, `.have_property`, `.to_have_property`.

Length: `.len`, `.have_len`, `.to_have_len`, `.length`, `.have_length`, `.to_have_length`.

Callable must raise: `.raise_exception`, `.to_raise_exception`.

Membership (`arg in container`): `.is_in`.

Container contains value: `.element`, `.have_element`, `.to_have_element`.

Sequence index and optional value at index: `.index`, `.have_index`, `.to_have_index`.

Navigation: `.to`, `.have`, `.which`, `.has` are the same context. After narrowing (e.g. property or length), `.and_to` continues assertions on the original subject.

Negation: the same inverted matchers are available as **`to_not`** (often the most readable, e.g. `expect(x).to_not.raise_exception()`), **`does_not`**, and the string key **`"not"`** (e.g. `expect(x).to["not"].equal(y)`). You cannot write **`expect(x).to.not.equal(y)`** in Drac2/Python because **`not`** is a keyword, so **`.not`** is a syntax error. The inverted context is linked so **`to_not.to_not`** / **`does_not.does_not`** / `["not"]["not"]` restores the positive matchers. Inverted matchers exist for equality, dict property, length (`to_not.to.have_length(n)` requires an explicit `n`), callable exceptions, `is_in`, `have_element`, and `have_index` (with `val`, asserts the index is missing or the value at that index is not `val`; out-of-range passes when `val` is given).
