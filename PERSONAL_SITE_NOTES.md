# Personal Site Maintenance Notes

This file records stable maintenance preferences for the personal homepage so future edits stay consistent.

## Content Sync

- Keep the following in sync whenever there is a major update:
  - `_config.yml`
  - `index.md`
  - `_includes/education.md`
  - `_data/publications.yml`
  - `resume/cv.tex`
- Current Ph.D. status:
  - Emory University Ph.D. completed in March 2026.
  - Advisor: [Dr. Liang Zhao](http://cs.emory.edu/~lzhao41/index.htm)
  - Dissertation: [Benchmarking, Correcting, and Accelerating AI Reasoning across Diverse Modalities](https://etd.library.emory.edu/concern/etds/3197xn83d?locale=en)

## Homepage Style Preferences

- Prefer a clean, simple academic homepage style.
- Avoid adding rounded card / bubble / heavy panel effects to `News` and `Services`.
- For publication teaser images:
  - Keep the left white teaser area a uniform fixed size across entries.
  - Embed teaser images inside that white area.
  - Preserve the full image when possible; allow small margins rather than aggressive cropping.
  - Do not redesign teaser presentation without explicit confirmation.
- When adjusting visual layout, make small targeted changes instead of broad style shifts.

## Publications and News

- Keep `Selected publications and preprints` visually consistent with the existing site style.
- When adding new papers, match the existing data format in `_data/publications.yml`.
- For `News`, keep the default behavior lightweight:
  - recent items visible
  - older items can be collapsed, but styling should remain minimal

## CV / Resume Workflow

- Resume source lives in `resume/cv.tex`.
- Generated PDF must be written to `assets/files/resume_Yifei.pdf`.
- Preferred update flow:
  - edit `resume/cv.tex`
  - run `make resume` locally if needed
  - GitHub Actions also rebuilds the PDF automatically on push
- In the CV, the "full publication list" link should point to Google Scholar, not the homepage.

## Editing Boundary

- Safe to update directly:
  - dates
  - affiliations
  - advisor / dissertation info
  - publication metadata
  - CV content refreshes
- Ask before making bigger visual redesign choices, especially for:
  - publication teaser layout
  - section styling
  - homepage-wide aesthetic changes
