# embeds

## Purpose

A helper library for building `!embed` command strings with title, description, fields, footer, image, thumbnail, color, and timeout.

It trims long text to Avrae limits. Use `get_embed` for one-off embeds; use `configure_get_embed` when many call sites share the same defaults.

## Import

```drac2
using(embeds = "ef9ccbb2-5aed-4231-a5d2-773d6a3039d9")
```

## Public API

### `format_to_length(content: str, length: int) -> str`

Returns `content` unchanged if shorter than `length`; otherwise truncates and appends `...`.

### `get_field(title, text="", inline=False) -> str`

Returns a field string for `get_embed`: `title|text`, or `title|text|inline` when `inline` is true.

### `get_embed(desc: str | None = None, title: str | None = None, fields: list[str] | None = None, footer: str | None = None, image: str | None = None, thumb: str | None = None, color: str | None = None, timeout: int | None = None) -> str`

Builds the embed command. Arguments that are `None` are omitted. Description and each field are passed through `format_to_length` (description max 4020, fields max 1020).

### `configure_get_embed(desc: str | None = None, title: str | None = None, fields: list[str] | None = None, footer: str | None = None, image: str | None = None, thumb: str | None = None, color: str | None = None, timeout: int | None = None)`

Returns a callable with the same keyword parameters as `get_embed`, using the captured values as defaults. Invoking it runs `get_embed` with any overrides you pass.
