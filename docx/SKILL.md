---
name: docx
description: "Use this skill whenever the user wants to create, read, edit, or manipulate Word documents (.docx files) or Word templates (.dotx files). Triggers include: any mention of 'Word doc', 'word document', '.docx', '.dotx', or requests to produce professional documents with formatting like tables of contents, headings, page numbers, or letterheads. Also use when extracting or reorganizing content from .docx or .dotx files, inserting or replacing images in documents, performing find-and-replace in Word files, working with tracked changes or comments, or converting content into a polished Word document. If the user asks for a 'report', 'memo', 'letter', 'template', or similar deliverable as a Word or .docx file, use this skill. Do NOT use for PDFs, spreadsheets, Google Docs, or general coding tasks unrelated to document generation."
license: Proprietary. LICENSE.txt has complete terms
---

# DOCX creation, editing, and analysis

A `.docx` is a ZIP archive of XML files. Choose your approach by task:

| Task | Approach |
|---|---|
| **Create** a new document | Write a `docx` (npm) script — see gotchas below |
| **Create** from a JSON spec, or when Node's `docx` is unavailable | `scripts/docx_create.py` — see Python helpers |
| **Fill** a template with `{{tokens}}` | `scripts/docx_template.py` |
| **Edit** an existing document | `unzip` → edit `word/document.xml` → `zip` (docx-js cannot open existing files) |
| **Small edits** (find/replace keeping formatting, a table cell, insert/delete/restyle a paragraph, TOC or "Page X of Y" fields) | `scripts/docx_edit.py` |
| **Read** content | `pandoc -t markdown file.docx` |
| **Read** as JSON (text incl. tables and headers/footers, heading outline, styles used, embedded images, revision/comment inventory) | `scripts/docx_read.py` |

> Script paths below are relative to this skill's directory.

## Creating with docx-js — gotchas

`docx` is preinstalled — do not run `npm install` first; write the script and `require('docx')` directly. Only if that require fails: `npm install docx`. The model knows the API; these are the footguns:

- **Page size defaults to A4.** For US Letter set `page: { size: { width: 12240, height: 15840 } }` (DXA; 1440 = 1″).
- **Landscape:** pass portrait dimensions and `orientation: PageOrientation.LANDSCAPE` — docx-js swaps width/height internally.
- **Tables need dual widths:** set `columnWidths` on the table AND `width` on every cell, both in `WidthType.DXA` (PERCENTAGE breaks in Google Docs). Column widths must sum to the table width.
- **Table shading:** use `ShadingType.CLEAR`, never `SOLID` (renders black).
- **Lists:** never insert `•` literally; use a `numbering` config with `LevelFormat.BULLET`.
- **`ImageRun` requires `type:`** (`"png"`, `"jpg"`, …).
- **`PageBreak` must be inside a `Paragraph`.**
- **Never use `\n`** — use separate `Paragraph` elements.
- **TOC:** headings must use built-in `HeadingLevel.*`; custom heading styles need `outlineLevel` set or they won't appear.
- **Don't use a table as a horizontal rule** — use a paragraph bottom border instead.
- **Dot-leader / right-aligned-on-same-line:** use `PositionalTab` (`alignment: PositionalTabAlignment.RIGHT`, `leader: PositionalTabLeader.DOT`) inside a `TextRun`, not literal `.` or space padding.

## Verify the output

