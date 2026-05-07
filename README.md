# Kindle Template Generator

A Python toolkit for generating multi-page PDF templates sized for the **Kindle Scribe** (1404 × 1872 px at 300 DPI). Each template is a self-contained module — pick the one you want, generate it, and load the PDF onto your device.

Once generated, see **[SCRIBE.md](SCRIBE.md)** for how to get the PDF onto your device and use it as a notebook.

## Quick start

```bash
pip install -r requirements.txt
python generate.py
```

The interactive menu lists all available templates. Select one to generate a PDF into `output/`.

## Usage

```bash
# Interactive selector
python generate.py

# Generate a specific template
python generate.py scorecard

# Generate with a cover page (interactive prompts)
python generate.py scorecard --cover

# Generate with a cover page (inline values)
python generate.py scorecard --cover visitor:Mets home:Rockies date:2026-05-06

# Custom output path
python generate.py scorecard -o ~/Desktop/game.pdf

# List available templates
python generate.py --list
```

Generated PDFs land in `output/` by default (git-ignored).

## Available templates

| Key | Name | Pages | Description |
|-----|------|-------|-------------|
| `scorecard` | Baseball Scorecard | 6 (+1) | Full baseball scoring sheet — game header, summary, and four lineup pages; optional cover page |
| `worklog` | Colorado MyUI Worklog | 3 | Colorado UI work-search activity log — 5 entries per page |

### Baseball Scorecard (`scorecard`)

Six pages sized for Kindle Scribe:

| Page | Content |
|------|---------|
| 1 | Game header: info grid, field-positions diagram, instructions |
| 2 | Game summary: inning totals, pitchers, catchers, umpires, scoring reference |
| 3–4 | Visiting / Home team lineup pages |
| 5–6 | Extra lineup pages (extra innings / batting around) |

**Cover page** (optional, adds page 0):

```bash
# Interactive — prompts for title, teams, date, ballpark
python generate.py scorecard --cover

# Fully inline — no prompts
python generate.py scorecard \
  --cover title:"2026-05-06 Mets at Rockies" \
          visitor:Mets home:Rockies \
          date:2026-05-06 \
          ballpark:"Coors Field" \
  -o output/2026-05-06-mets-rockies.pdf
```

The cover page renders as page 1 of the PDF and helps identify scorecards in Kindle's library. Values containing spaces must be quoted.

### Colorado MyUI Worklog (`worklog`)

Three identical pages, each containing a title, subtitle, column headers, and five blank work-search activity rows. Matches the Colorado MyUI recommended work-search activity log format.

Each row has columns for:

| Column | Content |
|--------|---------|
| Date | MM/DD/YY — written by hand |
| Activity Completed | Two checkbox columns: Submit Application, Submit Resume, Interview, Test/Exam, Job Board / Referral, Networking, Reemployment Service, Skills Development, Other |
| Completed Activity Details | Blank — employer name, address, phone, email, website, class or event info |
| Name & Title of Person Contacted or Confirmation Number | Blank — written by hand |
| How Contacted | Checkboxes: In Person, Phone/Fax, Mail, Email, Web Site |
| Work Sought or Skills Developed | Blank — written by hand |

```bash
python generate.py worklog
python generate.py worklog -o output/2026-w19-worklog.pdf
```

## Adding a new template

1. **Create a subdirectory** under `templates/`:
   ```
   templates/my_template/
   ├── __init__.py
   └── template.py
   ```

2. **Define `METADATA` and `generate()`** in `template.py`:
   ```python
   from reportlab.pdfgen import canvas as rl_canvas
   from core import dimensions as D

   METADATA = {
       "name":        "My Template",
       "description": "One-line description shown in the menu",
       "output":      "my_template.pdf",   # default filename
       "pages":       1,
   }

   def generate(output_path: str) -> None:
       c = rl_canvas.Canvas(output_path, pagesize=(D.PAGE_W, D.PAGE_H))
       # draw your pages here, call c.showPage() between pages
       c.save()
   ```

3. **Run** `python generate.py --list` to confirm it appears in the menu.

### Shared resources

| Module | What it provides |
|--------|-----------------|
| `core/dimensions.py` | `PAGE_W`, `PAGE_H`, `MARGIN` — Kindle Scribe page size in points |
| `core/style.py` | Fonts, line weights, grayscale fills, RGB color tuples |

Template-specific helpers (column widths, custom drawing functions, etc.) belong inside the template's own directory.

## Project structure

```
.
├── generate.py               # CLI entry point
├── core/
│   ├── dimensions.py         # Kindle Scribe page dimensions
│   └── style.py              # Shared visual constants
├── templates/
│   └── scorecard/            # Baseball scorecard template
│       ├── template.py       # METADATA + generate() + page drawing
│       └── utils.py          # Column/row constants and draw helpers
├── output/                   # Generated PDFs (git-ignored)
└── tests/
    ├── test_pages.py         # Page-render and dimension tests
    └── test_utils.py         # Unit tests for drawing helpers
```

## Running tests

```bash
pytest tests/
```

## License

Copyright (C) 2026 Paul Monday. Licensed under the [GNU General Public License v3.0](LICENSE) or later.
