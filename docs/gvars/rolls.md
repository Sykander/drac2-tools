# rolls

## Purpose

A helper library for building Avrae dice strings and labels for skills, saves, attacks, passive scores, and flat rolls, and for running them through `get_roll`.

Smaller helpers compose expressions (advantage, damage, joining fragments) and format display names when you are not using `get_roll` end-to-end.

## Import

```drac2
using(rolls = "b6fe8f32-72ee-4179-a5b2-6fe79c77f372")
```

## Public API

### `get_roll(character, roll_name, args: ParsedArguments, roll_type: str, ability_name: str | None = None, dc: int | None = None, adv: bool | None = None, bonuses: list[str] | None = None) -> dict`

Main entry point. `roll_type` is one of `"roll"`, `"check"`, `"passive"`, `"save"`, `"attack"`. For `"check"`, `"passive"`, `"save"`, and `"attack"`, `roll_name` is the usual string key (skill name, save name, or `"melee"` / `"ranged"` for attacks). When `roll_type == "roll"`, `roll_name` is the dice expression passed to `vroll`; it is normalized with `str()` first, so you can pass a string or another value (such as a number) that stringifies to valid dice syntax. `args` is parsed alias arguments (advantage flags, `-b`, `-guidance`, `-bless`, `-resistance`, ability overrides, etc.). `bonuses` is copied when provided so callers’ lists are not mutated.

Pass **`None`** for `character` to use the **active** Avrae sheet when one exists (`resolve_character`). For `"check"`, `"passive"`, `"save"`, and `"attack"`, a sheet is **required** after resolution—if there is no active character and no explicit override, `get_roll` errors. For `"roll"`, a missing sheet is still allowed for the roll string itself; when `character` is `None` and there is no active character, race/feat helpers behave as if there were no sheet.

Returns a dict with `roll`, `total`, `full`, `name`, `roll_string`, `dc`, `passed`, `crit`, and `crit_fail` (see `rolls.gvar`).

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

### `character_has_reliable_talent(character) -> bool`

### `character_has_observant(character) -> bool`

### `character_has_indomitable_might(character) -> bool`

Return `False` when `character` is `None`; otherwise check race, class levels, feats, etc., as in `rolls.gvar`.

### `get_mod_override(character, ability_a: str | None = None, ability_b: str | None = None) -> int`

Returns the difference between the two ability modifiers when overriding which ability applies; `0` when abilities match or `character` is `None`.

Module-level maps `skills_abilities`, `save_abilities`, and `attack_type_abilities` define default pairings used by the helpers above.
