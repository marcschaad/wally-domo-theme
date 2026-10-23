"""Adds full type controls (font, size, weight, line height, tracking, case) to every text in
sections/wd-editions.liquid, sections/wd-studio-note.liquid and sections/wd-footer.liquid. Usage: python3 -I gen_wd_sections.py <repo>
Idempotent: strips a previous run (between the WD-TYPE markers) before writing."""
import json, re, sys
repo = sys.argv[1]
FONT_OPTIONS = [("body", "Broadacre (Regular; Medium at 450+)"), ("arsenica-variable", "Arsenica Variable"),
                ("arsenica-variable-italic", "Arsenica Variable Italic"), ("arsenica-text", "Arsenica Text")]
CASE_OPTIONS = [("none", "As typed"), ("uppercase", "All caps"), ("lowercase", "All lowercase"), ("capitalize", "Initial caps")]

def group(key, label, d, rng):
    font, size, weight, lh, trk, case = d
    return [
        {"type": "header", "content": label},
        {"type": "select", "id": f"{key}_font", "label": "Font", "options": [{"value": v, "label": l} for v, l in FONT_OPTIONS], "default": font},
        {"type": "range", "id": f"{key}_size", "label": "Size", "min": rng[0], "max": rng[1], "step": 1, "unit": "px", "default": size},
        {"type": "range", "id": f"{key}_weight", "label": "Weight", "min": 100, "max": 900, "step": 50, "default": weight,
         "info": "Broadacre: under 450 = Regular, 450+ = Medium. Arsenica Text: 400 or 700."},
        {"type": "range", "id": f"{key}_lh", "label": "Line height", "min": 70, "max": 200, "step": 5, "unit": "%", "default": lh},
        {"type": "range", "id": f"{key}_tracking", "label": "Tracking", "min": -100, "max": 300, "step": 5, "default": trk, "info": "1/1000 em, as in Illustrator."},
        {"type": "select", "id": f"{key}_case", "label": "Case", "options": [{"value": v, "label": l} for v, l in CASE_OPTIONS], "default": case},
    ]

SPECS = {
  "sections/wd-editions.liquid": {
    "drop": ["heading_italic", "heading_size", "title_size"],
    "groups": [  # key, label, defaults, size range, selector (inside the section), insert before setting id
      ("ty_heading", "Heading type", ("arsenica-variable-italic", 48, 300, 105, -5, "none"), (20, 120), ".wd-ed__heading", "series_color"),
      ("ty_intro", "Intro text type", ("body", 14, 300, 140, 0, "none"), (10, 32), ":is(.wd-ed__lede, .wd-ed__lede *)", "series_color"),
      ("ty_title", "Print title type", ("arsenica-text", 24, 400, 120, 0, "none"), (12, 60), ".wd-ed__title", "space_top"),
      ("ty_note", "Note type", ("arsenica-variable-italic", 15, 300, 140, 0, "none"), (10, 28), ".wd-ed__note", "space_top"),
      ("ty_edition", "Edition line type", ("body", 12, 500, 120, 60, "uppercase"), (8, 24), ".wd-ed__edition", "space_top"),
      ("ty_price", "Price type", ("body", 14, 600, 130, 35, "none"), (8, 32), ".wd-ed__price", "space_top"),
    ],
    "insert_header_before": {"space_top": None},
  },
  "sections/wd-studio-note.liquid": {
    "drop": ["heading_size"],
    "groups": [
      ("ty_eyebrow", "Small line type", ("body", 12, 500, 120, 60, "uppercase"), (8, 24), ".wd-note__eyebrow", "show_signup"),
      ("ty_heading", "Heading type", ("arsenica-variable", 40, 300, 110, 0, "none"), (16, 96), ".wd-note__heading", "show_signup"),
      ("ty_text", "Text type", ("body", 14, 300, 140, 0, "none"), (10, 28), ":is(.wd-note__text, .wd-note__text *)", "show_signup"),
      ("ty_link", "Link type", ("body", 14, 300, 140, 0, "none"), (10, 28), ".wd-note__link", "space_top"),
    ],
  },
  "sections/wd-footer.liquid": {
    "drop": [],
    "note": False,
    "groups": [
      ("ty_top", "Byline small line type", ("body", 12, 500, 120, 80, "uppercase"), (8, 24), ".wd-ft__top", "col1_heading"),
      ("ty_name", "Byline name type", ("body", 30, 300, 100, -10, "none"), (14, 72), ".wd-ft__name", "col1_heading"),
      ("ty_line", "Studio line type", ("arsenica-variable-italic", 17, 300, 135, 0, "none"), (10, 36), ".wd-ft__line", "col1_heading"),
      ("ty_head", "Column heading type", ("body", 11, 500, 120, 100, "uppercase"), (8, 24), ".wd-ft__head", "show_pig"),
      ("ty_link", "Link type", ("body", 15, 300, 150, 0, "none"), (10, 28), ":is(.wd-ft__link, .wd-ft__link *)", "show_pig"),
      ("ty_cap", "Pig caption type", ("body", 10, 500, 120, 100, "uppercase"), (8, 20), ".wd-ft__cap", "copyright_name"),
      ("ty_small", "Small print type", ("body", 12, 300, 140, 10, "none"), (8, 20), ":is(.wd-ft__small, .wd-ft__small *)", "bg_color"),
    ],
  },
}
NOTE = {"type": "paragraph", "content": "Product type label, buttons and email fields follow the site-wide styles in Header > Wally Domo fonts and type, so they match everywhere."}

