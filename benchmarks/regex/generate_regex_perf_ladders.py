#!/usr/bin/env python3
"""Generate regex performance ladder tests with configurable stepped ranges."""

from __future__ import annotations

from pathlib import Path


LADDER_VALUES = (
    list(range(1, 10))
    + [i * 10 for i in range(1, 10)]
    + [i * 100 for i in range(1, 10)]
)

TEST_CASES = [
    ("benchmark search loop should keep correct spans", "loops"),
    ("benchmark class brace loop should keep full matches", "loops"),
    ("benchmark quantified alternation loop should keep matches", "loops"),
    ("benchmark compile multiple regexes in one invocation", "compiles"),
    ("benchmark compile cache hit loop should keep matches", "compiles"),
    ("benchmark compile cache miss loop should keep matches", "compiles"),
    ("benchmark compiled full_match loop should keep matches", "loops"),
    ("benchmark compiled fullmatch alias loop should keep matches", "loops"),
    ("benchmark compiled match loop should keep end index", "loops"),
    ("benchmark compiled search loop should keep span", "loops"),
    ("benchmark compiled match_from loop should keep end index", "loops"),
    ("benchmark compiled match_from_captures loop should keep captures", "loops"),
    ("benchmark compiled search_captures loop should keep captures", "loops"),
]


def build_block(testcase: str, arg_name: str, value: int) -> str:
    return (
        f'!regex-perf -testcase "{testcase}" -{arg_name} "{value}"\n'
        "---\n"
        "---\n"
        f"name: ladder {testcase} {value}\n"
    )


def build_ladders_content() -> str:
    blocks = []
    for testcase, arg_name in TEST_CASES:
        for value in LADDER_VALUES:
            blocks.append(build_block(testcase, arg_name, value))
    return "\n".join(blocks) + "\n"


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    target = repo_root / "benchmarks/regex/regex-perf.ladders.alias-test"
    target.write_text(build_ladders_content(), encoding="utf-8")
    total = len(TEST_CASES) * len(LADDER_VALUES)
    print(f"Wrote {target} with {total} ladder cases.")


if __name__ == "__main__":
    main()
