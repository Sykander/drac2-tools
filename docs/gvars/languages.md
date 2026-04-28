# languages

## Purpose

A helper library for **D&D 5e (2014-era)** language metadata and sheet integration. The **canonical catalog** is the module-level dict **`_LANGUAGES`** (see the long comment directly above it in `languages.gvar` for field meanings and layout).

The Avrae **`languages`** cvar holds a comma- or semicolon-separated list of language tokens; **`get_character_languages`** resolves those tokens (including **aliases**) to canonical names from **`_LANGUAGES`**.

**Consumer-facing API** is intentionally small: **`get_character_languages`**, **`language_comprehension_score`**, **`COMMUNICATION_METHODS`**, and **`LANGUAGE_NAMES`** are unprefixed. Other names on the gvar use a leading **`_`** (implementation detail). Avrae blocks **`languages._…`** access from workshop aliases, so downstream commands should call only these; repository tests exercise the same surface.

To regenerate the catalog block in `languages.gvar`, run **`python3 utils/_emit_languages_catalog.py`** from the repo root (offline only; Avrae does not run that script). The script prints **`_LANGUAGES = { … }`** plus a trailing **`LANGUAGE_NAMES`** rebuild loop—paste to replace the matching section in the gvar.

The shipped **`_LANGUAGES`** map is aligned to **D&D 5e (2014) PHB / SRD** standard and exotic language tables, plus **Thieves’ Cant**, **Druidic**, and **Primordial** dialect aliases (**Aquan**, **Auran**, **Ignan**, **Terran**). Creature-only or campaign-specific tongues are out of scope unless added to the dict.

**`LANGUAGE_NAMES`** is a **list** of those canonical names in the same order as dict keys in **`_LANGUAGES`** (insertion order in the shipped gvar).

## Import

Use the workshop UUID from `src/gvars/env.prod.gvar` (or your env gvar) for `languages`.

```py
using(languages = "3fd35bcf-1202-4a42-a0e1-abd1356b4cb3")
```

## Public API

### `get_character_languages(char=None) -> list`

Requires an active or explicit character. Reads **`char.get_cvar("languages", "")`**, splits on **commas and semicolons** (semicolons are normalized to commas first), strips each chunk, and drops empty chunks—so **extra commas and surrounding whitespace** are tolerated. **Periods, slashes, and other punctuation are not delimiters**; they stay inside a token (which may still fuzzy-resolve, e.g. trailing **`Orc.`**). Tokens that are **ambiguous** under fuzzy rules are omitted. Returns **canonical** catalog names for tokens that resolve (via keys, **`aliases`**, and the same fuzzy matching rules used internally). Order follows the cvar; duplicates collapse to a single canonical name each.

### `LANGUAGE_NAMES`

A **list** of canonical language names from **`_LANGUAGES`**, in dict key order. Use for menus, validation, or iteration without importing the private catalog dict.

### `COMMUNICATION_METHODS`

A **list** of canonical channel names, in stable order: **`vocal`**, **`script`**, **`telepathic`**, **`gestural`**. Pass these strings as **`communication_method`** to **`language_comprehension_score`** (or iterate them when probing all channels).

### `language_comprehension_score(language_name: str, char=None, communication_method="vocal") -> int`

**0–100** heuristic (not RAW) for how plausibly **`char`** could follow **`language_name`** in **`communication_method`** (default **`vocal`**).

- **Known** the target (on the resolved cvar list **or** class-granted **Thieves’ Cant** / **Druidic** when applicable, or **implicit Common** — see below): **100** if that language **supports** the requested channel in **`_LANGUAGES`** (the channel is present as a dict, not **`False`**); **0** if the language does not use that channel (incomprehensible on that medium).
- **Otherwise**: combines directed cross-language overlap on that **same medium** from every effective known language (again including **implicit Common** when the cvar omitted it), a small bonus when several known languages each overlap the target, optional **race** hints against **`common_speakers`**, then applies the modality factor.
- **Implicit Common (PHB-style):** for this heuristic only, **Common** is treated as known if it is missing from the **`languages`** cvar and not already granted by class. 5e assumes every PC speaks **Common**; the cvar often forgets to list it. **`get_character_languages`** is unchanged — it still reflects only what resolves on the sheet (plus class grants where applicable).
- **0** when, after that implicit **Common**, there is still no usable overlap or race hint for the target.

**`communication_method`** accepts the canonical names in **`COMMUNICATION_METHODS`** plus common aliases (**`telepathy`**, **`written`** / **`writing`**, **`sign`** and legacy **`visual`** → **`gestural`**, **`speech`** / **`spoken`**, case-insensitive). Unrecognized labels fall back to **`vocal`**.
