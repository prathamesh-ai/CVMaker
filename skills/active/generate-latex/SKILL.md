---
name: generate-latex
description: "Renders CV JSON data into LaTeX document using Jinja2 templates. Reads from output/cv_data.json (or cv_data_tailored.json if available) and generates resume.tex."
allowed_tools: [execute]
---

# Generate LaTeX

## Overview

This skill renders the CV JSON data into a professional LaTeX document using Jinja2 templating. It reads the JSON data and populates the resume.tex template.

## Instructions

### Step 1: Determine Input JSON

Check which JSON file exists:
- If `output/cv_data_tailored.json` exists, use it (JD tailoring was applied)
- Otherwise, use `output/cv_data.json` (raw CV data)

### Step 2: Execute Tool (CRITICAL)

Run the tool via shell command:

```bash
python skills/active/generate-latex/tools/main.py <json_path> <template_path> <output_path>
```

Example:
```bash
python skills/active/generate-latex/tools/main.py output/cv_data_tailored.json skills/active/generate-latex/templates/classic/resume.tex output/resume.tex
```

### Output

The populated .tex file will be written to: `output/resume.tex`

## Notes

- Uses Jinja2 with LaTeX-friendly delimiters (`{% %}` for blocks, `{{ }}` for variables)
- The resume.cls file (LaTeX class) should be in the same directory as resume.tex
- Template location: `skills/active/generate-latex/templates/classic/`
- Output always goes to: `output/resume.tex`