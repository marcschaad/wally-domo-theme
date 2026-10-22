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
Frame = Horizon's global palette: near-white #FAFAF7, ink #1A1A1A,
graphite #5E5A53, hairline #E2E0DA. Surfaces stay near-white everywhere.
Each drop gets ONE saturated colour pulled from its own art, used only for that
drop's headline and its call-to-action buttons (Marc, 2026-10-22):
Brooklyn = tower wood #8A5A2B (5.6:1 on near-white), Pigeon = cap blue #3F63B8 (5.4:1).
Global buttons (cart, checkout) stay ink. Max three drop colours on screen.
Product cards are tonal: the card background is the drop colour at 12% over
near-white (Pigeon #E4E8EF, Brooklyn #EDE7DF). Titles in the drop colour still pass AA.

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

## Type (2026-10-22)
Four roles, families fixed in snippets/wd-fonts.liquid: body = Broadacre Regular,
subheading = Broadacre Medium (small type), heading = Arsenica Variable,
accent = Arsenica Text. Weight per role = the weight variant of the Shopify font
picked in Theme settings > Typography (heading Inter Light 300; body, accent 400;
subheading 500). The picker's font name is ignored; only its weight counts.
H1-H6 and body sizes live in Horizon's own Typography panel (Dawn values snapped
to Horizon's options). Text blocks only honour their own size/case/font when their
preset is "Custom".

Everything Horizon's panel can't reach lives in OUR section `sections/wd-type.liquid`
(in the header group, editor: Header > "Wally Domo type"; one rule per element via
`snippets/wd-type-el.liquid`): buttons, desktop menu, phone menu, announcement bar,
product page title, prices, product card titles, badges, footer text, form fields,
H3 weight, and the headline weight sweep (Arsenica Variable h1/h2 in main; default
heavy to light, 450 to 300). Defaults = Marc's Dawn values. Dawn's captions and
vendor styles have no Horizon equivalent.
