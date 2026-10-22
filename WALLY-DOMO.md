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
Each BODY OF WORK (not each piece) gets ONE saturated colour pulled from its art,
used only for its titles and call-to-action buttons (Marc, 2026-10-22).
Series 1 (We Lived in Brooklyn, Baby + Pigeon Gone West) = tower wood #8A5A2B
(5.6:1 on near-white). Cap blue #3F63B8 retired with it; kept here if wanted.
Global buttons (cart, checkout) stay ink. Max three drop colours on screen.
Product cards are tonal: the card background is the series colour at 12% over
near-white (series 1: #EDE7DF). Titles in the drop colour still pass AA.

## The only exceptions (re-add after every Horizon update)
| file | change |
|---|---|
| layout/theme.liquid | `{%- render 'wd-fonts' -%}` after `render 'color-palette'` |
| layout/password.liquid | same line, same place |
| locales/en.default.schema.json | cosmetic labels only: options.body = "Broadacre", options.subheading = "Broadacre Medium", options.heading = "Arsenica Variable", options.accent = "Arsenica Text"; content.fonts = "Fonts: pickers unused (set fonts in Header > Wally Domo fonts and type)". If an update reverts them nothing breaks; the editor just shows Horizon's role names again. |

## Our files
- `snippets/wd-fonts.liquid`: Adobe kit gag8aux + Quicksand fallback; fixes Horizon's
  four font roles to our families: body = Broadacre Regular, subheading = Broadacre
  Medium, heading = Arsenica Variable, accent = Arsenica Text. Renders wd-cta.
- `sections/wd-type.liquid` (+ `snippets/wd-type-el.liquid`): editor Header >
  "Wally Domo fonts and type". Role weights, per-element type, H3 weight, sweep.
- `sections/wd-editions.liquid` ("WD Editions"): homepage print cards. Flat controls:
  heading, intro, series colour, card tint, card margin, gap, mat, print shape, title
  size, edition line, price, button label, spacing; one "Print" block per card.
- `sections/wd-studio-note.liquid` ("WD Studio note"): portrait + note + email sign-up
  (customer tags) + link, flat controls.
- Rule (Marc, 2026-10-22): build our own flat sections instead of nesting Horizon's
  generic groups. Every control on one screen, named plainly.

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
Four fonts, each tied to one Horizon role and labelled by its real name in every
Font menu: Broadacre (body), Broadacre Medium (subheading), Arsenica Variable
(heading), Arsenica Text (accent). Swap a font on anything = pick another name in
its Font menu. Weights: Header > Wally Domo fonts and type (Arsenica Variable 300,
Arsenica Text 400; Broadacre cuts fixed). The Typography font pickers are unused.
H1-H6 and body sizes live in Horizon's own Typography panel (Dawn values snapped to
Horizon's options). Text blocks only honour their own size/case/font when their
preset is "Custom".

Everything Horizon's panel can't reach lives in OUR section `sections/wd-type.liquid`
(in the header group, editor: Header > "Wally Domo fonts and type"; one rule per element via
`snippets/wd-type-el.liquid`): buttons, desktop menu, phone menu, announcement bar,
product page title, prices, product card titles, badges, footer text, form fields,
H3 weight, and the headline weight sweep (Arsenica Variable h1/h2 in main; default
heavy to light, 450 to 300). Defaults = Marc's Dawn values. Dawn's captions and
vendor styles have no Horizon equivalent.

## CTAs (2026-10-22, Marc: "the same exact CTA style I had on Dawn")
`snippets/wd-cta.liquid` (rendered from wd-fonts): homepage series buttons
(Button style "Custom"), Add to cart (main + sticky bar) and Checkout get a 2px
stroke, no fill, label in the button's border colour; hover/keyboard focus fills
with that colour and a near-white label; disabled never fills. Other buttons stay
solid. Buttons are square (radius 0, as on Dawn). Add class `wd-cta` to any
.button to opt in.

- `url` settings may only default to a store path (e.g. /collections/all). An outside URL
  default makes Shopify reject the whole section file, and any template using it.
- If Shopify rejects a file, its stale copy of anything that depends on it comes back to
  GitHub on the next editor save. Check `git log` for shopify[bot] commits after pushing.

## Product type eyebrow (2026-10-22)
Every product shows its Shopify **Product type** (Print, Tee, Kids Tee, Tote) above the
title: a "Custom Liquid" block named "Product type" (`<p class="wd-type-eyebrow">`) in every
product card template and above the product page title, plus `.wd-ed__eyebrow` in WD Editions
(per-print override available). Look: Header > Wally Domo fonts and type > "Product type label".
Why Custom Liquid: Shopify rejects `{{ closest.product.type }}` inside a Text block
("Dynamic source is invalid"); only some product fields are allowed as dynamic sources. Marc sets the
type in Shopify admin > Products > Type, so titles can just be the piece's name.
