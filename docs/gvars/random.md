# random

## Purpose

A helper library for seeded random integers and floats: you get deterministic draws when you control the seed, and optional one-off seeds that do not advance global state.

It uses an xorshift-style step internally.

## Import

```drac2
using(random = "9ddcdac4-2fb8-4d3b-bc4c-1cde24936dc5")
```

## Public API

### `setSeed(newSeed: int) -> None`

Sets both the initial and current seed stored in the module.

### `getState() -> dict[str, int]`

Returns the internal seed map (`SEED_CURRENT` and `SEED_INITIAL` keys).

### `setState(newState: dict[str, int]) -> None`

Replaces the internal seed map from `newState`.

### `getSeed() -> int`

Returns the initial seed value.

### `xorShift(seed: int) -> int`

Runs one xorshift step on `seed`, reduced modulo `2**31`; used by `get_random_integer` and `get_float`.

### `get_random_integer(start, stop, seed=None)`

Returns an integer in the inclusive range `[start, stop]`. If `start > stop`, the bounds are swapped; if they are equal, that value is returned.

With `seed=None`, uses and updates the module’s current seed. With an explicit `seed`, that value is used and stored state is not advanced.

### `get_float(seed=None)`

Returns a float uniformly distributed on the closed interval `[0, 1]` (endpoints are reachable via the mapped xorshift output).

Seed semantics match `get_random_integer`: `seed=None` advances the module’s current seed; an explicit `seed` does not.
