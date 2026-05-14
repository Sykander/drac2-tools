# performance_examples

Micro-benchmark helpers for comparing **equivalent-result** Drac2 patterns under Avrae’s **per-invocation statement cap** (“too many statements”).

## Public entry points

- **`bench_adv_dice_list_index` / `bench_adv_dice_if_chain`** — four-way “d20 shape” dispatch (list index vs `if`/`elif` chain).
- **`bench_three_way_list_index` / `bench_three_way_if_chain`** — three-way string pick.
- **`bench_dict_get_repeated` / `bench_dict_in_and_subscript`** — repeated read from a small mapping.
- **`bench_dict_get_bare_present_key` / `bench_dict_bracket_present_same_key`** — present key: **`a.get("key")`** vs **`a["key"]`** (same value each iteration).
- **`bench_membership_tuple_literal` / `bench_membership_list_literal`** — fixed small `in` check, tuple vs list literal.
- **`bench_counter_plus_assign` / `bench_counter_plus_eq`** — **`i = i + 1`** vs **`i += 1`**; optional second argument **`reps_per_iter`** (or **`-reps`** on the perf alias) repeats that many increments per outer step. **`performance_examples-perf`** commits **`-reps` 10** with probed **`-loops`** so CI exercises the inner-repetition path, not only the **`reps` 1** **`max_loops`** plateau.
- **`expected_checksum_*`** — deterministic totals for a given `loops` (and **`reps`** for counters) so tests can assert correctness.

Stress harness: **`performance_examples-perf.alias`** + **`performance_examples-perf.alias-test`** (tunable **`-loops`**, counter benchmarks also **`-reps`**). Probing workflow lives in **`AGENTS.md`** and **`.cursor/README.md`** (not here). To probe several perf testcases under the same extra flags (e.g. **`-reps`** on both counter benchmarks), run **`.cursor/scripts/probe_perf_boundaries.py`** with **one dimension row per testcase** (**`--dimension`** repeated, **`--dimensions-file`**, or **`--preset performance_examples`**); see **`--help`**.

## Patterns aligned with **`regex.gvar`**

The regex engine uses **subscript** reads (`node["k"]`, `atom["g"]`) on structures whose keys are known at that point, and **`.get(..., default)`** where a field may be absent (e.g. optional capture metadata, `set_map.get(ch, False)`). The **`bench_dict_bracket_known_key`** / **`bench_dict_get_known_key_with_default`** pair measures **known-key** `[]` vs `.get("k", 0)` in isolation—use it when deciding whether a hot path can assume the key exists. **`bench_dict_get_bare_present_key`** / **`bench_dict_bracket_present_same_key`** compare **`a.get("key")`** vs **`a["key"]`** when the key is always present (same return value; probes favor subscript slightly). For **optional keys with a default** (e.g. ``.get("key", 1)`` when absent), see **`bench_dict_get_missing_key_default_one`** vs **`bench_dict_in_else_subscript_missing_key_default_one`** (probed: effectively a tie—prefer ``.get`` for clarity).

## Using this in your own aliases

Import via **`using(env=…)`** then **`performance_examples = env.gvars.performance_examples`**. For day-to-day rolls, prefer **`rolls.get_roll`** and **`rolls.get_d20`**; this module is for **pattern comparison** and perf education, not general dice.
