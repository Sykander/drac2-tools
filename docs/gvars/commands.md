# commands

## Purpose

A helper library for building Avrae command strings with safe quoting and multiline formatting.

It lets you emit other commands from an alias without hand-escaping spaces or special characters. Multiline output includes `ctx.prefix` on each line; for single-line commands you add the prefix yourself when needed.

## Import

```drac2
using(commands = "4eb91b72-d65d-49a1-9f92-d804772546b0")
```

## Public API

### `get_multiline(commands: list[str]) -> str`

Returns a multiline command string: `multiline ` plus `ctx.prefix` and each command joined with newlines and `ctx.prefix`.

### `get_quotes(value: str) -> str`

Returns `value` unchanged if no quoting is needed; otherwise wraps it in double quotes, single quotes, or `《…》` when both quote characters appear inside `value`.

### `get_command(actions: list[str], args: list[Tuple[str, str]] | None = None) -> str`

Builds one command line: each action is passed through `get_quotes` and joined with spaces. Optional `args` are `[[flag, value], …]` pairs; values are quoted with `get_quotes`.
