# time

## Purpose

A helper library for timestamps: combat-based duration, breaking a duration into parts, human-readable text, and Discord timestamp snippets.

It exposes `SECOND`, `MINUTE`, `HOUR`, `DAY`, and `ROUND` (six seconds per combat round) for building durations.

## Import

```drac2
using(time = "623a1bb0-6b04-4757-bb6e-0c8beeb9ba20")
```

## Public API

### `get_ts_from_combat() -> float`

Returns `float(combat().round_num * ROUND)`, or `0.0` when not in combat.

### `get_time(ts: float = time()) -> dict[str, int]`

Returns `days`, `hours`, `minutes`, and `seconds` from a duration-style timestamp (floored components).

### `get_readable_time(ts: float = time()) -> str`

Builds a human-readable duration string from `get_time` (omits zero parts; still shows seconds when higher units are zero).

### `get_discord_timestamp(ts: float = time()) -> str`

Floors `ts` to an integer and returns the concatenated Discord absolute and relative time markers (`<t:…>` forms as in `time.gvar`).
