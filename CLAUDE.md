# CLAUDE.md — Kindle Template Generator

## What this project is

A Python / ReportLab toolkit that generates multi-page PDF templates sized for the **Kindle Scribe** e-ink tablet. Templates are self-contained modules discovered automatically by the CLI (`generate.py`).

## Page dimensions

All templates share the same page size, defined in `core/dimensions.py`:

| Constant | Value | Notes |
|----------|-------|-------|
| `PAGE_W` | 336.96 pt | 1404 px ÷ 300 DPI × 72 pt/in |
| `PAGE_H` | 449.28 pt | 1872 px ÷ 300 DPI × 72 pt/in |
| `MARGIN` | 6 pt | applied on all four sides |

ReportLab's coordinate origin is **bottom-left**; y increases upward. All drawing uses built-in Helvetica / Helvetica-Bold — no font files needed.

## Adding a template

Every template lives in `templates/<name>/template.py` and must export:

```python
METADATA = {
    "name":        str,   # shown in the menu
    "description": str,   # one-line summary
    "output":      str,   # default PDF filename
    "pages":       int,
}

def generate(output_path: str) -> None: ...
```

`generate.py` auto-discovers templates by scanning `templates/` for directories that contain `template.py`.

### Cover page support (optional)

Templates opt into cover pages by adding three things:

1. **`"cover_fields"`** in `METADATA` — list of `{"name", "prompt", "default"}` dicts defining what the CLI prompts for:
   ```python
   "cover_fields": [
       {"name": "title",   "prompt": "Document title", "default": "My Template"},
       {"name": "visitor", "prompt": "Visiting team",  "default": ""},
   ]
   ```

2. **`draw_cover(c, **meta)`** — draws the cover page using `c` (a ReportLab canvas). Absorb unknown keys with `**_`.

3. **`generate(output_path, **meta)`** — if `meta` is non-empty, call `draw_cover(c, **meta)` then `c.showPage()` before the rest of the pages.

`generate.py` handles `--cover` CLI parsing, interactive prompts, and calls `core.thumbnail.embed_cover_thumbnail` automatically. Templates without `cover_fields` are unaffected.

## Shared modules

- **`core/dimensions.py`** — page size constants only; import these into every template
- **`core/style.py`** — fonts, line weights, grayscale fills, RGB colors; shared visual language across templates

Template-specific helpers (column widths, custom drawing functions, domain constants) belong inside the template's own directory and should not leak into `core/`.

## Current templates

### `scorecard` — Baseball Scorecard (6 pages)

| Page | Content |
|------|---------|
| 1 | Game header: info grid + field-positions diagram + instructions |
| 2 | Game summary (SUMS, pitchers, catchers, umpires) + scoring reference |
| 3–4 | Visiting / Home team lineup pages |
| 5–6 | Extra lineup pages (extra innings / batting around) |

Key files:
- `templates/scorecard/template.py` — all page-drawing functions + `METADATA` + `generate()`
- `templates/scorecard/utils.py` — column/row constants, `draw_diamond()`, `col_x_positions()`; re-exports `core` constants so template code only needs `import utils as U`

#### Lineup page layout (pages 3–6)

```
ROW_TEAM_LABEL   18 pt   "Team:" label
ROW_HEADER       12 pt   column headers (#, Line Up, Pos, 1–10, AB, R, H, RBI)
ROW_STARTER × 9  30 pt   starter batter rows with scoring diamonds
DIVIDER_H         4 pt   dashed "substitutes" line
ROW_SUB × 4      20.5 pt substitute batter rows
INNING TOTALS    15 pt   R/H/E/L subgrid + inning cells
PITCHER header    9 pt   L/R, No, Pitcher, ERA, IP, H, R, ER, BB, SO, HR, P, BF
PITCHER rows × 3  9 pt   blank pitcher data rows
```

Total ≈ 449 pt, leaving ~0.3 pt slack within the page height.

## CLI

```bash
python generate.py                  # interactive menu
python generate.py scorecard        # direct generation
python generate.py scorecard -o path/to/file.pdf
python generate.py --list
```

Output goes to `output/` by default (git-ignored).

## Tests

```bash
pytest tests/
```

- `tests/test_pages.py` — render and page-count checks for each scorecard page
- `tests/test_utils.py` — unit tests for `draw_diamond`, column positions, dimension constants
