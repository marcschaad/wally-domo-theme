"""Generates sections/wd-type.liquid for the Wally Domo Horizon theme.

Usage: python3 -I gen_wd_type.py <repo_dir>
One section, placed in the header group, that styles the elements Horizon's
own Typography panel can't reach, plus the headline weight sweep. Defaults are
Marc's saved Dawn values (DRAFT theme, 2026-10-22).
"""
import json
import sys

repo = sys.argv[1]

# key, editor label, CSS selector, defaults: font, size, weight, line height %, tracking (1/1000 em), case
ELEMENTS = [
    ("button", "Buttons (Add to cart, Shop the print, Sign me up...)", ":is(.button, .button-secondary, .button-custom, button.shopify-payment-button__button--unbranded):not(.button-unstyled)",
     ("arsenica-variable", 13, 800, 120, 70, "uppercase"), (8, 32)),
    ("nav", "Menu (desktop)", ":is(.menu-list__link, .menu-list__link-title)",
     ("arsenica-variable", 13, 700, 120, 25, "capitalize"), (8, 32)),
    ("mobile_nav", "Menu (phone drawer)", ":is(.menu-drawer__menu-item, .menu-drawer__menu-item a)",
     ("body", 36, 400, 120, 0, "uppercase"), (12, 60)),
    ("announcement", "Announcement bar", ":is(.announcement-bar__text, .announcement-bar__link)",
     ("arsenica-text", 13, 400, 120, 0, "none"), (8, 32)),
    ("product_title", "Product page title", ".product-details :is(h1, h1 *)",
     ("body", 26, 300, 105, 0, "none"), (12, 72)),
    ("price", "Prices", ":is(product-price .price, .sticky-add-to-cart__price .price, .price-item__group)",
     ("body", 14, 600, 130, 35, "none"), (8, 40)),
    ("card_title", "Product card titles", "product-card [role=\"heading\"]",
     ("arsenica-variable", 15, 700, 125, 0, "capitalize"), (8, 40)),
    ("badge", "Badges (sale, sold out)", ".product-badges > *",
     ("body", 12, 400, 120, 0, "none"), (8, 24)),
    ("product_type", "Product type label (Print, Tee, Kids Tee, Tote)", ":is(.wd-type-eyebrow, .wd-ed__eyebrow)",
     ("body", 12, 500, 120, 80, "uppercase"), (8, 24)),
    ("signup", "Sign-up line (above email boxes)", ".wd-signup .wd-signup__cta",
     ("body", 14, 300, 140, 0, "none"), (10, 28)),
    ("footer", "Footer text", "footer :is(p, li, a, span, small):not(.button)",
     ("body", 14, 400, 140, 0, "none"), (8, 28)),
    ("form", "Form fields", ":is(input:not([type=checkbox], [type=radio], [type=hidden]), select, textarea, .wd-signup .wd-signup__msg, .wd-note__msg)",
     ("body", 15, 400, 130, 0, "none"), (12, 24)),
]

# Horizon's text presets (H1-H6, paragraph). We set Horizon's own --font-<preset>--* variables,
# so every Horizon block using a preset follows. key, label, (font, size, phone size, weight, lh %, tracking, case), size range
PRESETS = [
    ("paragraph", "Body text (paragraphs)", ("body", 14, 14, 300, 140, 0, "none"), (10, 24)),
    ("h1", "Heading 1", ("arsenica-text", 56, 44, 400, 120, 0, "uppercase"), (20, 120)),
    ("h2", "Heading 2", ("arsenica-variable", 40, 40, 300, 120, 0, "uppercase"), (16, 96)),
    ("h3", "Heading 3", ("body", 32, 32, 600, 120, 0, "none"), (14, 80)),
    ("h4", "Heading 4", ("body", 20, 20, 300, 120, 0, "none"), (12, 60)),
    ("h5", "Heading 5", ("body", 18, 18, 300, 120, 0, "none"), (12, 48)),
    ("h6", "Heading 6", ("body", 16, 16, 300, 120, 0, "none"), (10, 40)),
]

