# Wally Domo on Horizon: house rules

Base: Horizon 4.3.0 from the Shopify Theme Store (first commit = untouched baseline).

## The one rule
Never edit Horizon's own files. Everything Wally Domo lives in files we own,
named `wd-*` (snippets, blocks, sections, assets). Shopify keeps those through
a theme update; it overwrites everything else.

Content files are not code and are ours to edit: `config/settings_data.json`
(palette, theme settings) and `templates/*.json` / `sections/*-group.json`
(which sections sit on which page). Updates carry them over.

## Colour (2026-10-22)
Frame = Horizon's global palette: paper #F2EFE6, ink #1A1A1A, graphite #5E5A53,
stock #DAD5CA. Each release gets one loud section background pulled from its
own art and pushed: Brooklyn = tower wood #8A5A2B, Pigeon = cap blue #3F63B8.
Horizon picks paper or ink text automatically; every pair checked AA.
Max three release colours on screen.

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

## Gotchas
- Static blocks in templates/*.json need `"blocks": {}` even when empty, or Shopify
  silently drops their settings on sync (the commit still "succeeds").
- Theme editor saves are committed back to main by shopify[bot]. Always `git pull` first.
- Image references look like `shopify://shop_images/<filename>`.
