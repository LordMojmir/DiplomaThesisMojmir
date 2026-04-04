# Thesis — Leveraging AI to Optimize ERP System Decision Making

**Author:** Mojmír Horváth  
**Institution:** HTL Spengergasse

## Prerequisites

- A LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
- `biber` bibliography processor (included with most modern TeX distributions)

## Build

Run the following commands in order from the project root:

```bash
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
```

Two extra `pdflatex` passes are required to resolve cross-references and the table of contents.

## Output

The compiled thesis is written to `main.pdf`.

## Source Files

| File | Purpose |
|------|---------|
| `main.tex` | Root document — structure and all sections |
| `common.tex` | Shared preamble (packages, page geometry) |
| `bg-waves.tex` | Title page with animated wave graphic (TikZ) |
| `references.bib` | BibLaTeX bibliography (biblatex-chicago, biber backend) |
