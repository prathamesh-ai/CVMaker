---
name: compile-pdf
description: "Compiles LaTeX .tex files into PDF documents using Docker with TeX Live."
allowed_tools: [execute]
---

# Compile PDF

## Overview

This skill compiles the generated LaTeX resume into a PDF document using Docker container with TeX Live.

## Prerequisites

1. Docker installed and running
2. Docker image `resume-compiler-minimal` built from the provided Dockerfile
3. The following files in `output/` directory (auto-copied by generate-latex):
   - `resume.tex` - The LaTeX file to compile
   - `resume.cls` - The LaTeX class file

## Instructions

### Execute Tool (CRITICAL)

Run the tool via shell command:

```bash
python skills/active/compile-pdf/tools/main.py output/resume.tex output/resume.pdf
```

### Output

The final PDF will be written to: `output/resume.pdf`

## Notes

- Requires Docker image `resume-compiler-minimal`
- The Docker container mounts `output/` as `/data`
- LaTeX compilation runs twice for cross-references
- Check `output/resume.log` for any LaTeX warnings or errors