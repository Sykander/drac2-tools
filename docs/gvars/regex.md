# regex

## Purpose

A **small regular-expression subset** for Drac2 where Python’s `re` module is unavailable. Patterns compile once to an internal **program** (opcode list); matching walks the text with tight loops so Avrae is less likely to hit **too many statements** than ad‑hoc character-by-character re-parsing of the pattern string.

This is **not** a full PCRE engine. **`|`** is **alternation** at the same parenthesis level (e.g. `ab|cd` is `(ab)|(cd)`). Use **`\|`** for a literal pipe outside a character class. Unsupported: `^` / `$` as **anchors** (a literal `$` is still just a character), **backreferences** to captures, **`(?P<name>…)`** named captures, and flags.

**Quantifiers (minimal backtracking):** each `?`, `*`, `+`, and `{…}` repetition tries a **greedy** count first, then **reduces** the count if the rest of the pattern fails—enough for cases like `(ha)?ha` on **`ha`**. **Alternation** tries each `|` arm in order when the rest of the pattern needs it. Catastrophic slowdown on pathological patterns is still possible (classic NFA backtracking behavior).

## Supported syntax

- **Literals** — any character not special; use `\\` to escape metacharacters.
- **`.`** — any single character (dotall-style for one code unit).
- **Classes** — `\d` `\D` `\w` `\W` `\s` `\S` (ASCII-style: `\w` is letters, digits, `_`; `\s` is space, tab, CR, LF).
- **Character classes** — `[...]` matches one character from the built set; `[^...]` matches one character **not** in the set. Inside a class you may use literals, `-` ranges that stay within **`a-z`**, **`A-Z`**, or **`0-9`**, and **only** `\d`, `\w`, or `\s` (they expand to small fixed sets). Use `[^0-9]` instead of `\D` inside brackets. An empty body `[]` is invalid; **`[^]`** with nothing after `^` matches any one character (negated empty set).
- **Quantifiers** — `?` (0–1), `*` (0+), `+` (1+), `{n}` (exactly `n`), `{n,}` (at least `n`), `{n,m}` (between `n` and `m`, greedy).
- **Groups** — `(...)` is a **capturing** group (see **`match_from_captures`** / **`search_captures`**). **`(?:...)`** groups without capturing (does not consume a group index). Quantifiers apply to the whole parenthesized unit (e.g. `(ab){2}`).
- **Alternation** — `|` splits alternatives among concatenations at the same depth; first successful arm wins, then matching continues with the rest of the pattern. Nested parentheses create nested alternation scopes. Inside `[...]`, `|` is a normal class character unless you escape it for clarity.

## Import

```drac2
using(regex = "<workshop-uuid-from-env>")
```

## Public API

### `compile(pat: str) -> dict`

Normalizes the pattern string (same rules as **`compile_program`**), parses it, and returns a **dict** modeled on **`re.Pattern`**: keys **`pattern`** and **`groups`**, and methods **`fullmatch`**, **`match`**, and **`search`** (plus helpers below). Drac2 has no real **`Match`** objects, so callables return **`bool`**, **`int \| None`**, or **`dict \| None`** instead of CPython’s rich types.

- Optional prefix **`re:`** is stripped (handy when copying patterns from file-based fixtures that mimic that convention).
- If the string **starts and ends with `/`**, those slashes are stripped (body only; no flags suffix).

| Key | Type | Role |
|-----|------|------|
| **`pattern`** | `str` | Normalized pattern string (like **`re.Pattern.pattern`**). |
| **`groups`** | `int` | Capturing **`(`** count, excluding **`(?:…)`** (like **`re.Pattern.groups`**). |
| **`fullmatch`** | `(text, pos=0, endpos=None) -> bool` | Whole-string match from **`pos`** (like **`re.Pattern.fullmatch`**; **`endpos`** accepted but ignored). |
| **`full_match`** | same as **`fullmatch`** | Snake-case alias kept for consistency with module **`full_match`**. |
| **`match`** | `(text, pos=0, endpos=None) -> int \| None` | Match anchored at **`pos`**; exclusive end index or **`None`** (like **`re.Pattern.match`** span end; **`endpos`** ignored). |
| **`search`** | `(text, pos=0, endpos=None) -> dict \| None` | First match with **`start >= pos`**; **`{"start", "end"}`** or **`None`** (**`endpos`** ignored). |
| **`match_from`** | `(text, start=0) -> int \| None` | Same as module **`match_from`** on this **`program`**. |
| **`match_from_captures`** | `(text, start=0) -> dict \| None` | Same as module **`match_from_captures`**. |
| **`search_captures`** | `(text, pos=0, endpos=None) -> dict \| None` | Same as module **`search_from_captures`** with optional **`pos`**. |
| **`program`** | `list` | Opcode list for low-level calls. |