# Text styles (2026-10-23, Marc: controls too cumbersome). Set once here; every text in a WD
# section picks one from a Style menu, or "Custom" to get its own six controls.
# key, label, (font, size, phone size, weight, lh %, tracking, case), size range
STYLES = [
    ("display", "Display: big italic headline", ("arsenica-variable-italic", 48, 36, 300, 105, -5, "none"), (20, 120)),
    ("headline", "Headline", ("arsenica-variable", 40, 32, 300, 110, 0, "none"), (16, 96)),
    ("title_large", "Title large", ("arsenica-text", 36, 28, 400, 110, 0, "none"), (16, 96)),
    ("title", "Title: piece names", ("arsenica-text", 24, 20, 400, 120, 0, "none"), (12, 60)),
    ("title_small", "Title small", ("arsenica-text", 18, 18, 400, 120, 0, "none"), (10, 40)),
    ("body", "Body", ("body", 14, 14, 300, 140, 0, "none"), (10, 32)),
    ("note", "Note: italic aside", ("arsenica-variable-italic", 15, 15, 300, 140, 0, "none"), (10, 36)),
    ("label", "Label: small caps", ("body", 12, 12, 500, 120, 80, "uppercase"), (8, 24)),
    ("label_small", "Label small: tiny caps", ("body", 11, 11, 500, 120, 100, "uppercase"), (8, 24)),
    ("small", "Small print", ("body", 12, 12, 300, 140, 10, "none"), (8, 24)),
    ("price", "Price", ("body", 14, 14, 600, 130, 35, "none"), (8, 40)),
]

FONT_OPTIONS = [
    ("body", "Broadacre (Regular; Medium at 450+)"),
    ("arsenica-variable", "Arsenica Variable"),
    ("arsenica-variable-italic", "Arsenica Variable Italic"),
    ("arsenica-text", "Arsenica Text"),
]
CASE_OPTIONS = [("none", "As typed"), ("uppercase", "All caps"), ("lowercase", "All lowercase"), ("capitalize", "Initial caps")]


def settings_for(key, label, defaults, size_range, phone=None):
    font, size, weight, lh, trk, case = defaults
    lo, hi = size_range
    out = [
        {"type": "header", "content": label},
        {"type": "select", "id": f"{key}_font", "label": "Font",
         "options": [{"value": v, "label": l} for v, l in FONT_OPTIONS], "default": font},
        {"type": "range", "id": f"{key}_size", "label": "Size", "min": lo, "max": hi, "step": 1, "unit": "px", "default": size},
    ]
    if phone is not None:
        out.append({"type": "range", "id": f"{key}_phone", "label": "Size on phones", "min": lo, "max": hi, "step": 1, "unit": "px", "default": phone,
                    "info": "Shrinks smoothly from Size to this as the screen narrows."})
    return out + [
        {"type": "range", "id": f"{key}_weight", "label": "Weight", "min": 100, "max": 900, "step": 50, "default": weight,
         "info": "Broadacre: under 450 = Regular, 450+ = Medium. Arsenica Text: 400 or 700."},
        {"type": "range", "id": f"{key}_lh", "label": "Line height", "min": 70, "max": 200, "step": 5, "unit": "%", "default": lh},
        {"type": "range", "id": f"{key}_tracking", "label": "Tracking", "min": -100, "max": 300, "step": 5, "default": trk,
         "info": "1/1000 em, as in Illustrator."},
        {"type": "select", "id": f"{key}_case", "label": "Case",
         "options": [{"value": v, "label": l} for v, l in CASE_OPTIONS], "default": case},
    ]


# shared with sections/wd-editions.liquid and sections/wd-studio-note.liquid (see gen_wd_sections.py)


schema_settings = [
    {"type": "paragraph", "content": "The site uses four fonts. Every Font menu in the editor lists them by name: Broadacre, Broadacre Medium, Arsenica Variable, Arsenica Text. Each name always means that font. To swap the font on anything, pick a different name in its Font menu."},
    {"type": "paragraph", "content": "Every text style below has its own font, size, weight, line height, tracking and case. Theme settings > Typography is not used (it is overridden from here). Text inside WD sections (WD Editions, WD Studio note) is set in each section."},
    {"type": "paragraph", "content": "Weights: Arsenica Variable takes any weight 100-800. Arsenica Text is 400 or 700. Broadacre is two cuts: under 450 = Regular, 450 and up = Medium."},
    {"type": "paragraph", "content": "Headlines in Arsenica Variable get the weight sweep (bottom of this panel) instead of their own weight while the sweep is on."},
]
schema_settings += [{"type": "header", "content": "TEXT STYLES"},
    {"type": "paragraph", "content": "Set these once. Every text in a WD section (Editions, Weekly drop, Studio note, Footer, Canvas) has a Style menu that picks one of these. Change a style here and every text using it follows. Pick Custom in a text's Style menu to give that one text its own controls."}]
for key, label, d, rng in STYLES:
    font, size, phone, weight, lh, trk, case = d
    schema_settings += settings_for(f"st_{key}", f"Style: {label}", (font, size, weight, lh, trk, case), rng, phone)
