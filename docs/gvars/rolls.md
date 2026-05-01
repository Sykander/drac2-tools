# rolls

## Purpose

A helper library for building Avrae dice strings and labels for skills, saves, attacks, passive scores, and flat rolls, and for running them through `get_roll`.

Smaller helpers compose expressions (advantage, damage, joining fragments) and format display names when you are not using `get_roll` end-to-end.

## Import

```drac2
using(rolls = "b6fe8f32-72ee-4179-a5b2-6fe79c77f372")
```

## Supported public API

Only the functions in this section are considered a stable, supported surface for aliases and other gvars. Anything not listed here—including any **`_`**-prefixed name in `rolls.gvar`—is internal.

### `get_roll(character, roll_name, args: ParsedArguments, roll_type: str, ability_name: str | None = None, dc: int | None = None, adv: bool | None = None, bonuses: list[str] | None = None, arg_aliases: dict | None = None) -> dict`

Main entry point. `roll_type` is one of `"roll"`, `"check"`, `"passive"`, `"save"`, `"attack"`. For `"check"`, `"passive"`, `"save"`, and `"attack"`, `roll_name` is usually a skill or save key (or `"melee"` / `"ranged"` for attacks). When `roll_type == "roll"`, `roll_name` is the dice expression passed to `vroll`; it is normalized with `str()` first, so you can pass a string or another value (such as a number) that stringifies to valid dice syntax. `args` is parsed alias arguments (advantage flags, `-b`, `-guidance`, `-bless`, `-resistance`, ability overrides, etc.). `bonuses` is copied when provided so callers’ lists are not mutated.

For **`"check"`** and **`"passive"`**, `roll_name` is normalized with **`resolve_skill_input`** (substring match on sheet skill keys, case-insensitive, spaces removed). For **`"save"`**, use **`resolve_save_input`** (e.g. `dex` → `dexterity`); ambiguous partial names error.

Optional **`arg_aliases`** remaps argparse keys, e.g. `{"advantage": {"adv": "survAdv", "dis": "survDis"}, "b": "survBonus", "guidance": "survGuidance", "mc": "survMC"}`. Omitted entries keep defaults `adv`/`dis`, `b`, `guidance`, `mc`.

**Minimum d20 on checks:** `-mc <n>` sets the d20 minimum. Otherwise minimum **10** applies only when the skill is **proficient** (`skill.prof >= 1`) and the character either has Reliable Talent by level (`character_has_reliable_talent`) or the sheet csetting **`talent`** is true.

**Rerolls:** Halfling Lucky still uses `ro1` when applicable. If **`character.csettings.reroll`** is an integer, it is merged into the d20 reroll list (when `csettings` exists at runtime).

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

Returns the difference between the two ability modifiers when overriding which ability applies: `mod(ability_b) - mod(ability_a)`. Returns `0` when `character` is `None`, when **`ability_b` is `None`** (no override — the sheet skill/save total already uses the default ability), or when **`ability_a` and `ability_b` are the same**.

Module-level maps `skills_abilities`, `save_abilities`, and `attack_type_abilities` define default pairings used by the helpers above.

## Performance notes (`get_roll`)

`get_roll` always ends with **`vroll(roll_str)`**, which is engine-native and dominates wall time in real aliases. The surrounding Drac2 work is mostly **linear in the amount of branching you hit** for the chosen `roll_type`: argument and alias-key normalization, optional **`arg_aliases`** remapping, resolving **`roll_name`** (`resolve_skill_input` / `resolve_save_input` where applicable), building a readable label, pulling modifiers from the sheet, assembling the d20 expression (`get_d20`, **`join_roll_strings`**), then **`_natural_roll_from_result`** (walks the shallow `roll.raw` tree once, except for `"passive"` where `natural_roll` is skipped).

**Relative cost (avrae-ls statement budget, one invocation):** stress harness **`rolls-perf.alias-test`** runs five tight loops per file (mock sheet from **`avrae-ls`**). Probed maxima on this repo’s runner (see **`python3 .cursor/scripts/probe_perf_boundaries.py --preset rolls`**) were approximately:

| Scenario | Loops per invocation at boundary |
| --- | ---: |
| Flat `get_roll` (`"roll"`, `"1d1"`, no sheet) | 287 |
| Check (`"letics"` → athletics) | 110 |
| Save (`dex`) | 132 |
| Attack (`melee`) | 166 |
| Passive (`perception`) | 121 |

Higher numbers mean **more interpreter statements per `get_roll` call** for that path under the cap. Flat rolls do the least sheet work; checks do skill resolution, proficiency, reliable-talent / reroll wiring, then `vroll`. Re-tune boundaries after large `get_roll` refactors using **`.cursor/scripts/probe_perf_boundaries.py`** and **`.cursor/rules/gvar-perf-boundaries.mdc`**.

## Internal helpers (unsupported)

Names starting with **`_`** in `rolls.gvar` (for example `_get_skill_for_character`, `_natural_roll_from_result`, `_d20_reroll_list`) are implementation details; do not call them from other modules.
