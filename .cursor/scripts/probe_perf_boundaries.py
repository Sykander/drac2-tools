#!/usr/bin/env python3
"""Probe Avrae statement-budget maxima for *-perf stress tests (see gvar-perf-boundaries.mdc)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in here.parents:
        if (p / "src" / "gvars").is_dir():
            return p
    return Path.cwd()


PRESETS: dict[str, dict] = {
    "regex": {
        "alias_dir": "src/gvars/utils/regex",
        "stress_alias": "regex-perf",
        "probe_filename": "_probe.regex-perf.alias-test",
        "dimensions": [
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
        ],
    },
    "rolls": {
        "alias_dir": "src/gvars/utils/rolls",
        "stress_alias": "rolls-perf",
        "probe_filename": "_probe.rolls-perf.alias-test",
        "dimensions": [
            ("benchmark get_roll flat 1d1 loop should keep totals", "loops", 50, 25000),
            ("benchmark get_roll check loop should keep athletics", "loops", 50, 12000),
            ("benchmark get_roll save loop should keep dexterity", "loops", 50, 12000),
            ("benchmark get_roll attack loop should keep melee", "loops", 50, 12000),
            ("benchmark get_roll passive loop should keep perception", "loops", 50, 12000),
        ],
    },
    "performance_examples": {
        "alias_dir": "src/gvars/utils/performance_examples",
        "stress_alias": "performance_examples-perf",
        "probe_filename": "_probe.performance_examples-perf.alias-test",
        "dimensions": [
            ("benchmark adv dice list index loop should keep checksum", "loops", 500, 80000),
            ("benchmark adv dice if chain loop should keep checksum", "loops", 500, 80000),
            ("benchmark three way list index loop should keep checksum", "loops", 500, 80000),
            ("benchmark three way if chain loop should keep checksum", "loops", 500, 80000),
            ("benchmark dict get loop should keep checksum", "loops", 500, 80000),
            ("benchmark dict in and subscript loop should keep checksum", "loops", 500, 80000),
            ("benchmark tuple membership loop should keep checksum", "loops", 500, 80000),
            ("benchmark list membership loop should keep checksum", "loops", 500, 80000),
            ("benchmark dict bracket known key loop should keep checksum", "loops", 500, 80000),
            ("benchmark dict get known key loop should keep checksum", "loops", 500, 80000),
            ("benchmark counter plus assign loop should keep checksum", "loops", 500, 80000),
            ("benchmark counter plus eq loop should keep checksum", "loops", 500, 80000),
            ("benchmark string concat assign loop should keep checksum", "loops", 200, 20000),
            ("benchmark string concat plus eq loop should keep checksum", "loops", 200, 20000),
        ],
    },
}


def parse_dimension(s: str) -> tuple[str, str, int, int]:
    parts = [x.strip() for x in s.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError(
            f"Expected testcase,param,baseline,cap — got {len(parts)} fields in {s!r}"
        )
    testcase, param, low_s, cap_s = parts
    return testcase, param, int(low_s), int(cap_s)


def write_probe(probe_path: Path, testcase_line: str, name: str) -> None:
    body = f"{testcase_line}\n---\n---\nname: {name}\n"
    probe_path.write_text(body)


def try_val(
    root: Path,
    probe_rel: Path,
    stress_alias: str,
    testcase_line: str,
    name: str,
    timeout: int,
) -> bool:
    probe_abs = root / probe_rel
    write_probe(probe_abs, testcase_line, name)
    r = subprocess.run(
        ["avrae-ls", "--run-tests", str(probe_rel)],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    out = (r.stdout or "") + (r.stderr or "")
    return r.returncode == 0 and "FAIL" not in out


def line_for(stress_alias: str, sub: str, param: str, val: int) -> str:
    return f'!{stress_alias} -testcase "{sub}" -{param} "{val}"'


def find_max(
    root: Path,
    probe_rel: Path,
    stress_alias: str,
    sub: str,
    param: str,
    baseline: int,
    cap: int,
    timeout: int,
    max_binary: int,
) -> int:
    def trial(line: str, label: str) -> bool:
        return try_val(root, probe_rel, stress_alias, line, label, timeout)

    if not trial(
        line_for(stress_alias, sub, param, baseline),
        f"probe baseline {baseline}",
    ):
        raise SystemExit(f"baseline fails: {sub!r} @ {baseline}")

    if baseline >= cap:
        return baseline

    if trial(line_for(stress_alias, sub, param, cap), f"probe cap {cap}"):
        return cap

    lo = baseline
    hi = min(cap, max(lo + 1, lo * 2))
    steps = 0
    while hi <= cap and steps < 8:
        steps += 1
        if trial(line_for(stress_alias, sub, param, hi), f"probe hi {hi}"):
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
        if trial(line_for(stress_alias, sub, param, mid), f"probe mid {mid}"):
            good = mid
        else:
            bad = mid
    return good


def main() -> None:
    epilog = """Examples (repo root):
  python3 .cursor/scripts/probe_perf_boundaries.py --preset regex
  python3 .cursor/scripts/probe_perf_boundaries.py --preset rolls
  python3 .cursor/scripts/probe_perf_boundaries.py \\
    --alias-dir src/gvars/utils/foo --stress-alias foo-perf \\
    --dimension "Full testcase title as in *-perf.alias,loops,10,5000"
  python3 .cursor/scripts/probe_perf_boundaries.py \\
    --alias-dir src/gvars/utils/performance_examples \\
    --stress-alias performance_examples-perf \\
    --dimensions-file .cursor/templates/probe-performance_examples-from-committed.txt \\
    --max-binary 20

