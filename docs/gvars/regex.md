# regex

## Purpose

A **small regular-expression subset** for Drac2 where Python’s `re` module is unavailable. Call **`compile()`** once, then reuse the returned matchers; the engine is tuned so Avrae is less likely to hit **too many statements** than ad‑hoc re-parsing of the pattern on every check.

This is **not** a full PCRE engine. **`|`** is **alternation** at the same parenthesis level (e.g. `ab|cd` is `(ab)|(cd)`). Use **`\|`** for a literal pipe outside a character class. **`^`** and **`$`** are **string** anchors only: **`^`** matches only at **index 0** of the haystack; **`$`** only when the current index equals **end of string** (no multiline / **`re.M`** flags). Plain **`$`** is always the end anchor—use **`\$`** for a literal dollar sign. Plain **`^`** outside a class is the start anchor—use **`\^`** for a literal caret. Unsupported: **backreferences** to captures, **`(?P<name>…)`** named captures, and flags.

**Quantifiers (minimal backtracking):** each `?`, `*`, `+`, and `{…}` repetition tries a **greedy** count first, then **reduces** the count if the rest of the pattern fails—enough for cases like `(ha)?ha` on **`ha`**. **Alternation** tries each `|` arm in order when the rest of the pattern needs it. Catastrophic slowdown on pathological patterns is still possible (classic NFA backtracking behavior).

## Supported syntax

- **Literals** — any character not special; use `\\` to escape metacharacters.
- **`.`** — any single character (dotall-style for one code unit).
- **Classes** — `\d` `\D` `\w` `\W` `\s` `\S` (ASCII-style: `\w` is letters, digits, `_`; `\s` is space, tab, CR, LF).
- **Character classes** — `[...]` matches one character from the built set; `[^...]` matches one character **not** in the set. Inside a class you may use literals, `-` ranges that stay within **`a-z`**, **`A-Z`**, or **`0-9`**, and **only** `\d`, `\w`, or `\s` (they expand to small fixed sets). Use `[^0-9]` instead of `\D` inside brackets. An empty body `[]` is invalid; **`[^]`** with nothing after `^` matches any one character (negated empty set). A literal **`]`** inside the class must be written **`[\]]`**. ECMAScript’s spelling **`[^]]`** (first `]` closes the class) is **not** accepted here; write **`[^\]]`** instead when you need “any one character except **`]`**”.
- **Quantifiers** — `?` (0–1), `*` (0+), `+` (1+), `{n}` (exactly `n`), `{n,}` (at least `n`), `{n,m}` (between `n` and `m`, greedy).
- **Groups** — `(...)` is a **capturing** group (see **`compile()`**’s **`match_from_captures`** / **`search_captures`** callables). **`(?:...)`** groups without capturing (does not consume a group index). Quantifiers apply to the whole parenthesized unit (e.g. `(ab){2}`).
- **Alternation** — `|` splits alternatives among concatenations at the same depth; first successful arm wins, then matching continues with the rest of the pattern. Nested parentheses create nested alternation scopes. Inside `[...]`, `|` is a normal class character unless you escape it for clarity.
- **Anchors** — **`^`** (start of string) and **`$`** (end of string). They are **zero-width** and **cannot** take **`?` `*` `+` `{…}`**. Inside **`[...]`**, **`^`** at the first position after **`[`** still means **negated class** only; elsewhere in the class **`^`** is a literal class member (e.g. **`[^^]`** is “any character except **`^`**”).

## Import

```drac2
using(regex = "1bfe2ba2-6d6e-468e-9555-0e6490ff8d4b")
```

## Public API

### `compile(pat: str) -> dict`

**Primary entrypoint.** Normalizes the pattern (see below), parses it, and returns a **dict** modeled on **`re.Pattern`**: keys **`pattern`** and **`groups`**, plus callables **`fullmatch`**, **`match`**, **`search`**, and helpers in the table. Drac2 has no **`Match`** objects, so results are **`bool`**, **`int \| None`**, or small **`dict`** / **`None`**.

**Normalization** (applied before parsing):

- Optional prefix **`re:`** is stripped.
- If the string **starts and ends with `/`**, those slashes are stripped (body only; no flags suffix).

Parse failures use the same **`regex: …`** errors as **`compile()`** / **`diagnostic_compile`**; when a pattern index is reported, it is **0-based** into the **normalized** string (after the rules above), not the original literal you typed if it was transformed.

The returned dict only has **`pattern`**, **`groups`**, and the callables—heavy state is held inside those functions, not as extra dict keys.

