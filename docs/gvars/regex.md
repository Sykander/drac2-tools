# regex

## What it is

Drac2 cannot import Python’s `re`. This module gives you a **small regex engine**: call **`compile(pattern)`** once, then use **`full_match`**, **`match`**, **`search`**, and related helpers on the returned object.

It is **not** full PCRE. For what you *can* write in a pattern, see [Supported syntax](#supported-syntax) at the bottom.

## Import

```drac2
using(regex = "1bfe2ba2-6d6e-468e-9555-0e6490ff8d4b")
```

## Using `compile()`

`compile` returns a dict-shaped matcher (like a stripped-down `re.Pattern`): **`pattern`**, **`groups`**, and callables such as **`full_match`** and **`search`**. Compile **once** (e.g. at load), then reuse.

You can pass the pattern as a **raw string** **`r"…"`** or **`r'…'`** (Python-style) so backslashes are mostly literal—e.g. **`r"\d+"`** is equivalent to **`"\\d+"`** and is often easier to read.

**Whole string:**

```drac2
rx = regex.compile("/\\d{3}-\\d{4}/")
rx.full_match("555-1212")  # True
rx.full_match("call 555-1212")  # False
```

**Optional slash delimiters** — if the pattern string starts and ends with `/`, those slashes are stripped before parsing (handy for “regex-looking” literals):

```drac2
rx = regex.compile("/\\d+/")
rx.full_match("42")  # True — same as compile("\\d+")
```

**First match anywhere:**

```drac2
rx = regex.compile("\\d{3}-\\d{4}")
hit = rx.search("call 555-1212 today")
# hit is None or a dict with .start and .end
```

**Captures** (groups are 1-based in the result list; index 0 is the full match):

```drac2
rx = regex.compile("(\\d+)-(\\d+)")
m = rx.match_from_captures("12-34", 0)
# m.groups[0] full match, m.groups[1] first group, etc.
```

## Reference patterns (`common-regexes`)

The test alias [`common-regexes.alias`](../../src/gvars/utils/regex/common-regexes.alias) pins **copy-paste patterns** for common shapes. Use them by passing the string to **`regex.compile(...)`** in your own gvar or alias (they are not shipped as separate named constants).

### Web and data validation

| For | Pattern |
|-----|---------|
| Practical email shape | `[-\\w.%+]+@[-\\w.]+\\.[A-Za-z]{2,}` |
| UUID v4 (hex, version nibble `4`) | `[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89aAbB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}` |
| `http` / `https` URL with host and optional path | `https?://[-\\w.]+(/[-\\w./?%&=+~]*)?` |
| IPv4 octets | `(?:25[0-5]\|2[0-4]\\d\|1\\d\\d\|[1-9]?\\d)(?:\\.(?:25[0-5]\|2[0-4]\\d\|1\\d\\d\|[1-9]?\\d)){3}` |
| ISO-like `YYYY-MM-DD` (shape only; not full calendar validation) | `\\d{4}-(0[1-9]\|1[0-2])-(0[1-9]\|[12]\\d\|3[01])` |
| Hex color, optional `#`, 3 or 6 hex digits | `#?([0-9a-fA-F]{6}\|[0-9a-fA-F]{3})` |
| Kebab-case slug | `[a-z0-9]+(-[a-z0-9]+)*` |
| US ZIP 5 or 5+4 | `\\d{5}(-\\d{4})?` |
| MAC address `aa:bb:...` | `([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}` |
| Avrae-style UUID (workshop / gvar ids, lowercase hex) | `[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}` |

### Avrae-oriented tokens

| For | Pattern |
|-----|---------|
| Single dice term (`2d20kh1`, `8d6ro<3-1`, …) | `\\d+d\\d+([kK][hHlL]\\d+)?([rR][oO]?[<>]?\\d+)?([+\\-]\\d+)?` |
| Several dice terms with optional flat modifier (`1d20+5`, `2d6+1d4+3`) | `\\d+d\\d+([kK][hHlL]\\d+)?([+\\-]\\d+d\\d+([kK][hHlL]\\d+)?)*([+\\-]\\d+)?` |
| Attack / save / check shorthand (`save`, `check:stealth`, …) | `(atk\|attack\|save\|check\|skill)(:[A-Za-z_]+)?` |
| Damage roll plus D&D damage type | `\\d+d\\d+([+\\-]\\d+)?\\s*(acid\|cold\|fire\|force\|lightning\|necrotic\|poison\|psychic\|radiant\|thunder\|bludgeoning\|piercing\|slashing)` |
| Single `-flag` token | `-[A-Za-z][A-Za-z0-9_]*` |
| Coin amount (`150 gp`, `3pp`) | `\\d+\\s*(cp\|sp\|ep\|gp\|pp)` |

### Discord mentions

| For | Pattern |
|-----|---------|
| User `<@…>` / `<@!…>` | `<@!?[0-9]{17,20}>` |
| Channel `<#…>` | `<#[0-9]{17,20}>` |
| Role `<@&…>` | `<@&[0-9]{17,20}>` |

**Example** (email pattern):

```drac2
rx = regex.compile("[-\\w.%+]+@[-\\w.]+\\.[A-Za-z]{2,}")
rx.full_match("user@example.com")
```

## API overview

| Member | Role |
|--------|------|
| **`pattern`** | Normalized pattern string. |
| **`groups`** | Count of capturing `(` groups (excluding `(?:…)`). |
| **`full_match`**, **`fullmatch`** | Whole-string match from `pos` → `bool`. |
| **`match`** | Match anchored at `pos` → exclusive end index or `None`. |
| **`search`** | First match from `pos` → `{"start", "end"}` or `None`. |
| **`match_from`** | Like `match` with `start`. |
| **`match_from_captures`**, **`search_captures`** | Same, plus `groups` list on success. |

Parse errors raise like other `compile` failures. To avoid `try`/`except` awkwardness in Drac2, use **`diagnostic_compile`** (returns `(None, rx)` or `(error_tuple, None)`).

```drac2
err, rx = regex.diagnostic_compile(maybe_pat)
if err != None:
    # err[0] message, err[1] index or None
    ...
```

On success, **`rx`** matches **`compile(pat)`**. Error indices are **0-based** in the **normalized** pattern (after optional `re:` strip and `/…/` trimming).

**Note:** the dict’s **`groups`** is an **integer** count. In a successful **`match_from_captures`** / **`search_captures`** result, **`groups`** is a **list** of capture strings (`[0]` = full match, `[1..]` = groups).

---

## Supported syntax

- **Literals** — any character not special; use `\\` to escape metacharacters.
- **`.`** — any single character (dotall-style for one code unit).
- **Classes** — `\d` `\D` `\w` `\W` `\s` `\S` (ASCII-style: `\w` is letters, digits, `_`; `\s` is space, tab, CR, LF).
- **Character classes** — `[...]` matches one character from the built set; `[^...]` matches one character **not** in the set. Inside a class you may use literals, `-` ranges that stay within **`a-z`**, **`A-Z`**, or **`0-9`**, and **only** `\d`, `\w`, or `\s` (they expand to small fixed sets). Use `[^0-9]` instead of `\D` inside brackets. An empty body `[]` is invalid; **`[^]`** with nothing after `^` matches any one character (negated empty set). A literal **`]`** inside the class must be written **`[\]]`**. ECMAScript’s spelling **`[^]]`** (first `]` closes the class) is **not** accepted here; write **`[^\]]`** instead when you need “any one character except **`]`**”.
- **Quantifiers** — `?` (0–1), `*` (0+), `+` (1+), `{n}` (exactly `n`), `{n,}` (at least `n`), `{n,m}` (between `n` and `m`, greedy).
- **Groups** — `(...)` is a **capturing** group (see **`match_from_captures`** / **`search_captures`**). **`(?:...)`** groups without capturing (does not consume a group index). Quantifiers apply to the whole parenthesized unit (e.g. `(ab){2}`).
- **Alternation** — `|` splits alternatives among concatenations at the same depth; first successful arm wins, then matching continues with the rest of the pattern. Nested parentheses create nested alternation scopes. Inside `[...]`, `|` is a normal class character unless you escape it for clarity.
- **Anchors** — **`^`** (start of string) and **`$`** (end of string). They are **zero-width** and **cannot** take **`?` `*` `+` `{…}`**. Inside **`[...]`**, **`^`** at the first position after **`[`** still means **negated class** only; elsewhere in the class **`^`** is a literal class member (e.g. **`[^^]`** is “any character except **`^`**”).

**Not supported:** backreferences to captures, **`(?P<name>…)`** named captures, and flags. **`|`** is alternation at the same parenthesis level (e.g. `ab|cd` is `(ab)|(cd)`). Use **`\|`** for a literal pipe outside a character class. **`^`** and **`$`** are **string** anchors only (no multiline / **`re.M`**). Plain **`$`** is always the end anchor—use **`\$`** for a literal dollar. Plain **`^`** outside a class is the start anchor—use **`\^`** for a literal caret.

**Quantifiers (minimal backtracking):** each `?`, `*`, `+`, and `{…}` repetition tries a **greedy** count first, then **reduces** the count if the rest of the pattern fails—enough for cases like `(ha)?ha` on **`ha`**. **Alternation** tries each `|` arm in order when the rest of the pattern needs it. Catastrophic slowdown on pathological patterns is still possible (classic NFA backtracking behavior).

## `compile(pat: str)` — details

**Normalization** (applied before parsing):

- Optional prefix **`re:`** is stripped.
- If the string **starts and ends with `/`**, those slashes are stripped (body only; no flags suffix).

Parse failures use **`regex: …`** errors; when a pattern index is reported, it is **0-based** into the **normalized** string, not necessarily the original literal you typed.

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
| **`match_from_captures`** | `(text, start=0) -> dict \| None` | Match from **`start`** with capture **`groups`** list. |
| **`search_captures`** | `(text, pos=0, endpos=None) -> dict \| None` | Like **`search`**, plus **`groups`** (same layout as **`match_from_captures`**). |

### `diagnostic_compile(pat: str)`

Returns **`(None, pattern_dict)`** on success (same shape as **`compile(pat)`**) or **`(error_tuple, None)`** on failure—including invalid inputs such as **`pattern is None`**. Error indices use the same **normalized** pattern as **`compile()`**.

Capturing groups are numbered **`1 … rx.groups`** in source order (left to right by opening `(`). On success, **`match_from_captures`** / **`search_captures`** return **`{"end": …, "groups": g}`** (and **`search_captures`** also **`start`**) where **`g[0]`** is the full matched substring for that attempt and **`g[i]`** is group **`i`** or **`None`** if that group did not participate. There is no **`\1`** in patterns—only extraction via these APIs.

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