for path, spec in SPECS.items():
    f = f"{repo}/{path}"
    src = open(f).read()
    src = re.sub(r"\n?\{%- comment -%\}WD-TYPE START.*?WD-TYPE END\{%- endcomment -%\}\n?", "\n", src, flags=re.S)
    m = re.search(r"\{% schema %\}(.*)\{% endschema %\}", src, re.S)
    schema = json.loads(m.group(1))
    st = [x for x in schema["settings"] if x.get("id") not in spec["drop"] and not str(x.get("id", "")).startswith("ty_") and x is not None]
    st = [x for x in st if not (x.get("type") == "paragraph" and x.get("content") == NOTE["content"])]
    labels = [g[1] for g in spec["groups"]]
    st = [x for x in st if not (x.get("type") == "header" and x.get("content") in labels)]
    for key, label, d, rng, sel, before in spec["groups"]:
        idx = next(i for i, x in enumerate(st) if x.get("id") == before)
        # land before the header that opens `before`'s group
        while idx > 0 and st[idx - 1].get("type") == "header" and st[idx-1].get("content") not in [g[1] for g in spec["groups"]]:
            idx -= 1
        st[idx:idx] = group(key, label, d, rng)
    if spec.get("note", True):
        st.append(NOTE)
    schema["settings"] = st
    calls = "\n".join(f"  {{%- render 'wd-type-el', s: section.settings, el: '{k}', sel: wd_sel_{k} -%}}" for k, *_ in spec["groups"])
    assigns = "\n".join(f"  assign wd_sel_{k} = wd_scope | append: ' {sel}'" for k, _l, _d, _r, sel, _b in spec["groups"])
    block = ("{%- comment -%}WD-TYPE START (generated by gen_wd_sections.py){%- endcomment -%}\n"
             "{%- liquid\n  assign wd_scope = '#shopify-section-' | append: section.id\n" + assigns + "\n-%}\n<style>\n" + calls +
             "\n</style>\n{%- comment -%}WD-TYPE END{%- endcomment -%}")
    src = src[:m.start()] + block + "\n\n{% schema %}\n" + json.dumps(schema, indent=2, ensure_ascii=False) + "\n{% endschema %}\n"
    src = re.sub(r"\n{3,}", "\n\n", src)
    open(f, "w").write(src)
    print(path, len([x for x in st if x.get("id")]), "settings")
