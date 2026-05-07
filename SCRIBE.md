# Using Templates on Your Kindle Scribe

## The short version

Kindle Scribe does not support custom notebook templates, and older models do not support copying PDFs directly onto the device. The workflow is: **generate a PDF → give it a meaningful name → send it to your Kindle → open it as a notebook**.

---

## Step by step

### 1. Generate the PDF

```bash
python generate.py scorecard -o output/2026-05-06-mets-at-rockies.pdf
```

Use a descriptive filename — it becomes the document title on your device and is the primary way to tell scorecards apart. Kindle Scribe's document management is minimal, so good names do a lot of the work.

**Adding a cover page**

Pass `--cover` to prepend a styled title page with the teams, date, and ballpark. You can supply values inline or let the CLI prompt you:

```bash
# Fully inline (no prompts):
python generate.py scorecard \
  --cover title:"2026-05-06 Mets at Rockies" \
          visitor:Mets home:Rockies \
          date:2026-05-06 \
          ballpark:"Coors Field" \
  -o output/2026-05-06-mets-rockies.pdf

# Interactive (prompts for each field):
python generate.py scorecard --cover -o output/2026-05-06-mets-rockies.pdf
```

The cover becomes page 1 and makes it easy to identify the scorecard when you open it on device. Values containing spaces must be quoted.

Suggested naming schemes:

| Use case | Example filename |
|----------|-----------------|
| Baseball scorecard | `2026-05-06-mets-at-rockies.pdf` |
| Generic dated notebook | `2026-05-06-meeting-notes.pdf` |
| Recurring template | `2026-w19-weekly-review.pdf` |

Generated files land in `output/` by default.

### 2. Send to your Kindle

Amazon provides a **Send to Kindle** web uploader at:

**https://www.amazon.com/sendtokindle**

Sign in, drag in your PDF, and select your Kindle Scribe as the destination. It will appear in your library within a minute or two over Wi-Fi.

**Alternatives:**

- **Email** — every Kindle has a personal `@kindle.com` address (find it under *Manage Your Content and Devices → Devices → your Scribe → Personal Document Settings*). Attach the PDF and send from an approved sender address.
- **USB** — connect via USB-C, drag the PDF into the `documents/` folder on the device.

### 3. Open it as a notebook

On your Kindle Scribe, find the document in your library and open it. Tap the pencil icon to start annotating — all writing is stored as a layer on top of the PDF, leaving the template intact underneath.

---

## Document management

Kindle Scribe's on-device organisation is basic: you can create collections (folders) and pin favourites, but there is no bulk management or renaming. A few habits that help:

- **Name files before you send them.** Renaming after the fact means re-uploading.
- **Use date prefixes** (`YYYY-MM-DD`) so documents sort chronologically.
- **One PDF per use.** Reusing the same filename does not overwrite the old document — Amazon's cloud keeps both. Give every upload a unique name.
- **Archive finished documents** into a collection on-device, or simply delete them when you no longer need them.
- **Back up your annotations** via the Kindle app on a phone or tablet, which syncs the annotated PDF automatically.

---

## Tips

- PDFs render at full resolution on Kindle Scribe — these templates are sized to the device's native 1404 × 1872 px, so there is no scaling artefact.
- The default pen tool works well for filling in grid cells; the fineliner is good for small annotation text.
- If a template has multiple pages, swipe left/right to move between them just as you would any document.
