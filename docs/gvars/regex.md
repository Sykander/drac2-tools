# regex

## Purpose

A **small regular-expression subset** for Drac2 where Python’s `re` module is unavailable. Patterns compile once to an internal **program** (opcode list); matching walks the text with tight loops so Avrae is less likely to hit **too many statements** than ad‑hoc character-by-character re-parsing of the pattern string.

This is **not** a full PCRE engine. Unsupported features include `|`, `^` / `$` as dedicated anchors (use `search_from` to scan), backreferences, and flags.

## Supported syntax

- **Literals** — any character not special; use `\\` to escape metacharacters.
- **`.`** — any single character (dotall-style for one code unit).
- **Classes** — `\d` `\D` `\w` `\W` `\s` `\S` (ASCII-style: `\w` is letters, digits, `_`; `\s` is space, tab, CR, LF).
- **Character classes** — `[...]` matches one character from the built set; `[^...]` matches one character **not** in the set. Inside a class you may use literals, `-` ranges that stay within **`a-z`**, **`A-Z`**, or **`0-9`**, and **only** `\d`, `\w`, or `\s` (they expand to small fixed sets). Use `[^0-9]` instead of `\D` inside brackets. An empty body `[]` is invalid; **`[^]`** with nothing after `^` matches any one character (negated empty set).
- **Quantifiers** — `?` (0–1), `*` (0+), `+` (1+), `{n}` (exactly `n`), `{n,}` (at least `n`), `{n,m}` (between `n` and `m`, greedy).
- **Groups** — `(...)` group a subpattern so quantifiers apply to the whole group (e.g. `(ab){2}`).

## Import

```drac2
using(regex = "<workshop-uuid-from-env>")
```

## Public API

### `compile_program(pat: str) -> list`

Parse `pat` into a program. Raises with `regex: ...` on syntax errors.

### `match_from(program, text: str, start: int = 0) -> int | None`

Try to match `program` against `text` beginning at `start`. Returns the **exclusive end index** on success, or `None` on failure.

### `full_match(program, text: str) -> bool`

`True` iff the whole string matches (same as `match_from` from `0` ending at `len(text)`).

### `search_from(program, text: str) -> dict | None`

Left‑to‑right scan: returns `{"start": i, "end": j}` for the first match, or `None`.

## Performance notes

Compile **once** per static pattern (e.g. at alias load or in a gvar constant), then reuse the program for many strings. Avoid recompiling inside a tight loop over long inputs.