schema_settings += [{"type": "header", "content": "SITE-WIDE ELEMENTS"},
    {"type": "paragraph", "content": "Horizon's own parts: buttons, menus, product pages, prices, forms."}]
for key, label, _sel, defaults, rng in ELEMENTS:
    schema_settings += settings_for(key, label, defaults, rng)
schema_settings += [{"type": "paragraph", "content": "Headings and body text (used by Horizon blocks, e.g. a Text block set to Heading 2) are below."}]
for key, label, d, rng in PRESETS:
    font, size, phone, weight, lh, trk, case = d
    schema_settings += settings_for(key, label, (font, size, weight, lh, trk, case), rng, phone)
schema_settings += [
    {"type": "header", "content": "Default weights (text without its own controls)"},
    {"type": "range", "id": "w_arsenica_variable", "label": "Arsenica Variable", "min": 100, "max": 800, "step": 10, "default": 300,
     "info": "Only for Horizon text that has no weight control of its own."},
    {"type": "select", "id": "w_arsenica_text", "label": "Arsenica Text",
     "options": [{"value": "400", "label": "Regular (400)"}, {"value": "700", "label": "Bold (700)"}], "default": "400",
     "info": "Only for Horizon text that has no weight control of its own."},
]
schema_settings += [
    {"type": "header", "content": "Product type label colour"},
    {"type": "color", "id": "product_type_color", "label": "Colour",
     "info": "Empty = graphite from the palette. The label text itself is each product's Type in Shopify admin > Products."},
    {"type": "header", "content": "Headline weight sweep"},
    {"type": "checkbox", "id": "sweep_on", "label": "Sweep weight across Arsenica Variable headlines", "default": True},
    {"type": "select", "id": "sweep_dir", "label": "Direction",
     "options": [{"value": "up", "label": "Light to heavy"}, {"value": "down", "label": "Heavy to light"}], "default": "down"},
    {"type": "range", "id": "sweep_min", "label": "Lightest", "min": 100, "max": 800, "step": 10, "default": 300},
    {"type": "range", "id": "sweep_max", "label": "Heaviest", "min": 100, "max": 800, "step": 10, "default": 450},
]
schema = {"name": "Wally Domo fonts and type", "class": "wd-type-section", "settings": schema_settings,
          "enabled_on": {"groups": ["header"]}}

css_calls = "\n".join(
    f"  {{%- render 'wd-type-el', s: s, el: 'st_{key}', prefix: '{key}' -%}}" for key, _l, _d, _r in STYLES
) + "\n" + "\n".join(
    f"  {{%- render 'wd-type-el', s: s, el: '{key}', vars: '{key}' -%}}" for key, _l, _d, _r in PRESETS
) + "\n" + "\n".join(
    f"  {{%- render 'wd-type-el', s: s, el: '{key}', sel: '{sel}' -%}}" for key, _l, sel, _d, _r in ELEMENTS
)