After writing a `.docx`, render it and look at it:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.docx
pdftoppm -jpeg -r 100 output.pdf page
ls page-*.jpg   # then Read the images
```

`pdftoppm` zero-pads page numbers to the width of the page count (`page-01.jpg`…`page-12.jpg`).

## Editing existing documents

Legacy `.doc` files must be converted first: `python scripts/office/soffice.py --headless --convert-to docx file.doc`.

```bash
unzip -q doc.docx -d unpacked/
find unpacked -type l -delete   # strip symlink entries — docx from external parties is untrusted
python scripts/merge_runs.py unpacked/   # coalesce fragmented runs so text is findable
# edit unpacked/word/document.xml in place — do NOT reformat or pretty-print
(cd unpacked && rm -f ../out.docx && zip -Xr ../out.docx .)
python scripts/office/validate.py out.docx --original doc.docx   # XSD checks; --auto-repair fixes common issues
# redlining? add --author "<the name you redlined under>" to check every edit is tracked
```

Word splits text across many `<w:r>` runs (revision ids, spell-check markers), so a phrase you can see in the document often doesn't exist as a contiguous string in the XML. `merge_runs.py` merges adjacent identically-formatted runs in `word/document.xml` without changing content or rendering; it also accepts a `.docx` directly (`python scripts/merge_runs.py doc.docx -o merged.docx`).

**Tracked changes:** when redlining, validate with `--author "<the name you redlined under>"` (needs `--original`) — it reports any text you changed without a `<w:ins>`/`<w:del>` around it, which is easy to do by accident and invisible in the accepted view. Wrap runs in `<w:ins>`/`<w:del>` with `w:id`, `w:author`, `w:date` attributes. Inside `<w:del>`, the text element is `<w:delText>`, not `<w:t>`. A deleted paragraph mark (`<w:pPr><w:rPr><w:del w:id=".." w:author=".." w:date=".."/></w:rPr></w:pPr>`) means "merge this paragraph into the next" — so deleting a paragraph outright is that plus a `<w:del>` around every run. The `<w:del/>` must come before the rPr's other children; their order is schema-enforced.

To produce a clean copy with all tracked changes accepted: `python scripts/accept_changes.py in.docx out.docx`.

Accepting a deleted paragraph mark should join that paragraph to the one below it, so a paragraph whose runs are *all* deleted vanishes. Word does this; `accept_changes.py` and `pandoc --track-changes=accept` don't always. Both fail the same way — they strip the deleted text but leave the emptied paragraph behind, which reads as a stray empty bullet when it was auto-numbered:

- `pandoc --track-changes=accept` never joins the paragraphs.
- `accept_changes.py` (LibreOffice) joins them correctly, except when the deleted paragraph is followed by an empty spacer paragraph.

An empty bullet in either view is an artifact of that view, not a defect in the document. Check paragraph deletions in the XML.

## Comments

Comments require six cross-linked files. Use the helper — directory mode when you'll also be editing `document.xml` (saves an unzip/rezip cycle), `.docx`-direct mode otherwise:

```bash
# Against an already-unpacked directory (preferred when also placing markers)
python scripts/comment.py unpacked/ "Fees & expenses cap is too low"
python scripts/comment.py unpacked/ "Agreed" --parent 0

