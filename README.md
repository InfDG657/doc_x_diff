# doc-x-diff

A desktop app for comparing two `.docx` files and producing a single output document showing what changed — removals in strikethrough, additions underlined.

Built for non-technical editors and reviewers: drag in two files, get one file out.

## What it does

- Compares an old and new version of a `.docx` file word-by-word
- Outputs a new `.docx` with removals marked in strikethrough and additions marked with underline
- Simple two-file drag-and-drop UI

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

```bash
git clone https://github.com/InfDG657/doc_x_diff.git
cd doc_x_diff
uv sync
```

## Running

```bash
uv run python main.py
```

## Dependencies

- `ttkbootstrap` — UI framework
- `python-docx` — reading and writing `.docx` files
- `redlines` — word-by-word diff engine
- `tkinterdnd2` — drag-and-drop support
