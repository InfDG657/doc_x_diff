# doc-x-diff Development Strategy

## Overview
A ttkbootstrap desktop application for editors and reviewers to compare two `.docx` files and produce a single output `.docx` that shows what was added (underlined) and what was removed (strikethrough) between the old and new versions.

## Target User
Non-technical editors and reviewers of letters and client documentation. The tool should be simple — drag in two files, get one file out.

---

## Dependencies
- `ttkbootstrap` — themed UI framework (built on tkinter)
- `python-docx` — reading `.docx` files and writing the output `.docx`
- `redlines` — word-by-word diff engine producing strikethrough/underline markup

---

## Architecture Pipeline

Two pipeline implementations exist. `main.py` can swap between them by changing the import.

### `pipeline.py` — Paragraph-by-paragraph diff
```
Old .docx ──┐
            ├── Extract paragraphs ──> SequenceMatcher (paragraph-level) ──> Redlines (word-level per pair) ──> Output .docx
New .docx ──┘
```

### `pipeline_flat.py` — Full-document flat diff
```
Old .docx ──┐
            ├── Join all paragraphs into one string ──> Redlines (word-level, full doc) ──> Split on separator ──> Output .docx
New .docx ──┘
```

#### Step 1: Document Extraction (`pipeline_flat.py`)
- Use `python-docx` to read both files
- Join all paragraphs into a single string using a paragraph separator constant
- Paragraph structure is preserved via the separator for later reconstruction

#### Step 2: Diff Computation
- Pass both full-document strings to `Redlines` for **word-level** comparison
- One diff over the entire document — no paragraph-level alignment step

#### Step 3: Output Generation
- Split the diff output on the paragraph separator to recover paragraph boundaries
- Write each chunk to a new paragraph in the output `.docx` via `DiffHTMLParser`
- Strikethrough+red for removals, underline+green for additions

---

## UI Design
- Built with `ttkbootstrap`
- Two drag-and-drop zones: one for the **old version**, one for the **new version**
- Single "Compare" button
- Progress bar to indicate processing time
- Output `.docx` saved to a user-chosen location
- No color coding in v1 — strikethrough and underline only

---

## Decisions Log
| Decision | Choice | Reason |
|---|---|---|
| Output format | `.docx` | Editors live in Word; HTML feels out of place |
| Diff granularity | Word-by-word | Catches every change; paragraph-level buries small edits |
| Text extraction | Paragraph-by-paragraph | Preserves document structure in output |
| Color coding | Deferred | Core functionality first; QoL features later |
| UI complexity | Minimal launcher | Non-technical audience; two inputs, one output |

---

## Development Notes
- Running in a UV environment
- Follow the Development Loop: ~200-300 lines per section
- Triggers: `CLARIFY:`, `CODE:`, `EDIT:`, `REVIEW:`
- Never provide implementation-level detail in assignments — describe what to build, not how
