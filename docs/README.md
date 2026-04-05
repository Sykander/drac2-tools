# Documentation

## Gvar utilities

Drac2 global-variable helpers live under `src/gvars/utils/`. Production workshop UUIDs are in `src/gvars/env.prod.gvar`; development UUIDs are in `src/gvars/env.dev.gvar`.

| Module | What to use it for | Doc |
|--------|-------------------|-----|
| bags | Read or update per-character bag inventory in cvars (add/remove items, named bags). | [gvars/bags.md](gvars/bags.md) |
| commands | Build quoted `!` command strings and multiline command blocks safely. | [gvars/commands.md](gvars/commands.md) |
| dicts | Check whether a value is dict-like before treating it as a mapping. | [gvars/dicts.md](gvars/dicts.md) |
| embeds | Emit `!embed` commands with fields, limits, and optional defaults across many call sites. | [gvars/embeds.md](gvars/embeds.md) |
| expect | Fluent assertions in alias tests (`err` on failure); not for player-facing commands. | [gvars/expect.md](gvars/expect.md) |
| lists | List → dict by key, random picks without replacement, list type check, search helpers. | [gvars/lists.md](gvars/lists.md) |
| notes | Named per-character notebooks in cvars; append lines or replace whole notebooks. | [gvars/notes.md](gvars/notes.md) |
| random | Seeded or one-shot random integers for reproducible or isolated rolls. | [gvars/random.md](gvars/random.md) |
| rolls | Skill/save/attack/passive dice strings, `vroll` via `get_roll`, and roll-formatting helpers. | [gvars/rolls.md](gvars/rolls.md) |
| strings | Readable lists, ordinals, replace helpers, and string type checks. | [gvars/strings.md](gvars/strings.md) |
| time | Durations from combat rounds, human-readable time, Discord timestamp snippets. | [gvars/time.md](gvars/time.md) |
| tools | Resolve official tool names and read proficiency/expertise from character cvars. | [gvars/tools.md](gvars/tools.md) |
