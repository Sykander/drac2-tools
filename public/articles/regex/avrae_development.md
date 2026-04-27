# regex gvar

Drac2 can’t use Python’s `re`. For most use cases this gvar can fill that role: import it as **`re`**, **`re.compile(pattern)`** to make a matcher, then reuse it like Python’s **`re`**.

## Supported Patterns

- **Literals** and **`\` escapes** (backslash before specials when you need them literally).
- **`.`** — any single character.
- **Shorthand classes** — `\d` `\D` `\w` `\W` `\s` `\S` (ASCII-style).
- **Character classes** — `[...]` / `[^...]`, ranges like `a-z`. Inside `[]`, use e.g. **`[^0-9]`** instead of `\D`-style shorthands.
- **Quantifiers** — `?` `*` `+` and `{n}` `{n,}` `{n,m}` (greedy).
- **Grouping** — capturing **`(...)`**, non-capturing **`(?:...)`**; quantifiers apply to the whole group.
- **Alternation** — **`|`** at the same nesting level.
- **Anchors** — **`^`** start of string, **`$`** end of string.
- Optional **`/…/`** — outer slashes stripped before parse.

### Example

```py
using(re = "1bfe2ba2-6d6e-468e-9555-0e6490ff8d4b")
rx = re.compile(r"\d{3}-\d{4}")
rx.full_match("555-1212")
hit = rx.search("call 555-1212")
rx2 = re.compile(r"(\d+)-(\d+)")
m = rx2.match_from_captures("12-34", 0)
```

## Top-level

- **`re.compile(pat)`** → **matcher** dict on success; bad pattern raises `regex:` errors.
- **`re.diagnostic_compile(pat)`** → **`(None, matcher)`** or on an error **`((msg, idx), None)`**.

## On the matcher

- **`pattern`** **`str`** — normalized pattern string.

- **`groups`** **`int`** — capturing **`(`** count (**`(?:…)`** excluded).

- **`full_match`** / **`fullmatch`** — **`(text, pos=0)`** → **`bool`**.

- **`match`** — **`(text, pos=0)`** → end or **`None`**.

- **`search`** — **`(text, pos=0)`** → **`None`** or **`{start, end}`**.

- **`search_captures`** — **`(text, pos=0)`** → **`None`** or **`{start, end}`** plus **`groups`** ([0] full, [1]…).

- **`match_from`** — **`(text, start=0)`** → end or **`None`**.

- **`match_from_captures`** — **`(text, start=0)`** → **`None`** or **`{end, groups}`**.
