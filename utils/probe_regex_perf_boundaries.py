#!/usr/bin/env python3
"""
Probe one regex-perf boundary at a time using a *single-test* .alias-test file so each
avrae-ls invocation runs one case (not the full 13-pack).

Search strategy (≤ ~10 avrae-ls runs per boundary, typically ~6):
  1) If try(cap) passes → done in 1 run.
  2) Else exponential gallop: try min(cap, lo*2) from lo=baseline, doubling lo while passes
     and lo < cap (cap at most ~6 steps because lo doubles).
  3) Binary search between last pass and first fail (≤ 6 bisection steps).

Prints TSV lines: testcase_substr<TAB>param<TAB>maxima
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL_ALIAS_DIR = Path("src/gvars/utils/regex")
PROBE = ROOT / REL_ALIAS_DIR / "_probe.regex-perf.alias-test"


def write_probe(testcase_line: str, name: str) -> None:
    body = (
        f"{testcase_line}\n"
        "---\n"
        "---\n"
        f"name: {name}\n"
    )
    PROBE.write_text(body)


def try_val(testcase_line: str, name: str) -> bool:
    write_probe(testcase_line, name)
    r = subprocess.run(
        ["avrae-ls", "--run-tests", str(PROBE.relative_to(ROOT))],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    out = (r.stdout or "") + (r.stderr or "")
    return r.returncode == 0 and "FAIL" not in out


def line_for(sub: str, param: str, val: int) -> str:
    return f'!regex-perf -testcase "{sub}" -{param} "{val}"'


def find_max(sub: str, param: str, baseline: int, cap: int, max_binary: int = 6) -> int:
    if not try_val(line_for(sub, param, baseline), f"probe baseline {baseline}"):
        raise SystemExit(f"baseline fails: {sub} @ {baseline}")

    if baseline >= cap:
        return baseline

    if try_val(line_for(sub, param, cap), f"probe cap {cap}"):
        return cap

    lo = baseline
    hi = min(cap, max(lo + 1, lo * 2))
    steps = 0
    while hi <= cap and steps < 8:
        steps += 1
        if try_val(line_for(sub, param, hi), f"probe hi {hi}"):
            lo = hi
            if lo >= cap:
                return cap
            nxt = min(cap, max(lo + 1, lo * 2))
            if nxt <= lo:
                break
            hi = nxt
        else:
            break

    if lo >= cap:
        return cap

    good, bad = lo, hi
    bsteps = 0
    while good + 1 < bad and bsteps < max_binary:
        bsteps += 1
        mid = (good + bad) // 2
        if try_val(line_for(sub, param, mid), f"probe mid {mid}"):
            good = mid
        else:
            bad = mid
    return good


def main() -> None:
    cases = [
        ("benchmark search loop should keep correct spans", "loops", 1275, 10000),
        ("benchmark class brace loop should keep full matches", "loops", 3, 2000),
        ("benchmark quantified alternation loop should keep matches", "loops", 4, 80),
        ("benchmark compile multiple regexes in one invocation", "compiles", 107, 250),
        ("benchmark compile cache hit loop should keep matches", "compiles", 755, 4000),
        ("benchmark compile cache miss loop should keep matches", "compiles", 53, 300),
        ("benchmark compiled full_match loop should keep matches", "loops", 2360, 10000),
        ("benchmark compiled fullmatch alias loop should keep matches", "loops", 2360, 10000),
        ("benchmark compiled match loop should keep end index", "loops", 1780, 10000),
        ("benchmark compiled search loop should keep span", "loops", 1275, 10000),
        ("benchmark compiled match_from loop should keep end index", "loops", 1820, 10000),
        ("benchmark compiled match_from_captures loop should keep captures", "loops", 125, 600),
        ("benchmark compiled search_captures loop should keep captures", "loops", 56, 300),
    ]
    results: list[tuple[str, str, int]] = []
    try:
        for sub, param, low, cap in cases:
            m = find_max(sub, param, low, cap)
            results.append((sub, param, m))
            print(f"{m}\t{sub[:52]}…", file=sys.stderr)
    finally:
        if PROBE.exists():
            PROBE.unlink()

    for sub, param, m in results:
        print(f"{sub}\t{param}\t{m}")


if __name__ == "__main__":
    main()
