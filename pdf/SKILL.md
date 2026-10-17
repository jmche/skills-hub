---
name: pdf
description: Use this skill whenever the user wants to do anything with PDF files. This includes reading or extracting text/tables from PDFs, combining or merging multiple PDFs into one, splitting PDFs apart, rotating pages, adding watermarks, creating new PDFs, filling PDF forms, encrypting/decrypting PDFs, extracting images, and OCR on scanned PDFs to make them searchable. If the user mentions a .pdf file or asks to produce one, use this skill.
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

This guide covers essential PDF processing operations using Python libraries and command-line tools. For advanced features, JavaScript libraries, and detailed examples, see reference.md. If you need to fill out a PDF form, read forms.md and follow its instructions.

## Ready-made scripts

Most tasks have a tested CLI in `scripts/`. Prefer it over writing new code; drop to the library examples further down only for what the scripts do not cover. The `pdf_*.py` scripts support `--help`, read and write JSON as UTF-8, print JSON results to stdout, and exit non-zero on failure; their page arguments are 1-based (`1-3,5,9-`). Paths are relative to this skill's directory.

Requirements: Python 3.10+ with `pypdf`, `reportlab`, `pdfplumber` and `Pillow`. Rendering a real page (`pdf_page_image.py`, form overlays with `--pdf`) also needs `pypdfium2` or Poppler's `pdftoppm`; without either it reports `{"rendered": false, "missing": [...]}` and exits 0. A form overlay without `--pdf` is drawn on a blank page and needs Pillow only.

| Task | Command |
|---|---|
| Inspect first: page count, sizes, encrypted, likely-scanned pages | `python scripts/pdf_read.py f.pdf --meta` |
| Per-page text | `python scripts/pdf_read.py f.pdf --text` |
| Tables to JSON (+ CSV files) | `python scripts/pdf_read.py f.pdf --tables --csv-dir tables/` |
| List form fields with types and values | `python scripts/pdf_read.py f.pdf --fields` |
| Create a document (headings, paragraphs, tables, images, page breaks; page numbers added) | `python scripts/pdf_create.py spec.json -o out.pdf` |
| Merge, one bookmark per source | `python scripts/pdf_merge.py a.pdf b.pdf -o merged.pdf --bookmarks` |
| Extract pages, rotate, compress | `python scripts/pdf_split.py f.pdf --pages 1-3,7 -o part.pdf --rotate 90 --compress` |
| Overlay a one-page stamp PDF on every page | `python scripts/pdf_watermark.py f.pdf --stamp mark.pdf -o out.pdf [--under]` |
| Stamp text or an image at coordinates | `python scripts/pdf_stamp.py f.pdf -o out.pdf --text "DRAFT" --x 150 --y 400 --font-size 60 --rotation 45 --opacity 0.3 --color "#cc0000" [--pages 1-3]` · `--image sig.png --x 400 --y 60 --width 120` |
| Pages to PNG | `python scripts/pdf_page_image.py f.pdf --pages 1-3 --dpi 150 --out-dir imgs/` |
| Set or clear DocInfo metadata | `python scripts/pdf_meta.py f.pdf --set-meta --title "T" --author "A" -o out.pdf` · `--clear-meta` |
| Embedded file attachments | `python scripts/pdf_meta.py f.pdf --attach data.csv -o out.pdf` · `--list-attachments` · `--extract-attachments dir/` |
| Encrypt (AES-256) with distinct open and owner passwords / decrypt | `python scripts/pdf_secure.py f.pdf --encrypt -o enc.pdf --user-password "$PDF_PW" --owner-password "$PDF_OWNER_PW"` · `--decrypt -o dec.pdf --password "$PDF_PW"` |
| Build a new fillable form | lint `python scripts/pdf_form_layout.py spec.json`, then `python scripts/pdf_make_form.py spec.json -o form.pdf` — see `references/form-building.md` |
| Fill an existing form | follow forms.md (fillable fields and forms without fields) |
| Fill an AcroForm and flatten it | `python scripts/pdf_fill_form.py form.pdf --fields-json values.json -o filled.pdf --flatten` |
| Text extraction to Markdown, tables, images (text layer only) | `references/ocr-extraction.md` → `scripts/extract_pymupdf.py` |
| Scanned / image-only pages, OCR, equations, complex layout | `references/ocr-extraction.md` → `scripts/extract_marker.py` |
| Change text inside an existing PDF by instruction | `references/nano-pdf-editing.md` (external `nano-pdf` CLI, needs an LLM API key) |

Procedure:

1. Run `pdf_read.py --meta` first. If `encrypted` is true, decrypt before anything else. If `likely_scanned_pages` is non-empty, those pages have no text layer: render them with `pdf_page_image.py --dpi 300` and follow `references/ocr-extraction.md`. Never report empty extracted text as "no content".
2. After any change, re-run `pdf_read.py --meta` (page count, rotation) or `--fields` (filled values, compared exactly, including non-ASCII). For anything visual — stamps, watermarks, flattened forms, form layout — render the page with `pdf_page_image.py` and look at it.
3. Pass passwords through environment variables, as in the table, so they stay out of shell history. Without `--owner-password` the owner password equals the open password.
4. Filling forms: forms.md is the route for every existing form. Use `pdf_fill_form.py` only when the result must be flattened; its values follow the table in `references/form-building.md` (checkboxes `true`/`false`, radio values with the leading slash such as `"/red"`), which differs from the `checked_value` format in forms.md. It sets the AcroForm `NeedAppearances` flag so viewers regenerate field appearances; some minimal viewers ignore it, so flatten when the display must be exact.

Pitfalls:

