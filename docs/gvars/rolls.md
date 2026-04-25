# rolls

## Purpose

A helper library for building Avrae dice strings and labels for skills, saves, attacks, passive scores, and flat rolls, and for running them through `get_roll`.

Smaller helpers compose expressions (advantage, damage, joining fragments) and format display names when you are not using `get_roll` end-to-end.

## Import

```drac2
using(rolls = "b6fe8f32-72ee-4179-a5b2-6fe79c77f372")
```

## Supported public API

Only the functions in this section are considered a stable, supported surface for aliases and other gvars. Each one is covered by **`rolls.alias-test`** (with **`character`** / **`vars`** metadata where a mock sheet is required). Anything not listed here—including any **`_`**-prefixed name in `rolls.gvar`—is internal.

### `get_roll(character, roll_name, args: ParsedArguments, roll_type: str, ability_name: str | None = None, dc: int | None = None, adv: bool | None = None, bonuses: list[str] | None = None, arg_aliases: dict | None = None) -> dict`

Main entry point. `roll_type` is one of `"roll"`, `"check"`, `"passive"`, `"save"`, `"attack"`. For `"check"`, `"passive"`, `"save"`, and `"attack"`, `roll_name` is usually a skill or save key (or `"melee"` / `"ranged"` for attacks). When `roll_type == "roll"`, `roll_name` is the dice expression passed to `vroll`; it is normalized with `str()` first, so you can pass a string or another value (such as a number) that stringifies to valid dice syntax. `args` is parsed alias arguments (advantage flags, `-b`, `-guidance`, `-bless`, `-resistance`, ability overrides, etc.). `bonuses` is copied when provided so callers’ lists are not mutated.

For **`"check"`** and **`"passive"`**, `roll_name` is normalized with **`resolve_skill_input`** (substring match on sheet skill keys, case-insensitive, spaces removed). For **`"save"`**, use **`resolve_save_input`** (e.g. `dex` → `dexterity`); ambiguous partial names error.

Optional **`arg_aliases`** remaps argparse keys, e.g. `{"advantage": {"adv": "survAdv", "dis": "survDis"}, "b": "survBonus", "guidance": "survGuidance", "mc": "survMC"}`. Omitted entries keep defaults `adv`/`dis`, `b`, `guidance`, `mc`.

**Minimum d20 on checks:** `-mc <n>` sets the d20 minimum. Otherwise minimum **10** applies only when the skill is **proficient** (`skill.prof >= 1`) and the character either has Reliable Talent by level (`character_has_reliable_talent`) or the sheet csetting **`talent`** is true.

**Rerolls:** Halfling Lucky still uses `ro1` when applicable. If **`character.csettings["reroll"]`** is an integer, it is merged into the d20 reroll list (when `csettings` exists at runtime).

Pass **`None`** for `character` to use the **active** Avrae sheet when one exists (`resolve_character`). For `"check"`, `"passive"`, `"save"`, and `"attack"`, a sheet is **required** after resolution—if there is no active character and no explicit override, `get_roll` errors. For `"roll"`, a missing sheet is still allowed for the roll string itself; when `character` is `None` and there is no active character, race/feat helpers behave as if there were no sheet.

Returns a dict with `roll`, `total`, `full`, `name`, `roll_string`, `dc`, `passed`, `crit`, `crit_fail`, and **`natural_roll`** (first leaf of `roll.raw` when it can be coerced to `int`, else `None`; omitted meaning is `None` for `"passive"`). For **`"check"`**, **`"save"`**, **`"attack"`**, and **`"roll"`** expressions whose `roll_name` contains **`d20`**, **`crit`** / **`crit_fail`** follow **`natural_roll`**: `20` / `1` respectively; otherwise both are `False`. See `rolls.gvar`.

### `join_roll_strings(roll_strings: list[str]) -> str`

Joins roll fragments, inserting `+` between terms when needed; skips `None` and empty strings.

### `get_damage_roll(damage_dice: str, bonuses: list[str] | None = None) -> str`

Joins `damage_dice` with optional bonus strings.

### `get_d20(adv: bool | None = None, eadv: bool = False, mi: int | None = None, ma: int | None = None, ro: list[int] | None = None) -> str`

Builds the d20 portion (plain, advantage, disadvantage, elven accuracy, optional min/max and reroll snippets).

### `join_advantage(*advs) -> bool | None`

Combines multiple advantage flags into `True`, `False`, or `None` when both advantage and disadvantage appear.

### `get_readable_name_for_skill(skill_name, ability_name=None, is_passive=False) -> str`

Human-readable skill check label (including passive wording when `is_passive`).

### `get_readable_name_for_save(save_name, ability_name=None) -> str`

Human-readable saving throw label.

### `get_readable_name_for_attack(attack_type, ability_name) -> str`

Human-readable attack roll label.

### `get_default_ability_for_skill(skill_name: string) -> str | None`

Default ability for a skill key, or `None`.

### `get_default_ability_for_save(save_name: string) -> str | None`

Default ability for a save key, or `None`.

### `get_default_ability_for_attack_type(attack_type: string) -> str | None`

Default ability for `"melee"` or `"ranged"`, or `None`.

### `character_has_halfling_luck(character) -> bool`

### `resolve_skill_input(character, raw_name: str) -> str`

Requires a character. Returns the internal skill key from the first sheet skill whose key contains `raw_name` (case-insensitive, spaces stripped). Errors if nothing matches.

### `resolve_save_input(raw_name: str) -> str`

Returns a `save_abilities` key from a full or partial ability or special save name (`death`, `honor`, `sanity` when present on the sheet map).

### `character_has_reliable_talent(character) -> bool`

### `character_has_observant(character) -> bool`

### `character_has_indomitable_might(character) -> bool`

Return `False` when `character` is `None`; otherwise check race, class levels, feats, etc., as in `rolls.gvar`.

### `get_mod_override(character, ability_a: str | None = None, ability_b: str | None = None) -> int`

Returns the difference between the two ability modifiers when overriding which ability applies; `0` when abilities match or `character` is `None`.

Module-level maps `skills_abilities`, `save_abilities`, and `attack_type_abilities` define default pairings used by the helpers above.

## Internal helpers (unsupported)

Names starting with **`_`** in `rolls.gvar` (for example `_get_skill_for_character`, `_natural_roll_from_result`, `_d20_reroll_list`) are implementation details; do not call them from other modules.

## Alias tests (`avrae-ls`)

Tests live in **`rolls.alias`** / **`rolls.alias-test`** and run with **`avrae-ls --run-tests`** (see **`AGENTS.md`**).

After the second `---` in an `.alias-test` block, YAML metadata may include:

- **`name`** — testcase id (must match `testcase` in the paired `.alias`).
- **`character`** — shallow/deep merged onto the language server’s default mock character for that run (see **`avrae_ls` `ContextProfile.character`** / built-in defaults in the `avrae-ls` package’s `config.py`).
- **`vars`** — merged into mock `cvars` / `uvars` / etc. for that run.

**Note:** In **`avrae-ls` 0.8.x**, `avrae-ls --run-tests` uses the workspace **`defaultProfile`** from **`.avraels.json`** (or the built-in default when no profiles are defined). Per-testcase **`profile`** selection is not applied by the CLI test runner; use **`character`** / **`vars`** overrides for sheet-specific cases. Optional named **`profiles`** in **`.avraels.json`** are still useful for editor/LSP runs against a fixed sheet.
