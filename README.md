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
| `crossword` | Cruza y Aprende | 1+2N | Spanish vocabulary crossword puzzles — cover page plus puzzle/solution pairs; difficulty controls grid size, vocabulary depth, and word count |
| `scorecard` | Baseball Scorecard | 6 (+1) | Full baseball scoring sheet — game header, summary, and four lineup pages; optional cover page |
| `weekly-activities` | Weekly Planner | 7+ | Daily planner — one page per day with task sections, hourly schedule, and brain dump; configurable start day and page count |
| `worklog` | Colorado MyUI Worklog | 3 | Colorado UI work-search activity log — 5 entries per page |
| `prompt-notebook` | Prompt Notebook | 5+ | Structured prompt writing notebook with CO-STAR+ or P.R.O.M.P.T. framework; configurable prompt count, compact/expanded layout |

### Cruza y Aprende — Spanish Crossword (`crossword`)

A Spanish vocabulary crossword puzzle notebook. Each notebook has a cover page followed by N puzzle pairs (puzzle page + solution page). Vocabulary is drawn from a curated 726-entry word list built from LinkedIn Learning Spanish Parts 1–4.

**Difficulty** controls grid size, word count, and vocabulary depth simultaneously:

| Difficulty | Grid | Words | Vocabulary |
|------------|------|-------|------------|
| Easy | 9×9 | 8 | Words, phrases, infinitives, present tense |
| Medium | 11×11 | 10 | Easy + preterite + imperfect |
| Hard | 15×15 | 15 | Medium + future + conditional + subjunctive + imperative |

```bash
# Default: 3 easy puzzles (9×9, 8 words each)
python generate.py crossword

# 5 hard puzzles (15×15, 15 words each)
python generate.py crossword --params difficulty:hard count:5

# Custom output path
python generate.py crossword --params difficulty:medium count:10 -o output/spanish-practice.pdf
```

Parameters are prompted interactively if omitted.

#### Updating the vocabulary list

The vocabulary is stored in `templates/crossword/vocabulary.json` — a flat list of words, phrases, and verbs committed to the repo. You can extend it in three ways:

**By hand:** Add entries directly to `vocabulary.json` following the schema. Set `"source": "added-by-user"`. Minimum fields:

```json
{ "id": "unique-id", "entry": "WORD", "type": "word", "definition": "english meaning",
  "tags": [], "source": "added-by-user" }
```

Verb entries require a `"conjugations"` object with all 7 tenses (`present`, `preterite`, `imperfect`, `future`, `conditional`, `subjunctive`, `imperative`), each mapping the 6 subjects (`yo`, `tú`, `él`, `nosotros`, `vosotros`, `ellos`) plus `usted`/`ustedes` for imperative.

**From an index file:** If you have an `index.json` source file (same format as the LinkedIn Learning export), re-derive `vocabulary.json` with:

```bash
python templates/crossword/prepare_vocab.py \
  --source /path/to/index.json \
  --out templates/crossword/vocabulary.json
```

**Validate any time:**

```bash
python templates/crossword/prepare_vocab.py --validate
```

This checks schema validity, flags duplicate entries, and reports entries shorter than 3 characters (which are skipped during puzzle generation).

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

### Weekly Planner (`weekly-activities`)

One page per day, cycling from a configurable start day. Each page includes a task column (TOP 3, TO-DO, and PERSONAL sections with checkboxes), an hourly schedule (5 am–9 pm), and a free-form Brain Dump area with a Vibe Check mood strip at the bottom.

| Page zone | Content |
|-----------|---------|
| Header | Day name bar |
| Left column | TOP 3 (3 rows), TO-DO (6 rows), PERSONAL (4 rows) — all with checkboxes |
| Right column | Hourly schedule, 5 am–9 pm (17 slots) |
| Brain Dump | Free-form writing area + Vibe Check mood strip |

```bash
# Default — 7 days starting Monday
python generate.py weekly-activities

# Custom start day and length
python generate.py weekly-activities --params first_day:Sunday days:14

# Custom output path
python generate.py weekly-activities --params first_day:Monday days:5 -o output/work-week.pdf
```

Parameters are prompted interactively if omitted.

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

### Prompt Notebook (`prompt-notebook`)

A configurable notebook for writing structured prompts. Choose from two frameworks and two layouts.

**Frameworks:**

| Framework | Components |
|-----------|------------|
| **CO-STAR+** | Context, Objective, Style, Tone, Audience, Response, Examples |
| **P.R.O.M.P.T.** | Persona, Request, Outline, Material, Preference, Test |

**Layouts:**

| Layout | Description |
|--------|-------------|
| **Compact** | Header fields + all framework components on a single page per prompt |
| **Expanded** (default) | Header on first page, then 2 components per page with generous writing space (~17 ruled lines each) |

The first page is always a framework overview reference. Each page gets a footer (`Page N — Overview` / `Page N — Prompt M`).

```bash
# Default: 1 prompt, expanded, CO-STAR+
python generate.py prompt-notebook

# 3 prompts, compact, CO-STAR+
python generate.py prompt-notebook --params count:3 layout:compact

# 2 prompts, expanded, P.R.O.M.P.T.
python generate.py prompt-notebook --params count:2 framework:prompt

# With cover page
python generate.py prompt-notebook --cover \
  --params count:2 layout:expanded framework:co-star

# Fully specified
python generate.py prompt-notebook \
  --cover title:"My Prompt Book" date:2026-05-13 \
  --params count:3 layout:compact framework:prompt \
  -o output/my-prompts.pdf
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
│   ├── crossword/            # Cruza y Aprende Spanish crossword template
│   │   ├── template.py       # METADATA + generate() + draw_cover()
│   │   ├── generator.py      # Word selection + backtracking grid placer
│   │   ├── clues.py          # Difficulty-gated candidate pool + clue strings
│   │   ├── conjugator.py     # Regular rules + irregular verb tables (47 verbs)
│   │   ├── renderer.py       # ReportLab: cover, puzzle page, solution page
│   │   ├── prepare_vocab.py  # Build/validate vocabulary.json from source
│   │   └── vocabulary.json   # 726-entry curated word list (committed)
│   ├── scorecard/            # Baseball scorecard template
│   │   ├── template.py       # METADATA + generate() + page drawing
│   │   └── utils.py          # Column/row constants and draw helpers
│   ├── weekly-activities/    # Daily planner template
│   │   └── template.py       # METADATA + generate() + page drawing
│   ├── worklog/              # Colorado MyUI worklog template
│   │   └── template.py       # METADATA + generate() + page drawing
│   └── prompt-notebook/      # Prompt notebook template
│       └── template.py       # METADATA + generate() + page drawing
├── output/                   # Generated PDFs (git-ignored)
└── tests/
    ├── conftest.py           # Shared pytest fixtures
    ├── test_pages.py         # Page-render and dimension tests
    └── test_utils.py         # Unit tests for drawing helpers
```

## Running tests

```bash
pytest tests/
```

## License

Copyright (C) 2026 Paul Monday. Licensed under the [GNU General Public License v3.0](LICENSE) or later.