Example:

```drac2
rx = regex.compile("/\\d{3}-\\d{4}/")
rx.fullmatch("555-1212")
hit = rx.search("call 555-1212 today")
# hit.start, hit.end
```

Use **`compile_program`** when you build the pattern string yourself and want the raw **`list`** without going through the wrapper.

**Note:** the compiled dict’s **`groups`** is an **integer** count. The **`groups`** key inside a **successful** **`match_from_captures`** / **`search_captures`** / **`search_from_captures`** result is a **list** of capture strings (see below)—different meaning.

Capturing groups are numbered **`1 … group_count(program)`** in source order (left to right by opening `(`). On success, **`match_from_captures`** / **`search_captures`** return **`{"end": …, "groups": g}`** (and **`search_captures`** / **`search_from_captures`** also **`start`**) where **`g[0]`** is the full matched substring for that attempt and **`g[i]`** is group **`i`** or **`None`** if that group did not participate (e.g. optional branch unused). There is no **`\1`** in patterns—only extraction via these APIs.

### `compile_program(pat: str) -> list`

Parse `pat` into a program. Raises with `regex: ...` on syntax errors.

### `match_from(program, text: str, start: int = 0) -> int | None`

Try to match `program` against `text` beginning at `start`. Returns the **exclusive end index** on success, or `None` on failure.

### `full_match(program, text: str, pos: int = 0) -> bool`

`True` iff the suffix **`text[pos:]`** is matched in full (exclusive end equals **`len(text)`**).

### `search_from(program, text: str, pos: int = 0) -> dict | None`

Left‑to‑right scan from **`pos`**: returns **`{"start": i, "end": j}`** for the first match, or **`None`**.

### `match_from_captures(program, text: str, start: int = 0) -> dict | None`

Returns **`None`** on failure. On success: **`{"end": exclusive_index, "groups": list}`** with **`groups`** as described above (**`groups[0]`** is **`text[start:end]`**).

### `search_from_captures(program, text: str, pos: int = 0) -> dict | None`

Returns **`None`** or **`{"start", "end", "groups"}`** with the same **`groups`** list layout as **`match_from_captures`**, scanning from **`pos`**.

### `group_count(program: list) -> int`

Largest capturing group index (same count idea as Python’s pattern group count). **`0`** if there are no **`(`** captures.

## Performance notes

Compile **once** per static pattern (e.g. at alias load or in a gvar constant), then reuse the program for many strings. Avoid recompiling inside a tight loop over long inputs.

## Limits and scale (Avrae)

Avrae runs Drac2 under a **per-invocation execution budget** (“too many statements”). This library does not call native `re`; every match is interpreted in Drac2/Python, so **cost grows with pattern complexity, text length, and how often you retry from a new offset**.

Rough guidance (exact thresholds vary by pattern, other code in the same alias, and Avrae version):

| Concern | What to expect |
|--------|----------------|
| **`search` / `search_from`** | Tries the pattern from **each** start index until something matches. Cost scales with **haystack length ×** work per attempt. Long buffers (order of **many hundreds of characters** of “boring” prefix before a hit, or more) can exhaust the budget faster than a single **`full_match`** on a string of similar size. Prefer anchoring with **`match_from`** when you know where matching should start, or narrow the haystack before regex. |
| **`full_match` / `match_from`** | A **single** pass from a known index is usually cheaper than scanning the whole string. Braced repeats and classes in the **low hundreds** of code units per match are often fine; **thousands** of code units can still work for simple programs (e.g. `.*`, `\d{n}`), but keep an eye on budget if the alias does other heavy work in the same run. |
| **Deeply nested `(` … `)`** | Each nesting level uses **stack** in the matcher. **Many dozen** levels of purely nested groups can hit **maximum recursion depth** (failure before the statement cap). Flatten or simplify nesting if you need a lot of wrappers. |
| **Alternation and `full_match`** | Arms are tried **in order**. If an earlier arm matches the **beginning** of the text but not the **whole** string, and nothing follows that alternation in the pattern, **`full_match` still fails**—there is no automatic “try a longer arm” pass. Design alternatives so they are not **strict prefixes** of each other (e.g. fixed-width codes `a00`, `a01`, …), or put shared prefixes **outside** the alternation. |
| **Pathological backtracking** | Patterns such as nested quantifiers with overlapping choices (classic example: `(a+)+` against long runs of `a`) can blow up **time** and the statement budget. Avoid that shape on user-controlled or very long input. |
