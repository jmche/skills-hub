# Revisions and Comments — XML details

Deep reference for `docx_revisions.py` and `docx_comments.py`. Read this
when you need to reason about the raw WordprocessingML, extend the
scripts, or debug an unusual document. Everyday use only needs SKILL.md.

## Tracked changes (w:ins / w:del)

Word records run-level tracked changes as wrapper elements inside a
paragraph (`w:p`), in the `w` namespace
`http://schemas.openxmlformats.org/wordprocessingml/2006/main`:

```xml
<w:p>
  <w:r><w:t>Base </w:t></w:r>
  <w:ins w:id="1" w:author="Editor" w:date="2026-01-02T03:04:05Z">
    <w:r><w:t>inserted text</w:t></w:r>
  </w:ins>
  <w:del w:id="2" w:author="Editor" w:date="2026-01-02T03:04:05Z">
    <w:r><w:delText>deleted text</w:delText></w:r>
  </w:del>
</w:p>
```

Key facts the script relies on:

- Deleted text lives in `w:delText`, not `w:t` — that is why plain text
  extraction naturally shows the "accepted" view (insertions visible,
  deletions hidden).
- Resolution semantics:
  - accept `w:ins` → unwrap (move child runs up, drop the wrapper)
  - reject `w:ins` → remove the wrapper and its contents
  - accept `w:del` → remove the wrapper and its contents
  - reject `w:del` → rename each `w:delText` to `w:t`, then unwrap
- Revisions can appear anywhere block content is allowed: body, table
  cells (nested tables too), headers, footers, text boxes. The script
  iterates the body root plus every header/footer part root with
  `root.iter(W+"ins", W+"del")`, which finds them at any depth.
- `w:id` values are unique per revision *element*, but one logical edit
  session may produce several elements. `accept`/`reject --id` acts on
  exactly the element(s) carrying that id.

Not handled correctly by the script:

- Paragraph-mark revisions (`w:pPr/w:rPr/w:ins|w:del`) and table-row
  revisions (`w:trPr/w:ins|w:del`) are matched by the same
  `root.iter(...)` and resolved as if they were run wrappers: the marker
  is removed, but the paragraphs are not joined and the row is not
  inserted or removed. Afterwards `list` reports nothing left.
- Format-change records (`w:rPrChange`, `w:pPrChange`) and moves
  (`w:moveFrom`/`w:moveTo`) are left untouched and are not reported by
  `list`. `docx_read.py --revisions` returns only yes/no flags for
  insertions, deletions, format changes and comments; it does not
  detect moves.

When any of these are present, accept with `scripts/accept_changes.py`
(LibreOffice) or resolve the document in Word.

## Comments

Three cooperating pieces:

1. **`word/comments.xml`** — one `w:comment` element per comment,
   carrying `w:id`, `w:author`, `w:initials`, `w:date`, and body
   paragraphs. Related from document.xml via the relationship type
   `.../comments` and content type
   `application/vnd...wordprocessingml.comments+xml` (also needs a
   `[Content_Types].xml` override — python-docx's part machinery adds it
   when the part is registered).
2. **Range markers in the story** — `w:commentRangeStart w:id="N"`
   before the anchored runs, `w:commentRangeEnd w:id="N"` after them.
3. **The reference run** — a `w:r` containing `w:commentReference
   w:id="N"`, placed right after the range end; it ties the balloon to
   the location.

`docx_comments.py` behavior:

- **list / delete** always work at the XML level, so they handle files
  from any producer. `anchored_text` is reconstructed by walking each
  part root in document order and collecting `w:t` text between the
  start and end markers for each id.
- **add** first isolates the target text into whole runs. If the match
  starts or ends mid-run, the run is split at the boundary (the split
  copies `w:rPr`, so formatting is preserved). Then:
  - python-docx >= 1.2: the native `document.add_comment(runs, ...)`
    API is used (it creates the comments part, markers, and reference
    run itself).
  - older versions or `--xml`: the script builds `word/comments.xml`,
    registers the part + relationship through the opc layer, and
    inserts the markers/reference manually.
- Deleting a comment removes the `w:comment` element and all three
  marker kinds for that id; the anchored document text is untouched.

Modern Word also writes `commentsExtended.xml` (threading/resolved
state). `docx_comments.py` neither reads nor produces it: replies and
"resolved" flags are invisible to it, and comments it adds are plain
top-level comments. `scripts/comment.py` writes `commentsExtended.xml`
and can add replies (`--parent`).
