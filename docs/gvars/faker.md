# faker

## Purpose

Plausibly shaped **random test data** for Drac2 / Avrae aliases and gvar unit tests: names, D&D-flavoured class and level, attacks, items, workshop-style UUID strings, lorem text, dice strings, and more.

The module keeps its own **xorshift** state (independent of the [`random`](random.md) gvar). Use **`set_seed`** / **`get_seed`** when you need **reproducible** sequences in tests.

## Import

Use the workshop `env` gvar id from your environment (see [`docs/README.md`](../README.md)); then:

```drac2
using(faker = env.gvars.faker)
```

## Public API

### Seeding

| Symbol | Role |
|--------|------|
| **`get_seed() -> int`** | Current PRNG state (after any call that advances it). |
| **`set_seed(n: int) -> None`** | Resets state to `n` (mod \(2^{31}\)). |
| **`rand_int(low: int, high: int) -> int`** | Inclusive integer in `[low, high]`; advances state. |

### Identifiers and web-shaped strings

| Symbol | Role |
|--------|------|
| **`gvar_id() -> str`** | Random hex UUID-style id with four hyphens (36 characters), like workshop gvar ids. |
| **`workshop_id() -> str`** | Same as **`gvar_id`** (alias for readability in tests). |
| **`cvar_name() -> str`** | `test_cvar_` plus 8 random hex characters. |
| **`email() -> str`** | Two lorem “words” and a `.test` TLD, not real addresses. |
| **`url() -> str`** | `https://example.test/...` with random path segments. |
| **`tag() -> str`** | `#` plus a lorem word and 0–99. |
| **`discord_snowflake() -> str`** | 19 digit characters (padded with leading zeroes if needed), not a real Discord id. |

### People and D&D-flavoured labels

| Symbol | Role |
|--------|------|
| **`first_name() -> str`**, **`last_name() -> str`** | Picks from small built-in lists. |
| **`full_name() -> str`** | First and last separated by a space. |
| **`display_name() -> str`** | First name plus a random title phrase (`the Bold`, `of Northreach`, …). |
| **`age(min_age=8, max_age=80) -> int`** | Random age in the inclusive range. |
| **`race() -> str`**, **`background() -> str`** | Random entry from small lists. |
| **`dnd_class() -> str`**, **`class_name() -> str`** | Random class; **`class_name`** is an alias of **`dnd_class`**. |
| **`level() -> int`** | Random 1–20. |
| **`prof_bonus() -> int`** | Uses a **fresh** random **`level()`** internally and returns the corresponding PHB-style proficiency bonus. |

### Abilities, combat, and gear

| Symbol | Role |
|--------|------|
| **`ability_score() -> int`** | Random 3–18. |
| **`hp() -> int`**, **`armor_class() -> int`**, **`initiative() -> int`** | Random rough ranges (HP 5–200, AC 10–22, initiative -5 to 10). |
| **`save_kind() -> str`** | One of str/dex/con/int/wis/cha. |
| **`skill_name() -> str`** | One skill from a fixed list. |
| **`weapon_name() -> str`**, **`item_name() -> str`** | Random from small lists. |
| **`attack_name() -> str`** | Weapon + verb (e.g. `Longsword Cleave`). |
| **`feature_name() -> str`** | Two random word-chunks (e.g. `Improved Smite`, not a real 5e name). |
| **`spell_name() -> str`** | Fake name plus a random spell school in parentheses. |
| **`monster_name() -> str`** | Random descriptor + 1–9. |
| **`damage_type() -> str`** | Random damage type keyword. |
| **`size_category() -> str`** | One of Tiny … Gargantuan. |
| **`rest_kind() -> str`** | `short` or `long`. |
| **`coin_pouch() -> str`** | Like `47 gp` with random amount and D&D coin abbrev. |

### Text and numbers

| Symbol | Role |
|--------|------|
| **`lorem_word() -> str`**, **`lorem_words(count) -> str`**, **`sentence(word_count=5) -> str`** | Pseudo-Latin-ish tokens; **sentence** capitalizes the first character and appends `.`. |
| **`dice_notation() -> str`** | e.g. `2d6+3` with `n` 1–4, common sides, and mod 0–10. |
| **`integer(low=0, high=100) -> int`**, **`coin_flip() -> bool`** | Convenience wrappers over **`rand_int`**. |
| **`note_title() -> str`** | `Note` + number + em dash + capitalized lorem word. |
| **`one_of(items: list) -> str`** | Uniform random element (empty list returns `""`). |

## Performance

These helpers are for **tests and fixtures**, not hot paths. Avoid calling dozens of generators inside tight per-player command loops; compile static patterns when possible, as with other utils (see [regex](regex.md#performance-notes)).

## Limits

- Data is **not** balanced for gameplay or statistical realism; it only needs to “look” reasonable in tests.
- **No guarantee** of uniqueness across calls; use **seeds** or append counters if you need stable unique strings.
