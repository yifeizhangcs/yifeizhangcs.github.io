# Resume Source

This directory stores the LaTeX source for the homepage CV.

## Local build

From the repository root:

```bash
make resume
```

This compiles `resume/cv.tex` and writes the generated PDF to:

`assets/files/resume_Yifei.pdf`

## Automatic build

GitHub Actions also rebuilds the PDF whenever files under `resume/` change.
