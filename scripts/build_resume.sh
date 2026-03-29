#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/resume"
BUILD_DIR="$ROOT_DIR/.tmp/resume-build"
OUTPUT_DIR="$ROOT_DIR/assets/files"
OUTPUT_PDF="$OUTPUT_DIR/resume_Yifei.pdf"

mkdir -p "$BUILD_DIR" "$OUTPUT_DIR"

if command -v latexmk >/dev/null 2>&1; then
  latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error \
    -output-directory="$BUILD_DIR" "$SOURCE_DIR/cv.tex"
elif command -v tectonic >/dev/null 2>&1; then
  tectonic --outdir "$BUILD_DIR" "$SOURCE_DIR/cv.tex"
else
  echo "No LaTeX build tool found. Install latexmk or tectonic first." >&2
  exit 1
fi

cp "$BUILD_DIR/cv.pdf" "$OUTPUT_PDF"
echo "Built $OUTPUT_PDF"
