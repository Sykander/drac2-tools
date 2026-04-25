# regex

## Purpose

A **small regular-expression subset** for Drac2 where Python’s `re` module is unavailable. Patterns compile once to an internal **program** (opcode list); matching walks the text with tight loops so Avrae is less likely to hit **too many statements** than ad‑hoc character-by-character re-parsing of the pattern string.

This is **not** a full PCRE engine. Unsupported features include `|` as **alternation** (a literal `|` still matches itself), `^` / `$` as **anchors** (a literal `$` is just a character), backreferences, and flags.

**Quantifiers (minimal backtracking):** each `?`, `*`, `+`, and `{…}` repetition tries a **greedy** count first, then **reduces** the count if the rest of the pattern fails—enough for cases like `(ha)?ha` on **`ha`**. There is still **no** `|` branch backtracking; catastrophic slowdown on pathological patterns is possible (same as naive regex engines).

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

### `compile(pat: str) -> dict` and `pattern(pat: str) -> dict`

Same function under two names (Python **`re.compile`** style). Normalizes the pattern string, then parses it:

- Optional prefix **`re:`** (same convention as avrae-ls regex expectations) is stripped.
- If the string **starts and ends with `/`**, those slashes are stripped so you can write **`/body/`** like a JavaScript regex literal (only the simple `.../.../` form; no `/foo/bar/` flags suffix).

Returns a **dict** (treat it as an opaque pattern object) with:

| Key | Type | Role |
|-----|------|------|
| **`full_match`** | `(text: str) -> bool` | Whole-string match (Python **`re.fullmatch`**). |
| **`test`** | `(text: str) -> bool` | Same as **`full_match`**. |
| **`search`** | `(text: str) -> dict \| None` | First match anywhere; `{"start", "end"}` or `None`. |
| **`exec`** | `(text: str) -> dict \| None` | Same as **`search`** (name mirrors JS **`RegExp.prototype.exec`** for the first hit). |
| **`match_from`** | `(text: str, start: int = 0) -> int \| None` | Match anchored at `start`; exclusive end index or `None`. |
| **`program`** | `list` | Cached program for the low-level API below. |

Example:

```drac2
rx = regex.compile("/\\d{3}-\\d{4}/")
rx["full_match"]("555-1212")
hit = rx["search"]("call 555-1212 today")
# hit["start"], hit["end"]
```

Use **`compile_program`** when you build the pattern string yourself and want the raw **`list`** without going through the wrapper.

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
