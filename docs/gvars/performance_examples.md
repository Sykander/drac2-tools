# performance_examples

Micro-benchmark helpers for comparing **equivalent-result** Drac2 patterns under Avrae’s **per-invocation statement cap** (“too many statements”).

## Public entry points

- **`bench_adv_dice_list_index` / `bench_adv_dice_if_chain`** — four-way “d20 shape” dispatch (list index vs `if`/`elif` chain).
- **`bench_three_way_list_index` / `bench_three_way_if_chain`** — three-way string pick.
- **`bench_dict_get_repeated` / `bench_dict_in_and_subscript`** — repeated read from a small mapping.
- **`bench_membership_tuple_literal` / `bench_membership_list_literal`** — fixed small `in` check, tuple vs list literal.
- **`expected_checksum_*`** — deterministic totals for a given `loops` so tests can assert correctness.

Stress harness: **`performance_examples-perf.alias`** + **`performance_examples-perf.alias-test`** (tunable **`-loops`**). Probing workflow lives in **`AGENTS.md`** (not here).

## Patterns aligned with **`regex.gvar`**

The regex engine uses **subscript** reads (`node["k"]`, `atom["g"]`) on structures whose keys are known at that point, and **`.get(..., default)`** where a field may be absent (e.g. optional capture metadata, `set_map.get(ch, False)`). The **`bench_dict_bracket_known_key`** / **`bench_dict_get_known_key_with_default`** pair measures **known-key** `[]` vs `.get` in isolation—use it when deciding whether a hot path can assume the key exists.

## Using this in your own aliases

Import via **`using(env=…)`** then **`performance_examples = env.gvars.performance_examples`**. For day-to-day rolls, prefer **`rolls.get_roll`** and **`rolls.get_d20`**; this module is for **pattern comparison** and perf education, not general dice.