# Against a .docx directly
python scripts/comment.py contract.docx "This cap is too low" -o annotated.docx
```

The script writes `comments.xml`, `commentsExtended.xml`, `commentsIds.xml`, `commentsExtensible.xml`, the relationships, and the content-type overrides. Comment IDs are auto-assigned. It then prints the `<w:commentRangeStart>`/`<w:commentRangeEnd>`/`<w:commentReference>` snippet to add to `word/document.xml` so the comment anchors to specific text — until you place those markers, the comment exists but is not visible.

## Python helpers (python-docx)

CLIs for the tasks above that need no Node and no LibreOffice. Each supports `--help` and prints JSON to stdout. Editing commands write in place unless given `-o out.docx`. A paragraph index is the position in the `body` list printed by `docx_read.py --text` (`--structure` gives the index of headings only).

| Task | Command |
|---|---|
| Create from a JSON spec (page size/margins, header/footer, "Page X of Y" footer, custom styles, headings, paragraphs with runs, bullet/numbered lists, tables, images, TOC, page breaks; format at the top of the script) | `python scripts/docx_create.py spec.json out.docx` |
| Full text / heading outline + table shapes / styles used / revisions and comments present | `python scripts/docx_read.py f.docx --text` · `--structure` · `--styles` · `--revisions` |
| Extract embedded images | `python scripts/docx_read.py f.docx --images outdir/` |
| Find/replace across body, nested tables, headers and footers, keeping run formatting | `python scripts/docx_edit.py replace f.docx --find A --replace B -o out.docx [--body-only]` |
| Merge adjacent runs with identical formatting | `python scripts/docx_edit.py normalize f.docx -o out.docx` |
| Set a table cell (resets that cell's formatting) | `python scripts/docx_edit.py set-cell f.docx --table 0 --row 1 --col 2 --text X` |
| Insert / delete / restyle paragraph N | `python scripts/docx_edit.py insert f.docx --index N --text X --style Normal` · `delete --index N` · `style --index N --style "Heading 1"` |
| TOC field before paragraph N / "Page X of Y" footer | `python scripts/docx_edit.py toc f.docx --index N -o out.docx` · `page-numbers f.docx` |
| Fill `{{tokens}}`; fail if any remain | `python scripts/docx_template.py tpl.docx values.json out.docx --strict` |
| List `<w:ins>`/`<w:del>` revisions (id, author, date, text) | `python scripts/docx_revisions.py list f.docx` |
| Accept or reject one revision, or all (see the rule below first) | `python scripts/docx_revisions.py accept f.docx --id 3 -o out.docx` · `reject --id 3` · `accept-all` · `reject-all` |
| Add a plain top-level comment anchored to the first occurrence of a phrase | `python scripts/docx_comments.py add f.docx --target "phrase" --text "note" --author "Name"` |
| List comments with their anchored text / delete one | `python scripts/docx_comments.py list f.docx` · `delete f.docx --id 0` |
| Quick package health check (zip, required parts, relationship targets, image bytes, referenced styles) | `python scripts/docx_validate.py f.docx` |

Which tool when both exist:

- **Adding comments:** `docx_comments.py add --target` places a plain top-level comment on a phrase in one step (it splits runs and inserts the markers itself). Use `scripts/comment.py` for replies (`--parent`), or when the comment must carry all six comment parts.
- **Deleting comments:** `docx_comments.py delete` removes the comment from `comments.xml` and its markers from the text only. It leaves the entries in `commentsExtended.xml`, `commentsIds.xml` and `commentsExtensible.xml` and does not delete replies, so a deleted comment that had replies leaves orphans behind. For comments written by `comment.py`, delete the replies too and remove the matching entries from those three files.
- **Accepting or rejecting changes:** first search `word/document.xml` for revisions on paragraph marks (`<w:pPr>` → `<w:rPr>` → `<w:ins>`/`<w:del>`), on table rows (`<w:trPr>` → `<w:ins>`/`<w:del>`), moves (`<w:moveFrom>`, `<w:moveTo>`) and format changes (`<w:rPrChange>`, `<w:pPrChange>`). If none are present, `docx_revisions.py` works without LibreOffice and can also handle a single revision. If any are present, do not use it: it strips paragraph-mark and row markers without joining the paragraphs or removing the rows, leaves moves and format changes untouched, and its `list` then reports nothing left. Accept such documents with `accept_changes.py`; reject them in Word.
- **Validation:** `scripts/office/validate.py` is the schema check and the only one that verifies tracked edits (`--author`). `docx_validate.py` is a quick structural check; a file can pass it and still contain XML Word rejects.
- **Merging fragmented runs:** before editing `word/document.xml` by hand, use `merge_runs.py` (it also strips rsid attributes and `<w:proofErr>` markers, and never merges across a revision). Before `docx_edit.py replace` or `docx_template.py` on headers and footers, use `docx_edit.py normalize`, which covers them but stops at markers such as `<w:proofErr>`.
- **Template tokens and find/replace** survive Word's run fragmentation: matched runs are collapsed and the replacement takes the first run's formatting.

Pitfalls:

- Field codes (TOC, page numbers) are computed by Word or LibreOffice when the file opens; placeholder text shows until then.
- A style must exist in the document before it is applied (`KeyError` otherwise). Built-ins such as `Heading 1`, `List Bullet`, `List Number` and `Table Grid` exist; declare custom styles in the create spec.
- Separate `List Number` lists in one document may continue numbering instead of restarting.

## Dependencies

`docx` (npm, preinstalled — install only if `require('docx')` fails) · `pandoc` · LibreOffice (`soffice`) · `pdftoppm` (Poppler) · Python 3.10+ with `defusedxml` and `lxml` for the scripts, plus `python-docx` for `scripts/docx_*.py`

## Sources

`scripts/docx_*.py`, `references/` and `tests/` come from [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) under the MIT License (`LICENSE-HERMES.txt`). The rest of this skill is covered by `LICENSE.txt`.