- **Permission flags are not security.** Owner-password bits (no-print, no-copy) are requests that any library can strip; only the user password encrypts content.
- **`--compress` only deflates content streams** (typically 0–20%). It does not downsample images; that needs Ghostscript.
- **Flattening** converts widget appearances to page content. Plain text fields and checkboxes are reliable; rich-text fields, custom appearance streams and radio groups can drop or misrender — check the rendered page.
- **Non-Latin form values** are stored correctly, but the field's font may lack the glyphs, so a viewer can show blanks. Verify with `--fields`, not only by eye.
- **Rotated stamp text** extracts as scrambled letters through pdfplumber; check it with pypdf `extract_text()` or a rendered image.
- **`pdf_meta.py` writes the DocInfo dictionary only**; XMP metadata stays untouched and some viewers show it instead.
- **PDF/A** cannot be produced or validated with pypdf/reportlab. Use Ghostscript (`-dPDFA=2`) and validate with veraPDF.
- Table extraction is heuristic: borderless or merged-cell tables may need `table_settings` tuning in pdfplumber.

## Quick Start

```python
from pypdf import PdfReader, PdfWriter

# Read a PDF
reader = PdfReader("document.pdf")
print(f"Pages: {len(reader.pages)}")

# Extract text
text = ""
for page in reader.pages:
    text += page.extract_text()
```

## Python Libraries

### pypdf - Basic Operations

#### Merge PDFs
```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

#### Split PDF
```python
reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

#### Extract Metadata
```python
reader = PdfReader("document.pdf")
meta = reader.metadata
print(f"Title: {meta.title}")
print(f"Author: {meta.author}")
print(f"Subject: {meta.subject}")
print(f"Creator: {meta.creator}")
```

#### Rotate Pages
```python
reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### pdfplumber - Text and Table Extraction

#### Extract Text with Layout
```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

#### Extract Tables
```python
with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for j, table in enumerate(tables):
            print(f"Table {j+1} on page {i+1}:")
            for row in table:
                print(row)
```

#### Advanced Table Extraction
```python
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:  # Check if table is not empty
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### reportlab - Create PDFs

#### Basic PDF Creation
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
width, height = letter

# Add text
c.drawString(100, height - 100, "Hello World!")
c.drawString(100, height - 120, "This is a PDF created with reportlab")

# Add a line
c.line(100, height - 140, 400, height - 140)

# Save
c.save()
```

#### Create PDF with Multiple Pages
```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

# Build PDF
doc.build(story)
```

#### Subscripts and Superscripts

**IMPORTANT**: Never use Unicode subscript/superscript characters (₀₁₂₃₄₅₆₇₈₉, ⁰¹²³⁴⁵⁶⁷⁸⁹) in ReportLab PDFs. The built-in fonts do not include these glyphs, causing them to render as solid black boxes.

Instead, use ReportLab's XML markup tags in Paragraph objects:
```python
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

styles = getSampleStyleSheet()

# Subscripts: use <sub> tag
chemical = Paragraph("H<sub>2</sub>O", styles['Normal'])

# Superscripts: use <super> tag
squared = Paragraph("x<super>2</super> + y<super>2</super>", styles['Normal'])
```

For canvas-drawn text (not Paragraph objects), manually adjust font the size and position rather than using Unicode subscripts/superscripts.

## Command-Line Tools

### pdftotext (poppler-utils)
```bash
# Extract text
pdftotext input.pdf output.txt

# Extract text preserving layout
pdftotext -layout input.pdf output.txt

# Extract specific pages
pdftotext -f 1 -l 5 input.pdf output.txt  # Pages 1-5
```

### qpdf
```bash
# Merge PDFs
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf
qpdf input.pdf --pages . 6-10 -- pages6-10.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1  # Rotate page 1 by 90 degrees

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf
```

### pdftk (if available)
```bash
# Merge
pdftk file1.pdf file2.pdf cat output merged.pdf

# Split
pdftk input.pdf burst

# Rotate
pdftk input.pdf rotate 1east output rotated.pdf
```

## Common Tasks

### Extract Text from Scanned PDFs
```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark
```python
from pypdf import PdfReader, PdfWriter

# Create watermark (or load existing)
watermark = PdfReader("watermark.pdf").pages[0]

# Apply to all pages
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Extract Images
```bash
# Using pdfimages (poppler-utils)
pdfimages -j input.pdf output_prefix

# This extracts all images as output_prefix-000.jpg, output_prefix-001.jpg, etc.
```

### Password Protection
```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

# Add password
writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Quick Reference

| Task | Best Tool | Command/Code |
|------|-----------|--------------|
| Merge PDFs | pypdf | `writer.add_page(page)` |
| Split PDFs | pypdf | One page per file |
| Extract text | pdfplumber | `page.extract_text()` |
| Extract tables | pdfplumber | `page.extract_tables()` |
| Create PDFs | reportlab | Canvas or Platypus |
| Command line merge | qpdf | `qpdf --empty --pages ...` |
| OCR scanned PDFs | pytesseract | Convert to image first |
| Fill PDF forms | pdf-lib or pypdf (see forms.md) | See forms.md |

## Next Steps

- For advanced pypdfium2 usage, see reference.md
- For JavaScript libraries (pdf-lib), see reference.md
- If you need to fill out a PDF form, follow the instructions in forms.md
- For troubleshooting guides, see reference.md

## Sources

`scripts/pdf_*.py`, `scripts/extract_pymupdf.py`, `scripts/extract_marker.py`, `scripts/_raster.py`, `references/` and `tests/` come from [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) under the MIT License (`LICENSE-HERMES.txt`). The rest of this skill is covered by `LICENSE.txt`.
