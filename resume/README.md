# Resume Source

This directory stores the LaTeX source for the homepage CV.

The CV uses the official [moderncv](https://github.com/moderncv/moderncv)
Banking style (LPPL 1.3c). Publication entries use full-width titles, plain
author lines, and full venue names. Findings is a suffix on the full venue
name, not part of the conference acronym. Keep workshop names abbreviated.
Sections flow continuously across pages; avoid forced page breaks that leave
large blank areas. Keep each publication together when pagination permits.

## Local build

From the repository root:

```bash
make resume
```

This compiles `resume/cv.tex` and writes the generated PDF to:

`assets/files/resume_Yifei.pdf`

## Automatic build

GitHub Actions also rebuilds the PDF whenever files under `resume/` change.
