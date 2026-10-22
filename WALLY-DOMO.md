# Wally Domo on Horizon: house rules

Base: Horizon 4.3.0 from the Shopify Theme Store (first commit = untouched baseline).

## The one rule
Never edit Horizon's own files. Everything Wally Domo lives in files we own,
named `wd-*` (snippets, blocks, sections, assets). Shopify keeps those through
a theme update; it overwrites everything else.

## The only exceptions (re-add after every Horizon update)
| file | change |
|---|---|
| layout/theme.liquid | `{%- render 'wd-fonts' -%}` after `render 'color-palette'` |
| layout/password.liquid | same line, same place |

## Our files
- `snippets/wd-fonts.liquid`: Adobe kit gag8aux + Quicksand fallback; points Horizon's
  four font roles at our families (body/subheading = Broadacre Regular 0,
  heading/accent = Arsenica Variable). Families only; sizes and weights stay in
  Theme settings > Typography.

## Updating Horizon
1. Theme Store update makes a new theme copy ("Updated copy of ...").
2. Our `wd-*` files carry over. Re-add the hook lines above.
3. Pull the copy into this repo on a branch, diff against the baseline commit, merge.