liquid = """{%- comment -%}
  WALLY DOMO: type for the parts of Horizon its own Typography panel can't reach.
  Our file. Lives in the header group so it loads on every page; renders no visible markup.
  Generated by wd-tools/gen_wd_type.py from Marc's saved Dawn values, 2026-10-22.
  Last regenerated 2026-10-22 22:40 (H1-H6 + body text with full controls; sign-up line).
  Each element: font, size, weight, line height, tracking (1/1000 em), case.
  Broadacre weight rule (Marc): under 450 = broadacre-regular-0, 450+ = broadacre-medium-0.
  Headline weight sweep = the Dawn wd-arsenica effect, ported (h1/h2 in Arsenica Variable).
{%- endcomment -%}
{%- assign s = section.settings -%}
<style>
  :root {
    --font-body--weight: 300;
    --font-subheading--weight: 500;
    --font-heading--weight: {{ s.w_arsenica_variable | default: 300 }};
    --font-accent--weight: {{ s.w_arsenica_text | default: 400 }};
    --font-body--style: normal;
    --font-subheading--style: normal;
    --font-heading--style: normal;
    --font-accent--style: normal;
  }
""" + css_calls + """
  html body .wd-type-eyebrow { margin: 0; color: {{ s.product_type_color | default: settings.color_palette.color1 | default: '#5E5A53' }}; }
  html body .wd-ed__eyebrow { color: {{ s.product_type_color | default: 'var(--wd-ed-graphite)' }}; }
  .wd-type-section { display: contents; }
</style>
{%- if s.sweep_on -%}
<style>
  html body .wd-grad__w, html body .wd-grad__c {
    font-family: inherit !important; font-size: inherit !important;
    line-height: inherit !important; letter-spacing: inherit !important;
  }
  html body .wd-grad__w { white-space: nowrap; }
  html body .wd-grad__c { font-weight: var(--w) !important; font-variation-settings: "wght" var(--w) !important; }
</style>
<script>
  (function () {
    var DIR = {{ s.sweep_dir | default: 'down' | json }};
    var MIN = {{ s.sweep_min | default: 300 }};
    var MAX = {{ s.sweep_max | default: 450 }};
    var SEL = 'main h1, main h2, [data-wd-sweep]';
    var SKIP = '.product-details, product-card, .resource-card, header, footer, .menu-drawer, .cart-drawer, .visually-hidden, .wd-sb';

    function num(v, fallback) {
      var n = parseInt(v, 10);
      return isNaN(n) ? fallback : Math.max(100, Math.min(800, n));
    }

    function apply(el) {
      if (el.dataset.wdGrad || el.closest(SKIP)) return;
      var dir = el.dataset.wdSweep || DIR;
      if (dir !== 'up' && dir !== 'down') return;
      var min = num(el.dataset.wdMin, MIN);
      var max = num(el.dataset.wdMax, MAX);
      if (!/arsenica-variable/i.test(getComputedStyle(el).fontFamily)) return;
      var walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
      var nodes = [], total = 0, n;
      while ((n = walker.nextNode())) {
        nodes.push(n);
        total += Array.from(n.nodeValue.replace(/\\s/g, '')).length;
      }
      if (total < 2) return;
      el.setAttribute('aria-label', el.textContent.replace(/\\s+/g, ' ').trim());
      var cap = getComputedStyle(el).textTransform === 'capitalize';
      var wordStart = true, i = 0;
      nodes.forEach(function (node) {
        var frag = document.createDocumentFragment();
        node.nodeValue.split(/(\\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\\s+$/.test(part)) { wordStart = true; frag.appendChild(document.createTextNode(part)); return; }
          var word = document.createElement('span');
          word.className = 'wd-grad__w';
          word.setAttribute('aria-hidden', 'true');
          if (cap) word.style.setProperty('text-transform', 'none', 'important');
          Array.from(part).forEach(function (ch) {
            var t = i / (total - 1);
            if (dir === 'down') t = 1 - t;
            if (cap) { ch = wordStart ? ch.toUpperCase() : ch; wordStart = false; }
            var c = document.createElement('span');
            c.className = 'wd-grad__c';
            if (cap) c.style.setProperty('text-transform', 'none', 'important');
            c.style.setProperty('--w', Math.round(min + (max - min) * t));
            c.textContent = ch;
            word.appendChild(c);
            i++;
          });
          frag.appendChild(word);
        });
        node.parentNode.replaceChild(frag, node);
      });
      el.dataset.wdGrad = dir;
    }

    function run(root) { (root || document).querySelectorAll(SEL).forEach(apply); }
    function start() {
      if (document.fonts && document.fonts.ready) { document.fonts.ready.then(function () { run(); }); } else { run(); }
    }
    if (document.readyState === 'loading') { document.addEventListener('DOMContentLoaded', start); } else { start(); }
    document.addEventListener('shopify:section:load', function (e) { run(e.target); });
  })();
</script>
{%- endif -%}

{% schema %}
""" + json.dumps(schema, indent=2, ensure_ascii=False) + """
{% endschema %}
"""