| Key | Type | Role |
|-----|------|------|
| **`pattern`** | `str` | Normalized pattern string (like **`re.Pattern.pattern`**). |
| **`groups`** | `int` | Capturing **`(`** count, excluding **`(?:…)`** (like **`re.Pattern.groups`**). |
| **`fullmatch`** | `(text, pos=0, endpos=None) -> bool` | Whole-string match from **`pos`** (like **`re.Pattern.fullmatch`**; **`endpos`** accepted but ignored). |
| **`full_match`** | same as **`fullmatch`** | Snake-case alias on the dict (mirrors the **`full_match`** callable name). |
| **`match`** | `(text, pos=0, endpos=None) -> int \| None` | Match anchored at **`pos`**; exclusive end index or **`None`** (like **`re.Pattern.match`** span end; **`endpos`** ignored). |
| **`search`** | `(text, pos=0, endpos=None) -> dict \| None` | First match with **`start >= pos`**; **`{"start", "end"}`** or **`None`** (**`endpos`** ignored). |
| **`match_from`** | `(text, start=0) -> int \| None` | Match from **`start`**; exclusive end index or **`None`**. |
| **`match_from_captures`** | `(text, start=0) -> dict \| None` | Match from **`start`** with capture **`groups`** list (see below). |
| **`search_captures`** | `(text, pos=0, endpos=None) -> dict \| None` | Like **`search`**, plus **`groups`** (same layout as **`match_from_captures`**). |

### `diagnostic_compile(pat: str)`

Drac2 does not support **`except … as`**, so catching parse errors cleanly is awkward. **`diagnostic_compile`** returns **`(None, pattern_dict)`** on success (same shape as **`compile(pat)`**) or **`(error_tuple, None)`** on failure—including invalid inputs such as **`pattern is None`**. Error indices use the same **normalized** pattern as **`compile()`**.

**Diagnostics** (no `except` binding):

```drac2
err, rx = regex.diagnostic_compile(maybe_pat)
if err != None:
    # err[0] message, err[1] index or None
    ...
```

**Note:** the compiled dict’s **`groups`** is an **integer** count. The **`groups`** key inside a **successful** **`match_from_captures`** / **`search_captures`** result is a **list** of capture strings (see below)—different meaning.

Capturing groups are numbered **`1 … rx.groups`** (same count as the dict’s **`groups`** field) in source order (left to right by opening `(`). On success, **`match_from_captures`** / **`search_captures`** return **`{"end": …, "groups": g}`** (and **`search_captures`** also **`start`**) where **`g[0]`** is the full matched substring for that attempt and **`g[i]`** is group **`i`** or **`None`** if that group did not participate (e.g. optional branch unused). There is no **`\1`** in patterns—only extraction via these APIs.

## Performance notes

Compile **once** per static pattern (e.g. at alias load or in a gvar constant), then reuse the returned callables for many strings. Avoid recompiling inside a tight loop over long inputs.

**`compile()`** builds the opcode program and search hints (whether every top-level arm forces start index ``0``, plus the optional first-character prefilter) **once** per cache miss and keeps both in function closures—**not** as keys on the returned dict—so repeated **`rx.search`** does not rebuild that map.

## Limits and scale (Avrae)

Avrae runs Drac2 under a **per-invocation execution budget** (“too many statements”). This library does not call native `re`; every match is interpreted in Drac2/Python, so **cost grows with pattern complexity, text length, and how often you retry from a new offset**.

Rough guidance (exact thresholds vary by pattern, other code in the same alias, and Avrae version):

| Concern | What to expect |
|--------|----------------|
| **`search`** / **`search_captures`** | Tries the pattern from **each** start index until something matches. Cost scales with **haystack length ×** work per attempt. Long buffers (order of **many hundreds of characters** of “boring” prefix before a hit, or more) can exhaust the budget faster than a single **`full_match`** on a string of similar size. Prefer anchoring with **`match`** / **`match_from`** when you know where matching should start, or narrow the haystack before regex. If **every** top-level alternation arm begins with **`^`**, the implementation only considers start index **`0`** (and returns **`None`** from **`search*`** when **`pos > 0`**). |
| **`full_match` / `match`** | A **single** pass from a known index is usually cheaper than scanning the whole string. Braced repeats and classes in the **low hundreds** of code units per match are often fine; **thousands** of code units can still work for simple programs (e.g. `.*`, `\d{n}`), but keep an eye on budget if the alias does other heavy work in the same run. |
| **Deeply nested `(` … `)`** | Each nesting level uses **stack** in the matcher. **Many dozen** levels of purely nested groups can hit **maximum recursion depth** (failure before the statement cap). Flatten or simplify nesting if you need a lot of wrappers. |
| **Alternation and `full_match`** | Arms are tried **in order**. If an earlier arm matches the **beginning** of the text but not the **whole** string, and nothing follows that alternation in the pattern, **`full_match` still fails**—there is no automatic “try a longer arm” pass. Design alternatives so they are not **strict prefixes** of each other (e.g. fixed-width codes `a00`, `a01`, …), or put shared prefixes **outside** the alternation. |
| **Pathological backtracking** | Patterns such as nested quantifiers with overlapping choices (classic example: `(a+)+` against long runs of `a`) can blow up **time** and the statement budget. Avoid that shape on user-controlled or very long input. |