TSV on stdout (testcase, param, maxima). Progress on stderr."""
    ap = argparse.ArgumentParser(
        description=__doc__.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog,
    )
    ap.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root (default: auto-detect from this script)",
    )
    ap.add_argument(
        "--preset",
        choices=sorted(PRESETS.keys()),
        help="Built-in alias-dir, stress alias, probe filename, and dimensions",
    )
    ap.add_argument(
        "--alias-dir",
        type=str,
        help="Directory relative to root containing the probe file (e.g. src/gvars/utils/regex)",
    )
    ap.add_argument(
        "--stress-alias",
        type=str,
        help="Alias command name for the first line of the .alias-test (e.g. regex-perf)",
    )
    ap.add_argument(
        "--probe-filename",
        type=str,
        help="Probe file basename inside alias-dir (default: _probe.<stress-alias>.alias-test)",
    )
    ap.add_argument(
        "--dimension",
        action="append",
        default=[],
        type=parse_dimension,
        metavar="TESTCASE,PARAM,LOW,CAP",
        help="Repeatable; testcase string must match *-perf.alias elif branch exactly",
    )
    ap.add_argument(
        "--dimensions-file",
        type=Path,
        help="One dimension per line: testcase,param,baseline,cap (same as --dimension)",
    )
    ap.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Seconds per avrae-ls invocation (default: 120)",
    )
    ap.add_argument(
        "--max-binary",
        type=int,
        default=6,
        metavar="N",
        help="Max binary-search refinement steps between last pass and first fail (default: 6; use 16–24 when re-probing from an already-high baseline)",
    )
    args = ap.parse_args()

    root = (args.root or _repo_root()).resolve()

    dimensions: list[tuple[str, str, int, int]] = []
    alias_dir: str | None = None
    stress_alias: str | None = None
    probe_filename: str | None = None

    if args.preset:
        cfg = PRESETS[args.preset]
        alias_dir = cfg["alias_dir"]
        stress_alias = cfg["stress_alias"]
        probe_filename = cfg["probe_filename"]
        dimensions = list(cfg["dimensions"])

    if args.alias_dir:
        alias_dir = args.alias_dir
    if args.stress_alias:
        stress_alias = args.stress_alias
    if args.probe_filename:
        probe_filename = args.probe_filename

    if args.dimensions_file:
        df = args.dimensions_file
        if not df.is_absolute():
            df = root / df
        text = df.read_text(encoding="utf-8")
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            dimensions.append(parse_dimension(line))

    for d in args.dimension:
        dimensions.append(d)

    if not alias_dir or not stress_alias:
        ap.error("Provide --preset or both --alias-dir and --stress-alias")
    if not dimensions:
        ap.error("Provide dimensions via --preset, --dimension, or --dimensions-file")
    if not probe_filename:
        probe_filename = f"_probe.{stress_alias}.alias-test"

    probe_rel = Path(alias_dir) / probe_filename
    results: list[tuple[str, str, int]] = []
    try:
        for sub, param, low, cap in dimensions:
            m = find_max(
                root,
                probe_rel,
                stress_alias,
                sub,
                param,
                low,
                cap,
                args.timeout,
                args.max_binary,
            )
            results.append((sub, param, m))
            print(f"{m}\t{sub[:52]}…", file=sys.stderr)
    finally:
        p = root / probe_rel
        if p.exists():
            p.unlink()

    for sub, param, m in results:
        print(f"{sub}\t{param}\t{m}")


if __name__ == "__main__":
    main()