snippet = """{%- comment -%}
  WALLY DOMO: one element's full type rule for sections/wd-type.liquid.
  Params: s = section.settings, el = element key, and EITHER sel = CSS selector (writes a rule),
  OR prefix = text style key (writes --wd-st-<prefix>-* variables, read by wd-type-pick),
  OR vars = Horizon preset name (h1-h6, paragraph: writes Horizon's --font-<preset>--* variables).
  Optional <el>_phone setting = size on phones (fluid clamp, like Horizon's own).
  Font keys: body / broadacre (Regular under 450, Medium 450+), arsenica-variable(-italic),
  arsenica-text (snaps to 400 or 700).
{%- endcomment -%}
{%- liquid
  assign k_font = el | append: '_font'
  assign k_size = el | append: '_size'
  assign k_weight = el | append: '_weight'
  assign k_lh = el | append: '_lh'
  assign k_trk = el | append: '_tracking'
  assign k_case = el | append: '_case'
  assign font = s[k_font] | default: 'body'
  assign w = s[k_weight] | default: 400
  assign style = 'normal'
  case font
    when 'arsenica-variable'
      assign stack = 'var(--wd-font-arsenica)'
    when 'arsenica-variable-italic'
      assign stack = 'var(--wd-font-arsenica)'
      assign style = 'italic'
    when 'arsenica-text'
      assign stack = 'var(--wd-font-arsenica-text)'
      if w >= 550
        assign w = 700
      else
        assign w = 400
      endif
    else
      if w >= 450
        assign stack = 'var(--wd-font-broadacre-small)'
        assign w = 500
      else
        assign stack = 'var(--wd-font-broadacre)'
        assign w = 300
      endif
  endcase
  assign lh = s[k_lh] | default: 120 | divided_by: 100.0
  assign trk = s[k_trk] | default: 0 | divided_by: 1000.0
  assign size = s[k_size]
  assign k_phone = el | append: '_phone'
  assign phone = s[k_phone] | default: size
  if phone < size
    assign vw = size | times: 0.1
    capture size_css
      echo 'clamp(' | append: phone | append: 'px, ' | append: vw | append: 'vw, ' | append: size | append: 'px)'
    endcapture
  else
    assign size_css = size | append: 'px'
  endif
-%}
{%- if prefix != blank -%}
:root {
  --wd-st-{{ prefix }}-family: {{ stack }};
  --wd-st-{{ prefix }}-style: {{ style }};
  --wd-st-{{ prefix }}-weight: {{ w }};
  --wd-st-{{ prefix }}-size: {{ size_css }};
  --wd-st-{{ prefix }}-lh: {{ lh }};
  --wd-st-{{ prefix }}-trk: {{ trk }}em;
  --wd-st-{{ prefix }}-case: {{ s[k_case] | default: 'none' }};
}
{%- elsif vars != blank -%}
:root {
  --font-{{ vars }}--family: {{ stack }};
  --font-{{ vars }}--style: {{ style }};
  --font-{{ vars }}--weight: {{ w }};
  --font-{{ vars }}--size: {{ size_css }};
  --font-{{ vars }}--line-height: {{ lh }};
  --font-{{ vars }}--letter-spacing: {{ trk }}em;
  --font-{{ vars }}--case: {{ s[k_case] | default: 'none' }};
}
{%- else -%}
html body {{ sel }} {
  font-family: {{ stack }} !important;
  font-style: {{ style }} !important;
  font-size: {{ s[k_size] }}px !important;
  font-weight: {{ w }} !important;
  font-variation-settings: "wght" {{ w }};
  line-height: {{ lh }} !important;
  letter-spacing: {{ trk }}em !important;
  text-transform: {{ s[k_case] | default: 'none' }} !important;
}
{%- endif -%}
"""

pick = """{%- comment -%}
  WALLY DOMO: type for one text in a WD section. Generated by wd-tools/gen_wd_type.py.
  Params: s = settings (section or block), el = element key, sel = CSS selector.
  Reads s[el + '_style']: a text style key (set in Header > Wally Domo fonts and type) or 'custom'.
  Custom = the element's own six controls (snippets/wd-type-el).
{%- endcomment -%}
{%- assign wd_k = el | append: '_style' -%}
{%- assign wd_st = s[wd_k] | default: 'custom' -%}
{%- if wd_st == 'custom' -%}
  {%- render 'wd-type-el', s: s, el: el, sel: sel -%}
{%- else -%}
html body {{ sel }} {
  font-family: var(--wd-st-{{ wd_st }}-family) !important;
  font-style: var(--wd-st-{{ wd_st }}-style) !important;
  font-size: var(--wd-st-{{ wd_st }}-size) !important;
  font-weight: var(--wd-st-{{ wd_st }}-weight) !important;
  font-variation-settings: "wght" var(--wd-st-{{ wd_st }}-weight);
  line-height: var(--wd-st-{{ wd_st }}-lh) !important;
  letter-spacing: var(--wd-st-{{ wd_st }}-trk) !important;
  text-transform: var(--wd-st-{{ wd_st }}-case) !important;
}
{%- endif -%}
"""
with open(f"{repo}/snippets/wd-type-pick.liquid", "w") as f:
    f.write(pick)
with open(f"{repo}/wd-tools/styles.json", "w") as f:
    json.dump([{"key": k, "label": l, "d": d} for k, l, d, _r in STYLES], f, indent=1)

with open(f"{repo}/sections/wd-type.liquid", "w") as f:
    f.write(liquid)
with open(f"{repo}/snippets/wd-type-el.liquid", "w") as f:
    f.write(snippet)
print("wrote sections/wd-type.liquid and snippets/wd-type-el.liquid;",
      sum(1 for x in schema_settings if x.get("id")), "settings")
